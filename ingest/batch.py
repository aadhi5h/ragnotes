"""Walk a notes folder, ingest every supported file, save combined chunks to JSON."""
import json
import sys
from pathlib import Path

from ingest.pipeline import ingest_file

SUPPORTED = {".pdf", ".docx", ".txt"}


def batch_ingest(notes_dir: str, output_path: str = "data/chunks.json") -> list[dict]:
    """
    Expects notes_dir structured like:
        notes_dir/networks/*.pdf
        notes_dir/crypto/*.pdf
        notes_dir/bda/*.pdf
    Subfolder name becomes the subject tag automatically.
    """
    notes_dir = Path(notes_dir)
    if not notes_dir.exists():
        raise FileNotFoundError(f"No such folder: {notes_dir}")

    all_chunks = []
    failed = []

    for subject_dir in sorted(p for p in notes_dir.iterdir() if p.is_dir()):
        subject = subject_dir.name
        files = [f for f in subject_dir.iterdir() if f.suffix.lower() in SUPPORTED]

        for f in files:
            print(f"Ingesting [{subject}] {f.name} ...")
            try:
                chunks = ingest_file(str(f), subject)
                all_chunks.extend(chunks)
                print(f"  -> {len(chunks)} chunks")
            except Exception as e:
                print(f"  -> FAILED: {e}")
                failed.append((str(f), str(e)))

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as out:
        json.dump(all_chunks, out, ensure_ascii=False, indent=2)

    print(f"\nTotal chunks: {len(all_chunks)}")
    print(f"Saved to: {output_path}")
    if failed:
        print(f"\n{len(failed)} file(s) failed:")
        for path, err in failed:
            print(f"  - {path}: {err}")

    return all_chunks


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: python -m ingest.batch <notes_folder>")
        sys.exit(1)

    batch_ingest(sys.argv[1])