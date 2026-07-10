import argparse
import json
import sys
from pathlib import Path

from packages.tax_engine.runners.output import write_text_output
from packages.tax_engine.tax_workspace_runs import build_run_manifest, current_run_timestamp, execute_tax_workspace


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run a synthetic tax workspace workflow.")
    parser.add_argument("--workspace", required=True, help="Path to a tax workspace JSON file.")
    parser.add_argument("--output-dir", required=True, help="Directory where workflow artifacts should be written.")
    parser.add_argument(
        "--timestamp-run",
        action="store_true",
        help="Write artifacts under a filesystem-safe created-at timestamp directory inside --output-dir.",
    )
    parser.add_argument("--run-id", help="Optional run identifier. Defaults to '<workspace-id>-run'.")
    parser.add_argument("--created-at", help="Optional RFC3339 timestamp for deterministic runs.")
    parser.add_argument("--compact", action="store_true", help="Write compact JSON instead of pretty-printed JSON.")
    return parser


def render_json(payload: dict | list, *, compact: bool) -> str:
    return json.dumps(payload, separators=(",", ":") if compact else None, indent=None if compact else 2) + "\n"


def timestamp_directory_name(created_at: str) -> str:
    return (
        created_at
        .replace("-", "")
        .replace(":", "")
        .replace("+", "")
    )


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    result = execute_tax_workspace(Path(args.workspace))
    created_at = args.created_at or current_run_timestamp()
    output_dir = Path(args.output_dir)
    if args.timestamp_run:
        output_dir = output_dir / timestamp_directory_name(created_at)

    artifact_paths = {
        "normalized_source_documents": output_dir / "normalized-source-documents.json",
        "source_validation": output_dir / "source-validation.json",
        "field_coverage": output_dir / "field-coverage.json",
        "field_resolution": output_dir / "field-resolution.json",
        "return_artifact": output_dir / "return-artifact.json",
        "return_review_markdown": output_dir / "return-artifact.md",
        "field_coverage_markdown": output_dir / "field-coverage.md",
        "run_manifest": output_dir / "run-manifest.json",
    }
    run_manifest = build_run_manifest(
        workspace_path=Path(args.workspace),
        run_result=result,
        output_paths=artifact_paths,
        run_id=args.run_id or f"{result['workspace_id']}-run",
        created_at=created_at,
    )

    write_text_output(
        artifact_paths["normalized_source_documents"],
        render_json(result["normalized_source_documents"], compact=args.compact),
    )
    write_text_output(
        artifact_paths["source_validation"],
        render_json(result["source_validation"], compact=args.compact),
    )
    write_text_output(
        artifact_paths["field_coverage"],
        render_json(result["field_coverage"], compact=args.compact),
    )
    write_text_output(
        artifact_paths["field_resolution"],
        render_json(result["field_resolution"], compact=args.compact),
    )
    write_text_output(
        artifact_paths["return_artifact"],
        render_json(result["return_artifact"], compact=args.compact),
    )
    write_text_output(
        artifact_paths["return_review_markdown"],
        result["return_review_markdown"],
    )
    write_text_output(
        artifact_paths["field_coverage_markdown"],
        result["field_coverage_markdown"],
    )
    write_text_output(
        artifact_paths["run_manifest"],
        render_json(run_manifest, compact=args.compact),
    )

    sys.stdout.write(
        render_json(
            {
                "workspace_id": result["workspace_id"],
                "artifacts": {
                    name: str(path)
                    for name, path in artifact_paths.items()
                },
            },
            compact=args.compact,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
