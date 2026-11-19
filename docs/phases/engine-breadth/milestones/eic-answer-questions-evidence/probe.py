"""P0 probe: what a filer sees when an earned income credit answer is missing (eic-answer-questions).

Evidence for docs/phases/engine-breadth/milestones/eic-answer-questions.md.
Charter: docs/reviews/eic-answer-questions/charter-p0.md.

Builds synthetic demo.* returns with the hoh-eic probe's return builder (its
probe.py, loaded by path under a unique name; that builder answers every
credit answer honestly), then removes the recorded answers a case names, so
each case leaves those answers unanswered (nothing is pre-filled for them).
Each list runs once through the real ``live_coordinate_run``; the saved page
is rendered with the real renderer and every value is read from the model
embedded in that page.

A case is ``<status>/<dependents>/<wages>[/<hoh answer>]`` plus the answers
removed (``-`` for none). Short names:

  age     tax.us.2025.eic.age-25-under-65          (Step 4 question 2)
  home    tax.us.2025.eic.main-home-in-us          (Step 4 question 3)
  notdep  tax.us.2025.eic.not-claimable-as-dependent (Step 4 question 6)
  spssn   tax.us.2025.eic.spouse-valid-ssn         (Step 1 question 2, spouse)
  tpssn, nra, notqc, unsup   the four answers v99 already asks (controls)
  childage, childres  the counted child's tax.us.2025.eic.child.age or
            tax.us.2025.eic.child.residency roster answer

Run: python3 probe.py [--core v99 | --core-json core.json] [--out FILE]
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
base = _load("eicq_p0_hoh_eic_probe", MILESTONES / "hoh-eic-evidence/probe.py")
h = base.h

from packages.derivation.live import live_coordinate_run  # noqa: E402
from packages.derivation.live_session import _render_page  # noqa: E402

P = h.P
FACTS = {
    "age": P + "eic.age-25-under-65",
    "home": P + "eic.main-home-in-us",
    "notdep": P + "eic.not-claimable-as-dependent",
    "spssn": P + "eic.spouse-valid-ssn",
    "tpssn": P + "eic.taxpayer-valid-ssn",
    "nra": P + "eic.not-nonresident-alien",
    "notqc": P + "eic.not-qualifying-child-of-another",
    "unsup": P + "eic.no-unsupported-situations",
    "childage": P + "eic.child.age",
    "childres": P + "eic.child.residency",
}
UNASKED = ("age", "home", "notdep", "spssn")
CASES: tuple[tuple[str, str], ...] = (
    ("single/none/7000", "-"), ("single/none/7000", "age"), ("single/none/7000", "home"),
    ("single/none/7000", "notdep"), ("single/none/7000", "age,home,notdep"),
    ("single/none/7000", "tpssn"), ("single/none/7000", "nra"), ("single/none/7000", "notqc"),
    ("single/none/7000", "unsup"),
    ("single/none/16000", "age"), ("single/none/50000", "age,home,notdep"),
    ("qss/none/16000", "-"), ("qss/none/16000", "age"), ("qss/none/16000", "home"), ("qss/none/16000", "notdep"),
    ("hoh/parent/7000/yes", "-"), ("hoh/parent/7000/yes", "age"), ("hoh/parent/7000/yes", "home"),
    ("hoh/parent/7000/yes", "notdep"), ("hoh/parent/7000/yes", "age,home,notdep"),
    ("hoh/parent/7000/no", "age,home,notdep"),
    ("mfj/none/16000", "-"), ("mfj/none/16000", "age"), ("mfj/none/16000", "home"), ("mfj/none/16000", "spssn"),
    ("mfj/none/16000", "age,home,spssn"),
    ("mfj/child/30000", "-"), ("mfj/child/30000", "spssn"),
    ("single/child/30000", "age,home,notdep"), ("single/child/30000", "childage"),
    ("single/child/30000", "childres"),
    ("mfs/none/7000", "age,home,notdep"),
)
WATCH = base.WATCH
SYMBOLS = ("eic.status-class", "eic.column-count", "eic.questions-required", "eic.answer.age-25-under-65",
           "eic.answer.main-home-in-us", "eic.answer.not-claimable-as-dependent", "eic.answer.spouse-valid-ssn",
           "eic.gate-result", "eic.eligibility-result", "payments.line27a")


def case_id(key: str, removed: str) -> str:
    return f"{key}/-{removed}" if removed != "-" else f"{key}/answered"


def drop(acts: h.Acts, facts: list[str]) -> h.Acts:
    """Remove every recorded assertion of the named fact types (all keys)."""
    kept = []
    for act in acts:
        finding = (act.get("payload") or {}).get("finding") or {}
        if any(str(finding.get("fact_id", "")).startswith(fact + "|") for fact in facts):
            continue
        kept.append(act)
    return h.renumber(kept)


def build(key: str, removed: str, content: Path = h.CONTENT) -> h.Acts:
    parts = key.split("/")
    answer = parts[3] if len(parts) > 3 else "none"
    acts = base.build("/".join(parts[:3]), content, answer)
    names = [] if removed == "-" else removed.split(",")
    facts = [FACTS[n] for n in names]
    before = len(acts)
    acts = drop(acts, facts)
    if names and len(acts) >= before:
        # A fact the builder never recorded is not "removed"; say so rather than call it unanswered.
        raise AssertionError(f"{key}: nothing removed for {removed}")
    return acts


num = base.num


def observe(core: Any, key: str, removed: str) -> dict[str, Any]:
    acts = build(key, removed, core.content)
    run_id = "demo.eicq.p0." + case_id(key, removed).replace("/", ".").replace(",", "-")
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
    silent: list[str] = []
    for section in saved.get("sections") or []:
        field = section.get("field") or {}
        fid = str(field.get("id") or "").removeprefix(P)
        resolved = section.get("resolved") or {}
        said = []
        for name in ("questions", "reasons", "blocked_reasons"):
            for item in resolved.get(name) or []:
                sentence = str(item.get("sentence") or item.get("text") or "") if isinstance(item, dict) else str(item)
                if sentence.strip():
                    said.append(h.scrub(sentence)[:2000])
        for sentence in said:
            if sentence not in sentences:
                sentences.append(sentence)
        if resolved.get("disposition") == "blocked" and not said:
            silent.append(fid)
        if fid in WATCH:
            row: dict[str, Any] = {"disposition": resolved.get("disposition"), "value": num(resolved.get("value"))}
            if resolved.get("disposition") != "computed":
                row["said"] = [s[:160] for s in said[:4]]
            lines[fid] = row
    rows = report.get("dispositions") or []
    blocked = sorted({str(r.get("artifact_id")).removeprefix(P + "rule.") + ":" + str(r.get("code"))
                      for r in rows if r.get("disposition") == "blocked"})
    answers = set(FACTS.values())
    roots = sorted({str(m).removeprefix(P) for r in rows if r.get("disposition") == "blocked"
                    and r.get("code") == "DEPENDENCY_ABSENT" for m in (r.get("missing") or []) if str(m) in answers})
    pubs = {str(p.finding.get("symbol")): num(p.finding.get("value")) for p in outcome.publications or ()}
    return {"stop": report.get("stop_reason"), "lines": lines,
            "symbols": {s: pubs.get(P + s) for s in SYMBOLS}, "blocked_rules": blocked,
            "missing_answers_named": roots, "blocked_page_lines_without_sentence": silent,
            "sentences": [s[:300] for s in sentences[:16]]}


def _worker(args: tuple[Any, list[tuple[str, str]]]) -> list[tuple[str, dict[str, Any]]]:
    core, cases = args
    out = []
    for key, removed in cases:
        try:
            out.append((case_id(key, removed), observe(core, key, removed)))
        except Exception as exc:  # noqa: BLE001 - a rejected list is a result
            out.append((case_id(key, removed), {"error": type(exc).__name__, "message": h.scrub(str(exc))[:500]}))
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
    parser.add_argument("--core", default="v99")
    parser.add_argument("--core-json")
    parser.add_argument("--only", action="append", help="a case id, e.g. single/none/7000/-age")
    parser.add_argument("--workers", type=int, default=max(1, min(9, (os.cpu_count() or 2) - 1)))
    parser.add_argument("--out")
    args = parser.parse_args()
    core = core_from(args)
    todo = [c for c in CASES if not args.only or case_id(*c) in args.only]
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
            "runs": {case_id(*c): found[case_id(*c)] for c in todo}}
    text = json.dumps(body, indent=1, sort_keys=True) + "\n"
    if args.out:
        Path(args.out).write_text(text, encoding="utf-8")
    print(text[:6000])


if __name__ == "__main__":
    main()
