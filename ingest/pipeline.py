"""Single entrypoint: any supported file in, tagged chunks out."""
from pathlib import Path

from ingest.pdf_extract import extract_pdf_text
from ingest.docx_extract import extract_docx_text, extract_txt_text
from embed.chunker import chunk_text, chunk_pages_with_metadata


def ingest_file(path: str, subject: str) -> list[dict]:
    """
    Reads a pdf/docx/txt file, extracts text, chunks it, and returns
    a list of tagged chunk dicts ready for embedding.
    Scanned/unreadable pages are skipped with a warning, not silently dropped.
    """
    ext = Path(path).suffix.lower()

    if ext == ".pdf":
        pages = extract_pdf_text(path)
        skipped = [p["page"] for p in pages if p["likely_scanned"]]
        if skipped:
            print(f"[warn] {Path(path).name}: pages {skipped} look scanned/empty, skipping them")
        usable_pages = [p for p in pages if not p["likely_scanned"]]
        return chunk_pages_with_metadata(usable_pages, path, subject)

    elif ext == ".docx":
        text = extract_docx_text(path)
        if not text.strip():
            print(f"[warn] {Path(path).name}: no extractable text found")
            return []
        chunks = chunk_text(text)
        return [
            {"text": c, "source_file": Path(path).name, "page": None, "subject": subject}
            for c in chunks
        ]

    elif ext == ".txt":
        text = extract_txt_text(path)
        chunks = chunk_text(text)
        return [
            {"text": c, "source_file": Path(path).name, "page": None, "subject": subject}
            for c in chunks
        ]

    else:
        raise ValueError(f"Unsupported file type: {ext}")


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("usage: python -m ingest.pipeline <path> <subject>")
        sys.exit(1)

    path, subject = sys.argv[1], sys.argv[2]
    result = ingest_file(path, subject)

    print(f"Total usable chunks: {len(result)}\n")
    for i, c in enumerate(result, start=1):
        page_info = f"p{c['page']}" if c['page'] else "N/A"
        print(f"--- chunk {i} | {c['subject']} | {c['source_file']} {page_info} ---")
        print(c["text"][:150])
        print()