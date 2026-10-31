"""P0 probe -- incomplete withholding on core v60 (evidence only, no production edit).

For each withholding family the engine reads (Form W-2 box 2; Forms 1099-INT,
1099-DIV, 1099-R and 1099-G box 4; Form SSA-1099 box 6) this records what lines
25a, 25b, 25d, 33, 35a and 37 do on the committed core v60 / registry v58 /
release v58 when the family is incomplete in each way the charter names.

Run from the repository root:

    python3 docs/phases/engine-breadth/milestones/withholding-closure-evidence/probe.py

Synthetic ``demo.*`` ids only. Writes ``probe-output.json`` beside itself; no
absolute path is written into it. Every run goes through ``live_coordinate_run``
(via the 1099-K milestone's ``_run_on`` helper, which finishes the log, hands
the Social Security chain over and calls the coordinator).
"""

from __future__ import annotations

import copy
import json
import re
import sys
from pathlib import Path
from typing import Any, Callable, cast

REPO = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(REPO))

from tests.test_form_1099_k_income import _run_on  # noqa: E402
from tests.test_form_1099_withholding import (  # noqa: E402
    DIV_B4_FAMILY,
    G_B4_CLOSURE,
    G_B4_FAMILY,
    INT_B4_FAMILY,
    IRA_B4_FAMILY,
    SSA_B6_CLOSURE,
    SSA_B6_FAMILY,
    YEAR,
    _act,
    _attested,
    _base,
    _dividends,
    _interest,
    _retirements,
    _social_security,
    _social_security_withholding,
    _unemployment,
    _unemployment_withholding,
)

HERE = Path(__file__).resolve().parent
OUT_PATH = HERE / "probe-output.json"
_PATH = re.compile(r"(?:/Users|/private|/tmp|/var|/opt)[^\s'\"\\]*")

L25A = "tax.us.2025.payments.line25a"
L25B = "tax.us.2025.payments.line25b"
L25D = "tax.us.2025.payments.line25d"
L33 = "tax.us.2025.payments.line33"
L35A = "tax.us.2025.payments.line35a-refunded"
L37 = "tax.us.2025.payments.line37-amount-owed"
LINES = (
    ("25a", L25A, "form1040-line25a"),
    ("25b", L25B, "form1040-line25b"),
    ("25d", L25D, "form1040-line25d"),
    ("33", L33, "form1040-line33"),
    ("35a", L35A, "form1040-line35a"),
    ("37", L37, "form1040-line37"),
)
SUBTOTALS = (
    "tax.us.2025.interest.b4-withholding-subtotal",
    "tax.us.2025.dividends.b4-withholding-subtotal",
    "tax.us.2025.ira.box4-withholding-subtotal",
    "tax.us.2025.unemployment.b4-withholding-subtotal",
    "tax.us.2025.ssa1099.b6-withholding-subtotal",
)

W2_FAMILY = "tax.us.2025.w2"
W2_B2_FAMILY = "tax.us.2025.w2-box2"
W2_B2_CLOSURE = "tax.us.2025.w2-box2.source-closure"
W2_B2 = "tax.us.2025.w2.box2-withholding"
W2_B1 = "tax.us.2025.w2.box1-wages"


# --- closure manipulation ------------------------------------------------------


def _payload(act: dict[str, object]) -> dict[str, Any]:
    return cast(dict[str, Any], act["payload"])


def _horizons(acts: list[dict[str, object]], family_id: str) -> list[str]:
    """Genesis horizon, then each member-transition successor, in log order."""
    out: list[str] = []
    for act in acts:
        p = _payload(act)
        if act["kind"] == "horizon-genesis" and p["family"]["id"] == family_id:
            out.append(str(p["horizon_id"]))
        elif act["kind"] == "member-transition" and p["family"]["id"] == family_id:
            out.append(str(p["successor"]["id"]))
    return out


def _strip_closure(acts: list[dict[str, object]], closure_type: str) -> list[dict[str, object]]:
    kept = []
    for act in acts:
        finding = _payload(act).get("finding")
        if isinstance(finding, dict) and str(finding.get("fact_id", "")).startswith(closure_type + "|"):
            continue
        kept.append(act)
    return kept


def _set_closure(acts: list[dict[str, object]], family_id: str, closure_type: str, mode: str) -> list[dict[str, object]]:
    """mode: none (unanswered) | head (true at the current horizon) | first (true at the
    horizon after the first recorded member, so any later member leaves it stale)."""
    out = _strip_closure(acts, closure_type)
    horizons = _horizons(out, family_id)
    if mode == "none":
        return out
    horizon = horizons[-1] if mode == "head" else horizons[1]
    closure = _act(len(out), "assertion", {
        "finding": _attested("demo.p0.closure." + family_id + "." + mode,
                             f"{closure_type}|family-horizon={horizon},tax-year={YEAR}", True),
    })
    if mode == "head":
        out.append(closure)
        return out
    # "first": the closure must be recorded while its horizon is current, i.e. straight
    # after the act that created it; the next member then advances the horizon past it.
    # (A closure recorded later against a superseded horizon is refused as an unknown fact.)
    for index, act in enumerate(out):
        p = _payload(act)
        if act["kind"] == "member-transition" and p["family"]["id"] == family_id and str(p["successor"]["id"]) == horizon:
            out.insert(index + 1, closure)
            return out
    raise AssertionError("first-member horizon not found")


# --- returns -------------------------------------------------------------------

AMOUNTS: dict[str, tuple[float, float]] = {"g": (600.0, 400.0), "ssa": (800.0, 500.0), "int": (50.0, 30.0),
                                           "div": (40.0, 20.0), "ira": (1200.0, 800.0)}
CLOSURES: dict[str, tuple[str, str]] = {
    "g": (G_B4_FAMILY, G_B4_CLOSURE),
    "ssa": (SSA_B6_FAMILY, SSA_B6_CLOSURE),
    "int": (INT_B4_FAMILY, "tax.us.2025.f1099int.b4.source-closure"),
    "div": (DIV_B4_FAMILY, "tax.us.2025.f1099div.b4.source-closure"),
    "ira": (IRA_B4_FAMILY, "tax.us.2025.f1099r.box4.source-closure"),
}


def _build_box4(family: str, n: int, amounts: list[float | None]) -> list[dict[str, object]]:
    """A return with ``n`` statements of ``family`` (each with its income box), box-4/6
    amounts per ``amounts`` (None records no amount), the family's closure left unanswered,
    and every other withholding family closed empty."""
    acts = _base(wages=50000.0, w2_withheld=4500.0)
    if family == "g":
        _unemployment(acts, [6000.0, 4000.0][:n], authority=None)
        _unemployment_withholding(acts, amounts, close=False)
        _social_security_withholding(acts, [])
    elif family == "ssa":
        _social_security(acts, [12000.0, 8000.0][:n], witness=None)
        _unemployment_withholding(acts, [])
        _social_security_withholding(acts, amounts, close=False)
    else:
        statements = list(zip([500.0, 300.0][:n] if family != "ira" else [10000.0, 5000.0][:n], amounts))
        {"int": _interest, "div": _dividends, "ira": _retirements}[family](acts, statements)
        _unemployment_withholding(acts, [])
        _social_security_withholding(acts, [])
    return acts


def _box4_case(family: str, cause: str) -> list[dict[str, object]]:
    a, b = AMOUNTS[family]
    fam_id, closure = CLOSURES[family]
    spec: dict[str, tuple[int, list[float | None], str]] = {
        # cause: (statements, amounts, closure mode)
        "a-unanswered": (2, [a, None], "none"),
        "a-answered": (2, [a, None], "head"),
        "b-unanswered": (1, [None], "none"),
        "b-answered": (1, [None], "head"),
        "c-empty": (1, [], "none"),
        "c-one-amount": (1, [a], "none"),
        "stale": (2, [a, b], "first"),
        "d-control": (2, [a, b], "head"),
    }
    n, amounts, mode = spec[cause]
    acts = _build_box4(family, n, amounts)
    return _set_closure(acts, fam_id, closure, mode)


def _w2_second_slip(acts: list[dict[str, object]], *, box2: float | None) -> list[dict[str, object]]:
    """A second W-2 (box 1 as a member of the W-2 box 1 family; box 2 a plain assertion)."""
    out = copy.deepcopy(acts)
    head = _horizons(out, W2_FAMILY)[-1]
    out = _strip_closure(out, "tax.us.2025.w2.source-closure")
    employer, slip, new_head = "demo.p0.w2b.employer", "demo.p0.w2b.slip", "demo.p0.w2.h2"

    def add(kind: str, payload: dict[str, object]) -> None:
        out.append(_act(len(out), kind, payload))

    add("entity-introduced", {"entity": {"schema": "entity.v1", "id": employer, "kind": "tax.us.employer", "label": "Synthetic"}})
    add("entity-introduced", {"entity": {"schema": "entity.v1", "id": slip, "kind": "tax.us.w2-slip", "label": "Synthetic"}})
    ident = f"employer={employer},w2-slip={slip},tax-year={YEAR}"
    family_version = next(str(_payload(a)["family"]["version"]) for a in out
                          if a["kind"] == "horizon-genesis" and _payload(a)["family"]["id"] == W2_FAMILY)
    add("member-transition", {
        "family": {"id": W2_FAMILY, "version": family_version},
        "scope": {"tax-year": YEAR, "subject": "demo.primary"},
        "member": {"action": "assert", "finding": _attested("demo.p0.w2b.box1", f"{W2_B1}|{ident}", 20000.0)},
        "successor": {"id": new_head, "predecessor": head},
    })
    add("assertion", {"finding": _attested("demo.p0.w2.reclose", f"tax.us.2025.w2.source-closure|family-horizon={new_head},tax-year={YEAR}", True)})
    if box2 is not None:
        add("assertion", {"finding": _attested("demo.p0.w2b.box2", f"{W2_B2}|{ident}", box2)})
    return out


def _drop_base_box2(acts: list[dict[str, object]]) -> list[dict[str, object]]:
    kept = []
    for act in acts:
        finding = _payload(act).get("finding")
        if isinstance(finding, dict) and str(finding.get("fact_id", "")).startswith(W2_B2 + "|"):
            continue
        kept.append(act)
    return kept


def _w2_case(cause: str) -> list[dict[str, object]]:
    base = _base(wages=50000.0, w2_withheld=4500.0)
    _unemployment_withholding(base, [])
    _social_security_withholding(base, [])
    if cause == "a-unanswered":   # two W-2s, one box 2; box-2 closure unanswered
        acts = _w2_second_slip(base, box2=None)
        mode = "none"
    elif cause == "a-answered":   # two W-2s, one box 2; box-2 closure true
        acts = _w2_second_slip(base, box2=None)
        mode = "head"
    elif cause == "b-unanswered":  # one W-2 with no box 2 answer; closure unanswered
        acts = _drop_base_box2(base)
        mode = "none"
    elif cause == "b-answered":    # one W-2 with no box 2 answer; closure true
        acts = _drop_base_box2(base)
        mode = "head"
    elif cause == "c-one-amount":  # box 2 recorded for the only W-2; closure unanswered
        acts = base
        mode = "none"
    elif cause == "d-control":
        acts = _w2_second_slip(base, box2=1200.0)
        mode = "head"
    else:
        raise KeyError(cause)
    return _set_closure(acts, W2_B2_FAMILY, W2_B2_CLOSURE, mode)


# --- multi-family and joint returns --------------------------------------------


def _all_families(*, closed: set[str], joint: bool = False, drop: str | None = None) -> list[dict[str, object]]:
    """One return with withholding in every box-4 family (and W-2 box 2).

    ``closed`` names the families whose closure is attested at the final horizon;
    any other family is left unanswered. ``drop`` omits the last amount of that family
    (its second statement records no amount). Joint returns carry two statements per family
    so each spouse's is present.
    """
    acts = _base(wages=80000.0 if joint else 50000.0, w2_withheld=7000.0 if joint else 4500.0, joint=joint)
    _unemployment(acts, [5000.0, 4000.0], authority=None)
    _unemployment_withholding(acts, [500.0, None if drop == "g" else 400.0], close=False)
    _social_security(acts, [12000.0, 8000.0], witness=None)
    _social_security_withholding(acts, [800.0, None if drop == "ssa" else 500.0], close=False)
    _interest(acts, [(500.0, 50.0), (300.0, None if drop == "int" else 30.0)])
    _dividends(acts, [(400.0, 40.0), (200.0, None if drop == "div" else 20.0)])
    _retirements(acts, [(10000.0, 1200.0), (5000.0, None if drop == "ira" else 800.0)])
    for key, (fam_id, closure) in CLOSURES.items():
        acts = _set_closure(acts, fam_id, closure, "head" if key in closed else "none")
    return acts


ALL = {"g", "ssa", "int", "div", "ira"}


# --- running -------------------------------------------------------------------


def redact(text: str) -> str:
    return _PATH.sub("[path]", text)


def _cell(symbol: str, token: str, pubs: dict[str, Any], blocked: list[dict[str, Any]]) -> str:
    if symbol in pubs:
        return "published " + str(pubs[symbol]["value"])
    for row in blocked:
        if str(row.get("artifact_id", "")).endswith("rule." + token):
            return f"blocked {row.get('code')} missing={json.dumps(list(row.get('missing') or []))}"
    return "absent (no disposition row)"


def _run(acts: list[dict[str, object]], run_id: str) -> dict[str, Any]:
    try:
        pubs, blocked = _run_on(acts, run_id, "v60")
    except Exception as exc:  # a refusal is evidence
        return {"status": "error", "error": redact(f"{type(exc).__name__}: {exc}")[:600]}
    roots = [
        {"artifact_id": str(r["artifact_id"]), "code": r["code"], "missing": list(r.get("missing") or [])}
        for r in blocked if r["code"] != "DEPENDENCY_ABSENT"
    ]
    return {
        "status": "ran",
        "lines": {label: _cell(sym, tok, pubs, blocked) for label, sym, tok in LINES},
        "subtotals": {s: (str(pubs[s]["value"]) if s in pubs else None) for s in SUBTOTALS},
        "root_blocks": roots,
        "blocked_count": len(blocked),
    }


def main() -> None:
    cases: list[dict[str, Any]] = []

    def record(family: str, cause: str, build: Callable[[], list[dict[str, object]]]) -> None:
        run_id = f"demo.p0.wc.{family}.{cause}"
        print("run", run_id, flush=True)
        cases.append({"family": family, "cause": cause, "run_id": run_id, **_run(build(), run_id)})
        OUT_PATH.write_text(json.dumps({"core": "v60", "cases": cases}, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    control = _base(wages=50000.0, w2_withheld=4500.0)
    _unemployment_withholding(control, [])
    _social_security_withholding(control, [])
    record("none", "no-withholding-anywhere", lambda: control)
    record("w2", "base-one-w2-complete", lambda: control)
    for cause in ("a-unanswered", "a-answered", "b-unanswered", "b-answered", "c-one-amount", "d-control"):
        record("w2", cause, lambda c=cause: _w2_case(c))
    for joint in (False, True):
        tag = "joint" if joint else "single"
        record("all", f"{tag}-every-family-complete", lambda j=joint: _all_families(closed=ALL, joint=j))
        record("all", f"{tag}-only-1099g-unanswered", lambda j=joint: _all_families(closed=ALL - {"g"}, joint=j))
        record("all", f"{tag}-g-one-amount-omitted-closure-true", lambda j=joint: _all_families(closed=ALL, joint=j, drop="g"))
        record("all", f"{tag}-g-one-amount-omitted-closure-unanswered", lambda j=joint: _all_families(closed=ALL - {"g"}, joint=j, drop="g"))
    record("all", "single-int-and-g-both-unanswered", lambda: _all_families(closed=ALL - {"g", "int"}))
    record("all", "single-nothing-answered", lambda: _all_families(closed=set()))
    for family in ("g", "ssa", "int", "div", "ira"):
        for cause in ("a-unanswered", "a-answered", "b-unanswered", "b-answered", "c-empty", "c-one-amount", "stale", "d-control"):
            record(family, cause, lambda f=family, c=cause: _box4_case(f, c))


if __name__ == "__main__":
    main()
