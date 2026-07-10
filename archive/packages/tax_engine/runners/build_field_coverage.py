import argparse
import json
import sys
from pathlib import Path

from packages.tax_engine.direct_mapping import load_direct_mapping_payload, run_direct_source_mapping
from packages.tax_engine.field_coverage import build_field_coverage, validate_field_coverage
from packages.tax_engine.runners.output import write_text_output
from packages.tax_engine.source_documents import load_source_document


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Build federal field coverage from source document JSON files.")
    parser.add_argument(
        "--source-document",
        action="append",
        dest="source_documents",
        required=True,
        help="Path to a source document JSON file. May be supplied multiple times.",
    )
    parser.add_argument(
        "--output",
        help="Optional output path. If omitted, coverage JSON is written to stdout.",
    )
    parser.add_argument(
        "--compact",
        action="store_true",
        help="Write compact JSON instead of pretty-printed JSON.",
    )
    return parser


def run(source_document_paths: list[Path]) -> dict:
    documents = [load_source_document(path) for path in source_document_paths]
    mapping_payload = load_direct_mapping_payload()
    direct_mapping_result = run_direct_source_mapping(documents, mapping_payload)
    coverage = build_field_coverage(
        direct_mapping_result=direct_mapping_result,
        mapping_payload=mapping_payload,
    )
    validate_field_coverage(coverage)
    return coverage


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    coverage = run([Path(path) for path in args.source_documents])
    rendered = json.dumps(coverage, separators=(",", ":") if args.compact else None, indent=None if args.compact else 2)
    rendered += "\n"

    if args.output:
        write_text_output(Path(args.output), rendered)
    else:
        sys.stdout.write(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
