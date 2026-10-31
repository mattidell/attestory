"""Itemization with cents (2025): core v66 rounds each line once, at its total.

Every run goes through ``live_coordinate_run`` on the committed packages: core v65 /
registry v63 / release v63 (the cents tie-out block, pinned) against the successor core v66 /
registry v64 / release v64. A statement is recorded the way a filer does: by member-transition
into its family, with the family's closure attested at the horizon that results.

The hand values are those of the milestone's P0 (section 5 of
``itemization-cents-evidence/p0-trace-and-design.md``), computed from the 2025 Tax Table before
the engine ran. Synthetic ``demo.*`` data only.
"""

from __future__ import annotations

import copy
import hashlib
import json
import re
from dataclasses import dataclass, field
from decimal import Decimal
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any
import unittest

from packages.derivation.live import live_coordinate_run
from packages.derivation.live_workspace import WorkspaceCapability
from packages.derivation.production_resolver import PublicationSurface
from packages.derivation.runner import ITEMIZATION_TIE_OUT_VIOLATION
from packages.kernel.findings import FindingModelError
from tests import test_collect_closure as cc
from tests import test_w2g_gambling as w2g
from tests.test_attachment_closure import _add_member_with_companion
from tests.test_form_1099_k_income import _handover
from tests.test_refund_or_amount_owed_track1 import _finish
from tests.helpers import current_core_returns as ccr
from tests.test_withholding_closure import _strip_closure

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "packages/content/tax/2025"
RELEASE_DIR = ROOT / "packages/sample_data/student_loan_worksheet_integration/publication_surface/releases"

PACKAGE_V65 = CONTENT / "package.core-calculations.v65.json"
RELEASE_V63 = RELEASE_DIR / "demo.release.sli-worksheet-integration.2025.v63.json"
SURFACE_V65 = PublicationSurface(RELEASE_DIR, CONTENT / "published-packages.v63.json", CONTENT)
PACKAGE_V66 = CONTENT / "package.core-calculations.v66.json"
RELEASE_V64 = RELEASE_DIR / "demo.release.sli-worksheet-integration.2025.v64.json"
SURFACE_V66 = PublicationSurface(RELEASE_DIR, CONTENT / "published-packages.v64.json", CONTENT)

P = "tax.us.2025."
USER = "demo.user.filer-1"
YEAR = "2025"

AGI = P + "income.agi"
TAXABLE = P + "income.taxable-income"
TAX = P + "tax.line24-total-tax"
REFUND = P + "payments.line35a-refunded"
LINE7 = P + "schedule1.line7-unemployment"
LINE8B = P + "schedule1.line8b-gambling"
LINE21 = P + "schedule1.line21-sli-deduction"
SCHEDULE1_DISPOSITION = P + "schedule1.disposition"
F1099G_SUBTOTAL = P + "unemployment.box1-subtotal"
W2G_SUBTOTAL = P + "gambling.b1-winnings-subtotal"
SLI_SUBTOTAL = P + "sli-worksheet.line1-total-interest-paid-subtotal"
SCHEDULE_D_DISPOSITION = P + "schedule-d.disposition"
SCHEDULE_B_DISPOSITION = P + "scheduleb.disposition"
LINE13 = P + "schedule-d.line-13"
LINE15 = P + "schedule-d.line-15"
LINE3B = P + "dividends.ordinary-total"
D2A_SUBTOTAL = P + "dividends.2a-subtotal"
D1A_SUBTOTAL = P + "dividends.1a-subtotal"
PREFERENTIAL_BASE = P + "capital-gains.selected-preferential-base"


@dataclass
class IRun:
    pubs: dict[str, dict[str, Any]]
    blocked: list[dict[str, Any]]
    held: list[dict[str, Any]] = field(default_factory=list)

    def value(self, symbol: str) -> Decimal | None:
        return Decimal(str(self.pubs[symbol]["value"])) if symbol in self.pubs else None

    def values(self) -> dict[str, str]:
        """Every published value, by symbol, numbers normalised (a subtotal that no longer rounds
        prints 200.0 where the rounded one printed 200; the amounts are equal)."""
        return {s: json.dumps(_numeric(f["value"]), sort_keys=True) for s, f in sorted(self.pubs.items())}

    def blocked_codes(self) -> set[tuple[str, str]]:
        return {(str(r.get("artifact_id", "")).replace(P, ""), str(r.get("code"))) for r in self.blocked}

    def itemization(self, subtotal_symbol: str, disposition: str = SCHEDULE1_DISPOSITION) -> dict[str, Any]:
        value = self.pubs[disposition]["value"]
        for part in value["itemizations"]:
            for row_set in part["row_sets"]:
                if row_set["subtotal"]["symbol"] == subtotal_symbol:
                    return {"row_sum": Decimal(str(row_set["row_sum"])), "subtotal": Decimal(str(row_set["subtotal"]["value"])), "part": part}
        raise AssertionError(subtotal_symbol)


def _run(acts: list[dict[str, object]], run_id: str, *, core: str) -> IRun:
    """Runs the return; a base "none" declaration that a recorded member contradicts is withdrawn first
    (as a filer withdraws it by recording the member), once per contradicted declaration."""
    for _ in range(5):
        try:
            return _run_once(acts, run_id, core=core)
        except FindingModelError as exc:
            found = re.search(r"contradiction: (\S+) is currently", str(exc))
            if not found:
                raise
            acts = _strip_closure(acts, found.group(1))
    raise AssertionError("too many declaration withdrawals")


def _run_once(acts: list[dict[str, object]], run_id: str, *, core: str) -> IRun:
    if core == "v66":
        package, version, release, rel_version, surface = PACKAGE_V66, "v66", RELEASE_V64, "v64", SURFACE_V66
    else:
        package, version, release, rel_version, surface = PACKAGE_V65, "v65", RELEASE_V63, "v63", SURFACE_V65
    finished = _finish(
        copy.deepcopy(acts), package_path=package, package_version=version,
        release_path=release, release_version=rel_version, note=run_id,
    )
    finished = _handover(finished, surface=surface, reconfirm=True)
    with TemporaryDirectory() as tmp:
        outcome = live_coordinate_run(
            WorkspaceCapability(Path(tmp) / "L"),
            repo_root=ROOT,
            authoritative_acts=finished,
            workspace_revision=len(finished),
            run_scope={"jurisdiction": "us", "year": YEAR},
            scope_user=USER,
            request={"schema": "run-request.v1"},
            run_id=run_id,
            governance_pins=[],
            surface=surface,
            output_name="out.json",
        )
        if outcome.refusal is not None:
            raise AssertionError(f"{run_id} refused: {outcome.refusal.reason} {outcome.refusal.detail}")
        pubs = {str(p.finding["symbol"]): p.finding for p in outcome.publications or ()}
        blocked: list[dict[str, Any]] = []
        held: list[dict[str, Any]] = []
        if outcome.output_path is not None:
            report = json.loads(outcome.output_path.read_text(encoding="utf-8"))
            blocked = [r for r in report.get("dispositions", []) if r.get("disposition") == "blocked"]
            held = [r for r in report.get("dispositions", []) if r.get("disposition") not in ("blocked", "published")]
    return IRun(pubs, blocked, held)


def _numeric(node: Any) -> Any:
    """The same JSON with every number (or numeric string) normalised, so 200 and 200.0 compare equal."""
    if isinstance(node, dict):
        return {k: _numeric(v) for k, v in node.items()}
    if isinstance(node, list):
        return [_numeric(v) for v in node]
    if isinstance(node, bool) or node is None:
        return node
    if isinstance(node, (int, float)) or (isinstance(node, str) and node[:1] in "-0123456789"):
        try:
            return format(Decimal(str(node)).normalize(), "f")
        except ArithmeticError:
            return node
    return node


def _members(family: str, amounts: list[float], tag: str, *, base: list[dict[str, object]] | None = None,
             companion: str | None = None) -> list[dict[str, object]]:
    """The base return plus one member per amount of ``family``, the family closed after the last."""
    acts = base if base is not None else w2g._w2g_return([])
    for i, amount in enumerate(amounts):
        if companion is not None:
            acts = _add_member_with_companion(acts, P + family, amount, tag=f"{tag}{i}", companion=P + companion)
        else:
            acts = cc._add_member(acts, P + family, amount, close=i == len(amounts) - 1, tag=f"{tag}{i}")
    return acts


def _both(acts: list[dict[str, object]], name: str) -> tuple[IRun, IRun]:
    return _run(acts, f"demo.ic.{name}.v65", core="v65"), _run(acts, f"demo.ic.{name}.v66", core="v66")


# Symbols core v66 publishes that v65 did not, by the track that adds them (a rounded line of its own).
ADDED_SYMBOLS = (LINE13,)


def _assert_same_values(case: unittest.TestCase, old: IRun, new: IRun, label: str) -> None:
    """Every value v65 published is published, unchanged, by v66; v66 adds only the tracks' new line symbols."""
    new_values = new.values()
    added = set(new_values) - set(old.values())
    case.assertLessEqual(added, set(ADDED_SYMBOLS), label)
    case.assertEqual({s: v for s, v in new_values.items() if s not in added}, old.values(), label)
    case.assertEqual(old.blocked_codes(), new.blocked_codes(), label)


def _tie_out_blocked(run: IRun, attachment: str) -> bool:
    return (f"rule.attachment.{attachment}", ITEMIZATION_TIE_OUT_VIOLATION) in run.blocked_codes()


def _f1099g(cents: bool) -> list[dict[str, object]]:
    return _members("f1099g.1", [100.40, 100.40] if cents else [100.0, 100.0], "g")


def _w2g_statements(cents: bool) -> list[dict[str, object]]:
    return w2g._w2g_return([(100.40, None), (100.40, None)] if cents else [(100.0, None), (100.0, None)])


class Track1Schedule1(unittest.TestCase):
    def test_f1099g_cents_block_on_v65_and_publish_on_v66(self) -> None:
        old, new = _both(_f1099g(True), "g")
        self.assertTrue(_tie_out_blocked(old, "schedule-1"), old.blocked_codes())
        self.assertNotIn(SCHEDULE1_DISPOSITION, old.pubs)
        self.assertFalse(_tie_out_blocked(new, "schedule-1"), new.blocked_codes())
        self.assertIn(SCHEDULE1_DISPOSITION, new.pubs)
        rows = new.itemization(F1099G_SUBTOTAL)
        self.assertEqual(rows["row_sum"], Decimal("200.80"))
        self.assertEqual(rows["subtotal"], Decimal("200.80"))
        # The subtotal carries cents and the line rounds it once (P0 t1).
        self.assertEqual(new.value(F1099G_SUBTOTAL), Decimal("200.8"))
        self.assertEqual(new.value(LINE7), Decimal("201"))
        self.assertEqual(old.value(LINE7), Decimal("201"))
        self.assertEqual(new.value(AGI), Decimal("50201"))
        self.assertEqual(new.value(TAXABLE), Decimal("34451"))
        self.assertEqual(new.value(TAX), Decimal("3899"))
        self.assertEqual(new.value(REFUND), Decimal("601"))

    def test_w2g_cents_block_on_v65_and_publish_on_v66(self) -> None:
        old, new = _both(_w2g_statements(True), "w")
        self.assertTrue(_tie_out_blocked(old, "schedule-1"), old.blocked_codes())
        self.assertFalse(_tie_out_blocked(new, "schedule-1"), new.blocked_codes())
        self.assertIn(SCHEDULE1_DISPOSITION, new.pubs)
        rows = new.itemization(W2G_SUBTOTAL)
        self.assertEqual((rows["row_sum"], rows["subtotal"]), (Decimal("200.80"), Decimal("200.80")))
        self.assertEqual(new.value(W2G_SUBTOTAL), Decimal("200.8"))
        self.assertEqual(new.value(LINE8B), Decimal("201"))
        self.assertEqual(old.value(LINE8B), Decimal("201"))
        self.assertEqual(new.value(TAXABLE), Decimal("34451"))
        self.assertEqual(new.value(REFUND), Decimal("601"))

    def test_whole_dollar_returns_are_identical_on_v65_and_v66(self) -> None:
        for name, acts in (("g", _f1099g(False)), ("w", _w2g_statements(False))):
            old, new = _both(acts, name + "whole")
            self.assertFalse(_tie_out_blocked(new, "schedule-1"))
            self.assertIn(SCHEDULE1_DISPOSITION, new.pubs)
            _assert_same_values(self, old, new, name)

    def test_the_explanation_shows_the_subtotal_with_cents_and_the_line_rounded(self) -> None:
        run = _run(_f1099g(True), "demo.ic.explain", core="v66")
        line = run.pubs[LINE7]
        by_id = {str(f["id"]): f for f in run.pubs.values()}
        inputs = [by_id[str(p["id"])] for p in line["pins"] if p["role"] == "input" and str(p["id"]) in by_id]
        # The line's lineage reaches the subtotal finding, which carries the cents ...
        subtotal = next(f for f in inputs if f["symbol"] == F1099G_SUBTOTAL)
        self.assertEqual(Decimal(str(subtotal["value"])), Decimal("200.80"))
        # ... and the line, produced by the rounding operation, is the whole-dollar figure.
        self.assertEqual(str(line["value"]), "201")
        self.assertIn(("operation-semantics", "round"), {(str(p["role"]), str(p["id"])) for p in line["pins"]})

    def test_the_sli_line_one_subtotal_stops_rounding_and_every_reader_rounds_it(self) -> None:
        """Form 1098-E: the worksheet's line 1 entry is the rounded subtotal (structure; see the handoff)."""
        subtotal = _load("rule.sli-worksheet-line1-subtotal.v2.json")
        self.assertEqual(subtotal["value"]["op"], "add")
        self.assertEqual((subtotal["pins"], subtotal["requires"]), ([], []))
        worksheet = _load("rule.sli-worksheet.v6.json")
        rounded: list[Any] = []
        bare: list[Any] = []

        def walk(node: Any, parent_is_round: bool) -> None:
            if isinstance(node, dict):
                if node.get("op") == "ref" and node.get("name") == SLI_SUBTOTAL:
                    (rounded if parent_is_round else bare).append(node)
                for key, child in node.items():
                    walk(child, node.get("op") == "round" and key == "value")
            elif isinstance(node, list):
                for child in node:
                    walk(child, False)

        walk(worksheet, False)
        self.assertEqual(len(rounded), 4)
        self.assertEqual(bare, [])


def _dividends_2a(amounts: list[float]) -> list[dict[str, object]]:
    """Box 2a distributions, with a closed Form 1099-B family beside them so Schedule D attaches."""
    base = cc._add_member(w2g._w2g_return([]), P + "f1099b.covered-st-proceeds", 1000.0, close=True, tag="trig")
    return _members("f1099div.2a", amounts, "d", base=base)


def _dividends_1a(amounts: list[float]) -> list[dict[str, object]]:
    return _members("f1099div.1a", amounts, "o")


class Track2ScheduleDAndLine3b(unittest.TestCase):
    def test_box_2a_cents_block_on_v65_and_publish_on_v66(self) -> None:
        old, new = _both(_dividends_2a([100.40, 100.40]), "d2a")
        self.assertTrue(_tie_out_blocked(old, "schedule-d"), old.blocked_codes())
        self.assertNotIn(SCHEDULE_D_DISPOSITION, old.pubs)
        self.assertFalse(_tie_out_blocked(new, "schedule-d"), new.blocked_codes())
        self.assertIn(SCHEDULE_D_DISPOSITION, new.pubs)
        rows = new.itemization(D2A_SUBTOTAL, SCHEDULE_D_DISPOSITION)
        self.assertEqual((rows["row_sum"], rows["subtotal"]), (Decimal("200.80"), Decimal("200.80")))
        # P0 t4: the subtotal carries cents; line 13 is the rounded 201 (v65 rounded the subtotal to 201 too).
        self.assertEqual(new.value(D2A_SUBTOTAL), Decimal("200.8"))
        self.assertEqual(new.value(LINE13), Decimal("201"))
        self.assertEqual(old.value(D2A_SUBTOTAL), Decimal("201"))
        self.assertIsNone(old.value(LINE13))
        # Line 15 adds the rounded line 13: it equals the whole-dollar return with 201 of distributions.
        whole = _run(_dividends_2a([100.0, 101.0]), "demo.ic.d2a.whole201", core="v65")
        self.assertEqual(new.value(LINE15), whole.value(LINE15))
        self.assertEqual(new.value(PREFERENTIAL_BASE), whole.value(PREFERENTIAL_BASE))
        parts = [new.value(P + "schedule-d." + tail) for tail in ("line-14", "line-8b", "line-8a-gain")]
        self.assertNotIn(None, parts)
        self.assertEqual(new.value(LINE15), Decimal("201") + sum((p for p in parts if p is not None), Decimal(0)))

    def test_box_1a_cents_block_on_v65_and_publish_on_v66(self) -> None:
        old, new = _both(_dividends_1a([800.40, 800.40]), "d1a")
        self.assertTrue(_tie_out_blocked(old, "schedule-b"), old.blocked_codes())
        self.assertFalse(_tie_out_blocked(new, "schedule-b"), new.blocked_codes())
        self.assertIn(SCHEDULE_B_DISPOSITION, new.pubs)
        rows = new.itemization(D1A_SUBTOTAL, SCHEDULE_B_DISPOSITION)
        self.assertEqual((rows["row_sum"], rows["subtotal"]), (Decimal("1600.80"), Decimal("1600.80")))
        # P0 t3's dividend analogue: the subtotal carries cents, line 3b is the rounded 1,601 and total income adds it.
        self.assertEqual(new.value(D1A_SUBTOTAL), Decimal("1600.8"))
        self.assertEqual(new.value(LINE3B), Decimal("1601"))
        self.assertEqual(old.value(LINE3B), Decimal("1601"))
        self.assertEqual(new.value(AGI), Decimal("51601"))

    def test_whole_dollar_returns_are_identical_on_v65_and_v66(self) -> None:
        for name, acts in (("d2a", _dividends_2a([100.0, 100.0])), ("d1a", _dividends_1a([800.0, 800.0]))):
            old, new = _both(acts, name + "whole")
            _assert_same_values(self, old, new, name)
            self.assertFalse(_tie_out_blocked(new, "schedule-d") or _tie_out_blocked(new, "schedule-b"))

    def test_the_explanation_shows_the_subtotal_with_cents_and_line_13_rounded(self) -> None:
        run = _run(_dividends_2a([100.40, 100.40]), "demo.ic.explain13", core="v66")
        line = run.pubs[LINE13]
        by_id = {str(f["id"]): f for f in run.pubs.values()}
        inputs = [by_id[str(p["id"])] for p in line["pins"] if p["role"] == "input" and str(p["id"]) in by_id]
        subtotal = next(f for f in inputs if f["symbol"] == D2A_SUBTOTAL)
        self.assertEqual(Decimal(str(subtotal["value"])), Decimal("200.80"))
        self.assertEqual(str(line["value"]), "201")
        self.assertIn(("operation-semantics", "round"), {(str(p["role"]), str(p["id"])) for p in line["pins"]})

    def test_line_13_is_its_own_rule_and_its_readers_move_to_it(self) -> None:
        field = _load("schedule-d.line-13.form-field.v2.json")
        self.assertEqual(field["binds_symbol"], LINE13)
        for name in ("rule.schedule-d-line15.v5.json", "rule.selected-preferential-base.v6.json"):
            text = json.dumps(_load(name))
            self.assertIn(LINE13, text)
            self.assertNotIn(D2A_SUBTOTAL, text)
        subtotals = (("rule.f1099div-2a-subtotal.v3.json", "f1099div.2a"), ("rule.f1099div-1a-subtotal.v2.json", "f1099div.1a"))
        for name, source_set in subtotals:
            rule = _load(name)
            self.assertEqual(rule["value"]["op"], "add")
            self.assertEqual((rule["pins"], rule["requires"]), ([], []))
        # The box-2a guard is kept; box 1a had none.
        self.assertEqual(_load("rule.f1099div-2a-subtotal.v3.json")["when"], {"op": "require_closed", "source_set": P + "f1099div.2a"})
        self.assertEqual(_load("rule.form1040-line3b.v2.json")["value"]["op"], "round")


class Track4OtherAddingLines(unittest.TestCase):
    """Lines 25b, 2a and Schedule 8812 line 21 add subtotals; they now add the cents and round once."""

    @staticmethod
    def _withholding(interest: float, dividends: float) -> list[dict[str, object]]:
        acts = cc._add_member(w2g._w2g_return([]), P + "f1099int.b4", interest, close=True, tag="i4")
        return cc._add_member(acts, P + "f1099div.b4", dividends, close=True, tag="v4")

    def test_line_25b_rounds_the_cents_sum_once(self) -> None:
        old, new = _both(self._withholding(100.40, 100.40), "d4")
        # P0 d4: 1099-INT box 4 100.40 + 1099-DIV box 4 100.40.
        for run, line25b, line25d, refund in ((old, "200", "4700", "825"), (new, "201", "4701", "826")):
            self.assertEqual(run.value(P + "payments.line25b"), Decimal(line25b))
            self.assertEqual(run.value(P + "payments.line25d"), Decimal(line25d))
            self.assertEqual(run.value(REFUND), Decimal(refund))
        self.assertEqual(new.value(P + "interest.b4-withholding-subtotal"), Decimal("100.4"))
        self.assertEqual(new.value(P + "dividends.b4-withholding-subtotal"), Decimal("100.4"))

    def test_whole_dollar_withholding_returns_are_identical_on_v65_and_v66(self) -> None:
        old, new = _both(self._withholding(100.0, 100.0), "d4whole")
        _assert_same_values(self, old, new, "d4whole")
        self.assertEqual(new.value(P + "payments.line25b"), Decimal("200"))

    def test_subtotals_keep_their_guards_and_line_25b_is_untouched(self) -> None:
        for name in ("f1099int-b4", "f1099div-b4", "f1099r-box4", "f1099g-b4", "ssa1099-b6", "f1099div-12", "f1099int-b8", "w2-box4", "w2-box6"):
            suffix = "total" if name.startswith("w2") else "subtotal"
            old, new = _load(f"rule.{name}-{suffix}.json"), _load(f"rule.{name}-{suffix}.v2.json")
            self.assertEqual(new["when"], old["when"], name)
            self.assertEqual(new["value"], old["value"]["value"], name)
            self.assertNotIn("rounding.convention", new["requires"], name)
        self.assertNotIn(P + "rule.form1040-line25b", {P + n for n in REPLACED})

    def test_lines_2a_and_8812_line_21_round_the_sum_once(self) -> None:
        """Structural: no committed harness drives these on core v65 (the 1099-INT box 8 / 1099-DIV box 12 and
        W-2 box 4 / 6 returns are built on pre-v59 bases that stop at the Social Security chain, and a box 12
        member needs a companion fact the current-core base does not record), so the rule bodies are checked."""
        line2a_old, line2a = _load("rule.form1040-line2a.v3.json"), _load("rule.form1040-line2a.v4.json")
        line21_old, line21 = _load("rule.ctc-sch8812-line-21.json"), _load("rule.ctc-sch8812-line-21.v2.json")
        for old, new in ((line2a_old, line2a), (line21_old, line21)):
            self.assertEqual(new["value"]["op"], "round")
            self.assertEqual(new["value"]["value"], old["value"])
            self.assertEqual(new["value"]["mode"], {"name": "rounding.convention", "op": "ref"})
            self.assertIn("rounding.convention", new["requires"])
            self.assertEqual(new["when"], old["when"])


class Track4LinesDrivenLive(unittest.TestCase):
    """The checks ``test_lines_2a_and_8812_line_21_round_the_sum_once`` could only make on the rule bodies,
    and the Form 1098-E line 21 check, now run on the real coordinator over the current-core returns of
    ``tests/helpers/current_core_returns.py``. The structural check stays. Each hand value is the sum of
    the cents, rounded once: two amounts of 100.40 are 200.80, so 201 (rounding each first would give 200)."""

    def test_line_2a_over_two_box_8_amounts_rounds_the_sum_once(self) -> None:
        run = ccr.run_current_core(ccr.add_tax_exempt_interest_1099int(ccr.base_return(), [100.40, 100.40]), "demo.ic.live.2a.b8")
        self.assertEqual(run.blocked_names(), set())
        self.assertEqual(run.value(ccr.BOX8_SUBTOTAL), Decimal("200.8"))
        self.assertEqual(run.value(ccr.LINE2A), Decimal("201"))

    def test_line_2a_over_two_box_12_amounts_rounds_the_sum_once(self) -> None:
        run = ccr.run_current_core(ccr.add_exempt_interest_dividends_1099div(ccr.base_return(), [100.40, 100.40]), "demo.ic.live.2a.b12")
        self.assertEqual(run.blocked_names(), set())
        self.assertEqual(run.value(ccr.BOX12_SUBTOTAL), Decimal("200.8"))
        self.assertEqual(run.value(ccr.LINE2A), Decimal("201"))

    def test_line_2a_adds_box_8_and_box_12_before_it_rounds(self) -> None:
        acts = ccr.add_tax_exempt_interest_1099int(ccr.base_return(), [100.40])
        run = ccr.run_current_core(ccr.add_exempt_interest_dividends_1099div(acts, [100.40]), "demo.ic.live.2a.both")
        self.assertEqual(run.blocked_names(), set())
        self.assertEqual(run.value(ccr.LINE2A), Decimal("201"))  # 100.40 + 100.40 = 200.80, not 100 + 100

    def test_schedule_8812_line_21_rounds_the_box_4_and_box_6_sum_once(self) -> None:
        run = ccr.run_current_core(ccr.part_ii_b_return(box4=100.40, box6=100.40), "demo.ic.live.8812")
        self.assertEqual(run.blocked_names(), set())
        self.assertEqual(run.value(P + "w2.box4-total"), Decimal("100.4"))
        self.assertEqual(run.value(P + "w2.box6-total"), Decimal("100.4"))
        self.assertEqual(run.value(ccr.SCH8812_LINE21), Decimal("201"))
        # Lines 23 and 25 follow the whole-dollar line 21: 201, then max(201 - 6,761, 0) = 0.
        self.assertEqual(run.value(P + "ctc.sch8812.line-23"), Decimal("201"))
        self.assertEqual(run.value(P + "ctc.sch8812.line-25"), Decimal("0"))

    def test_schedule_1_line_21_rounds_the_two_form_1098_e_amounts_once(self) -> None:
        run = ccr.run_current_core(ccr.add_student_loan_interest_1098e(ccr.base_return(), [100.40, 100.40]), "demo.ic.live.sli")
        self.assertEqual(run.blocked_names(), set())
        self.assertEqual(run.value(SLI_SUBTOTAL), Decimal("200.8"))
        self.assertEqual(run.value(LINE21), Decimal("201"))
        # Hand: AGI 50,000 - 201 = 49,799; taxable 49,799 - 15,750 = 34,049; Tax Table row 34,000-34,050
        # (midpoint 34,025) 1,192.50 + 12% of 22,100 = 3,844.50 -> 3,845; refund 4,500 - 3,845 = 655.
        self.assertEqual(run.value(AGI), Decimal("49799"))
        self.assertEqual(run.value(TAXABLE), Decimal("34049"))
        self.assertEqual(run.value(TAX), Decimal("3845"))
        self.assertEqual(run.value(REFUND), Decimal("655"))


class RecordedStatementMakesItsScheduleRequired(unittest.TestCase):
    """Intended behaviour, pinned: a recorded statement makes its schedule required, even when its
    rounded line is 0 (the schedule is required by the recorded amount, not by the rounded figure)."""

    def test_a_1099g_of_forty_cents_requires_schedule_1_with_line_7_zero(self) -> None:
        run = _run(_members("f1099g.1", [0.40], "tiny-g"), "demo.ic.tiny.g", core="v66")
        self.assertIn(SCHEDULE1_DISPOSITION, run.pubs)
        self.assertFalse(_tie_out_blocked(run, "schedule-1"), run.blocked_codes())
        self.assertEqual(run.value(F1099G_SUBTOTAL), Decimal("0.4"))
        self.assertEqual(run.itemization(F1099G_SUBTOTAL)["row_sum"], Decimal("0.40"))
        self.assertEqual(run.value(LINE7), Decimal("0"))

    def test_a_w2g_of_thirty_cents_requires_schedule_1_with_line_8b_zero(self) -> None:
        run = _run(w2g._w2g_return([(0.30, None)]), "demo.ic.tiny.w", core="v66")
        self.assertIn(SCHEDULE1_DISPOSITION, run.pubs)
        self.assertFalse(_tie_out_blocked(run, "schedule-1"), run.blocked_codes())
        self.assertEqual(run.value(W2G_SUBTOTAL), Decimal("0.3"))
        self.assertEqual(run.value(LINE8B), Decimal("0"))

    def test_a_box_2a_of_forty_cents_publishes_schedule_d(self) -> None:
        run = _run(_dividends_2a([0.40]), "demo.ic.tiny.d", core="v66")
        self.assertIn(SCHEDULE_D_DISPOSITION, run.pubs)
        self.assertFalse(_tie_out_blocked(run, "schedule-d"), run.blocked_codes())
        self.assertEqual(run.value(D2A_SUBTOTAL), Decimal("0.4"))
        self.assertEqual(run.value(LINE13), Decimal("0"))

    def test_line_25b_field_says_cents_are_included_and_the_total_rounded_once(self) -> None:
        old, new = _load("form1040.line-25b.form-field.v2.json"), _load("form1040.line-25b.form-field.v3.json")
        self.assertEqual(new["version"], "v3")
        self.assertEqual({k: v for k, v in new.items() if k not in ("version", "dispositions")}, {k: v for k, v in old.items() if k not in ("version", "dispositions")})
        text = new["dispositions"]["published_value"]["explain"]
        self.assertIn("cents included", text)
        self.assertIn("rounded once", text)
        self.assertNotIn("equals the sum", text)
        for key in old["dispositions"]:
            if key != "published_value":
                self.assertEqual(new["dispositions"][key], old["dispositions"][key])


def _load(name: str) -> dict[str, Any]:
    loaded: dict[str, Any] = json.loads((CONTENT / name).read_text("utf-8"))
    return loaded


def _citizens(registry: str) -> dict[tuple[str, str], str]:
    document = json.loads((CONTENT / registry).read_text("utf-8"))
    return {(c["id"], c["version"]): c["checksum"] for c in document["citizens"]}


def _package_members(package: Path) -> dict[str, str]:
    return {m["id"]: m["version"] for m in json.loads(package.read_text("utf-8"))["members"]}


def _entrypoints(package: Path) -> dict[str, str]:
    return {e["id"]: e["version"] for e in json.loads(package.read_text("utf-8"))["entrypoints"]}


# What each track replaces or adds on core v66, by id: (from, to). A track extends this table.
TRACK1_REPLACED = {
    "rule.f1099g-1-subtotal": ("v2", "v3"), "rule.w2g-b1-subtotal": ("v1", "v2"),
    "rule.sli-worksheet-line1-subtotal": ("v1", "v2"), "rule.schedule1-line7": ("v2", "v3"),
    "rule.schedule1-line8b": ("v1", "v2"), "rule.sli-worksheet": ("v5", "v6"),
}
TRACK2_REPLACED = {
    "rule.f1099div-2a-subtotal": ("v2", "v3"), "schedule-d.line-13": ("v1", "v2"),
    "rule.schedule-d-line15": ("v4", "v5"), "rule.selected-preferential-base": ("v5", "v6"),
    "rule.f1099div-1a-subtotal": ("v1", "v2"), "rule.form1040-line3b": ("v1", "v2"),
}
TRACK2_ADDED = {"rule.schedule-d-line13": "v1"}
TRACK2_ENTRYPOINTS = {"rule.f1099div-2a-subtotal", "rule.selected-preferential-base"}
TRACK4_REPLACED = {
    **{f"rule.{n}-subtotal": ("v1", "v2") for n in ("f1099int-b4", "f1099div-b4", "f1099r-box4", "f1099g-b4", "ssa1099-b6", "f1099div-12", "f1099int-b8")},
    "rule.w2-box4-total": ("v1", "v2"), "rule.w2-box6-total": ("v1", "v2"),
    "rule.form1040-line2a": ("v3", "v4"), "rule.ctc-sch8812-line-21": ("v1", "v2"),
    "form1040.line-25b": ("v2", "v3"),
}
TRACK4_ENTRYPOINTS = {"rule.f1099div-12-subtotal", "rule.f1099int-b8-subtotal", "rule.form1040-line2a", "rule.ctc-sch8812-line-21"}
TRACK1_ENTRYPOINTS = {"rule.f1099g-1-subtotal", "rule.sli-worksheet-line1-subtotal", "rule.schedule1-line7", "rule.sli-worksheet"}
REPLACED = {**TRACK1_REPLACED, **TRACK2_REPLACED, **TRACK4_REPLACED}
ADDED = {**TRACK2_ADDED}
ENTRYPOINTS = TRACK1_ENTRYPOINTS | TRACK2_ENTRYPOINTS | TRACK4_ENTRYPOINTS


class PackageDeltas(unittest.TestCase):
    def test_registry_v64_only_adds_to_registry_v63(self) -> None:
        old, new = _citizens("published-packages.v63.json"), _citizens("published-packages.v64.json")
        for key, checksum in old.items():
            self.assertEqual(new.get(key), checksum, key)
        expected = {(P + name, to) for name, (_, to) in REPLACED.items()} | {(P + name, v) for name, v in ADDED.items()}
        self.assertEqual(set(new) - set(old), expected)
        registry = json.loads((CONTENT / "published-packages.v64.json").read_text("utf-8"))
        self.assertEqual(
            len(registry["packages"]), len(json.loads((CONTENT / "published-packages.v63.json").read_text("utf-8"))["packages"]) + 1,
        )

    def test_core_v66_replaces_and_adds_exactly_the_tracks_citizens(self) -> None:
        old, new = _package_members(PACKAGE_V65), _package_members(PACKAGE_V66)
        changed = {k: (old[k], new[k]) for k in old if old[k] != new.get(k)}
        self.assertEqual(changed, {P + name: pair for name, pair in REPLACED.items()})
        self.assertEqual({k: new[k] for k in set(new) - set(old)}, {P + name: v for name, v in ADDED.items()})
        old_e, new_e = _entrypoints(PACKAGE_V65), _entrypoints(PACKAGE_V66)
        self.assertEqual(
            {k: (old_e[k], new_e[k]) for k in old_e if old_e[k] != new_e.get(k)},
            {P + name: REPLACED[name] for name in ENTRYPOINTS if name in REPLACED},
        )
        a, b = json.loads(PACKAGE_V65.read_text("utf-8")), json.loads(PACKAGE_V66.read_text("utf-8"))
        self.assertEqual(a["admitted_schemas"], b["admitted_schemas"])
        self.assertEqual(a["input_bindings"], b["input_bindings"])

    def test_the_release_names_the_registry_it_ships_with(self) -> None:
        release = json.loads(RELEASE_V64.read_text("utf-8"))
        digest = hashlib.sha256((CONTENT / "published-packages.v64.json").read_bytes()).hexdigest()
        self.assertEqual(release["package_registry_sha256"], digest)
        self.assertEqual(release["version"], "v64")

    def test_core_v66_shares_v65s_companion_declaration(self) -> None:
        from packages.tax.loader import domain_package_companion_declarations

        declarations = domain_package_companion_declarations()
        core = P + "package.core-calculations"
        self.assertEqual(declarations[(core, "v66")], declarations[(core, "v65")])
