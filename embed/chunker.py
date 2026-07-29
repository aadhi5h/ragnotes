"""Split text into overlapping fixed-size chunks."""


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50, min_chunk_size: int = 100) -> list[str]:
    """
    Splits text into chunks of `chunk_size` characters, with `overlap`
    characters repeated between consecutive chunks so context isn't lost
    at chunk boundaries. Trailing chunks smaller than `min_chunk_size`
    get merged into the previous chunk instead of staying tiny/useless.
    """
    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive")
    if overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size")

    text = " ".join(text.split())  # collapse repeated whitespace/newlines
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

    # merge a too-small trailing chunk into the previous one
    if len(chunks) > 1 and len(chunks[-1]) < min_chunk_size:
        chunks[-2] = chunks[-2] + " " + chunks[-1]
        chunks.pop()

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