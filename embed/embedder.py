"""Embed text chunks into vectors using all-MiniLM-L6-v2."""
from sentence_transformers import SentenceTransformer

_model = None


def get_model():
    """Lazy-load the model once, reuse across calls (loading it is slow)."""
    global _model
    if _model is None:
        print("Loading embedding model (first time only, may take a moment)...")
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model


def embed_texts(texts: list[str]) -> list[list[float]]:
    """Takes a list of strings, returns a list of embedding vectors."""
    model = get_model()
    embeddings = model.encode(texts, show_progress_bar=True)
    return embeddings.tolist()


if __name__ == "__main__":
    import json
    import sys

    if len(sys.argv) != 2:
        print("usage: python -m embed.embedder <path_to_chunks.json>")
        sys.exit(1)

    with open(sys.argv[1], "r", encoding="utf-8") as f:
        chunks = json.load(f)

    texts = [c["text"] for c in chunks]
    print(f"Embedding {len(texts)} chunks...")
    vectors = embed_texts(texts)

    print(f"\nDone. {len(vectors)} vectors, dimension {len(vectors[0])}")
    print(f"First vector (first 5 dims): {vectors[0][:5]}")