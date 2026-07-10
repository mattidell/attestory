import argparse
import json
import sys
from pathlib import Path

from packages.tax_engine.coverage_markdown import render_grouped_coverage_markdown
from packages.tax_engine.draft_coverage import build_field_coverage_from_drafts
from packages.tax_engine.runners.output import write_text_output


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Build federal field coverage directly from source document drafts.")
    parser.add_argument(
        "--draft",
        action="append",
        dest="drafts",
        required=True,
        help="Path to a source document draft JSON file. May be supplied multiple times.",
    )
    parser.add_argument("--output", help="Optional output path. If omitted, output is written to stdout.")
    parser.add_argument("--format", choices=["json", "markdown"], default="json", help="Output format.")
    parser.add_argument("--compact", action="store_true", help="Write compact JSON instead of pretty-printed JSON.")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    coverage = build_field_coverage_from_drafts([Path(path) for path in args.drafts])
    if args.format == "markdown":
        rendered = render_grouped_coverage_markdown(coverage)
    else:
        rendered = json.dumps(coverage, separators=(",", ":") if args.compact else None, indent=None if args.compact else 2)
        rendered += "\n"

    if args.output:
        write_text_output(Path(args.output), rendered)
    else:
        sys.stdout.write(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
