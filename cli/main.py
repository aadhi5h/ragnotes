"""notesrag CLI entrypoint."""
import argparse
import sys

from ingest.update import update_all
from query.answer import ask, format_answer


def main():
    parser = argparse.ArgumentParser(prog="notesrag", description="Offline RAG tool for class notes")
    subparsers = parser.add_subparsers(dest="command", required=True)

    ingest_parser = subparsers.add_parser("ingest", help="Ingest and index notes from a folder")
    ingest_parser.add_argument("folder", nargs="?", default="notes", help="Folder containing subject subfolders (default: notes)")

    ask_parser = subparsers.add_parser("ask", help="Ask a question about your notes")
    ask_parser.add_argument("question", help="The question to ask")
    ask_parser.add_argument("--subject", default=None, help="Filter to a specific subject")

    args = parser.parse_args()

    if args.command == "ingest":
        update_all(args.folder)
    elif args.command == "ask":
        try:
            result = ask(args.question, subject=args.subject)
            print(format_answer(result))
        except RuntimeError as e:
            print(f"Error: {e}")
            sys.exit(1)


if __name__ == "__main__":
    main()