import json
import os
from datetime import UTC, datetime
from pathlib import Path

import jsonschema

from packages.tax_engine.coverage_markdown import render_grouped_coverage_markdown
from packages.tax_engine.direct_mapping import load_direct_mapping_payload, run_direct_source_mapping
from packages.tax_engine.field_coverage import build_field_coverage, validate_field_coverage
from packages.tax_engine.field_resolution import build_field_resolution
from packages.tax_engine.return_artifacts import build_return_artifact
from packages.tax_engine.return_review import render_return_review_markdown
from packages.tax_engine.source_document_drafts import load_source_document_draft_payload, normalize_source_document_draft
from packages.tax_engine.source_documents import source_document_from_payload, validate_source_document_payload
from packages.tax_engine.source_validation import build_source_validation_report
from packages.tax_engine.tax_workspaces import load_tax_workspace, load_tax_workspace_payload


ROOT = Path(__file__).resolve().parents[2]
RUN_MANIFEST_SCHEMA_PATH = ROOT / "packages" / "schemas" / "run-manifest.schema.json"
ENGINE_VERSION = "prototype"


def execute_tax_workspace(workspace_path: Path) -> dict:
    workspace = load_tax_workspace(workspace_path)
    normalized_source_documents = []
    source_documents = []

    for draft_path in workspace.source_document_draft_paths:
        draft_payload = load_source_document_draft_payload(draft_path)
        source_document_payload = normalize_source_document_draft(draft_payload)
        validate_source_document_payload(source_document_payload)
        normalized_source_documents.append(source_document_payload)
        source_documents.append(source_document_from_payload(source_document_payload))

    mapping_payload = load_direct_mapping_payload()
    direct_mapping_result = run_direct_source_mapping(source_documents, mapping_payload)
    field_coverage = build_field_coverage(
        direct_mapping_result=direct_mapping_result,
        mapping_payload=mapping_payload,
    )
    validate_field_coverage(field_coverage)

    field_resolution = build_field_resolution(field_coverage)
    return_artifact = build_return_artifact(field_resolution)

    return {
        "workspace_id": workspace.workspace_id,
        "tax_year": workspace.tax_year,
        "jurisdiction": workspace.jurisdiction,
        "normalized_source_documents": normalized_source_documents,
        "source_validation": build_source_validation_report(source_documents),
        "field_coverage": field_coverage,
        "field_resolution": field_resolution,
        "return_artifact": return_artifact,
        "return_review_markdown": render_return_review_markdown(return_artifact),
        "field_coverage_markdown": render_grouped_coverage_markdown(field_coverage),
    }


def current_run_timestamp() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def build_run_manifest(
    *,
    workspace_path: Path,
    run_result: dict,
    output_paths: dict[str, Path],
    run_id: str,
    created_at: str,
) -> dict:
    workspace_payload = load_tax_workspace_payload(workspace_path)
    manifest = {
        "schema_version": "1.0.0",
        "run_id": run_id,
        "workspace_id": run_result["workspace_id"],
        "tax_year": run_result["tax_year"],
        "jurisdiction": run_result["jurisdiction"],
        "engine_version": ENGINE_VERSION,
        "created_at": created_at,
        "inputs": [
            {
                "artifact_type": "tax_workspace",
                "path": str(workspace_path),
                "media_type": "application/json",
            },
            *[
                {
                    "artifact_type": "source_document_draft",
                    "path": portable_workspace_reference_path(workspace_path, draft["path"]),
                    "media_type": "application/json",
                }
                for draft in workspace_payload["source_document_drafts"]
            ],
        ],
        "outputs": [
            {
                "artifact_type": artifact_type,
                "path": str(path),
                "media_type": media_type_for_output(artifact_type),
            }
            for artifact_type, path in output_paths.items()
        ],
    }
    validate_run_manifest(manifest)
    return manifest


def media_type_for_output(artifact_type: str) -> str:
    if artifact_type in {"field_coverage_markdown", "return_review_markdown"}:
        return "text/markdown"
    return "application/json"


def portable_workspace_reference_path(workspace_path: Path, referenced_path: str) -> str:
    path = Path(referenced_path)
    if path.is_absolute():
        return str(path)
    return os.path.normpath(str(workspace_path.parent / path))


def validate_run_manifest(payload: dict) -> None:
    schema = json.loads(RUN_MANIFEST_SCHEMA_PATH.read_text())
    jsonschema.validate(payload, schema)
