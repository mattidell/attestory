"""Seven distinct published-v95 lists, once each through the saved page model.

Measured reason for the live marker: this module's seven distinct saved-page
cases measured 18.75–19.68 s per call at standard xdist concurrency, above
the 3.0 s fast-lane budget. Each case calls
live_coordinate_run, the real presentation projection and page renderer.
Expected names are computed from the input findings, never the run result.
"""
from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
from typing import Any, cast

import pytest

from packages.derivation.live import live_coordinate_run
from packages.derivation.live_session import _render_page
from tests import evidence_loader

pytestmark = pytest.mark.live
REPO = Path(__file__).resolve().parents[1]
MILESTONES = REPO / "docs/phases/engine-breadth/milestones"
EVIDENCE = MILESTONES / "line16-names-evidence"
BNQ = MILESTONES / "blocked-names-question-evidence"
P = "tax.us.2025."
EXC = tuple(P + name for name in (
    "exception1.only-box2a-capital-gains", "exception1.no-capital-losses",
    "exception1.no-qof-deferral", "exception1.no-boxes-2b-2c-2d",
))
FOUR = tuple(P + name for name in (
    "f1099b.noncovered-sold.source-closure", "f8949.no1099b-sold.source-closure",
    "schedule-d-boundary.no-form8949-sources", "schedule-d-boundary.no-other-form8949-adjustments",
))
FIELDS = ("form1040.line-16", "form1040.line-20", "form1040.line-7a")
CASES = ("one", "two", "four", "correct-one", "personal-loss", "boundary-unanswered", "computing")
Acts = list[dict[str, Any]]


def _harness() -> Any:
    # Bind legacy bare-name siblings by exact path before loading their parent.
    # An unrelated evidence directory first on PYTHONPATH cannot replace them.
    evidence_loader.load(BNQ / "common.py", "common")
    evidence_loader.load(BNQ / "probe.py", "probe")
    return evidence_loader.load(MILESTONES / "sale-family-audit-evidence/audit_harness.py", "l16_v95_harness")


def _probe() -> Any:
    _harness()
    return evidence_loader.load(BNQ / "probe.py", "l16_v95_bnq_probe")


def _findings(acts: Acts, fact: str) -> list[dict[str, Any]]:
    return [f for act in acts if isinstance(f := (act.get("payload") or {}).get("finding"), dict)
            and str(f.get("fact_id", "")).startswith(fact + "|")]


def _failed(acts: Acts) -> list[str]:
    current = {fact: _findings(acts, fact)[-1]["value"] for fact in EXC}
    assert set(current.values()) <= {"yes", "no"}
    return [fact for fact in EXC if current[fact] == "no"]


def _fixture(case: str) -> Acts:
    h, probe = _harness(), _probe()
    if case == "personal-loss":
        acts = cast(Acts, probe.personal_loss_8949())
    else:
        acts = cast(Acts, probe.empty(exc1_only_2a="yes", exc1_no_losses="yes"))
        mask = {"one": 1, "two": 3, "four": 15, "correct-one": 3, "boundary-unanswered": 1, "computing": 0}[case]
        for i, fact in enumerate(EXC):
            acts = h.say(acts, fact, "no" if mask & (1 << i) else "yes", "l16v95." + case + "." + str(i))
        if case == "correct-one":
            # Preserve the old no and append the actual correction to the same fact.
            previous = _findings(acts, EXC[1])[-1]
            h._add(acts, "assertion", {"finding": h._attested("demo.l16v95.correct-loss", previous["fact_id"], "yes")})
            assert [f["value"] for f in _findings(acts, EXC[1])] == ["no", "yes"]
        if case == "boundary-unanswered": acts = h.strip(acts, FOUR[2])
    for fact in (P + "taxpayer-over-65", P + "taxpayer-blind"):
        acts = h.say(acts, fact, False, "l16v95." + case + "." + fact.removeprefix(P))
    return cast(Acts, h.renumber(acts))


@pytest.fixture(scope="module")
def act_lists() -> dict[str, Acts]:
    cases = {case: _fixture(case) for case in CASES}
    digests = {hashlib.sha256(json.dumps(acts, sort_keys=True).encode()).hexdigest() for acts in cases.values()}
    assert len(digests) == len(CASES)
    return cases


def _run(acts: Acts, case: str, root: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    h = _harness()
    core = h.Core("v95", "v93", "v93")
    assert core.loader_from is None
    finished = h._handover(h._finish(copy.deepcopy(acts), package_path=core.package_path,
        package_version=core.version, release_path=core.release_path,
        release_version=core.release_version, note="demo.l16v95." + case), surface=core.surface(), reconfirm=True)
    cap = h.WorkspaceCapability(root / "L")
    outcome = live_coordinate_run(cap, repo_root=REPO, authoritative_acts=finished,
        workspace_revision=len(finished), run_scope={"jurisdiction": "us", "year": h.YEAR},
        scope_user=h.ccr.USER, request={"schema": "run-request.v1"}, run_id="demo.l16v95." + case,
        governance_pins=[], surface=core.surface(), output_name="out.json")
    assert outcome.refusal is None
    assert outcome.output_path is not None and outcome.presentation_path is not None
    report = cast(dict[str, Any], json.loads(outcome.output_path.read_text()))
    assert report["stop_reason"] == "saturated"
    model = cast(dict[str, Any], json.loads(outcome.presentation_path.read_text()))
    page = root / "demo.l16v95.page.html"
    page.write_bytes(_render_page(REPO, cap, outcome.presentation_path))
    text = page.read_text()
    marker = "const MODEL = Object.freeze("
    saved, _ = json.JSONDecoder().raw_decode(text, text.index(marker) + len(marker))
    assert saved == model
    return cast(dict[str, Any], saved), report


def _section(model: dict[str, Any], field: str) -> dict[str, Any]:
    return next(cast(dict[str, Any], section) for section in model["sections"] if section["field"]["id"] == P + field)


def _sentences(section: dict[str, Any]) -> list[str]:
    return [reason["sentence"] for reason in section["resolved"].get("reasons", [])]


def _questions(names: list[str]) -> list[str]:
    words = {P + row["name"]: row["sentence"] for row in json.loads((EVIDENCE / "law.json").read_text())["questions"]}
    return sorted(words[name] for name in names)


def _states(model: dict[str, Any]) -> dict[str, Any]:
    return {section["field"]["id"].removeprefix(P): {
        "disposition": section["resolved"]["disposition"], "value": section["resolved"].get("value"),
        "sentences": _sentences(section)} for section in model["sections"]}


@pytest.mark.parametrize("case", CASES)
def test_published_v95_names_from_current_facts_once(case: str, act_lists: dict[str, Acts], tmp_path: Path) -> None:
    acts = act_lists[case]
    expected = _failed(acts)
    if case in ("one", "two", "four", "correct-one"):
        wanted = {"one": [EXC[0]], "two": list(EXC[:2]), "four": list(EXC), "correct-one": [EXC[0]]}[case]
        assert expected == wanted
    model, report = _run(acts, case, tmp_path)
    if case == "computing":
        assert expected == []
        before = json.loads((EVIDENCE / "track0b-neighbours.json").read_text())["before"]
        fields = before["cases"]["no-schedule-d/single"]["fields"]
        frozen = {name: {"disposition": before["field_states"][index]["disposition"],
                         "value": before["field_states"][index]["value"],
                         "sentences": [r["sentence"] for r in before["field_states"][index]["reasons"]]}
                  for name, index in fields.items()}
        assert json.dumps(_states(model), sort_keys=True) == json.dumps(frozen, sort_keys=True)
        assert _section(model, "form1040.line-16")["resolved"]["value"] == 3875
        return
    names = list(FOUR) if case == "personal-loss" else [FOUR[2]] if case == "boundary-unanswered" else expected
    if case == "personal-loss": assert _findings(acts, FOUR[2])[-1]["value"] == "no"
    if case == "boundary-unanswered": assert _findings(acts, FOUR[2]) == []
    for field in FIELDS:
        section = _section(model, field)
        assert section["resolved"]["disposition"] == "blocked"
        assert _sentences(section) == _questions(names)
    if case not in ("personal-loss", "boundary-unanswered"):
        for artifact in ("form1040-line16", "selected-preferential-base"):
            row = next(r for r in report["dispositions"] if r["artifact_id"] == P + "rule." + artifact)
            assert (row["disposition"], row["code"], row["missing"]) == ("blocked", "DEPENDENCY_ABSENT", expected)
