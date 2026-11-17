"""P0: read line 6b's actual live-run presentation sentences on core v91.

Run: python3 <this-file> [--smoke]
Synthetic demo.* lists only. Sibling harnesses are loaded by unique names.
"""
from __future__ import annotations

import argparse
import copy
import importlib.util
import json
import os
import re
import sys
import tempfile
import time
from concurrent.futures import ProcessPoolExecutor
from functools import lru_cache
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
sys.path.insert(0, str(REPO))
CONTENT = REPO / "packages/content/tax/2025"
P = "tax.us.2025."
RULE = P + "rule.ss-benefits-worksheet"
STATUSES = ("single", "married_filing_jointly", "married_filing_separately")


def load(name: str, path: Path) -> Any:
    if name not in sys.modules:
        spec = importlib.util.spec_from_file_location(name, path)
        assert spec and spec.loader
        module = importlib.util.module_from_spec(spec)
        sys.modules[name] = module
        spec.loader.exec_module(module)
    return sys.modules[name]


def harness() -> Any:
    qw = load("l6b_p0_qw", HERE.parent / "question-wording-evidence/probe.py")
    return qw.load_harness()


def scopes() -> list[str]:
    rule = json.loads((CONTENT / "rule.ss-benefits-worksheet.v4.json").read_text())
    return [m["name"] for m in rule["when"]["args"][1]["members"]] + [
        P + "ss-benefits-scope.no-rrb-or-foreign-social-benefit"
    ]


@lru_cache(maxsize=1)
def producer_symbols() -> dict[str, str]:
    package = json.loads((CONTENT / "package.core-calculations.v91.json").read_text())
    result = {}
    for member in package["members"]:
        if member["role"] != "computation":
            continue
        slug = member["id"].removeprefix(P)
        candidates = (CONTENT / f"{slug}.{member['version']}.json", CONTENT / f"{slug}.json")
        for path in candidates:
            if path.is_file():
                body = json.loads(path.read_text())
                if body.get("id") == member["id"] and body.get("version") == member["version"]:
                    if isinstance(body.get("publishes"), str):
                        result[member["id"]] = body["publishes"]
                    break
    return result


def root_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Only line 6b's blocked producer walk, not unrelated return diagnostics."""
    symbols = producer_symbols()
    wanted = {P + "social-security.line6b"}
    found = []
    while True:
        added = [r for r in rows if r not in found and symbols.get(r.get("artifact_id", "")) in wanted]
        if not added:
            return found
        found.extend(added)
        for row in added:
            wanted.update(row.get("missing", []))


def base(status: str, *, benefits: bool = True, closed: bool = True,
         answered: bool = True) -> list[dict[str, Any]]:
    h = harness()
    qw = load("l6b_p0_qw", HERE.parent / "question-wording-evidence/probe.py")
    acts = qw.complete(h)
    answers = {
        P + "f1099b.no-sale-box4-present": "no",
        P + "filing-status": status,
        P + "taxpayer-over-65": False, P + "taxpayer-blind": False,
        P + "spouse-over-65": False, P + "spouse-blind": False,
        P + "mfs-lived-apart-all-year": "yes",
    }
    if answered:
        answers.update(dict.fromkeys(scopes(), "yes"))
    for fact, value in answers.items():
        acts = h.say(acts, fact, value, "l6b." + fact.removeprefix(P))
    if benefits:
        fw = load("l6b_p0_fw", REPO / "tests/test_form_1099_withholding.py")
        # Reproduce page-alerts' wage + SSA case, keeping the new membership
        # transition before its re-targeted closure attestation.
        head = fw._head(acts, fw.SSA_FAMILY)
        successor = "demo.l6b.ssa.h1"
        keys = (("statement", "demo.l6b.ssa.statement"),)
        fw._introduce(acts, "demo.l6b.ssa.statement", "tax.us.ssa1099-statement")
        for fact, value, tag in (
            (fw.SSA_B3, 12000.0, "box3"), (fw.SSA_B4, 0.0, "box4"),
            (fw.SSA_B6_WITNESS, 0.0, "box6-witness"),
            (fw.SSA_RECIPIENT, "taxpayer", "recipient"),
            (fw.SSA_KIND, "ssa-1099", "kind"), (fw.SSA_LUMP, False, "election"),
        ):
            fw._assert(acts, "demo.l6b.ssa." + tag, fact, keys, value)
        fw._transition(acts, (fw.SSA_FAMILY, "v1"), head, successor,
                       "demo.l6b.ssa.box5", fw.SSA_B5, keys, 12000.0)
        if closed:
            for index, act in enumerate(acts):
                finding = act.get("payload", {}).get("finding", {})
                if str(finding.get("fact_id", "")).startswith(P + "ssa1099.source-closure|"):
                    finding["fact_id"] = re.sub(r"family-horizon=[^,|]+",
                                                "family-horizon=" + successor, finding["fact_id"])
                    acts.append(acts.pop(index))
                    break
    elif not closed:
        acts = h.strip(acts, P + "ssa1099.source-closure")
    return h.renumber(acts)


def cases() -> list[dict[str, Any]]:
    h = harness()
    rows = []
    for status in STATUSES:
        stem = status.replace("married_filing_", "")
        acts = base(status)
        rows.append({"id": stem + ".all-yes", "status": status, "vary": None, "answer": "yes", "acts": acts})
        for fact in scopes():
            for answer in ("no", None):
                changed = h.strip(copy.deepcopy(acts), fact) if answer is None else h.say(
                    copy.deepcopy(acts), fact, answer, "l6b.vary")
                rows.append({"id": stem + "." + fact.removeprefix(P) + "." + (answer or "unanswered"),
                             "status": status, "vary": fact, "answer": answer, "acts": changed})
        for answer in ("no", None):
            fact = P + "mfs-lived-apart-all-year"
            changed = h.strip(copy.deepcopy(acts), fact) if answer is None else h.say(
                copy.deepcopy(acts), fact, answer, "l6b.living")
            rows.append({"id": stem + ".living." + (answer or "unanswered"),
                         "status": status, "vary": fact, "answer": answer, "acts": changed})
        for tag, kw in (
            ("ssa-open", {"closed": False}),
            ("no-benefits", {"benefits": False}),
            ("no-benefits-open", {"benefits": False, "closed": False}),
            ("original-incomplete", {"answered": False}),
        ):
            rows.append({"id": stem + "." + tag, "status": status, "vary": tag,
                         "answer": None, "acts": base(status, **kw)})
        election = h.say(copy.deepcopy(acts), P + "ss-benefits-scope.no-lump-sum-election", "no", "l6b.elected")
        for act in election:
            finding = act.get("payload", {}).get("finding", {})
            if str(finding.get("fact_id", "")).startswith(P + "ssa1099.lump-sum-election|"):
                finding["value"] = True
        rows.append({"id": stem + ".election-made", "status": status,
                     "vary": P + "ssa1099.lump-sum-election", "answer": True, "acts": election})
        missing_all = copy.deepcopy(acts)
        for fact in scopes():
            missing_all = h.strip(missing_all, fact)
        rows.append({"id": stem + ".all-scopes-unanswered", "status": status,
                     "vary": "all-scopes", "answer": None, "acts": missing_all})
        rows.append({"id": stem + ".conditional-scopes-unanswered", "status": status,
                     "vary": "conditional-scopes", "answer": None,
                     "acts": h.say(missing_all, P + "ss-benefits-scope.no-rrb-or-foreign-social-benefit", "yes", "l6b.ordinary")})
    return rows


def run(acts: list[dict[str, Any]], run_id: str, core: Any = None, *, reconfirm: bool = True) -> dict[str, Any]:
    h = harness()
    core = core or h.Core("v91", "v89", "v89")
    surface = core.surface()
    with h.loader_entries(core):
        finished = h._handover(h._finish(
            acts, package_path=core.package_path, package_version=core.version,
            release_path=core.release_path, release_version=core.release_version,
            note=run_id), surface=surface, reconfirm=reconfirm)
        with tempfile.TemporaryDirectory() as tmp:
            outcome = h.live_coordinate_run(
                h.WorkspaceCapability(Path(tmp) / "L"), repo_root=REPO,
                authoritative_acts=finished, workspace_revision=len(finished),
                run_scope={"jurisdiction": "us", "year": h.YEAR}, scope_user=h.ccr.USER,
                request={"schema": "run-request.v1"}, run_id=run_id,
                governance_pins=[], surface=surface, output_name="out.json")
            if outcome.refusal:
                return {"outcome": "refused", "reason": outcome.refusal.reason}
            model = json.loads(outcome.presentation_path.read_text())
            report = json.loads(outcome.output_path.read_text())
    return {"outcome": "success", "model": model, "report": report}


def view(result: dict[str, Any]) -> dict[str, Any]:
    if result["outcome"] != "success":
        return result
    report = result["report"]
    sections = []
    for section in result["model"].get("sections", []):
        field = section.get("field", {})
        if field.get("id") != P + "form1040.line-6b":
            continue
        resolved = section["resolved"]
        sections.append({"disposition": resolved.get("disposition"),
                         "value": resolved.get("value"),
                         "active_codes": resolved.get("activeCodes"),
                         "reasons": resolved.get("reasons", []),
                         "instructions": field.get("dispositions", {}).get(resolved.get("disposition"))})
    def compact(row: dict[str, Any]) -> dict[str, Any]:
        return {key: value for key, value in row.items() if key in (
            "artifact_id", "disposition", "code", "missing", "symbol", "guard_result")}
    return {"outcome": "success", "sections": sections,
            "worksheet_rows": [compact(r) for r in report.get("dispositions", []) if r.get("artifact_id") == RULE],
            "blocked": root_rows([compact(r) for r in report.get("dispositions", []) if r.get("disposition") == "blocked"])}


def worker(row: dict[str, Any]) -> dict[str, Any]:
    try:
        result = view(run(row["acts"], "demo.l6b.p0." + row["id"],
                          reconfirm=row["vary"] not in {"ssa-open", "no-benefits-open"}))
    except Exception as exc:
        # A source that fails actual admission is a reachability finding.
        message = re.sub(r"/(?:Users|private|tmp|var)/\S+", "<path>", str(exc))
        result = {"outcome": "error", "error": type(exc).__name__, "message": message[:600]}
    return {**{k: v for k, v in row.items() if k != "acts"}, **result}


def write_json(path: Path, body: Any) -> None:
    text = json.dumps(body, indent=2) + "\n"
    if re.search(r"/(Users|private|tmp|var)/", text):
        raise ValueError("public evidence contains a local path")
    path.write_text(text)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--smoke", action="store_true")
    parser.add_argument("--supplement", action="store_true", help="replace corrected open cases; add election and combined-absence cases")
    args = parser.parse_args()
    started = time.monotonic()
    rows = cases()
    if args.smoke:
        rows = [rows[0], next(r for r in rows if r["id"] == "single.original-incomplete")]
    if args.supplement:
        rows = [r for r in rows if r["vary"] in {"ssa-open", "no-benefits-open", P + "ssa1099.lump-sum-election", "all-scopes"}]
    from tests import evidence_loader
    owner = evidence_loader.current_owner()
    if owner:
        evidence_loader.release(owner)
    workers = max(1, (os.cpu_count() or 2) - 1)
    with ProcessPoolExecutor(max_workers=workers) as pool:
        results = []
        for result in pool.map(worker, rows):
            results.append(result)
            sections = result.get("sections", [{}])
            print(result["id"], [(r.get("disposition"), len(r.get("reasons", []))) for r in sections], flush=True)
    elapsed = round(time.monotonic()-started, 3)
    if args.supplement:
        previous = json.loads((HERE / "probe-output.json").read_text())
        merged = {row["id"]: row for row in previous["cases"]}
        merged.update({row["id"]: row for row in results})
        results = list(merged.values())
        elapsed += previous["wall_time_s"]
    write_json(HERE / ("smoke-output.json" if args.smoke else "probe-output.json"),
               {"core": "v91", "workers": workers, "wall_time_s": elapsed, "cases": results})


if __name__ == "__main__":
    main()
