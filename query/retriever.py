"""Retrieve the most relevant chunks for a given question."""
from store.vectorstore import query_collection


def retrieve(question: str, n_results: int = 5, subject: str = None) -> list[dict]:
    """
    Returns a list of relevant chunks for the question, each as:
    {"text": ..., "subject": ..., "source_file": ..., "page": ..., "distance": ...}
    Sorted by relevance (best match first) — this is Chroma's default order.
    """
    results = query_collection(question, n_results=n_results, subject=subject)

    if not results["documents"] or not results["documents"][0]:
        return []

    retrieved = []
    for doc, meta, dist in zip(
        results["documents"][0], results["metadatas"][0], results["distances"][0]
    ):
        retrieved.append({
            "text": doc,
            "subject": meta["subject"],
            "source_file": meta["source_file"],
            "page": meta["page"] if meta["page"] != -1 else None,
            "distance": round(dist, 3),
        })

    return retrieved


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print('usage: python -m query.retriever "<question>" [subject]')
        sys.exit(1)

    question = sys.argv[1]
    subject = sys.argv[2] if len(sys.argv) > 2 else None

    results = retrieve(question, subject=subject)

    if not results:
        print("No relevant chunks found.")
    else:
        for i, r in enumerate(results, start=1):
            page_info = f"p{r['page']}" if r['page'] else "N/A"
            print(f"--- match {i} | {r['subject']} | {r['source_file']} {page_info} | dist={r['distance']} ---")
            print(r["text"][:200])
            print()