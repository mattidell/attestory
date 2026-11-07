"""What core v79 does with a sale the filer got no Form 1099-B for.

P0 evidence for docs/phases/engine-breadth/milestones/f8949-boxes-cf.md.
Synthetic demo.* findings on the harness wage return. Reads production
content; reuses the noncovered-sales evidence helpers (probe, prototype,
p0b, track0) the v79 tests already drive. Writes cf-probe-output.json
beside this file. Does not edit packages/.

    python3 docs/phases/engine-breadth/milestones/f8949-boxes-cf-evidence/cf_probe.py [case ...]

Core v79 has no box C or box F family and no Schedule D line 3 or line 10.
A filer with such a sale can (a) record nothing, or (b) record it on the
box B or box E family, the only families with a filer-supplied basis.
Both are measured.
"""

from __future__ import annotations

import copy
import importlib
import json
import sys
import time
import traceback
from collections import Counter
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any, Callable

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
NONCOVERED_EVIDENCE = HERE.parent / "noncovered-sales-evidence"
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(NONCOVERED_EVIDENCE))

probe: Any = importlib.import_module("probe")
proto: Any = importlib.import_module("prototype")
p0b: Any = importlib.import_module("p0b")

from packages.derivation.live import live_coordinate_run  # noqa: E402
from packages.derivation.live_workspace import WorkspaceCapability  # noqa: E402
from packages.derivation.presentation_projection import validate_presentation_model  # noqa: E402
from packages.derivation.production_resolver import PublicationSurface  # noqa: E402
from tests.helpers import current_core_returns as ccr  # noqa: E402
from tests.test_form_1099_k_income import _handover  # noqa: E402
from tests.test_refund_or_amount_owed_track1 import _finish  # noqa: E402

P = "tax.us.2025."
OUT = HERE / "cf-probe-output.json"
IN_CLASS = P + "schedule-d-boundary.noncovered-in-class"
WATCH = tuple(P + name for name in (
    "schedule-d.line-1a", "schedule-d.line-2", "schedule-d.line-3", "schedule-d.line-7",
    "schedule-d.line-8a", "schedule-d.line-9", "schedule-d.line-10", "schedule-d.line-15",
    "schedule-d.line-16", "schedule-d.line-21", "form1040.line-7a", "form1040.line-15",
    "form1040.line-16",
))
SYMBOLS = (P + "capital-gains.selected-preferential-base",)
TEXT_LINES = tuple(P + f"schedule-d.line-{n}" for n in ("2", "3", "9", "10"))


def pin_v79() -> None:
    probe.PACKAGE = "package.core-calculations.v79.json"
    probe.PACKAGE_VERSION = "v79"
    probe.REGISTRY = "published-packages.v77.json"
    probe.RELEASE = "demo.release.sli-worksheet-integration.2025.v77.json"
    probe.RELEASE_VERSION = "v77"


def install_v79_noncovered() -> None:
    """Point the prototype helpers at the production v79 noncovered bundles.

    The same step tests/test_noncovered_sales_v79.py takes.
    """
    content = probe.CONTENT
    proto.USE_V2 = True
    bundles = {
        key: json.loads((content / name).read_text(encoding="utf-8"))
        for key, name in (
            ("st", "f1099b-noncovered-st.bundle.json"),
            ("lt", "f1099b-noncovered-lt.bundle.json"),
            ("boundary", "schedule-d-boundary-noncovered.bundle.json"),
        )
    }
    facts = {fact["id"]: fact for bundle in bundles.values() for fact in bundle["fact_types"]}
    families, member_of = [], {}
    for path in sorted(content.glob("family.f1099b-noncovered-*.json")):
        body = json.loads(path.read_text(encoding="utf-8"))
        families.append(body["id"])
        member_of[body["id"]] = body["member_predicate"]["fact_type"]
    proto.BUILT.clear()
    proto.BUILT.update({"bundles": bundles, "facts": facts, "families": families, "member_of": member_of})


# ---- case builders -------------------------------------------------------


def on_be(acts: list[dict[str, Any]], term: str, proceeds: float, basis: float | None, tag: str,
          adjustment: float | None = None, *, scalars: tuple[str, ...] = ("proceeds", "basis", "adjustment")) -> None:
    """Record one sale on the box B (st) or box E (lt) families, in place."""
    value: dict[str, Any] = {
        "proceeds": proceeds,
        "basis_reported_to_irs": "no",
        "long_term": "yes" if term == "lt" else "no",
        "wash_disallowed": 0 if adjustment is None else adjustment,
    }
    if basis is not None:
        value["basis"] = basis
    proto._record(acts, proto._family_id(term, None), value, tag)
    if "proceeds" in scalars:
        proto._record(acts, proto._family_id(term, "proceeds"), proceeds, tag)
    if "basis" in scalars and basis is not None:
        proto._record(acts, proto._family_id(term, "basis"), basis, tag)
    if "adjustment" in scalars and adjustment is not None:
        proto._record(acts, proto._family_id(term, "adjustment"), adjustment, tag)


def covered_a(acts: list[dict[str, Any]], proceeds: float, basis: float, tag: str) -> list[dict[str, Any]]:
    """A basis-reported short-term sale (box A via line 1a)."""
    sale = probe.txn(proceeds=proceeds, basis=basis, long_term="no", reported="yes", covered="yes")
    acts = probe.record(acts, P + "f1099b.covered-st", sale, tag)
    acts = probe.record(acts, P + "f1099b.covered-st-proceeds", proceeds, tag + "p")
    return probe.record(acts, P + "f1099b.covered-st-basis", basis, tag + "b")


def answered(acts: list[dict[str, Any]], *, q1: str, form8949: str = "no", other: str | None = "no",
             in_class: str | None = None, tag: str) -> list[dict[str, Any]]:
    """Answer the noncovered question last (so it is not stale), then the boundaries."""
    p0b._assert_answer(acts, q1, f"{q1}-{tag}")
    acts = probe.boundary(acts, form8949, other)
    if in_class is not None:
        acts = probe.answer(acts, IN_CLASS, in_class, "inclass")
    return ccr._renumbered(acts)


def opened() -> list[dict[str, Any]]:
    acts = copy.deepcopy(ccr.base_return())
    p0b._open(acts, None)
    return acts


def cases() -> dict[str, Callable[[], list[dict[str, Any]]]]:
    def wage_one_no() -> list[dict[str, Any]]:
        return p0b._with_answer(ccr.base_return(), "no")

    def unrecorded(form8949: str, other: str | None, in_class: str | None) -> Callable[[], list[dict[str, Any]]]:
        def build() -> list[dict[str, Any]]:
            return answered(opened(), q1="no", form8949=form8949, other=other, in_class=in_class, tag="unrec")
        return build

    def f_gain_on_e(in_class: str) -> Callable[[], list[dict[str, Any]]]:
        def build() -> list[dict[str, Any]]:
            acts = opened()
            on_be(acts, "lt", 6000.0, 2000.0, "fgain")
            return answered(acts, q1="yes", in_class=in_class, tag="fgain")
        return build

    def c_loss_on_b(in_class: str) -> Callable[[], list[dict[str, Any]]]:
        def build() -> list[dict[str, Any]]:
            acts = opened()
            on_be(acts, "st", 2000.0, 8000.0, "closs")
            return answered(acts, q1="yes", in_class=in_class, tag="closs")
        return build

    def c_wash_on_b(in_class: str) -> Callable[[], list[dict[str, Any]]]:
        def build() -> list[dict[str, Any]]:
            acts = opened()
            on_be(acts, "st", 4000.0, 7000.0, "cwash", adjustment=1000.0)
            return answered(acts, q1="yes", in_class=in_class, tag="cwash")
        return build

    def mixed(in_class: str) -> Callable[[], list[dict[str, Any]]]:
        def build() -> list[dict[str, Any]]:
            acts = opened()
            on_be(acts, "st", 3000.0, 3500.0, "mxb")
            on_be(acts, "st", 2500.0, 1000.0, "mxc")
            on_be(acts, "lt", 6000.0, 2000.0, "mxf")
            acts = covered_a(ccr._renumbered(acts), 5000.0, 4000.0, "mxa")
            return answered(acts, q1="yes", in_class=in_class, tag="mx")
        return build

    def missing(scalars: tuple[str, ...], tag: str) -> Callable[[], list[dict[str, Any]]]:
        def build() -> list[dict[str, Any]]:
            acts = opened()
            on_be(acts, "lt", 6000.0, 2000.0, tag, scalars=scalars)
            return answered(acts, q1="yes", in_class="yes", tag=tag)
        return build

    def basis_object_missing() -> list[dict[str, Any]]:
        acts = opened()
        on_be(acts, "lt", 6000.0, None, "objnob", scalars=("proceeds",))
        return answered(acts, q1="yes", in_class="yes", tag="objnob")

    return {
        "wage_one_no": wage_one_no,
        # (a) the sale is not recorded anywhere; the filer answers honestly.
        "c_unrecorded_8949_no": unrecorded("no", None, None),
        "c_unrecorded_8949_no_other_no": unrecorded("no", "no", None),
        "c_unrecorded_all_no": unrecorded("no", "no", "no"),
        # (b) the sale is recorded on the box B / box E families.
        "f_gain_on_e_in_class_no": f_gain_on_e("no"),
        "f_gain_on_e_in_class_yes": f_gain_on_e("yes"),
        "c_loss_on_b_in_class_no": c_loss_on_b("no"),
        "c_loss_on_b_in_class_yes": c_loss_on_b("yes"),
        "c_wash_on_b_in_class_no": c_wash_on_b("no"),
        "c_wash_on_b_in_class_yes": c_wash_on_b("yes"),
        "mixed_abcf_in_class_no": mixed("no"),
        "mixed_abcf_in_class_yes": mixed("yes"),
        # Missing amounts on the v79 box E families (the pattern a successor copies).
        "e_basis_scalar_missing": missing(("proceeds",), "nobasis"),
        "e_proceeds_scalar_missing": missing(("basis",), "noproc"),
        "e_basis_object_missing": basis_object_missing,
    }


# ---- run and summarize ---------------------------------------------------


def summarize(outcome: Any) -> dict[str, Any]:
    if outcome.refusal is not None:
        return {"refusal": {"reason": outcome.refusal.reason, "detail": probe.scrub(str(outcome.refusal.detail))[:400]}}
    report = json.loads(outcome.output_path.read_text(encoding="utf-8"))
    model = json.loads(outcome.presentation_path.read_text(encoding="utf-8"))
    summary: dict[str, Any] = {"stop_reason": report.get("stop_reason")}
    try:
        validate_presentation_model(model)
        summary["presentation_valid"] = True
    except Exception as exc:  # noqa: BLE001 — record the validator's refusal
        summary["presentation_valid"] = False
        summary["presentation_error"] = probe.scrub(str(exc))[:400]
    ids = [str((s.get("field") or {}).get("id")) for s in model.get("sections") or [] if (s.get("field") or {}).get("id")]
    summary["duplicate_field_ids"] = sorted(i for i, n in Counter(ids).items() if n > 1)
    lines: dict[str, Any] = {}
    texts: dict[str, Any] = {}
    sentences: list[str] = []
    for section in model.get("sections") or []:
        field_id = str((section.get("field") or {}).get("id") or "")
        resolved = section.get("resolved") or {}
        for reason in resolved.get("reasons") or []:
            if isinstance(reason, dict) and reason.get("sentence"):
                sentence = probe.scrub(str(reason["sentence"]))[:240]
                if sentence not in sentences:
                    sentences.append(sentence)
        if field_id in TEXT_LINES:
            instruction = ((section.get("field") or {}).get("dispositions") or {}).get(str(resolved.get("disposition"))) or {}
            reasons = [probe.scrub(str(r["sentence"]))[:240] for r in (resolved.get("reasons") or [])
                       if isinstance(r, dict) and r.get("sentence")]
            texts[field_id.removeprefix(P)] = {"explain": instruction.get("explain"), "reasons": reasons[:4]}
        if field_id in WATCH:
            value = resolved.get("value")
            if isinstance(value, float) and value.is_integer():
                value = int(value)
            lines[field_id.removeprefix(P)] = [resolved.get("disposition"), value]
    summary["lines"] = lines
    summary["line_text"] = texts
    summary["missing_lines"] = sorted(w.removeprefix(P) for w in WATCH if w.removeprefix(P) not in lines)
    summary["symbols"] = {
        str(item.finding.get("symbol")).removeprefix(P): item.finding.get("value")
        for item in outcome.publications or ()
        if str(item.finding.get("symbol")) in SYMBOLS
    }
    summary["attachments"] = {
        str(a.get("id")).split(".")[-1]: (a.get("resolved") or {}).get("disposition")
        for a in model.get("attachments") or []
        if "8949" in str(a.get("id")) or "schedule-d" in str(a.get("id"))
    }
    blocked = []
    for row in report.get("dispositions") or []:
        if row.get("disposition") != "blocked":
            continue
        artifact = str(row.get("artifact_id", ""))
        if not any(t in artifact for t in ("schedule-d", "line7a", "preferential", "8949", "noncovered", "f1099b")):
            continue
        blocked.append({"artifact": artifact.removeprefix(P), "code": row.get("code"),
                        "missing": [str(m).removeprefix(P) for m in (row.get("missing") or [])][:6]})
    summary["blocked"] = blocked[:30]
    summary["questions"] = [s for s in sentences if s.endswith("?")][:12]
    groups = []
    for group in model.get("citationGroups") or []:
        if "8949" not in str(group.get("id")):
            continue
        groups.extend(str(part.get("heading") or "") for part in group.get("parts") or [])
    summary["f8949_parts"] = groups
    return summary


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
        return summarize(outcome)


def execute(build: Callable[[], list[dict[str, Any]]], run_id: str) -> dict[str, Any]:
    started = time.monotonic()
    try:
        result = run_case(build(), run_id)
    except Exception as exc:  # noqa: BLE001 — record the failure instead of hiding it
        result = {"error": type(exc).__name__, "message": probe.scrub(str(exc))[:600],
                  "trace": probe.scrub(traceback.format_exc())[-500:]}
    result["seconds"] = round(time.monotonic() - started, 1)
    return result


def main() -> None:
    pin_v79()
    install_v79_noncovered()
    selected = set(sys.argv[1:])
    results: dict[str, Any] = {"package": "core-calculations v79", "release": "v77", "cases": {}}
    for name, build in cases().items():
        if selected and name not in selected:
            continue
        results["cases"][name] = execute(build, f"demo.cf.p0.{name}")
        r = results["cases"][name]
        print(name, r.get("error") or r.get("stop_reason"), r.get("seconds"), flush=True)
    if selected and OUT.exists():
        merged = json.loads(OUT.read_text(encoding="utf-8"))
        merged["cases"].update(results["cases"])
        results = merged
    OUT.write_text(probe.scrub(json.dumps(results, indent=1, sort_keys=True)) + "\n", encoding="utf-8")
    print(f"wrote {OUT.name}", flush=True)


if __name__ == "__main__":
    main()
