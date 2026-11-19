"""P0 cases for box C and F losses are limited and carried (cf-loss-limit).

Evidence for docs/phases/engine-breadth/milestones/cf-loss-limit.md.
Charter: docs/reviews/cf-loss-limit/charter-p0.md.

Builds synthetic demo.* returns whose Schedule D line 16 is a net loss from
Form 8949 box C sales, box F sales, or both, and the same amounts through
box A/D (covered sales, lines 1a/8a) as a control, under every filing status
the capital-loss-limit parameter names. Each runs once through the real
live_coordinate_run on published core v96 (registry v94, release v94); the
saved page is rendered with the real renderer and every value is read from
the model embedded in that saved page. Hand values come from hand.py.

Run: python3 cases.py [--only KEY] [--workers N]
Writes runs.json (compact) beside this file. Nothing in packages/ or tests/
is edited. The audit harness is loaded by path under a unique name.
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
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


h = _load("cfl_p0_audit_harness", REPO / "docs/phases/engine-breadth/milestones/sale-family-audit-evidence/audit_harness.py")
hand = _load("cfl_p0_hand", HERE / "hand.py")

from packages.derivation.live import live_coordinate_run  # noqa: E402
from packages.derivation.live_session import _render_page  # noqa: E402

P = h.P
CORE = h.Core("v96", "v94", "v94")
STATUSES = ("single", "married_filing_jointly", "married_filing_separately", "head_of_household",
            "qualifying_surviving_spouse")
LIMIT = {"married_filing_separately": 1500}
WATCH = ("schedule-d.line-1a", "schedule-d.line-3", "schedule-d.line-6", "schedule-d.line-7", "schedule-d.line-8a",
         "schedule-d.line-10", "schedule-d.line-14", "schedule-d.line-15", "schedule-d.line-16", "schedule-d.line-21",
         "form1040.line-7a", "form1040.line-9", "form1040.line-11a", "form1040.line-15")
CARRY = (P + "capital-loss-carryover.short-term", P + "capital-loss-carryover.long-term")


def amounts(status: str) -> dict[str, int]:
    """Net loss amounts below, at and above the status limit."""
    limit = LIMIT.get(status, 3000)
    return {"below": limit // 2, "at": limit, "above": limit + 2000}


# A shape is (short-term net, long-term net) as a function of the total loss.
SHAPES = {
    "st": lambda loss: (-loss, 0),
    "lt": lambda loss: (0, -loss),
    "both": lambda loss: (-(loss - loss // 2), -(loss // 2)),
}
ROUTES = {"cf": "no1099b", "ad": "covered"}


def build(route: str, shape: str, status: str, size: str) -> h.Acts:
    loss = amounts(status)[size]
    st, lt = SHAPES[shape](loss)
    kind = ROUTES[route]
    acts = h.opened()
    for term, net in (("st", st), ("lt", lt)):
        if net:
            # One sale per term: proceeds 1,000, basis 1,000 - net.
            acts = h.sale(acts, kind, term, proceeds=1000.0, basis=float(1000 - net),
                          tag=f"cfl-{route}-{term}")
    answers = h.honest({kind}, loss=True)
    answers.update(h.honest_exception1(acts))
    answers.update({"lines_18_19": "yes", "no_other_sd": "yes", "no_da_qof": "yes"})
    acts = h.answer(acts, **answers)
    acts = h.say(acts, P + "f1099b.no-sale-box4-present", "no", "no-sale-box4")
    if kind == "covered":
        acts = statement_answers(acts)
    acts = h.say(acts, P + "filing-status", status, "cfl-status")
    for fact in ("taxpayer-over-65", "taxpayer-blind") + (
            ("spouse-over-65", "spouse-blind") if status.startswith("married") else ()):
        acts = h.say(acts, P + fact, False, "cfl-" + fact)
    if status == "married_filing_separately":
        # The two separate-return answers the core asks of every MFS filer (not capital-loss questions).
        if P + "standard-deduction.spouse-separate-condition" not in h._adopted(acts):
            h._add(acts, "bundle-adoption", {"bundle": h._read("core_calculations.bundle.v4.json")})
        acts = h.say(acts, P + "mfs-lived-apart-all-year", "yes", "cfl-mfs-apart")
        acts = h.say(acts, P + "standard-deduction.spouse-separate-condition", False, "cfl-mfs-spouse")
    return h.renumber(acts)


def statement_answers(acts: h.Acts) -> h.Acts:
    """The box 4 and box 7 statement answers each recorded Form 1099-B statement needs (no, no)."""
    statements = list(dict.fromkeys(str(a["payload"]["entity"]["id"]) for a in acts
                                    if a.get("kind") == "entity-introduced"
                                    and a["payload"]["entity"].get("kind") == "tax.us.f1099b-statement"))
    if not statements:
        return acts
    h.adopt(acts, "f1099b-statement-boxes.bundle.json")
    for statement in statements:
        for slug in ("statement-box4-withholding-reported", "statement-box7-loss-not-allowed"):
            fact_id = h.fact_id_for(P + "f1099b." + slug, (("statement", statement), ("tax-year", h.YEAR)))
            h._add(acts, "assertion", {"finding": h._attested(f"demo.cfl.{slug}.{statement}", fact_id, "no")})
    return h.renumber(acts)


def keys() -> list[str]:
    return [f"{route}/{shape}/{status}/{size}" for route in ROUTES for shape in SHAPES
            for status in STATUSES for size in ("below", "at", "above")]


def num(value: Any) -> Any:
    if isinstance(value, str):
        try:
            value = float(value)
        except ValueError:
            return value
    if isinstance(value, float) and value.is_integer():
        return int(value)
    return value


def observe(key: str) -> dict[str, Any]:
    route, shape, status, size = key.split("/")
    acts = build(route, shape, status, size)
    run_id = "demo.cfl.p0." + key.replace("/", ".")
    surface = CORE.surface()
    finished = h._handover(h._finish(copy.deepcopy(acts), package_path=CORE.package_path,
                                     package_version=CORE.version, release_path=CORE.release_path,
                                     release_version=CORE.release_version, note=run_id),
                           surface=surface, reconfirm=True)
    with TemporaryDirectory() as tmp:
        capability = h.WorkspaceCapability(Path(tmp) / "L")
        outcome = live_coordinate_run(capability, repo_root=REPO, authoritative_acts=finished,
                                      workspace_revision=len(finished), run_scope={"jurisdiction": "us", "year": h.YEAR},
                                      scope_user=h.ccr.USER, request={"schema": "run-request.v1"}, run_id=run_id,
                                      governance_pins=[], surface=surface, output_name="out.json")
        if outcome.refusal is not None:
            return {"refusal": outcome.refusal.reason, "detail": h.scrub(str(outcome.refusal.detail))[:300]}
        report = json.loads(outcome.output_path.read_text(encoding="utf-8"))
        model = json.loads(outcome.presentation_path.read_text(encoding="utf-8"))
        page = Path(tmp) / "page.html"
        page.write_bytes(_render_page(REPO, capability, outcome.presentation_path))
        text = page.read_text(encoding="utf-8")
        marker = "const MODEL = Object.freeze("
        saved, _ = json.JSONDecoder().raw_decode(text, text.index(marker) + len(marker))
        assert saved == model, "saved page model differs from the presentation model"
    lines: dict[str, Any] = {}
    questions: list[str] = []
    carry_text: list[str] = []
    for section in saved.get("sections") or []:
        field = section.get("field") or {}
        fid = str(field.get("id") or "").removeprefix(P)
        resolved = section.get("resolved") or {}
        sentences = [str(r.get("sentence") or "") for r in resolved.get("reasons") or [] if isinstance(r, dict)]
        questions += [s for s in sentences if s.strip().endswith("?") and s not in questions]
        if fid in WATCH:
            lines[fid] = {"disposition": resolved.get("disposition"), "value": num(resolved.get("value"))}
        # Where a filer could see a carryover: a field bound to a carryover symbol,
        # or any shown sentence about carrying a loss or about 2026.
        if "carryover" in str(field.get("binds_symbol") or ""):
            carry_text.append({"field": fid, "binds": str(field.get("binds_symbol")).removeprefix(P),
                               "value": num(resolved.get("value"))})
        for text in sentences + [str(field.get("label") or "")]:
            if "2026" in text or "carr" in text.lower():
                carry_text.append({"field": fid, "text": text})
    publications = {str(p.finding.get("symbol")): num(p.finding.get("value")) for p in outcome.publications or ()}
    blocked = sorted({str(r.get("artifact_id")).removeprefix(P + "rule.") for r in report.get("dispositions") or []
                      if r.get("disposition") == "blocked"})
    return {
        "stop": report.get("stop_reason"),
        "lines": lines,
        "carryover_published": {s.removeprefix(P): publications.get(s) for s in CARRY},
        # Every published symbol that names a carryover or 2026 (the 2025 -> 2026 search).
        "carry_or_2026_symbols": sorted(s.removeprefix(P) for s in publications
                                        if "carry" in s.lower() or "2026" in s),
        "page_carryover_mentions": carry_text,
        "page_attachments": {str(a.get("id")).removeprefix(P + "rule.attachment."): (a.get("resolved") or {}).get("disposition")
                             for a in saved.get("attachments") or []},
        "blocked_rules": blocked,
        "questions": questions[:10],
    }


def worker(shard: list[str]) -> list[tuple[str, dict[str, Any]]]:
    out = []
    for key in shard:
        try:
            out.append((key, observe(key)))
        except Exception as exc:  # noqa: BLE001 - a rejected list is a result
            out.append((key, {"error": type(exc).__name__, "message": h.scrub(str(exc))[:400]}))
    return out


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--only", action="append")
    parser.add_argument("--workers", type=int, default=max(1, (os.cpu_count() or 2) - 1))
    parser.add_argument("--out", default=str(HERE / "runs.json"))
    args = parser.parse_args()
    todo = args.only or keys()
    started = time.monotonic()
    workers = min(args.workers, len(todo))
    if workers <= 1:
        found = dict(worker(todo))
    else:
        with multiprocessing.get_context("spawn").Pool(workers) as pool:
            found = dict(pair for part in pool.map(worker, [todo[i::workers] for i in range(workers)]) for pair in part)
    body = {"core": {"package": CORE.version, "registry": CORE.registry, "release": CORE.release_version},
            "wall_time_s": round(time.monotonic() - started, 1), "runs": {k: found[k] for k in todo}}
    runs = body.pop("runs")
    text = json.dumps(body, sort_keys=True)[:-1] + ', "runs": {\n' + ",\n".join(
        json.dumps(k) + ": " + json.dumps(v, sort_keys=True) for k, v in runs.items()) + "\n}}\n"
    json.loads(text)
    Path(args.out).write_text(text, encoding="utf-8")
    print(json.dumps({"runs": len(found), "wall_time_s": body["wall_time_s"]}))


if __name__ == "__main__":
    main()
