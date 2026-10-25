"""Seeded-defect test for the required-versus-read path mode.

The helper ``tests/helpers/rvr_seeded_run.py`` publishes one synthetic rule
through ``live_coordinate_run`` on a throwaway publication surface. The rule
reads an answer only inside a branch that a gate selects. This test runs the
helper under the path mode's probe and asserts the reported result:

* gate closed (the answer's branch is never taken): the rule is reported with
  the answer as a required input absent from the published finding's pins;
* gate open (the branch is taken): the answer is pinned and not reported.

It drives the live coordinator, so it is an integration test in the live
lane. The static check's tests stay in ``tests/test_required_versus_read.py``.
"""

from __future__ import annotations

import collections
import os
from pathlib import Path
from typing import Any

import pytest

# Drives live_coordinate_run on a throwaway surface (~5 s): an integration test.
pytestmark = pytest.mark.live

from tools.required_versus_read import (
    index_content,
    path_report,
    path_summary,
    read_dumps,
    run_path_probe,
)

REPO = Path(__file__).resolve().parents[1]
HELPER = REPO / "tests" / "helpers" / "rvr_seeded_run.py"
RULE_KEY = "probe.rule.rvr-branch@v1"
ANSWER = "probe.rvr.answer"
GATE = "probe.rvr.gate"
CLOSED_TEST = "test_gate_closed_answer_is_bound_but_never_read"
OPEN_TEST = "test_gate_open_answer_is_read"


@pytest.fixture(scope="module")
def seeded_run(tmp_path_factory: pytest.TempPathFactory) -> tuple[Path, dict[tuple[str, str], dict[str, Any]]]:
    """Run the helper once under the probe; return its surface root and the probe records."""
    base = tmp_path_factory.mktemp("rvr-seeded")
    surfaces = base / "surfaces"
    surfaces.mkdir()
    dump_dir = base / "dump"
    dump_dir.mkdir()
    previous = os.environ.get("RVR_SEEDED_ROOT")
    os.environ["RVR_SEEDED_ROOT"] = str(surfaces)
    try:
        returncode = run_path_probe([str(HELPER)], dump_dir)
    finally:
        if previous is None:
            os.environ.pop("RVR_SEEDED_ROOT", None)
        else:
            os.environ["RVR_SEEDED_ROOT"] = previous
    assert returncode == 0, "the seeded helper's own assertions failed"
    return surfaces, read_dumps(dump_dir)


def _summary_for(
    surfaces: Path, label: str, test_name: str,
    records: dict[tuple[str, str], dict[str, Any]],
) -> tuple[collections.Counter[str], dict[str, dict[str, Any]]]:
    selected = {key: row for key, row in records.items() if key[0].endswith(test_name)}
    assert selected, f"no probe records for {test_name}"
    return path_summary(selected, index_content(surfaces / label / "members"))


def test_unread_branch_answer_is_reported(
    seeded_run: tuple[Path, dict[tuple[str, str], dict[str, Any]]],
    capsys: pytest.CaptureFixture[str],
) -> None:
    surfaces, records = seeded_run
    stats, rules = _summary_for(surfaces, "gate-closed", CLOSED_TEST, records)

    assert stats["matched to a rule evaluation"] == 1
    rule = rules[RULE_KEY]
    assert dict(rule["absent_count"]) == {ANSWER: 1}
    assert rule["status"][ANSWER] == collections.Counter({"unpinned": 1})
    assert rule["status"][GATE] == collections.Counter({"pinned": 1})

    path_report(stats, {RULE_KEY: rule}, "seeded gate-closed run", set())
    printed = capsys.readouterr().out
    assert f"{RULE_KEY} | no | 1 | 1 | 1 | {ANSWER}: 1 | -" in printed


def test_read_branch_answer_is_not_reported(
    seeded_run: tuple[Path, dict[tuple[str, str], dict[str, Any]]],
) -> None:
    surfaces, records = seeded_run
    stats, rules = _summary_for(surfaces, "gate-open", OPEN_TEST, records)

    assert stats["matched to a rule evaluation"] == 1
    rule = rules[RULE_KEY]
    assert not rule["absent_count"]
    assert rule["status"][ANSWER] == collections.Counter({"pinned": 1})
