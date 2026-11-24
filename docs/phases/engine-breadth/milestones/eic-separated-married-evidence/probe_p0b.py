"""Trace: Step 3 question 3 on published core v103.

Re-runs the 21 P0 cases and six more. The 21 still carry a separated-spouse
answer and no new answer. ``q3-no`` answers the new question no and records
no separated-spouse answer. ``q3-yes`` answers yes and leaves the
separated-spouse answer off the return. ``q3-yes-no`` answers yes and then no.

A question counts as asked when the answer publication pins that fact.
Supplied answers stay on the return either way.

Run: python3 probe_p0b.py --core v103 [--only KEY] [--out FILE]
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
from tempfile import TemporaryDirectory
from typing import Any

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))


def _load(name: str, path: Path) -> Any:
    if name in sys.modules:
        return sys.modules[name]
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


p0 = _load("esm_p0b_p0_probe", HERE / "probe.py")
hand = _load("esm_p0b_hand", HERE / "hand.py")
h = p0.h
base = p0.base

from packages.derivation.live import live_coordinate_run  # noqa: E402

P = h.P
MARRIED = P + "eic.married-taxpayer"
EXTRA = (
    "q3-no/ssn", "q3-no/nossn", "q3-yes/ssn", "q3-yes/nossn", "q3-yes-no/ssn", "q3-yes-no/nossn",
    "recorded-no/ssn/unmarried", "recorded-no/nossn/unmarried",
    "recorded-no/ssn/married", "recorded-no/nossn/married",
)
KEYS = list(p0.KEYS) + list(EXTRA)
ASK = dict(p0.ASK)
ASK["married-taxpayer"] = MARRIED
ANSWER_SYMBOL = dict(p0.ANSWER_SYMBOL)
ANSWER_SYMBOL["married-taxpayer"] = "eic.answer.married-taxpayer"
SYMBOLS = p0.SYMBOLS + (
    "eic.married-taxpayer-recorded",
    "eic.married-taxpayer-from-separated",
    "eic.answer.married-taxpayer",
)


def build(key: str, content: Path = h.CONTENT) -> h.Acts:
    if key.startswith("recorded-no/"):
        _, kids, which = key.split("/")
        base_key = f"hoh-unmarried/{kids}/no" if which == "unmarried" else f"hoh-married/{kids}/no"
        value = "no" if which == "unmarried" else "yes"
        return h.renumber(h.say(p0.build(base_key, content), MARRIED, value, "esm-married", content))
    if key not in EXTRA:
        return p0.build(key, content)
    kind, kids = key.split("/")
    base_key = f"hoh-unmarried/{kids}/no" if kind == "q3-no" else f"hoh-married/{kids}/no"
    acts = h.strip(p0.build(base_key, content), p0.SEP)
    if kind == "q3-yes-no":
        acts = h.say(acts, p0.SEP, "no", "esm-separated", content)
    value = "no" if kind == "q3-no" else "yes"
    return h.renumber(h.say(acts, MARRIED, value, "esm-married", content))


def observe(core: Any, key: str) -> dict[str, Any]:
    return run(core, build(key, core.content), key)


def run(core: Any, acts: h.Acts, key: str) -> dict[str, Any]:
    asserted = {label: p0._assertion_ids(acts, fact) for label, fact in ASK.items()}
    run_id = "demo.esm.p0b." + key.replace("/", ".")
    surface = core.surface()
    with h.loader_entries(core):
        finished = h._handover(h._finish(
            copy.deepcopy(acts), package_path=core.package_path, package_version=core.version,
            release_path=core.release_path, release_version=core.release_version, note=run_id,
        ), surface=surface, reconfirm=True)
        with TemporaryDirectory() as tmp:
            capability = h.WorkspaceCapability(Path(tmp) / "L")
            outcome = live_coordinate_run(
                capability, repo_root=REPO, authoritative_acts=finished, workspace_revision=len(finished),
                run_scope={"jurisdiction": "us", "year": h.YEAR}, scope_user=h.ccr.USER,
                request={"schema": "run-request.v1"}, run_id=run_id, governance_pins=[],
                surface=surface, output_name="out.json",
            )
            if outcome.refusal is not None:
                return {"refusal": outcome.refusal.reason, "detail": h.scrub(str(outcome.refusal.detail))[:300]}
            report = json.loads(outcome.output_path.read_text(encoding="utf-8"))
            model = json.loads(outcome.presentation_path.read_text(encoding="utf-8"))
    lines: dict[str, Any] = {}
    for section in model.get("sections") or []:
        field = section.get("field") or {}
        fid = str(field.get("id") or "").removeprefix(P)
        if fid not in p0.WATCH:
            continue
        resolved = section.get("resolved") or {}
        lines[fid] = {"disposition": resolved.get("disposition"), "value": base.num(resolved.get("value"))}
    by_symbol: dict[str, list[dict[str, Any]]] = {}
    for pub in outcome.publications or ():
        by_symbol.setdefault(str(pub.finding.get("symbol")), []).append(pub.finding)

    def rows_for(name: str) -> list[dict[str, Any]]:
        exact = by_symbol.get(P + name) or []
        prefixed = [row for symbol, rows in by_symbol.items() if symbol.startswith(P + name + "|") for row in rows]
        return exact + prefixed

    symbols = {}
    for name in SYMBOLS:
        rows = rows_for(name)
        symbols[name] = base.num(rows[0].get("value")) if len(rows) == 1 else ([base.num(row.get("value")) for row in rows] or None)
    asked = {}
    for label in ASK:
        rows = rows_for(ANSWER_SYMBOL[label])
        ids = asserted[label]
        asked[label] = bool(rows) and any(
            str(pin.get("id") or "") in ids for row in rows for pin in row.get("pins") or []
        )
    blocked = sorted({
        str(row.get("artifact_id")).removeprefix(P + "rule.") + ":" + str(row.get("code"))
        for row in report.get("dispositions") or [] if row.get("disposition") == "blocked"
    })
    missing = sorted({
        str(item)
        for row in report.get("dispositions") or [] if row.get("disposition") == "blocked"
        for item in (row.get("missing") or [])
    })
    credit = lines.get("form1040.line-27a", {})
    return {
        "stop": report.get("stop_reason"),
        "credit": credit.get("value"),
        "credit_disposition": credit.get("disposition"),
        "symbols": symbols,
        "asked": asked,
        "blocked_rules": blocked,
        "blocked_missing": missing,
    }


def _worker(args: tuple[Any, list[str]]) -> list[tuple[str, dict[str, Any]]]:
    core, todo = args
    out = []
    for key in todo:
        try:
            out.append((key, observe(core, key)))
        except Exception as exc:  # noqa: BLE001 - a rejected list is a result
            out.append((key, {"error": type(exc).__name__, "message": h.scrub(str(exc))[:500]}))
    return out


def _attach(found: dict[str, dict[str, Any]]) -> None:
    for key, row in found.items():
        source = hand.expect(key)
        row["source"] = source
        if "credit" not in row:
            continue
        blocked = bool(row.get("blocked_rules"))
        row["credit_equals_source"] = row["credit"] == source["credit"] and blocked is source["blocked"]
        row["asked_matches_source"] = (
            row.get("asked", {}).get("separated-spouse") is source["ask_separated"]
            and row.get("asked", {}).get("married-taxpayer") is source["ask_married"]
            and row.get("asked", {}).get("not-married") is source["ask_not_married"]
        )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--core", default="v102")
    parser.add_argument("--core-json")
    parser.add_argument("--only", action="append")
    parser.add_argument("--workers", type=int, default=max(1, min(6, (os.cpu_count() or 2) - 1)))
    parser.add_argument("--out")
    args = parser.parse_args()
    core = base.core_from(args)
    todo = args.only or list(KEYS)
    unknown = [key for key in todo if key not in KEYS]
    if unknown:
        raise SystemExit(f"unknown keys: {unknown}")
    started = time.monotonic()
    workers = min(args.workers, len(todo))
    if workers <= 1:
        found = dict(_worker((core, todo)))
    else:
        with multiprocessing.get_context("spawn").Pool(workers) as pool:
            parts = pool.map(_worker, [(core, todo[i::workers]) for i in range(workers)])
        found = dict(pair for part in parts for pair in part)
    _attach(found)
    body = {
        "core": {"package": core.version, "registry": core.registry, "release": core.release_version},
        "wages": hand.WAGES,
        "cases": len(todo),
        "wall_time_s": round(time.monotonic() - started, 1),
        "credit_equals_source": sum(1 for row in found.values() if row.get("credit_equals_source")),
        "asked_matches_source": sum(1 for row in found.values() if row.get("asked_matches_source")),
        "errors": sum(1 for row in found.values() if "error" in row or "refusal" in row),
        "runs": {key: found[key] for key in todo},
    }
    text = json.dumps(body, indent=1, sort_keys=True) + "\n"
    if args.out:
        Path(args.out).write_text(text, encoding="utf-8")
    brief = {
        key: {
            "credit": row.get("credit"),
            "disposition": row.get("credit_disposition"),
            "source": (row.get("source") or {}).get("credit"),
            "instruction": (row.get("source") or {}).get("instruction"),
            "recorded": (row.get("symbols") or {}).get("eic.married-taxpayer-recorded"),
            "married_answer": (row.get("symbols") or {}).get("eic.answer.married-taxpayer"),
            "separated_answer": (row.get("symbols") or {}).get("eic.answer.separated-spouse"),
            "gate": (row.get("symbols") or {}).get("eic.gate-result"),
            "line6": (row.get("symbols") or {}).get("eic.worksheet-a.line-6"),
            "asked": row.get("asked"),
            "match": row.get("credit_equals_source"),
            "asked_match": row.get("asked_matches_source"),
            "error": row.get("error") or row.get("refusal"),
            "blocked": row.get("blocked_rules"),
            "missing": row.get("blocked_missing"),
        }
        for key, row in body["runs"].items()
    }
    print(json.dumps({
        "core": body["core"], "wall_time_s": body["wall_time_s"],
        "credit_equals_source": body["credit_equals_source"],
        "asked_matches_source": body["asked_matches_source"],
        "errors": body["errors"], "runs": brief,
    }, indent=1))


if __name__ == "__main__":
    main()
