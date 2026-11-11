"""Regenerate the v70 entry seed from the committed complete-return source.

This scratch generator reads ``complete-core-return.jsonl`` (the acts the
production generator holds before it edits them) and applies those edits.
It imports no test module.
"""

from __future__ import annotations

import ast
import copy
import hashlib
import json
import sys
from pathlib import Path
from typing import Any


def _repo_root() -> Path:
    here = Path(__file__).resolve()
    for parent in here.parents:
        if (parent / "packages" / "kernel" / "__init__.py").is_file() and (
            parent / "tests"
        ).is_dir():
            return parent
    raise RuntimeError("repository root not found")


ROOT = _repo_root()
sys.path.insert(0, str(ROOT))

from packages.derivation.entry_loop import (  # noqa: E402
    CURRENT_CORE_ENTRY_FIXTURE,
    ENTRY_CORE_PROFILES,
    ENTRY_RUN_SCOPES,
    W2_EVIDENCE_ID,
    load_seed_acts,
)

SOURCE = Path(__file__).resolve().parent / "complete-core-return.jsonl"
HERE = Path(__file__).resolve().parent
W2_EMPLOYER_FROM_COMPLETE_RETURN = "demo.cgd.t2.employer"
W2_SLIP_FROM_COMPLETE_RETURN = "demo.cgd.t2.w2"
W2_EMPLOYER_FOR_ENTRY = "demo.presentation-l2.employer"
W2_SLIP_FOR_ENTRY = "demo.presentation-l2.w2"
W2_FAMILY = "tax.us.2025.w2"
W2_CLOSURE = "tax.us.2025.w2.source-closure|"
W2_BOX1 = "tax.us.2025.w2.box1-wages|"
_PATH_PARTS = {"Users", "tmp", "private", "var", "folders"}


def _assert_no_test_import(path: Path) -> None:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    for node in ast.walk(tree):
        names: list[str] = []
        if isinstance(node, ast.Import):
            names = [alias.name for alias in node.names]
        elif isinstance(node, ast.ImportFrom):
            names = [node.module or ""]
        for name in names:
            if name == "tests" or name.startswith("tests."):
                raise RuntimeError(f"{path.name} imports a test module")


def _assert_clean(text: str) -> None:
    norm = text.replace("\\", "/")
    if norm.startswith("/") or norm.startswith("~"):
        raise RuntimeError("generated text contains a machine path")
    parts = [part for part in norm.split("/") if part]
    if any(part in _PATH_PARTS for part in parts):
        raise RuntimeError("generated text contains a machine path")


def _document(value: Any) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode("utf-8")


def _replace_w2_identity(value: Any) -> Any:
    if isinstance(value, str):
        return value.replace(
            W2_EMPLOYER_FROM_COMPLETE_RETURN, W2_EMPLOYER_FOR_ENTRY
        ).replace(W2_SLIP_FROM_COMPLETE_RETURN, W2_SLIP_FOR_ENTRY)
    if isinstance(value, list):
        return [_replace_w2_identity(item) for item in value]
    if isinstance(value, dict):
        return {key: _replace_w2_identity(item) for key, item in value.items()}
    return value


def load_source() -> list[dict[str, Any]]:
    acts: list[dict[str, Any]] = []
    for line in SOURCE.read_text(encoding="utf-8").splitlines():
        if line:
            acts.append(json.loads(line))
    return acts


def seed_acts() -> list[dict[str, Any]]:
    """Return the deterministic v70 seed, with only W-2 Box 1 left open."""

    acts = _replace_w2_identity(load_source())
    result: list[dict[str, Any]] = []
    removed_box1 = 0
    removed_closure = 0
    for act in acts:
        payload = act.get("payload", {})
        member = payload.get("member") if isinstance(payload, dict) else None
        member_finding = member.get("finding") if isinstance(member, dict) else None
        finding = payload.get("finding") if isinstance(payload, dict) else None
        if (
            act.get("kind") == "member-transition"
            and isinstance(member_finding, dict)
            and str(member_finding.get("fact_id", "")).startswith(W2_BOX1)
        ):
            removed_box1 += 1
            continue
        if isinstance(finding, dict) and str(finding.get("fact_id", "")).startswith(
            W2_CLOSURE
        ):
            removed_closure += 1
            continue
        if act.get("kind") == "package-adoption" and isinstance(payload, dict):
            payload["scope"] = dict(ENTRY_RUN_SCOPES["v70"])
        result.append(act)

    if removed_box1 != 1 or removed_closure != 1:
        raise RuntimeError(
            "complete v70 return must have one W-2 Box 1 member and closure"
        )

    legacy_evidence = next(
        (
            act
            for act in load_seed_acts(ROOT)
            if act.get("kind") == "evidence-submitted"
            and act.get("payload", {}).get("evidence", {}).get("id") == W2_EVIDENCE_ID
        ),
        None,
    )
    if legacy_evidence is None:
        raise RuntimeError("legacy seed has no matching synthetic W-2 evidence")

    w2_entity_indexes = [
        index
        for index, act in enumerate(result)
        if act.get("kind") == "entity-introduced"
        and act.get("payload", {}).get("entity", {}).get("id") == W2_SLIP_FOR_ENTRY
    ]
    if len(w2_entity_indexes) != 1:
        raise RuntimeError("current-core seed must retain one W-2 slip entity")
    result.insert(w2_entity_indexes[0] + 1, copy.deepcopy(legacy_evidence))

    if not any(
        act.get("kind") == "horizon-genesis"
        and act.get("payload", {}).get("family", {}).get("id") == W2_FAMILY
        and act.get("payload", {}).get("horizon_id") == "demo.presentation-l2.w2.h0"
        for act in result
    ):
        raise RuntimeError("current-core seed lost the W-2 family start point")
    if any(
        isinstance(act.get("payload", {}).get("member"), dict)
        and str(act["payload"]["member"].get("finding", {}).get("fact_id", "")).startswith(
            W2_BOX1
        )
        for act in result
    ):
        raise RuntimeError("current-core seed still contains a W-2 Box 1 member")

    for revision, act in enumerate(result):
        act["committed_against"] = revision
    return result


def render_fixture_files() -> dict[str, bytes]:
    profile = ENTRY_CORE_PROFILES[("tax.us.2025.package.core-calculations", "v70")]
    evaluation = {
        "schema": "demo.entry-loop-evaluation.v1",
        "document": "Synthetic Form W-2 from Demo Workshop",
        "entries": {"initial": {"box1": 90000}, "correction": {"box1": 91000}},
        "expected_impact_lines": [
            field.line for field in profile.fields if field.group == "expected-impact"
        ],
        "untouched_comparison_lines": [
            field.line
            for field in profile.fields
            if field.group == "untouched-comparison"
        ],
    }
    seed_bytes = b"".join(
        json.dumps(act, sort_keys=True, separators=(",", ":")).encode("utf-8") + b"\n"
        for act in seed_acts()
    )
    return {
        "workspace/acts.jsonl": seed_bytes,
        "evaluation-w2.json": _document(evaluation),
    }


def _line_count(path: Path) -> int:
    return len(path.read_text(encoding="utf-8").splitlines())


def main() -> None:
    _assert_no_test_import(Path(__file__))
    rendered = render_fixture_files()
    fixture = ROOT / CURRENT_CORE_ENTRY_FIXTURE
    files: list[dict[str, Any]] = []
    matches = True
    for relative, contents in rendered.items():
        _assert_clean(contents.decode("utf-8"))
        committed = (fixture / relative).read_bytes()
        same = contents == committed
        matches = matches and same
        files.append(
            {
                "bytes": len(contents),
                "matches_committed": same,
                "relative": f"{CURRENT_CORE_ENTRY_FIXTURE}/{relative}",
                "sha256": hashlib.sha256(contents).hexdigest(),
            }
        )
    introduced = sorted(
        name
        for name in sys.modules
        if name == "tests" or name.startswith("tests.")
    )
    report = {
        "byte_test_still_catches": "source-fixture drift",
        "files": files,
        "generator_lines": _line_count(Path(__file__)),
        "imports_test_module": bool(introduced),
        "matches_committed_seed": matches,
        "shape": "source-fixture",
        "source_lines": _line_count(SOURCE),
        "test_modules_imported": introduced,
        "tests_touched": 0,
    }
    text = json.dumps(report, indent=2, sort_keys=True) + "\n"
    _assert_clean(text)
    (HERE / "result.json").write_text(text, encoding="utf-8")
    if not matches or introduced:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
