"""P0 trace: a married filer whose child has no valid SSN, on the live coordinator.

Evidence for docs/phases/engine-breadth/milestones/eic-no-ssn-child.md.
Charter: docs/reviews/eic-no-ssn-child/charter-p0.md.

Builds synthetic demo.* returns with the other-dependents return builder and
the head-of-household probe's completion (each loaded by path under a unique
name) and runs each once through live_coordinate_run. Wages are 7000.
A head of household return answers the head-of-household tests yes and answers
the earned-income-credit not-married question no (the filer is married).
Married filing separately adopts the separate-return spouse answers the
published builder needs; the standard-deduction apart fact stays yes and is
not the credit's separated-spouse test.

``apart`` and ``writing`` both record separated-spouse yes. The published
question collapses the two statutory prongs into that one yes. ``no`` records
no. ``more`` and ``less`` are whether the child lived with the filer more than
half the year. ``mm`` ``ml`` ``lm`` ``ll`` are the SSN child then the no-SSN
child. ``age-no`` fails the credit's age test for the no-SSN child.

A question counts as asked when the answer publication pins that fact.
Supplied answers stay on the return either way.

Run: python3 probe.py [--core v101 | --core-json core.json] [--only KEY] [--out FILE]
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
h = _load("ens_p0_audit_harness", MILESTONES / "sale-family-audit-evidence/audit_harness.py")
base = _load("ens_p0_hoh_probe", MILESTONES / "hoh-qualifying-person-evidence/probe.py")
hand = _load("ens_p0_hand", HERE / "hand.py")

from packages.derivation.live import live_coordinate_run  # noqa: E402
from tests import test_other_dependents_credit_track1 as odc  # noqa: E402
from tests import test_w2g_gambling as w2g  # noqa: E402
from tests.helpers import current_core_returns as ccr  # noqa: E402
from tests.test_form_1099_withholding import _social_security_withholding, _unemployment_withholding  # noqa: E402
from tests.test_refund_or_amount_owed_track1 import _act, _attested  # noqa: E402

P = h.P
STATUS = {
    "hoh": "head_of_household", "mfs": "married_filing_separately",
    "single": "single", "qss": "qualifying_surviving_spouse", "mfj": "married_filing_jointly",
    "uhoh": "head_of_household",
}
SSN_CHILD = "demo-ens-child-ssn"
NOSSN_CHILD = "demo-ens-child-nossn"
EIC_AGE = P + "eic.child.age"
EIC_RES = P + "eic.child.residency"
SEP = P + "eic.separated-spouse"
NOT_MARRIED = P + "eic.not-married"
HOH_TESTS = P + "hoh.tests-met"
CORE_BUNDLE = json.loads((h.CONTENT / "core_calculations.bundle.v4.json").read_text())["id"]
STEP4 = (P + "eic.age-25-under-65", P + "eic.main-home-in-us")
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
    "eic.status-class", "eic.column-count", "eic.table-key", "eic.qualifying-child-count", "eic.qualifying-child-present",
    "eic.early-stop", "eic.questions-required", "eic.answer.separated-spouse", "eic.answer.not-married",
    "eic.answer.age-25-under-65", "eic.answer.main-home-in-us", "eic.answer.not-claimable-as-dependent",
    "eic.answer.not-qualifying-child-of-another", "eic.gate-result", "eic.worksheet-a.line-6",
    "eic.eligibility-result", "payments.line27a",
)
WATCH = ("form1040.line-11", "form1040.line-15", "form1040.line-27a")
RULES = (
    "eic-child.counts", "eic-child.qualifies", "eic-qualifying-child-count", "eic-qualifying-child-present",
    "eic-column-count", "eic-status-class", "eic-early-stop", "eic-questions-required",
    "eic-answer.separated-spouse", "eic-answer.not-married", "eic-answer.age-25-under-65",
    "eic-answer.main-home-in-us", "eic-answer.not-claimable-as-dependent",
    "eic-answer.not-qualifying-child-of-another", "eic-gate-result",
)


def keys() -> list[str]:
    found = []
    for status in ("hoh", "mfs"):
        for kids in ("ssn", "nossn"):
            for sep in ("apart", "writing", "no"):
                for lived in ("more", "less"):
                    found.append(f"{status}/{kids}/{sep}/{lived}")
        for sep in ("apart", "writing", "no"):
            for lived in ("mm", "ml", "lm", "ll"):
                found.append(f"{status}/both/{sep}/{lived}")
        found.append(f"{status}/nossn/apart/more/age-no")
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
    status_key, kids, sep, lived, *rest = key.split("/")
    age_no = rest == ["age-no"]
    assert not rest or age_no
    children: dict[str, dict[str, str]] = {}
    if kids in ("ssn", "both"):
        children[SSN_CHILD] = odc.ctc_child()
    if kids in ("nossn", "both"):
        children[NOSSN_CHILD] = odc.odc_child_itin()
    answers = {fact: "yes" for fact in STEP4}
    acts = odc.build(
        wages=float(hand.WAGES), filing_status=STATUS[status_key], children=children, return_answers=answers,
    )
    if kids in ("ssn", "both"):
        _set_fact(acts, EIC_RES, SSN_CHILD, "yes" if lived[0] == "m" else "no")
    if kids in ("nossn", "both"):
        more = lived == "more" if kids == "nossn" else lived[1] == "m"
        _set_fact(acts, EIC_RES, NOSSN_CHILD, "yes" if more else "no")
        if age_no:
            _set_fact(acts, EIC_AGE, NOSSN_CHILD, "no")
    if children:
        acts.append(_act(len(acts), "bundle-adoption", {"bundle": ccr._load("dtb-questions.bundle.json")}))
        for name in children:
            for question, value in ccr._TIE_BREAKER_ANSWERS.items():
                fid = f"{P}dtb.child.{question}|child={name},tax-year={h.YEAR}"
                acts.append(_act(len(acts), "assertion", {
                    "finding": _attested(f"demo.ens.dtb.{question}.{name}", fid, value),
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
            acts = h.say(acts, P + fact, False, "ens-" + fact, content)
        acts = h.say(acts, P + "mfs-lived-apart-all-year", "yes", "ens-mfs-apart", content)
    if status_key == "mfj":
        for fact in ("spouse-over-65", "spouse-blind"):
            acts = h.say(acts, P + fact, False, "ens-" + fact, content)
    if status_key == "hoh":
        acts = h.say(acts, HOH_TESTS, "yes", "ens-hoh-tests", content)
        acts = h.say(acts, NOT_MARRIED, "no", "ens-not-married", content)
    if status_key == "uhoh":
        acts = h.say(acts, HOH_TESTS, "yes", "ens-hoh-tests", content)
        acts = h.say(acts, NOT_MARRIED, "yes", "ens-not-married", content)
    if status_key == "qss":
        acts = h.say(acts, P + "qss.tests-met", "yes", "ens-qss-tests", content)
    acts = h.say(acts, SEP, "yes" if sep in ("apart", "writing") else "no", "ens-separated", content)
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
    run_id = "demo.ens.p0." + key.replace("/", ".")
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
    rules = {}
    for row in report.get("dispositions") or []:
        aid = str(row.get("artifact_id") or "")
        short = aid.removeprefix(P + "rule.")
        if short in RULES and short not in rules:
            rules[short] = row.get("disposition")
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
        "rules": rules,
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


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--core", default="v101")
    parser.add_argument("--core-json")
    parser.add_argument("--only", action="append")
    parser.add_argument("--workers", type=int, default=max(1, min(8, (os.cpu_count() or 2) - 1)))
    parser.add_argument("--out")
    args = parser.parse_args()
    core = base.core_from(args)
    todo = args.only or list(KEYS)
    unknown = [key for key in todo if key not in KEYS and key.split("/")[0] not in STATUS]
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
            "source": (row.get("source") or {}).get("credit"),
            "class": (row.get("symbols") or {}).get("eic.status-class"),
            "column": (row.get("symbols") or {}).get("eic.column-count"),
            "present": (row.get("symbols") or {}).get("eic.qualifying-child-present"),
            "asked": row.get("asked"),
            "error": row.get("error") or row.get("refusal"),
        }
        for key, row in body["runs"].items()
    }
    print(json.dumps({"core": body["core"], "wall_time_s": body["wall_time_s"],
                      "credit_equals_source": body["credit_equals_source"], "errors": body["errors"],
                      "runs": brief}, indent=1))


if __name__ == "__main__":
    main()
