"""Track 1: 2025 tax on taxable income, proved through the real coordinator.

Worksheet lines are read from the publications the successor rules emit.
Expected tax figures are the plan's hand-computed case values.
"""

from __future__ import annotations

import importlib.util
import json
from decimal import Decimal
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any

import unittest

from packages.derivation.live import live_coordinate_run
from packages.derivation.live_workspace import WorkspaceCapability
from packages.derivation.production_resolver import PublicationSurface

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "packages" / "content" / "tax" / "2025"
RELEASE_DIR = (
    ROOT
    / "packages"
    / "sample_data"
    / "student_loan_worksheet_integration"
    / "publication_surface"
    / "releases"
)
PACKAGE_V50 = CONTENT / "package.core-calculations.v50.json"
PACKAGE_V49 = CONTENT / "package.core-calculations.v49.json"
REGISTRY_V48 = CONTENT / "published-packages.v48.json"
REGISTRY_V47 = CONTENT / "published-packages.v47.json"
RELEASE_V48 = RELEASE_DIR / "demo.release.sli-worksheet-integration.2025.v48.json"
RELEASE_V47 = RELEASE_DIR / "demo.release.sli-worksheet-integration.2025.v47.json"
SURFACE_V50 = PublicationSurface(RELEASE_DIR, REGISTRY_V48, CONTENT)

def _line(number: int) -> str:
    return f"tax.us.2025.qdcg-worksheet.line-{number}"


TI = "tax.us.2025.income.taxable-income"
QD = "tax.us.2025.dividends.qualified-total"
PREF = "tax.us.2025.capital-gains.selected-preferential-base"
TOTAL = "tax.us.2025.tax.total-tax"
STD = "demo.form1040.standard_deduction"
LINE5 = _line(5)
LINE9 = _line(9)
LINE17 = _line(17)
LINE20 = _line(20)
LINE22 = _line(22)
LINE23 = _line(23)
LINE24 = _line(24)
LINE25 = _line(25)
ORD = "tax.us.2025.parameter.ordinary-rate-schedule"
ZERO_CEILING = "tax.us.2025.parameter.preferential-zero-ceiling"
FIFTEEN_CEILING = "tax.us.2025.parameter.preferential-fifteen-ceiling"
BOX2A = "tax.us.2025.dividends.2a-subtotal"
LINE12_CITE = "tax.us.2025.citation.form1040.line-12"
_WORKSHEET_LINES = (4, 5, *range(6, 26))

REMOVED = {
    ("demo.parameter.additional-deduction-rate.2025", "v1"),
    ("demo.parameter.qdcg-preferential-brackets.2025", "v2"),
    ("demo.parameter.standard-deduction-base.2025", "v1"),
    ("demo.parameter.tax-brackets.2025", "v2"),
    ("tax.us.2025.rule.form1040-line16", "v5"),
    ("tax.us.2025.rule.selected-preferential-base", "v4"),
    ("tax.us.2025.rule.form1040-standard-deduction", "v1"),
}
ADDED = {
    ("tax.us.2025.parameter.ordinary-rate-schedule", "v1"),
    ("tax.us.2025.parameter.preferential-zero-ceiling", "v1"),
    ("tax.us.2025.parameter.preferential-fifteen-ceiling", "v1"),
    ("tax.us.2025.parameter.standard-deduction-base", "v1"),
    ("tax.us.2025.parameter.additional-standard-deduction", "v1"),
    ("tax.us.2025.parameter.tax-table-ceiling", "v1"),
    (LINE12_CITE, "v1"),
    ("tax.us.2025.rule.form1040-line16", "v6"),
    ("tax.us.2025.rule.selected-preferential-base", "v5"),
    ("tax.us.2025.rule.form1040-standard-deduction", "v2"),
} | {
    (f"tax.us.2025.rule.qdcg-worksheet.line-{number}", "v1")
    for number in _WORKSHEET_LINES
}

_PROBE = None


def _probe() -> Any:
    global _PROBE
    if _PROBE is None:
        path = (
            ROOT
            / "docs"
            / "phases"
            / "engine-breadth"
            / "milestones"
            / "tax-on-taxable-income-evidence"
            / "probe.py"
        )
        spec = importlib.util.spec_from_file_location("toti_track1_probe", path)
        if spec is None or spec.loader is None:
            raise RuntimeError("could not load the P0 probe helpers")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        _PROBE = module
    return _PROBE


def _finish_v50(acts: list[dict[str, object]], note: str) -> list[dict[str, object]]:
    import copy
    import hashlib

    probe = _probe()
    pkg = json.loads(PACKAGE_V50.read_text(encoding="utf-8"))
    rel_csum = hashlib.sha256(RELEASE_V48.read_bytes()).hexdigest()
    built = copy.deepcopy(acts)
    adoption = copy.deepcopy(probe._load_fixture_adoption())
    adoption["act_id"] = f"demo.toti.adopt.{len(built):03d}"
    payload = adoption["payload"]
    assert isinstance(payload, dict)
    payload["package"] = {
        "id": "tax.us.2025.package.core-calculations",
        "version": "v50",
        "checksum": pkg["package_checksum"],
    }
    payload["release"] = {
        "id": "demo.release.sli-worksheet-integration.2025",
        "version": "v48",
        "checksum": rel_csum,
    }
    payload["audit"] = {"note": note}
    built.append(adoption)
    for index, row in enumerate(built):
        row["committed_against"] = index
        row["actor"] = probe.USER
    return built


def _age(acts: list[dict[str, object]], **flags: bool) -> list[dict[str, object]]:
    import copy

    probe = _probe()
    built = copy.deepcopy(acts)
    facts = {
        "taxpayer_over_65": "tax.us.2025.taxpayer-over-65",
        "taxpayer_blind": "tax.us.2025.taxpayer-blind",
        "spouse_over_65": "tax.us.2025.spouse-over-65",
        "spouse_blind": "tax.us.2025.spouse-blind",
    }
    for name, fact_type in facts.items():
        if not flags.get(name):
            continue
        built.append(
            probe._act(
                len(built),
                "assertion",
                {
                    "finding": probe._attested(
                        f"demo.toti.{name}",
                        f"{fact_type}|tax-year=2025",
                        True,
                    )
                },
            )
        )
    return built


def _run(acts: list[dict[str, object]], run_id: str) -> tuple[dict[str, dict[str, Any]], list[dict[str, Any]]]:
    probe = _probe()
    with TemporaryDirectory() as tmp:
        outcome = live_coordinate_run(
            WorkspaceCapability(Path(tmp) / "L"),
            repo_root=ROOT,
            authoritative_acts=acts,
            workspace_revision=len(acts),
            run_scope={"jurisdiction": "us", "year": "2025"},
            scope_user=probe.USER,
            request={"schema": "run-request.v1"},
            run_id=run_id,
            governance_pins=[],
            surface=SURFACE_V50,
            output_name="out.json",
        )
        if outcome.refusal is not None:
            raise AssertionError(f"{run_id} refused: {outcome.refusal.reason} {outcome.refusal.detail}")
        pubs: dict[str, dict[str, Any]] = {}
        for pub in outcome.publications or ():
            pubs[str(pub.finding["symbol"])] = pub.finding
        blocked: list[dict[str, Any]] = []
        if outcome.output_path is not None:
            report = json.loads(outcome.output_path.read_text(encoding="utf-8"))
            for row in report.get("dispositions", []):
                if row.get("disposition") != "blocked":
                    continue
                artifact = str(row.get("artifact_id", ""))
                if any(token in artifact for token in ("qdcg", "line16", "standard-deduction", "preferential", "line15")):
                    blocked.append(row)
        return pubs, blocked


def _value(pubs: dict[str, dict[str, Any]], blocked: list[dict[str, Any]], symbol: str) -> Decimal:
    finding = pubs.get(symbol)
    if finding is None:
        raise AssertionError(f"missing {symbol}; blocked={blocked}")
    return Decimal(str(finding["value"]))


def _pins_parameter(finding: dict[str, Any], parameter_id: str) -> bool:
    return any(
        pin.get("role") == "parameter" and pin.get("id") == parameter_id
        for pin in finding.get("pins", [])
    )


def _pins_id(finding: dict[str, Any], finding_id: str) -> bool:
    return any(pin.get("id") == finding_id for pin in finding.get("pins", []))


def _assert_lines(
    pubs: dict[str, dict[str, Any]],
    blocked: list[dict[str, Any]],
    expected: dict[int, Decimal],
) -> None:
    for number, value in expected.items():
        if _value(pubs, blocked, _line(number)) != value:
            raise AssertionError(f"line {number}: {_value(pubs, blocked, _line(number))} != {value}")


def _wages(taxable: int, *, standard: int = 15750, other: int = 0) -> float:
    return float(taxable + standard - other)


class TaxOnTaxableIncomeTrack1Tests(unittest.TestCase):
    def _ordinary(self, taxable: int, run_id: str, *, status: str = "single", standard: int = 15750) -> tuple[dict[str, dict[str, Any]], list[dict[str, Any]]]:
        probe = _probe()
        acts = _finish_v50(
            probe._base_acts(wages=_wages(taxable, standard=standard), filing_status=status),
            f"synthetic {run_id}",
        )
        pubs, blocked = _run(acts, run_id)
        self.assertEqual(_value(pubs, blocked, TI), Decimal(taxable))
        return pubs, blocked

    def test_case_01_tax_table_46850(self) -> None:
        pubs, blocked = self._ordinary(46850, "demo.toti.case01")
        self.assertEqual(_value(pubs, blocked, TOTAL), Decimal(5387))

    def test_case_02_last_tax_table_band(self) -> None:
        pubs, blocked = self._ordinary(99999, "demo.toti.case02")
        self.assertEqual(_value(pubs, blocked, TOTAL), Decimal(16909))

    def test_case_03_tax_computation_worksheet(self) -> None:
        pubs, blocked = self._ordinary(100000, "demo.toti.case03")
        self.assertEqual(_value(pubs, blocked, LINE24), Decimal(16914))
        self.assertEqual(_value(pubs, blocked, TOTAL), Decimal(16914))

    def test_case_04_thirty_five_percent_bracket(self) -> None:
        pubs, blocked = self._ordinary(596850, "demo.toti.case04")
        self.assertEqual(_value(pubs, blocked, LINE24), Decimal("178444.75"))
        self.assertEqual(_value(pubs, blocked, TOTAL), Decimal(178445))

    def test_case_05_mfj(self) -> None:
        pubs, blocked = self._ordinary(150000, "demo.toti.case05", status="married_filing_jointly", standard=31500)
        self.assertEqual(_value(pubs, blocked, TOTAL), Decimal(22828))

    def test_case_06_bottom_rows(self) -> None:
        expected = {3: 0, 10: 1, 20: 2, 1000: 101, 2990: 299, 3000: 303}
        for taxable, tax in expected.items():
            pubs, blocked = self._ordinary(taxable, f"demo.toti.case06.{taxable}")
            self.assertEqual(_value(pubs, blocked, TOTAL), Decimal(tax), taxable)

    def test_case_07_qualified_dividends_zero_band(self) -> None:
        probe = _probe()
        acts = _finish_v50(
            probe._base_acts(
                wages=_wages(25000, other=5000),
                ordinary_dividends=5000,
                qualified_dividends=5000,
            ),
            "synthetic case 07",
        )
        pubs, blocked = _run(acts, "demo.toti.case07")
        self.assertEqual(_value(pubs, blocked, TI), Decimal(25000))
        self.assertEqual(_value(pubs, blocked, LINE5), Decimal(20000))
        self.assertEqual(_value(pubs, blocked, LINE22), Decimal(2165))
        self.assertEqual(_value(pubs, blocked, LINE24), Decimal(2765))
        self.assertEqual(_value(pubs, blocked, TOTAL), Decimal(2165))

    def test_case_08_straddle_zero_and_fifteen(self) -> None:
        probe = _probe()
        acts = _finish_v50(
            probe._base_acts(
                wages=_wages(54250, other=20000),
                ordinary_dividends=20000,
                qualified_dividends=20000,
            ),
            "synthetic case 08",
        )
        pubs, blocked = _run(acts, "demo.toti.case08")
        self.assertEqual(_value(pubs, blocked, TI), Decimal(54250))
        _assert_lines(pubs, blocked, {
            4: Decimal(20000),
            5: Decimal(34250),
            6: Decimal(48350),
            7: Decimal(48350),
            8: Decimal(34250),
            9: Decimal(14100),
            10: Decimal(20000),
            11: Decimal(14100),
            12: Decimal(5900),
            13: Decimal(533400),
            14: Decimal(54250),
            15: Decimal(48350),
            16: Decimal(5900),
            17: Decimal(5900),
            18: Decimal(885),
            19: Decimal(20000),
            20: Decimal(0),
            21: Decimal(0),
            22: Decimal(3875),
            23: Decimal(4760),
            24: Decimal(6855),
        })
        self.assertEqual(_value(pubs, blocked, TOTAL), Decimal(4760))
        self.assertTrue(_pins_id(pubs[LINE5], pubs[TI]["id"]))
        self.assertTrue(_pins_id(pubs[LINE5], pubs[QD]["id"]))
        self.assertTrue(_pins_id(pubs[LINE5], pubs[PREF]["id"]))
        self.assertTrue(_pins_parameter(pubs[_line(6)], ZERO_CEILING))
        self.assertTrue(_pins_parameter(pubs[_line(13)], FIFTEEN_CEILING))
        self.assertTrue(_pins_id(pubs[LINE9], pubs[_line(7)]["id"]))
        self.assertTrue(_pins_id(pubs[LINE9], pubs[_line(8)]["id"]))
        self.assertTrue(_pins_id(pubs[LINE17], pubs[_line(12)]["id"]))
        self.assertTrue(_pins_id(pubs[LINE17], pubs[_line(16)]["id"]))
        self.assertTrue(_pins_id(pubs[LINE22], pubs[LINE5]["id"]))
        self.assertTrue(_pins_parameter(pubs[LINE22], ORD))
        self.assertTrue(_pins_parameter(pubs[LINE24], ORD))
        self.assertTrue(_pins_id(pubs[LINE24], pubs[TI]["id"]))

    def test_case_09_straddle_fifteen_and_twenty(self) -> None:
        probe = _probe()
        acts = _finish_v50(
            probe._base_acts(
                wages=_wages(600000, other=100000),
                ordinary_dividends=100000,
                qualified_dividends=100000,
            ),
            "synthetic case 09",
        )
        pubs, blocked = _run(acts, "demo.toti.case09")
        self.assertEqual(_value(pubs, blocked, TI), Decimal(600000))
        _assert_lines(pubs, blocked, {
            4: Decimal(100000),
            6: Decimal(48350),
            7: Decimal(48350),
            8: Decimal(48350),
            9: Decimal(0),
            10: Decimal(100000),
            11: Decimal(0),
            12: Decimal(100000),
            13: Decimal(533400),
            14: Decimal(533400),
            15: Decimal(500000),
            16: Decimal(33400),
            17: Decimal(33400),
            18: Decimal(5010),
            19: Decimal(33400),
            20: Decimal(66600),
            21: Decimal(13320),
            22: Decimal("144547.25"),
            23: Decimal("162877.25"),
        })
        self.assertEqual(_value(pubs, blocked, LINE25), Decimal("162877.25"))
        self.assertEqual(_value(pubs, blocked, TOTAL), Decimal(162877))

    def test_case_10_short_term_gain_is_ordinary(self) -> None:
        probe = _probe()
        acts = _finish_v50(
            probe._splice_schedule_d_transactions(
                probe._base_acts(wages=90000),
                st=[(5000.0, 0.0)],
                lt=[(1000.0, 0.0)],
            ),
            "synthetic case 10",
        )
        pubs, blocked = _run(acts, "demo.toti.case10")
        self.assertEqual(_value(pubs, blocked, TI), Decimal(80250))
        self.assertEqual(_value(pubs, blocked, PREF), Decimal(1000))
        self.assertEqual(_value(pubs, blocked, LINE22), Decimal(12355))
        self.assertEqual(_value(pubs, blocked, LINE23), Decimal(12505))
        self.assertEqual(_value(pubs, blocked, TOTAL), Decimal(12505))

    def test_case_11_long_term_loss_zeros_the_base(self) -> None:
        probe = _probe()
        acts = _finish_v50(
            probe._splice_schedule_d_transactions(
                probe._base_acts(wages=50000),
                st=[(5000.0, 0.0)],
                lt=[(0.0, 2000.0)],
            ),
            "synthetic case 11",
        )
        pubs, blocked = _run(acts, "demo.toti.case11")
        self.assertEqual(_value(pubs, blocked, PREF), Decimal(0))

    def test_case_12_net_long_term_after_short_term_loss(self) -> None:
        probe = _probe()
        acts = _finish_v50(
            probe._splice_schedule_d_transactions(
                probe._base_acts(wages=50000),
                st=[(0.0, 1000.0)],
                lt=[(4000.0, 0.0)],
            ),
            "synthetic case 12",
        )
        pubs, blocked = _run(acts, "demo.toti.case12")
        self.assertEqual(_value(pubs, blocked, PREF), Decimal(3000))

    def test_case_13_standard_deduction_amounts(self) -> None:
        probe = _probe()
        scenarios: tuple[tuple[str, str, dict[str, bool], Decimal], ...] = (
            ("demo.toti.case13.single", "single", {}, Decimal(15750)),
            (
                "demo.toti.case13.mfj",
                "married_filing_jointly",
                {"taxpayer_over_65": True, "spouse_over_65": True},
                Decimal(34700),
            ),
            (
                "demo.toti.case13.single-blind-65",
                "single",
                {"taxpayer_over_65": True, "taxpayer_blind": True},
                Decimal(19750),
            ),
            (
                "demo.toti.case13.hoh",
                "head_of_household",
                {"taxpayer_over_65": True},
                Decimal(25625),
            ),
            ("demo.toti.case13.mfs", "married_filing_separately", {}, Decimal(15750)),
        )
        for run_id, status, flags, expected in scenarios:
            acts = _age(probe._base_acts(wages=80000, filing_status=status), **flags)
            pubs, blocked = _run(_finish_v50(acts, f"synthetic {run_id}"), run_id)
            self.assertEqual(_value(pubs, blocked, STD), expected, run_id)

    def test_case_14_basis_names_uncomputed_deductions(self) -> None:
        probe = _probe()
        acts = _age(probe._base_acts(wages=80000), taxpayer_over_65=True)
        pubs, blocked = _run(_finish_v50(acts, "synthetic case 14"), "demo.toti.case14")
        self.assertEqual(_value(pubs, blocked, STD), Decimal(17750))
        finding = pubs[STD]
        computation = [
            pin for pin in finding["pins"]
            if pin.get("role") == "computation"
            and pin.get("id") == "tax.us.2025.rule.form1040-standard-deduction"
        ]
        self.assertEqual([pin["version"] for pin in computation], ["v2"])
        self.assertTrue(any(
            pin.get("role") == "citation"
            and pin.get("id") == LINE12_CITE
            and pin.get("version") == "v1"
            for pin in finding["pins"]
        ))
        rule = json.loads((CONTENT / "rule.form1040-standard-deduction.v2.json").read_text(encoding="utf-8"))
        named = " ".join(rule["basis"]["left_with_person"])
        self.assertIn("dependent's limited standard deduction", named)
        self.assertIn("senior deduction", named)

    def test_case_15_no_schedule_d_uses_line_7a(self) -> None:
        probe = _probe()
        acts = _finish_v50(
            probe._base_acts(wages=50000, capital_gains=4000),
            "synthetic case 15",
        )
        pubs, blocked = _run(acts, "demo.toti.case15")
        self.assertEqual(_value(pubs, blocked, BOX2A), Decimal(4000))
        self.assertEqual(_value(pubs, blocked, PREF), Decimal(4000))

    def test_case_16_v49_package_is_unchanged(self) -> None:
        probe = _probe()
        acts = probe._finish_v49(
            probe._base_acts(wages=61850),
            "synthetic v49 wages-only comparison",
        )
        result = probe._run(acts, "demo.toti.case16")
        self.assertIsNone(result.get("refusal"), result.get("refusal"))
        self.assertEqual(Decimal(str(probe._taxable_income(result))), Decimal(46850))
        self.assertEqual(Decimal(str(probe._line16(result))), Decimal(5390))
        package = json.loads(PACKAGE_V49.read_text(encoding="utf-8"))
        member = next(row for row in package["members"] if row["id"] == "tax.us.2025.rule.form1040-line16")
        self.assertEqual(member["version"], "v5")
        registry = json.loads(REGISTRY_V47.read_text(encoding="utf-8"))
        published = next(
            row for row in registry["packages"]
            if row["id"] == package["id"] and row["version"] == "v49"
        )
        self.assertEqual(published["checksum"], package["package_checksum"])

    def test_package_union_is_v49_plus_successors_minus_replaced(self) -> None:
        before = json.loads(PACKAGE_V49.read_text(encoding="utf-8"))
        after = json.loads(PACKAGE_V50.read_text(encoding="utf-8"))
        pred = {(row["id"], row["version"]) for row in before["members"]}
        succ = {(row["id"], row["version"]) for row in after["members"]}
        self.assertEqual(pred - succ, REMOVED)
        self.assertEqual(succ - pred, ADDED)
        self.assertEqual(after["schema"], before["schema"])
        for rule_id, version in (
            ("tax.us.2025.rule.form1040-line16", "v6"),
            ("tax.us.2025.rule.selected-preferential-base", "v5"),
        ):
            entry = next(row for row in after["entrypoints"] if row["id"] == rule_id)
            self.assertEqual(entry["version"], version)

    def test_removed_demo_parameters_are_not_reachable(self) -> None:
        package = json.loads(PACKAGE_V50.read_text(encoding="utf-8"))
        corpus: dict[tuple[str, str], dict[str, Any]] = {}
        for path in CONTENT.glob("*.json"):
            try:
                value = json.loads(path.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                continue
            if isinstance(value, dict) and isinstance(value.get("id"), str) and isinstance(value.get("version"), str):
                corpus[(value["id"], value["version"])] = value
        producers: dict[str, list[tuple[str, str]]] = {}
        members = {(row["id"], row["version"]) for row in package["members"]}
        for key in members:
            citizen = corpus[key]
            symbol = citizen.get("publishes")
            if isinstance(symbol, str):
                producers.setdefault(symbol, []).append(key)
        demo_ids = {item[0] for item in REMOVED if item[0].startswith("demo.parameter.")}
        stack = [
            ("tax.us.2025.rule.form1040-line16", "v6"),
            ("tax.us.2025.rule.form1040-standard-deduction", "v2"),
        ]
        seen: set[tuple[str, str]] = set()
        while stack:
            key = stack.pop()
            if key in seen:
                continue
            seen.add(key)
            citizen = corpus[key]
            blob = json.dumps(citizen)
            for demo_id in demo_ids:
                self.assertNotIn(demo_id, blob, key)
            for symbol in citizen.get("requires", []):
                for producer in producers.get(symbol, []):
                    if producer in members:
                        stack.append(producer)

    def test_worksheet_rules_stay_within_the_size_target(self) -> None:
        limit = 6 * 1024
        paths = sorted(CONTENT.glob("rule.qdcg-worksheet.*.json"))
        self.assertEqual(
            {path.name for path in paths},
            {f"rule.qdcg-worksheet.line-{number}.json" for number in _WORKSHEET_LINES},
        )
        for path in paths:
            self.assertLessEqual(path.stat().st_size, limit, path.name)
