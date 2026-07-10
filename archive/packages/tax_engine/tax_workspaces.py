import json
from dataclasses import dataclass
from pathlib import Path

import jsonschema


ROOT = Path(__file__).resolve().parents[2]
TAX_WORKSPACE_SCHEMA_PATH = ROOT / "packages" / "schemas" / "tax-workspace.schema.json"


@dataclass(frozen=True)
class TaxWorkspace:
    workspace_id: str
    label: str
    tax_year: int
    jurisdiction: str
    source_document_draft_paths: tuple[Path, ...]


def validate_tax_workspace_payload(payload: dict) -> None:
    schema = json.loads(TAX_WORKSPACE_SCHEMA_PATH.read_text())
    jsonschema.validate(payload, schema)


def load_tax_workspace_payload(path: Path) -> dict:
    payload = json.loads(path.read_text())
    validate_tax_workspace_payload(payload)
    return payload


def resolve_workspace_path(workspace_path: Path, referenced_path: str) -> Path:
    path = Path(referenced_path)
    if path.is_absolute():
        return path
    return (workspace_path.parent / path).resolve()


def tax_workspace_from_payload(workspace_path: Path, payload: dict) -> TaxWorkspace:
    return TaxWorkspace(
        workspace_id=payload["workspace_id"],
        label=payload["label"],
        tax_year=payload["tax_year"],
        jurisdiction=payload["jurisdiction"],
        source_document_draft_paths=tuple(
            resolve_workspace_path(workspace_path, draft["path"])
            for draft in payload["source_document_drafts"]
        ),
    )


def load_tax_workspace(path: Path) -> TaxWorkspace:
    return tax_workspace_from_payload(path, load_tax_workspace_payload(path))
