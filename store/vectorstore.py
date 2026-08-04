"""Persistent local vector store using ChromaDB."""
import json
import chromadb

_client = None
_collection = None

DB_PATH = "chroma_db"
COLLECTION_NAME = "notes"


def get_collection():
    """Lazy-load a persistent Chroma client + collection, reuse across calls."""
    global _client, _collection
    if _collection is None:
        _client = chromadb.PersistentClient(path=DB_PATH)
        _collection = _client.get_or_create_collection(name=COLLECTION_NAME)
    return _collection


def store_chunks(embedded_chunks_path: str = "data/embedded_chunks.json"):
    """
    Loads embedded chunks (text + vector + metadata) and upserts them
    into the Chroma collection. Uses upsert so re-running is safe —
    existing ids get overwritten, not duplicated.
    """
    with open(embedded_chunks_path, "r", encoding="utf-8") as f:
        chunks = json.load(f)

    collection = get_collection()

    ids = [f"chunk_{i}" for i in range(len(chunks))]
    embeddings = [c["embedding"] for c in chunks]
    documents = [c["text"] for c in chunks]
    metadatas = [
        {
            "subject": c["subject"],
            "source_file": c["source_file"],
            "page": c["page"] if c["page"] is not None else -1,  # Chroma disallows None
        }
        for c in chunks
    ]

    collection.upsert(
        ids=ids,
        embeddings=embeddings,
        documents=documents,
        metadatas=metadatas,
    )

    print(f"Stored {len(chunks)} chunks in Chroma collection '{COLLECTION_NAME}'")
    print(f"Collection now has {collection.count()} total items")


if __name__ == "__main__":
    import sys
    path = sys.argv[1] if len(sys.argv) > 1 else "data/embedded_chunks.json"
    store_chunks(path)