"""Replay the seven mortgage cases on the currently adopted published package.

Run from the repository root:

    python3 docs/phases/tax-circumstance-breadth/milestones/mortgage-interest-circumstances-evidence/p0_current_path.py

Mortgage and surrounding return acts reuse the published synthetic fixtures.
The current-return additions are only the native closed-empty Form 1098-E
family and twelve Schedule 1 adjustment-absence declarations needed by the
current package's dependency chain. No line 21, line 26, or AGI result is
asserted by this script.
"""

from __future__ import annotations

import copy
import hashlib
import json
import sys
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT))

from packages.derivation.live import live_coordinate_run
from packages.derivation.live_workspace import WorkspaceCapability
from packages.derivation.production_resolver import PublicationSurface
from tests.test_f1098_mortgage_interest_line12e_track2 import (
    ATTACHMENT_ID,
    CONTENT,
    FIXTURES,
    LINE8A_RULE,
    SCOPE,
    USER,
    _by_artifact,
    _f1098_acts,
    _load_fixture_adoption,
    _path_a_acts,
    _published_numeric,
)
from tests.test_f1098e_student_loan_interest_agi_track6 import (
    CLOSURE_TYPE as F1098E_CLOSURE_TYPE,
    FAMILY_ID as F1098E_FAMILY_ID,
    SCHED1_LINE_TOKENS,
    _f1098e_acts,
)

PACKAGE_PATH = CONTENT / "package.core-calculations.v42.json"
RELEASE_DIR = ROOT / "packages" / "sample_data" / "student_loan_worksheet_integration" / "publication_surface" / "releases"
RELEASE_PATH = RELEASE_DIR / "demo.release.sli-worksheet-integration.2025.v40.json"
REGISTRY_PATH = CONTENT / "published-packages.v40.json"
F1098E_BUNDLE_ID = "tax.us.2025.f1098e.vocabulary"
SCHED1_BUNDLE_ID = "tax.us.2025.schedule1-adjustments-scope.vocabulary"
SCHED1_PREFIX = "tax.us.2025.schedule1-adjustments-scope."
LINE21_FACT = "tax.us.2025.schedule1.line21-sli-deduction"
LINE26_FACT = "tax.us.2025.schedule1.line26-total-adjustments"
STANDARD_RULE = "tax.us.2025.rule.form1040-standard-deduction"
LINE12E_RULE = "tax.us.2025.rule.form1040-line12e"
LINE11B_RULE = "tax.us.2025.rule.form1040-line11"


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text("utf-8"))


def _selected_current_dependency_acts() -> list[dict[str, object]]:
    """Select only the specified native empty-family and Schedule 1 setup."""
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

    schedule1_ids = {
        row["payload"]["finding"]["fact_id"]
        for row in selected
        if row.get("kind") == "assertion"
        and isinstance(row.get("payload"), dict)
        and isinstance(row["payload"].get("finding"), dict)
        and row["payload"]["finding"].get("fact_id", "").startswith(SCHED1_PREFIX)
    }
    expected_ids = {f"{SCHED1_PREFIX}{token}|tax-year=2025" for token in SCHED1_LINE_TOKENS}
    if schedule1_ids != expected_ids:
        raise AssertionError(f"expected the twelve Schedule 1 absence assertions; got {sorted(schedule1_ids)}")
    if not any(
        row.get("kind") == "assertion"
        and row.get("payload", {}).get("finding", {}).get("fact_id", "").startswith(F1098E_CLOSURE_TYPE + "|")
        for row in selected
    ):
        raise AssertionError("the native closed-empty Form 1098-E closure was not selected")
    return selected


def _current_adoption(template: dict[str, object], revision: int) -> dict[str, object]:
    package = _read_json(PACKAGE_PATH)
    release = _read_json(RELEASE_PATH)
    adoption = copy.deepcopy(template)
    adoption["act_id"] = "demo.f1098.p0.adopt-current"
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
    payload["audit"] = {"note": "synthetic P0 current-package replay; adoption identity loaded from published v42 package and release"}
    return adoption


def _case_acts(
    interest: float | None,
    *,
    authority_overrides: dict[str, str] | None = None,
    itemized_assertion: float | None = None,
    omit_acquisition_confirmation: bool = False,
) -> list[dict[str, object]]:
    if interest is None:
        acts = _path_a_acts(wages=90000)
    else:
        acts = _f1098_acts(
            interest=interest,
            wages=90000,
            authority_overrides=authority_overrides,
            itemized_assertion=itemized_assertion,
        )
    if omit_acquisition_confirmation:
        acts = [
            row
            for row in acts
            if not (
                isinstance(row.get("payload"), dict)
                and isinstance(row["payload"].get("finding"), dict)
                and str(row["payload"]["finding"].get("fact_id", "")).startswith(
                    "tax.us.2025.f1098.acquisition-debt-use|"
                )
            )
        ]
    acts.pop()  # replace the v29 adoption with the v42 adoption
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
            raise AssertionError(f"current published package refused: {result.refusal!r}")
        assert result.output_path is not None and result.presentation_path is not None
        report = json.loads(result.output_path.read_text("utf-8"))
        model = json.loads(result.presentation_path.read_text("utf-8"))
        return report, model, result


def _publication_rows(result: Any) -> list[dict[str, Any]]:
    publications = result.publications or ()
    return [copy.deepcopy(publication.finding) for publication in publications]


def _published_fact_value(findings: list[dict[str, Any]], fact_type: str) -> Any:
    matches = [
        finding
        for finding in findings
        if finding.get("symbol") == fact_type
    ]
    if len(matches) != 1:
        raise AssertionError(f"expected one native publication for {fact_type}, got {len(matches)}")
    return matches[0].get("value")


def _row_map(report: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return _by_artifact(report)


def _small_row(row: dict[str, Any] | None) -> dict[str, Any] | None:
    if row is None:
        return None
    selected = {key: row[key] for key in ("disposition", "code", "missing", "symbol") if key in row}
    selected["pins"] = [
        {key: pin[key] for key in ("id", "role", "version", "origin") if key in pin}
        for pin in row.get("pins", [])
        if pin.get("role") in {"adoption", "parameter", "computation"} or pin.get("origin") == "declared_default"
    ]
    return selected


def _supplied_facts(acts: list[dict[str, object]]) -> dict[str, Any]:
    facts: dict[str, Any] = {}
    for row in acts:
        payload = row.get("payload", {})
        if not isinstance(payload, dict):
            continue
        candidates: list[dict[str, Any]] = []
        finding = payload.get("finding")
        if isinstance(finding, dict):
            candidates.append(finding)
        member = payload.get("member")
        if isinstance(member, dict) and isinstance(member.get("finding"), dict):
            candidates.append(member["finding"])
        for candidate in candidates:
            fact_id = candidate.get("fact_id")
            if isinstance(fact_id, str) and (
                fact_id.startswith("tax.us.2025.f1098.")
                or fact_id.startswith("tax.us.2025.f1098-scope.")
                or fact_id.startswith("tax.us.2025.schedule-a-boundary.")
                or fact_id.startswith("tax.us.2025.qbi.")
                or fact_id.startswith("tax.us.2025.schedule1a.")
                or fact_id.startswith(SCHED1_PREFIX)
                or fact_id.startswith(F1098E_CLOSURE_TYPE + "|")
                or fact_id.startswith("tax.us.2025.w2.box1-wages|")
                or fact_id == "tax.us.2025.filing-status|tax-year=2025"
            ):
                facts[fact_id] = candidate.get("value")
    return facts


def _case(name: str, interest: float | None, **kwargs: Any) -> dict[str, Any]:
    acts = _case_acts(interest, **kwargs)
    report, model, result = _run_current(acts, f"demo.f1098.p0.v42.{name}")
    rows = _row_map(report)
    findings = _publication_rows(result)
    attachment = next(item for item in model["attachments"] if item["id"] == ATTACHMENT_ID)
    return {
        "case": name,
        "supplied_facts": _supplied_facts(acts),
        "declared_default_inputs": [
            {
                "fact_id": finding["resolved_input"]["fact_id"],
                "symbol": finding["symbol"],
                "value": finding["value"],
                "origin": finding["resolved_input"]["origin"],
                "parameter_pins": [
                    {key: pin[key] for key in ("id", "version") if key in pin}
                    for pin in finding.get("pins", [])
                    if pin.get("role") == "parameter"
                ],
            }
            for finding in findings
            if finding.get("resolved_input", {}).get("origin") == "declared_default"
        ],
        "line8a_rule": _small_row(rows.get(LINE8A_RULE)),
        "schedule_a_attachment": attachment["resolved"],
        "line12e_rule": _small_row(rows.get(LINE12E_RULE)),
        "standard_deduction_rule": _small_row(rows.get(STANDARD_RULE)),
        "line11b_rule": _small_row(rows.get(LINE11B_RULE)),
        "line8a_tie_out": _schedule_a_tie_out(model) if attachment["resolved"].get("disposition") == "published" else None,
        "line12e": _published_numeric(model, "line-12e"),
        "line21_native": _published_fact_value(findings, LINE21_FACT),
        "line26_native": _published_fact_value(findings, LINE26_FACT),
        "line11b_agi": _published_numeric(model, "line-11b"),
        "line15_taxable_income": _published_numeric(model, "line-15"),
        "native_return_publications": {
            symbol: {
                "value": finding.get("value"),
                "version": finding.get("version"),
                "pins": [
                    {key: pin[key] for key in ("id", "role", "version", "origin") if key in pin}
                    for pin in finding.get("pins", [])
                    if pin.get("role") in {"adoption", "computation", "parameter"}
                ],
            }
            for symbol in (LINE21_FACT, LINE26_FACT)
            for finding in findings
            if finding.get("symbol") == symbol
        },
    }


def _schedule_a_tie_out(model: dict[str, Any]) -> float:
    group = next(g for g in model["citationGroups"] if g["id"] == ATTACHMENT_ID)
    part = group["parts"][0]
    import re

    match = re.search(r"Reported subtotal: ([0-9.]+)", part["tieOutText"])
    if match is None:
        raise AssertionError(part["tieOutText"])
    return float(match.group(1))


def _observed_version_summary(cases: list[dict[str, Any]]) -> dict[str, Any]:
    first = cases[0]
    relevant = [
        ("line8a_rule", first["line8a_rule"]),
        ("standard_deduction_rule", first["standard_deduction_rule"]),
        ("line12e_rule", first["line12e_rule"]),
        ("line11b_rule", first["line11b_rule"]),
    ]
    package = _read_json(PACKAGE_PATH)
    relevant_member_ids = {
        LINE8A_RULE,
        STANDARD_RULE,
        LINE12E_RULE,
        LINE11B_RULE,
    }
    relevant_member_ids.update({
        "tax.us.2025.rule.sli-worksheet",
        "tax.us.2025.rule.schedule1-line26",
    })
    package_members = {
        member["id"]: member["version"]
        for member in package["members"]
        if member.get("id") in relevant_member_ids
    }
    return {
        "resolved_package_member_versions": package_members,
        "package_adoption_pins": {
            name: next((pin for pin in row.get("pins", []) if pin.get("role") == "adoption"), None)
            for name, row in relevant
        },
        "parameter_pins": {
            name: [pin for pin in row.get("pins", []) if pin.get("role") == "parameter"]
            for name, row in relevant
        },
        "declared_default_pins": {
            name: [pin for pin in row.get("pins", []) if pin.get("origin") == "declared_default"]
            for name, row in relevant
        },
        "observed_rule_and_parameter_pins": {
            name: [
                pin for pin in row.get("pins", [])
                if pin.get("role") in {"computation", "parameter"}
            ]
            for name, row in relevant
        },
    }


def _assertion_summary(cases: list[dict[str, Any]]) -> dict[str, Any]:
    """Summarize assertion origin and expose the actual mortgage case inputs."""
    closed_empty = next(case for case in cases if case["case"] == "closed-empty-no-statement")
    sample_facts = cases[0]["supplied_facts"]
    f1098_prefix = "tax.us.2025.f1098."
    sched1_prefix = SCHED1_PREFIX

    def fact_value(facts: dict[str, Any], starts: str) -> Any:
        return next((value for key, value in facts.items() if key.startswith(starts)), None)

    sched1_ids = sorted(key for key in sample_facts if key.startswith(sched1_prefix))
    schedule_a_ids = sorted(key for key in sample_facts if key.startswith("tax.us.2025.schedule-a-boundary."))
    qbi_ids = sorted(key for key in sample_facts if key.startswith("tax.us.2025.qbi."))
    sched1a_ids = sorted(key for key in sample_facts if key.startswith("tax.us.2025.schedule1a."))
    statement_inputs: dict[str, dict[str, Any]] = {}
    missing_acquisition_use: dict[str, bool] = {}
    for case in cases:
        facts = case["supplied_facts"]
        normalized = {
            key[len(f1098_prefix):].split("|", 1)[0]: value
            for key, value in facts.items()
            if key.startswith(f1098_prefix)
        }
        statement_inputs[case["case"]] = normalized
        missing_acquisition_use[case["case"]] = not any(
            key.startswith(f1098_prefix + "acquisition-debt-use|") for key in facts
        )
    return {
        "shared_setup_assertions": {
            "w2_box1_wages": fact_value(sample_facts, "tax.us.2025.w2.box1-wages|"),
            "filing_status": fact_value(sample_facts, "tax.us.2025.filing-status|"),
            "closed_empty_f1098e_family_asserted": any(
                key.startswith(F1098E_CLOSURE_TYPE + "|")
                for key in closed_empty["supplied_facts"]
            ),
            "schedule1_adjustment_absence_assertion_count": len(sched1_ids),
            "schedule_a_category_absence_assertion_count": len(schedule_a_ids),
            "qbi_absence_assertion_count": len(qbi_ids),
            "schedule1a_absence_assertion_count": len(sched1a_ids),
        },
        "mortgage_statement_assertions_by_case": statement_inputs,
        "acquisition_use_confirmation_absent_by_case": missing_acquisition_use,
    }


def main() -> None:
    cases = [
        _case("admitted-20k", 20000.0),
        _case("admitted-zero", 0.0),
        _case("closed-empty-no-statement", None),
        _case("acquisition-use-no-20k", 20000.0, authority_overrides={"acquisition-debt-use": "no"}),
        _case("acquisition-use-missing-20k", 20000.0, omit_acquisition_confirmation=True),
        _case("admitted-5k-below-standard", 5000.0),
        _case("admitted-8k-below-standard", 8000.0),
    ]
    assertions = _assertion_summary(cases)
    shared_defaults = cases[0]["declared_default_inputs"]
    native_return = cases[0]["native_return_publications"]
    for case in cases:
        case.pop("supplied_facts")
        case.pop("declared_default_inputs")
        case.pop("native_return_publications")
    print(json.dumps({
        "versions_and_origins": _observed_version_summary(cases),
        "assertions": assertions,
        "declared_default_inputs_observed": shared_defaults,
        "native_return_publications_observed": native_return,
        "cases": cases,
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
