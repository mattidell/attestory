"""Track 0 adversarial closure for the preferential-base successor.

Every case is a ``live_coordinate_run`` on published core v90 and the P0
scratch core v91. Hand values are the 2025 instruction figures for the wage
return (single, wages 50,000, withholding 4,500, standard deduction 15,750):
taxable income 34,250 and Tax Table tax 3,875 when line 7a is zero; the
Qualified Dividends and Capital Gain Tax Worksheet leaves that tax unchanged
while a long-term gain stays inside the single 0% band (48,350). A 3,000
allowed loss makes taxable income 31,250 and Tax Table tax 3,515.

    python3 track0.py authority <scratch-core.json>
    python3 track0.py matrix <scratch-core.json>
    python3 track0.py names <scratch-core.json> <variant-directory>
    python3 track0.py late <scratch-core.json>
    python3 track0.py reuse <scratch-core.json>
    python3 track0.py neighbour --part <part-file> --log <time-log> --workers N
    python3 track0.py surface <scratch-core.json>

Nothing here edits packages/ or tests/.
"""

from __future__ import annotations

import copy
import json
import multiprocessing
import os
import sys
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from tests import evidence_loader  # noqa: E402

import probe  # noqa: E402
import prototype  # noqa: E402
import rerun  # noqa: E402

OWNER = "pbr_track0"
P = probe.P
PREFERENTIAL = "capital-gains.selected-preferential-base"
CONCLUSION = "schedule-d-required.conclusion"
FOUR = [
    "f1099b.noncovered-sold.source-closure",
    "f8949.no1099b-sold.source-closure",
    "schedule-d-boundary.no-form8949-sources",
    "schedule-d-boundary.no-other-form8949-adjustments",
]
EXC_SHORT = [
    "exception1.only-box2a-capital-gains",
    "exception1.no-capital-losses",
    "exception1.no-qof-deferral",
    "exception1.no-boxes-2b-2c-2d",
]
PARKED = {"form1040.line-25b", "form1040.line-25d"}
# 2025 Tax Table, single, wages 50,000, standard deduction 15,750.
WAGE_HAND = {
    "form1040.line-7a": 0, "form1040.line-11a": 50000, "form1040.line-15": 34250,
    "form1040.line-16": 3875, "form1040.line-24": 3875,
    "form1040.line-33": 4500, "form1040.line-37": 0,
}
# Box 2a 1,000 is a long-term gain inside the 0% band, so the tax stays 3,875.
BOX2A_HAND = {
    "form1040.line-7a": 1000, "form1040.line-11a": 51000, "form1040.line-15": 35250,
    "form1040.line-16": 3875, "form1040.line-24": 3875,
    "form1040.line-33": 4500, "form1040.line-37": 0,
}
# Capital Loss Carryover Worksheet on the prior-year lines below: short-term
# carryover 5,000, long-term carryover 5,000. Allowed loss 3,000. Tax Table
# on taxable income 31,250 is 3,515.
CARRY_HAND = {
    "capital-loss-carryover.short-term": 5000, "capital-loss-carryover.long-term": 5000,
    "schedule-d.line-7": -5000, "schedule-d.line-15": -5000, "schedule-d.line-16": -10000,
    "schedule-d.line-21": 3000, "form1040.line-7a": -3000, "form1040.line-11a": 47000,
    "form1040.line-15": 31250, "form1040.line-16": 3515, "form1040.line-24": 3515,
    "form1040.line-33": 4500, "form1040.line-37": 0,
}
# Prior return that the worksheet turns into those two carryovers.
PRIOR = {
    "prior-return.form1040.line-15": 50000,
    "prior-return.schedule-d.line-7": -8000,
    "prior-return.schedule-d.line-15": -5000,
    "prior-return.schedule-d.line-16": -13000,
    "prior-return.schedule-d.line-21": -3000,
}
SALE_LINES = (
    "schedule-d.line-1b", "schedule-d.line-2", "schedule-d.line-3",
    "schedule-d.line-8b", "schedule-d.line-9", "schedule-d.line-10",
)
ACTIVITIES = ("none", "sale", "amount")
CONCLUSIONS = ("no", "required", "open")
BOUNDARIES = ("open", "answered")


def num(value: Any) -> Any:
    if isinstance(value, bool) or value is None:
        return value
    if isinstance(value, (int, float)):
        return int(value) if float(value).is_integer() else value
    try:
        number = float(value)
    except (TypeError, ValueError):
        return value
    return int(number) if number.is_integer() else number


def write(name: str, payload: Any) -> None:
    text = json.dumps(payload, indent=2) + "\n"
    for needle in ("/Users/", "/private/", "/tmp/", "/var/"):
        if needle in text:
            raise SystemExit(f"{name} contains a local path")
    (HERE / name).write_text(text, encoding="utf-8")


def harness() -> Any:
    evidence_loader.activate(OWNER)
    common = evidence_loader.load(probe.BNQ / "common.py", "common")
    return common.harness()


def _say(acts: list[dict[str, Any]], fact: str, value: Any, tag: str) -> list[dict[str, Any]]:
    return harness().say(acts, P + fact, value, tag)


def _strip(acts: list[dict[str, Any]], fact: str) -> list[dict[str, Any]]:
    return harness().strip(acts, P + fact)


def _prior(acts: list[dict[str, Any]], fact: str, value: float, tag: str) -> list[dict[str, Any]]:
    """A 2024 line the Capital Loss Carryover Worksheet reads."""
    h = harness()
    full = P + fact
    acts = h.strip(acts, full)
    body = h.bundle_for(full, h.CONTENT)
    if body is not None and not {row["id"] for row in body["fact_types"]} & h._adopted(acts):
        h._add(acts, "bundle-adoption", {"bundle": body})
    fact_id = h.fact_id_for(full, (("tax-year", h.YEAR), ("source-tax-year", "2024")))
    h._add(acts, "assertion", {"finding": h._attested(f"demo.pbr.{tag}", fact_id, value)})
    return h.renumber(acts)


def _age(acts: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return probe._state_age(acts)


def _base() -> list[dict[str, Any]]:
    """Wage return with the Exception 1, boundary, and carryover answers removed."""
    h = harness()
    acts = h.opened()
    for fact in (
        *EXC_SHORT, *FOUR, "f1099b.code-b-sold.source-closure",
        "schedule-d-boundary.noncovered-in-class", "schedule-d-boundary.form8949-in-class",
        "schedule-d-boundary.form8949-code-b-in-class", "schedule-d-boundary.no-lines-18-19-sources",
        "schedule-d-boundary.no-other-schedule-d-sources", "schedule-d-boundary.no-1099da-or-qof",
        "schedule-d-boundary.no-inbound-capital-loss-carryovers",
    ):
        acts = h.strip(acts, P + fact)
    return acts


def _exception(acts: list[dict[str, Any]], conclusion: str) -> list[dict[str, Any]]:
    """Conclusion no is every component yes. Required is only-box-2a no. Open leaves QOF out."""
    if conclusion == "open":
        for fact, value in (
            ("exception1.only-box2a-capital-gains", "yes"),
            ("exception1.no-capital-losses", "yes"),
            ("exception1.no-boxes-2b-2c-2d", "yes"),
        ):
            acts = _say(acts, fact, value, fact)
        return acts
    only = "yes" if conclusion == "no" else "no"
    for fact, value in (
        ("exception1.only-box2a-capital-gains", only),
        ("exception1.no-capital-losses", "yes"),
        ("exception1.no-qof-deferral", "yes"),
        ("exception1.no-boxes-2b-2c-2d", "yes"),
    ):
        acts = _say(acts, fact, value, fact)
    return acts


def _boundary(acts: list[dict[str, Any]], mode: str, *, sale: bool) -> list[dict[str, Any]]:
    if mode == "open":
        return acts
    # The other Schedule D boundary answers stay "no such amount", which is what
    # the wage return already said. The four line 16 answers follow the activity.
    common = {"lines_18_19": "yes", "no_other_sd": "yes", "no_da_qof": "yes"}
    if sale:
        return harness().answer(
            acts, q1="no", q2="yes", q3="no", form8949="no", path_b="no", ic80="yes", **common,
        )
    return harness().answer(
        acts, q1="no", q2="no", q3="no", form8949="yes", path_b="yes", **common,
    )


def _activity(acts: list[dict[str, Any]], activity: str) -> list[dict[str, Any]]:
    if activity == "sale":
        acts = _say(acts, "schedule-d-boundary.no-inbound-capital-loss-carryovers", "yes", "carry")
        return harness().sale(acts, "no1099b", "st", proceeds=2000, basis=8000, tag="pbr-sale")
    if activity == "amount":
        acts = _say(acts, "schedule-d-boundary.no-inbound-capital-loss-carryovers", "no", "carry")
        for fact, value in PRIOR.items():
            acts = _prior(acts, fact, value, fact.replace(".", "-"))
        return acts
    return _say(acts, "schedule-d-boundary.no-inbound-capital-loss-carryovers", "yes", "carry")


def cell_acts(activity: str, conclusion: str, boundary: str) -> list[dict[str, Any]]:
    acts = _exception(_base(), conclusion)
    acts = _activity(acts, activity)
    acts = _boundary(acts, boundary, sale=activity == "sale")
    return _age(acts)


def add_box2a(acts: list[dict[str, Any]], amount: float = 1000.0) -> list[dict[str, Any]]:
    """Form 1099-DIV box 2a, the Schedule D line 13 amount, with box 4 closed at zero."""
    from tests import test_collect_closure as cc

    h = harness()
    acts = cc._add_member(acts, P + "f1099div.2a", amount, close=True, tag="pbrcgd")
    acts = h.renumber(acts)
    stmt = (("payer", "demo.cc.pbrcgd.payer"), ("statement", "demo.cc.pbrcgd.statement"))
    family = P + "f1099div.b4"
    acts = h.strip(acts, family + ".source-closure")
    head = h.horizons(acts, family)[-1]
    h._add(acts, "member-transition", {
        "family": {"id": family, "version": "v1"},
        "scope": {"tax-year": h.YEAR, "subject": "demo.primary"},
        "member": {"action": "assert", "finding": h._attested(
            "demo.pbr.cgd.b4",
            h.fact_id_for(P + "f1099div.box4-withholding", (*stmt, ("tax-year", h.YEAR))),
            0.0,
        )},
        "successor": {"id": "demo.pbr.cgd.b4.h1", "predecessor": head},
    })
    h._close(acts, family + ".source-closure", "demo.pbr.cgd.b4.h1", "demo.pbr.cgd.b4.closure")
    acts = h.say(acts, P + "capital-gain-distributions", "yes", "cgd")
    return h.renumber(acts)


def remove_sale(acts: list[dict[str, Any]], kind: str, term: str, tag: str) -> list[dict[str, Any]]:
    """Remove one sale and its amount rows, and close a per-family family again."""
    h = harness()
    per_family = h.SALE_KINDS[kind]["grouped"] is None
    out = copy.deepcopy(acts)
    for scalar in (*h.SALE_KINDS[kind]["kinds"], None):
        family = h.family_id(kind, term, scalar)
        member = h.member_fact(kind, term, scalar)
        fact_ids = [
            str(act["payload"]["member"]["finding"]["fact_id"])
            for act in out
            if act.get("kind") == "member-transition"
            and act["payload"]["family"]["id"] == family
            and str((act["payload"]["member"].get("finding") or {}).get("fact_id", "")).startswith(member + "|")
            and f"demo.sfa.{tag}." in str(act["payload"]["member"]["finding"]["fact_id"])
        ]
        for fact_id in fact_ids:
            if per_family:
                out = h.strip(out, family + ".source-closure")
            head = h.horizons(out, family)[-1]
            successor = f"demo.pbr.rm.{tag}.{family.removeprefix(P)}.h{len(h.horizons(out, family))}"
            h._add(out, "member-transition", {
                "family": {"id": family, "version": h.SALE_KINDS[kind]["version"]},
                "scope": {"tax-year": h.YEAR, "subject": "demo.primary"},
                "member": {"action": "remove", "fact_id": fact_id},
                "successor": {"id": successor, "predecessor": head},
            })
            if per_family:
                h._close(out, family + ".source-closure", successor, f"demo.pbr.rm.{tag}.closure")
    return h.renumber(out)


def _nonzero(value: Any) -> bool:
    number = num(value)
    return isinstance(number, (int, float)) and not isinstance(number, bool) and number != 0


def observed_activity(values: dict[str, Any]) -> str:
    sale = any(_nonzero(values.get(line)) for line in SALE_LINES)
    carry = _nonzero(values.get("capital-loss-carryover.short-term")) or _nonzero(
        values.get("capital-loss-carryover.long-term"))
    if sale:
        return "sale"
    if carry:
        return "amount"
    return "none"


def observed_conclusion(row: dict[str, Any]) -> str:
    conclusion = row.get("conclusion") or {}
    if conclusion.get("disposition") == "blocked":
        return "open"
    value = conclusion.get("value")
    if value == "no":
        return "no"
    if value == "yes":
        return "required"
    return "unobserved:" + str(conclusion.get("disposition"))


def signature(producer: dict[str, Any] | None) -> dict[str, Any]:
    row = producer or {}
    return {
        "disposition": row.get("disposition"),
        "code": row.get("code"),
        "guard_result": row.get("guard_result"),
        "missing": row.get("missing") or [],
        "value": num(row.get("value")),
    }


def silent_fields(blocked: list[dict[str, Any]]) -> list[str]:
    return sorted(
        field["field"] for field in blocked
        if not field.get("questions") and field["field"] not in PARKED
    )


def parked_fields(blocked: list[dict[str, Any]]) -> list[str]:
    return sorted(
        field["field"] for field in blocked
        if not field.get("questions") and field["field"] in PARKED
    )


def duplicate_fields(blocked: list[dict[str, Any]]) -> list[str]:
    return sorted(
        field["field"] for field in blocked
        if len(field.get("questions") or []) != len(set(field.get("questions") or []))
    )


def hand_misses(row: dict[str, Any], expected: dict[str, Any]) -> list[str]:
    misses = []
    values = {**(row.get("lines") or {}), **(row.get("values") or {})}
    for field, wanted in expected.items():
        got = num(values.get(field))
        if got != wanted:
            misses.append(f"{field}: hand {wanted}, live {got}")
    return misses


def _publications(outcome: Any) -> dict[str, Any]:
    found: dict[str, Any] = {}
    for item in outcome.publications or ():
        finding = getattr(item, "finding", None)
        if not isinstance(finding, dict):
            continue
        found[probe.short(finding.get("symbol"))] = num(finding.get("value"))
    return found


def _attach_values(summary: dict[str, Any], values: dict[str, Any]) -> dict[str, Any]:
    summary["values"] = values
    for symbol in (PREFERENTIAL, CONCLUSION):
        row = (summary.get("producers") or {}).get(symbol)
        if isinstance(row, dict) and row.get("disposition") == "published":
            row["value"] = values.get(symbol)
    return summary


def execute(case_id: str, acts: list[dict[str, Any]], core_json: str | None) -> dict[str, Any]:
    evidence_loader.activate(OWNER)
    common = evidence_loader.load(probe.BNQ / "common.py", "common")
    h = common.harness()
    core = probe._core_from(h, core_json)
    surface = core.surface()
    run_id = "demo.pbr.track0." + case_id.replace("/", "-").replace("_", "-")
    try:
        with h.loader_entries(core):
            finished = h._handover(
                h._finish(
                    json.loads(json.dumps(acts)),
                    package_path=core.package_path,
                    package_version=core.version,
                    release_path=core.release_path,
                    release_version=core.release_version,
                    note=run_id,
                ),
                surface=surface,
                reconfirm=True,
            )
            import tempfile
            with tempfile.TemporaryDirectory() as tmp:
                outcome = h.live_coordinate_run(
                    h.WorkspaceCapability(Path(tmp) / "L"),
                    repo_root=REPO,
                    authoritative_acts=finished,
                    workspace_revision=len(finished),
                    run_scope={"jurisdiction": "us", "year": h.YEAR},
                    scope_user=h.ccr.USER,
                    request={"schema": "run-request.v1"},
                    run_id=run_id,
                    governance_pins=[],
                    surface=surface,
                    output_name="out.json",
                )
                if outcome.refusal is not None:
                    return {"id": case_id, "outcome": "refused",
                            "message": probe.scrub(str(outcome.refusal.reason))[:300]}
                summary = probe.summarize(core, outcome)
                return {"id": case_id, **_attach_values(summary, _publications(outcome))}
    except Exception as exc:  # noqa: BLE001 - a rejected list is a result
        return {"id": case_id, "outcome": "error", "error": type(exc).__name__,
                "message": probe.scrub(str(exc))[:400]}


def _worker(payload: tuple[str | None, list[tuple[str, list[dict[str, Any]]]]]) -> list[dict[str, Any]]:
    core_json, shard = payload
    evidence_loader.activate(OWNER)
    try:
        return [execute(case_id, acts, core_json) for case_id, acts in shard]
    finally:
        evidence_loader.finish(OWNER)


def run_all(lists: list[tuple[str, list[dict[str, Any]]]], core_json: str | None) -> dict[str, dict[str, Any]]:
    workers = max(1, (os.cpu_count() or 2) - 1)
    shards = [(core_json, lists[index::workers]) for index in range(workers) if lists[index::workers]]
    found: list[dict[str, Any]] = []
    context = multiprocessing.get_context("spawn")
    with context.Pool(len(shards)) as pool:
        for part in pool.map(_worker, shards):
            found.extend(part)
    return {row["id"]: row for row in found}


def compact(row: dict[str, Any]) -> dict[str, Any]:
    blocked = [
        {"field": field["field"], "code": field.get("code"), "missing": field.get("missing") or [],
         "questions": field.get("questions") or []}
        for field in row.get("blocked_fields") or []
    ]
    lines = {
        field: num(value)
        for field, value in (row.get("lines") or {}).items()
        if field.startswith("form1040.") or field.startswith("schedule-d.") or field.startswith("form.")
    }
    keep = (
        "capital-loss-carryover.short-term", "capital-loss-carryover.long-term",
        PREFERENTIAL, CONCLUSION, *SALE_LINES,
        "schedule-d.line-6", "schedule-d.line-7", "schedule-d.line-13",
        "schedule-d.line-14", "schedule-d.line-15", "schedule-d.line-16", "schedule-d.line-21",
        "form1040.line-7a", "form1040.line-11a", "form1040.line-15", "form1040.line-16",
        "form1040.line-24", "form1040.line-33", "form1040.line-34", "form1040.line-37",
    )
    values = {name: num((row.get("values") or {}).get(name)) for name in keep if name in (row.get("values") or {})}
    return {
        "outcome": row.get("outcome"),
        "error": row.get("message") or row.get("error"),
        "page_questions": row.get("page_questions") or [],
        "producer": signature((row.get("producers") or {}).get(PREFERENTIAL)),
        "conclusion": signature((row.get("producers") or {}).get(CONCLUSION)),
        "lines": lines,
        "values": values,
        "blocked": blocked,
        "silent": silent_fields(blocked),
        "parked_silent": parked_fields(blocked),
        "duplicate_questions": duplicate_fields(blocked),
    }


def both(lists: list[tuple[str, list[dict[str, Any]]]], core_json: str) -> dict[str, dict[str, Any]]:
    evidence_loader.finish_all()
    v90 = run_all(lists, None)
    v91 = run_all(lists, core_json)
    return {
        case_id: {"v90": compact(v90[case_id]), "v91": compact(v91[case_id])}
        for case_id, _acts in lists
    }


def _prepared(builder: Any) -> list[tuple[str, list[dict[str, Any]]]]:
    evidence_loader.activate(OWNER)
    try:
        return list(builder())
    finally:
        # Age setup activates another owner. Spawn can see __main__ only after
        # every owner is finished.
        evidence_loader.finish_all()


def authority(core_json: str) -> None:
    def build() -> list[tuple[str, list[dict[str, Any]]]]:
        return [
            (f"{activity}/{conclusion}/{boundary}", cell_acts(activity, conclusion, boundary))
            for activity in ACTIVITIES
            for conclusion in CONCLUSIONS
            for boundary in BOUNDARIES
        ]

    lists = _prepared(build)
    runs = both(lists, core_json)
    cells = []
    for activity in ACTIVITIES:
        for conclusion in CONCLUSIONS:
            for boundary in BOUNDARIES:
                case_id = f"{activity}/{conclusion}/{boundary}"
                pair = runs[case_id]
                v10 = pair["v90"]["producer"]
                v11 = pair["v91"]["producer"]
                differs = v10 != v11
                v11_names = (
                    v11.get("disposition") == "blocked"
                    and v11.get("code") == "DEPENDENCY_ABSENT"
                    and v11.get("missing") == FOUR
                )
                seen = observed_activity({**pair["v90"]["lines"], **pair["v90"]["values"]})
                seen_conclusion = observed_conclusion(pair["v90"])
                # An open grouped closure blocks the activity test on the counts.
                # That cell is not a realized "no activity" result, so v11 is not
                # allowed to differ from v10 there.
                open_counts = boundary == "open" and v10.get("disposition") == "blocked" and any(
                    name.endswith("-count") for name in v10.get("missing") or []
                )
                realized_allowed = (
                    activity == "none" and conclusion == "required" and boundary == "answered"
                    and seen == "none" and seen_conclusion == "required"
                )
                axes = seen_conclusion == conclusion and (seen == activity or open_counts)
                if pair["v90"]["outcome"] != "success" or pair["v91"]["outcome"] != "success" or not axes:
                    right = "unobserved"
                    passed = False
                elif realized_allowed:
                    right = "v11 names the four questions" if v11_names else "v11 did not name the four questions"
                    passed = v11_names and differs and v10.get("disposition") == "inapplicable"
                else:
                    right = "the shared v10 result" if not differs else "v10; v11 changed another cell"
                    passed = not differs
                cells.append({
                    "id": case_id,
                    "activity": activity,
                    "conclusion": conclusion,
                    "boundary": boundary,
                    "observed_activity": "blocked-on-open-counts" if open_counts else seen,
                    "observed_conclusion": seen_conclusion,
                    "axes_match": axes,
                    "allowed_difference": realized_allowed,
                    "open_counts_block_the_activity_test": open_counts,
                    "v10": v10,
                    "v11": v11,
                    "differs": differs,
                    "which_is_right": right,
                    "pass": passed,
                })
    fails = [cell["id"] for cell in cells if not cell["pass"]]
    payload = {
        "cells": cells,
        "count": len(cells),
        "fail_ids": fails,
        "verdict": "PASS" if not fails and len(cells) == 18 else "FAIL",
    }
    write("track0-authority.json", payload)
    print(json.dumps({"verdict": payload["verdict"], "fails": fails}, indent=2))


def _recorded() -> list[tuple[str, list[dict[str, Any]]]]:
    import tests.test_sale_family_audit_v82 as sfa

    track = sfa.track0()
    core = sfa.v82(track)
    found = []
    for name in probe.RECORDED:
        acts = _age(sfa.track0_acts(track, name, "honest", core))
        found.append(("recorded/" + name, acts))
    return found


def _sale_answer(acts: list[dict[str, Any]]) -> list[dict[str, Any]]:
    h = harness()
    sold = h.sale(copy.deepcopy(acts), "no1099b", "st", proceeds=2000, basis=8000, tag="pbr-sale")
    return h.answer(
        sold, q2="yes", form8949="no", path_b="no", ic80="yes",
        exc1_only_2a="no", exc1_no_losses="no",
    )


def matrix(core_json: str) -> None:
    """The four recorded returns plus the synthetic neighbours the charter names."""

    def build() -> list[tuple[str, list[dict[str, Any]]]]:
        lists: list[tuple[str, list[dict[str, Any]]]] = []
        for case_id, acts in _recorded():
            lists.append((case_id + "/unanswered", acts))
            lists.append((case_id + "/answered", _age(_sale_answer(acts))))
        # Exception 1 "no" on each question, with nothing recorded.
        for name, fact in (
            ("exc1-only2a-no", "exception1.only-box2a-capital-gains"),
            ("exc1-nolosses-no", "exception1.no-capital-losses"),
        ):
            unanswered = _exception(_base(), "no")
            unanswered = _say(unanswered, fact, "no", fact)
            unanswered = _activity(unanswered, "none")
            lists.append((name + "/unanswered", _age(unanswered)))
            answered = _boundary(_exception(copy.deepcopy(unanswered), "no"), "answered", sale=False)
            answered = _say(answered, fact, "yes", fact + "-yes")
            lists.append((name + "/answered", _age(answered)))
        # Box 2a only, Exception 1 holding. The distribution is the other form.
        box = add_box2a(_activity(_exception(_base(), "no"), "none"))
        lists.append(("box2a-only/unanswered", _age(box)))
        lists.append(("box2a-only/answered", _age(_boundary(copy.deepcopy(box), "answered", sale=False))))
        # Nothing: Exception 1 holds, no sale, no distribution, no carryover.
        nothing = _activity(_exception(_base(), "no"), "none")
        lists.append(("nothing/unanswered", _age(nothing)))
        lists.append(("nothing/answered", _age(_boundary(copy.deepcopy(nothing), "answered", sale=False))))
        # Capital-loss carryover and no sale. Exception 1 holds: a carryover is
        # not a 2025 sale or a 2025 capital loss.
        carry = _activity(_exception(_base(), "no"), "amount")
        lists.append(("carryover/unanswered", _age(carry)))
        lists.append(("carryover/answered", _age(_boundary(copy.deepcopy(carry), "answered", sale=False))))
        # Schedule D amount from another form: box 2a, with the mistaken
        # Exception 1 "no" the recorded return also uses.
        mistaken = _exception(_base(), "no")
        mistaken = _say(mistaken, "exception1.only-box2a-capital-gains", "no", "only2a")
        mistaken = add_box2a(_activity(mistaken, "none"))
        lists.append(("other-source-box2a/unanswered", _age(mistaken)))
        corrected = _say(copy.deepcopy(mistaken), "exception1.only-box2a-capital-gains", "yes", "only2a-yes")
        lists.append((
            "other-source-box2a/answered",
            _age(_boundary(corrected, "answered", sale=False)),
        ))
        return lists

    lists = _prepared(build)
    runs = both(lists, core_json)
    recorded_hand = {
        "schedule-d.line-3": -6000, "schedule-d.line-7": -6000, "schedule-d.line-21": 3000,
        "form1040.line-7a": -3000, "form1040.line-11a": 47000, "form1040.line-15": 31250,
        "form1040.line-16": 3515, "form1040.line-24": 3515,
        "form1040.line-33": 4500, "form1040.line-37": 0,
    }
    expected = {
        "exc1-only2a-no": WAGE_HAND,
        "exc1-nolosses-no": WAGE_HAND,
        "box2a-only": BOX2A_HAND,
        "nothing": WAGE_HAND,
        "carryover": CARRY_HAND,
        "other-source-box2a": BOX2A_HAND,
    }
    cases = []
    for case_id, _acts in lists:
        if case_id.endswith("/unanswered"):
            continue
        stem = case_id[: -len("/answered")]
        unanswered = runs[stem + "/unanswered"]["v91"]
        answered = runs[stem + "/answered"]["v91"]
        hand = recorded_hand if stem.startswith("recorded/") else expected[stem]
        misses = hand_misses(answered, hand)
        same = runs[stem + "/answered"]["v90"]["lines"] == answered["lines"]
        silent = unanswered["silent"]
        cases.append({
            "id": stem,
            "unanswered_silent": silent,
            "unanswered_parked_silent": unanswered["parked_silent"],
            "unanswered_blocked": len(unanswered["blocked"]),
            "unanswered_page_questions": unanswered["page_questions"],
            "answered_hand_misses": misses,
            "answered_same_lines_as_v90": same,
            "answered_lines": {field: answered["lines"].get(field) for field in hand if field in answered["lines"]},
            "answered_values": {field: answered["values"].get(field) for field in hand if field in answered["values"]},
            "pass": not silent and not misses and same and answered["outcome"] == "success",
        })
    fails = [row["id"] for row in cases if not row["pass"]]
    payload = {"cases": cases, "runs": runs, "fail_ids": fails,
               "verdict": "PASS" if cases and not fails else "FAIL"}
    write("track0-matrix.json", payload)
    print(json.dumps({
        "verdict": payload["verdict"],
        "fails": fails,
        "silent": {row["id"]: row["unanswered_silent"] for row in cases},
        "hands": {row["id"]: row["answered_hand_misses"] for row in cases},
    }, indent=2))


def _four_ways(acts: list[dict[str, Any]]) -> list[tuple[str, list[dict[str, Any]]]]:
    """Each yes/no combination of the four named questions. The no-sale truthful set is no, no, yes, yes."""
    h = harness()
    found = []
    for bits in range(16):
        answers = {
            "q1": "yes" if bits & 1 else "no",
            "q2": "yes" if bits & 2 else "no",
            "form8949": "yes" if bits & 4 else "no",
            "path_b": "yes" if bits & 8 else "no",
        }
        label = "q1-{q1}/q2-{q2}/form8949-{form8949}/pathb-{path_b}".format(**answers)
        found.append((label, _age(h.answer(copy.deepcopy(acts), **answers))))
    return found


def _question_text() -> list[dict[str, str]]:
    """The Exception 1 question citizens the published package resolves."""
    common = evidence_loader.load(probe.BNQ / "common.py", "common")
    core = common.harness().Core("v90", "v88", "v88")
    package = json.loads(core.package_path.read_text(encoding="utf-8"))
    members = {(row.get("id"), row.get("version")) for row in package["members"]}
    found = []
    for short in EXC_SHORT:
        chosen = None
        for path in sorted(core.content.glob("input-question.exception1-*.json")):
            body = json.loads(path.read_text(encoding="utf-8"))
            fact = str((body.get("fact_type") or {}).get("id", ""))
            if not fact.endswith(short):
                continue
            if (body.get("id"), body.get("version")) not in members:
                continue
            chosen = body
        if chosen is None:
            raise SystemExit("no published question for " + short)
        found.append({
            "fact": short,
            "question_id": str(chosen.get("id")).removeprefix(P),
            "version": str(chosen.get("version")),
            "question": chosen.get("question"),
        })
    return found


def _line16_missing() -> list[str]:
    common = evidence_loader.load(probe.BNQ / "common.py", "common")
    core = common.harness().Core("v90", "v88", "v88")
    body = json.loads((core.content / "rule.form1040-line16.v8.json").read_text(encoding="utf-8"))
    found: list[str] = []

    def walk(node: Any) -> None:
        if isinstance(node, dict):
            if node.get("op") == "block":
                found.extend(probe.short(item) for item in node.get("missing") or [])
            for value in node.values():
                walk(value)
        elif isinstance(node, list):
            for value in node:
                walk(value)

    walk(body.get("when"))
    return found


def build_variant(scratch: Path, missing: list[str]) -> dict[str, Any]:
    """A second scratch core. The P0 successor's block also names Exception 1."""
    if scratch.exists():
        raise SystemExit("variant scratch directory already exists")
    import hashlib
    import shutil

    from packages.derivation.package_validation import citizen_checksum
    from tools.package_successor import generate_to_directory

    content, releases = scratch / "content", scratch / "releases"
    shutil.copytree(prototype.CONTENT, content)
    shutil.copytree(prototype.RELEASES, releases)
    body = prototype.successor_body()
    found = 0

    def walk(node: Any) -> None:
        nonlocal found
        if isinstance(node, dict):
            if node.get("op") == "block" and node.get("missing") == prototype.NAMED:
                node["missing"] = list(missing)
                found += 1
                return
            for value in node.values():
                walk(value)
        elif isinstance(node, list):
            for value in node:
                walk(value)

    walk(body["when"])
    if found != 1:
        raise SystemExit("the named block was not found exactly once")
    (content / prototype.SUCCESSOR).write_text(json.dumps(body, indent=2) + "\n", encoding="utf-8")
    changes_path = scratch / "changes.json"
    changes_path.write_text(json.dumps(prototype.changes(body), indent=2) + "\n", encoding="utf-8")
    report = generate_to_directory(
        content / f"package.core-calculations.{prototype.FROM['package']}.json",
        content / f"published-packages.{prototype.FROM['registry']}.json",
        releases / f"{prototype.RELEASE_STEM}.{prototype.FROM['release']}.json",
        content,
        changes_path,
        scratch / "out",
    )
    for src, folder, target in (
        ("package.json", content, f"package.core-calculations.{prototype.TO['package']}.json"),
        ("registry.json", content, f"published-packages.{prototype.TO['registry']}.json"),
        ("release.json", releases, f"{prototype.RELEASE_STEM}.{prototype.TO['release']}.json"),
    ):
        shutil.copy(scratch / "out" / src, folder / target)
    registry_path = content / f"published-packages.{prototype.TO['registry']}.json"
    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    checksum = citizen_checksum(json.loads((content / prototype.SUCCESSOR).read_text(encoding="utf-8")))
    matched = False
    for citizen in registry["citizens"]:
        if citizen["id"] == body["id"] and citizen["version"] == body["version"]:
            citizen["checksum"] = checksum
            matched = True
    if not matched:
        raise SystemExit("variant successor is missing from the generated registry")
    registry_path.write_text(json.dumps(registry, indent=2) + "\n", encoding="utf-8")
    release_path = releases / f"{prototype.RELEASE_STEM}.{prototype.TO['release']}.json"
    release = json.loads(release_path.read_text(encoding="utf-8"))

    def sha(path: Path) -> str:
        return hashlib.sha256(path.read_bytes()).hexdigest()

    release["package_registry_sha256"] = sha(registry_path)
    release_path.write_text(json.dumps(release, indent=2) + "\n", encoding="utf-8")
    core = {
        "version": prototype.TO["package"], "registry": prototype.TO["registry"],
        "release_version": prototype.TO["release"], "content": str(content),
        "releases": str(releases), "loader_from": prototype.FROM["package"],
    }
    (scratch / "core.json").write_text(json.dumps(core, indent=2) + "\n", encoding="utf-8")
    summary = {
        "from": prototype.FROM, "to": prototype.TO,
        "package": report["package"]["version"],
        "successor": prototype.SUCCESSOR,
        "named_questions": [probe.short(name) for name in missing],
        "added_over_p0": [probe.short(name) for name in missing if name not in prototype.NAMED],
    }
    write("track0-variant-build.json", summary)
    return summary


def _pref_blocked(row: dict[str, Any]) -> bool:
    return row.get("producer", {}).get("disposition") == "blocked"


def _has_question(row: dict[str, Any], text: str) -> bool:
    if text in (row.get("page_questions") or []):
        return True
    return any(text in (field.get("questions") or []) for field in row.get("blocked") or [])


def names(core_json: str, variant_dir: str) -> None:
    def build() -> dict[str, Any]:
        recorded = dict(_recorded())
        # Both recorded returns already close every sale family. Each one has a
        # mistaken Exception 1 "no" and no sale left to enter.
        t4 = recorded["recorded/t4_s1_removed"]
        mistaken = recorded["recorded/m_empty_exc1_only2a_no"]
        return {"t4": t4, "mistaken": mistaken, "questions": _question_text(), "line16_missing": _line16_missing()}

    evidence_loader.activate(OWNER)
    try:
        prepared = build()
    finally:
        evidence_loader.finish_all()
    lists: list[tuple[str, list[dict[str, Any]]]] = []
    for stem, base in (("t4", prepared["t4"]), ("mistaken", prepared["mistaken"])):
        for label, acts in _four_ways(base):
            lists.append((f"{stem}/four/{label}", acts))
        cleared = _exception(copy.deepcopy(base), "no")
        lists.append((f"{stem}/exception-yes", _age(cleared)))
    sale = _age(_sale_answer(prepared["t4"]))
    lists.append(("computing-sale", sale))
    p0_runs = both(lists, core_json)
    missing = list(prototype.NAMED) + [P + fact for fact in EXC_SHORT]
    variant = build_variant(Path(variant_dir), missing)
    variant_core = str(Path(variant_dir) / "core.json")
    # The variant is measured on the two blocked returns, the exception-yes
    # resolution, and the computing sale. The 16 combinations stay on v91.
    variant_ids = [
        "t4/four/q1-no/q2-no/form8949-yes/pathb-yes",
        "mistaken/four/q1-no/q2-no/form8949-yes/pathb-yes",
        "t4/exception-yes", "mistaken/exception-yes", "computing-sale",
    ]
    variant_lists = [(case_id, acts) for case_id, acts in lists if case_id in variant_ids]
    evidence_loader.finish_all()
    variant_runs = run_all(variant_lists, variant_core)
    exc_texts = [row["question"] for row in prepared["questions"] if row.get("question")]
    truthful = "q1-no/q2-no/form8949-yes/pathb-yes"

    def unblocked(row: dict[str, Any]) -> bool:
        producer = row.get("producer") or {}
        return producer.get("disposition") in {"published", "inapplicable"} and producer.get("disposition") != "blocked"

    combinations = []
    any_unblocked = False
    for stem in ("t4", "mistaken"):
        for case_id, pair in p0_runs.items():
            if not case_id.startswith(stem + "/four/"):
                continue
            v91 = pair["v91"]
            opened = not _pref_blocked(v91)
            any_unblocked = any_unblocked or opened
            line16 = next((field for field in v91["blocked"] if field["field"] == "form1040.line-16"), None)
            line16_value = v91["lines"].get("form1040.line-16")
            combinations.append({
                "id": case_id,
                "truthful_no_sale": case_id.endswith(truthful),
                "preferential_unblocked": opened,
                "producer": v91["producer"],
                "line16_blocked": line16 is not None,
                "line16_questions": None if line16 is None else line16["questions"],
                "line16_value": line16_value,
                "silent": v91["silent"],
            })
    what_unblocks = {}
    for stem in ("t4", "mistaken"):
        row = p0_runs[stem + "/exception-yes"]["v91"]
        what_unblocks[stem] = {
            "producer": row["producer"],
            "hand_misses": hand_misses(row, WAGE_HAND),
            "silent": row["silent"],
        }
    truthful_rows = [row for row in combinations if row["truthful_no_sale"]]
    line16_same_gap = all(row["line16_blocked"] for row in truthful_rows)
    variant_view = {}
    computing_new: list[str] = []
    shows_exception = False
    for case_id in variant_ids:
        row = compact(variant_runs[case_id])
        variant_view[case_id] = {
            "producer": row["producer"],
            "page_questions": row["page_questions"],
            "silent": row["silent"],
            "duplicate_questions": row["duplicate_questions"],
            "exception_questions_shown": [text for text in exc_texts if _has_question(row, text)],
        }
        if case_id.endswith(truthful) and variant_view[case_id]["exception_questions_shown"]:
            shows_exception = True
    sale_v90 = set(p0_runs["computing-sale"]["v90"]["page_questions"])
    sale_variant = set(variant_view["computing-sale"]["page_questions"])
    computing_new = sorted(sale_variant - sale_v90)
    exception_unblocks = all(not item["hand_misses"] and item["producer"].get("disposition") == "published"
                             for item in what_unblocks.values())
    recommend_variant = (not any_unblocked) and exception_unblocks and shows_exception and not computing_new
    payload = {
        "question_citizens": prepared["questions"],
        "line16_v8_missing": prepared["line16_missing"],
        "line16_names_exception": any(name.startswith("exception1.") for name in prepared["line16_missing"]),
        "combinations": combinations,
        "any_combination_unblocks_preferential": any_unblocked,
        "what_unblocks": what_unblocks,
        "line16_same_gap": line16_same_gap,
        "variant_build": variant,
        "variant_runs": variant_view,
        "variant_shows_exception_question": shows_exception,
        "computing_return_new_questions": computing_new,
        "recommendation": (
            "Also name the four Exception 1 questions. Answering the four sale questions does not unblock, "
            "changing Exception 1 to yes does, the projection shows the Exception 1 sentences, and the "
            "computing sale gains no question."
            if recommend_variant else
            "Keep the P0 four-name successor. The Exception 1 variant did not satisfy the measured bars."
        ),
        "variant_prototyped": "exception names added to the P0 block" if recommend_variant else "measured and not preferred",
        "line16_should_follow": bool(line16_same_gap and recommend_variant),
    }
    write("track0-names.json", payload)
    print(json.dumps({
        "any_unblocked": any_unblocked,
        "exception_unblocks": exception_unblocks,
        "shows_exception": shows_exception,
        "computing_new": computing_new,
        "line16_same_gap": line16_same_gap,
        "recommend_variant": recommend_variant,
        "line16_missing": prepared["line16_missing"],
    }, indent=2))


def late(core_json: str) -> None:
    def build() -> list[tuple[str, list[dict[str, Any]]]]:
        # Start on the realized four-name block: Schedule D required, no
        # activity, and the no-sale boundary answered. An open boundary
        # blocks the activity test on family counts before that block.
        blocked = _age(_boundary(
            _activity(_exception(_base(), "required"), "none"),
            "answered",
            sale=False,
        ))
        sold = _age(_sale_answer(blocked))
        removed = remove_sale(sold, "no1099b", "st", "pbr-sale")
        # The sale's boundary answers stay, and Exception 1 stays "no".
        exception_yes = _age(_exception(copy.deepcopy(blocked), "no"))
        return [
            ("blocked", blocked),
            ("sale-entered", sold),
            ("sale-removed", _age(removed)),
            ("exception-yes", exception_yes),
        ]

    lists = _prepared(build)
    runs = both(lists, core_json)
    sale = runs["sale-entered"]["v91"]
    removed = runs["sale-removed"]["v91"]
    removed_v90 = runs["sale-removed"]["v90"]
    cleared = runs["exception-yes"]["v91"]
    blocked = runs["blocked"]["v91"]
    sale_hand = {
        "schedule-d.line-3": -6000, "schedule-d.line-7": -6000, "schedule-d.line-21": 3000,
        "form1040.line-7a": -3000, "form1040.line-11a": 47000, "form1040.line-15": 31250,
        "form1040.line-16": 3515, "form1040.line-24": 3515,
        "form1040.line-33": 4500, "form1040.line-37": 0,
    }
    # Removing the sale row leaves the "I sold" answers in place, so this
    # return is not the no-activity cell. Both cores must drop the published
    # sale value together. Restoring the four-name else is the allowed
    # difference only when the activity test itself resolves to none.
    removal_same = signature(removed["producer"]) == signature(removed_v90["producer"])
    removal_allowed = (
        removed["producer"].get("disposition") == "blocked"
        and removed["producer"].get("missing") == FOUR
        and removed_v90["producer"].get("disposition") == "inapplicable"
    )
    checks = {
        "blocked_names_four": blocked["producer"].get("disposition") == "blocked" and blocked["producer"].get("missing") == FOUR,
        "blocked_start_fields_name_the_question": blocked["silent"] == [],
        "sale_clears_and_matches_hand": sale["producer"].get("disposition") == "published" and not hand_misses(sale, sale_hand),
        "sale_matches_v90_lines": runs["sale-entered"]["v90"]["lines"] == sale["lines"],
        "removal_drops_the_sale_with_v90": removed["lines"] == removed_v90["lines"] and (removal_same or removal_allowed),
        "exception_yes_publishes_wage_hand": cleared["producer"].get("disposition") == "published" and not hand_misses(cleared, WAGE_HAND),
        "exception_yes_matches_v90_lines": runs["exception-yes"]["v90"]["lines"] == cleared["lines"],
    }
    payload = {
        "steps": runs, "checks": checks, "sale_hand_misses": hand_misses(sale, sale_hand),
        "wage_hand_misses": hand_misses(cleared, WAGE_HAND),
        "removal_missing": {
            "v90": removed_v90["producer"].get("missing"),
            "v91": removed["producer"].get("missing"),
        },
        "verdict": "PASS" if all(checks.values()) else "FAIL",
    }
    write("track0-late.json", payload)
    print(json.dumps({"verdict": payload["verdict"], "checks": checks,
                      "sale_misses": payload["sale_hand_misses"],
                      "wage_misses": payload["wage_hand_misses"],
                      "removal_missing": payload["removal_missing"]}, indent=2))


def _member_body(core: Any, member: dict[str, Any]) -> dict[str, Any]:
    slug = str(member["id"]).removeprefix(P + "rule.")
    for name in (f"rule.{slug}.{member['version']}.json", f"rule.{slug}.json"):
        path = core.content / name
        if path.exists():
            body = json.loads(path.read_text(encoding="utf-8"))
            if body.get("version") == member["version"]:
                return body
    raise SystemExit("missing rule body for " + str(member["id"]))


def _changed(old: Any, new: Any, prefix: str = "") -> list[str]:
    if old == new:
        return []
    if isinstance(old, dict) and isinstance(new, dict):
        found = []
        for key in sorted(set(old) | set(new)):
            found.extend(_changed(old.get(key), new.get(key), prefix + "/" + str(key)))
        return found
    if isinstance(old, list) and isinstance(new, list) and len(old) == len(new):
        found = []
        for index, (left, right) in enumerate(zip(old, new)):
            found.extend(_changed(left, right, prefix + f"/{index}"))
        return found
    return [prefix or "/"]


def reuse(core_json: str) -> None:
    evidence_loader.activate(OWNER)
    common = evidence_loader.load(probe.BNQ / "common.py", "common")
    h = common.harness()
    old = h.Core("v90", "v88", "v88")
    new = probe._core_from(h, core_json)
    old_package = json.loads(old.package_path.read_text(encoding="utf-8"))
    new_package = json.loads(new.package_path.read_text(encoding="utf-8"))
    old_members = {member["id"]: member for member in old_package["members"]}
    changed_members = []
    for member in new_package["members"]:
        prior = old_members.get(member["id"])
        if prior is None or prior.get("version") == member.get("version"):
            continue
        changed_members.append({"id": probe.short(member["id"]), "old": prior.get("version"), "new": member.get("version")})
    old_body = _member_body(old, old_members[P + "rule.selected-preferential-base"])
    new_body = _member_body(new, next(member for member in new_package["members"] if member["id"].endswith("selected-preferential-base")))
    normalized = copy.deepcopy(new_body)
    normalized["version"] = old_body["version"]
    normalized["schema"] = old_body["schema"]
    # Undo only the authorized else rewrite, then the bodies must match.
    undone = 0

    def walk(node: Any) -> None:
        nonlocal undone
        if isinstance(node, dict):
            choice = node.get("else")
            if (
                node.get("op") == "choose"
                and node.get("then") is True
                and isinstance(choice, dict)
                and choice.get("op") == "choose"
                and choice.get("then") is True
                and isinstance(choice.get("else"), dict)
                and choice["else"].get("op") == "block"
            ):
                node["else"] = choice.get("when")
                undone += 1
                return
            for value in node.values():
                walk(value)
        elif isinstance(node, list):
            for value in node:
                walk(value)

    walk(normalized.get("when"))
    diffs = _changed(old_body, normalized)
    # A v90 workspace: the wage return and the sale return, opened on v91.
    def build() -> list[tuple[str, list[dict[str, Any]]]]:
        wage = _age(_boundary(_activity(_exception(_base(), "no"), "none"), "answered", sale=False))
        blocked = _age(_boundary(
            _activity(_exception(_base(), "required"), "none"), "answered", sale=False,
        ))
        return [("wage", wage), ("sale", _age(_sale_answer(blocked)))]

    lists = build()
    evidence_loader.finish_all()
    runs = both(lists, core_json)
    new_questions = {
        case_id: sorted(set(pair["v91"]["page_questions"]) - set(pair["v90"]["page_questions"]))
        for case_id, pair in runs.items()
    }
    checks = {
        "one_successor": changed_members == [{"id": "selected-preferential-base", "old": "v10", "new": "v11"}],
        "undoing_the_else_leaves_v10": undone == 1 and not diffs,
        "no_new_question_on_wage_workspace": new_questions["wage"] == [],
        "no_new_question_on_sale_workspace": new_questions["sale"] == [],
        "wage_lines_unchanged": runs["wage"]["v90"]["lines"] == runs["wage"]["v91"]["lines"],
        "sale_lines_unchanged": runs["sale"]["v90"]["lines"] == runs["sale"]["v91"]["lines"],
    }
    payload = {
        "changed_members": changed_members,
        "differences_after_undoing_the_else": diffs,
        "new_questions": new_questions,
        "checks": checks,
        "verdict": "PASS" if all(checks.values()) else "FAIL",
    }
    write("track0-reuse.json", payload)
    print(json.dumps({"verdict": payload["verdict"], "checks": checks, "diffs": diffs[:12]}, indent=2))


def neighbour(part: str, log: str, workers: int) -> None:
    loaded = json.loads(Path(part).read_text(encoding="utf-8"))
    results = loaded["results"] if isinstance(loaded.get("results"), dict) else loaded
    body = rerun.classify(results)
    numbers = []
    for row in body["numbers_changed"]:
        pins = (results.get(row["id"]) or {}).get("pins") or {}
        left = (pins.get("v90") or {}).get("rows") or {}
        right = (pins.get("v91") or {}).get("rows") or {}
        changed_rows = sorted(set(left) | set(right))
        changed_rows = [name for name in changed_rows if left.get(name) != right.get(name)]
        left_questions = (pins.get("v90") or {}).get("questions") or []
        right_questions = (pins.get("v91") or {}).get("questions") or []
        numbers.append({
            "id": row["id"],
            "number_fields": row["number_fields"],
            "line_diffs": row["lines"],
            "changed_rows": changed_rows,
            "v90_preferential": left.get("selected-preferential-base"),
            "v91_preferential": right.get("selected-preferential-base"),
            "questions_added": sorted(set(right_questions) - set(left_questions)),
            "questions_removed": sorted(set(left_questions) - set(right_questions)),
        })
    question_diffs = []
    for key, row in results.items():
        pins = (row or {}).get("pins") or {}
        left_questions = (pins.get("v90") or {}).get("questions") or []
        right_questions = (pins.get("v91") or {}).get("questions") or []
        added = sorted(set(right_questions) - set(left_questions))
        removed = sorted(set(left_questions) - set(right_questions))
        if added or removed:
            question_diffs.append({"id": key, "added": added, "removed": removed})
    line_value_changes = [row["id"] for row in numbers if row["line_diffs"]]
    changed_ids = sorted(row["id"] for row in numbers)
    checks = {
        "lists": len(results) == 775,
        "no_line_value_changed": not line_value_changes,
        "no_computing_return_gained_a_question": not body["newly_asked_on_computing_return"],
        "no_computing_return_lost_a_question": not body["questions_removed_on_computing_return"],
        "question_changes_only_on_the_changed_lists": (
            sorted(item["id"] for item in question_diffs) == changed_ids
            and all(not item["removed"] for item in question_diffs)
        ),
    }
    payload = {
        "cores": "published core v90 and the recommended scratch successor",
        "lists": len(results),
        "workers": workers,
        "wall_time_s": rerun._wall_time(Path(log)),
        "counts": body["counts"],
        "by_set": body["by_set"],
        "numbers_changed": numbers,
        "question_diffs": question_diffs,
        "line_value_changes": line_value_changes,
        "newly_asked_on_computing_return": body["newly_asked_on_computing_return"],
        "questions_removed_on_computing_return": body["questions_removed_on_computing_return"],
        "checks": checks,
        "verdict": "PASS" if all(checks.values()) else "FAIL",
    }
    write("track0-neighbour.json", payload)
    print(json.dumps({
        "verdict": payload["verdict"], "lists": payload["lists"], "counts": payload["counts"],
        "wall_time_s": payload["wall_time_s"], "line_value_changes": line_value_changes,
        "new_questions": len(payload["newly_asked_on_computing_return"]),
    }, indent=2))


def surface(core_json: str) -> None:
    """Four recorded returns and two neighbours, field questions on both cores."""

    def build() -> list[tuple[str, list[dict[str, Any]]]]:
        lists = [(case_id, acts) for case_id, acts in _recorded()]
        carry = _activity(_exception(_base(), "no"), "amount")
        box = add_box2a(_activity(_exception(_base(), "no"), "none"))
        lists.append(("neighbour/carryover", _age(carry)))
        lists.append(("neighbour/box2a", _age(box)))
        return lists

    lists = _prepared(build)
    runs = both(lists, core_json)
    rows = []
    for case_id, _acts in lists:
        pair = runs[case_id]
        v90_blocked = {field["field"]: field for field in pair["v90"]["blocked"]}
        became_blocked = sorted(
            field for field, row in v90_blocked.items()
            if field not in {item["field"] for item in pair["v91"]["blocked"]}
            and False
        )
        # A field that computed on v90 is one with a numeric line. It fails if v91 blocks it.
        computed = []
        for field, value in pair["v90"]["lines"].items():
            if isinstance(value, (int, float)) and not isinstance(value, bool):
                if any(item["field"] == field for item in pair["v91"]["blocked"]):
                    computed.append(field)
        rows.append({
            "id": case_id,
            "v90_page_questions": pair["v90"]["page_questions"],
            "v91_page_questions": pair["v91"]["page_questions"],
            "v90_fields": [{"field": field["field"], "questions": field["questions"]} for field in pair["v90"]["blocked"]],
            "v91_fields": [{"field": field["field"], "questions": field["questions"]} for field in pair["v91"]["blocked"]],
            "duplicate_questions": pair["v91"]["duplicate_questions"],
            "computed_on_v90_blocked_on_v91": sorted(computed),
            "silent": pair["v91"]["silent"],
            "pass": not pair["v91"]["duplicate_questions"] and not computed and not pair["v91"]["silent"],
        })
        del became_blocked
    fails = [row["id"] for row in rows if not row["pass"]]
    payload = {"cases": rows, "fail_ids": fails, "verdict": "PASS" if rows and not fails else "FAIL"}
    write("track0-surface.json", payload)
    print(json.dumps({"verdict": payload["verdict"], "fails": fails}, indent=2))


def main() -> None:
    command = sys.argv[1] if len(sys.argv) > 1 else ""
    if command == "authority" and len(sys.argv) == 3:
        authority(sys.argv[2])
    elif command == "matrix" and len(sys.argv) == 3:
        matrix(sys.argv[2])
    elif command == "names" and len(sys.argv) == 4:
        names(sys.argv[2], sys.argv[3])
    elif command == "late" and len(sys.argv) == 3:
        late(sys.argv[2])
    elif command == "reuse" and len(sys.argv) == 3:
        reuse(sys.argv[2])
    elif command == "neighbour" and len(sys.argv) == 8 and sys.argv[2:7:2] == ["--part", "--log", "--workers"]:
        neighbour(sys.argv[3], sys.argv[5], int(sys.argv[7]))
    elif command == "surface" and len(sys.argv) == 3:
        surface(sys.argv[2])
    else:
        raise SystemExit(
            "usage: track0.py authority|matrix|late|reuse|surface <scratch-core.json> | "
            "names <scratch-core.json> <variant-directory> | "
            "neighbour --part <part> --log <time-log> --workers N"
        )


if __name__ == "__main__":
    main()
