"""Live checks for core v109 (line16-next-step, ADR 0091).

Seven synthetic returns run once on published v108 and once on published
v109 through live_coordinate_run and the presentation projection: one, two
and four Exception 1 questions answered no on a required Schedule D with no
sale, a no answer corrected to yes on the same fact, the personal-loss case,
an unanswered Exception 1 question, and a recorded sale. On every return
each line's disposition, value and codes, every question group and every
question link are the same on both cores. Each blocked line's reasons on
v109 are its v108 reasons followed by the declared sentence for every
Exception 1 question it names whose current answer is no, and nothing else.

Package validation accepts published v109, and the saved page draws the
sentences beside the question link.
"""

from __future__ import annotations

import copy
import json
import os
import subprocess
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any, cast

import pytest

from packages.derivation.live import live_coordinate_run
from packages.derivation.live_workspace import WorkspaceCapability
from packages.derivation.loader import DerivationSchemas
from packages.derivation.package_validation import validate_package
from packages.derivation.presentation_projection import validate_presentation_model
from tests import evidence_loader
from tests.helpers import current_core_returns as ccr
from tools.package_successor import load_corpus

pytestmark = pytest.mark.live
ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "packages" / "content" / "tax" / "2025"
MILESTONES = ROOT / "docs" / "phases" / "engine-breadth" / "milestones"
BNQ = MILESTONES / "blocked-names-question-evidence"
PAGE = ROOT / "packages" / "presentation" / "pages" / "citation-walk.v1.html"
DOM_CHECKER = MILESTONES / "page-plain-words-evidence" / "check_page_dom.mjs"
P = "tax.us.2025."
SLUGS = ("only-box2a-capital-gains", "no-capital-losses", "no-qof-deferral", "no-boxes-2b-2c-2d")
EXC = tuple(P + "exception1." + slug for slug in SLUGS)
CASES = ("one", "two", "four", "correct-one", "personal-loss", "unanswered", "recorded-sale")
Acts = list[dict[str, Any]]


def _sentence(slug: str) -> str:
    body = json.loads((CONTENT / f"answer-explanation.exception1-{slug}-no.v1.json").read_text(encoding="utf-8"))
    return str(body["explanation"])


def _harness() -> Any:
    evidence_loader.load(BNQ / "common.py", "common")
    evidence_loader.load(BNQ / "probe.py", "probe")
    return evidence_loader.load(MILESTONES / "sale-family-audit-evidence/audit_harness.py", "l16ns_t1_harness")


def _probe() -> Any:
    _harness()
    return evidence_loader.load(BNQ / "probe.py", "l16ns_t1_bnq_probe")


def _findings(acts: Acts, fact: str) -> list[dict[str, Any]]:
    return [f for act in acts if isinstance(f := (act.get("payload") or {}).get("finding"), dict)
            and str(f.get("fact_id", "")).startswith(fact + "|")]


def _fixture(case: str) -> Acts:
    h, probe = _harness(), _probe()
    if case == "personal-loss":
        acts = cast(Acts, probe.personal_loss_8949())
    elif case == "recorded-sale":
        acts = cast(Acts, probe.sale("no1099b"))
    else:
        acts = cast(Acts, probe.empty(exc1_only_2a="yes", exc1_no_losses="yes"))
        mask = {"one": 1, "two": 3, "four": 15, "correct-one": 3, "unanswered": 0}[case]
        for i, fact in enumerate(EXC):
            acts = h.say(acts, fact, "no" if mask & (1 << i) else "yes", "l16ns.t1." + case + "." + str(i))
        if case == "correct-one":
            # Keep the earlier no and append the correction to the same fact.
            previous = _findings(acts, EXC[1])[-1]
            h._add(acts, "assertion", {"finding": h._attested("demo.l16ns.t1.correct-loss", previous["fact_id"], "yes")})
            assert [f["value"] for f in _findings(acts, EXC[1])] == ["no", "yes"]
        if case == "unanswered":
            acts = h.strip(acts, EXC[0])
    for fact in (P + "taxpayer-over-65", P + "taxpayer-blind"):
        acts = h.say(acts, fact, False, "l16ns.t1." + case + "." + fact.removeprefix(P))
    return cast(Acts, h.renumber(acts))


def _current_no(acts: Acts) -> set[str]:
    return {fact for fact in EXC if (found := _findings(acts, fact)) and found[-1]["value"] == "no"}


def _run(case: str, version: str, acts: Acts) -> dict[str, Any]:
    h = _harness()
    registry = "v" + str(int(version[1:]) - 2)
    core = h.Core(version, registry, registry)
    surface = core.surface()
    finished = h._handover(
        h._finish(copy.deepcopy(acts), package_path=core.package_path, package_version=core.version,
                  release_path=core.release_path, release_version=core.release_version,
                  note=f"demo.l16ns.t1.{case}"),
        surface=surface, reconfirm=True,
    )
    with TemporaryDirectory() as tmp:
        outcome = live_coordinate_run(
            WorkspaceCapability(Path(tmp) / "L"), repo_root=ROOT, authoritative_acts=finished,
            workspace_revision=len(finished), run_scope={"jurisdiction": "us", "year": h.YEAR},
            scope_user=ccr.USER, request={"schema": "run-request.v1"},
            run_id=f"demo.l16ns.t1.{case}", governance_pins=[], surface=surface, output_name="out.json",
        )
        assert outcome.refusal is None, (case, outcome.refusal)
        assert outcome.presentation_path is not None
        model = cast(dict[str, Any], json.loads(outcome.presentation_path.read_text(encoding="utf-8")))
    validate_presentation_model(model)
    return model


def _states(model: dict[str, Any]) -> dict[str, Any]:
    return {s["field"]["id"]: (s["resolved"]["disposition"], s["resolved"].get("value"), s["resolved"].get("activeCodes"),
                               s["resolved"].get("questionRefs")) for s in model["sections"]}


def _named(model: dict[str, Any], section: dict[str, Any]) -> set[str]:
    targets = {g["id"]: g["answerTarget"]["factTypeId"] for g in model.get("questionGroups", [])}
    return {targets[ref["groupId"]] for ref in section["resolved"].get("questionRefs", [])}


@pytest.mark.parametrize("case", CASES)
def test_v109_adds_only_the_declared_sentence_for_each_named_no_answer(case: str) -> None:
    acts = _fixture(case)
    m108, m109 = _run(case, "v108", acts), _run(case, "v109", acts)
    assert _states(m108) == _states(m109), case
    assert m108.get("questionGroups") == m109.get("questionGroups"), case
    no = _current_no(acts)
    expected_no = {"one": EXC[:1], "two": EXC[:2], "four": EXC, "correct-one": EXC[:1],
                   "personal-loss": EXC[:2], "unanswered": (), "recorded-sale": EXC[:2]}[case]
    assert no == set(expected_no), case
    sentences = {P + "exception1." + slug: _sentence(slug) for slug in SLUGS}
    explained = 0
    for s108, s109 in zip(m108["sections"], m109["sections"]):
        before = [r["sentence"] for r in s108["resolved"].get("reasons", [])]
        after = [r["sentence"] for r in s109["resolved"].get("reasons", [])]
        added = sorted(sentences[fact] for fact in _named(m108, s108) & no)
        assert after == before + added, (case, s108["field"]["id"])
        assert all(set(r) == {"sentence"} for r in s109["resolved"].get("reasons", [])[len(before):])
        explained += bool(added)
    line16 = next(s for s in m109["sections"] if s["field"]["id"] == P + "form1040.line-16")
    if case in ("one", "two", "four", "correct-one"):
        assert explained == 28, case
        assert line16["resolved"]["disposition"] == "blocked"
        assert [r["sentence"] for r in line16["resolved"]["reasons"]][-len(expected_no):] == sorted(
            sentences[fact] for fact in expected_no)
    else:
        # The personal-loss case names the sale and boundary questions, not Exception 1.
        assert explained == 0, case
    if case == "recorded-sale":
        assert line16["resolved"]["disposition"] == "published_value"


def test_live_v109_page_draws_each_sentence_beside_its_question_link() -> None:
    model = _run("render.two", "v109", _fixture("two"))
    env = os.environ.copy()
    env["PPW_CHECK_DETAIL"] = "1"
    proc = subprocess.run(
        ["node", str(DOM_CHECKER), str(PAGE)],
        input=json.dumps({"key": "two", "model": model}) + "\n",
        text=True, capture_output=True, timeout=60, check=True, env=env,
    )
    report = json.loads(proc.stdout)["two"]
    assert report["section_errors"] == 0, report
    text = report["first_read_text"]
    for slug in SLUGS[:2]:
        assert _sentence(slug) in text
    for slug in SLUGS[2:]:
        assert _sentence(slug) not in text
    assert "See the question and affected lines above" in text
    assert "You answered yes" not in text


def test_core_v109_passes_full_validate_package() -> None:
    corpus, _ = load_corpus(CONTENT)
    package = json.loads((CONTENT / "package.core-calculations.v109.json").read_text(encoding="utf-8"))
    outcome = validate_package(package, corpus, DerivationSchemas())
    assert outcome.ok, outcome.issues
