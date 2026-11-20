"""P0 probe: what a filer sees when a counted dependent is missing a per-member answer (eic-child-answers).

Evidence for docs/phases/engine-breadth/milestones/eic-child-answers.md.
Charter: docs/reviews/eic-child-answers/charter-p0.md.

Builds synthetic demo.* returns with the hoh-eic probe's helpers (its probe.py,
loaded by path under a unique name): wages, the standard deduction, withholding
5% of wages up to 500, every return-level credit answer honest, one or two
children on the earned income, child tax credit and tie-breaker rosters (every
per-child answer honest), or one child on the other-dependent child roster, or
one dependent parent on the other-dependent relative roster. Then it removes
one per-member answer for one member, so that answer is unanswered (nothing is
pre-filled). Each list runs once through the real ``live_coordinate_run``; the
saved page is rendered with the real renderer and every value is read from the
model embedded in that page.

For every blocked page line the probe walks the run's disposition rows as the
projection's question walk does (``missing`` names through blocked rows of the
same symbol) and records each root tuple (artifact, code, missing name) where
the walk stops.

A case is ``<status>/<roster>/<wages>`` plus ``-`` (nothing removed) or
``<answer>@<member>``. Rosters: ``kid1`` and ``kid2`` (one or two children
under 17, counted for both credits), ``odckid`` (a 17-year-old child, the
credit for other dependents), ``parent`` (a dependent parent, the relative
roster). Members are named demo-eicc-child-1, demo-eicc-child-2 and
demo-eicc-parent-1.

Run: python3 probe.py [--core v100 | --core-json core.json] [--only CASE] [--out FILE]
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
hoh_eic = _load("eicc_p0_hoh_eic_probe", MILESTONES / "hoh-eic-evidence/probe.py")
h = hoh_eic.h
hqp = hoh_eic.base
odc = hoh_eic.odc
ccr = hoh_eic.ccr
_act = hoh_eic._act
_attested = hoh_eic._attested

from packages.derivation.live import live_coordinate_run  # noqa: E402
from packages.derivation.live_session import _render_page  # noqa: E402

P = h.P
STATUS = hoh_eic.STATUS
CHILD = ("demo-eicc-child-1", "demo-eicc-child-2")
PARENT = "demo-eicc-parent-1"
# Short name -> (fact type, key name). Per-member answers only; the roster membership facts
# (eic.child.relationship, ctc.child.claimed-as-dependent, odc.child.other-dependent-box,
# odc.dependent.other-dependent-box) are the members themselves and are not removable answers.
ANSWERS = {
    "age": (P + "eic.child.age", "child"),
    "res": (P + "eic.child.residency", "child"),
    "joint": (P + "eic.child.joint-return", "child"),
    "ssn": (P + "eic.child.ssn", "child"),
    "dtb-another": (P + "dtb.child.another-could-claim", "child"),
    "dtb-filer-parent": (P + "dtb.child.filer-is-parent", "child"),
    "u17": (P + "ctc.child.under-17", "child"),
    "lived": (P + "ctc.child.lived-with-you", "child"),
    "support": (P + "ctc.child.no-over-half-support", "child"),
    "citizen": (P + "ctc.child.citizen-or-resident", "child"),
    "odc-tin": (P + "odc.child.tin", "child"),
    "rel-relationship": (P + "odc.dependent.relationship", "dependent"),
    "rel-notqc": (P + "odc.dependent.not-qualifying-child", "dependent"),
    "rel-gross": (P + "odc.dependent.gross-income-under-limit", "dependent"),
    "rel-support": (P + "odc.dependent.over-half-support", "dependent"),
    "rel-tin": (P + "odc.dependent.tin", "dependent"),
    "rel-citizen": (P + "odc.dependent.citizen-or-resident", "dependent"),
    "rel-notjoint": (P + "odc.dependent.not-joint-return", "dependent"),
}
KID = ("age", "res", "joint", "ssn", "dtb-another", "dtb-filer-parent", "u17", "lived", "support", "citizen")
CASES: tuple[str, ...] = (
    "single/kid1/30000/-", "single/kid2/30000/-", "mfj/kid1/30000/-",
    *(f"single/kid1/30000/{a}@1" for a in KID),
    *(f"single/kid2/30000/{a}@2" for a in KID),
    "mfj/kid1/30000/age@1", "mfj/kid1/30000/joint@1",
    "single/odckid/30000/-", "single/odckid/30000/odc-tin@1", "single/odckid/30000/ssn@1",
    "single/odckid/30000/lived@1", "single/odckid/30000/joint@1",
    "single/parent/30000/-",
    *(f"single/parent/30000/{a}@p" for a in ANSWERS if a.startswith("rel-")),
)
WATCH = ("form1040.line-19", "form1040.line-24", "form1040.line-27a", "form1040.line-28", "form1040.line-33",
         "form1040.line-34", "form1040.line-35a", "form1040.line-37", "form.eic-worksheet-a.line-2",
         "form.eic-worksheet-a.line-5", "form.eic-worksheet-a.line-6")
SYMBOLS = ("eic.qualifying-child-count", "eic.column-count", "eic.gate-result", "eic.eligibility-result",
           "payments.line27a", "ctc.child-count", "odc.child-count", "odc.relative-count", "ctc.form1040-line19",
           "tax.total-tax")


def build(case: str, content: Path = h.CONTENT) -> h.Acts:
    status_key, roster, wages_text, removed = case.split("/")
    wages = float(wages_text)
    status = STATUS[status_key]
    kids: dict[str, dict[str, str]] = {}
    if roster in ("kid1", "kid2"):
        kids = {name: odc.ctc_child() for name in CHILD[: int(roster[-1])]}
    elif roster == "odckid":
        kids = {CHILD[0]: odc.odc_child()}  # 17: fails the under-17 test, claimed for the other-dependent credit
    rels = {PARENT: odc.relative()} if roster == "parent" else {}
    answers: dict[str, str | None] = {fact: "yes" for fact in hoh_eic.STEP4_ANSWERS}
    if not kids:
        answers[P + "eic.no-qualifying-child"] = "yes"
    acts = odc.build(wages=wages, filing_status=status, children=kids, relatives=rels, return_answers=answers)
    if roster == "odckid":
        for act in acts:  # 17 or older and not a student: fails the credit's age test, not counted
            finding = (act.get("payload") or {}).get("finding") or {}
            if str(finding.get("fact_id", "")).startswith(hoh_eic.EIC_AGE + "|"):
                finding["value"] = "no"
    if kids:
        acts.append(_act(len(acts), "bundle-adoption", {"bundle": ccr._load("dtb-questions.bundle.json")}))
        for name in kids:
            for question, value in ccr._TIE_BREAKER_ANSWERS.items():
                fid = f"{P}dtb.child.{question}|child={name},tax-year={h.YEAR}"
                acts.append(_act(len(acts), "assertion", {"finding": _attested(f"demo.eicc.dtb.{question}.{name}", fid, value)}))
    acts = hqp._complete(acts, min(500.0, wages * 0.05))
    hoh_eic._unemployment_withholding(acts, [])
    hoh_eic._social_security_withholding(acts, [])
    hoh_eic.w2g._w2g(acts, [])
    acts = ccr.state_taxpayer_facts(acts, core="v88")
    acts = hqp._sale_families_closed(acts, content)
    if status == "married_filing_jointly":
        for fact in ("spouse-over-65", "spouse-blind"):
            acts = h.say(acts, P + fact, False, "eicc-" + fact, content)
    acts = h.renumber(acts)
    if removed != "-":
        acts = drop(acts, removed)
    return acts


def member_name(where: str) -> str:
    return PARENT if where == "p" else CHILD[int(where) - 1]


def drop(acts: h.Acts, removed: str) -> h.Acts:
    """Remove the one member's assertion(s) of the named answer; refuse when nothing was there to remove."""
    short, where = removed.split("@")
    fact, key = ANSWERS[short]
    marker = f"{key}={member_name(where)},"
    kept = [a for a in acts if not (str(((a.get("payload") or {}).get("finding") or {}).get("fact_id", ""))
                                    .startswith(fact + "|") and marker in str(((a.get("payload") or {}).get("finding") or {}).get("fact_id", "")))]
    if len(kept) == len(acts):
        raise AssertionError(f"nothing removed for {removed}")
    return h.renumber(kept)


def short(name: Any) -> str:
    return str(name).replace(P, "")


_SYMBOLS: dict[str, dict[str, str]] = {}


def rule_symbols(content: Path) -> dict[str, str]:
    """Rule id -> the symbol it publishes, from every rule file in the content directory."""
    key = str(content)
    if key not in _SYMBOLS:
        found: dict[str, str] = {}
        for path in sorted(content.glob("*.json")):
            try:
                body = json.loads(path.read_text(encoding="utf-8"))
            except ValueError:
                continue
            if isinstance(body, dict) and body.get("publishes"):
                found[str(body["id"])] = str(body["publishes"])
        _SYMBOLS[key] = found
    return _SYMBOLS[key]


def roots_of(row: dict[str, Any], by_symbol: dict[str, list[dict[str, Any]]]) -> list[tuple[str, str, str]]:
    """The (artifact, code, missing name) tuples where the projection's walk stops for this row.

    A missing name with blocked rows of its own is followed; a name with none is a root. This is the
    walk of ``presentation_projection._closure_question_reasons`` without the question lookups.
    """
    found: set[tuple[str, str, str]] = set()
    seen: set[int] = set()

    def walk(current: dict[str, Any]) -> None:
        if id(current) in seen:
            return
        seen.add(id(current))
        missing = current.get("missing") or []
        if not missing:
            found.add((short(current.get("artifact_id")), str(current.get("code")), "(none)"))
        for item in missing:
            blocked = [r for r in by_symbol.get(str(item), []) if r.get("disposition") == "blocked"]
            if blocked:
                for r in blocked:
                    walk(r)
            else:
                found.add((short(current.get("artifact_id")), str(current.get("code")), short(item)))

    walk(row)
    return sorted(found)


def observe(core: Any, case: str) -> dict[str, Any]:
    acts = build(case, core.content)
    run_id = "demo.eicc.p0." + case.replace("/", ".").replace("@", "-at-")
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
    rows = report.get("dispositions") or []
    publishes = rule_symbols(core.content)
    by_symbol: dict[str, list[dict[str, Any]]] = {}
    for r in rows:
        sym = r.get("symbol") or publishes.get(r.get("artifact_id"))
        if sym is None:
            raise AssertionError(f"no symbol for {r.get('artifact_id')}")
        by_symbol.setdefault(str(sym), []).append(r)
    lines: dict[str, Any] = {}
    silent: list[str] = []
    asked: list[str] = []
    root_tuples: dict[str, list[list[str]]] = {}
    sentences: list[str] = []
    for section in saved.get("sections") or []:
        field = section.get("field") or {}
        fid = short(field.get("id"))
        resolved = section.get("resolved") or {}
        said = []
        for name in ("questions", "reasons", "blocked_reasons"):
            for item in resolved.get(name) or []:
                sentence = str(item.get("sentence") or item.get("text") or "") if isinstance(item, dict) else str(item)
                if sentence.strip():
                    said.append(h.scrub(sentence))
        for sentence in said:
            if sentence not in sentences:
                sentences.append(sentence)
        if resolved.get("disposition") == "blocked":
            (asked if said else silent).append(fid)
            symbol = str(field.get("binds_symbol"))
            line_rows = [r for r in by_symbol.get(symbol, []) if r.get("disposition") == "blocked"]
            tuples = sorted({t for r in line_rows for t in roots_of(r, by_symbol)})
            root_tuples[fid] = [list(t) for t in tuples]
        if fid in WATCH:
            row: dict[str, Any] = {"disposition": resolved.get("disposition"), "value": hoh_eic.num(resolved.get("value"))}
            if resolved.get("disposition") != "computed":
                row["said"] = [s[:200] for s in said[:4]]
            lines[fid] = row
    blocked_rules = sorted({short(r.get("artifact_id")).removeprefix("rule.") + ":" + str(r.get("code"))
                            for r in rows if r.get("disposition") == "blocked"})
    member_rows = sorted({(short(r.get("artifact_id")), str(r.get("code")), short(r.get("symbol")),
                           ",".join(short(m) for m in r.get("missing") or []))
                          for r in rows if r.get("disposition") == "blocked" and "|" in str(r.get("symbol") or "")})
    distinct_roots = sorted({tuple(t) for ts in root_tuples.values() for t in ts})
    pubs = {str(p.finding.get("symbol")): hoh_eic.num(p.finding.get("value")) for p in outcome.publications or ()}
    return {"stop": report.get("stop_reason"), "lines": lines,
            "symbols": {s: pubs.get(P + s) for s in SYMBOLS},
            "blocked_rules": blocked_rules,
            "blocked_page_lines_without_sentence": sorted(silent),
            "blocked_page_lines_with_sentence": sorted(asked),
            "root_tuples": [list(t) for t in distinct_roots],
            "blocked_member_rows": [list(t) for t in member_rows],
            "sentences": [s[:400] for s in sentences[:16]]}


def _worker(args: tuple[Any, list[str]]) -> list[tuple[str, dict[str, Any]]]:
    core, cases = args
    out = []
    for case in cases:
        try:
            out.append((case, observe(core, case)))
        except Exception as exc:  # noqa: BLE001 - a rejected list is a result
            out.append((case, {"error": type(exc).__name__, "message": h.scrub(str(exc))[:500]}))
    return out


def core_from(args: argparse.Namespace) -> Any:
    if args.core_json:
        body = json.loads(Path(args.core_json).read_text(encoding="utf-8"))
        return h.Core(body["version"], body["registry"], body["release_version"], content=Path(body["content"]),
                      releases=Path(body["releases"]), loader_from=body.get("loader_from"))
    n = int(args.core[1:])
    return h.Core(args.core, f"v{n - 2}", f"v{n - 2}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--core", default="v100")
    parser.add_argument("--core-json")
    parser.add_argument("--only", action="append")
    parser.add_argument("--workers", type=int, default=max(1, min(9, (os.cpu_count() or 2) - 1)))
    parser.add_argument("--out")
    args = parser.parse_args()
    core = core_from(args)
    todo = [c for c in CASES if not args.only or c in args.only] if not args.only or set(args.only) <= set(CASES) \
        else list(args.only)
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
