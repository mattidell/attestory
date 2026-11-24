"""P0 trace: who is asked the separated-spouse question, on the live coordinator.

Evidence for docs/phases/engine-breadth/milestones/eic-separated-married.md.
P0 of eic-separated-married.

Builds synthetic demo.* returns with the other-dependents return builder and
the head-of-household probe's completion (each loaded by path under a unique
name) and runs each once through live_coordinate_run. Wages are 7000.

``hoh-married`` answers the head-of-household tests yes and the earned-income
credit not-married question no. ``hoh-unmarried`` answers that question yes.
Married filing separately adopts the separate-return spouse answers the
published builder needs. The standard-deduction apart fact stays yes and is
not the credit's separated-spouse test.

``apart`` and ``writing`` both record separated-spouse yes. The published
question collapses the two statutory prongs, and "not married", into that one
yes. ``no`` records no. ``ssn`` is one qualifying child with a valid SSN.
``nossn`` is one qualifying child without one. ``none`` is no qualifying child.
Every child lived with the filer for more than half the year and meets the
age test.

A question counts as asked when the answer publication pins that fact.
Supplied answers stay on the return either way.

Run: python3 probe.py [--core v102 | --core-json core.json] [--only KEY] [--out FILE]
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
h = _load("esm_p0_audit_harness", MILESTONES / "sale-family-audit-evidence/audit_harness.py")
base = _load("esm_p0_hoh_probe", MILESTONES / "hoh-qualifying-person-evidence/probe.py")
hand = _load("esm_p0_hand", HERE / "hand.py")

from packages.derivation.live import live_coordinate_run  # noqa: E402
from tests import test_other_dependents_credit_track1 as odc  # noqa: E402
from tests import test_w2g_gambling as w2g  # noqa: E402
from tests.helpers import current_core_returns as ccr  # noqa: E402
from tests.test_form_1099_withholding import _social_security_withholding, _unemployment_withholding  # noqa: E402
from tests.test_refund_or_amount_owed_track1 import _act, _attested  # noqa: E402

P = h.P
STATUS = {
    "hoh-married": "head_of_household",
    "hoh-unmarried": "head_of_household",
    "mfs": "married_filing_separately",
}
SSN_CHILD = "demo-esm-child-ssn"
NOSSN_CHILD = "demo-esm-child-nossn"
EIC_RES = P + "eic.child.residency"
SEP = P + "eic.separated-spouse"
NOT_MARRIED = P + "eic.not-married"
HOH_TESTS = P + "hoh.tests-met"
CORE_BUNDLE = json.loads((h.CONTENT / "core_calculations.bundle.v4.json").read_text())["id"]
STEP4 = (
    P + "eic.age-25-under-65",
    P + "eic.main-home-in-us",
    P + "eic.not-claimable-as-dependent",
    P + "eic.not-qualifying-child-of-another",
)
ASK = {
    "separated-spouse": SEP,
    "not-married": NOT_MARRIED,
    "age": P + "eic.age-25-under-65",
    "main-home": P + "eic.main-home-in-us",
    "not-claimable": P + "eic.not-claimable-as-dependent",
    "not-qc": P + "eic.not-qualifying-child-of-another",
}
ANSWER_SYMBOL = {
    "separated-spouse": "eic.answer.separated-spouse",
    "not-married": "eic.answer.not-married",
    "age": "eic.answer.age-25-under-65",
    "main-home": "eic.answer.main-home-in-us",
    "not-claimable": "eic.answer.not-claimable-as-dependent",
    "not-qc": "eic.answer.not-qualifying-child-of-another",
}
SYMBOLS = (
    "eic.status-class",
    "eic.column-count",
    "eic.qualifying-child-present",
    "eic.answer.separated-spouse",
    "eic.answer.not-married",
    "eic.gate-result",
    "eic.worksheet-a.line-6",
    "eic.eligibility-result",
    "payments.line27a",
)
WATCH = ("form1040.line-11", "form1040.line-15", "form1040.line-27a")


def keys() -> list[str]:
    found = []
    for status in ("hoh-married", "hoh-unmarried", "mfs"):
        found.append(f"{status}/none")
        for kids in ("ssn", "nossn"):
            for sep in ("apart", "writing", "no"):
                found.append(f"{status}/{kids}/{sep}")
    return found


KEYS = keys()


def _set_fact(acts: h.Acts, fact_type: str, child: str, value: str) -> None:
    prefix = f"{fact_type}|child={child},"
    hit = 0
    for act in acts:
        finding = (act.get("payload") or {}).get("finding") or {}
        if str(finding.get("fact_id", "")).startswith(prefix):
            finding["value"] = value
            hit += 1
    assert hit == 1, (fact_type, child, hit)


def build(key: str, content: Path = h.CONTENT) -> h.Acts:
    status_key, kids, *rest = key.split("/")
    sep = rest[0] if rest else "no"
    assert not rest or rest == [sep]
    assert kids in ("ssn", "nossn", "none")
    children: dict[str, dict[str, str]] = {}
    if kids == "ssn":
        children[SSN_CHILD] = odc.ctc_child()
    elif kids == "nossn":
        children[NOSSN_CHILD] = odc.odc_child_itin()
    answers = {fact: "yes" for fact in STEP4}
    acts = odc.build(
        wages=float(hand.WAGES),
        filing_status=STATUS[status_key],
        children=children,
        return_answers=answers,
    )
    if kids == "ssn":
        _set_fact(acts, EIC_RES, SSN_CHILD, "yes")
    elif kids == "nossn":
        _set_fact(acts, EIC_RES, NOSSN_CHILD, "yes")
    if children:
        acts.append(_act(len(acts), "bundle-adoption", {"bundle": ccr._load("dtb-questions.bundle.json")}))
        for name in children:
            for question, value in ccr._TIE_BREAKER_ANSWERS.items():
                fid = f"{P}dtb.child.{question}|child={name},tax-year={h.YEAR}"
                acts.append(_act(len(acts), "assertion", {
                    "finding": _attested(f"demo.esm.dtb.{question}.{name}", fid, value),
                }))
    acts = base._complete(acts, min(500.0, hand.WAGES * 0.05))
    _unemployment_withholding(acts, [])
    _social_security_withholding(acts, [])
    w2g._w2g(acts, [])
    acts = ccr.state_taxpayer_facts(acts, core="v88")
    acts = base._sale_families_closed(acts, content)
    if status_key == "mfs":
        adopted = {
            str(((a.get("payload") or {}).get("bundle") or {}).get("version"))
            for a in acts if a.get("kind") == "bundle-adoption"
            and ((a.get("payload") or {}).get("bundle") or {}).get("id") == CORE_BUNDLE
        }
        if "v4" not in adopted:
            h._add(acts, "bundle-adoption", {"bundle": json.loads((content / "core_calculations.bundle.v4.json").read_text())})
        for fact in ("spouse-over-65", "spouse-blind", "standard-deduction.spouse-separate-condition"):
            acts = h.say(acts, P + fact, False, "esm-" + fact, content)
        acts = h.say(acts, P + "mfs-lived-apart-all-year", "yes", "esm-mfs-apart", content)
    if status_key == "hoh-married":
        acts = h.say(acts, HOH_TESTS, "yes", "esm-hoh-tests", content)
        acts = h.say(acts, NOT_MARRIED, "no", "esm-not-married", content)
    if status_key == "hoh-unmarried":
        acts = h.say(acts, HOH_TESTS, "yes", "esm-hoh-tests", content)
        acts = h.say(acts, NOT_MARRIED, "yes", "esm-not-married", content)
    acts = h.say(acts, SEP, "yes" if sep in ("apart", "writing") else "no", "esm-separated", content)
    return h.renumber(acts)


def _assertion_ids(acts: h.Acts, fact_type: str) -> set[str]:
    """Content ids of assertions of ``fact_type``. A conditional answer pins that id only when it reads the fact."""
    prefix = fact_type + "|"
    found: set[str] = set()
    for act in acts:
        finding = (act.get("payload") or {}).get("finding") or {}
        fact_id = str(finding.get("fact_id") or "")
        if fact_id == fact_type or fact_id.startswith(prefix):
            ident = finding.get("id")
            if isinstance(ident, str):
                found.add(ident)
    return found


def _subject_child(symbol: str) -> str | None:
    marker = "|child="
    if marker not in symbol:
        return None
    return symbol.split(marker, 1)[1].split(",", 1)[0]


def observe(core: Any, key: str) -> dict[str, Any]:
    acts = build(key, core.content)
    asserted = {label: _assertion_ids(acts, fact) for label, fact in ASK.items()}
    run_id = "demo.esm.p0." + key.replace("/", ".")
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
        if fid not in WATCH:
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
    children: dict[str, dict[str, Any]] = {}
    for name in ("eic.child.counts", "eic.child.qualifies"):
        for row in rows_for(name):
            symbol = next(symbol for symbol, rows in by_symbol.items() if row in rows)
            child = _subject_child(symbol) or name
            children.setdefault(child, {})[name] = base.num(row.get("value"))
    blocked = sorted({
        str(row.get("artifact_id")).removeprefix(P + "rule.") + ":" + str(row.get("code"))
        for row in report.get("dispositions") or [] if row.get("disposition") == "blocked"
    })
    credit = lines.get("form1040.line-27a", {})
    return {
        "stop": report.get("stop_reason"),
        "credit": credit.get("value"),
        "credit_disposition": credit.get("disposition"),
        "agi": (lines.get("form1040.line-11") or {}).get("value"),
        "symbols": symbols,
        "asked": asked,
        "children": children,
        "blocked_rules": blocked,
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
        row["source"] = hand.decide(key)
        if "credit" in row:
            row["credit_equals_source"] = row["credit"] == row["source"]["credit"]
            row["asked_matches_source"] = (
                row.get("asked", {}).get("separated-spouse") is row["source"]["ask_separated"]
                and row.get("asked", {}).get("not-married") is row["source"]["ask_not_married"]
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
        "mfs_standard_deduction_lived_apart": "yes on every married-filing-separately return; not the credit's separated-spouse test",
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
            "class": (row.get("symbols") or {}).get("eic.status-class"),
            "column": (row.get("symbols") or {}).get("eic.column-count"),
            "present": (row.get("symbols") or {}).get("eic.qualifying-child-present"),
            "gate": (row.get("symbols") or {}).get("eic.gate-result"),
            "line6": (row.get("symbols") or {}).get("eic.worksheet-a.line-6"),
            "asked": row.get("asked"),
            "match": row.get("credit_equals_source"),
            "asked_match": row.get("asked_matches_source"),
            "error": row.get("error") or row.get("refusal"),
            "blocked": row.get("blocked_rules"),
        }
        for key, row in body["runs"].items()
    }
    print(json.dumps({
        "core": body["core"],
        "wall_time_s": body["wall_time_s"],
        "credit_equals_source": body["credit_equals_source"],
        "asked_matches_source": body["asked_matches_source"],
        "errors": body["errors"],
        "runs": brief,
    }, indent=1))


if __name__ == "__main__":
    main()
