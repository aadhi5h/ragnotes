"""Split text into overlapping fixed-size chunks."""


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> list[str]:
    """
    Splits text into chunks of `chunk_size` characters, with `overlap`
    characters repeated between consecutive chunks so context isn't lost
    at chunk boundaries.
    """
    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive")
    if overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size")

    text = text.strip()
    if not text:
        return []

    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        start += chunk_size - overlap  # step forward, minus the overlap

    return chunks


if __name__ == "__main__":
    import sys
    sys.path.append(".")
    from ingest.pdf_extract import extract_pdf_text

    if len(sys.argv) != 2:
        print("usage: python -m embed.chunker <path_to_pdf>")
        sys.exit(1)

    pages = extract_pdf_text(sys.argv[1])
    full_text = "\n".join(p["text"] for p in pages)
    chunks = chunk_text(full_text)

    print(f"Total chunks: {len(chunks)}\n")
    for i, c in enumerate(chunks, start=1):
        print(f"--- chunk {i} ({len(c)} chars) ---")
        print(c[:150])
        print()