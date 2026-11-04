"""P0 trace: scope answers on core v73, through live_coordinate_run.

Nothing under packages/ or tests/ is edited. Synthetic demo.* data only.
Run from the repository root:

    python3 docs/phases/engine-breadth/milestones/derived-answers-evidence/probe.py

Writes probe-output.json beside itself. Cases already in that file are kept.
"""
from __future__ import annotations

import copy
import json
import sys
from pathlib import Path
from typing import Any, Callable

REPO = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(REPO))

from tests import test_input_questions as miq  # noqa: E402
from tests import test_other_dependents_credit_track1 as odc  # noqa: E402
from tests import test_statement_withholding_answer as swa  # noqa: E402
from tests import test_w2g_gambling as w2g  # noqa: E402
from tests.helpers import current_core_returns as ccr  # noqa: E402
from tests.test_form_1099_withholding import (  # noqa: E402
    _social_security_withholding,
    _unemployment_withholding,
)
from tests.test_scope_answer_questions import GROUPS  # noqa: E402

HERE = Path(__file__).resolve().parent
OUT = HERE / "probe-output.json"
P = "tax.us.2025."
CORE = "v73"
swa.CORES[CORE] = (
    "package.core-calculations.v73.json", "v73",
    "demo.release.sli-worksheet-integration.2025.v71.json", "v71",
    "published-packages.v71.json",
)

SCOPE = P + "f1098-scope.no-mortgage-statement"
INT = P + "line2a-scope.no-f1099int-tax-exempt"
OID = P + "line2a-scope.no-f1099oid-tax-exempt"
OD = P + "ctc.no-other-dependent"
F1116 = P + "direct-ftc-scope.no-form-1116-required"
EXC = (
    P + "exception1.only-box2a-capital-gains",
    P + "exception1.no-capital-losses",
    P + "exception1.no-qof-deferral",
    P + "exception1.no-boxes-2b-2c-2d",
)
# Above both the single standard deduction (15,750) and the joint one (30,000),
# so a recorded Form 1098 moves line 12e off the standard deduction.
MORTGAGE = 40000.0
CG_DIST = P + "capital-gain-distributions"
WATCH = (
    "deductions.line-12e",
    "schedule-a.line8a",
    "tax-exempt-interest.line2a-total",
    "interest.b8-tax-exempt-subtotal",
    "ctc.sch8812.line-6",
    "odc.dependent-present",
    "odc.child-count",
    "odc.child-marked-conflict",
    "schedule3.line1-direct-ftc",
    "schedule-d-required.conclusion",
    "capital-gains.line7a-total",
    "payments.line35a-refunded",
    "payments.line37-amount-owed",
    "payments.line34-overpayment",
)
RULES = (
    "form1040-line12e",
    "form1040-line2a",
    "ctc-sch8812-line-6",
    "odc-dependent-present",
    "odc-child-marked-conflict",
    "odc-relative-marked-conflict",
    "schedule3-line1-direct-ftc",
    "schedule-d-required.conclusion",
    "form1040-line7a",
)
QUESTIONS = {
    "m1": "Did you receive a Form 1098",
    "l2a": "tax-exempt interest on a Form 1099-INT",
    "oid": "Form 1099-OID",
    "ctc": "besides the children you counted",
    "ftc": "Form 1116",
    "exc": "capital gain distributions in box 2a",
}


def _drop(acts: list[dict[str, object]], *facts: str) -> list[dict[str, object]]:
    return miq.drop(acts, *facts)


def _complete_odc(acts: list[dict[str, object]]) -> list[dict[str, object]]:
    acts = odc._complete(acts)
    _unemployment_withholding(acts, [])
    _social_security_withholding(acts, [])
    w2g._w2g(acts, [])
    return acts


def _odc(answer: str | None) -> list[dict[str, object]]:
    """One marked other-dependent child, roster closed, tie-breaker answered.

    The per-child count reads the tie-breaker. Without those answers the
    roster is marked and the credit still does not publish, which hides the
    line the scope answer holds.
    """
    answers: dict[str, str | None] = {}
    if answer is not None:
        answers[OD] = answer
    child = "demo-child-odc"
    acts = odc.build(wages=50000.0, children={child: odc.odc_child()}, return_answers=answers)
    acts.append(ccr._act(len(acts), "bundle-adoption", {"bundle": ccr._load("dtb-questions.bundle.json")}))
    for question, value in ccr._TIE_BREAKER_ANSWERS.items():
        fid = f"{P}dtb.child.{question}|child={child},tax-year=2025"
        acts.append(ccr._act(
            len(acts), "assertion",
            {"finding": ccr._attested(f"demo.p0.dtb.{question}.{child}", fid, value)}))
    if answer is None:
        acts = _drop(acts, OD)
    return _complete_odc(acts)


def case_table() -> list[tuple[str, str, Callable[[], list[dict[str, object]]]]]:
    """(run id, question key, builder)."""
    base = ccr.base_return
    return [
        ("base", "", base),
        ("m1-silent", "m1", lambda: _drop(base(), SCOPE)),
        ("m1-proved-unanswered", "m1", lambda: _drop(ccr.add_mortgage_itemizer(base(), MORTGAGE), SCOPE)),
        ("m1-agreed", "m1", lambda: ccr.add_mortgage_itemizer(base(), MORTGAGE)),
        ("m1-contradict", "m1", lambda: _set(ccr.add_mortgage_itemizer(base(), MORTGAGE), SCOPE, True)),
        ("m1-joint-proved-unanswered", "m1", lambda: _drop(
            ccr.add_mortgage_itemizer(w2g._w2g_return([], joint=True), MORTGAGE), SCOPE)),
        ("l2a-silent", "l2a", lambda: _drop(base(), INT)),
        ("l2a-proved-unanswered", "l2a", lambda: _drop(
            ccr.add_tax_exempt_interest_1099int(base(), [125.0]), INT)),
        ("l2a-agreed", "l2a", lambda: ccr.add_tax_exempt_interest_1099int(base(), [125.0])),
        ("l2a-contradict", "l2a", lambda: _set(
            ccr.add_tax_exempt_interest_1099int(base(), [125.0]), INT, "yes")),
        ("l2a-zero-unanswered", "l2a", lambda: _drop(
            ccr.add_tax_exempt_interest_1099int(base(), [0.0]), INT)),
        ("ctc-silent", "ctc", lambda: _drop(base(), OD)),
        ("ctc-proved-unanswered", "ctc", lambda: _odc(None)),
        ("ctc-agreed", "ctc", lambda: _odc("no")),
        ("ctc-contradict", "ctc", lambda: _odc("yes")),
        ("ftc-under-unanswered", "ftc", lambda: _drop(ccr.add_foreign_tax_1099div(base(), [30.0]), F1116)),
        ("ftc-over-unanswered", "ftc", lambda: _drop(ccr.add_foreign_tax_1099div(base(), [400.0]), F1116)),
        ("ftc-under-yes", "ftc", lambda: ccr.add_foreign_tax_1099div(base(), [30.0])),
        ("ftc-over-yes", "ftc", lambda: ccr.add_foreign_tax_1099div(base(), [400.0])),
        ("ftc-under-no", "ftc", lambda: _set(ccr.add_foreign_tax_1099div(base(), [30.0]), F1116, "no")),
        ("exc-silent", "exc", lambda: _drop(base(), *EXC)),
        # The base absence answer refuses a box 2a member. Flip that declaration
        # first so the statement can be recorded, then withhold the four facts.
        ("exc-box2a-unanswered", "exc", lambda: _drop(
            ccr._record_members(_set(base(), CG_DIST, "yes"), P + "f1099div.2a", [40.0], tag="b2a"), *EXC)),
        ("oid-silent", "oid", lambda: _drop(base(), OID)),
        ("oid-box1-unanswered", "oid", lambda: _drop(
            ccr._record_members(base(), P + "f1099oid.b1", [75.0], tag="oid1"), OID)),
    ]


def _set(acts: list[dict[str, object]], fact: str, value: object) -> list[dict[str, object]]:
    out = copy.deepcopy(acts)
    w2g._set_answer(out, fact, value)
    return out


def _fact_values(acts: list[dict[str, object]], facts: tuple[str, ...]) -> dict[str, list[Any]]:
    found: dict[str, list[Any]] = {fact: [] for fact in facts}
    for act in acts:
        finding = act.get("payload", {}).get("finding")  # type: ignore[union-attr]
        if not isinstance(finding, dict):
            continue
        fid = str(finding.get("fact_id", "")).split("|")[0]
        if fid in found:
            found[fid].append(finding.get("value"))
    return {key.replace(P, ""): values for key, values in found.items()}


def _closures(acts: list[dict[str, object]]) -> list[str]:
    names: set[str] = set()
    for act in acts:
        finding = act.get("payload", {}).get("finding")  # type: ignore[union-attr]
        if not isinstance(finding, dict):
            continue
        fid = str(finding.get("fact_id", "")).split("|")[0]
        if fid.endswith("source-closure") or fid.endswith(".closure"):
            names.add(fid.replace(P, ""))
    return sorted(names)


def summarize(run: swa.Run, question: str) -> dict[str, Any]:
    blocked = miq.blocked(run.model)
    asked = sorted(
        line for line, reasons in blocked.items()
        if reasons and any(question in sentence for sentence in reasons)
    ) if question else []
    pubs = {}
    for symbol, finding in run.pubs.items():
        short = symbol.replace(P, "")
        if short in WATCH or any(short.endswith(token) for token in WATCH):
            pubs[short] = finding.get("value")
    rows = []
    for row in run.dispositions:
        artifact = str(row.get("artifact_id", "")).replace(P + "rule.", "")
        if artifact in RULES and row.get("disposition") != "computed":
            rows.append({
                "rule": artifact,
                "disposition": row.get("disposition"),
                "code": row.get("code"),
                "missing": [str(item).replace(P, "") for item in row.get("missing", []) or []],
            })
    return {
        "blocked": len(blocked),
        "asked": asked,
        "lines": pubs,
        "held": rows,
    }


def readers() -> dict[str, list[str]]:
    """Current v73 computation rules whose text names each candidate fact."""
    package = json.loads((ccr.CONTENT / "package.core-calculations.v73.json").read_text(encoding="utf-8"))
    index: dict[tuple[str, str], dict[str, Any]] = {}
    for path in ccr.CONTENT.glob("*.json"):
        try:
            body = json.loads(path.read_text(encoding="utf-8"))
        except ValueError:
            continue
        if isinstance(body, dict) and "id" in body and "version" in body:
            index[(str(body["id"]), str(body["version"]))] = body
    facts = (SCOPE, INT, OID, OD, F1116, *EXC)
    found = {fact: [] for fact in facts}
    for member in package["members"]:
        if member.get("role") != "computation":
            continue
        body = index.get((member["id"], member["version"]))
        if body is None:
            continue
        text = json.dumps(body)
        for fact in facts:
            if fact in text:
                found[fact].append(f"{member['id'].replace(P, '')}@{member['version']}")
    return {key.replace(P, ""): sorted(value) for key, value in found.items()}


def families() -> list[dict[str, str]]:
    package = json.loads((ccr.CONTENT / "package.core-calculations.v73.json").read_text(encoding="utf-8"))
    members = {(m["id"], m["version"]) for m in package["members"]}
    rows = []
    for path in sorted(ccr.CONTENT.glob("family*.json")):
        try:
            body = json.loads(path.read_text(encoding="utf-8"))
        except ValueError:
            continue
        if not isinstance(body, dict) or (body.get("id"), body.get("version")) not in members:
            continue
        if not str(body.get("schema", "")).startswith("source-family"):
            continue
        predicate = body.get("member_predicate") or {}
        rows.append({
            "family": str(body.get("id", "")).replace(P, ""),
            "member": str(predicate.get("fact_type", "")).replace(P, ""),
        })
    return rows


def polarities() -> list[dict[str, str]]:
    rows = []
    for gid, _text, members in GROUPS:
        for fact, pol, ret in members:
            rows.append({"question": gid, "fact": fact, "polarity": pol, "return": ret})
    return rows


def run_case(run_id: str, question: str, builder: Callable[[], list[dict[str, object]]]) -> dict[str, Any]:
    try:
        acts = builder()
        watched = (SCOPE, INT, OID, OD, F1116, *EXC)
        result = swa.run(acts, f"demo.p0.da.{run_id}", CORE)
        summary = summarize(result, QUESTIONS.get(question, "___"))
        summary["recorded"] = _fact_values(acts, watched)
        summary["closures"] = [
            name for name in _closures(acts)
            if name.startswith("f1098") or "b8" in name or "2a" in name or "oid" in name
            or "child-roster" in name or "f1099div.7" in name or name.endswith("f1099div.7.source-closure")
        ]
        summary["status"] = "ran"
        return {"run_id": run_id, **summary}
    except Exception as exc:
        # The exception text only. A traceback would carry this machine's paths.
        return {
            "run_id": run_id,
            "status": "error",
            "error": f"{type(exc).__name__}: {exc}",
        }


def main() -> None:
    done: dict[str, Any] = {}
    payload: dict[str, Any] = {"core": CORE, "readers": {}, "families": [], "polarities": [], "cases": []}
    if OUT.exists():
        payload = json.loads(OUT.read_text(encoding="utf-8"))
        done = {row["run_id"]: row for row in payload.get("cases", [])}
    payload["readers"] = readers()
    payload["families"] = families()
    payload["polarities"] = polarities()
    cases = []
    for run_id, question, builder in case_table():
        if run_id in done and done[run_id].get("status") == "ran":
            row = done[run_id]
        else:
            row = run_case(run_id, question, builder)
            print(run_id, row["status"], row.get("asked"), row.get("lines"), flush=True)
        cases.append(row)
        payload["cases"] = cases
        OUT.write_text(json.dumps(payload, indent=1) + "\n", encoding="utf-8")
    print("wrote", OUT.name, flush=True)


if __name__ == "__main__":
    main()
