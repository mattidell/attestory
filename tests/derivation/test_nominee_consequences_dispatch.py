"""ADR-0074 coordinator smoke: intercept, C0/C1/C4/C13 ledger rows."""

from __future__ import annotations

import json
import unittest
from pathlib import Path
from typing import Any

import tempfile

from packages.derivation.loader import DerivationSchemas
from packages.derivation.records import CURRENT_RECORD_SCHEMA, RecordStream
from dataclasses import replace

from packages.derivation.runner import RunContext, SourceFact, run, run_and_record
from packages.tax.nominee_allocation_recording import derive_nominee_allocation_fact_id
from packages.tax.nominee_consequences import (
    NomineeIdentityError,
    NOMINEE_ALLOCATIONS_EXCEED_REPORT,
    PUBLISHES,
    RULE_ID,
)
from packages.tax.report_statement_identity import (
    REPORT_FACT_TYPE,
    derive_1099int_box1_fact_id,
    derive_reported_payer_entity_id,
    derive_reported_statement_entity_id,
)

CONTENT = Path(__file__).resolve().parents[2] / "packages" / "content" / "tax" / "2025"
ADOPTION = {"role": "adoption", "id": "demo.package.nominee", "version": "v1"}
GOVERNANCE = [{"role": "governance", "id": "governance.constitution", "version": "v1"}]
PAYER = "demo.payer.a"
STMT = "demo.stmt.a"
YEAR = 2025


def _rule() -> dict[str, Any]:
    loaded: dict[str, Any] = json.loads(
        (CONTENT / "rule.interest.nominee-reduction.json").read_text("utf-8")
    )
    return loaded


def _report_keys(payer_name: str, statement_reference: str, tax_year: int) -> tuple[tuple[str, str], ...]:
    """The kernel lattice's structured bindings for a box-1 report fact."""
    return (
        ("payer", derive_reported_payer_entity_id(payer_name)),
        (
            "statement",
            derive_reported_statement_entity_id(
                payer_name=payer_name, statement_reference=statement_reference
            ),
        ),
        ("tax-year", str(tax_year)),
    )


def _alloc_keys(
    payer_name: str, statement_reference: str, tax_year: int, recipient_id: str
) -> tuple[tuple[str, str], ...]:
    return _report_keys(payer_name, statement_reference, tax_year) + (("recipient", recipient_id),)


def _report_source(
    value: str, finding_id: str, *, payer_name: str, statement_reference: str, tax_year: int = YEAR
) -> SourceFact:
    return SourceFact(
        REPORT_FACT_TYPE,
        value,
        finding_id,
        derive_1099int_box1_fact_id(
            payer_name=payer_name, statement_reference=statement_reference, tax_year=tax_year
        ),
        keys=_report_keys(payer_name, statement_reference, tax_year),
    )


def _alloc_source(
    value: str,
    finding_id: str,
    *,
    payer_name: str,
    statement_reference: str,
    recipient_id: str,
    tax_year: int = YEAR,
) -> SourceFact:
    return SourceFact(
        "tax.us.nominee-allocation.amount",
        value,
        finding_id,
        derive_nominee_allocation_fact_id(
            payer_name=payer_name,
            statement_reference=statement_reference,
            tax_year=tax_year,
            recipient_id=recipient_id,
        ),
        keys=_alloc_keys(payer_name, statement_reference, tax_year, recipient_id),
    )


def _ctx(sources: list[SourceFact]) -> RunContext:
    return RunContext(
        run_id="demo.run.nominee-dispatch",
        rules=[_rule()],
        parameters={},
        canon={},
        inputs=[],
        sources=sources,
        adoption_pin=ADOPTION,
        governance_pins=GOVERNANCE,
        reporting_year=YEAR,
    )


class NomineeConsequencesDispatch(unittest.TestCase):
    def setUp(self) -> None:
        self.schemas = DerivationSchemas()
        self.report_fact_id = derive_1099int_box1_fact_id(
            payer_name=PAYER, statement_reference=STMT, tax_year=YEAR
        )
        self.pat_fact_id = derive_nominee_allocation_fact_id(
            payer_name=PAYER, statement_reference=STMT, tax_year=YEAR, recipient_id="demo.pat"
        )
        self.kim_fact_id = derive_nominee_allocation_fact_id(
            payer_name=PAYER, statement_reference=STMT, tax_year=YEAR, recipient_id="demo.kim"
        )
        self.report_keys = _report_keys(PAYER, STMT, YEAR)
        self.pat_keys = _alloc_keys(PAYER, STMT, YEAR, "demo.pat")
        self.kim_keys = _alloc_keys(PAYER, STMT, YEAR, "demo.kim")
        self.suffix = f"{PUBLISHES}|{self.report_fact_id}"

    def test_c1_publishes_450(self) -> None:
        result = run(
            _ctx(
                [
                    SourceFact(REPORT_FACT_TYPE, "1200", "demo.f.box1.a1", self.report_fact_id, keys=self.report_keys),
                    SourceFact(
                        "tax.us.nominee-allocation.amount",
                        "450",
                        "demo.f.pat.1",
                        self.pat_fact_id, keys=self.pat_keys,
                    ),
                ]
            ),
            self.schemas,
        )
        published = [p.finding for p in result.publications if p.finding["symbol"] == self.suffix]
        self.assertEqual(len(published), 1)
        self.assertEqual(published[0]["value"], "450")

    def test_c4_records_exceed_report_code(self) -> None:
        result = run(
            _ctx(
                [
                    SourceFact(REPORT_FACT_TYPE, "1200", "demo.f.box1.a1", self.report_fact_id, keys=self.report_keys),
                    SourceFact(
                        "tax.us.nominee-allocation.amount",
                        "800",
                        "demo.f.pat.1",
                        self.pat_fact_id, keys=self.pat_keys,
                    ),
                    SourceFact(
                        "tax.us.nominee-allocation.amount",
                        "450",
                        "demo.f.kim.1",
                        self.kim_fact_id, keys=self.kim_keys,
                    ),
                ]
            ),
            self.schemas,
        )
        rows = [row for row in result.dispositions if row["artifact_id"] == RULE_ID]
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["disposition"], "blocked")
        self.assertEqual(rows[0]["code"], NOMINEE_ALLOCATIONS_EXCEED_REPORT)
        self.assertEqual(rows[0]["missing"], [])
        self.assertEqual(rows[0]["symbol"], self.suffix)

    def test_c0_records_no_groups_selected(self) -> None:
        result = run(
            _ctx([SourceFact(REPORT_FACT_TYPE, "1200", "demo.f.box1.a1", self.report_fact_id, keys=self.report_keys)]),
            self.schemas,
        )
        rows = [row for row in result.dispositions if row["artifact_id"] == RULE_ID]
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["disposition"], "inapplicable")
        self.assertTrue(rows[0]["no_groups_selected"])
        self.assertEqual(rows[0]["symbol"], PUBLISHES)
        self.assertEqual(result.publications, [])

    def test_c13_dependency_absent_names_report_fact_id(self) -> None:
        result = run(
            _ctx(
                [
                    SourceFact(
                        "tax.us.nominee-allocation.amount",
                        "450",
                        "demo.f.pat.1",
                        self.pat_fact_id, keys=self.pat_keys,
                    )
                ]
            ),
            self.schemas,
        )
        rows = [row for row in result.dispositions if row["artifact_id"] == RULE_ID]
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["disposition"], "blocked")
        self.assertEqual(rows[0]["code"], "DEPENDENCY_ABSENT")
        self.assertEqual(rows[0]["missing"], [self.report_fact_id])
        self.assertEqual(rows[0]["symbol"], self.suffix)
        pin_ids = {p["id"] for p in rows[0]["pins"] if p["role"] == "input"}
        self.assertEqual(pin_ids, {"demo.f.pat.1"})

    def test_c3_publishes_450_and_pins_both_allocations(self) -> None:
        result = run(
            _ctx(
                [
                    SourceFact(REPORT_FACT_TYPE, "1200", "demo.f.box1.a1", self.report_fact_id, keys=self.report_keys),
                    SourceFact(
                        "tax.us.nominee-allocation.amount",
                        "300",
                        "demo.f.pat.1",
                        self.pat_fact_id, keys=self.pat_keys,
                    ),
                    SourceFact(
                        "tax.us.nominee-allocation.amount",
                        "150",
                        "demo.f.kim.1",
                        self.kim_fact_id, keys=self.kim_keys,
                    ),
                ]
            ),
            self.schemas,
        )
        published = [p.finding for p in result.publications if p.finding["symbol"] == self.suffix]
        self.assertEqual(len(published), 1)
        self.assertEqual(published[0]["value"], "450")
        pin_ids = {p["id"] for p in published[0]["pins"] if p["role"] == "input"}
        self.assertEqual(pin_ids, {"demo.f.box1.a1", "demo.f.pat.1", "demo.f.kim.1"})

    def test_c10_isolates_pins_and_grouped_ledger_rows(self) -> None:
        report_c = derive_1099int_box1_fact_id(
            payer_name="demo.payer.c", statement_reference="demo.stmt.c", tax_year=YEAR
        )
        report_c_keys = _report_keys("demo.payer.c", "demo.stmt.c", YEAR)
        sam_keys = _alloc_keys("demo.payer.c", "demo.stmt.c", YEAR, "demo.sam")
        sam = derive_nominee_allocation_fact_id(
            payer_name="demo.payer.c",
            statement_reference="demo.stmt.c",
            tax_year=YEAR,
            recipient_id="demo.sam",
        )
        suffix_c = f"{PUBLISHES}|{report_c}"
        result = run(
            _ctx(
                [
                    SourceFact(REPORT_FACT_TYPE, "1200", "demo.f.box1.a1", self.report_fact_id, keys=self.report_keys),
                    SourceFact(
                        "tax.us.nominee-allocation.amount",
                        "800",
                        "demo.f.pat.1",
                        self.pat_fact_id, keys=self.pat_keys,
                    ),
                    SourceFact(
                        "tax.us.nominee-allocation.amount",
                        "450",
                        "demo.f.kim.1",
                        self.kim_fact_id, keys=self.kim_keys,
                    ),
                    SourceFact(REPORT_FACT_TYPE, "1200", "demo.f.box1.c1", report_c, keys=report_c_keys),
                    SourceFact(
                        "tax.us.nominee-allocation.amount",
                        "400",
                        "demo.f.sam.1",
                        sam, keys=sam_keys,
                    ),
                ]
            ),
            self.schemas,
        )
        rule_rows = [row for row in result.dispositions if row["artifact_id"] == RULE_ID]
        # Grouped-ledger kill 2: exactly one row per selected disposition-group.
        # Assert the row COUNT before collapsing by symbol -- a dict keyed on
        # symbol silently merges a duplicate group outcome, which is the very
        # condition this kill exists to detect (Track 1 review, non-blocking 1).
        self.assertEqual(len(rule_rows), 2)
        by_symbol = {row["symbol"]: row for row in rule_rows}
        self.assertEqual(set(by_symbol), {self.suffix, suffix_c})
        self.assertEqual(by_symbol[self.suffix]["disposition"], "blocked")
        self.assertEqual(by_symbol[self.suffix]["code"], NOMINEE_ALLOCATIONS_EXCEED_REPORT)
        self.assertEqual(by_symbol[suffix_c]["disposition"], "published")
        published = [p.finding for p in result.publications if p.finding["symbol"] == suffix_c]
        self.assertEqual(len(published), 1)
        self.assertEqual(published[0]["value"], "400")
        a_pins = {p["id"] for p in by_symbol[self.suffix]["pins"] if p["role"] == "input"}
        c_pins = {p["id"] for p in published[0]["pins"] if p["role"] == "input"}
        self.assertNotIn("demo.f.sam.1", a_pins)
        self.assertNotIn("demo.f.pat.1", c_pins)
        self.assertNotIn("demo.f.kim.1", c_pins)
        self.assertIn("demo.f.sam.1", c_pins)

    def test_c4_closing_record_carries_exact_code(self) -> None:
        ctx = _ctx(
            [
                SourceFact(REPORT_FACT_TYPE, "1200", "demo.f.box1.a1", self.report_fact_id, keys=self.report_keys),
                SourceFact(
                    "tax.us.nominee-allocation.amount",
                    "800",
                    "demo.f.pat.1",
                    self.pat_fact_id, keys=self.pat_keys,
                ),
                SourceFact(
                    "tax.us.nominee-allocation.amount",
                    "450",
                    "demo.f.kim.1",
                    self.kim_fact_id, keys=self.kim_keys,
                ),
            ]
        )
        with tempfile.TemporaryDirectory() as tmp:
            stream = RecordStream(Path(tmp) / "workspace", self.schemas)
            run_and_record(
                ctx,
                self.schemas,
                stream,
                workspace_revision=1,
                adopted_packages={ADOPTION["id"]},
                start_record_id="demo.start.nominee-c4",
                completion_record_id="demo.done.nominee-c4",
            )
            closing = stream.standings()[ctx.run_id].closing
        assert closing is not None
        self.assertEqual(closing["schema"], CURRENT_RECORD_SCHEMA)
        rows = [row for row in closing["dispositions"] if row["artifact_id"] == RULE_ID]
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["code"], NOMINEE_ALLOCATIONS_EXCEED_REPORT)
        self.assertNotEqual(rows[0]["code"], "DEPENDENCY_INVALID")
        self.assertEqual(rows[0]["symbol"], self.suffix)
        self.assertEqual(rows[0]["missing"], [])

    def test_c0_grouped_ledger_xor(self) -> None:
        result = run(
            _ctx([SourceFact(REPORT_FACT_TYPE, "1200", "demo.f.box1.a1", self.report_fact_id, keys=self.report_keys)]),
            self.schemas,
        )
        rows = [row for row in result.dispositions if row["artifact_id"] == RULE_ID]
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["symbol"], PUBLISHES)
        self.assertTrue(rows[0].get("no_groups_selected"))
        self.assertFalse(any("|" in (row.get("symbol") or "") for row in rows))

    def test_cross_year_2024_allocation_does_not_contribute(self) -> None:
        lee_2024_keys = _alloc_keys(PAYER, STMT, 2024, "demo.lee")
        lee_2024 = derive_nominee_allocation_fact_id(
            payer_name=PAYER, statement_reference=STMT, tax_year=2024, recipient_id="demo.lee"
        )
        result = run(
            _ctx(
                [
                    SourceFact(REPORT_FACT_TYPE, "1200", "demo.f.box1.a1", self.report_fact_id, keys=self.report_keys),
                    SourceFact(
                        "tax.us.nominee-allocation.amount",
                        "450",
                        "demo.f.pat.1",
                        self.pat_fact_id, keys=self.pat_keys,
                    ),
                    SourceFact(
                        "tax.us.nominee-allocation.amount",
                        "800",
                        "demo.f.lee.1",
                        lee_2024, keys=lee_2024_keys,
                    ),
                ]
            ),
            self.schemas,
        )
        published = [p.finding for p in result.publications if p.finding["symbol"] == self.suffix]
        self.assertEqual(len(published), 1)
        self.assertEqual(published[0]["value"], "450")
        pin_ids = {p["id"] for p in published[0]["pins"] if p["role"] == "input"}
        self.assertNotIn("demo.f.lee.1", pin_ids)
        blocked = [row for row in result.dispositions if row.get("disposition") == "blocked"]
        for row in blocked:
            for missing in row.get("missing") or []:
                self.assertNotIn("tax-year=2024", missing)

    def test_c9_rule_declares_no_payment_or_legacy_nominee_dependency(self) -> None:
        rule = _rule()
        blob = json.dumps(rule)
        forbidden = (
            "tax.us.2025.scheduleb.adjustment.nominee.amount",
            "accrued_interest_paid_to_seller",
            "tax.us.2025.f1099div.box7-foreign-tax-paid",
            "tax.us.2025.quantity.foreign-tax-paid",
        )
        for name in forbidden:
            self.assertNotIn(name, blob)
            self.assertNotIn(name, rule.get("requires", []))


class NomineeIdentityTransport(unittest.TestCase):
    """Missing or inconsistent structured identity must fail LOUDLY.

    Each case previously produced a wrong tax answer presented as an ordinary
    one: the source was silently dropped by the year filter, so a real report
    became C0 or a real allocation vanished from the total and the pins.
    """

    def setUp(self) -> None:
        self.schemas = DerivationSchemas()
        self.report = _report_source(
            "1200", "demo.f.box1.a1", payer_name=PAYER, statement_reference=STMT
        )
        self.pat = _alloc_source(
            "300", "demo.f.pat.1", payer_name=PAYER, statement_reference=STMT,
            recipient_id="demo.pat",
        )
        self.kim = _alloc_source(
            "150", "demo.f.kim.1", payer_name=PAYER, statement_reference=STMT,
            recipient_id="demo.kim",
        )

    def _run(self, sources: list[SourceFact]) -> Any:
        return run(_ctx(sources), self.schemas)

    def test_all_unkeyed_refuses_instead_of_reporting_no_groups(self) -> None:
        """A report and a $450 allocation with keys=None previously gave C0."""
        sources = [
            replace(self.report, keys=None),
            replace(self.pat, value="450", keys=None),
        ]
        with self.assertRaises(NomineeIdentityError) as caught:
            self._run(sources)
        self.assertIn("no structured identity keys", str(caught.exception))

    def test_partially_unkeyed_refuses_instead_of_a_smaller_total(self) -> None:
        """$300 keyed + $150 unkeyed previously published $300 and lost a pin."""
        sources = [self.report, self.pat, replace(self.kim, keys=None)]
        with self.assertRaises(NomineeIdentityError):
            self._run(sources)

    def test_missing_identity_component_refuses(self) -> None:
        broken = replace(
            self.pat, keys=tuple(kv for kv in (self.pat.keys or ()) if kv[0] != "statement")
        )
        with self.assertRaises(NomineeIdentityError) as caught:
            self._run([self.report, broken])
        self.assertIn("missing identity component", str(caught.exception))

    def test_keys_and_fact_id_disagreement_refuses(self) -> None:
        disagreeing = replace(
            self.pat,
            keys=tuple(
                (name, "demo.other" if name == "recipient" else value)
                for name, value in (self.pat.keys or ())
            ),
        )
        with self.assertRaises(NomineeIdentityError) as caught:
            self._run([self.report, disagreeing])
        self.assertIn("disagree with its fact_id", str(caught.exception))

    def test_unexpected_identity_component_refuses(self) -> None:
        """An extra binding is a different proposition, not a harmless extra.

        A fact type's declared identity keys individuate it. A source carrying
        a component the type does not declare is not the fact this coordinator
        thinks it is, so accepting it would compute a report-scoped tax result
        for an identity the report never had.
        """
        extra = replace(self.pat, keys=(self.pat.keys or ()) + (("scenario", "demo.s1"),))
        with self.assertRaises(NomineeIdentityError) as caught:
            self._run([self.report, extra])
        self.assertIn("unexpected identity component", str(caught.exception))

    def test_missing_fact_id_refuses(self) -> None:
        """Bindings with no fact_id cannot be checked for agreement.

        _validated_keys proves keys and fact_id render to the same string. With
        no fact_id there is nothing to agree with, so the consistency check
        cannot run and the source must not be trusted by default.
        """
        no_fact_id = replace(self.pat, fact_id=None)
        with self.assertRaises(NomineeIdentityError) as caught:
            self._run([self.report, no_fact_id])
        self.assertIn("no fact_id", str(caught.exception))

    def test_ambiguously_rendered_identity_refuses(self) -> None:
        """The rendering is non-injective; refuse rather than guess.

        ``facts._fact_id`` joins on "," without escaping, so a component value
        containing ``,<keyname>=`` can render identically to a different tuple
        of bindings. Structured keys do not repair that -- the kernel lattice
        is itself keyed on the collided rendering. Track 1 is limited to
        uniquely rendered identities.
        """
        payer = "a,statement=a::statement::b"
        collided = _report_source(
            "1200", "demo.f.box1.x", payer_name=payer, statement_reference="c"
        )
        with self.assertRaises(NomineeIdentityError) as caught:
            self._run([collided])
        self.assertIn("ambiguously rendered", str(caught.exception))

    def test_unscoped_run_refuses_rather_than_excluding_everything(self) -> None:
        ctx = replace(_ctx([self.report, self.pat]), reporting_year=None)
        with self.assertRaises(NomineeIdentityError) as caught:
            run(ctx, self.schemas)
        self.assertIn("no reporting year", str(caught.exception))


if __name__ == "__main__":
    unittest.main()
