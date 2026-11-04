"""Core v73: a blocked line names the question for a missing scope answer or filing status (scope-answer-questions).

``input-question.v1`` citizens (one per fact, carrying its group's sentence) and the package's input-binding map
let the presentation projection copy the sentence verbatim as the reason on a line whose every cause has one.
Every case runs through ``live_coordinate_run`` on the committed packages and reads the saved presentation model.
Hand expectations are the P0 table (``scope-answer-questions-evidence/p0-questions.md``): each question asks
whether the thing is PRESENT; ``abs`` facts assert an absence, so the question's "yes" records the fact's ``no``.
Synthetic ``demo.*`` data only.
"""

from __future__ import annotations

import copy
import json
import unittest
from functools import lru_cache
from typing import Any
from unittest import mock

from packages.derivation import presentation_projection as pp
from packages.derivation.loader import DerivationSchemas
from packages.derivation.package_validation import load_published_citizen_checksums, validate_package
from packages.tax.loader import domain_package_companion_declarations
from tests import test_input_questions as miq
from tests.helpers import current_core_returns as c
from tests.test_input_questions import CONTENT, RELEASE_DIR, P, blocked, drop
from tests.test_statement_withholding_answer import _no_withholding

CORE = miq.CORE
CORES = dict(miq.CORES)
CORES["v73"] = ("package.core-calculations.v73.json", "v73", "demo.release.sli-worksheet-integration.2025.v71.json",
                "v71", "published-packages.v71.json")

# Group id, the filer's question (yes = present), and its facts as (fact type, polarity, return). Polarity "abs":
# the recorded "yes" asserts the thing is absent, so the question's yes records "no" and its no records "yes";
# "pos": question and record agree; "choice": filing status records the chosen value.
GROUPS: list[tuple[str, str, list[tuple[str, str, str]]]] = [
    ('FTC1', 'Do you want to claim the foreign tax you paid as a credit without filing Form 1116?',
     [('direct-ftc.election', 'pos', 'div-b7')]),
    ('FTC2', 'Besides the foreign tax shown on your Form 1099-DIV statements, did you have foreign income, or pay foreign tax, that was reported anywhere else (for example on a Form 1099-INT, a Schedule K-1 or K-3, or from any other source)?',
     [('direct-ftc-scope.all-foreign-income-on-1099div', 'abs', 'div-b7'), ('direct-ftc-scope.no-f1099int-foreign-tax', 'abs', 'div-b7'), ('direct-ftc-scope.no-k1-k3-foreign-tax', 'abs', 'div-b7'), ('direct-ftc-scope.no-other-foreign-tax-source', 'abs', 'div-b7')]),
    ('FTC3', 'Was the foreign tax you are claiming an income tax (or a tax charged in place of one), paid to a country the United States recognizes and that does not support terrorism, which you were legally responsible for and paid yourself?',
     [('direct-ftc-scope.tax-type-creditable', 'pos', 'div-b7'), ('direct-ftc-scope.country-recognized-non-terrorism', 'pos', 'div-b7'), ('direct-ftc-scope.legal-liability-and-paid', 'pos', 'div-b7')]),
    ('FTC4', 'Was all of your foreign income passive investment income, such as dividends?',
     [('direct-ftc-scope.all-foreign-income-passive', 'pos', 'div-b7')]),
    ('FTC5', 'Did you hold each dividend-paying stock or fund that produced foreign tax for at least 16 days around its ex-dividend date?',
     [('direct-ftc-scope.holding-period-16-day-met', 'pos', 'div-b7')]),
    ('FTC6', 'Was any of the foreign tax refunded, rebated, subsidized or reimbursed to you, linked to income you excluded from your return, or tied to a short sale or other obligation to pay the dividend on to someone else?',
     [('direct-ftc-scope.no-refund-rebate-subsidy', 'abs', 'div-b7'), ('direct-ftc-scope.no-excluded-income-association', 'abs', 'div-b7'), ('direct-ftc-scope.no-short-sale-obligation', 'abs', 'div-b7')]),
    ('FTC7', 'Do you have foreign tax credit to carry back to an earlier year or forward from another year?',
     [('direct-ftc-scope.no-carryback-carryforward', 'abs', 'div-b7')]),
    ('FTC8', 'Are you deducting foreign tax on Schedule A instead of taking a credit?',
     [('direct-ftc-scope.no-schedule-a-deduction-election', 'abs', 'div-b7')]),
    ('FTC9', 'Do you claim any other nonrefundable credit on Schedule 3 lines 2 through 6 (for example child and dependent care, education, retirement savings, home energy, or other credits)?',
     [('direct-ftc-scope.no-sch3-line2', 'abs', 'base'), ('direct-ftc-scope.no-sch3-line3', 'abs', 'base'), ('direct-ftc-scope.no-sch3-line4', 'abs', 'base'), ('direct-ftc-scope.no-sch3-line5', 'abs', 'base'), ('direct-ftc-scope.no-sch3-line6', 'abs', 'base')]),
    ('FTC10', 'Does the tax on your 2025 Form 1040 line 16 include tax from a lump-sum distribution (Form 4972), or do you have any additional tax on Form 1040 line 17 (from Schedule 2)?',
     [('direct-ftc-scope.no-form-4972-on-line16', 'abs', 'div-b7'), ('direct-ftc-scope.no-line17-schedule2-additional', 'abs', 'base')]),
    ('FTC12', 'Does your 2025 Schedule 2 show an amount on Part I line 1a or line 1z (an addition to your regular tax)?',
     [('direct-ftc-scope.no-schedule2-regular-tax-add', 'abs', 'div-b7')]),
    ('FTC11', 'Is your total foreign tax from all sources more than $300 ($600 if you file jointly), or is there any other reason you must file Form 1116?',
     [('direct-ftc-scope.no-form-1116-required', 'abs', 'div-b7')]),
    ('S1A', 'In 2025, did you have any of these adjustments to income: educator expenses; business expenses of a reservist, performing artist or fee-basis government official; a health savings account deduction; moving expenses for the Armed Forces; the deductible part of self-employment tax; a self-employed SEP, SIMPLE or qualified plan deduction; self-employed health insurance; a penalty on early withdrawal of savings; alimony you paid; an IRA deduction; an Archer MSA deduction; or any other adjustment listed on Schedule 1 lines 24a through 24z (do not count student loan interest)?',
     [('schedule1-adjustments-scope.no-line11-educator', 'abs', 'base'), ('schedule1-adjustments-scope.no-line12-business-expenses', 'abs', 'base'), ('schedule1-adjustments-scope.no-line13-hsa', 'abs', 'base'), ('schedule1-adjustments-scope.no-line14-moving', 'abs', 'base'), ('schedule1-adjustments-scope.no-line15-deductible-se', 'abs', 'base'), ('schedule1-adjustments-scope.no-line16-se-retirement', 'abs', 'base'), ('schedule1-adjustments-scope.no-line17-se-health', 'abs', 'base'), ('schedule1-adjustments-scope.no-line18-penalty', 'abs', 'base'), ('schedule1-adjustments-scope.no-line19-alimony-paid', 'abs', 'base'), ('schedule1-adjustments-scope.no-line20-ira-deduction', 'abs', 'base'), ('schedule1-adjustments-scope.no-line23-archer-msa', 'abs', 'base'), ('schedule1-adjustments-scope.no-line25-other-adjustments', 'abs', 'base')]),
    ('S1B', 'In 2025, did you receive alimony, or have income or loss from a business, a farm, rental property or royalties, a partnership, S corporation or trust, or any other gain or loss reported on Schedule 1 lines 2a through 6?',
     [('schedule1-part1-scope.no-sch1-line2a-alimony', 'abs', 'base'), ('schedule1-part1-scope.no-sch1-line3-business', 'abs', 'base'), ('schedule1-part1-scope.no-sch1-line4-other-gains', 'abs', 'base'), ('schedule1-part1-scope.no-sch1-line5-rental', 'abs', 'base'), ('schedule1-part1-scope.no-sch1-line6-farm', 'abs', 'base')]),
    ('S1C', 'Did you receive a refund, credit or offset of state or local income tax in 2025?',
     [('schedule1-part1-scope.no-f1099g-box2-state-refund', 'abs', 'base'), ('schedule1-part1-scope.no-sch1-line1-taxable-refunds', 'abs', 'base')]),
    ('S1D', 'Did you receive any other payment on a Form 1099-G besides unemployment compensation and state or local tax refunds (for example a taxable grant or an agriculture payment)?',
     [('schedule1-part1-scope.no-f1099g-other-payment-classes', 'abs', 'base')]),
    ('S1E', 'Did you repay any unemployment compensation in 2025?',
     [('schedule1-part1-scope.no-unemployment-repayment', 'abs', 'base')]),
    ('L2A1', 'Did you receive tax-exempt interest on a Form 1099-INT (box 8) in 2025?',
     [('line2a-scope.no-f1099int-tax-exempt', 'abs', 'base')]),
    ('L2A2', 'Did you receive tax-exempt interest or tax-exempt original issue discount shown on a Form 1099-OID, tax-exempt interest that was not reported on any form, or have an adjustment for bond premium or acquisition premium on tax-exempt bonds?',
     [('line2a-scope.no-f1099oid-tax-exempt', 'abs', 'base'), ('line2a-scope.no-unreported-tax-exempt', 'abs', 'base'), ('line2a-scope.no-premium-adjustment', 'abs', 'base')]),
    ('L2A3', "Does your 2025 return include Form 6251 (alternative minimum tax), Form 8814 (election to report your child's interest and dividends), or a credit or deduction that counts your tax-exempt interest as part of your income?",
     [('line2a-scope.no-amt-form-6251', 'abs', 'base'), ('line2a-scope.no-credit-using-tax-exempt', 'abs', 'base'), ('line2a-scope.no-deduction-using-tax-exempt', 'abs', 'base'), ('line2a-scope.no-child-income-election', 'abs', 'base')]),
    ('DEP1', 'Can someone else claim you (or your spouse, on a joint return) as a dependent on their 2025 return?',
     [('standard-deduction.can-be-claimed-as-dependent', 'pos', 'base')]),
    ('DEP2', 'Is someone else claiming you as a dependent on their 2025 return?',
     [('sli-scope.not-claimed-as-dependent', 'abs', 'f1098e')]),
    ('SLI1', 'Are you legally obligated to pay the interest on the student loan(s) you are claiming?',
     [('sli-scope.legally-obligated-for-interest', 'pos', 'f1098e')]),
    ('EXC1', 'For 2025, did you claim the foreign earned income exclusion (Form 2555), or exclude income as a bona fide resident of Puerto Rico or American Samoa (Form 4563)?',
     [('sli-scope.no-form-2555', 'abs', 'f1098e'), ('sli-scope.no-form-4563', 'abs', 'f1098e'), ('sli-scope.no-puerto-rico-or-samoa-income', 'abs', 'f1098e'), ('ctc.no-puerto-rico-or-4563-exclusion', 'abs', 'base')]),
    ('EIC1', 'Does your Social Security number allow you to work in the United States? Answer yes if it was issued by the Social Security Administration on or before the due date of your 2025 return (including extensions) and is not marked "Not Valid for Employment", or if it is marked "Valid for Work Only With DHS Authorization" and that authorization is still valid.',
     [('eic.taxpayer-valid-ssn', 'pos', 'part-ii-b')]),
    ('EIC2', 'Were you, or was your spouse, a nonresident alien for any part of 2025 (do not count a nonresident or dual-status alien spouse you chose to treat as a U.S. resident for the whole year)?',
     [('eic.not-nonresident-alien', 'abs', 'part-ii-b')]),
    ('EIC3', 'Could you be a qualifying child of another person for 2025 (do not count the case where that person is not required to file a 2025 return and is not filing one, or is filing only to claim a refund of withheld or estimated tax)?',
     [('eic.not-qualifying-child-of-another', 'abs', 'part-ii-b')]),
    ('EIC4', 'Does any of these apply to you for 2025: you file Form 2555; you must file Form 8862 or are barred from the earned income credit for a prior year; you are self-employed with Schedule SE or Schedule C as a statutory employee, or you are a member of the clergy or had church employee income of $108.28 or more; you elect to include nontaxable combat pay; you excluded a Medicaid waiver payment on Schedule 1 line 8s; or you have Schedule E, Form 4797, Form 8814, personal property rental, or passive activity income or loss?',
     [('eic.no-unsupported-situations', 'abs', 'base')]),
    ('CG1', 'Besides capital gain distributions in box 2a of Form 1099-DIV, did you have any other capital gain or loss in 2025 (including any capital loss, any amount in Form 1099-DIV box 2b, 2c or 2d, or a gain deferred through a qualified opportunity fund)?',
     [('exception1.only-box2a-capital-gains', 'abs', 'base'), ('exception1.no-capital-losses', 'abs', 'base'), ('exception1.no-qof-deferral', 'abs', 'base'), ('exception1.no-boxes-2b-2c-2d', 'abs', 'base')]),
    ('CG2', 'Do you have a capital loss carried over from 2024 or an earlier year?',
     [('schedule-d-boundary.no-inbound-capital-loss-carryovers', 'abs', 'base')]),
    ('CTC1', 'Do you claim any dependent on your 2025 return besides the children you counted for the child tax credit (for example a qualifying relative, or a child who does not meet the child tax credit tests)?',
     [('ctc.no-other-dependent', 'abs', 'base')]),
    ('CR1', 'Do you claim the American opportunity credit, the refundable adoption credit, or any Schedule 3 Part II credit (Form 1040 lines 29 through 31)?',
     [('lines29-31-scope.no-other-refundable-credits', 'abs', 'base')]),
    ('SS1', 'Did you choose the lump-sum election for Social Security benefits that relate to an earlier year?',
     [('ss-benefits-scope.no-lump-sum-election', 'abs', 'base')]),
    ('SS2', 'Did you receive a Form RRB-1099, a Form SSA-1042S, or any foreign social benefit statement in 2025?',
     [('ss-benefits-scope.no-rrb-or-foreign-social-benefit', 'abs', 'base')]),
    ('M1', 'Did you receive a Form 1098 mortgage interest statement for 2025?',
     [('f1098-scope.no-mortgage-statement', 'abs', 'base')]),
    ('M2', 'Do you owe $1,000 or more in tax for 2025 after subtracting your withholding and refundable credits, and did you pay less through withholding and estimated payments than both 90% of your 2025 tax and 100% of your 2024 tax (110% of your 2024 tax if your 2024 adjusted gross income was more than $150,000)?',
     [('line38-scope.no-estimated-tax-penalty', 'abs', 'base')]),
    ('M3', 'In 2025, did you have qualified business income, qualified REIT dividends (Form 1099-DIV box 5), or publicly traded partnership income that could give you a qualified business income deduction?',
     [('qbi.no-qbi-deduction-declared', 'abs', 'base')]),
    ('M4', 'Did you receive qualified tips or qualified overtime pay in 2025, or pay interest on a loan for a new personal vehicle (qualified passenger vehicle loan interest), that could give you a deduction on Schedule 1-A Parts II through IV?',
     [('schedule1a.no-parts-ii-iv-deductions-declared', 'abs', 'base')]),
    ('M5', 'Do you owe any of the other taxes on Schedule 2 Part II, such as self-employment tax, additional Medicare tax, or net investment income tax?',
     [('schedule2-partii-scope.no-line21-additional-taxes', 'abs', 'base')]),
    ('M6', "Besides gambling winnings on a Form W-2G you have recorded, did you have any other income that goes on Schedule 1 lines 8a through 8z (for example gambling winnings not on a W-2G, a Form W-2G in someone else's name, gambling that is a business, prizes and awards, jury duty pay, an Alaska Permanent Fund dividend, or canceled debt)?",
     [('w2g-scope.no-sch1-other-income-except-w2g', 'abs', 'base')]),
    ('FS1', 'What is your filing status for 2025: single, married filing jointly, married filing separately, head of household, or qualifying surviving spouse?',
     [('filing-status', 'choice', 'base')]),
]

DIV_BOX4 = miq.QUESTION["f1099div.box4-withholding"]
RETURNS = {
    "base": lambda: c.base_return(),
    "div-b7": lambda: c.add_foreign_tax_1099div(c.base_return(), [30.0]),
    "f1098e": lambda: c.add_student_loan_interest_1098e(c.base_return(), [500.0]),
    "part-ii-b": lambda: c.part_ii_b_return(box4=300.0, box6=200.0),
}
FACTS = {fact: (gid, text, pol, ret) for gid, text, ms in GROUPS for fact, pol, ret in ms}
SENTENCE = {gid: text for gid, text, _ in GROUPS}


def run_model(acts: list[dict[str, object]], name: str, core: str) -> dict[str, Any]:
    saved = dict(miq.CORES)
    miq.CORES.update(CORES)
    try:
        return miq.run_model(acts, name, core)
    finally:
        miq.CORES.clear()
        miq.CORES.update(saved)


def withheld(facts: list[str], ret: str) -> list[dict[str, object]]:
    acts = RETURNS[ret]()
    return drop(acts, *[P + f for f in facts])


@lru_cache(maxsize=None)
def run(case: str, core: str = "v73") -> str:
    kind, _, rest = case.partition(":")
    if kind == "withhold":  # withhold:<return>:<fact>[,<fact>...]
        ret, _, facts = rest.partition(":")
        acts = withheld(facts.split(","), ret)
    elif kind == "box2+scope":
        acts = drop(c.base_return(), P + "w2.box2-withholding", P + "line2a-scope.no-amt-form-6251")
    else:
        raise KeyError(case)
    return json.dumps(run_model(acts, f"demo.saq.{abs(hash(case)) % 10**8}.{core}", core), sort_keys=True)


def loaded(case: str, core: str = "v73") -> dict[str, Any]:
    value: dict[str, Any] = json.loads(run(case, core))
    return value


def lines_with(model: dict[str, Any]) -> dict[str, list[str] | None]:
    return blocked(model)


class OneCasePerGroup(unittest.TestCase):
    """Withhold one fact of the group on the return that asks it: every blocked line names the group's question."""


def _add_group_test(gid: str, fact: str, ret: str) -> None:
    def test(self: unittest.TestCase) -> None:
        got = lines_with(loaded(f"withhold:{ret}:{fact}"))
        self.assertTrue(got, "withholding the fact blocks at least one line")
        named = 0
        extra = {DIV_BOX4} if ret == "div-b7" else set()  # that builder predates v71 and lacks the 1099-DIV box 4 answer
        for line, reasons in got.items():
            self.assertIsNotNone(reasons, f"{gid} {fact}: line {line} kept the generic text")
            assert reasons is not None
            if extra and reasons == [DIV_BOX4]:  # held only by the builder's missing box 4 answer
                continue
            named += 1
            self.assertIn(SENTENCE[gid], reasons, f"{gid} {fact}: line {line}")
            self.assertLessEqual(set(reasons) - {SENTENCE[gid]}, extra, f"{gid} {fact}: line {line}")
        self.assertGreater(named, 0, f"{gid} {fact}: no line names the question")
    test.__name__ = f"test_{gid.lower()}_{fact.replace('.', '_').replace('-', '_')}"
    setattr(OneCasePerGroup, test.__name__, test)


for _gid, _text, _members in GROUPS:
    _add_group_test(_gid, _members[0][0], _members[0][2])
# EXC1 spans returns: its student-loan members need a Form 1098-E
for _fact in ("sli-scope.no-form-2555",):
    _gid, _text, _pol, _ret = FACTS[_fact]
    _add_group_test(_gid, _fact, _ret)


class SeveralFactsOfOneGroup(unittest.TestCase):
    def test_a_group_question_is_shown_once_when_every_member_is_missing(self) -> None:
        members = [f for f, _, _ in dict((g, ms) for g, _, ms in GROUPS)["S1A"]]
        self.assertEqual(len(members), 12)
        got = lines_with(loaded("withhold:base:" + ",".join(members)))
        self.assertTrue(got)
        for line, reasons in got.items():
            self.assertEqual(reasons, [SENTENCE["S1A"]], line)

    def test_two_groups_missing_together_name_both_sorted_where_a_line_waits_on_both(self) -> None:
        a = [f for f, _, _ in dict((g, ms) for g, _, ms in GROUPS)["S1B"]][:2]
        b = ["line2a-scope.no-amt-form-6251"]
        got = lines_with(loaded("withhold:base:" + ",".join(a + b)))
        both = sorted([SENTENCE["S1B"], SENTENCE["L2A3"]])
        self.assertIn(both, got.values())
        self.assertLessEqual({tuple(r) for r in got.values() if r}, {tuple(both), (SENTENCE["S1B"],), (SENTENCE["L2A3"],)})
        self.assertTrue(all(got.values()))

    def test_a_missing_filing_status_names_its_question_on_every_line_it_blocks(self) -> None:
        got = lines_with(loaded("withhold:base:filing-status"))
        self.assertEqual(len(got), 35)
        self.assertEqual({tuple(r or ()) for r in got.values()}, {(SENTENCE["FS1"],)})

    def test_the_rounding_convention_beside_a_scope_answer_keeps_the_generic_text(self) -> None:
        acts = drop(c.base_return(), "rounding.convention", P + "line2a-scope.no-amt-form-6251")
        got = lines_with(run_model_json(acts, "demo.saq.rounding-and-scope"))
        self.assertTrue(got)
        self.assertEqual({r for r in got.values() if r}, set())


def run_model_json(acts: list[dict[str, object]], name: str) -> dict[str, Any]:
    return run_model(acts, name, "v73")


class MixedWithAnAmount(unittest.TestCase):
    def test_a_line_waiting_on_a_missing_amount_and_a_scope_answer_names_both_sorted(self) -> None:
        got = lines_with(loaded("box2+scope"))
        w2, scope = miq.QUESTION["w2.box2-withholding"], SENTENCE["L2A3"]
        self.assertEqual(got["25a"], [w2])
        self.assertEqual(got["2a"], [scope])
        both = sorted([w2, scope])
        self.assertEqual(got["33"], both)
        self.assertEqual(got["37"], both)


class EarlierCoresAreUnchanged(unittest.TestCase):
    """The saved presentation of v68-v72 equals what the projection wrote before the binding map existed."""

    CASES = ("withhold:base:filing-status", "withhold:base:line2a-scope.no-amt-form-6251", "box2+scope")

    @staticmethod
    def _without_binding_map(*args: Any, symbol_fact_types: Any = None, **kwargs: Any) -> Any:
        return _ORIGINAL(*args, **kwargs)

    def test_v68_to_v72_saved_presentations_are_byte_identical_without_the_binding_map(self) -> None:
        for core in ("v68", "v69", "v70", "v71", "v72"):
            for case in self.CASES:
                with self.subTest(core=core, case=case):
                    after = run(case, core)
                    with mock.patch.object(pp, "_closure_question_reasons", self._without_binding_map):
                        kind, _, rest = case.partition(":")
                        acts = drop(c.base_return(), P + "w2.box2-withholding", P + "line2a-scope.no-amt-form-6251") \
                            if kind == "box2+scope" else withheld(rest.partition(":")[2].split(","), "base")
                        before = json.dumps(run_model(acts, f"demo.saq.{abs(hash(case)) % 10**8}.{core}", core), sort_keys=True)
                    self.assertEqual(after, before)

    def test_earlier_cores_name_no_scope_answer_or_filing_status(self) -> None:
        for core in ("v72",):
            got = lines_with(loaded("withhold:base:filing-status", core))
            self.assertTrue(got)
            self.assertEqual({r for r in got.values() if r}, set())
            got = lines_with(loaded("withhold:base:line2a-scope.no-amt-form-6251", core))
            self.assertEqual({r for r in got.values() if r}, set())

    def test_v73_blocks_exactly_the_lines_v72_does(self) -> None:
        for case in self.CASES:
            with self.subTest(case=case):
                self.assertEqual(sorted(lines_with(loaded(case, "v72"))), sorted(lines_with(loaded(case, "v73"))))


_ORIGINAL = pp._closure_question_reasons


def _pkg(name: str) -> dict[str, Any]:
    return miq._package(name)


class Declaration(unittest.TestCase):
    def test_eighty_citizens_one_per_fact_each_with_its_groups_sentence_verbatim(self) -> None:
        corpus = miq._corpus()
        package = _pkg("package.core-calculations.v73.json")
        pinned = [m for m in package["members"] if m["role"] == "input-question"]
        self.assertEqual(len(pinned), 88)
        got: dict[str, str] = {}
        for pin in pinned:
            body = corpus[(pin["id"], pin["version"])]
            self.assertEqual(body["schema"], "input-question.v1")
            fact = body["fact_type"]["id"].removeprefix(P)
            self.assertNotIn(fact, got, "one citizen per fact type")
            got[fact] = body["question"]
        expected = {f: text for _, text, ms in GROUPS for f, _, _ in ms}
        expected.update(miq.QUESTION)
        self.assertEqual(got, expected)
        self.assertEqual(len(GROUPS), 41)
        self.assertEqual(len({f for _, _, ms in GROUPS for f, _, _ in ms}), 80)

    def test_every_question_asks_whether_the_thing_is_present(self) -> None:
        for gid, text, _ in GROUPS:
            with self.subTest(gid=gid):
                self.assertIn("?", text)
                self.assertTrue(text.endswith("?") or gid == "EIC1")
                self.assertNotRegex(text, r"(?i)\b(none of|not present|absent)\b")
                self.assertFalse(text.lower().startswith(("do you not", "did you not", "have you no")))

    def test_v73_validates_and_v72_still_does(self) -> None:
        corpus = miq._corpus()
        for name, registry in (("package.core-calculations.v73.json", "published-packages.v71.json"),
                               ("package.core-calculations.v72.json", "published-packages.v70.json")):
            package = _pkg(name)
            self.assertEqual(package["schema"], "artifact-package.v39")
            members = {(m["id"], m["version"]): corpus[(m["id"], m["version"])] for m in package["members"]}
            result = validate_package(package, members, DerivationSchemas(),
                                      load_published_citizen_checksums(CONTENT / registry))
            self.assertEqual(list(result.issues), [], name)

    def test_v73_adds_only_the_80_citizens_and_keeps_every_binding(self) -> None:
        v72, v73 = _pkg("package.core-calculations.v72.json"), _pkg("package.core-calculations.v73.json")
        pins72 = {(m["id"], m["version"]) for m in v72["members"]}
        pins73 = {(m["id"], m["version"]) for m in v73["members"]}
        self.assertEqual(pins72 - pins73, set())
        added = pins73 - pins72
        self.assertEqual(len(added), 80)
        self.assertTrue(all(i.startswith("tax.us.2025.input-question.") for i, _ in added))
        self.assertEqual(v72["input_bindings"], v73["input_bindings"])
        self.assertEqual(v72["schema"], v73["schema"])
        declarations = domain_package_companion_declarations()
        self.assertEqual(declarations[(CORE, "v73")], declarations[(CORE, "v72")])

    def test_registry_v71_only_adds_to_v70_and_release_v71_pins_it(self) -> None:
        import hashlib
        old, new = _pkg("published-packages.v70.json"), _pkg("published-packages.v71.json")
        self.assertEqual(len(new["citizens"]), len(old["citizens"]) + 80)
        old_c = {(x["id"], x["version"]): x["checksum"] for x in old["citizens"]}
        new_c = {(x["id"], x["version"]): x["checksum"] for x in new["citizens"]}
        self.assertTrue(old_c.items() <= new_c.items())
        old_p = {(x["id"], x["version"]): x["checksum"] for x in old["packages"]}
        new_p = {(x["id"], x["version"]): x["checksum"] for x in new["packages"]}
        self.assertTrue(old_p.items() <= new_p.items())
        self.assertEqual(set(new_p) - set(old_p), {(CORE, "v73")})
        release = json.loads((RELEASE_DIR / CORES["v73"][2]).read_text("utf-8"))
        self.assertEqual(release["version"], "v71")
        self.assertEqual(release["package_registry_sha256"],
                         hashlib.sha256((CONTENT / "published-packages.v71.json").read_bytes()).hexdigest())

    def test_the_filing_status_citizen_pins_the_fact_type_the_binding_names(self) -> None:
        package = _pkg("package.core-calculations.v73.json")
        binding = next(b for b in package["input_bindings"] if b["symbol"] == "filing_status")
        citizen = copy.deepcopy(miq._citizen("filing-status"))
        self.assertEqual(citizen["fact_type"], binding["fact_type"])
        self.assertEqual(citizen["question"], SENTENCE["FS1"])


# --- the polarity of each fact against what the rules read -------------------------------------------

# Facts whose reading rules branch on "no" as well as "yes" (the other value is a legal zero, a different path or a
# credit of $0, not only a block); every other fact is read only as "yes" (any "no" falls through to a block).
BRANCHES_ON_NO = {
    "ctc.no-other-dependent",                      # no -> line 6 counts the closed rosters of other dependents
    "line2a-scope.no-f1099int-tax-exempt",         # no -> the closed Form 1099-INT box 8 subtotal (Path B)
    "standard-deduction.can-be-claimed-as-dependent",  # yes -> line 4c worksheet, no -> line 3 + line 4b
    "sli-scope.not-claimed-as-dependent",          # no -> legal zero deduction
    "sli-scope.legally-obligated-for-interest",    # no -> legal zero deduction
    "f1098-scope.no-mortgage-statement",           # boolean: true -> itemized path, false -> statement path
    "eic.taxpayer-valid-ssn",                      # no -> the earned income credit answer publishes 0 (or blocks)
    "eic.not-nonresident-alien",                   # no -> credit not available
    "eic.not-qualifying-child-of-another",         # no -> credit $0
    "eic.no-unsupported-situations",               # no -> outside the computation (blocks)
}
# A positive-looking fact title can still contain an absence word; these are the "pos" facts that do.
POS_TITLE_HAS_ABSENCE_WORD = {"direct-ftc-scope.country-recognized-non-terrorism", "eic.taxpayer-valid-ssn",
                              "direct-ftc.election", "sli-scope.legally-obligated-for-interest"}
# "abs" facts whose title is stated positively; the question asks the opposite ("any other ...?"), so its yes records no.
ABS_WITH_POSITIVE_TITLE = {"direct-ftc-scope.all-foreign-income-on-1099div", "exception1.only-box2a-capital-gains"}
ABSENCE_WORDS = ("no ", "not ", "none", "absent", "without", "neither")


def _literals(package: dict[str, Any], corpus: dict[tuple[str, str], dict[str, Any]], fact: str) -> set[str]:
    """Every literal a reading rule compares the fact with (``eq``/``ne``), over the package's rule members."""
    found: set[str] = set()

    def walk(node: Any) -> None:
        if isinstance(node, dict):
            if node.get("op") == "categorical_compare":
                left, right = node.get("left", {}), node.get("right", {})
                if left.get("name") == P + fact and right.get("op") == "category_literal":
                    found.add(str(right["value"]))
            for value in node.values():
                walk(value)
        elif isinstance(node, list):
            for value in node:
                walk(value)

    for pin in package["members"]:
        body = corpus[(pin["id"], pin["version"])]
        if str(body.get("schema", "")).startswith("rule-artifact."):
            walk(body)
    return found


class Polarity(unittest.TestCase):
    """Each fact's flag in GROUPS (abs: the recorded "yes" asserts an absence; pos: question and record agree)
    is read against the value the rules treat as supported, and against the fact's own title."""

    corpus: dict[tuple[str, str], dict[str, Any]]
    package: dict[str, Any]
    titles: dict[str, str]

    @classmethod
    def setUpClass(cls) -> None:
        cls.corpus = miq._corpus()
        cls.package = _pkg("package.core-calculations.v73.json")
        cls.titles = {}
        for pin in cls.package["members"]:
            body = cls.corpus[(pin["id"], pin["version"])]
            for fact_type in body.get("fact_types", []):
                cls.titles[str(fact_type["id"]).removeprefix(P)] = str(fact_type["title"])

    def facts(self) -> list[tuple[str, str]]:
        return [(f, pol) for _, _, ms in GROUPS for f, pol, _ in ms if pol != "choice"]

    def test_there_are_79_flagged_facts_and_filing_status_is_a_choice(self) -> None:
        self.assertEqual(len(self.facts()), 79)
        self.assertEqual([pol for _, _, ms in GROUPS for f, pol, _ in ms if f == "filing-status"], ["choice"])

    def test_the_rules_compare_each_single_valued_fact_only_with_yes(self) -> None:
        for fact, _ in self.facts():
            if fact in BRANCHES_ON_NO:
                continue
            with self.subTest(fact=fact):
                literals = _literals(self.package, self.corpus, fact)
                self.assertTrue(literals, "a reading rule compares the fact")
                self.assertEqual(literals - {"yes", "no"}, set())
                # the rules gate on "yes": a rule that branched on "no" would make "no" a supported value
                self.assertNotIn("no", literals)

    def test_the_question_yes_value_is_unsupported_for_abs_and_supported_for_pos(self) -> None:
        for fact, pol in self.facts():
            if fact in BRANCHES_ON_NO:
                continue
            with self.subTest(fact=fact):
                question_yes = "no" if pol == "abs" else "yes"
                supported = "yes"
                self.assertEqual(question_yes == supported, pol == "pos")

    def test_an_abs_fact_title_says_something_is_absent_and_a_pos_title_does_not_unless_listed(self) -> None:
        for fact, pol in self.facts():
            if fact == "f1098-scope.no-mortgage-statement" or fact == "qbi.no-qbi-deduction-declared":
                continue
            title = self.titles[fact].split(" Contributed categorical")[0].lower()
            has_word = any(word in title or title.startswith(word.strip()) for word in ABSENCE_WORDS)
            with self.subTest(fact=fact, pol=pol):
                if pol == "abs" and fact in ABS_WITH_POSITIVE_TITLE:
                    self.assertFalse(has_word, title)
                elif pol == "abs":
                    self.assertTrue(has_word, title)
                elif fact not in POS_TITLE_HAS_ABSENCE_WORD:
                    self.assertFalse(has_word, title)

    def test_the_boolean_fact_is_true_exactly_when_no_statement_is_recorded(self) -> None:
        fact = "f1098-scope.no-mortgage-statement"
        pol = [p for _, _, ms in GROUPS for f, p, _ in ms if f == fact]
        self.assertEqual(pol, ["abs"])
        text = json.dumps([self.corpus[(m["id"], m["version"])] for m in self.package["members"]
                           if m["id"] == P + "rule.form1040-line12e"])
        self.assertIn("F1098_SCOPE_CONTRADICTION", text)
        self.assertIn(P + fact, text)


class BindingMap(unittest.TestCase):
    def test_a_symbol_the_map_does_not_name_is_looked_up_as_given(self) -> None:
        row = {"code": "DEPENDENCY_ABSENT", "missing": ["tax.us.2025.some-fact"]}
        members = [{"schema": "input-question.v1", "question": "Q?", "fact_type": {"id": "tax.us.2025.some-fact", "version": "v1"}}]
        for mapping in (None, {}, {"filing_status": "tax.us.2025.filing-status"}):
            self.assertEqual(pp._closure_question_reasons(row, resolved_members=members, by_symbol={}, symbol_fact_types=mapping),
                             [{"sentence": "Q?"}])

    def test_a_binding_symbol_reaches_the_question_of_its_fact_type_only_through_the_map(self) -> None:
        row = {"code": "DEPENDENCY_ABSENT", "missing": ["filing_status"]}
        members = [{"schema": "input-question.v1", "question": "Which?",
                    "fact_type": {"id": "tax.us.2025.filing-status", "version": "v1"}}]
        self.assertEqual(pp._closure_question_reasons(row, resolved_members=members, by_symbol={}), [])
        self.assertEqual(pp._closure_question_reasons(row, resolved_members=members, by_symbol={},
                                                      symbol_fact_types={"filing_status": "tax.us.2025.filing-status"}),
                         [{"sentence": "Which?"}])


if __name__ == "__main__":
    unittest.main()
