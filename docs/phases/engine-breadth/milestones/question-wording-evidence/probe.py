"""P0 probes for question wording on published core v86.

Evidence for docs/phases/engine-breadth/milestones/question-wording.md.
Charter: docs/reviews/question-wording/charter-p0.md.

Every case is one live_coordinate_run of synthetic demo.* findings. Sale
returns answer box 7 and box 4 the way the recorded v83 returns do. Hand
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
V83_TEST = REPO / "tests/test_f1099b_backup_withholding_v83.py"
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
    """Published core v86, or the scratch core prototype.py built when QW_CORE names its core.json."""
    scratch = os.environ.get("QW_CORE")
    if not scratch:
        return h.Core("v86", "v84", "v84")
    body = json.loads(Path(scratch).read_text(encoding="utf-8"))
    return h.Core(body["version"], body["registry"], body["release_version"],
                  content=Path(body["content"]), releases=Path(body["releases"]),
                  loader_from=body.get("loader_from"))


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


def v83_track0() -> Any:
    """The recorded v83 module's Track 0 harness: its box 4 and box 7 answers are the ones v86 replays."""
    name = "qw_p0_v83_test"
    module = sys.modules.get(name)
    if module is None:
        spec = importlib.util.spec_from_file_location(name, V83_TEST)
        assert spec is not None and spec.loader is not None
        module = importlib.util.module_from_spec(spec)
        sys.modules[name] = module
        spec.loader.exec_module(module)
    return module


def sale_return(h: Any, kind_term: list[tuple[str, str, float, float, float]]) -> list[dict[str, Any]]:
    """Sales on the opened wage return, answered as the recorded returns are.

    Box 7 is answered no for each statement and each statement's box 4 amount
    is $0, the way ``return_acts`` and ``with_zero`` in the recorded v83 test
    answer them, so v86 publishes the whole return.
    """
    acts = h.opened()
    kinds = set()
    for kind, term, proceeds, basis, wash in kind_term:
        tag = f"{kind}-{term}-{int(proceeds)}"
        acts = h.sale(acts, kind, term, proceeds=proceeds, basis=basis, wash=wash, tag=tag)
        kinds.add(kind)
    acts = h.answer(acts, **h.honest(kinds))
    test = v83_track0()
    track = test.track0()
    acts = track.sfa_t0.box_answers(acts, track.V82, set(track.sfa_t0.DESIGNS["final"]), "no", "no")
    return test.with_zero(track, acts, core_of(h))


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
    P + "rule.f1099b-covered-w-st-adjustment-subtotal": "when the covered-w short-term adjustment family is closed, sums its members: the column (g) amount of each covered short-term sale with a wash-sale adjustment. A plain covered sale is not in this family",
    P + "rule.f1099b-covered-w-lt-adjustment-subtotal": "the long-term pair of the short-term subtotal",
    P + "rule.closure-check.f1099b-covered-w-st-adjustment": "the closure answer: yes closes the family",
    P + "rule.closure-check.f1099b-covered-w-lt-adjustment": "the closure answer: yes closes the family",
    P + "rule.schedule-d-line1b": "requires the covered-w short-term families closed, including the adjustment family; line 1b is proceeds less basis plus the adjustment subtotal, plus the code B short-term gain",
    P + "rule.schedule-d-line8b": "the long-term pair of line 1b",
    P + "rule.f1099b.covered-w-st-txn.admission-check": "admits a covered short-term wash-sale transaction from its proceeds, basis and adjustment members",
    P + "rule.f1099b.covered-w-lt-txn.admission-check": "admits a covered long-term wash-sale transaction from its proceeds, basis and adjustment members",
    P + "rule.schedule-d-required.conclusion": "all four Exception 1 facts present; all yes publishes conclusion no, any no publishes yes; any absent blocks",
    P + "rule.form1040-line7b": "checked only when the conclusion is no and no sale count or covered proceeds is above 0; any recorded sale makes the line guard_inapplicable",
    P + "rule.form1040-line16": "requires the conclusion; with any recorded sale the guard is true without reading it; with no sale it reads conclusion no to take the Exception 1 path",
    P + "rule.selected-preferential-base": "requires the conclusion; with any recorded sale (or carryover, or nonzero line 1b, 2, 3, 8b, 9, 10) it takes Schedule D lines 15 and 16 and does not read the conclusion",
    P + "rule.form1040-standard-deduction": "can-be-claimed yes takes the dependents worksheet line 4c; otherwise worksheet line 3 plus line 4b",
    P + "rule.dependents-worksheet-line-1": "counts taxpayer_over_65 and taxpayer_blind, and spouse_over_65 and spouse_blind on a joint, separate or qualifying surviving spouse return",
    P + "rule.dependents-worksheet-line-4b": "line 1 count times the additional standard deduction ($2,000 single or head of household, $1,600 otherwise)",
    P + "rule.schedule1a-part-v-line-36a": "taxpayer_over_65 true, not married filing separately, and taxpayer valid SSN yes publishes the line 35 per-person amount; otherwise 0",
    P + "rule.schedule1a-part-v-line-36b": "spouse_over_65 true, not married filing separately, and spouse valid SSN yes publishes the line 35 per-person amount; otherwise 0",
    P + "rule.sli-worksheet": "not-claimed-as-dependent no (or legally-obligated no) publishes a legal $0; yes lets the worksheet compute",
    P + "rule.ctc-filer-gate": "reads can-be-claimed-as-dependent",
    P + "rule.odc-return-gate": "reads can-be-claimed-as-dependent",
}


def _bindings() -> dict[str, list[str]]:
    package = json.loads((CONTENT / "package.core-calculations.v86.json").read_text(encoding="utf-8"))
    found: dict[str, list[str]] = {}
    for row in package.get("input_bindings") or []:
        fact = (row.get("fact_type") or {}).get("id")
        if fact and row.get("symbol") != fact:
            found.setdefault(str(fact), []).append(str(row["symbol"]))
    return found


def _readers(rules: dict[tuple[str, str], dict[str, Any]], needles: list[str]) -> list[dict[str, Any]]:
    readers = []
    for (rule_id, version), rule in sorted(rules.items()):
        blob = json.dumps(rule)
        hit = [needle for needle in needles if f'"{needle}"' in blob]
        if hit:
            readers.append({
                "id": rule_id,
                "version": version,
                "publishes": rule.get("publishes"),
                "names": hit,
                "reads": READS.get(rule_id, "names this input"),
            })
    return readers


def question_table(runs: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    rules = pinned_rules()
    bindings = _bindings()
    citizens = [
        ("closure-mapping.f1099b-covered-w-st-adjustment.v3.json", "closure_question", "wash-st-plain-unclosed", WASH_ST,
         "the closure question of the covered-w short-term adjustment family; asked when a line waits only on that closure"),
        ("closure-mapping.f1099b-covered-w-lt-adjustment.v3.json", "closure_question", "wash-lt-plain-unclosed", WASH_LT,
         "the long-term pair"),
        ("input-question.exception1-only-box2a-capital-gains.v2.json", "question", "exc1-questions-shown", ONLY_2A,
         "every return while the fact is absent"),
        ("input-question.exception1-no-capital-losses.v2.json", "question", "exc1-questions-shown", NO_LOSSES,
         "every return while the fact is absent"),
        ("input-question.exception1-no-qof-deferral.v2.json", "question", "exc1-questions-shown", None,
         "every return while the fact is absent"),
        ("input-question.exception1-no-boxes-2b-2c-2d.v2.json", "question", "exc1-questions-shown", None,
         "every return while the fact is absent"),
        ("input-question.sli-scope-not-claimed-as-dependent.v1.json", "question", "sli-question-shown", SLI_Q,
         "a return with a Form 1098-E while the fact is absent"),
        ("input-question.standard-deduction-can-be-claimed-as-dependent.v1.json", "question", None, None,
         "context only: the 'can be claimed' answer beside the SLI answer"),
    ]
    rows = []
    for filename, field, case_id, expect, who in citizens:
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
        needles = [str(fact.get("id") or ""), str(body.get("admits_symbol") or ""),
                   str((body.get("family") or {}).get("id") or "")]
        needles += bindings.get(str(fact.get("id") or ""), [])
        needles = [needle for needle in needles if needle]
        row = {
            "id": body["id"],
            "version": body["version"],
            "schema": body["schema"],
            "text": text,
            "who_is_asked": who,
            "presentation_case": case_id,
            "presentation_text": shown,
            "presentation_matches_citizen": shown == text if case_id else None,
            "citizen_text_expected": expect,
            "citizen_matches_expected": text == expect if expect else None,
            "asked_on": asked_on,
            "fact": fact,
            "admits_symbol": body.get("admits_symbol"),
            "family": body.get("family"),
            "rules": _readers(rules, needles),
            "history": history(f"packages/content/tax/2025/{filename}"),
        }
        if "exception1" in filename:
            row["conclusion_readers"] = _readers(rules, [P + "schedule-d-required.conclusion"])
        rows.append(row)
    bundle = json.loads((CONTENT / "core_calculations.bundle.v2.json").read_text(encoding="utf-8"))
    title_run = runs.get("demographic-titles") or {}
    for fact in bundle["fact_types"]:
        if fact["id"] not in DEMOGRAPHIC:
            continue
        title = str(fact["title"])
        titles = title_run.get("titles") or []
        shown = next((row["factTypeTitle"] for row in titles if row["factTypeId"] == fact["id"]), None)
        if shown is None and title in (title_run.get("title_mentions") or []):
            shown = title
        needles = [fact["id"], *bindings.get(fact["id"], [])]
        rows.append({
            "id": fact["id"],
            "version": fact["version"],
            "schema": fact["schema"],
            "text": title,
            "who_is_asked": "nobody: optional_default false, so an absent fact never blocks and no input-question names it",
            "surface": "fact title in the vocabulary bundle; no presentation text measured",
            "presentation_case": "demographic-titles",
            "presentation_text": shown,
            "presentation_matches_citizen": shown == title if shown else False,
            "asked_on": [],
            "rules": _readers(rules, needles),
            "history": history("packages/content/tax/2025/core_calculations.bundle.v2.json"),
        })
    return rows


MFJ = "married_filing_jointly"


def write_scratch(core: Any, cases: list[dict[str, Any]]) -> None:
    """The same cases on scratch core v87: hand values, and which proposed words the page shows."""
    words = json.loads((HERE / "prototype-build.json").read_text(encoding="utf-8"))["words"]
    sentences = [words["wash_st"], words["wash_lt"], words["only_box2a"], words["sli"]]
    old = [WASH_ST, WASH_LT, ONLY_2A, SLI_Q]
    blob = json.dumps([case["measured"].get("questions") for case in cases])
    shown = {
        "proposed_shown": {sentence: sentence in blob for sentence in sentences},
        "current_shown": {sentence: sentence in blob for sentence in old},
        "titles_shown": {
            fact: title in json.dumps([case["measured"] for case in cases])
            for fact, title in words["titles"].items()
        },
    }
    payload = {
        "core": {"package": core.version, "registry": core.registry, "release": core.release_version,
                 "built_by": "prototype.py"},
        "words": shown,
        "cases": [
            {"id": case["id"], "hand": case["hand"], "hand_mismatches": case["hand_mismatches"],
             "lines": case["measured"].get("lines"), "questions": case["measured"].get("questions"),
             "error": case["measured"].get("error")}
            for case in cases
        ],
    }
    text = json.dumps(payload, indent=2) + "\n"
    for needle in ("/Users/", "/private/", "/tmp/", "/var/"):
        if needle in text:
            raise SystemExit(f"probe output contains {needle}")
    (HERE / "probe-v87-output.json").write_text(text, encoding="utf-8")
    print(json.dumps(shown, indent=2))


def mfj(h: Any, acts: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return h.say(acts, P + "filing-status", MFJ, "fs")


def main() -> None:
    h = load_harness()
    install_summarize(h)
    core = core_of(h)
    built: dict[str, list[dict[str, Any]]] = {}
    built["nosale-base"] = complete(h)
    built["exc1-questions-shown"] = h.strip(h.strip(h.strip(h.strip(
        complete(h), EXC1[0]), EXC1[1]), EXC1[2]), EXC1[3])
    for term, line in (("st", "1"), ("lt", "8")):
        plain = [("covered", term, 1000.0, 800.0, 0.0)]
        mixed = plain + [("w", term, 500.0, 700.0, 200.0)]
        closure = P + f"f1099b.covered-w-{term}-adjustment.source-closure"
        built[f"wash-{term}-plain-closed"] = set_exc1(h, sale_return(h, plain), "no", "yes")
        built[f"wash-{term}-plain-unclosed"] = h.strip(built[f"wash-{term}-plain-closed"], closure)
        built[f"wash-{term}-closed"] = set_exc1(h, sale_return(h, mixed), "no", "yes")
        built[f"wash-{term}-unclosed"] = h.strip(built[f"wash-{term}-closed"], closure)
    zero = [("covered", "st", 1000.0, 1000.0, 0.0)]
    built["exc1-zero-current-yes"] = set_exc1(h, sale_return(h, zero), "yes", "yes")
    built["exc1-zero-proposed-no"] = set_exc1(h, sale_return(h, zero), "no", "yes")
    built["exc1-zero-both-no"] = set_exc1(h, sale_return(h, zero), "no", "no")
    built["exc1-zero-questions-shown"] = h.strip(h.strip(h.strip(h.strip(
        sale_return(h, zero), EXC1[0]), EXC1[1]), EXC1[2]), EXC1[3])
    built["age-true"] = h.say(
        h.say(complete(h), P + "taxpayer-over-65", True, "age"),
        P + "senior-deduction.taxpayer-valid-ssn", "yes", "ssn")
    built["blind-true"] = h.say(complete(h), P + "taxpayer-blind", True, "blind")
    built["mfj-base"] = mfj(h, complete(h))
    built["mfj-spouse-age-true"] = h.say(
        h.say(mfj(h, complete(h)), P + "spouse-over-65", True, "spouse-age"),
        P + "senior-deduction.spouse-valid-ssn", "yes", "spouse-ssn")
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
    built["sli-can-be-claimed-not-claimed"] = h.say(
        sli_return(h, "yes"), P + "standard-deduction.can-be-claimed-as-dependent", "yes", "can-claim")
    built["sli-mfj-not-claimed-yes"] = mfj(h, sli_return(h, "yes"))
    built["sli-mfj-claimed-no"] = mfj(h, sli_return(h, "no"))

    single_sale = {"form1040.line-7a": 200, "form1040.line-15": 34450, "form1040.line-16": 3899}
    hands: dict[str, dict[str, Any]] = {
        "nosale-base": {"form1040.line-12e": 15750, "form1040.line-15": 34250, "form1040.line-16": 3875,
                        "form1040.line-7a": 0, "schedule1a.line36a-taxpayer": 0},
        "wash-st-plain-closed": {"schedule-d.line-1a": 200, "schedule-d.line-1b": 0, **single_sale},
        "wash-st-plain-unclosed": {"schedule-d.line-1b": "blocked"},
        "wash-st-closed": {"schedule-d.line-1a": 200, "schedule-d.line-1b": 0, "schedule-d.line-7": 200,
                           "f1099b.covered-w-st-adjustment-subtotal": 200, **single_sale},
        "wash-st-unclosed": {"schedule-d.line-1b": "blocked"},
        "wash-lt-plain-closed": {"schedule-d.line-8a": 200, "schedule-d.line-8b": 0, "form1040.line-7a": 200,
                                 "form1040.line-15": 34450, "form1040.line-16": 3875},
        "wash-lt-plain-unclosed": {"schedule-d.line-8b": "blocked"},
        "wash-lt-closed": {"schedule-d.line-8a": 200, "schedule-d.line-8b": 0, "schedule-d.line-15": 200,
                           "f1099b.covered-w-lt-adjustment-subtotal": 200, "form1040.line-7a": 200,
                           "form1040.line-15": 34450, "form1040.line-16": 3875},
        "wash-lt-unclosed": {"schedule-d.line-8b": "blocked"},
        "exc1-zero-current-yes": {"schedule-d.line-1a": 0, "form1040.line-7a": 0, "form1040.line-15": 34250,
                                  "form1040.line-16": 3875},
        "exc1-zero-proposed-no": {"schedule-d.line-1a": 0, "form1040.line-7a": 0, "form1040.line-15": 34250,
                                  "form1040.line-16": 3875},
        "exc1-zero-both-no": {"schedule-d.line-1a": 0, "form1040.line-7a": 0, "form1040.line-15": 34250,
                              "form1040.line-16": 3875},
        "age-true": {"form1040.line-12e": 17750, "schedule1a.line36a-taxpayer": 6000, "form1040.line-15": 26250,
                     "form1040.line-16": 2915},
        "blind-true": {"form1040.line-12e": 17750, "form1040.line-15": 32250, "form1040.line-16": 3635},
        "mfj-base": {"form1040.line-12e": 31500, "schedule1a.line36b-spouse": 0, "form1040.line-15": 18500,
                     "form1040.line-16": 1853},
        "mfj-spouse-age-true": {"form1040.line-12e": 33100, "schedule1a.line36b-spouse": 6000,
                                "form1040.line-15": 10900, "form1040.line-16": 1093},
        "sli-not-claimed-yes": {"schedule1.line21-sli-deduction": 500, "form1040.line-15": 33750,
                                "form1040.line-16": 3815},
        "sli-claimed-no": {"schedule1.line21-sli-deduction": 0, "form1040.line-15": 34250},
        "sli-can-be-claimed-not-claimed": {"schedule1.line21-sli-deduction": 500, "form1040.line-12e": 15750,
                                           "form1040.line-15": 33750, "form1040.line-16": 3815},
        "sli-mfj-not-claimed-yes": {"schedule1.line21-sli-deduction": 500, "form1040.line-15": 18000,
                                    "form1040.line-16": 1803},
        "sli-mfj-claimed-no": {"schedule1.line21-sli-deduction": 0, "form1040.line-15": 18500,
                               "form1040.line-16": 1853},
    }
    notes = {
        "nosale-base": "Single, wages 50,000, no sale. Exception 1 answered yes four times. Age and blindness at the default false.",
        "exc1-questions-shown": "No sale, the four Exception 1 facts absent: the page shows their questions.",
        "wash-st-plain-closed": "One covered short-term sale, proceeds 1,000 basis 800, no wash sale. Adjustment family closed (the proposed truthful yes).",
        "wash-st-plain-unclosed": "Same sale, adjustment closure absent: the page shows the current question. Read literally, the filer has recorded no wash-sale adjustment for this sale, so a careful no leaves the family open.",
        "wash-st-closed": "The plain sale plus a covered wash sale (proceeds 500, basis 700, box 1g 200). Family closed.",
        "wash-st-unclosed": "Same two sales, adjustment closure absent. The wash transaction's admission check also blocks (DEPENDENCY_INVALID), which has no question, so line 1b shows no question at all.",
        "wash-lt-plain-closed": "Long-term pair of wash-st-plain-closed.",
        "wash-lt-plain-unclosed": "Long-term pair of wash-st-plain-unclosed.",
        "wash-lt-closed": "Long-term pair of wash-st-closed.",
        "wash-lt-unclosed": "Long-term pair of wash-st-unclosed.",
        "exc1-zero-current-yes": "Covered short-term sale, proceeds 1,000 basis 1,000. Current words read literally: no gain other than box 2a (yes), no loss (yes).",
        "exc1-zero-proposed-no": "Same sale. Proposed words: only-box-2a no, because the filer sold property; no-capital-losses yes.",
        "exc1-zero-both-no": "Same sale with both answers no, to show neither answer moves a number once a sale is recorded.",
        "exc1-zero-questions-shown": "Same sale, the four Exception 1 facts absent: they are still asked beside a sale.",
        "age-true": "Taxpayer boolean true, valid SSN yes. The truthful value for a filer born January 1, 1961 under the instruction.",
        "blind-true": "Taxpayer blindness true, age false.",
        "mfj-base": "Married filing jointly, same wages. Spouse age false: the instruction's value for a spouse born February 14, 1960 who died February 12, 2025, and for a spouse born January 2, 1961.",
        "mfj-spouse-age-true": "Joint, spouse age true, spouse valid SSN yes: the instruction's value for a spouse born February 14, 1960 who died February 13, 2025, and for a spouse born January 1, 1961.",
        "demographic-titles": "All four booleans true, to look for the titles on the page. Not a hand case.",
        "sli-not-claimed-yes": "Single, Form 1098-E interest 500; fact yes (nobody claims the filer).",
        "sli-claimed-no": "Same; fact no (the filer is claimed).",
        "sli-question-shown": "Same; fact absent: the page shows the question.",
        "sli-can-be-claimed-not-claimed": "The filer can be claimed (standard-deduction fact yes) but nobody claims them (SLI fact yes).",
        "sli-mfj-not-claimed-yes": "Joint, interest 500, SLI fact yes. This is what the current words record for a joint filer whose spouse, not the filer, is claimed.",
        "sli-mfj-claimed-no": "Joint, interest 500, SLI fact no. What the proposed words record when the spouse is claimed.",
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

    if os.environ.get("QW_CORE"):
        write_scratch(core, cases)
        return
    payload = {
        "core": {"package": "v86", "registry": "v84", "release": "v84"},
        "law": "law.json",
        "hand_basis": (
            "2025 Form 1040 instructions: standard deduction 15,750 single and 31,500 joint; additional 2,000 single "
            "and 1,600 joint per box; senior deduction 6,000 per qualifying person below the MAGI threshold; tax from "
            "the 2025 Tax Table (midpoint of the 50-dollar row) and the Qualified Dividends and Capital Gain Tax "
            "Worksheet for a long-term gain; Form 8949 column (h) = proceeds - basis + column (g)."
        ),
        "questions": question_table(measured_by_id),
        "cases": cases,
        "design_map": [
            {
                "id": "wash-plain-sale",
                "runs": ["wash-st-plain-unclosed", "wash-st-plain-closed", "wash-lt-plain-unclosed", "wash-lt-plain-closed"],
                "current_truthful": "no: no wash-sale adjustment was recorded for this sale, so the line stays blocked on the question",
                "proposed_truthful": "yes: every covered sale with a wash-sale adjustment (there is none) has its amount recorded",
                "hand": "short-term: line 1a 200, line 1b 0, Form 1040 line 7a 200, line 16 3,899; long-term: line 8a 200, line 8b 0, line 16 3,875",
            },
            {
                "id": "wash-mixed",
                "runs": ["wash-st-unclosed", "wash-st-closed", "wash-lt-unclosed", "wash-lt-closed"],
                "current_truthful": "no for the same reason (the plain sale has no adjustment); the page shows no question here",
                "proposed_truthful": "yes once the 200 is recorded",
                "hand": "line 1a 200, line 1b 0 (500 - 700 + 200), column (g) 200, Form 1040 line 7a 200",
            },
            {
                "id": "exc1-zero-net",
                "runs": ["exc1-zero-questions-shown", "exc1-zero-current-yes", "exc1-zero-proposed-no", "exc1-zero-both-no"],
                "current_truthful": "only-box-2a yes, no-capital-losses yes (no gain, no loss)",
                "proposed_truthful": "only-box-2a no (the filer sold property), no-capital-losses yes",
                "hand": "Schedule D line 1a 0, Form 1040 line 7a 0, line 15 34,250, line 16 3,875 whatever the answers; Exception 1 does not apply because a sale is reported on Form 8949 and Schedule D",
            },
            {
                "id": "exc1-no-sale",
                "runs": ["exc1-questions-shown", "nosale-base"],
                "current_truthful": "yes on all four",
                "proposed_truthful": "yes on all four",
                "hand": "line 7b checked; standard deduction 15,750; line 16 3,875",
            },
            {
                "id": "age-born-1961-01-01",
                "runs": ["nosale-base", "age-true"],
                "current_truthful": "false under 'over 65 years of age for 2025' (the filer is 64 on December 31, 2025)",
                "proposed_truthful": "true (born before January 2, 1961)",
                "hand": "true: line 12e 17,750, senior 6,000, line 16 2,915",
            },
            {
                "id": "age-born-1961-01-02",
                "runs": ["nosale-base"],
                "current_truthful": "false",
                "proposed_truthful": "false",
                "hand": "line 12e 15,750, senior 0",
            },
            {
                "id": "age-spouse-died-2025-02-13",
                "runs": ["mfj-base", "mfj-spouse-age-true"],
                "current_truthful": "unclear: the title does not say how a death in 2025 counts",
                "proposed_truthful": "true (age 65 the day before the 65th birthday)",
                "hand": "line 12e 33,100, senior 6,000, line 16 1,093",
            },
            {
                "id": "age-spouse-died-2025-02-12",
                "runs": ["mfj-base", "mfj-spouse-age-true"],
                "current_truthful": "unclear; a filer reading 'over 65 for 2025' of a spouse born in 1960 may answer true",
                "proposed_truthful": "false",
                "hand": "line 12e 31,500, senior 0, line 16 1,853; true would give 33,100, 6,000 and 1,093",
            },
            {
                "id": "sli-can-be-claimed-but-is-not",
                "runs": ["sli-can-be-claimed-not-claimed", "sli-not-claimed-yes", "sli-claimed-no", "sli-question-shown"],
                "current_truthful": "question no, which records fact yes (not claimed)",
                "proposed_truthful": "question no, the same fact yes",
                "hand": "Schedule 1 line 21 500, line 12e 15,750. A filer who is claimed: 0.",
            },
            {
                "id": "sli-joint-spouse-claimed",
                "runs": ["sli-mfj-not-claimed-yes", "sli-mfj-claimed-no"],
                "current_truthful": "question no (asks about 'you' only), which records fact yes and deducts 500",
                "proposed_truthful": "question yes, which records fact no and deducts 0",
                "hand": "0: Form 1040 line 21 requires that you, or your spouse if filing jointly, aren't claimed. The case is narrow: a joint filer is generally a dependent only when the joint return is filed only to claim a refund.",
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
