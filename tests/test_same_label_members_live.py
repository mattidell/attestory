"""Members with the same recorded label each get their question, told apart by entry order (ADR 0087, 0090).

same-label-members Track 1 and same-label-ordinal Track 1. The P0 probe returns
(``same-label-members-evidence/probe.py``, observed through
``same-label-ordinal-evidence/probe.py``) go through live_coordinate_run, the
real presentation projection and the saved page, on published core v108.
Members share one recorded label ("Demo Sam") by case; each case leaves answers
out of named members' records. Every blocked line that shows a member reason
must show one per missing answer, each labelled with the recorded label. A label
shared within the member's kind carries the member's place in entry order
(``memberOrdinal``); one person's questions sit together. The page (rendered by
the page-plain-words DOM checker) draws each as
"<label> (the <nth> one you added with this name): <question>".

Measured reason for the live marker: each live_coordinate_run with page
rendering takes about 5 s, above the fast-lane budget.
"""
from __future__ import annotations

import shutil
from collections import Counter
from functools import lru_cache
from pathlib import Path
from typing import Any

import pytest

from tests import evidence_loader

pytestmark = pytest.mark.live
REPO = Path(__file__).resolve().parents[1]
EVIDENCE = REPO / "docs/phases/engine-breadth/milestones/same-label-ordinal-evidence"
PAGE = REPO / "packages/presentation/pages/citation-walk.v1.html"
ORDINAL_WORDS = ("first", "second", "third")


@lru_cache(maxsize=1)
def _ordinal_probe() -> Any:
    return evidence_loader.load(EVIDENCE / "probe.py", "slo_t1_live_probe")


def _probe() -> Any:
    return _ordinal_probe().slm


@lru_cache(maxsize=None)
def _run(case: str) -> dict[str, Any]:
    probe = _probe()
    core = probe.h.Core("v108", "v106", "v106")
    assert core.package_path.name == "package.core-calculations.v108.json"
    if shutil.which("node"):
        return dict(_ordinal_probe().observe(core, case, page=PAGE))
    return dict(probe.observe(core, case))


def _expected_labels(case: str) -> tuple[Counter[str], int]:
    """Member labels, one per left-out answer, and how many distinct answers are left out."""
    probe = _probe()
    _, roster, letters, removed = case.split("/")
    children, parents = probe.members(roster)
    label_of = dict(zip([*children, *parents], (probe.LABELS[letter] for letter in letters)))
    parts = [part.split("@") for part in removed.split("+")]
    return Counter(label_of[probe.member_name(where)] for _, where in parts), len({short for short, _ in parts})


def _expected_members(case: str) -> list[tuple[str, int]]:
    """(label, ordinal) for each left-out answer, sorted as the page groups them; 0 is no ordinal."""
    probe = _probe()
    _, roster, letters, removed = case.split("/")
    children, parents = probe.members(roster)
    order = [*children, *parents]
    label_of = dict(zip(order, (probe.LABELS[letter] for letter in letters)))

    def ordinal(member: str) -> int:
        peers = [m for m in order if label_of[m] == label_of[member] and (m in children) == (member in children)]
        return peers.index(member) + 1 if len(peers) > 1 else 0

    members = [probe.member_name(part.split("@")[1]) for part in removed.split("+")]
    return sorted((label_of[m], ordinal(m)) for m in members)


SAME_LABEL = (
    "single/kid2/AA/age@1+age@2",
    "single/kid2/AA/res@1+res@2",
    "single/kid2/AA/age@1+res@2",
    "single/kid2/AA/u17@1+u17@2",
    "single/kid2/AA/dtb-another@1+dtb-another@2",
    "mfj/kid2/AA/age@1+age@2",
    "single/kid2/AA/age@1",
    "single/kid2/AA/age@2",
    "single/kid3/AAA/age@1+age@2+age@3",
    "single/kid3/AAA/age@1+res@3",
    "single/kid3/AAA/age@3",
    "single/kid3/AAB/age@1+age@2+age@3",
    "single/kid3/ABA/age@3",
    "single/odckid2/AA/odc-tin@1+odc-tin@2",
    "single/parent2/AA/rel-tin@p1+rel-tin@p2",
    "single/parent2/AA/rel-tin@p1+rel-citizen@p2",
    "single/parent2/AA/rel-tin@p2",
)
CONTROLS = (
    "single/kid2/AB/age@1+age@2",
    "single/parent2/AB/rel-tin@p1+rel-tin@p2",
)


@pytest.mark.parametrize("case", SAME_LABEL + CONTROLS)
def test_each_member_missing_an_answer_gets_its_own_reason(case: str) -> None:
    run = _run(case)
    assert "error" not in run and "refusal" not in run, run
    assert run["blocked_page_lines_without_sentence"] == []
    labels, distinct = _expected_labels(case)
    lines = {line: [r for r in said if r[0]] for line, said in run["reasons"].items()}
    lines = {line: said for line, said in lines.items() if said}
    assert lines, "no line shows a member reason"
    for line, said in lines.items():
        assert Counter(label for label, _, _ in said) == labels, (line, said)
        assert len({sentence for _, _, sentence in said}) == distinct, (line, said)
        assert [(label, ordinal) for label, ordinal, _ in said] == _expected_members(case), (line, said)
        # One person's questions sit together: label, then ordinal, then sentence.
        assert said == sorted(said), (line, said)
    # Member questions link no question group (ADR 0087 Decision 3).
    assert run["question_groups"] == 0 and run["question_links"] == {}


@pytest.mark.parametrize("case", SAME_LABEL + CONTROLS)
def test_the_page_draws_every_member_reason(case: str) -> None:
    if shutil.which("node") is None:
        pytest.skip("node is not installed")
    run = _run(case)
    dom = run["dom"]
    assert dom["section_errors"] == 0 and dom["first_read_leaks"] == 0
    expected = {line: len([r for r in said if r[0]]) for line, said in run["reasons"].items()}
    assert dom["member_item_counts"] == {line: n for line, n in expected.items() if n}
    # The drawn text: the label, its place when the label is shared, then the question.
    assert set(run["drawn"]) == set(dom["member_item_counts"])
    for line, items in run["drawn"].items():
        said = [r for r in run["reasons"][line] if r[0]]
        assert len(items) == len(said), (line, items)
        for item, (label, ordinal, sentence) in zip(items, said):
            which = f" (the {ORDINAL_WORDS[ordinal - 1]} one you added with this name)" if ordinal else ""
            assert item == f"{label}{which}: {sentence}", (line, item)


def test_a_child_and_a_parent_sharing_a_label_keep_their_own_questions() -> None:
    run = _run("single/kidpar/AA/age@1+rel-tin@p1")
    said = {tuple(r) for rows in run["reasons"].values() for r in rows if r[0]}
    assert {label for label, _, _ in said} == {"Demo Sam"}
    assert len({sentence for _, _, sentence in said}) == 2
    # A child and a parent are different kinds: neither carries an ordinal.
    assert {ordinal for _, ordinal, _ in said} == {0}
