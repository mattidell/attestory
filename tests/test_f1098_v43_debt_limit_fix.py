"""Successor rule v2 and core calculations v43: the Schedule A line 8a
mortgage-debt limit, verified live against the real published v43 package.

The charter's finding: on adopted v42, ``tax.us.2025.schedule-a.line8a.rule``
v1 collects box 2 (``tax.us.2025.f1098.box2-outstanding-principal``) from the
``tax.us.2025.f1098`` family, whose member predicate is box 1 only
(``family.f1098.json``). A collect with no rows on a closed source set
returns an empty list, so the sum is zero, which always passes ``lte`` the
limit - a principal over the limit deducted the whole interest, and a
missing principal took the same silent path. Repair round: v2 reads box 2's
single-admitted-statement fact directly (``ref``, joining ``requires``), so
a missing or over-limit principal blocks instead of passing as zero.

This module replays P0's current-path pattern
(``docs/phases/tax-circumstance-breadth/milestones/mortgage-interest-circumstances-evidence/p0_current_path.py``)
against the v43 package / registry v41 / release v41 successor route
instead of the adopted v42 / registry v40 / release v40 route, reusing the
same proven return corpus (Track 2's ``_f1098_acts``/``_path_a_acts`` plus
Track 6's native closed-empty Form 1098-E family and the twelve Schedule 1
absence declarations the v42-successor dependency chain needs).
"""

from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any, cast
import unittest

from packages.derivation.live import live_coordinate_run
from packages.derivation.live_workspace import WorkspaceCapability
from packages.derivation.production_resolver import PublicationSurface
from packages.tax.loader import TAX_CONTENT_DIR
from tests.test_f1098_mortgage_interest_line12e_track2 import (
    LINE8A_RULE,
    SCOPE,
    USER,
    _by_artifact,
    _f1098_acts,
    _load_fixture_adoption,
    _path_a_acts,
)
from tests.test_form1099g_box1_schedule1_line7 import _published_numeric
from tests.test_f1098e_student_loan_interest_agi_track6 import (
    CLOSURE_TYPE as F1098E_CLOSURE_TYPE,
    FAMILY_ID as F1098E_FAMILY_ID,
    SCHED1_LINE_TOKENS,
    _f1098e_acts,
)

ROOT = Path(__file__).resolve().parent.parent
CONTENT = TAX_CONTENT_DIR
RELEASE_DIR = ROOT / "packages" / "sample_data" / "student_loan_worksheet_integration" / "publication_surface" / "releases"

PACKAGE_PATH = CONTENT / "package.core-calculations.v43.json"
RELEASE_PATH = RELEASE_DIR / "demo.release.sli-worksheet-integration.2025.v41.json"
REGISTRY_PATH = CONTENT / "published-packages.v41.json"

F1098E_BUNDLE_ID = "tax.us.2025.f1098e.vocabulary"
SCHED1_BUNDLE_ID = "tax.us.2025.schedule1-adjustments-scope.vocabulary"
SCHED1_PREFIX = "tax.us.2025.schedule1-adjustments-scope."
LINE12E_RULE = "tax.us.2025.rule.form1040-line12e"

STANDARD_DEDUCTION_SINGLE = 15000.0
LINE8A_SYMBOL = "tax.us.2025.schedule-a.line8a"
BOX2_FACT_TYPE = "tax.us.2025.f1098.box2-outstanding-principal"
FILING_STATUS_FACT = "tax.us.2025.filing-status|tax-year=2025"


def _read_json(path: Path) -> dict[str, Any]:
    return cast(dict[str, Any], json.loads(path.read_text("utf-8")))


def _selected_current_dependency_acts() -> list[dict[str, object]]:
    """Select only the specified native empty-family and Schedule 1 setup.

    Lifted verbatim from ``p0_current_path.py``: the v42-successor
    dependency chain needs the native closed-empty Form 1098-E family and
    the twelve Schedule 1 adjustment-absence declarations, nothing else
    from that helper's broader return."""
    rows = _f1098e_acts(statements=[], close=True, wages=90000)
    selected: list[dict[str, object]] = []
    for row in rows:
        payload = row.get("payload", {})
        if not isinstance(payload, dict):
            continue
        bundle = payload.get("bundle")
        if isinstance(bundle, dict) and bundle.get("id") in {F1098E_BUNDLE_ID, SCHED1_BUNDLE_ID}:
            selected.append(copy.deepcopy(row))
            continue
        family = payload.get("family")
        if row.get("kind") == "horizon-genesis" and isinstance(family, dict) and family.get("id") == F1098E_FAMILY_ID:
            selected.append(copy.deepcopy(row))
            continue
        finding = payload.get("finding")
        fact_id = finding.get("fact_id") if isinstance(finding, dict) else None
        if row.get("kind") == "assertion" and isinstance(fact_id, str) and (
            fact_id.startswith(F1098E_CLOSURE_TYPE + "|") or fact_id.startswith(SCHED1_PREFIX)
        ):
            selected.append(copy.deepcopy(row))

    schedule1_ids: set[str] = set()
    for row in selected:
        if row.get("kind") != "assertion":
            continue
        payload = row.get("payload")
        if not isinstance(payload, dict):
            continue
        finding = payload.get("finding")
        if not isinstance(finding, dict):
            continue
        fact_id = finding.get("fact_id", "")
        if isinstance(fact_id, str) and fact_id.startswith(SCHED1_PREFIX):
            schedule1_ids.add(fact_id)
    expected_ids = {f"{SCHED1_PREFIX}{token}|tax-year=2025" for token in SCHED1_LINE_TOKENS}
    if schedule1_ids != expected_ids:
        raise AssertionError(f"expected the twelve Schedule 1 absence assertions; got {sorted(schedule1_ids)}")
    return selected


def _current_adoption(template: dict[str, object], revision: int) -> dict[str, object]:
    package = _read_json(PACKAGE_PATH)
    release = _read_json(RELEASE_PATH)
    adoption = copy.deepcopy(template)
    adoption["act_id"] = "demo.f1098.v43.adopt-current"
    adoption["committed_against"] = revision
    payload = adoption["payload"]
    assert isinstance(payload, dict)
    payload["package"] = {
        "id": package["id"],
        "version": package["version"],
        "checksum": package["package_checksum"],
    }
    payload["release"] = {
        "id": release["id"],
        "version": release["version"],
        "checksum": hashlib.sha256(RELEASE_PATH.read_bytes()).hexdigest(),
    }
    payload["revision"] = revision
    payload["audit"] = {"note": "synthetic v43 debt-limit-fix replay; adoption identity loaded from the published v43 package and v41 release"}
    return adoption


def _drop_fact(acts: list[dict[str, object]], fact_type_prefix: str) -> list[dict[str, object]]:
    """Remove every assertion act whose finding's fact_id starts with the
    given fact-type prefix (mirrors ``omit_acquisition_confirmation`` in
    ``p0_current_path.py``, generalized to any fact type)."""
    kept: list[dict[str, object]] = []
    for row in acts:
        payload = row.get("payload")
        finding = payload.get("finding") if isinstance(payload, dict) else None
        fact_id = finding.get("fact_id") if isinstance(finding, dict) else None
        if isinstance(fact_id, str) and fact_id.startswith(fact_type_prefix + "|"):
            continue
        kept.append(row)
    return kept


def _override_filing_status(acts: list[dict[str, object]], value: str) -> None:
    for row in acts:
        payload = row.get("payload")
        if not isinstance(payload, dict):
            continue
        finding = payload.get("finding")
        if isinstance(finding, dict) and finding.get("fact_id") == FILING_STATUS_FACT:
            finding["value"] = value
            return
    raise AssertionError("filing-status assertion not found in base corpus")


def _case_acts(
    interest: float | None,
    *,
    box2: float = 200000.0,
    filing_status: str | None = None,
    omit_box2: bool = False,
    authority_overrides: dict[str, str] | None = None,
    itemized_assertion: float | None = None,
    omit_acquisition_confirmation: bool = False,
) -> list[dict[str, object]]:
    if interest is None:
        acts = _path_a_acts(wages=90000)
    else:
        acts = _f1098_acts(
            interest=interest,
            box2=box2,
            wages=90000,
            authority_overrides=authority_overrides,
            itemized_assertion=itemized_assertion,
        )
    if omit_acquisition_confirmation:
        acts = _drop_fact(acts, "tax.us.2025.f1098.acquisition-debt-use")
    if filing_status is not None:
        _override_filing_status(acts, filing_status)
    if omit_box2:
        acts = _drop_fact(acts, BOX2_FACT_TYPE)
    acts.pop()  # replace the v29 adoption with the v43 adoption
    acts.extend(_selected_current_dependency_acts())
    acts.append(_current_adoption(_load_fixture_adoption(), len(acts)))
    for index, row in enumerate(acts):
        row["committed_against"] = index
    return acts


def _run_current(acts: list[dict[str, object]], run_id: str) -> tuple[dict[str, Any], dict[str, Any], Any]:
    surface = PublicationSurface(RELEASE_DIR, REGISTRY_PATH, CONTENT)
    with TemporaryDirectory() as tmp:
        result = live_coordinate_run(
            WorkspaceCapability(Path(tmp) / "workspace"),
            repo_root=ROOT,
            authoritative_acts=acts,
            workspace_revision=len(acts),
            run_scope=SCOPE,
            scope_user=USER,
            request={"schema": "run-request.v1"},
            run_id=run_id,
            governance_pins=[],
            surface=surface,
            output_name="out.json",
        )
        if result.refusal is not None:
            raise AssertionError(f"v43 published package refused: {result.refusal!r}")
        assert result.output_path is not None and result.presentation_path is not None
        report = json.loads(result.output_path.read_text("utf-8"))
        model = json.loads(result.presentation_path.read_text("utf-8"))
        return report, model, result


def _publication_value(result: Any, symbol: str) -> Any:
    matches = [p.finding for p in (result.publications or ()) if p.finding.get("symbol") == symbol]
    return matches[0].get("value") if matches else None


class TestLine8aV2DebtLimit(unittest.TestCase):
    """The successor rule actually applies the mortgage debt limit."""

    def test_package_checksum_and_route(self) -> None:
        v43 = _read_json(PACKAGE_PATH)
        from packages.derivation.package_validation import package_instance_checksum

        self.assertEqual(v43["package_checksum"], package_instance_checksum(v43))
        self.assertEqual(v43["version"], "v43")
        member_versions = {m["id"]: m["version"] for m in v43["members"]}
        self.assertEqual(member_versions[LINE8A_RULE], "v2")
        entry_versions = {e["id"]: e["version"] for e in v43["entrypoints"]}
        self.assertEqual(entry_versions[LINE8A_RULE], "v2")

    def test_over_limit_blocks_value_invalid_no_line8a_published(self) -> None:
        acts = _case_acts(20000.0, box2=800000.0)
        report, model, result = _run_current(acts, "demo.f1098.v43.over-limit")
        rows = _by_artifact(report)
        line8a_row = rows[LINE8A_RULE]
        self.assertEqual(line8a_row["disposition"], "blocked")
        self.assertEqual(line8a_row["code"], "VALUE_INVALID")
        self.assertIsNone(_publication_value(result, LINE8A_SYMBOL))

        line12e_row = rows[LINE12E_RULE]
        self.assertEqual(line12e_row["disposition"], "blocked")
        self.assertEqual(line12e_row["code"], "DEPENDENCY_ABSENT")
        self.assertNotEqual(_published_numeric(model, "line-12e"), 20000.0)

    def test_at_limit_publishes_box1(self) -> None:
        acts = _case_acts(20000.0, box2=750000.0)
        report, model, result = _run_current(acts, "demo.f1098.v43.at-limit")
        rows = _by_artifact(report)
        self.assertEqual(rows[LINE8A_RULE]["disposition"], "published")
        self.assertEqual(_publication_value(result, LINE8A_SYMBOL), "20000.0")
        self.assertEqual(_published_numeric(model, "line-12e"), 20000.0)

    def test_under_limit_publishes_box1(self) -> None:
        acts = _case_acts(20000.0, box2=500000.0)
        report, model, result = _run_current(acts, "demo.f1098.v43.under-limit")
        rows = _by_artifact(report)
        self.assertEqual(rows[LINE8A_RULE]["disposition"], "published")
        self.assertEqual(_publication_value(result, LINE8A_SYMBOL), "20000.0")
        self.assertEqual(_published_numeric(model, "line-12e"), 20000.0)

    def test_mfs_principal_between_375k_and_750k_blocks(self) -> None:
        acts = _case_acts(20000.0, box2=500000.0, filing_status="married_filing_separately")
        report, model, result = _run_current(acts, "demo.f1098.v43.mfs-between-limits")
        rows = _by_artifact(report)
        line8a_row = rows[LINE8A_RULE]
        self.assertEqual(line8a_row["disposition"], "blocked")
        self.assertEqual(line8a_row["code"], "VALUE_INVALID")
        self.assertIsNone(_publication_value(result, LINE8A_SYMBOL))

        line12e_row = rows[LINE12E_RULE]
        self.assertEqual(line12e_row["disposition"], "blocked")
        self.assertEqual(line12e_row["code"], "DEPENDENCY_ABSENT")

    def test_mfs_principal_under_375k_publishes(self) -> None:
        """Control: the same MFS filing status, but under the MFS-specific
        limit, still publishes - the limit is filing-status-keyed, not a
        flat rejection of married-filing-separately."""
        acts = _case_acts(20000.0, box2=300000.0, filing_status="married_filing_separately")
        report, model, result = _run_current(acts, "demo.f1098.v43.mfs-under-limit")
        rows = _by_artifact(report)
        self.assertEqual(rows[LINE8A_RULE]["disposition"], "published")
        self.assertEqual(_publication_value(result, LINE8A_SYMBOL), "20000.0")

    def test_box2_missing_blocks_dependency_absent(self) -> None:
        acts = _case_acts(20000.0, omit_box2=True)
        report, model, result = _run_current(acts, "demo.f1098.v43.box2-missing")
        rows = _by_artifact(report)
        line8a_row = rows[LINE8A_RULE]
        self.assertEqual(line8a_row["disposition"], "blocked")
        self.assertEqual(line8a_row["code"], "DEPENDENCY_ABSENT")
        self.assertIn(BOX2_FACT_TYPE, line8a_row["missing"])
        self.assertIsNone(_publication_value(result, LINE8A_SYMBOL))

        line12e_row = rows[LINE12E_RULE]
        self.assertEqual(line12e_row["disposition"], "blocked")
        self.assertEqual(line12e_row["code"], "DEPENDENCY_ABSENT")


class TestSevenP0CasesUnchangedOnV43(unittest.TestCase):
    """The seven P0 cases (adopted v42, box2 default 200000.0, always under
    every filing status's limit) give the same results on the v43
    successor as recorded against the adopted v42 package."""

    def _run_case(self, name: str, interest: float | None, **kwargs: Any) -> tuple[dict[str, Any], dict[str, Any], Any]:
        acts = _case_acts(interest, **kwargs)
        return _run_current(acts, f"demo.f1098.v43.p0.{name}")

    def test_admitted_20k(self) -> None:
        report, model, result = self._run_case("admitted-20k", 20000.0)
        rows = _by_artifact(report)
        self.assertEqual(rows[LINE8A_RULE]["disposition"], "published")
        self.assertEqual(_published_numeric(model, "line-12e"), 20000.0)

    def test_admitted_zero(self) -> None:
        report, model, result = self._run_case("admitted-zero", 0.0)
        rows = _by_artifact(report)
        self.assertEqual(rows[LINE8A_RULE]["disposition"], "published")
        self.assertEqual(_published_numeric(model, "line-12e"), STANDARD_DEDUCTION_SINGLE)

    def test_closed_empty_no_statement(self) -> None:
        report, model, result = self._run_case("closed-empty-no-statement", None)
        rows = _by_artifact(report)
        self.assertEqual(rows[LINE8A_RULE]["disposition"], "inapplicable")
        self.assertEqual(_published_numeric(model, "line-12e"), STANDARD_DEDUCTION_SINGLE)

    def test_acquisition_use_no_20k(self) -> None:
        report, model, result = self._run_case("acquisition-use-no-20k", 20000.0, authority_overrides={"acquisition-debt-use": "no"})
        rows = _by_artifact(report)
        self.assertEqual(rows[LINE8A_RULE]["disposition"], "inapplicable")
        self.assertEqual(rows[LINE12E_RULE]["disposition"], "blocked")
        self.assertEqual(rows[LINE12E_RULE]["code"], "DEPENDENCY_ABSENT")

    def test_acquisition_use_missing_20k(self) -> None:
        report, model, result = self._run_case("acquisition-use-missing-20k", 20000.0, omit_acquisition_confirmation=True)
        rows = _by_artifact(report)
        self.assertEqual(rows[LINE8A_RULE]["disposition"], "blocked")
        self.assertEqual(rows[LINE8A_RULE]["code"], "DEPENDENCY_ABSENT")
        self.assertIn("tax.us.2025.f1098.acquisition-debt-use", rows[LINE8A_RULE]["missing"])
        self.assertEqual(rows[LINE12E_RULE]["disposition"], "blocked")
        self.assertEqual(rows[LINE12E_RULE]["code"], "DEPENDENCY_ABSENT")

    def test_admitted_5k_below_standard(self) -> None:
        report, model, result = self._run_case("admitted-5k-below-standard", 5000.0)
        rows = _by_artifact(report)
        self.assertEqual(rows[LINE8A_RULE]["disposition"], "published")
        self.assertEqual(_published_numeric(model, "line-12e"), STANDARD_DEDUCTION_SINGLE)

    def test_admitted_8k_below_standard(self) -> None:
        report, model, result = self._run_case("admitted-8k-below-standard", 8000.0)
        rows = _by_artifact(report)
        self.assertEqual(rows[LINE8A_RULE]["disposition"], "published")
        self.assertEqual(_published_numeric(model, "line-12e"), STANDARD_DEDUCTION_SINGLE)


if __name__ == "__main__":
    unittest.main()
