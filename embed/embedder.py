"""Embed text chunks into vectors using all-MiniLM-L6-v2."""
import json
from pathlib import Path
from sentence_transformers import SentenceTransformer

_model = None


def get_model():
    """Lazy-load the model once, reuse across calls (loading it is slow)."""
    global _model
    if _model is None:
        print("Loading embedding model (first time only, may take a moment)...")
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model


def embed_texts(texts: list[str], batch_size: int = 64) -> list[list[float]]:
    """Takes a list of strings, returns a list of embedding vectors."""
    model = get_model()
    embeddings = model.encode(texts, batch_size=batch_size, show_progress_bar=True)
    return embeddings.tolist()


def embed_chunks_file(chunks_path: str, output_path: str = "data/embedded_chunks.json") -> list[dict]:
    """
    Reads chunks.json, embeds every chunk, saves chunk + vector together.
    Skips chunks that already have an embedding if output_path exists,
    so re-runs after adding new notes don't re-embed everything.
    """
    with open(chunks_path, "r", encoding="utf-8") as f:
        chunks = json.load(f)

    existing = {}
    if Path(output_path).exists():
        with open(output_path, "r", encoding="utf-8") as f:
            for c in json.load(f):
                existing[c["text"]] = c

    to_embed = [c for c in chunks if c["text"] not in existing]
    print(f"{len(chunks)} total chunks, {len(existing)} already embedded, {len(to_embed)} new")

    if to_embed:
        vectors = embed_texts([c["text"] for c in to_embed])
        for c, v in zip(to_embed, vectors):
            c["embedding"] = v

    result = list(existing.values()) + to_embed

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False)

    print(f"Saved {len(result)} embedded chunks to {output_path}")
    return result


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("usage: python -m embed.embedder <path_to_chunks.json>")
        sys.exit(1)

    embed_chunks_file(sys.argv[1])