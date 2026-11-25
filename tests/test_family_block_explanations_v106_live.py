"""Live integration and rendered-HTML checks for ADR 0088 (core v106)."""

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
from packages.derivation.loader import DerivationSchemas
from packages.derivation.package_validation import validate_package
from packages.derivation.presentation_projection import validate_presentation_model
from tests import evidence_loader
from tests.helpers import current_core_returns as ccr
from tools.package_successor import load_corpus

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "packages" / "content" / "tax" / "2025"
EVIDENCE = ROOT / "docs" / "phases" / "engine-breadth" / "milestones" / "sale-block-explanations-evidence"
AUDIT_HARNESS = ROOT / "docs" / "phases" / "engine-breadth" / "milestones" / "sale-family-audit-evidence" / "audit_harness.py"
PAGE = ROOT / "packages" / "presentation" / "pages" / "citation-walk.v1.html"
DOM_CHECKER = ROOT / "docs" / "phases" / "engine-breadth" / "milestones" / "page-plain-words-evidence" / "check_page_dom.mjs"
P = "tax.us.2025."
QUESTION_CODES = {"CODE_W_ON_GAIN", "ADJUSTMENT_EXCEEDS_LOSS"}


def test_core_v106_passes_full_validate_package() -> None:
    v106 = json.loads((CONTENT / "package.core-calculations.v106.json").read_text(encoding="utf-8"))
    schemas = DerivationSchemas()
    corpus, _ = load_corpus(CONTENT)
    mapped = {(c["id"], c["version"]): c for c in corpus.values()}
    res = validate_package(v106, mapped, schemas)
    assert res.ok, res.issues


def _load_probe() -> tuple[Any, Any]:
    h = evidence_loader.load(AUDIT_HARNESS, "sbe_t1_audit_harness")
    probe = evidence_loader.load(EVIDENCE / "inventory_probe.py", "sbe_t1_inventory_probe")
    return h, probe


def _run_case(h: Any, core: Any, name: str, acts: list[dict[str, Any]]) -> dict[str, Any]:
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
            run_id=f"demo.sbe.t1.{core.version}.{name}",
            governance_pins=[],
            surface=surface,
            output_name="out.json",
        )
        assert outcome.refusal is None, (name, outcome.refusal)
        assert outcome.presentation_path is not None
        model: dict[str, Any] = json.loads(outcome.presentation_path.read_text(encoding="utf-8"))
        validate_presentation_model(model)
        return model


def _sched_snapshot(model: dict[str, Any]) -> dict[str, tuple[Any, Any]]:
    wanted = {
        P + "schedule-d.line-1b",
        P + "schedule-d.line-2",
        P + "schedule-d.line-3",
        P + "schedule-d.line-8b",
        P + "schedule-d.line-9",
        P + "schedule-d.line-10",
        P + "schedule-d.line-7",
        P + "schedule-d.line-15",
        P + "schedule-d.line-16",
        P + "schedule-d.line-21",
        P + "form1040.line-7a",
        P + "form1040.line-16",
    }
    return {
        s["field"]["id"]: (s["resolved"]["disposition"], s["resolved"].get("value"))
        for s in model["sections"]
        if s["field"]["id"] in wanted
    }


def test_v106_all_38_synthetic_cases_plain_reasons_and_question_links() -> None:
    h, probe = _load_probe()
    v105 = h.Core("v105", "v103", "v103")
    v106 = h.Core("v106", "v104", "v104")
    wording = json.loads((EVIDENCE / "wording.json").read_text(encoding="utf-8"))
    by_key = {(r["family_id"], r["block_code"]): r for r in wording["replacements"]}
    fam_prefix = {
        "w": P + "f1099b.covered-w-",
        "noncovered": P + "f1099b.noncovered-",
        "no1099b": P + "f8949.no1099b-",
        "codeb": P + "f1099b.code-b-",
    }

    for kind, term, variants in probe.CASES:
        fam_id = fam_prefix[kind] + term
        for variant in variants:
            cname = f"{kind}.{term}.{variant}"
            m105 = _run_case(h, v105, cname, probe.build_sale_case(kind, term, variant, v105, h, ccr))
            m106 = _run_case(h, v106, cname, probe.build_sale_case(kind, term, variant, v106, h, ccr))
            assert _sched_snapshot(m105) == _sched_snapshot(m106), cname

            blocked = [s for s in m106["sections"] if s["resolved"]["disposition"] == "blocked"]
            qgroups = m106.get("questionGroups", [])
            if variant == "valid_loss":
                assert blocked == [], cname
                assert qgroups == [], cname
                continue

            assert len(blocked) > 0, cname
            entry = by_key[(fam_id, variant)]
            sample = blocked[0]["resolved"]
            sentences = [r.get("sentence") for r in sample.get("reasons", [])]
            assert entry["new"] in sentences, (cname, sentences)
            if variant in QUESTION_CODES:
                assert len(qgroups) == 1, (cname, qgroups)
                assert len(sample.get("questionRefs", [])) == 1, (cname, sample)
                assert entry["fixing_question"] in sentences, (cname, sentences)
            else:
                assert qgroups == [], (cname, qgroups)
                assert sample.get("questionRefs", []) == [], (cname, sample)


def test_v106_two_sale_disambiguation_targets_only_violating_sale() -> None:
    h, probe = _load_probe()
    v106 = h.Core("v106", "v104", "v104")
    model = _run_case(h, v106, "two_sale", probe.build_two_sale_case(v106, h, ccr))
    qgroups = model.get("questionGroups", [])
    assert len(qgroups) == 1
    dumped = json.dumps(qgroups)
    assert "demo.sbe.two.bad.transaction" in dumped
    assert "demo.sbe.two.good" not in dumped


def test_v105_backward_compatibility_keeps_pinned_meaning_and_no_question() -> None:
    h, probe = _load_probe()
    v105 = h.Core("v105", "v103", "v103")
    wording = json.loads((EVIDENCE / "wording.json").read_text(encoding="utf-8"))
    by_key = {(r["family_id"], r["block_code"]): r for r in wording["replacements"]}

    m_w = _run_case(h, v105, "compat_w", probe.build_sale_case("w", "st", "CODE_W_ON_GAIN", v105, h, ccr))
    assert m_w.get("questionGroups", []) == []
    blocked_w = [s for s in m_w["sections"] if s["resolved"]["disposition"] == "blocked"]
    w_sentences = [r.get("sentence") for r in blocked_w[0]["resolved"].get("reasons", [])]
    assert by_key[(P + "f1099b.covered-w-st", "CODE_W_ON_GAIN")]["old"] in w_sentences

    m_hp = _run_case(h, v105, "compat_hp", probe.build_sale_case("noncovered", "lt", "HOLDING_PERIOD_MISMATCH", v105, h, ccr))
    assert m_hp.get("questionGroups", []) == []
    blocked_hp = [s for s in m_hp["sections"] if s["resolved"]["disposition"] == "blocked"]
    hp_sentences = [r.get("sentence") for r in blocked_hp[0]["resolved"].get("reasons", [])]
    assert by_key[(P + "f1099b.noncovered-lt", "HOLDING_PERIOD_MISMATCH")]["old"] in hp_sentences


def test_v106_missing_adjustment_row_surfaces_question_and_sibling_questions() -> None:
    """Missing .adjustment row triggers the new input-question and preserves sibling unanswered questions."""
    h, probe = _load_probe()
    v105 = h.Core("v105", "v103", "v103")
    v106 = h.Core("v106", "v104", "v104")

    def _acts(core: Any) -> list[dict[str, Any]]:
        acts = h.opened()
        acts = h.sale(acts, "w", "st", proceeds=2000, basis=3000, wash=0, tag="sbe.missing_adj", rows={"adjustment": None})
        acts = h.answer(acts, **h.honest({"w"}, loss=True, new_questions=False))
        # Leave taxpayer-over-65 unanswered (like v82 corpus) while answering statement answers.
        acts = h.say(acts, probe.NO_SALE_BOX4, "no", "sbe.missing_adj.nsb4", core.content)
        for ft, short in ((probe.BOX4, "box4"), (probe.BOX7, "box7")):
            body = h.bundle_for(ft, core.content)
            if body is not None and not {f["id"] for f in body["fact_types"]} & h._adopted(acts):
                h._add(acts, "bundle-adoption", {"bundle": body})
            fid = h.fact_id_for(ft, (("statement", "demo.sfa.sbe.missing_adj.statement"), ("tax-year", h.YEAR)))
            h._add(acts, "assertion", {"finding": h._attested(f"demo.sbe.missing_adj.{short}", fid, "no")})
        renumbered: list[dict[str, Any]] = h.renumber(acts)
        return renumbered

    m105 = _run_case(h, v105, "missing_adj_105", _acts(v105))
    m106 = _run_case(h, v106, "missing_adj_106", _acts(v106))

    qg106_ft = {g["answerTarget"]["factTypeId"] for g in m106.get("questionGroups", [])}
    assert P + "f1099b.covered-w-st-txn.adjustment" in qg106_ft
    assert P + "taxpayer-over-65" in qg106_ft

    sched7_105 = next(s for s in m105["sections"] if s["field"]["id"] == P + "schedule-d.line-7")
    sched7_106 = next(s for s in m106["sections"] if s["field"]["id"] == P + "schedule-d.line-7")
    assert sched7_105["resolved"].get("reasons", []) == []
    sentences_106 = [r.get("sentence") for r in sched7_106["resolved"].get("reasons", [])]
    assert any("wash-sale loss in box 1g" in s for s in sentences_106)


def test_live_v106_blocked_model_renders_cleanly_in_citation_walk_html() -> None:
    """ADR 0088 Decision 3 rendered-HTML check: two-reason blocked sale renders without leaks or SectionError."""
    h, probe = _load_probe()
    v106 = h.Core("v106", "v104", "v104")
    model = _run_case(h, v106, "render_code_w", probe.build_sale_case("w", "st", "CODE_W_ON_GAIN", v106, h, ccr))
    wording = json.loads((EVIDENCE / "wording.json").read_text(encoding="utf-8"))
    plain_code_w = next(
        r["new"]
        for r in wording["replacements"]
        if r["family_id"] == P + "f1099b.covered-w-st" and r["block_code"] == "CODE_W_ON_GAIN"
    )

    env = os.environ.copy()
    env["PPW_CHECK_DETAIL"] = "1"
    proc = subprocess.run(
        ["node", str(DOM_CHECKER), str(PAGE)],
        input=json.dumps({"key": "code_w", "model": model}) + "\n",
        text=True,
        capture_output=True,
        timeout=30,
        check=True,
        env=env,
    )
    report = json.loads(proc.stdout)["code_w"]
    assert report["section_errors"] == 0, report
    assert report["total_first_read_leaks"] == 0, report
    text = report["first_read_text"]
    assert plain_code_w in text
    assert "See the question and affected lines above" in text
    assert "What is the nondeductible wash-sale loss in box 1g of Form 1099-B" in text
