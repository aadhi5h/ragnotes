"""Extract raw text from PDF files."""
from pathlib import Path
from pypdf import PdfReader


def extract_pdf_text(path: str) -> list[dict]:
    """
    Returns a list of {"page": int, "text": str} for each page.
    Empty/near-empty pages (likely scanned images) are flagged, not dropped.
    """
    if not Path(path).exists():
        raise FileNotFoundError(f"No such file: {path}")

    try:
        reader = PdfReader(path)
    except Exception as e:
        raise RuntimeError(f"Could not open PDF '{path}': {e}")

    pages = []
    for i, page in enumerate(reader.pages, start=1):
        try:
            text = page.extract_text() or ""
        except Exception as e:
            print(f"[warn] failed to extract page {i}: {e}")
            text = ""
        pages.append({
            "page": i,
            "text": text.strip(),
            "likely_scanned": len(text.strip()) < 20,
        })
    return pages


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("usage: python pdf_extract.py <path_to_pdf>")
        sys.exit(1)

    result = extract_pdf_text(sys.argv[1])
    for p in result:
        flag = " [LIKELY SCANNED - no text found]" if p["likely_scanned"] else ""
        print(f"--- page {p['page']}{flag} ---")
        print(p["text"][:200])
        print()