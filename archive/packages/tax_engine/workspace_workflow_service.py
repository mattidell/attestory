from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Generic, Literal, TypeVar, TypedDict

import jsonschema

from packages.tax_engine.local_workspace_persistence import LocalRunRecords, LocalWorkspaceRepository
from packages.tax_engine.product_boundary import (
    ArtifactReference,
    ProductRunDetailPayload,
    ProductRunSummaryPayload,
    ProductSourceDraftRef,
    ProductWorkspacePayload,
)


JsonObject = dict[str, Any]
ResultStatus = Literal[
    "success",
    "validation_error",
    "not_found",
    "conflict",
    "execution_failed",
]
ErrorCode = Literal[
    "validation_error",
    "not_found",
    "conflict",
    "execution_failed",
]

RESULT_SUCCESS: ResultStatus = "success"
RESULT_VALIDATION_ERROR: ResultStatus = "validation_error"
RESULT_NOT_FOUND: ResultStatus = "not_found"
RESULT_CONFLICT: ResultStatus = "conflict"
RESULT_EXECUTION_FAILED: ResultStatus = "execution_failed"

T = TypeVar("T")


class SourceRevisionRef(TypedDict):
    draft_id: str
    revision_id: str


@dataclass(frozen=True)
class ServiceError:
    code: ErrorCode
    message: str


@dataclass(frozen=True)
class OperationResult(Generic[T]):
    status: ResultStatus
    value: T | None = None
    errors: tuple[ServiceError, ...] = ()

    @property
    def ok(self) -> bool:
        return self.status == RESULT_SUCCESS


@dataclass(frozen=True)
class ResolvedArtifact:
    artifact_ref: ArtifactReference
    path: Path
    media_type: str
    exists: bool


class WorkspaceWorkflowService:
    def __init__(
        self,
        storage_root: Path | str | None = None,
        repository: LocalWorkspaceRepository | None = None,
    ):
        if repository is None and storage_root is None:
            raise ValueError("storage_root or repository is required")
        if repository is None:
            assert storage_root is not None
            repository = LocalWorkspaceRepository(Path(storage_root))
        self.repository = repository

    def create_workspace(self, workspace: ProductWorkspacePayload) -> OperationResult[ProductWorkspacePayload]:
        return self._run(lambda: self.repository.create_workspace(workspace))

    def get_workspace(self, owner_id: str, workspace_id: str) -> OperationResult[ProductWorkspacePayload]:
        return self._run(lambda: self.repository.load_workspace(owner_id, workspace_id))

    def list_workspaces(self, owner_id: str) -> OperationResult[list[ProductWorkspacePayload]]:
        return self._run(lambda: self.repository.list_workspaces(owner_id))

    def create_source_draft(
        self,
        *,
        owner_id: str,
        workspace_id: str,
        draft_payload: JsonObject,
        status: Literal["active", "archived"] = "active",
    ) -> OperationResult[JsonObject]:
        def create() -> JsonObject:
            workspace = self.repository.load_workspace(owner_id, workspace_id)
            draft_id = draft_payload["source_document_id"]
            if any(draft["draft_id"] == draft_id for draft in workspace["source_drafts"]):
                raise FileExistsError(f"source draft already exists: {draft_id}")
            latest_pointer = self.repository.save_source_draft_revision(
                owner_id=owner_id,
                workspace_id=workspace_id,
                draft_payload=draft_payload,
                status=status,
            )
            return {
                "latest_pointer": latest_pointer,
                "draft": self.repository.load_latest_source_draft_revision(
                    owner_id=owner_id,
                    workspace_id=workspace_id,
                    draft_id=draft_id,
                ),
            }

        return self._run(create)

    def create_source_draft_revision(
        self,
        *,
        owner_id: str,
        workspace_id: str,
        draft_payload: JsonObject,
        status: Literal["active", "archived"] = "active",
    ) -> OperationResult[dict[str, Any]]:
        def create_revision() -> JsonObject:
            workspace = self.repository.load_workspace(owner_id, workspace_id)
            draft_id = draft_payload["source_document_id"]
            if not any(draft["draft_id"] == draft_id for draft in workspace["source_drafts"]):
                raise FileNotFoundError(f"source draft not found: {draft_id}")
            latest_pointer = self.repository.save_source_draft_revision(
                owner_id=owner_id,
                workspace_id=workspace_id,
                draft_payload=draft_payload,
                status=status,
            )
            return {
                "latest_pointer": latest_pointer,
                "draft": self.repository.load_source_draft_revision(
                    owner_id=owner_id,
                    workspace_id=workspace_id,
                    draft_id=draft_id,
                    revision_id=draft_payload["source_revision_id"],
                ),
            }

        return self._run(create_revision)

    def get_latest_source_draft_revision(
        self,
        *,
        owner_id: str,
        workspace_id: str,
        draft_id: str,
    ) -> OperationResult[dict[str, Any]]:
        return self._run(
            lambda: self.repository.load_latest_source_draft_revision(
                owner_id=owner_id,
                workspace_id=workspace_id,
                draft_id=draft_id,
            )
        )

    def get_source_draft_revision(
        self,
        *,
        owner_id: str,
        workspace_id: str,
        draft_id: str,
        revision_id: str,
    ) -> OperationResult[JsonObject]:
        return self._run(
            lambda: self.repository.load_source_draft_revision(
                owner_id=owner_id,
                workspace_id=workspace_id,
                draft_id=draft_id,
                revision_id=revision_id,
            )
        )

    def list_source_draft_revisions(
        self,
        *,
        owner_id: str,
        workspace_id: str,
        draft_id: str,
    ) -> OperationResult[list[JsonObject]]:
        return self._run(
            lambda: self.repository.list_source_draft_revisions(
                owner_id=owner_id,
                workspace_id=workspace_id,
                draft_id=draft_id,
            )
        )

    def archive_source_draft(
        self,
        *,
        owner_id: str,
        workspace_id: str,
        draft_id: str,
    ) -> OperationResult[ProductSourceDraftRef]:
        return self._run(
            lambda: self.repository.archive_source_draft(
                owner_id=owner_id,
                workspace_id=workspace_id,
                draft_id=draft_id,
            )
        )

    def execute_run(
        self,
        *,
        owner_id: str,
        workspace_id: str,
        run_id: str,
        created_at: str,
        completed_at: str,
        source_revision_refs: list[SourceRevisionRef],
    ) -> OperationResult[LocalRunRecords]:
        return self._run(
            lambda: self.repository.execute_and_persist_run(
                owner_id=owner_id,
                workspace_id=workspace_id,
                run_id=run_id,
                created_at=created_at,
                completed_at=completed_at,
                source_revision_refs=source_revision_refs,
            ),
            execution=True,
        )

    def execute_run_from_latest_revisions(
        self,
        *,
        owner_id: str,
        workspace_id: str,
        run_id: str,
        created_at: str,
        completed_at: str,
    ) -> OperationResult[LocalRunRecords]:
        return self._run(
            lambda: self.repository.execute_and_persist_run(
                owner_id=owner_id,
                workspace_id=workspace_id,
                run_id=run_id,
                created_at=created_at,
                completed_at=completed_at,
            ),
            execution=True,
        )

    def list_run_summaries(
        self,
        owner_id: str,
        workspace_id: str,
    ) -> OperationResult[list[ProductRunSummaryPayload]]:
        return self._run(lambda: self.repository.list_run_summaries(owner_id, workspace_id))

    def get_latest_run_summary(
        self,
        owner_id: str,
        workspace_id: str,
    ) -> OperationResult[ProductRunSummaryPayload]:
        def latest() -> ProductRunSummaryPayload:
            summary = self.repository.latest_run_summary(owner_id, workspace_id)
            if summary is None:
                raise FileNotFoundError("latest run not found")
            return summary

        return self._run(latest)

    def get_run_detail(
        self,
        owner_id: str,
        workspace_id: str,
        run_id: str,
    ) -> OperationResult[ProductRunDetailPayload]:
        return self._run(lambda: self.repository.load_run_detail(owner_id, workspace_id, run_id))

    def get_latest_run_detail(self, owner_id: str, workspace_id: str) -> OperationResult[JsonObject]:
        def latest_detail() -> JsonObject:
            summary = self.repository.latest_run_summary(owner_id, workspace_id)
            if summary is None:
                raise FileNotFoundError("latest run not found")
            return {
                "run_summary": summary,
                "run_detail": self.repository.load_run_detail(owner_id, workspace_id, summary["run_id"]),
            }

        return self._run(latest_detail)

    def resolve_artifact_ref(
        self,
        *,
        owner_id: str,
        workspace_id: str,
        artifact_ref: ArtifactReference,
    ) -> OperationResult[ResolvedArtifact]:
        def resolve() -> ResolvedArtifact:
            path = self.repository.resolve_artifact_ref(
                owner_id=owner_id,
                workspace_id=workspace_id,
                artifact_ref=artifact_ref,
            )
            return ResolvedArtifact(
                artifact_ref=artifact_ref,
                path=path,
                media_type=artifact_ref["media_type"],
                exists=path.exists(),
            )

        return self._run(resolve)

    def _run(self, operation: Callable[[], T], *, execution: bool = False) -> OperationResult[T]:
        try:
            return OperationResult(status=RESULT_SUCCESS, value=operation())
        except FileNotFoundError as error:
            return self._failure(RESULT_NOT_FOUND, "not_found", str(error))
        except FileExistsError as error:
            return self._failure(RESULT_CONFLICT, "conflict", str(error))
        except (jsonschema.ValidationError, ValueError, KeyError) as error:
            if execution:
                return self._failure(RESULT_EXECUTION_FAILED, "execution_failed", str(error))
            return self._failure(RESULT_VALIDATION_ERROR, "validation_error", str(error))

    def _failure(self, status: ResultStatus, code: ErrorCode, message: str) -> OperationResult[Any]:
        return OperationResult(
            status=status,
            errors=(ServiceError(code=code, message=message),),
        )
