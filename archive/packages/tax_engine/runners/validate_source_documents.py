import argparse
import json
import sys
from pathlib import Path

from packages.tax_engine.runners.output import write_text_output
from packages.tax_engine.source_document_drafts import load_source_document_draft_payload, normalize_source_document_draft
from packages.tax_engine.source_documents import load_source_document, source_document_from_payload, validate_source_document_payload
from packages.tax_engine.source_validation import build_source_validation_report, render_source_validation_report_markdown


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Validate source document drafts or canonical source documents.")
    parser.add_argument("--draft", action="append", dest="drafts", default=[], help="Path to a draft JSON file. May be supplied multiple times.")
    parser.add_argument("--source-document", action="append", dest="source_documents", default=[], help="Path to a canonical source document JSON file. May be supplied multiple times.")
    parser.add_argument("--output", help="Optional output path. If omitted, output is written to stdout.")
    parser.add_argument("--format", choices=["json", "markdown"], default="json", help="Output format.")
    parser.add_argument("--compact", action="store_true", help="Write compact JSON instead of pretty-printed JSON.")
    return parser


def load_documents(draft_paths: list[Path], source_document_paths: list[Path]):
    documents = []
    for draft_path in draft_paths:
        draft_payload = load_source_document_draft_payload(draft_path)
        source_document_payload = normalize_source_document_draft(draft_payload)
        validate_source_document_payload(source_document_payload)
        documents.append(source_document_from_payload(source_document_payload))
    for source_document_path in source_document_paths:
        documents.append(load_source_document(source_document_path))
    return documents


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if not args.drafts and not args.source_documents:
        build_parser().error("at least one --draft or --source-document is required")

    report = build_source_validation_report(
        load_documents(
            [Path(path) for path in args.drafts],
            [Path(path) for path in args.source_documents],
        )
    )
    if args.format == "markdown":
        rendered = render_source_validation_report_markdown(report)
    else:
        rendered = json.dumps(report, separators=(",", ":") if args.compact else None, indent=None if args.compact else 2)
        rendered += "\n"

    if args.output:
        write_text_output(Path(args.output), rendered)
    else:
        sys.stdout.write(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
