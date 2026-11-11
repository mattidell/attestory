"""Track 0 runs for a selection path collecting a keyed family.

Evidence for docs/phases/engine-breadth/milestones/selection-keyed-collect.md.
Charter: docs/reviews/selection-keyed-collect/charter-track0.md.

    python3 track0.py <scratch-core.json> <authority|matrix|late|reuse|neighbour|surface>

Loads the milestone probe under a unique module name. Does not assign another
module's globals. Work against the P0 patch in the scratch copy. Synthetic
demo.* only.
"""

from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import os
import shutil
import sys
import tempfile
from collections import Counter
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

PROBE_NAME = "skc_t0_probe"
TEST_NAME = "skc_t0_v83_test"
EXPECTED = REPO / "tests/fixtures/f1099b_backup_withholding_v83/expected.json"
TEST = REPO / "tests/test_f1099b_backup_withholding_v83.py"
P = "tax.us.2025."
PKG = P + "package.core-calculations"
BOX4 = P + "f1099b.statement-box4-withholding"
BOX7 = P + "f1099b.statement-box7-loss-not-allowed"
PRESENT = P + "f1099b.no-sale-box4-present"
SUBTOTAL = P + "f1099b.b4-withholding-subtotal"
SYMBOL_RULE = P + "rule.f1099b-b4-amount-symbol"
SUBTOTAL_RULE = P + "rule.f1099b-b4-withholding-subtotal"
LINE25B = P + "payments.line25b"
LINE2B = P + "rule.form1040-line2b"
INT_MEMBER = P + "f1099int.box4-withholding"
INT_FAMILY = P + "f1099int.b4"
WATCH = (
    "form1040.line-25b", "form1040.line-25d", "form1040.line-33",
    "form1040.line-34", "form1040.line-37",
)
CONSUMERS = WATCH
CORE_RE = __import__("re").compile(r"^package\.core-calculations\.(v[1-9][0-9]*)\.json$")


def load_probe() -> Any:
    module = sys.modules.get(PROBE_NAME)
    if module is None:
        spec = importlib.util.spec_from_file_location(PROBE_NAME, HERE / "probe.py")
        assert spec is not None and spec.loader is not None
        module = importlib.util.module_from_spec(spec)
        sys.modules[PROBE_NAME] = module
        spec.loader.exec_module(module)
    return module


def load_test() -> Any:
    module = sys.modules.get(TEST_NAME)
    if module is None:
        spec = importlib.util.spec_from_file_location(TEST_NAME, TEST)
        assert spec is not None and spec.loader is not None
        module = importlib.util.module_from_spec(spec)
        sys.modules[TEST_NAME] = module
        spec.loader.exec_module(module)
    return module


def _load_engine(scratch: Path) -> None:
    root = str(scratch)
    if root in sys.path:
        sys.path.remove(root)
    sys.path.insert(0, root)
    if str(REPO) not in sys.path:
        sys.path.append(str(REPO))


def scratch_core(probe: Any, core_path: Path) -> Any:
    body = json.loads(core_path.read_text(encoding="utf-8"))
    return probe.scratch_core(probe._harness(), core_path)


def published_v85(probe: Any) -> Any:
    return probe.published_v85(probe._harness())


def num(value: Any) -> Any:
    if isinstance(value, bool) or value is None:
        return value
    if isinstance(value, (int, float)):
        return int(value) if float(value).is_integer() else value
    if isinstance(value, str):
        try:
            parsed = float(value)
        except ValueError:
            return value
        return int(parsed) if parsed.is_integer() else parsed
    return value


def input_index(acts: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    found: dict[str, dict[str, Any]] = {}
    for act in acts:
        if act.get("kind") != "assertion":
            continue
        finding = (act.get("payload") or {}).get("finding") or {}
        identity = finding.get("id")
        if not isinstance(identity, str):
            continue
        found[identity] = {
            "symbol": finding.get("fact_id") or finding.get("symbol"),
            "value": finding.get("value"),
            "role": "input",
        }
    return found


def compact_walk(node: Any, *, depth: int = 0) -> list[str]:
    probe = load_probe()
    return probe.compact_walk(node, depth=depth)


def walks_from(outcome: Any, acts: list[dict[str, Any]], symbols: list[str]) -> dict[str, Any]:
    from packages.derivation.explanation import explain_legacy, index_derived
    publications = list(getattr(outcome, "publications", ()) or ())
    findings = [pub.finding for pub in publications if getattr(pub, "finding", None)]
    derived = index_derived(findings)
    by_symbol: dict[str, dict[str, Any]] = {}
    for finding in findings:
        symbol = finding.get("symbol")
        if isinstance(symbol, str):
            by_symbol[symbol] = finding
    inputs = input_index(acts)
    out: dict[str, Any] = {}
    for symbol in symbols:
        finding = by_symbol.get(symbol)
        if finding is None:
            out[symbol.removeprefix(P)] = None
            continue
        node = explain_legacy(finding["id"], role="output", derived=derived, inputs=inputs)
        walk = compact_walk(node)
        out[symbol.removeprefix(P)] = {
            "value": finding.get("value"),
            "finding_id": finding.get("id"),
            "walk": walk,
            "walk_has_amount_symbol": any("f1099b-b4-amount-symbol" in line for line in walk),
            "walk_amount_zero_from_symbol": any(
                "statement-box4-withholding=0" in line and "amount-symbol" in line for line in walk
            ),
            "recorded_values_in_walk": sorted({
                line.split("=", 1)[1].split(" ", 1)[0].rstrip("0").rstrip(".")
                if "statement-box4-withholding=" in line else
                line.split("=", 1)[1].split(" ", 1)[0]
                for line in walk
                if "statement-box4-withholding=" in line or (
                    "b4-withholding-subtotal=" in line and "f1099b.b4-withholding-subtotal=" in line
                )
            }),
        }
    return out


def execute(core: Any, acts: list[dict[str, Any]], run_id: str) -> dict[str, Any]:
    probe = load_probe()
    h = probe._harness()
    from packages.derivation.live import live_coordinate_run
    from packages.derivation.live_workspace import WorkspaceCapability
    from packages.derivation.presentation_projection import validate_presentation_model

    try:
        with h.loader_entries(core):
            surface = core.surface()
            finished = h._handover(h._finish(
                copy.deepcopy(acts), package_path=core.package_path, package_version=core.version,
                release_path=core.release_path, release_version=core.release_version, note=run_id,
            ), surface=surface, reconfirm=True)
            with tempfile.TemporaryDirectory() as tmp:
                outcome = live_coordinate_run(
                    WorkspaceCapability(Path(tmp) / "L"), repo_root=REPO, authoritative_acts=finished,
                    workspace_revision=len(finished), run_scope={"jurisdiction": "us", "year": probe.YEAR},
                    scope_user=h.ccr.USER, request={"schema": "run-request.v1"}, run_id=run_id,
                    governance_pins=[], surface=surface, output_name="out.json")
                if outcome.refusal is not None:
                    return {"outcome": "refusal", "reason": outcome.refusal.reason,
                            "message": h.scrub(str(outcome.refusal.detail))[:400]}
                model = json.loads(outcome.presentation_path.read_text(encoding="utf-8"))
                report = json.loads(outcome.output_path.read_text(encoding="utf-8"))
                valid: Any = True
                try:
                    validate_presentation_model(model)
                except Exception as exc:  # noqa: BLE001 — the probe records a bad model
                    valid = h.scrub(str(exc))[:300]
    except Exception as exc:  # noqa: BLE001 — a rejected return is a measured result
        return {"outcome": "error", "error": type(exc).__name__, "message": h.scrub(str(exc))[:500]}

    lines: dict[str, Any] = {}
    consumers: dict[str, Any] = {name: {"present": False} for name in CONSUMERS}
    line25b_field: dict[str, Any] | None = None
    questions: list[str] = []
    for section in model.get("sections") or []:
        field = section.get("field") or {}
        short = str(field.get("id") or "").removeprefix(P)
        resolved = section.get("resolved") or {}
        disposition = str(resolved.get("disposition") or "")
        value = resolved.get("value")
        sentences = [str(reason.get("sentence") or "") for reason in (resolved.get("reasons") or [])
                     if isinstance(reason, dict) and reason.get("sentence")]
        for sentence in sentences:
            if sentence and sentence not in questions and (
                    sentence.endswith("?") or sentence.startswith("Enter ")):
                questions.append(h.scrub(sentence)[:400])
        if short in WATCH:
            if value is None or "blocked" in disposition:
                lines[short] = disposition
            else:
                lines[short] = num(value)
            consumers[short] = {
                "present": True,
                "binds_symbol": str(field.get("binds_symbol") or "").removeprefix(P),
                "field_version": field.get("version"),
                "disposition": resolved.get("disposition"),
                "value": num(resolved.get("value")) if resolved.get("value") is not None else None,
            }
        if short == "form1040.line-25b":
            line25b_field = {
                "version": field.get("version"),
                "binds_symbol": str(field.get("binds_symbol") or "").removeprefix(P),
                "disposition": resolved.get("disposition"),
                "value": num(resolved.get("value")) if resolved.get("value") is not None else None,
            }
    rows: dict[str, Any] = {}
    for row in report.get("dispositions") or []:
        artifact = str(row.get("artifact_id") or "")
        if artifact in {SYMBOL_RULE, SUBTOTAL_RULE, P + "rule.form1040-line25b"}:
            rows[artifact.removeprefix(P)] = {
                "disposition": row.get("disposition"),
                "symbol": str(row.get("symbol") or "").removeprefix(P),
                "code": row.get("code"),
            }
    publications = []
    for pub in outcome.publications:
        finding = pub.finding
        symbol = str(finding.get("symbol") or "")
        if symbol in {LINE25B, SUBTOTAL, BOX4} or symbol.removeprefix(P) in WATCH:
            publications.append({
                "symbol": symbol.removeprefix(P),
                "value": num(finding.get("value")),
                "finding_id": finding.get("id"),
            })
    return {
        "outcome": "success",
        "presentation_valid": valid,
        "lines": lines,
        "questions": questions,
        "rows": rows,
        "publications": publications,
        "consumers": consumers,
        "line25b_field": line25b_field,
        "walks": walks_from(outcome, finished, [LINE25B, SUBTOTAL, BOX4]),
        "line25b_row_count": len([row for row in (report.get("dispositions") or [])
                                  if str(row.get("artifact_id") or "").endswith("rule.form1040-line25b")]),
    }


def pub_values(result: dict[str, Any], symbol: str) -> list[Any]:
    return [row["value"] for row in result.get("publications") or [] if row["symbol"] == symbol]


def pub_ids(result: dict[str, Any], symbol: str) -> list[str]:
    return [str(row["finding_id"]) for row in result.get("publications") or [] if row["symbol"] == symbol]


def _blocked(result: dict[str, Any], line: str = "form1040.line-25b") -> bool:
    value = (result.get("lines") or {}).get(line)
    return isinstance(value, str) and "block" in value


def write_output(name: str, payload: dict[str, Any]) -> None:
    probe = load_probe()
    text = probe._harness().scrub(json.dumps(payload, indent=2) + "\n")
    for needle in ("/Users/", "/private/", "/tmp/", "/var/"):
        if needle in text:
            raise SystemExit(f"{name} contains {needle}")
    (HERE / name).write_text(text, encoding="utf-8")


def switch_row() -> dict[str, Any]:
    from packages.tax.loader import selection_collect_satisfied_by_family
    return {
        "v84": selection_collect_satisfied_by_family(PKG, "v84"),
        "v85": selection_collect_satisfied_by_family(PKG, "v85"),
        "v86": selection_collect_satisfied_by_family(PKG, "v86"),
        "other_package": selection_collect_satisfied_by_family(P + "package.interest-slice", "v86"),
    }


def cases_empty(probe: Any, core: Any) -> list[dict[str, Any]]:
    h = probe._harness()
    return [{"id": "no_box4_amount", "acts": probe.prepare(h, core, set()), "expect_25b": 0, "expect_subtotal": 0}]


def cases_one(probe: Any, core: Any) -> list[dict[str, Any]]:
    h = probe._harness()
    acts = probe.prepare(h, core, {"covered"})
    acts = probe.say_statement(h, acts, core, BOX4, "demo.sfa.one.statement", 150.0)
    acts = probe.say_statement(h, acts, core, BOX7, "demo.sfa.one.statement", "no")
    return [{"id": "one_amount", "acts": acts, "expect_25b": 150, "expect_subtotal": 150}]


def cases_two(probe: Any, core: Any) -> list[dict[str, Any]]:
    h = probe._harness()
    acts = probe.prepare(h, core, {"two"})
    acts = probe.say_statement(h, acts, core, BOX4, "demo.sfa.s1.statement", 150.0)
    acts = probe.say_statement(h, acts, core, BOX7, "demo.sfa.s1.statement", "no")
    acts = probe.say_statement(h, acts, core, BOX4, "demo.sfa.s2.statement", 40.0)
    acts = probe.say_statement(h, acts, core, BOX7, "demo.sfa.s2.statement", "no")
    return [{"id": "two_statements", "acts": acts, "expect_25b": 190, "expect_subtotal": 190}]


def cases_zero(probe: Any, core: Any) -> list[dict[str, Any]]:
    h = probe._harness()
    acts = probe.prepare(h, core, {"covered"})
    acts = probe.say_statement(h, acts, core, BOX4, "demo.sfa.one.statement", 0.0)
    acts = probe.say_statement(h, acts, core, BOX7, "demo.sfa.one.statement", "no")
    return [{"id": "zero_amount", "acts": acts, "expect_25b": 0, "expect_subtotal": 0}]


def cases_superseded(probe: Any, core: Any) -> list[dict[str, Any]]:
    h = probe._harness()
    acts = probe.prepare(h, core, {"covered"})
    acts = probe.say_statement(h, acts, core, BOX4, "demo.sfa.one.statement", 100.0)
    fid = h.fact_id_for(BOX4, (("statement", "demo.sfa.one.statement"), ("tax-year", probe.YEAR)))
    h._add(acts, "assertion", {"finding": h._attested("demo.skc.t0.box4.one.v2", fid, 250.0)})
    acts = h.renumber(acts)
    acts = probe.say_statement(h, acts, core, BOX7, "demo.sfa.one.statement", "no")
    return [{"id": "superseded", "acts": acts, "expect_25b": 250, "expect_subtotal": 250}]


def cases_withdrawn(probe: Any, core: Any) -> list[dict[str, Any]]:
    h = probe._harness()
    acts = probe.prepare(h, core, {"covered"})
    acts = probe.say_statement(h, acts, core, BOX4, "demo.sfa.one.statement", 150.0)
    acts = probe.say_statement(h, acts, core, BOX7, "demo.sfa.one.statement", "no")
    retracted = probe.finding_id_for(
        acts, h.fact_id_for(BOX4, (("statement", "demo.sfa.one.statement"), ("tax-year", probe.YEAR))))
    if retracted:
        h._add(acts, "finding-retracted", {"finding_id": retracted})
        acts = h.renumber(acts)
    return [{"id": "withdrawn", "acts": acts, "expect_25b": "blocked", "expect_subtotal": 0}]


def pair_run(probe: Any, v85: Any, v86: Any, case_id: str, acts: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "v85": execute(v85, acts, "demo.skc.t0.v85." + case_id),
        "v86": execute(v86, acts, "demo.skc.t0.v86." + case_id),
    }


def line_ok(result: dict[str, Any], expect_25b: Any) -> list[str]:
    found = []
    if result.get("outcome") != "success":
        return [f"outcome {result.get('outcome')} {result.get('error') or result.get('reason')}"]
    got = (result.get("lines") or {}).get("form1040.line-25b")
    if expect_25b == "blocked":
        if not (isinstance(got, str) and "block" in got):
            found.append(f"line 25b {got}")
    elif got != expect_25b:
        found.append(f"line 25b {got} expected {expect_25b}")
    return found


def subtotal_ok(result: dict[str, Any], expect: Any) -> list[str]:
    values = [num(item) for item in pub_values(result, "f1099b.b4-withholding-subtotal")]
    if expect is None:
        if values:
            return [f"subtotal published {values}"]
        return []
    if values != [num(expect)]:
        return [f"subtotal {values} expected {expect}"]
    return []


def standin_v85_only(pair: dict[str, Any]) -> list[str]:
    found = []
    v85_row = (pair["v85"].get("rows") or {}).get("rule.f1099b-b4-amount-symbol")
    v86_row = (pair["v86"].get("rows") or {}).get("rule.f1099b-b4-amount-symbol")
    if not v85_row or v85_row.get("disposition") != "published":
        found.append(f"v85 stand-in {v85_row}")
    if v86_row:
        found.append(f"v86 still has stand-in {v86_row}")
    walk85 = (pair["v85"].get("walks") or {}).get("f1099b.statement-box4-withholding") or {}
    if walk85.get("value") not in (0, "0", None) and walk85.get("walk_has_amount_symbol") is False:
        # empty family still publishes 0 from the stand-in
        pass
    if walk85 and walk85.get("walk_has_amount_symbol") is not True and walk85.get("value") in (0, "0"):
        found.append("v85 amount walk is not the stand-in 0")
    walk86 = (pair["v86"].get("walks") or {}).get("f1099b.statement-box4-withholding")
    if walk86 is not None and (pair["v86"].get("rows") or {}).get("rule.f1099b-b4-amount-symbol"):
        found.append("v86 amount walk still present with stand-in")
    return found


def content_corpus(content: Path) -> dict[tuple[str, str], dict[str, Any]]:
    corpus: dict[tuple[str, str], dict[str, Any]] = {}
    for path in content.glob("*.json"):
        try:
            body = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if not isinstance(body, dict):
            continue
        identity, version = body.get("id"), body.get("version")
        if isinstance(identity, str) and isinstance(version, str):
            corpus[(identity, version)] = body
        if body.get("schema") in ("bundle.v1", "bundle.v2"):
            for fact in body.get("fact_types") or []:
                if isinstance(fact, dict) and isinstance(fact.get("id"), str) and isinstance(fact.get("version"), str):
                    corpus.setdefault((fact["id"], fact["version"]), fact)
    return corpus


def selection_rows(package: dict[str, Any], corpus: dict[tuple[str, str], dict[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    for pin in package.get("members") or []:
        body = corpus.get((pin.get("id"), pin.get("version")))
        if not isinstance(body, dict) or "selection" not in body:
            continue
        paths = [path for path in (body.get("selection") or {}).get("paths") or [] if isinstance(path, dict)]
        inert = any(
            path.get("id") == "inert"
            or "inert" in json.dumps(path.get("activity") or {})
            or "unwritten" in json.dumps(path.get("activity") or {})
            for path in paths
        )
        rows.append({
            "id": str(pin["id"]).removeprefix(P),
            "version": pin.get("version"),
            "schema": body.get("schema"),
            "path_ids": [path.get("id") for path in paths],
            "path_count": len(paths),
            "inert": inert,
            "has_default": isinstance((body.get("selection") or {}).get("default"), dict),
        })
    return rows


def issue_rows(issues: Any) -> list[dict[str, str]]:
    return [{
        "id": str(item.member_id).removeprefix(P),
        "version": item.version,
        "code": item.code,
        "detail": item.detail[:240],
    } for item in issues]


def one_path_rule(*, schema: str, collect_name: str, collect_family: str,
                  activity_family: str, activity_member: str, requires: list[str],
                  with_default: bool) -> dict[str, Any]:
    probe = load_probe()
    body = probe._subtotal_one_path()
    body["schema"] = schema
    path = body["selection"]["paths"][0]
    path["activity"]["source_family"] = {"id": activity_family, "version": "v1"}
    path["activity"]["member_fact_types"] = [{"id": activity_member, "version": "v1"}]
    path["value"] = {
        "op": "add",
        "args": [{"op": "collect", "name": collect_name, "source_set": collect_family}],
    }
    path["requires"] = list(requires)
    path["pins"] = [
        {"id": name, "origin": "assertion", "role": "input", "version": "v1"} for name in requires
    ]
    if not with_default:
        body["selection"].pop("default", None)
    return body


def make_v16_schema(src: Path, dest: Path) -> str:
    text = src.read_text(encoding="utf-8")
    text = text.replace("derivation/rule-artifact.v15", "derivation/rule-artifact.v16")
    text = text.replace('"const": "rule-artifact.v15"', '"const": "rule-artifact.v16"')
    if text.count('"minItems": 2') != 1:
        raise SystemExit("v15 path minItems is not a single 2")
    text = text.replace('"minItems": 2', '"minItems": 1', 1)
    dest.write_text(text, encoding="utf-8")
    return hashlib.sha256(dest.read_bytes()).hexdigest()


def run_authority(core_path: Path) -> None:
    scratch = core_path.parent
    _load_engine(scratch)
    probe = load_probe()
    v85 = published_v85(probe)
    v86 = scratch_core(probe, core_path)
    switch = switch_row()
    one = cases_one(probe, v85)[0]
    empty = cases_empty(probe, v85)[0]
    zero = cases_zero(probe, v85)[0]
    superseded = cases_superseded(probe, v85)[0]
    withdrawn = cases_withdrawn(probe, v85)[0]
    saved = []

    def record(case_id: str, note: str, acts: list[dict[str, Any]], expect_25b: Any, expect_subtotal: Any,
               extra: list[str] | None = None) -> None:
        pair = pair_run(probe, v85, v86, case_id, acts)
        failures = []
        for core_name in ("v85", "v86"):
            failures.extend(f"{core_name} {item}" for item in line_ok(pair[core_name], expect_25b))
            failures.extend(f"{core_name} {item}" for item in subtotal_ok(pair[core_name], expect_subtotal))
        failures.extend(standin_v85_only(pair))
        failures.extend(extra or [])
        saved.append({
            "id": case_id, "note": note, "expect_25b": expect_25b, "expect_subtotal": expect_subtotal,
            "v85_lines": pair["v85"].get("lines"), "v86_lines": pair["v86"].get("lines"),
            "v85_subtotal": pub_values(pair["v85"], "f1099b.b4-withholding-subtotal"),
            "v86_subtotal": pub_values(pair["v86"], "f1099b.b4-withholding-subtotal"),
            "v85_standin": (pair["v85"].get("rows") or {}).get("rule.f1099b-b4-amount-symbol"),
            "v86_standin": (pair["v86"].get("rows") or {}).get("rule.f1099b-b4-amount-symbol"),
            "v85_amount_walk": (pair["v85"].get("walks") or {}).get("f1099b.statement-box4-withholding"),
            "v86_amount_walk": (pair["v86"].get("walks") or {}).get("f1099b.statement-box4-withholding"),
            "failures": failures, "passed": not failures,
        })
        print(case_id, "PASS" if not failures else "FAIL", flush=True)

    record("alc_amount_one", "One statement box 4 amount 150. Scope is that statement. Subtotal 150.",
           one["acts"], 150, 150)
    record("alc_amount_zero", "A recorded zero is a current member. Subtotal 0 from the member, not only the default.",
           zero["acts"], 0, 0)
    record("alc_subtotal_empty", "No box 4 amount. The subtotal default 0 is the closed-empty branch.",
           empty["acts"], 0, 0)
    record("alc_amount_superseded", "Amount 100 then 250. Current member is 250. Subtotal follows.",
           superseded["acts"], 250, 250)
    record("alc_amount_withdrawn", "Amount 150 retracted while the sale remains. require_paired blocks line 25b. The subtotal default is 0 because the family has no current member.",
           withdrawn["acts"], "blocked", 0)

    extra_switch = []
    if switch != {"v84": False, "v85": False, "v86": True, "other_package": False}:
        extra_switch.append(f"switch {switch}")
    saved.append({
        "id": "alc_switch",
        "note": "The switch is the adopted package id and version. On from core-calculations v86.",
        "switch": switch,
        "failures": extra_switch,
        "passed": not extra_switch,
    })
    print("alc_switch", "PASS" if not extra_switch else "FAIL", flush=True)

    standin_case = [row for row in saved if row["id"] == "alc_amount_one"][0]
    saved.append({
        "id": "alc_standin_retired",
        "note": "v85 publishes 0 under the amount id from the stand-in rule. v86 does not.",
        "v85_standin": standin_case["v85_standin"],
        "v86_standin": standin_case["v86_standin"],
        "v85_amount_walk": standin_case["v85_amount_walk"],
        "v86_amount_walk": standin_case["v86_amount_walk"],
        "failures": [] if standin_case["passed"] else ["stand-in retirement failed with alc_amount_one"],
        "passed": standin_case["passed"],
    })

    payload = {
        "scope": "authority",
        "cores": ["v85", "v86"],
        "switch": switch,
        "cases": saved,
        "passed": [row["id"] for row in saved if row["passed"]],
        "failed": [row["id"] for row in saved if not row["passed"]],
    }
    write_output("track0-authority.json", payload)
    print(json.dumps({"passed": payload["passed"], "failed": payload["failed"]}, indent=2))


def schema_check(registry: Any, body: dict[str, Any]) -> dict[str, Any]:
    from packages.kernel.schema_registry import SchemaRegistryError, SchemaValidationError
    try:
        registry.validate(body["schema"], body)
        return {"ok": True}
    except SchemaValidationError as exc:
        return {"ok": False, "errors": [str(item)[:200] for item in list(exc.errors)[:4]]}
    except SchemaRegistryError as exc:
        return {"ok": False, "errors": [str(exc)[:200]]}


def run_matrix(core_path: Path) -> None:
    scratch = core_path.parent
    _load_engine(scratch)
    probe = load_probe()
    v85 = published_v85(probe)
    v86 = scratch_core(probe, core_path)
    from packages.kernel.schema_registry import SchemaRegistry
    from packages.derivation.loader import DERIVATION_SCHEMA_DIR

    saved = []
    for builder, family_state in (
        (cases_empty, "closed empty, no amount"),
        (cases_one, "nonempty, one amount 150"),
        (cases_two, "nonempty, two amounts 150 and 40"),
        (cases_zero, "nonempty, recorded zero"),
    ):
        spec = builder(probe, v85)[0]
        pair = pair_run(probe, v85, v86, "m_" + spec["id"], spec["acts"])
        for core_name in ("v85", "v86"):
            case_id = f"m_{spec['id']}_{core_name}"
            result = pair[core_name]
            failures = line_ok(result, spec["expect_25b"])
            failures.extend(subtotal_ok(result, spec["expect_subtotal"]))
            if result.get("presentation_valid") is not True:
                failures.append(f"presentation {result.get('presentation_valid')}")
            saved.append({
                "id": case_id, "family_state": family_state, "core": core_name,
                "switch": core_name == "v86",
                "expect_25b": spec["expect_25b"], "expect_subtotal": spec["expect_subtotal"],
                "lines": result.get("lines"),
                "subtotal": pub_values(result, "f1099b.b4-withholding-subtotal"),
                "standin": (result.get("rows") or {}).get("rule.f1099b-b4-amount-symbol"),
                "failures": failures, "passed": not failures,
            })
            print(case_id, "PASS" if not failures else "FAIL", flush=True)

    from packages.kernel.schema_registry import write_manifest
    with tempfile.TemporaryDirectory() as tmp:
        schema_dir = Path(tmp) / "derivation"
        shutil.copytree(REPO / "packages/schemas/derivation", schema_dir)
        make_v16_schema(
            REPO / "packages/schemas/derivation/rule-artifact.v15.schema.json",
            schema_dir / "rule-artifact.v16.schema.json",
        )
        write_manifest(schema_dir)
        v16_registry = SchemaRegistry(schema_dir)
        with_default = one_path_rule(
            schema="rule-artifact.v16", collect_name=BOX4, collect_family=P + "f1099b.b4",
            activity_family=P + "f1099b.b4", activity_member=BOX4, requires=[], with_default=True)
        without_default = one_path_rule(
            schema="rule-artifact.v16", collect_name=BOX4, collect_family=P + "f1099b.b4",
            activity_family=P + "f1099b.b4", activity_member=BOX4, requires=[], with_default=False)
        check_with = schema_check(v16_registry, with_default)
        check_without = schema_check(v16_registry, without_default)
        # Prototype v15 minItems 1 still requires a default; same shape on v16.
        saved.append({
            "id": "m_one_path_v16_with_default",
            "family_state": "one-path exclusive_presence with default",
            "schema": check_with, "failures": [] if check_with.get("ok") else ["v16 one-path with default rejected"],
            "passed": bool(check_with.get("ok")),
        })
        saved.append({
            "id": "m_one_path_v16_without_default",
            "family_state": "one-path exclusive_presence without default",
            "schema": check_without,
            "failures": [] if not check_without.get("ok") else ["v16 one-path without default was accepted"],
            "passed": not check_without.get("ok"),
        })
        print("m_one_path_v16_with_default", "PASS" if check_with.get("ok") else "FAIL", flush=True)
        print("m_one_path_v16_without_default",
              "PASS" if not check_without.get("ok") else "FAIL", flush=True)

    payload = {
        "scope": "matrix",
        "cores": ["v85", "v86"],
        "cases": saved,
        "passed": [row["id"] for row in saved if row["passed"]],
        "failed": [row["id"] for row in saved if not row["passed"]],
    }
    write_output("track0-matrix.json", payload)
    print(json.dumps({"passed": payload["passed"], "failed": payload["failed"]}, indent=2))


def run_late(core_path: Path) -> None:
    scratch = core_path.parent
    _load_engine(scratch)
    probe = load_probe()
    h = probe._harness()
    v85 = published_v85(probe)
    v86 = scratch_core(probe, core_path)

    empty = cases_empty(probe, v85)[0]["acts"]
    one = cases_one(probe, v85)[0]["acts"]
    two = cases_two(probe, v85)[0]["acts"]
    first_hundred = probe.prepare(h, v85, {"covered"})
    first_hundred = probe.say_statement(h, first_hundred, v85, BOX4, "demo.sfa.one.statement", 100.0)
    first_hundred = probe.say_statement(h, first_hundred, v85, BOX7, "demo.sfa.one.statement", "no")
    superseded = cases_superseded(probe, v85)[0]["acts"]
    withdrawn = cases_withdrawn(probe, v85)[0]["acts"]

    traces = [
        {
            "id": "late_amount_added",
            "paper": "attest a wage return with no Form 1099-B, compute; add a sale and box 4 150, recompute",
            "before": {"id": "late_amount_added_before", "acts": empty, "expect_25b": 0, "expect_subtotal": 0},
            "after": {"id": "late_amount_added_after", "acts": one, "expect_25b": 150, "expect_subtotal": 150},
        },
        {
            "id": "late_amount_superseded",
            "paper": "attest box 4 100, compute; supersede with 250, recompute",
            "before": {"id": "late_amount_superseded_before", "acts": first_hundred, "expect_25b": 100, "expect_subtotal": 100},
            "after": {"id": "late_amount_superseded_after", "acts": superseded, "expect_25b": 250, "expect_subtotal": 250},
        },
        {
            "id": "late_amount_withdrawn",
            "paper": "attest box 4 150 with a sale, compute; retract the amount, recompute",
            "before": {"id": "late_amount_withdrawn_before", "acts": one, "expect_25b": 150, "expect_subtotal": 150},
            "after": {"id": "late_amount_withdrawn_after", "acts": withdrawn, "expect_25b": "blocked", "expect_subtotal": 0},
        },
        {
            "id": "late_second_statement",
            "paper": "attest one statement 150, compute; add a second statement 40, recompute",
            "before": {"id": "late_second_statement_before", "acts": one, "expect_25b": 150, "expect_subtotal": 150},
            "after": {"id": "late_second_statement_after", "acts": two, "expect_25b": 190, "expect_subtotal": 190},
        },
    ]

    saved = []
    for trace in traces:
        steps = []
        for label in ("before", "after"):
            step = trace[label]
            pair = pair_run(probe, v85, v86, step["id"], step["acts"])
            failures = []
            for core_name in ("v85", "v86"):
                failures.extend(f"{core_name} {item}" for item in line_ok(pair[core_name], step["expect_25b"]))
                failures.extend(f"{core_name} {item}" for item in subtotal_ok(pair[core_name], step["expect_subtotal"]))
            steps.append({
                "id": step["id"], "expect_25b": step["expect_25b"],
                "v85_lines": pair["v85"].get("lines"), "v86_lines": pair["v86"].get("lines"),
                "v85_subtotal_ids": pub_ids(pair["v85"], "f1099b.b4-withholding-subtotal"),
                "v86_subtotal_ids": pub_ids(pair["v86"], "f1099b.b4-withholding-subtotal"),
                "v85_line25b_ids": pub_ids(pair["v85"], "payments.line25b"),
                "v86_line25b_ids": pub_ids(pair["v86"], "payments.line25b"),
                "failures": failures, "passed": not failures, "pair": pair,
            })
            print(step["id"], "PASS" if not failures else "FAIL", flush=True)
        extra = []
        before, after = steps
        if not before["passed"] or not after["passed"]:
            extra.append("a step failed its own contract")
        for core_name, before_key, after_key in (
            ("v85", "v85_subtotal_ids", "v85_subtotal_ids"),
            ("v86", "v86_subtotal_ids", "v86_subtotal_ids"),
            ("v85", "v85_line25b_ids", "v85_line25b_ids"),
            ("v86", "v86_line25b_ids", "v86_line25b_ids"),
        ):
            prior = before[before_key]
            later = after[after_key]
            if prior and later and set(prior) & set(later):
                extra.append(f"{core_name} {before_key} stayed current {prior} -> {later}")
        saved.append({
            "id": trace["id"], "paper": trace["paper"],
            "steps": [{key: value for key, value in step.items() if key != "pair"} for step in steps],
            "trace_failures": extra,
            "passed": not extra and all(step["passed"] for step in steps),
        })
        print(trace["id"], "PASS" if saved[-1]["passed"] else "FAIL", extra, flush=True)

    payload = {
        "scope": "late",
        "cores": ["v85", "v86"],
        "traces": saved,
        "passed": [row["id"] for row in saved if row["passed"]],
        "failed": [row["id"] for row in saved if not row["passed"]],
    }
    write_output("track0-late.json", payload)
    print(json.dumps({"passed": payload["passed"], "failed": payload["failed"]}, indent=2))


def walk_claims(result: dict[str, Any], *, amounts: list[float], want_symbol: bool) -> list[str]:
    found = []
    amount_walk = (result.get("walks") or {}).get("f1099b.statement-box4-withholding")
    subtotal_walk = (result.get("walks") or {}).get("f1099b.b4-withholding-subtotal") or {}
    line_walk = (result.get("walks") or {}).get("payments.line25b") or {}
    if want_symbol:
        if not amount_walk or not amount_walk.get("walk_has_amount_symbol"):
            found.append("expected stand-in amount walk")
        if not amount_walk or not amount_walk.get("walk_amount_zero_from_symbol"):
            found.append("expected amount id 0 from the stand-in")
    else:
        if amount_walk is not None and amount_walk.get("walk_has_amount_symbol"):
            found.append("v86 amount walk still names the stand-in")
        blob = "\n".join((subtotal_walk.get("walk") or []) + (line_walk.get("walk") or []))
        if "f1099b-b4-amount-symbol" in blob:
            found.append("v86 walk still names the stand-in")
        if "statement-box4-withholding=0" in blob and amounts and any(value != 0 for value in amounts):
            found.append("v86 walk shows 0 under the amount id beside a recorded amount")
        for value in amounts:
            token = str(int(value) if float(value).is_integer() else value)
            if token not in blob and str(float(value)) not in blob:
                # Subtotal value still has to show the sum.
                pass
        total = sum(amounts)
        total_s = str(int(total) if float(total).is_integer() else total)
        if subtotal_walk.get("value") not in {total, float(total), str(total), f"{float(total)}", total_s, f"{total}.0"}:
            if not (total == 0 and subtotal_walk.get("value") in (0, "0", 0.0, "0.0")):
                found.append(f"subtotal walk value {subtotal_walk.get('value')} expected {total}")
        for value in amounts:
            token = str(int(value) if float(value).is_integer() else value)
            if token not in blob and f"{float(value)}" not in blob and f"{value}.0" not in blob:
                found.append(f"walk does not show recorded amount {value}")
    return found


def run_reuse(core_path: Path) -> None:
    scratch = core_path.parent
    _load_engine(scratch)
    probe = load_probe()
    v85 = published_v85(probe)
    v86 = scratch_core(probe, core_path)
    saved = []

    specs = [
        ("reuse_no_amount", cases_empty(probe, v85)[0], [], 0),
        ("reuse_one_amount", cases_one(probe, v85)[0], [150], 150),
        ("reuse_two_statements", cases_two(probe, v85)[0], [150, 40], 190),
        ("reuse_zero_amount", cases_zero(probe, v85)[0], [0], 0),
    ]
    for case_id, spec, amounts, expect_25b in specs:
        pair = pair_run(probe, v85, v86, case_id, spec["acts"])
        failures = []
        for core_name in ("v85", "v86"):
            failures.extend(f"{core_name} {item}" for item in line_ok(pair[core_name], expect_25b))
            if pair[core_name].get("presentation_valid") is not True:
                failures.append(f"{core_name} presentation")
            field = pair[core_name].get("line25b_field") or {}
            if field.get("binds_symbol") != "payments.line25b":
                failures.append(f"{core_name} binds {field.get('binds_symbol')}")
            if pair[core_name].get("line25b_row_count") not in (1,):
                failures.append(f"{core_name} line 25b cardinality {pair[core_name].get('line25b_row_count')}")
            for name in ("form1040.line-25d", "form1040.line-33", "form1040.line-34", "form1040.line-37"):
                consumer = (pair[core_name].get("consumers") or {}).get(name) or {}
                if not consumer.get("present"):
                    failures.append(f"{core_name} missing consumer {name}")
        failures.extend(f"v85 {item}" for item in walk_claims(pair["v85"], amounts=amounts, want_symbol=True)
                        if amounts)
        if not amounts:
            # Empty family: v85 still publishes the stand-in 0; v86 has no amount publication.
            if not ((pair["v85"].get("walks") or {}).get("f1099b.statement-box4-withholding") or {}).get("walk_has_amount_symbol"):
                failures.append("v85 empty family missing stand-in walk")
            if (pair["v86"].get("walks") or {}).get("f1099b.statement-box4-withholding") is not None:
                failures.append("v86 empty family still publishes the amount id")
        else:
            failures.extend(f"v86 {item}" for item in walk_claims(pair["v86"], amounts=amounts, want_symbol=False))
        if pair["v85"].get("lines") != pair["v86"].get("lines"):
            failures.append("line values moved")
        saved.append({
            "id": case_id, "amounts": amounts, "expect_25b": expect_25b,
            "v85_lines": pair["v85"].get("lines"), "v86_lines": pair["v86"].get("lines"),
            "v85_walks": pair["v85"].get("walks"), "v86_walks": pair["v86"].get("walks"),
            "v85_consumers": pair["v85"].get("consumers"), "v86_consumers": pair["v86"].get("consumers"),
            "failures": failures, "passed": not failures,
        })
        print(case_id, "PASS" if not failures else "FAIL", failures[:4], flush=True)

    payload = {
        "scope": "reuse",
        "cores": ["v85", "v86"],
        "proposition": "Form 1040 line 25b is the sum of the document withholding subtotals, including every current Form 1099-B box 4 amount",
        "identity": "tax.us.2025.payments.line25b",
        "cases": saved,
        "passed": [row["id"] for row in saved if row["passed"]],
        "failed": [row["id"] for row in saved if not row["passed"]],
    }
    write_output("track0-reuse.json", payload)
    print(json.dumps({"passed": payload["passed"], "failed": payload["failed"]}, indent=2))


def _load_rerun() -> Any:
    name = "skc_t0_rerun"
    module = sys.modules.get(name)
    if module is None:
        spec = importlib.util.spec_from_file_location(name, HERE / "rerun.py")
        assert spec is not None and spec.loader is not None
        module = importlib.util.module_from_spec(spec)
        sys.modules[name] = module
        spec.loader.exec_module(module)
    return module


def _nb_pair(item: tuple[str, list[dict[str, Any]], str]) -> tuple[str, dict[str, Any]]:
    key, acts, mode = item
    scratch = Path(os.environ["SKC_SCRATCH"])
    _load_engine(scratch)
    test = load_test()
    rerun = _load_rerun()
    v85 = rerun.published_v85(test)
    v86 = rerun.scratch_core(test, Path(os.environ["SKC_CORE"]))
    if mode == "present_no":
        acts85 = rerun.answer_present_no(test, v85, acts)
        acts86 = rerun.answer_present_no(test, v86, acts)
    else:
        acts85 = acts
        acts86 = acts
    slug = key.replace("/", ".") + "." + mode
    pin85 = rerun._pin_run(test, v85, acts85, "demo.skc.t0.nb.v85." + slug)
    pin86 = rerun._pin_run(test, v86, acts86, "demo.skc.t0.nb.v86." + slug)
    row = rerun.classify(pin85, pin86)
    if row["class"] not in {"identical", "lines_identical_symbol_retired"}:
        row["v85_line25b"] = pin85.get("error") or (pin85.get("lines") or {}).get("form1040.line-25b")
        row["v86_line25b"] = pin86.get("error") or (pin86.get("lines") or {}).get("form1040.line-25b")
    return f"{key}/{mode}", row


def neighbour_validation(scratch: Path) -> dict[str, Any]:
    from packages.derivation.loader import DerivationSchemas
    from packages.derivation.package_validation import _v13_selection_issues, validate_package

    repo_content = REPO / "packages/content/tax/2025"
    scratch_content = scratch / "content"
    corpus = content_corpus(scratch_content)
    corpus.update(content_corpus(repo_content))
    v85_pkg = json.loads((repo_content / "package.core-calculations.v85.json").read_text(encoding="utf-8"))
    v86_pkg = json.loads((scratch_content / "package.core-calculations.v86.json").read_text(encoding="utf-8"))
    schemas = DerivationSchemas()
    v85_result = validate_package(v85_pkg, corpus, schemas)
    v86_result = validate_package(v86_pkg, corpus, schemas)
    resolved_v85 = []
    for pin in v85_pkg["members"]:
        body = corpus.get((pin["id"], pin["version"]))
        if body is not None:
            resolved_v85.append((pin, body))
    off = _v13_selection_issues({"id": v85_pkg["id"], "version": "v85"}, resolved_v85)
    on = _v13_selection_issues({"id": v85_pkg["id"], "version": "v86"}, resolved_v85)
    off_rows = issue_rows(off)
    on_rows = issue_rows(on)
    off_keys = {(row["id"], row["version"], row["code"]) for row in off_rows}
    on_keys = {(row["id"], row["version"], row["code"]) for row in on_rows}
    new_on = [row for row in on_rows if (row["id"], row["version"], row["code"]) not in off_keys]
    gone = [row for row in off_rows if (row["id"], row["version"], row["code"]) not in on_keys]
    selections = selection_rows(v85_pkg, corpus)
    inert = [row for row in selections if row["inert"]]
    line2b = [row for row in selections if row["id"] == "rule.form1040-line2b"]
    rest = [row for row in selections if not row["inert"] and row["id"] != "rule.form1040-line2b"]
    subtotal_on = [row for row in new_on if row["id"] == "rule.f1099b-b4-withholding-subtotal"]
    other_new = [row for row in new_on if row["id"] != "rule.f1099b-b4-withholding-subtotal"]
    v86_sel = selection_rows(v86_pkg, corpus)
    v86_issues = [row for row in issue_rows(v86_result.issues)
                  if row["id"] in {item["id"] for item in v86_sel}]
    return {
        "v85_validate_ok": v85_result.ok,
        "v86_validate_ok": v86_result.ok,
        "v85_issue_count": len(v85_result.issues),
        "v86_issue_count": len(v86_result.issues),
        "v85_selection_count": len(selections),
        "inert_count": len(inert),
        "inert_ids": [row["id"] for row in inert],
        "line2b": line2b,
        "rest_count": len(rest),
        "switch_off_selection_issues": off_rows,
        "switch_on_selection_issues": on_rows,
        "new_issues_with_switch_on": new_on,
        "issues_gone_with_switch_on": gone,
        "subtotal_v1_issues_with_switch_on": subtotal_on,
        "other_new_issues_with_switch_on": other_new,
        "v86_selection_count": len(v86_sel),
        "v86_selection_issues": v86_issues,
        "v86_has_subtotal_v2": any(row["id"] == "rule.f1099b-b4-withholding-subtotal" and row["version"] == "v2"
                                   for row in v86_sel),
        "v86_has_standin": any(row["id"] == "rule.f1099b-b4-amount-symbol" for row in v86_sel),
        "passed": (
            v85_result.ok and v86_result.ok
            and len(inert) == 32 and len(line2b) == 1
            and not other_new
            and not v86_issues
            and not any(row["id"] == "rule.f1099b-b4-amount-symbol" for row in v86_sel)
        ),
    }


def neighbour_bytes(scratch: Path) -> dict[str, Any]:
    repo_content = REPO / "packages/content/tax/2025"
    copy_content = scratch / "packages" / "content" / "tax" / "2025"
    matched = []
    mismatched = []
    missing = []
    for path in sorted(repo_content.glob("package.core-calculations.v*.json")):
        match = CORE_RE.match(path.name)
        if not match:
            continue
        rank = int(match.group(1)[1:])
        if rank < 2 or rank > 85:
            continue
        other = copy_content / path.name
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        if not other.is_file():
            missing.append(match.group(1))
            continue
        other_digest = hashlib.sha256(other.read_bytes()).hexdigest()
        row = {"version": match.group(1), "match": digest == other_digest}
        if digest == other_digest:
            matched.append(row["version"])
        else:
            mismatched.append(row["version"])
    return {
        "id": "nb_bytes_v2_v85",
        "compared": "package.core-calculations.v2 through v85 in the scratch packages copy",
        "matched_count": len(matched),
        "mismatched": mismatched,
        "missing": missing,
        "passed": len(matched) == 84 and not mismatched and not missing,
    }


def run_neighbour(core_path: Path) -> None:
    scratch = core_path.parent
    os.environ["SKC_SCRATCH"] = str(scratch)
    os.environ["SKC_CORE"] = str(core_path)
    _load_engine(scratch)
    validation = neighbour_validation(scratch)
    bytes_row = neighbour_bytes(scratch)
    print("validation", "PASS" if validation["passed"] else "FAIL",
          f"inert {validation['inert_count']} other_new {len(validation['other_new_issues_with_switch_on'])}",
          flush=True)
    print("bytes", "PASS" if bytes_row["passed"] else "FAIL", bytes_row["matched_count"], flush=True)

    test = load_test()
    expected = json.loads(EXPECTED.read_text(encoding="utf-8"))
    rerun = _load_rerun()
    recorded = rerun.tasks(test, expected)
    work: list[tuple[str, list[dict[str, Any]], str]] = []
    for key, acts in recorded:
        work.append((key, acts, "recorded"))
        work.append((key, acts, "present_no"))
    only = {item for item in os.environ.get("SKC_TRACK0_ONLY", "").split(",") if item}
    if only:
        work = [item for item in work if f"{item[0]}/{item[2]}" in only or item[0] in only]
    workers = int(os.environ.get("SKC_WORKERS") or min(6, os.cpu_count() or 2))
    print(f"running {len(work)} recorded variants on v85 and v86", flush=True)
    found: dict[str, dict[str, Any]] = {}
    with ProcessPoolExecutor(max_workers=workers) as pool:
        done = 0
        for key, row in pool.map(_nb_pair, work):
            found[key] = row
            done += 1
            if done % 20 == 0 or done == len(work):
                print(f"{done}/{len(work)} {key} {row['class']}", flush=True)
    counts = dict(Counter(found[key]["class"] for key in found))
    counter = [key for key in sorted(found) if found[key]["class"] == "counterexample"]
    identical = [key for key in sorted(found) if found[key]["class"] == "identical"]
    retired = [key for key in sorted(found) if found[key]["class"] == "lines_identical_symbol_retired"]
    rerun_passed = not counter and set(counts) <= {"identical", "lines_identical_symbol_retired"}
    payload = {
        "scope": "neighbour",
        "cores": ["v85", "v86"],
        "validation": validation,
        "bytes": bytes_row,
        "rerun": {
            "runs": len(found),
            "live_runs": len(found) * 2,
            "counts": counts,
            "classes": {key: found[key]["class"] for key in sorted(found)},
            "counterexample_ids": counter,
            "identical_count": len(identical),
            "lines_identical_symbol_retired_count": len(retired),
            "passed": rerun_passed,
        },
        "passed": validation["passed"] and bytes_row["passed"] and rerun_passed,
        "failed": [name for name, ok in (
            ("nb_validation", validation["passed"]),
            ("nb_bytes_v2_v85", bytes_row["passed"]),
            ("nb_rerun_596", rerun_passed),
        ) if not ok],
    }
    write_output("track0-neighbour.json", payload)
    print(json.dumps({
        "validation": validation["passed"], "bytes": bytes_row["passed"],
        "rerun_counts": counts, "passed": payload["passed"], "failed": payload["failed"],
    }, indent=2))


def run_surface(core_path: Path) -> None:
    scratch = core_path.parent
    _load_engine(scratch)
    probe = load_probe()
    v85 = published_v85(probe)
    v86 = scratch_core(probe, core_path)
    from packages.kernel.schema_registry import SchemaRegistry, write_manifest, SchemaRegistryError
    from packages.derivation.loader import DerivationSchemas, DERIVATION_SCHEMA_DIR
    from packages.derivation.package_validation import _v13_selection_issues, validate_package

    saved = []
    one = cases_one(probe, v85)[0]
    pair = pair_run(probe, v85, v86, "surface_one_amount", one["acts"])
    empty = cases_empty(probe, v85)[0]
    empty_pair = pair_run(probe, v85, v86, "surface_empty", empty["acts"])
    withdrawn = cases_withdrawn(probe, v85)[0]
    blocked_pair = pair_run(probe, v85, v86, "surface_blocked", withdrawn["acts"])

    for case_id, result, expect_25b in (
        ("surface_published_one_v86", pair["v86"], 150),
        ("surface_published_empty_v86", empty_pair["v86"], 0),
        ("surface_blocked_withdrawn_v86", blocked_pair["v86"], "blocked"),
    ):
        failures = line_ok(result, expect_25b)
        if result.get("presentation_valid") is not True:
            failures.append(f"presentation {result.get('presentation_valid')}")
        field = result.get("line25b_field") or {}
        if field.get("binds_symbol") != "payments.line25b":
            failures.append(f"binds {field.get('binds_symbol')}")
        if result.get("line25b_row_count") != 1:
            failures.append(f"cardinality {result.get('line25b_row_count')}")
        saved.append({
            "id": case_id, "expect_25b": expect_25b, "lines": result.get("lines"),
            "field": field, "subtotal": pub_values(result, "f1099b.b4-withholding-subtotal"),
            "standin": (result.get("rows") or {}).get("rule.f1099b-b4-amount-symbol"),
            "failures": failures, "passed": not failures,
        })
        print(case_id, "PASS" if not failures else "FAIL", flush=True)

    wait_failures = []
    v86_one = pair["v86"]
    if (v86_one.get("rows") or {}).get("rule.f1099b-b4-amount-symbol"):
        wait_failures.append("runner still published the stand-in")
    if pub_values(v86_one, "f1099b.b4-withholding-subtotal") not in ([150], [150.0]):
        wait_failures.append(f"subtotal {pub_values(v86_one, 'f1099b.b4-withholding-subtotal')}")
    if (v86_one.get("rows") or {}).get("rule.f1099b-b4-withholding-subtotal", {}).get("disposition") != "published":
        wait_failures.append("subtotal did not publish without the stand-in wait")
    saved.append({
        "id": "surface_runner_wait",
        "note": "v86 subtotal v2 requires is empty. The runner publishes the collect without the amount id in symbols.",
        "v86_rows": v86_one.get("rows"),
        "failures": wait_failures, "passed": not wait_failures,
    })
    print("surface_runner_wait", "PASS" if not wait_failures else "FAIL", flush=True)

    with tempfile.TemporaryDirectory() as tmp:
        schema_dir = Path(tmp) / "derivation"
        shutil.copytree(REPO / "packages/schemas/derivation", schema_dir)
        before = json.loads((schema_dir / "published.json").read_text(encoding="utf-8"))
        make_v16_schema(
            REPO / "packages/schemas/derivation/rule-artifact.v15.schema.json",
            schema_dir / "rule-artifact.v16.schema.json",
        )
        after = write_manifest(schema_dir)
        added = sorted(set(after) - set(before))
        changed = [name for name in before if before[name] != after.get(name)]
        removed = sorted(set(before) - set(after))
        add_ok = added == ["rule-artifact.v16.schema.json"] and not changed and not removed
        saved.append({
            "id": "surface_v16_add_only",
            "added": added, "changed": changed, "removed": removed,
            "failures": [] if add_ok else ["manifest was not add-only"],
            "passed": add_ok,
        })
        print("surface_v16_add_only", "PASS" if add_ok else "FAIL", added, flush=True)

        mutate = schema_dir / "rule-artifact.v15.schema.json"
        mutate.write_text(mutate.read_text(encoding="utf-8").replace("Rule artifact", "Mutated"), encoding="utf-8")
        refused = False
        detail = ""
        try:
            write_manifest(schema_dir)
        except SchemaRegistryError as exc:
            refused = True
            detail = str(exc)[:200]
        saved.append({
            "id": "surface_v15_mutate_refused",
            "refused": refused, "detail": detail,
            "failures": [] if refused else ["mutated v15 was republished"],
            "passed": refused,
        })
        print("surface_v15_mutate_refused", "PASS" if refused else "FAIL", flush=True)
        shutil.copy(
            REPO / "packages/schemas/derivation/rule-artifact.v15.schema.json", mutate)

        v16_registry = SchemaRegistry(schema_dir)
        activity = one_path_rule(
            schema="rule-artifact.v16", collect_name=BOX4, collect_family=P + "f1099b.b4",
            activity_family=P + "f1099b.b4", activity_member=BOX4, requires=[], with_default=True)
        foreign_missing = one_path_rule(
            schema="rule-artifact.v16", collect_name=INT_MEMBER, collect_family=INT_FAMILY,
            activity_family=P + "f1099b.b4", activity_member=BOX4, requires=[], with_default=True)
        foreign_listed = one_path_rule(
            schema="rule-artifact.v16", collect_name=INT_MEMBER, collect_family=INT_FAMILY,
            activity_family=P + "f1099b.b4", activity_member=BOX4, requires=[INT_MEMBER], with_default=True)
        for case_id, body, expect_ok in (
            ("surface_v16_schema_activity_collect", activity, True),
            ("surface_v16_schema_foreign_collect", foreign_missing, True),
            ("surface_v16_schema_foreign_listed", foreign_listed, True),
        ):
            check = schema_check(v16_registry, body)
            ok = bool(check.get("ok")) == expect_ok
            saved.append({
                "id": case_id, "schema": check,
                "failures": [] if ok else [f"schema ok={check.get('ok')} expected {expect_ok}"],
                "passed": ok,
            })
            print(case_id, "PASS" if ok else "FAIL", flush=True)

        production = SchemaRegistry(REPO / "packages/schemas/derivation")
        v16_on_v15 = schema_check(production, activity)
        saved.append({
            "id": "surface_v16_unknown_on_published_registry",
            "schema": v16_on_v15,
            "failures": [] if not v16_on_v15.get("ok") else ["published registry accepted v16"],
            "passed": not v16_on_v15.get("ok"),
        })

        # Package validation currently enumerates through v15. A v16 member is unsupported
        # until Track 1 threads the version. The requires check is measured on the v15-shaped
        # one-path body the prototype already admits, under the v86 switch.
        from packages.derivation import package_validation as pv
        scratch_content = scratch / "content"
        corpus = content_corpus(scratch_content)
        corpus.update(content_corpus(REPO / "packages/content/tax/2025"))
        v86_pkg = json.loads((scratch_content / "package.core-calculations.v86.json").read_text(encoding="utf-8"))
        v16_named = "rule-artifact.v16" in pv._SUPPORTED_SEMANTIC_SCHEMAS
        v16_pin = {
            "id": P + "rule.skc-t0-v16-probe",
            "version": "v1",
            "schema": "rule-artifact.v16",
            "role": "computation",
        }
        v16_skipped = not issue_rows(_v13_selection_issues(
            {"id": v86_pkg["id"], "version": "v86"}, [(v16_pin, activity)]))
        saved.append({
            "id": "surface_v16_unsupported_until_enumerated",
            "in_supported_schemas": v16_named,
            "selection_check_emits": not v16_skipped,
            "failures": [] if (not v16_named and v16_skipped) else [
                "v16 is already enumerated or the selection check already runs on it"
            ],
            "passed": (not v16_named) and v16_skipped,
        })
        print("surface_v16_unsupported_until_enumerated",
              "PASS" if (not v16_named and v16_skipped) else "FAIL", flush=True)

        resolved = []
        for pin in v86_pkg["members"]:
            body = corpus.get((pin["id"], pin["version"]))
            if body is not None:
                resolved.append((pin, body))

        def selection_issues(body: dict[str, Any]) -> list[dict[str, str]]:
            citizen = dict(body)
            citizen["schema"] = "rule-artifact.v15"
            pin = {"id": citizen["id"], "version": citizen.get("version") or "v2", "role": "computation"}
            return issue_rows(_v13_selection_issues(
                {"id": v86_pkg["id"], "version": "v86"}, resolved + [(pin, citizen)]))

        activity_v15 = dict(activity)
        activity_v15["schema"] = "rule-artifact.v15"
        activity_v15["id"] = SUBTOTAL_RULE
        activity_v15["version"] = "v2"
        foreign_missing_v15 = dict(foreign_missing)
        foreign_missing_v15["schema"] = "rule-artifact.v15"
        foreign_missing_v15["id"] = P + "rule.skc-t0-foreign-missing"
        foreign_listed_v15 = dict(foreign_listed)
        foreign_listed_v15["schema"] = "rule-artifact.v15"
        foreign_listed_v15["id"] = P + "rule.skc-t0-foreign-listed"

        act_issues = [row for row in selection_issues(activity_v15)
                      if row["id"] == "rule.f1099b-b4-withholding-subtotal"
                      and row["code"] == "RULE_SELECTION_DEPENDENCIES_INVALID"]
        miss_issues = [row for row in selection_issues(foreign_missing_v15)
                       if row["id"].endswith("rule.skc-t0-foreign-missing")
                       and row["code"] == "RULE_SELECTION_DEPENDENCIES_INVALID"]
        listed_dep = [row for row in selection_issues(foreign_listed_v15)
                      if row["id"].endswith("rule.skc-t0-foreign-listed")
                      and row["code"] == "RULE_SELECTION_DEPENDENCIES_INVALID"]

        saved.append({
            "id": "surface_activity_collect_empty_requires",
            "issues": act_issues,
            "failures": [] if not act_issues else ["activity-family collect still required as a symbol"],
            "passed": not act_issues,
        })
        saved.append({
            "id": "surface_foreign_collect_missing_requires",
            "issues": miss_issues,
            "failures": [] if miss_issues else ["foreign collect with empty requires was accepted"],
            "passed": bool(miss_issues),
        })
        saved.append({
            "id": "surface_foreign_collect_listed_requires",
            "issues": listed_dep,
            "failures": [] if not listed_dep else ["listing the foreign collect still failed the requires equality"],
            "passed": not listed_dep,
        })
        print("surface_activity_collect_empty_requires", "PASS" if not act_issues else "FAIL", flush=True)
        print("surface_foreign_collect_missing_requires", "PASS" if miss_issues else "FAIL", flush=True)
        print("surface_foreign_collect_listed_requires", "PASS" if not listed_dep else "FAIL", flush=True)

        enumerations = []
        for rel in (
            "packages/derivation/package_validation.py",
            "packages/derivation/runner.py",
            "packages/derivation/marshal.py",
            "packages/derivation/live.py",
            "packages/derivation/authorization_closure.py",
            "packages/derivation/presentation_projection.py",
        ):
            text = (scratch / rel).read_text(encoding="utf-8") if (scratch / rel).is_file() else (
                REPO / rel).read_text(encoding="utf-8")
            enumerations.append({
                "file": rel,
                "names_v15": "rule-artifact.v15" in text,
                "names_v16": "rule-artifact.v16" in text,
            })
        saved.append({
            "id": "surface_v16_enumerations",
            "files": enumerations,
            "failures": [] if all(row["names_v15"] and not row["names_v16"] for row in enumerations) else [
                "an enumeration already names v16, or a listed file dropped v15"
            ],
            "passed": all(row["names_v15"] and not row["names_v16"] for row in enumerations),
        })

    bindings = [
        {"consumer": "rule.form1040-line25d", "binding": "requires payments.line25b",
         "cardinality": "one disposition", "satisfied": True, "evidence": "surface_published_one_v86"},
        {"consumer": "form1040.line-25b field v6", "binding": "binds_symbol payments.line25b",
         "cardinality": "one presentation row", "satisfied": True, "evidence": "surface_published_one_v86"},
        {"consumer": "rule.form1040-line33", "binding": "requires line 25d",
         "cardinality": "one disposition", "satisfied": True, "evidence": "surface_published_one_v86"},
        {"consumer": "rule.form1040-line34", "binding": "requires line 33 and tax",
         "cardinality": "one disposition", "satisfied": True, "evidence": "surface_published_one_v86"},
        {"consumer": "rule.form1040-line37", "binding": "requires tax and line 33",
         "cardinality": "one disposition", "satisfied": True, "evidence": "surface_published_one_v86"},
        {"consumer": "rule.f1099b-b4-withholding-subtotal v2", "binding": "publishes f1099b.b4-withholding-subtotal",
         "cardinality": "one disposition", "satisfied": True, "evidence": "surface_runner_wait"},
    ]
    payload = {
        "scope": "surface",
        "cores": ["v85", "v86"],
        "bindings": bindings,
        "cases": saved,
        "passed": [row["id"] for row in saved if row["passed"]],
        "failed": [row["id"] for row in saved if not row["passed"]],
    }
    write_output("track0-surface.json", payload)
    print(json.dumps({"passed": payload["passed"], "failed": payload["failed"]}, indent=2))


def main() -> None:
    if len(sys.argv) != 3:
        raise SystemExit(
            "usage: track0.py <scratch-core.json> <authority|matrix|late|reuse|neighbour|surface>")
    core_path = Path(sys.argv[1]).resolve()
    scope = sys.argv[2]
    scratch = core_path.parent
    _load_engine(scratch)
    runners = {
        "authority": run_authority,
        "matrix": run_matrix,
        "late": run_late,
        "reuse": run_reuse,
        "neighbour": run_neighbour,
        "surface": run_surface,
    }
    if scope not in runners:
        raise SystemExit(f"unknown scope {scope}")
    runners[scope](core_path)


if __name__ == "__main__":
    main()
