"""Line 25 pairing on core v77, through live_coordinate_run.

The 44 rows are the P0 case table. v76 results are the recorded probe output.
A row that v76 already blocked still names the withholding fact. A row that
v76 published without that fact's row on the same statement now blocks and
shows that fact's existing question. Answered rows, the $0 answer, and a
withholding-only extra publish the recorded amount.
"""

from __future__ import annotations

import copy
import importlib.util
import json
from decimal import Decimal
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any

import pytest

from packages.derivation.live import live_coordinate_run
from packages.derivation.live_workspace import WorkspaceCapability
from packages.derivation.production_resolver import PublicationSurface
from packages.kernel.findings import FindingModelError
from tests.helpers import current_core_returns as ccr
from tests.test_form_1099_k_income import _handover
from tests.test_form_1099_withholding import YEAR
from tests.test_refund_or_amount_owed_track1 import _finish

ROOT = Path(__file__).resolve().parents[1]
PROBE_PATH = (
    ROOT
    / "docs"
    / "phases"
    / "engine-breadth"
    / "milestones"
    / "statement-withholding-pairing-evidence"
    / "probe.py"
)
ORACLE_PATH = PROBE_PATH.with_name("probe-output.json")
P = "tax.us.2025."

V76 = (
    "package.core-calculations.v76.json",
    "v76",
    "demo.release.sli-worksheet-integration.2025.v74.json",
    "v74",
    "published-packages.v74.json",
)
V77 = (
    "package.core-calculations.v77.json",
    "v77",
    "demo.release.sli-worksheet-integration.2025.v75.json",
    "v75",
    "published-packages.v75.json",
)

WITHHOLDING = {
    "int": P + "f1099int.box4-withholding",
    "div": P + "f1099div.box4-withholding",
    "ira": P + "f1099r.ira-box4-withholding",
    "g": P + "f1099g.box4-withholding",
    "ssa": P + "ssa1099.box6-voluntary-withholding",
    "w2": P + "w2.box2-withholding",
    "cross": P + "f1099div.box4-withholding",
}
QUESTIONS = {
    P + "f1099int.box4-withholding": (
        "Enter the federal income tax withheld in box 4 of each Form 1099-INT "
        "you or your spouse received for 2025. If box 4 is blank, enter $0."
    ),
    P + "f1099div.box4-withholding": (
        "Enter the federal income tax withheld in box 4 of each Form 1099-DIV "
        "you or your spouse received for 2025. If box 4 is blank, enter $0."
    ),
    P + "f1099r.ira-box4-withholding": (
        "Enter the federal income tax withheld in box 4 of each Form 1099-R "
        "you or your spouse received for 2025. If box 4 is blank, enter $0."
    ),
    P + "f1099g.box4-withholding": (
        "Enter the federal income tax withheld in box 4 of each Form 1099-G "
        "you or your spouse received for 2025. If box 4 is blank, enter $0."
    ),
    P + "ssa1099.box6-voluntary-withholding": (
        "Enter the voluntary federal income tax withheld in box 6 of each Form "
        "SSA-1099 you or your spouse received for 2025. If box 6 is blank, enter $0."
    ),
    P + "w2.box2-withholding": (
        "Enter the federal income tax withheld in box 2 of each Form W-2 you or "
        "your spouse received for 2025. If box 2 is blank, enter $0."
    ),
}
V76_SPOT = ("int.both-answered", "int.offset", "w2.second-slip-unanswered")


def _load_probe() -> Any:
    spec = importlib.util.spec_from_file_location("statement_withholding_pairing_probe", PROBE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("pairing probe did not load")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


PROBE = _load_probe()
CASES: list[tuple[Any, ...]] = list(PROBE.case_table())
ORACLE = {
    row["id"]: row
    for row in json.loads(ORACLE_PATH.read_text(encoding="utf-8"))["cases"]
}


def _money(amount: float) -> str:
    return format(Decimal(str(amount)), "f")


def _family(case_id: str) -> str:
    return "w2" if case_id.startswith("w2.") else case_id.split(".", 1)[0]


def _line_name(case_id: str) -> str:
    return "line25a" if case_id.startswith("w2.") else "line25b"


def _section_id(case_id: str) -> str:
    return "line-25a" if case_id.startswith("w2.") else "line-25b"


def _expects_block(case_id: str) -> bool:
    if case_id.endswith(".same-statement-second"):
        return False
    return case_id == "cross.int-answered-div-open" or case_id.endswith(("offset", "unanswered"))


def _run(acts: list[dict[str, object]], name: str, core: tuple[str, str, str, str, str]) -> dict[str, Any]:
    package, version, release, rel_version, registry = core
    surface = PublicationSurface(ccr.RELEASE_DIR, ccr.CONTENT / registry, ccr.CONTENT)
    finished = _handover(
        _finish(
            acts,
            package_path=ccr.CONTENT / package,
            package_version=version,
            release_path=ccr.RELEASE_DIR / release,
            release_version=rel_version,
            note=name,
        ),
        surface=surface,
        reconfirm=True,
    )
    with TemporaryDirectory() as tmp:
        outcome = live_coordinate_run(
            WorkspaceCapability(Path(tmp) / "L"),
            repo_root=ROOT,
            authoritative_acts=finished,
            workspace_revision=len(finished),
            run_scope={"jurisdiction": "us", "year": YEAR},
            scope_user=ccr.USER,
            request={"schema": "run-request.v1"},
            run_id=name,
            governance_pins=[],
            surface=surface,
            output_name="out.json",
        )
        if outcome.refusal is not None:
            return {"reachable": False, "refusal": f"{outcome.refusal.reason} {outcome.refusal.detail}"}
        assert outcome.output_path is not None and outcome.presentation_path is not None
        pubs = {str(item.finding["symbol"]): item.finding for item in outcome.publications or ()}
        report = json.loads(outcome.output_path.read_text(encoding="utf-8"))
        model = json.loads(outcome.presentation_path.read_text(encoding="utf-8"))
    lines: dict[str, str | None] = {}
    for label, symbol in PROBE.LINES.items():
        lines[label] = _money(float(pubs[symbol]["value"])) if symbol in pubs else None
    blocks = []
    for row in report.get("dispositions", []):
        if row.get("disposition") != "blocked":
            continue
        artifact = str(row.get("artifact_id", ""))
        if "line25a" in artifact or "line25b" in artifact:
            blocks.append(
                {
                    "artifact": artifact,
                    "code": row.get("code"),
                    "missing": [str(item) for item in row.get("missing", [])],
                }
            )
    return {"reachable": True, "lines": lines, "line_blocks": blocks, "model": model}


def _sentences(model: dict[str, Any], section_id: str) -> list[str]:
    section = next(item for item in model["sections"] if item["id"] == section_id)
    reasons = section["resolved"].get("reasons") or []
    return [str(reason["sentence"]) for reason in reasons]


def _assert_matches_oracle(result: dict[str, Any], case_id: str) -> None:
    recorded = ORACLE[case_id]
    assert result["reachable"] is True
    assert result["lines"] == recorded["lines"]
    got = [
        (block["code"], [item.removeprefix(P) for item in block["missing"]])
        for block in result["line_blocks"]
    ]
    recorded_blocks = [(block["code"], block["missing"]) for block in recorded.get("line_blocks") or []]
    assert got == recorded_blocks


@pytest.mark.parametrize(("case_id", "builder"), [(row[0], row[4]) for row in CASES], ids=[row[0] for row in CASES])
def test_v77_row(case_id: str, builder: Any) -> None:
    recorded = ORACLE[case_id]
    if case_id.endswith(".same-statement-second"):
        assert recorded["reachable"] is False
        with pytest.raises(FindingModelError, match="already in the family"):
            _run(builder(), f"demo.swp.v77.{case_id}", V77)
        return
    result = _run(builder(), f"demo.swp.v77.{case_id}", V77)
    assert result["reachable"] is True, result.get("refusal")
    fact = WITHHOLDING[_family(case_id)]
    line = _line_name(case_id)
    if _expects_block(case_id):
        assert result["lines"][line] is None
        target = [block for block in result["line_blocks"] if str(block["artifact"]).endswith("rule.form1040-" + line)]
        assert target == [
            {
                "artifact": P + "rule.form1040-" + line,
                "code": "DEPENDENCY_ABSENT",
                "missing": [fact],
            }
        ]
        assert QUESTIONS[fact] in _sentences(result["model"], _section_id(case_id))
        held = ("line24", "line25a") if line == "line25b" else ("line24", "line25b")
        for label in held:
            assert result["lines"][label] == recorded["lines"][label]
        return
    assert result["lines"] == recorded["lines"]
    assert result["line_blocks"] == []


@pytest.mark.parametrize("case_id", V76_SPOT)
def test_v76_row_matches_the_recorded_probe(case_id: str) -> None:
    builder = next(row[4] for row in CASES if row[0] == case_id)
    result = _run(builder(), f"demo.swp.v76.{case_id}", V76)
    _assert_matches_oracle(result, case_id)


def test_a_return_with_no_form_1099_is_unchanged() -> None:
    assert len(CASES) == 44
    assert set(ORACLE) == {row[0] for row in CASES}
    old = _run(PROBE._no_statements(), "demo.swp.v76.no-1099", V76)
    new = _run(PROBE._no_statements(), "demo.swp.v77.no-1099", V77)
    assert old["reachable"] is True and new["reachable"] is True
    assert new["lines"] == old["lines"]
    assert new["lines"]["line25a"] == "4500.0"
    assert new["lines"]["line25b"] == "0.0"
    assert new["line_blocks"] == []


def test_a_joint_return_with_one_statement_per_spouse_is_unchanged() -> None:
    acts = PROBE.family_return("int", 2, [50.0, 30.0], joint=True)
    old = _run(copy.deepcopy(acts), "demo.swp.v76.joint", V76)
    new = _run(copy.deepcopy(acts), "demo.swp.v77.joint", V77)
    assert old["reachable"] is True and new["reachable"] is True
    assert new["lines"] == old["lines"]
    assert new["lines"]["line25b"] == "80.0"
    assert new["line_blocks"] == []
