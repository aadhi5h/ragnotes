"""notesrag CLI entrypoint."""
import argparse
import sys

from ingest.update import update_all
from query.answer import ask, format_answer


def run_interactive(subject: str = None):
    """Loop taking questions until the user quits."""
    print("notesrag interactive mode. Type 'quit' or 'exit' to stop.\n")
    while True:
        try:
            question = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting.")
            break

        if question.lower() in ("quit", "exit"):
            print("Exiting.")
            break
        if not question:
            continue

        try:
            result = ask(question, subject=subject)
            print(format_answer(result))
            print()
        except RuntimeError as e:
            print(f"Error: {e}\n")


def main():
    parser = argparse.ArgumentParser(prog="notesrag", description="Offline RAG tool for class notes")
    subparsers = parser.add_subparsers(dest="command", required=True)

    ingest_parser = subparsers.add_parser("ingest", help="Ingest and index notes from a folder")
    ingest_parser.add_argument("folder", nargs="?", default="notes", help="Folder containing subject subfolders (default: notes)")

    ask_parser = subparsers.add_parser("ask", help="Ask a question about your notes")
    ask_parser.add_argument("question", help="The question to ask")
    ask_parser.add_argument("--subject", default=None, help="Filter to a specific subject")

    interactive_parser = subparsers.add_parser("chat", help="Interactive question loop")
    interactive_parser.add_argument("--subject", default=None, help="Filter to a specific subject")

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
    elif args.command == "chat":
        run_interactive(subject=args.subject)


if __name__ == "__main__":
    main()