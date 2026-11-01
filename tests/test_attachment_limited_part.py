"""Schedule A shows gambling losses: attachment-rule.v12 and core v70 (attachment-limited-part).

Every run goes through ``live_coordinate_run`` on the committed packages: core v69 (registry v67,
release v67) against core v70 (registry v68, release v68). The hand values are P0's
(``attachment-limited-part-evidence/p0-design.md``, section 4), which in turn are #245's. The guards
that cannot be reached by a consistent return (an omitted part whose line is nonzero; a limited line
that is not the lesser of the rows and the limit; an unreadable condition) run the real Schedule A v4
citizen through ``_Run.attempt_attachment`` on a hand-built run. Synthetic ``demo.*`` data only.
"""

from __future__ import annotations

import copy
import hashlib
import json
import re
import unittest
from decimal import Decimal
from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace
from typing import Any, cast

from packages.derivation.live import live_coordinate_run
from packages.derivation.live_session import _render_page
from packages.derivation.live_workspace import WorkspaceCapability
from packages.derivation.production_resolver import PublicationSurface
from packages.derivation.runner import ITEMIZATION_TIE_OUT_VIOLATION, _Run
from packages.kernel.findings import FindingModelError
from packages.tax.loader import domain_package_companion_declarations
from tests import test_collect_closure as cc
from tests.test_collect_closure import _adopt
from tests.test_form_1099_withholding import _assert
from tests import test_w2g_gambling as w2g
from tests.helpers import current_core_returns as c
from tests.test_form_1099_k_income import _handover
from tests.test_refund_or_amount_owed_track1 import _finish
from tests.test_withholding_closure import _strip_closure

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "packages/content/tax/2025"
RELEASE_DIR = c.RELEASE_DIR
SCHEMAS = ROOT / "packages/schemas"
P = c.P

CORES = {
    "v69": (CONTENT / "package.core-calculations.v69.json", "v69", RELEASE_DIR / "demo.release.sli-worksheet-integration.2025.v67.json", "v67", CONTENT / "published-packages.v67.json"),
    "v70": (CONTENT / "package.core-calculations.v70.json", "v70", RELEASE_DIR / "demo.release.sli-worksheet-integration.2025.v68.json", "v68", CONTENT / "published-packages.v68.json"),
}

SCHEDULE_A = P + "scheduleA.disposition"
LINE8A, LINE16, TOTAL, LINE12E = (P + "schedule-a.line8a", P + "schedule-a.line16", P + "schedule-a.total", P + "deductions.line-12e")
WINNINGS = P + "gambling.b1-winnings-subtotal"
LOSSES = P + "gambling.losses-subtotal"
PART_8A, PART_16 = "line-8a-home-mortgage-interest", "line-16-gambling-losses"
OTHER_ATTACHMENTS = {
    "schedule-1": P + "schedule1.disposition",
    "schedule-b": P + "scheduleb.disposition",
    "schedule-d": P + "schedule-d.disposition",
    "form-8949": P + "form8949.disposition",
}


class Run:
    def __init__(self, pubs: dict[str, dict[str, Any]], dispositions: list[dict[str, Any]], model: dict[str, Any], page: bytes) -> None:
        self.pubs, self.dispositions, self.model, self.page = pubs, dispositions, model, page

    def value(self, symbol: str) -> Decimal:
        return Decimal(str(self.pubs[symbol]["value"]))

    def blocked(self) -> set[tuple[str, str]]:
        return {(str(r["artifact_id"]).replace(P, ""), str(r.get("code"))) for r in self.dispositions if r.get("disposition") == "blocked"}

    def disposition(self, rule_id: str) -> dict[str, Any]:
        return next(r for r in self.dispositions if r.get("artifact_id") == P + rule_id)

    def parts(self) -> dict[str, dict[str, Any]]:
        return {p["part_id"]: p for p in self.pubs[SCHEDULE_A]["value"]["itemizations"]}

    def page_parts(self) -> list[dict[str, Any]]:
        group = next((g for g in self.model["citationGroups"] if g["id"] == P + "rule.attachment.schedule-a"), None)
        return [] if group is None else list(group["parts"])


def run(acts: list[dict[str, object]], name: str, core: str) -> Run:
    package, version, release, rel_version, registry = CORES[core]
    surface = PublicationSurface(RELEASE_DIR, registry, CONTENT)
    for _ in range(5):
        try:
            finished = _handover(
                _finish(copy.deepcopy(acts), package_path=package, package_version=version, release_path=release,
                        release_version=rel_version, note=name),
                surface=surface, reconfirm=True)
            with TemporaryDirectory() as tmp:
                outcome = live_coordinate_run(
                    WorkspaceCapability(Path(tmp) / "L"), repo_root=ROOT, authoritative_acts=finished,
                    workspace_revision=len(finished), run_scope={"jurisdiction": "us", "year": "2025"},
                    scope_user=c.USER, request={"schema": "run-request.v1"}, run_id=name, governance_pins=[],
                    surface=surface, output_name="out.json")
                if outcome.refusal is not None:
                    raise AssertionError(f"{name} refused: {outcome.refusal.reason} {outcome.refusal.detail}")
                pubs = {str(p.finding["symbol"]): p.finding for p in outcome.publications or ()}
                assert outcome.output_path is not None and outcome.presentation_path is not None
                report = json.loads(outcome.output_path.read_text(encoding="utf-8"))
                model = json.loads(outcome.presentation_path.read_text(encoding="utf-8"))
                page = _render_page(ROOT, WorkspaceCapability(Path(tmp) / "L"), outcome.presentation_path)
            return Run(pubs, list(report.get("dispositions", [])), model, page)
        except FindingModelError as exc:
            found = re.search(r"contradiction: (\S+) is currently", str(exc))
            if not found:
                raise
            acts = _strip_closure(acts, found.group(1))
    raise AssertionError("too many declaration withdrawals")


def w2g_return(winnings: float = 6000.0, withheld: float = 1440.0) -> list[dict[str, object]]:
    return w2g._w2g_return([(winnings, withheld)])


def itemizer(losses: list[float], *, mortgage: float | None = 20000.0, winnings: float = 6000.0,
             withheld: float = 1440.0) -> list[dict[str, object]]:
    acts = w2g_return(winnings, withheld)
    if mortgage is not None:
        acts = c.add_mortgage_itemizer(acts, mortgage)
    return c.declare_no_other_line16(c.add_gambling_losses(acts, losses))


def dec(text: Any) -> Decimal:
    return Decimal(str(text))


class HandValues(unittest.TestCase):
    """P0 section 4, on core v70, beside what core v69 does."""

    def test_case_1_mortgage_and_losses_show_both_parts(self) -> None:
        acts = itemizer([2000.0])
        new, old = run(acts, "demo.alp.c1.v70", "v70"), run(acts, "demo.alp.c1.v69", "v69")
        self.assertEqual(new.blocked(), set())
        self.assertEqual(list(new.parts()), [PART_8A, PART_16])
        value = new.pubs[SCHEDULE_A]["value"]
        self.assertEqual(value["omitted_parts"], [])
        self.assertEqual(dec(new.parts()[PART_8A]["tie_out"]["line_value"]), 20000)
        sixteen = new.parts()[PART_16]
        self.assertEqual((dec(sixteen["part_sum"]), dec(sixteen["limited_to"]["value"]), dec(sixteen["tie_out"]["line_value"]), dec(sixteen["not_counted"])),
                         (2000, 6000, 2000, 0))
        self.assertEqual(sixteen["limited_to"]["symbol"], WINNINGS)
        self.assertEqual(sum(dec(p["tie_out"]["line_value"]) for p in new.parts().values()), 22000)
        self.assertEqual((new.value(TOTAL), new.value(LINE12E)), (22000, 22000))
        # v69 lists only line 8a for the same return and the same figures.
        self.assertEqual(list(old.parts()), [PART_8A])
        self.assertEqual(old.value(LINE12E), 22000)

    def test_case_2_losses_only_publishes_where_v69_blocks(self) -> None:
        acts = itemizer([20000.0], mortgage=None, winnings=20000.0, withheld=4800.0)
        old = run(acts, "demo.alp.c2.v69", "v69")
        self.assertEqual(old.blocked(), {("rule.attachment.schedule-a", "DEPENDENCY_ABSENT")})
        self.assertEqual(old.disposition("rule.attachment.schedule-a")["missing"], [LINE8A])
        new = run(acts, "demo.alp.c2.v70", "v70")
        self.assertEqual(new.blocked(), set())
        self.assertEqual(list(new.parts()), [PART_16])
        self.assertEqual(new.pubs[SCHEDULE_A]["value"]["omitted_parts"], [{"part_id": PART_8A, "reason": "family_empty"}])
        sixteen = new.parts()[PART_16]
        self.assertEqual((dec(sixteen["part_sum"]), dec(sixteen["limited_to"]["value"]), dec(sixteen["tie_out"]["line_value"]), dec(sixteen["not_counted"])),
                         (20000, 20000, 20000, 0))
        self.assertEqual((new.value(TOTAL), new.value(LINE12E)), (20000, 20000))
        # Every figure is the one v69 already published.
        for symbol in (TOTAL, LINE12E, LINE16, P + "income.taxable-income", P + "payments.line35a-refunded"):
            self.assertEqual(new.value(symbol), old.value(symbol), symbol)

    def test_case_3_no_losses_is_the_v69_itemization(self) -> None:
        acts = itemizer([])
        new, old = run(acts, "demo.alp.c3.v70", "v70"), run(acts, "demo.alp.c3.v69", "v69")
        self.assertEqual(list(new.parts()), [PART_8A])
        self.assertEqual(new.pubs[SCHEDULE_A]["value"]["omitted_parts"], [{"part_id": PART_16, "reason": "line_is_zero"}])
        old_value, new_value = old.pubs[SCHEDULE_A]["value"], new.pubs[SCHEDULE_A]["value"]
        for key in ("itemizations", "triggers", "required", "answers", "named_obligations"):
            self.assertEqual(new_value[key], old_value[key], key)
        self.assertEqual(set(new_value) - set(old_value), {"omitted_parts"})
        self.assertEqual(new.value(LINE12E), 20000)

    def test_case_4_losses_above_winnings_are_limited(self) -> None:
        for losses in ([9000.0], [4000.0, 5000.0]):
            with self.subTest(losses=losses):
                new = run(itemizer(losses), f"demo.alp.c4.{len(losses)}.v70", "v70")
                self.assertEqual(new.blocked(), set())
                sixteen = new.parts()[PART_16]
                self.assertEqual(dec(sixteen["row_sets"][0]["row_sum"]), 9000)
                self.assertEqual(len(sixteen["row_sets"][0]["rows"]), len(losses))
                self.assertEqual((dec(sixteen["part_sum"]), dec(sixteen["limited_to"]["value"]), dec(sixteen["tie_out"]["line_value"]), dec(sixteen["not_counted"])),
                                 (9000, 6000, 6000, 3000))
                self.assertEqual(sum(dec(p["tie_out"]["line_value"]) for p in new.parts().values()), 26000)
                self.assertEqual((new.value(TOTAL), new.value(LINE12E), new.value(LINE16)), (26000, 26000, 6000))

    def test_case_4b_losses_equal_to_winnings(self) -> None:
        new = run(itemizer([6000.0]), "demo.alp.c4b.v70", "v70")
        sixteen = new.parts()[PART_16]
        self.assertEqual((dec(sixteen["tie_out"]["line_value"]), dec(sixteen["not_counted"])), (6000, 0))

    def test_case_5_standard_deduction_has_no_schedule_a(self) -> None:
        acts = c.add_gambling_losses(w2g_return(), [2000.0])
        new, old = run(acts, "demo.alp.c5.v70", "v70"), run(acts, "demo.alp.c5.v69", "v69")
        for r in (old, new):
            self.assertNotIn(SCHEDULE_A, r.pubs)
            self.assertEqual(r.disposition("rule.attachment.schedule-a")["disposition"], "inapplicable")
            self.assertEqual(r.value(LINE12E), 15750)
        self.assertEqual(new.disposition("rule.attachment.schedule-a")["guard_result"], False)

    def test_losses_with_no_winnings_leave_the_line_16_part_out(self) -> None:
        acts = c.declare_no_other_line16(c.add_gambling_losses(c.add_mortgage_itemizer(c.base_return(), 20000.0), [2000.0]))
        new = run(acts, "demo.alp.nowin.v70", "v70")
        self.assertEqual(list(new.parts()), [PART_8A])
        self.assertEqual(new.pubs[SCHEDULE_A]["value"]["omitted_parts"], [{"part_id": PART_16, "reason": "line_is_zero"}])
        self.assertEqual(new.value(LINE16), 0)

    def test_the_limited_part_pins_the_winnings_subtotal(self) -> None:
        new = run(itemizer([9000.0]), "demo.alp.pin.v70", "v70")
        pin_ids = {pin["id"] for pin in new.pubs[SCHEDULE_A]["pins"]}
        self.assertIn(new.pubs[WINNINGS]["id"], pin_ids)
        self.assertIn(new.pubs[LINE16]["id"], pin_ids)


class OtherAttachmentsAreUnchanged(unittest.TestCase):
    """Each of the four other attachments publishes the same payload on core v69 and core v70."""

    def _same(self, acts: list[dict[str, object]], name: str, attachment: str) -> None:
        old, new = run(acts, f"demo.alp.{name}.v69", "v69"), run(acts, f"demo.alp.{name}.v70", "v70")
        symbol = OTHER_ATTACHMENTS[attachment]
        self.assertEqual(old.blocked(), new.blocked(), name)
        old_row = old.disposition(f"rule.attachment.{attachment if attachment != 'form-8949' else 'f8949'}")
        new_row = new.disposition(f"rule.attachment.{attachment if attachment != 'form-8949' else 'f8949'}")
        self.assertEqual(old_row["disposition"], new_row["disposition"], name)
        self.assertEqual(old_row.get("code"), new_row.get("code"), name)
        self.assertEqual(symbol in old.pubs, symbol in new.pubs, name)
        if symbol in old.pubs:
            self.assertEqual(new.pubs[symbol]["value"], old.pubs[symbol]["value"], name)
            skip = {"adoption", "package"}

            def keep(r: Run) -> list[tuple[str, str, str]]:
                return sorted((p["role"], p["id"], p["version"]) for p in r.pubs[symbol]["pins"]
                              if p["role"] not in skip and not p["id"].startswith("finding:derived:"))

            self.assertEqual(keep(new), keep(old), name)

    def test_schedule_1_publishes_the_same_payload(self) -> None:
        acts = w2g_return()
        self._same(acts, "s1", "schedule-1")
        self.assertIn(OTHER_ATTACHMENTS["schedule-1"], run(acts, "demo.alp.s1.check", "v70").pubs)

    def test_schedule_b_publishes_the_same_payload(self) -> None:
        acts = w2g._w2g_return([])
        for i, amount in enumerate([1000.0, 800.0]):
            acts = cc._add_member(acts, P + "f1099int.b1", amount, close=i == 1, tag=f"ib{i}")
        self._same(acts, "sb", "schedule-b")
        self.assertIn(OTHER_ATTACHMENTS["schedule-b"], run(acts, "demo.alp.sb.check", "v70").pubs)

    def test_schedule_d_is_the_same(self) -> None:
        acts = cc._add_member(w2g._w2g_return([]), P + "f1099b.covered-st-proceeds", 1000.0, close=True, tag="trig")
        for i, amount in enumerate([100.0, 200.0]):
            acts = cc._add_member(acts, P + "f1099div.2a", amount, close=i == 1, tag=f"d{i}")
        self._same(acts, "sd", "schedule-d")
        checked = run(acts, "demo.alp.sd.check", "v70")
        self.assertEqual(checked.disposition("rule.attachment.schedule-d")["disposition"], "published")

    def test_form_8949_is_the_same(self) -> None:
        # Covered, wash-sale-adjusted short- and long-term sales (proceeds, basis, adjustment) and the Part III answer.
        acts = w2g._w2g_return([])
        boundary = P + "schedule-d-boundary.no-other-form8949-adjustments"
        _adopt(acts, boundary)
        _assert(acts, "demo.alp.boundary.8949", boundary, (), "yes")
        for term in ("st", "lt"):
            for kind, amount in (("proceeds", 1000.0), ("basis", 1000.0), ("adjustment", 50.0)):
                acts = cc._add_member(acts, P + f"f1099b.covered-w-{term}-{kind}", amount, close=True, tag=f"w{term}{kind[:2]}")
        self._same(acts, "f8949", "form-8949")
        checked = run(acts, "demo.alp.f8949.check", "v70")
        self.assertEqual(checked.disposition("rule.attachment.f8949")["disposition"], "published")

    def test_a_return_using_schedule_a_and_schedule_1_changes_only_schedule_a(self) -> None:
        acts = itemizer([2000.0])
        old, new = run(acts, "demo.alp.both.v69", "v69"), run(acts, "demo.alp.both.v70", "v70")
        symbol = OTHER_ATTACHMENTS["schedule-1"]
        self.assertEqual(new.pubs[symbol]["value"], old.pubs[symbol]["value"])


class ThePage(unittest.TestCase):
    def test_the_limited_part_reads_as_one_sentence_and_an_omitted_part_is_absent(self) -> None:
        both = run(itemizer([9000.0]), "demo.alp.page1.v70", "v70")
        parts = {p["heading"]: p for p in both.page_parts()}
        sixteen = next(p for h, p in parts.items() if h.startswith("Line 16"))
        self.assertEqual(sixteen["tieOutText"], "Recorded: 9000. Limited to gambling winnings of 6000. On this line: 6000. Not counted: 3000.")
        self.assertEqual(len(sixteen["citationSites"]), 1)
        eight = next(p for h, p in parts.items() if h.startswith("Line 8a"))
        self.assertEqual(eight["tieOutText"], "Reported subtotal: 20000")
        self.assertIn(b"Limited to gambling winnings of 6000", both.page)

        only_16 = run(itemizer([20000.0], mortgage=None, winnings=20000.0, withheld=4800.0), "demo.alp.page2.v70", "v70")
        self.assertEqual([p["heading"][:7] for p in only_16.page_parts()], ["Line 16"])
        no_losses = run(itemizer([]), "demo.alp.page3.v70", "v70")
        self.assertEqual([p["heading"][:7] for p in no_losses.page_parts()], ["Line 8a"])
        self.assertEqual(no_losses.page_parts()[0]["tieOutText"], "Reported subtotal: 20000")


# --- the guards, on the real Schedule A v4 citizen --------------------------------------------


class _Schemas:
    def validate_declared(self, _finding: dict[str, Any]) -> None:
        return None


FAMILY_8A, FAMILY_16 = P + "f1098", P + "gambling.losses"
BOX1, LOSS = P + "f1098.box1-mortgage-interest", P + "gambling.loss"


def _rule() -> dict[str, Any]:
    return cast(dict[str, Any], json.loads((CONTENT / "attachment.schedule-a.v4.json").read_text("utf-8")))


def _fake_run(*, line8a: str | None, line16: str | None, mortgage: list[str], losses: list[str], losses_subtotal: str = "0",
              winnings: str | None = "6000", admitted: tuple[str, ...] = (FAMILY_8A, FAMILY_16)) -> _Run:
    rule = _rule()
    run_: Any = object.__new__(_Run)
    run_.ctx = SimpleNamespace(
        run_id="demo.run.alp", adoption_pin={"role": "adoption", "id": "demo.package", "version": "v1"}, governance_pins=[],
        parameters={P + "parameter.default-zero": {"values": "0"}},
        family_declarations=[{"id": FAMILY_8A, "member_predicate": {"fact_type": BOX1}}, {"id": FAMILY_16, "member_predicate": {"fact_type": LOSS}}],
    )
    run_.schemas = _Schemas()
    run_.use_v2 = True
    symbols = {P + "schedule-a.excess-over-standard": "100"}
    for answer in rule["completeness"]["required_answers"]:
        symbols[answer["symbol"]] = answer["equals"]
    for name, value in ((LINE8A, line8a), (LINE16, line16), (LOSSES, losses_subtotal if losses else None), (WINNINGS, winnings)):
        if value is not None:
            symbols[name] = value
    if losses or line16 is not None:
        symbols.setdefault(LOSSES, losses_subtotal)
    run_.symbols = symbols
    run_.symbol_pin = {name: (f"finding:{name}", "v1", "input", "assertion") for name in symbols}
    run_.sources = {BOX1: list(mortgage), LOSS: list(losses)}
    run_.source_fids = {BOX1: [f"demo.m.{i}" for i in range(len(mortgage))], LOSS: [f"demo.l.{i}" for i in range(len(losses))]}
    run_.source_finding_versions = {fid: "v1" for ids in run_.source_fids.values() for fid in ids}
    run_.admissions = {family: SimpleNamespace() for family in admitted}
    run_.publications, run_.dispositions, run_.blocked, run_.resolved = [], [], [], set()
    run_.symbol_publisher, run_.live_sources = {}, []
    return cast(_Run, run_)


def _published(run_: _Run) -> dict[str, Any]:
    return cast(dict[str, Any], next(p for p in run_.publications if p.finding["symbol"] == SCHEDULE_A).finding["value"])


class Guards(unittest.TestCase):
    def test_consistent_inputs_publish(self) -> None:
        r = _fake_run(line8a="500", line16="6000", mortgage=["500"], losses=["9000"], losses_subtotal="9000")
        self.assertEqual(r.attempt_attachment(_rule()), "published")
        value = _published(r)
        self.assertEqual([p["part_id"] for p in value["itemizations"]], [PART_8A, PART_16])
        self.assertEqual(dec(value["itemizations"][1]["not_counted"]), 3000)

    def test_an_omitted_part_whose_line_is_nonzero_is_a_tie_out_violation(self) -> None:
        # No Form 1098 statement is recorded, yet line 8a is published nonzero: omission would lose a figure.
        r = _fake_run(line8a="500", line16="0", mortgage=[], losses=[])
        self.assertEqual(r.attempt_attachment(_rule()), "blocked")
        row = r.dispositions[-1]
        self.assertEqual(row["code"], ITEMIZATION_TIE_OUT_VIOLATION)
        self.assertEqual(row["missing"], [f"{PART_8A}:omitted_but_line_present"])

    def test_a_limited_line_that_is_not_the_lesser_of_rows_and_limit_is_a_violation(self) -> None:
        for line16 in ("5000", "9000", "6000.01"):
            with self.subTest(line16=line16):
                r = _fake_run(line8a=None, line16=line16, mortgage=[], losses=["9000"], losses_subtotal="9000")
                self.assertEqual(r.attempt_attachment(_rule()), "blocked")
                self.assertEqual(r.dispositions[-1]["code"], ITEMIZATION_TIE_OUT_VIOLATION)
                self.assertEqual(r.dispositions[-1]["missing"], [f"{PART_16}:{LINE16}"])
        ok = _fake_run(line8a=None, line16="6000", mortgage=[], losses=["9000"], losses_subtotal="9000")
        self.assertEqual(ok.attempt_attachment(_rule()), "published")

    def test_rows_that_do_not_sum_to_their_subtotal_are_still_a_violation(self) -> None:
        r = _fake_run(line8a=None, line16="6000", mortgage=[], losses=["9000"], losses_subtotal="9500")
        self.assertEqual(r.attempt_attachment(_rule()), "blocked")
        self.assertEqual(r.dispositions[-1]["code"], ITEMIZATION_TIE_OUT_VIOLATION)

    def test_an_unreadable_condition_blocks_and_is_never_read_as_omission(self) -> None:
        r = _fake_run(line8a=None, line16=None, mortgage=[], losses=[], winnings=None)
        self.assertEqual(r.attempt_attachment(_rule()), "blocked")
        self.assertEqual((r.dispositions[-1]["code"], r.dispositions[-1]["missing"]), ("DEPENDENCY_ABSENT", [LINE16]))
        r2 = _fake_run(line8a=None, line16="0", mortgage=[], losses=[], admitted=(FAMILY_16,))
        self.assertEqual(r2.attempt_attachment(_rule()), "blocked")
        self.assertEqual((r2.dispositions[-1]["code"], r2.dispositions[-1]["missing"]), ("DEPENDENCY_ABSENT", [FAMILY_8A]))

    def test_a_v4_labelled_attachment_does_not_require_a_limit_symbol(self) -> None:
        rule = _rule()
        rule["schema"] = "attachment-rule.v4"
        # Winnings are not published; v4 ignores limited_to, so the part ties exactly to its rows (2,000).
        r = _fake_run(line8a="500", line16="2000", mortgage=["500"], losses=["2000"], losses_subtotal="2000", winnings=None)
        self.assertEqual(r.attempt_attachment(rule), "published")
        value = _published(r)
        self.assertEqual([p["part_id"] for p in value["itemizations"]], [PART_8A, PART_16])
        self.assertNotIn("limited_to", value["itemizations"][1])
        self.assertNotIn(WINNINGS, {pin["id"] for pin in r.publications[-1].finding["pins"]})
        # The same inputs under v12 are unreadable without the limit.
        v12 = _fake_run(line8a="500", line16="2000", mortgage=["500"], losses=["2000"], losses_subtotal="2000", winnings=None)
        self.assertEqual(v12.attempt_attachment(_rule()), "blocked")
        self.assertEqual(v12.dispositions[-1]["missing"], [WINNINGS])

    def test_the_scheduling_gate_waits_only_for_what_applies(self) -> None:
        rule = _rule()
        none_yet = _fake_run(line8a=None, line16=None, mortgage=[], losses=[], winnings=None)
        self.assertEqual(none_yet._requires(rule), sorted({P + "schedule-a.excess-over-standard", LINE16}))
        zero = _fake_run(line8a=None, line16="0", mortgage=[], losses=[])
        self.assertEqual(zero._requires(rule), [P + "schedule-a.excess-over-standard"])
        both = _fake_run(line8a="1", line16="2", mortgage=["1"], losses=["2"], losses_subtotal="2")
        self.assertEqual(set(both._requires(rule)), {P + "schedule-a.excess-over-standard", LINE8A, LINE16, LOSSES, WINNINGS})


def _load(path: Path) -> Any:
    return json.loads(path.read_text("utf-8"))


# --- the validator's v12 checks, on the real core v70 Schedule A citizen ----------------------


def _v70_issue_codes(mutate: Any = None) -> set[str]:
    from packages.derivation.loader import DerivationSchemas
    from packages.derivation.package_validation import validate_package

    package = _load(CORES["v70"][0])
    members: dict[tuple[str, str], dict[str, Any]] = {}
    for pin in package["members"]:
        members[(pin["id"], pin["version"])] = _load(CONTENT / _FILES[(pin["id"], pin["version"])])
    if mutate is not None:
        mutate(members[("tax.us.2025.rule.attachment.schedule-a", "v4")])
    result = validate_package(copy.deepcopy(package), members, DerivationSchemas(), None)
    return {issue.code for issue in result.issues}


def _index_files() -> dict[tuple[str, str], str]:
    found: dict[tuple[str, str], str] = {}
    for path in CONTENT.glob("*.json"):
        body = _load(path)
        if isinstance(body, dict) and isinstance(body.get("id"), str) and isinstance(body.get("version"), str) and "citizens" not in body:
            found[(body["id"], body["version"])] = path.name
    return found


_FILES = _index_files()


def _sixteen(citizen: dict[str, Any]) -> dict[str, Any]:
    return cast(dict[str, Any], next(p for p in citizen["itemizations"] if p["part_id"] == PART_16))


class ValidatorChecks(unittest.TestCase):
    def test_the_committed_core_v70_has_no_issues(self) -> None:
        self.assertEqual(_v70_issue_codes(), set())

    def test_a_nonexistent_limit_symbol_is_refused(self) -> None:
        def mutate(citizen: dict[str, Any]) -> None:
            _sixteen(citizen)["tie_out"]["limited_to"]["symbol"] = "demo.no-such-symbol"
        self.assertIn("ATTACHMENT_LIMIT_SYMBOL_ABSENT", _v70_issue_codes(mutate))

    def test_a_limit_equal_to_the_line_is_refused(self) -> None:
        def mutate(citizen: dict[str, Any]) -> None:
            part = _sixteen(citizen)
            part["tie_out"]["limited_to"]["symbol"] = part["tie_out"]["line_symbol"]
        self.assertIn("ATTACHMENT_LIMIT_SYMBOL_ABSENT", _v70_issue_codes(mutate))

    def test_line_nonzero_on_an_unpublished_line_is_refused(self) -> None:
        def mutate(citizen: dict[str, Any]) -> None:
            part = _sixteen(citizen)
            part["tie_out"]["line_symbol"] = "demo.unpublished-line"
            del part["tie_out"]["limited_to"]
        self.assertIn("ATTACHMENT_LINE_AUTHORITY_MISMATCH", _v70_issue_codes(mutate))

    def test_dropping_limited_to_leaves_a_line_that_is_not_the_family_subtotal(self) -> None:
        def mutate(citizen: dict[str, Any]) -> None:
            del _sixteen(citizen)["tie_out"]["limited_to"]
        self.assertIn("ATTACHMENT_LINE_AUTHORITY_MISMATCH", _v70_issue_codes(mutate))


# --- schema, registry and package deltas ------------------------------------------------------


class Deltas(unittest.TestCase):
    def test_v12_is_v4_plus_the_two_optional_fields(self) -> None:
        v4 = _load(SCHEMAS / "tax/attachment-rule.v4.schema.json")
        v12 = _load(SCHEMAS / "tax/attachment-rule.v12.schema.json")
        self.assertEqual(v12["$id"], "tax/attachment-rule.v12")
        self.assertEqual(v12["properties"]["schema"]["const"], "attachment-rule.v12")
        part4, part12 = v4["properties"]["itemizations"]["items"], v12["properties"]["itemizations"]["items"]
        self.assertEqual(set(part12["properties"]) - set(part4["properties"]), {"applies_when"})
        self.assertEqual(part12["required"], part4["required"])
        self.assertEqual(part12["properties"]["applies_when"], {"enum": ["always", "line_nonzero", "family_nonempty"]})
        tie4, tie12 = part4["properties"]["tie_out"], part12["properties"]["tie_out"]
        self.assertEqual(set(tie12["properties"]) - set(tie4["properties"]), {"limited_to"})
        self.assertEqual(tie12["required"], tie4["required"])
        self.assertIs(tie12["additionalProperties"], False)
        self.assertIs(part12["additionalProperties"], False)
        self.assertIs(tie4["additionalProperties"], False)  # so v4..v11 cannot carry the new keys
        for key in ("$defs", "required", "type", "additionalProperties"):
            self.assertEqual(v12[key], v4[key], key)
        for key in set(v4["properties"]) - {"schema", "itemizations"}:
            self.assertEqual(v12["properties"][key], v4["properties"][key], key)

    def test_the_new_files_are_published_by_checksum_and_the_manifests_list_every_schema(self) -> None:
        for directory, added in (("tax", "attachment-rule.v12.schema.json"), ("derivation", "artifact-package.v38.schema.json")):
            manifest = _load(SCHEMAS / directory / "published.json")
            path = SCHEMAS / directory / added
            self.assertEqual(manifest[added], hashlib.sha256(path.read_bytes()).hexdigest())
            self.assertEqual(set(manifest), {p.name for p in (SCHEMAS / directory).glob("*.schema.json")})

    def test_package_v38_is_v37_plus_v12_only(self) -> None:
        v37 = _load(SCHEMAS / "derivation/artifact-package.v37.schema.json")
        v38 = _load(SCHEMAS / "derivation/artifact-package.v38.schema.json")
        text37 = json.dumps(v37, sort_keys=True).replace("artifact-package.v37", "artifact-package.v38")
        text38 = json.dumps(v38, sort_keys=True).replace('"attachment-rule.v11", "attachment-rule.v12"', '"attachment-rule.v11"')
        self.assertEqual(text37, text38)

    def test_the_core_v70_package_differs_from_v69_in_schedule_a_and_v12_admission_only(self) -> None:
        v69, v70 = _load(CORES["v69"][0]), _load(CORES["v70"][0])

        def key(m: dict[str, Any]) -> tuple[str, str]:
            return (m["id"], m["version"])

        gone, new = {key(m) for m in v69["members"]} - {key(m) for m in v70["members"]}, {key(m) for m in v70["members"]} - {key(m) for m in v69["members"]}
        self.assertEqual(gone, {("tax.us.2025.rule.attachment.schedule-a", "v3")})
        self.assertEqual(new, {("tax.us.2025.rule.attachment.schedule-a", "v4")})
        self.assertEqual({key(e) for e in v69["entrypoints"]} - {key(e) for e in v70["entrypoints"]}, gone)
        self.assertEqual({key(e) for e in v70["entrypoints"]} - {key(e) for e in v69["entrypoints"]}, new)
        self.assertEqual(set(v70["admitted_schemas"]) - set(v69["admitted_schemas"]), {"attachment-rule.v12"})
        self.assertEqual(set(v69["admitted_schemas"]) - set(v70["admitted_schemas"]), set())
        self.assertEqual((v69["schema"], v70["schema"]), ("artifact-package.v37", "artifact-package.v38"))
        # The other attachments keep their exact pins (id, version and schema).

        def others(p: dict[str, Any]) -> list[tuple[str, str, str]]:
            return sorted((m["id"], m["version"], m["schema"]) for m in p["members"] if m["role"] == "attachment-rule" and "schedule-a" not in m["id"])

        self.assertEqual(others(v70), others(v69))
        self.assertEqual(len(others(v70)), 4)
        self.assertEqual({k: v for k, v in v70.items() if k not in ("members", "entrypoints", "admitted_schemas", "schema", "version", "package_checksum")},
                         {k: v for k, v in v69.items() if k not in ("members", "entrypoints", "admitted_schemas", "schema", "version", "package_checksum")})

    def test_registry_v68_only_adds_to_v67_and_release_v68_pins_it(self) -> None:
        old, new = _load(CORES["v69"][4]), _load(CORES["v70"][4])
        for field in ("citizens", "packages"):
            before = {(e["id"], e["version"]): e["checksum"] for e in old[field]}
            after = {(e["id"], e["version"]): e["checksum"] for e in new[field]}
            self.assertTrue(before.items() <= after.items(), field)
        self.assertEqual({(e["id"], e["version"]) for e in new["citizens"]} - {(e["id"], e["version"]) for e in old["citizens"]},
                         {("tax.us.2025.rule.attachment.schedule-a", "v4")})
        self.assertEqual({(e["id"], e["version"]) for e in new["packages"]} - {(e["id"], e["version"]) for e in old["packages"]},
                         {("tax.us.2025.package.core-calculations", "v70")})
        release = _load(CORES["v70"][2])
        self.assertEqual(release["version"], "v68")
        self.assertEqual(release["package_registry_sha256"], hashlib.sha256(CORES["v70"][4].read_bytes()).hexdigest())
        declarations = domain_package_companion_declarations()
        core = "tax.us.2025.package.core-calculations"
        self.assertEqual(declarations[(core, "v70")], declarations[(core, "v69")])

    def test_schedule_a_v4_keeps_v3_requirement_and_completeness(self) -> None:
        v3, v4 = _load(CONTENT / "attachment.schedule-a.v3.json"), _rule()
        for key in ("requirement", "completeness", "publishes", "attachment", "scope", "id"):
            self.assertEqual(v4[key], v3[key], key)
        self.assertEqual(v4["itemizations"][0]["row_sets"], v3["itemizations"][0]["row_sets"])
        self.assertEqual(v4["itemizations"][0]["tie_out"], v3["itemizations"][0]["tie_out"])
        self.assertEqual((v4["schema"], v4["version"]), ("attachment-rule.v12", "v4"))


if __name__ == "__main__":
    unittest.main()
