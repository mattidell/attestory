"""Unit tests for cross-family sale identity-exclusivity collision explanations."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from packages.derivation.presentation_projection import _closure_question_reasons
from packages.tax.loader import (
    IDENTITY_EXCLUSIVITY_COLLISION_CODE,
    IDENTITY_EXCLUSIVITY_COLLISION_SENTENCE,
    SALE_COLLISION_CATEGORY_LABELS,
    explains_identity_exclusivity_collision,
)

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "packages" / "content" / "tax" / "2025"
CORE = "tax.us.2025.package.core-calculations"
P = "tax.us.2025."


def _v106_exclusivity_families() -> list[dict[str, Any]]:
    pkg = json.loads((CONTENT / "package.core-calculations.v106.json").read_text(encoding="utf-8"))
    by_id_ver: dict[tuple[str, str], dict[str, Any]] = {}
    for path in sorted(CONTENT.glob("family.*.json")):
        doc = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(doc.get("id"), str) and isinstance(doc.get("version"), str):
            by_id_ver[(doc["id"], doc["version"])] = doc
    out: list[dict[str, Any]] = []
    for member in pkg["members"]:
        if member.get("role") == "source-family":
            doc = by_id_ver[(str(member["id"]), str(member["version"]))]
            if doc.get("identity_exclusivity"):
                out.append(doc)
    return out


def test_explains_identity_exclusivity_collision_version_gate() -> None:
    assert explains_identity_exclusivity_collision(CORE, "v81") is False
    assert explains_identity_exclusivity_collision(CORE, "v105") is False
    assert explains_identity_exclusivity_collision(CORE, "v106") is True
    assert explains_identity_exclusivity_collision(CORE, "v107") is True
    assert explains_identity_exclusivity_collision("tax.us.2025.package.other", "v106") is False
    assert explains_identity_exclusivity_collision(CORE, "v106-draft") is False
    assert explains_identity_exclusivity_collision(CORE, "106") is False


def test_all_v106_exclusivity_families_carry_plain_labels() -> None:
    families = _v106_exclusivity_families()
    assert len(families) == 6
    total_rules = 0
    for family in families:
        fam_id = str(family["id"])
        assert fam_id in SALE_COLLISION_CATEGORY_LABELS
        for excl in family["identity_exclusivity"]:
            total_rules += 1
            counterpart_id = str(excl["incompatible_family"]["id"])
            assert counterpart_id in SALE_COLLISION_CATEGORY_LABELS
    assert total_rules == 18

    for text in [IDENTITY_EXCLUSIVITY_COLLISION_SENTENCE, *SALE_COLLISION_CATEGORY_LABELS.values()]:
        lowered = text.lower()
        assert "family" not in lowered
        assert "tax.us." not in lowered
        assert "identity_" not in lowered
        assert "synthesized" not in lowered
        assert "member-validation" not in lowered


def test_symmetric_mutual_exclusivity_deduplicates_to_one_bullet() -> None:
    members = [
        {
            "schema": "source-family.v2",
            "id": P + "f1099b.covered-w-st",
            "version": "v2",
            "identity_exclusivity": [{
                "id": P + "block.covered-w.identity-key-collision",
                "incompatible_family": {"id": P + "f1099b.covered-st", "version": "v1"},
                "components": [{"fact_id_bound_key": "transaction"}],
            }],
        },
        {
            "schema": "source-family.v2",
            "id": P + "f1099b.covered-st",
            "version": "v1",
            "identity_exclusivity": [{
                "id": P + "block.covered-st.excludes.covered-w-st",
                "incompatible_family": {"id": P + "f1099b.covered-w-st", "version": "v2"},
                "components": [{"fact_id_bound_key": "transaction"}],
            }],
        },
    ]
    by_symbol = {
        P + "f1099b.covered-w-st.member-validation": [{
            "artifact_id": P + "f1099b.covered-w-st.member-validation.synthesized",
            "disposition": "blocked",
            "code": "DEPENDENCY_INVALID",
            "missing": [
                IDENTITY_EXCLUSIVITY_COLLISION_CODE,
                f"identity_exclusivity:{P}block.covered-w.identity-key-collision",
            ],
        }],
        P + "f1099b.covered-st.member-validation": [{
            "artifact_id": P + "f1099b.covered-st.member-validation.synthesized",
            "disposition": "blocked",
            "code": "DEPENDENCY_INVALID",
            "missing": [
                IDENTITY_EXCLUSIVITY_COLLISION_CODE,
                f"identity_exclusivity:{P}block.covered-st.excludes.covered-w-st",
            ],
        }],
    }
    row = {
        "artifact_id": P + "rule.test-consumer",
        "disposition": "blocked",
        "code": "DEPENDENCY_ABSENT",
        "missing": [
            P + "f1099b.covered-w-st.member-validation",
            P + "f1099b.covered-st.member-validation",
        ],
    }
    reasons = _closure_question_reasons(
        row,
        resolved_members=members,
        by_symbol=by_symbol,
        later_any_arm_refs=True,
        collision_sentence=IDENTITY_EXCLUSIVITY_COLLISION_SENTENCE,
        collision_category_labels=SALE_COLLISION_CATEGORY_LABELS,
    )
    assert reasons == [{
        "sentence": (
            "The same sale was entered as both a short-term covered Form 1099-B sale "
            "(no adjustment) and a short-term covered Form 1099-B wash sale (code W); "
            "keep this sale in only one category and remove the duplicate entry."
        ),
    }]


def test_component_missing_and_family_absent_stay_fail_closed() -> None:
    members = [
        {
            "schema": "source-family.v2",
            "id": P + "f1099b.covered-w-st",
            "version": "v2",
            "identity_exclusivity": [{
                "id": P + "block.covered-w.identity-key-collision",
                "incompatible_family": {"id": P + "f1099b.covered-st", "version": "v1"},
                "components": [{"fact_id_bound_key": "transaction"}],
            }],
        }
    ]
    for missing_tokens in (
        ["IDENTITY_COMPONENT_MISSING", f"identity_exclusivity:{P}block.covered-w.identity-key-collision"],
        [
            "IDENTITY_EXCLUSIVITY_FAMILY_ABSENT",
            f"identity_exclusivity:{P}block.covered-w.identity-key-collision:{P}f1099b.covered-st",
        ],
    ):
        reasons = _closure_question_reasons(
            {
                "artifact_id": P + "rule.test-consumer",
                "disposition": "blocked",
                "code": "DEPENDENCY_ABSENT",
                "missing": [P + "f1099b.covered-w-st.member-validation"],
            },
            resolved_members=members,
            by_symbol={
                P + "f1099b.covered-w-st.member-validation": [{
                    "artifact_id": P + "f1099b.covered-w-st.member-validation.synthesized",
                    "disposition": "blocked",
                    "code": "DEPENDENCY_INVALID",
                    "missing": missing_tokens,
                }]
            },
            later_any_arm_refs=True,
            collision_sentence=IDENTITY_EXCLUSIVITY_COLLISION_SENTENCE,
            collision_category_labels=SALE_COLLISION_CATEGORY_LABELS,
        )
        assert reasons == [], missing_tokens


def test_unmapped_family_and_bare_collision_fall_back_to_generic_sentence() -> None:
    for missing_tokens in (
        [IDENTITY_EXCLUSIVITY_COLLISION_CODE, f"identity_exclusivity:{P}block.unmapped"],
        [IDENTITY_EXCLUSIVITY_COLLISION_CODE],
    ):
        reasons = _closure_question_reasons(
            {
                "artifact_id": P + "rule.test-consumer",
                "disposition": "blocked",
                "code": "DEPENDENCY_ABSENT",
                "missing": [P + "f1099b.unmapped.member-validation"],
            },
            resolved_members=[],
            by_symbol={
                P + "f1099b.unmapped.member-validation": [{
                    "artifact_id": P + "f1099b.unmapped.member-validation.synthesized",
                    "disposition": "blocked",
                    "code": "DEPENDENCY_INVALID",
                    "missing": missing_tokens,
                }]
            },
            later_any_arm_refs=True,
            collision_sentence=IDENTITY_EXCLUSIVITY_COLLISION_SENTENCE,
            collision_category_labels=SALE_COLLISION_CATEGORY_LABELS,
        )
        assert reasons == [{"sentence": IDENTITY_EXCLUSIVITY_COLLISION_SENTENCE}]


def test_pre_v106_gate_off_leaves_collision_empty() -> None:
    members = _v106_exclusivity_families()
    reasons = _closure_question_reasons(
        {
            "artifact_id": P + "rule.test-consumer",
            "disposition": "blocked",
            "code": "DEPENDENCY_ABSENT",
            "missing": [P + "f1099b.covered-w-st.member-validation"],
        },
        resolved_members=members,
        by_symbol={
            P + "f1099b.covered-w-st.member-validation": [{
                "artifact_id": P + "f1099b.covered-w-st.member-validation.synthesized",
                "disposition": "blocked",
                "code": "DEPENDENCY_INVALID",
                "missing": [
                    IDENTITY_EXCLUSIVITY_COLLISION_CODE,
                    f"identity_exclusivity:{P}block.covered-w.identity-key-collision",
                ],
            }]
        },
        later_any_arm_refs=True,
    )
    assert reasons == []


def test_shared_covered_w_excl_id_distinguishes_short_and_long_term() -> None:
    members = _v106_exclusivity_families()
    shared_excl = f"identity_exclusivity:{P}block.covered-w.identity-key-collision"
    st_reasons = _closure_question_reasons(
        {
            "artifact_id": P + "rule.test-st",
            "disposition": "blocked",
            "code": "DEPENDENCY_ABSENT",
            "missing": [P + "f1099b.covered-w-st.member-validation"],
        },
        resolved_members=members,
        by_symbol={
            P + "f1099b.covered-w-st.member-validation": [{
                "artifact_id": P + "f1099b.covered-w-st.member-validation.synthesized",
                "disposition": "blocked",
                "code": "DEPENDENCY_INVALID",
                "missing": [IDENTITY_EXCLUSIVITY_COLLISION_CODE, shared_excl],
            }]
        },
        later_any_arm_refs=True,
        collision_sentence=IDENTITY_EXCLUSIVITY_COLLISION_SENTENCE,
        collision_category_labels=SALE_COLLISION_CATEGORY_LABELS,
    )
    lt_reasons = _closure_question_reasons(
        {
            "artifact_id": P + "rule.test-lt",
            "disposition": "blocked",
            "code": "DEPENDENCY_ABSENT",
            "missing": [P + "f1099b.covered-w-lt.member-validation"],
        },
        resolved_members=members,
        by_symbol={
            P + "f1099b.covered-w-lt.member-validation": [{
                "artifact_id": P + "f1099b.covered-w-lt.member-validation.synthesized",
                "disposition": "blocked",
                "code": "DEPENDENCY_INVALID",
                "missing": [IDENTITY_EXCLUSIVITY_COLLISION_CODE, shared_excl],
            }]
        },
        later_any_arm_refs=True,
        collision_sentence=IDENTITY_EXCLUSIVITY_COLLISION_SENTENCE,
        collision_category_labels=SALE_COLLISION_CATEGORY_LABELS,
    )
    assert st_reasons != lt_reasons
    assert "short-term" in st_reasons[0]["sentence"]
    assert "long-term" in lt_reasons[0]["sentence"]
