"""Live ceilings for worksheet lines 6 and 13 on core v104.

Each traced return goes through live_coordinate_run. Yes and the three
other filing statuses publish the 2025 ceiling. A head of household or
qualifying surviving spouse no, and an unanswered answer, block lines 6
and 13 and name that answer. Three scratch mutants of the published
successors fail those checks.
"""
from __future__ import annotations

import copy
import hashlib
import json
import shutil
from pathlib import Path
from typing import Any

import pytest

from packages.derivation.live import live_coordinate_run
from packages.derivation.package_validation import citizen_checksum
from tests import evidence_loader

EVIDENCE = Path(__file__).resolve().parents[1] / "docs/phases/engine-breadth/milestones/hoh-no-worksheet-ceilings-evidence"
REPO = EVIDENCE.parents[4]
CONTENT = REPO / "packages/content/tax/2025"
RELEASES = REPO / "packages/sample_data/student_loan_worksheet_integration/publication_surface/releases"
STEM = "demo.release.sli-worksheet-integration.2025"
LINE6 = "rule.qdcg-worksheet.line-6.v2.json"
LINE13 = "rule.qdcg-worksheet.line-13.v2.json"
trace = evidence_loader.load(EVIDENCE / "trace.py", "hnw_t1_live_trace")

# key, answer, disposition, line 6, line 13, code, missing fact
CASES = (
    ("hoh/none", "yes", "published", 64750, 566700, None, None),
    ("hoh/none", "no", "blocked", None, None, "DEPENDENCY_INVALID", "hoh.tests-met"),
    ("hoh/none", "none", "blocked", None, None, "DEPENDENCY_ABSENT", "hoh.tests-met"),
    ("qss/none", "yes", "published", 96700, 600050, None, None),
    ("qss/none", "no", "blocked", None, None, "DEPENDENCY_INVALID", "qss.tests-met"),
    ("qss/none", "none", "blocked", None, None, "DEPENDENCY_ABSENT", "qss.tests-met"),
    ("single/none", "none", "published", 48350, 533400, None, None),
    ("mfj/none", "none", "published", 96700, 600050, None, None),
    ("mfs/none", "none", "published", 48350, 300000, None, None),
)


def _core() -> Any:
    probe = trace._probe()
    return trace._core(probe, {"version": "v104"})


def _line(row: dict[str, Any], name: str) -> dict[str, Any]:
    item = row["rules"][name]
    assert isinstance(item, dict)
    return item


def _expect(row: dict[str, Any], disposition: str, line6: int | None, line13: int | None,
            code: str | None, missing: str | None) -> None:
    assert "error" not in row and "refusal" not in row, row.get("error") or row.get("refusal")
    for name, value in (("qdcg-worksheet.line-6", line6), ("qdcg-worksheet.line-13", line13)):
        item = _line(row, name)
        assert item["disposition"] == disposition
        assert item.get("code") == code
        if disposition == "published":
            assert item["value"] == value
        else:
            assert missing in item["missing"]


@pytest.mark.parametrize(("key", "answer", "disposition", "line6", "line13", "code", "missing"), CASES)
def test_lines_6_and_13(key: str, answer: str, disposition: str, line6: int | None, line13: int | None,
                        code: str | None, missing: str | None) -> None:
    assert live_coordinate_run.__name__ == "live_coordinate_run"
    probe = trace._probe()
    row = trace.observe(probe, _core(), key, answer)
    _expect(row, disposition, line6, line13, code, missing)


def _single_lookup(parameter: dict[str, Any]) -> dict[str, Any]:
    return {
        "op": "parameter",
        "parameter_id": parameter["parameter_id"],
        "key": {
            "op": "category_literal",
            "fact_type": {"id": "tax.us.2025.filing-status", "version": "v1"},
            "value": "single",
        },
    }


def _mutate(node: Any, kind: str) -> Any:
    if isinstance(node, dict) and node.get("op") == "choose":
        then, otherwise = node.get("then"), node.get("else")
        if kind == "publish_ceiling" and isinstance(otherwise, dict) and otherwise.get("op") == "block" and isinstance(then, dict) and then.get("op") == "parameter":
            node["else"] = copy.deepcopy(then)
        elif kind == "single_fallback" and isinstance(otherwise, dict) and otherwise.get("op") == "block" and isinstance(then, dict) and then.get("op") == "parameter":
            node["else"] = _single_lookup(then)
        elif kind == "block_controls" and isinstance(otherwise, dict) and otherwise.get("op") == "parameter":
            when = node.get("when") or {}
            right = when.get("right") or {}
            if right.get("value") == "qualifying_surviving_spouse":
                node["else"] = {"op": "block", "code": "DEPENDENCY_INVALID", "missing": ["filing_status"]}
        _mutate(node.get("then"), kind)
        _mutate(node.get("else"), kind)
    return node


def _mutant_core(directory: Path, kind: str) -> Any:
    content = directory / "content"
    releases = directory / "releases"
    shutil.copytree(CONTENT, content)
    releases.mkdir()
    for name in (LINE6, LINE13):
        path = content / name
        body = json.loads(path.read_text(encoding="utf-8"))
        _mutate(body["value"], kind)
        path.write_text(json.dumps(body, indent=2) + "\n", encoding="utf-8")
    registry_path = content / "published-packages.v102.json"
    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    bodies = {json.loads((content / name).read_text(encoding="utf-8"))["id"]: json.loads((content / name).read_text(encoding="utf-8")) for name in (LINE6, LINE13)}
    for citizen in registry["citizens"]:
        body = bodies.get(citizen["id"])
        if body is not None and citizen["version"] == "v2":
            citizen["checksum"] = citizen_checksum(body)
    raw = json.dumps(registry, indent=2) + "\n"
    registry_path.write_text(raw, encoding="utf-8")
    release = json.loads((RELEASES / f"{STEM}.v102.json").read_text(encoding="utf-8"))
    release["package_registry_sha256"] = hashlib.sha256(raw.encode("utf-8")).hexdigest()
    (releases / f"{STEM}.v102.json").write_text(json.dumps(release, indent=2) + "\n", encoding="utf-8")
    probe = trace._probe()
    return probe.h.Core("v104", "v102", "v102", content=content, releases=releases)


def _mutant_row(directory: Path, kind: str, key: str, answer: str) -> dict[str, Any]:
    probe = trace._probe()
    found = trace.observe(probe, _mutant_core(directory, kind), key, answer)
    assert isinstance(found, dict)
    row: dict[str, Any] = found
    assert "error" not in row and "refusal" not in row, row.get("error") or row.get("refusal")
    return row


def test_a_refused_status_publishing_its_ceiling_fails_the_check(tmp_path: Path) -> None:
    """The v1 lookup on a no still publishes the head of household ceiling."""
    row = _mutant_row(tmp_path, "publish_ceiling", "hoh/none", "no")
    assert _line(row, "qdcg-worksheet.line-6")["value"] == 64750
    assert _line(row, "qdcg-worksheet.line-13")["value"] == 566700
    with pytest.raises(AssertionError):
        _expect(row, "blocked", None, None, "DEPENDENCY_INVALID", "hoh.tests-met")


def test_a_fallback_to_the_single_ceiling_fails_the_check(tmp_path: Path) -> None:
    """A no that publishes the single amounts is not the instructed block."""
    row = _mutant_row(tmp_path, "single_fallback", "hoh/none", "no")
    assert _line(row, "qdcg-worksheet.line-6")["value"] == 48350
    assert _line(row, "qdcg-worksheet.line-13")["value"] == 533400
    with pytest.raises(AssertionError):
        _expect(row, "blocked", None, None, "DEPENDENCY_INVALID", "hoh.tests-met")


def test_a_control_status_blocking_fails_the_check(tmp_path: Path) -> None:
    """Single keeps its own ceiling. Blocking that lookup fails the control."""
    row = _mutant_row(tmp_path, "block_controls", "single/none", "none")
    assert _line(row, "qdcg-worksheet.line-6")["disposition"] == "blocked"
    assert _line(row, "qdcg-worksheet.line-13")["disposition"] == "blocked"
    with pytest.raises(AssertionError):
        _expect(row, "published", 48350, 533400, None, None)
