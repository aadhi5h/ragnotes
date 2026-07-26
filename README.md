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

## Status
🚧 Day 1 — project scaffolded, ingestion not yet built.

## Setup
```bash
python -m venv venv
source venv/bin/activate       # Windows: venv\Scripts\activate
pip install -r requirements.txt
```
