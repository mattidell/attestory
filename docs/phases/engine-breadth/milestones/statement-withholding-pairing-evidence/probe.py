"""P0 probe: line 25b on core v76, through live_coordinate_run only.

Reproduces the unpaired withholding check on synthetic demo.* findings.
Nothing under packages/ is edited. Run from the repository root:

    python3 docs/phases/engine-breadth/milestones/statement-withholding-pairing-evidence/probe.py [case id ...]

Writes probe-output.json beside this file. A case already in that file is
kept, not rerun. An admission, identity, or horizon refusal is recorded as
unreachable; it is not treated as a defect.
"""

from __future__ import annotations

import json
import re
import sys
import traceback
from decimal import Decimal
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any, Callable

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
sys.path.insert(0, str(REPO))

from packages.derivation.live import live_coordinate_run  # noqa: E402
from packages.derivation.live_workspace import WorkspaceCapability  # noqa: E402
from packages.derivation.production_resolver import PublicationSurface  # noqa: E402
from packages.kernel.findings import FindingModelError  # noqa: E402
from tests.helpers import current_core_returns as ccr  # noqa: E402
from tests.test_form_1099_k_income import _handover  # noqa: E402
from tests.test_form_1099_withholding import (  # noqa: E402
    DIV_B4_FAMILY,
    G_B4_FAMILY,
    INT_B4_FAMILY,
    IRA_B4_FAMILY,
    SCOPE_KEY,
    SSA_B6_FAMILY,
    YEAR,
    _add,
    _assert,
    _base,
    _dividends,
    _introduce,
    _social_security_withholding,
    _transition,
    _unemployment_withholding,
)
from tests.test_refund_or_amount_owed_track1 import _finish  # noqa: E402
from tests.test_statement_withholding_answer import (  # noqa: E402
    FACTS,
    FIRST_AMOUNT,
    L24,
    L25A,
    L25B,
    L25D,
    L33,
    L35A,
    L37,
    family_return,
)
from tests.test_w2g_gambling import _set_answer, _w2g  # noqa: E402
from tests.test_withholding_closure import _horizons, _set_closure  # noqa: E402

CONTENT = ccr.CONTENT
RELEASE_DIR = ccr.RELEASE_DIR
P = ccr.P
CORE = (
    "package.core-calculations.v76.json",
    "v76",
    "demo.release.sli-worksheet-integration.2025.v74.json",
    "v74",
    "published-packages.v74.json",
)
ORPHAN = 7.0
SECOND_AMOUNT = {"int": 30.0, "div": 20.0, "ira": 800.0, "g": 400.0, "ssa": 500.0}
OTHER_AMOUNT = 100.0
W2_SECOND_WAGES = 20000.0
W2_SECOND_BOX2 = 800.0
W2_THIRD_BOX2 = 100.0
W2_REPLACEMENT = 9999.0

FORMS: dict[str, dict[str, Any]] = {
    "int": {
        "form": "1099-INT",
        "family": INT_B4_FAMILY,
        "fact": FACTS["int"],
        "payer_kind": "tax.us.interest-payer",
        "stmt_kind": "tax.us.1099int-statement",
        "keys0": (("payer", "demo.fw.int.payer.0"), ("statement", "demo.fw.int.stmt.0")),
    },
    "div": {
        "form": "1099-DIV",
        "family": DIV_B4_FAMILY,
        "fact": FACTS["div"],
        "payer_kind": "tax.us.dividend-payer",
        "stmt_kind": "tax.us.1099div-statement",
        "keys0": (("payer", "demo.fw.div.payer.0"), ("statement", "demo.fw.div.stmt.0")),
    },
    "ira": {
        "form": "1099-R",
        "family": IRA_B4_FAMILY,
        "fact": FACTS["ira"],
        "payer_kind": "tax.us.ira-payer",
        "stmt_kind": "tax.us.1099r-statement",
        "keys0": (("payer", "demo.fw.r.payer.0"), ("statement", "demo.fw.r.stmt.0")),
    },
    "g": {
        "form": "1099-G",
        "family": G_B4_FAMILY,
        "fact": FACTS["g"],
        "payer_kind": "tax.us.unemployment-payer",
        "stmt_kind": "tax.us.1099g-statement",
        "keys0": (("payer", "demo.fw.g.payer.0"), ("statement", "demo.fw.g.stmt.0")),
    },
    "ssa": {
        "form": "SSA-1099",
        "family": SSA_B6_FAMILY,
        "fact": FACTS["ssa"],
        "payer_kind": None,
        "stmt_kind": "tax.us.ssa1099-statement",
        "keys0": (("statement", "demo.fw.ssa.stmt.0"),),
    },
}

LINES = {
    "line24": L24,
    "line25a": L25A,
    "line25b": L25B,
    "line25d": L25D,
    "line33": L33,
    "line35a": L35A,
    "line37": L37,
    "int_b4": P + "interest.b4-withholding-subtotal",
    "div_b4": P + "dividends.b4-withholding-subtotal",
    "ira_b4": P + "ira.box4-withholding-subtotal",
    "g_b4": P + "unemployment.b4-withholding-subtotal",
    "ssa_b6": P + "ssa1099.b6-withholding-subtotal",
}

# Other boxes that can record a statement without that form's counted income box.
OTHERS: tuple[dict[str, Any], ...] = (
    {"id": "int.box3", "form_key": "int", "box": "box 3", "family": P + "f1099int.b3", "tag": "b3"},
    {"id": "int.box8", "form_key": "int", "box": "box 8", "family": P + "f1099int.b8", "tag": "b8", "helper": "box8"},
    {"id": "int.box10", "form_key": "int", "box": "box 10", "family": P + "f1099int.b10", "tag": "b10"},
    {"id": "div.box2a", "form_key": "div", "box": "box 2a", "family": P + "f1099div.2a", "tag": "b2a", "flip": "cg"},
    {"id": "div.box7", "form_key": "div", "box": "box 7", "family": P + "f1099div.7", "tag": "b7", "helper": "box7"},
    {"id": "div.box12", "form_key": "div", "box": "box 12", "family": P + "f1099div.12", "tag": "b12", "helper": "box12"},
)


def _money(amount: float) -> str:
    return format(Decimal(str(amount)), "f")


def _clean(text: str) -> str:
    text = re.sub(r"/(?:Users|private|var|tmp)/\S+", "<path>", text)
    return text[:800]


def _no_statements() -> list[dict[str, object]]:
    acts = _base(wages=50000.0, w2_withheld=4500.0)
    _unemployment_withholding(acts, [])
    _social_security_withholding(acts, [])
    _w2g(acts, [])
    return acts


def _orphan_keys(spec: dict[str, Any]) -> tuple[tuple[str, str], ...]:
    if spec["payer_kind"] is None:
        return (("statement", "demo.swp.x.stmt"),)
    return (("payer", "demo.swp.x.payer"), ("statement", "demo.swp.x.stmt"))


def _add_orphan(acts: list[dict[str, object]], key: str, amount: float = ORPHAN) -> list[dict[str, object]]:
    """A withholding member on a new statement that has no income-box member."""
    spec = FORMS[key]
    if spec["payer_kind"] is not None:
        _introduce(acts, "demo.swp.x.payer", spec["payer_kind"])
    _introduce(acts, "demo.swp.x.stmt", spec["stmt_kind"])
    head = _horizons(acts, spec["family"])[-1]
    _transition(
        acts, (spec["family"], "v1"), head, "demo.swp.x.h", "demo.swp.x.withholding",
        spec["fact"], _orphan_keys(spec), amount,
    )
    return _set_closure(acts, key, "head")


def _second_on_same(key: str) -> list[dict[str, object]]:
    """A second withholding member written on the first statement's own keys."""
    spec = FORMS[key]
    acts = family_return(key, 1, [FIRST_AMOUNT[key]])
    head = _horizons(acts, spec["family"])[-1]
    _transition(
        acts, (spec["family"], "v1"), head, "demo.swp.dup.h", "demo.swp.dup.withholding",
        spec["fact"], spec["keys0"], ORPHAN,
    )
    return _set_closure(acts, key, "head")


def _second_by_assertion() -> list[dict[str, object]]:
    """The correction path the rejected transition names: an ordinary assertion on the same keys."""
    spec = FORMS["int"]
    acts = family_return("int", 1, [FIRST_AMOUNT["int"]])
    _assert(acts, "demo.swp.dup.assert", spec["fact"], spec["keys0"], ORPHAN)
    return acts


def _offset(key: str) -> list[dict[str, object]]:
    """Two income statements, withholding on the first only, plus a withholding-only statement."""
    return _add_orphan(family_return(key, 2, [FIRST_AMOUNT[key], None]), key)


def _both(key: str) -> list[dict[str, object]]:
    return family_return(key, 2, [FIRST_AMOUNT[key], SECOND_AMOUNT[key]])


def _answered_plus_orphan(key: str) -> list[dict[str, object]]:
    return _add_orphan(_both(key), key)


def _one_unanswered(key: str) -> list[dict[str, object]]:
    return family_return(key, 2, [FIRST_AMOUNT[key], None])


def _zero_is_an_answer() -> list[dict[str, object]]:
    return family_return("int", 2, [FIRST_AMOUNT["int"], 0.0])


def _cross() -> list[dict[str, object]]:
    """INT fully answered, plus a withholding-only INT, plus one DIV with no withholding."""
    acts = _add_orphan(family_return("int", 2, [FIRST_AMOUNT["int"], SECOND_AMOUNT["int"]]), "int")
    _dividends(acts, [(500.0, None)])
    return acts


def _record_other(acts: list[dict[str, object]], spec: dict[str, Any]) -> list[dict[str, object]]:
    if spec.get("flip") == "cg":
        _set_answer(acts, P + "capital-gain-distributions", "yes")
    helper = spec.get("helper")
    if helper == "box8":
        return ccr.add_tax_exempt_interest_1099int(acts, [OTHER_AMOUNT])
    if helper == "box12":
        return ccr.add_exempt_interest_dividends_1099div(acts, [OTHER_AMOUNT])
    if helper == "box7":
        return ccr.add_foreign_tax_1099div(acts, [OTHER_AMOUNT])
    return ccr._record_members(acts, spec["family"], [OTHER_AMOUNT], tag=spec["tag"])


def _other(spec: dict[str, Any], *, answered: bool) -> list[dict[str, object]]:
    acts = _record_other(_no_statements(), spec)
    if not answered:
        return acts
    keys = (
        ("payer", f"demo.ccr.{spec['tag']}0.payer"),
        ("statement", f"demo.ccr.{spec['tag']}0.statement"),
    )
    form = FORMS[spec["form_key"]]
    horizons = _horizons(acts, form["family"])
    if not horizons:
        genesis = f"demo.swp.{spec['tag']}.h0"
        _add(acts, "horizon-genesis", {
            "family": {"id": form["family"], "version": "v1"},
            "scope": dict(SCOPE_KEY),
            "horizon_id": genesis,
        })
        horizons = [genesis]
    _transition(
        acts, (form["family"], "v1"), horizons[-1], f"demo.swp.{spec['tag']}.h",
        f"demo.swp.{spec['tag']}.withholding", form["fact"], keys, ORPHAN,
    )
    return _set_closure(acts, spec["form_key"], "head")


def _finding_ids(acts: list[dict[str, object]], prefix: str) -> list[str]:
    found: list[str] = []
    for act in acts:
        payload = act.get("payload")
        if not isinstance(payload, dict):
            continue
        candidates = [payload.get("finding")]
        member = payload.get("member")
        if isinstance(member, dict):
            candidates.append(member.get("finding"))
        for finding in candidates:
            if isinstance(finding, dict) and str(finding.get("fact_id", "")).startswith(prefix):
                found.append(str(finding["fact_id"]))
    return found


def _parse_box2(fact_id: str) -> tuple[str, str]:
    body = fact_id.split("|", 1)[1]
    pairs = dict(part.split("=", 1) for part in body.split(","))
    return pairs["employer"], pairs["w2-slip"]


def _strip_closure(acts: list[dict[str, object]], prefix: str) -> list[dict[str, object]]:
    kept: list[dict[str, object]] = []
    for act in acts:
        payload = act.get("payload")
        finding = payload.get("finding") if isinstance(payload, dict) else None
        if act.get("kind") == "assertion" and isinstance(finding, dict) and str(finding.get("fact_id", "")).startswith(prefix):
            continue
        kept.append(act)
    return kept


def _second_w2(acts: list[dict[str, object]], *, box2: float | None) -> list[dict[str, object]]:
    predecessor = _horizons(acts, "tax.us.2025.w2")[-1]
    acts = _strip_closure(acts, "tax.us.2025.w2.source-closure|")
    employer, slip = "demo.swp.w2second.employer", "demo.swp.w2second.slip"
    _introduce(acts, employer, "tax.us.employer")
    _introduce(acts, slip, "tax.us.w2-slip")
    successor = "demo.swp.w2.h2"
    _transition(
        acts, ("tax.us.2025.w2", "v2"), predecessor, successor, "demo.swp.w2second.wages",
        "tax.us.2025.w2.box1-wages", (("employer", employer), ("w2-slip", slip)), W2_SECOND_WAGES,
    )
    _close(acts, "tax.us.2025.w2.source-closure", successor, "demo.swp.w2.reclose")
    if box2 is not None:
        _assert(acts, "demo.swp.w2second.box2", "tax.us.2025.w2.box2-withholding",
                (("employer", employer), ("w2-slip", slip)), box2)
    return acts


def _close(acts: list[dict[str, object]], closure_fact: str, horizon: str, finding_id: str) -> None:
    from tests.test_form_1099_withholding import _close as close
    close(acts, closure_fact, horizon, finding_id)


def _third_box2_only(acts: list[dict[str, object]]) -> list[dict[str, object]]:
    employer, slip = "demo.swp.w2third.employer", "demo.swp.w2third.slip"
    _introduce(acts, employer, "tax.us.employer")
    _introduce(acts, slip, "tax.us.w2-slip")
    _assert(acts, "demo.swp.w2third.box2", "tax.us.2025.w2.box2-withholding",
            (("employer", employer), ("w2-slip", slip)), W2_THIRD_BOX2)
    return acts


def _same_slip_second_box2(acts: list[dict[str, object]]) -> list[dict[str, object]]:
    employer, slip = _parse_box2(_finding_ids(acts, "tax.us.2025.w2.box2-withholding|")[0])
    _assert(acts, "demo.swp.w2.same.box2", "tax.us.2025.w2.box2-withholding",
            (("employer", employer), ("w2-slip", slip)), W2_REPLACEMENT)
    return acts


def case_table() -> list[tuple[str, str, str, str, Callable[[], list[dict[str, object]]]]]:
    """(case id, form, case, right answer, builder)."""
    rows: list[tuple[str, str, str, str, Callable[[], list[dict[str, object]]]]] = []
    for key, spec in FORMS.items():
        form = spec["form"]
        rows.append((
            f"{key}.one-unanswered", form, "two statements, one withholding answer missing",
            "block", lambda key=key: _one_unanswered(key),
        ))
        rows.append((
            f"{key}.offset", form,
            "two statements, one answer missing, plus a withholding-only statement of 7",
            "block", lambda key=key: _offset(key),
        ))
        rows.append((
            f"{key}.both-answered", form, "two statements, each with its own withholding answer",
            f"publish {_money(FIRST_AMOUNT[key] + SECOND_AMOUNT[key])}",
            lambda key=key: _both(key),
        ))
        rows.append((
            f"{key}.answered-plus-orphan", form,
            "both statements answered, plus a withholding-only statement of 7",
            f"publish {_money(FIRST_AMOUNT[key] + SECOND_AMOUNT[key] + ORPHAN)}",
            lambda key=key: _answered_plus_orphan(key),
        ))
        rows.append((
            f"{key}.same-statement-second", form,
            "a second withholding member on the answered statement's own keys",
            "one current answer for that statement; a second member is not a second statement",
            lambda key=key: _second_on_same(key),
        ))
    rows.append((
        "int.same-statement-assert", "1099-INT",
        "an ordinary assertion of box 4 on the answered statement's own keys",
        "one current answer for that statement; a second member is not a second statement",
        _second_by_assertion,
    ))
    rows.append((
        "int.zero-is-an-answer", "1099-INT",
        "two statements, the second withholding answer recorded as 0",
        f"publish {_money(FIRST_AMOUNT['int'])}", _zero_is_an_answer,
    ))
    rows.append((
        "cross.int-answered-div-open", "1099-INT and 1099-DIV",
        "INT both answered plus a withholding-only INT, and one DIV with no withholding",
        "block", _cross,
    ))
    for spec in OTHERS:
        form = FORMS[spec["form_key"]]["form"]
        rows.append((
            f"{spec['id']}.unanswered", form,
            f"a statement recorded only through {spec['box']}, no withholding answer",
            "block", lambda spec=spec: _other(spec, answered=False),
        ))
        rows.append((
            f"{spec['id']}.answered", form,
            f"a statement recorded only through {spec['box']}, withholding 7 on that statement",
            f"publish {_money(ORPHAN)}", lambda spec=spec: _other(spec, answered=True),
        ))
    rows.append((
        "w2.second-slip-unanswered", "W-2",
        "two W-2 slips, box 2 answered on the first only",
        "block", lambda: _second_w2(_no_statements(), box2=None),
    ))
    rows.append((
        "w2.offset", "W-2",
        "two W-2 slips with box 2 on the first only, plus a box-2-only third slip of 100",
        "block", lambda: _third_box2_only(_second_w2(_no_statements(), box2=None)),
    ))
    rows.append((
        "w2.both-answered", "W-2",
        "two W-2 slips, each with its own box 2",
        f"publish {_money(4500.0 + W2_SECOND_BOX2)}",
        lambda: _second_w2(_no_statements(), box2=W2_SECOND_BOX2),
    ))
    rows.append((
        "w2.same-slip-second", "W-2",
        "a second box 2 write on the base slip's own keys",
        "one current box 2 for that slip",
        lambda: _same_slip_second_box2(_no_statements()),
    ))
    return rows


def _run(acts: list[dict[str, object]], name: str) -> dict[str, Any]:
    package, version, release, rel_version, registry = CORE
    surface = PublicationSurface(RELEASE_DIR, CONTENT / registry, CONTENT)
    finished = _handover(
        _finish(
            acts, package_path=CONTENT / package, package_version=version,
            release_path=RELEASE_DIR / release, release_version=rel_version, note=name,
        ),
        surface=surface, reconfirm=True,
    )
    with TemporaryDirectory() as tmp:
        outcome = live_coordinate_run(
            WorkspaceCapability(Path(tmp) / "L"), repo_root=REPO, authoritative_acts=finished,
            workspace_revision=len(finished), run_scope={"jurisdiction": "us", "year": YEAR},
            scope_user=ccr.USER, request={"schema": "run-request.v1"}, run_id=name,
            governance_pins=[], surface=surface, output_name="out.json",
        )
        if outcome.refusal is not None:
            return {
                "reachable": False,
                "refusal": _clean(f"{outcome.refusal.reason} {outcome.refusal.detail}"),
            }
        pubs = {str(p.finding["symbol"]): p.finding for p in outcome.publications or ()}
        report = json.loads(outcome.output_path.read_text(encoding="utf-8")) if outcome.output_path else {}
    dispositions = list(report.get("dispositions", []))
    lines: dict[str, str | None] = {}
    for label, symbol in LINES.items():
        lines[label] = _money(float(pubs[symbol]["value"])) if symbol in pubs else None
    blocked = []
    for row in dispositions:
        if row.get("disposition") != "blocked":
            continue
        artifact = str(row.get("artifact_id", ""))
        if "line25a" in artifact or "line25b" in artifact:
            blocked.append({
                "artifact": artifact.replace(P, ""),
                "code": row.get("code"),
                "missing": [str(item).replace(P, "") for item in row.get("missing", [])],
            })
    return {"reachable": True, "lines": lines, "line_blocks": blocked}


def execute_case(
    case_id: str, form: str, label: str, right: str,
    builder: Callable[[], list[dict[str, object]]],
) -> dict[str, Any]:
    """Build one case and run it on the core ``CORE`` currently names."""
    row: dict[str, Any] = {"id": case_id, "form": form, "case": label, "right_answer": right}
    try:
        acts = builder()
        if case_id.startswith("w2."):
            row["w2_box1"] = _finding_ids(acts, "tax.us.2025.w2.box1-wages|")
            row["w2_box2"] = _finding_ids(acts, "tax.us.2025.w2.box2-withholding|")
        row.update(_run(acts, f"demo.swp.{case_id}"))
    except (FindingModelError, AssertionError, KeyError, IndexError, ValueError) as exc:
        row["reachable"] = False
        row["refusal"] = _clean(f"{type(exc).__name__}: {exc}")
    except Exception as exc:  # a horizon or admission failure is a refusal to record
        row["reachable"] = False
        row["refusal"] = _clean(f"{type(exc).__name__}: {exc}\n{traceback.format_exc(limit=4)}")
    return row


def _write(path: Path, cases: list[dict[str, Any]]) -> None:
    merged = {}
    if path.exists():
        merged = {row["id"]: row for row in json.loads(path.read_text(encoding="utf-8"))["cases"]}
    for row in cases:
        merged[row["id"]] = row
    ordered = sorted(merged.values(), key=lambda row: row["id"])
    path.write_text(json.dumps({"core": "v76", "cases": ordered}, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    selected = sys.argv[1:]
    out_path = HERE / "probe-output.json"
    done: dict[str, dict[str, Any]] = {}
    if out_path.exists():
        done = {row["id"]: row for row in json.loads(out_path.read_text(encoding="utf-8"))["cases"]}
    cases: list[dict[str, Any]] = []
    for case_id, form, label, right, builder in case_table():
        if selected and not any(token in case_id for token in selected):
            if case_id in done:
                cases.append(done[case_id])
            continue
        if case_id in done and not selected:
            cases.append(done[case_id])
            continue
        print("run", case_id, flush=True)
        row = execute_case(case_id, form, label, right, builder)
        cases.append(row)
        _write(out_path, cases)
        line = (row.get("lines") or {}).get("line25b") if row.get("reachable") else row.get("refusal")
        target = "line25a" if case_id.startswith("w2.") else "line25b"
        if row.get("reachable"):
            line = (row.get("lines") or {}).get(target)
        print(" ", case_id, "reachable" if row.get("reachable") else "refused", line, flush=True)
    if not selected:
        _write(out_path, cases)
    print("wrote", out_path.name, len(cases), "cases", flush=True)


if __name__ == "__main__":
    main()
