"""Track 0 runs for Form 1099-B box 4 withholding without a sale.

Evidence for docs/phases/engine-breadth/milestones/f1099b-box4-only.md.
Charter: docs/reviews/f1099b-box4-only/charter-track0.md.

    python3 track0.py <scratch-core.json> <authority|matrix|late|reuse|neighbour|surface>

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
from collections import Counter
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

PROBE_NAME = "f1099b_b4only_track0_probe"
TEST_NAME = "f1099b_b4only_track0_v83_test"
EXPECTED = REPO / "tests/fixtures/f1099b_backup_withholding_v83/expected.json"
TEST = REPO / "tests/test_f1099b_backup_withholding_v83.py"
P = "tax.us.2025."
PRESENT = P + "f1099b.no-sale-box4-present"
AMOUNT = P + "f1099b.no-sale-box4-withholding"
BOX4_Q_PATH = REPO / "packages/content/tax/2025/input-question.f1099b-box4.v1.json"
ORPHAN = "demo.sfa.orphan.statement"
SALE = "demo.sfa.sale1.statement"
CONSUMER_FIELDS = (
    "form1040.line-25a", "form1040.line-25b", "form1040.line-25c", "form1040.line-25d",
    "form1040.line-33", "form1040.line-34", "form1040.line-37",
    "form1040.line-7a", "form1040.line-15", "form1040.line-16", "form1040.line-24",
    "schedule-d.line-16",
)
SUBTOTALS = (
    "interest.b4-withholding-subtotal",
    "dividends.b4-withholding-subtotal",
    "ira.box4-withholding-subtotal",
    "unemployment.b4-withholding-subtotal",
    "ssa1099.b6-withholding-subtotal",
    "f1099b.b4-withholding-subtotal",
)
SCOPE_KEY = {"tax-year": "2025", "subject": "demo.primary"}
BLOCKED_EXPLAIN = (
    "Form 1040 line 25b is blocked because an input it needs is missing or not yet closed. "
    "It is also blocked while a recorded sale's statement has no box 4 amount, and while "
    "it is unanswered whether a Form 1099-B shows box 4 withholding and no closed sale, "
    "other than a statement whose box 4 was entered with its sales."
)
PRESENT_EXCLUDE = "Do not count a statement whose box 4 you already entered with its sales."
AMOUNT_EXCLUDE = "Do not include a statement whose box 4 you already entered with its sales."


def load_probe() -> Any:
    module = sys.modules.get(PROBE_NAME)
    if module is None:
        spec = importlib.util.spec_from_file_location(PROBE_NAME, HERE / "probe.py")
        assert spec is not None and spec.loader is not None
        module = importlib.util.module_from_spec(spec)
        sys.modules[PROBE_NAME] = module
        spec.loader.exec_module(module)
    return module


def load_test() -> Any:
    module = sys.modules.get(TEST_NAME)
    if module is None:
        spec = importlib.util.spec_from_file_location(TEST_NAME, TEST)
        assert spec is not None and spec.loader is not None
        module = importlib.util.module_from_spec(spec)
        sys.modules[TEST_NAME] = module
        spec.loader.exec_module(module)
    return module


def scratch_core(probe: Any, core_path: Path) -> Any:
    body = json.loads(core_path.read_text(encoding="utf-8"))
    return probe.h.Core(
        body["version"], body["registry"], body["release_version"],
        content=Path(body["content"]), releases=Path(body["releases"]),
        loader_from=body.get("loader_from"),
    )


def published_v84(probe: Any) -> Any:
    return probe.h.Core("v84", "v82", "v82")


def question_texts(core: Any) -> tuple[str, str, str]:
    present = json.loads((core.content / "input-question.f1099b-no-sale-box4-present.v1.json").read_text(encoding="utf-8"))
    amount = json.loads((core.content / "input-question.f1099b-no-sale-box4-amount.v1.json").read_text(encoding="utf-8"))
    box4 = json.loads(BOX4_Q_PATH.read_text(encoding="utf-8"))
    return str(present["question"]), str(amount["question"]), str(box4["question"])


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


def _watched_row(row: dict[str, Any]) -> dict[str, Any]:
    artifact = str(row.get("artifact_id") or "")
    raw = str(row.get("symbol")).removeprefix(P) if row.get("symbol") else ""
    base, _, subject = raw.partition("|")
    return {
        "artifact": artifact.removeprefix(P),
        "disposition": row.get("disposition"),
        "code": row.get("code"),
        "missing": [str(item).removeprefix(P) for item in (row.get("missing") or [])],
        "symbol": base or None,
        "subject": subject or None,
        "finding_id": row.get("finding_id"),
    }


def _interesting(name: str) -> bool:
    base = name.split("|", 1)[0]
    tokens = (
        "line25", "form1040.line", "form1040-line", "payments.line25",
        "no-sale-box4", "statement-box4", "b4-withholding", "box4-withholding",
        "box7-loss-check", "box7-verdict", "selected-preferential",
    )
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
                        raw = symbol.removeprefix(P)
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
    line25b_field: dict[str, Any] | None = None
    for section in model.get("sections") or []:
        field = section.get("field") or {}
        short = str(field.get("id") or "").removeprefix(P)
        resolved = section.get("resolved") or {}
        sentences = [str(reason.get("sentence") or "") for reason in (resolved.get("reasons") or [])
                     if isinstance(reason, dict) and reason.get("sentence")]
        for sentence in sentences:
            if sentence and sentence not in questions and (
                    sentence.endswith("?") or "?" in sentence or sentence.startswith("Enter ")):
                questions.append(sentence)
        if short in probe.LINES or short in CONSUMER_FIELDS:
            value = resolved.get("value")
            disposition = str(resolved.get("disposition"))
            if value is None or "blocked" in disposition:
                lines[short] = disposition
            else:
                lines[short] = num(value)
            if "blocked" in disposition:
                reasons[short] = [probe.h.scrub(sentence)[:400] for sentence in sentences]
        if short in consumers:
            blocked = ((field.get("dispositions") or {}).get("blocked") or {})
            consumers[short] = {
                "present": True,
                "binds_symbol": str(field.get("binds_symbol") or "").removeprefix(P),
                "field_version": field.get("version"),
                "disposition": resolved.get("disposition"),
                "value": num(resolved.get("value")) if resolved.get("value") is not None else None,
                "reasons": sentences,
                "blocked_explain": blocked.get("explain"),
            }
        if short == "form1040.line-25b":
            blocked = ((field.get("dispositions") or {}).get("blocked") or {})
            line25b_field = {
                "version": field.get("version"),
                "description": field.get("description"),
                "blocked_explain": blocked.get("explain"),
                "published_explain": ((field.get("dispositions") or {}).get("published_value") or {}).get("explain"),
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
        "questions": [probe.h.scrub(question)[:400] for question in questions],
        "publications": publications,
        "rows": rows,
        "consumers": consumers,
        "line25b_field": line25b_field,
        "line25b_rows": [row for row in rows if row["artifact"] == "rule.form1040-line25b"],
    }


def pub_values(result: dict[str, Any], symbol: str) -> list[Any]:
    return [row["value"] for row in result.get("publications") or [] if row["symbol"] == symbol]


def row_for(result: dict[str, Any], artifact: str) -> list[dict[str, Any]]:
    return [row for row in result.get("rows") or [] if row["artifact"] == artifact]


def hand_failures(result: dict[str, Any], hand: dict[str, Any]) -> list[str]:
    found = []
    for line, expected in hand.items():
        if line == "disposition":
            continue
        got = (result.get("lines") or {}).get(line)
        if got != expected:
            found.append(f"{line}: hand {expected} got {got}")
    return found


def _blocked(result: dict[str, Any], line: str = "form1040.line-25b") -> bool:
    value = (result.get("lines") or {}).get(line)
    return isinstance(value, str) and "block" in value


def snapshot(probe: Any, acts: list[dict[str, Any]]) -> dict[str, Any]:
    present = []
    amount = []
    box4 = []
    for act in acts:
        if act.get("kind") != "assertion":
            continue
        finding = (act.get("payload") or {}).get("finding") or {}
        fact_id = str(finding.get("fact_id") or "")
        row = {"id": finding.get("id"), "fact_id": fact_id, "value": finding.get("value")}
        if "no-sale-box4-present|" in fact_id:
            present.append(row)
        elif "no-sale-box4-withholding|" in fact_id:
            amount.append(row)
        elif "statement-box4-withholding|" in fact_id:
            box4.append(row)
    return {"present": present, "amount": amount, "box4": box4}


def refresh(probe: Any, core: Any, acts: list[dict[str, Any]], *, box4_sales: bool = True) -> list[dict[str, Any]]:
    fresh = probe.h.honest_exception1(acts)
    if fresh.get("exc1_only_2a") is None and fresh.get("exc1_no_losses") is None:
        fresh = {"exc1_only_2a": "yes", "exc1_no_losses": "yes"}
    acts = probe.h.answer(acts, core.content, **{key: value for key, value in fresh.items() if value is not None})
    if box4_sales:
        acts = probe.box4_zero_sales(acts, core)
    return acts


def wage(probe: Any, core: Any, *, kinds: set[str] | None = None, tag: str = "sale1",
         proceeds: float = 5000, basis: float = 4000, loss: bool = False,
         box4_sales: bool = True) -> list[dict[str, Any]]:
    acts = probe.h.opened()
    kinds = kinds or set()
    if kinds:
        kind = next(iter(kinds))
        acts = probe.h.sale(acts, kind, "st", tag=tag, proceeds=proceeds, basis=basis)
    answers = probe.h.honest(kinds, loss=loss, new_questions=False)
    answers.update(probe.h.honest_exception1(acts))
    acts = probe.h.answer(acts, core.content, **{key: value for key, value in answers.items() if value is not None})
    if box4_sales:
        acts = probe.box4_zero_sales(acts, core)
    return acts


def with_present(probe: Any, core: Any, acts: list[dict[str, Any]], present: str | None,
                 amount: float | None, tag: str = "t0") -> list[dict[str, Any]]:
    if present is not None:
        acts = probe.say_return(acts, core, probe.PRESENT, present, f"{tag}.present")
    if amount is not None:
        acts = probe.say_return(acts, core, probe.AMOUNT, amount, f"{tag}.amount")
    return acts


def with_orphan(probe: Any, acts: list[dict[str, Any]], tag: str = "orphan") -> list[dict[str, Any]]:
    return probe.introduce_statement(acts, tag)


def set_stmt(probe: Any, core: Any, acts: list[dict[str, Any]], statement: str,
             box4: float | None, box7: str | None = "no") -> list[dict[str, Any]]:
    if box4 is not None:
        acts = probe.say_statement(acts, core, probe.BOX4, statement, box4)
    if box7 is not None:
        acts = probe.say_statement(acts, core, probe.BOX7, statement, box7)
    return acts


def supersede(probe: Any, acts: list[dict[str, Any]], fact_type: str, value: object, tag: str) -> list[dict[str, Any]]:
    out = copy.deepcopy(acts)
    fact_id = probe.h.fact_id_for(fact_type, (("tax-year", probe.YEAR),))
    probe.h._add(out, "assertion", {"finding": probe.h._attested(f"demo.b4only.t0.{tag}", fact_id, value)})
    return probe.h.renumber(out)


def spec(case_id: str, kind: str, acts: list[dict[str, Any]], *, hand: dict[str, Any] | None,
         note: str, expect_25b: Any = None, st_gain: float = 0) -> dict[str, Any]:
    return {
        "id": case_id, "kind": kind, "acts": acts, "hand": hand, "note": note,
        "expect_25b": expect_25b, "st_gain": st_gain,
    }


def build_authority(probe: Any, core: Any) -> list[dict[str, Any]]:
    cases = []
    empty = with_present(probe, core, wage(probe, core), None, None)
    cases.append(spec(
        "alc_present_unanswered", "blocked_present", empty,
        hand=probe.hand_return(blocked=True),
        note="No Form 1099-B. Present unanswered. Line 25b blocks and asks the yes/no.",
    ))
    cases.append(spec(
        "alc_present_no", "published", with_present(probe, core, wage(probe, core), "no", None),
        hand=probe.hand_return(line25b=0), expect_25b=0,
        note="Present no on a return with no Form 1099-B. Line 25b is 0. Nothing more is asked.",
    ))
    cases.append(spec(
        "alc_present_yes_amount", "published",
        with_present(probe, core, wage(probe, core), "yes", 150),
        hand=probe.hand_return(line25b=150), expect_25b=150,
        note="Present yes and return-level $150. That amount is the withholding. Scope is the return.",
    ))
    cases.append(spec(
        "alc_present_yes_amount_unanswered", "blocked_amount",
        with_present(probe, core, wage(probe, core), "yes", None),
        hand=probe.hand_return(blocked=True),
        note="Present yes and the return-level amount unanswered. Line 25b names the amount.",
    ))
    sale = set_stmt(probe, core, wage(probe, core, kinds={"covered"}), SALE, 200)
    cases.append(spec(
        "alc_stmt_with_sale", "published", with_present(probe, core, sale, "no", None),
        hand=probe.hand_return(st_gain=1000, line25b=200), expect_25b=200, st_gain=1000,
        note="Per-statement box 4 $200 on a statement with a sale. Present is no. One copy.",
    ))
    nosale = set_stmt(probe, core, with_orphan(probe, wage(probe, core)), ORPHAN, 150)
    cases.append(spec(
        "alc_stmt_without_sale", "published", with_present(probe, core, nosale, "yes", 0),
        hand=probe.hand_return(line25b=150), expect_25b=150,
        note="Per-statement $150 on a statement with no sale. Present yes with return-level 0. Decision 6.",
    ))
    mixed = set_stmt(probe, core, wage(probe, core, kinds={"covered"}), SALE, 200)
    mixed = with_orphan(probe, mixed)
    mixed = with_present(probe, core, mixed, "yes", 150)
    cases.append(spec(
        "alc_stmt_identity", "published", mixed,
        hand=probe.hand_return(st_gain=1000, line25b=350), expect_25b=350, st_gain=1000,
        note="Sale statement $200 is that statement's amount. Return-level $150 is the no-sale copy. 350.",
    ))
    double = set_stmt(probe, core, with_orphan(probe, wage(probe, core)), ORPHAN, 150)
    double = with_present(probe, core, double, "yes", 150)
    cases.append(spec(
        "alc_double_count", "double", double,
        hand=probe.hand_return(line25b=300), expect_25b=300,
        note="Dishonest: per-statement $150 and return-level $150. Line 25b is 300. Named, not a bar failure.",
    ))
    return cases


def build_matrix(probe: Any, core: Any) -> list[dict[str, Any]]:
    cases = []

    def add(case_id: str, kind: str, acts: list[dict[str, Any]], *, line25b: float | None,
            st_gain: float = 0, note: str) -> None:
        blocked = kind.startswith("blocked")
        hand = probe.hand_return(st_gain=st_gain, line25b=0 if line25b is None else line25b, blocked=blocked)
        cases.append(spec(case_id, kind, acts, hand=hand, note=note, expect_25b=line25b, st_gain=st_gain))

    add("m_none_unanswered", "blocked_present", with_present(probe, core, wage(probe, core), None, None),
        line25b=None, note="No Form 1099-B, present unanswered.")
    add("m_none_no", "published", with_present(probe, core, wage(probe, core), "no", None),
        line25b=0, note="No Form 1099-B, present no.")
    add("m_none_yes_amount", "published", with_present(probe, core, wage(probe, core), "yes", 150),
        line25b=150, note="No Form 1099-B, present yes with amount 150.")
    add("m_none_yes_amount_unanswered", "blocked_amount",
        with_present(probe, core, wage(probe, core), "yes", None),
        line25b=None, note="No Form 1099-B, present yes, amount unanswered.")

    sale200 = set_stmt(probe, core, wage(probe, core, kinds={"covered"}), SALE, 200)
    sale0 = set_stmt(probe, core, wage(probe, core, kinds={"covered"}), SALE, 0)
    add("m_sale_unanswered_stmt200", "blocked_present", with_present(probe, core, sale200, None, None),
        line25b=None, st_gain=1000, note="Sale statements only, box 4 200, present unanswered.")
    add("m_sale_no_stmt200", "published", with_present(probe, core, sale200, "no", None),
        line25b=200, st_gain=1000, note="Sale statements only, box 4 200, present no. Equals v84.")
    add("m_sale_yes_amount_stmt200", "published", with_present(probe, core, sale200, "yes", 150),
        line25b=350, st_gain=1000, note="Sale 200 plus return-level 150. Additional no-sale withholding.")
    add("m_sale_yes_amount_unanswered_stmt200", "blocked_amount",
        with_present(probe, core, sale200, "yes", None),
        line25b=None, st_gain=1000, note="Sale 200, present yes, amount unanswered.")
    add("m_sale_no_stmt0", "published", with_present(probe, core, sale0, "no", None),
        line25b=0, st_gain=1000, note="Sale statements only, per-statement box 4 zero, present no.")
    add("m_sale_unanswered_stmt0", "blocked_present", with_present(probe, core, sale0, None, None),
        line25b=None, st_gain=1000, note="Sale statements only, per-statement zero, present unanswered.")

    nosale = with_orphan(probe, wage(probe, core))
    nosale150 = set_stmt(probe, core, with_orphan(probe, wage(probe, core)), ORPHAN, 150)
    nosale0 = set_stmt(probe, core, with_orphan(probe, wage(probe, core)), ORPHAN, 0)
    add("m_nosale_unanswered", "blocked_present", with_present(probe, core, nosale, None, None),
        line25b=None, note="No-sale statement only, present unanswered.")
    add("m_nosale_no", "published", with_present(probe, core, nosale, "no", None),
        line25b=0, note="No-sale statement only, present no. Nothing more is asked.")
    add("m_nosale_yes_amount", "published", with_present(probe, core, nosale, "yes", 150),
        line25b=150, note="No-sale statement only, return-level 150, no per-statement amount.")
    add("m_nosale_yes_amount_unanswered", "blocked_amount",
        with_present(probe, core, nosale, "yes", None),
        line25b=None, note="No-sale statement only, present yes, amount unanswered.")
    add("m_nosale_no_stmt150", "published", with_present(probe, core, nosale150, "no", None),
        line25b=150, note="No-sale per-statement 150, present no. Decision 6 still counts it.")
    add("m_nosale_yes_amount0_stmt150", "published", with_present(probe, core, nosale150, "yes", 0),
        line25b=150, note="Honest Decision 6: per-statement 150, return-level 0.")
    add("m_nosale_no_stmt0", "published", with_present(probe, core, nosale0, "no", None),
        line25b=0, note="No-sale per-statement zero, present no.")
    add("m_nosale_yes_amount_stmt0", "published", with_present(probe, core, nosale0, "yes", 150),
        line25b=150, note="No-sale per-statement zero, return-level 150.")

    both = with_orphan(probe, set_stmt(probe, core, wage(probe, core, kinds={"covered"}), SALE, 200))
    both150 = set_stmt(probe, core, with_orphan(probe, set_stmt(
        probe, core, wage(probe, core, kinds={"covered"}), SALE, 200)), ORPHAN, 150)
    both0 = set_stmt(probe, core, with_orphan(probe, set_stmt(
        probe, core, wage(probe, core, kinds={"covered"}), SALE, 200)), ORPHAN, 0)
    add("m_both_unanswered_sale200", "blocked_present", with_present(probe, core, both, None, None),
        line25b=None, st_gain=1000, note="Sale and no-sale, present unanswered.")
    add("m_both_no_sale200", "published", with_present(probe, core, both, "no", None),
        line25b=200, st_gain=1000, note="Sale 200 and a no-sale statement, present no.")
    add("m_both_yes_amount_sale200", "published", with_present(probe, core, both, "yes", 150),
        line25b=350, st_gain=1000, note="Sale 200 plus return-level 150.")
    add("m_both_yes_amount_unanswered_sale200", "blocked_amount",
        with_present(probe, core, both, "yes", None),
        line25b=None, st_gain=1000, note="Sale and no-sale, present yes, amount unanswered.")
    add("m_both_no_sale200_stmt150", "published", with_present(probe, core, both150, "no", None),
        line25b=350, st_gain=1000, note="Sale 200 and no-sale per-statement 150, present no. Decision 6.")
    add("m_both_no_sale200_stmt0", "published", with_present(probe, core, both0, "no", None),
        line25b=200, st_gain=1000, note="Sale 200 and no-sale per-statement zero, present no.")
    add("m_both_yes_amount0_sale200_stmt150", "published", with_present(probe, core, both150, "yes", 0),
        line25b=350, st_gain=1000, note="Honest both: sale 200, no-sale 150, return-level 0.")
    return cases


def build_late(probe: Any, core: Any) -> list[dict[str, Any]]:
    traces = []
    before = with_present(probe, core, with_orphan(probe, wage(probe, core)), "yes", 150, tag="late1")
    after = probe.sale_on(before, "covered", "st", "later", statement_tag="orphan",
                          proceeds=5000, basis=4000)
    after = refresh(probe, core, after)
    after = set_stmt(probe, core, after, ORPHAN, 150)
    after = supersede(probe, after, probe.PRESENT, "no", "late1.present.no")
    traces.append({
        "id": "late_yes_then_sale_then_no",
        "paper": (
            "attest a no-sale statement, answer present yes and return-level 150, compute; "
            "add a sale to that statement, enter its per-statement box 4, supersede present to no, recompute"
        ),
        "steps": [
            {"id": "late_yes_then_sale_then_no_before", "kind": "published", "acts": before,
             "hand": probe.hand_return(line25b=150), "expect_25b": 150},
            {"id": "late_yes_then_sale_then_no_after", "kind": "published", "acts": after,
             "hand": probe.hand_return(st_gain=1000, line25b=150), "expect_25b": 150, "st_gain": 1000},
        ],
    })
    before = with_present(
        probe, core, set_stmt(probe, core, wage(probe, core, kinds={"covered"}), SALE, 200), "no", None, tag="late2")
    after = probe.remove_sale(before, "covered", "st", "sale1")
    after = refresh(probe, core, after, box4_sales=False)
    traces.append({
        "id": "late_sale_removed",
        "paper": "attest a sale with box 4 200, present no, compute; remove the sale, reclose, recompute",
        "steps": [
            {"id": "late_sale_removed_before", "kind": "published", "acts": before,
             "hand": probe.hand_return(st_gain=1000, line25b=200), "expect_25b": 200, "st_gain": 1000},
            {"id": "late_sale_removed_after", "kind": "published", "acts": after,
             "hand": probe.hand_return(line25b=200), "expect_25b": 200},
        ],
    })
    before = with_present(probe, core, wage(probe, core), "yes", 150, tag="late3")
    after = supersede(probe, before, probe.AMOUNT, 80, "late3.amount.80")
    traces.append({
        "id": "late_amount_corrected",
        "paper": "attest present yes and amount 150, compute; supersede the amount with 80, recompute",
        "steps": [
            {"id": "late_amount_corrected_before", "kind": "published", "acts": before,
             "hand": probe.hand_return(line25b=150), "expect_25b": 150},
            {"id": "late_amount_corrected_after", "kind": "published", "acts": after,
             "hand": probe.hand_return(line25b=80), "expect_25b": 80},
        ],
    })
    before = with_present(probe, core, wage(probe, core), "yes", 150, tag="late4")
    after = supersede(probe, before, probe.PRESENT, "no", "late4.present.no")
    traces.append({
        "id": "late_yes_to_no",
        "paper": "attest present yes and amount 150, compute; supersede present to no, recompute",
        "steps": [
            {"id": "late_yes_to_no_before", "kind": "published", "acts": before,
             "hand": probe.hand_return(line25b=150), "expect_25b": 150},
            {"id": "late_yes_to_no_after", "kind": "published", "acts": after,
             "hand": probe.hand_return(line25b=0), "expect_25b": 0},
        ],
    })
    return traces


def get_head(probe: Any, acts: list[dict[str, Any]], family_id: str) -> str:
    for act in acts:
        payload = act.get("payload") or {}
        if act.get("kind") == "horizon-genesis" and (payload.get("family") or {}).get("id") == family_id:
            return str(payload.get("horizon_id"))
    raise AssertionError(f"no horizon genesis for {family_id}")


def ensure_genesis(probe: Any, acts: list[dict[str, Any]], family_id: str, version: str = "v1") -> str:
    for act in acts:
        payload = act.get("payload") or {}
        if act.get("kind") == "horizon-genesis" and (payload.get("family") or {}).get("id") == family_id:
            return str(payload.get("horizon_id"))
    head_id = f"demo.reuse.{family_id.split('.')[-1]}.h0"
    probe.h._add(acts, "horizon-genesis", {
        "family": {"id": family_id, "version": version},
        "scope": dict(SCOPE_KEY),
        "horizon_id": head_id,
    })
    return head_id


def make_transition(
    probe: Any, acts: list[dict[str, Any]], family: tuple[str, str], predecessor: str,
    successor: str, finding_id: str, fact_type: str, keys: tuple[tuple[str, str], ...], value: Any,
) -> str:
    fact_id = probe.h.fact_id_for(fact_type, keys + (("tax-year", probe.YEAR),))
    probe.h._add(acts, "member-transition", {
        "family": {"id": family[0], "version": family[1]},
        "scope": dict(SCOPE_KEY),
        "member": {"action": "assert", "finding": probe.h._attested(finding_id, fact_id, value)},
        "successor": {"id": successor, "predecessor": predecessor},
    })
    return successor


def make_close(probe: Any, acts: list[dict[str, Any]], closure_fact: str, horizon: str, finding_id: str) -> None:
    probe.h._add(acts, "assertion", {
        "finding": probe.h._attested(finding_id, f"{closure_fact}|family-horizon={horizon},tax-year={probe.YEAR}", True),
    })


def assert_fact(probe: Any, acts: list[dict[str, Any]], finding_id: str, fact_type: str,
                keys: tuple[tuple[str, str], ...], value: Any) -> None:
    fact_id = probe.h.fact_id_for(fact_type, keys + (("tax-year", probe.YEAR),))
    probe.h._add(acts, "assertion", {"finding": probe.h._attested(finding_id, fact_id, value)})


def add_interest_withholding(probe: Any, acts: list[dict[str, Any]], box4: float, box1: float = 100.0) -> list[dict[str, Any]]:
    acts = copy.deepcopy(acts)
    b1_head = get_head(probe, acts, "tax.us.2025.f1099int.b1")
    b4_head = get_head(probe, acts, "tax.us.2025.f1099int.b4")
    payer, stmt = "demo.reuse.int.payer", "demo.reuse.int.stmt"
    keys = (("payer", payer), ("statement", stmt))
    probe.h._introduce(acts, payer, "tax.us.interest-payer")
    probe.h._introduce(acts, stmt, "tax.us.1099int-statement")
    b1_head = make_transition(
        probe, acts, ("tax.us.2025.f1099int.b1", "v1"), b1_head, "demo.reuse.int.b1.h1",
        "demo.reuse.int.box1", "tax.us.2025.f1099int.box1-interest", keys, box1)
    b4_head = make_transition(
        probe, acts, ("tax.us.2025.f1099int.b4", "v1"), b4_head, "demo.reuse.int.b4.h1",
        "demo.reuse.int.box4", "tax.us.2025.f1099int.box4-withholding", keys, box4)
    make_close(probe, acts, "tax.us.2025.f1099int.b1.source-closure", b1_head, "demo.reuse.int.closure.box1")
    make_close(probe, acts, "tax.us.2025.f1099int.b4.source-closure", b4_head, "demo.reuse.int.closure.box4")
    return probe.h.renumber(acts)


def add_dividend_withholding(probe: Any, acts: list[dict[str, Any]], box4: float, box1a: float = 200.0) -> list[dict[str, Any]]:
    acts = copy.deepcopy(acts)
    a_head = get_head(probe, acts, "tax.us.2025.f1099div.1a")
    div_b4_head = get_head(probe, acts, "tax.us.2025.f1099div.b4")
    payer, stmt = "demo.reuse.div.payer", "demo.reuse.div.stmt"
    keys = (("payer", payer), ("statement", stmt))
    probe.h._introduce(acts, payer, "tax.us.dividend-payer")
    probe.h._introduce(acts, stmt, "tax.us.1099div-statement")
    a_head = make_transition(
        probe, acts, ("tax.us.2025.f1099div.1a", "v1"), a_head, "demo.reuse.div.1a.h1",
        "demo.reuse.div.box1a", "tax.us.2025.f1099div.box1a-ordinary", keys, box1a)
    div_b4_head = make_transition(
        probe, acts, ("tax.us.2025.f1099div.b4", "v1"), div_b4_head, "demo.reuse.div.b4.h1",
        "demo.reuse.div.box4", "tax.us.2025.f1099div.box4-withholding", keys, box4)
    make_close(probe, acts, "tax.us.2025.f1099div.1a.source-closure", a_head, "demo.reuse.div.closure.1a")
    make_close(probe, acts, "tax.us.2025.f1099div.b4.source-closure", div_b4_head, "demo.reuse.div.closure.box4")
    return probe.h.renumber(acts)


def add_ira_withholding(probe: Any, acts: list[dict[str, Any]], withheld: float, distribution: float = 1000.0) -> list[dict[str, Any]]:
    acts = copy.deepcopy(acts)
    payer, stmt = "demo.reuse.r.payer", "demo.reuse.r.stmt"
    keys = (("payer", payer), ("statement", stmt))
    probe.h._introduce(acts, payer, "tax.us.ira-payer")
    probe.h._introduce(acts, stmt, "tax.us.1099r-statement")
    assert_fact(probe, acts, "demo.reuse.r.box2a", "tax.us.2025.f1099r.ira-box2a-taxable-amount", keys, distribution)
    assert_fact(probe, acts, "demo.reuse.r.checkbox", "tax.us.2025.f1099r.ira-sep-simple-checkbox", keys, True)
    assert_fact(probe, acts, "demo.reuse.r.code", "tax.us.2025.f1099r.distribution-code", keys, "7")
    assert_fact(probe, acts, "demo.reuse.r.box2b", "tax.us.2025.f1099r.box2b-not-determined", keys, False)
    head = make_transition(
        probe, acts, ("tax.us.2025.f1099r.ira-fully-taxable", "v2"),
        get_head(probe, acts, "tax.us.2025.f1099r.ira-fully-taxable"),
        "demo.reuse.r.h1", "demo.reuse.r.box1", "tax.us.2025.f1099r.ira-box1-taxable-distribution", keys, distribution)
    make_close(probe, acts, "tax.us.2025.f1099r.ira-fully-taxable.source-closure", head, "demo.reuse.r.closure.box1")
    b4_head = make_transition(
        probe, acts, ("tax.us.2025.f1099r.box4", "v1"), get_head(probe, acts, "tax.us.2025.f1099r.box4"),
        "demo.reuse.r.b4.h1", "demo.reuse.r.box4", "tax.us.2025.f1099r.ira-box4-withholding", keys, withheld)
    make_close(probe, acts, "tax.us.2025.f1099r.box4.source-closure", b4_head, "demo.reuse.r.closure.box4")
    return probe.h.renumber(acts)


def add_unemployment_withholding(probe: Any, acts: list[dict[str, Any]], withheld: float, amount: float = 1000.0) -> list[dict[str, Any]]:
    acts = copy.deepcopy(acts)
    body_b4 = json.loads((REPO / "packages/content/tax/2025/f1099g-box4.bundle.json").read_text(encoding="utf-8"))
    if not {item["id"] for item in body_b4["fact_types"]} & probe.h._adopted(acts):
        probe.h._add(acts, "bundle-adoption", {"bundle": body_b4})
    head = get_head(probe, acts, "tax.us.2025.f1099g.1")
    payer, stmt = "demo.reuse.g.payer", "demo.reuse.g.stmt"
    keys = (("payer", payer), ("statement", stmt))
    probe.h._introduce(acts, payer, "tax.us.unemployment-payer")
    probe.h._introduce(acts, stmt, "tax.us.1099g-statement")
    head = make_transition(
        probe, acts, ("tax.us.2025.f1099g.1", "v1"), head, "demo.reuse.g1.h1",
        "demo.reuse.g.box1", "tax.us.2025.f1099g.box1-unemployment", keys, amount)
    make_close(probe, acts, "tax.us.2025.f1099g.1.source-closure", head, "demo.reuse.g.closure.box1")
    head_b4 = ensure_genesis(probe, acts, "tax.us.2025.f1099g.b4", "v1")
    head_b4 = make_transition(
        probe, acts, ("tax.us.2025.f1099g.b4", "v1"), head_b4, "demo.reuse.g4.h1",
        "demo.reuse.g.box4", "tax.us.2025.f1099g.box4-withholding", keys, withheld)
    make_close(probe, acts, "tax.us.2025.f1099g.b4.source-closure", head_b4, "demo.reuse.g.closure.box4")
    return probe.h.renumber(acts)


def add_ssa_withholding(probe: Any, acts: list[dict[str, Any]], withheld: float, benefits: float = 1000.0) -> list[dict[str, Any]]:
    acts = copy.deepcopy(acts)
    body_b6 = json.loads((REPO / "packages/content/tax/2025/ssa1099-box6.bundle.json").read_text(encoding="utf-8"))
    if not {item["id"] for item in body_b6["fact_types"]} & probe.h._adopted(acts):
        probe.h._add(acts, "bundle-adoption", {"bundle": body_b6})
    scope_fact = "tax.us.2025.schedule1-adjustments-scope.no-line24z-writein"
    if not any(str((act.get("payload") or {}).get("finding", {}).get("fact_id", "")).startswith(scope_fact + "|") for act in acts):
        probe.h._add(acts, "assertion", {"finding": probe.h._attested(
            "demo.reuse.ssa.scope.no-line24z-writein", f"{scope_fact}|tax-year={probe.YEAR}", "yes")})
    head = get_head(probe, acts, "tax.us.2025.ssa1099.benefits")
    stmt = "demo.reuse.ssa.stmt"
    keys = (("statement", stmt),)
    probe.h._introduce(acts, stmt, "tax.us.ssa1099-statement")
    assert_fact(probe, acts, "demo.reuse.ssa.b3", "tax.us.2025.ssa1099.box3-benefits-paid", keys, benefits)
    assert_fact(probe, acts, "demo.reuse.ssa.b4", "tax.us.2025.ssa1099.box4-repayment", keys, 0.0)
    assert_fact(probe, acts, "demo.reuse.ssa.witness", "tax.us.2025.ssa1099.box6-withholding", keys, 0.0)
    assert_fact(probe, acts, "demo.reuse.ssa.recipient", "tax.us.2025.ssa1099.recipient", keys, "taxpayer")
    assert_fact(probe, acts, "demo.reuse.ssa.kind", "tax.us.2025.ssa1099.statement-kind", keys, "ssa-1099")
    assert_fact(probe, acts, "demo.reuse.ssa.lump", "tax.us.2025.ssa1099.lump-sum-election", keys, False)
    head = make_transition(
        probe, acts, ("tax.us.2025.ssa1099.benefits", "v1"), head, "demo.reuse.ssa.h1",
        "demo.reuse.ssa.b5", "tax.us.2025.ssa1099.box5-net-benefits", keys, benefits)
    make_close(probe, acts, "tax.us.2025.ssa1099.source-closure", head, "demo.reuse.ssa.closure.benefits")
    head_b6 = ensure_genesis(probe, acts, "tax.us.2025.ssa1099.b6", "v1")
    head_b6 = make_transition(
        probe, acts, ("tax.us.2025.ssa1099.b6", "v1"), head_b6, "demo.reuse.ssa6.h1",
        "demo.reuse.ssa.box6", "tax.us.2025.ssa1099.box6-voluntary-withholding", keys, withheld)
    make_close(probe, acts, "tax.us.2025.ssa1099.b6.source-closure", head_b6, "demo.reuse.ssa.closure.box6")
    return probe.h.renumber(acts)


def build_reuse(probe: Any, core: Any) -> list[dict[str, Any]]:
    base = wage(probe, core)
    cases = []
    for case_id, builder, withheld, note in (
        ("reuse_int_alone", add_interest_withholding, 50.0, "Form 1099-INT withholding 50. Present no."),
        ("reuse_div_alone", add_dividend_withholding, 75.0, "Form 1099-DIV withholding 75. Present no."),
        ("reuse_ira_alone", add_ira_withholding, 80.0, "Form 1099-R withholding 80. Present no."),
        ("reuse_unemp_alone", add_unemployment_withholding, 90.0, "Form 1099-G withholding 90. Present no."),
        ("reuse_ssa_alone", add_ssa_withholding, 60.0, "Form SSA-1099 box 6 withholding 60. Present no."),
    ):
        acts = builder(probe, base, withheld)
        cases.append({
            "id": case_id, "kind": "reuse_equal", "acts": acts, "hand": None, "note": note,
            "expect_25b": withheld, "compare": "equal_v84",
        })
    all_five = add_interest_withholding(probe, base, 50.0)
    all_five = add_dividend_withholding(probe, all_five, 75.0)
    all_five = add_ira_withholding(probe, all_five, 80.0)
    all_five = add_unemployment_withholding(probe, all_five, 90.0)
    all_five = add_ssa_withholding(probe, all_five, 60.0)
    cases.append({
        "id": "reuse_all_five_alone", "kind": "reuse_equal", "acts": all_five, "hand": None,
        "note": "Five legacy subtotals 355. Present no.", "expect_25b": 355.0, "compare": "equal_v84",
    })
    with_b4 = set_stmt(probe, core, wage(probe, core, kinds={"covered"}, tag="reuse_b4"),
                       "demo.sfa.reuse_b4.statement", 100)
    with_b4 = add_interest_withholding(probe, with_b4, 50.0)
    with_b4 = add_dividend_withholding(probe, with_b4, 75.0)
    with_b4 = add_ira_withholding(probe, with_b4, 80.0)
    with_b4 = add_unemployment_withholding(probe, with_b4, 90.0)
    with_b4 = add_ssa_withholding(probe, with_b4, 60.0)
    cases.append({
        "id": "reuse_all_with_b4", "kind": "reuse_equal", "acts": with_b4, "hand": None,
        "note": "Five legacy subtotals 355 plus per-statement box 4 100. Present no. Line 25b 455.",
        "expect_25b": 455.0, "compare": "equal_v84",
    })
    sale = set_stmt(probe, core, wage(probe, core, kinds={"covered"}), SALE, 200)
    cases.append({
        "id": "reuse_b4_subtotal", "kind": "reuse_equal", "acts": sale,
        "hand": probe.hand_return(st_gain=1000, line25b=200),
        "note": "Per-statement box 4 subtotal 200 and the sale question compose on a present-no return.",
        "expect_25b": 200, "compare": "equal_v84",
    })
    unanswered = wage(probe, core, kinds={"covered"}, box4_sales=False)
    cases.append({
        "id": "reuse_box4_question", "kind": "box4_unanswered", "acts": unanswered, "hand": None,
        "note": "A sale with no per-statement box 4. Both cores ask the unchanged sale box 4 question.",
        "compare": "box4_question",
    })
    loss = wage(probe, core, kinds={"covered"}, proceeds=1000, basis=2000, loss=True)
    loss = set_stmt(probe, core, loss, SALE, 0, box7="yes")
    cases.append({
        "id": "reuse_box7_check", "kind": "box7_loss", "acts": loss, "hand": None,
        "note": "Box 7 yes beside a loss. Line 16 blocks the same way on both cores. Present no.",
        "compare": "box7",
    })
    cases.append({
        "id": "reuse_no_equals_v84", "kind": "reuse_equal", "acts": wage(probe, core),
        "hand": probe.hand_return(line25b=0),
        "note": "A present-no wage return. Line 25b equals v84.",
        "expect_25b": 0, "compare": "equal_v84",
    })
    return cases


def build_surface(probe: Any, core: Any) -> list[dict[str, Any]]:
    return [
        spec("surface_published_no", "published", with_present(probe, core, wage(probe, core), "no", None),
             hand=probe.hand_return(line25b=0), note="Present no. Line 25b 0. Consumers publish.", expect_25b=0),
        spec("surface_published_yes", "published", with_present(probe, core, wage(probe, core), "yes", 150),
             hand=probe.hand_return(line25b=150), note="Present yes, amount 150. Consumers follow 25b.",
             expect_25b=150),
        spec("surface_published_sale", "published",
             with_present(probe, core, set_stmt(probe, core, wage(probe, core, kinds={"covered"}), SALE, 200), "no", None),
             hand=probe.hand_return(st_gain=1000, line25b=200), note="Sale 200, present no.",
             expect_25b=200, st_gain=1000),
        spec("surface_blocked_present", "blocked_present", with_present(probe, core, wage(probe, core), None, None),
             hand=probe.hand_return(blocked=True), note="Unanswered yes/no. Presentation shows that question."),
        spec("surface_blocked_amount", "blocked_amount", with_present(probe, core, wage(probe, core), "yes", None),
             hand=probe.hand_return(blocked=True), note="Unanswered amount. Presentation shows the amount question."),
        spec("surface_blocked_sale_box4", "box4_unanswered",
             with_present(probe, core, wage(probe, core, kinds={"covered"}, box4_sales=False), "no", None),
             hand=None, note="Sale box 4 unanswered, present no. The per-statement question is asked."),
    ]


def contract_failures(case: dict[str, Any], result: dict[str, Any],
                      present_q: str, amount_q: str, box4_q: str) -> list[str]:
    if result.get("outcome") != "success":
        return [f"outcome {result.get('outcome')} {result.get('error') or result.get('reason')}"]
    found: list[str] = []
    if result.get("presentation_valid") is not True:
        found.append(f"presentation {result.get('presentation_valid')}")
    kind = case["kind"]
    questions = result.get("questions") or []
    field = result.get("line25b_field") or {}
    if field.get("version") != "v6":
        found.append(f"line 25b field version {field.get('version')}")
    if field.get("blocked_explain") != BLOCKED_EXPLAIN:
        found.append("line 25b blocked explain is not the Decision 7 sentence")
    if PRESENT_EXCLUDE not in present_q:
        found.append("present question omits the Decision 7 exclusion")
    if AMOUNT_EXCLUDE not in amount_q:
        found.append("amount question omits the Decision 7 exclusion")
    if len(result.get("line25b_rows") or []) != 1:
        found.append(f"line 25b cardinality {len(result.get('line25b_rows') or [])}")
    if kind == "published":
        found.extend(hand_failures(result, case["hand"] or {}))
        if present_q in questions or amount_q in questions:
            found.append(f"published return still asking {questions}")
        if case.get("expect_25b") is not None and (result.get("lines") or {}).get("form1040.line-25b") != case["expect_25b"]:
            found.append(f"line 25b { (result.get('lines') or {}).get('form1040.line-25b') } expected {case['expect_25b']}")
    if kind == "double":
        if (result.get("lines") or {}).get("form1040.line-25b") != 300:
            found.append(f"double-count line 25b {(result.get('lines') or {}).get('form1040.line-25b')}")
    if kind == "blocked_present":
        if not _blocked(result):
            found.append(f"line 25b {(result.get('lines') or {}).get('form1040.line-25b')}")
        if present_q not in questions:
            found.append(f"questions {questions}")
        missing = (row_for(result, "rule.form1040-line25b") or [{}])[0].get("missing") or []
        if "f1099b.no-sale-box4-present" not in missing:
            found.append(f"missing {missing}")
        for line in ("form1040.line-25d", "form1040.line-33", "form1040.line-34", "form1040.line-37"):
            if not _blocked(result, line):
                found.append(f"{line} {(result.get('lines') or {}).get(line)}")
        if (result.get("lines") or {}).get("form1040.line-25a") != 4500:
            found.append(f"line 25a {(result.get('lines') or {}).get('form1040.line-25a')}")
        row = (row_for(result, "rule.form1040-line25b") or [{}])[0]
        if row.get("code") not in ("DEPENDENCY_ABSENT", None) and row.get("disposition") != "blocked":
            found.append(f"line 25b row {row}")
    if kind == "blocked_amount":
        if not _blocked(result):
            found.append(f"line 25b {(result.get('lines') or {}).get('form1040.line-25b')}")
        if amount_q not in questions:
            found.append(f"questions {questions}")
        missing = (row_for(result, "rule.form1040-line25b") or [{}])[0].get("missing") or []
        if "f1099b.no-sale-box4-withholding" not in missing:
            found.append(f"missing {missing}")
        for line in ("form1040.line-25d", "form1040.line-33", "form1040.line-34", "form1040.line-37"):
            if not _blocked(result, line):
                found.append(f"{line} {(result.get('lines') or {}).get(line)}")
    if kind == "box4_unanswered":
        if box4_q not in questions:
            found.append(f"questions {questions}")
        if not _blocked(result):
            found.append(f"line 25b {(result.get('lines') or {}).get('form1040.line-25b')}")
    if kind == "box7_loss":
        if not _blocked(result, "schedule-d.line-16"):
            found.append(f"line 16 {(result.get('lines') or {}).get('schedule-d.line-16')}")
    return found


def late_failures(trace: dict[str, Any], steps: list[dict[str, Any]]) -> list[str]:
    found: list[str] = []
    if len(steps) != 2:
        return ["missing step"]
    before, after = steps
    if not before["passed"] or not after["passed"]:
        found.append("a step failed its own contract")
    name = trace["id"]
    before_ids = [row["finding_id"] for row in (before["result"].get("publications") or [])
                  if row["symbol"] in {"payments.line25b", "form1040.line-25b"}]
    after_ids = [row["finding_id"] for row in (after["result"].get("publications") or [])
                 if row["symbol"] in {"payments.line25b", "form1040.line-25b"}]
    if name == "late_yes_then_sale_then_no":
        if not before_ids or before_ids[0] in after_ids:
            found.append(f"prior line 25b finding stayed current {before_ids} -> {after_ids}")
        values = [row["value"] for row in after["snapshot"]["present"]]
        if values != ["yes", "no"]:
            found.append(f"present findings {values}")
        if (after["result"].get("lines") or {}).get("form1040.line-25b") != 150:
            found.append("after-sale line 25b is not the one per-statement copy")
    if name == "late_sale_removed":
        if (after["result"].get("lines") or {}).get("form1040.line-25b") != 200:
            found.append("leftover per-statement amount did not remain")
    if name == "late_amount_corrected":
        values = [row["value"] for row in after["snapshot"]["amount"]]
        if values != [150, 80]:
            found.append(f"amount findings {values}")
        if not before_ids or before_ids[0] in after_ids:
            found.append(f"prior line 25b finding stayed current {before_ids} -> {after_ids}")
    if name == "late_yes_to_no":
        values = [row["value"] for row in after["snapshot"]["present"]]
        if values != ["yes", "no"]:
            found.append(f"present findings {values}")
        if (after["result"].get("lines") or {}).get("form1040.line-25b") != 0:
            found.append("present no still added the return-level amount")
        if not before_ids or before_ids[0] in after_ids:
            found.append(f"prior line 25b finding stayed current {before_ids} -> {after_ids}")
    return found


def reuse_failures(case: dict[str, Any], paired: dict[str, Any],
                   present_q: str, amount_q: str, box4_q: str) -> list[str]:
    v85 = paired["v85"]
    v84 = paired["v84"]
    found = contract_failures({**case, "kind": case["kind"] if case["kind"] != "reuse_equal" else "published"},
                              v85, present_q, amount_q, box4_q) if case["kind"] != "reuse_equal" else []
    if case["kind"] == "reuse_equal":
        found.extend(contract_failures({**case, "kind": "published", "hand": case.get("hand") or {}},
                                       v85, present_q, amount_q, box4_q) if case.get("hand") else [])
        if v84.get("outcome") != "success":
            found.append(f"v84 {v84.get('outcome')} {v84.get('error') or v84.get('message')}")
            return found
        if case.get("hand"):
            found.extend(f"v84 {item}" for item in hand_failures(v84, case["hand"]))
        v85_line = (v85.get("lines") or {}).get("form1040.line-25b")
        v84_line = (v84.get("lines") or {}).get("form1040.line-25b")
        if v85_line != v84_line:
            found.append(f"line 25b v85 {v85_line} v84 {v84_line}")
        if case.get("expect_25b") is not None and v85_line != num(case["expect_25b"]):
            found.append(f"line 25b {v85_line} expected {case['expect_25b']}")
        for symbol in SUBTOTALS:
            if pub_values(v85, symbol) != pub_values(v84, symbol) and pub_values(v84, symbol):
                found.append(f"{symbol} v85 {pub_values(v85, symbol)} v84 {pub_values(v84, symbol)}")
        v85_lines = {key: value for key, value in (v85.get("lines") or {}).items()
                     if not str(value).startswith("blocked") or key in (v84.get("lines") or {})}
        # Published numbers on v84 must match v85.
        for key, value in (v84.get("lines") or {}).items():
            if (v85.get("lines") or {}).get(key) != value:
                found.append(f"{key} v85 {(v85.get('lines') or {}).get(key)} v84 {value}")
        del v85_lines
    if case["kind"] == "box4_unanswered":
        if box4_q not in (v85.get("questions") or []):
            found.append(f"v85 questions {v85.get('questions')}")
        if box4_q not in (v84.get("questions") or []):
            found.append(f"v84 questions {v84.get('questions')}")
        if not _blocked(v85) or not _blocked(v84):
            found.append("sale box 4 unanswered did not block line 25b")
    if case["kind"] == "box7_loss":
        if not _blocked(v85, "schedule-d.line-16") or not _blocked(v84, "schedule-d.line-16"):
            found.append("box 7 loss did not block line 16 on both cores")
        if (v85.get("lines") or {}).get("form1040.line-25b") != (v84.get("lines") or {}).get("form1040.line-25b"):
            found.append("line 25b moved on a box 7 loss return")
    return found


def package_identity(v85: Any, v84: Any) -> dict[str, Any]:
    def versions(core: Any) -> dict[str, list[str]]:
        package = json.loads(core.package_path.read_text(encoding="utf-8"))
        found: dict[str, list[str]] = {}
        for member in package["members"]:
            mid = str(member["id"])
            if (
                mid.endswith("rule.form1040-line25b")
                or "form1040.line-25b" in mid
                or mid.endswith("rule.f1099b-b4-withholding-subtotal")
                or mid.endswith("input-question.f1099b-box4")
                or "box7-loss-check" in mid
                or mid.endswith("rule.f1099int-b4-subtotal")
                or mid.endswith("rule.f1099div-b4-subtotal")
                or mid.endswith("rule.f1099r-box4-subtotal")
                or mid.endswith("rule.f1099g-b4-subtotal")
                or mid.endswith("rule.ssa1099-b6-subtotal")
            ):
                found.setdefault(mid.removeprefix(P), []).append(member["version"])
        return found

    left, right = versions(v84), versions(v85)
    return {
        "same_ids": sorted(set(left) & set(right)),
        "version_diff": [
            {"id": key, "v84": left.get(key), "v85": right.get(key)}
            for key in sorted(set(left) | set(right)) if left.get(key) != right.get(key)
        ],
    }


def line25b_bindings(core: Any) -> list[dict[str, Any]]:
    package = json.loads(core.package_path.read_text(encoding="utf-8"))
    members = {(member["id"], member["version"]): member for member in package["members"]}
    symbol = "tax.us.2025.payments.line25b"
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
            "id": str(body["id"]).removeprefix(P),
            "version": body.get("version"),
            "direct_require": symbol in requires,
            "binds_symbol": str(body.get("binds_symbol") or "").removeprefix(P) or None,
        })
    return found


def write_output(name: str, payload: dict[str, Any]) -> None:
    probe = load_probe()
    text = probe.h.scrub(json.dumps(payload, indent=2) + "\n")
    for needle in ("/Users/", "/private/", "/tmp/", "/var/"):
        if needle in text:
            raise SystemExit(f"{name} contains {needle}")
    (HERE / name).write_text(text, encoding="utf-8")


def _one(item: tuple[str, str, list[dict[str, Any]]]) -> tuple[str, dict[str, Any]]:
    case_id, core_path, acts = item
    probe = load_probe()
    core = scratch_core(probe, Path(core_path))
    return case_id, execute(core, acts, "demo.b4only.t0." + case_id)


def _pair(item: tuple[str, str, list[dict[str, Any]]]) -> tuple[str, dict[str, Any]]:
    case_id, core_path, acts = item
    probe = load_probe()
    v85 = scratch_core(probe, Path(core_path))
    v84 = published_v84(probe)
    v85_acts = with_present(probe, v85, copy.deepcopy(acts), "no", None, tag="reuse")
    return case_id, {
        "v85": execute(v85, v85_acts, "demo.b4only.t0." + case_id + ".v85"),
        "v84": execute(v84, acts, "demo.b4only.t0." + case_id + ".v84"),
    }


def run_pool(core_path: str, cases: list[tuple[str, list[dict[str, Any]]]]) -> dict[str, dict[str, Any]]:
    workers = int(os.environ.get("B4ONLY_WORKERS") or min(6, os.cpu_count() or 2))
    found: dict[str, dict[str, Any]] = {}
    items = [(case_id, core_path, acts) for case_id, acts in cases]
    with ProcessPoolExecutor(max_workers=workers) as pool:
        done = 0
        for case_id, result in pool.map(_one, items):
            found[case_id] = result
            done += 1
            line = (result.get("lines") or {}).get("form1040.line-25b")
            print(f"{done}/{len(items)} {case_id} {result.get('outcome')} {line}", flush=True)
    return found


def attach(case: dict[str, Any], result: dict[str, Any], probe: Any,
           present_q: str, amount_q: str, box4_q: str) -> dict[str, Any]:
    failures = contract_failures(case, result, present_q, amount_q, box4_q)
    return {
        "id": case["id"],
        "kind": case["kind"],
        "note": case.get("note"),
        "hand": case.get("hand"),
        "snapshot": snapshot(probe, case["acts"]),
        "result": result,
        "failures": failures,
        "passed": not failures,
    }


def _nb_diff(left: Any, right: Any) -> list[str]:
    if left == right:
        return []
    if not isinstance(left, dict) or not isinstance(right, dict):
        return ["pin"]
    found = []
    for key in sorted(set(left) | set(right)):
        if left.get(key) == right.get(key):
            continue
        if isinstance(left.get(key), dict) and isinstance(right.get(key), dict):
            for name in sorted(set(left[key]) | set(right[key])):
                if left[key].get(name) != right[key].get(name):
                    found.append(f"{key}.{name}")
        else:
            found.append(str(key))
    return found


def classify_neighbour(v84: dict[str, Any], v85: dict[str, Any]) -> dict[str, Any]:
    if v84 == v85:
        return {"class": "identical"}
    if "error" in v84 or "error" in v85:
        return {"class": "counterexample", "changed": _nb_diff(v84, v85)[:24]}
    v84_line = (v84.get("lines") or {}).get("form1040.line-25b")
    v85_line = (v85.get("lines") or {}).get("form1040.line-25b")
    v84_ok = isinstance(v84_line, (int, float)) or v84_line == 0
    v85_blocked = isinstance(v85_line, str) and "block" in str(v85_line)
    missing = []
    row = (v85.get("rows") or {}).get("form1040-line25b")
    if isinstance(row, list) and len(row) == 3 and isinstance(row[2], list):
        missing = [str(item) for item in row[2]]
    reasons = (v85.get("reasons") or {}).get("form1040.line-25b") or []
    blob = json.dumps(v85)
    asks_present = PRESENT in blob or any("no closed sale" in str(item) for item in reasons)
    asks_amount = AMOUNT in blob or any("Enter" in str(item) and "no closed sale" in str(item) for item in reasons)
    if v84_ok and v85_blocked and asks_present:
        return {"class": "asks_no_sale_present", "v85_missing": missing[:8]}
    if v84_ok and v85_blocked and asks_amount:
        return {"class": "asks_no_sale_amount", "v85_missing": missing[:8]}
    v84_blocked = isinstance(v84_line, str) and "block" in str(v84_line)
    if v84_blocked and v85_blocked:
        changed = _nb_diff(v84, v85)
        if asks_present:
            return {"class": "still_blocked_also_asks_present", "changed": changed[:24]}
        return {"class": "still_blocked", "changed": changed[:24]}
    return {"class": "counterexample", "changed": _nb_diff(v84, v85)[:24]}


def _nb_pin(test: Any, core: Any, acts: list[dict[str, Any]], run_id: str) -> dict[str, Any]:
    t = test.track0()
    with t.h.loader_entries(core):
        return test.pin(t.run_coordinate(core, acts, run_id))


def _nb_scratch(test: Any, core_path: Path) -> Any:
    body = json.loads(core_path.read_text(encoding="utf-8"))
    t = test.track0()
    return t.h.Core(
        body["version"], body["registry"], body["release_version"],
        content=Path(body["content"]), releases=Path(body["releases"]),
        loader_from=body.get("loader_from"),
    )


def _nb_pair(item: tuple[str, list[dict[str, Any]]]) -> tuple[str, dict[str, Any], dict[str, Any], dict[str, Any]]:
    key, acts = item
    test = load_test()
    slug = key.replace("/", ".")
    v85 = _nb_scratch(test, Path(os.environ["B4ONLY_CORE"]))
    v84 = test.track0().h.Core("v84", "v82", "v82")
    pin85 = _nb_pin(test, v85, acts, "demo.b4only.t0.nb.v85." + slug)
    pin84 = _nb_pin(test, v84, acts, "demo.b4only.t0.nb.v84." + slug)
    row = classify_neighbour(pin84, pin85)
    if row["class"] != "identical":
        row["v84_line25b"] = pin84.get("error") or (pin84.get("lines") or {}).get("form1040.line-25b")
        row["v85_line25b"] = pin85.get("error") or (pin85.get("lines") or {}).get("form1040.line-25b")
    return key, row, pin84, pin85


def _nb_restore(item: tuple[str, list[dict[str, Any]], dict[str, Any]]) -> tuple[str, dict[str, Any]]:
    key, acts, pin84 = item
    test = load_test()
    probe = load_probe()
    slug = key.replace("/", ".")
    v85 = _nb_scratch(test, Path(os.environ["B4ONLY_CORE"]))
    answered = probe.say_return(copy.deepcopy(acts), v85, probe.PRESENT, "no", "t0.restore")
    pin85 = _nb_pin(test, v85, answered, "demo.b4only.t0.nb.restore." + slug)
    line_keys = sorted(set((pin84.get("lines") or {}) | (pin85.get("lines") or {})))
    diffs = [name for name in line_keys if (pin84.get("lines") or {}).get(name) != (pin85.get("lines") or {}).get(name)]
    return key, {
        "restored": not diffs and "error" not in pin85,
        "diffs": diffs[:24],
        "v84_line25b": pin84.get("error") or (pin84.get("lines") or {}).get("form1040.line-25b"),
        "v85_line25b": pin85.get("error") or (pin85.get("lines") or {}).get("form1040.line-25b"),
    }


def neighbour_tasks(test: Any, expected: dict[str, Any]) -> list[tuple[str, list[dict[str, Any]]]]:
    t = test.track0()
    print("building track 0 act lists", flush=True)
    cases = dict(test.decided_cases(t))
    print("exporting the 213 returns", flush=True)
    with tempfile.TemporaryDirectory() as tmp:
        exported = test.export_returns(Path(tmp))
    returns = test.return_acts(t, exported)
    v84 = t.h.Core("v84", "v82", "v82")
    out: list[tuple[str, list[dict[str, Any]]]] = []
    for key in expected["track0"]:
        out.append((f"track0/{key}", cases[key]))
    for key in expected["returns"]:
        out.append((f"returns/{key}", returns[key]))
    for key in expected["zero_sample"]:
        out.append((f"zero/{key}", test.with_zero(t, returns[key], v84)))
    return out


def run_neighbour(core_path: str) -> None:
    os.environ["B4ONLY_CORE"] = core_path
    test = load_test()
    expected = json.loads(EXPECTED.read_text(encoding="utf-8"))
    work = neighbour_tasks(test, expected)
    only = {item for item in os.environ.get("B4ONLY_RERUN_ONLY", "").split(",") if item}
    if only:
        work = [item for item in work if item[0] in only]
    workers = int(os.environ.get("B4ONLY_WORKERS") or min(6, os.cpu_count() or 2))
    print(f"running {len(work)} recorded returns on live v84 and scratch v85", flush=True)
    found: dict[str, dict[str, Any]] = {}
    pins84: dict[str, dict[str, Any]] = {}
    acts_by: dict[str, list[dict[str, Any]]] = {key: acts for key, acts in work}
    with ProcessPoolExecutor(max_workers=workers) as pool:
        done = 0
        for key, row, pin84, _pin85 in pool.map(_nb_pair, work):
            found[key] = row
            pins84[key] = pin84
            done += 1
            if done % 20 == 0 or done == len(work):
                print(f"{done}/{len(work)} {key} {row['class']}", flush=True)
    counts = dict(Counter(found[key]["class"] for key in found))
    changes = [{"id": key, **found[key]} for key in sorted(found) if found[key]["class"] != "identical"]
    asks = [key for key in sorted(found) if found[key]["class"] == "asks_no_sale_present"]
    identical = [key for key in sorted(found) if found[key]["class"] == "identical"]
    counter = [key for key in sorted(found) if found[key]["class"] == "counterexample"]
    print(f"restoring {len(asks)} returns with present=no", flush=True)
    restore_work = [(key, acts_by[key], pins84[key]) for key in asks]
    restored: dict[str, dict[str, Any]] = {}
    with ProcessPoolExecutor(max_workers=workers) as pool:
        done = 0
        for key, row in pool.map(_nb_restore, restore_work):
            restored[key] = row
            done += 1
            if done % 20 == 0 or done == len(restore_work):
                print(f"restore {done}/{len(restore_work)} {key} {row['restored']}", flush=True)
    restore_failed = [key for key in asks if not restored[key]["restored"]]
    payload = {
        "scope": "neighbour",
        "core": "live-v84-and-live-v85",
        "compared_to": "live v84 against live scratch v85; recorded answers, not substituted",
        "answers": "recorded, not substituted; restore adds present=no on the 91",
        "runs": len(found),
        "live_runs": len(found) * 2 + len(asks),
        "counts": counts,
        "classes": {key: found[key]["class"] for key in sorted(found)},
        "asks_no_sale_present_ids": asks,
        "identical_ids": identical,
        "counterexample_ids": counter,
        "changes": changes,
        "change_count": len(changes),
        "restore": {
            "added_answer": "f1099b.no-sale-box4-present = no",
            "count": len(asks),
            "restored": [key for key in asks if restored[key]["restored"]],
            "failed": restore_failed,
            "rows": [{"id": key, **restored[key]} for key in asks],
        },
        "passed": not counter and not restore_failed and len(asks) + len(identical) == len(found),
    }
    write_output("track0-neighbour.json", payload)
    print(json.dumps({
        "runs": len(found), "counts": counts, "asks": len(asks),
        "restore_failed": restore_failed, "passed": payload["passed"],
    }, indent=2))


def main() -> None:
    if len(sys.argv) != 3:
        raise SystemExit(
            "usage: track0.py <scratch-core.json> <authority|matrix|late|reuse|neighbour|surface>")
    scope = sys.argv[2]
    core_path = str(Path(sys.argv[1]).resolve())
    if scope == "neighbour":
        run_neighbour(core_path)
        return
    probe = load_probe()
    core = scratch_core(probe, Path(core_path))
    present_q, amount_q, box4_q = question_texts(core)
    only = {item for item in os.environ.get("B4ONLY_TRACK0_ONLY", "").split(",") if item}

    if scope == "late":
        traces = build_late(probe, core)
        items = [(step["id"], step["acts"]) for trace in traces for step in trace["steps"]]
        if only:
            items = [item for item in items if item[0] in only]
        found = run_pool(core_path, items)
        saved = []
        for trace in traces:
            steps = []
            for step in trace["steps"]:
                if step["id"] not in found:
                    continue
                steps.append(attach({**step, "note": trace["paper"]}, found[step["id"]], probe,
                                    present_q, amount_q, box4_q))
            extra = late_failures(trace, steps) if len(steps) == 2 else ["missing step"]
            saved.append({
                "id": trace["id"], "paper": trace["paper"], "steps": steps, "trace_failures": extra,
                "passed": not extra and all(step["passed"] for step in steps),
            })
        payload = {"scope": scope, "core": "v85", "present_question": present_q,
                   "amount_question": amount_q, "traces": saved,
                   "passed": [row["id"] for row in saved if row["passed"]],
                   "failed": [row["id"] for row in saved if not row["passed"]]}
        write_output("track0-late.json", payload)
        print(json.dumps({"passed": payload["passed"], "failed": payload["failed"]}, indent=2))
        return

    if scope == "reuse":
        v84 = published_v84(probe)
        cases = build_reuse(probe, core)
        if only:
            cases = [case for case in cases if case["id"] in only]
        workers = int(os.environ.get("B4ONLY_WORKERS") or min(4, os.cpu_count() or 2))
        items = [(case["id"], core_path, case["acts"]) for case in cases]
        found_pairs: dict[str, dict[str, Any]] = {}
        with ProcessPoolExecutor(max_workers=workers) as pool:
            for case_id, paired in pool.map(_pair, items):
                found_pairs[case_id] = paired
                print(f"{case_id} v85 {paired['v85'].get('outcome')} v84 {paired['v83'].get('outcome') if False else paired['v84'].get('outcome')}", flush=True)
        saved = []
        for case in cases:
            failures = reuse_failures(case, found_pairs[case["id"]], present_q, amount_q, box4_q)
            saved.append({
                "id": case["id"], "compare": case.get("compare"), "kind": case["kind"],
                "note": case.get("note"), "hand": case.get("hand"),
                "snapshot": snapshot(probe, case["acts"]),
                "v85": found_pairs[case["id"]]["v85"], "v84": found_pairs[case["id"]]["v84"],
                "failures": failures, "passed": not failures,
            })
        identity = package_identity(core, v84)
        payload = {"scope": scope, "core": "v85-and-v84", "package_identity": identity, "cases": saved,
                   "passed": [row["id"] for row in saved if row["passed"]],
                   "failed": [row["id"] for row in saved if not row["passed"]]}
        write_output("track0-reuse.json", payload)
        print(json.dumps({"passed": payload["passed"], "failed": payload["failed"],
                          "version_diff": identity["version_diff"]}, indent=2))
        return

    builders = {"authority": build_authority, "matrix": build_matrix, "surface": build_surface}
    if scope not in builders:
        raise SystemExit(f"unknown scope {scope}")
    cases = builders[scope](probe, core)
    if only:
        cases = [case for case in cases if case["id"] in only]
    found = run_pool(core_path, [(case["id"], case["acts"]) for case in cases])
    saved = [attach(case, found[case["id"]], probe, present_q, amount_q, box4_q) for case in cases]
    payload: dict[str, Any] = {
        "scope": scope, "core": "v85", "present_question": present_q, "amount_question": amount_q,
        "box4_question": box4_q, "cases": saved,
        "passed": [row["id"] for row in saved if row["passed"]],
        "failed": [row["id"] for row in saved if not row["passed"]],
    }
    if scope == "surface":
        payload["bindings"] = line25b_bindings(core)
    write_output(f"track0-{scope}.json", payload)
    print(json.dumps({"passed": len(payload["passed"]), "failed": payload["failed"]}, indent=2))


if __name__ == "__main__":
    if os.environ.get("B4ONLY_TRACK0_WORKER") != "1":
        os.environ["B4ONLY_TRACK0_WORKER"] = "1"
        main()
