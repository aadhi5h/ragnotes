"""Extract raw text from .docx and .txt files."""
from pathlib import Path
from docx import Document


def extract_docx_text(path: str) -> str:
    """Returns full document text, paragraphs joined by newline."""
    if not Path(path).exists():
        raise FileNotFoundError(f"No such file: {path}")

    try:
        doc = Document(path)
    except Exception as e:
        raise RuntimeError(f"Could not open docx '{path}': {e}")

    paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
    return "\n".join(paragraphs)


def extract_txt_text(path: str) -> str:
    """Returns raw text file contents."""
    if not Path(path).exists():
        raise FileNotFoundError(f"No such file: {path}")
    return Path(path).read_text(encoding="utf-8", errors="ignore")


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("usage: python docx_extract.py <path_to_file>")
        sys.exit(1)

    path = sys.argv[1]
    if path.endswith(".docx"):
        print(extract_docx_text(path)[:500])
    elif path.endswith(".txt"):
        print(extract_txt_text(path)[:500])
    else:
        print("unsupported file type")