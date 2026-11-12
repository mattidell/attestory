"""Design-case probes on published core v85 and scratch core v86.

Evidence for docs/phases/engine-breadth/milestones/selection-keyed-collect.md.
Charter: docs/reviews/selection-keyed-collect/charter-p0.md.

    python3 probe.py /path/outside/core.json

The scratch directory is the one prototype.py built. Engine code comes from
its packages/ copy. Synthetic demo.* facts only.
"""

from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import os
import sys
import tempfile
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

P = "tax.us.2025."
YEAR = "2025"
BOX4 = P + "f1099b.statement-box4-withholding"
BOX7 = P + "f1099b.statement-box7-loss-not-allowed"
PRESENT = P + "f1099b.no-sale-box4-present"
SUBTOTAL = P + "f1099b.b4-withholding-subtotal"
SYMBOL_RULE = P + "rule.f1099b-b4-amount-symbol"
SUBTOTAL_RULE = P + "rule.f1099b-b4-withholding-subtotal"
LINE25B = P + "payments.line25b"
WATCH = (
    "form1040.line-25b", "form1040.line-25d", "form1040.line-33",
    "form1040.line-34", "form1040.line-37",
)


def _load_engine(scratch: Path) -> None:
    packages = scratch / "packages"
    if not packages.is_dir():
        raise SystemExit("scratch packages/ missing; run prototype.py first")
    root = str(scratch)
    if root in sys.path:
        sys.path.remove(root)
    sys.path.insert(0, root)
    if str(REPO) not in sys.path:
        sys.path.append(str(REPO))


def _harness():
    name = "skc_p0_audit_harness"
    module = sys.modules.get(name)
    if module is None:
        spec = importlib.util.spec_from_file_location(
            name, REPO / "docs/phases/engine-breadth/milestones/sale-family-audit-evidence/audit_harness.py")
        assert spec is not None and spec.loader is not None
        module = importlib.util.module_from_spec(spec)
        sys.modules[name] = module
        spec.loader.exec_module(module)
    return module


def published_v85(h: Any) -> Any:
    return h.Core("v85", "v83", "v83")


def scratch_core(h: Any, core_path: Path) -> Any:
    body = json.loads(core_path.read_text(encoding="utf-8"))
    return h.Core(
        body["version"], body["registry"], body["release_version"],
        content=Path(body["content"]), releases=Path(body["releases"]),
        loader_from=body.get("loader_from"),
    )


def say_statement(h: Any, acts: list[dict[str, Any]], core: Any, fact_type: str,
                  statement: str, value: object) -> list[dict[str, Any]]:
    fact_id = h.fact_id_for(fact_type, (("statement", statement), ("tax-year", YEAR)))
    kept = []
    for act in acts:
        finding = (act.get("payload") or {}).get("finding") if isinstance(act.get("payload"), dict) else None
        if isinstance(finding, dict) and finding.get("fact_id") == fact_id:
            continue
        kept.append(act)
    acts = kept
    body = h.bundle_for(fact_type, core.content)
    if body is not None and not {fact["id"] for fact in body["fact_types"]} & h._adopted(acts):
        h._add(acts, "bundle-adoption", {"bundle": body})
    h._add(acts, "assertion", {"finding": h._attested(
        f"demo.skc.{fact_type.rsplit('.', 1)[-1]}.{statement.split('.')[-2]}", fact_id, value)})
    return h.renumber(acts)


def answer_present_no(h: Any, acts: list[dict[str, Any]], core: Any) -> list[dict[str, Any]]:
    return h.say(acts, PRESENT, "no", "present-no", core.content)


def prepare(h: Any, core: Any, kinds: set[str]) -> list[dict[str, Any]]:
    acts = h.opened()
    if kinds:
        for kind, term, tag in (("covered", "st", "one"),) if kinds == {"covered"} else ():
            acts = h.sale(acts, kind, term, proceeds=5000, basis=4000, tag=tag)
        if kinds != {"covered"}:
            tags = {"s1": ("covered", "st", 5000, 4000), "s2": ("covered", "st", 2000, 1600)}
            if "two" in kinds:
                for tag, (kind, term, proceeds, basis) in tags.items():
                    acts = h.sale(acts, kind, term, proceeds=proceeds, basis=basis, tag=tag)
    acts = h.answer(acts, core.content, **{key: value for key, value in h.honest(
        {"covered"} if kinds else set(), loss=False).items() if value is not None})
    return answer_present_no(h, acts, core)


def finding_id_for(acts: list[dict[str, Any]], fact_id: str) -> str | None:
    found = None
    for act in acts:
        finding = (act.get("payload") or {}).get("finding") if isinstance(act.get("payload"), dict) else None
        if isinstance(finding, dict) and finding.get("fact_id") == fact_id:
            found = str(finding.get("id"))
    return found


def compact_walk(node: Any, *, depth: int = 0) -> list[str]:
    if node is None:
        return []
    symbol = getattr(node, "symbol", None) or node.get("symbol") if isinstance(node, dict) else getattr(node, "symbol", None)
    value = getattr(node, "value", None) if not isinstance(node, dict) else node.get("value")
    produced = getattr(node, "produced_by", None) if not isinstance(node, dict) else node.get("produced_by")
    role = getattr(node, "role", None) if not isinstance(node, dict) else node.get("role")
    produced_id = None
    if isinstance(produced, dict):
        produced_id = produced.get("id")
    head = str(symbol or "").removeprefix(P) or "leaf"
    value_s = "" if value is None else f"={value}"
    rule = "" if not produced_id else f" <- {str(produced_id).removeprefix(P)}"
    line = f"{'  ' * depth}[{role}] {head}{value_s}{rule}"
    children = getattr(node, "children", ()) if not isinstance(node, dict) else node.get("children") or ()
    out = [line]
    for child in children:
        out.extend(compact_walk(child, depth=depth + 1))
    return out


def walks_from(outcome: Any, symbols: list[str]) -> dict[str, Any]:
    from packages.derivation.explanation import explain_legacy, index_derived
    publications = list(getattr(outcome, "publications", ()) or ())
    findings = [pub.finding for pub in publications if getattr(pub, "finding", None)]
    derived = index_derived(findings)
    by_symbol: dict[str, dict[str, Any]] = {}
    for finding in findings:
        symbol = finding.get("symbol")
        if isinstance(symbol, str):
            by_symbol[symbol] = finding
    out: dict[str, Any] = {}
    for symbol in symbols:
        finding = by_symbol.get(symbol)
        if finding is None:
            out[symbol.removeprefix(P)] = None
            continue
        node = explain_legacy(finding["id"], role="output", derived=derived)
        out[symbol.removeprefix(P)] = {
            "value": finding.get("value"),
            "walk": compact_walk(node)[:24],
        }
    return out


def run_case(h: Any, core: Any, acts: list[dict[str, Any]], run_id: str) -> dict[str, Any]:
    from packages.derivation.live import live_coordinate_run
    from packages.derivation.live_workspace import WorkspaceCapability
    with h.loader_entries(core):
        surface = core.surface()
        finished = h._handover(h._finish(
            copy.deepcopy(acts), package_path=core.package_path, package_version=core.version,
            release_path=core.release_path, release_version=core.release_version, note=run_id,
        ), surface=surface, reconfirm=True)
        with tempfile.TemporaryDirectory() as tmp:
            outcome = live_coordinate_run(
                WorkspaceCapability(Path(tmp) / "L"), repo_root=REPO, authoritative_acts=finished,
                workspace_revision=len(finished), run_scope={"jurisdiction": "us", "year": YEAR},
                scope_user=h.ccr.USER, request={"schema": "run-request.v1"}, run_id=run_id,
                governance_pins=[], surface=surface, output_name="out.json")
            if outcome.refusal is not None:
                return {"outcome": "refusal", "reason": outcome.refusal.reason,
                        "message": h.scrub(str(outcome.refusal.detail))[:240]}
            model = json.loads(outcome.presentation_path.read_text(encoding="utf-8"))
            report = json.loads(outcome.output_path.read_text(encoding="utf-8"))
    lines: dict[str, Any] = {}
    questions: list[str] = []
    for section in model.get("sections") or []:
        field_id = str((section.get("field") or {}).get("id") or "").removeprefix(P)
        resolved = section.get("resolved") or {}
        disposition = str(resolved.get("disposition") or "")
        value = resolved.get("value")
        if field_id in WATCH:
            if value is None or "blocked" in disposition:
                lines[field_id] = disposition
            elif isinstance(value, float) and value.is_integer():
                lines[field_id] = int(value)
            else:
                lines[field_id] = value
        for reason in resolved.get("reasons") or []:
            sentence = str(reason.get("sentence") or "") if isinstance(reason, dict) else ""
            if sentence.endswith("?") or sentence.startswith("Enter "):
                if sentence not in questions:
                    questions.append(h.scrub(sentence)[:240])
    rows = {}
    for row in report.get("dispositions") or []:
        artifact = str(row.get("artifact_id") or "")
        if artifact in {SYMBOL_RULE, SUBTOTAL_RULE, P + "rule.form1040-line25b"} or artifact.endswith("line25b"):
            rows[artifact.removeprefix(P)] = {
                "disposition": row.get("disposition"),
                "symbol": str(row.get("symbol") or "").removeprefix(P),
                "code": row.get("code"),
            }
    return {
        "outcome": "success",
        "lines": lines,
        "questions": questions,
        "rows": rows,
        "walks": walks_from(outcome, [LINE25B, SUBTOTAL, BOX4]),
        "digest": hashlib.sha256(json.dumps(
            {"lines": lines, "rows": rows}, sort_keys=True).encode("utf-8")).hexdigest()[:16],
    }


def build_cases(h: Any, core: Any) -> list[tuple[str, list[dict[str, Any]]]]:
    cases: list[tuple[str, list[dict[str, Any]]]] = []

    acts = prepare(h, core, set())
    cases.append(("no_box4_amount", acts))

    acts = prepare(h, core, {"covered"})
    stmt = "demo.sfa.one.statement"
    acts = say_statement(h, acts, core, BOX4, stmt, 150.0)
    acts = say_statement(h, acts, core, BOX7, stmt, "no")
    cases.append(("one_amount", acts))

    acts = prepare(h, core, {"two"})
    acts = say_statement(h, acts, core, BOX4, "demo.sfa.s1.statement", 150.0)
    acts = say_statement(h, acts, core, BOX7, "demo.sfa.s1.statement", "no")
    acts = say_statement(h, acts, core, BOX4, "demo.sfa.s2.statement", 40.0)
    acts = say_statement(h, acts, core, BOX7, "demo.sfa.s2.statement", "no")
    cases.append(("two_statements", acts))

    acts = prepare(h, core, {"covered"})
    acts = say_statement(h, acts, core, BOX4, stmt, 0.0)
    acts = say_statement(h, acts, core, BOX7, stmt, "no")
    cases.append(("zero_amount", acts))

    acts = prepare(h, core, {"covered"})
    acts = say_statement(h, acts, core, BOX4, "demo.sfa.one.statement", 100.0)
    fid = h.fact_id_for(BOX4, (("statement", "demo.sfa.one.statement"), ("tax-year", YEAR)))
    h._add(acts, "assertion", {"finding": h._attested("demo.skc.box4.one.v2", fid, 250.0)})
    acts = h.renumber(acts)
    acts = say_statement(h, acts, core, BOX7, "demo.sfa.one.statement", "no")
    cases.append(("superseded", acts))

    acts = prepare(h, core, {"covered"})
    acts = say_statement(h, acts, core, BOX4, "demo.sfa.one.statement", 150.0)
    acts = say_statement(h, acts, core, BOX7, "demo.sfa.one.statement", "no")
    retracted = finding_id_for(acts, h.fact_id_for(BOX4, (("statement", "demo.sfa.one.statement"), ("tax-year", YEAR))))
    if retracted:
        h._add(acts, "finding-retracted", {"finding_id": retracted})
        acts = h.renumber(acts)
    cases.append(("withdrawn", acts))
    return cases


def classify(v85: dict[str, Any], v86: dict[str, Any]) -> dict[str, Any]:
    if v85.get("outcome") != "success" or v86.get("outcome") != "success":
        return {"class": "error", "v85": v85.get("outcome"), "v86": v86.get("outcome")}
    line_same = (v85.get("lines") or {}) == (v86.get("lines") or {})
    symbol_v85 = (v85.get("rows") or {}).get("rule.f1099b-b4-amount-symbol")
    symbol_v86 = (v86.get("rows") or {}).get("rule.f1099b-b4-amount-symbol")
    amount_v85 = ((v85.get("walks") or {}).get("f1099b.statement-box4-withholding") or {})
    amount_v86 = ((v86.get("walks") or {}).get("f1099b.statement-box4-withholding") or {})
    changes: list[str] = []
    if not line_same:
        changes.append("lines")
    if symbol_v85 and not symbol_v86:
        changes.append("symbol_rule_retired")
    if amount_v85.get("value") == "0" and not amount_v86:
        changes.append("amount_symbol_walk_gone")
    def walk_body(pin: dict[str, Any], name: str) -> dict[str, Any]:
        item = (pin.get("walks") or {}).get(name) or {}
        return {"value": item.get("value"), "walk": item.get("walk")}
    if walk_body(v85, "f1099b.b4-withholding-subtotal") != walk_body(v86, "f1099b.b4-withholding-subtotal"):
        changes.append("subtotal_walk")
    if walk_body(v85, "payments.line25b") != walk_body(v86, "payments.line25b"):
        changes.append("line25b_walk")
    expected = {"symbol_rule_retired", "amount_symbol_walk_gone"}
    if line_same and set(changes) - expected <= {"subtotal_walk", "line25b_walk"} and (
            walk_body(v85, "f1099b.b4-withholding-subtotal").get("value")
            == walk_body(v86, "f1099b.b4-withholding-subtotal").get("value")
            and walk_body(v85, "payments.line25b").get("value")
            == walk_body(v86, "payments.line25b").get("value")):
        return {"class": "lines_identical_symbol_retired", "changes": changes}
    if line_same and set(changes) <= expected:
        return {"class": "lines_identical_symbol_retired", "changes": changes}
    if line_same and not changes:
        return {"class": "identical"}
    if line_same:
        return {"class": "lines_identical_walk_changed", "changes": changes}
    return {"class": "counterexample", "changes": changes}


def _pair(item: tuple[str, str, list[dict[str, Any]]]) -> tuple[str, dict[str, Any]]:
    case_id, core_path, acts = item
    scratch = Path(os.environ["SKC_SCRATCH"])
    _load_engine(scratch)
    h = _harness()
    v85 = published_v85(h)
    v86 = scratch_core(h, Path(core_path))
    pin85 = run_case(h, v85, acts, "demo.skc.v85." + case_id)
    pin86 = run_case(h, v86, acts, "demo.skc.v86." + case_id)
    row = classify(pin85, pin86)
    return case_id, {"v85": pin85, "v86": pin86, **row}


def validation_cases(scratch: Path) -> dict[str, Any]:
    """One real path plus default, and two real paths, under old and new validation."""
    _load_engine(scratch)
    from packages.kernel.schema_registry import SchemaRegistry, SchemaValidationError
    from packages.derivation.loader import DERIVATION_SCHEMA_DIR
    patched = SchemaRegistry(DERIVATION_SCHEMA_DIR)
    one = _subtotal_one_path()
    two = json.loads((REPO / "packages/content/tax/2025/rule.f1099b-b4-withholding-subtotal.json").read_text(encoding="utf-8"))
    line2b = json.loads((REPO / "packages/content/tax/2025/rule.form1040-line2b.v8.json").read_text(encoding="utf-8"))

    def check(registry: SchemaRegistry, body: dict[str, Any]) -> dict[str, Any]:
        try:
            registry.validate(body["schema"], body)
            return {"ok": True}
        except SchemaValidationError as exc:
            return {"ok": False, "errors": list(exc.errors)[:4]}

    production = SchemaRegistry(REPO / "packages/schemas/derivation")
    return {
        "one_path_patched_v15": check(patched, one),
        "one_path_published_v15": check(production, one),
        "two_path_subtotal_patched": check(patched, two),
        "two_path_subtotal_published": check(production, two),
        "two_real_line2b_patched": check(patched, line2b),
        "two_real_line2b_published": check(production, line2b),
    }


def _subtotal_one_path() -> dict[str, Any]:
    from prototype import _subtotal_v2
    return _subtotal_v2()


def switch_off_identity(h: Any, scratch: Path) -> dict[str, Any]:
    """The v86 switch is off for v85 and earlier; v85 lines are the published values."""
    from packages.tax.loader import selection_collect_satisfied_by_family
    core = "tax.us.2025.package.core-calculations"
    return {
        "class": "switch_off_before_v86",
        "v84": selection_collect_satisfied_by_family(core, "v84"),
        "v85": selection_collect_satisfied_by_family(core, "v85"),
        "v86": selection_collect_satisfied_by_family(core, "v86"),
        "other_package": selection_collect_satisfied_by_family("tax.us.2025.package.interest-slice", "v86"),
    }


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("usage: probe.py <scratch-core.json-or-scratch-dir>")
    target = Path(sys.argv[1]).resolve()
    core_path = target if target.name == "core.json" else target / "core.json"
    scratch = core_path.parent
    os.environ["SKC_SCRATCH"] = str(scratch)
    _load_engine(scratch)
    h = _harness()
    v85 = published_v85(h)
    cases = build_cases(h, v85)
    work = [(case_id, str(core_path), acts) for case_id, acts in cases]
    found: dict[str, Any] = {}
    workers = int(os.environ.get("SKC_WORKERS") or min(4, os.cpu_count() or 2))
    with ProcessPoolExecutor(max_workers=workers) as pool:
        for case_id, row in pool.map(_pair, work):
            found[case_id] = row
            print(case_id, row["class"], flush=True)
    validation = validation_cases(scratch)
    identity = switch_off_identity(h, scratch)
    payload = {
        "cores": ["v85", "v86"],
        "cases": found,
        "validation": validation,
        "switch_off_v85": identity,
        "case_ids": [case_id for case_id, _acts in cases],
    }
    text = json.dumps(payload, indent=2) + "\n"
    for needle in ("/Users/", "/private/", "/tmp/", "/var/"):
        if needle in text:
            raise SystemExit(f"probe output contains {needle}")
    (HERE / "probe-output.json").write_text(text, encoding="utf-8")
    print(json.dumps({
        "cases": {key: found[key]["class"] for key in found},
        "validation_one_path_published_ok": validation["one_path_published_v15"]["ok"],
        "validation_one_path_patched_ok": validation["one_path_patched_v15"]["ok"],
        "switch_off": identity["class"],
        "output": "probe-output.json",
    }, indent=2))


if __name__ == "__main__":
    main()
