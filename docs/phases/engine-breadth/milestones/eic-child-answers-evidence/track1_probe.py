"""Track 1 probe: a counted member's missing answer is asked, named by that member (eic-child-answers).

Evidence for docs/phases/engine-breadth/milestones/eic-child-answers.md, Track 1.
Charter: docs/reviews/eic-child-answers/charter-track1.md. ADR 0087.

Builds on P0's ``probe.py`` (loaded by path under a unique name): the same
synthetic demo.* returns, plus two members on the other-dependent child roster
(``odckid2``, two 17-year-olds) and on the relative roster (``parent2``, two
dependent parents). Each member's entity keeps a label of its own
("Synthetic <member id>"), so two members can be told apart. One per-member
answer is removed for one member, so it is unanswered; nothing is pre-filled.
Each list runs once through the real ``live_coordinate_run``; the saved page is
rendered with the real renderer and every value is read from the model embedded
in that page.

For every blocked page line it records the reasons the page shows, each as
``[member label or "", sentence]``.

Run: python3 track1_probe.py [--core v101] [--only CASE] [--out FILE]
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


p0 = _load("eicc_t1_p0_probe", HERE / "probe.py")
h = p0.h
hoh_eic = p0.hoh_eic
odc = p0.odc
ccr = p0.ccr

from packages.derivation.live import live_coordinate_run  # noqa: E402
from packages.derivation.live_session import _render_page  # noqa: E402

P = h.P
CHILD = p0.CHILD
PARENT = (p0.PARENT, "demo-eicc-parent-2")
ANSWERS = {**p0.ANSWERS, **{short: (P + "dtb.child." + name, "child") for short, name in (
    ("dtb-multiple", "multiple-other-claimants"), ("dtb-other-parent", "other-is-parent"),
    ("dtb-8332", "form-8332-released"), ("dtb-nights", "more-nights-with-filer"), ("dtb-same-nights", "same-nights"),
    ("dtb-agi", "filer-agi-higher"), ("dtb-will-claim", "other-will-claim"), ("dtb-same-agi", "same-agi"))}}
KID = p0.KID
# ``kid1pp``: one child whom both you and the other person, both its parents, could claim, with equal nights; every
# tie-breaker answer is then read on the way to "the same AGI" (no: the other parent, with the higher AGI, wins).
BOTH_PARENTS = {"another-could-claim": "yes", "multiple-other-claimants": "no", "filer-is-parent": "yes",
                "other-is-parent": "yes", "form-8332-released": "no", "more-nights-with-filer": "no",
                "same-nights": "yes", "filer-agi-higher": "no", "other-will-claim": "yes", "same-agi": "no"}
REL = tuple(a for a in ANSWERS if a.startswith("rel-"))
ODC_KID = ("odc-tin", "ssn", "lived", "joint")
CASES: tuple[str, ...] = (
    "single/kid1/30000/-", "single/kid2/30000/-",
    *(f"single/kid1/30000/{a}@1" for a in KID),
    *(f"single/kid2/30000/{a}@2" for a in KID),
    "single/kid2/30000/age@1", "single/kid2/30000/age@1+age@2", "single/kid2/30000/age@1+res@2",
    "single/kid1/30000/dtb-multiple@1", "single/kid1/30000/dtb-other-parent@1", "single/kid1pp/30000/-",
    *(f"single/kid1pp/30000/{a}@1" for a in ("dtb-8332", "dtb-nights", "dtb-same-nights", "dtb-agi",
                                              "dtb-will-claim", "dtb-same-agi")),
    "mfj/kid1/30000/age@1", "mfj/kid1/30000/joint@1",
    "single/odckid/30000/-", "single/odckid2/30000/-",
    *(f"single/odckid/30000/{a}@1" for a in ODC_KID),
    *(f"single/odckid2/30000/{a}@2" for a in ODC_KID),
    "single/parent/30000/-", "single/parent2/30000/-",
    *(f"single/parent/30000/{a}@p1" for a in REL),
    *(f"single/parent2/30000/{a}@p2" for a in REL),
    "single/parent2/30000/rel-tin@p1+rel-citizen@p2",
)
WATCH = p0.WATCH


def member_name(where: str) -> str:
    if where.startswith("p"):
        return PARENT[int(where[1:] or "1") - 1]
    return CHILD[int(where) - 1]


def label(member: str) -> str:
    return "Synthetic " + member


def drop(acts: h.Acts, removed: str) -> h.Acts:
    """Remove each named member's assertion(s) of the named answer; refuse when nothing was there to remove."""
    for part in removed.split("+"):
        short, where = part.split("@")
        fact, key = ANSWERS[short]
        marker = f"{key}={member_name(where)},"

        def hit(act: dict[str, Any]) -> bool:
            fid = str(((act.get("payload") or {}).get("finding") or {}).get("fact_id", ""))
            return fid.startswith(fact + "|") and marker in fid

        kept = [a for a in acts if not hit(a)]
        if len(kept) == len(acts):
            raise AssertionError(f"nothing removed for {part}")
        acts = kept
    return h.renumber(acts)


def build(case: str, content: Path = h.CONTENT) -> h.Acts:
    status_key, roster, wages_text, removed = case.split("/")
    wages = float(wages_text)
    status = hoh_eic.STATUS[status_key]
    kids: dict[str, dict[str, str]] = {}
    if roster in ("kid1", "kid2", "kid1pp"):
        kids = {name: odc.ctc_child() for name in CHILD[: 2 if roster == "kid2" else 1]}
    elif roster in ("odckid", "odckid2"):
        count = 2 if roster.endswith("2") else 1
        kids = {name: odc.odc_child() for name in CHILD[:count]}  # 17: the credit for other dependents
    rels = {name: odc.relative() for name in PARENT[: 2 if roster == "parent2" else 1]} \
        if roster.startswith("parent") else {}
    answers: dict[str, str | None] = {fact: "yes" for fact in hoh_eic.STEP4_ANSWERS}
    if not kids:
        answers[P + "eic.no-qualifying-child"] = "yes"
    acts = odc.build(wages=wages, filing_status=status, children=kids, relatives=rels, return_answers=answers)
    for act in acts:
        entity = (act.get("payload") or {}).get("entity")
        if isinstance(entity, dict) and entity.get("id") in (*CHILD, *PARENT):
            entity["label"] = label(str(entity["id"]))  # each member's own recorded label
    if roster.startswith("odckid"):
        for act in acts:  # 17 or older and not a student: fails the credit's age test, not counted
            finding = (act.get("payload") or {}).get("finding") or {}
            if str(finding.get("fact_id", "")).startswith(hoh_eic.EIC_AGE + "|"):
                finding["value"] = "no"
    if kids:
        acts.append(p0._act(len(acts), "bundle-adoption", {"bundle": ccr._load("dtb-questions.bundle.json")}))
        for name in kids:
            for question, value in (BOTH_PARENTS if roster == "kid1pp" else ccr._TIE_BREAKER_ANSWERS).items():
                fid = f"{P}dtb.child.{question}|child={name},tax-year={h.YEAR}"
                acts.append(p0._act(len(acts), "assertion",
                                    {"finding": p0._attested(f"demo.eicc.dtb.{question}.{name}", fid, value)}))
    acts = p0.hqp._complete(acts, min(500.0, wages * 0.05))
    hoh_eic._unemployment_withholding(acts, [])
    hoh_eic._social_security_withholding(acts, [])
    hoh_eic.w2g._w2g(acts, [])
    acts = ccr.state_taxpayer_facts(acts, core="v88")
    acts = p0.hqp._sale_families_closed(acts, content)
    if status == "married_filing_jointly":
        for fact in ("spouse-over-65", "spouse-blind"):
            acts = h.say(acts, P + fact, False, "eicc-" + fact, content)
    acts = h.renumber(acts)
    if removed != "-":
        acts = drop(acts, removed)
    return acts


def observe(core: Any, case: str, page_out: Path | None = None) -> dict[str, Any]:
    """One run; ``page_out`` keeps a copy of the saved page."""
    acts = build(case, core.content)
    run_id = "demo.eicc.t1." + case.replace("/", ".").replace("@", "-at-").replace("+", "-and-")
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
            if page_out is not None:
                page_out.write_text(text, encoding="utf-8")
            marker = "const MODEL = Object.freeze("
            saved, _ = json.JSONDecoder().raw_decode(text, text.index(marker) + len(marker))
            assert saved == model, "saved page model differs from the presentation model"
    rows = report.get("dispositions") or []
    reasons: dict[str, list[list[str]]] = {}
    silent: list[str] = []
    lines: dict[str, Any] = {}
    for section in saved.get("sections") or []:
        field = section.get("field") or {}
        fid = p0.short(field.get("id"))
        resolved = section.get("resolved") or {}
        if resolved.get("disposition") == "blocked":
            said = [[str(r.get("member_label") or ""), h.scrub(str(r.get("sentence")))]
                    for r in resolved.get("reasons") or [] if isinstance(r, dict)]
            if said:
                reasons[fid] = said
            else:
                silent.append(fid)
        if fid in WATCH:
            lines[fid] = {"disposition": resolved.get("disposition"), "value": hoh_eic.num(resolved.get("value"))}
    blocked_rules = sorted({p0.short(r.get("artifact_id")).removeprefix("rule.") + ":" + str(r.get("code"))
                            for r in rows if r.get("disposition") == "blocked"})
    pubs = {str(p.finding.get("symbol")): hoh_eic.num(p.finding.get("value")) for p in outcome.publications or ()}
    return {"stop": report.get("stop_reason"), "lines": lines,
            "symbols": {s: pubs.get(P + s) for s in p0.SYMBOLS},
            "blocked_rules": blocked_rules,
            "blocked_page_lines_without_sentence": sorted(silent),
            "reasons": reasons}


def _worker(args: tuple[Any, list[str]]) -> list[tuple[str, dict[str, Any]]]:
    core, cases = args
    out = []
    for case in cases:
        try:
            out.append((case, observe(core, case)))
        except Exception as exc:  # noqa: BLE001 - a rejected list is a result
            out.append((case, {"error": type(exc).__name__, "message": h.scrub(str(exc))[:500]}))
    return out


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--core", default="v101")
    parser.add_argument("--core-json")
    parser.add_argument("--only", action="append")
    parser.add_argument("--workers", type=int, default=max(1, min(9, (os.cpu_count() or 2) - 1)))
    parser.add_argument("--out")
    args = parser.parse_args()
    core = p0.core_from(args)
    todo = list(args.only) if args.only else list(CASES)
    started = time.monotonic()
    workers = min(args.workers, len(todo))
    if workers <= 1:
        found = dict(_worker((core, todo)))
    else:
        with multiprocessing.get_context("spawn").Pool(workers) as pool:
            parts = pool.map(_worker, [(core, todo[i::workers]) for i in range(workers)])
        found = dict(pair for part in parts for pair in part)
    body = {"core": {"package": core.version, "registry": core.registry, "release": core.release_version},
            "wall_time_s": round(time.monotonic() - started, 1),
            "runs": {c: found[c] for c in todo}}
    text = json.dumps(body, indent=1, sort_keys=True) + "\n"
    if args.out:
        Path(args.out).write_text(text, encoding="utf-8")
    print(text[:8000])


if __name__ == "__main__":
    main()
