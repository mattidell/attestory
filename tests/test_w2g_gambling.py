"""Track 1: Form W-2G winnings reach Schedule 1 line 8b and withholding reaches line 25c on core v65.

Every run goes through ``live_coordinate_run`` on the committed packages (core v64 /
registry v62 / release v62 and the successor core v65 / registry v63 / release v63), on
a complete return built the way the Form 1099 withholding tests build theirs. A Form W-2G
is recorded the way a filer does: the statement entities are introduced and each box is
recorded by a member-transition that advances its family's horizon, with each family's
closure attested at the horizon that results.

The hand values are those of the milestone's P0 (section 5 of
``w2g-gambling-evidence/p0-trace-and-design.md``), computed from the 2025 Tax Table before
the engine ran; the cases assert them. Synthetic ``demo.*`` data only.
"""

from __future__ import annotations

import copy
import hashlib
import json
from dataclasses import dataclass, field
from decimal import Decimal
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any, Sequence, cast
import unittest

from packages.derivation.live import live_coordinate_run
from packages.derivation.live_workspace import WorkspaceCapability
from packages.derivation.production_resolver import PublicationSurface
from packages.derivation.runner import ITEMIZATION_TIE_OUT_VIOLATION
from packages.kernel.findings import FindingModelError, project
from tests.test_collect_closure_regression import (
    HELD_DOWNSTREAM,
    KNOWN_GAP_ATTACHMENTS_V63,
    _flagged,
    _flagged_attachments,
)
from tools.collect_closure_survey import survey
from tests.test_form_1099_k_income import _handover, _splice
from tests.test_form_1099_withholding import (
    Run,
    _add,
    _assert,
    _base,
    _close,
    _introduce,
    _roots,
    _social_security_withholding,
    _transition,
    _unemployment_withholding,
    _walk_ids,
)
from tests.test_refund_or_amount_owed_track1 import _attested, _finish, _load

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "packages/content/tax/2025"
RELEASE_DIR = ROOT / "packages/sample_data/student_loan_worksheet_integration/publication_surface/releases"

PACKAGE_V64 = CONTENT / "package.core-calculations.v64.json"
RELEASE_V62 = RELEASE_DIR / "demo.release.sli-worksheet-integration.2025.v62.json"
SURFACE_V64 = PublicationSurface(RELEASE_DIR, CONTENT / "published-packages.v62.json", CONTENT)
PACKAGE_V65 = CONTENT / "package.core-calculations.v65.json"
RELEASE_V63 = RELEASE_DIR / "demo.release.sli-worksheet-integration.2025.v63.json"
SURFACE_V65 = PublicationSurface(RELEASE_DIR, CONTENT / "published-packages.v63.json", CONTENT)

P = "tax.us.2025."
USER = "demo.user.filer-1"
YEAR = "2025"
SCOPE_KEY = {"tax-year": YEAR, "subject": "demo.primary"}

B1_FAMILY = P + "w2g.b1"
B4_FAMILY = P + "w2g.b4"
BOX1 = P + "w2g.box1-winnings"
BOX4 = P + "w2g.box4-withholding"
B1_CLOSURE = P + "w2g.b1.source-closure"
B4_CLOSURE = P + "w2g.b4.source-closure"
SCOPE_ANSWER = P + "w2g-scope.no-sch1-other-income-except-w2g"
OLD_OTHER_INCOME = P + "schedule1-part1-scope.no-sch1-other-income"
GAMBLING_DECLARED = P + "schedule-a-boundary.no-gambling-other-declared"
B1_SUBTOTAL = P + "gambling.b1-winnings-subtotal"
B4_SUBTOTAL = P + "gambling.b4-withholding-subtotal"

LINE8B = P + "schedule1.line8b-gambling"
LINE10 = P + "schedule1.line10-additional-income"
LINE8 = P + "income.additional-income"
AGI = P + "income.agi"
TAXABLE = P + "income.taxable-income"
LINE24 = P + "tax.line24-total-tax"
LINE25C = P + "payments.line25c"
LINE25D = P + "payments.line25d"
LINE35A = P + "payments.line35a-refunded"
LINE37 = P + "payments.line37-amount-owed"
VALUE_SYMBOLS = (LINE8B, LINE10, LINE8, AGI, TAXABLE, LINE24, LINE25C, LINE25D, LINE35A, LINE37)

# --- recording ---------------------------------------------------------------


def _set_answer(acts: list[dict[str, object]], fact_type: str, value: object) -> None:
    hits = 0
    for act in acts:
        finding = cast(dict[str, Any], act["payload"]).get("finding")
        if isinstance(finding, dict) and str(finding.get("fact_id", "")).startswith(fact_type + "|"):
            finding["value"] = value
            hits += 1
    assert hits == 1, (fact_type, hits)


def _v64_return(*, wages: float = 50000.0, w2: float = 4500.0, joint: bool = False) -> list[dict[str, object]]:
    """A complete return as core v64 asks it: no W-2G fact exists, every earlier answer given."""
    acts = _base(wages=wages, w2_withheld=w2, joint=joint)
    _unemployment_withholding(acts, [])
    _social_security_withholding(acts, [])
    return acts


def _w2g(
    acts: list[dict[str, object]],
    statements: Sequence[tuple[float | None, float | None]],
    *,
    b1: str = "closed",
    b4: str = "closed",
    other_income: str | None = "yes",
) -> None:
    """Records Form W-2G statements as (box 1, box 4) pairs and the three v65 answers.

    ``b1`` / ``b4`` is ``"closed"`` (closure attested after the last member), ``"never"`` (no
    closure) or ``"stale"`` (closed after the first statement, then a later statement is
    recorded so the closure is behind the family's horizon). ``None`` for a box records no
    amount on that statement. ``other_income`` is the new Schedule 1 answer (None leaves it
    unanswered).
    """
    _add(acts, "bundle-adoption", {"bundle": _load("w2g.bundle.json")})
    heads = {B1_FAMILY: "demo.w2g.b1.h0", B4_FAMILY: "demo.w2g.b4.h0"}
    for family, head in heads.items():
        _add(acts, "horizon-genesis", {"family": {"id": family, "version": "v1"}, "scope": dict(SCOPE_KEY), "horizon_id": head})
    modes = {B1_FAMILY: b1, B4_FAMILY: b4}
    closures = {B1_FAMILY: B1_CLOSURE, B4_FAMILY: B4_CLOSURE}
    names = {B1_FAMILY: "b1", B4_FAMILY: "b4"}
    for i, (box1, box4) in enumerate(statements):
        keys = (("payer", f"demo.w2g.payer.{i}"), ("statement", f"demo.w2g.stmt.{i}"))
        _introduce(acts, f"demo.w2g.payer.{i}", "tax.us.gambling-payer")
        _introduce(acts, f"demo.w2g.stmt.{i}", "tax.us.w2g-statement")
        for family, fact_type, amount, tag in ((B1_FAMILY, BOX1, box1, "box1"), (B4_FAMILY, BOX4, box4, "box4")):
            if amount is None:
                continue
            heads[family] = _transition(
                acts, (family, "v1"), heads[family], f"demo.w2g.{names[family]}.h{i + 1}",
                f"demo.w2g.{tag}.{i}", fact_type, keys, amount,
            )
        if i == 0 and len(statements) > 1:
            for family in heads:
                if modes[family] == "stale":
                    _close(acts, closures[family], heads[family], f"demo.w2g.closure.{names[family]}.stale")
    for family in heads:
        if modes[family] == "closed":
            _close(acts, closures[family], heads[family], f"demo.w2g.closure.{names[family]}")
    if other_income is not None:
        _add(acts, "assertion", {"finding": _attested("demo.w2g.scope.other-income", f"{SCOPE_ANSWER}|tax-year={YEAR}", other_income)})


def _w2g_return(
    statements: Sequence[tuple[float | None, float | None]],
    *,
    wages: float = 50000.0,
    w2: float = 4500.0,
    joint: bool = False,
    **kwargs: Any,
) -> list[dict[str, object]]:
    acts = _v64_return(wages=wages, w2=w2, joint=joint)
    _w2g(acts, statements, **kwargs)
    return acts


# --- running -----------------------------------------------------------------


@dataclass
class W2GRun(Run):
    """A run plus the rules the guards held as not applicable (they publish nothing, and are not blocked rows)."""

    held: list[dict[str, Any]] = field(default_factory=list)

    def held_names(self) -> set[str]:
        return {str(r["artifact_id"]).replace(P, "") for r in self.held}


def _run(acts: list[dict[str, object]], run_id: str, *, core: str = "v65") -> W2GRun:
    if core == "v65":
        package, version, release, rel_version, surface = PACKAGE_V65, "v65", RELEASE_V63, "v63", SURFACE_V65
    else:
        package, version, release, rel_version, surface = PACKAGE_V64, "v64", RELEASE_V62, "v62", SURFACE_V64
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
    return W2GRun(pubs, blocked, held)


def _values(run: Run) -> dict[str, str | None]:
    return {s: (format(Decimal(str(run.pubs[s]["value"])).normalize(), "f") if s in run.pubs else None) for s in VALUE_SYMBOLS}


def _expect(run: Run, **want: str) -> None:
    got = _values(run)
    names = {
        "l8b": LINE8B, "l10": LINE10, "l8": LINE8, "agi": AGI, "taxable": TAXABLE, "l24": LINE24,
        "l25c": LINE25C, "l25d": LINE25D, "refund": LINE35A, "owed": LINE37,
    }
    for key, expected in want.items():
        assert got[names[key]] == expected, (key, got[names[key]], expected)


def _blocked_names(run: Run) -> set[str]:
    return {str(r["artifact_id"]).replace(P, "") for r in run.blocked}


# --- the cases ---------------------------------------------------------------


class W2GWinningsAndWithholding(unittest.TestCase):
    def test_base_return_is_the_hand_baseline(self) -> None:
        run = _run(_w2g_return([]), "demo.w2g.b")
        _expect(run, l8b="0", l10="0", l8="0", agi="50000", taxable="34250", l24="3875", l25c="0", l25d="4500", refund="625", owed="0")
        self.assertEqual(run.value(B1_SUBTOTAL), 0)
        self.assertEqual(run.value(B4_SUBTOTAL), 0)
        self.assertEqual(run.blocked, [])

    def test_case_1_one_w2g_without_withholding(self) -> None:
        run = _run(_w2g_return([(1200.0, None)]), "demo.w2g.c1")
        # P0 case 1: tax 4,019 (+144), refund 481 (-144).
        _expect(run, l8b="1200", l10="1200", l8="1200", agi="51200", taxable="35450", l24="4019", l25c="0", l25d="4500", refund="481", owed="0")
        self.assertEqual(run.blocked, [])

    def test_case_2_a_w2g_with_twenty_four_percent_withheld(self) -> None:
        base = _run(_w2g_return([]), "demo.w2g.c2.base")
        run = _run(_w2g_return([(6000.0, 1440.0)]), "demo.w2g.c2")
        # P0 case 2: line 8b +6,000, line 25c +1,440, tax 4,595 (+720), refund 1,345 (+720).
        _expect(run, l8b="6000", l10="6000", l8="6000", agi="56000", taxable="40250", l24="4595", l25c="1440", l25d="5940", refund="1345", owed="0")
        self.assertEqual(run.value(LINE8B) - base.value(LINE8B), 6000)
        self.assertEqual(run.value(LINE25C) - base.value(LINE25C), 1440)
        self.assertEqual(run.value(LINE24) - base.value(LINE24), 720)
        self.assertEqual(run.net() - base.net(), 720)
        self.assertEqual(run.blocked, [])

    def test_case_3_a_joint_return_with_one_w2g_each(self) -> None:
        acts = _w2g_return([(3000.0, 720.0), (2000.0, None)], wages=80000.0, w2=7000.0, joint=True)
        run = _run(acts, "demo.w2g.c3")
        # P0 case 3: 8b 5,000, 25c 720, AGI 85,000, taxable 53,500, tax 5,946, payments 7,720, refund 1,774.
        _expect(run, l8b="5000", l25c="720", agi="85000", taxable="53500", l24="5946", l25d="7720", refund="1774", owed="0")
        self.assertEqual(run.blocked, [])
        finding_ids, _ = _walk_ids(run, LINE8B)
        self.assertTrue({"demo.w2g.box1.0", "demo.w2g.box1.1"} <= finding_ids)

    def test_case_4a_an_unconfirmed_box_1_family_blocks_the_winnings(self) -> None:
        for mode in ("never", "stale"):
            statements = [(6000.0, 1440.0)] if mode == "never" else [(3000.0, 720.0), (3000.0, 720.0)]
            run = _run(_w2g_return(statements, b1=mode), f"demo.w2g.c4a.{mode}")
            roots = _roots(run)
            code, missing = roots[P + "rule.w2g-b1-subtotal"]
            self.assertEqual(code, "SOURCE_SET_UNCLOSED")
            self.assertEqual(missing, [B1_FAMILY])
            for symbol in (B1_SUBTOTAL, LINE8B, LINE10, LINE8, AGI, TAXABLE, LINE24, LINE35A):
                self.assertNotIn(symbol, run.pubs, (mode, symbol))
            # Withholding is a separate family: line 25c and 25d still publish.
            self.assertEqual(run.value(LINE25C), 1440)
            self.assertEqual(run.value(LINE25D), 5940)

    def test_case_4b_an_unconfirmed_box_4_family_blocks_the_withholding_only(self) -> None:
        for mode in ("never", "stale"):
            statements = [(6000.0, 1440.0)] if mode == "never" else [(3000.0, 720.0), (3000.0, 720.0)]
            run = _run(_w2g_return(statements, b4=mode), f"demo.w2g.c4b.{mode}")
            roots = _roots(run)
            code, missing = roots[P + "rule.w2g-b4-subtotal"]
            self.assertEqual(code, "SOURCE_SET_UNCLOSED")
            self.assertEqual(missing, [B4_FAMILY])
            for symbol in (B4_SUBTOTAL, LINE25C, LINE25D, LINE35A):
                self.assertNotIn(symbol, run.pubs, (mode, symbol))
            _expect(run, l8b="6000", l10="6000", l8="6000", agi="56000", taxable="40250", l24="4595")

    def test_case_5a_winnings_with_no_w2g_are_refused_by_the_answer(self) -> None:
        run = _run(_w2g_return([], other_income="no"), "demo.w2g.c5a")
        self.assertNotIn(LINE10, run.pubs)
        self.assertNotIn(AGI, run.pubs)
        self.assertNotIn(LINE35A, run.pubs)
        self.assertIn("rule.schedule1-line10", run.held_names())
        # The old answer does not clear it: v65 reads only the new one.
        old_yes = _w2g_return([], other_income="no")
        _set_answer(old_yes, OLD_OTHER_INCOME, "yes")
        self.assertNotIn(AGI, _run(old_yes, "demo.w2g.c5a.old-yes").pubs)

    def test_case_5b_losses_with_a_recorded_w2g_are_refused_by_the_declaration(self) -> None:
        acts = _w2g_return([(6000.0, 1440.0)])
        _set_answer(acts, GAMBLING_DECLARED, "no")
        run = _run(acts, "demo.w2g.c5b")
        for symbol in (B1_SUBTOTAL, LINE8B, LINE10, LINE8, AGI, TAXABLE, LINE35A):
            self.assertNotIn(symbol, run.pubs, symbol)
        self.assertIn("rule.w2g-b1-subtotal", run.held_names())
        # The withholding family is separate: line 25c still publishes.
        self.assertEqual(run.value(LINE25C), 1440)

    def test_the_loss_declaration_is_not_read_when_no_w2g_is_recorded(self) -> None:
        acts = _w2g_return([])
        _set_answer(acts, GAMBLING_DECLARED, "no")
        run = _run(acts, "demo.w2g.c5b.empty")
        _expect(run, l8b="0", l10="0", agi="50000", taxable="34250", l24="3875", refund="625")

    def test_case_6_a_v64_return_without_gambling_is_unchanged_on_v65(self) -> None:
        v64 = _run(_v64_return(), "demo.w2g.c6.v64", core="v64")
        acts = _w2g_return([])
        v65 = _run(acts, "demo.w2g.c6.v65")
        keys = (AGI, TAXABLE, LINE24, LINE25D, LINE35A, LINE37, LINE8, LINE10, LINE25C)
        for symbol in keys:
            self.assertEqual(v64.value(symbol), v65.value(symbol), symbol)
        self.assertEqual(v64.blocked, [])

    def test_line_8b_adds_to_line_10_on_the_form_1099k_statement_path(self) -> None:
        # P0's "Track 1 must prove": line 7 + line 8b inside the 1099-K path's `choose` branch.
        acts = _splice(_w2g_return([(6000.0, 1440.0)]), box4=0.0, omit=None)
        run = _run(acts, "demo.w2g.k-path")
        _expect(run, l8b="6000", l10="6000", l8="6000", agi="56000", taxable="40250", l24="4595", l25c="1440", refund="1345")
        self.assertEqual(run.blocked, [])
        # An unresolved Form 1099-K still blocks line 10 on v65, winnings or not.
        unresolved = _run(_splice(_w2g_return([(6000.0, 1440.0)]), box4=150.0, omit=None), "demo.w2g.k-path.unresolved")
        self.assertNotIn(LINE10, unresolved.pubs)
        self.assertEqual(unresolved.value(LINE8B), 6000)

    def test_v65_blocks_until_the_three_adoption_answers_are_given(self) -> None:
        # No W-2G family closure and no new Schedule 1 answer: the v64 answer set alone is not enough.
        acts = _v64_return()
        _add(acts, "bundle-adoption", {"bundle": _load("w2g.bundle.json")})
        for family in (B1_FAMILY, B4_FAMILY):
            _add(acts, "horizon-genesis", {"family": {"id": family, "version": "v1"}, "scope": dict(SCOPE_KEY), "horizon_id": f"demo.w2g.{family[-2:]}.h0"})
        run = _run(acts, "demo.w2g.adopt")
        roots = _roots(run)
        self.assertEqual(roots[P + "rule.w2g-b1-subtotal"][0], "SOURCE_SET_UNCLOSED")
        self.assertEqual(roots[P + "rule.w2g-b4-subtotal"][0], "SOURCE_SET_UNCLOSED")
        self.assertNotIn(AGI, run.pubs)

    def test_a_log_carrying_a_w2g_is_refused_on_v64_not_computed_without_it(self) -> None:
        acts = _w2g_return([(6000.0, 1440.0)])
        self.assertEqual(_run(acts, "demo.w2g.v65.ok").value(LINE25C), 1440)
        with self.assertRaises(FindingModelError) as raised:
            _run(acts, "demo.w2g.on.v64", core="v64")
        message = str(raised.exception)
        self.assertIn("companion presence violated", message)
        self.assertIn("tax.us.2025.w2g.", message)

    def test_a_w2g_box_4_alone_is_refused_on_v64_naming_the_companion(self) -> None:
        acts = _w2g_return([(None, 1440.0)])
        with self.assertRaises(FindingModelError) as raised:
            _run(acts, "demo.w2g.b4only.on.v64", core="v64")
        self.assertIn("companion presence violated", str(raised.exception))

    def test_r1_a_box_4_amount_without_box_1_is_refused_at_recording_on_v65(self) -> None:
        with self.assertRaises(FindingModelError) as raised:
            _run(_w2g_return([(None, 1440.0)]), "demo.w2g.r1.b4only")
        message = str(raised.exception)
        self.assertIn("companion presence violated", message)
        self.assertIn(BOX1, message)
        # A normal W-2G, with and without box 4, is unchanged.
        self.assertEqual(_run(_w2g_return([(6000.0, 1440.0)]), "demo.w2g.r1.ok").value(LINE25C), 1440)
        self.assertEqual(_run(_w2g_return([(1200.0, None)]), "demo.w2g.r1.nob4").value(LINE8B), 1200)

    def test_r2_known_gap_two_box_1_amounts_of_100_40_block_the_attachment(self) -> None:
        # Known gap, inherited and parked (not fixed here): each statement's box 1 is rounded
        # in the row set sum differently from the rounded subtotal, so 100.40 + 100.40 = 200.80
        # publishes subtotal 201 and the attachment's tie-out is violated. Two Form 1099-G box 1
        # amounts of 100.40 do the same on core v64.
        run = _run(_w2g_return([(100.40, None), (100.40, None)]), "demo.w2g.r2")
        self.assertEqual(run.value(B1_SUBTOTAL), 201)
        row = run.blocked_on("rule.attachment.schedule-1")
        self.assertEqual(row["code"], ITEMIZATION_TIE_OUT_VIOLATION)

    def test_the_explanation_walks_from_line_8b_and_line_25c_to_each_statement(self) -> None:
        run = _run(_w2g_return([(3000.0, 720.0), (2000.0, 240.0)]), "demo.w2g.walk")
        finding_ids, symbols = _walk_ids(run, LINE8B)
        self.assertIn(B1_SUBTOTAL, symbols)
        self.assertTrue({"demo.w2g.box1.0", "demo.w2g.box1.1"} <= finding_ids)
        self.assertNotIn("demo.w2g.box4.0", finding_ids)
        finding_ids, symbols = _walk_ids(run, LINE25C)
        self.assertIn(B4_SUBTOTAL, symbols)
        self.assertTrue({"demo.w2g.box4.0", "demo.w2g.box4.1"} <= finding_ids)
        # On v65 a box 4 amount is pinned to its same-statement box 1 companion (R1), so the
        # box 1 finding is on the walk too; the box 4 findings are the amounts line 25c sums.
        self.assertIn("demo.w2g.box1.0", finding_ids)
        self.assertEqual(run.value(LINE25C), 960)
        self.assertEqual(run.value(LINE8B), 5000)

    def test_the_schedule_1_attachment_itemizes_line_8b(self) -> None:
        run = _run(_w2g_return([(6000.0, 1440.0)]), "demo.w2g.attachment")
        disposition = run.pubs[P + "schedule1.disposition"]
        text = json.dumps(disposition, sort_keys=True)
        self.assertIn("line-8b-gambling", text)


class PackageDeltas(unittest.TestCase):
    def test_registry_v63_only_adds_to_registry_v62(self) -> None:
        old = json.loads((CONTENT / "published-packages.v62.json").read_text("utf-8"))
        new = json.loads((CONTENT / "published-packages.v63.json").read_text("utf-8"))
        old_c = {(c["id"], c["version"]): c["checksum"] for c in old["citizens"]}
        new_c = {(c["id"], c["version"]): c["checksum"] for c in new["citizens"]}
        for key, checksum in old_c.items():
            self.assertEqual(new_c.get(key), checksum, key)
        added = sorted(set(new_c) - set(old_c))
        expected = [(P + name, "v1") for name in (
            "w2g.vocabulary", "w2g.b1", "w2g.b4", "closure-mapping.w2g-b1", "closure-mapping.w2g-b4",
            "rule.w2g-b1-subtotal", "rule.w2g-b4-subtotal", "rule.schedule1-line8b",
            "citation.schedule1.line-8b", "schedule1.line-8b",
        )] + [
            (P + "rule.schedule1-line10", "v3"), (P + "rule.form1040-line25c", "v2"),
            (P + "rule.attachment.schedule-1", "v5"), (P + "schedule1.line-10", "v3"),
            (P + "form1040.line-25c", "v2"), (P + "form1040.line-8", "v2"),
        ]
        self.assertEqual(added, sorted(expected))
        self.assertEqual(len(old["packages"]) + 1, len(new["packages"]))

    def test_core_v65_replaces_exactly_the_six_successors_and_adds_the_ten_citizens(self) -> None:
        old = json.loads(PACKAGE_V64.read_text("utf-8"))
        new = json.loads(PACKAGE_V65.read_text("utf-8"))
        old_m = {m["id"]: m["version"] for m in old["members"]}
        new_m = {m["id"]: m["version"] for m in new["members"]}
        changed = {k: (old_m[k], new_m[k]) for k in old_m if old_m[k] != new_m.get(k)}
        self.assertEqual(
            changed,
            {
                P + "rule.schedule1-line10": ("v2", "v3"),
                P + "rule.form1040-line25c": ("v1", "v2"),
                P + "rule.attachment.schedule-1": ("v4", "v5"),
                P + "schedule1.line-10": ("v2", "v3"),
                P + "form1040.line-25c": ("v1", "v2"),
                P + "form1040.line-8": ("v1", "v2"),
            },
        )
        self.assertEqual(len(new_m) - len(old_m), 10)
        self.assertEqual(old["admitted_schemas"], new["admitted_schemas"])
        old_e = {e["id"]: e["version"] for e in old["entrypoints"]}
        new_e = {e["id"]: e["version"] for e in new["entrypoints"]}
        self.assertEqual(
            {k: (old_e[k], new_e[k]) for k in old_e if old_e[k] != new_e.get(k)},
            {P + "rule.schedule1-line10": ("v2", "v3"), P + "rule.attachment.schedule-1": ("v4", "v5")},
        )
        self.assertEqual(set(new_e) - set(old_e), set())

    def test_the_release_names_the_registry_it_ships_with(self) -> None:
        release = json.loads(RELEASE_V63.read_text("utf-8"))
        digest = hashlib.sha256((CONTENT / "published-packages.v63.json").read_bytes()).hexdigest()
        self.assertEqual(release["package_registry_sha256"], digest)

    def test_companion_declarations_for_v65(self) -> None:
        from packages.tax.loader import (
            domain_companion_presence_pairs,
            domain_package_companion_declarations,
        )

        pairs = domain_companion_presence_pairs()
        self.assertEqual(pairs[BOX1], pairs[BOX4])
        declarations = domain_package_companion_declarations()
        core = P + "package.core-calculations"
        for version in ("v59", "v60", "v61", "v62", "v63", "v64"):
            self.assertNotIn(BOX1, declarations[(core, version)]["presence_pairs"], version)
        v65 = declarations[(core, "v65")]
        self.assertIsNone(v65["presence_pairs"][BOX1])
        # R1: a box 4 amount needs the same statement's box 1 on v65.
        self.assertEqual(v65["presence_pairs"][BOX4], BOX1)
        # v65 keeps v64's withholding declaration.
        for key, value in declarations[(core, "v64")]["presence_pairs"].items():
            self.assertEqual(v65["presence_pairs"][key], value)
        self.assertEqual(v65["value_domains"], declarations[(core, "v64")]["value_domains"])


class EarlierPackagesRefuseAW2G(unittest.TestCase):
    def _registry(self) -> Any:
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

    def test_r3_every_earlier_core_package_and_a_log_with_no_adoption_refuse_a_recorded_w2g(self) -> None:
        registry = self._registry()
        versions = sorted(
            int(p.name.split(".v")[-1].split(".")[0])
            for p in CONTENT.glob("package.core-calculations.v*.json")
            if int(p.name.split(".v")[-1].split(".")[0]) < 65
        )
        self.assertIn(64, versions)
        self.assertIn(1, versions[:3] + [1])
        base = _w2g_return([(6000.0, 1440.0)])
        # No adoption act at all: the global maps apply.
        with self.assertRaises(FindingModelError) as raised:
            project(tuple(copy.deepcopy(base)), registry)
        self.assertIn("companion presence violated", str(raised.exception))
        refused = 0
        for number in versions:
            path = CONTENT / f"package.core-calculations.v{number}.json"
            acts = _finish(
                copy.deepcopy(base), package_path=path, package_version=f"v{number}",
                release_path=RELEASE_V63, release_version="v63", note=f"demo.w2g.sweep.v{number}",
            )
            with self.assertRaises(FindingModelError, msg=f"v{number}") as raised:
                project(tuple(acts), registry)
            self.assertIn("companion presence violated", str(raised.exception), f"v{number}")
            refused += 1
        self.assertEqual(refused, len(versions))
        # Positive control: v65 folds the same log.
        project(tuple(_finish(
            copy.deepcopy(base), package_path=PACKAGE_V65, package_version="v65",
            release_path=RELEASE_V63, release_version="v63", note="demo.w2g.sweep.v65",
        )), registry)

    def test_r4_the_witness_is_not_a_registered_fact_type_anywhere(self) -> None:
        from packages.tax.loader import W2G_UNREAD_WITNESS

        for root in (ROOT / "packages/content", ROOT / "packages/schemas"):
            for path in root.rglob("*.json"):
                self.assertNotIn(W2G_UNREAD_WITNESS, path.read_text("utf-8"), str(path))


class ClosureRegression(unittest.TestCase):
    """The two new collects are guarded at their own site; the survey flags nothing new on v65."""

    def test_core_v65_has_no_unexplained_path_to_a_bound_line(self) -> None:
        self.assertEqual(_flagged(PACKAGE_V65) - HELD_DOWNSTREAM, set())
        self.assertEqual(_flagged(PACKAGE_V65), _flagged(CONTENT / "package.core-calculations.v64.json"))

    def test_core_v65_attachment_known_gaps_are_unchanged(self) -> None:
        self.assertEqual(_flagged_attachments(PACKAGE_V65), KNOWN_GAP_ATTACHMENTS_V63)

    def test_the_two_w2g_collects_are_guarded_at_their_own_site(self) -> None:
        guarded = {e["source_set"]: e["guard"] for e in survey(PACKAGE_V65)["collects_guarded_at_their_own_site"]}
        for family in (B1_FAMILY, B4_FAMILY):
            self.assertEqual(guarded.get(family), "enclosing when", family)
            self.assertNotIn(family, _flagged(PACKAGE_V65))


if __name__ == "__main__":
    unittest.main()
