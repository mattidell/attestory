"""Regenerate the wholly synthetic First Real Return Slice Track 1 corpus.

The corpus is constructed solely from the published schema contracts in this
repository.  It neither reads nor accepts a live workspace or source document.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent / "packages" / "sample_data" / "frrs_t1"
_GENERATOR_PATH = Path(__file__).resolve()


def _document(value: Any) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode("utf-8")


def _corpus() -> dict[str, Any]:
    return {
        "examples/act-assertion.v2.json": {
            "finding": {
                "schema": "finding.v2", "id": "demo.finding-2", "fact_id": "demo.fact-1",
                "value": 100, "basis": "documentary", "evidence_ids": ["demo.evidence-1"],
            },
        },
        "examples/act-contribution.v1.json": {
            "contribution": {
                "schema": "contribution.v1", "id": "demo.contribution-1",
                "evidence_id": "demo.evidence-1", "content": {},
            },
        },
        "examples/act-member-transition.v2.json": {
            "family": {"id": "demo.family", "version": "v1"}, "scope": {"year": "2025"},
            "member": {"action": "remove", "fact_id": "demo.fact-1"},
            "successor": {"id": "demo.successor-1", "predecessor": "demo.predecessor-1"},
        },
        "examples/classification.v1.json": {
            "schema": "classification.v1", "decision": "MAY_CROSS",
            "kind": "independently-constructed synthetic fixture",
            "reason": "Generated from public schema contracts only.",
        },
        "examples/contribution-record.v1.json": {
            "schema": "contribution-record.v1", "record_id": "demo.record-1",
            "contribution_id": "demo.contribution-1", "phase": "completed",
            "workspace_revision": 1, "stop_reason": "completed",
            "facts_asserted": [{"fact_id": "demo.fact-1", "finding_id": "demo.finding-1", "act_id": "demo.act-1"}],
        },
        "examples/contribution.v1.json": {
            "schema": "contribution.v1", "id": "demo.contribution-1",
            "evidence_id": "demo.evidence-1", "content": {"example": "synthetic"},
        },
        "examples/finding.v2.json": {
            "schema": "finding.v2", "id": "demo.finding-2", "fact_id": "demo.fact-1",
            "value": 100, "basis": "documentary", "evidence_ids": ["demo.evidence-1"],
            "contribution_id": "demo.contribution-1",
        },
        "examples/reserved-illustration-domain.v1.json": {
            "schema": "reserved-illustration-domain.v1", "examples": ["example.invalid"],
        },
        "examples/run-request.v1.json": {"schema": "run-request.v1"},
        "negatives/act-assertion.v2.v1-finding.json": {
            "finding": {
                "schema": "finding.v1", "id": "demo.finding-2", "fact_id": "demo.fact-1",
                "value": 100, "basis": "documentary", "evidence_ids": ["demo.evidence-1"],
            },
        },
        "negatives/act-contribution.v1.bad-schema.json": {
            "contribution": {"schema": "contribution.v2"},
        },
        "negatives/act-member-transition.v2.bad-scope.json": {
            "family": {"id": "demo.family", "version": "v1"}, "scope": {},
            "member": {"action": "remove", "fact_id": "demo.fact-1"},
            "successor": {"id": "demo.successor-1", "predecessor": "demo.predecessor-1"},
        },
        "negatives/classification.v1.never-with-kind.json": {
            "schema": "classification.v1", "decision": "NEVER_CROSSES",
            "kind": "public-origin code",
        },
        "negatives/contribution-record.v1.invalid-started.json": {
            "schema": "contribution-record.v1", "record_id": "demo.record-1",
            "contribution_id": "demo.contribution-1", "phase": "started",
            "workspace_revision": 1, "stop_reason": "completed",
        },
        "negatives/contribution.v1.missing-evidence.json": {
            "schema": "contribution.v1", "id": "demo.contribution-1", "content": {},
        },
        "negatives/finding.v2.bad-basis.json": {
            "schema": "finding.v2", "id": "demo.finding-2", "fact_id": "demo.fact-1",
            "value": 100, "basis": "invalid-basis", "evidence_ids": ["demo.evidence-1"],
        },
        "negatives/fixture-provenance-manifest.v1.missing-attestation.json": {
            "schema": "fixture-provenance-manifest.v1",
            "generator": {"id": "demo.generator", "version": "v1", "digest": "a" * 64},
            "grammar_digest": "b" * 64, "profile_digest": "c" * 64, "seed": "demo-seed",
            "constraints": {}, "input_kinds": ["public schema contract"], "artifacts": [
                {"path": "examples/run-request.v1.json", "sha256": "d" * 64}
            ],
        },
        "negatives/reserved-illustration-domain.v1.extra-prop.json": {
            "schema": "reserved-illustration-domain.v1", "examples": ["example.invalid"], "extra": "bad",
        },
        "negatives/run-request.v1.with-value.json": {"schema": "run-request.v1", "some_value": 1},
    }


def render_fixture_files() -> dict[str, bytes]:
    """Return the complete fixture corpus from public, versioned generator inputs."""
    documents = _corpus()
    rendered = {path: _document(value) for path, value in documents.items()}
    artifacts = [
        {"path": path, "sha256": hashlib.sha256(rendered[path]).hexdigest()}
        for path in sorted(rendered)
    ]
    manifest = {
        "schema": "fixture-provenance-manifest.v1",
        "generator": {
            "id": "tools.generate_frrs_t1_fixtures",
            "version": "v1",
            "digest": hashlib.sha256(_GENERATOR_PATH.read_bytes()).hexdigest(),
        },
        "grammar_digest": hashlib.sha256(b"frrs-t1-public-schema-grammar.v1").hexdigest(),
        "profile_digest": hashlib.sha256(b"frrs-t1-synthetic-contract-profile.v1").hexdigest(),
        "seed": "frrs-t1-schema-contract-fixtures-v1",
        "constraints": {
            "construction": "public schemas and accepted contract text only",
            "live_document_input": False,
            "reserved_value_domain": "demo identifiers and small integers",
        },
        "input_kinds": ["public schema contracts", "accepted repository contracts"],
        "artifacts": artifacts,
        "attestation_no_live_data": True,
    }
    rendered["examples/fixture-provenance-manifest.v1.json"] = _document(manifest)
    return rendered


def main() -> None:
    for relative_path, contents in render_fixture_files().items():
        target = ROOT / relative_path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(contents)


if __name__ == "__main__":
    main()
