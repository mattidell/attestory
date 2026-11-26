"""Live checks for core v108 (code-b-basis-sentence): only the four code B wash-sale sentences moved.

Each code B synthetic sale case from the ADR 0088 inventory (short-term and
long-term: a valid loss and the four blocks) runs on v107 and v108 through
live_coordinate_run. Every line's disposition and value and every question
link are the same. A code B wash-sale block (ADJUSTMENT_EXCEEDS_LOSS or
CODE_W_ON_GAIN) shows the v108 sentence, never the v107 one, and asks the
same question; the other code B blocks read exactly as on v107. The rendered
page check runs a v108 code B CODE_W_ON_GAIN model through citation-walk.v1.html.
"""

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
MILESTONES = ROOT / "docs" / "phases" / "engine-breadth" / "milestones"
INVENTORY = MILESTONES / "sale-block-explanations-evidence" / "inventory_probe.py"
WORDING = MILESTONES / "code-b-basis-sentence-evidence" / "wording.json"
AUDIT_HARNESS = MILESTONES / "sale-family-audit-evidence" / "audit_harness.py"
PAGE = ROOT / "packages" / "presentation" / "pages" / "citation-walk.v1.html"
DOM_CHECKER = MILESTONES / "page-plain-words-evidence" / "check_page_dom.mjs"
P = "tax.us.2025."
WASH = {"CODE_W_ON_GAIN", "ADJUSTMENT_EXCEEDS_LOSS"}


def _wording() -> dict[tuple[str, str], dict[str, Any]]:
    rows = json.loads(WORDING.read_text(encoding="utf-8"))["replacements"]
    return {(r["family_id"], r["block_code"]): r for r in rows}


def _load() -> tuple[Any, Any]:
    h = evidence_loader.load(AUDIT_HARNESS, "cbbs_t1_audit_harness")
    probe = evidence_loader.load(INVENTORY, "cbbs_t1_inventory_probe")
    return h, probe


def _run(h: Any, core: Any, name: str, acts: list[dict[str, Any]]) -> dict[str, Any]:
    surface = core.surface()
    finished = h._handover(
        h._finish(copy.deepcopy(acts), package_path=core.package_path, package_version=core.version,
                  release_path=core.release_path, release_version=core.release_version, note=name),
        surface=surface, reconfirm=True,
    )
    with TemporaryDirectory() as tmp:
        outcome = live_coordinate_run(
            WorkspaceCapability(Path(tmp) / "L"), repo_root=ROOT, authoritative_acts=finished,
            workspace_revision=len(finished), run_scope={"jurisdiction": "us", "year": h.YEAR},
            scope_user=ccr.USER, request={"schema": "run-request.v1"},
            run_id=f"demo.cbbs.t1.{name}", governance_pins=[], surface=surface, output_name="out.json",
        )
        assert outcome.refusal is None, (name, outcome.refusal)
        assert outcome.presentation_path is not None
        model: dict[str, Any] = json.loads(outcome.presentation_path.read_text(encoding="utf-8"))
        validate_presentation_model(model)
        return model


def _results(model: dict[str, Any]) -> dict[str, tuple[Any, Any]]:
    return {s["field"]["id"]: (s["resolved"]["disposition"], s["resolved"].get("value")) for s in model["sections"]}


def _links(model: dict[str, Any]) -> dict[str, list[tuple[str, tuple[str, ...]]]]:
    groups = {g["id"]: g["answerTarget"]["factTypeId"] for g in model.get("questionGroups", [])}
    out: dict[str, list[tuple[str, tuple[str, ...]]]] = {}
    for s in model["sections"]:
        reasons = [r.get("sentence") for r in s["resolved"].get("reasons", [])]
        out[s["field"]["id"]] = sorted(
            (groups[ref["groupId"]], tuple(sorted(str(reasons[i]) for i in ref["reasonIndices"])))
            for ref in s["resolved"].get("questionRefs", [])
        )
    return out


def _sentences(model: dict[str, Any]) -> list[list[Any]]:
    return [sorted(str(r.get("sentence")) for r in s["resolved"].get("reasons", [])) for s in model["sections"]]


def test_core_v108_passes_full_validate_package() -> None:
    v108 = json.loads((CONTENT / "package.core-calculations.v108.json").read_text(encoding="utf-8"))
    corpus, _ = load_corpus(CONTENT)
    res = validate_package(v108, {(c["id"], c["version"]): c for c in corpus.values()}, DerivationSchemas())
    assert res.ok, res.issues


def test_v108_code_b_cases_keep_every_result_and_link_and_show_the_correct_basis_sentence() -> None:
    h, probe = _load()
    v107 = h.Core("v107", "v105", "v105")
    v108 = h.Core("v108", "v106", "v106")
    wording = _wording()
    checked = 0
    for kind, term, variants in probe.CASES:
        if kind != "codeb":
            continue
        family = f"{P}f1099b.code-b-{term}"
        for variant in variants:
            name = f"{kind}.{term}.{variant}"
            m107 = _run(h, v107, "v107." + name, probe.build_sale_case(kind, term, variant, v107, h, ccr))
            m108 = _run(h, v108, "v108." + name, probe.build_sale_case(kind, term, variant, v108, h, ccr))
            assert _results(m107) == _results(m108), name
            assert [g["question"] for g in m107.get("questionGroups", [])] == [
                g["question"] for g in m108.get("questionGroups", [])], name
            assert [g["answerTarget"] for g in m107.get("questionGroups", [])] == [
                g["answerTarget"] for g in m108.get("questionGroups", [])], name
            row = wording.get((family, variant))
            if row is None:
                assert _sentences(m107) == _sentences(m108), name
                assert _links(m107) == _links(m108), name
                checked += 1
                continue
            assert variant in WASH
            # A sale with no loss trips both wash-sale blocks, so every declared sentence is renamed.
            rename = {r["old"]: r["new"] for r in wording.values()}
            assert _links(m108) == {
                line: sorted((t, tuple(sorted(rename.get(s, s) for s in sents))) for t, sents in links)
                for line, links in _links(m107).items()
            }, name
            assert _sentences(m108) == [sorted(rename.get(s, s) for s in reasons) for reasons in _sentences(m107)]
            blocked = [s for s in m108["sections"] if s["resolved"]["disposition"] == "blocked"]
            assert blocked, name
            for section in blocked:
                shown = [r.get("sentence") for r in section["resolved"].get("reasons", [])]
                assert row["new"] in shown and row["old"] not in shown, (name, shown)
            assert len(m108.get("questionGroups", [])) == 1, name
            checked += 1
    assert checked == 10


def test_live_v108_code_b_wash_sale_block_renders_the_correct_basis_sentence() -> None:
    h, probe = _load()
    v108 = h.Core("v108", "v106", "v106")
    model = _run(h, v108, "render.code_b", probe.build_sale_case("codeb", "st", "CODE_W_ON_GAIN", v108, h, ccr))
    row = _wording()[(f"{P}f1099b.code-b-st", "CODE_W_ON_GAIN")]
    env = os.environ.copy()
    env["PPW_CHECK_DETAIL"] = "1"
    proc = subprocess.run(
        ["node", str(DOM_CHECKER), str(PAGE)],
        input=json.dumps({"key": "code_b", "model": model}) + "\n",
        text=True, capture_output=True, timeout=30, check=True, env=env,
    )
    report = json.loads(proc.stdout)["code_b"]
    assert report["section_errors"] == 0, report
    assert report["total_first_read_leaks"] == 0, report
    text = report["first_read_text"]
    assert row["new"] in text
    assert row["old"] not in text
    assert "See the question and affected lines above" in text
