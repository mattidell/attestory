import argparse
import json
import sys
from pathlib import Path

from packages.tax_engine.coverage_read_model import (
    build_field_detail_read_model,
    build_grouped_coverage_read_model,
)
from packages.tax_engine.coverage_markdown import render_field_detail_markdown, render_grouped_coverage_markdown
from packages.tax_engine.field_coverage import validate_field_coverage


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Inspect federal field coverage JSON.")
    parser.add_argument("--coverage", required=True, help="Path to field coverage JSON.")
    parser.add_argument("--field-id", help="Optional field ID to inspect. If omitted, grouped coverage is emitted.")
    parser.add_argument("--format", choices=["json", "markdown"], default="json", help="Output format.")
    parser.add_argument("--compact", action="store_true", help="Write compact JSON instead of pretty-printed JSON.")
    return parser


def load_coverage(coverage_path: Path) -> dict:
    coverage = json.loads(coverage_path.read_text())
    validate_field_coverage(coverage)
    return coverage


def run(coverage_path: Path, field_id: str | None = None) -> dict:
    coverage = load_coverage(coverage_path)
    if field_id:
        return build_field_detail_read_model(coverage, field_id)
    return build_grouped_coverage_read_model(coverage)


def run_markdown(coverage_path: Path, field_id: str | None = None) -> str:
    coverage = load_coverage(coverage_path)
    if field_id:
        return render_field_detail_markdown(coverage, field_id)
    return render_grouped_coverage_markdown(coverage)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.format == "markdown":
        sys.stdout.write(run_markdown(Path(args.coverage), args.field_id))
        return 0

    payload = run(Path(args.coverage), args.field_id)
    rendered = json.dumps(payload, separators=(",", ":") if args.compact else None, indent=None if args.compact else 2)
    sys.stdout.write(rendered + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
