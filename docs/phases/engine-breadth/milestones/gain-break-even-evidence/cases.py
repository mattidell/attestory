"""P0 cases for gains and break-even sales reach Schedule D (gain-break-even).

Evidence for docs/phases/engine-breadth/milestones/gain-break-even.md.
Charter: docs/reviews/gain-break-even/charter-p0.md.

Builds synthetic demo.* returns with one sale (a gain or an exact break-even)
on each sale path the engine accepts -- covered with basis reported (box A/D,
the control), covered code W (box A/D via Form 8949), noncovered (box B/E),
code B (box B/E with a corrected basis) and no Form 1099-B (box C/F) -- short
and long term, single and married filing jointly; plus mixed returns (a gain
on one path and a loss on another, netting to a gain) and two code W probes
of the ADR-0062 / ADR-0066 bound. Each runs once through the real
live_coordinate_run on published core v96 (registry v94, release v94); the
saved page is rendered with the real renderer and every page value is read
from the model embedded in that saved page. Hand values come from hand.py.

Run: python3 cases.py [--only KEY] [--workers N]
Writes runs.json beside this file. Nothing in packages/ or tests/ is edited.
The audit harness is loaded by path under a unique name.
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


h = _load("gbe_p0_audit_harness", REPO / "docs/phases/engine-breadth/milestones/sale-family-audit-evidence/audit_harness.py")

from packages.derivation.live import live_coordinate_run  # noqa: E402
from packages.derivation.live_session import _render_page  # noqa: E402

P = h.P
CORE = h.Core("v96", "v94", "v94")
STATUSES = ("single", "married_filing_jointly")
PATHS = ("covered", "w", "noncovered", "codeb", "no1099b")
TERMS = ("st", "lt")

# One sale per case. Each spec: proceeds (d), reported basis (e), and the extra
# fields that make column (h) the intended amount.
#   gain  -> column (h) = +20,000
#   even  -> column (h) = 0 (proceeds equal the basis the filer reports)
# On the code W family a gain or break-even row carries a box 1g amount of 0
# (ADR-0062 Decision 2 bars g > 0 when proceeds >= basis); "even" there is a
# loss of 500 fully disallowed (g = 500), so (h) = 0, and "even-plain" is
# proceeds equal to basis with g = 0. Code B's corrected basis is 1,000 below
# the reported basis, so (g) = +1,000 and (h) is the intended amount.
SPECS: dict[tuple[str, str], dict[str, Any]] = {
    ("covered", "gain"): {"proceeds": 25000.0, "basis": 5000.0},
    ("covered", "even"): {"proceeds": 8000.0, "basis": 8000.0},
    ("noncovered", "gain"): {"proceeds": 25000.0, "basis": 5000.0},
    ("noncovered", "even"): {"proceeds": 8000.0, "basis": 8000.0},
    ("no1099b", "gain"): {"proceeds": 25000.0, "basis": 5000.0},
    ("no1099b", "even"): {"proceeds": 8000.0, "basis": 8000.0},
    ("codeb", "gain"): {"proceeds": 25000.0, "basis": 6000.0, "corrected": 5000.0},
    ("codeb", "even"): {"proceeds": 8000.0, "basis": 9000.0, "corrected": 8000.0},
    ("w", "gain"): {"proceeds": 25000.0, "basis": 5000.0, "wash": 0.0},
    ("w", "even"): {"proceeds": 1000.0, "basis": 1500.0, "wash": 500.0},
    ("w", "even-plain"): {"proceeds": 8000.0, "basis": 8000.0, "wash": 0.0},
    # ADR-0062 Decision 2 (mechanism ADR-0066) probes: g > 0 on a gain, and on d == e.
    ("w", "probe-gain"): {"proceeds": 25000.0, "basis": 5000.0, "wash": 500.0},
    ("w", "probe-even"): {"proceeds": 8000.0, "basis": 8000.0, "wash": 500.0},
}

# Mixed returns: (path, term, spec) per sale; each nets to a gain.
MIXED: dict[str, list[tuple[str, str, dict[str, Any]]]] = {
    # long-term gain on a noncovered sale, short-term loss on a no-Form-1099-B sale.
    "lt-gain": [("noncovered", "lt", {"proceeds": 25000.0, "basis": 5000.0}),
                ("no1099b", "st", {"proceeds": 1000.0, "basis": 4000.0})],
    # short-term gain on a code B sale, long-term loss on a code W sale (500 of 3,000 disallowed).
    "st-gain": [("codeb", "st", {"proceeds": 25000.0, "basis": 6000.0, "corrected": 5000.0}),
                ("w", "lt", {"proceeds": 1000.0, "basis": 4000.0, "wash": 500.0})],
    # long-term break-even (covered) beside a long-term gain on Form 8949 box F and a short-term loss (box A).
    "three": [("covered", "lt", {"proceeds": 8000.0, "basis": 8000.0}),
              ("no1099b", "lt", {"proceeds": 12000.0, "basis": 2000.0}),
              ("covered", "st", {"proceeds": 2000.0, "basis": 4500.0})],
}


def column_h(path: str, spec: dict[str, Any]) -> float:
    basis = spec.get("corrected", spec["basis"])
    return spec["proceeds"] - basis + spec.get("wash", 0.0)


def case_sales(key: str) -> list[tuple[str, str, dict[str, Any]]]:
    parts = key.split("/")
    if parts[0] == "mixed":
        return MIXED[parts[1]]
    path, term, shape, _status = parts
    return [(path, term, SPECS[(path, shape)])]


def keys() -> list[str]:
    out = []
    for path in PATHS:
        for term in TERMS:
            for shape in ("gain", "even") if path != "w" else ("gain", "even", "even-plain", "probe-gain", "probe-even"):
                for status in STATUSES:
                    if shape.startswith("probe") and status != "single":
                        continue
                    out.append(f"{path}/{term}/{shape}/{status}")
    out += [f"mixed/{name}/{status}" for name in MIXED for status in STATUSES]
    return out


def build(key: str) -> h.Acts:
    status = key.split("/")[-1]
    sales = case_sales(key)
    acts = h.opened()
    kinds: set[str] = set()
    for i, (path, term, spec) in enumerate(sales):
        acts = h.sale(acts, path, term, proceeds=spec["proceeds"], basis=spec["basis"],
                      wash=spec.get("wash", 0.0), corrected=spec.get("corrected"), tag=f"gbe-{i}-{path}-{term}")
        kinds.add(path)
    loss = any(column_h(p, s) < 0 for p, _t, s in sales)
    answers = h.honest(kinds, loss=loss)
    answers.update(h.honest_exception1(acts))
    answers.update({"lines_18_19": "yes", "no_other_sd": "yes", "no_da_qof": "yes"})
    acts = h.answer(acts, **answers)
    acts = h.say(acts, P + "f1099b.no-sale-box4-present", "no", "no-sale-box4")
    acts = statement_answers(acts)
    acts = h.say(acts, P + "filing-status", status, "gbe-status")
    for fact in ("taxpayer-over-65", "taxpayer-blind") + (
            ("spouse-over-65", "spouse-blind") if status.startswith("married") else ()):
        acts = h.say(acts, P + fact, False, "gbe-" + fact)
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
            h._add(acts, "assertion", {"finding": h._attested(f"demo.gbe.{slug}.{statement}", fact_id, "no")})
    return h.renumber(acts)


def num(value: Any) -> Any:
    if isinstance(value, str):
        try:
            value = float(value)
        except ValueError:
            return value
    if isinstance(value, float) and value.is_integer():
        return int(value)
    return value


PUBLISHED = ("schedule-d.", "qdcg-worksheet.", "capital-gains.selected-preferential-base",
             "tax.total-tax", "form1040.line-7a", "form1040.line-15", "form1040.line-16", "sale-count")
PAGE = ("schedule-d.", "form8949", "f8949", "form1040.line-7a", "form1040.line-15", "form1040.line-16")


def observe(key: str) -> dict[str, Any]:
    acts = build(key)
    run_id = "demo.gbe.p0." + key.replace("/", ".")
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
    for section in saved.get("sections") or []:
        field = section.get("field") or {}
        fid = str(field.get("id") or "").removeprefix(P)
        resolved = section.get("resolved") or {}
        sentences = [str(r.get("sentence") or "") for r in resolved.get("reasons") or [] if isinstance(r, dict)]
        questions += [h.scrub(s)[:200] for s in sentences if s.strip().endswith("?") and s not in questions]
        if any(t in fid for t in PAGE):
            lines[fid] = {"disposition": resolved.get("disposition"), "value": num(resolved.get("value"))}
    published: dict[str, Any] = {}
    parts: dict[str, Any] = {}
    for p in outcome.publications or ():
        symbol = str(p.finding.get("symbol")).removeprefix(P)
        value = p.finding.get("value")
        if symbol in ("form8949.disposition", "schedule-d.disposition") and isinstance(value, dict):
            # The attachment's own part totals (Form 8949 columns d, e, g per box) and its requirement.
            parts[symbol.split(".")[0]] = {"required": value.get("required"),
                                           "parts": {i["part_id"]: num(i["part_sum"]) for i in value.get("itemizations") or []
                                                     if num(i["part_sum"]) != 0},
                                           "named_obligations": value.get("named_obligations")}
        elif any(symbol.startswith(t) for t in PUBLISHED) or (
                symbol.startswith(("f1099b.", "f8949.")) and symbol.endswith(("-subtotal", "-count")) and num(value) != 0):
            published[symbol] = num(value)
    blocked = sorted({(str(r.get("artifact_id")).removeprefix(P + "rule."), str(r.get("code")))
                      for r in report.get("dispositions") or [] if r.get("disposition") == "blocked"})
    attachments = {}
    for a in saved.get("attachments") or []:
        res = a.get("resolved") or {}
        attachments[str(a.get("id")).removeprefix(P + "rule.attachment.")] = res.get("disposition")
    return {
        "stop": report.get("stop_reason"),
        "lines": lines,
        "published": published,
        "attachment_parts": parts,
        "attachments": attachments,
        "blocked_rules": [list(b) for b in blocked],
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
            "wall_time_s": round(time.monotonic() - started, 1)}
    runs = {k: found[k] for k in todo}
    text = json.dumps(body, sort_keys=True)[:-1] + ', "runs": {\n' + ",\n".join(
        json.dumps(k) + ": " + json.dumps(v, sort_keys=True) for k, v in runs.items()) + "\n}}\n"
    json.loads(text)
    Path(args.out).write_text(text, encoding="utf-8")
    print(json.dumps({"runs": len(found), "wall_time_s": body["wall_time_s"]}))


if __name__ == "__main__":
    main()
