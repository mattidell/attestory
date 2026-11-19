"""P0 probe for the earned income credit for a head of household (hoh-eic).

Evidence for docs/phases/engine-breadth/milestones/hoh-eic.md.
Charter: docs/reviews/hoh-eic/charter-p0.md.

Builds synthetic demo.* returns with the hoh-qualifying-person probe's return
builder (its probe.py and the audit harness, each loaded by path under a
unique name) and runs each once through the real live_coordinate_run, renders
the saved page with the real renderer and reads every value from the model
embedded in that page. Every head of household return answers v98's head of
household tests question yes.

Cases (status/dependents/wages):

  hoh/parent/W     head of household whose qualifying person is a dependent
                   parent on the other-dependent relative roster; no child
  hoh/child/W      head of household with one child counted for the earned
                   income credit and the child tax credit
  hoh/childnosep/W the same child with the credit's separated-spouse answer
                   left unanswered (what v98 asks a head of household with a child)
  hoh/oldchild/W   head of household with one child who is not a qualifying
                   child for the credit (fails the age test) and is claimed
                   for the credit for other dependents
  single/none/W, single/parent/W, single/child/W, mfs/none/W, mfs/child/W
                   controls

Wages 7,000 (no-child credit phase-in), 16,000 (no-child phase-out),
30,000 (one-child phase-out, above every no-child amount) and 50,000.

On a scratch core that adds the marital-status question, ``--answer`` adds
the filer's answer to every head of household case (``yes``: not married at
the end of 2025, ``no``: married; ``none`` leaves it unanswered).

Run: python3 probe.py [--core v98 | --core-json core.json] [--answer none|yes|no] [--out FILE]
Nothing in packages/ or tests/ is edited.
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


MILESTONES = REPO / "docs/phases/engine-breadth/milestones"
h = _load("hoh_p0_audit_harness", MILESTONES / "sale-family-audit-evidence/audit_harness.py")
base = _load("hoh_eic_p0_hoh_probe", MILESTONES / "hoh-qualifying-person-evidence/probe.py")

from packages.derivation.live import live_coordinate_run  # noqa: E402
from packages.derivation.live_session import _render_page  # noqa: E402
from tests import test_other_dependents_credit_track1 as odc  # noqa: E402
from tests import test_w2g_gambling as w2g  # noqa: E402
from tests.helpers import current_core_returns as ccr  # noqa: E402
from tests.test_form_1099_withholding import _social_security_withholding, _unemployment_withholding  # noqa: E402
from tests.test_refund_or_amount_owed_track1 import _act, _attested  # noqa: E402

P = h.P
STATUS = {"single": "single", "mfs": "married_filing_separately", "hoh": "head_of_household",
          "mfj": "married_filing_jointly", "qss": "qualifying_surviving_spouse"}
KEYS = ("hoh/parent/7000", "hoh/parent/16000", "hoh/parent/50000",
        "hoh/child/7000", "hoh/child/30000", "hoh/childnosep/7000",
        "hoh/oldchild/7000", "hoh/oldchild/16000",
        "single/none/7000", "single/none/16000", "single/parent/16000", "single/child/30000",
        "mfj/none/16000", "qss/none/16000",
        "mfs/none/7000", "mfs/child/30000")
HOH_TESTS = P + "hoh.tests-met"
QSS_TESTS = P + "qss.tests-met"
# The question a scratch successor adds (design.py); absent from v98.
QUESTION = P + "eic.not-married"
EIC_AGE = "tax.us.2025.eic.child.age"
CORE_BUNDLE = json.loads((h.CONTENT / "core_calculations.bundle.v4.json").read_text())["id"]
WATCH = ("form1040.line-11", "form1040.line-12e", "form1040.line-15", "form1040.line-16", "form1040.line-19",
         "form1040.line-24", "form1040.line-27a", "form1040.line-28", "form1040.line-33", "form1040.line-34",
         "form1040.line-35a", "form1040.line-37")
SYMBOLS = ("eic.status-class", "eic.column-count", "eic.early-stop", "eic.questions-required",
           "eic.answer.separated-spouse", "eic.answer.not-married", "eic.answer.age-25-under-65",
           "eic.answer.not-claimable-as-dependent", "eic.worksheet-a.line-6", "eic.gate-result",
           "eic.eligibility-result", "payments.line27a", "ctc.child-count", "odc.relative-count",
           "ctc.form1040-line19", "tax.total-tax")


def build(key: str, content: Path = h.CONTENT, answer: str = "none") -> h.Acts:
    status_key, deps, wages_text = key.split("/")
    wages = float(wages_text)
    status = STATUS[status_key]
    kids: dict[str, dict[str, str]] = {}
    if deps in ("child", "childnosep"):
        kids = {"demo-hoh-eic-child-1": odc.ctc_child()}
    elif deps == "oldchild":
        kids = {"demo-hoh-eic-child-1": odc.odc_child()}  # 17 or older: credit for other dependents
    rels = {"demo-hoh-eic-parent-1": odc.relative()} if deps == "parent" else {}
    answers: dict[str, str | None] = {P + "eic.age-25-under-65": "yes", P + "eic.main-home-in-us": "yes"}
    if deps not in ("child", "childnosep"):
        answers[P + "eic.no-qualifying-child"] = "yes"
    acts = odc.build(wages=wages, filing_status=status, children=kids, relatives=rels, return_answers=answers)
    if deps == "oldchild":
        # The child fails the credit's age test (19 or older, not a student, not disabled): not counted.
        for act in acts:
            finding = (act.get("payload") or {}).get("finding") or {}
            if str(finding.get("fact_id", "")).startswith(EIC_AGE + "|"):
                finding["value"] = "no"
    if deps == "childnosep":
        acts = [a for a in acts if not str(((a.get("payload") or {}).get("finding") or {}).get("fact_id", ""))
                .startswith(P + "eic.separated-spouse|")]
        acts = h.renumber(acts)
    if kids:
        acts.append(_act(len(acts), "bundle-adoption", {"bundle": ccr._load("dtb-questions.bundle.json")}))
        for name in kids:
            for question, value in ccr._TIE_BREAKER_ANSWERS.items():
                fid = f"{P}dtb.child.{question}|child={name},tax-year={h.YEAR}"
                acts.append(_act(len(acts), "assertion", {"finding": _attested(f"demo.hoheic.dtb.{question}.{name}", fid, value)}))
    acts = base._complete(acts, min(500.0, wages * 0.05))
    _unemployment_withholding(acts, [])
    _social_security_withholding(acts, [])
    w2g._w2g(acts, [])
    acts = ccr.state_taxpayer_facts(acts, core="v88")
    acts = base._sale_families_closed(acts, content)
    if status == "married_filing_separately":
        adopted = {str(((a.get("payload") or {}).get("bundle") or {}).get("version"))
                   for a in acts if a.get("kind") == "bundle-adoption"
                   and ((a.get("payload") or {}).get("bundle") or {}).get("id") == CORE_BUNDLE}
        if "v4" not in adopted:  # the separate-return spouse answer is declared from core bundle v4
            h._add(acts, "bundle-adoption", {"bundle": json.loads((content / "core_calculations.bundle.v4.json").read_text())})
        for fact in ("spouse-over-65", "spouse-blind", "standard-deduction.spouse-separate-condition"):
            acts = h.say(acts, P + fact, False, "hoheic-" + fact, content)
        acts = h.say(acts, P + "mfs-lived-apart-all-year", "yes", "hoheic-mfs-apart", content)
    if status == "married_filing_jointly":
        for fact in ("spouse-over-65", "spouse-blind"):
            acts = h.say(acts, P + fact, False, "hoheic-" + fact, content)
    if status_key == "qss":
        acts = h.say(acts, QSS_TESTS, "yes", "hoheic-qss-tests", content)
    if status_key == "hoh":
        acts = h.say(acts, HOH_TESTS, "yes", "hoheic-hoh-tests", content)
        if answer != "none":
            first, *later = answer.split(">")  # "yes>no": the filer answers yes, then changes the answer to no
            acts = h.say(acts, QUESTION, first, "hoheic-not-married", content)
            for n, value in enumerate(later, 2):
                fact = h.fact_id_for(QUESTION, (("tax-year", h.YEAR),))
                h._add(acts, "assertion", {"finding": h._attested(f"demo.sfa.answer.hoheic-not-married-{n}", fact, value)})
                acts = h.renumber(acts)
    return h.renumber(acts)


num = base.num


def observe(core: Any, key: str, answer: str = "none") -> dict[str, Any]:
    acts = build(key, core.content, answer)
    run_id = "demo.hoheic.p0." + key.replace("/", ".")
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
                    said.append(h.scrub(text)[:2000])
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
    pubs = {str(p.finding.get("symbol")): num(p.finding.get("value")) for p in outcome.publications or ()}
    return {"stop": report.get("stop_reason"), "lines": lines,
            "symbols": {s: pubs.get(P + s) for s in SYMBOLS}, "blocked_rules": blocked, "sentences": sentences[:16]}


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
    parser.add_argument("--core", default="v98")
    parser.add_argument("--core-json")
    parser.add_argument("--answer", choices=("none", "yes", "no"), default="none")
    parser.add_argument("--only", action="append")
    parser.add_argument("--workers", type=int, default=max(1, min(9, (os.cpu_count() or 2) - 1)))
    parser.add_argument("--out")
    args = parser.parse_args()
    core = base.core_from(args)
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
