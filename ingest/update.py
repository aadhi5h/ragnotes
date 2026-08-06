"""One command to re-ingest, re-embed, and re-store notes after adding new files."""
import sys

from ingest.batch import batch_ingest
from embed.embedder import embed_chunks_file
from store.vectorstore import store_chunks


def update_all(notes_dir: str = "notes"):
    print("=== Step 1: Ingesting notes ===")
    batch_ingest(notes_dir)

    print("\n=== Step 2: Embedding (new chunks only) ===")
    embed_chunks_file("data/chunks.json")

    print("\n=== Step 3: Storing in Chroma ===")
    store_chunks("data/embedded_chunks.json")

    print("\nDone. Run a query to confirm new notes are searchable.")


if __name__ == "__main__":
    notes_dir = sys.argv[1] if len(sys.argv) > 1 else "notes"
    update_all(notes_dir)