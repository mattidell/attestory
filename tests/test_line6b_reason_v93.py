"""Published v93 explains line 6b through real runs, projection and saved pages.

The fourteen required act lists, two mainland-income counterexamples,
and the distinct joint-filing browser list
each run once. These tests exceed the fast-lane budget: real coordinate
runs took 6.77-23.08 seconds in the repair targeted run; the Chrome test
took 22.94 seconds. Like the v92 page-alerts precedent, the whole module
is explicitly live.

Decision 8: a spoken no to a positive question about an excluded circumstance
sets its no-* fact to yes. Living apart is an affirmative fact: yes means yes.
No entry control is under test. Left-out facts are removed here, in each test's
act list, and checked absent both before and after package handover.
"""
from __future__ import annotations

import html
import json
import re
import shutil
from pathlib import Path
from typing import Any, cast

import pytest

from packages.derivation.live import live_coordinate_run
from packages.derivation.live_session import _render_page
from tests import evidence_loader
from tests.test_page_alerts_v92 import _dump, _section
from tools.sale_page_observation import _new_owned_chrome_tempdir

pytestmark = pytest.mark.live

REPO = Path(__file__).resolve().parents[1]
MILESTONES = REPO / "docs/phases/engine-breadth/milestones"
EVIDENCE = MILESTONES / "line6b-reason-evidence"
P = "tax.us.2025."
SCOPE = "ss-benefits-scope.no-form-2555"
LIVING = "mfs-lived-apart-all-year"
TERRITORIAL = "ss-benefits-scope.no-puerto-rico-or-samoa-income"
TERRITORIAL_QUESTION = "For 2025, were you (or your spouse, if filing jointly) a bona fide resident of Puerto Rico or American Samoa who had any income?"
COUNTEREXAMPLES = ("resident-mainland-income", "joint-spouse-resident-mainland-income")
FACTS = (
    "ss-benefits-scope.no-unsupported-line1-entries",
    "ss-benefits-scope.no-pension-annuity-line5b",
    "ss-benefits-scope.no-traditional-ira-deduction",
    SCOPE,
    "ss-benefits-scope.no-form-4563",
    "ss-benefits-scope.no-form-8815",
    "ss-benefits-scope.no-excluded-adoption-benefits",
    "ss-benefits-scope.no-puerto-rico-or-samoa-income",
    "schedule1-adjustments-scope.no-line24z-writein",
    LIVING,
)
CASES = (*FACTS, "scope-pair", "mfs-pair", "fully-answered", "mfs-no-benefits", *COUNTEREXAMPLES)
Acts = list[dict[str, Any]]


def _evidence() -> Any:
    # Bind every evidence dependency by path, including the names its parent
    # harness resolves dynamically. No ambient PYTHONPATH probe can supply it.
    evidence_loader.load(MILESTONES / "sale-family-audit-evidence/audit_harness.py", "qw_p0_harness")
    evidence_loader.load(MILESTONES / "question-wording-evidence/probe.py", "l6b_p0_qw")
    evidence_loader.load(EVIDENCE / "probe.py", "l6b_t0_probe")
    evidence_loader.load(EVIDENCE / "prototype.py", "l6b_t0_proto")
    return evidence_loader.load(EVIDENCE / "track0.py", "l6b_t1_v93_track0")


def _facts(acts: Acts, fact: str) -> list[dict[str, Any]]:
    return [finding for act in acts
            if isinstance(finding := act.get("payload", {}).get("finding"), dict)
            and str(finding.get("fact_id", "")).startswith(fact + "|")]


def _absent(acts: Acts, missing: set[str]) -> None:
    assert all(not _facts(acts, fact) for fact in missing)


def _run(helper: Any, acts: Acts, missing: set[str], name: str, root: Path) -> tuple[dict[str, Any], Path]:
    h = helper.probe.harness()
    core = helper.rr.resolve_core("v93")
    assert core.loader_from is None
    _absent(acts, missing)
    finished = h._handover(h._finish(
        acts, package_path=core.package_path, package_version=core.version,
        release_path=core.release_path, release_version=core.release_version,
        note="demo.l6b.v93." + name,
    ), surface=core.surface(), reconfirm=True)
    _absent(finished, missing)
    cap = h.WorkspaceCapability(root / "L")
    outcome = live_coordinate_run(
        cap, repo_root=REPO, authoritative_acts=finished, workspace_revision=len(finished),
        run_scope={"jurisdiction": "us", "year": h.YEAR}, scope_user=h.ccr.USER,
        request={"schema": "run-request.v1"}, run_id="demo.l6b.v93." + name,
        governance_pins=[], surface=core.surface(), output_name="out.json",
    )
    assert outcome.refusal is None
    assert outcome.output_path is not None
    assert outcome.presentation_path is not None
    report = json.loads(outcome.output_path.read_text())
    assert report["stop_reason"] == "saturated"
    projected = json.loads(outcome.presentation_path.read_text())
    page = root / "demo.page.html"
    page.write_bytes(_render_page(REPO, cap, outcome.presentation_path))
    text = page.read_text()
    marker = "const MODEL = Object.freeze("
    saved, _ = json.JSONDecoder().raw_decode(text, text.index(marker) + len(marker))
    assert saved == projected
    return cast(dict[str, Any], saved), page


def _field(model: dict[str, Any], slug: str) -> dict[str, Any]:
    return next(cast(dict[str, Any], s) for s in model["sections"] if s["field"]["id"] == P + slug)


def _questions(section: dict[str, Any]) -> list[str]:
    return [r["sentence"] for r in section["resolved"].get("reasons", [])]


def _blocked(section: dict[str, Any], wanted: set[str]) -> None:
    assert section["resolved"]["disposition"] == "blocked"
    assert set(_questions(section)) == wanted
    assert len(_questions(section)) == len(wanted)
    # Explicit reasons select the question path in the page renderer. The
    # browser test below checks that path's drawn text as well.
    generic = section["field"]["dispositions"]["blocked"].get("explain")
    assert generic not in _questions(section)


@pytest.mark.parametrize("case", CASES)
def test_required_v93_cases_once(case: str, tmp_path: Path) -> None:
    helper = _evidence()
    questions = dict(cast(dict[str, str], helper.proto.QUESTIONS))
    questions[TERRITORIAL] = TERRITORIAL_QUESTION
    assert set(questions) == set(FACTS)
    separate = case in {LIVING, "mfs-pair", "mfs-no-benefits"}
    status = ("married_filing_jointly" if case == "joint-spouse-resident-mainland-income" else
              "married_filing_separately" if separate else "single")
    if case == "mfs-no-benefits":
        acts = cast(Acts, helper.current_answers(helper.probe.base(status, benefits=False), status))
        missing_slugs = {LIVING}
    else:
        acts = cast(Acts, helper.complete_ssa(status))
        missing_slugs = ({case} if case in FACTS else
                         {SCOPE, "ss-benefits-scope.no-pension-annuity-line5b"} if case == "scope-pair" else
                         {SCOPE, LIVING} if case == "mfs-pair" else set())
    # All exclusions answered no, living-apart answered yes, by Decision 8.
    for slug in FACTS:
        assert [f["value"] for f in _facts(acts, P + slug)] == ["yes"]
    if case in COUNTEREXAMPLES:
        # Synthetic resident (or spouse on a joint return), only mainland
        # income: the truthful answer to any income is yes. Decision 8
        # records no for the absence fact, unlike the former source qualifier.
        recorded_value = helper.predicate_value(P + TERRITORIAL, "yes")
        assert recorded_value == "no"
        acts = cast(Acts, helper.probe.harness().say(
            acts, P + TERRITORIAL, recorded_value, "l6b.repair." + case))
        assert [f["value"] for f in _facts(acts, P + TERRITORIAL)] == ["no"]
    missing = {P + slug for slug in missing_slugs}
    # The omission is local and visible; no shared helper removes these facts.
    acts = [a for a in acts if not any(
        str(a.get("payload", {}).get("finding", {}).get("fact_id", "")).startswith(f + "|")
        for f in missing
    )]
    _absent(acts, missing)
    model, _page = _run(helper, acts, missing, case.replace(".", "-"), tmp_path)
    line6b = _field(model, "form1040.line-6b")
    if case in COUNTEREXAMPLES:
        assert line6b["resolved"]["disposition"] == "guard_inapplicable"
        assert line6b["resolved"].get("value") is None
        assert _questions(line6b) == []
    elif case == "fully-answered":
        # 2025 Social Security Benefits Worksheet, printed p32; local source
        # lines 2072-2110 in the audited law.json extract. Box 5 = 12,000,
        # wages = 50,000, tax-exempt interest and adjustments = zero.
        combined = 50000 + 12000 / 2
        lower_band = min(combined - 25000, 9000)
        hand = min(0.85 * 12000, 0.85 * (combined - 34000) + min(12000 / 2, lower_band / 2))
        assert hand == 10200
        assert line6b["resolved"]["disposition"] == "published_value"
        assert line6b["resolved"]["value"] == hand
        assert _questions(line6b) == []
    elif case == "mfs-no-benefits":
        refund = _field(model, "form1040.line-34")["resolved"]
        # The v92 computing neighbour also refunds 625 (Track 1 matrix).
        assert (refund["disposition"], refund["value"]) == ("published_value", 625)
        _blocked(_field(model, "form1040.line-6d"), {questions[LIVING]})
    elif case == "mfs-pair":
        _blocked(line6b, {questions[SCOPE]})
        _blocked(_field(model, "form1040.line-6d"), {questions[LIVING]})
        page_questions = {q for s in model["sections"] for q in _questions(s)}
        assert {questions[SCOPE], questions[LIVING]} <= page_questions
    else:
        _blocked(line6b, {questions[slug] for slug in missing_slugs})


def test_chrome_draws_the_v93_question_with_zero_safe_render_alerts() -> None:
    helper = _evidence()
    # Joint filing makes this act list distinct from all fourteen above.
    acts = cast(Acts, helper.complete_ssa("married_filing_jointly"))
    missing = {P + SCOPE}
    acts = [a for a in acts if not str(
        a.get("payload", {}).get("finding", {}).get("fact_id", "")
    ).startswith(P + SCOPE + "|")]
    _absent(acts, missing)
    root = _new_owned_chrome_tempdir()
    try:
        model, page = _run(helper, acts, missing, "joint-browser", root)
        section = _field(model, "form1040.line-6b")
        wanted = str(helper.proto.QUESTIONS[SCOPE])
        _blocked(section, {wanted})
        dom = _dump(page, root / "chrome")
        assert 'class="section-error"' not in dom
        drawn = _section(dom, section["field"]["label"])
        plain = html.unescape(re.sub(r"<[^>]+>", " ", drawn))
        plain = re.sub(r"\s+", " ", plain)
        assert wanted in plain
        generic = section["field"]["dispositions"]["blocked"].get("explain")
        assert not generic or generic not in plain
        assert 'class="remedy-box"' not in drawn
    finally:
        shutil.rmtree(root)
