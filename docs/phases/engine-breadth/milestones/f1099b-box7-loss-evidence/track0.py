"""Track 0 runs for Form 1099-B box 7 beside a loss.

Evidence for docs/phases/engine-breadth/milestones/f1099b-box7-loss.md.
Charter: docs/reviews/f1099b-box7-loss/charter-track0.md.

    python3 track0.py <scratch-core.json> <authority|matrix|late|reuse|surface>

Loads the milestone probe under a unique module name. Does not assign another
module's globals. Hand values come from probe.hand_return (the 2025 method),
not from a publication. Synthetic demo.* only.
"""

from __future__ import annotations

import copy
import importlib.util
import json
import os
import sys
import tempfile
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

PROBE_NAME = "f1099b_box7_track0_probe"
FAMILY = (
    ("covered-st", "covered", "st"),
    ("covered-lt", "covered", "lt"),
    ("covered-w-st", "w", "st"),
    ("covered-w-lt", "w", "lt"),
    ("noncovered-st", "noncovered", "st"),
    ("noncovered-lt", "noncovered", "lt"),
    ("code-b-st", "codeb", "st"),
    ("code-b-lt", "codeb", "lt"),
)
SIGNS = {
    "gain": (2000.0, 1000.0, 1000.0),
    "loss": (1000.0, 2000.0, -1000.0),
    "zero": (1000.0, 1000.0, 0.0),
}
REFUSAL = (
    "Schedule D line 16 has no value yet. It is waiting for line 7 or line 15. "
    "It is also blocked while a recorded Form 1099-B statement has no answer about box 7. "
    "It is blocked when box 7 is checked and a sale on that statement is at a loss: "
    "a loss based on the box 1d amount is not allowed, and this return does not compute it."
)
BOX7_FACT = "f1099b.statement-box7-loss-not-allowed"
CONSUMER_FIELDS = (
    "schedule-d.line-16", "schedule-d.line-17", "schedule-d.line-18", "schedule-d.line-19",
    "schedule-d.line-20", "schedule-d.line-21", "schedule-d.line-22",
    "form1040.line-7a", "form1040.line-15", "form1040.line-16", "form1040.line-24",
    "form1040.line-33", "form1040.line-34", "form1040.line-37",
)
RULE_OF = {
    "schedule-d.line-16": "rule.schedule-d-line16",
    "schedule-d.line-21": "rule.schedule-d-line21",
    "form1040.line-7a": "rule.form1040-line7a",
    "form1040.line-15": "rule.form1040-line15",
    "form1040.line-16": "rule.form1040-line16",
    "form1040.line-24": "rule.form1040-line24",
    "form1040.line-33": "rule.form1040-line33",
    "form1040.line-34": "rule.form1040-line34",
    "form1040.line-37": "rule.form1040-line37",
}


def load_probe() -> Any:
    module = sys.modules.get(PROBE_NAME)
    if module is None:
        spec = importlib.util.spec_from_file_location(PROBE_NAME, HERE / "probe.py")
        assert spec is not None and spec.loader is not None
        module = importlib.util.module_from_spec(spec)
        sys.modules[PROBE_NAME] = module
        spec.loader.exec_module(module)
    return module


def question_text() -> str:
    body = json.loads(
        (REPO / "packages/content/tax/2025/input-question.f1099b-statement-box7-loss-not-allowed.json").read_text(
            encoding="utf-8"))
    return str(body["question"])


def scratch_core(probe: Any, core_path: Path) -> Any:
    body = json.loads(core_path.read_text(encoding="utf-8"))
    return probe.h.Core(
        body["version"], body["registry"], body["release_version"],
        content=Path(body["content"]), releases=Path(body["releases"]),
        loader_from=body.get("loader_from"),
    )


def published_v83(probe: Any) -> Any:
    return probe.h.Core("v83", "v81", "v81")


def num(value: Any) -> Any:
    if isinstance(value, bool) or value is None:
        return value
    if isinstance(value, (int, float)):
        return int(value) if float(value).is_integer() else value
    if isinstance(value, str):
        try:
            parsed = float(value)
        except ValueError:
            return value
        return int(parsed) if parsed.is_integer() else parsed
    return value


def refresh_exception1(probe: Any, acts: list[dict[str, Any]], core: Any) -> list[dict[str, Any]]:
    fresh = probe.h.honest_exception1(acts)
    if fresh.get("exc1_only_2a") is None and fresh.get("exc1_no_losses") is None:
        fresh = {"exc1_only_2a": "yes", "exc1_no_losses": "yes"}
    return probe.h.answer(acts, core.content, **{key: value for key, value in fresh.items() if value is not None})


def snapshot(probe: Any, acts: list[dict[str, Any]], slug: str | None = None) -> dict[str, Any]:
    box7 = []
    closures = []
    for act in acts:
        if act.get("kind") != "assertion":
            continue
        finding = (act.get("payload") or {}).get("finding") or {}
        fact_id = str(finding.get("fact_id") or "")
        if BOX7_FACT + "|" in fact_id:
            box7.append({"id": finding.get("id"), "fact_id": fact_id, "value": finding.get("value")})
        if ".source-closure|" in fact_id and (slug is None or f"f1099b.{slug}." in fact_id or fact_id.startswith(
                f"tax.us.2025.f1099b.{slug}.source-closure")):
            closures.append({"id": finding.get("id"), "fact_id": fact_id})
    horizons: list[str] = []
    if slug is not None:
        kind, term = next((kind, term) for name, kind, term in FAMILY if name == slug)
        horizons = probe.h.horizons(acts, probe.h.family_id(kind, term, None))
    return {"box7": box7, "closures": closures, "horizons": horizons}


def _watched_row(row: dict[str, Any]) -> dict[str, Any]:
    artifact = str(row.get("artifact_id") or "")
    raw = str(row.get("symbol")).removeprefix("tax.us.2025.") if row.get("symbol") else ""
    base, _, subject = raw.partition("|")
    return {
        "artifact": artifact.removeprefix("tax.us.2025."),
        "disposition": row.get("disposition"),
        "code": row.get("code"),
        "missing": [str(item).removeprefix("tax.us.2025.") for item in (row.get("missing") or [])],
        "symbol": base or None,
        "subject": subject or None,
        "finding_id": row.get("finding_id"),
    }


def _interesting(name: str) -> bool:
    base = name.split("|", 1)[0]
    tokens = ("box7-verdict", "box7-loss-check", "schedule-d.line", "schedule-d-line",
              "form1040.line", "form1040-line", "selected-preferential", "-count")
    return any(token in base for token in tokens)


def execute(core: Any, acts: list[dict[str, Any]], run_id: str) -> dict[str, Any]:
    probe = load_probe()
    from packages.derivation.live import live_coordinate_run
    from packages.derivation.live_workspace import WorkspaceCapability
    from packages.derivation.presentation_projection import validate_presentation_model

    try:
        with probe.h.loader_entries(core):
            surface = core.surface()
            finished = probe.h._handover(probe.h._finish(
                copy.deepcopy(acts), package_path=core.package_path, package_version=core.version,
                release_path=core.release_path, release_version=core.release_version, note=run_id,
            ), surface=surface, reconfirm=True)
            with tempfile.TemporaryDirectory() as tmp:
                outcome = live_coordinate_run(
                    WorkspaceCapability(Path(tmp) / "L"), repo_root=REPO, authoritative_acts=finished,
                    workspace_revision=len(finished), run_scope={"jurisdiction": "us", "year": probe.YEAR},
                    scope_user=probe.h.ccr.USER, request={"schema": "run-request.v1"}, run_id=run_id,
                    governance_pins=[], surface=surface, output_name="out.json")
                if outcome.refusal is not None:
                    return {"outcome": "refusal", "reason": outcome.refusal.reason,
                            "message": probe.h.scrub(str(outcome.refusal.detail))[:400]}
                model = json.loads(outcome.presentation_path.read_text(encoding="utf-8"))
                report = json.loads(outcome.output_path.read_text(encoding="utf-8"))
                valid: Any = True
                try:
                    validate_presentation_model(model)
                except Exception as exc:  # noqa: BLE001 — the probe records a bad model
                    valid = probe.h.scrub(str(exc))[:300]
                publications = []
                for pub in outcome.publications:
                    finding = pub.finding
                    symbol = str(finding.get("symbol") or "")
                    if _interesting(symbol):
                        raw = symbol.removeprefix("tax.us.2025.")
                        base, _, subject = raw.partition("|")
                        publications.append({
                            "symbol": base,
                            "subject": subject or None,
                            "value": num(finding.get("value")),
                            "finding_id": finding.get("id"),
                        })
    except Exception as exc:  # noqa: BLE001 — a rejected return is a measured result
        return {"outcome": "error", "error": type(exc).__name__, "message": probe.h.scrub(str(exc))[:500]}

    lines: dict[str, Any] = {}
    reasons: dict[str, list[str]] = {}
    questions: list[str] = []
    consumers: dict[str, Any] = {name: {"present": False} for name in CONSUMER_FIELDS}
    line16_field: dict[str, Any] | None = None
    for section in model.get("sections") or []:
        field = section.get("field") or {}
        short = str(field.get("id") or "").removeprefix("tax.us.2025.")
        resolved = section.get("resolved") or {}
        sentences = [str(reason.get("sentence") or "") for reason in (resolved.get("reasons") or [])
                     if isinstance(reason, dict) and reason.get("sentence")]
        for sentence in sentences:
            if sentence.endswith("?") and sentence not in questions:
                questions.append(sentence)
        if short in probe.LINES:
            value = resolved.get("value")
            disposition = str(resolved.get("disposition"))
            if value is None or "blocked" in disposition:
                lines[short] = disposition
            else:
                lines[short] = num(value)
            if "blocked" in disposition:
                reasons[short] = [probe.h.scrub(sentence)[:240] for sentence in sentences]
        if short in consumers:
            blocked = ((field.get("dispositions") or {}).get("blocked") or {})
            consumers[short] = {
                "present": True,
                "binds_symbol": str(field.get("binds_symbol") or "").removeprefix("tax.us.2025."),
                "field_version": field.get("version"),
                "disposition": resolved.get("disposition"),
                "value": num(resolved.get("value")) if resolved.get("value") is not None else None,
                "reasons": sentences,
                "blocked_explain": blocked.get("explain"),
            }
        if short == "schedule-d.line-16":
            blocked = ((field.get("dispositions") or {}).get("blocked") or {})
            line16_field = {
                "version": field.get("version"),
                "description": field.get("description"),
                "blocked_explain": blocked.get("explain"),
                "disposition": resolved.get("disposition"),
                "value": num(resolved.get("value")) if resolved.get("value") is not None else None,
                "reasons": sentences,
            }
    rows = [_watched_row(row) for row in (report.get("dispositions") or [])
            if _interesting(str(row.get("artifact_id") or ""))]
    return {
        "outcome": "success",
        "stop": report.get("stop_reason"),
        "presentation_valid": valid,
        "lines": lines,
        "reasons": reasons,
        "questions": [probe.h.scrub(question)[:300] for question in questions],
        "publications": publications,
        "rows": rows,
        "consumers": consumers,
        "line16_field": line16_field,
        "line16_rows": [row for row in rows if row["artifact"] == "rule.schedule-d-line16"],
    }


def pub_values(result: dict[str, Any], symbol: str) -> list[Any]:
    return [row["value"] for row in result.get("publications") or [] if row["symbol"] == symbol]


def row_for(result: dict[str, Any], artifact: str) -> list[dict[str, Any]]:
    return [row for row in result.get("rows") or [] if row["artifact"] == artifact]


def hand_failures(result: dict[str, Any], hand: dict[str, Any]) -> list[str]:
    found = []
    for line, expected in hand.items():
        got = (result.get("lines") or {}).get(line)
        if got != expected:
            found.append(f"{line}: hand {expected} got {got}")
    return found


def count_failures(result: dict[str, Any], expected: dict[str, int]) -> list[str]:
    found = []
    for slug, wanted in expected.items():
        got = pub_values(result, f"f1099b.{slug}-count")
        if got != [wanted]:
            found.append(f"{slug}-count: expected [{wanted}] got {got}")
    return found


def check_symbol(slug: str) -> str:
    return f"f1099b.{slug}-txn.box7-loss-check"


def verdict_symbol(slug: str) -> str:
    return f"f1099b.{slug}-txn.box7-verdict"


def contract_failures(case: dict[str, Any], result: dict[str, Any], question: str) -> list[str]:
    if result.get("outcome") != "success":
        return [f"outcome {result.get('outcome')} {result.get('error') or result.get('reason')}"]
    found: list[str] = []
    if result.get("presentation_valid") is not True:
        found.append(f"presentation {result.get('presentation_valid')}")
    kind = case["kind"]
    slug = case.get("slug")
    if kind in {"hand", "empty", "statement_scope"}:
        found.extend(hand_failures(result, case["hand"]))
    if case.get("counts"):
        found.extend(count_failures(result, case["counts"]))
    if kind == "yes_loss":
        found.extend(_loss_block(result, slug, question, allow_question=False))
    if kind == "unanswered":
        found.extend(_unanswered(result, slug, question))
    if kind == "absence":
        missing = (row_for(result, "rule.schedule-d-line16") or [{}])[0].get("missing") or []
        if f"f1099b.{slug}-count" not in missing:
            found.append(f"line 16 missing {missing} does not name {slug}-count")
    if kind == "empty":
        for name, _kind, _term in FAMILY:
            if pub_values(result, check_symbol(name)) != [0]:
                found.append(f"{name} check {pub_values(result, check_symbol(name))}")
            if pub_values(result, f"f1099b.{name}-count") != [0]:
                found.append(f"{name} count {pub_values(result, f'f1099b.{name}-count')}")
        if result.get("questions"):
            found.append(f"empty return asked {result.get('questions')}")
    if kind == "statement_scope":
        values = pub_values(result, verdict_symbol("covered-st"))
        if values != ["clear", "clear"]:
            found.append(f"cross-statement verdicts {values}")
        if pub_values(result, check_symbol("covered-st")) != [0]:
            found.append(f"cross-statement check {pub_values(result, check_symbol('covered-st'))}")
    if kind == "same_statement":
        values = pub_values(result, verdict_symbol("covered-st"))
        if sorted(str(item) for item in values) != ["clear", "disallowed"]:
            found.append(f"same-statement verdicts {values}")
        found.extend(_loss_block(result, "covered-st", question, allow_question=False))
    if kind == "covered_flag":
        sentence = "Record this sale as a noncovered sale. The broker did not report its basis to the IRS."
        blob = json.dumps(result.get("reasons") or {})
        if sentence not in blob:
            found.append("covered-flag sentence absent")
    if len(result.get("line16_rows") or []) != 1 and kind != "covered_flag":
        found.append(f"line 16 cardinality {len(result.get('line16_rows') or [])}")
    field = result.get("line16_field") or {}
    if kind != "covered_flag" and field.get("blocked_explain") != REFUSAL:
        found.append("line 16 field explain is not the narrowed sentence")
    if field.get("version") != "v4" and kind != "covered_flag":
        found.append(f"line 16 field version {field.get('version')}")
    return found


def _loss_block(result: dict[str, Any], slug: str, question: str, *, allow_question: bool) -> list[str]:
    found = []
    if pub_values(result, verdict_symbol(slug)) != ["disallowed"] and slug:
        # same-statement has two verdicts; caller checks those itself when slug is covered and kind differs
        if "disallowed" not in [str(item) for item in pub_values(result, verdict_symbol(slug))]:
            found.append(f"verdict {pub_values(result, verdict_symbol(slug))}")
    checks = row_for(result, f"rule.f1099b.{slug}-txn.box7-loss-check")
    if not checks or checks[0].get("disposition") != "blocked" or checks[0].get("missing") not in ([],):
        found.append(f"check row {checks[:1]}")
    line = row_for(result, "rule.schedule-d-line16")
    if not line or line[0].get("disposition") != "blocked" or check_symbol(slug) not in (line[0].get("missing") or []):
        found.append(f"line 16 row {line[:1]}")
    if question in (result.get("questions") or []) and not allow_question:
        found.append("yes-loss asked the box 7 question")
    reasons = (result.get("line16_field") or {}).get("reasons") or []
    if reasons and not allow_question:
        found.append(f"yes-loss line 16 reasons {reasons}")
    return found


def _unanswered(result: dict[str, Any], slug: str, question: str) -> list[str]:
    found = []
    if question not in (result.get("questions") or []):
        found.append(f"questions {result.get('questions')}")
    checks = row_for(result, f"rule.f1099b.{slug}-txn.box7-loss-check")
    verdicts = row_for(result, f"rule.f1099b.{slug}-txn.box7-verdict")
    named = any(BOX7_FACT in (row.get("missing") or []) for row in (*checks, *verdicts))
    if not named:
        found.append(f"unanswered missing checks={checks[:1]} verdicts={verdicts[:1]}")
    line = (result.get("lines") or {}).get("schedule-d.line-16")
    if not (isinstance(line, str) and "blocked" in line):
        found.append(f"line 16 {line}")
    return found


def one_sale(probe: Any, core: Any, slug: str, sign: str, answer: str | None, tag: str = "s"
             ) -> tuple[list[dict[str, Any]], list[tuple[str, str, float]]]:
    """One sale. Code B shifts the basis the broker showed so a correction exists.

    A code B member whose shown basis equals the correct basis is refused
    (CODE_B_WITHOUT_CORRECTION) and line 1b or 8b never publishes. Column (h)
    stays proceeds minus the correct basis.
    """
    _name, kind, term = next(row for row in FAMILY if row[0] == slug)
    proceeds, basis, column = SIGNS[sign]
    kwargs: dict[str, Any] = {}
    if kind == "codeb":
        kwargs["corrected"] = basis
        basis = basis + 500.0
    acts = probe.h.opened()
    acts = probe.h.sale(acts, kind, term, tag=tag, proceeds=proceeds, basis=basis, **kwargs)
    acts = probe.prepare(acts, core, {kind}, column < 0)
    if answer is not None:
        acts = probe.box7(acts, core, {"*": answer})
    return acts, [(kind, term, column)]


def wage(probe: Any, core: Any) -> list[dict[str, Any]]:
    acts = probe.h.opened()
    return probe.prepare(acts, core, set(), False)


def counts_for(active: dict[str, int] | None = None) -> dict[str, int]:
    expected = {slug: 0 for slug, _kind, _term in FAMILY}
    expected.update(active or {})
    return expected


def build_authority(probe: Any, core: Any) -> list[dict[str, Any]]:
    cases = []
    for slug, _kind, _term in FAMILY:
        for sign, answer, kind in (("gain", "yes", "hand"), ("loss", "yes", "yes_loss")):
            acts, sales = one_sale(probe, core, slug, sign, answer)
            cases.append({
                "id": f"alc_{slug}_{sign}",
                "kind": kind,
                "slug": slug,
                "acts": acts,
                "hand": probe.hand_return(sales) if kind == "hand" else None,
                "counts": counts_for({slug: 1}),
                "note": f"{slug} box 7 yes beside a {sign}",
            })
    acts, sales = one_sale(probe, core, "covered-st", "gain", None)
    cases.append({
        "id": "alc_covered_st_unanswered", "kind": "unanswered", "slug": "covered-st",
        "acts": acts, "hand": None, "note": "One covered short-term gain and no box 7 answer",
    })
    acts = probe.h.opened()
    acts = probe.h.sale(acts, "covered", "st", tag="ya", proceeds=2000, basis=1000)
    acts = probe.h.sale(acts, "covered", "st", tag="nb", proceeds=2000, basis=2400)
    acts = probe.prepare(acts, core, {"covered"}, True)
    acts = probe.box7(acts, core, {"demo.sfa.ya.statement": "yes", "demo.sfa.nb.statement": "no"})
    cases.append({
        "id": "alc_statement_scope", "kind": "statement_scope", "slug": "covered-st",
        "acts": acts, "hand": probe.hand_return([("covered", "st", 1000), ("covered", "st", -400)]),
        "counts": counts_for({"covered-st": 2}),
        "note": "Yes on the gain statement. The loss is on the statement answered no.",
    })
    acts = probe.h.opened()
    acts = probe.h.sale(acts, "covered", "st", tag="both", proceeds=2000, basis=1000)
    acts = probe.sale_on(acts, "covered", "st", "loss", statement_tag="both", proceeds=1000, basis=2000)
    acts = probe.prepare(acts, core, {"covered"}, True)
    acts = probe.box7(acts, core, {"*": "yes"})
    cases.append({
        "id": "alc_same_statement", "kind": "same_statement", "slug": "covered-st",
        "acts": acts, "hand": None, "counts": counts_for({"covered-st": 2}),
        "note": "A gain and a loss on one box 7 yes statement. Line 16 stays unpublished.",
    })
    acts = probe.h.opened()
    acts = probe.h.sale(acts, "covered", "st", tag="a", proceeds=2000, basis=1000)
    acts = probe.h.sale(acts, "covered", "st", tag="b", proceeds=2000, basis=1000)
    acts = probe.prepare(acts, core, {"covered"}, False)
    acts = probe.box7(acts, core, {"*": "no"})
    cases.append({
        "id": "alc_count_two", "kind": "hand", "slug": "covered-st", "acts": acts,
        "hand": probe.hand_return([("covered", "st", 1000), ("covered", "st", 1000)]),
        "counts": counts_for({"covered-st": 2}),
        "note": "Two current covered short-term sales. The count is 2.",
    })
    cases.append({
        "id": "alc_closed_empty", "kind": "empty", "slug": None, "acts": wage(probe, core),
        "hand": probe.hand_return([]), "note": "No sale. Every family check is 0 and every count is 0.",
    })
    return cases


def build_matrix(probe: Any, core: Any) -> list[dict[str, Any]]:
    states = (
        ("no", "loss", "no", "hand"),
        ("yes_gain", "gain", "yes", "hand"),
        ("yes_loss", "loss", "yes", "yes_loss"),
        ("yes_zero", "zero", "yes", "hand"),
        ("unanswered", "gain", None, "unanswered"),
    )
    cases = []
    for slug, _kind, _term in FAMILY:
        for state, sign, answer, kind in states:
            acts, sales = one_sale(probe, core, slug, sign, answer)
            cases.append({
                "id": f"m_{slug}_{state}",
                "kind": kind,
                "slug": slug,
                "acts": acts,
                "hand": probe.hand_return(sales) if kind == "hand" else None,
                "counts": counts_for({slug: 1}) if kind == "hand" else None,
                "note": f"{slug} {state}",
            })
    cases.append({
        "id": "m_closed_empty", "kind": "empty", "slug": None, "acts": wage(probe, core),
        "hand": probe.hand_return([]),
        "note": "Closed empty on every family. Absence authority is the source closure. Line 16 is zero.",
    })
    for slug, kind, term in FAMILY:
        acts = wage(probe, core)
        grouped = probe.h.SALE_KINDS[kind]["grouped"]
        if grouped is None:
            acts = probe.h.strip(acts, probe.h.family_id(kind, term, None) + ".source-closure")
            note = f"Closed empty except the {slug} source closure is missing."
        else:
            acts = probe.h.strip(acts, grouped)
            note = (
                f"Closed empty except the grouped closure {grouped.removeprefix('tax.us.2025.')} "
                f"is missing. That closure is the absence authority for {slug}."
            )
        cases.append({
            "id": f"m_absence_{slug}", "kind": "absence", "slug": slug, "acts": acts, "hand": None,
            "note": note,
        })
    return cases


def build_late(probe: Any, core: Any) -> list[dict[str, Any]]:
    traces = []
    acts, sales = one_sale(probe, core, "covered-st", "gain", "yes", tag="g")
    added = probe.sale_on(acts, "covered", "st", "loss", statement_tag="g", proceeds=1000, basis=2000)
    added = refresh_exception1(probe, added, core)
    traces.append({
        "id": "late_gain_then_loss",
        "slug": "covered-st",
        "paper": "attest gain, close, answer yes, compute; add a loss on that statement, reclose, recompute",
        "steps": [
            {"id": "late_gain_then_loss_before", "kind": "hand", "acts": acts,
             "hand": probe.hand_return(sales), "counts": counts_for({"covered-st": 1})},
            {"id": "late_gain_then_loss_after", "kind": "same_statement", "acts": added, "hand": None,
             "counts": counts_for({"covered-st": 2})},
        ],
    })
    acts, _sales = one_sale(probe, core, "covered-st", "loss", "yes", tag="r")
    removed = probe.remove_sale(acts, "covered", "st", "r")
    removed = refresh_exception1(probe, removed, core)
    traces.append({
        "id": "late_loss_removed",
        "slug": "covered-st",
        "paper": "attest a loss, answer yes, compute; remove that sale, reclose, recompute",
        "steps": [
            {"id": "late_loss_removed_before", "kind": "yes_loss", "acts": acts, "hand": None,
             "counts": counts_for({"covered-st": 1})},
            {"id": "late_loss_removed_after", "kind": "empty", "acts": removed,
             "hand": probe.hand_return([]), "expect_checks": True},
        ],
    })
    acts, sales = one_sale(probe, core, "covered-st", "loss", "yes", tag="s")
    statement = probe.statements_of(acts)[0]
    later = copy.deepcopy(acts)
    fact_id = probe.h.fact_id_for(probe.BOX7, (("statement", statement), ("tax-year", probe.YEAR)))
    probe.h._add(later, "assertion", {"finding": probe.h._attested(
        "demo.b7.supersede.no.s", fact_id, "no")})
    later = probe.h.renumber(later)
    traces.append({
        "id": "late_yes_to_no",
        "slug": "covered-st",
        "paper": "attest a loss, answer yes, compute; supersede that answer with no; recompute",
        "steps": [
            {"id": "late_yes_to_no_before", "kind": "yes_loss", "acts": acts, "hand": None},
            {"id": "late_yes_to_no_after", "kind": "hand", "acts": later, "hand": probe.hand_return(sales),
             "counts": counts_for({"covered-st": 1}), "expect_verdict": "clear"},
        ],
    })
    acts, sales = one_sale(probe, core, "covered-st", "gain", "yes", tag="a")
    extra = probe.h.sale(acts, "covered", "st", tag="b", proceeds=2000, basis=1000)
    extra = refresh_exception1(probe, extra, core)
    traces.append({
        "id": "late_new_statement_unanswered",
        "slug": "covered-st",
        "paper": "attest statement A, answer yes, compute; add statement B with no box 7 answer; recompute",
        "steps": [
            {"id": "late_new_statement_before", "kind": "hand", "acts": acts,
             "hand": probe.hand_return(sales), "counts": counts_for({"covered-st": 1})},
            {"id": "late_new_statement_after", "kind": "unanswered", "acts": extra, "hand": None},
        ],
    })
    return traces


def build_reuse(probe: Any, core: Any) -> list[dict[str, Any]]:
    acts, sales = one_sale(probe, core, "covered-st", "loss", "no")
    no_loss = {"id": "reuse_box7_no", "kind": "hand", "slug": "covered-st", "acts": acts,
               "hand": probe.hand_return(sales), "counts": counts_for({"covered-st": 1}),
               "compare": "identical"}
    wage_acts = wage(probe, core)
    empty = {"id": "reuse_no_sale", "kind": "empty", "slug": None, "acts": wage_acts,
             "hand": probe.hand_return([]), "compare": "identical"}
    acts, sales = one_sale(probe, core, "covered-st", "gain", "yes")
    yes_gain = {"id": "reuse_yes_gain", "kind": "hand", "slug": "covered-st", "acts": acts,
                "hand": probe.hand_return(sales), "counts": counts_for({"covered-st": 1}),
                "compare": "line7_line15_counts"}
    acts = probe.h.opened()
    acts = probe.h.sale(acts, "covered", "st", tag="cf", proceeds=2000, basis=1000, basis_reported_to_irs="no")
    acts = probe.prepare(acts, core, {"covered"}, False)
    acts = probe.box7(acts, core, {"*": "no"})
    flag = {"id": "reuse_covered_flag", "kind": "covered_flag", "slug": "covered-st", "acts": acts,
            "hand": None, "compare": "sentence"}
    return [no_loss, empty, yes_gain, flag]


def build_surface(probe: Any, core: Any) -> list[dict[str, Any]]:
    specs = []
    mapping = (
        ("surface_published_gain", "covered-st", "gain", "yes", "hand"),
        ("surface_published_loss", "covered-st", "loss", "no", "hand"),
        ("surface_published_zero", "covered-st", "zero", "yes", "hand"),
        ("surface_blocked_yes_loss", "covered-st", "loss", "yes", "yes_loss"),
        ("surface_blocked_unanswered", "covered-st", "gain", None, "unanswered"),
    )
    for case_id, slug, sign, answer, kind in mapping:
        acts, sales = one_sale(probe, core, slug, sign, answer)
        specs.append({
            "id": case_id, "kind": kind, "slug": slug, "acts": acts,
            "hand": probe.hand_return(sales) if kind == "hand" else None,
            "counts": counts_for({slug: 1}) if kind == "hand" else None,
            "note": case_id,
        })
    specs.append({
        "id": "surface_no_box7_activity", "kind": "empty", "slug": None, "acts": wage(probe, core),
        "hand": probe.hand_return([]), "note": "Box 7 has no activity.",
    })
    acts = wage(probe, core)
    acts = probe.h.strip(acts, probe.h.family_id("covered", "st", None) + ".source-closure")
    specs.append({
        "id": "surface_blocked_count", "kind": "absence", "slug": "covered-st", "acts": acts, "hand": None,
        "note": "Line 16 blocked because the covered short-term count has no closure.",
    })
    return specs


def _one(item: tuple[str, str, list[dict[str, Any]]]) -> tuple[str, dict[str, Any]]:
    case_id, core_path, acts = item
    probe = load_probe()
    core = scratch_core(probe, Path(core_path))
    return case_id, execute(core, acts, "demo.b7.t0." + case_id)


def _pair(item: tuple[str, str, list[dict[str, Any]]]) -> tuple[str, dict[str, Any]]:
    case_id, core_path, acts = item
    probe = load_probe()
    v84 = scratch_core(probe, Path(core_path))
    v83 = published_v83(probe)
    return case_id, {
        "v84": execute(v84, acts, "demo.b7.t0." + case_id + ".v84"),
        "v83": execute(v83, acts, "demo.b7.t0." + case_id + ".v83"),
    }


def run_pool(core_path: str, cases: list[tuple[str, list[dict[str, Any]]]]) -> dict[str, dict[str, Any]]:
    workers = int(os.environ.get("BOX7_WORKERS") or min(4, os.cpu_count() or 2))
    found: dict[str, dict[str, Any]] = {}
    items = [(case_id, core_path, acts) for case_id, acts in cases]
    with ProcessPoolExecutor(max_workers=workers) as pool:
        done = 0
        for case_id, result in pool.map(_one, items):
            found[case_id] = result
            done += 1
            line = (result.get("lines") or {}).get("schedule-d.line-16")
            print(f"{done}/{len(items)} {case_id} {result.get('outcome')} {line}", flush=True)
    return found


def attach(case: dict[str, Any], result: dict[str, Any], probe: Any, question: str) -> dict[str, Any]:
    failures = contract_failures(case, result, question)
    return {
        "id": case["id"],
        "kind": case["kind"],
        "slug": case.get("slug"),
        "note": case.get("note"),
        "hand": case.get("hand"),
        "snapshot": snapshot(probe, case["acts"], case.get("slug")),
        "result": result,
        "failures": failures,
        "passed": not failures,
    }


def reuse_failures(case: dict[str, Any], paired: dict[str, Any], question: str) -> list[str]:
    v84 = paired["v84"]
    v83 = paired["v83"]
    found = contract_failures(case, v84, question)
    mode = case["compare"]
    if v83.get("outcome") != "success":
        found.append(f"v83 {v83.get('outcome')} {v83.get('error') or v83.get('message')}")
        return found
    if mode == "identical":
        found.extend(f"v83 {item}" for item in hand_failures(v83, case["hand"]))
        if v84.get("lines") != v83.get("lines"):
            found.append("lines differ from v83")
        if (v84.get("line16_rows") or [{}])[0].get("disposition") != (v83.get("line16_rows") or [{}])[0].get("disposition"):
            found.append("line 16 disposition differs from v83")
        if (v84.get("lines") or {}).get("schedule-d.line-16") != (v83.get("lines") or {}).get("schedule-d.line-16"):
            found.append("line 16 value differs from v83")
    if mode == "line7_line15_counts":
        for line in ("schedule-d.line-7", "schedule-d.line-15"):
            if (v84.get("lines") or {}).get(line) != (v83.get("lines") or {}).get(line):
                found.append(f"{line} differs from v83")
        for slug, _kind, _term in FAMILY:
            if pub_values(v84, f"f1099b.{slug}-count") != pub_values(v83, f"f1099b.{slug}-count"):
                found.append(f"{slug} count differs from v83")
        if (v83.get("lines") or {}).get("schedule-d.line-16") == (v84.get("lines") or {}).get("schedule-d.line-16"):
            found.append("v83 line 16 matched v84 on a box 7 yes gain")
    if mode == "sentence":
        sentence = "Record this sale as a noncovered sale. The broker did not report its basis to the IRS."
        if sentence not in json.dumps(v83.get("reasons") or {}):
            found.append("v83 covered-flag sentence absent")
    return found


def late_failures(trace: dict[str, Any], steps: list[dict[str, Any]]) -> list[str]:
    found: list[str] = []
    before, after = steps
    if not before["passed"] or not after["passed"]:
        found.append("a step failed its own contract")
    name = trace["id"]
    before_ids = [row["finding_id"] for row in (before["result"].get("publications") or [])
                  if row["symbol"] == "schedule-d.line-16"]
    after_ids = [row["finding_id"] for row in (after["result"].get("publications") or [])
                 if row["symbol"] == "schedule-d.line-16"]
    if name == "late_gain_then_loss":
        if not before_ids or before_ids[0] in after_ids:
            found.append(f"prior line 16 finding stayed current {before_ids} -> {after_ids}")
        before_closures = {row["id"] for row in before["snapshot"]["closures"]}
        after_closures = {row["id"] for row in after["snapshot"]["closures"]}
        if not before_closures or before_closures & after_closures:
            found.append("prior closure stayed on the act list")
    if name == "late_loss_removed":
        if pub_values(after["result"], check_symbol("covered-st")) != [0]:
            found.append(f"check after removal {pub_values(after['result'], check_symbol('covered-st'))}")
        if pub_values(after["result"], verdict_symbol("covered-st")):
            found.append("disallowed verdict still published after removal")
    if name == "late_yes_to_no":
        values = [row["value"] for row in after["snapshot"]["box7"]]
        if values != ["yes", "no"]:
            found.append(f"box 7 findings {values}")
        if pub_values(after["result"], verdict_symbol("covered-st")) != ["clear"]:
            found.append(f"verdict after no {pub_values(after['result'], verdict_symbol('covered-st'))}")
    if name == "late_new_statement_unanswered":
        if not before_ids or before_ids[0] in after_ids:
            found.append(f"prior line 16 finding stayed current {before_ids} -> {after_ids}")
    return found


def package_identity(v84: Any, v83: Any) -> dict[str, Any]:
    def versions(core: Any) -> dict[str, list[str]]:
        package = json.loads(core.package_path.read_text(encoding="utf-8"))
        found: dict[str, list[str]] = {}
        for member in package["members"]:
            mid = str(member["id"])
            if (
                mid.endswith("rule.schedule-d-line7")
                or mid.endswith("rule.schedule-d-line15")
                or mid.endswith("rule.schedule-d-line16")
                or "schedule-d.line-16" in mid
                or (mid.endswith("-count") and "f1099b" in mid)
                or mid.endswith("f8949.no1099b-st-count")
                or mid.endswith("f8949.no1099b-lt-count")
            ):
                found.setdefault(mid.removeprefix("tax.us.2025."), []).append(member["version"])
        return found

    left, right = versions(v83), versions(v84)
    return {
        "same_ids": sorted(set(left) & set(right)),
        "version_diff": [
            {"id": key, "v83": left.get(key), "v84": right.get(key)}
            for key in sorted(set(left) | set(right)) if left.get(key) != right.get(key)
        ],
    }


def line16_bindings(core: Any) -> list[dict[str, Any]]:
    package = json.loads(core.package_path.read_text(encoding="utf-8"))
    members = {(member["id"], member["version"]): member for member in package["members"]}
    symbol = "tax.us.2025.schedule-d.line-16"
    found = []
    for path in sorted(core.content.glob("*.json")):
        try:
            body = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if not isinstance(body, dict) or (body.get("id"), body.get("version")) not in members:
            continue
        text = json.dumps(body)
        if symbol not in text:
            continue
        requires = body.get("requires") if isinstance(body.get("requires"), list) else []
        found.append({
            "role": body.get("role") or members[(body["id"], body["version"])].get("role"),
            "id": str(body["id"]).removeprefix("tax.us.2025."),
            "version": body.get("version"),
            "direct_require": symbol in requires,
            "binds_symbol": str(body.get("binds_symbol") or "").removeprefix("tax.us.2025.") or None,
        })
    return found


def write_output(name: str, payload: dict[str, Any]) -> None:
    probe = load_probe()
    text = probe.h.scrub(json.dumps(payload, indent=2) + "\n")
    for needle in ("/Users/", "/private/", "/tmp/", "/var/"):
        if needle in text:
            raise SystemExit(f"{name} contains {needle}")
    (HERE / name).write_text(text, encoding="utf-8")


def main() -> None:
    if len(sys.argv) != 3:
        raise SystemExit(
            "usage: track0.py <scratch-core.json> <authority|matrix|late|reuse|surface|smaller>")
    scope = sys.argv[2]
    probe = load_probe()
    core = scratch_core(probe, Path(sys.argv[1]).resolve())
    question = question_text()
    only = {item for item in os.environ.get("BOX7_TRACK0_ONLY", "").split(",") if item}

    if scope == "late":
        traces = build_late(probe, core)
        items = [(step["id"], step["acts"]) for trace in traces for step in trace["steps"]]
        if only:
            items = [item for item in items if item[0] in only]
        found = run_pool(str(Path(sys.argv[1]).resolve()), items)
        saved = []
        for trace in traces:
            steps = []
            for step in trace["steps"]:
                if step["id"] not in found:
                    continue
                steps.append(attach({**step, "slug": trace["slug"], "note": trace["paper"]}, found[step["id"]], probe, question))
            extra = late_failures(trace, steps) if len(steps) == 2 else ["missing step"]
            saved.append({
                "id": trace["id"], "paper": trace["paper"], "steps": steps, "trace_failures": extra,
                "passed": not extra and all(step["passed"] for step in steps),
            })
        payload = {"scope": scope, "core": "v84", "traces": saved,
                   "passed": [row["id"] for row in saved if row["passed"]],
                   "failed": [row["id"] for row in saved if not row["passed"]]}
        write_output("track0-late.json", payload)
        print(json.dumps({"passed": payload["passed"], "failed": payload["failed"]}, indent=2))
        return

    if scope == "reuse":
        v83 = published_v83(probe)
        cases = build_reuse(probe, core)
        if only:
            cases = [case for case in cases if case["id"] in only]
        workers = int(os.environ.get("BOX7_WORKERS") or min(4, os.cpu_count() or 2))
        items = [(case["id"], str(Path(sys.argv[1]).resolve()), case["acts"]) for case in cases]
        found_pairs: dict[str, dict[str, Any]] = {}
        with ProcessPoolExecutor(max_workers=workers) as pool:
            for case_id, paired in pool.map(_pair, items):
                found_pairs[case_id] = paired
                print(f"{case_id} v84 {paired['v84'].get('outcome')} v83 {paired['v83'].get('outcome')}", flush=True)
        saved = []
        for case in cases:
            failures = reuse_failures(case, found_pairs[case["id"]], question)
            saved.append({
                "id": case["id"], "compare": case["compare"], "hand": case.get("hand"),
                "snapshot": snapshot(probe, case["acts"], case.get("slug")),
                "v84": found_pairs[case["id"]]["v84"], "v83": found_pairs[case["id"]]["v83"],
                "failures": failures, "passed": not failures,
            })
        identity = package_identity(core, v83)
        payload = {"scope": scope, "core": "v84-and-v83", "package_identity": identity, "cases": saved,
                   "passed": [row["id"] for row in saved if row["passed"]],
                   "failed": [row["id"] for row in saved if not row["passed"]]}
        write_output("track0-reuse.json", payload)
        print(json.dumps({"passed": payload["passed"], "failed": payload["failed"],
                          "version_diff": identity["version_diff"]}, indent=2))
        return

    if scope == "smaller":
        wanted = {
            "alc_closed_empty", "alc_covered-st_gain", "alc_covered-st_loss", "alc_covered_st_unanswered",
        }
        cases = [case for case in build_authority(probe, core) if case["id"] in wanted]
        found = run_pool(str(Path(sys.argv[1]).resolve()), [(case["id"], case["acts"]) for case in cases])
        saved = [attach(case, found[case["id"]], probe, question) for case in cases]
        summary_path = Path(sys.argv[1]).resolve().parent / "build-summary.json"
        build = json.loads(summary_path.read_text(encoding="utf-8")) if summary_path.is_file() else None
        payload = {
            "scope": scope,
            "shape": "verdicts-only",
            "new_rules": None if build is None else build.get("new_rules"),
            "adopted": False,
            "why": (
                "Eight verdict rules and no family check. Line 16 requires the eight verdict symbols. "
                "An empty family publishes no subject verdict, so a closed-empty return and a one-family "
                "return both leave line 16 unpublished. The 16-rule shape stays the default."
            ),
            "build": build,
            "core": "v84-smaller",
            "cases": saved,
            "passed": [row["id"] for row in saved if row["passed"]],
            "failed": [row["id"] for row in saved if not row["passed"]],
        }
        write_output("track0-smaller.json", payload)
        print(json.dumps({"passed": payload["passed"], "failed": payload["failed"],
                          "new_rules": payload["new_rules"], "adopted": False}, indent=2))
        return

    builders = {"authority": build_authority, "matrix": build_matrix, "surface": build_surface}
    if scope not in builders:
        raise SystemExit(f"unknown scope {scope}")
    cases = builders[scope](probe, core)
    if only:
        cases = [case for case in cases if case["id"] in only]
    found = run_pool(str(Path(sys.argv[1]).resolve()), [(case["id"], case["acts"]) for case in cases])
    saved = [attach(case, found[case["id"]], probe, question) for case in cases]
    payload = {"scope": scope, "core": "v84", "question": question, "cases": saved,
               "passed": [row["id"] for row in saved if row["passed"]],
               "failed": [row["id"] for row in saved if not row["passed"]]}
    if scope == "surface":
        payload["bindings"] = line16_bindings(core)
        payload["unbound_schedule_d_lines"] = [
            f"schedule-d.line-{number}" for number in (17, 18, 19, 20, 22)
        ]
    write_output(f"track0-{scope}.json", payload)
    print(json.dumps({"passed": len(payload["passed"]), "failed": payload["failed"]}, indent=2))


if __name__ == "__main__":
    if os.environ.get("BOX7_TRACK0_WORKER") != "1":
        os.environ["BOX7_TRACK0_WORKER"] = "1"
        main()
