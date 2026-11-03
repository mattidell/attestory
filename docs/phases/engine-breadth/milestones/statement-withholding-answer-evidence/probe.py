"""P0 probe -- a statement recorded without its withholding answer, on core v70 (evidence only).

For each family the engine reads on Form 1040 line 25b (Forms 1099-INT, 1099-DIV, 1099-R and
1099-G box 4; Form SSA-1099 box 6), and for Form W-2 box 2 (line 25a), this records what the
withholding lines and the bottom line do on the committed core v70 / registry v68 / release v68
when a statement is recorded without its answer, beside the same return with $0 answered.

Run from the repository root:

    python3 docs/phases/engine-breadth/milestones/statement-withholding-answer-evidence/probe.py

Every run goes through ``live_coordinate_run``. The returns are the withholding-closure
milestone's builders (``tests/test_withholding_closure.py``) on the v64 base, plus the W-2G
answers core v65 asks (``tests/test_w2g_gambling.py``): the base
``tests/helpers/current_core_returns.py`` (``base_return``) uses, which core v70 accepts.
Synthetic ``demo.*`` ids only. Writes ``probe-output.json`` beside itself; no absolute path.
"""

from __future__ import annotations

import copy
import json
import re
import sys
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any, Callable, cast

REPO = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(REPO))

from packages.derivation.live import live_coordinate_run  # noqa: E402
from packages.derivation.live_workspace import WorkspaceCapability  # noqa: E402
from packages.derivation.production_resolver import PublicationSurface  # noqa: E402
from tests import test_w2g_gambling as w2g  # noqa: E402
from tests.helpers import current_core_returns as cr  # noqa: E402
from tests.test_form_1099_k_income import _handover  # noqa: E402
from tests.test_form_1099_withholding import (  # noqa: E402
    DIV_B4_FAMILY,
    G_B4_FAMILY,
    INT_B4_FAMILY,
    IRA_B4_FAMILY,
    SSA_B6_FAMILY,
    YEAR,
    _act,
    _attested,
    _base,
    _dividends,
    _interest,
    _introduce,
    _retirements,
    _social_security,
    _social_security_withholding,
    _transition,
    _unemployment,
    _unemployment_withholding,
)
from tests.test_refund_or_amount_owed_track1 import _finish  # noqa: E402
from tests.test_withholding_closure import FAMILIES, _horizons, _set_closure, _strip_closure  # noqa: E402

HERE = Path(__file__).resolve().parent
OUT_PATH = HERE / "probe-output.json"
_PATH = re.compile(r"(?:/Users|/private|/tmp|/var|/opt)[^\s'\"\\]*")

CONTENT = cr.CONTENT
RELEASE_DIR = cr.RELEASE_DIR
# core -> (package file, package version, release file, release version, registry file)
CORES = {
    "v70": ("package.core-calculations.v70.json", "v70", "demo.release.sli-worksheet-integration.2025.v68.json", "v68", "published-packages.v68.json"),
}

L24 = "tax.us.2025.tax.line24-total-tax"
L25A = "tax.us.2025.payments.line25a"
L25B = "tax.us.2025.payments.line25b"
L25D = "tax.us.2025.payments.line25d"
L33 = "tax.us.2025.payments.line33"
L35A = "tax.us.2025.payments.line35a-refunded"
L37 = "tax.us.2025.payments.line37-amount-owed"
LINES = (("24", L24), ("25a", L25A), ("25b", L25B), ("25d", L25D), ("33", L33), ("35a", L35A), ("37", L37))
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
AMOUNTS = {"g": (600.0, 400.0), "ssa": (800.0, 500.0), "int": (50.0, 30.0), "div": (40.0, 20.0), "ira": (1200.0, 800.0)}
ALL = set(FAMILIES)


def _payload(act: dict[str, object]) -> dict[str, Any]:
    return cast(dict[str, Any], act["payload"])


# --- running (the shape of tests/test_attachment_limited_part.py ``run``) ------------


def run_core(acts: list[dict[str, object]], run_id: str, core: str = "v70") -> tuple[dict[str, Any], list[dict[str, Any]]]:
    package, version, release, rel_version, registry = CORES[core]
    surface = PublicationSurface(RELEASE_DIR, CONTENT / registry, CONTENT)
    finished = _handover(
        _finish(copy.deepcopy(acts), package_path=CONTENT / package, package_version=version,
                release_path=RELEASE_DIR / release, release_version=rel_version, note=run_id),
        surface=surface, reconfirm=True)
    with TemporaryDirectory() as tmp:
        outcome = live_coordinate_run(
            WorkspaceCapability(Path(tmp) / "L"), repo_root=REPO, authoritative_acts=finished,
            workspace_revision=len(finished), run_scope={"jurisdiction": "us", "year": YEAR},
            scope_user=cr.USER, request={"schema": "run-request.v1"}, run_id=run_id, governance_pins=[],
            surface=surface, output_name="out.json")
        if outcome.refusal is not None:
            raise AssertionError(f"refused: {outcome.refusal.reason} {outcome.refusal.detail}")
        pubs = {str(p.finding["symbol"]): p.finding for p in outcome.publications or ()}
        blocked: list[dict[str, Any]] = []
        if outcome.output_path is not None:
            report = json.loads(outcome.output_path.read_text(encoding="utf-8"))
            blocked = [r for r in report.get("dispositions", []) if r.get("disposition") == "blocked"]
    return pubs, blocked


def redact(text: str) -> str:
    return _PATH.sub("[path]", text)


def _cell(symbol: str, pubs: dict[str, Any]) -> str:
    return str(pubs[symbol]["value"]) if symbol in pubs else "blocked"


def summarize(acts: list[dict[str, object]], run_id: str, core: str = "v70") -> dict[str, Any]:
    try:
        pubs, blocked = run_core(acts, run_id, core)
    except Exception as exc:  # a refusal is evidence
        return {"status": "error", "error": redact(f"{type(exc).__name__}: {exc}")[:600]}
    roots = [
        {"artifact": str(r["artifact_id"]).replace("tax.us.2025.rule.", ""), "code": r["code"],
         "missing": [m.replace("tax.us.2025.", "") for m in (r.get("missing") or [])]}
        for r in blocked if r["code"] != "DEPENDENCY_ABSENT"
    ]
    return {
        "status": "ran",
        "lines": {label: _cell(sym, pubs) for label, sym in LINES},
        "subtotals": {s.replace("tax.us.2025.", ""): (str(pubs[s]["value"]) if s in pubs else None) for s in SUBTOTALS},
        "root_blocks": roots,
        # the disposition of the two withholding lines themselves, whatever its code
        "line_dispositions": {
            tok: {"code": r["code"], "missing": [m.replace("tax.us.2025.", "") for m in (r.get("missing") or [])]}
            for tok in ("form1040-line25a", "form1040-line25b")
            for r in blocked if str(r["artifact_id"]).endswith("rule." + tok)
        },
        "blocked_count": len(blocked),
    }


# --- returns -------------------------------------------------------------------------


def _finish_base(acts: list[dict[str, object]]) -> list[dict[str, object]]:
    """The v65 W-2G answers a core v70 return needs (no W-2G statement)."""
    w2g._w2g(acts, [])
    return acts


def family_return(key: str, n: int, amounts: list[float | None], *, joint: bool = False,
                  mode: str = "head") -> list[dict[str, object]]:
    """``n`` statements of one family (each with its income box), box 4/6 amounts per ``amounts``
    (None records no amount), that family's closure per ``mode``, every other withholding family
    closed empty. As ``tests/test_withholding_closure.py::_family_return``, on the v70 base."""
    acts = _base(wages=80000.0 if joint else 50000.0, w2_withheld=7000.0 if joint else 4500.0, joint=joint)
    if key == "g":
        _unemployment(acts, [6000.0, 4000.0][:n], authority=None)
        _unemployment_withholding(acts, amounts, close=False)
        _social_security_withholding(acts, [])
    elif key == "ssa":
        _social_security(acts, [12000.0, 8000.0][:n], witness=None)
        _unemployment_withholding(acts, [])
        _social_security_withholding(acts, amounts, close=False)
    else:
        income = [10000.0, 5000.0][:n] if key == "ira" else [500.0, 300.0][:n]
        {"int": _interest, "div": _dividends, "ira": _retirements}[key](acts, list(zip(income, amounts)))
        _unemployment_withholding(acts, [])
        _social_security_withholding(acts, [])
    acts = _set_closure(acts, key, mode)
    return _finish_base(acts)


def all_families(*, joint: bool = False, drop: str | tuple[str, ...] | None = None, zero: str | None = None) -> list[dict[str, object]]:
    """One return with two statements in every family, every closure attested at its horizon.
    ``drop`` records no amount for that family's second statement; ``zero`` records $0 there."""
    def second(key: str, value: float) -> float | None:
        dropped = drop if isinstance(drop, tuple) else (drop,)
        return None if key in dropped else (0.0 if zero == key else value)

    acts = _base(wages=80000.0 if joint else 50000.0, w2_withheld=7000.0 if joint else 4500.0, joint=joint)
    _unemployment(acts, [5000.0, 4000.0], authority=None)
    _unemployment_withholding(acts, [500.0, second("g", 400.0)], close=False)
    _social_security(acts, [12000.0, 8000.0], witness=None)
    _social_security_withholding(acts, [800.0, second("ssa", 500.0)], close=False)
    _interest(acts, [(500.0, 50.0), (300.0, second("int", 30.0))])
    _dividends(acts, [(400.0, 40.0), (200.0, second("div", 20.0))])
    _retirements(acts, [(10000.0, 1200.0), (5000.0, second("ira", 800.0))])
    for key in FAMILIES:
        acts = _set_closure(acts, key, "head")
    return _finish_base(acts)


def no_withholding() -> list[dict[str, object]]:
    acts = _base(wages=50000.0, w2_withheld=4500.0)
    _unemployment_withholding(acts, [])
    _social_security_withholding(acts, [])
    return _finish_base(acts)


def int_box4_on_a_statement_without_box1(*, second_answered: bool = False) -> list[dict[str, object]]:
    """Two 1099-INT statements with box 1, plus a third statement that has a box 4 answer and no
    box 1 recorded. With only the first answered the box 4 count (2) equals the box 1 count (2);
    with both answered the box 4 count (3) exceeds it."""
    acts = family_return("int", 2, [50.0, 30.0 if second_answered else None])
    head = _horizons(acts, INT_B4_FAMILY)[-1]
    keys = (("payer", "demo.p0.x.payer"), ("statement", "demo.p0.x.stmt"))
    _introduce(acts, "demo.p0.x.payer", "tax.us.interest-payer")
    _introduce(acts, "demo.p0.x.stmt", "tax.us.1099int-statement")
    _transition(acts, (INT_B4_FAMILY, "v1"), head, "demo.p0.x.h", "demo.p0.x.box4",
                "tax.us.2025.f1099int.box4-withholding", keys, 7.0)
    return _set_closure(acts, "int", "head")


# family key -> (box 4/6 family, its fact type, identity keys of the second statement the builders record)
SECOND_STATEMENT = {
    "int": (INT_B4_FAMILY, "tax.us.2025.f1099int.box4-withholding", (("payer", "demo.fw.int.payer.1"), ("statement", "demo.fw.int.stmt.1"))),
    "div": (DIV_B4_FAMILY, "tax.us.2025.f1099div.box4-withholding", (("payer", "demo.fw.div.payer.1"), ("statement", "demo.fw.div.stmt.1"))),
    "ira": (IRA_B4_FAMILY, "tax.us.2025.f1099r.ira-box4-withholding", (("payer", "demo.fw.r.payer.1"), ("statement", "demo.fw.r.stmt.1"))),
    "g": (G_B4_FAMILY, "tax.us.2025.f1099g.box4-withholding", (("payer", "demo.fw.g.payer.1"), ("statement", "demo.fw.g.stmt.1"))),
    "ssa": (SSA_B6_FAMILY, "tax.us.2025.ssa1099.box6-voluntary-withholding", (("statement", "demo.fw.ssa.stmt.1"),)),
}


def adopt_and_answer(key: str, *, reclose: bool) -> list[dict[str, object]]:
    """The two-statement return whose second statement has no box 4 answer, as a v70 workspace is
    adopted onto the successor and the filer then records that statement's $0 answer. The answer is
    a member-transition (it advances the box 4 family's horizon), so the closure attested before it
    is behind the horizon; ``reclose`` re-attests it at the new horizon."""
    a = AMOUNTS[key][0]
    acts = family_return(key, 2, [a, None])
    family, fact_type, keys = SECOND_STATEMENT[key]
    head = _horizons(acts, family)[-1]
    _transition(acts, (family, "v1"), head, "demo.p0.adopt.h", "demo.p0.adopt.box4", fact_type, keys, 0.0)
    return _set_closure(acts, key, "head") if reclose else acts


# --- Form W-2 box 2 (line 25a) --------------------------------------------------------


def _w2_second_slip(acts: list[dict[str, object]], *, box2: float | None) -> list[dict[str, object]]:
    """A second W-2 (box 1 a member of the W-2 box 1 family; box 2 a plain assertion)."""
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


def w2_case(cause: str) -> list[dict[str, object]]:
    base = no_withholding()
    if cause == "second-slip-no-box2":      # two W-2s, one box 2 answer
        acts = _w2_second_slip(base, box2=None)
    elif cause == "second-slip-zero":       # two W-2s, the second answered $0
        acts = _w2_second_slip(base, box2=0.0)
    elif cause == "second-slip-answered":   # two W-2s, both answered
        acts = _w2_second_slip(base, box2=1200.0)
    elif cause == "single-no-box2":         # one W-2, no box 2 answer
        acts = _drop_base_box2(base)
    elif cause == "base":
        acts = base
    else:
        raise KeyError(cause)
    return _set_closure_w2(acts, "head")


def _set_closure_w2(acts: list[dict[str, object]], mode: str) -> list[dict[str, object]]:
    out = _strip_closure(acts, W2_B2_CLOSURE)
    if mode == "none":
        return out
    horizon = _horizons(out, W2_B2_FAMILY)[-1]
    out.append(_act(len(out), "assertion", {
        "finding": _attested("demo.p0.w2.box2.closure", f"{W2_B2_CLOSURE}|family-horizon={horizon},tax-year={YEAR}", True)}))
    return out


def w2_zero_single() -> list[dict[str, object]]:
    """One W-2 whose box 2 is answered $0 (the base's box 2 set to zero)."""
    acts = copy.deepcopy(no_withholding())
    hits = 0
    for act in acts:
        finding = _payload(act).get("finding")
        if isinstance(finding, dict) and str(finding.get("fact_id", "")).startswith(W2_B2 + "|"):
            finding["value"] = 0.0
            hits += 1
    assert hits == 1, hits
    return acts


# --- main ----------------------------------------------------------------------------


def case_table() -> list[tuple[str, str, Callable[[], list[dict[str, object]]]]]:
    """(family, cause, builder) for every case, in run order."""
    table: list[tuple[str, str, Callable[[], list[dict[str, object]]]]] = [
        ("none", "no-withholding-anywhere", no_withholding)]
    for key in ("int", "div", "ira", "g", "ssa"):
        a, b = AMOUNTS[key]
        table += [
            (key, "one-statement-no-answer-closed", lambda k=key: family_return(k, 1, [None])),
            (key, "one-statement-zero-answered", lambda k=key: family_return(k, 1, [0.0])),
            (key, "one-statement-answered", lambda k=key, a=a: family_return(k, 1, [a])),
            (key, "two-statements-first-answered-second-not", lambda k=key, a=a: family_return(k, 2, [a, None])),
            (key, "two-statements-first-answered-second-zero", lambda k=key, a=a: family_return(k, 2, [a, 0.0])),
            (key, "two-statements-both-answered", lambda k=key, a=a, b=b: family_return(k, 2, [a, b])),
            (key, "joint-two-statements-second-not-answered", lambda k=key, a=a: family_return(k, 2, [a, None], joint=True)),
            (key, "joint-two-statements-both-answered", lambda k=key, a=a, b=b: family_return(k, 2, [a, b], joint=True)),
        ]
    for joint in (False, True):
        tag = "joint" if joint else "single"
        table.append(("all", f"{tag}-every-statement-answered", lambda j=joint: all_families(joint=j)))
        for key in ("int", "div", "ira", "g", "ssa"):
            table.append(("all", f"{tag}-only-{key}-second-not-answered", lambda j=joint, k=key: all_families(joint=j, drop=k)))
            table.append(("all", f"{tag}-only-{key}-second-zero", lambda j=joint, k=key: all_families(joint=j, zero=k)))
    for key in ("int", "div", "ira", "g", "ssa"):
        table.append(("adopt", f"{key}-zero-recorded-closure-not-reattested", lambda k=key: adopt_and_answer(k, reclose=False)))
        table.append(("adopt", f"{key}-zero-recorded-closure-reattested", lambda k=key: adopt_and_answer(k, reclose=True)))
    # an income family left unclosed beside a box 4 answer: the count needs the income family closed too.
    # (Not done for Form SSA-1099: the Social Security hand-over re-attests that family's closure.)
    table.append(("income-closure", "div-1a-closure-unanswered-box4-answered",
                  lambda: _strip_closure(family_return("div", 1, [40.0]), "tax.us.2025.f1099div.1a.source-closure")))
    table.append(("all", "single-int-and-g-second-not-answered", lambda: all_families(drop=("int", "g"))))
    table += [
        # what the count check cannot see: statements that never reach the income family it counts
        ("census", "int-box8-only-statement-no-box4", lambda: cr.add_tax_exempt_interest_1099int(cr.base_return(), [40.0])),
        ("census", "div-box12-only-statement-no-box4", lambda: cr.add_exempt_interest_dividends_1099div(cr.base_return(), [60.0])),
        ("census", "int-box4-on-a-statement-without-box1", int_box4_on_a_statement_without_box1),
        ("census", "int-every-statement-answered-plus-one-answer-without-box1",
         lambda: int_box4_on_a_statement_without_box1(second_answered=True)),
    ]
    table += [
        ("w2", "base-one-w2-answered", no_withholding),
        ("w2", "one-w2-box2-zero", w2_zero_single),
        ("w2", "one-w2-no-box2-closed", lambda: w2_case("single-no-box2")),
        ("w2", "two-w2-one-box2-closed", lambda: w2_case("second-slip-no-box2")),
        ("w2", "two-w2-second-box2-zero-closed", lambda: w2_case("second-slip-zero")),
        ("w2", "two-w2-both-answered-closed", lambda: w2_case("second-slip-answered")),
    ]
    return table


def main() -> None:
    """Runs every case and writes ``probe-output.json``. Cases already in an existing output file
    are kept, not rerun (delete the file to rerun all)."""
    done: dict[str, Any] = {}
    if OUT_PATH.exists():
        done = {c["run_id"]: c for c in json.loads(OUT_PATH.read_text(encoding="utf-8"))["cases"]}
    cases: list[dict[str, Any]] = []
    for family, cause, build in case_table():
        run_id = f"demo.p0.swa.{family}.{cause}"
        if run_id in done and "line_dispositions" in done[run_id]:
            cases.append(done[run_id])
            continue
        print("run", run_id, flush=True)
        cases.append({"family": family, "cause": cause, "run_id": run_id, **summarize(build(), run_id)})
        OUT_PATH.write_text(json.dumps({"core": "v70", "cases": cases}, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    OUT_PATH.write_text(json.dumps({"core": "v70", "cases": cases}, indent=2, sort_keys=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
