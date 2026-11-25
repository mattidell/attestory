"""Live integration and rendered-HTML checks for sale-collision-explanation."""

from __future__ import annotations

import copy
import json
import os
import subprocess
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any

from packages.derivation.live import live_coordinate_run
from packages.derivation.live_workspace import WorkspaceCapability
from packages.derivation.presentation_projection import validate_presentation_model
from packages.tax.loader import SALE_COLLISION_CATEGORY_LABELS
from tests import evidence_loader
from tests.helpers import current_core_returns as ccr

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "docs" / "phases" / "engine-breadth" / "milestones" / "sale-collision-explanation-evidence"
AUDIT_HARNESS = ROOT / "docs" / "phases" / "engine-breadth" / "milestones" / "sale-family-audit-evidence" / "audit_harness.py"
PAGE = ROOT / "packages" / "presentation" / "pages" / "citation-walk.v1.html"
DOM_CHECKER = ROOT / "docs" / "phases" / "engine-breadth" / "milestones" / "page-plain-words-evidence" / "check_page_dom.mjs"
P = "tax.us.2025."

KIND_TO_FAMILY_PREFIX = {
    "covered": P + "f1099b.covered-",
    "w": P + "f1099b.covered-w-",
    "noncovered": P + "f1099b.noncovered-",
    "codeb": P + "f1099b.code-b-",
}


def _load_probe() -> tuple[Any, Any]:
    h = evidence_loader.load(AUDIT_HARNESS, "sce_t1_audit_harness")
    probe = evidence_loader.load(EVIDENCE / "collision_probe.py", "sce_t1_collision_probe")
    return h, probe


def _run_model(h: Any, core: Any, name: str, acts: list[dict[str, Any]]) -> dict[str, Any]:
    surface = core.surface()
    finished = h._handover(
        h._finish(
            copy.deepcopy(acts),
            package_path=core.package_path,
            package_version=core.version,
            release_path=core.release_path,
            release_version=core.release_version,
            note=name,
        ),
        surface=surface,
        reconfirm=True,
    )
    with TemporaryDirectory() as tmp:
        outcome = live_coordinate_run(
            WorkspaceCapability(Path(tmp) / "L"),
            repo_root=ROOT,
            authoritative_acts=finished,
            workspace_revision=len(finished),
            run_scope={"jurisdiction": "us", "year": h.YEAR},
            scope_user=ccr.USER,
            request={"schema": "run-request.v1"},
            run_id=f"demo.sce.t1.{core.version}.{name}",
            governance_pins=[],
            surface=surface,
            output_name="out.json",
        )
        assert outcome.refusal is None, (name, outcome.refusal)
        assert outcome.presentation_path is not None
        model: dict[str, Any] = json.loads(outcome.presentation_path.read_text(encoding="utf-8"))
        validate_presentation_model(model)
        return model


def _expected_pair_sentence(kind_a: str, term_a: str, kind_b: str, term_b: str) -> str:
    fam_a = KIND_TO_FAMILY_PREFIX[kind_a] + term_a
    fam_b = KIND_TO_FAMILY_PREFIX[kind_b] + term_b
    first, second = sorted((
        SALE_COLLISION_CATEGORY_LABELS[fam_a],
        SALE_COLLISION_CATEGORY_LABELS[fam_b],
    ))
    return (
        f"The same sale was entered as both {first} and {second}; "
        "keep this sale in only one category and remove the duplicate entry."
    )


def test_v106_all_18_declared_pairs_and_controls_via_live_coordinate_run() -> None:
    _h, probe = _load_probe()
    results = probe.run_probe(ROOT, "v106", "v104", "v104")

    for kind_a, term_a, kind_b, term_b, excl_id in probe.DECLARED_PAIRS:
        key = f"pair.{kind_a}_{term_a}.vs.{kind_b}_{term_b}"
        entry = results[key]
        assert entry["blocked_sections_count"] == 32, (key, entry)
        assert entry["question_groups_count"] == 0, (key, entry)
        assert len(entry["member_validation_blocks"]) == 1, (key, entry)
        mv = entry["member_validation_blocks"][0]
        assert mv["missing"] == ["IDENTITY_EXCLUSIVITY_COLLISION", f"identity_exclusivity:{excl_id}"]
        expected_sentence = _expected_pair_sentence(kind_a, term_a, kind_b, term_b)
        assert entry["sample_reasons"] == [{"sentence": expected_sentence}], (key, entry)
        assert entry["distinct_reason_shapes"] == {
            json.dumps([{"sentence": expected_sentence}], sort_keys=True): 32
        }, (key, entry)
        assert "family" not in expected_sentence.lower()
        assert "tax.us." not in expected_sentence.lower()

    three_way = results["three_way.w_st.noncovered_st.codeb_st"]
    assert three_way["blocked_sections_count"] == 33
    assert three_way["question_groups_count"] == 0
    assert len(three_way["member_validation_blocks"]) == 2
    assert all(
        json.loads(shape) != []
        for shape in three_way["distinct_reason_shapes"]
    )

    mixed_q = results["mixed.w_st.vs.covered_st.unanswered_over_65"]
    assert mixed_q["blocked_sections_count"] == 35
    assert mixed_q["question_groups_count"] == 1
    assert mixed_q["question_groups"][0]["answerTarget"]["factTypeId"] == P + "taxpayer-over-65"
    expected_w_cov = _expected_pair_sentence("w", "st", "covered", "st")
    assert all(
        json.loads(shape) != []
        for shape in mixed_q["distinct_reason_shapes"]
    )
    assert any(
        len(json.loads(shape)) == 2
        and any(r["sentence"] == expected_w_cov for r in json.loads(shape))
        and any("born before January 2, 1961" in r["sentence"] for r in json.loads(shape))
        for shape in mixed_q["distinct_reason_shapes"]
    )

    mixed_w = results["mixed.w_st.vs.covered_st.code_w_on_gain"]
    assert mixed_w["blocked_sections_count"] == 32
    assert mixed_w["question_groups_count"] == 1
    assert mixed_w["question_groups"][0]["answerTarget"]["factTypeId"] == P + "f1099b.covered-w-st-txn.adjustment"
    mixed_sentences = [r["sentence"] for r in mixed_w["sample_reasons"]]
    assert expected_w_cov in mixed_sentences
    assert any("not a loss" in s for s in mixed_sentences)
    assert any("more than this sale's loss" in s for s in mixed_sentences)
    assert any("What is the nondeductible wash-sale loss in box 1g" in s for s in mixed_sentences)
    assert len(mixed_w["sample_question_refs"]) == 1

    control = results["control.w_st.vs.covered_st.distinct"]
    assert control["blocked_sections_count"] == 0
    assert control["question_groups_count"] == 0
    assert control["member_validation_blocks"] == []


def test_v105_backward_compatibility_keeps_empty_collision_reasons() -> None:
    h, probe = _load_probe()
    v105 = h.Core("v105", "v103", "v103")
    model = _run_model(
        h,
        v105,
        "compat_v105_collision",
        probe.build_collision_pair("w", "st", "covered", "st", v105, h, ccr),
    )
    blocked = [s for s in model["sections"] if s["resolved"]["disposition"] == "blocked"]
    assert len(blocked) == 32
    assert all(s["resolved"].get("reasons", []) == [] for s in blocked)


def test_v106_collision_models_render_cleanly_in_citation_walk_html() -> None:
    h, probe = _load_probe()
    v106 = h.Core("v106", "v104", "v104")
    cases = {
        "pair_w_covered": probe.build_collision_pair("w", "st", "covered", "st", v106, h, ccr),
        "three_way": probe.build_three_way_collision(v106, h, ccr),
        "mixed_code_w": probe.build_collision_pair("w", "st", "covered", "st", v106, h, ccr, gain_for_w=True),
    }
    payload_lines = [
        json.dumps({"key": key, "model": _run_model(h, v106, f"dom_{key}", acts)})
        for key, acts in cases.items()
    ]
    env = os.environ.copy()
    env["PPW_CHECK_DETAIL"] = "1"
    proc = subprocess.run(
        ["node", str(DOM_CHECKER), str(PAGE)],
        input="\n".join(payload_lines) + "\n",
        text=True,
        capture_output=True,
        timeout=60,
        check=True,
        env=env,
    )
    reports = json.loads(proc.stdout)
    expected_by_key = {
        "pair_w_covered": _expected_pair_sentence("w", "st", "covered", "st"),
        "three_way": _expected_pair_sentence("w", "st", "noncovered", "st"),
        "mixed_code_w": _expected_pair_sentence("w", "st", "covered", "st"),
    }
    for key, expected_sentence in expected_by_key.items():
        rep = reports[key]
        assert rep["section_errors"] == 0, (key, rep)
        assert rep["total_first_read_leaks"] == 0, (key, rep)
        assert expected_sentence in rep["first_read_text"], (key, rep)
    assert "See the question and affected lines above" in reports["mixed_code_w"]["first_read_text"]
    assert "What is the nondeductible wash-sale loss in box 1g" in reports["mixed_code_w"]["first_read_text"]
