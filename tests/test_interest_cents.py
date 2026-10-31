"""Interest with cents (2025): core v68 admits the line 2b successor and rounds once at the total.

Track 0 (the package validator's successor-graph table) is tested here on the committed core v67
package; later sections run v67 against v68 through ``live_coordinate_run``. Synthetic ``demo.*``
data only.
"""

from __future__ import annotations

import copy
import json
import re
from dataclasses import dataclass
from decimal import Decimal
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any
import unittest

from packages.derivation.live import live_coordinate_run
from packages.derivation.live_workspace import WorkspaceCapability
from packages.derivation.loader import DerivationSchemas
from packages.derivation.package_validation import load_published_citizen_checksums, validate_package
from packages.derivation.production_resolver import PublicationSurface
from packages.derivation.runner import ITEMIZATION_TIE_OUT_VIOLATION
from packages.kernel.findings import FindingModelError
from tests import test_collect_closure as cc
from tests import test_w2g_gambling as w2g
from tests.test_form_1099_k_income import _handover
from tests.test_refund_or_amount_owed_track1 import _finish
from tests.test_withholding_closure import _strip_closure

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "packages/content/tax/2025"
PACKAGE_V67 = CONTENT / "package.core-calculations.v67.json"
REGISTRY_V65 = CONTENT / "published-packages.v65.json"
RELEASE_DIR = ROOT / "packages/sample_data/student_loan_worksheet_integration/publication_surface/releases"
PACKAGE_V68 = CONTENT / "package.core-calculations.v68.json"
RELEASE_V65 = RELEASE_DIR / "demo.release.sli-worksheet-integration.2025.v65.json"
RELEASE_V66 = RELEASE_DIR / "demo.release.sli-worksheet-integration.2025.v66.json"
SURFACE_V67 = PublicationSurface(RELEASE_DIR, CONTENT / "published-packages.v65.json", CONTENT)
SURFACE_V68 = PublicationSurface(RELEASE_DIR, CONTENT / "published-packages.v66.json", CONTENT)

P = "tax.us.2025."
USER = "demo.user.filer-1"
YEAR = "2025"
AGI = P + "income.agi"
TAXABLE = P + "income.taxable-income"
REFUND = P + "payments.line35a-refunded"
TAXABLE_INTEREST_TOTAL = P + "interest.taxable-total"
LINE_2B = P + "interest.line-2b"
B1_SUBTOTAL = P + "interest.b1-subtotal"
B3_SUBTOTAL = P + "interest.b3-subtotal"
POSITIVE_TOTAL = P + "interest.positive-total"
SCHEDULE_B_DISPOSITION = P + "scheduleb.disposition"

LINE_2B_FIELD = "tax.us.2025.form1040.line-2b"
GRAPH_CODE = "NOMINEE_RETURN_SUCCESSOR_GRAPH_MIXED"


def _corpus() -> dict[tuple[str, str], dict[str, Any]]:
    corpus: dict[tuple[str, str], dict[str, Any]] = {}
    for path in CONTENT.glob("*.json"):
        citizen = json.loads(path.read_text("utf-8"))
        if (
            isinstance(citizen, dict)
            and isinstance(citizen.get("id"), str)
            and isinstance(citizen.get("version"), str)
            and not ("citizens" in citizen and "packages" in citizen)
        ):
            corpus[(citizen["id"], citizen["version"])] = citizen
    return corpus


def _codes(package: dict[str, Any]) -> set[str]:
    return _codes_for(package, REGISTRY_V65)


def _codes_for(package: dict[str, Any], registry: Path) -> set[str]:
    corpus = _corpus()
    members = {(m["id"], m["version"]): corpus[(m["id"], m["version"])] for m in package["members"]}
    result = validate_package(
        copy.deepcopy(package), members, DerivationSchemas(), load_published_citizen_checksums(registry)
    )
    return {issue.code for issue in result.issues}


def _pin(package: dict[str, Any], member_id: str) -> dict[str, Any]:
    return next(m for m in package["members"] if m["id"] == member_id)


class SuccessorGraphTable(unittest.TestCase):
    def test_v67_still_governed_by_the_v38_entry(self) -> None:
        package = json.loads(PACKAGE_V67.read_text("utf-8"))
        self.assertEqual(_pin(package, LINE_2B_FIELD)["version"], "v5")
        self.assertNotIn(GRAPH_CODE, _codes(package))

    def test_v67_with_the_v6_field_is_still_refused(self) -> None:
        package = json.loads(PACKAGE_V67.read_text("utf-8"))
        _pin(package, LINE_2B_FIELD)["version"] = "v6"
        self.assertIn(GRAPH_CODE, _codes(package))

    def test_the_committed_v68_package_validates_against_its_entry(self) -> None:
        package = json.loads(PACKAGE_V68.read_text("utf-8"))
        self.assertEqual(_pin(package, LINE_2B_FIELD)["version"], "v6")
        self.assertEqual(_codes_for(package, CONTENT / "published-packages.v66.json"), set())

    def test_a_v68_package_with_the_v5_field_is_refused(self) -> None:
        package = json.loads(PACKAGE_V67.read_text("utf-8"))
        package["version"] = "v68"
        self.assertEqual(_pin(package, LINE_2B_FIELD)["version"], "v5")
        self.assertIn(GRAPH_CODE, _codes(package))

    def test_a_v68_package_with_another_mix_is_refused(self) -> None:
        package = json.loads(PACKAGE_V67.read_text("utf-8"))
        package["version"] = "v68"
        _pin(package, "tax.us.2025.rule.attachment.schedule-b")["version"] = "v6"
        self.assertIn(GRAPH_CODE, _codes(package))


WORKSHEET = "tax.us.2025.rule.ss-benefits-worksheet"
SUCCESSION_CODE = "SUCCESSION_PACKAGE_INCOMPLETE"
from packages.tax.schedule1_adjustments_succession import MIGRATION_ID, SUCCESSOR_BUNDLE_ID


def _with_worksheet(version: str, *, drop: str | None = None) -> Any:
    """The v67 package with the worksheet pinned at ``version`` (a copy of v3's body), validated
    without the publication registry, which cannot know a version that is not yet published."""
    package = json.loads(PACKAGE_V67.read_text("utf-8"))
    corpus = _corpus()
    body = copy.deepcopy(corpus[(WORKSHEET, "v3")])
    body["version"] = version
    corpus[(WORKSHEET, version)] = body
    for member in package["members"] + package["entrypoints"]:
        if member["id"] == WORKSHEET:
            member["version"] = version
    if drop is not None:
        package["members"] = [m for m in package["members"] if m["id"] != drop]
        package["entrypoints"] = [e for e in package["entrypoints"] if e["id"] != drop]
    members = {(m["id"], m["version"]): corpus[(m["id"], m["version"])] for m in package["members"]}
    return validate_package(package, members, DerivationSchemas(), None)


class SocialSecuritySuccessionCheck(unittest.TestCase):
    def test_worksheet_v3_and_later_are_accepted(self) -> None:
        for version in ("v3", "v4", "v10"):
            with self.subTest(version=version):
                result = _with_worksheet(version)
                self.assertTrue(result.ok, result.issues)

    def test_worksheet_v2_is_still_refused(self) -> None:
        codes = {issue.code for issue in _with_worksheet("v2").issues}
        self.assertIn(SUCCESSION_CODE, codes)

    def test_missing_successor_bundle_or_migration_is_still_refused(self) -> None:
        codes = {issue.code for issue in _with_worksheet("v4", drop=SUCCESSOR_BUNDLE_ID).issues}
        self.assertIn(SUCCESSION_CODE, codes)
        codes = {issue.code for issue in _with_worksheet("v4", drop=MIGRATION_ID).issues}
        self.assertIn(SUCCESSION_CODE, codes)


@dataclass
class IRun:
    pubs: dict[str, dict[str, Any]]
    blocked: list[dict[str, Any]]

    def value(self, symbol: str) -> Decimal | None:
        return Decimal(str(self.pubs[symbol]["value"])) if symbol in self.pubs else None

    def values(self) -> dict[str, str]:
        """Every published value by symbol, numbers normalised (a subtotal that no longer rounds
        prints 200.0 where the rounded one printed 200; the amounts are equal)."""
        return {s: json.dumps(_numeric(f["value"]), sort_keys=True) for s, f in sorted(self.pubs.items())}

    def blocked_codes(self) -> set[tuple[str, str]]:
        return {(str(r.get("artifact_id", "")).replace(P, ""), str(r.get("code"))) for r in self.blocked}


def _numeric(node: Any) -> Any:
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


def _run(acts: list[dict[str, object]], run_id: str, *, core: str) -> IRun:
    """Runs the return on core v67 or v68; a base "none" declaration that a recorded member contradicts
    is withdrawn first (as a filer withdraws it by recording the member)."""
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
    if core == "v68":
        package, release, rel_version, surface = PACKAGE_V68, RELEASE_V66, "v66", SURFACE_V68
    else:
        package, release, rel_version, surface = PACKAGE_V67, RELEASE_V65, "v65", SURFACE_V67
    finished = _finish(
        copy.deepcopy(acts), package_path=package, package_version=core,
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
        if outcome.output_path is not None:
            report = json.loads(outcome.output_path.read_text(encoding="utf-8"))
            blocked = [r for r in report.get("dispositions", []) if r.get("disposition") == "blocked"]
    return IRun(pubs, blocked)


def _interest(b1: list[float], b3: list[float] | None = None) -> list[dict[str, object]]:
    """The base return (wages 50,000, 4,500 withheld) plus Form 1099-INT box 1 (and box 3) amounts."""
    acts = w2g._w2g_return([])
    for family, amounts, tag in (("f1099int.b1", b1, "ib1"), ("f1099int.b3", b3 or [], "ib3")):
        for i, amount in enumerate(amounts):
            acts = cc._add_member(acts, P + family, amount, close=i == len(amounts) - 1, tag=f"{tag}{i}")
    return acts


def _both(acts: list[dict[str, object]], name: str) -> tuple[IRun, IRun]:
    return _run(acts, f"demo.ic.{name}.v67", core="v67"), _run(acts, f"demo.ic.{name}.v68", core="v68")


# Symbols core v68 publishes that v67 did not (a rounded line of its own).
ADDED_SYMBOLS = (LINE_2B,)


def _assert_same_values(case: unittest.TestCase, old: IRun, new: IRun, label: str) -> None:
    """Every value v67 published is published, unchanged, by v68; v68 adds only line 2b's rounded symbol."""
    new_values = new.values()
    added = set(new_values) - set(old.values())
    case.assertLessEqual(added, set(ADDED_SYMBOLS), label)
    case.assertEqual({s: v for s, v in new_values.items() if s not in added}, old.values(), label)
    case.assertEqual(old.blocked_codes(), new.blocked_codes(), label)


class WholeDollarReturnsAreUnchanged(unittest.TestCase):
    def test_interest_in_whole_dollars_is_identical_on_v67_and_v68(self) -> None:
        for name, acts in (
            ("none", _interest([])),
            ("b1", _interest([100.0, 100.0])),
            ("b1b3", _interest([300.0], [200.0])),
            ("over1500", _interest([800.0, 800.0])),
        ):
            with self.subTest(name):
                old, new = _both(acts, name)
                _assert_same_values(self, old, new, name)
                self.assertFalse(_tie_out_blocked(new))
                if name != "none":
                    self.assertEqual(new.value(LINE_2B), new.value(TAXABLE_INTEREST_TOTAL))
                    self.assertEqual(new.value(LINE_2B), old.value(TAXABLE_INTEREST_TOTAL))


def _tie_out_blocked(run: IRun) -> bool:
    return ("rule.attachment.schedule-b", ITEMIZATION_TIE_OUT_VIOLATION) in run.blocked_codes()


NOMINEE_FAMILY = "scheduleb.adjustment.nominee"
D = Decimal


def _with_nominee(b1: list[float], nominee: float) -> list[dict[str, object]]:
    acts = _interest(b1)
    return cc._add_member(acts, P + NOMINEE_FAMILY, nominee, close=True, tag="nom")


class InterestWithCents(unittest.TestCase):
    """The hand values are P0's (section 5 of ``itemization-cents-evidence/p0-trace-and-design.md``),
    with base return single, wages 50,000: AGI is 50,000 plus line 2b."""

    def test_two_box_1_amounts_of_100_40_round_once(self) -> None:
        # Below the $1,500 threshold no Schedule B attaches, so nothing ties out on either core;
        # one family rounds its subtotal once on both, and line 2b is 201 (P0 t3 analogue).
        old, new = _both(_interest([100.40, 100.40]), "b1pair")
        self.assertEqual(new.value(B1_SUBTOTAL), D("200.8"))
        self.assertEqual(new.value(LINE_2B), D("201"))
        self.assertEqual(old.value(TAXABLE_INTEREST_TOTAL), D("201"))
        self.assertEqual((old.value(AGI), new.value(AGI)), (D("50201"), D("50201")))
        self.assertEqual(new.value(TAXABLE), D("34451"))
        self.assertNotIn(SCHEDULE_B_DISPOSITION, new.pubs)

    def test_d1_box_1_and_box_3(self) -> None:
        old, new = _both(_interest([100.40], [100.40]), "d1")
        self.assertEqual(old.value(TAXABLE_INTEREST_TOTAL), D("200"))  # 100 + 100, each rounded first
        self.assertEqual(new.value(LINE_2B), D("201"))  # round(200.80)
        self.assertEqual((old.value(AGI), new.value(AGI)), (D("50200"), D("50201")))
        self.assertFalse(_tie_out_blocked(new), new.blocked_codes())

    def test_d2_two_halves(self) -> None:
        old, new = _both(_interest([100.50], [100.50]), "d2")
        self.assertEqual(old.value(TAXABLE_INTEREST_TOTAL), D("202"))  # 101 + 101
        self.assertEqual(new.value(LINE_2B), D("201"))  # round(201.00)
        self.assertEqual((old.value(AGI), new.value(AGI)), (D("50202"), D("50201")))

    def test_d3_a_nominee_adjustment(self) -> None:
        acts = _with_nominee([300.60], 100.40)
        old, new = _both(acts, "d3")
        self.assertEqual(old.value(TAXABLE_INTEREST_TOTAL), D("201"))  # 301 - 100
        self.assertEqual(new.value(TAXABLE_INTEREST_TOTAL), D("200.2"))  # 300.60 - 100.40
        self.assertEqual(new.value(LINE_2B), D("200"))
        self.assertEqual((old.value(AGI), new.value(AGI)), (D("50201"), D("50200")))
        self.assertFalse(_tie_out_blocked(new), new.blocked_codes())

    def test_the_schedule_b_threshold_reads_the_rounded_figure(self) -> None:
        below = _run(_interest([1500.40]), "thr.below", core="v68")
        above = _run(_interest([1500.50]), "thr.above", core="v68")
        self.assertEqual(below.value(POSITIVE_TOTAL), D("1500"))
        self.assertEqual(above.value(POSITIVE_TOTAL), D("1501"))
        self.assertNotIn(SCHEDULE_B_DISPOSITION, below.pubs)
        self.assertIn(SCHEDULE_B_DISPOSITION, above.pubs)
        self.assertFalse(_tie_out_blocked(above), above.blocked_codes())

    def test_over_the_threshold_with_cents(self) -> None:
        old, new = _both(_interest([800.40, 800.40]), "t3")
        self.assertTrue(_tie_out_blocked(old))
        self.assertEqual(new.value(B1_SUBTOTAL), D("1600.8"))
        self.assertEqual(new.value(LINE_2B), D("1601"))
        self.assertIn(SCHEDULE_B_DISPOSITION, new.pubs)


def _pins(package: dict[str, Any]) -> set[tuple[str, str]]:
    return {(m["id"], m["version"]) for m in package["members"]}


class Packages(unittest.TestCase):
    def test_the_change_set_is_the_whole_package_delta(self) -> None:
        old = json.loads(PACKAGE_V67.read_text("utf-8"))
        new = json.loads(PACKAGE_V68.read_text("utf-8"))
        self.assertEqual(new["version"], "v68")
        replaced = {
            "form1040.line-2b": ("v5", "v6"), "rule.form1040-line9": ("v7", "v8"),
            "rule.ss-benefits-worksheet": ("v3", "v4"), "rule.eic-investment-income": ("v1", "v2"),
            "rule.interest-positive-total": ("v1", "v2"),
        }
        for name in (
            "f1099int-b1", "f1099int-b3", "f1099int-b10", "f1099oid", "f1099oid-b5", "non-form-interest",
            "form1065-k1-box5", "scheduleb-adjustment.nominee", "scheduleb-adjustment.abp-adjustment",
        ):
            replaced[f"rule.{name}-subtotal"] = ("v2", "v3")
        self.assertEqual(_pins(old) - _pins(new), {(P + k, v[0]) for k, v in replaced.items()})
        self.assertEqual(
            _pins(new) - _pins(old),
            {(P + k, v[1]) for k, v in replaced.items()} | {(P + "rule.form1040-line2b-rounded", "v1")},
        )

    def test_the_registry_only_adds(self) -> None:
        def entries(path: Path, key: str) -> dict[tuple[str, str], str]:
            return {(e["id"], e["version"]): e["checksum"] for e in json.loads(path.read_text("utf-8"))[key]}

        for key in ("citizens", "packages"):
            old = entries(REGISTRY_V65, key)
            new = entries(CONTENT / "published-packages.v66.json", key)
            self.assertEqual({k: v for k, v in new.items() if k in old}, old, key)
        added = set(entries(CONTENT / "published-packages.v66.json", "citizens")) - set(entries(REGISTRY_V65, "citizens"))
        self.assertEqual(len(added), 15)
        self.assertEqual(
            set(entries(CONTENT / "published-packages.v66.json", "packages")) - set(entries(REGISTRY_V65, "packages")),
            {("tax.us.2025.package.core-calculations", "v68")},
        )

    def test_release_v66_pins_registry_v66_and_the_companion_declaration_is_v67s(self) -> None:
        import hashlib
        from packages.tax.loader import domain_package_companion_declarations

        release = json.loads(RELEASE_V66.read_text("utf-8"))
        self.assertEqual(release["version"], "v66")
        self.assertEqual(
            release["package_registry_sha256"],
            hashlib.sha256((CONTENT / "published-packages.v66.json").read_bytes()).hexdigest(),
        )
        declarations = domain_package_companion_declarations()
        core = "tax.us.2025.package.core-calculations"
        self.assertEqual(declarations[(core, "v68")], declarations[(core, "v67")])


class ClosureRegression(unittest.TestCase):
    def test_nothing_new_is_flagged_by_the_closure_survey(self) -> None:
        from tests.test_collect_closure_regression import _flagged

        self.assertEqual(_flagged(PACKAGE_V68), _flagged(PACKAGE_V67))


if __name__ == "__main__":
    unittest.main()
