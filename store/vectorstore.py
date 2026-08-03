"""Persistent local vector store using ChromaDB."""
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


if __name__ == "__main__":
    collection = get_collection()
    print(f"Collection '{COLLECTION_NAME}' ready at {DB_PATH}/")
    print(f"Current item count: {collection.count()}")