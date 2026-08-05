"""Split text into overlapping fixed-size chunks, with metadata per chunk."""
from pathlib import Path


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50, min_chunk_size: int = 100) -> list[str]:
    """Splits text into overlapping chunks. Pure text in, list of strings out."""
    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive")
    if overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size")

    text = " ".join(text.split())
    if not text:
        return []

    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        start += chunk_size - overlap

    if len(chunks) > 1 and len(chunks[-1]) < min_chunk_size:
        chunks[-2] = chunks[-2] + " " + chunks[-1]
        chunks.pop()

    return chunks


def dedupe_chunks(chunks: list[dict], similarity_threshold: float = 0.95) -> list[dict]:
    """
    Removes chunks whose text is near-identical to a previous chunk.
    Uses simple normalized text comparison (cheap, no embedding needed) —
    catches exact/near-exact duplicates from chunk overlap, not semantic dupes.
    """
    seen = []
    deduped = []

    for chunk in chunks:
        normalized = " ".join(chunk["text"].lower().split())
        is_dupe = False
        for prev in seen:
            overlap = len(set(normalized.split()) & set(prev.split()))
            union = len(set(normalized.split()) | set(prev.split()))
            if union > 0 and overlap / union > similarity_threshold:
                is_dupe = True
                break
        if not is_dupe:
            seen.append(normalized)
            deduped.append(chunk)

    removed = len(chunks) - len(deduped)
    if removed:
        print(f"Deduped {removed} near-identical chunk(s)")
    return deduped

def chunk_pages_with_metadata(pages: list[dict], source_file: str, subject: str,
                                chunk_size: int = 500, overlap: int = 50) -> list[dict]:
    """
    Takes pypdf-style page dicts ({"page": int, "text": str}), chunks each
    page's text, and attaches metadata to every chunk.
    """
    filename = Path(source_file).name
    tagged_chunks = []

    for page in pages:
        page_chunks = chunk_text(page["text"], chunk_size, overlap)
        for chunk in page_chunks:
            tagged_chunks.append({
                "text": chunk,
                "source_file": filename,
                "page": page["page"],
                "subject": subject,
            })

    return dedupe_chunks(tagged_chunks)

if __name__ == "__main__":
    import sys
    sys.path.append(".")
    from ingest.pdf_extract import extract_pdf_text

    if len(sys.argv) != 3:
        print("usage: python -m embed.chunker <path_to_pdf> <subject>")
        sys.exit(1)

    path, subject = sys.argv[1], sys.argv[2]
    pages = extract_pdf_text(path)
    tagged = chunk_pages_with_metadata(pages, path, subject)

    print(f"Total chunks: {len(tagged)}\n")
    for i, c in enumerate(tagged, start=1):
        print(f"--- chunk {i} | {c['subject']} | {c['source_file']} p{c['page']} ---")
        print(c["text"][:150])
        print()