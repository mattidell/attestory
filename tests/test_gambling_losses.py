"""Track 1: gambling losses reach Schedule A line 16 on core v67.

Every run goes through ``live_coordinate_run`` on the committed packages (core v66 / registry v64 /
release v64, pinned, and the successor core v67 / registry v65 / release v65). The hand values are
those of the milestone's P0 (section 4 of ``gambling-losses-evidence/p0-trace-and-design.md``), computed
from the 2025 Tax Table before the engine ran; the cases assert them. Synthetic ``demo.*`` data only.
"""

from __future__ import annotations

import json
import unittest
from decimal import Decimal
from pathlib import Path
from typing import Any

from packages.tax.loader import domain_package_companion_declarations
from tests import test_w2g_gambling as w2g
from tests.test_refund_or_amount_owed_track1 import _finish
from tests.helpers import current_core_returns as c

P = c.P
ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "packages/content/tax/2025"
EVIDENCE = ROOT / "docs/phases/engine-breadth/milestones/gambling-losses-evidence"

LINE16 = P + "schedule-a.line16"
TOTAL = P + "schedule-a.total"
LINE12E = P + "deductions.line-12e"
AGI = P + "income.agi"
TAXABLE = P + "income.taxable-income"
TAX = P + "tax.line24-total-tax"
REFUND = P + "payments.line35a-refunded"
OWED = P + "payments.line37-amount-owed"
LOSSES_SUBTOTAL = P + "gambling.losses-subtotal"
WINNINGS = P + "gambling.b1-winnings-subtotal"
SCHEDULE_A = P + "scheduleA.disposition"
WATCH = (LINE16, TOTAL, LINE12E, AGI, TAXABLE, TAX, REFUND, OWED)


def _num(run: c.CurrentRun, symbol: str) -> str | None:
    value = run.value(symbol)
    return None if value is None else format(value.normalize(), "f")


def _expect(case: unittest.TestCase, run: c.CurrentRun, **want: str) -> None:
    names = {"l16": LINE16, "total": TOTAL, "l12e": LINE12E, "agi": AGI, "taxable": TAXABLE, "tax": TAX, "refund": REFUND, "owed": OWED}
    for key, expected in want.items():
        case.assertEqual(_num(run, names[key]), expected, (key, expected))


def _roots(run: c.CurrentRun) -> dict[str, tuple[str, list[str]]]:
    return {str(r["artifact_id"]).replace(P, ""): (str(r.get("code")), [str(m) for m in r.get("missing", [])]) for r in run.blocked}


def _w2g(statements: list[tuple[float | None, float | None]], losses: list[float] | None, *, closure: str = "closed",
         itemizer: float | None = None, assertion: float | None = None) -> list[dict[str, object]]:
    """A v67 return: Form W-2G statements, the losses family (None leaves it unanswered), and the way it itemizes."""
    acts = w2g._w2g_return(statements)
    if itemizer is not None:
        acts = c.add_mortgage_itemizer(acts, itemizer)
    if assertion is not None:
        acts = c.add_itemized_assertion(acts, assertion)
    if losses is not None:
        acts = c.add_gambling_losses(acts, losses, closure=closure)
    return acts


def _run(acts: list[dict[str, object]], name: str, *, core: str = "v67") -> c.CurrentRun:
    return c.run_current_core(acts, f"demo.gl.{name}", core=core)


class GamblingLossesCases(unittest.TestCase):
    def test_case_0_baseline_w2g_with_no_losses_is_the_v66_return(self) -> None:
        old = _run(w2g._w2g_return([(6000.0, 1440.0)]), "c0.v66", core="v66")
        new = _run(_w2g([(6000.0, 1440.0)], []), "c0.v67")
        for run in (old, new):
            _expect(self, run, l12e="15750", agi="56000", taxable="40250", tax="4595", refund="1345")
        self.assertEqual(new.value(LINE16), 0)
        self.assertEqual(new.blocked, [])

    def test_case_1_standard_deduction_with_losses_is_unchanged(self) -> None:
        run = _run(_w2g([(6000.0, 1440.0)], [2000.0]), "c1")
        _expect(self, run, l16="2000", l12e="15750", agi="56000", taxable="40250", tax="4595", refund="1345")
        self.assertEqual(run.blocked, [])
        self.assertNotIn(SCHEDULE_A, run.pubs)

    def test_a_filer_who_says_they_have_losses_is_no_longer_refused(self) -> None:
        refused = w2g._w2g_return([(6000.0, 1440.0)])
        w2g._set_answer(refused, w2g.GAMBLING_DECLARED, "no")
        old = _run(refused, "refused.v66", core="v66")
        self.assertNotIn(AGI, old.pubs)  # the v66 refusal, by the declaration
        accepted = _w2g([(6000.0, 1440.0)], [2000.0])
        w2g._set_answer(accepted, w2g.GAMBLING_DECLARED, "no")
        new = _run(accepted, "refused.v67")
        _expect(self, new, agi="56000", taxable="40250", tax="4595", refund="1345")
        self.assertEqual(new.blocked, [])

    def test_case_2_losses_alone_decide_to_itemize(self) -> None:
        acts = c.declare_no_other_line16(_w2g([(20000.0, 4800.0)], [20000.0]))
        run = _run(acts, "c2")
        _expect(self, run, l16="20000", total="20000", l12e="20000", agi="70000", taxable="50000", tax="5920", refund="3380")
        # Known gap (reported): Schedule A is required here but the line 8a part has no Form 1098 statement
        # to itemize, so the attachment alone blocks; every figure above still publishes.
        self.assertEqual(run.blocked_names(), {("rule.attachment.schedule-a", "DEPENDENCY_ABSENT")})
        self.assertEqual(run.blocked[0]["missing"], [P + "schedule-a.line8a"])
        # The same winnings without the losses stay on the standard deduction.
        base = _run(_w2g([(20000.0, 4800.0)], []), "c2.base")
        _expect(self, base, l12e="15750", taxable="54250", tax="6855", refund="2445")

    def test_case_3_itemizer_with_losses_below_winnings(self) -> None:
        acts = c.declare_no_other_line16(_w2g([(6000.0, 1440.0)], [2000.0], itemizer=20000.0))
        run = _run(acts, "c3")
        _expect(self, run, l16="2000", total="22000", l12e="22000", taxable="34000", tax="3845", refund="2095")
        self.assertEqual(run.blocked, [])
        value = run.pubs[SCHEDULE_A]["value"]
        self.assertTrue(value["required"])
        self.assertEqual(Decimal(str(value["triggers"][0]["value"])), 6250)
        control = _run(c.declare_no_other_line16(_w2g([(6000.0, 1440.0)], [], itemizer=20000.0)), "c3.base")
        _expect(self, control, l12e="20000", taxable="36000", tax="4085", refund="1855")

    def test_case_4_losses_above_winnings_are_limited(self) -> None:
        for losses in ([9000.0], [4000.0, 5000.0]):
            acts = c.declare_no_other_line16(_w2g([(6000.0, 1440.0)], losses, itemizer=20000.0))
            run = _run(acts, f"c4.{len(losses)}")
            _expect(self, run, l16="6000", total="26000", l12e="26000", taxable="30000", tax="3365", refund="2575")
            self.assertEqual(run.blocked, [])
            # The part of the losses that does not count is the two published symbols' difference.
            self.assertEqual(run.value(LOSSES_SUBTOTAL) - run.value(LINE16), 3000)  # type: ignore[operator]

    def test_case_4b_losses_equal_to_winnings(self) -> None:
        run = _run(c.declare_no_other_line16(_w2g([(6000.0, 1440.0)], [6000.0], itemizer=20000.0)), "c4b")
        _expect(self, run, l16="6000", l12e="26000")

    def test_case_5_losses_with_no_winnings_count_as_zero(self) -> None:
        acts = c.declare_no_other_line16(c.add_gambling_losses(c.add_mortgage_itemizer(c.base_return(), 20000.0), [2000.0]))
        run = _run(acts, "c5")
        _expect(self, run, l16="0", total="20000", l12e="20000", taxable="30000", tax="3365", refund="1135")
        self.assertEqual(run.blocked, [])
        std = _run(c.add_gambling_losses(c.base_return(), [2000.0]), "c5b")
        _expect(self, std, l16="0", l12e="15750", taxable="34250", tax="3875", refund="625")

    def test_case_6_an_unconfirmed_losses_family_is_unresolved_not_zero(self) -> None:
        for mode in ("never", "stale"):
            losses = [2000.0] if mode == "never" else [1000.0, 1000.0]
            run = _run(_w2g([(6000.0, 1440.0)], losses, closure=mode), f"c6.{mode}")
            code, missing = _roots(run)["rule.gambling-losses-subtotal"]
            self.assertEqual(code, "SOURCE_SET_UNCLOSED")
            self.assertEqual(_roots(run)["rule.schedule-a-line16"][0], "DEPENDENCY_ABSENT")
            self.assertEqual(missing, [P + "gambling.losses"])
            for symbol in (LINE16, LOSSES_SUBTOTAL, TOTAL, LINE12E, TAXABLE, TAX, REFUND):
                self.assertNotIn(symbol, run.pubs, (mode, symbol))
            self.assertEqual(_num(run, AGI), "56000")

    def test_a_w2g_return_that_never_answered_the_losses_question_stops_at_line_12e(self) -> None:
        run = _run(_w2g([(6000.0, 1440.0)], None), "d1")
        for symbol in (LINE16, LINE12E, TAXABLE, REFUND):
            self.assertNotIn(symbol, run.pubs, symbol)
        self.assertEqual(_num(run, AGI), "56000")

    def test_case_7_the_tie_goes_to_the_standard_deduction(self) -> None:
        run = _run(c.declare_no_other_line16(_w2g([(20000.0, 4800.0)], [15750.0])), "c7")
        _expect(self, run, l16="15750", total="15750", l12e="15750", taxable="54250", tax="6855", refund="2445")
        self.assertNotIn(SCHEDULE_A, run.pubs)

    def test_d2_a_hand_entered_total_and_line_16_are_refused_by_name(self) -> None:
        run = _run(_w2g([(6000.0, 1440.0)], [2000.0], assertion=20000.0), "d2")
        # The block's own code is not in the closed blocked-code set, so the row is DEPENDENCY_INVALID on
        # line 12e; the reason is in the rule's notes (decision 4).
        code, _ = _roots(run)["rule.form1040-line12e"]
        self.assertEqual(code, "DEPENDENCY_INVALID")
        self.assertIn("ITEMIZED_TOTAL_WITH_GAMBLING_LOSSES", (CONTENT / "rule.form1040-line12e.v3.json").read_text())
        for symbol in (LINE12E, TAXABLE, REFUND):
            self.assertNotIn(symbol, run.pubs, symbol)
        # Either alone is fine: the total with no losses, and losses with no total (case 2).
        alone = _run(_w2g([(6000.0, 1440.0)], [], assertion=20000.0), "d2.alone")
        _expect(self, alone, l12e="20000", taxable="36000", refund="1855")
        no_losses_above = _run(_w2g([(6000.0, 1440.0)], [2000.0], assertion=0.0), "d2.zero")
        _expect(self, no_losses_above, l12e="15750")

    def test_the_old_gambling_answer_no_longer_blocks_the_attachment(self) -> None:
        acts = c.declare_no_other_line16(c.add_mortgage_itemizer(c.base_return(), 20000.0))
        w2g._set_answer(acts, w2g.GAMBLING_DECLARED, "no")
        run = _run(acts, "oldno")
        self.assertTrue(run.pubs[SCHEDULE_A]["value"]["required"])
        # The new declaration is what the attachment asks: "no" holds it.
        no = c.declare_no_other_line16(c.add_mortgage_itemizer(c.base_return(), 20000.0), "no")
        held = _run(no, "newno")
        self.assertIn(("rule.attachment.schedule-a", "COMPLETENESS_VALUE_VIOLATION"), held.blocked_names())
        # And without it the attachment is incomplete rather than silently complete.
        missing = _run(c.add_mortgage_itemizer(c.base_return(), 20000.0), "newmissing")
        self.assertNotIn(SCHEDULE_A, missing.pubs)


class V66ReturnsWithoutGamblingAreUnchanged(unittest.TestCase):
    def _same(self, v66: list[dict[str, object]], v67: list[dict[str, object]], name: str) -> None:
        old, new = _run(v66, f"{name}.v66", core="v66"), _run(v67, f"{name}.v67")
        for symbol, finding in old.pubs.items():
            if symbol == SCHEDULE_A or symbol.endswith("disposition") or symbol.endswith("schedule-a-boundary.no-gambling-other"):
                continue
            self.assertIn(symbol, new.pubs, symbol)
            self.assertEqual(Decimal(str(finding["value"])) if not isinstance(finding["value"], (dict, list, str, bool)) else finding["value"],
                             Decimal(str(new.pubs[symbol]["value"])) if not isinstance(new.pubs[symbol]["value"], (dict, list, str, bool)) else new.pubs[symbol]["value"], symbol)
        self.assertEqual(old.blocked_names(), new.blocked_names())

    def test_the_base_return(self) -> None:
        self._same(c.base_return(), c.base_return(), "u.base")

    def test_a_w2g_return_once_it_confirms_no_losses(self) -> None:
        self._same(w2g._w2g_return([(6000.0, 1440.0)]), _w2g([(6000.0, 1440.0)], []), "u.w2g")

    def test_the_schedule_a_attachment_payload_of_a_return_without_gambling_is_unchanged(self) -> None:
        acts = c.add_mortgage_itemizer(c.base_return(), 20000.0)
        old = _run(acts, "u.payload.v66", core="v66")
        new = _run(c.declare_no_other_line16(acts), "u.payload.v67")
        old_value, new_value = old.pubs[SCHEDULE_A]["value"], new.pubs[SCHEDULE_A]["value"]
        self.assertEqual(old_value["itemizations"], new_value["itemizations"])
        self.assertEqual(old_value["triggers"], new_value["triggers"])
        self.assertEqual(old_value["required"], new_value["required"])
        # Only the declaration the attachment asks for differs.
        self.assertEqual(set(old_value["answers"]) - set(new_value["answers"]), {P + "schedule-a-boundary.no-gambling-other-declared"})
        self.assertEqual(set(new_value["answers"]) - set(old_value["answers"]), {c.NO_OTHER_LINE16})

    def test_a_schedule_a_itemizer_with_no_w2g(self) -> None:
        old = c.add_mortgage_itemizer(c.base_return(), 20000.0)
        self._same(old, c.declare_no_other_line16(old), "u.itemizer")


class EarlierPackagesRefuseARecordedLoss(unittest.TestCase):
    """ADR-0082: no core before v67 reads a gambling loss entry, so every one refuses a recorded loss."""

    def test_every_core_before_v67_and_a_log_with_no_adoption_refuse_a_recorded_loss(self) -> None:
        import copy
        from packages.kernel.findings import FindingModelError, project
        registry = w2g_registry()
        versions = sorted(
            int(p.name.split(".v")[-1].split(".")[0]) for p in CONTENT.glob("package.core-calculations.v*.json")
            if int(p.name.split(".v")[-1].split(".")[0]) < 67)
        self.assertIn(66, versions)
        base = _w2g([(6000.0, 1440.0)], [2000.0])
        with self.assertRaises(FindingModelError) as raised:
            project(tuple(copy.deepcopy(base)), registry)
        self.assertIn("companion presence violated", str(raised.exception))
        for number in versions:
            acts = _finish(
                copy.deepcopy(base), package_path=CONTENT / f"package.core-calculations.v{number}.json",
                package_version=f"v{number}", release_path=c.RELEASE, release_version=c.RELEASE_VERSION,
                note=f"demo.gl.sweep.v{number}")
            with self.assertRaises(FindingModelError, msg=f"v{number}") as raised:
                project(tuple(acts), registry)
            self.assertIn("companion presence violated", str(raised.exception), f"v{number}")
        # Positive control: v67 folds the same log.
        project(tuple(_finish(
            copy.deepcopy(base), package_path=c.PACKAGE, package_version="v67", release_path=c.RELEASE,
            release_version=c.RELEASE_VERSION, note="demo.gl.sweep.v67")), registry)

    def test_the_witness_is_not_a_registered_fact_type_anywhere(self) -> None:
        from packages.tax.loader import GAMBLING_LOSS_UNREAD_WITNESS
        for root in (ROOT / "packages/content", ROOT / "packages/schemas"):
            for path in root.rglob("*.json"):
                self.assertNotIn(GAMBLING_LOSS_UNREAD_WITNESS, path.read_text("utf-8"), str(path))


def w2g_registry() -> Any:
    from packages.derivation.loader import DerivationSchemas
    from packages.tax.loader import (
        install_domain_companion_equalities,
        install_domain_companion_presence,
        install_domain_declaration_signal_contradictions,
    )

    registry = DerivationSchemas().registry
    install_domain_companion_presence(registry)
    install_domain_companion_equalities(registry)
    install_domain_declaration_signal_contradictions(registry)
    return registry


class ClosureRegression(unittest.TestCase):
    def test_the_losses_collect_is_guarded_at_its_own_site_and_nothing_new_is_flagged(self) -> None:
        from tests.test_collect_closure_regression import HELD_DOWNSTREAM, _flagged
        from tools.collect_closure_survey import survey
        v66, v67 = CONTENT / "package.core-calculations.v66.json", c.PACKAGE
        guarded = {e["source_set"]: e["guard"] for e in survey(v67)["collects_guarded_at_their_own_site"]}
        self.assertEqual(guarded.get(P + "gambling.losses"), "enclosing when")
        self.assertEqual(_flagged(v67) - HELD_DOWNSTREAM, set())
        self.assertEqual(_flagged(v67), _flagged(v66))


class Packages(unittest.TestCase):
    def test_the_change_set_is_the_whole_package_delta(self) -> None:
        old = json.loads((CONTENT / "package.core-calculations.v66.json").read_text())
        new = json.loads((CONTENT / "package.core-calculations.v67.json").read_text())
        def pins(pkg: dict[str, Any]) -> set[tuple[str, str]]:
            return {(m["id"], m["version"]) for m in pkg["members"]}

        self.assertEqual(new["version"], "v67")
        self.assertEqual(pins(old) - pins(new), {
            (P + "rule.schedule-a-boundary-no-gambling-other", "v1"), (P + "rule.w2g-b1-subtotal", "v2"),
            (P + "rule.schedule-a-total", "v1"), (P + "rule.schedule-a-total-closed-empty", "v1"),
            (P + "rule.form1040-line12e", "v2"), (P + "rule.attachment.schedule-a", "v2")})
        self.assertEqual(pins(new) - pins(old), {
            (P + "gambling-losses.vocabulary", "v1"), (P + "gambling.losses", "v1"), (P + "closure-mapping.gambling-losses", "v1"),
            (P + "rule.gambling-losses-subtotal", "v1"), (P + "rule.schedule-a-line16", "v1"),
            (P + "rule.w2g-b1-subtotal", "v3"),
            (P + "rule.schedule-a-total", "v2"), (P + "rule.schedule-a-total-closed-empty", "v2"),
            (P + "rule.form1040-line12e", "v3"), (P + "rule.attachment.schedule-a", "v3")})

    def test_the_registry_only_adds(self) -> None:
        old = {(e["id"], e["version"]): e["checksum"] for e in json.loads((CONTENT / "published-packages.v64.json").read_text())["citizens"]}
        new = {(e["id"], e["version"]): e["checksum"] for e in json.loads((CONTENT / "published-packages.v65.json").read_text())["citizens"]}
        self.assertTrue(set(old) <= set(new))
        self.assertTrue(all(new[k] == v for k, v in old.items()))
        self.assertEqual(len(set(new) - set(old)), 10)

    def test_the_companion_declaration_for_v67_matches_v66(self) -> None:
        declarations = domain_package_companion_declarations()
        key = "tax.us.2025.package.core-calculations"
        self.assertEqual(declarations[(key, "v67")]["presence_pairs"], {**declarations[(key, "v66")]["presence_pairs"], P + "gambling.loss": None})

    def test_published_files_are_untouched(self) -> None:
        # Successors are new files; the predecessors named in the change set keep their versions.
        for name in ("rule.w2g-b1-subtotal.v2.json", "rule.schedule-a-total.json", "rule.schedule-a-total-closed-empty.json",
                     "rule.form1040-line12e.v2.json", "attachment.schedule-a.v2.json", "rule.schedule-a-boundary-no-gambling-other.json"):
            self.assertTrue((CONTENT / name).is_file(), name)

    def test_the_release_change_set_is_the_committed_one(self) -> None:
        change = json.loads((EVIDENCE / "v66-to-v67.json").read_text())
        self.assertEqual((change["package_version"], change["release_version"]), ("v67", "v65"))


if __name__ == "__main__":
    unittest.main()
