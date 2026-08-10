"""Build a RAG prompt from retrieved chunks + a question."""

TEMPLATE = """You are a study assistant. Answer the question using ONLY the context below.
If the context doesn't contain the answer, say "I don't have that in your notes" — do not guess.

Context:
{context}

Question: {question}

Answer:"""


def build_prompt(question: str, chunks: list[dict]) -> str:
    """Formats retrieved chunks + question into a single prompt string."""
    context_parts = []
    for c in chunks:
        page_info = f", p{c['page']}" if c.get("page") else ""
        context_parts.append(f"[{c['source_file']}{page_info}]\n{c['text']}")

    context = "\n\n".join(context_parts)
    return TEMPLATE.format(context=context, question=question)