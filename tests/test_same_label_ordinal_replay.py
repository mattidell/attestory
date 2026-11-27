"""Controls for the full-surface comparator used by same-label-ordinal."""
from pathlib import Path
from typing import Any

import pytest

from tests import evidence_loader

REPLAY = (
    Path(__file__).resolve().parents[1]
    / "docs/phases/engine-breadth/milestones/same-label-ordinal-evidence/replay.py"
)


def _saved(*reasons: dict[str, Any], value: int = 0) -> dict[str, Any]:
    return {
        "outcome": "success",
        "model": {"sections": [{"id": "demo.line", "resolved": {"reasons": list(reasons)}}]},
        "report": {"demo_value": value},
    }


def test_replay_accepts_only_probe_member_ordinals_and_order() -> None:
    replay = evidence_loader.load(REPLAY, "slo_repair_replay")
    first = {"memberLabel": "Demo Sam", "sentence": "Demo first question"}
    second = {"memberLabel": "Demo Sam", "sentence": "Demo second question"}
    before = _saved(first, second)
    after = _saved(dict(second, memberOrdinal=1), dict(first, memberOrdinal=2))
    assert replay.compare_saved(before, after, probe=True)["class"] == "ordinals-and-order"
    assert replay.compare_saved(before, after, probe=False)["class"] == "unexpected"


def test_replay_control_rejects_a_report_value_change() -> None:
    replay = evidence_loader.load(REPLAY, "slo_repair_replay")
    assert replay.report_value_control()["class"] == "unexpected"


def test_replay_control_rejects_reordering_without_ordinals() -> None:
    replay = evidence_loader.load(REPLAY, "slo_repair_replay")
    first = {"memberLabel": "Demo Sam", "sentence": "Demo first question"}
    second = {"memberLabel": "Demo Sam", "sentence": "Demo second question"}
    assert replay.compare_saved(_saved(first, second), _saved(second, first), probe=True)["class"] == "unexpected"


def test_replay_uses_the_candidate_build_parent(monkeypatch: pytest.MonkeyPatch) -> None:
    replay = evidence_loader.load(REPLAY, "slo_repair_replay")

    def git(*args: str) -> str:
        if args[0] == "log":
            assert args[-1] == "demo.candidate"
            assert "--grep=^build(same-label-ordinal)" in args
            return "demo.close\tclose(same-label-ordinal): closeout\ndemo.build\tbuild(same-label-ordinal): ordinal\n"
        assert args == ("rev-parse", "--verify", "demo.build^")
        return "demo.plan\n"

    monkeypatch.setattr(replay, "_git", git)
    assert replay._baseline_commit("demo.candidate") == "demo.plan"
