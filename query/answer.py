"""Full RAG flow: retrieve chunks, build prompt, get answer, attach citations."""
from query.retriever import retrieve
from query.prompt import build_prompt
from query.llm import ask_ollama


def ask(question: str, subject: str = None, n_results: int = 5) -> dict:
    """
    Runs the full pipeline and returns both the answer and its sources.
    Returns: {"answer": str, "sources": list[dict]}
    """
    chunks = retrieve(question, n_results=n_results, subject=subject)

    if not chunks:
        return {
            "answer": "I don't have that in your notes.",
            "sources": [],
        }

    prompt = build_prompt(question, chunks)
    answer = ask_ollama(prompt)

    # dedupe sources by (file, page) - multiple chunks can come from the same page
    seen = set()
    sources = []
    for c in chunks:
        key = (c["source_file"], c["page"])
        if key not in seen:
            seen.add(key)
            sources.append({"file": c["source_file"], "page": c["page"], "subject": c["subject"]})

    return {"answer": answer, "sources": sources}


def format_answer(result: dict) -> str:
    """Pretty-prints an answer with its sources for CLI display."""
    lines = [result["answer"], ""]
    if result["sources"]:
        lines.append("Sources:")
        for s in result["sources"]:
            page_info = f", p{s['page']}" if s["page"] else ""
            lines.append(f"  - {s['subject']}/{s['file']}{page_info}")
    return "\n".join(lines)


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print('usage: python -m query.answer "<question>" [subject]')
        sys.exit(1)

    question = sys.argv[1]
    subject = sys.argv[2] if len(sys.argv) > 2 else None

    result = ask(question, subject=subject)
    print(format_answer(result))