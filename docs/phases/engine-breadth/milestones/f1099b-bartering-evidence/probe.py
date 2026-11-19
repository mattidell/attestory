"""P0 probe for a Form 1099-B bartering amount is not lost (f1099b-bartering).

Evidence for docs/phases/engine-breadth/milestones/f1099b-bartering.md.
Charter: docs/reviews/f1099b-bartering/charter-p0.md.

Builds synthetic demo.* returns that stand for a filer holding a 2025 Form
1099-B with an amount in box 13 (bartering) and runs each once through the
real live_coordinate_run, then renders the saved page with the real renderer
and reads every value from the model embedded in that page.

Core v96 has no fact type for a box 13 amount, so "box 13" is the Form 1099-B
statement and broker entities recorded with nothing about box 13, and the
filer's answers to the questions the core does ask. Cases:

  alone/as-asked      statement with only box 13; every Schedule 1 scope
                      question answered as the base return answers it (no)
  alone/business      same, the lines 2a-6 question answered yes (line 3
                      business income: Schedule C, Pub. 525)
  alone/business-all  same, all five facts that share that question answered yes
  alone/other-income  same, the lines 8a-8z question answered yes (Schedule 1
                      line 8z, bartering not from a business)
  alone/unanswered    same, the five facts that share the lines 2a-6 question
                      left unanswered (the page asks it)
  sale/as-asked       box 13 beside an ordinary covered short-term gain sale on
                      the same statement (box 4 and box 7 answered no)
  sale/business       the same with the lines 2a-6 question answered yes
  zero/as-asked       box 13 of 0: the statement and nothing else (the core
                      cannot tell it from alone/as-asked)
  control/base        the base wage return, no Form 1099-B at all

Run: python3 probe.py [--core v96 | --core-json core.json] [--out FILE]
Nothing in packages/ or tests/ is edited. The audit harness is loaded by path
under a unique name.
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


h = _load("bart_p0_audit_harness", REPO / "docs/phases/engine-breadth/milestones/sale-family-audit-evidence/audit_harness.py")

from packages.derivation.live import live_coordinate_run  # noqa: E402
from packages.derivation.live_session import _render_page  # noqa: E402

P = h.P
V96 = h.Core("v96", "v94", "v94")
BUSINESS = P + "schedule1-part1-scope.no-sch1-line3-business"
SHARED = tuple(P + "schedule1-part1-scope." + s for s in (
    "no-sch1-line2a-alimony", "no-sch1-line3-business", "no-sch1-line4-other-gains", "no-sch1-line5-rental",
    "no-sch1-line6-farm"))
OTHER = P + "w2g-scope.no-sch1-other-income-except-w2g"
KEYS = ("alone/as-asked", "alone/business", "alone/business-all", "alone/other-income", "alone/unanswered",
        "sale/as-asked",
        "sale/business", "zero/as-asked", "control/base")
WATCH = ("schedule1.line-10", "schedule1.top-entry", "form1040.line-8", "form1040.line-9", "form1040.line-11",
         "form1040.line-15", "form1040.line-16", "form1040.line-24", "form1040.line-25b", "form1040.line-33",
         "form1040.line-34", "form1040.line-37", "form1040.line-7a", "schedule-d.line-16")


def core_from(args: argparse.Namespace) -> Any:
    if args.core_json:
        body = json.loads(Path(args.core_json).read_text(encoding="utf-8"))
        return h.Core(body["version"], body["registry"], body["release_version"], content=Path(body["content"]),
                      releases=Path(body["releases"]), loader_from=body.get("loader_from"))
    n = int(args.core[1:])
    return h.Core(args.core, f"v{n - 2}", f"v{n - 2}")


def _set(acts: h.Acts, fact: str, value: str, tag: str) -> h.Acts:
    """Replace the base return's answer to one return-level fact (the filer's own answer)."""
    prefix = fact + "|"
    kept = [a for a in acts if not str(((a.get("payload") or {}).get("finding") or {}).get("fact_id", "")).startswith(prefix)]
    assert len(kept) == len(acts) - 1, (fact, len(acts) - len(kept))
    h._add(kept, "assertion", {"finding": h._attested(f"demo.bart.{tag}", h.fact_id_for(fact, (("tax-year", h.YEAR),)), value)})
    return h.renumber(kept)


def _statement(acts: h.Acts) -> h.Acts:
    """The barter exchange's Form 1099-B: broker and statement entities, nothing about box 13 (no fact type)."""
    h._introduce(acts, "demo.bart.exchange.broker", "tax.us.f1099b-broker")
    h._introduce(acts, "demo.bart.exchange.statement", "tax.us.f1099b-statement")
    return h.renumber(acts)


def build(key: str, content: Path) -> h.Acts:
    """The harness wage return (single, wages 50,000, 4,500 withheld) with every sale family open and closed."""
    shape, answers = key.split("/")
    acts = h.opened()
    kinds: set[str] = set()
    if shape == "sale":
        acts = h.sale(acts, "covered", "st", proceeds=25000.0, basis=5000.0, tag="bart-sale")
        kinds.add("covered")
    acts = h.answer(acts, content, **h.honest(kinds))
    acts = h.answer(acts, content, **h.honest_exception1(acts))
    acts = h.answer(acts, content, lines_18_19="yes", no_other_sd="yes", no_da_qof="yes")
    acts = h.say(acts, P + "f1099b.no-sale-box4-present", "no", "no-sale-box4", content)
    if shape == "sale":
        # The sale's own statement is the barter exchange's statement; box 4 and box 7 answered no.
        statement = "demo.sfa.bart-sale.statement"
        h.adopt(acts, "f1099b-statement-boxes.bundle.json")
        for slug in ("statement-box4-withholding-reported", "statement-box7-loss-not-allowed"):
            fid = h.fact_id_for(P + "f1099b." + slug, (("statement", statement), ("tax-year", h.YEAR)))
            h._add(acts, "assertion", {"finding": h._attested(f"demo.bart.{slug}", fid, "no")})
    elif shape in ("alone", "zero"):
        acts = _statement(acts)
    acts = h.say(acts, P + "filing-status", "single", "bart-status", content)
    for fact in ("taxpayer-over-65", "taxpayer-blind"):
        acts = h.say(acts, P + fact, False, "bart-" + fact, content)
    acts = h.renumber(acts)
    if answers == "business":
        acts = _set(acts, BUSINESS, "no", "business")
    elif answers == "business-all":
        for fact in SHARED:
            acts = _set(acts, fact, "no", fact.rsplit(".", 1)[-1])
    elif answers == "other-income":
        acts = _set(acts, OTHER, "no", "other-income")
    elif answers == "unanswered":
        for fact in SHARED:
            acts = h.strip(acts, fact)
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


def observe(core: Any, key: str) -> dict[str, Any]:
    acts = build(key, core.content)
    run_id = "demo.bart.p0." + key.replace("/", ".")
    surface = core.surface()
    with h.loader_entries(core):
        finished = h._handover(h._finish(copy.deepcopy(acts), package_path=core.package_path,
                                         package_version=core.version, release_path=core.release_path,
                                         release_version=core.release_version, note=run_id),
                               surface=surface, reconfirm=True)
        with TemporaryDirectory() as tmp:
            capability = h.WorkspaceCapability(Path(tmp) / "L")
            outcome = live_coordinate_run(capability, repo_root=REPO, authoritative_acts=finished,
                                          workspace_revision=len(finished),
                                          run_scope={"jurisdiction": "us", "year": h.YEAR}, scope_user=h.ccr.USER,
                                          request={"schema": "run-request.v1"}, run_id=run_id, governance_pins=[],
                                          surface=surface, output_name="out.json")
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
        for sentence in sentences:  # every distinct reason sentence the page draws (questions among them)
            text = h.scrub(sentence)[:600]
            if text.strip() and text not in questions:
                questions.append(text)
        if fid in WATCH:
            row = {"disposition": resolved.get("disposition"), "value": num(resolved.get("value"))}
            if resolved.get("disposition") != "computed":
                row["reasons"] = [h.scrub(x)[:500] for x in sentences if x.strip()]
                row["explanation"] = h.scrub(str(resolved.get("explanation") or resolved.get("blocked_explanation") or ""))[:600]
            lines[fid] = row
    blocked = sorted({(str(r.get("artifact_id")).removeprefix(P + "rule."), str(r.get("code")),
                       tuple(sorted(str(m).removeprefix(P) for m in (r.get("missing") or []))))
                      for r in report.get("dispositions") or [] if r.get("disposition") == "blocked"})
    attachments = {str(a.get("id")).removeprefix(P + "rule.attachment."): (a.get("resolved") or {}).get("disposition")
                   for a in saved.get("attachments") or []}
    return {
        "acts": len(acts),
        "stop": report.get("stop_reason"),
        "lines": lines,
        "attachments": attachments,
        "blocked_rules": [[b[0], b[1], list(b[2])] for b in blocked],
        "reason_sentences": questions,
        "guard_sentences": _guard_sentences(saved),
    }


def _guard_sentences(saved: dict[str, Any]) -> dict[str, str]:
    """The sentence the page shows for each watched line that is not computed (from its field)."""
    out = {}
    for section in saved.get("sections") or []:
        field = section.get("field") or {}
        fid = str(field.get("id") or "").removeprefix(P)
        disposition = (section.get("resolved") or {}).get("disposition")
        if fid in WATCH and disposition not in ("computed_zero", "published_value"):
            out[fid] = str(((field.get("dispositions") or {}).get(disposition) or {}).get("explain") or "")
    return out


def worker(job: tuple[Any, list[str]]) -> list[tuple[str, dict[str, Any]]]:
    core, keys = job
    out = []
    for key in keys:
        try:
            out.append((key, observe(core, key)))
        except Exception as exc:  # noqa: BLE001 - a rejected list is a result
            out.append((key, {"error": type(exc).__name__, "message": h.scrub(str(exc))[:400]}))
    return out


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--core", default="v96")
    parser.add_argument("--core-json")
    parser.add_argument("--only", action="append")
    parser.add_argument("--workers", type=int, default=max(1, (os.cpu_count() or 2) - 1))
    parser.add_argument("--out", default=str(HERE / "probe-v96.json"))
    args = parser.parse_args()
    core = core_from(args)
    todo = args.only or list(KEYS)
    started = time.monotonic()
    workers = min(args.workers, len(todo))
    with multiprocessing.get_context("spawn").Pool(workers) as pool:
        found = dict(pair for part in pool.map(worker, [(core, todo[i::workers]) for i in range(workers)]) for pair in part)
    body = {"core": {"package": core.version, "registry": core.registry, "release": core.release_version},
            "wall_time_s": round(time.monotonic() - started, 1), "runs": {k: found[k] for k in todo}}
    text = json.dumps(body, indent=1, sort_keys=True) + "\n"
    for marker in ("/Users/", "/private/", "/tmp/", "/var/"):
        assert marker not in text, marker
    Path(args.out).write_text(text, encoding="utf-8")
    print(json.dumps({"runs": len(found), "wall_time_s": body["wall_time_s"]}))


if __name__ == "__main__":
    main()
