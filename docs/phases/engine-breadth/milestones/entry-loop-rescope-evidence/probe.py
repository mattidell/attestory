#!/usr/bin/env python3
"""Evidence-only P0 probe for entry-loop-rescope.

Runs the committed legacy entry-loop seed unchanged, plus a complete synthetic
return from current_core_returns on the actually published v70/v68 surface.
Also re-pins a copy of the thin legacy seed to v70 to expose its current-core
partial-entry behavior. It writes no repository files; JSON goes to stdout.
"""

from __future__ import annotations

import copy
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any, Mapping


ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT))

from packages.derivation.entry_loop import (  # noqa: E402
    EVALUATION_LINES,
    EXPECTED_IMPACT_LINES,
    RUN_SCOPE,
    SCOPE_USER,
    EntryLoopError,
    SyntheticW2EntryRuntime,
    load_seed_acts,
    _line_values,
)
from packages.derivation.live import live_coordinate_run  # noqa: E402
from packages.derivation.live_workspace import WorkspaceCapability  # noqa: E402
from packages.derivation.production_resolver import (  # noqa: E402
    PublicationSurface,
    Refusal,
    resolve_adopted_surface,
)
from packages.derivation.loader import DerivationSchemas  # noqa: E402
from tests.helpers import current_core_returns  # noqa: E402
from tests.test_form_1099_k_income import _handover  # noqa: E402
from tests.test_refund_or_amount_owed_track1 import _finish  # noqa: E402


CONTENT = ROOT / "packages/content/tax/2025"
PACKAGE_PATH = CONTENT / "package.core-calculations.v70.json"
RELEASE_DIR = (
    ROOT
    / "packages/sample_data/student_loan_worksheet_integration/publication_surface/releases"
)
RELEASE_PATH = RELEASE_DIR / "demo.release.sli-worksheet-integration.2025.v68.json"
REGISTRY_PATH = CONTENT / "published-packages.v68.json"
LEGACY_RELEASE_DIR = (
    ROOT / "packages/sample_data/frrs_t3/publication_surface/releases"
)
SCHEMA_PATH = ROOT / "packages/schemas/tax/form-field.v3.schema.json"

V70_LINE_SYMBOLS = {
    "1a": "tax.us.2025.wages.total-w2-box1",
    "2b": "tax.us.2025.interest.line-2b",
    "3a": "tax.us.2025.dividends.qualified-total",
    "3b": "tax.us.2025.dividends.ordinary-total",
    "9": "tax.us.2025.income.total-income",
    "11a": "tax.us.2025.income.agi",
    "11b": "tax.us.2025.income.agi",
    "12e": "tax.us.2025.deductions.line-12e",
    "15": "tax.us.2025.income.taxable-income",
    "16": "tax.us.2025.tax.total-tax",
    "25d": "tax.us.2025.payments.line25d",
    "35a": "tax.us.2025.payments.line35a-refunded",
    "37": "tax.us.2025.payments.line37-amount-owed",
}
V70_PROFILE_LINES = ("1a", "9", "11a", "11b", "15", "16", "2b", "3a", "3b", "12e")
V70_OBSERVATION_ONLY_LINES = ("25d", "35a", "37")
PROFILE_BY_PACKAGE = {
    "v6": {
        "expected-impact": [
            {"id": f"tax.us.2025.form1040.line-{line}", "version": "v1"}
            for line in ("1a", "9", "11", "15", "16")
        ],
        "untouched-comparison": [
            {"id": f"tax.us.2025.form1040.line-{line}", "version": "v1"}
            for line in ("2b", "3a", "3b", "12")
        ],
    },
    "v70": {
        "expected-impact": [
            {"id": f"tax.us.2025.form1040.line-{line}", "version": "v1"}
            for line in ("1a", "9", "11a", "11b", "15", "16")
        ],
        "untouched-comparison": [
            {"id": "tax.us.2025.form1040.line-2b", "version": "v6"},
            *[
                {"id": f"tax.us.2025.form1040.line-{line}", "version": "v1"}
                for line in ("3a", "3b", "12e")
            ],
        ],
    },
}


def _plain(value: Any) -> Any:
    """Convert Decimal-like values into JSON-safe numbers/strings."""
    if isinstance(value, Mapping):
        return {str(key): _plain(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_plain(item) for item in value]
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    return str(value)


def _resolve(
    acts: list[dict[str, Any]],
    release_dir: Path,
    *,
    run_scope: Mapping[str, str],
    scope_user: str,
) -> PublicationSurface | Refusal:
    return resolve_adopted_surface(
        acts,
        run_scope=run_scope,
        scope_user=scope_user,
        workspace_revision=len(acts),
        release_dir=release_dir,
        member_dir=CONTENT,
        schemas=DerivationSchemas(),
    )


def _run(
    acts: list[dict[str, Any]],
    surface: PublicationSurface,
    run_id: str,
    *,
    run_scope: Mapping[str, str],
    scope_user: str,
) -> dict[str, Any]:
    with TemporaryDirectory() as scratch:
        outcome = live_coordinate_run(
            WorkspaceCapability(Path(scratch) / "workspace"),
            repo_root=ROOT,
            authoritative_acts=acts,
            workspace_revision=len(acts),
            run_scope=run_scope,
            scope_user=scope_user,
            request={"schema": "run-request.v1"},
            run_id=run_id,
            governance_pins=[],
            surface=surface,
            output_name="probe-report.json",
        )
        if outcome.refusal is not None:
            return {"refusal": outcome.refusal.reason}
        if outcome.output_path is None or outcome.presentation_path is None:
            return {"refusal": "missing-output"}
        report = json.loads(outcome.output_path.read_text(encoding="utf-8"))
        model = json.loads(outcome.presentation_path.read_text(encoding="utf-8"))
        publications = {
            str(row.finding["symbol"]): row.finding
            for row in outcome.publications or ()
        }
    return {
        "report": report,
        "model": model,
        "publications": publications,
    }


def _form1040_fields(model: Mapping[str, Any]) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    for section in model.get("sections", []):
        if not isinstance(section, dict):
            continue
        field = section.get("field")
        resolved = section.get("resolved")
        if not isinstance(field, dict) or not isinstance(resolved, dict):
            continue
        form = field.get("form")
        if not isinstance(form, dict):
            continue
        if (
            form.get("authority") != "IRS"
            or form.get("form_id") != "1040"
            or form.get("jurisdiction") != "US-federal"
            or form.get("tax_year") != 2025
        ):
            continue
        result.append(
            {
                "id": field.get("id"),
                "version": field.get("version"),
                "form_id": form.get("form_id"),
                "line": str(field.get("line", "")),
                "label": field.get("label"),
                "binds_symbol": field.get("binds_symbol"),
                "disposition": resolved.get("disposition"),
                "value": _plain(resolved.get("value")),
                "value_type": type(resolved.get("value")).__name__,
            }
        )
    return sorted(result, key=lambda item: (item["line"], str(item["id"])))


def _all_form_fields(model: Mapping[str, Any]) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    for section in model.get("sections", []):
        if not isinstance(section, dict):
            continue
        field = section.get("field")
        resolved = section.get("resolved")
        if not isinstance(field, dict) or not isinstance(resolved, dict):
            continue
        form = field.get("form")
        if not isinstance(form, dict):
            continue
        result.append(
            {
                "form_id": form.get("form_id"),
                "id": field.get("id"),
                "line": str(field.get("line", "")),
                "value_type": type(resolved.get("value")).__name__,
                "value": _plain(resolved.get("value")),
                "disposition": resolved.get("disposition"),
            }
        )
    return result


def _field_states(fields: list[dict[str, Any]], lines: tuple[str, ...] | list[str]) -> list[dict[str, Any]]:
    selected = set(lines)
    return [field for field in fields if field["line"] in selected]


def _blocked_summary(report: Mapping[str, Any]) -> dict[str, Any]:
    rows = [
        row
        for row in report.get("dispositions", [])
        if isinstance(row, dict) and row.get("disposition") == "blocked"
    ]
    return {
        "count": len(rows),
        "codes": dict(sorted(Counter(str(row.get("code", "unknown")) for row in rows).items())),
    }


def _surface_summary(surface: PublicationSurface | Refusal) -> dict[str, Any]:
    if isinstance(surface, Refusal):
        return {"refusal": surface.reason}
    return {
        "registry": surface.package_registry_path.relative_to(ROOT).as_posix(),
        "release_dir": surface.release_dir.relative_to(ROOT).as_posix(),
        "member_dir": surface.member_dir.relative_to(ROOT).as_posix(),
    }


def _repin_thin_seed_to_v70() -> list[dict[str, Any]]:
    acts = copy.deepcopy(load_seed_acts(ROOT))
    package = json.loads(PACKAGE_PATH.read_text(encoding="utf-8"))
    release_checksum = hashlib.sha256(RELEASE_PATH.read_bytes()).hexdigest()
    adoption_acts = [act for act in acts if act.get("kind") == "package-adoption"]
    if not adoption_acts:
        raise RuntimeError("legacy seed has no package adoption")
    payload = adoption_acts[-1].get("payload")
    if not isinstance(payload, dict):
        raise RuntimeError("legacy seed adoption is malformed")
    payload["package"] = {
        "id": "tax.us.2025.package.core-calculations",
        "version": "v70",
        "checksum": package["package_checksum"],
    }
    payload["release"] = {
        "id": "demo.release.sli-worksheet-integration.2025",
        "version": "v68",
        "checksum": release_checksum,
    }
    return acts


def _change_only_box1(acts: list[dict[str, Any]], value: float) -> list[dict[str, Any]]:
    """Change the sole synthetic Box 1 member while preserving every other act."""
    changed = copy.deepcopy(acts)
    hits = 0
    for act in changed:
        payload = act.get("payload")
        if not isinstance(payload, dict):
            continue
        member = payload.get("member")
        finding = member.get("finding") if isinstance(member, dict) else None
        if (
            isinstance(finding, dict)
            and str(finding.get("fact_id", "")).startswith("tax.us.2025.w2.box1-wages|")
        ):
            finding["value"] = value
            hits += 1
    if hits != 1:
        raise RuntimeError(f"expected one synthetic W-2 Box 1 member, found {hits}")
    return changed


def main() -> None:
    package = json.loads(PACKAGE_PATH.read_text(encoding="utf-8"))
    release = json.loads(RELEASE_PATH.read_text(encoding="utf-8"))
    form_schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    legacy_seed = load_seed_acts(ROOT)
    legacy_runtime: dict[str, Any]
    with TemporaryDirectory() as scratch:
        runtime = SyntheticW2EntryRuntime(
            WorkspaceCapability(Path(scratch) / "legacy-entry"),
            repo_root=ROOT,
            seed_acts=legacy_seed,
        )
        before = runtime.snapshot().payload
        submitted = copy.deepcopy(before["contribution"])
        submitted["payload"]["contribution"]["content"]["w2_box1"] = 50000
        after = runtime.contribute(submitted).payload
        legacy_runtime = {
            "surface": "runtime-fixed-frrs_t3",
            "before": {
                "complete": before["complete"],
                "missing": [row.get("id") for row in before["missing"]],
                "lines": [
                    {
                        "line": row["line"],
                        "computed": row["computed"],
                        "value": _plain(row["value"]),
                    }
                    for row in before["lines"]
                ],
                "contribution_fields": sorted(
                    submitted["payload"]["contribution"]["content"].keys()
                ),
            },
            "after_box1_50000": {
                "complete": after["complete"],
                "missing": [row.get("id") for row in after["missing"]],
                "lines": [
                    {
                        "line": row["line"],
                        "computed": row["computed"],
                        "value": _plain(row["value"]),
                        "group": row["group"],
                        "change": row["change"],
                    }
                    for row in after["lines"]
                ],
            },
            "legacy_seed_has_box2_withholding": any(
                "tax.us.2025.w2.box2-withholding" in json.dumps(act)
                for act in legacy_seed
            ),
        }

    # The current-core helper is a complete synthetic return, not an entry seed:
    # it already has W-2 Box 1 and Box 2 findings. Adopt and resolve it on the
    # actually published v70/v68 release and registry chain.
    current_acts = _finish(
        copy.deepcopy(current_core_returns.base_return()),
        package_path=PACKAGE_PATH,
        package_version="v70",
        release_path=RELEASE_PATH,
        release_version="v68",
        note="P0 synthetic current-core v70 evidence probe",
    )
    current_scope = {"jurisdiction": "us", "year": "2025"}
    current_user = current_core_returns.USER
    current_surface = _resolve(
        current_acts,
        RELEASE_DIR,
        run_scope=current_scope,
        scope_user=current_user,
    )
    if not isinstance(current_surface, PublicationSurface):
        raise RuntimeError(f"current v70 surface did not resolve: {current_surface}")
    current_acts = _handover(current_acts, surface=current_surface, reconfirm=True)
    current_run = _run(
        current_acts,
        current_surface,
        "demo.entry-loop.p0.core-v70-complete",
        run_scope=current_scope,
        scope_user=current_user,
    )
    changed_box1_acts = _change_only_box1(current_acts, 90000.0)
    changed_box1_run = _run(
        changed_box1_acts,
        current_surface,
        "demo.entry-loop.p0.core-v70-box1-changed",
        run_scope=current_scope,
        scope_user=current_user,
    )

    # Re-pin, but do not alter, a separate copy of the thin v6 seed. This tests
    # completeness on v70; it does not claim that the fixture is a migration.
    thin_v70_acts = _repin_thin_seed_to_v70()
    thin_surface = _resolve(
        thin_v70_acts,
        RELEASE_DIR,
        run_scope=RUN_SCOPE,
        scope_user=SCOPE_USER,
    )
    thin_v70_run = _run(
        thin_v70_acts,
        thin_surface,
        "demo.entry-loop.p0.core-v70-thin-seed",
        run_scope=RUN_SCOPE,
        scope_user=SCOPE_USER,
    ) if isinstance(thin_surface, PublicationSurface) else {"refusal": thin_surface.reason}
    fixed_surface_resolution = _resolve(
        thin_v70_acts,
        LEGACY_RELEASE_DIR,
        run_scope=RUN_SCOPE,
        scope_user=SCOPE_USER,
    )
    try:
        _line_values(thin_v70_run["model"])
        line_values_result = "accepted"
    except (KeyError, TypeError, EntryLoopError) as exc:
        line_values_result = str(exc)

    current_fields = _form1040_fields(current_run["model"])
    changed_box1_fields = _form1040_fields(changed_box1_run["model"])
    all_fields = _all_form_fields(current_run["model"])
    form_counts = Counter(str(row["form_id"]) for row in all_fields)
    line_forms: dict[str, set[str]] = {}
    for row in all_fields:
        line_forms.setdefault(row["line"], set()).add(str(row["form_id"]))
    duplicate_lines_across_forms = [
        {"line": line, "form_ids": sorted(forms)}
        for line, forms in sorted(line_forms.items())
        if len(forms) > 1
    ]
    non_numeric_1040_fields = [
        row
        for row in current_fields
        if row["value_type"] not in {"int", "float"}
    ]
    thin_fields = (
        _form1040_fields(thin_v70_run["model"])
        if "model" in thin_v70_run
        else []
    )
    current_publications = current_run["publications"]
    current_line_values = {
        line: _plain(current_publications[symbol]["value"])
        for line, symbol in V70_LINE_SYMBOLS.items()
        if symbol in current_publications
    }
    baseline_by_member = {
        (str(row["id"]), str(row["version"])): row for row in current_fields
    }
    changed_by_member = {
        (str(row["id"]), str(row["version"])): row for row in changed_box1_fields
    }
    changed_form1040_fields = []
    for identity, before in sorted(baseline_by_member.items()):
        after = changed_by_member.get(identity)
        if after is None:
            continue
        if before["disposition"] != after["disposition"] or before["value"] != after["value"]:
            changed_form1040_fields.append(
                {
                    "id": before["id"],
                    "version": before["version"],
                    "line": before["line"],
                    "before": before["value"],
                    "after": after["value"],
                }
            )
    profile_observed = {}
    for role, members in PROFILE_BY_PACKAGE["v70"].items():
        profile_observed[role] = []
        for member in members:
            identity = (member["id"], member["version"])
            before = baseline_by_member[identity]
            after = changed_by_member[identity]
            profile_observed[role].append(
                {
                    "id": member["id"],
                    "version": member["version"],
                    "line": before["line"],
                    "before": before["value"],
                    "after": after["value"],
                    "changed": before["value"] != after["value"]
                    or before["disposition"] != after["disposition"],
                }
            )
    package_bindings = package.get("input_bindings", [])
    optional_defaults = [
        row for row in package_bindings if row.get("mode") == "optional_default"
    ]
    required_bindings = [row for row in package_bindings if row.get("mode") == "required"]
    legacy_entry_refusal = None
    try:
        with TemporaryDirectory() as scratch:
            SyntheticW2EntryRuntime(
                WorkspaceCapability(Path(scratch) / "thin-v70-entry"),
                repo_root=ROOT,
                seed_acts=thin_v70_acts,
            )
    except EntryLoopError as exc:
        legacy_entry_refusal = str(exc)

    result = {
        "probe": "entry-loop-rescope-p0",
        "inputs": {
            "package": f"{package['id']}@{package['version']}",
            "package_checksum": package["package_checksum"],
            "release": f"{release['id']}@{release['version']}",
            "release_checksum": hashlib.sha256(RELEASE_PATH.read_bytes()).hexdigest(),
            "release_registry_checksum": release.get("package_registry_sha256"),
            "registry": REGISTRY_PATH.relative_to(ROOT).as_posix(),
            "helper": "tests/helpers/current_core_returns.py::base_return",
            "legacy_seed": "packages/sample_data/entry_loop_t1/workspace/acts.jsonl",
            "synthetic": True,
        },
        "surface_resolution": {
            "current_adopted_v70": _surface_summary(current_surface),
            "same_v70_adoption_on_entry_loop_fixed_surface": _surface_summary(
                fixed_surface_resolution
            ),
        },
        "form_field_v3_schema": {
            "properties": sorted(form_schema.get("properties", {}).keys()),
            "has_explicit_value_type": "value_type" in form_schema.get("properties", {}),
            "has_entry_role": "entry_role" in form_schema.get("properties", {}),
        },
        "v70_input_binding_modes": {
            "required_count": len(required_bindings),
            "optional_default_count": len(optional_defaults),
            "optional_default_examples": [row.get("symbol") for row in optional_defaults[:6]],
        },
        "current_core_v70_run": {
            "refusal": current_run.get("refusal"),
            "blocked": _blocked_summary(current_run["report"]),
            "form1040_field_count": len(current_fields),
            "form1040_lines": [row["line"] for row in current_fields],
            "all_package_form_field_count": len(all_fields),
            "form_id_counts": dict(sorted(form_counts.items())),
            "duplicate_line_ids_across_forms": duplicate_lines_across_forms[:8],
            "non_numeric_form1040_field_examples": non_numeric_1040_fields[:8],
            "evaluation_line_constants_in_v6_runtime": list(EVALUATION_LINES),
            "expected_impact_constants_in_v6_runtime": list(EXPECTED_IMPACT_LINES),
            "selected_v70_field_states": _field_states(
                current_fields, list(V70_PROFILE_LINES)
            ),
            "observed_but_not_in_box1_entry_profile": _field_states(
                current_fields, list(V70_OBSERVATION_ONLY_LINES)
            ),
            "bounded_profile_candidate_by_adopted_core": PROFILE_BY_PACKAGE,
            "published_values": current_line_values,
            "controlled_box1_change": {
                "only_input_changed": "W-2 Box 1 finding: 50,000 -> 90,000",
                "baseline_blocked": _blocked_summary(current_run["report"]),
                "changed_input_blocked": _blocked_summary(changed_box1_run["report"]),
                "changed_form1040_fields": changed_form1040_fields,
                "profile_membership_observed": profile_observed,
            },
        },
        "thin_v6_seed_re_pinned_to_v70": {
            "surface_resolution": _surface_summary(thin_surface),
            "entry_runtime_result_on_fixed_surface": legacy_entry_refusal,
            "blocked": _blocked_summary(thin_v70_run["report"])
            if "report" in thin_v70_run
            else None,
            "selected_v70_field_states": _field_states(
                thin_fields, list(V70_LINE_SYMBOLS.keys())
            ),
            "legacy_v6_line_selector_result": line_values_result,
        },
        "legacy_v6_runtime_unchanged_seed": legacy_runtime,
        "recording_and_execution": {
            "legacy_entry_accepts_only": ["w2_box1"],
            "legacy_first_entry_recorder": [
                "contribution act",
                "W-2 member-transition for Box 1",
                "W-2 family closure assertion",
            ],
            "current_core_helper_box2_is_entry_control": False,
            "line_values_source": "live_coordinate_run + package rules + resolved presentation fields",
            "optional_defaults_source": "package input_bindings optional_default -> exact fact-type parameter in Runner",
        },
    }
    print(json.dumps(_plain(result), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
