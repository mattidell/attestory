"""Generate a synthetic v70 W-2 entry seed with only Box 1 left open.

The seed starts from ``complete-core-return.jsonl`` beside the fixture.
That file was produced once from the current test helpers: a copy of
``tests.helpers.current_core_returns.base_return``, finished by
``tests.test_refund_or_amount_owed_track1._finish`` against the v70 core
package and the v68 worksheet release, resolved to an adopted surface, then
handed over by ``tests.test_form_1099_k_income._handover``. Those are the
acts this tool receives before it replaces the W-2 identity, drops Box 1,
or splices legacy evidence. Refreshing the file is deliberate. The
production entry runtime reads only the generated JSONL fixture; it never
imports this tool.
"""

from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any

from packages.derivation.entry_loop import (
    ENTRY_CORE_PROFILES,
    CURRENT_CORE_ENTRY_FIXTURE,
    ENTRY_RUN_SCOPES,
    W2_EVIDENCE_ID,
    load_seed_acts,
)


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / CURRENT_CORE_ENTRY_FIXTURE
SOURCE = OUT / "complete-core-return.jsonl"
W2_EMPLOYER_FROM_COMPLETE_RETURN = "demo.cgd.t2.employer"
W2_SLIP_FROM_COMPLETE_RETURN = "demo.cgd.t2.w2"
W2_EMPLOYER_FOR_ENTRY = "demo.presentation-l2.employer"
W2_SLIP_FOR_ENTRY = "demo.presentation-l2.w2"
W2_FAMILY = "tax.us.2025.w2"
W2_CLOSURE = "tax.us.2025.w2.source-closure|"
W2_BOX1 = "tax.us.2025.w2.box1-wages|"


def _document(value: Any) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode("utf-8")


def _replace_w2_identity(value: Any) -> Any:
    if isinstance(value, str):
        return (
            value.replace(W2_EMPLOYER_FROM_COMPLETE_RETURN, W2_EMPLOYER_FOR_ENTRY)
            .replace(W2_SLIP_FROM_COMPLETE_RETURN, W2_SLIP_FOR_ENTRY)
        )
    if isinstance(value, list):
        return [_replace_w2_identity(item) for item in value]
    if isinstance(value, dict):
        return {key: _replace_w2_identity(item) for key, item in value.items()}
    return value


def _load_complete_core_return() -> list[dict[str, Any]]:
    acts: list[dict[str, Any]] = []
    for line in SOURCE.read_text(encoding="utf-8").splitlines():
        if line:
            acts.append(json.loads(line))
    return acts


def seed_acts() -> list[dict[str, Any]]:
    """Return the deterministic v70 seed, with only W-2 Box 1 left open."""

    acts = _replace_w2_identity(_load_complete_core_return())
    result: list[dict[str, Any]] = []
    removed_box1 = 0
    removed_closure = 0
    for act in acts:
        payload = act.get("payload", {})
        member = payload.get("member") if isinstance(payload, dict) else None
        member_finding = (
            member.get("finding") if isinstance(member, dict) else None
        )
        finding = payload.get("finding") if isinstance(payload, dict) else None
        if (
            act.get("kind") == "member-transition"
            and isinstance(member_finding, dict)
            and str(member_finding.get("fact_id", "")).startswith(W2_BOX1)
        ):
            removed_box1 += 1
            continue
        if (
            isinstance(finding, dict)
            and str(finding.get("fact_id", "")).startswith(W2_CLOSURE)
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
            and act.get("payload", {}).get("evidence", {}).get("id")
            == W2_EVIDENCE_ID
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
        and str(
            act["payload"]["member"].get("finding", {}).get("fact_id", "")
        ).startswith(W2_BOX1)
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
        json.dumps(act, sort_keys=True, separators=(",", ":")).encode("utf-8")
        + b"\n"
        for act in seed_acts()
    )
    return {
        "workspace/acts.jsonl": seed_bytes,
        "evaluation-w2.json": _document(evaluation),
    }


def main() -> None:
    for relative, contents in render_fixture_files().items():
        target = OUT / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(contents)
    print(f"current-core entry fixture: {len(seed_acts())} acts")


if __name__ == "__main__":
    main()
