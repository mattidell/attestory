import argparse
import json
import sys
from pathlib import Path

from packages.tax_engine.source_document_drafts import (
    load_source_document_draft_payload,
    normalize_source_document_draft,
)
from packages.tax_engine.runners.output import write_text_output
from packages.tax_engine.source_documents import validate_source_document_payload


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Normalize an editable source document draft.")
    parser.add_argument("--draft", required=True, help="Path to a source document draft JSON file.")
    parser.add_argument("--output", help="Optional output path. If omitted, source document JSON is written to stdout.")
    parser.add_argument("--compact", action="store_true", help="Write compact JSON instead of pretty-printed JSON.")
    return parser


def run(draft_path: Path) -> dict:
    draft_payload = load_source_document_draft_payload(draft_path)
    source_document = normalize_source_document_draft(draft_payload)
    validate_source_document_payload(source_document)
    return source_document


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    source_document = run(Path(args.draft))
    rendered = json.dumps(source_document, separators=(",", ":") if args.compact else None, indent=None if args.compact else 2)
    rendered += "\n"

    if args.output:
        write_text_output(Path(args.output), rendered)
    else:
        sys.stdout.write(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
