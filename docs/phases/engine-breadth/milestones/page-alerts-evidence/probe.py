"""Reproduce saved-page alerts on published core v91.

Evidence for docs/phases/engine-breadth/milestones/page-alerts.md.
Charter: docs/reviews/page-alerts/charter-p0.md.

Each case is a synthetic demo.* act list run through live_coordinate_run,
the presentation projection, and the saved citation-walk page. The page is
opened in headless Chrome by observe.mjs. Nothing under packages/ is edited.

    python3 probe.py <scratch-directory-outside-the-repo>
"""

from __future__ import annotations

import copy
import importlib.util
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
L12D = REPO / "docs/phases/engine-breadth/milestones/line12d-boxes-evidence"
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))
if str(L12D) not in sys.path:
    sys.path.insert(0, str(L12D))

import probe as l12d  # noqa: E402

from packages.derivation.live_session import _render_page  # noqa: E402

P = "tax.us.2025."
LUMP = P + "ss-benefits-scope.no-lump-sum-election"
PAGE = Path("packages/presentation/pages/citation-walk.v1.html")
WATCH = (
    "form1040.line-6c",
    "schedule1.top-entry",
    "form1040.line-6d",
    "form1040.line-8",
    "schedule1.line-8b",
    "schedule1.line-10",
    "form1040.line-6a",
    "form1040.line-6b",
)


def _module(name: str, path: Path) -> Any:
    module = sys.modules.get(name)
    if module is None:
        spec = importlib.util.spec_from_file_location(name, path)
        assert spec is not None and spec.loader is not None
        module = importlib.util.module_from_spec(spec)
        sys.modules[name] = module
        spec.loader.exec_module(module)
    return module


def scrub(text: str) -> str:
    text = text.replace(str(REPO), ".")
    return re.sub(r"/(?:Users|private|tmp|var|opt)/\S+", "<path>", text)


def core_v91() -> Any:
    return l12d.harness().Core("v91", "v89", "v89")


def wage(status: str = "single", answers: dict[str, Any] | None = None) -> list[dict[str, Any]]:
    """The line 12d wage return: 50,000 wages, 4,500 withheld, age and blindness stated."""
    acts = l12d.base(status)
    stated = {l12d.AGE: False, l12d.BLIND: False}
    if answers:
        stated.update(answers)
    return l12d.answer(acts, stated)


def _move_closure(acts: list[dict[str, Any]], prefix: str, successor: str) -> None:
    """Point the family's existing closure at ``successor`` and keep it after new members."""
    found = None
    for index, act in enumerate(acts):
        finding = (act.get("payload") or {}).get("finding")
        if isinstance(finding, dict) and str(finding.get("fact_id", "")).startswith(prefix + "|"):
            finding["fact_id"] = re.sub(
                r"family-horizon=[^,|]+",
                f"family-horizon={successor}",
                str(finding["fact_id"]),
            )
            found = index
            break
    if found is None:
        raise RuntimeError(f"no closure for {prefix}")
    # The caller appends; the closure must follow those members.
    closure = acts.pop(found)
    acts.append(closure)


def with_benefits(acts: list[dict[str, Any]], amount: float, *, election: str, reclose: bool = True) -> list[dict[str, Any]]:
    """One synthetic SSA-1099 on the wage return, and the lump-sum scope answer.

    The wage return already closed the benefits family empty. The statement
    advances that horizon; box 6 stays the closed-empty family the return has.
    """
    fw = _module("pa_fw", REPO / "tests/test_form_1099_withholding.py")
    built = copy.deepcopy(acts)
    head = fw._head(built, fw.SSA_FAMILY)
    successor = "demo.pa.ssa.h1"
    keys = (("statement", "demo.pa.ssa.stmt.0"),)
    fw._introduce(built, "demo.pa.ssa.stmt.0", "tax.us.ssa1099-statement")
    fw._assert(built, "demo.pa.ssa.b3.0", fw.SSA_B3, keys, amount)
    fw._assert(built, "demo.pa.ssa.b4.0", fw.SSA_B4, keys, 0.0)
    fw._assert(built, "demo.pa.ssa.witness.0", fw.SSA_B6_WITNESS, keys, 0.0)
    fw._assert(built, "demo.pa.ssa.recipient.0", fw.SSA_RECIPIENT, keys, "taxpayer")
    fw._assert(built, "demo.pa.ssa.kind.0", fw.SSA_KIND, keys, "ssa-1099")
    fw._assert(built, "demo.pa.ssa.lump.0", fw.SSA_LUMP, keys, False)
    fw._transition(
        built, (fw.SSA_FAMILY, "v1"), head, successor,
        "demo.pa.ssa.b5.0", fw.SSA_B5, keys, amount,
    )
    if reclose:
        _move_closure(built, "tax.us.2025.ssa1099.source-closure", successor)
    return l12d.answer(l12d.harness().renumber(built), {LUMP: election})


def with_1099k(acts: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """One synthetic Form 1099-K personal-item loss (box 1a 880) on the wage return."""
    kprobe = _module(
        "pa_k_probe",
        REPO / "docs/phases/engine-breadth/milestones/form-1099-k-income-evidence/probe.py",
    )
    spliced = kprobe._splice(acts, box4=0.0, omit=None)
    return l12d.harness().renumber(spliced["acts"])


def with_w2g(acts: list[dict[str, Any]], winnings: float) -> list[dict[str, Any]]:
    """One synthetic Form W-2G on the wage return's already closed-empty families."""
    fw = _module("pa_fw", REPO / "tests/test_form_1099_withholding.py")
    w2g = _module("pa_w2g", REPO / "tests/test_w2g_gambling.py")
    built = copy.deepcopy(acts)
    keys = (("payer", "demo.pa.w2g.payer.0"), ("statement", "demo.pa.w2g.stmt.0"))
    fw._introduce(built, "demo.pa.w2g.payer.0", "tax.us.gambling-payer")
    fw._introduce(built, "demo.pa.w2g.stmt.0", "tax.us.w2g-statement")
    for family, fact, successor, closure, finding_id, amount in (
        (w2g.B1_FAMILY, w2g.BOX1, "demo.pa.w2g.b1.h1", w2g.B1_CLOSURE, "demo.pa.w2g.box1.0", winnings),
        (w2g.B4_FAMILY, w2g.BOX4, "demo.pa.w2g.b4.h1", w2g.B4_CLOSURE, "demo.pa.w2g.box4.0", 0.0),
    ):
        head = fw._head(built, family)
        fw._transition(built, (family, "v1"), head, successor, finding_id, fact, keys, amount)
        _move_closure(built, closure, successor)
    return l12d.harness().renumber(built)


def _num(value: Any) -> Any:
    if isinstance(value, float) and value.is_integer():
        return int(value)
    return value


def section_view(section: dict[str, Any]) -> dict[str, Any]:
    field = section.get("field") or {}
    resolved = section.get("resolved") or {}
    disposition = resolved.get("disposition")
    dispositions = field.get("dispositions") or {}
    key = "published_value" if disposition == "published_categorical" else disposition
    instruction = dispositions.get(key) if isinstance(dispositions, dict) else None
    render = instruction.get("render") if isinstance(instruction, dict) else None
    explain = instruction.get("explain") if isinstance(instruction, dict) else None
    citation = field.get("citation") if isinstance(field.get("citation"), dict) else None
    finding = ((resolved.get("act") or {}).get("finding") or {}) if isinstance(resolved.get("act"), dict) else {}
    reasons = []
    for reason in resolved.get("reasons") or []:
        if isinstance(reason, dict) and isinstance(reason.get("sentence"), str):
            reasons.append(reason["sentence"])
    return {
        "section_id": section.get("id"),
        "field_id": str(field.get("id") or "").removeprefix(P),
        "label": field.get("label"),
        "line": field.get("line"),
        "disposition": disposition,
        "value": _num(resolved.get("value")),
        "finding_value": _num(finding.get("value")) if finding else None,
        "instruction_key": key,
        "render": render,
        "explain": explain,
        "citation_id": None if not citation else str(citation.get("id") or "").removeprefix(P),
        "active_codes": list(resolved.get("activeCodes") or []),
        "reasons": reasons[:8],
    }


def watched(model: dict[str, Any]) -> list[dict[str, Any]]:
    rows = []
    for section in model.get("sections") or []:
        view = section_view(section)
        ident = view["field_id"]
        if ident.startswith("form1040.line-12d-") or ident.startswith("form1040.line-6d"):
            rows.append(view)
            continue
        if ident in WATCH or ident.startswith("schedule1.top-entry"):
            rows.append(view)
    return rows


def run_case(core: Any, acts: list[dict[str, Any]], run_id: str, page_dir: Path) -> dict[str, Any]:
    h = l12d.harness()
    surface = core.surface()
    with h.loader_entries(core):
        try:
            finished = h._handover(
                h._finish(
                    acts,
                    package_path=core.package_path,
                    package_version=core.version,
                    release_path=core.release_path,
                    release_version=core.release_version,
                    note=run_id,
                ),
                surface=surface,
                reconfirm=True,
            )
            with tempfile.TemporaryDirectory() as tmp:
                capability = h.WorkspaceCapability(Path(tmp) / "L")
                outcome = h.live_coordinate_run(
                    capability,
                    repo_root=REPO,
                    authoritative_acts=finished,
                    workspace_revision=len(finished),
                    run_scope={"jurisdiction": "us", "year": h.YEAR},
                    scope_user=h.ccr.USER,
                    request={"schema": "run-request.v1"},
                    run_id=run_id,
                    governance_pins=[],
                    surface=surface,
                    output_name="out.json",
                )
                if outcome.refusal is not None:
                    return {"outcome": "refused", "reason": outcome.refusal.reason}
                model = json.loads(outcome.presentation_path.read_text(encoding="utf-8"))
                report = json.loads(outcome.output_path.read_text(encoding="utf-8"))
                page = _render_page(REPO, capability, outcome.presentation_path)
                page_dir.mkdir(parents=True, exist_ok=True)
                (page_dir / f"{run_id}.html").write_bytes(page)
        except Exception as exc:  # noqa: BLE001 - a rejected act list is a result
            return {"outcome": "error", "error": type(exc).__name__, "message": scrub(str(exc))[:500]}
    return {
        "outcome": "success",
        "stop": report.get("stop_reason"),
        "sections": watched(model),
        "section_count": len(model.get("sections") or []),
    }


def _build(builder: Any) -> dict[str, Any] | list[dict[str, Any]]:
    try:
        return builder()
    except Exception as exc:  # noqa: BLE001 - a case that cannot be built is a result
        return {"outcome": "error", "error": type(exc).__name__, "message": scrub(str(exc))[:500]}


def cases() -> list[dict[str, Any]]:
    """The plan's cases, plus the line 12d Track 0 browser cases."""
    single = wage()
    rows: list[tuple[str, str, Any]] = [
        ("wages-only", "Single filer, wages 50,000, withholding 4,500, not 65, not blind. No Schedule 1 income.", lambda: single),
        ("ss-not-elected", "Same wages, one SSA-1099 box 5 of 12,000, lump-sum scope answer yes (no election).", lambda: with_benefits(single, 12000.0, election="yes")),
        ("ss-elected", "Same wages and SSA-1099, lump-sum scope answer no (election made).", lambda: with_benefits(single, 12000.0, election="no")),
        ("elected-no-benefits", "Same wages, no SSA-1099, lump-sum scope answer no (election made).", lambda: l12d.answer(single, {LUMP: "no"})),
        ("f1099k-top-entry", "Same wages, one Form 1099-K personal-item loss, box 1a 880.", lambda: with_1099k(single)),
        ("w2g-winnings", "Same wages, one Form W-2G with winnings 1,200 and box 4 zero.", lambda: with_w2g(single, 1200.0)),
        ("l12d-single-age", "Single; born before January 2, 1961; not blind.", lambda: wage("single", {l12d.AGE: True, l12d.BLIND: False, l12d.SSN: "yes"})),
        ("l12d-joint-spouse-age", "Joint; only the spouse born before January 2, 1961.", lambda: wage(l12d.MFJ, {l12d.AGE: False, l12d.BLIND: False, l12d.S_AGE: True, l12d.S_BLIND: False})),
        ("l12d-separate-condition-no", "Separate; spouse blind recorded; condition no.", lambda: wage(l12d.MFS, {l12d.AGE: False, l12d.BLIND: False, l12d.S_AGE: False, l12d.S_BLIND: True, l12d.COND: False})),
        ("l12d-separate-lived-with", "Separate; condition no; lived with the spouse during 2025.", lambda: wage(l12d.MFS, {l12d.AGE: False, l12d.BLIND: False, l12d.S_AGE: False, l12d.S_BLIND: True, l12d.COND: False, P + "mfs-lived-apart-all-year": "no"})),
        ("l12d-hoh", "Head of household; not 65; not blind.", lambda: wage(l12d.HOH, {l12d.AGE: False, l12d.BLIND: False})),
        ("l12d-unanswered-age", "Single; age and blindness left unanswered.", lambda: l12d.base("single")),
    ]
    built_rows = []
    for case_id, says, builder in rows:
        built_rows.append({"id": case_id, "says": says, "acts": _build(builder)})
    return built_rows


def write_json(path: Path, payload: dict[str, Any]) -> None:
    text = json.dumps(payload, indent=2) + "\n"
    for needle in ("/Users/", "/private/", "/tmp/", "/var/"):
        if needle in text:
            raise SystemExit(f"{path.name} contains {needle}")
    path.write_text(text, encoding="utf-8")


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("usage: probe.py <scratch-directory-outside-the-repo>")
    scratch = Path(sys.argv[1]).resolve()
    if REPO in scratch.parents or scratch == REPO:
        raise SystemExit("scratch directory must be outside the repository")
    scratch.mkdir(parents=True, exist_ok=True)
    page_dir = scratch / "pages"
    core = core_v91()
    built = cases()
    results = []
    manifest = []
    for row in built:
        run_id = f"demo.pa.p0.v91.{row['id']}"
        print(row["id"], flush=True)
        if isinstance(row["acts"], dict):
            measured = row["acts"]
        else:
            measured = run_case(core, row["acts"], run_id, page_dir)
        print(" ", measured.get("outcome"), flush=True)
        results.append({"id": row["id"], "says": row["says"], "run_id": run_id, **measured})
        if measured.get("outcome") == "success":
            manifest.append({"id": row["id"], "page": f"{run_id}.html"})
    (scratch / "cases.json").write_text(
        json.dumps({"root": str(page_dir), "cases": manifest}, indent=2) + "\n",
        encoding="utf-8",
    )
    proc = subprocess.run(
        ["node", str(HERE / "observe.mjs"), str(scratch / "cases.json")],
        cwd=REPO,
        capture_output=True,
        text=True,
        timeout=300,
    )
    if proc.returncode != 0:
        raise SystemExit("browser observation failed: " + scrub(proc.stderr)[-500:])
    dom = json.loads((scratch / "dom-observations.json").read_text(encoding="utf-8"))
    by_id = {item["id"]: item for item in dom.get("cases") or []}
    for row in results:
        observed = by_id.get(row["id"])
        if observed is None:
            continue
        alerts = observed.get("alerts") or []
        sections = {item.get("id"): item for item in observed.get("sections") or []}
        drawn = []
        for alert in alerts:
            section = sections.get(alert.get("id")) or {}
            model_section = next(
                (item for item in row.get("sections") or [] if item.get("section_id") == alert.get("id")),
                None,
            )
            drawn.append({
                "section_id": alert.get("id"),
                "alert": alert.get("text"),
                "heading": section.get("heading"),
                "value": section.get("value"),
                "explain": section.get("explain"),
                "model": model_section,
            })
        row["drawn_alerts"] = drawn
        row["dom_alert_count"] = len(alerts)
        row["dom_section_count"] = observed.get("section_count")
    payload = {
        "core": {"package": "v91", "registry": "v89", "release": "v89"},
        "page": str(PAGE),
        "browser": dom.get("browser_version"),
        "node": dom.get("node_version"),
        "cases": [
            {key: value for key, value in row.items() if key != "acts"}
            for row in results
        ],
    }
    write_json(HERE / "probe-output.json", payload)
    for row in payload["cases"]:
        alerts = [item.get("alert") for item in row.get("drawn_alerts") or []]
        print(row["id"], row.get("outcome"), len(alerts), alerts, flush=True)


if __name__ == "__main__":
    main()
