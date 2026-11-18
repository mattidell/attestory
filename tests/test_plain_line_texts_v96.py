"""Six distinct act lists, once each on published v95 and published v96.

Each list goes through live_coordinate_run, the real presentation projection
and the saved page model. The live test reads only the active disposition
explain text, attachment headings and drawn mortgage notes. The Track 0 and
repair manifest texts appear in the v96 page exactly as the manifests word
them, no text judged not-plain in the repair table remains drawn, and every
value, disposition and refusal code equals v95's.

Measured reason for the live marker: each live_coordinate_run with page
rendering took about 20 s per core at standard xdist concurrency, above the
3.0 s fast-lane budget (two cores per case).
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
EVIDENCE = MILESTONES / "plain-line-texts-evidence"
BNQ = MILESTONES / "blocked-names-question-evidence"
CASES = ("wage-only", "interest-dividends", "closed-empty", "rounds-to-zero", "sale", "mortgage-detail")
Acts = list[dict[str, Any]]


def _harness() -> Any:
    # Bind legacy bare-name siblings by exact path before loading their parent.
    evidence_loader.load(BNQ / "common.py", "common")
    evidence_loader.load(BNQ / "probe.py", "probe")
    return evidence_loader.load(MILESTONES / "sale-family-audit-evidence/audit_harness.py", "plt_v96_harness")


def _builders() -> tuple[Any, Any]:
    _harness()
    census = evidence_loader.load(EVIDENCE / "census.py", "plt_v96_census")
    states = evidence_loader.load(EVIDENCE / "track0_states.py", "plt_v96_states")
    return census, states


def _fixture(case: str) -> Acts:
    h = _harness()
    census, states = _builders()
    named = dict(census.synthetic())
    if case == "wage-only":
        return cast(Acts, named["demo.plt.wage.single"])
    if case == "interest-dividends":
        return cast(Acts, named["demo.plt.interest-dividends"])
    if case == "sale":
        return cast(Acts, named["demo.plt.sale"])
    if case == "mortgage-detail":
        return cast(Acts, h.ccr.add_mortgage_itemizer(h.ccr.base_return(), 18000.0))
    wanted = {"closed-empty": "demo.t0.no-w2-interest-only", "rounds-to-zero": "demo.t0.rounding-zeros-and-w2g-only"}[case]
    return cast(Acts, next(acts for key, acts, _ in states.supplementary_cases() if key == wanted))


@pytest.fixture(scope="module")
def act_lists() -> dict[str, Acts]:
    cases = {case: _fixture(case) for case in CASES}
    digests = {hashlib.sha256(json.dumps(acts, sort_keys=True).encode()).hexdigest() for acts in cases.values()}
    assert len(digests) == len(CASES)
    return cases


def _run(acts: Acts, case: str, version: str, root: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    h = _harness()
    registry = {"v95": "v93", "v96": "v94"}[version]
    core = h.Core(version, registry, registry)
    finished = h._handover(h._finish(copy.deepcopy(acts), package_path=core.package_path,
        package_version=core.version, release_path=core.release_path,
        release_version=core.release_version, note="demo.plt96." + case), surface=core.surface(), reconfirm=True)
    cap = h.WorkspaceCapability(root / version)
    outcome = live_coordinate_run(cap, repo_root=REPO, authoritative_acts=finished,
        workspace_revision=len(finished), run_scope={"jurisdiction": "us", "year": h.YEAR},
        scope_user=h.ccr.USER, request={"schema": "run-request.v1"}, run_id="demo.plt96." + case,
        governance_pins=[], surface=core.surface(), output_name="out.json")
    assert outcome.refusal is None
    assert outcome.output_path is not None and outcome.presentation_path is not None
    report = cast(dict[str, Any], json.loads(outcome.output_path.read_text()))
    model = cast(dict[str, Any], json.loads(outcome.presentation_path.read_text()))
    page = root / f"demo.plt96.{version}.page.html"
    page.write_bytes(_render_page(REPO, cap, outcome.presentation_path))
    text = page.read_text()
    marker = "const MODEL = Object.freeze("
    saved, _ = json.JSONDecoder().raw_decode(text, text.index(marker) + len(marker))
    assert saved == model
    return cast(dict[str, Any], saved), report


def _manifest() -> list[dict[str, Any]]:
    rows = cast(list[dict[str, Any]], json.loads((EVIDENCE / "track0-wording.json").read_text())["replacements"])
    rows += cast(list[dict[str, Any]], json.loads((EVIDENCE / "repair-wording.json").read_text())["replacements"])
    assert len(rows) == 71
    return rows


def _not_plain() -> list[str]:
    rows = cast(list[dict[str, Any]], json.loads((EVIDENCE / "repair-drawn-texts.json").read_text())["texts"])
    return [row["text"] for row in rows if not row["plain"] and not row.get("parked")]


def _drawn(model: dict[str, Any]) -> list[str]:
    drawn: list[str] = []
    for section in model["sections"]:
        resolved = section["resolved"]
        disposition = resolved.get("disposition")
        instruction_key = "published_value" if disposition == "published_categorical" else disposition
        reasons = resolved.get("reasons") or []
        if disposition == "blocked" and reasons:
            continue
        instruction = (section["field"].get("dispositions") or {}).get(instruction_key) or {}
        explain = instruction.get("explain")
        if isinstance(explain, str) and explain:
            drawn.append(explain)
    for attachment in model.get("attachments") or []:
        title = attachment.get("title")
        if isinstance(title, str) and title:
            drawn.append(title.split(":", 1)[0].strip())
    chain = (model.get("mortgageBorrowingExplanation") or {}).get("calculationChain") or {}
    for member in chain.get("resolvedContent") or []:
        note = member.get("notes")
        if isinstance(note, str) and note:
            drawn.append(note)
    return drawn


def _dispositions(report: dict[str, Any]) -> list[Any]:
    return sorted(
        ((r["artifact_id"], r.get("symbol")), r["disposition"], r.get("code"), r.get("missing", []))
        for r in report["dispositions"])


def _states(model: dict[str, Any]) -> list[Any]:
    return [(s["id"], s["field"]["id"], s["resolved"].get("value"), s["resolved"].get("disposition"),
             s["resolved"].get("activeCodes")) for s in model["sections"]]


@pytest.mark.parametrize("case", CASES)
def test_published_v96_draws_the_manifest_texts_and_keeps_v95_values(
    case: str, act_lists: dict[str, Acts], tmp_path: Path,
) -> None:
    old_model, old_report = _run(act_lists[case], case, "v95", tmp_path)
    new_model, new_report = _run(act_lists[case], case, "v96", tmp_path)
    old_drawn, new_drawn = _drawn(old_model), _drawn(new_model)
    replaced = 0
    for row in _manifest():
        for before, after in ((row["shown"], row["new_shown"]),):
            if before in old_drawn:
                replaced += 1
                assert after in new_drawn, (row["id"], row["property"])
            assert before not in new_drawn, (row["id"], row["property"])
    assert replaced >= 1
    leftover = [text for text in _not_plain() if text in new_drawn]
    assert leftover == []
    assert _states(new_model) == _states(old_model)
    assert (new_report["stop_reason"], new_report["values"] if "values" in new_report else None) == (
        old_report["stop_reason"], old_report["values"] if "values" in old_report else None)
    assert _dispositions(new_report) == _dispositions(old_report)
