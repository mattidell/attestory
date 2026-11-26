"""P0 probe: two roster members with the same recorded label (same-label-members).

Evidence for docs/phases/engine-breadth/milestones/same-label-members.md, P0.

Builds on eic-child-answers' ``track1_probe.py`` (loaded by path under a unique
name): the same synthetic demo.* returns, with each member's recorded label set
by the case instead of one label per member. A case is

    <status>/<roster>/<labels>/<removed>

``roster`` is ``kid2`` or ``kid3`` (children on the earned income, child tax
credit and tie-breaker rosters), ``odckid2`` (two 17-year-olds on the
other-dependent child roster), ``parent2`` (two dependent parents on the
relative roster) or ``kidpar`` (one child and one parent). ``labels`` gives one
letter per member in entry order; members with the same letter share one
recorded label ("Demo Sam", "Demo Alex", "Demo Kim"). ``removed`` is as in
``track1_probe.drop`` (``age@1+age@2``; parents are ``p1``, ``p2``).

Each list runs once through the real ``live_coordinate_run``; the saved page is
rendered with the real renderer and every value is read from the model embedded
in that page. For every blocked page line it records the reasons the page
shows, each as ``[member label or "", member ordinal or 0, sentence]``, and the
question links (``questionRefs``) on that line.

``--scratch <projection.py>`` runs the same lists with the top-level functions
and classes of that copy of ``packages/derivation/presentation_projection.py``
that differ from the repository's own swapped in for the run (see
``scratch_projection``). Nothing in the repository is edited.

``--dom <page.html>`` also renders each saved model with that page through the
page-plain-words DOM checker (``check_page_dom.mjs``, node) and records the
member reason items the page draws.

Run: python3 probe.py [--core v107] [--scratch FILE] [--dom PAGE] [--only CASE] [--out FILE]
"""
from __future__ import annotations

import argparse
import ast
import contextlib
import copy
import importlib.util
import json
import multiprocessing
import os
import subprocess
import sys
import time
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any, Iterator

HERE = Path(__file__).resolve().parent
MILESTONES = HERE.parent
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


t1 = _load("slm_p0_eicc_t1_probe", MILESTONES / "eic-child-answers-evidence/track1_probe.py")
p0 = t1.p0
h = t1.h
hoh_eic = t1.hoh_eic
odc = t1.odc
ccr = t1.ccr

from packages.derivation import presentation_projection as projection  # noqa: E402
from packages.derivation.live import live_coordinate_run  # noqa: E402
from packages.derivation.live_session import _render_page  # noqa: E402

P = h.P
CHILD = (*t1.CHILD, "demo-slm-child-3")
PARENT = t1.PARENT
LABELS = {"A": "Demo Sam", "B": "Demo Alex", "C": "Demo Kim"}
CHECKER = MILESTONES / "page-plain-words-evidence/check_page_dom.mjs"

CASES: tuple[str, ...] = (
    # Controls: every member answered.
    "single/kid2/AA/-", "single/parent2/AA/-",
    # Distinct labels (control): one reason per member already.
    "single/kid2/AB/age@1+age@2", "single/kid2/AB/age@2", "single/parent2/AB/rel-tin@p1+rel-tin@p2",
    # Two members share a label, both missing the same answer.
    "single/kid2/AA/age@1+age@2", "single/kid2/AA/res@1+res@2", "single/kid2/AA/u17@1+u17@2",
    "single/kid2/AA/dtb-another@1+dtb-another@2",
    "single/odckid2/AA/odc-tin@1+odc-tin@2", "single/parent2/AA/rel-tin@p1+rel-tin@p2",
    # Two share a label, each missing a different answer.
    "single/kid2/AA/age@1+res@2", "single/parent2/AA/rel-tin@p1+rel-citizen@p2",
    # Two share a label, only one is missing the answer.
    "single/kid2/AA/age@1", "single/kid2/AA/age@2", "single/parent2/AA/rel-tin@p2",
    # Three share a label.
    "single/kid3/AAA/age@1+age@2+age@3", "single/kid3/AAA/age@3", "single/kid3/AAA/age@1+res@3",
    # Two of three share a label.
    "single/kid3/AAB/age@1+age@2+age@3", "single/kid3/ABA/age@3",
    # A child and a parent share a label (different kinds, different questions).
    "single/kidpar/AA/age@1+rel-tin@p1",
    # Joint return.
    "mfj/kid2/AA/age@1+age@2",
)


def _changed_names(base: str, scratch: str) -> list[str]:
    """Top-level definitions whose source differs, or that only the scratch copy has."""
    def tops(text: str) -> dict[str, str]:
        tree = ast.parse(text)
        found: dict[str, str] = {}
        for node in tree.body:
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                found[node.name] = ast.get_source_segment(text, node) or ""
        return found

    a, b = tops(base), tops(scratch)
    return sorted(name for name in b if a.get(name) != b[name])


_SCRATCH: dict[str, Any] = {}


def _scratch_namespace(path: Path, names: list[str]) -> dict[str, Any]:
    """The scratch copy loaded as its own module, with every unchanged name bound to the real object."""
    key = str(path)
    if key not in _SCRATCH:
        spec = importlib.util.spec_from_file_location("slm_p0_scratch_projection", path)
        assert spec is not None and spec.loader is not None
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        # Unchanged definitions resolve to the real module's objects, so
        # exception classes and shared helpers keep their identity.
        for name, value in projection.__dict__.items():
            if name not in names and not name.startswith("__"):
                setattr(module, name, value)
        _SCRATCH[key] = module.__dict__
    return _SCRATCH[key]


@contextlib.contextmanager
def scratch_projection(path: Path | None) -> Iterator[list[str]]:
    """For the block, the changed definitions of a scratch projection copy, swapped into the real module."""
    if path is None:
        yield []
        return
    names = _changed_names(Path(projection.__file__).read_text(encoding="utf-8"), path.read_text(encoding="utf-8"))
    namespace = _scratch_namespace(path, names)
    saved = {name: projection.__dict__.get(name) for name in names}
    try:
        for name in names:
            setattr(projection, name, namespace[name])
        yield names
    finally:
        for name, value in saved.items():
            if value is None:
                delattr(projection, name)
            else:
                setattr(projection, name, value)


def member_name(where: str) -> str:
    if where.startswith("p"):
        return PARENT[int(where[1:] or "1") - 1]
    return CHILD[int(where) - 1]


def drop(acts: h.Acts, removed: str) -> h.Acts:
    """Remove each named member's assertion(s) of the named answer; refuse when nothing was there to remove."""
    for part in removed.split("+"):
        short, where = part.split("@")
        fact, key = t1.ANSWERS[short]
        marker = f"{key}={member_name(where)},"

        def hit(act: dict[str, Any]) -> bool:
            fid = str(((act.get("payload") or {}).get("finding") or {}).get("fact_id", ""))
            return fid.startswith(fact + "|") and marker in fid

        kept = [a for a in acts if not hit(a)]
        if len(kept) == len(acts):
            raise AssertionError(f"nothing removed for {part}")
        acts = kept
    return h.renumber(acts)


def members(roster: str) -> tuple[list[str], list[str]]:
    """(children, parents) in entry order."""
    if roster in ("kid2", "odckid2"):
        return list(CHILD[:2]), []
    if roster == "kid3":
        return list(CHILD[:3]), []
    if roster == "parent2":
        return [], list(PARENT[:2])
    if roster == "kidpar":
        return [CHILD[0]], [PARENT[0]]
    raise ValueError(roster)


def build(case: str, content: Path = h.CONTENT) -> h.Acts:
    status_key, roster, letters, removed = case.split("/")
    wages = 30000.0
    status = hoh_eic.STATUS[status_key]
    children, parents = members(roster)
    if len(letters) != len(children) + len(parents):
        raise ValueError(f"{case}: one label letter per member")
    labels = dict(zip([*children, *parents], (LABELS[letter] for letter in letters)))
    if roster == "odckid2":
        kids = {name: odc.odc_child() for name in children}
    else:
        kids = {name: odc.ctc_child() for name in children}
    rels = {name: odc.relative() for name in parents}
    answers: dict[str, str | None] = {fact: "yes" for fact in hoh_eic.STEP4_ANSWERS}
    if not kids:
        answers[P + "eic.no-qualifying-child"] = "yes"
    acts = odc.build(wages=wages, filing_status=status, children=kids, relatives=rels, return_answers=answers)
    for act in acts:
        entity = (act.get("payload") or {}).get("entity")
        if isinstance(entity, dict) and entity.get("id") in labels:
            entity["label"] = labels[str(entity["id"])]
    if roster == "odckid2":
        for act in acts:  # 17 or older and not a student: fails the credit's age test, not counted
            finding = (act.get("payload") or {}).get("finding") or {}
            if str(finding.get("fact_id", "")).startswith(hoh_eic.EIC_AGE + "|"):
                finding["value"] = "no"
    if kids:
        acts.append(p0._act(len(acts), "bundle-adoption", {"bundle": ccr._load("dtb-questions.bundle.json")}))
        for name in kids:
            for question, value in ccr._TIE_BREAKER_ANSWERS.items():
                fid = f"{P}dtb.child.{question}|child={name},tax-year={h.YEAR}"
                acts.append(p0._act(len(acts), "assertion",
                                    {"finding": p0._attested(f"demo.slm.dtb.{question}.{name}", fid, value)}))
    acts = p0.hqp._complete(acts, min(500.0, wages * 0.05))
    hoh_eic._unemployment_withholding(acts, [])
    hoh_eic._social_security_withholding(acts, [])
    hoh_eic.w2g._w2g(acts, [])
    acts = ccr.state_taxpayer_facts(acts, core="v88")
    acts = p0.hqp._sale_families_closed(acts, content)
    if status == "married_filing_jointly":
        for fact in ("spouse-over-65", "spouse-blind"):
            acts = h.say(acts, P + fact, False, "slm-" + fact, content)
    acts = h.renumber(acts)
    if removed != "-":
        acts = drop(acts, removed)
    return acts


def dom_check(page: Path, model: dict[str, Any]) -> dict[str, Any]:
    """The page-plain-words DOM checker's result for one saved model (first-read text included)."""
    env = os.environ.copy()
    env["PPW_CHECK_DETAIL"] = "1"
    proc = subprocess.run(["node", str(CHECKER), str(page)], input=json.dumps({"key": "case", "model": model}) + "\n",
                          text=True, capture_output=True, timeout=60, check=True, env=env)
    return dict(json.loads(proc.stdout)["case"])


def observe(core: Any, case: str, scratch: Path | None = None, page: Path | None = None) -> dict[str, Any]:
    acts = build(case, core.content)
    run_id = "demo.slm.p0." + case.replace("/", ".").replace("@", "-at-").replace("+", "-and-")
    surface = core.surface()
    with h.loader_entries(core), scratch_projection(scratch):
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
            text = _render_page(REPO, capability, outcome.presentation_path).decode("utf-8")
            marker = "const MODEL = Object.freeze("
            saved, _ = json.JSONDecoder().raw_decode(text, text.index(marker) + len(marker))
            assert saved == model, "saved page model differs from the presentation model"
            projection.validate_presentation_model(saved)
    rows = report.get("dispositions") or []
    reasons: dict[str, list[list[Any]]] = {}
    links: dict[str, list[Any]] = {}
    silent: list[str] = []
    for section in saved.get("sections") or []:
        field = section.get("field") or {}
        fid = p0.short(field.get("id"))
        resolved = section.get("resolved") or {}
        if resolved.get("disposition") == "blocked":
            said = [[str(r.get("memberLabel") or ""), int(r.get("memberOrdinal") or 0), h.scrub(str(r.get("sentence")))]
                    for r in resolved.get("reasons") or [] if isinstance(r, dict)]
            if said:
                reasons[fid] = said
            else:
                silent.append(fid)
            if resolved.get("questionRefs"):
                links[fid] = [ref.get("reasonIndices") for ref in resolved["questionRefs"]]
    member_targets = sorted(
        str((group.get("answerTarget") or {}).get("targetFactId", ""))
        for group in saved.get("questionGroups") or []
        if any(marker in json.dumps(group.get("answerTarget") or {}) for marker in ("child=", "dependent=")))
    pubs = {str(p.finding.get("symbol")): hoh_eic.num(p.finding.get("value")) for p in outcome.publications or ()}
    found: dict[str, Any] = {
        "stop": report.get("stop_reason"),
        "symbols": {s: pubs.get(P + s) for s in p0.SYMBOLS},
        "blocked_rules": sorted({p0.short(r.get("artifact_id")).removeprefix("rule.") + ":" + str(r.get("code"))
                                 for r in rows if r.get("disposition") == "blocked"}),
        "blocked_page_lines_without_sentence": sorted(silent),
        "reasons": reasons,
        "question_links": links,
        "question_groups": len(saved.get("questionGroups") or []),
        "member_question_group_targets": [p0.short(t) for t in member_targets],
    }
    if page is not None:
        dom = dom_check(page, saved)
        first = str(dom.get("first_read_text") or "")
        found["dom"] = {
            "section_errors": dom.get("section_errors"),
            "first_read_leaks": dom.get("total_first_read_leaks"),
            # Each distinct member reason item the page draws ("<name>: <sentence>"), first 60 characters.
            "member_items": sorted({line.strip()[:60] for line in first.split("\n")
                                    if any(line.strip().startswith(label) for label in LABELS.values())}),
        }
    return found


def _worker(args: tuple[Any, list[str], Path | None, Path | None]) -> list[tuple[str, dict[str, Any]]]:
    core, cases, scratch, page = args
    out = []
    for case in cases:
        try:
            out.append((case, observe(core, case, scratch, page)))
        except Exception as exc:  # noqa: BLE001 - a rejected list is a result
            out.append((case, {"error": type(exc).__name__, "message": h.scrub(str(exc))[:500]}))
    return out


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--core", default="v107")
    parser.add_argument("--core-json")
    parser.add_argument("--scratch", type=Path)
    parser.add_argument("--dom", type=Path)
    parser.add_argument("--only", action="append")
    parser.add_argument("--workers", type=int, default=max(1, min(9, (os.cpu_count() or 2) - 1)))
    parser.add_argument("--out")
    args = parser.parse_args()
    core = p0.core_from(args)
    todo = list(args.only) if args.only else list(CASES)
    started = time.monotonic()
    workers = min(args.workers, len(todo))
    if workers <= 1:
        found = dict(_worker((core, todo, args.scratch, args.dom)))
    else:
        with multiprocessing.get_context("spawn").Pool(workers) as pool:
            parts = pool.map(_worker, [(core, todo[i::workers], args.scratch, args.dom) for i in range(workers)])
        found = dict(pair for part in parts for pair in part)
    body = {"core": {"package": core.version, "registry": core.registry, "release": core.release_version},
            "projection": "scratch" if args.scratch else "repository",
            "swapped": _changed_names(Path(projection.__file__).read_text(encoding="utf-8"),
                                      args.scratch.read_text(encoding="utf-8")) if args.scratch else [],
            "wall_time_s": round(time.monotonic() - started, 1),
            "runs": {c: found[c] for c in todo}}
    text = json.dumps(body, indent=1, sort_keys=True) + "\n"
    if args.out:
        Path(args.out).write_text(text, encoding="utf-8")
    print(text[:4000])


if __name__ == "__main__":
    main()
