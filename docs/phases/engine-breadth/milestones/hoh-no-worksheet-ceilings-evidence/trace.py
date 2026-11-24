"""Live trace of worksheet lines 6 and 13 on published v102 or a scratch core.

Synthetic demo.* returns, one head of household and one qualifying surviving
spouse, each with the status-test answer yes, no and unanswered, plus a
single control and a married-filing-jointly control. Each return is the
head-of-household probe's wages-only return (50,000 wages, 4,500 withheld,
no qualified dividends and no sale) run through live_coordinate_run.

Run: python3 trace.py --core v102 --out trace-v102.json
     python3 trace.py --core-json <scratch-core.json> --out trace-v103.json

The sibling probe and the audit harness are loaded by path under unique names.
"""
from __future__ import annotations

import argparse
import copy
import importlib.util
import json
import multiprocessing
import os
import sys
import time
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
PROBE_PATH = REPO / "docs/phases/engine-breadth/milestones/hoh-qualifying-person-evidence/probe.py"
P = "tax.us.2025."
CASES = (
    ("hoh/none", "yes"),
    ("hoh/none", "no"),
    ("hoh/none", "none"),
    ("qss/none", "yes"),
    ("qss/none", "no"),
    ("qss/none", "none"),
    ("single/none", "none"),
    ("mfj/none", "none"),
    ("mfs/none", "none"),
)
WATCH_SYMBOLS = tuple(
    [f"qdcg-worksheet.line-{number}" for number in (4, 5, *range(6, 26))]
    + ["dependents-worksheet.line3", "income.taxable-income", "deductions.line-12e"]
)
PAGE_FIELDS = (
    "form1040.line-12e", "form1040.line-15", "form1040.line-16",
)
CEILING_DIGITS = ("48350", "64750", "96700", "300000", "533400", "566700", "600050")
QUESTION_MARKS = (
    "cannot file as head of household",
    "cannot file as a qualifying surviving spouse",
)


def _load(name: str, path: Path) -> Any:
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def _probe() -> Any:
    return _load("hnw_p0_hoh_probe", PROBE_PATH)


def _core(probe: Any, spec: dict[str, Any]) -> Any:
    harness = probe.h
    if spec.get("core_json"):
        body = json.loads(Path(spec["core_json"]).read_text(encoding="utf-8"))
        return harness.Core(body["version"], body["registry"], body["release_version"], content=Path(body["content"]),
                            releases=Path(body["releases"]), loader_from=body.get("loader_from"))
    number = int(spec["version"][1:])
    return harness.Core(spec["version"], f"v{number - 2}", f"v{number - 2}")


def _num(value: Any) -> Any:
    if isinstance(value, str):
        try:
            value = float(value)
        except ValueError:
            return value
    if isinstance(value, float) and value.is_integer():
        return int(value)
    return value


def _sentences(resolved: dict[str, Any], scrub: Any) -> list[str]:
    said = []
    for name in ("questions", "reasons", "blocked_reasons"):
        for item in resolved.get(name) or []:
            text = str(item.get("sentence") or item.get("text") or "") if isinstance(item, dict) else str(item)
            if text.strip():
                said.append(scrub(text)[:500])
    return said


def _html_hits(text: str) -> dict[str, int]:
    folded = text.casefold()
    hits = {}
    for digits in CEILING_DIGITS:
        shown = f"{int(digits):,}"
        hits[shown] = text.count(shown) + text.count(digits)
    for mark in QUESTION_MARKS:
        hits[mark] = folded.count(mark)
    return {key: count for key, count in hits.items() if count}


def observe(probe: Any, core: Any, key: str, answer: str) -> dict[str, Any]:
    from packages.derivation.live import live_coordinate_run  # noqa: E402
    from packages.derivation.live_session import _render_page  # noqa: E402
    from tempfile import TemporaryDirectory

    harness = probe.h
    probe.STATUS["mfs"] = "married_filing_separately"
    acts = probe.build(key, core.content, answer)
    run_id = "demo.hnw.p0." + key.replace("/", ".") + "." + answer
    surface = core.surface()
    with harness.loader_entries(core):
        finished = harness._handover(
            harness._finish(copy.deepcopy(acts), package_path=core.package_path, package_version=core.version,
                            release_path=core.release_path, release_version=core.release_version, note=run_id),
            surface=surface, reconfirm=True)
        with TemporaryDirectory() as tmp:
            capability = harness.WorkspaceCapability(Path(tmp) / "L")
            outcome = live_coordinate_run(
                capability, repo_root=REPO, authoritative_acts=finished, workspace_revision=len(finished),
                run_scope={"jurisdiction": "us", "year": harness.YEAR}, scope_user=harness.ccr.USER,
                request={"schema": "run-request.v1"}, run_id=run_id, governance_pins=[],
                surface=surface, output_name="out.json")
            if outcome.refusal is not None:
                return {"refusal": outcome.refusal.reason, "detail": harness.scrub(str(outcome.refusal.detail))[:300]}
            report = json.loads(outcome.output_path.read_text(encoding="utf-8"))
            model = json.loads(outcome.presentation_path.read_text(encoding="utf-8"))
            page = Path(tmp) / "page.html"
            page.write_bytes(_render_page(REPO, capability, outcome.presentation_path))
            html = page.read_text(encoding="utf-8")
    pubs = {}
    for publication in outcome.publications or ():
        symbol = str(publication.finding.get("symbol") or "")
        pubs[symbol] = _num(publication.finding.get("value"))
    rules: dict[str, Any] = {}
    for row in report.get("dispositions") or []:
        artifact = str(row.get("artifact_id") or "")
        if "qdcg-worksheet" not in artifact and not artifact.endswith((
            "rule.dependents-worksheet-line-3", "rule.form1040-line15", "rule.form1040-line16", "rule.form1040-line12e",
        )):
            continue
        name = artifact.removeprefix(P + "rule.")
        item = {"disposition": row.get("disposition"), "code": row.get("code")}
        missing = row.get("missing")
        if missing:
            item["missing"] = [str(part).removeprefix(P) for part in missing][:8]
        symbol = str(row.get("symbol") or "")
        if symbol in pubs:
            item["value"] = pubs[symbol]
        rules[name] = item
    graph = {}
    nodes = (model.get("explanationGraph") or {}).get("nodes") or {}
    if isinstance(nodes, dict):
        for node in nodes.values():
            if not isinstance(node, dict):
                continue
            symbol = str(node.get("symbol") or "")
            short = symbol.removeprefix(P)
            if short in WATCH_SYMBOLS or short in PAGE_FIELDS:
                graph[short] = {"kind": node.get("kind"), "value": _num(node.get("value")), "version": node.get("version")}
    page_lines: dict[str, Any] = {}
    question_lines: list[str] = []
    for section in model.get("sections") or []:
        field = section.get("field") or {}
        fid = str(field.get("id") or "").removeprefix(P)
        resolved = section.get("resolved") or {}
        said = _sentences(resolved, harness.scrub)
        if fid in PAGE_FIELDS or any(mark in " ".join(said).casefold() for mark in QUESTION_MARKS):
            row = {"disposition": resolved.get("disposition"), "value": _num(resolved.get("value"))}
            if said:
                row["said"] = said[:4]
            if fid:
                page_lines[fid] = row
            for sentence in said:
                if any(mark in sentence.casefold() for mark in QUESTION_MARKS) and sentence not in question_lines:
                    question_lines.append(sentence)
    symbols = {name: pubs.get(P + name, pubs.get(name)) for name in WATCH_SYMBOLS}
    return {
        "stop": report.get("stop_reason"),
        "symbols": {key: value for key, value in symbols.items() if value is not None},
        "rules": rules,
        "graph": graph,
        "page": page_lines,
        "question_on_page": question_lines[:4],
        "html_hits": _html_hits(html),
    }


def _worker(task: tuple[dict[str, Any], str, str]) -> tuple[str, dict[str, Any]]:
    spec, key, answer = task
    probe = _probe()
    if str(REPO) not in sys.path:
        sys.path.insert(0, str(REPO))
    core = _core(probe, spec)
    label = f"{key}/{answer}"
    try:
        return label, observe(probe, core, key, answer)
    except Exception as exc:  # a rejected list is a result
        return label, {"error": type(exc).__name__, "message": probe.h.scrub(str(exc))[:500]}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--core", default="v102")
    parser.add_argument("--core-json")
    parser.add_argument("--only", action="append")
    parser.add_argument("--workers", type=int, default=max(1, min(8, (os.cpu_count() or 2) - 1)))
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    spec = {"version": args.core, "core_json": args.core_json}
    wanted = set(args.only) if args.only else None
    cases = [(key, answer) for key, answer in CASES if wanted is None or f"{key}/{answer}" in wanted or key in wanted]
    started = time.monotonic()
    tasks = [(spec, key, answer) for key, answer in cases]
    workers = min(args.workers, len(tasks))
    if workers <= 1:
        found = dict(_worker(task) for task in tasks)
    else:
        with multiprocessing.get_context("spawn").Pool(workers) as pool:
            found = dict(pool.map(_worker, tasks))
    order = [f"{key}/{answer}" for key, answer in cases]
    body = {
        "core": spec["version"] if not args.core_json else "scratch",
        "wall_time_s": round(time.monotonic() - started, 1),
        "return": "demo wages 50000, withholding 4500, standard deduction, no qualified dividends and no sale",
        "runs": {label: found[label] for label in order},
    }
    if args.core_json:
        meta = json.loads(Path(args.core_json).read_text(encoding="utf-8"))
        body["core"] = {"package": meta["version"], "registry": meta["registry"], "release": meta["release_version"],
                        "loader_from": meta.get("loader_from")}
    text = json.dumps(body, indent=1) + "\n"
    for needle in ("/Users/", "/private/", "/tmp/", "/var/"):
        if needle in text:
            raise SystemExit(f"trace output contains {needle}")
    args.out.write_text(text, encoding="utf-8")
    brief = {}
    for label, row in body["runs"].items():
        if "error" in row or "refusal" in row:
            brief[label] = row
            continue
        brief[label] = {
            "stop": row.get("stop"),
            "line6": row["rules"].get("qdcg-worksheet.line-6"),
            "line13": row["rules"].get("qdcg-worksheet.line-13"),
            "line7": row["rules"].get("qdcg-worksheet.line-7"),
            "line14": row["rules"].get("qdcg-worksheet.line-14"),
            "line3": row["rules"].get("dependents-worksheet-line-3"),
            "line16": row["rules"].get("form1040-line16"),
            "html_hits": row.get("html_hits"),
            "question_on_page": bool(row.get("question_on_page")),
        }
    print(json.dumps({"wall_time_s": body["wall_time_s"], "runs": brief}, indent=1)[:20000])


if __name__ == "__main__":
    main()
