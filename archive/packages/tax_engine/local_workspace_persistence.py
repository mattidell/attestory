import copy
import json
import re
from pathlib import Path
from typing import Any, Literal, Mapping, TypedDict, cast

from packages.tax_engine.product_boundary import (
    ENGINE_ARTIFACT_TYPES,
    PRODUCT_RUN_DETAIL_SCHEMA_PATH,
    PRODUCT_RUN_PAYLOAD_SCHEMA_PATH,
    PRODUCT_RUN_SUMMARY_SCHEMA_PATH,
    PRODUCT_WORKSPACE_SCHEMA_PATH,
    SOURCE_DOCUMENT_DRAFT_SCHEMA_PATH,
    ArtifactReference,
    DocumentType,
    ProductRunDetailPayload,
    ProductRunPayload,
    ProductRunSummaryPayload,
    ProductSourceDraftRef,
    ProductWorkspacePayload,
    SourceDraftSnapshot,
    artifact_file_name,
    execute_product_run_payload,
    load_json,
    media_type_for_artifact,
    validate_product_run_detail,
    validate_product_run_payload,
    validate_product_run_summary,
    validate_product_workspace,
    validate_with_schema,
)
from packages.tax_engine.tax_workspace_runs import ENGINE_VERSION, validate_run_manifest


ROOT = Path(__file__).resolve().parents[2]
LOCAL_SOURCE_DRAFT_LATEST_SCHEMA_PATH = (
    ROOT / "packages" / "schemas" / "local-source-draft-latest.schema.json"
)

SAFE_SEGMENT_PATTERN = re.compile(r"^[A-Za-z0-9._-]+$")

JsonObject = dict[str, Any]


class SourceRevisionRef(TypedDict):
    draft_id: str
    revision_id: str


class LocalSourceDraftLatestPointer(TypedDict):
    schema_version: str
    draft_id: str
    document_type: DocumentType
    revision_id: str
    uri: str


class LocalRunRecords(TypedDict):
    run_payload: ProductRunPayload
    run_summary: ProductRunSummaryPayload
    run_detail: ProductRunDetailPayload
    engine_result: JsonObject


class LocalWorkspaceRepository:
    def __init__(self, storage_root: Path):
        self.storage_root = Path(storage_root)

    def create_workspace(self, workspace: ProductWorkspacePayload) -> ProductWorkspacePayload:
        validate_product_workspace(workspace)
        owner_id = workspace["owner_id"]
        workspace_id = workspace["workspace_id"]
        self._validate_segment(owner_id)
        self._validate_segment(workspace_id)
        self._write_json(self.workspace_path(owner_id, workspace_id), workspace)
        return copy.deepcopy(workspace)

    def load_workspace(self, owner_id: str, workspace_id: str) -> ProductWorkspacePayload:
        workspace = load_json(self.workspace_path(owner_id, workspace_id))
        validate_product_workspace(workspace)
        return cast(ProductWorkspacePayload, workspace)

    def list_workspaces(self, owner_id: str) -> list[ProductWorkspacePayload]:
        owner_dir = self._owner_dir(owner_id)
        if not owner_dir.exists():
            return []
        workspaces = [
            self.load_workspace(owner_id, workspace_dir.name)
            for workspace_dir in owner_dir.iterdir()
            if workspace_dir.is_dir() and (workspace_dir / "workspace.json").exists()
        ]
        return sorted(workspaces, key=lambda workspace: workspace["workspace_id"])

    def save_source_draft_revision(
        self,
        *,
        owner_id: str,
        workspace_id: str,
        draft_payload: JsonObject,
        status: Literal["active", "archived"] = "active",
    ) -> LocalSourceDraftLatestPointer:
        validate_with_schema(draft_payload, SOURCE_DOCUMENT_DRAFT_SCHEMA_PATH)
        workspace = self.load_workspace(owner_id, workspace_id)
        if draft_payload["tax_year"] != workspace["tax_year"]:
            raise ValueError("draft tax_year must match workspace tax_year")

        draft_id = draft_payload["source_document_id"]
        revision_id = draft_payload["source_revision_id"]
        document_type = draft_payload["document_type"]
        self._validate_segment(draft_id)
        self._validate_segment(revision_id)

        revision_uri = f"source-drafts/{draft_id}/{revision_id}.json"
        latest_pointer = {
            "schema_version": "1.0.0",
            "draft_id": draft_id,
            "document_type": document_type,
            "revision_id": revision_id,
            "uri": revision_uri,
        }
        validate_source_draft_latest(latest_pointer)
        typed_latest_pointer = cast(LocalSourceDraftLatestPointer, latest_pointer)

        self._write_json(
            self.source_draft_revision_path(owner_id, workspace_id, draft_id, revision_id),
            draft_payload,
        )
        self._write_json(
            self.source_draft_latest_path(owner_id, workspace_id, draft_id),
            typed_latest_pointer,
        )
        updated_workspace = self._workspace_with_source_draft(
            workspace=workspace,
            draft_id=draft_id,
            document_type=document_type,
            revision_id=revision_id,
            status=status,
            label=draft_payload["label"],
            uri=revision_uri,
        )
        self._write_json(self.workspace_path(owner_id, workspace_id), updated_workspace)
        return typed_latest_pointer

    def load_latest_source_draft_revision(
        self,
        *,
        owner_id: str,
        workspace_id: str,
        draft_id: str,
    ) -> JsonObject:
        latest_pointer = load_json(self.source_draft_latest_path(owner_id, workspace_id, draft_id))
        validate_source_draft_latest(latest_pointer)
        draft_payload = load_json(self._workspace_file(owner_id, workspace_id, latest_pointer["uri"]))
        validate_with_schema(draft_payload, SOURCE_DOCUMENT_DRAFT_SCHEMA_PATH)
        return draft_payload

    def load_source_draft_revision(
        self,
        *,
        owner_id: str,
        workspace_id: str,
        draft_id: str,
        revision_id: str,
    ) -> JsonObject:
        draft_payload = load_json(
            self.source_draft_revision_path(owner_id, workspace_id, draft_id, revision_id)
        )
        validate_with_schema(draft_payload, SOURCE_DOCUMENT_DRAFT_SCHEMA_PATH)
        if draft_payload["source_document_id"] != draft_id:
            raise ValueError("draft payload source_document_id must match requested draft_id")
        if draft_payload["source_revision_id"] != revision_id:
            raise ValueError("draft payload source_revision_id must match requested revision_id")
        return draft_payload

    def list_source_draft_revisions(
        self,
        *,
        owner_id: str,
        workspace_id: str,
        draft_id: str,
    ) -> list[JsonObject]:
        draft_dir = self.source_draft_dir(owner_id, workspace_id, draft_id)
        if not draft_dir.exists():
            return []
        revisions = [
            self.load_source_draft_revision(
                owner_id=owner_id,
                workspace_id=workspace_id,
                draft_id=draft_id,
                revision_id=revision_path.stem,
            )
            for revision_path in draft_dir.glob("*.json")
            if revision_path.name != "latest.json"
        ]
        return sorted(revisions, key=lambda draft: draft["source_revision_id"])

    def archive_source_draft(
        self,
        *,
        owner_id: str,
        workspace_id: str,
        draft_id: str,
    ) -> ProductSourceDraftRef:
        workspace = self.load_workspace(owner_id, workspace_id)
        updated_workspace = copy.deepcopy(workspace)
        updated_drafts: list[ProductSourceDraftRef] = []
        archived_draft: ProductSourceDraftRef | None = None
        for source_draft in updated_workspace["source_drafts"]:
            if source_draft["draft_id"] == draft_id:
                archived_draft = {**source_draft, "status": "archived"}
                updated_drafts.append(archived_draft)
            else:
                updated_drafts.append(source_draft)
        if archived_draft is None:
            raise FileNotFoundError(f"source draft not found: {draft_id}")
        updated_workspace["source_drafts"] = sorted(
            updated_drafts,
            key=lambda draft: draft["draft_id"],
        )
        validate_product_workspace(updated_workspace)
        self._write_json(self.workspace_path(owner_id, workspace_id), updated_workspace)
        return archived_draft

    def build_run_payload(
        self,
        *,
        owner_id: str,
        workspace_id: str,
        run_id: str,
        source_revision_refs: list[SourceRevisionRef] | None = None,
    ) -> ProductRunPayload:
        self._validate_segment(run_id)
        workspace = self.load_workspace(owner_id, workspace_id)
        source_draft_snapshots: list[SourceDraftSnapshot] = []
        using_latest_revisions = source_revision_refs is None
        draft_refs: list[SourceRevisionRef]
        if using_latest_revisions:
            draft_refs = [
                {
                    "draft_id": draft["draft_id"],
                    "revision_id": draft["revision_id"],
                }
                for draft in workspace["source_drafts"]
                if draft["status"] == "active"
            ]
        else:
            assert source_revision_refs is not None
            draft_refs = source_revision_refs
        workspace_drafts = {
            draft["draft_id"]: draft
            for draft in workspace["source_drafts"]
        }
        for draft_ref in draft_refs:
            draft_id = draft_ref["draft_id"]
            revision_id = draft_ref["revision_id"]
            workspace_draft = workspace_drafts.get(draft_id)
            if workspace_draft is None:
                raise FileNotFoundError(f"source draft not found: {draft_id}")
            if workspace_draft["status"] != "active":
                raise ValueError(f"source draft is not active: {draft_id}")
            if using_latest_revisions:
                draft_payload = self.load_latest_source_draft_revision(
                    owner_id=owner_id,
                    workspace_id=workspace_id,
                    draft_id=draft_id,
                )
            else:
                draft_payload = self.load_source_draft_revision(
                    owner_id=owner_id,
                    workspace_id=workspace_id,
                    draft_id=draft_id,
                    revision_id=revision_id,
                )
            source_draft_snapshots.append(
                {
                    "draft_id": draft_payload["source_document_id"],
                    "document_type": draft_payload["document_type"],
                    "revision_id": draft_payload["source_revision_id"],
                    "payload": draft_payload,
                }
            )

        run_payload = {
            "schema_version": "1.0.0",
            "run_id": run_id,
            "owner_id": workspace["owner_id"],
            "workspace_id": workspace["workspace_id"],
            "tax_year": workspace["tax_year"],
            "jurisdictions": workspace["jurisdictions"],
            "data_classification": workspace["data_classification"],
            "source_draft_snapshots": source_draft_snapshots,
        }
        validate_product_run_payload(run_payload)
        return cast(ProductRunPayload, run_payload)

    def execute_and_persist_run(
        self,
        *,
        owner_id: str,
        workspace_id: str,
        run_id: str,
        created_at: str,
        completed_at: str,
        source_revision_refs: list[SourceRevisionRef] | None = None,
    ) -> LocalRunRecords:
        run_payload = self.build_run_payload(
            owner_id=owner_id,
            workspace_id=workspace_id,
            run_id=run_id,
            source_revision_refs=source_revision_refs,
        )
        result = execute_product_run_payload(
            run_payload,
            created_at=created_at,
            completed_at=completed_at,
        )
        run_manifest = build_local_run_manifest(
            run_payload=run_payload,
            run_summary=result["run_summary"],
            artifact_refs=result["run_detail"]["artifact_refs"],
            created_at=created_at,
        )
        engine_result: JsonObject = {
            **result["engine_result"],
            "run_manifest": run_manifest,
        }
        self.persist_run_records(
            owner_id=owner_id,
            workspace_id=workspace_id,
            run_payload=run_payload,
            run_summary=result["run_summary"],
            run_detail=result["run_detail"],
            engine_result=engine_result,
        )
        return {
            "run_payload": run_payload,
            "run_summary": result["run_summary"],
            "run_detail": result["run_detail"],
            "engine_result": engine_result,
        }

    def persist_run_records(
        self,
        *,
        owner_id: str,
        workspace_id: str,
        run_payload: ProductRunPayload,
        run_summary: ProductRunSummaryPayload,
        run_detail: ProductRunDetailPayload,
        engine_result: JsonObject,
    ) -> None:
        validate_product_run_payload(run_payload)
        validate_product_run_summary(run_summary)
        validate_product_run_detail(run_detail)
        if run_payload["owner_id"] != owner_id:
            raise ValueError("run payload owner_id must match storage owner_id")
        if run_payload["workspace_id"] != workspace_id:
            raise ValueError("run payload workspace_id must match storage workspace_id")
        if run_summary["run_id"] != run_payload["run_id"]:
            raise ValueError("run summary run_id must match run payload run_id")
        if run_summary["workspace_id"] != workspace_id:
            raise ValueError("run summary workspace_id must match storage workspace_id")
        run_id = run_payload["run_id"]
        self._validate_segment(run_id)
        run_dir = self.run_dir(owner_id, workspace_id, run_id)
        if run_dir.exists():
            raise FileExistsError(f"run already exists: {run_id}")

        self._write_json(run_dir / "product-run-payload.json", run_payload)
        self._write_json(run_dir / "product-run-summary.json", run_summary)
        self._write_json(run_dir / "product-run-detail.json", run_detail)

        artifacts_dir = run_dir / "artifacts"
        for artifact_type in ENGINE_ARTIFACT_TYPES:
            artifact_name = artifact_file_name(artifact_type)
            artifact_path = artifacts_dir / artifact_name
            artifact_payload = engine_result[artifact_type]
            if media_type_for_artifact(artifact_type) == "text/markdown":
                self._write_text(artifact_path, artifact_payload)
            else:
                self._write_json(artifact_path, artifact_payload)

    def list_run_summaries(self, owner_id: str, workspace_id: str) -> list[ProductRunSummaryPayload]:
        runs_dir = self.runs_dir(owner_id, workspace_id)
        if not runs_dir.exists():
            return []
        summaries = [
            self.load_run_summary(owner_id, workspace_id, run_dir.name)
            for run_dir in runs_dir.iterdir()
            if run_dir.is_dir() and (run_dir / "product-run-summary.json").exists()
        ]
        return sorted(
            summaries,
            key=lambda summary: (summary["completed_at"], summary["run_id"]),
        )

    def latest_run_summary(self, owner_id: str, workspace_id: str) -> ProductRunSummaryPayload | None:
        summaries = self.list_run_summaries(owner_id, workspace_id)
        if not summaries:
            return None
        return summaries[-1]

    def load_run_summary(self, owner_id: str, workspace_id: str, run_id: str) -> ProductRunSummaryPayload:
        summary = load_json(self.run_dir(owner_id, workspace_id, run_id) / "product-run-summary.json")
        validate_product_run_summary(summary)
        return cast(ProductRunSummaryPayload, summary)

    def load_run_payload(self, owner_id: str, workspace_id: str, run_id: str) -> ProductRunPayload:
        run_payload = load_json(self.run_dir(owner_id, workspace_id, run_id) / "product-run-payload.json")
        validate_product_run_payload(run_payload)
        return cast(ProductRunPayload, run_payload)

    def load_run_detail(self, owner_id: str, workspace_id: str, run_id: str) -> ProductRunDetailPayload:
        detail = load_json(self.run_dir(owner_id, workspace_id, run_id) / "product-run-detail.json")
        validate_product_run_detail(detail)
        return cast(ProductRunDetailPayload, detail)

    def resolve_artifact_ref(
        self,
        *,
        owner_id: str,
        workspace_id: str,
        artifact_ref: ArtifactReference,
    ) -> Path:
        uri_path = Path(artifact_ref["uri"])
        if uri_path.is_absolute() or ".." in uri_path.parts:
            raise ValueError("artifact URI must be relative and stay inside the workspace")
        parts = uri_path.parts
        if len(parts) != 3 or parts[0] != "runs":
            raise ValueError("artifact URI must use runs/<run-id>/<file>")
        run_id = parts[1]
        file_name = parts[2]
        self._validate_segment(run_id)
        self._validate_segment(file_name)
        run_dir = self.run_dir(owner_id, workspace_id, run_id)
        if file_name in {
            "product-run-payload.json",
            "product-run-summary.json",
            "product-run-detail.json",
        }:
            return run_dir / file_name
        return run_dir / "artifacts" / file_name

    def workspace_path(self, owner_id: str, workspace_id: str) -> Path:
        return self.workspace_dir(owner_id, workspace_id) / "workspace.json"

    def workspace_dir(self, owner_id: str, workspace_id: str) -> Path:
        self._validate_segment(owner_id)
        self._validate_segment(workspace_id)
        return self._owner_dir(owner_id) / workspace_id

    def source_draft_revision_path(
        self,
        owner_id: str,
        workspace_id: str,
        draft_id: str,
        revision_id: str,
    ) -> Path:
        self._validate_segment(revision_id)
        return self.source_draft_dir(owner_id, workspace_id, draft_id) / f"{revision_id}.json"

    def source_draft_latest_path(self, owner_id: str, workspace_id: str, draft_id: str) -> Path:
        return self.source_draft_dir(owner_id, workspace_id, draft_id) / "latest.json"

    def source_draft_dir(self, owner_id: str, workspace_id: str, draft_id: str) -> Path:
        self._validate_segment(draft_id)
        return self.workspace_dir(owner_id, workspace_id) / "source-drafts" / draft_id

    def runs_dir(self, owner_id: str, workspace_id: str) -> Path:
        return self.workspace_dir(owner_id, workspace_id) / "runs"

    def run_dir(self, owner_id: str, workspace_id: str, run_id: str) -> Path:
        self._validate_segment(run_id)
        return self.runs_dir(owner_id, workspace_id) / run_id

    def _owner_dir(self, owner_id: str) -> Path:
        self._validate_segment(owner_id)
        return self.storage_root / "workspaces" / owner_id

    def _workspace_file(self, owner_id: str, workspace_id: str, uri: str) -> Path:
        path = Path(uri)
        if path.is_absolute() or ".." in path.parts:
            raise ValueError("workspace URI must be relative and stay inside the workspace")
        return self.workspace_dir(owner_id, workspace_id) / path

    def _workspace_with_source_draft(
        self,
        *,
        workspace: ProductWorkspacePayload,
        draft_id: str,
        document_type: DocumentType,
        revision_id: str,
        status: Literal["active", "archived"],
        label: str,
        uri: str,
    ) -> ProductWorkspacePayload:
        updated_workspace = copy.deepcopy(workspace)
        source_draft: ProductSourceDraftRef = {
            "draft_id": draft_id,
            "document_type": document_type,
            "revision_id": revision_id,
            "status": status,
            "label": label,
            "uri": uri,
        }
        source_drafts = [
            existing
            for existing in updated_workspace["source_drafts"]
            if existing["draft_id"] != draft_id
        ]
        source_drafts.append(source_draft)
        updated_workspace["source_drafts"] = sorted(
            source_drafts,
            key=lambda draft: draft["draft_id"],
        )
        validate_product_workspace(updated_workspace)
        return updated_workspace

    def _validate_segment(self, value: str) -> None:
        if not SAFE_SEGMENT_PATTERN.match(value):
            raise ValueError(f"unsafe storage path segment: {value}")

    def _write_json(self, path: Path, payload: Mapping[str, Any]) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(payload, indent=2) + "\n")

    def _write_text(self, path: Path, payload: str) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(payload)


def load_source_draft_latest(path: Path) -> LocalSourceDraftLatestPointer:
    payload = load_json(path)
    validate_source_draft_latest(payload)
    return cast(LocalSourceDraftLatestPointer, payload)


def validate_source_draft_latest(payload: Mapping[str, Any]) -> None:
    validate_with_schema(payload, LOCAL_SOURCE_DRAFT_LATEST_SCHEMA_PATH)


def build_local_run_manifest(
    *,
    run_payload: ProductRunPayload,
    run_summary: ProductRunSummaryPayload,
    artifact_refs: list[ArtifactReference],
    created_at: str,
) -> JsonObject:
    manifest = {
        "schema_version": "1.0.0",
        "run_id": run_payload["run_id"],
        "workspace_id": run_payload["workspace_id"],
        "tax_year": run_payload["tax_year"],
        "jurisdiction": "federal",
        "engine_version": ENGINE_VERSION,
        "created_at": created_at,
        "inputs": [
            {
                "artifact_type": "product_run_payload",
                "path": f"runs/{run_payload['run_id']}/product-run-payload.json",
                "media_type": "application/json",
            },
            *[
                {
                    "artifact_type": "source_document_draft",
                    "path": f"source-drafts/{snapshot['draft_id']}/{snapshot['revision_id']}.json",
                    "media_type": "application/json",
                }
                for snapshot in run_payload["source_draft_snapshots"]
            ],
        ],
        "outputs": [
            {
                "artifact_type": "product_run_summary",
                "path": f"runs/{run_payload['run_id']}/product-run-summary.json",
                "media_type": "application/json",
            },
            {
                "artifact_type": "product_run_detail",
                "path": run_summary["detail_ref"]["uri"],
                "media_type": "application/json",
            },
            *[
                {
                    "artifact_type": artifact_ref["artifact_type"],
                    "path": artifact_ref["uri"],
                    "media_type": artifact_ref["media_type"],
                }
                for artifact_ref in artifact_refs
                if artifact_ref["artifact_type"] != "run_manifest"
            ],
            {
                "artifact_type": "run_manifest",
                "path": f"runs/{run_payload['run_id']}/run-manifest.json",
                "media_type": "application/json",
            },
        ],
    }
    validate_run_manifest(manifest)
    return manifest


def validate_local_storage_fixture(root: Path) -> None:
    repository = LocalWorkspaceRepository(root)
    for owner_dir in (root / "workspaces").iterdir():
        if not owner_dir.is_dir():
            continue
        for workspace in repository.list_workspaces(owner_dir.name):
            owner_id = workspace["owner_id"]
            workspace_id = workspace["workspace_id"]
            for draft in workspace["source_drafts"]:
                latest_path = repository.source_draft_latest_path(
                    owner_id,
                    workspace_id,
                    draft["draft_id"],
                )
                latest_pointer = load_source_draft_latest(latest_path)
                if latest_pointer["revision_id"] != draft["revision_id"]:
                    raise ValueError("latest pointer must match workspace draft revision")
                repository.load_latest_source_draft_revision(
                    owner_id=owner_id,
                    workspace_id=workspace_id,
                    draft_id=draft["draft_id"],
                )
            for summary in repository.list_run_summaries(owner_id, workspace_id):
                run_payload = repository.load_run_payload(owner_id, workspace_id, summary["run_id"])
                detail = repository.load_run_detail(owner_id, workspace_id, summary["run_id"])
                if detail["run_payload"] != run_payload:
                    raise ValueError("run detail payload must match stored run payload")
                if detail["run_summary"] != summary:
                    raise ValueError("run detail summary must match stored run summary")
                for artifact_ref in [summary["detail_ref"], *detail["artifact_refs"]]:
                    artifact_path = repository.resolve_artifact_ref(
                        owner_id=owner_id,
                        workspace_id=workspace_id,
                        artifact_ref=artifact_ref,
                    )
                    if not artifact_path.exists() and artifact_ref["artifact_type"] != "run_manifest":
                        continue


def schema_paths_for_local_storage() -> tuple[Path, ...]:
    return (
        LOCAL_SOURCE_DRAFT_LATEST_SCHEMA_PATH,
        PRODUCT_WORKSPACE_SCHEMA_PATH,
        PRODUCT_RUN_PAYLOAD_SCHEMA_PATH,
        PRODUCT_RUN_SUMMARY_SCHEMA_PATH,
        PRODUCT_RUN_DETAIL_SCHEMA_PATH,
    )
