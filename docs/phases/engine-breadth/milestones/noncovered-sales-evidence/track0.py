"""Track 0 adversarial closure probes for noncovered sales.

Reuses probe.py and prototype.py. Builds a scratch core v79 under a temp
directory and runs live_coordinate_run. Writes track0-output.json beside
this file. Does not edit packages/.

    python3 docs/phases/engine-breadth/milestones/noncovered-sales-evidence/track0.py [mode ...]

Modes: wage, standard, one_question, version_bump, v2, all.
`all` runs the experiments first and leaves the standard package last,
so prototype-rules/ matches that build.
"""

from __future__ import annotations

import copy
import json
import sys
import tempfile
import time
import traceback
from collections import Counter
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(HERE))

import probe  # noqa: E402
import prototype as proto  # noqa: E402
from packages.derivation.live import live_coordinate_run  # noqa: E402
from packages.derivation.live_workspace import WorkspaceCapability  # noqa: E402
from packages.derivation.presentation_projection import validate_presentation_model  # noqa: E402
from packages.derivation.production_resolver import PublicationSurface  # noqa: E402
from packages.kernel.horizons import HorizonModelError  # noqa: E402
from tests.helpers import current_core_returns as ccr  # noqa: E402
from tests.test_form_1099_k_income import _handover  # noqa: E402
from tests.test_refund_or_amount_owed_track1 import _finish  # noqa: E402

P = proto.P
NONCOVERED = proto.NONCOVERED
SHARED = P + "f1099b.noncovered-sold.source-closure"
QUESTION = "Did you sell any securities whose basis was not reported to the IRS?"
OUT = HERE / "track0-output.json"
PIN_KEYS = (
    "CONTENT",
    "RELEASE_DIR",
    "PACKAGE",
    "PACKAGE_VERSION",
    "REGISTRY",
    "RELEASE",
    "RELEASE_VERSION",
)
ORIGIN = {key: getattr(probe, key) for key in PIN_KEYS}
ORIGINAL_DECL = __import__("packages.tax.loader", fromlist=["domain_package_companion_declarations"]).domain_package_companion_declarations
SYMBOLS = (
    P + "schedule-d.line-2",
    P + "schedule-d.line-7",
    P + "schedule-d.line-9",
    P + "schedule-d.line-15",
    P + "schedule-d.line-16",
    P + "schedule-d.line-21",
    P + "capital-gains.line7a-total",
    P + "form1040.line-7a",
    P + "capital-gains.selected-preferential-base",
    P + "form8949.disposition",
    P + "schedule-d.line-1a",
    P + "schedule-d.line-8a",
    P + "schedule-d.line-1a-gain",
    P + "schedule-d.line-8a-gain",
)
WATCH = (
    P + "schedule-d.line-1a",
    P + "schedule-d.line-2",
    P + "schedule-d.line-7",
    P + "schedule-d.line-8a",
    P + "schedule-d.line-9",
    P + "schedule-d.line-15",
    P + "schedule-d.line-16",
    P + "schedule-d.line-21",
    P + "form1040.line-7a",
    P + "form1040.line-15",
    P + "form1040.line-16",
    P + "capital-gains.selected-preferential-base",
)


def _reset_probe() -> None:
    for key, value in ORIGIN.items():
        setattr(probe, key, value)


def _snapshot() -> dict[str, Any]:
    return {key: getattr(probe, key) for key in PIN_KEYS}


def _restore(snap: dict[str, Any]) -> None:
    for key, value in snap.items():
        setattr(probe, key, value)


def _declare_once() -> None:
    def with_v79() -> dict[tuple[str, str], dict[str, Any]]:
        declarations = dict(ORIGINAL_DECL())
        declarations[(P + "package.core-calculations", "v79")] = declarations[
            (P + "package.core-calculations", "v78")
        ]
        return declarations

    proto.loader.domain_package_companion_declarations = with_v79  # type: ignore[method-assign]


def _load() -> dict[str, Any]:
    if OUT.exists():
        return json.loads(OUT.read_text(encoding="utf-8"))
    return {"source_ref": "bb766465641abe3fb367a527701a5ca7393fb488", "modes": {}}


def _save(payload: dict[str, Any]) -> None:
    text = probe.scrub(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    OUT.write_text(text, encoding="utf-8")


def _succinct(report: dict[str, Any]) -> dict[str, Any]:
    package = report.get("package") or {}
    release = report.get("release") or {}
    inherited = report.get("inherited_inconsistencies") or ()
    return {
        "package": package.get("version"),
        "release": release.get("version"),
        "members": report.get("members"),
        "activity_anys": report.get("activity_anys"),
        "inherited_inconsistencies": [list(row) for row in inherited],
    }


def run_case(acts: list[dict[str, Any]], run_id: str) -> dict[str, Any]:
    surface = PublicationSurface(probe.RELEASE_DIR, probe.CONTENT / probe.REGISTRY, probe.CONTENT)
    finished = _handover(
        _finish(
            copy.deepcopy(acts),
            package_path=probe.CONTENT / probe.PACKAGE,
            package_version=probe.PACKAGE_VERSION,
            release_path=probe.RELEASE_DIR / probe.RELEASE,
            release_version=probe.RELEASE_VERSION,
            note=run_id,
        ),
        surface=surface,
        reconfirm=True,
    )
    with TemporaryDirectory() as tmp:
        outcome = live_coordinate_run(
            WorkspaceCapability(Path(tmp) / "L"),
            repo_root=ccr.ROOT,
            authoritative_acts=finished,
            workspace_revision=len(finished),
            run_scope={"jurisdiction": "us", "year": probe.YEAR},
            scope_user=ccr.USER,
            request={"schema": "run-request.v1"},
            run_id=run_id,
            governance_pins=[],
            surface=surface,
            output_name="out.json",
        )
        summary = probe.summarize_run(outcome)
        summary["presentation_valid"] = None
        if outcome.presentation_path is not None and outcome.refusal is None:
            model = json.loads(outcome.presentation_path.read_text(encoding="utf-8"))
            try:
                validate_presentation_model(model)
                summary["presentation_valid"] = True
            except Exception as exc:  # noqa: BLE001 — the probe records the validator's refusal
                summary["presentation_valid"] = False
                summary["presentation_error"] = probe.scrub(str(exc))[:500]
            ids = [
                str((section.get("field") or {}).get("id"))
                for section in model.get("sections") or []
                if (section.get("field") or {}).get("id")
            ]
            summary["duplicate_field_ids"] = sorted(item for item, count in Counter(ids).items() if count > 1)
            summary["section_count"] = len(ids)
        return summary


def _execute(acts: list[dict[str, Any]], run_id: str) -> dict[str, Any]:
    started = time.monotonic()
    try:
        result = run_case(acts, run_id)
    except Exception as exc:  # noqa: BLE001 — record the failure, including HorizonModelError
        result = {
            "error": type(exc).__name__,
            "message": probe.scrub(str(exc))[:800],
            "horizon_refused": isinstance(exc, HorizonModelError),
            "trace": probe.scrub(traceback.format_exc())[-600:],
        }
    result["seconds"] = round(time.monotonic() - started, 2)
    return result


def _line_map(result: dict[str, Any]) -> dict[str, Any]:
    found = {}
    for row in result.get("lines") or []:
        if row.get("id") in WATCH:
            found[row["id"]] = {"disposition": row.get("disposition"), "value": row.get("value")}
    return found


def _digest(result: dict[str, Any]) -> dict[str, Any]:
    kept = {
        "error": result.get("error"),
        "message": result.get("message"),
        "horizon_refused": result.get("horizon_refused"),
        "refusal": result.get("refusal"),
        "stop_reason": result.get("stop_reason"),
        "seconds": result.get("seconds"),
        "presentation_valid": result.get("presentation_valid"),
        "presentation_error": result.get("presentation_error"),
        "duplicate_field_ids": result.get("duplicate_field_ids"),
        "section_count": result.get("section_count"),
        "lines": _line_map(result),
        "attachments": result.get("attachments"),
        "groups": result.get("groups"),
        "blocked": [
            row for row in (result.get("blocked") or [])
            if any(token in str(row.get("artifact_id", "")) for token in (
                "schedule-d", "line7a", "preferential", "8949", "noncovered", "f1099b", "line-1a", "line-8a",
            ))
        ][:24],
    }
    return {key: value for key, value in kept.items() if value not in (None, [], {})}


def _renumber(acts: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return ccr._renumbered(acts)


def _families_on(acts: list[dict[str, Any]]) -> list[dict[str, Any]]:
    out = copy.deepcopy(acts)
    for bundle in proto.BUILT["bundles"].values():
        proto._adopt(out, bundle)
    proto._open_families(out, set())
    return out


def _standard_cases() -> dict[str, list[dict[str, Any]]]:
    built = proto.cases()
    gain_no = proto._prepared()
    proto._sale(gain_no, "lt", 6000.0, 2000.0, "ltno")
    empty_no = proto._with_boundaries(proto._prepared(), "no")
    net = proto._prepared()
    proto._sale(net, "lt", 5000.0, 5000.0, "net0")
    covered_no = proto._prepared()
    covered_no = probe.direct(covered_no, "lt", 6000.0, 2000.0, "cno")
    covered_no = probe.boundary(covered_no, "no", "no")
    flagged = proto._prepared()
    flagged = probe.direct(flagged, "lt", 6000.0, 2000.0, "mis")
    yes_txn = probe.txn(proceeds=6000.0, basis=2000.0, long_term="yes", reported="yes", covered="yes")
    no_txn = probe.txn(proceeds=6000.0, basis=2000.0, long_term="yes", reported="no", covered="yes")
    corrected = proto._prepared()
    corrected = probe.record(corrected, P + "f1099b.covered-lt", yes_txn, "corr")
    corrected = probe.record(corrected, P + "f1099b.covered-lt-proceeds", 6000.0, "corrp")
    corrected = probe.record(corrected, P + "f1099b.covered-lt-basis", 2000.0, "corrb")
    corrected_no = probe.correct(copy.deepcopy(corrected), P + "f1099b.covered-lt", no_txn, "corr")
    late = proto._prepared()
    late_value = {
        "proceeds": 6000.0,
        "basis": 2000.0,
        "basis_reported_to_irs": "no",
        "long_term": "yes",
    }
    if proto.USE_V2:
        late_value["wash_disallowed"] = 0
    for family_id, value in (
        (proto._family_id("lt", None), late_value),
        (proto._family_id("lt", "proceeds"), 6000.0),
        (proto._family_id("lt", "basis"), 2000.0),
    ):
        proto._record(late, family_id, value, "late", close=False)
    late = proto._with_boundaries(late, "yes")
    reclosed = copy.deepcopy(late)
    for family_id in (
        proto._family_id("lt", None),
        proto._family_id("lt", "proceeds"),
        proto._family_id("lt", "basis"),
    ):
        head = probe.horizons(reclosed, family_id)[-1]
        slug = family_id.removeprefix(P + "f1099b.")
        probe._close(reclosed, family_id + ".source-closure", head, f"demo.ns.late.re.{slug}")
    bad_wash = proto._prepared()
    proto._sale(bad_wash, "lt", 6000.0, 2000.0, "badw", adjustment=500.0)
    neighbors = {
        "wage": ccr.base_return(),
        "foreign_tax": ccr.add_foreign_tax_1099div(ccr.base_return(), [601.0]),
        "exempt_interest": ccr.add_tax_exempt_interest_1099int(ccr.base_return(), [50.0]),
        "student_loan": ccr.add_student_loan_interest_1098e(ccr.base_return(), [200.0]),
    }
    cases = {
        "wage_closed_empty": built["wage_closed_empty"],
        "wage_unclosed": built["wage_unclosed"],
        "wage_boundary_no": _renumber(empty_no),
        "lt_gain": built["lt_gain"],
        "st_loss": built["st_loss"],
        "wash": built["wash"],
        "mixed": built["mixed"],
        "boundary_no_gain": built["boundary_no"],
        "basis_unclosed": built["basis_unclosed"],
        "basis_omitted": built["basis_omitted"],
        "net_zero": _renumber(proto._with_boundaries(net, "yes")),
        "covered_both_boundaries_no": _renumber(covered_no),
        "covered_flag_no_path_a": _renumber(flagged),
        "covered_flag_yes": _renumber(corrected),
        "covered_flag_corrected_to_no": _renumber(corrected_no),
        "late_member_unclosed": _renumber(late),
        "late_member_reclosed": _renumber(reclosed),
        "code_w_on_gain": _renumber(proto._with_boundaries(bad_wash, "yes")),
    }
    for name, acts in neighbors.items():
        cases["v79_" + name] = _renumber(_families_on(acts))
    cases["_v78"] = neighbors
    return cases


def _static_surface() -> dict[str, Any]:
    package = json.loads((probe.CONTENT / probe.PACKAGE).read_text(encoding="utf-8"))
    members = {(row["id"], row["version"]) for row in package["members"]}
    publishers: dict[str, list[str]] = {symbol: [] for symbol in SYMBOLS}
    binders: dict[str, list[str]] = {symbol: [] for symbol in SYMBOLS}
    requirers: dict[str, list[str]] = {symbol: [] for symbol in SYMBOLS}
    for path in probe.CONTENT.glob("*.json"):
        try:
            body = json.loads(path.read_text(encoding="utf-8"))
        except ValueError:
            continue
        if not isinstance(body, dict) or "id" not in body or "version" not in body:
            continue
        if (body["id"], body["version"]) not in members:
            continue
        pin = f"{body['id']}@{body['version']}"
        published = body.get("publishes")
        if published in publishers:
            publishers[published].append(pin)
        bound = body.get("binds_symbol")
        if bound in binders:
            binders[bound].append(pin)
        for name in body.get("requires") or []:
            if name in requirers:
                requirers[name].append(pin)
        text = json.dumps(body)
        if "attachment.f8949" in str(body.get("id")) or body.get("id", "").endswith("rule.attachment.f8949"):
            binders[P + "form8949.disposition"].append(pin + " attachment-rule")
    entrypoints = [
        f"{row['id']}@{row['version']}"
        for row in package.get("entrypoints") or []
        if any(token in row["id"] for token in (
            "schedule-d-line", "line7a", "preferential", "attachment.f8949", "form1040-line7a",
        ))
    ]
    return {
        "publishers": publishers,
        "binders": binders,
        "requirers": {key: value for key, value in requirers.items() if value},
        "entrypoints": entrypoints,
    }


def _claim_shape() -> dict[str, Any]:
    preferential = json.loads((HERE / "prototype-rules" / "rule.selected-preferential-base.v7.json").read_text(encoding="utf-8"))
    gate_names: list[list[str]] = []

    def walk(node: Any) -> None:
        if isinstance(node, dict):
            if node.get("op") == "any":
                names = [
                    (arg.get("left") or {}).get("name")
                    for arg in node.get("args") or []
                    if isinstance(arg, dict) and arg.get("op") == "categorical_compare"
                ]
                if names:
                    gate_names.append([str(name) for name in names])
            for value in node.values():
                walk(value)
        elif isinstance(node, list):
            for item in node:
                walk(item)

    walk(preferential)
    mappings = []
    for path in sorted((HERE / "prototype-rules").glob("closure-mapping*.json")):
        body = json.loads(path.read_text(encoding="utf-8"))
        mappings.append({
            "id": body["id"],
            "family": body["family"]["id"],
            "closure_fact_type": body["closure_fact_type"]["id"],
            "closure_question": body["closure_question"],
        })
    return {
        "preferential_version": preferential["version"],
        "preferential_schema": preferential["schema"],
        "categorical_anys": gate_names,
        "mappings": mappings,
    }


def _build(scratch: Path) -> dict[str, Any]:
    _reset_probe()
    proto._declare_v79 = _declare_once  # type: ignore[method-assign]
    report = proto.build(scratch)
    return _succinct(report)


def _run_named(mode: str, cases: dict[str, list[dict[str, Any]]], payload: dict[str, Any], prefix: str) -> None:
    bucket = payload["modes"].setdefault(mode, {})
    results = bucket.setdefault("cases", {})
    for name, acts in cases.items():
        if name.startswith("_"):
            continue
        print("run", mode, name, flush=True)
        results[name] = _digest(_execute(acts, f"demo.ns.t0.{prefix}.{name}"))
        _save(payload)
        print(" ", name, results[name].get("error") or results[name].get("stop_reason"), results[name].get("seconds"), flush=True)


def _use_v78() -> None:
    probe.PACKAGE = "package.core-calculations.v78.json"
    probe.PACKAGE_VERSION = "v78"
    probe.REGISTRY = "published-packages.v76.json"
    probe.RELEASE = "demo.release.sli-worksheet-integration.2025.v76.json"
    probe.RELEASE_VERSION = "v76"


def mode_standard(payload: dict[str, Any], *, only: set[str] | None = None, use_v2: bool = False) -> None:
    proto.USE_V2 = use_v2
    proto.EXTRAS = []
    with tempfile.TemporaryDirectory() as tmp:
        try:
            report = _build(Path(tmp).resolve() / "s")
        except Exception as exc:  # noqa: BLE001
            payload["modes"]["standard"] = {
                "use_v2": use_v2,
                "build_error": type(exc).__name__,
                "message": probe.scrub(str(exc))[:4000],
            }
            _save(payload)
            print("standard build failed", type(exc).__name__, flush=True)
            return
        v79 = _snapshot()
        bucket = payload["modes"].setdefault("standard", {})
        bucket.pop("build_error", None)
        bucket.pop("message", None)
        bucket["use_v2"] = use_v2
        bucket["successor"] = report
        bucket["surface"] = _static_surface()
        bucket["claims"] = _claim_shape()
        _save(payload)
        cases = _standard_cases()
        v78_cases = cases.pop("_v78")
        _use_v78()
        selected_v78 = {
            name: acts for name, acts in v78_cases.items()
            if only is None or ("v78_" + name) in only
        }
        if only is None or any(name.startswith("v78_") for name in only):
            print("v78 neighbors", flush=True)
            v78_results = bucket.setdefault("v78", {})
            for name, acts in selected_v78.items():
                print("run v78", name, flush=True)
                v78_results[name] = _digest(_execute(acts, f"demo.ns.t0.v78.{name}"))
                _save(payload)
        _restore(v79)
        selected = {name: acts for name, acts in cases.items() if only is None or name in only}
        _run_named("standard", selected, payload, "v79")


def _install_one_question() -> tuple[Any, Any]:
    original_mapping = proto._mapping
    original_boundary = proto._boundary_bundle

    def mapping(term: str, kind: str | None) -> dict[str, Any]:
        body = original_mapping(term, kind)
        body["closure_fact_type"] = {"id": SHARED, "version": "v1"}
        body["closure_question"] = QUESTION
        return body

    def boundary() -> dict[str, Any]:
        body = original_boundary()
        body["fact_types"].append(proto._fact(SHARED, QUESTION, {"type": "boolean"}, proto._closure_keys()))
        return body

    proto._mapping = mapping  # type: ignore[method-assign]
    proto._boundary_bundle = boundary  # type: ignore[method-assign]
    return original_mapping, original_boundary


def _genesis(shared_horizon: str | None = None) -> tuple[list[dict[str, Any]], dict[str, str]]:
    acts = copy.deepcopy(ccr.base_return())
    for bundle in proto.BUILT["bundles"].values():
        proto._adopt(acts, bundle)
    horizons: dict[str, str] = {}
    for family_id in proto.BUILT["families"]:
        slug = family_id.removeprefix(P + "f1099b.")
        horizon = shared_horizon or f"demo.ns.oq.{slug}.h0"
        probe._add(acts, "horizon-genesis", {
            "family": {"id": family_id, "version": "v1"},
            "scope": {"tax-year": probe.YEAR, "subject": "demo.primary"},
            "horizon_id": horizon,
        })
        horizons[family_id] = horizon
    return acts, horizons


def _closure_count(acts: list[dict[str, Any]], fact_type: str) -> int:
    count = 0
    for act in acts:
        payload = act.get("payload")
        finding = payload.get("finding") if isinstance(payload, dict) else None
        if isinstance(finding, dict) and str(finding.get("fact_id", "")).startswith(fact_type + "|"):
            count += 1
    return count


def mode_one_question(payload: dict[str, Any]) -> None:
    proto.USE_V2 = False
    proto.EXTRAS = []
    originals = _install_one_question()
    try:
        with tempfile.TemporaryDirectory() as tmp:
            try:
                report = _build(Path(tmp).resolve() / "s")
            except Exception as exc:  # noqa: BLE001
                payload["modes"]["one_question"] = {
                    "build_error": type(exc).__name__,
                    "message": probe.scrub(str(exc))[:4000],
                }
                _save(payload)
                return
            bucket = payload["modes"].setdefault("one_question", {})
            bucket.pop("build_error", None)
            bucket.pop("message", None)
            bucket["successor"] = report
            bucket["shared_fact"] = SHARED
            cases: dict[str, list[dict[str, Any]]] = {}
            notes: dict[str, Any] = {}
            one, horizons = _genesis()
            first = next(iter(horizons))
            probe._close(one, SHARED, horizons[first], "demo.ns.oq.one")
            cases["one_finding"] = _renumber(one)
            notes["one_finding"] = {"closures": _closure_count(one, SHARED), "closed_family": first}
            eight, horizons = _genesis()
            for family_id, horizon in horizons.items():
                slug = family_id.removeprefix(P + "f1099b.")
                probe._close(eight, SHARED, horizon, f"demo.ns.oq.eight.{slug}")
            cases["eight_findings"] = _renumber(eight)
            notes["eight_findings"] = {"closures": _closure_count(eight, SHARED)}
            dup, _horizons = _genesis("demo.ns.oq.shared.h0")
            cases["duplicate_horizon"] = _renumber(dup)
            notes["duplicate_horizon"] = {"horizon_id": "demo.ns.oq.shared.h0", "families": len(_horizons)}
            bucket["notes"] = notes
            _save(payload)
            _run_named("one_question", cases, payload, "oq")
    finally:
        proto._mapping, proto._boundary_bundle = originals


def _bump_covered_st(content: Path, members: list[dict[str, Any]], entrypoints: list[dict[str, Any]]) -> None:
    family = json.loads((content / "family.f1099b-covered-st.json").read_text(encoding="utf-8"))
    family["schema"] = "source-family.v2"
    family["version"] = "v2"
    (content / "family.f1099b-covered-st.v2.json").write_text(json.dumps(family, indent=2) + "\n", encoding="utf-8")
    mapping = json.loads((content / "closure-mapping.f1099b-covered-st.v2.json").read_text(encoding="utf-8"))
    mapping["version"] = "v3"
    mapping["family"] = {"id": family["id"], "version": "v2"}
    (content / "closure-mapping.f1099b-covered-st.v3.json").write_text(json.dumps(mapping, indent=2) + "\n", encoding="utf-8")
    members.append({
        "op": "replace",
        "old": {"id": family["id"], "version": "v1", "schema": "source-family.v1", "role": "source-family"},
        "new": {"id": family["id"], "version": "v2", "schema": "source-family.v2", "role": "source-family"},
    })
    members.append({
        "op": "replace",
        "old": {"id": mapping["id"], "version": "v2", "schema": "source-closure-mapping.v3", "role": "source-closure-mapping"},
        "new": {"id": mapping["id"], "version": "v3", "schema": "source-closure-mapping.v3", "role": "source-closure-mapping"},
    })
    entrypoints.append({
        "op": "replace",
        "old": {"id": family["id"], "version": "v1"},
        "new": {"id": family["id"], "version": "v2"},
    })
    # source-family.v2 does not emit the v1 family's edge to its closure
    # mapping, and this mapping is not an entrypoint. Reach it the way the
    # covered-w mappings are reached: as its own entrypoint. No handover.
    entrypoints.append({
        "op": "add",
        "value": {"id": mapping["id"], "version": "v3"},
    })


def mode_version_bump(payload: dict[str, Any]) -> None:
    proto.USE_V2 = False
    proto.EXTRAS = [_bump_covered_st]
    try:
        with tempfile.TemporaryDirectory() as tmp:
            try:
                report = _build(Path(tmp).resolve() / "s")
            except Exception as exc:  # noqa: BLE001
                payload["modes"]["version_bump"] = {
                    "build_error": type(exc).__name__,
                    "message": probe.scrub(str(exc))[:4000],
                }
                _save(payload)
                print("version bump build failed", flush=True)
                return
            bucket = payload["modes"].setdefault("version_bump", {})
            bucket.pop("build_error", None)
            bucket.pop("message", None)
            bucket["successor"] = report
            bucket["note"] = (
                "covered-st family v1 replaced by a v2 of the same meaning, mapping pin moved, no handover"
            )
            _save(payload)
            _run_named("version_bump", {"wage": ccr.base_return()}, payload, "bump")
    finally:
        proto.EXTRAS = []


def mode_v2_probe(payload: dict[str, Any]) -> None:
    """Build source-family.v2 once. The standard mode repeats it when this build works."""
    proto.USE_V2 = True
    proto.EXTRAS = []
    with tempfile.TemporaryDirectory() as tmp:
        try:
            report = _build(Path(tmp).resolve() / "s")
        except Exception as exc:  # noqa: BLE001
            payload["modes"]["v2"] = {
                "build_error": type(exc).__name__,
                "message": probe.scrub(str(exc))[:4000],
            }
            _save(payload)
            print("v2 build failed", flush=True)
            return
        payload["modes"]["v2"] = {"successor": report, "built": True}
        _save(payload)
        print("v2 build ok", report, flush=True)


def main() -> None:
    modes = sys.argv[1:] or ["all"]
    payload = _load()
    if "all" in modes:
        mode_one_question(payload)
        mode_version_bump(payload)
        mode_v2_probe(payload)
        v2_ok = "build_error" not in payload["modes"].get("v2", {"build_error": True})
        mode_standard(payload, use_v2=bool(v2_ok))
        return
    if "wage" in modes:
        mode_v2_probe(payload)
        v2_ok = "build_error" not in payload["modes"].get("v2", {"build_error": True})
        mode_standard(payload, only={"wage_closed_empty", "st_loss", "boundary_no_gain"}, use_v2=bool(v2_ok))
    if "one_question" in modes:
        mode_one_question(payload)
    if "version_bump" in modes:
        mode_version_bump(payload)
    if "v2" in modes:
        mode_v2_probe(payload)
    if "standard" in modes:
        v2_ok = "build_error" not in payload["modes"].get("v2", {"build_error": True}) and payload["modes"].get("v2", {}).get("built")
        mode_standard(payload, use_v2=bool(v2_ok))


if __name__ == "__main__":
    main()
