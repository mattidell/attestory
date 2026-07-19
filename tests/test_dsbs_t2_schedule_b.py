"""Track 2 deliverables 5-8 authoritative-surface goldens: the complete
Schedule B attachment (existence conditional, collect_members itemization,
the tie-out invariant, Part III completeness), entering exclusively through
``live_coordinate_run`` from an authoritative act log (never a ``RunContext``
shortcut) - the charter's mandatory verification shape.

The package under test is ``tax.us.2025.package.core-calculations`` v5
(tools/generate_dsbs_t2_schedule_b_content.py), adopted via
``packages/sample_data/frrs_t3/adoptions/adopt-core-v5-current.json`` at
scope year 2054 - a distinct synthetic scope from the v4 goldens in
tests/test_dsbs_t2_coordinator.py, so both packages stay independently
exercisable.

Every fixture keeps taxable interest at a closure-backed zero (no 1099-INT
box-1 member is ever asserted); the $1,500 threshold is crossed through
ordinary dividends alone. This still exercises both itemization paths in one
run: Part I (interest) ties out an *empty* row set against a closure-backed
zero line, Part II (dividends) ties out a *non-empty* row set against a
computed line - the scope-bounded simplification documented on
rule.attachment.schedule-b.json (Part I itemizes the box-1 family only, the
only interest family this milestone's fixtures ever populate).
"""

from __future__ import annotations

import json
import unittest
from decimal import Decimal
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any, cast

from packages.derivation.live import live_coordinate_run
from packages.derivation.live_workspace import WorkspaceCapability
from packages.derivation.loader import DerivationSchemas, load_canon
from packages.derivation.production_resolver import PublicationSurface
from packages.derivation.runner import (
    InputFinding,
    RunContext,
    SourceFact,
    run,
)
from packages.derivation.runner import ITEMIZATION_TIE_OUT_VIOLATION
from packages.derivation.source_authority import ClosureFindingRecord

REPO = Path(__file__).resolve().parent.parent
CONTENT = REPO / "packages" / "content" / "tax" / "2025"
T3 = REPO / "packages" / "sample_data" / "frrs_t3"
USER = "demo.user.filer-1"
SCOPE = {"jurisdiction": "us", "year": "2054"}

ATTACHMENT_RULE = "tax.us.2025.rule.attachment.schedule-b"
LINE_3B_RULE = "tax.us.2025.rule.form1040-line3b"
FOREIGN_ACCOUNT_SYMBOL = "tax.us.2025.scheduleb.foreign-account"
FOREIGN_TRUST_SYMBOL = "tax.us.2025.scheduleb.foreign-trust"
COUNTRY_SYMBOL = "tax.us.2025.scheduleb.7b-country"


def _act(name: str) -> dict[str, object]:
    return cast(dict[str, object], json.loads((T3 / "adoptions" / name).read_text("utf-8")))


def _surface() -> PublicationSurface:
    return PublicationSurface(
        T3 / "publication_surface" / "releases", CONTENT / "published-packages.json", CONTENT
    )


def _live_act(index: int, kind: str, payload: dict[str, object]) -> dict[str, object]:
    return {
        "schema": "act.v1",
        "act_id": f"demo.dsbs.t2.schb.act.{index:03d}",
        "kind": kind,
        "actor": USER,
        "at": f"2026-07-19T01:00:{index:02d}Z",
        "committed_against": index,
        "payload": payload,
    }


def _attested_finding(finding_id: str, fact_id: str, value: object) -> dict[str, object]:
    return {"schema": "finding.v1", "id": finding_id, "fact_id": fact_id, "value": value, "basis": "attested", "evidence_ids": []}


def _schedule_b_acts(
    *,
    box1a: float | None = None,
    close_1a: bool = True,
    box1_interest: float | None = None,
    box3_interest: float | None = None,
    foreign_account: str | None = None,
    foreign_trust: str | None = None,
    country: str | None = None,
) -> list[dict[str, object]]:
    """A complete synthetic live record for the v5 package.

    ``box1a`` is the single demo statement's ordinary-dividend box amount
    (``None`` means no member is recorded). ``box1_interest``/
    ``box3_interest`` are 1099-INT amounts - present concurrently, they
    regression-cover F1 (Part I's tie-out target must be the box-1 subtotal
    alone, never line 2b's four-family sum, or a non-zero box-3 balance
    would spuriously fire ITEMIZATION_TIE_OUT_VIOLATION against a correctly
    computed return). ``foreign_account``/``foreign_trust``/``country`` are
    the Part III answers - ``None`` means that answer is never asserted
    (the absence golden).
    """
    acts: list[dict[str, object]] = []

    def add(kind: str, payload: dict[str, object]) -> None:
        acts.append(_live_act(len(acts), kind, payload))

    for name in (
        "w2.bundle.v3.json",
        "f1099int.bundle.json",
        "interest_composition.bundle.json",
        "core_calculations.bundle.v2.json",
        "f1099div.bundle.json",
        "scheduleb.bundle.json",
    ):
        add("bundle-adoption", {"bundle": json.loads((CONTENT / name).read_text())})

    add("entity-introduced", {"entity": {"schema": "entity.v1", "id": "demo.dsbs.t2.schb.employer", "kind": "tax.us.employer", "label": "Synthetic employer"}})
    add("entity-introduced", {"entity": {"schema": "entity.v1", "id": "demo.dsbs.t2.schb.w2", "kind": "tax.us.w2-slip", "label": "Synthetic W-2 slip"}})
    add("entity-introduced", {"entity": {"schema": "entity.v1", "id": "demo.dsbs.t2.schb.payer", "kind": "tax.us.dividend-payer", "label": "Synthetic dividend payer"}})
    add("entity-introduced", {"entity": {"schema": "entity.v1", "id": "demo.dsbs.t2.schb.stmt", "kind": "tax.us.1099div-statement", "label": "Synthetic 1099-DIV statement"}})
    if box1_interest is not None or box3_interest is not None:
        add("entity-introduced", {"entity": {"schema": "entity.v1", "id": "demo.dsbs.t2.schb.int-payer", "kind": "tax.us.interest-payer", "label": "Synthetic interest payer"}})
        add("entity-introduced", {"entity": {"schema": "entity.v1", "id": "demo.dsbs.t2.schb.int-stmt", "kind": "tax.us.1099int-statement", "label": "Synthetic 1099-INT statement"}})

    scope = {"tax-year": "2025", "subject": "demo.primary"}
    families = (
        ("tax.us.2025.w2", "v2", "demo.dsbs.t2.schb.w2.h0"),
        ("tax.us.2025.f1099int.b1", "v1", "demo.dsbs.t2.schb.int-b1.h0"),
        ("tax.us.2025.f1099int.b3", "v1", "demo.dsbs.t2.schb.int-b3.h0"),
        ("tax.us.2025.f1099oid.b1", "v1", "demo.dsbs.t2.schb.oid-b1.h0"),
        ("tax.us.2025.non-form-interest", "v1", "demo.dsbs.t2.schb.nonform.h0"),
        ("tax.us.2025.f1099div.1a", "v1", "demo.dsbs.t2.schb.div1a.h0"),
        ("tax.us.2025.f1099div.1b", "v1", "demo.dsbs.t2.schb.div1b.h0"),
    )
    for family_id, version, horizon_id in families:
        add("horizon-genesis", {"family": {"id": family_id, "version": version}, "scope": scope, "horizon_id": horizon_id})

    div1a_horizon = "demo.dsbs.t2.schb.div1a.h0"
    if box1a is not None:
        add("member-transition", {
            "family": {"id": "tax.us.2025.f1099div.1a", "version": "v1"},
            "scope": scope,
            "member": {"action": "assert", "finding": {
                "schema": "finding.v2", "id": "demo.dsbs.t2.schb.finding.box1a",
                "fact_id": "tax.us.2025.f1099div.box1a-ordinary|payer=demo.dsbs.t2.schb.payer,statement=demo.dsbs.t2.schb.stmt,tax-year=2025",
                "value": box1a, "basis": "attested", "evidence_ids": [],
            }},
            "successor": {"id": "demo.dsbs.t2.schb.div1a.h1", "predecessor": div1a_horizon},
        })
        div1a_horizon = "demo.dsbs.t2.schb.div1a.h1"

    int_b1_horizon = "demo.dsbs.t2.schb.int-b1.h0"
    if box1_interest is not None:
        add("member-transition", {
            "family": {"id": "tax.us.2025.f1099int.b1", "version": "v1"},
            "scope": scope,
            "member": {"action": "assert", "finding": {
                "schema": "finding.v2", "id": "demo.dsbs.t2.schb.finding.int-box1",
                "fact_id": "tax.us.2025.f1099int.box1-interest|payer=demo.dsbs.t2.schb.int-payer,statement=demo.dsbs.t2.schb.int-stmt,tax-year=2025",
                "value": box1_interest, "basis": "attested", "evidence_ids": [],
            }},
            "successor": {"id": "demo.dsbs.t2.schb.int-b1.h1", "predecessor": int_b1_horizon},
        })
        int_b1_horizon = "demo.dsbs.t2.schb.int-b1.h1"

    int_b3_horizon = "demo.dsbs.t2.schb.int-b3.h0"
    if box3_interest is not None:
        add("member-transition", {
            "family": {"id": "tax.us.2025.f1099int.b3", "version": "v1"},
            "scope": scope,
            "member": {"action": "assert", "finding": {
                "schema": "finding.v2", "id": "demo.dsbs.t2.schb.finding.int-box3",
                "fact_id": "tax.us.2025.f1099int.box3-interest|payer=demo.dsbs.t2.schb.int-payer,statement=demo.dsbs.t2.schb.int-stmt,tax-year=2025",
                "value": box3_interest, "basis": "attested", "evidence_ids": [],
            }},
            "successor": {"id": "demo.dsbs.t2.schb.int-b3.h1", "predecessor": int_b3_horizon},
        })
        int_b3_horizon = "demo.dsbs.t2.schb.int-b3.h1"

    add("assertion", {"finding": _attested_finding("demo.dsbs.t2.schb.finding.rounding", "rounding.convention|tax-year=2025", "half_up")})
    add("assertion", {"finding": _attested_finding("demo.dsbs.t2.schb.finding.status", "tax.us.2025.filing-status|tax-year=2025", "single")})

    if foreign_account is not None:
        add("assertion", {"finding": _attested_finding("demo.dsbs.t2.schb.finding.foreign-account", f"{FOREIGN_ACCOUNT_SYMBOL}|tax-year=2025", foreign_account)})
    if foreign_trust is not None:
        add("assertion", {"finding": _attested_finding("demo.dsbs.t2.schb.finding.foreign-trust", f"{FOREIGN_TRUST_SYMBOL}|tax-year=2025", foreign_trust)})
    if country is not None:
        add("assertion", {"finding": _attested_finding("demo.dsbs.t2.schb.finding.country", f"{COUNTRY_SYMBOL}|tax-year=2025", country)})

    closures = [
        ("demo.dsbs.t2.schb.closure.w2", "tax.us.2025.w2.source-closure", "demo.dsbs.t2.schb.w2.h0"),
        ("demo.dsbs.t2.schb.closure.int-b1", "tax.us.2025.f1099int.b1.source-closure", int_b1_horizon),
        ("demo.dsbs.t2.schb.closure.int-b3", "tax.us.2025.f1099int.b3.source-closure", int_b3_horizon),
        ("demo.dsbs.t2.schb.closure.oid-b1", "tax.us.2025.f1099oid.b1.source-closure", "demo.dsbs.t2.schb.oid-b1.h0"),
        ("demo.dsbs.t2.schb.closure.nonform", "tax.us.2025.non-form-interest.source-closure", "demo.dsbs.t2.schb.nonform.h0"),
        ("demo.dsbs.t2.schb.closure.div1b", "tax.us.2025.f1099div.1b.source-closure", "demo.dsbs.t2.schb.div1b.h0"),
    ]
    if close_1a:
        closures.append(("demo.dsbs.t2.schb.closure.div1a", "tax.us.2025.f1099div.1a.source-closure", div1a_horizon))
    for finding_id, fact_type, horizon_id in closures:
        add("assertion", {"finding": _attested_finding(finding_id, f"{fact_type}|family-horizon={horizon_id},tax-year=2025", True)})

    adoption = _act("adopt-core-v5-current.json")
    adoption["committed_against"] = len(acts)
    acts.append(adoption)
    return acts


def _run(acts: list[dict[str, object]], run_id: str) -> dict[str, Any]:
    with TemporaryDirectory() as tmp:
        root = Path(tmp)
        result = live_coordinate_run(
            WorkspaceCapability(root / "L"), repo_root=REPO, authoritative_acts=acts,
            workspace_revision=len(acts), run_scope=SCOPE, scope_user=USER,
            request={"schema": "run-request.v1"}, run_id=run_id, governance_pins=[],
            surface=_surface(), output_name="out.json",
        )
        assert result.refusal is None, result.refusal
        assert result.output_path is not None
        return cast(dict[str, Any], json.loads(result.output_path.read_text()))


def _by_artifact(report: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {row["artifact_id"]: row for row in report["dispositions"]}


class AttachmentCannotPropagateToALine(unittest.TestCase):
    """Deliverable 5: sibling line rules (2b/3a/3b/9) never reference the
    attachment symbol, so a blocked attachment cannot propagate to a line -
    verified against committed content, not just asserted."""

    def test_no_sibling_rule_names_the_attachment_symbol_anywhere(self) -> None:
        attachment_symbol = json.loads((CONTENT / "rule.attachment.schedule-b.json").read_text())["publishes"]
        siblings = (
            "rule.form1040-line2b.json",
            "rule.form1040-line3a.json",
            "rule.form1040-line3b.json",
            "rule.form1040-line9.v2.json",
        )
        for name in siblings:
            with self.subTest(name=name):
                text = (CONTENT / name).read_text()
                self.assertNotIn(attachment_symbol, text)


class NotRequired(unittest.TestCase):
    """Charter Verification item 3: not-required (both subtotals at or
    below the $1,500 threshold)."""

    def test_zero_dividends_and_zero_interest_is_not_required(self) -> None:
        report = _run(
            _schedule_b_acts(box1a=None, foreign_account="no", foreign_trust="no"),
            "demo.dsbs.t2.schb.not-required",
        )
        row = _by_artifact(report)[ATTACHMENT_RULE]
        self.assertEqual(row["disposition"], "inapplicable")
        self.assertEqual(row["guard_result"], False)
        # Walkable, never silent: the threshold parameter and citation are
        # named in the pins even though the attachment did not publish.
        pin_ids = {p["id"] for p in row["pins"]}
        self.assertIn("tax.us.2025.parameter.schedule-b-threshold", pin_ids)
        self.assertIn("tax.us.2025.citation.schedule-b", pin_ids)

    def test_exactly_at_threshold_is_not_required(self) -> None:
        # Boundary semantics: exactly $1,500 is not over (strictly greater
        # than only).
        report = _run(
            _schedule_b_acts(box1a=1500, foreign_account="no", foreign_trust="no"),
            "demo.dsbs.t2.schb.exactly-threshold",
        )
        row = _by_artifact(report)[ATTACHMENT_RULE]
        self.assertEqual(row["disposition"], "inapplicable")

    def test_missing_answers_never_block_when_not_required(self) -> None:
        # Not-required short-circuits before completeness is ever read - a
        # missing Part III answer cannot turn a not-required attachment into
        # a spurious block.
        report = _run(_schedule_b_acts(box1a=None), "demo.dsbs.t2.schb.not-required-no-answers")
        row = _by_artifact(report)[ATTACHMENT_RULE]
        self.assertEqual(row["disposition"], "inapplicable")


class RequiredAndComplete(unittest.TestCase):
    """Charter Verification item 4: required-and-complete (the whole form -
    Part I/II itemizations tying to 2b/3b, Part III both answers present)."""

    def test_both_answers_no_publishes_whole_form(self) -> None:
        # The live report's dispositions ledger (ADR-0020 decisions 1/1a) is
        # the authoritative non-publication *and* publication walk surface;
        # it exposes finding_id/act_id/symbol/pins but never a raw
        # publication value - so this golden verifies the walkable surface
        # (pins to every consumed fact). Exact content of the whole-form
        # value (rows, row-sums, obligations) is pinned down precisely by
        # the supplementary RunContext-level class below, over the same
        # committed attachment citizen - not a substitute for this golden.
        report = _run(
            _schedule_b_acts(box1a=2000, foreign_account="no", foreign_trust="no"),
            "demo.dsbs.t2.schb.complete-both-no",
        )
        rows = _by_artifact(report)
        row = rows[ATTACHMENT_RULE]
        self.assertEqual(row["disposition"], "published")
        self.assertIn("finding_id", row)
        self.assertIn("act_id", row)
        self.assertEqual(row["symbol"], "tax.us.2025.scheduleb.disposition")
        # Pinned to every consumed fact: the dividend row's own finding id,
        # both Part III answers, the 3b line finding, the citation, the
        # threshold parameter.
        pin_ids = {p["id"] for p in row["pins"]}
        self.assertIn(rows[LINE_3B_RULE]["finding_id"], pin_ids)
        self.assertIn("demo.dsbs.t2.schb.finding.box1a", pin_ids)
        self.assertIn("demo.dsbs.t2.schb.finding.foreign-account", pin_ids)
        self.assertIn("demo.dsbs.t2.schb.finding.foreign-trust", pin_ids)
        self.assertIn("tax.us.2025.citation.schedule-b", pin_ids)
        self.assertIn("tax.us.2025.parameter.schedule-b-threshold", pin_ids)

    def test_foreign_account_yes_names_fincen_obligation_and_requires_7b(self) -> None:
        report = _run(
            _schedule_b_acts(box1a=2000, foreign_account="yes", foreign_trust="no", country="gb"),
            "demo.dsbs.t2.schb.complete-yes-branch",
        )
        row = _by_artifact(report)[ATTACHMENT_RULE]
        self.assertEqual(row["disposition"], "published")
        pin_ids = {p["id"] for p in row["pins"]}
        self.assertIn("demo.dsbs.t2.schb.finding.foreign-account", pin_ids)
        self.assertIn("demo.dsbs.t2.schb.finding.country", pin_ids)


class PartIInterestTieOutWithConcurrentNonBox1Interest(unittest.TestCase):
    """Regression for F1 (2026-07-19 independent review): Part I's tie-out
    target must be the box-1 subtotal alone (tax.us.2025.interest.b1-
    subtotal), never line 2b's four-family taxable-interest total. Every
    other Track 2 golden holds box-3/OID/non-form interest at a closure-
    backed zero, so this is the only test where line 2b's value and the
    box-1 subtotal genuinely diverge - exactly the input combination that
    silently misfired before the fix."""

    def test_concurrent_box1_and_box3_interest_does_not_spuriously_tie_out_violate(self) -> None:
        report = _run(
            _schedule_b_acts(
                box1a=2000, box1_interest=300, box3_interest=150,
                foreign_account="no", foreign_trust="no",
            ),
            "demo.dsbs.t2.schb.concurrent-interest",
        )
        rows = _by_artifact(report)
        # Line 2b genuinely composes both families: 300 + 150 = 450, not 300.
        self.assertEqual(rows["tax.us.2025.rule.form1040-line2b"]["disposition"], "published")
        row = rows[ATTACHMENT_RULE]
        self.assertEqual(row["disposition"], "published")
        self.assertNotEqual(row.get("code"), ITEMIZATION_TIE_OUT_VIOLATION)
        # Part I's row pins the box-1 finding only, never the box-3 one -
        # the itemization's own scope is honestly box-1-only, and its
        # tie-out target must agree with that scope, not with line 2b's
        # wider composition.
        pin_ids = {p["id"] for p in row["pins"]}
        self.assertIn("demo.dsbs.t2.schb.finding.int-box1", pin_ids)
        self.assertNotIn("demo.dsbs.t2.schb.finding.int-box3", pin_ids)


class RequiredAndIncomplete(unittest.TestCase):
    """Charter Verification item 5: required-and-incomplete - honest block
    naming exactly the missing required answer(s), independently for each
    answer absent alone and both absent together."""

    def test_foreign_account_absent_alone_names_only_that_answer(self) -> None:
        report = _run(
            _schedule_b_acts(box1a=2000, foreign_trust="no"),
            "demo.dsbs.t2.schb.missing-account-only",
        )
        row = _by_artifact(report)[ATTACHMENT_RULE]
        self.assertEqual(row["disposition"], "blocked")
        self.assertEqual(row["code"], "DEPENDENCY_ABSENT")
        self.assertEqual(row["missing"], [FOREIGN_ACCOUNT_SYMBOL])

    def test_foreign_trust_absent_alone_names_only_that_answer(self) -> None:
        # Presence is checked independently before any value is read: one
        # answer's absence never masks evaluation of the other.
        report = _run(
            _schedule_b_acts(box1a=2000, foreign_account="no"),
            "demo.dsbs.t2.schb.missing-trust-only",
        )
        row = _by_artifact(report)[ATTACHMENT_RULE]
        self.assertEqual(row["disposition"], "blocked")
        self.assertEqual(row["code"], "DEPENDENCY_ABSENT")
        self.assertEqual(row["missing"], [FOREIGN_TRUST_SYMBOL])

    def test_both_answers_absent_names_both(self) -> None:
        report = _run(_schedule_b_acts(box1a=2000), "demo.dsbs.t2.schb.missing-both")
        row = _by_artifact(report)[ATTACHMENT_RULE]
        self.assertEqual(row["disposition"], "blocked")
        self.assertEqual(row["code"], "DEPENDENCY_ABSENT")
        self.assertEqual(sorted(row["missing"]), sorted([FOREIGN_ACCOUNT_SYMBOL, FOREIGN_TRUST_SYMBOL]))

    def test_foreign_account_yes_without_7b_country_blocks_naming_it(self) -> None:
        report = _run(
            _schedule_b_acts(box1a=2000, foreign_account="yes", foreign_trust="no"),
            "demo.dsbs.t2.schb.missing-7b",
        )
        row = _by_artifact(report)[ATTACHMENT_RULE]
        self.assertEqual(row["disposition"], "blocked")
        self.assertEqual(row["code"], "DEPENDENCY_ABSENT")
        self.assertEqual(row["missing"], [COUNTRY_SYMBOL])

    def test_open_dividend_family_blocks_on_the_subtotal_symbol(self) -> None:
        # No completeness evaluation is even reached: the requirement
        # conditional itself cannot resolve without its subtotal symbols.
        report = _run(
            _schedule_b_acts(box1a=2000, close_1a=False, foreign_account="no", foreign_trust="no"),
            "demo.dsbs.t2.schb.open-family",
        )
        row = _by_artifact(report)[ATTACHMENT_RULE]
        self.assertEqual(row["disposition"], "blocked")
        self.assertEqual(row["code"], "DEPENDENCY_ABSENT")
        self.assertEqual(row["missing"], ["tax.us.2025.dividends.ordinary-total"])


class WholeFormValueContent(unittest.TestCase):
    """Supplementary coverage over the same committed attachment citizen, at
    the RunContext/evaluator level (not a substitute for the
    live_coordinate_run goldens above - those are the authoritative
    surface): pins down the exact whole-form value content the live
    report's dispositions ledger does not expose (rows, row-sums,
    tie-outs, answers, named obligations)."""

    def setUp(self) -> None:
        self.schemas = DerivationSchemas()
        self.canon = load_canon(self.schemas)
        self.family_1a = json.loads((CONTENT / "family.f1099div-1a.json").read_text())
        self.mapping_1a = json.loads((CONTENT / "closure-mapping.f1099div-1a.json").read_text())
        self.attachment = json.loads((CONTENT / "rule.attachment.schedule-b.json").read_text())
        self.threshold = json.loads((CONTENT / "parameter.schedule-b-threshold.json").read_text())

    def _context(self, *, foreign_account: str, country: str | None) -> RunContext:
        inputs = [
            InputFinding("tax.us.2025.interest.taxable-total", "0", "demo.int.zero", "input"),
            # Part I's tie-out target is the box-1 subtotal alone (F1 fix,
            # 2026-07-19), not the requirement conditional's taxable-total
            # input above - both must be supplied since attempt_attachment
            # reads them for two different purposes (threshold vs. tie-out).
            InputFinding("tax.us.2025.interest.b1-subtotal", "0", "demo.int.b1.zero", "input"),
            InputFinding("tax.us.2025.dividends.ordinary-total", "2000", "demo.div3b", "input"),
            InputFinding(FOREIGN_ACCOUNT_SYMBOL, foreign_account, "demo.fa", "input"),
            InputFinding(FOREIGN_TRUST_SYMBOL, "no", "demo.ft", "input"),
        ]
        if country is not None:
            inputs.append(InputFinding(COUNTRY_SYMBOL, country, "demo.country", "input"))
        return RunContext(
            run_id="demo.dsbs.t2.schb.value-content",
            rules=[self.attachment],
            parameters={"tax.us.2025.parameter.schedule-b-threshold": self.threshold},
            canon=self.canon,
            inputs=inputs,
            sources=[SourceFact("tax.us.2025.f1099div.box1a-ordinary", "2000", "demo.row.box1a")],
            adoption_pin={"role": "adoption", "id": "tax.us.2025.package.core-calculations", "version": "v5"},
            governance_pins=[],
            family_declarations=[self.family_1a],
            closure_mappings=[self.mapping_1a],
            closure_findings=[ClosureFindingRecord("demo.closure.1a", "tax.us.2025.f1099div.1a.source-closure", "demo.h1a", True)],
            current_horizons={self.family_1a["id"]: "demo.h1a"},
        )

    def test_both_no_whole_form_content(self) -> None:
        ctx = self._context(foreign_account="no", country=None)
        result = run(ctx, self.schemas)
        pub = next(p for p in result.publications if p.finding["symbol"] == self.attachment["publishes"])
        content = pub.finding["value"]
        self.assertTrue(content["required"])
        self.assertEqual(content["answers"][FOREIGN_ACCOUNT_SYMBOL], "no")
        self.assertEqual(content["answers"][FOREIGN_TRUST_SYMBOL], "no")
        self.assertNotIn(COUNTRY_SYMBOL, content["answers"])
        self.assertEqual(content["named_obligations"], [])
        parts = {p["part_id"]: p for p in content["itemizations"]}
        self.assertEqual(parts["part-i-interest"]["rows"], [])
        self.assertEqual(parts["part-i-interest"]["row_sum"], "0")
        self.assertEqual(parts["part-ii-ordinary-dividends"]["rows"], [{"finding_id": "demo.row.box1a", "value": "2000"}])
        self.assertEqual(parts["part-ii-ordinary-dividends"]["row_sum"], "2000")
        self.assertEqual(parts["part-ii-ordinary-dividends"]["tie_out"], {"line_symbol": "tax.us.2025.dividends.ordinary-total", "line_value": "2000"})

    def test_yes_branch_names_fincen_obligation_never_produces_it(self) -> None:
        ctx = self._context(foreign_account="yes", country="gb")
        result = run(ctx, self.schemas)
        pub = next(p for p in result.publications if p.finding["symbol"] == self.attachment["publishes"])
        content = pub.finding["value"]
        self.assertEqual(content["answers"][COUNTRY_SYMBOL], "gb")
        self.assertEqual(content["named_obligations"], [{
            "code": "FINCEN_114_NAMED",
            "label": "Foreign Bank Account Report (FinCEN Form 114 / FBAR) obligation named; "
                     "this product never produces FinCEN-114 content or a filing artifact of any kind.",
        }])
        # Never produces FinCEN-114 content: the named obligation is text
        # only - no form/field/filing key anywhere in the published value.
        serialized = json.dumps(content)
        for forbidden in ("form_id", "\"form\":", "\"fields\":"):
            self.assertNotIn(forbidden, serialized)


class TieOutInvariant(unittest.TestCase):
    """Charter Verification item 6 (tie-out half): both named kill-tests at
    the RunContext/evaluator level, since the defect - a fabricated
    divergence between a subtotal's published value and its own itemization
    rows - is not expressible through an honest authoritative act log (a
    correctly-computed run can never disagree with itself); this is the
    charter's named allowance for a runner-level test.
    """

    def setUp(self) -> None:
        self.schemas = DerivationSchemas()
        self.canon = load_canon(self.schemas)
        self.family_1a = json.loads((CONTENT / "family.f1099div-1a.json").read_text())
        self.mapping_1a = json.loads((CONTENT / "closure-mapping.f1099div-1a.json").read_text())
        self.attachment = json.loads((CONTENT / "rule.attachment.schedule-b.json").read_text())
        self.threshold = json.loads((CONTENT / "parameter.schedule-b-threshold.json").read_text())

    def _context(self, *, dividend_line_value: str, dividend_rows: list[SourceFact]) -> RunContext:
        return RunContext(
            run_id="demo.dsbs.t2.schb.tieout",
            rules=[self.attachment],
            parameters={"tax.us.2025.parameter.schedule-b-threshold": self.threshold},
            canon=self.canon,
            inputs=[
                InputFinding("tax.us.2025.interest.taxable-total", "0", "demo.int.zero", "input"),
                InputFinding("tax.us.2025.interest.b1-subtotal", "0", "demo.int.b1.zero", "input"),
                InputFinding("tax.us.2025.dividends.ordinary-total", dividend_line_value, "demo.div3b", "input"),
                InputFinding(FOREIGN_ACCOUNT_SYMBOL, "no", "demo.fa", "input"),
                InputFinding(FOREIGN_TRUST_SYMBOL, "no", "demo.ft", "input"),
            ],
            sources=dividend_rows,
            adoption_pin={"role": "adoption", "id": "tax.us.2025.package.core-calculations", "version": "v5"},
            governance_pins=[],
            family_declarations=[self.family_1a],
            closure_mappings=[self.mapping_1a],
            closure_findings=[ClosureFindingRecord("demo.closure.1a", "tax.us.2025.f1099div.1a.source-closure", "demo.h1a", True)],
            current_horizons={self.family_1a["id"]: "demo.h1a"},
        )

    def test_stale_row_set_a_row_superseded_after_subtotal_but_before_tie_out(self) -> None:
        # The published line value (2000, over the $1,500 threshold) reflects
        # a row that has since been superseded to a different value (1600) -
        # the row set is stale relative to the line it was summed into.
        ctx = self._context(
            dividend_line_value="2000",
            dividend_rows=[SourceFact("tax.us.2025.f1099div.box1a-ordinary", "1600", "demo.row.superseded")],
        )
        result = run(ctx, self.schemas)
        rows = {row["artifact_id"]: row for row in result.dispositions}
        row = rows[self.attachment["id"]]
        self.assertEqual(row["disposition"], "blocked")
        self.assertEqual(row["code"], ITEMIZATION_TIE_OUT_VIOLATION)
        self.assertFalse(any(p.finding["symbol"] == self.attachment["publishes"] for p in result.publications))

    def test_stale_line_the_published_line_value_superseded_independent_of_the_itemization(self) -> None:
        # The rows sum honestly to 2500 (over threshold), but the line
        # symbol carries a value (3000) from a supersession the itemization
        # never saw - the line is the stale side this time.
        ctx = self._context(
            dividend_line_value="3000",
            dividend_rows=[SourceFact("tax.us.2025.f1099div.box1a-ordinary", "2500", "demo.row.current")],
        )
        result = run(ctx, self.schemas)
        rows = {row["artifact_id"]: row for row in result.dispositions}
        row = rows[self.attachment["id"]]
        self.assertEqual(row["disposition"], "blocked")
        self.assertEqual(row["code"], ITEMIZATION_TIE_OUT_VIOLATION)

    def test_tying_rows_publish_clean(self) -> None:
        ctx = self._context(
            dividend_line_value="2500",
            dividend_rows=[SourceFact("tax.us.2025.f1099div.box1a-ordinary", "2500", "demo.row.clean")],
        )
        result = run(ctx, self.schemas)
        rows = {row["artifact_id"]: row for row in result.dispositions}
        self.assertEqual(rows[self.attachment["id"]]["disposition"], "published")


if __name__ == "__main__":
    unittest.main()
