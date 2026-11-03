"""Core v71: line 25b waits for each statement's withholding answer (statement-withholding-answer).

Every run goes through ``live_coordinate_run`` on the committed packages: core v70 (registry v68,
release v68) beside core v71 (registry v69, release v69). The hand values are P0's
(``statement-withholding-answer-evidence/p0-trace-and-design.md``, section 7). Returns are the
withholding-closure builders on the v64 base plus the W-2G answers, the base
``tests/helpers/current_core_returns.py`` builds. Synthetic ``demo.*`` data only.
"""

from __future__ import annotations

import copy
import json
import re
import unittest
from decimal import Decimal
from functools import lru_cache, partial
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any, Callable

from packages.derivation.live import live_coordinate_run
from packages.derivation.live_workspace import WorkspaceCapability
from packages.derivation.production_resolver import PublicationSurface
from packages.tax.loader import domain_package_companion_declarations
from tests import test_w2g_gambling as w2g
from tests.helpers import current_core_returns as c
from tests.test_form_1099_k_income import _handover
from tests.test_form_1099_withholding import (
    DIV_B4_FAMILY,
    G_B4_FAMILY,
    INT_B4_FAMILY,
    IRA_B4_FAMILY,
    SSA_B6_FAMILY,
    YEAR,
    _base,
    _dividends,
    _interest,
    _introduce,
    _retirements,
    _social_security,
    _social_security_withholding,
    _transition,
    _unemployment,
    _unemployment_withholding,
)
from tests.test_refund_or_amount_owed_track1 import _finish
from tests.test_withholding_closure import _horizons, _set_closure

ROOT = Path(__file__).resolve().parents[1]
CONTENT = c.CONTENT
RELEASE_DIR = c.RELEASE_DIR
P = c.P
CORE = "tax.us.2025.package.core-calculations"
CORES = {
    "v70": ("package.core-calculations.v70.json", "v70", "demo.release.sli-worksheet-integration.2025.v68.json", "v68", "published-packages.v68.json"),
    "v71": ("package.core-calculations.v71.json", "v71", "demo.release.sli-worksheet-integration.2025.v69.json", "v69", "published-packages.v69.json"),
}

L24, L25A, L25B = P + "tax.line24-total-tax", P + "payments.line25a", P + "payments.line25b"
L25D, L33, L35A, L37 = P + "payments.line25d", P + "payments.line33", P + "payments.line35a-refunded", P + "payments.line37-amount-owed"
LINES = (L24, L25A, L25B, L25D, L33, L35A, L37)
BEHIND = (L25D, L33, L35A, L37)

# family -> (box 4 / box 6 family, its fact, amounts of the two statements, hand line 24 with one statement)
FACTS = {
    "int": P + "f1099int.box4-withholding",
    "div": P + "f1099div.box4-withholding",
    "ira": P + "f1099r.ira-box4-withholding",
    "g": P + "f1099g.box4-withholding",
    "ssa": P + "ssa1099.box6-voluntary-withholding",
}
SECOND = {  # the second statement's family and identity keys, as the builders record it
    "int": (INT_B4_FAMILY, (("payer", "demo.fw.int.payer.1"), ("statement", "demo.fw.int.stmt.1"))),
    "div": (DIV_B4_FAMILY, (("payer", "demo.fw.div.payer.1"), ("statement", "demo.fw.div.stmt.1"))),
    "ira": (IRA_B4_FAMILY, (("payer", "demo.fw.r.payer.1"), ("statement", "demo.fw.r.stmt.1"))),
    "g": (G_B4_FAMILY, (("payer", "demo.fw.g.payer.1"), ("statement", "demo.fw.g.stmt.1"))),
    "ssa": (SSA_B6_FAMILY, (("statement", "demo.fw.ssa.stmt.1"),)),
}
FIRST_AMOUNT = {"int": 50.0, "div": 40.0, "ira": 1200.0, "g": 600.0, "ssa": 800.0}
# P0 section 7, hand: line 24, refund (+) or amount owed (-) with one statement and no answer / $0.
HAND_ONE = {"int": ("3935", "565"), "div": ("3935", "565"), "ira": ("5075", "-575"), "g": ("4595", "-95"), "ssa": ("5099", "-599")}


class Run:
    def __init__(self, pubs: dict[str, dict[str, Any]], dispositions: list[dict[str, Any]], model: dict[str, Any]) -> None:
        self.pubs, self.dispositions, self.model = pubs, dispositions, model

    def value(self, symbol: str) -> Decimal | None:
        return Decimal(str(self.pubs[symbol]["value"])) if symbol in self.pubs else None

    def lines(self) -> dict[str, Decimal | None]:
        return {s: self.value(s) for s in LINES}

    def net(self) -> Decimal:
        """Refund minus amount owed."""
        return (self.value(L35A) or Decimal(0)) - (self.value(L37) or Decimal(0))

    def row(self, token: str) -> dict[str, Any]:
        return next(r for r in self.dispositions if str(r.get("artifact_id", "")).endswith("rule." + token))

    def roots(self) -> list[tuple[str, str, tuple[str, ...]]]:
        return sorted(
            (str(r["artifact_id"]).replace(P + "rule.", ""), str(r["code"]), tuple(str(m).replace(P, "") for m in r.get("missing", [])))
            for r in self.dispositions if r.get("disposition") == "blocked" and r.get("code") != "DEPENDENCY_ABSENT")


def run(acts: list[dict[str, object]], name: str, core: str) -> Run:
    package, version, release, rel_version, registry = CORES[core]
    surface = PublicationSurface(RELEASE_DIR, CONTENT / registry, CONTENT)
    finished = _handover(
        _finish(copy.deepcopy(acts), package_path=CONTENT / package, package_version=version,
                release_path=RELEASE_DIR / release, release_version=rel_version, note=name),
        surface=surface, reconfirm=True)
    with TemporaryDirectory() as tmp:
        outcome = live_coordinate_run(
            WorkspaceCapability(Path(tmp) / "L"), repo_root=ROOT, authoritative_acts=finished,
            workspace_revision=len(finished), run_scope={"jurisdiction": "us", "year": YEAR},
            scope_user=c.USER, request={"schema": "run-request.v1"}, run_id=name, governance_pins=[],
            surface=surface, output_name="out.json")
        assert outcome.refusal is None, f"{name} refused: {outcome.refusal}"
        assert outcome.output_path is not None and outcome.presentation_path is not None
        pubs = {str(p.finding["symbol"]): p.finding for p in outcome.publications or ()}
        report = json.loads(outcome.output_path.read_text(encoding="utf-8"))
        model = json.loads(outcome.presentation_path.read_text(encoding="utf-8"))
    return Run(pubs, list(report.get("dispositions", [])), model)


# --- returns ---------------------------------------------------------------------------------


def family_return(key: str, n: int, amounts: list[float | None], *, joint: bool = False) -> list[dict[str, object]]:
    """``n`` statements of one family (each with its income box), box 4 / box 6 amounts as given (None
    records no amount), the family's closure attested at its horizon, every other withholding family
    closed empty."""
    acts = _base(wages=80000.0 if joint else 50000.0, w2_withheld=7000.0 if joint else 4500.0, joint=joint)
    if key == "g":
        _unemployment(acts, [6000.0, 4000.0][:n], authority=None)
        _unemployment_withholding(acts, amounts, close=False)
        _social_security_withholding(acts, [])
    elif key == "ssa":
        _social_security(acts, [12000.0, 8000.0][:n], witness=None)
        _unemployment_withholding(acts, [])
        _social_security_withholding(acts, amounts, close=False)
    else:
        income = [10000.0, 5000.0][:n] if key == "ira" else [500.0, 300.0][:n]
        {"int": _interest, "div": _dividends, "ira": _retirements}[key](acts, list(zip(income, amounts)))
        _unemployment_withholding(acts, [])
        _social_security_withholding(acts, [])
    acts = _set_closure(acts, key, "head")
    w2g._w2g(acts, [])
    return acts


def answer_second(acts: list[dict[str, object]], key: str, amount: float, *, reclose: bool) -> list[dict[str, object]]:
    """The second statement's answer recorded afterwards, as a filer adopting v71 records it. It is a
    member-transition, so the family's closure is behind its horizon until it is attested again."""
    family, keys = SECOND[key]
    out = copy.deepcopy(acts)
    head = _horizons(out, family)[-1]
    _transition(out, (family, "v1"), head, "demo.swa.adopt.h", "demo.swa.adopt.box4", FACTS[key], keys, amount)
    return _set_closure(out, key, "head") if reclose else out


def surplus_answer_return() -> list[dict[str, object]]:
    """Two 1099-INT statements, both answered, plus a third box 4 answer on a statement with no box 1."""
    acts = family_return("int", 2, [50.0, 30.0])
    keys = (("payer", "demo.swa.x.payer"), ("statement", "demo.swa.x.stmt"))
    _introduce(acts, "demo.swa.x.payer", "tax.us.interest-payer")
    _introduce(acts, "demo.swa.x.stmt", "tax.us.1099int-statement")
    _transition(acts, (INT_B4_FAMILY, "v1"), _horizons(acts, INT_B4_FAMILY)[-1], "demo.swa.x.h", "demo.swa.x.box4",
                FACTS["int"], keys, 7.0)
    return _set_closure(acts, "int", "head")


def _adopted(key: str, reclose: bool) -> list[dict[str, object]]:
    return answer_second(family_return(key, 2, [FIRST_AMOUNT[key], None]), key, 0.0, reclose=reclose)


@lru_cache(maxsize=None)
def cached(case: str, core: str) -> Run:
    return run(BUILDERS[case](), f"demo.swa.{case}.{core}", core)


BUILDERS: dict[str, Callable[[], list[dict[str, object]]]] = {
    **{f"{k}.one-unanswered": partial(family_return, k, 1, [None]) for k in FACTS},
    **{f"{k}.one-zero": partial(family_return, k, 1, [0.0]) for k in FACTS},
    **{f"{k}.two-second-unanswered": partial(family_return, k, 2, [FIRST_AMOUNT[k], None]) for k in FACTS},
    **{f"{k}.two-second-zero": partial(family_return, k, 2, [FIRST_AMOUNT[k], 0.0]) for k in FACTS},
    **{f"{k}.adopt-no-reclose": partial(_adopted, k, False) for k in FACTS},
    **{f"{k}.adopt-reclosed": partial(_adopted, k, True) for k in FACTS},
    "g.two-second-400": lambda: family_return("g", 2, [600.0, 400.0]),
    "int.joint-second-unanswered": lambda: family_return("int", 2, [50.0, None], joint=True),
    "int.joint-second-zero": lambda: family_return("int", 2, [50.0, 0.0], joint=True),
    "int.joint-second-30": lambda: family_return("int", 2, [50.0, 30.0], joint=True),
    "none": lambda: _no_withholding(),
    "surplus": surplus_answer_return,
}


def _no_withholding() -> list[dict[str, object]]:
    acts = _base(wages=50000.0, w2_withheld=4500.0)
    _unemployment_withholding(acts, [])
    _social_security_withholding(acts, [])
    w2g._w2g(acts, [])
    return acts


def assert_blocks_at_25b(test: unittest.TestCase, result: Run, key: str) -> None:
    row = result.row("form1040-line25b")
    test.assertEqual((row["disposition"], row["code"]), ("blocked", "DEPENDENCY_ABSENT"))
    test.assertEqual(list(row["missing"]), [FACTS[key]])
    test.assertNotIn(L25B, result.pubs)
    for symbol in BEHIND:
        test.assertNotIn(symbol, result.pubs, symbol)
    for symbol in (L24, L25A):
        test.assertIn(symbol, result.pubs, symbol)


class StatementWithoutItsAnswerBlocks(unittest.TestCase):
    def test_each_family_blocks_on_v71_and_computes_as_zero_on_v70(self) -> None:
        for key in FACTS:
            with self.subTest(family=key):
                old, new = cached(f"{key}.one-unanswered", "v70"), cached(f"{key}.one-unanswered", "v71")
                # v70, pinned: the missing answer computes as $0 and nothing blocks.
                self.assertEqual(old.value(L25B), 0)
                self.assertEqual(old.value(L24), Decimal(HAND_ONE[key][0]))
                self.assertEqual(old.net(), Decimal(HAND_ONE[key][1]))
                self.assertEqual(old.roots(), [])
                assert_blocks_at_25b(self, new, key)
                self.assertEqual(new.value(L24), old.value(L24))
                self.assertEqual(new.value(L25A), old.value(L25A))

    def test_a_zero_answer_publishes_exactly_what_v70_does(self) -> None:
        for key in FACTS:
            with self.subTest(family=key):
                old, new = cached(f"{key}.one-zero", "v70"), cached(f"{key}.one-zero", "v71")
                self.assertEqual(new.lines(), old.lines())
                self.assertEqual(set(new.pubs), set(old.pubs))
                self.assertEqual(new.value(L25B), 0)
                self.assertEqual(new.net(), Decimal(HAND_ONE[key][1]))
                self.assertEqual(new.roots(), [])
                # the unanswered v70 return computes the same numbers as the $0 one: that is the gap.
                self.assertEqual(cached(f"{key}.one-unanswered", "v70").lines(), old.lines())

    def test_two_statements_one_unanswered(self) -> None:
        for key in FACTS:
            with self.subTest(family=key):
                old, new = cached(f"{key}.two-second-unanswered", "v70"), cached(f"{key}.two-second-unanswered", "v71")
                self.assertEqual(old.value(L25B), Decimal(str(FIRST_AMOUNT[key])))
                assert_blocks_at_25b(self, new, key)
                zero_old, zero_new = cached(f"{key}.two-second-zero", "v70"), cached(f"{key}.two-second-zero", "v71")
                self.assertEqual(zero_new.lines(), zero_old.lines())
                self.assertEqual(zero_old.lines(), old.lines())

    def test_two_forms_1099_g_hand_values(self) -> None:
        # Box 1 6,000 and 4,000 (line 24 5,075); box 4 600 recorded, 400 unrecorded.
        old, new = cached("g.two-second-unanswered", "v70"), cached("g.two-second-unanswered", "v71")
        self.assertEqual((old.value(L24), old.value(L25B), old.value(L33), old.net()),
                         (Decimal(5075), Decimal(600), Decimal(5100), Decimal(25)))
        assert_blocks_at_25b(self, new, "g")
        self.assertEqual(new.value(L24), Decimal(5075))
        answered = cached("g.two-second-400", "v71")
        self.assertEqual((answered.value(L25B), answered.value(L33), answered.net()), (Decimal(1000), Decimal(5500), Decimal(425)))
        self.assertEqual(answered.lines(), cached("g.two-second-400", "v70").lines())

    def test_joint_return_with_one_statement_unanswered(self) -> None:
        # Wages 80,000, W-2 7,000, 1099-INT box 1 500 and 300: line 24 5,442.
        old, new = cached("int.joint-second-unanswered", "v70"), cached("int.joint-second-unanswered", "v71")
        self.assertEqual((old.value(L24), old.value(L25B), old.value(L33), old.net()),
                         (Decimal(5442), Decimal(50), Decimal(7050), Decimal(1608)))
        assert_blocks_at_25b(self, new, "int")
        zero = cached("int.joint-second-zero", "v71")
        self.assertEqual(zero.lines(), old.lines())
        full = cached("int.joint-second-30", "v71")
        self.assertEqual((full.value(L25B), full.net()), (Decimal(80), Decimal(1638)))
        self.assertEqual(full.lines(), cached("int.joint-second-30", "v70").lines())

    def test_no_form_1099_is_unchanged(self) -> None:
        old, new = cached("none", "v70"), cached("none", "v71")
        self.assertEqual(new.lines(), old.lines())
        self.assertEqual((new.value(L25B), new.value(L33), new.net()), (Decimal(0), Decimal(4500), Decimal(625)))
        self.assertEqual(new.roots(), [])

    def test_a_surplus_answer_without_a_statement_is_as_on_v70(self) -> None:
        # gte: three answers (50, 30, 7) beside two statements. Line 25b 87.
        old, new = cached("surplus", "v70"), cached("surplus", "v71")
        self.assertEqual(old.value(L25B), Decimal(87))
        self.assertEqual(new.lines(), old.lines())
        self.assertEqual(new.roots(), [])

    def test_the_first_short_family_is_named(self) -> None:
        acts = family_return("int", 2, [50.0, None])  # int short; the rest closed empty
        result = run(acts, "demo.swa.order.v71", "v71")
        self.assertEqual(list(result.row("form1040-line25b")["missing"]), [FACTS["int"]])


class AdoptedV70Return(unittest.TestCase):
    def test_asked_the_amount_then_the_closure_then_v70_numbers(self) -> None:
        for key in FACTS:
            with self.subTest(family=key):
                before = cached(f"{key}.two-second-unanswered", "v71")
                assert_blocks_at_25b(self, before, key)
                # The answer ($0) is recorded; the family's closure is now behind its horizon.
                stale = cached(f"{key}.adopt-no-reclose", "v71")
                row = stale.row("form1040-line25b")
                self.assertEqual((row["code"], list(row["missing"])), ("SOURCE_SET_UNCLOSED", [_set_of(key)]))
                self.assertNotIn(L25B, stale.pubs)
                # The closure answered again: v70's numbers, nothing else moved.
                done = cached(f"{key}.adopt-reclosed", "v71")
                self.assertEqual(done.lines(), cached(f"{key}.adopt-reclosed", "v70").lines())
                self.assertEqual(done.lines(), cached(f"{key}.two-second-unanswered", "v70").lines())
                self.assertEqual(done.roots(), [])


def _set_of(key: str) -> str:
    return P + {"int": "f1099int.b4", "div": "f1099div.b4", "ira": "f1099r.box4", "g": "f1099g.b4", "ssa": "ssa1099.b6"}[key]


def _load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


class SuccessorShape(unittest.TestCase):
    def test_registry_only_adds_and_release_matches(self) -> None:
        old, new = _load(CONTENT / "published-packages.v68.json"), _load(CONTENT / "published-packages.v69.json")
        for field in ("citizens", "packages"):
            before = {(e["id"], e["version"]): e["checksum"] for e in old[field]}
            after = {(e["id"], e["version"]): e["checksum"] for e in new[field]}
            self.assertTrue(before.items() <= after.items(), field)
        self.assertEqual({(e["id"], e["version"]) for e in new["citizens"]} - {(e["id"], e["version"]) for e in old["citizens"]},
                         {(P + "rule.form1040-line25b", "v4")})
        self.assertEqual({(e["id"], e["version"]) for e in new["packages"]} - {(e["id"], e["version"]) for e in old["packages"]},
                         {(CORE, "v71")})
        import hashlib
        release = _load(RELEASE_DIR / CORES["v71"][2])
        self.assertEqual(release["version"], "v69")
        self.assertEqual(release["package_registry_sha256"], hashlib.sha256((CONTENT / CORES["v71"][4]).read_bytes()).hexdigest())

    def test_v71_replaces_only_line_25b(self) -> None:
        old, new = _load(CONTENT / CORES["v70"][0]), _load(CONTENT / CORES["v71"][0])
        changed = [(a, b) for a, b in zip(old["members"], new["members"]) if a != b]
        self.assertEqual(len(old["members"]), len(new["members"]))
        self.assertEqual([(b["id"], a["version"], b["version"], b["schema"]) for a, b in changed],
                         [(P + "rule.form1040-line25b", "v3", "v4", "rule-artifact.v4")])

    def test_rule_keeps_v3_guards_and_adds_one_count_check_per_family(self) -> None:
        v3, v4 = _load(CONTENT / "rule.form1040-line25b.v3.json"), _load(CONTENT / "rule.form1040-line25b.v4.json")
        for key in ("value", "pins", "requires", "blocked", "publishes", "id", "role", "scope"):
            self.assertEqual(v4[key], v3[key], key)
        args = v4["when"]["args"]
        self.assertEqual(args[:5], v3["when"]["args"])
        checks = args[5:]
        self.assertEqual([a["args"][1]["name"] for a in checks], [FACTS[k] for k in ("int", "div", "ira", "g", "ssa")])
        for a in checks:
            self.assertEqual(a["op"], "any")
            self.assertEqual(a["args"][0]["cmp"], "gte")
            self.assertEqual(a["args"][0]["left"]["op"], "count")
            self.assertEqual(a["args"][0]["right"]["op"], "count")

    def test_v71_companion_declaration_is_v70s(self) -> None:
        declarations = domain_package_companion_declarations()
        self.assertEqual(declarations[(CORE, "v71")], declarations[(CORE, "v70")])
        self.assertTrue(re.search(r"v7[01]", str(sorted(k[1] for k in declarations if k[0] == CORE))))


class ExplanationOfTheBlock(unittest.TestCase):
    """What the existing explanation and presentation carry for the v71 block (nothing changed to say it)."""

    def test_the_disposition_node_names_the_fact_and_the_section_says_only_that_an_input_is_missing(self) -> None:
        model = cached("g.two-second-unanswered", "v71").model
        record = model["dispositionNodes"][L25B]["records"][0]
        self.assertEqual((record["disposition"], record["code"], record["missing"]), ("blocked", "DEPENDENCY_ABSENT", [FACTS["g"]]))
        self.assertIn(record["pins"][0]["version"], {"v71"})
        section = next(s for s in model["sections"] if s["id"] == "line-25b")
        self.assertEqual(section["resolved"]["disposition"], "blocked")
        self.assertEqual(section["field"]["dispositions"]["blocked"]["explain"],
                         "Form 1040 line 25b is blocked because an input it needs is missing or not yet closed.")


if __name__ == "__main__":
    unittest.main()
