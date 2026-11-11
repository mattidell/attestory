"""P0 probes for question wording on published core v86.

Evidence for docs/phases/engine-breadth/milestones/question-wording.md.
Charter: docs/reviews/question-wording/charter-p0.md.

Every case is one live_coordinate_run of synthetic demo.* findings. Hand
values are the 2025 instruction amounts in law.json, not a prototype's
output. This script writes probe-output.json beside itself and does not
edit packages/, tests/, or a published schema.

    python3 docs/phases/engine-breadth/milestones/question-wording-evidence/probe.py
"""

from __future__ import annotations

import importlib.util
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

HARNESS = REPO / "docs/phases/engine-breadth/milestones/sale-family-audit-evidence/audit_harness.py"
CONTENT = REPO / "packages/content/tax/2025"
P = "tax.us.2025."

WASH_ST = (
    "Have you recorded the wash-sale loss adjustment amount (a loss disallowed "
    "because you bought the same investment within 30 days before or after the sale) "
    "of every covered short-term sale on every Form 1099-B you or your spouse received for 2025?"
)
WASH_LT = WASH_ST.replace("short-term", "long-term")
ONLY_2A = (
    "Is it true that you had no capital gains in 2025 other than capital gain "
    "distributions in box 2a of Form 1099-DIV (for example, no gain from selling "
    "stock, funds or other property)?"
)
NO_LOSSES = (
    "Is it true that you had no capital losses in 2025 (for example, no loss from "
    "selling stock, funds or other property)?"
)
SLI_Q = "Is someone else claiming you as a dependent on their 2025 return?"
AGE_TITLE = "Taxpayer is over 65 years of age for 2025"
BLIND_TITLE = "Taxpayer is blind for 2025"
SPOUSE_AGE = "Spouse is over 65 years of age for 2025"
SPOUSE_BLIND = "Spouse is blind for 2025"

DEMOGRAPHIC = (
    P + "taxpayer-over-65",
    P + "taxpayer-blind",
    P + "spouse-over-65",
    P + "spouse-blind",
)
EXC1 = (
    P + "exception1.only-box2a-capital-gains",
    P + "exception1.no-capital-losses",
    P + "exception1.no-qof-deferral",
    P + "exception1.no-boxes-2b-2c-2d",
)
WATCH_LINES = (
    "form1040.line-7a", "form1040.line-7b", "form1040.line-12e", "form1040.line-13b",
    "form1040.line-15", "form1040.line-16",
    "schedule-d.line-1a", "schedule-d.line-1b", "schedule-d.line-7",
    "schedule-d.line-8a", "schedule-d.line-8b", "schedule-d.line-15", "schedule-d.line-16",
    "schedule1.line-21",
)
SYMBOL_KEEP = (
    "adjustment-subtotal", "schedule-d-required", "deductions.line-12e",
    "deductions.schedule-1a", "line36a", "line36b", "line-21", "line21", "sli-worksheet", "senior",
)


def load_harness() -> Any:
    name = "qw_p0_harness"
    module = sys.modules.get(name)
    if module is None:
        spec = importlib.util.spec_from_file_location(name, HARNESS)
        assert spec is not None and spec.loader is not None
        module = importlib.util.module_from_spec(spec)
        sys.modules[name] = module
        spec.loader.exec_module(module)
    return module


def scrub(text: str) -> str:
    text = text.replace(str(REPO), ".")
    import re
    return re.sub(r"/(?:Users|private|tmp|var|opt)/\S+", "<path>", text)


def _num(value: Any) -> Any:
    if isinstance(value, float) and value.is_integer():
        return int(value)
    if isinstance(value, str):
        try:
            number = float(value)
        except ValueError:
            return value
        if number.is_integer():
            return int(number)
    return value


def install_summarize(h: Any) -> None:
    def summarize(outcome: Any) -> dict[str, Any]:
        if outcome.refusal is not None:
            return {"refusal": {"reason": outcome.refusal.reason, "detail": scrub(str(outcome.refusal.detail))[:400]}}
        report = json.loads(outcome.output_path.read_text(encoding="utf-8"))
        model = json.loads(outcome.presentation_path.read_text(encoding="utf-8"))
        lines: dict[str, Any] = {}
        asked: list[dict[str, Any]] = []
        questions: list[str] = []
        titles: list[dict[str, str]] = []

        def take_sentence(sentence: str) -> None:
            sentence = scrub(sentence).strip()
            if sentence.endswith("?") and sentence not in questions:
                questions.append(sentence)

        def walk(node: Any) -> None:
            if isinstance(node, dict):
                fact_id = node.get("factTypeId")
                title = node.get("factTypeTitle")
                if fact_id in DEMOGRAPHIC and isinstance(title, str):
                    row = {"factTypeId": fact_id, "factTypeTitle": title}
                    if row not in titles:
                        titles.append(row)
                for value in node.values():
                    walk(value)
            elif isinstance(node, list):
                for value in node:
                    walk(value)

        for section in model.get("sections") or []:
            field_id = str((section.get("field") or {}).get("id") or "").removeprefix(P)
            resolved = section.get("resolved") or {}
            sentences = []
            for reason in resolved.get("reasons") or []:
                if isinstance(reason, dict):
                    sentence = str(reason.get("sentence") or "").strip()
                    if sentence:
                        sentences.append(scrub(sentence))
                        take_sentence(sentence)
            if field_id in WATCH_LINES:
                value = resolved.get("value")
                disposition = str(resolved.get("disposition"))
                shown = disposition if value is None or "blocked" in disposition else _num(value)
                lines[field_id] = shown
            if sentences and "block" in str(resolved.get("disposition")):
                asked.append({"field": field_id, "sentences": sentences})
        walk(model)
        symbols = {}
        for pub in outcome.publications or ():
            symbol = str(pub.finding.get("symbol") or "")
            short = symbol.removeprefix(P)
            if any(token in short for token in SYMBOL_KEEP):
                symbols[short] = _num(pub.finding.get("value"))
        blocked_rules = []
        for row in report.get("dispositions") or []:
            if row.get("disposition") != "blocked":
                continue
            art = str(row.get("artifact_id") or "")
            if not any(token in art for token in (
                "sli-worksheet", "schedule1a", "standard-deduction", "line7b",
                "covered-w-st-adjustment", "covered-w-lt-adjustment", "schedule-d.line-1",
                "schedule-d.line-8", "line21",
            )):
                continue
            blocked_rules.append({
                "artifact": art.removeprefix(P + "rule."),
                "code": row.get("code"),
                "missing": [str(item).removeprefix(P) for item in (row.get("missing") or [])][:12],
            })
        return {
            "stop": report.get("stop_reason"),
            "lines": lines,
            "symbols": symbols,
            "questions": questions,
            "titles": titles,
            "asked_on": asked,
            "blocked_rules": blocked_rules[:40],
            "title_mentions": [title for title in (AGE_TITLE, BLIND_TITLE, SPOUSE_AGE, SPOUSE_BLIND) if title in json.dumps(model)],
            "wash_sentence_present": "wash-sale loss adjustment amount" in json.dumps(model),
        }

    h.summarize = summarize


def core_of(h: Any) -> Any:
    return h.Core("v86", "v84", "v84")


def run(h: Any, core: Any, acts: list[dict[str, Any]], run_id: str) -> dict[str, Any]:
    result = h.run(core, acts, run_id)
    if "message" in result:
        result["message"] = scrub(str(result["message"]))
    return result


def complete(h: Any) -> list[dict[str, Any]]:
    """Wage return with the sale families opened and answered, so v86 can publish AGI.

    ``base_return`` alone leaves the code-B, noncovered, and no-1099-B questions
    unanswered on v86, and that blocks total income.
    """
    return h.answer(h.opened(), **h.honest(set()))


def sale_return(h: Any, kind_term: list[tuple[str, str, float, float, float]]) -> list[dict[str, Any]]:
    acts = h.opened()
    kinds = set()
    for kind, term, proceeds, basis, wash in kind_term:
        tag = f"{kind}-{term}-{int(proceeds)}"
        acts = h.sale(acts, kind, term, proceeds=proceeds, basis=basis, wash=wash, tag=tag)
        kinds.add(kind)
    acts = h.answer(acts, **h.honest(kinds))
    return acts


def set_exc1(h: Any, acts: list[dict[str, Any]], only_2a: str, no_losses: str) -> list[dict[str, Any]]:
    acts = h.say(acts, EXC1[0], only_2a, "only2a")
    acts = h.say(acts, EXC1[1], no_losses, "noloss")
    acts = h.say(acts, EXC1[2], "yes", "qof")
    acts = h.say(acts, EXC1[3], "yes", "boxes")
    return acts


def sli_return(h: Any, claimed: str | None) -> list[dict[str, Any]]:
    from tests.helpers import current_core_returns as ccr

    # The current-core helper already answers the worksheet. Override only the
    # one fact this probe varies. Setting the other scope facts again blocks it.
    acts = ccr.add_student_loan_interest_1098e(complete(h), [500.0])
    fact_id = P + "sli-scope.not-claimed-as-dependent"
    if claimed is None:
        return h.strip(acts, fact_id)
    return h.say(acts, fact_id, claimed, "sli-claimed")


def match_hand(measured: dict[str, Any], hand: dict[str, Any]) -> list[str]:
    bad = []
    lines = measured.get("lines") or {}
    symbols = measured.get("symbols") or {}
    for key, expected in hand.items():
        got = lines.get(key, symbols.get(key))
        if isinstance(expected, str) and expected in {"blocked", "guard_inapplicable"}:
            if expected not in str(got):
                bad.append(f"{key}={got!r}")
        elif _num(got) != _num(expected):
            bad.append(f"{key}={got!r}")
    return bad


def contains(measured: dict[str, Any], text: str) -> bool:
    blob = json.dumps(measured.get("questions") or []) + json.dumps(measured.get("titles") or [])
    blob += json.dumps(measured.get("asked_on") or [])
    return text in blob


def history(path: str) -> list[str]:
    out = subprocess.check_output(
        ["git", "log", "--follow", "--format=%h %s", "-3", "--", path],
        cwd=REPO, text=True,
    )
    return [line for line in out.splitlines() if line]


def pinned_rules() -> dict[tuple[str, str], dict[str, Any]]:
    package = json.loads((CONTENT / "package.core-calculations.v86.json").read_text(encoding="utf-8"))
    found = {}
    for member in package["members"]:
        if member.get("role") != "computation":
            continue
        slug = str(member["id"]).removeprefix(P + "rule.")
        version = str(member["version"])
        path = CONTENT / f"rule.{slug}.{version}.json"
        if not path.exists():
            path = CONTENT / f"rule.{slug}.json"
        if path.exists():
            found[(member["id"], version)] = json.loads(path.read_text(encoding="utf-8"))
    return found


READS = {
    P + "rule.f1099b-covered-w-st-adjustment-subtotal": "sums covered-w short-term adjustment members; the closure question's yes is what closes that family",
    P + "rule.f1099b-covered-w-lt-adjustment-subtotal": "sums covered-w long-term adjustment members; the closure question's yes is what closes that family",
    P + "rule.schedule-d-required.conclusion": "all four Exception 1 facts eq yes publishes conclusion no; any no publishes yes",
    P + "rule.form1040-line7b": "conclusion no and no sale activity publishes checked; a recorded sale makes the line guard_inapplicable",
    P + "rule.form1040-standard-deduction": "each true age or blindness boolean is one box; spouse boxes count only for joint, separate, and qualifying surviving spouse; each box adds $2,000 (single or head of household) or $1,600",
    P + "rule.schedule1a-part-v-line-36a": "taxpayer-over-65 true, valid SSN yes, and not married filing separately publishes the $6,000 per-person amount; otherwise 0",
    P + "rule.schedule1a-part-v-line-36b": "spouse-over-65 true, spouse valid SSN yes, and not married filing separately publishes the $6,000 per-person amount; otherwise 0",
    P + "rule.dependents-worksheet-line-1": "counts the four age and blindness booleans",
    P + "rule.sli-worksheet": "not-claimed-as-dependent eq no, or legally-obligated eq no, publishes a legal zero; yes on not-claimed-as-dependent means the filer is not claimed and the deduction proceeds",
}


def question_table(runs: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    rules = pinned_rules()
    citizens = [
        ("closure-mapping.f1099b-covered-w-st-adjustment.v3.json", "closure_question", "wash-st-unclosed", WASH_ST),
        ("closure-mapping.f1099b-covered-w-lt-adjustment.v3.json", "closure_question", "wash-lt-unclosed", WASH_LT),
        ("input-question.exception1-only-box2a-capital-gains.v2.json", "question", "exc1-questions-shown", ONLY_2A),
        ("input-question.exception1-no-capital-losses.v2.json", "question", "exc1-questions-shown", NO_LOSSES),
        ("input-question.exception1-no-qof-deferral.v2.json", "question", "exc1-questions-shown", None),
        ("input-question.exception1-no-boxes-2b-2c-2d.v2.json", "question", "exc1-questions-shown", None),
        ("input-question.sli-scope-not-claimed-as-dependent.v1.json", "question", "sli-question-shown", SLI_Q),
        ("input-question.standard-deduction-can-be-claimed-as-dependent.v1.json", "question", None, None),
    ]
    rows = []
    for filename, field, case_id, expect in citizens:
        body = json.loads((CONTENT / filename).read_text(encoding="utf-8"))
        text = str(body[field])
        shown = None
        asked_on: list[str] = []
        if case_id and case_id in runs:
            measured = runs[case_id]
            if text in json.dumps(measured.get("questions") or []):
                shown = text
            for block in measured.get("asked_on") or []:
                if text in json.dumps(block.get("sentences") or []):
                    asked_on.append(str(block.get("field")))
        fact = body.get("fact_type") or body.get("closure_fact_type") or {}
        mention = text if field == "question" else str((body.get("admits_symbol") or fact.get("id") or ""))
        readers = []
        needles = [str(fact.get("id") or ""), str(body.get("admits_symbol") or "")]
        needles = [needle for needle in needles if needle]
        for (rule_id, version), rule in sorted(rules.items()):
            blob = json.dumps(rule)
            if any(needle and needle in blob for needle in needles):
                readers.append({
                    "id": rule_id,
                    "version": version,
                    "publishes": rule.get("publishes"),
                    "reads": READS.get(rule_id, "mentions this fact or the symbol the closure admits"),
                })
        rows.append({
            "id": body["id"],
            "version": body["version"],
            "schema": body["schema"],
            "text": text,
            "presentation_case": case_id,
            "presentation_text": shown,
            "presentation_matches_citizen": shown == text if case_id else None,
            "citizen_text_expected": expect,
            "citizen_matches_expected": text == expect if expect else None,
            "asked_on": asked_on,
            "fact": fact,
            "admits_symbol": body.get("admits_symbol"),
            "family": body.get("family"),
            "rules": readers,
            "history": history(f"packages/content/tax/2025/{filename}"),
            "mention": mention,
        })
    bundle = json.loads((CONTENT / "core_calculations.bundle.v2.json").read_text(encoding="utf-8"))
    title_run = runs.get("demographic-titles") or {}
    mentions = set(title_run.get("title_mentions") or [])
    for fact in bundle["fact_types"]:
        if fact["id"] not in DEMOGRAPHIC:
            continue
        title = str(fact["title"])
        titles = title_run.get("titles") or []
        shown = next((row["factTypeTitle"] for row in titles if row["factTypeId"] == fact["id"]), None)
        if shown is None and title in mentions:
            shown = title
        readers = []
        for (rule_id, version), rule in sorted(rules.items()):
            if fact["id"] in json.dumps(rule):
                readers.append({
                    "id": rule_id,
                    "version": version,
                    "publishes": rule.get("publishes"),
                    "reads": READS.get(rule_id, "mentions this boolean"),
                })
        rows.append({
            "id": fact["id"],
            "version": fact["version"],
            "schema": fact["schema"],
            "text": title,
            "surface": "fact title, copied onto a source finding as factTypeTitle; optional_default false, so an unanswered fact does not block",
            "presentation_case": "demographic-titles",
            "presentation_text": shown,
            "presentation_matches_citizen": shown == title if shown else False,
            "asked_on": [],
            "rules": readers,
            "history": history("packages/content/tax/2025/core_calculations.bundle.v2.json"),
        })
    return rows


def main() -> None:
    h = load_harness()
    install_summarize(h)
    core = core_of(h)
    built: dict[str, list[dict[str, Any]]] = {}
    built["nosale-base"] = complete(h)
    built["exc1-questions-shown"] = h.strip(h.strip(h.strip(h.strip(
        complete(h), EXC1[0]), EXC1[1]), EXC1[2]), EXC1[3])
    st = [("covered", "st", 1000.0, 800.0, 0.0), ("w", "st", 500.0, 700.0, 200.0)]
    lt = [("covered", "lt", 1000.0, 800.0, 0.0), ("w", "lt", 500.0, 700.0, 200.0)]
    built["wash-st-closed"] = set_exc1(h, sale_return(h, st), "no", "yes")
    built["wash-st-unclosed"] = h.strip(built["wash-st-closed"], P + "f1099b.covered-w-st-adjustment.source-closure")
    built["wash-lt-closed"] = set_exc1(h, sale_return(h, lt), "no", "yes")
    built["wash-lt-unclosed"] = h.strip(built["wash-lt-closed"], P + "f1099b.covered-w-lt-adjustment.source-closure")
    zero = [("covered", "st", 1000.0, 1000.0, 0.0)]
    built["exc1-zero-current-yes"] = set_exc1(h, sale_return(h, zero), "yes", "yes")
    built["exc1-zero-proposed-no"] = set_exc1(h, sale_return(h, zero), "no", "yes")
    built["exc1-zero-both-no"] = set_exc1(h, sale_return(h, zero), "no", "no")
    built["age-true"] = h.say(
        h.say(complete(h), P + "taxpayer-over-65", True, "age"),
        P + "senior-deduction.taxpayer-valid-ssn", "yes", "ssn")
    built["blind-true"] = h.say(complete(h), P + "taxpayer-blind", True, "blind")
    titled = complete(h)
    for fact_id, value, tag in (
        (P + "taxpayer-over-65", True, "age"),
        (P + "taxpayer-blind", True, "blind"),
        (P + "spouse-over-65", True, "spouse-age"),
        (P + "spouse-blind", True, "spouse-blind"),
    ):
        titled = h.say(titled, fact_id, value, tag)
    built["demographic-titles"] = h.say(
        titled, P + "senior-deduction.taxpayer-valid-ssn", "yes", "ssn")
    built["sli-not-claimed-yes"] = sli_return(h, "yes")
    built["sli-claimed-no"] = sli_return(h, "no")
    built["sli-question-shown"] = sli_return(h, None)

    hands: dict[str, dict[str, Any]] = {
        "nosale-base": {"form1040.line-12e": 15750, "schedule1a.line36a-taxpayer": 0},
        "wash-st-closed": {
            "schedule-d.line-1a": 200, "schedule-d.line-1b": 0,
            "f1099b.covered-w-st-adjustment-subtotal": 200,
        },
        "wash-lt-closed": {
            "schedule-d.line-8a": 200, "schedule-d.line-8b": 0,
            "f1099b.covered-w-lt-adjustment-subtotal": 200,
        },
        "wash-st-unclosed": {"schedule-d.line-1b": "blocked"},
        "wash-lt-unclosed": {"schedule-d.line-8b": "blocked"},
        "exc1-zero-current-yes": {"schedule-d.line-1a": 0},
        "exc1-zero-proposed-no": {"schedule-d.line-1a": 0},
        "age-true": {"form1040.line-12e": 17750, "schedule1a.line36a-taxpayer": 6000},
        "blind-true": {"form1040.line-12e": 17750},
        "sli-not-claimed-yes": {"schedule1.line21-sli-deduction": 500},
        "sli-claimed-no": {"schedule1.line21-sli-deduction": 0},
    }
    notes = {
        "nosale-base": "No sale. Current and proposed Exception 1 answers are yes. Age and blindness stay at the default false.",
        "exc1-questions-shown": "The four Exception 1 facts are absent, so the blocked line shows the sentences.",
        "wash-st-closed": "Filer closed the wash-sale adjustment family. Column (h) is 200 on the plain sale and 0 on the wash sale. Column (g) subtotal is the disallowed 200.",
        "wash-st-unclosed": "Current words: a careful filer does not close, because the plain covered sale has no wash-sale adjustment. The family stays open.",
        "wash-lt-closed": "Long-term pair of the closed short-term case.",
        "wash-lt-unclosed": "Long-term pair of the unclosed short-term case.",
        "exc1-zero-current-yes": "Zero-net covered sale, proceeds 1000 basis 1000. Current words: both Exception 1 answers yes.",
        "exc1-zero-proposed-no": "Same sale. Proposed words: only-box-2a no, because a sale that comes out even is still a sale; no-capital-losses stays yes.",
        "exc1-zero-both-no": "Same sale with both Exception 1 answers no, to see whether the loss answer moves a number the gain answer does not.",
        "age-true": "Boolean true and valid SSN yes. This is the January 1, 1961 filer under the proposed born-before-January-2 words, and the February 13, 2025 death under those words.",
        "blind-true": "Blindness boolean true, age left false. Additional standard deduction only.",
        "demographic-titles": "All four age and blindness booleans asserted, so each title can appear as factTypeTitle. Not a hand case.",
        "sli-not-claimed-yes": "Fact yes means not claimed. Current and proposed 'is claiming' words both record this when nobody is claiming the filer. Interest 500.",
        "sli-claimed-no": "Fact no means claimed. The worksheet publishes 0. Interest 500.",
        "sli-question-shown": "The not-claimed fact is absent. The other student-loan scope facts are yes.",
    }
    cases = []
    measured_by_id = {}
    only = {item for item in os.environ.get("QW_ONLY", "").split(",") if item}
    for case_id, acts in built.items():
        if only and case_id not in only:
            continue
        measured = run(h, core, acts, "demo.qw.p0." + case_id)
        measured_by_id[case_id] = measured
        bad = match_hand(measured, hands.get(case_id, {}))
        cases.append({
            "id": case_id,
            "note": notes[case_id],
            "hand": hands.get(case_id, {}),
            "hand_mismatches": bad,
            "measured": measured,
        })
        print(case_id, "OK" if not bad else bad, measured.get("error") or measured.get("refusal") or measured.get("stop"))

    payload = {
        "core": {"package": "v86", "registry": "v84", "release": "v84"},
        "law": "law.json",
        "questions": question_table(measured_by_id),
        "cases": cases,
        "design_map": [
            {
                "id": "wash-mixed-st",
                "runs": ["wash-st-closed", "wash-st-unclosed"],
                "current_truthful": "no, leave the adjustment family open",
                "proposed_truthful": "yes, close it",
                "hand": "line 1a 200, line 1b 0, column (g) 200",
            },
            {
                "id": "wash-mixed-lt",
                "runs": ["wash-lt-closed", "wash-lt-unclosed"],
                "current_truthful": "no, leave the adjustment family open",
                "proposed_truthful": "yes, close it",
                "hand": "line 8a 200, line 8b 0, column (g) 200",
            },
            {
                "id": "exc1-zero-net",
                "runs": ["exc1-zero-current-yes", "exc1-zero-proposed-no", "exc1-zero-both-no"],
                "current_truthful": "only-box-2a yes, no-capital-losses yes",
                "proposed_truthful": "only-box-2a no, no-capital-losses yes",
                "hand": "Schedule D line 1a 0; line 7b not the Exception 1 check; a sale that nets zero is still reported",
            },
            {
                "id": "exc1-no-sale",
                "runs": ["nosale-base", "exc1-questions-shown"],
                "current_truthful": "yes on all four",
                "proposed_truthful": "yes on all four",
                "hand": "line 7b checked when Exception 1 applies and no sale is recorded; standard deduction 15750",
            },
            {
                "id": "age-born-1961-01-01",
                "runs": ["nosale-base", "age-true"],
                "current_truthful": "false under 'over 65'",
                "proposed_truthful": "true under born before January 2, 1961",
                "hand": "false: line 12e 15750 and senior 0; true: line 12e 17750 and senior 6000",
            },
            {
                "id": "age-born-1961-01-02",
                "runs": ["nosale-base"],
                "current_truthful": "false",
                "proposed_truthful": "false",
                "hand": "line 12e 15750 and senior 0",
            },
            {
                "id": "age-died-2025-02-13",
                "runs": ["age-true"],
                "current_truthful": "the title 'over 65' does not say; the instruction checks the box",
                "proposed_truthful": "true",
                "hand": "line 12e 17750 and senior 6000. No death-date fact exists; the return computes the boolean the filer asserts.",
            },
            {
                "id": "age-died-2025-02-12",
                "runs": ["nosale-base"],
                "current_truthful": "false",
                "proposed_truthful": "false",
                "hand": "line 12e 15750 and senior 0",
            },
            {
                "id": "sli-can-be-claimed-but-is-not",
                "runs": ["sli-not-claimed-yes", "sli-claimed-no", "sli-question-shown"],
                "current_truthful": "question no, which records fact yes (not claimed)",
                "proposed_truthful": "question no, same fact yes; the spouse clause does not change this filer",
                "hand": "Schedule 1 line 21 is 500. A claimed filer is 0. 'Can be claimed' would record the wrong fact.",
            },
        ],
    }
    text = json.dumps(payload, indent=2) + "\n"
    for needle in ("/Users/", "/private/", "/tmp/", "/var/"):
        if needle in text:
            raise SystemExit(f"probe output contains {needle}")
    out = HERE / ("probe-debug.json" if only else "probe-output.json")
    out.write_text(text, encoding="utf-8")
    shown = [
        (row["id"].removeprefix(P), row["presentation_matches_citizen"])
        for row in payload["questions"]
    ]
    print(json.dumps({"cases": len(cases), "presentation": shown}, indent=2))


if __name__ == "__main__":
    main()
