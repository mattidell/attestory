"""Published core v87 runs the question-wording Track 0 cases, and the 298 recorded v83 runs.

v87 is package core-calculations v87, registry v85 and release v85. The
authority, matrix and late cases come from this milestone's track0.py. Each
distinct v87 act list runs once through ``live_coordinate_run`` and the
presentation model; cases that share an act list are judged on that one run.
Hand values are the instruction values track0.py records from law.json,
written here, never read from a run. The question text shown is pinned
exactly.

The 298 recorded v83 runs are compared with
``tests/fixtures/f1099b_backup_withholding_v83/expected.json`` in place, as
the v86 module replays them: 207 as recorded, 91 restored with present=no.
The fixture is not copied.

One run is several seconds, over the 3.0 s fast-lane budget, so this module
is live.
"""

from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import sys
from pathlib import Path
from types import ModuleType
from typing import Any, cast

import pytest

from tests import evidence_loader

# One live_coordinate_run is several seconds, over the 3.0 s fast-lane budget.
pytestmark = pytest.mark.live

REPO = Path(__file__).resolve().parents[1]
CONTENT = REPO / "packages/content/tax/2025"
EVIDENCE = REPO / "docs/phases/engine-breadth/milestones/question-wording-evidence"
BOX4_EVIDENCE = REPO / "docs/phases/engine-breadth/milestones/f1099b-box4-only-evidence"
AUDIT = REPO / "docs/phases/engine-breadth/milestones/sale-family-audit-evidence/audit_harness.py"
RECORDED_PATH = REPO / "tests/fixtures/f1099b_backup_withholding_v83/expected.json"
TRACK0_NAME = "qw_t1_v87_live_track0"
RECORDED_NAME = "qw_t1_v87_recorded"
HARNESS_NAME = "qw_t1_v87_harness"
PRESENT = "tax.us.2025.f1099b.no-sale-box4-present"

# The decided v87 words (Decisions 1-3), exactly as the page shows them.
WORDS = {
    "wash_st": (
        "Have you recorded the wash-sale loss adjustment amount of every covered short-term sale "
        "with a wash-sale loss adjustment (a loss disallowed because you bought the same "
        "investment within 30 days before or after the sale) on every Form 1099-B you or "
        "your spouse received for 2025?"),
    "wash_lt": (
        "Have you recorded the wash-sale loss adjustment amount of every covered long-term sale "
        "with a wash-sale loss adjustment (a loss disallowed because you bought the same "
        "investment within 30 days before or after the sale) on every Form 1099-B you or "
        "your spouse received for 2025?"),
    "only_box2a": (
        "Is it true that you had no capital gains in 2025 other than capital gain "
        "distributions in box 2a of Form 1099-DIV, and that you did not sell stock, funds "
        "or other property in 2025 (even a sale with no gain or loss)?"),
    "sli": (
        "Is someone else claiming you (or your spouse, on a joint return) as a dependent "
        "on their 2025 return?"),
}

NOSALE = {"form1040.line-7a": 0, "form1040.line-15": 34250, "form1040.line-16": 3875}
ST_200 = {"form1040.line-7a": 200, "form1040.line-15": 34450, "form1040.line-16": 3899}
LT_200 = {"form1040.line-7a": 200, "form1040.line-15": 34450, "form1040.line-16": 3875}

# Hand values per case or late step, from the 2025 instructions as track0.py
# records them (law.json). Never read from a run.
HAND: dict[str, dict[str, Any]] = {
    "alc_wash_st_unanswered": {"schedule-d.line-1b": "blocked"},
    "alc_wash_st_no": {"schedule-d.line-1b": "blocked"},
    "alc_wash_st_yes": {"schedule-d.line-1a": 200, "schedule-d.line-1b": 0, **ST_200},
    "alc_wash_lt_unanswered": {"schedule-d.line-8b": "blocked"},
    "alc_wash_lt_yes": {"schedule-d.line-8a": 200, "schedule-d.line-8b": 0, **LT_200},
    "alc_exc1_unanswered": {"form1040.line-7a": "blocked", "form1040.line-7b": "blocked"},
    "alc_exc1_yes": {"form1040.line-7b": "published_categorical", "schedule-d-required.conclusion": "no", **NOSALE},
    "alc_exc1_sale_unanswered": {"form1040.line-7a": "blocked"},
    "alc_exc1_sale_no": {"schedule-d-required.conclusion": "yes", "form1040.line-7b": "guard_inapplicable", **ST_200},
    "alc_sli_unanswered": {"schedule1.line-21": "blocked"},
    "alc_sli_not_claimed": {"schedule1.line-21": 500, "form1040.line-15": 33750, "form1040.line-16": 3815},
    "alc_sli_claimed": {"schedule1.line-21": 0, "form1040.line-15": 34250, "form1040.line-16": 3875},
    "alc_title_age": {"form1040.line-12e": 17750, "schedule1a.line36a-taxpayer": 6000, "form1040.line-16": 2915},
    "alc_title_blind": {"form1040.line-12e": 17750, "form1040.line-16": 3635},
    "alc_title_spouse_age": {"form1040.line-12e": 33100, "schedule1a.line36b-spouse": 6000, "form1040.line-16": 1093},
    "alc_title_spouse_died_before_65": {
        "form1040.line-12e": 31500, "schedule1a.line36b-spouse": 0, "form1040.line-16": 1853},
    "m_wash_none": {"schedule-d.line-1a": 0, "schedule-d.line-1b": 0, **NOSALE},
    "m_wash_none_unanswered": {"schedule-d.line-1b": "blocked"},
    "m_wash_plain": {"schedule-d.line-1a": 200, "schedule-d.line-1b": 0, **ST_200},
    "m_wash_one": {"schedule-d.line-1a": 0, "schedule-d.line-1b": 0, "form1040.line-7a": 0,
                   "f1099b.covered-w-st-adjustment-subtotal": 200, **NOSALE},
    "m_wash_both": {"schedule-d.line-1a": 200, "schedule-d.line-1b": 0,
                    "f1099b.covered-w-st-adjustment-subtotal": 200, **ST_200},
    "m_exc1_nosale": {"form1040.line-7b": "published_categorical", **NOSALE},
    "m_exc1_zero": {"schedule-d.line-1a": 0, "form1040.line-7b": "guard_inapplicable", **NOSALE},
    "m_exc1_gain": {"schedule-d.line-1a": 200, "form1040.line-7b": "guard_inapplicable", **ST_200},
    "m_sli_single_not": {"schedule1.line-21": 500, "form1040.line-16": 3815},
    "m_sli_single_claimed": {"schedule1.line-21": 0, "form1040.line-16": 3875},
    "m_sli_joint_neither": {"schedule1.line-21": 500, "form1040.line-15": 18000, "form1040.line-16": 1803},
    "m_sli_joint_filer_claimed": {"schedule1.line-21": 0, "form1040.line-15": 18500, "form1040.line-16": 1853},
    "m_sli_joint_spouse_claimed": {"schedule1.line-21": 0, "form1040.line-15": 18500, "form1040.line-16": 1853},
    "late_wash_member/answered_yes": {"schedule-d.line-1a": 200, "schedule-d.line-1b": 0, **ST_200},
    "late_wash_member/wash_sale_added_unclosed": {"schedule-d.line-1b": "blocked", "form1040.line-7a": "blocked"},
    "late_wash_member/reclosed_yes": {"schedule-d.line-1a": 200, "schedule-d.line-1b": 0,
                                      "f1099b.covered-w-st-adjustment-subtotal": 200, **ST_200},
    "late_exc1_sale_after_yes/nosale_yes": {"form1040.line-7b": "published_categorical",
                                            "schedule-d-required.conclusion": "no", **NOSALE},
    "late_exc1_sale_after_yes/sale_added_yes_kept": {"form1040.line-7b": "guard_inapplicable",
                                                     "schedule-d.line-1a": 200, **ST_200},
    "late_exc1_sale_after_yes/only2a_superseded_no": {"form1040.line-7b": "guard_inapplicable",
                                                      "schedule-d-required.conclusion": "yes", **ST_200},
    "late_sli_superseded/not_claimed": {"schedule1.line-21": 500},
    "late_sli_superseded/superseded_claimed": {"schedule1.line-21": 0, "form1040.line-16": 3875},
    "late_sli_superseded/superseded_not_claimed": {"schedule1.line-21": 500, "form1040.line-16": 3815},
}

# Each distinct v87 act list, run once, with the cases and late steps that
# share it, and the changed questions (keys of WORDS) its page shows. A false
# wash-sale closure answer is asked again. With a recorded wash sale and the
# adjustment family open, the page asks nothing (parked, Decision 6).
RUNS: tuple[tuple[str, tuple[str, ...], tuple[str, ...]], ...] = (
    ("wash_st_unanswered", ("alc_wash_st_unanswered",), ("wash_st",)),
    ("wash_st_no", ("alc_wash_st_no",), ("wash_st",)),
    ("st_gain_answered", ("alc_wash_st_yes", "alc_exc1_sale_no", "m_wash_plain", "m_exc1_gain",
                          "late_wash_member/answered_yes"), ()),
    ("wash_lt_unanswered", ("alc_wash_lt_unanswered",), ("wash_lt",)),
    ("lt_gain_answered", ("alc_wash_lt_yes",), ()),
    ("exc1_unanswered", ("alc_exc1_unanswered",), ("only_box2a",)),
    ("complete", ("alc_exc1_yes", "m_wash_none", "m_exc1_nosale"), ()),
    ("exc1_sale_unanswered", ("alc_exc1_sale_unanswered",), ("only_box2a",)),
    ("sli_unanswered", ("alc_sli_unanswered",), ("sli",)),
    ("sli_not_claimed", ("alc_sli_not_claimed", "m_sli_single_not", "late_sli_superseded/not_claimed"), ()),
    ("sli_claimed", ("alc_sli_claimed", "m_sli_single_claimed"), ()),
    ("title_age", ("alc_title_age",), ()),
    ("title_blind", ("alc_title_blind",), ()),
    ("title_spouse_age", ("alc_title_spouse_age",), ()),
    ("title_spouse_died_before_65", ("alc_title_spouse_died_before_65",), ()),
    ("wash_none_unanswered", ("m_wash_none_unanswered",), ("wash_st",)),
    ("wash_one", ("m_wash_one",), ()),
    ("wash_both", ("m_wash_both",), ()),
    ("exc1_zero", ("m_exc1_zero",), ()),
    ("sli_joint_neither", ("m_sli_joint_neither",), ()),
    ("sli_joint_claimed", ("m_sli_joint_filer_claimed", "m_sli_joint_spouse_claimed"), ()),
    ("late_wash_added_unclosed", ("late_wash_member/wash_sale_added_unclosed",), ()),
    ("late_wash_reclosed", ("late_wash_member/reclosed_yes",), ()),
    ("late_exc1_nosale_yes", ("late_exc1_sale_after_yes/nosale_yes",), ()),
    ("late_exc1_sale_added", ("late_exc1_sale_after_yes/sale_added_yes_kept",), ()),
    ("late_exc1_superseded_no", ("late_exc1_sale_after_yes/only2a_superseded_no",), ()),
    ("late_sli_claimed", ("late_sli_superseded/superseded_claimed",), ()),
    ("late_sli_not_claimed", ("late_sli_superseded/superseded_not_claimed",), ()),
)


def _module(name: str, path: Path) -> ModuleType:
    module = sys.modules.get(name)
    if module is None:
        if str(REPO) not in sys.path:
            sys.path.insert(0, str(REPO))
        spec = importlib.util.spec_from_file_location(name, path)
        assert spec is not None and spec.loader is not None
        module = importlib.util.module_from_spec(spec)
        sys.modules[name] = module
        spec.loader.exec_module(module)
    return module


def load_track0() -> ModuleType:
    """This milestone's Track 0 harness, under a name no other test uses. Nothing on it is assigned."""
    if str(REPO) not in sys.path:
        sys.path.insert(0, str(REPO))
    return evidence_loader.load(EVIDENCE / "track0.py", TRACK0_NAME)


def load_recorded() -> ModuleType:
    """The published v83 live module, under a name no other test uses. Nothing on it is assigned."""
    return _module(RECORDED_NAME, REPO / "tests/test_f1099b_backup_withholding_v83.py")


def load_harness() -> ModuleType:
    """The sale-family audit harness, under a name no other test uses. Nothing on it is assigned."""
    if str(REPO) not in sys.path:
        sys.path.insert(0, str(REPO))
    return evidence_loader.load(AUDIT, HARNESS_NAME)


def published(harness: Any) -> Any:
    """Published core v87. The loader entries live in packages/tax/loader.py."""
    core = harness.Core("v87", "v85", "v85")
    assert core.loader_from is None and core.content == CONTENT
    return core


def _v86_words() -> dict[str, str]:
    def read(name: str, field: str) -> str:
        return str(json.loads((CONTENT / name).read_text(encoding="utf-8"))[field])
    return {
        "wash_st": read("closure-mapping.f1099b-covered-w-st-adjustment.v3.json", "closure_question"),
        "wash_lt": read("closure-mapping.f1099b-covered-w-lt-adjustment.v3.json", "closure_question"),
        "only_box2a": read("input-question.exception1-only-box2a-capital-gains.v2.json", "question"),
        "sli": read("input-question.sli-scope-not-claimed-as-dependent.v1.json", "question"),
    }


def _v87_acts(track0: ModuleType) -> dict[str, list[dict[str, Any]]]:
    """Every case's and late step's truthful v87 act list, keyed as HAND is."""
    acts: dict[str, list[dict[str, Any]]] = {}
    for spec in track0.cases():
        acts[spec["id"]] = spec["build87"]()
    for trace in track0.late_traces():
        for step_id, step_acts, _hand in trace["steps"]():
            acts[f"{trace['id']}/{step_id}"] = step_acts
    return acts


def _digest(acts: list[dict[str, Any]]) -> str:
    return hashlib.sha256(json.dumps(acts, sort_keys=True, default=str).encode("utf-8")).hexdigest()


def test_hand_values_are_track0s_instruction_values() -> None:
    track0 = load_track0()
    recorded = {spec["id"]: spec["hand"] for spec in track0.cases()}
    assert len(recorded) == 29
    for trace in track0.late_traces():
        for step_id, _acts, hand in trace["steps"]():
            recorded[f"{trace['id']}/{step_id}"] = hand
    assert recorded == HAND
    asks = {spec["id"]: tuple(spec["asks"]) for spec in track0.cases()}
    for _run, members, shown in RUNS:
        for member in members:
            if member in asks:
                assert set(asks[member]) <= set(shown), member
    assert track0.words(published(track0.harness())) == WORDS


def test_runs_are_the_distinct_v87_act_lists() -> None:
    """Every case and late step is in exactly one run, and no two runs share an act list."""
    acts = _v87_acts(load_track0())
    members = [member for _run, group, _shown in RUNS for member in group]
    assert sorted(members) == sorted(HAND) == sorted(acts)
    digests = []
    for _run, group, _shown in RUNS:
        group_digests = {_digest(acts[member]) for member in group}
        assert len(group_digests) == 1, group
        digests.append(group_digests.pop())
    assert len(set(digests)) == len(RUNS) == 28


@pytest.mark.parametrize("run_id,members,shown", RUNS, ids=[run[0] for run in RUNS])
def test_track0_case_on_published_v87(run_id: str, members: tuple[str, ...], shown: tuple[str, ...]) -> None:
    track0 = load_track0()
    core = published(track0.harness())
    acts = _v87_acts(track0)[members[0]]
    result = track0.execute(core, acts, "demo.qw.t1.v87." + run_id)
    assert result.get("outcome") == "success", (run_id, result.get("error") or result.get("reason"), result.get("message"))
    for member in members:
        assert track0.hand_failures(result, HAND[member]) == [], member
    questions = result.get("questions") or []
    for key, sentence in WORDS.items():
        assert (sentence in questions) is (key in shown), (run_id, key)
    blob = json.dumps(result)
    for key, sentence in _v86_words().items():
        assert sentence != WORDS[key]
        assert sentence not in blob, (run_id, key)


# ---- the 298 recorded v83 runs -------------------------------------------------------


def _recorded() -> dict[str, Any]:
    return cast(dict[str, Any], json.loads(RECORDED_PATH.read_text(encoding="utf-8")))


def _neighbour() -> dict[str, Any]:
    return cast(dict[str, Any], json.loads((BOX4_EVIDENCE / "track0-neighbour.json").read_text(encoding="utf-8")))


RECORDED = _recorded()
NEIGHBOUR = _neighbour()
ASKS = tuple(NEIGHBOUR["asks_no_sale_present_ids"])
IDENTICAL = tuple(NEIGHBOUR["identical_ids"])


def test_recorded_split_is_207_identical_and_91_asks() -> None:
    assert len(IDENTICAL) == 207
    assert len(ASKS) == 91
    assert len(set(IDENTICAL) & set(ASKS)) == 0
    fixture_ids = (
        [f"track0/{key}" for key in RECORDED["track0"]]
        + [f"returns/{key}" for key in RECORDED["returns"]]
        + [f"zero/{key}" for key in RECORDED["zero_sample"]]
    )
    assert len(fixture_ids) == 298
    assert set(fixture_ids) == set(IDENTICAL) | set(ASKS)
    # Every zero-sample run is restored; the parametrized tests below cover all 298.
    assert not [key for key in IDENTICAL if key.startswith("zero/")]


def _neighbour_acts(catalog: dict[str, Any], neighbour_id: str) -> list[dict[str, Any]]:
    test = catalog["test"]
    if neighbour_id.startswith("track0/"):
        return cast(list[dict[str, Any]], catalog["track0"][neighbour_id[len("track0/"):]])
    if neighbour_id.startswith("returns/"):
        return cast(list[dict[str, Any]], catalog["returns"][neighbour_id[len("returns/"):]])
    if neighbour_id.startswith("zero/"):
        key = neighbour_id[len("zero/"):]
        return cast(list[dict[str, Any]], test.with_zero(catalog["harness"], catalog["returns"][key], catalog["v86"]))
    raise AssertionError(neighbour_id)


def _recorded_pin(neighbour_id: str) -> dict[str, Any]:
    if neighbour_id.startswith("track0/"):
        return cast(dict[str, Any], RECORDED["track0"][neighbour_id[len("track0/"):]])
    if neighbour_id.startswith("returns/"):
        return cast(dict[str, Any], RECORDED["returns"][neighbour_id[len("returns/"):]]["v83"])
    if neighbour_id.startswith("zero/"):
        return cast(dict[str, Any], RECORDED["zero_sample"][neighbour_id[len("zero/"):]]["v83"])
    raise AssertionError(neighbour_id)


@pytest.fixture(scope="module")
def recorded_acts(tmp_path_factory: pytest.TempPathFactory) -> dict[str, Any]:
    test = load_recorded()
    harness = test.track0()
    exported = test.export_returns(tmp_path_factory.mktemp("qw-t1-v87"))
    harness_mod = load_harness()
    return {
        "test": test,
        "harness": harness,
        "harness_mod": harness_mod,
        "track0": dict(test.decided_cases(harness)),
        "returns": test.return_acts(harness, exported),
        # The zero-sample act lists are built against v86, as the v86 module and
        # the P0 rerun build them; they run on v87.
        "v86": harness_mod.Core("v86", "v84", "v84"),
        "core": published(harness_mod),
    }


def _assert_recorded(catalog: dict[str, Any], neighbour_id: str, acts: list[dict[str, Any]]) -> None:
    test = catalog["test"]
    got = test.pin(test.track0().run_coordinate(
        catalog["core"], acts, "demo.qw.t1.v87.recorded." + neighbour_id.replace("/", ".")))
    assert got == _recorded_pin(neighbour_id), neighbour_id


def _restored(catalog: dict[str, Any], neighbour_id: str) -> list[dict[str, Any]]:
    return cast(list[dict[str, Any]], catalog["harness_mod"].say(
        copy.deepcopy(_neighbour_acts(catalog, neighbour_id)), PRESENT, "no", "t1.restore"))


@pytest.mark.parametrize("neighbour_id", [key for key in IDENTICAL if key.startswith("track0/")])
def test_recorded_track0_identical(recorded_acts: dict[str, Any], neighbour_id: str) -> None:
    _assert_recorded(recorded_acts, neighbour_id, _neighbour_acts(recorded_acts, neighbour_id))


@pytest.mark.parametrize("neighbour_id", [key for key in IDENTICAL if key.startswith("returns/")])
def test_recorded_return_identical(recorded_acts: dict[str, Any], neighbour_id: str) -> None:
    _assert_recorded(recorded_acts, neighbour_id, _neighbour_acts(recorded_acts, neighbour_id))


@pytest.mark.parametrize("neighbour_id", [key for key in ASKS if key.startswith("track0/")])
def test_recorded_track0_restore_present_no(recorded_acts: dict[str, Any], neighbour_id: str) -> None:
    _assert_recorded(recorded_acts, neighbour_id, _restored(recorded_acts, neighbour_id))


@pytest.mark.parametrize("neighbour_id", [key for key in ASKS if key.startswith("returns/")])
def test_recorded_return_restore_present_no(recorded_acts: dict[str, Any], neighbour_id: str) -> None:
    _assert_recorded(recorded_acts, neighbour_id, _restored(recorded_acts, neighbour_id))


@pytest.mark.parametrize("neighbour_id", [key for key in ASKS if key.startswith("zero/")])
def test_recorded_zero_restore_present_no(recorded_acts: dict[str, Any], neighbour_id: str) -> None:
    _assert_recorded(recorded_acts, neighbour_id, _restored(recorded_acts, neighbour_id))
