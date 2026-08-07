# NotesRAG

Offline RAG tool for class notes. Dump PDFs/docs from Networks, Crypto, BDA, Tableau — ask questions, get answers with source citations, no internet needed after setup.

## Pipeline
```
ingest/  → extract text from PDFs/docs/txt
embed/   → chunk + embed text (all-MiniLM-L6-v2)
store/   → persist vectors in ChromaDB
query/   → retrieve relevant chunks, ask local LLM (Ollama)
cli/     → command-line interface
```

## Setup
```bash
python -m venv venv
source venv/bin/activate       # Windows: venv\Scripts\activate
pip install -r requirements.txt
```
## Chunking decisions
- Chunk size: 500 chars, overlap: 50 chars — balances context preservation vs. embedding focus.
- Whitespace collapsed before chunking (PDF extraction leaves ragged line breaks).
- Trailing chunks under 100 chars get merged into the previous chunk instead of staying as noise.

## Embed → Store flow

1. `python -m embed.embedder data/chunks.json` — embeds chunks with `all-MiniLM-L6-v2` (384-dim vectors), caches to `data/embedded_chunks.json`. Skips chunks already embedded (matched by text) so re-runs after adding notes only embed what's new.
2. `python -m store.vectorstore` — upserts embedded chunks into a persistent local ChromaDB collection (`chroma_db/`, gitignored). Upsert is safe to re-run — same ids get overwritten, not duplicated.
3. `python -m ingest.update notes/` — runs ingest → embed → store in one command. This is the one to run after adding new files to `notes/`.

**Known limitation:** some PDF pages (slide-deck exports with mostly diagrams/images, low embedded text) get skipped during ingestion — flagged as "likely scanned" if under 20 chars of extractable text. Currently ~26 pages across the dataset are skipped this way. OCR is a possible future fix if this content turns out to matter for retrieval.