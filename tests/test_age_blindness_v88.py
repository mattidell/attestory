"""Published core v88 asks age, blindness, and the separate-return condition.

Measured reason: the check run made 39 distinct authority, matrix and late
live_coordinate_run calls in 236.4 s, then 298 recorded v83 calls in
558.2 s on 4 workers. That is outside the 3 second fast-lane budget.
The 775-list result, including the v81 comparison, is the committed
neighbour evidence (age-blindness-asked-evidence/track0-neighbour.json).

Hand values are the chart arithmetic in the age Track 0 module (law.json
anchors), never a number read off a run. The 298 recorded v83 returns are
answered false as the record implies and read from the fixture file in
place. A v83 fixture is the pin, so that pin must be identical. The
recorded replay uses at most four worker processes.
"""

from __future__ import annotations

import hashlib
import json
import multiprocessing
import os
import time
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
from types import ModuleType
from typing import Any, cast

import pytest

from tests import evidence_loader

pytestmark = pytest.mark.live

REPO = Path(__file__).resolve().parents[1]
EVIDENCE = REPO / "docs/phases/engine-breadth/milestones/age-blindness-asked-evidence"
QW = REPO / "docs/phases/engine-breadth/milestones/question-wording-evidence"
FIXTURES = REPO / "tests/fixtures"
P = "tax.us.2025."

# Chart anchors. track0.BASE, PER_BOX and TAX are these values.
BASE = {
    "single": 15750,
    "head_of_household": 23625,
    "married_filing_jointly": 31500,
    "married_filing_separately": 15750,
    "qualifying_surviving_spouse": 31500,
}
PER_BOX = {
    "single": 2000,
    "head_of_household": 2000,
    "married_filing_jointly": 1600,
    "married_filing_separately": 1600,
    "qualifying_surviving_spouse": 1600,
}
TAX = {
    ("single", 34250): 3875,
    ("single", 32250): 3635,
    ("single", 26250): 2915,
    ("single", 24250): 2675,
    ("married_filing_jointly", 18500): 1853,
    ("married_filing_jointly", 10900): 1093,
    ("married_filing_separately", 32650): 3683,
    ("married_filing_separately", 34250): 3875,
    ("qualifying_surviving_spouse", 18500): 1853,
    ("head_of_household", 26375): 2825,
}
TAXPAYER_AGE = (
    "Were you born before January 2, 1961? A person reaches age 65 on the day before "
    "their 65th birthday, so a birthday of January 1, 1961 counts and January 2, 1961 "
    "does not. If this return is for someone who died in 2025 before reaching age 65, "
    "answer no."
)
TAXPAYER_BLIND = (
    "Were you totally blind on December 31, 2025, or do you have a statement certified "
    "by your eye doctor (ophthalmologist or optometrist) that you can't see better than "
    "20/200 in your better eye with glasses or contact lenses, or that your field of "
    "vision is 20 degrees or less? If your eye condition isn't likely to improve beyond "
    "the conditions listed above, you can get a statement certified by your eye doctor "
    "(ophthalmologist or optometrist) to this effect instead."
)
SPOUSE_AGE = (
    "Was your spouse born before January 2, 1961? A person reaches age 65 on the day "
    "before their 65th birthday. If your spouse died in 2025 before reaching age 65, "
    "answer no."
)
SPOUSE_BLIND = (
    "Was your spouse totally blind on December 31, 2025, or does your spouse have a "
    "statement certified by an eye doctor (ophthalmologist or optometrist) that they "
    "can't see better than 20/200 in the better eye with glasses or contact lenses, or "
    "that their field of vision is 20 degrees or less? If your spouse's eye condition "
    "isn't likely to improve beyond the conditions listed above, your spouse can get a "
    "statement certified by an eye doctor (ophthalmologist or optometrist) to this "
    "effect instead."
)
COND_QUESTION = (
    "Is it true that your spouse had no income, isn't filing a return, and can't be claimed "
    "as a dependent on another person's return?"
)
SENTENCES = {
    "taxpayer-over-65": TAXPAYER_AGE,
    "taxpayer-blind": TAXPAYER_BLIND,
    "spouse-over-65": SPOUSE_AGE,
    "spouse-blind": SPOUSE_BLIND,
    "standard-deduction.spouse-separate-condition": COND_QUESTION,
}
# Lines this core can change. A number the fixture published for one of
# these must still be that number.
WATCHED_LINES = (
    "form1040.line-12e",
    "form1040.line-13b",
    "form1040.line-15",
    "form1040.line-16",
    "schedule1a.line36a-taxpayer",
    "schedule1a.line36b-spouse",
)


def _normalized(node: Any) -> Any:
    """The act list with every synthetic demo.* id replaced by one placeholder."""
    if isinstance(node, dict):
        return {key: _normalized(value) for key, value in node.items()}
    if isinstance(node, list):
        return [_normalized(value) for value in node]
    if isinstance(node, str) and node.startswith("demo."):
        return "demo.*"
    return node


def _digest(acts: list[dict[str, Any]]) -> str:
    return hashlib.sha256(json.dumps(_normalized(acts), sort_keys=True, default=str).encode("utf-8")).hexdigest()


def _age() -> ModuleType:
    return evidence_loader.load(EVIDENCE / "track0.py", "aba_t1_age_track0")


def _published(track: ModuleType) -> Any:
    return track.probe().harness().Core("v88", "v86", "v86")


def _authority_failures(track: ModuleType, spec: dict[str, Any], result: dict[str, Any]) -> list[str]:
    measured = {"v88": result}
    if spec.get("open"):
        failures = list(track.judge_open(measured, spec["ask"], {}))
        missing = set(result.get("missing") or [])
        for symbol in spec.get("missing") or []:
            if symbol not in missing:
                failures.append(f"v88 did not block on {symbol}")
        return failures
    bits = spec["bits"]
    dependent = bool(spec.get("dependent"))
    status = "single" if dependent else spec["status"]
    spouse = bits[2:] if spec.get("record_spouse") or status in (track.MFJ, track.MFS) else (False, False)
    if spec.get("record_spouse"):
        hand = track.hand_amounts(status, bits[0], bits[1], False, False)
    else:
        hand = track.hand_amounts(
            status, bits[0], bits[1], spouse[0], spouse[1],
            dependent=dependent, condition=bool(spec.get("condition", True)))
    ask = spec["expect_ask"] if "expect_ask" in spec else None
    return list(track.judge_answered(measured, hand, ask=ask))


def _matrix_failures(track: ModuleType, spec: dict[str, Any], result: dict[str, Any]) -> list[str]:
    measured = {"v88": result}
    if spec.get("open"):
        return list(track.judge_open(measured, spec["ask"], {}))
    bits = spec["bits"]
    dependent = bool(spec.get("dependent"))
    status = spec["status"]
    condition = spec.get("condition")
    condition_yes = True if condition is None else bool(condition)
    if spec.get("record_spouse"):
        hand = track.hand_amounts(status, bits[0], bits[1], False, False)
    else:
        hand = track.hand_amounts(
            "single" if dependent else status, bits[0], bits[1], bits[2], bits[3],
            dependent=dependent, condition=condition_yes)
    return list(track.judge_answered(measured, hand))


def _late_failures(track: ModuleType, step: dict[str, Any], result: dict[str, Any]) -> list[str]:
    measured = {"v88": result}
    if step.get("open"):
        return list(track.judge_open(measured, step["ask"], {}))
    return list(track.judge_answered(measured, step["hand"]))


def _shown(spec_or_step: dict[str, Any], result: dict[str, Any]) -> list[str]:
    """Open cases show each asked sentence. An answered case keeps its ask list and shows none of them."""
    if not spec_or_step.get("open"):
        return []
    ask = list(spec_or_step.get("ask") or [])
    questions = list(result.get("questions") or [])
    return [slug for slug in ask if SENTENCES[slug] not in questions]


@pytest.fixture(scope="module")
def age_track0() -> ModuleType:
    return _age()


def test_hand_anchors_are_the_chart(age_track0: ModuleType) -> None:
    """The literals below are the law.json chart, not a coordinate run."""
    assert age_track0.BASE == BASE
    assert age_track0.PER_BOX == PER_BOX
    assert age_track0.TAX == TAX
    assert age_track0.questions() == SENTENCES
    single = age_track0.hand_amounts("single", False, False, False, False)
    assert single["form1040.line-12e"] == 15750
    assert single["form1040.line-15"] == 34250
    assert single["form1040.line-16"] == 3875
    joint = age_track0.hand_amounts("married_filing_jointly", False, False, True, False)
    assert joint["form1040.line-12e"] == 33100
    assert joint["form1040.line-13b"] == 6000
    assert joint["schedule1a.line36b-spouse"] == 6000
    assert joint["form1040.line-16"] == 1093
    separate_no = age_track0.hand_amounts(
        "married_filing_separately", False, False, True, False, condition=False)
    assert separate_no["form1040.line-12e"] == 15750
    assert separate_no["form1040.line-15"] == 34250
    assert separate_no["form1040.line-16"] == 3875
    separate_yes = age_track0.hand_amounts(
        "married_filing_separately", False, False, True, False, condition=True)
    assert separate_yes["form1040.line-12e"] == 17350
    assert separate_yes["form1040.line-16"] == 3683
    qss = age_track0.hand_amounts("qualifying_surviving_spouse", False, False, True, False)
    assert qss["form1040.line-12e"] == 31500
    assert qss["form1040.line-15"] == 18500
    assert qss["form1040.line-16"] == 1853
    dependent = age_track0.hand_amounts("single", True, True, False, False, dependent=True)
    assert dependent["form1040.line-12e"] == 19750
    assert dependent["form1040.line-16"] == 2675


def test_authority_matrix_and_late_on_published_v88(age_track0: ModuleType) -> None:
    """Each distinct act list runs once, through live_coordinate_run and the presentation model."""
    track = age_track0
    core = _published(track)
    groups: dict[str, dict[str, Any]] = {}
    order: list[str] = []

    def _add(kind: str, label: str, spec: dict[str, Any], acts: list[dict[str, Any]]) -> None:
        digest = _digest(acts)
        if digest not in groups:
            groups[digest] = {"acts": acts, "rows": []}
            order.append(digest)
        groups[digest]["rows"].append((kind, label, spec))

    for spec in cast(list[dict[str, Any]], track.authority_specs()):
        _add("authority", str(spec["id"]), spec, cast(list[dict[str, Any]], track.acts_of(spec)))
    for spec in cast(list[dict[str, Any]], track.matrix_specs()):
        _add("matrix", str(spec["id"]), spec, cast(list[dict[str, Any]], track.acts_of(spec)))
    for trace in cast(list[dict[str, Any]], track.late_steps()):
        for step in cast(list[dict[str, Any]], trace["steps"]):
            _add("late", f"{trace['id']}/{step['name']}", step, cast(list[dict[str, Any]], step["acts"]))

    started = time.perf_counter()
    failures: list[str] = []
    for index, digest in enumerate(order, 1):
        group = groups[digest]
        result = cast(dict[str, Any], track.execute(core, group["acts"], f"demo.aba.t1.v88.{digest[:12]}"))
        if result.get("outcome") == "success" and (
            "questions" not in result or "blocked_fields" not in result
        ):
            failures.append(f"{digest[:12]} did not read the presentation model")
        for kind, label, spec in group["rows"]:
            if kind == "authority":
                bad = _authority_failures(track, spec, result)
            elif kind == "matrix":
                bad = _matrix_failures(track, spec, result)
            else:
                bad = _late_failures(track, spec, result)
            missing = _shown(spec, result) if result.get("outcome") == "success" else []
            if bad or missing:
                failures.append(f"{label}: {bad or missing}")
        if index % 10 == 0 or index == len(order):
            print(f"ABA_V88_CASES {index}/{len(order)}", flush=True)
    wall = time.perf_counter() - started
    print(f"ABA_V88_CASES runs={len(order)} wall_s={wall:.1f} failed={len(failures)}", flush=True)
    assert failures == []


def _fixture_file(name: str) -> dict[str, Any]:
    return cast(dict[str, Any], json.loads((FIXTURES / name).read_text(encoding="utf-8")))


def _recorded_pin(expected: dict[str, Any], key: str) -> dict[str, Any]:
    group, _, name = key.partition("/")
    if group == "track0":
        return cast(dict[str, Any], expected["track0"][name])
    if group == "returns":
        return cast(dict[str, Any], expected["returns"][name]["v83"])
    return cast(dict[str, Any], expected["zero_sample"][name]["v83"])


def _late_alias() -> dict[str, str]:
    """Map a neighbour late key onto the fixture's late/{step id}."""
    import sys
    found: dict[str, str] = {}
    pairs = (
        ("v84", "qw_t0_box7_test", "box7_cases"),
        ("v85", "qw_t0_box4_test", "box4_cases"),
    )
    for prefix, module_name, method in pairs:
        cases = getattr(sys.modules[module_name], method)()
        for trace in cases["late"]:
            index = 0
            for step in trace.get("steps") or []:
                if isinstance(step, dict) and "acts" in step:
                    found[f"{prefix}/late/{trace['id']}/{index}"] = f"late/{step['id']}"
                    index += 1
    return found


def _expect(key: str, alias: dict[str, str]) -> tuple[str, dict[str, Any]]:
    """The fixture entry for one recorded list. ``pin`` is a full v83 pin."""
    prefix, _, rest = key.partition("/")
    if prefix == "v83":
        return "pin", _recorded_pin(_fixture_file("f1099b_backup_withholding_v83/expected.json"), rest)
    if prefix == "v82":
        body = _fixture_file("sale_family_audit_v82/expected.json")
        return "subset", cast(dict[str, Any], body["track0"][rest])
    if prefix == "v81":
        group, _, name = rest.partition("/")
        entry = cast(dict[str, Any], _fixture_file("code_b_sales_v81/expected.json")[group][name])
        if group == "case":
            return "subset", entry
        return "subset", cast(dict[str, Any], entry["v81"])
    table = "f1099b_box7_loss_v84/expected.json" if prefix == "v84" else "f1099b_box4_only_v85/expected.json"
    fixture_key = alias.get(key, rest)
    view = cast(dict[str, Any], _fixture_file(table)["cases"][fixture_key]["view"])
    return "view", view


def _as_number(value: Any) -> int | float | None:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        if isinstance(value, list) and value and isinstance(value[-1], (int, float)) and not isinstance(value[-1], bool):
            return value[-1]
        return None
    return value


def _fixture_diffs(key: str, pin: dict[str, Any], alias: dict[str, str]) -> tuple[list[str], bool]:
    """Disagreements with the fixture, and whether a v81 list is an earlier core's result.

    v83 stores the pin itself. Other fixtures store that core's projection:
    a number both sides publish has to match. A standard-deduction number
    has to survive, except on the uncorrected v81 exports. Those lists are
    blocked or refused on the published core where v81 published a number,
    because questions added after v81 are still unanswered. That is not an
    age change: the same pin is what published v87 produces.
    """
    kind, fixture = _expect(key, alias)
    diffs: list[str] = []
    earlier = False
    questions = list(pin.get("questions") or [])
    asked = [sentence for sentence in SENTENCES.values() if sentence in questions]
    if asked:
        diffs.append("asked an age or condition question")
    if kind == "pin" and pin != fixture:
        diffs.append("pin differs from the v83 fixture")
    v81 = key.startswith("v81/")
    if isinstance(fixture, dict) and "error" in fixture and "lines" not in fixture:
        if pin.get("error") != fixture.get("error"):
            diffs.append(f"error {pin.get('error')!r} != {fixture.get('error')!r}")
        return diffs, earlier
    if pin.get("error") and kind != "pin":
        if v81:
            earlier = True
        else:
            diffs.append(f"error {pin.get('error')!r}")
        return diffs, earlier
    flines: Any = fixture.get("lines") if isinstance(fixture, dict) else None
    plines: Any = pin.get("lines")
    if not isinstance(flines, dict) or not isinstance(plines, dict):
        return diffs, earlier
    for name, expected in flines.items():
        got = plines.get(name)
        expected_number = _as_number(expected)
        got_number = _as_number(got)
        if expected_number is not None and got_number is not None and expected_number != got_number:
            diffs.append(f"{name} fixture {expected_number} pin {got_number}")
        if name in WATCHED_LINES and expected_number is not None and got_number is None:
            if v81:
                earlier = True
            else:
                diffs.append(f"{name} fixture {expected_number} pin {got!r}")
    return diffs, earlier


def _recorded_shard(payload: tuple[list[tuple[str, list[dict[str, Any]]]], dict[str, str]]) -> dict[str, Any]:
    """One shard of the recorded replay. Importable by a spawned worker."""
    work, alias = payload
    qw_rerun = evidence_loader.load(QW / "rerun.py", "aba_t1_qw_rerun")
    aba = evidence_loader.load(EVIDENCE / "rerun.py", "aba_t1_aba_rerun")
    test = qw_rerun.load_test()
    core = test.track0().h.Core("v88", "v86", "v86")
    diffs: list[dict[str, Any]] = []
    earlier = 0
    for key, acts in work:
        slug = key.replace("/", ".")
        prepared = aba.adopt_v88(core, aba.answered(acts, aba.implied(acts)))
        pin = cast(dict[str, Any], qw_rerun._pin_run(test, core, prepared, "demo.aba.t1.v88.recorded." + slug))
        bad, v81_earlier = _fixture_diffs(key, pin, alias)
        if bad:
            diffs.append({"id": key, "fields": bad[:8]})
        if v81_earlier:
            earlier += 1
    return {"runs": len(work), "diffs": diffs, "v81_earlier": earlier}


def _recorded_workers() -> int:
    count = os.cpu_count() or 2
    return min(4, max(1, count - 1))


def test_recorded_returns_match_their_fixtures() -> None:
    """The recorded lists, answered false, against the fixture files in place."""
    qw = evidence_loader.load(QW / "track0.py", "aba_t1_qw_track0")
    work = [
        item for item in cast(list[tuple[str, list[dict[str, Any]]]], qw.neighbour_tasks())
        if item[0].startswith("v83/")
    ]
    only = {item for item in os.environ.get("ABA_V88_ONLY", "").split(",") if item}
    if only:
        work = [item for item in work if item[0] in only]
    else:
        assert len(work) == 298
    alias = _late_alias()
    workers = _recorded_workers()
    shards = [work[index::workers] for index in range(workers) if work[index::workers]]
    started = time.perf_counter()
    context = multiprocessing.get_context("spawn")
    diffs: list[dict[str, Any]] = []
    runs = 0
    earlier = 0
    with ProcessPoolExecutor(max_workers=workers, mp_context=context) as pool:
        for part in pool.map(_recorded_shard, [(shard, alias) for shard in shards]):
            runs += int(part["runs"])
            earlier += int(part["v81_earlier"])
            diffs.extend(cast(list[dict[str, Any]], part["diffs"]))
    wall = time.perf_counter() - started
    print(
        f"ABA_V88_RECORDED runs={runs} wall_s={wall:.1f} workers={workers} "
        f"diffs={len(diffs)} of={len(work)} v81_earlier={earlier}",
        flush=True,
    )
    for row in diffs[:12]:
        print(f"ABA_V88_DIFF {row['id']} {row['fields']}", flush=True)
    assert runs == len(work)
    assert diffs == []
