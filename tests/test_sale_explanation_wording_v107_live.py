"""Live checks for core v107 (sale-explanation-wording): only the words moved.

Each of the 38 synthetic sale cases from the ADR 0088 inventory runs on v106
and v107 through live_coordinate_run. The Schedule D and Form 1040 results,
every line's disposition and every question link are the same; a blocked
sale shows the v107 explanation, and a wash-sale block still asks its
question in the v107 words. The rendered page check runs the saved v107
model through citation-walk.v1.html.
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
WORDING = MILESTONES / "sale-explanation-wording-evidence" / "wording.json"
AUDIT_HARNESS = MILESTONES / "sale-family-audit-evidence" / "audit_harness.py"
PAGE = ROOT / "packages" / "presentation" / "pages" / "citation-walk.v1.html"
DOM_CHECKER = MILESTONES / "page-plain-words-evidence" / "check_page_dom.mjs"
P = "tax.us.2025."
QUESTION_CODES = {"CODE_W_ON_GAIN", "ADJUSTMENT_EXCEEDS_LOSS"}
FAMILY_PREFIX = {
    "w": P + "f1099b.covered-w-",
    "noncovered": P + "f1099b.noncovered-",
    "no1099b": P + "f8949.no1099b-",
    "codeb": P + "f1099b.code-b-",
}
QUESTION_STEM = {"w": "f1099b-covered-w", "noncovered": "f1099b-noncovered", "no1099b": "f8949-no1099b",
                 "codeb": "f1099b-code-b"}


def _wording() -> list[dict[str, Any]]:
    return list(json.loads(WORDING.read_text(encoding="utf-8"))["replacements"])


def _load() -> tuple[Any, Any]:
    h = evidence_loader.load(AUDIT_HARNESS, "sew_t1_audit_harness")
    probe = evidence_loader.load(INVENTORY, "sew_t1_inventory_probe")
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
            run_id=f"demo.sew.t1.{name}", governance_pins=[], surface=surface, output_name="out.json",
        )
        assert outcome.refusal is None, (name, outcome.refusal)
        assert outcome.presentation_path is not None
        model: dict[str, Any] = json.loads(outcome.presentation_path.read_text(encoding="utf-8"))
        validate_presentation_model(model)
        return model


def _results(model: dict[str, Any]) -> dict[str, tuple[Any, Any]]:
    return {s["field"]["id"]: (s["resolved"]["disposition"], s["resolved"].get("value")) for s in model["sections"]}


def _links(model: dict[str, Any]) -> dict[str, list[tuple[str, tuple[str, ...]]]]:
    """Each blocked line's question links, by question target and the reason sentences they point at."""
    groups = {g["id"]: g["answerTarget"]["factTypeId"] for g in model.get("questionGroups", [])}
    out: dict[str, list[tuple[str, tuple[str, ...]]]] = {}
    for s in model["sections"]:
        reasons = [r.get("sentence") for r in s["resolved"].get("reasons", [])]
        out[s["field"]["id"]] = sorted(
            (groups[ref["groupId"]], tuple(sorted(str(reasons[i]) for i in ref["reasonIndices"])))
            for ref in s["resolved"].get("questionRefs", [])
        )
    return out


def test_core_v107_passes_full_validate_package() -> None:
    v107 = json.loads((CONTENT / "package.core-calculations.v107.json").read_text(encoding="utf-8"))
    corpus, _ = load_corpus(CONTENT)
    res = validate_package(v107, {(c["id"], c["version"]): c for c in corpus.values()}, DerivationSchemas())
    assert res.ok, res.issues


def test_v107_all_38_cases_keep_every_result_and_link_and_read_the_new_words() -> None:
    h, probe = _load()
    v106 = h.Core("v106", "v104", "v104")
    v107 = h.Core("v107", "v105", "v105")
    rows = _wording()
    explanation = {(r["family_id"], r["block_code"]): r for r in rows if r["property"] == "explanation"}
    question = {r["id"]: r for r in rows if r["property"] == "question"}
    to_new = {r["old"]: r["new"] for r in rows if r["property"] == "question"}
    checked = 0
    for kind, term, variants in probe.CASES:
        family = FAMILY_PREFIX[kind] + term
        for variant in variants:
            name = f"{kind}.{term}.{variant}"
            m106 = _run(h, v106, "v106." + name, probe.build_sale_case(kind, term, variant, v106, h, ccr))
            m107 = _run(h, v107, "v107." + name, probe.build_sale_case(kind, term, variant, v107, h, ccr))
            assert _results(m106) == _results(m107), name
            blocked = [s for s in m107["sections"] if s["resolved"]["disposition"] == "blocked"]
            if variant == "valid_loss":
                assert blocked == [] and m107.get("questionGroups", []) == [], name
                continue
            row = explanation[(family, variant)]
            old_links = _links(m106)
            new_links = _links(m107)
            assert set(old_links) == set(new_links), name
            for line, links in old_links.items():
                renamed = [(target, tuple(sorted(to_new.get(s, s) if s != row["old"] else row["new"] for s in sents)))
                           for target, sents in links]
                assert sorted(renamed) == new_links[line], (name, line)
            for section in blocked:
                sentences = [r.get("sentence") for r in section["resolved"].get("reasons", [])]
                assert row["new"] in sentences and row["old"] not in sentences, (name, sentences)
            groups = m107.get("questionGroups", [])
            if variant in QUESTION_CODES:
                q = question[f"{P}input-question.{QUESTION_STEM[kind]}-{term}-adjustment"]
                assert [g["question"] for g in groups] == [q["new"]], name
                assert [g["answerTarget"]["factTypeId"] for g in groups] == [
                    g["answerTarget"]["factTypeId"] for g in m106["questionGroups"]
                ], name
            else:
                assert groups == [], name
            checked += 1
    assert checked == 30


def test_live_v107_wash_sale_block_renders_the_new_words_and_its_question() -> None:
    h, probe = _load()
    v107 = h.Core("v107", "v105", "v105")
    model = _run(h, v107, "render.code_w", probe.build_sale_case("w", "st", "CODE_W_ON_GAIN", v107, h, ccr))
    rows = _wording()
    plain = next(r["new"] for r in rows if r.get("family_id") == P + "f1099b.covered-w-st"
                 and r.get("block_code") == "CODE_W_ON_GAIN")
    asked = next(r["new"] for r in rows if r["id"] == P + "input-question.f1099b-covered-w-st-adjustment")
    env = os.environ.copy()
    env["PPW_CHECK_DETAIL"] = "1"
    proc = subprocess.run(
        ["node", str(DOM_CHECKER), str(PAGE)],
        input=json.dumps({"key": "code_w", "model": model}) + "\n",
        text=True, capture_output=True, timeout=30, check=True, env=env,
    )
    report = json.loads(proc.stdout)["code_w"]
    assert report["section_errors"] == 0, report
    assert report["total_first_read_leaks"] == 0, report
    text = report["first_read_text"]
    assert plain in text
    assert asked in text
    assert "See the question and affected lines above" in text
