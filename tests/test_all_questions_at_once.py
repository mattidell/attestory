"""Core v76 shows the knowable questions in round one.

The loops go through ``live_coordinate_run``, reusing the P0 probe. v75 is
the before table. v76 is the prototype's full patch. A closure-check symbol
may publish ``true``; it is not a form amount and is not part of the face.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path
from typing import Any

import pytest

from packages.derivation.evaluator import AccessLog, Environment, EvalBlocked, evaluate
from packages.derivation.live import live_coordinate_run
from packages.derivation.presentation_projection import _closure_question_reasons
from packages.tax.loader import later_any_arm_refs_while_count_blocked

ROOT = Path(__file__).resolve().parents[1]
CORE = "tax.us.2025.package.core-calculations"
_PROBE_PATH = (
    ROOT / "docs/phases/engine-breadth/milestones/all-questions-at-once-evidence/probe.py"
)

_CORES: dict[str, tuple[str, str, str, str, str]] = {
    "v75": (
        "package.core-calculations.v75.json",
        "v75",
        "published-packages.v73.json",
        "demo.release.sli-worksheet-integration.2025.v73.json",
        "v73",
    ),
    "v76": (
        "package.core-calculations.v76.json",
        "v76",
        "published-packages.v74.json",
        "demo.release.sli-worksheet-integration.2025.v74.json",
        "v74",
    ),
}

# Question rounds. v75 is P0 section 1. v76 is the full-patch prototype.
_ROUNDS = {
    "v75": {
        "scope-withheld": 2,
        "amounts-open": 4,
        "mortgage-empty": 4,
        "form-1099b-empty": 4,
        "dependent-empty": 6,
        "foreign-tax-empty": 6,
    },
    "v76": {
        "scope-withheld": 2,
        "amounts-open": 2,
        "mortgage-empty": 2,
        "form-1099b-empty": 3,
        "dependent-empty": 5,
        # The prototype left the box 7 closure in its own later round, because
        # the in-process patch never gave that closure a line. The successor
        # names it on the credit rule, so it is asked in round 1 and the
        # worksheet rounds move up by one.
        "foreign-tax-empty": 5,
    },
}
_STOPS = {
    "scope-withheld": "no-filer-question",
    "amounts-open": "no-filer-question",
    "mortgage-empty": "no-filer-question",
    "form-1099b-empty": "no-filer-question",
    "dependent-empty": "no-filer-question",
    "foreign-tax-empty": "nothing-new",
}
_V75_ROUND_ONE = {
    "scope-withheld": 25,
    "amounts-open": 35,
    "mortgage-empty": 61,
    "form-1099b-empty": 60,
    "dependent-empty": 60,
    "foreign-tax-empty": 59,
}

BOX2 = (
    "Enter the federal income tax withheld in box 2 of each Form W-2 you or "
    "your spouse received for 2025. If box 2 is blank, enter $0."
)
BOX4 = (
    "Enter the federal income tax withheld in box 4 of each Form 1099-DIV you "
    "or your spouse received for 2025. If box 4 is blank, enter $0."
)
WAGE = (
    "Have you recorded every wage amount in box 1 of every Form W-2 you or "
    "your spouse received for 2025?"
)
BOX7 = (
    "Have you recorded every foreign tax paid amount in box 7 of every Form "
    "1099-DIV you or your spouse received for 2025?"
)
PARENTS = (
    "Have you recorded every covered short-term sale (a sale of an investment "
    "you held a year or less, with your cost basis reported to the IRS) on "
    "every Form 1099-B you or your spouse received for 2025?",
    "Have you recorded every covered long-term sale (a sale of an investment "
    "you held more than a year, with your cost basis reported to the IRS) on "
    "every Form 1099-B you or your spouse received for 2025?",
)
WASH = (
    "Have you recorded the cost basis of every covered short-term sale with a "
    "wash-sale loss adjustment (a loss disallowed because you bought the same "
    "investment within 30 days before or after the sale) on every Form 1099-B "
    "you or your spouse received for 2025?",
    "Have you recorded the sale proceeds of every covered short-term sale with "
    "a wash-sale loss adjustment (a loss disallowed because you bought the same "
    "investment within 30 days before or after the sale) on every Form 1099-B "
    "you or your spouse received for 2025?",
    "Have you recorded the wash-sale loss adjustment amount (a loss disallowed "
    "because you bought the same investment within 30 days before or after the "
    "sale) of every covered short-term sale on every Form 1099-B you or your "
    "spouse received for 2025?",
    "Have you recorded the cost basis of every covered long-term sale with a "
    "wash-sale loss adjustment (a loss disallowed because you bought the same "
    "investment within 30 days before or after the sale) on every Form 1099-B "
    "you or your spouse received for 2025?",
    "Have you recorded the sale proceeds of every covered long-term sale with a "
    "wash-sale loss adjustment (a loss disallowed because you bought the same "
    "investment within 30 days before or after the sale) on every Form 1099-B "
    "you or your spouse received for 2025?",
    "Have you recorded the wash-sale loss adjustment amount (a loss disallowed "
    "because you bought the same investment within 30 days before or after the "
    "sale) of every covered long-term sale on every Form 1099-B you or your "
    "spouse received for 2025?",
)
KNOWABLE_ROUND_ONE = (WAGE, BOX2, *PARENTS, *WASH)
OPEN_STARTS = (
    "amounts-open",
    "mortgage-empty",
    "form-1099b-empty",
    "dependent-empty",
    "foreign-tax-empty",
)
CONDITIONAL = (
    "Did you receive a Form 1098 mortgage interest statement for 2025?",
    "Enter how much of your 2025 overpayment you want applied to your 2026 estimated tax. If none, enter $0.",
    "Does your Social Security number allow you to work in the United States? Answer yes if it was issued by the Social Security Administration on or before the due date of your 2025 return (including extensions) and is not marked \"Not Valid for Employment\", or if it is marked \"Valid for Work Only With DHS Authorization\" and that authorization is still valid.",
    "Could you be a qualifying child of another person for 2025 (do not count the case where that person is not required to file a 2025 return and is not filing one, or is filing only to claim a refund of withheld or estimated tax)?",
    "Were you, or was your spouse, a nonresident alien for any part of 2025 (do not count a nonresident or dual-status alien spouse you chose to treat as a U.S. resident for the whole year)?",
    "Have you recorded every Social Security tax withheld amount in box 4 of every Form W-2 you or your spouse received for 2025?",
    "Have you recorded every Medicare tax withheld amount in box 6 of every Form W-2 you or your spouse received for 2025?",
    "Is your total foreign tax from all sources more than $300 ($600 if you file jointly), or is there any other reason you must file Form 1116?",
    "Do you want to claim the foreign tax you paid as a credit without filing Form 1116?",
)
_W2_FACTS = {"tax.us.2025.w2.box1-wages", "tax.us.2025.w2.box2-withholding"}
# The wage closure fact is attested on the horizon the wage member opens.
# A return with no W-2 keeps the empty family and drops that attestation.
_W2_CLOSURE = "tax.us.2025.w2.source-closure"


def _load_probe() -> Any:
    spec = importlib.util.spec_from_file_location("all_questions_probe", _PROBE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("question-round probe failed to load")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _round_sentences(result: dict[str, Any], number: int) -> list[str]:
    for item in result["rounds"]:
        if item["round"] == number:
            return list(item["sentences"])
    return []


def _first_round(result: dict[str, Any], sentence: str) -> int | None:
    for item in result["rounds"]:
        if sentence in item["sentences"]:
            return int(item["round"])
    return None


def _face(lines: list[dict[str, Any]]) -> list[tuple[str, tuple[str, ...]]]:
    return sorted(
        (row["line"], tuple(sorted(row["sentences"])))
        for row in lines
    )


def _scalars(values: dict[str, Any]) -> dict[str, Any]:
    return {
        symbol: value
        for symbol, value in values.items()
        if not str(symbol).endswith(".closure-check")
    }


def test_switch_is_on_from_core_v76() -> None:
    assert live_coordinate_run.__module__ == "packages.derivation.live"
    assert later_any_arm_refs_while_count_blocked(CORE, "v76") is True
    assert later_any_arm_refs_while_count_blocked(CORE, "v75") is False
    assert later_any_arm_refs_while_count_blocked(CORE, "v74") is False
    assert later_any_arm_refs_while_count_blocked("tax.us.2025.package.interest-slice", "v76") is False


def test_later_ref_is_recorded_only_when_a_compared_set_has_a_member() -> None:
    when = {
        "op": "any",
        "args": [
            {
                "op": "compare",
                "cmp": "eq",
                "left": {
                    "op": "count",
                    "name": "tax.us.2025.w2.box2-withholding",
                    "source_set": "tax.us.2025.w2-box2",
                },
                "right": {
                    "op": "count",
                    "name": "tax.us.2025.w2.box1-wages",
                    "source_set": "tax.us.2025.w2",
                },
            },
            {"op": "ref", "name": "tax.us.2025.w2.box2-withholding"},
        ],
    }

    def run(sources: dict[str, list[str]], flag: bool) -> EvalBlocked:
        environment = Environment(
            symbols={},
            sources=sources,
            closed_sets=frozenset(),
            parameters={},
            canon={},
            record_later_any_refs=flag,
        )
        with pytest.raises(EvalBlocked) as caught:
            evaluate(when, environment, AccessLog())
        return caught.value

    wages = {"tax.us.2025.w2.box1-wages": ["50000"]}
    off = run(wages, False)
    assert off.missing == ["tax.us.2025.w2-box2"]
    assert off.later_refs == []
    on = run(wages, True)
    assert on.missing == ["tax.us.2025.w2-box2", "tax.us.2025.w2.box2-withholding"]
    assert on.later_refs == ["tax.us.2025.w2.box2-withholding"]
    empty = run({}, True)
    assert empty.missing == ["tax.us.2025.w2-box2"]
    assert empty.later_refs == []


def test_mixed_closure_row_names_the_family_and_the_later_ref() -> None:
    family = "tax.us.2025.w2-box4"
    amount = "tax.us.2025.w2.box4-social-security"
    closure = "Have you recorded every Social Security tax withheld amount in box 4 of every Form W-2 you or your spouse received for 2025?"
    asked = "Enter the Social Security tax withheld."
    members = [
        {
            "schema": "source-closure-mapping.v3",
            "closure_question": closure,
            "family": {"id": family},
        },
        {
            "schema": "input-question.v1",
            "question": asked,
            "fact_type": {"id": amount},
        },
    ]
    row = {"code": "SOURCE_SET_UNCLOSED", "missing": [family, amount]}
    hidden = _closure_question_reasons(row, resolved_members=members, by_symbol={})
    assert hidden == []
    shown = _closure_question_reasons(
        row, resolved_members=members, by_symbol={}, later_any_arm_refs=True
    )
    assert [item["sentence"] for item in shown] == sorted([closure, asked])
    family_only = [
        member for member in members if str(member.get("schema", "")).startswith("source-closure-mapping.")
    ]
    closure_row = {"code": "SOURCE_SET_UNCLOSED", "missing": [family, amount]}
    named = _closure_question_reasons(
        closure_row, resolved_members=family_only, by_symbol={}, later_any_arm_refs=True
    )
    assert [item["sentence"] for item in named] == [closure]
    absent = {"code": "DEPENDENCY_ABSENT", "missing": [amount]}
    assert _closure_question_reasons(
        absent, resolved_members=family_only, by_symbol={}, later_any_arm_refs=True
    ) == []


def _loops(probe: Any) -> dict[str, dict[str, dict[str, Any]]]:
    personas = probe.build_personas()
    found: dict[str, dict[str, dict[str, Any]]] = {}
    for version, core in _CORES.items():
        probe.CORE = core
        catalog = probe.load_catalog()
        found[version] = {}
        for name, mode, persona_name, _description in probe.SCENARIOS:
            found[version][name] = probe.loop_scenario(
                name, mode, personas[persona_name], catalog
            )
    return found


def _completes(probe: Any) -> dict[str, dict[str, dict[str, Any]]]:
    personas = probe.build_personas()
    found: dict[str, dict[str, dict[str, Any]]] = {}
    for version, core in _CORES.items():
        probe.CORE = core
        found[version] = {}
        for persona_name, persona in personas.items():
            acts = probe.materialize(persona, set(range(len(persona))))
            found[version][persona_name] = probe.run_acts(
                acts, f"demo.aq.{version}.{persona_name}.complete"
            )
    return found


def test_question_rounds_match_the_prototype() -> None:
    probe = _load_probe()
    loops = _loops(probe)

    for name, expected in _ROUNDS["v75"].items():
        result = loops["v75"][name]
        assert result["rounds_with_questions"] == expected, name
        assert result["stop"] == _STOPS[name], name
        assert len(_round_sentences(result, 1)) == _V75_ROUND_ONE[name], name
    opened = _round_sentences(loops["v75"]["amounts-open"], 1)
    assert WAGE not in opened
    assert BOX2 not in opened

    for name, expected in _ROUNDS["v76"].items():
        result = loops["v76"][name]
        assert result["rounds_with_questions"] == expected, (name, result["stop"])
        assert result["stop"] == _STOPS[name], name

    for name in OPEN_STARTS:
        shown = set(_round_sentences(loops["v76"][name], 1))
        missing = [sentence for sentence in KNOWABLE_ROUND_ONE if sentence not in shown]
        assert missing == [], (name, missing)
    scope = set(_round_sentences(loops["v76"]["scope-withheld"], 1))
    assert BOX2 not in scope
    assert WAGE not in scope

    for name in _ROUNDS["v76"]:
        assert BOX4 not in _round_sentences(loops["v76"][name], 1), name
        shown = set(_round_sentences(loops["v76"][name], 1))
        present = [sentence for sentence in CONDITIONAL if sentence in shown]
        assert present == [], (name, present)
    # Only the foreign-tax persona records a Form 1099-DIV, so only it is
    # ever asked the box 4 amount, and from round 2 until the loop stops.
    for name in _ROUNDS["v76"]:
        if name == "foreign-tax-empty":
            continue
        for item in loops["v76"][name]["rounds"]:
            assert BOX4 not in item["sentences"], (name, item["round"])
    foreign = loops["v76"]["foreign-tax-empty"]
    assert _first_round(foreign, BOX4) == 2
    for item in foreign["rounds"]:
        assert (BOX4 in item["sentences"]) == (item["round"] >= 2), item["round"]
    assert _first_round(foreign, BOX7) == 1
    assert _first_round(foreign, CONDITIONAL[8]) == 3
    assert _first_round(foreign, CONDITIONAL[7]) == 4
    dependent = loops["v76"]["dependent-empty"]
    assert _first_round(dependent, CONDITIONAL[2]) == 2
    assert _first_round(dependent, CONDITIONAL[3]) == 2
    assert _first_round(dependent, CONDITIONAL[4]) == 2
    assert _first_round(dependent, CONDITIONAL[5]) == 3
    assert _first_round(dependent, CONDITIONAL[6]) == 4
    assert _first_round(dependent, CONDITIONAL[1]) == 5

    probe.CORE = _CORES["v76"]
    catalog = probe.load_catalog()
    persona = []
    for act in probe.build_personas()["base"]:
        fact_types = {probe.fact_type_of(finding) for finding in probe.findings_of(act)}
        if fact_types & _W2_FACTS or _W2_CLOSURE in fact_types:
            continue
        persona.append(act)
    no_w2 = probe.loop_scenario("no-w2", "amounts", persona, catalog)
    for item in no_w2["rounds"]:
        assert BOX2 not in item["sentences"], item["round"]

    completes = _completes(probe)
    for persona_name in completes["v75"]:
        before = completes["v75"][persona_name]
        after = completes["v76"][persona_name]
        assert _scalars(before["values"]) == _scalars(after["values"]), persona_name
        assert probe.headline(before["values"]) == probe.headline(after["values"]), persona_name
        assert _face(before["lines"]) == _face(after["lines"]), persona_name
