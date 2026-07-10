import json
from pathlib import Path
from typing import Any, Literal, Mapping, TypedDict, cast

import jsonschema

from packages.tax_engine.coverage_markdown import render_grouped_coverage_markdown
from packages.tax_engine.direct_mapping import load_direct_mapping_payload, run_direct_source_mapping
from packages.tax_engine.field_coverage import build_field_coverage, validate_field_coverage
from packages.tax_engine.field_resolution import build_field_resolution
from packages.tax_engine.return_artifacts import build_return_artifact
from packages.tax_engine.return_review import render_return_review_markdown
from packages.tax_engine.source_document_drafts import normalize_source_document_draft
from packages.tax_engine.source_documents import source_document_from_payload, validate_source_document_payload
from packages.tax_engine.source_validation import build_source_validation_report


ROOT = Path(__file__).resolve().parents[2]
SCHEMA_DIR = ROOT / "packages" / "schemas"

PRODUCT_WORKSPACE_SCHEMA_PATH = SCHEMA_DIR / "product-workspace.schema.json"
PRODUCT_RUN_PAYLOAD_SCHEMA_PATH = SCHEMA_DIR / "product-run-payload.schema.json"
PRODUCT_RUN_SUMMARY_SCHEMA_PATH = SCHEMA_DIR / "product-run-summary.schema.json"
PRODUCT_RUN_DETAIL_SCHEMA_PATH = SCHEMA_DIR / "product-run-detail.schema.json"
SOURCE_DOCUMENT_DRAFT_SCHEMA_PATH = SCHEMA_DIR / "source-document-draft.schema.json"

ENGINE_ARTIFACT_TYPES = (
    "normalized_source_documents",
    "source_validation",
    "field_coverage",
    "field_resolution",
    "return_artifact",
    "return_review_markdown",
    "field_coverage_markdown",
    "run_manifest",
)

JsonObject = dict[str, Any]
DocumentType = Literal["w2", "1099-int"]
DataClassification = Literal["synthetic_demo"]
RunStatus = Literal["succeeded"]


class ArtifactReference(TypedDict):
    artifact_type: str
    media_type: str
    uri: str


class ProductSourceDraftRef(TypedDict):
    draft_id: str
    document_type: DocumentType
    revision_id: str
    status: Literal["active", "archived"]
    label: str
    uri: str


class ProductWorkspacePayload(TypedDict):
    schema_version: str
    owner_id: str
    workspace_id: str
    tax_year: int
    jurisdictions: list[str]
    data_classification: DataClassification
    source_drafts: list[ProductSourceDraftRef]


class SourceDraftSnapshot(TypedDict):
    draft_id: str
    document_type: DocumentType
    revision_id: str
    payload: JsonObject


class ProductRunPayload(TypedDict):
    schema_version: str
    run_id: str
    owner_id: str
    workspace_id: str
    tax_year: int
    jurisdictions: list[str]
    data_classification: DataClassification
    source_draft_snapshots: list[SourceDraftSnapshot]


class InputRevisionRef(TypedDict):
    draft_id: str
    revision_id: str
    document_type: DocumentType


class ProductRunResultSummary(TypedDict):
    validation_error_count: int
    blocked_field_count: int
    generated_artifact_count: int


class ProductRunSummaryPayload(TypedDict):
    schema_version: str
    run_id: str
    workspace_id: str
    tax_year: int
    created_at: str
    completed_at: str
    status: RunStatus
    input_revision_refs: list[InputRevisionRef]
    result_summary: ProductRunResultSummary
    detail_ref: ArtifactReference


class ProductRunDetailPayload(TypedDict):
    schema_version: str
    run_summary: ProductRunSummaryPayload
    run_payload: ProductRunPayload
    artifact_refs: list[ArtifactReference]


class EngineWorkflowResult(TypedDict):
    workspace_id: str
    tax_year: int
    jurisdictions: list[str]
    normalized_source_documents: list[JsonObject]
    source_validation: JsonObject
    field_coverage: JsonObject
    field_resolution: JsonObject
    return_artifact: JsonObject
    return_review_markdown: str
    field_coverage_markdown: str


class ProductRunExecutionResult(TypedDict):
    run_summary: ProductRunSummaryPayload
    run_detail: ProductRunDetailPayload
    engine_result: EngineWorkflowResult


def load_json(path: Path) -> JsonObject:
    return cast(JsonObject, json.loads(path.read_text()))


def validate_with_schema(payload: Mapping[str, Any], schema_path: Path) -> None:
    jsonschema.validate(payload, load_json(schema_path))


def load_product_workspace(path: Path) -> ProductWorkspacePayload:
    payload = load_json(path)
    validate_product_workspace(payload)
    return cast(ProductWorkspacePayload, payload)


def validate_product_workspace(payload: Mapping[str, Any]) -> None:
    validate_with_schema(payload, PRODUCT_WORKSPACE_SCHEMA_PATH)


def load_product_run_payload(path: Path) -> ProductRunPayload:
    payload = load_json(path)
    validate_product_run_payload(payload)
    return cast(ProductRunPayload, payload)


def validate_product_run_payload(payload: Mapping[str, Any]) -> None:
    validate_with_schema(payload, PRODUCT_RUN_PAYLOAD_SCHEMA_PATH)
    for snapshot in payload["source_draft_snapshots"]:
        draft_payload = snapshot["payload"]
        validate_with_schema(draft_payload, SOURCE_DOCUMENT_DRAFT_SCHEMA_PATH)
        if snapshot["draft_id"] != draft_payload["source_document_id"]:
            raise ValueError("snapshot draft_id must match embedded draft payload")
        if snapshot["document_type"] != draft_payload["document_type"]:
            raise ValueError("snapshot document_type must match embedded draft payload")
        if snapshot["revision_id"] != draft_payload["source_revision_id"]:
            raise ValueError("snapshot revision_id must match embedded draft payload")
        if payload["tax_year"] != draft_payload["tax_year"]:
            raise ValueError("run tax_year must match embedded draft payload")


def load_product_run_summary(path: Path) -> ProductRunSummaryPayload:
    payload = load_json(path)
    validate_product_run_summary(payload)
    return cast(ProductRunSummaryPayload, payload)


def validate_product_run_summary(payload: Mapping[str, Any]) -> None:
    validate_with_schema(payload, PRODUCT_RUN_SUMMARY_SCHEMA_PATH)


def load_product_run_detail(path: Path) -> ProductRunDetailPayload:
    payload = load_json(path)
    validate_product_run_detail(payload)
    return cast(ProductRunDetailPayload, payload)


def validate_product_run_detail(payload: Mapping[str, Any]) -> None:
    validate_with_schema(payload, PRODUCT_RUN_DETAIL_SCHEMA_PATH)
    validate_product_run_summary(payload["run_summary"])
    validate_product_run_payload(payload["run_payload"])


def artifact_reference(*, artifact_type: str, run_id: str) -> ArtifactReference:
    return {
        "artifact_type": artifact_type,
        "media_type": media_type_for_artifact(artifact_type),
        "uri": f"runs/{run_id}/{artifact_file_name(artifact_type)}",
    }


def artifact_refs_for_run(run_id: str) -> list[ArtifactReference]:
    return [
        artifact_reference(artifact_type=artifact_type, run_id=run_id)
        for artifact_type in ENGINE_ARTIFACT_TYPES
    ]


def artifact_file_name(artifact_type: str) -> str:
    return {
        "normalized_source_documents": "normalized-source-documents.json",
        "source_validation": "source-validation.json",
        "field_coverage": "field-coverage.json",
        "field_resolution": "field-resolution.json",
        "return_artifact": "return-artifact.json",
        "return_review_markdown": "return-artifact.md",
        "field_coverage_markdown": "field-coverage.md",
        "run_manifest": "run-manifest.json",
    }[artifact_type]


def media_type_for_artifact(artifact_type: str) -> str:
    if artifact_type in {"return_review_markdown", "field_coverage_markdown"}:
        return "text/markdown"
    return "application/json"


def build_product_run_summary(
    *,
    run_payload: ProductRunPayload,
    run_result: EngineWorkflowResult,
    created_at: str,
    completed_at: str,
    artifact_refs: list[ArtifactReference],
) -> ProductRunSummaryPayload:
    source_validation = run_result["source_validation"]
    return_artifact = run_result["return_artifact"]
    blocked_fields = return_artifact["resolution_summary"]["blocked_fields"]
    summary = {
        "schema_version": "1.0.0",
        "run_id": run_payload["run_id"],
        "workspace_id": run_payload["workspace_id"],
        "tax_year": run_payload["tax_year"],
        "created_at": created_at,
        "completed_at": completed_at,
        "status": "succeeded",
        "input_revision_refs": [
            {
                "draft_id": snapshot["draft_id"],
                "revision_id": snapshot["revision_id"],
                "document_type": snapshot["document_type"],
            }
            for snapshot in run_payload["source_draft_snapshots"]
        ],
        "result_summary": {
            "validation_error_count": sum(
                len(document["missing_required_fields"])
                for document in source_validation["documents"]
            ),
            "blocked_field_count": len(blocked_fields),
            "generated_artifact_count": len(artifact_refs),
        },
        "detail_ref": {
            "artifact_type": "product_run_detail",
            "media_type": "application/json",
            "uri": f"runs/{run_payload['run_id']}/product-run-detail.json",
        },
    }
    validate_product_run_summary(summary)
    return cast(ProductRunSummaryPayload, summary)


def build_product_run_detail(
    *,
    run_payload: ProductRunPayload,
    run_summary: ProductRunSummaryPayload,
    artifact_refs: list[ArtifactReference],
) -> ProductRunDetailPayload:
    detail = {
        "schema_version": "1.0.0",
        "run_summary": run_summary,
        "run_payload": run_payload,
        "artifact_refs": artifact_refs,
    }
    validate_product_run_detail(detail)
    return cast(ProductRunDetailPayload, detail)


def execute_product_run_payload(
    run_payload: ProductRunPayload,
    *,
    created_at: str,
    completed_at: str,
) -> ProductRunExecutionResult:
    validate_product_run_payload(run_payload)
    run_result = execute_engine_workflow_from_run_payload(run_payload)
    artifact_refs = artifact_refs_for_run(run_payload["run_id"])
    run_summary = build_product_run_summary(
        run_payload=run_payload,
        run_result=run_result,
        created_at=created_at,
        completed_at=completed_at,
        artifact_refs=artifact_refs,
    )
    return {
        "run_summary": run_summary,
        "run_detail": build_product_run_detail(
            run_payload=run_payload,
            run_summary=run_summary,
            artifact_refs=artifact_refs,
        ),
        "engine_result": run_result,
    }


def execute_engine_workflow_from_run_payload(run_payload: ProductRunPayload) -> EngineWorkflowResult:
    normalized_source_documents: list[JsonObject] = []
    source_documents = []

    for snapshot in run_payload["source_draft_snapshots"]:
        source_document_payload = normalize_source_document_draft(snapshot["payload"])
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
        "workspace_id": run_payload["workspace_id"],
        "tax_year": run_payload["tax_year"],
        "jurisdictions": run_payload["jurisdictions"],
        "normalized_source_documents": normalized_source_documents,
        "source_validation": build_source_validation_report(source_documents),
        "field_coverage": field_coverage,
        "field_resolution": field_resolution,
        "return_artifact": return_artifact,
        "return_review_markdown": render_return_review_markdown(return_artifact),
        "field_coverage_markdown": render_grouped_coverage_markdown(field_coverage),
    }
