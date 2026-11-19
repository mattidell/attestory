"""P0 probe for head of household needs a qualifying person (hoh-qualifying-person).

Evidence for docs/phases/engine-breadth/milestones/hoh-qualifying-person.md.
Charter: docs/reviews/hoh-qualifying-person/charter-p0.md.

Builds synthetic demo.* returns (wages 50,000, 4,500 withheld, standard
deduction) under each filing status, with and without a child or other
dependent recorded, and runs each once through the real
live_coordinate_run, renders the saved page with the real renderer and reads
every value from the model embedded in that page.

Cases (status/dependents[/answer]):

  single/none, mfj/none        controls, no dependent
  hoh/none                     head of household, no child or dependent recorded
  hoh/child                    head of household, one child counted for the
                               earned income credit and the child tax credit
  hoh/relative                 head of household, only an other-dependent relative
                               (credit for other dependents)
  qss/none                     qualifying surviving spouse, no child recorded
  qss/child                    qualifying surviving spouse with a dependent child
  single/child, mfj/child      the same child under single and joint (controls)
  single/none/low, hoh/relative/low
                               wages 12,000 (1,000 withheld): where the earned
                               income credit with no qualifying child is not $0

On a scratch core that adds the head of household and qualifying surviving
spouse questions, ``--answer`` adds the filer's answer to that question to
every hoh and qss case (``yes`` or ``no``; ``none`` leaves it unanswered).

Run: python3 probe.py [--core v97 | --core-json core.json] [--answer none|yes|no] [--out FILE]
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


h = _load("hoh_p0_audit_harness", REPO / "docs/phases/engine-breadth/milestones/sale-family-audit-evidence/audit_harness.py")

from packages.derivation.live import live_coordinate_run  # noqa: E402
from packages.derivation.live_session import _render_page  # noqa: E402
from tests import test_other_dependents_credit_track1 as odc  # noqa: E402
from tests import test_w2g_gambling as w2g  # noqa: E402
from tests.helpers import current_core_returns as ccr  # noqa: E402
from tests.test_form_1099_withholding import _social_security_withholding, _unemployment_withholding  # noqa: E402
from tests.test_refund_or_amount_owed_track1 import _act, _attested, _close_empty, _close_other_box4_families  # noqa: E402
from tests.test_refund_or_amount_owed_track2 import _add_bottom_line_answers, _add_box2_only  # noqa: E402

P = h.P
V97 = h.Core("v97", "v95", "v95")
STATUS = {"single": "single", "mfj": "married_filing_jointly", "hoh": "head_of_household",
          "qss": "qualifying_surviving_spouse"}
KEYS = ("single/none", "mfj/none", "hoh/none", "hoh/child", "hoh/relative", "qss/none", "qss/child",
        "single/child", "mfj/child", "single/none/low", "hoh/relative/low")
# The questions a scratch successor adds (prototype.py); absent from v97.
QUESTION = {"hoh": P + "hoh.tests-met", "qss": P + "qss.tests-met"}
WATCH = ("form1040.line-11", "form1040.line-11a", "form1040.line-12e", "form1040.line-14", "form1040.line-15",
         "form1040.line-16", "form1040.line-19", "form1040.line-22", "form1040.line-24", "form1040.line-27a",
         "form1040.line-28", "form1040.line-33", "form1040.line-34", "form1040.line-35a", "form1040.line-37")


def core_from(args: argparse.Namespace) -> Any:
    if args.core_json:
        body = json.loads(Path(args.core_json).read_text(encoding="utf-8"))
        return h.Core(body["version"], body["registry"], body["release_version"], content=Path(body["content"]),
                      releases=Path(body["releases"]), loader_from=body.get("loader_from"))
    n = int(args.core[1:])
    return h.Core(args.core, f"v{n - 2}", f"v{n - 2}")


def build(key: str, content: Path = h.CONTENT, answer: str = "none") -> h.Acts:
    """The current-core child-credit return (as ``part_ii_b_return`` builds it) for one status and dependents."""
    status_key, deps = key.split("/")[:2]
    low = key.endswith("/low")
    status = STATUS[status_key]
    kids = {"demo-hoh-child-1": odc.ctc_child()} if deps == "child" else {}
    rels = {"demo-hoh-relative-1": odc.relative()} if deps == "relative" else {}
    answers: dict[str, str | None] = {}
    if kids or low:
        answers.update({P + "eic.age-25-under-65": "yes", P + "eic.main-home-in-us": "yes"})
    if low and not kids:
        answers[P + "eic.no-qualifying-child"] = "yes"
    acts = odc.build(wages=12000.0 if low else 50000.0, filing_status=status, children=kids, relatives=rels, return_answers=answers)
    if kids:
        acts.append(_act(len(acts), "bundle-adoption", {"bundle": ccr._load("dtb-questions.bundle.json")}))
        for name in kids:
            for question, value in ccr._TIE_BREAKER_ANSWERS.items():
                fid = f"{P}dtb.child.{question}|child={name},tax-year={h.YEAR}"
                acts.append(_act(len(acts), "assertion", {"finding": _attested(f"demo.hoh.dtb.{question}.{name}", fid, value)}))
    acts = _complete(acts, 1000.0 if low else 4500.0)
    _unemployment_withholding(acts, [])
    _social_security_withholding(acts, [])
    w2g._w2g(acts, [])
    acts = ccr.state_taxpayer_facts(acts, core="v88")
    acts = _sale_families_closed(acts, content)
    if status == "married_filing_jointly":
        for fact in ("spouse-over-65", "spouse-blind"):
            acts = h.say(acts, P + fact, False, "hoh-" + fact, content)
    if status_key in QUESTION and answer != "none":
        acts = h.say(acts, QUESTION[status_key], answer, "hoh-tests", content)
    return h.renumber(acts)


def _complete(acts: h.Acts, withheld: float) -> h.Acts:
    """``odc._complete`` with W-2 box 2 withholding (the base return's 4,500) instead of 0."""
    acts = _add_box2_only(acts, employer="demo.cgd.t2.employer", slip="demo.cgd.t2.w2", amount=withheld)
    _close_empty(acts, family=P + "w2-box2", version="v1", closure_fact=P + "w2-box2.source-closure",
                 horizon="demo.odc.complete.w2box2")
    _close_other_box4_families(acts, skip={"w2-box2"})
    return _add_bottom_line_answers(acts, estimated=0.0, applied_2026=0.0)


def _sale_families_closed(acts: h.Acts, content: Path) -> h.Acts:
    """Every sale family open and closed by the honest answers of a filer with no sale (as ``h.opened`` and
    the bartering probe's control return do), plus the no-sale box 4 answer."""
    for name in h.OPEN_BUNDLES:
        h.adopt(acts, name)
    for kind in ("noncovered", "no1099b", "codeb"):
        for term in h.TERMS:
            for scalar in (None, *h.SALE_KINDS[kind]["kinds"]):
                fam = h.family_id(kind, term, scalar)
                h._add(acts, "horizon-genesis", {
                    "family": {"id": fam, "version": h.SALE_KINDS[kind]["version"]},
                    "scope": {"tax-year": h.YEAR, "subject": "demo.primary"},
                    "horizon_id": f"demo.sfa.{fam.removeprefix(P)}.h0",
                })
    acts = h.renumber(acts)
    acts = h.answer(acts, content, **h.honest(set()))
    acts = h.answer(acts, content, **h.honest_exception1(acts))
    acts = h.answer(acts, content, lines_18_19="yes", no_other_sd="yes", no_da_qof="yes")
    return h.say(acts, P + "f1099b.no-sale-box4-present", "no", "no-sale-box4", content)


def num(value: Any) -> Any:
    if isinstance(value, str):
        try:
            value = float(value)
        except ValueError:
            return value
    if isinstance(value, float) and value.is_integer():
        return int(value)
    return value


def observe(core: Any, key: str, answer: str = "none") -> dict[str, Any]:
    acts = build(key, core.content, answer)
    run_id = "demo.hoh.p0." + key.replace("/", ".")
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
    sentences: list[str] = []
    for section in saved.get("sections") or []:
        field = section.get("field") or {}
        fid = str(field.get("id") or "").removeprefix(P)
        resolved = section.get("resolved") or {}
        said = []
        for name in ("questions", "reasons", "blocked_reasons"):
            for item in resolved.get(name) or []:
                text = str(item.get("sentence") or item.get("text") or "") if isinstance(item, dict) else str(item)
                if text.strip():
                    said.append(h.scrub(text)[:700])
        for text in said:
            if text not in sentences:
                sentences.append(text)
        if fid in WATCH:
            row: dict[str, Any] = {"disposition": resolved.get("disposition"), "value": num(resolved.get("value"))}
            if resolved.get("disposition") != "computed":
                row["said"] = said[:4]
            lines[fid] = row
    blocked = sorted({str(r.get("artifact_id")).removeprefix(P + "rule.") + ":" + str(r.get("code"))
                      for r in report.get("dispositions") or [] if r.get("disposition") == "blocked"})
    held = sorted({str(r.get("artifact_id")).removeprefix(P + "rule.")
                   for r in report.get("dispositions") or [] if r.get("disposition") == "guard_inapplicable"})
    pubs = {str(p.finding.get("symbol")): num(p.finding.get("value")) for p in outcome.publications or ()}
    symbols = {s.removeprefix(P): pubs.get(s) for s in (
        P + "filing-status", "filing_status", "demo.form1040.standard_deduction", P + "dependents-worksheet.line3",
        P + "income.taxable-income", P + "tax.total-tax", P + "eic.form1040-line27a", P + "ctc.form1040-line19",
        P + "ctc.form1040-line28", P + "ctc.child-count", P + "odc.relative-count", P + "eic.qualifying-child-count")}
    return {"stop": report.get("stop_reason"), "lines": lines, "symbols": symbols, "blocked_rules": blocked,
            "guard_inapplicable_rules": held, "sentences": sentences[:16]}


def _worker(args: tuple[Any, list[str], str]) -> list[tuple[str, dict[str, Any]]]:
    core, keys, answer = args
    out = []
    for key in keys:
        try:
            out.append((key, observe(core, key, answer)))
        except Exception as exc:  # noqa: BLE001 - a rejected list is a result
            out.append((key, {"error": type(exc).__name__, "message": h.scrub(str(exc))[:500]}))
    return out


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--core", default="v97")
    parser.add_argument("--core-json")
    parser.add_argument("--answer", choices=("none", "yes", "no"), default="none")
    parser.add_argument("--only", action="append")
    parser.add_argument("--workers", type=int, default=max(1, min(9, (os.cpu_count() or 2) - 1)))
    parser.add_argument("--out")
    args = parser.parse_args()
    core = core_from(args)
    todo = args.only or list(KEYS)
    started = time.monotonic()
    workers = min(args.workers, len(todo))
    if workers <= 1:
        found = dict(_worker((core, todo, args.answer)))
    else:
        with multiprocessing.get_context("spawn").Pool(workers) as pool:
            parts = pool.map(_worker, [(core, todo[i::workers], args.answer) for i in range(workers)])
        found = dict(pair for part in parts for pair in part)
    body = {"core": {"package": core.version, "registry": core.registry, "release": core.release_version},
            "answer": args.answer, "wall_time_s": round(time.monotonic() - started, 1),
            "runs": {k: found[k] for k in todo}}
    text = json.dumps(body, indent=1, sort_keys=True) + "\n"
    if args.out:
        Path(args.out).write_text(text, encoding="utf-8")
    print(text[:20000])


if __name__ == "__main__":
    main()
