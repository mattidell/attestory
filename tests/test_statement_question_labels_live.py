"""Saved Form 1099-B questions rendered through the page DOM checker."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
from collections import Counter
from pathlib import Path

import pytest

from tests import evidence_loader
from tools import recorded_replay as rr

pytestmark = pytest.mark.live
REPO = Path(__file__).resolve().parents[1]
MILESTONES = REPO / "docs/phases/engine-breadth/milestones"
PROBE = MILESTONES / "statement-question-labels-evidence/probe.py"
CHECKER = MILESTONES / "page-plain-words-evidence/check_page_dom.mjs"
PAGE = REPO / "packages/presentation/pages/citation-walk.v1.html"
WITHHOLDING_PROBE = MILESTONES / "statement-labels-forms-evidence/probe.py"


@pytest.mark.parametrize("case", [
    "two.amount-and-box7.s2",
    "two.amount.both.same-label",
    "two.box4-no-beside-yes",
    "three.box7.all",
])
def test_the_saved_page_names_each_unanswered_statement(case: str) -> None:
    probe = evidence_loader.load(PROBE, "statement_labels_live_probe")
    cases = dict(probe.case_lists())
    expected = next(spec["expect"] for spec in probe.CASES if spec["id"] == case)
    saved = rr.saved_output(rr.resolve_core("v108"), cases[case], "demo.statement-labels.live")
    assert saved["outcome"] == "success", saved
    model = saved["model"]
    observed = probe.observe(model, saved["report"])
    assert probe.labels_by_fact(observed) == expected
    assert observed["groups"] == []
    assert all(not reason["linked"] for reason in observed["reasons"])
    assert all(reason["statementLabel"]["taxYear"] == "2025" for reason in observed["reasons"])

    node = shutil.which("node")
    if node is None:
        pytest.skip("Node is required for the saved page DOM check")
    expected_by_line: dict[str, Counter[str]] = {}
    for reason in observed["reasons"]:
        counts = expected_by_line.setdefault(reason["line"], Counter())
        counts[reason["statementLabel"]["statement"] + ":"] += 1
    inputs = [json.dumps({"key": "page", "model": model})]
    for section in model["sections"]:
        if section["id"] not in expected_by_line:
            continue
        # Render each line separately so the checker's text limit cannot
        # hide its labels. Keep only groups that the chosen line references.
        group_ids = {ref["groupId"] for ref in section["resolved"].get("questionRefs", [])}
        groups = [group for group in model["questionGroups"] if group["id"] in group_ids]
        inputs.append(json.dumps({"key": section["id"], "model": {
            **model, "sections": [section], "questionGroups": groups,
        }}))
    process = subprocess.run(
        [node, str(CHECKER), str(PAGE)], input="\n".join(inputs), text=True,
        capture_output=True, timeout=60, check=True, env={**os.environ, "PPW_CHECK_DETAIL": "1"},
    )
    results = json.loads(process.stdout)
    page = results.pop("page")
    assert page["section_errors"] == page["total_first_read_leaks"] == 0
    assert results.keys() == expected_by_line.keys()
    for line, result in results.items():
        assert result["section_errors"] == 0
        assert result["total_first_read_leaks"] == 0
        names = Counter(text.strip() for text in result["first_read_text"].splitlines()
                        if text.strip().startswith("demo statement") and text.strip().endswith(":"))
        assert names == expected_by_line[line]


@pytest.mark.parametrize("name", [
    *(f"demo.{form}.{shape}" for form in ("int", "div", "ira", "g", "ssa")
      for shape in ("single", "two-missing", "three-one-zero")),
    "demo.int.same-label",
    "demo.int.withholding-only-offset",
    "demo.int.unclosed",
])
def test_line25b_names_unanswered_withholding_statements(name: str) -> None:
    probe = evidence_loader.load(WITHHOLDING_PROBE, "withholding_statement_labels_live_probe")
    case = probe.cases()[name]
    saved = rr.saved_output(rr.resolve_core(probe.CORE), case.acts, name)
    assert saved["outcome"] == "success", saved
    fact_type = probe.FORMS[case.form].withholding
    sentence = probe.questions()[fact_type][1]
    line = next(section["resolved"] for section in saved["model"]["sections"]
                if section["id"].endswith("line-25b"))
    reasons = line.get("reasons", [])
    indices = [index for index, reason in enumerate(reasons) if reason["sentence"] == sentence]
    labels = [{"sentence": sentence, "statementLabel": {"statement": label, "taxYear": "2025"}}
              for label in case.labels]
    linked = name in {"demo.int.single", "demo.ssa.single"}
    assert [reasons[index] for index in indices] == ([{"sentence": sentence}] if linked else []) + labels
    group_ids = {group["id"] for group in saved["model"]["questionGroups"]
                 if group["answerTarget"]["factTypeId"] == fact_type}
    refs = [ref for ref in line.get("questionRefs", []) if ref["groupId"] in group_ids]
    if linked:
        assert [ref["reasonIndices"] for ref in refs] == [[indices[0]]]
        assert indices == list(range(indices[0], indices[0] + len(indices)))
    else:
        assert refs == []
