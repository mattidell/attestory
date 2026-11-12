"""P0 probes for age and blindness being asked: published v86, scratch v87 and scratch v88.

Evidence for docs/phases/engine-breadth/milestones/age-blindness-asked.md.
Charter: docs/reviews/age-blindness-asked/charter-p0.md.

Every case is one live_coordinate_run of synthetic demo.* findings on the
question-wording harness's wage return (wages 50,000, 4,500 withheld, every
other question answered). Each case is run three ways where they differ:

- ``unanswered``: none of the four facts is recorded (how every recorded
  return stands today);
- ``truthful``: the facts recorded as a filer in the case's circumstances
  answers the proposed v88 questions (law.json);
- on v88 only, ``partial`` variants that answer some facts and leave others.

Hand values come from the 2025 instructions (law.json), never from a run.
v87 runs re-adopt question-wording's three bundle successors. v88 runs
re-adopt the same two small bundles and vocabulary bundle v4. Decision 9
puts the separate-return condition on its own fact, answered on v88 only.
The scratch cores come from prototype.py.

    python3 probe.py <scratch>/core-v87.json <scratch>/core-v88.json
"""

from __future__ import annotations

import copy
import importlib.util
import json
import re
import sys
import tempfile
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

QW = REPO / "docs/phases/engine-breadth/milestones/question-wording-evidence"
P = "tax.us.2025."
Acts = list[dict[str, Any]]

AGE, BLIND, S_AGE, S_BLIND = (P + "taxpayer-over-65", P + "taxpayer-blind", P + "spouse-over-65", P + "spouse-blind")
COND = P + "standard-deduction.spouse-separate-condition"
FOUR = (AGE, BLIND, S_AGE, S_BLIND)
SSN, S_SSN = P + "senior-deduction.taxpayer-valid-ssn", P + "senior-deduction.spouse-valid-ssn"
DEPENDENT = P + "standard-deduction.can-be-claimed-as-dependent"
STATUS = P + "filing-status"
SUCCESSOR_BUNDLES = ("exception1.bundle.v2.json", "sli-scope.bundle.v2.json", "core_calculations.bundle.v3.json")

WATCH = ("form1040.line-12e", "form1040.line-13b", "form1040.line-14", "form1040.line-15",
         "form1040.line-16", "form1040.line-24", "form1040.line-33", "form1040.line-34", "form1040.line-37")
SYMBOLS = (
    "dependents-worksheet.line1-box-count", "dependents-worksheet.line3", "dependents-worksheet.line4a",
    "dependents-worksheet.line4b", "dependents-worksheet.line4c", "schedule1a.line36a-taxpayer",
    "schedule1a.line36b-spouse", "schedule1a.line37-enhanced-deduction-total", "deductions.line-12e",
)


def _module(name: str, path: Path) -> Any:
    module = sys.modules.get(name)
    if module is None:
        spec = importlib.util.spec_from_file_location(name, path)
        assert spec is not None and spec.loader is not None
        module = importlib.util.module_from_spec(spec)
        sys.modules[name] = module
        spec.loader.exec_module(module)
    return module


def qw_probe() -> Any:
    return _module("aba_p0_qw_probe", QW / "probe.py")


def harness() -> Any:
    return qw_probe().load_harness()


def core(path: Path | None) -> Any:
    h = harness()
    if path is None:
        return h.Core("v86", "v84", "v84")
    body = json.loads(path.read_text(encoding="utf-8"))
    return h.Core(body["version"], body["registry"], body["release_version"],
                  content=Path(body["content"]), releases=Path(body["releases"]),
                  loader_from=body.get("loader_from"))


def scrub(text: str) -> str:
    text = text.replace(str(REPO), ".")
    return re.sub(r"/(?:Users|private|tmp|var|opt)/\S+", "<path>", text)


def _num(value: Any) -> Any:
    if isinstance(value, str):
        try:
            number = float(value)
        except ValueError:
            return value
        return int(number) if number.is_integer() else number
    if isinstance(value, float) and value.is_integer():
        return int(value)
    return value


def bundles_for(c: Any) -> tuple[str, ...]:
    """v88's package member is vocabulary v4, which already carries v3's other titles."""
    if c.version == "v88":
        return ("exception1.bundle.v2.json", "sli-scope.bundle.v2.json", "core_calculations.bundle.v4.json")
    return SUCCESSOR_BUNDLES


def _condition_assertion_index(acts: Acts) -> int | None:
    """Index of the first assertion of the separate-return condition fact."""
    prefix = COND + "|"
    for index, act in enumerate(acts):
        if act.get("kind") != "assertion":
            continue
        payload = act.get("payload")
        finding = payload.get("finding") if isinstance(payload, dict) else None
        if isinstance(finding, dict) and str(finding.get("fact_id", "")).startswith(prefix):
            return index
    return None


def readopt(acts: Acts, c: Any) -> Acts:
    """Re-adopt the successor bundles.

    A return that does not assert the condition fact keeps every adoption at the
    end of the list, which is how the prior v88 pins were measured. An assertion
    of that fact is validated against fact types adopted so far, and the fact
    exists only in vocabulary v4, so that one adoption is inserted immediately
    before the assertion. The other bundles stay at the end.
    """
    if c.version == "v86":
        return acts
    h = harness()
    out = copy.deepcopy(acts)
    names = list(bundles_for(c))
    vocabulary = "core_calculations.bundle.v4.json"
    if c.version == "v88" and vocabulary in names:
        at = _condition_assertion_index(out)
        if at is not None:
            holder: Acts = []
            h._add(holder, "bundle-adoption", {
                "bundle": json.loads((c.content / vocabulary).read_text(encoding="utf-8"))})
            out = out[:at] + holder + out[at:]
            names.remove(vocabulary)
    for name in names:
        h._add(out, "bundle-adoption", {"bundle": json.loads((c.content / name).read_text(encoding="utf-8"))})
    return h.renumber(out)


def summarize(outcome: Any) -> dict[str, Any]:
    if outcome.refusal is not None:
        return {"outcome": "refused", "reason": outcome.refusal.reason,
                "detail": scrub(str(outcome.refusal.detail))[:300]}
    report = json.loads(outcome.output_path.read_text(encoding="utf-8"))
    model = json.loads(outcome.presentation_path.read_text(encoding="utf-8"))
    lines: dict[str, Any] = {}
    asked: dict[str, list[str]] = {}
    blocked_fields: list[str] = []
    for section in model.get("sections") or []:
        field_id = str((section.get("field") or {}).get("id") or "").removeprefix(P)
        resolved = section.get("resolved") or {}
        disposition = str(resolved.get("disposition"))
        sentences = [scrub(str(r.get("sentence") or "").strip()) for r in resolved.get("reasons") or []
                     if isinstance(r, dict) and str(r.get("sentence") or "").strip()]
        if "blocked" in disposition:
            blocked_fields.append(field_id)
            if sentences:
                asked[field_id] = sentences
        if field_id in WATCH:
            value = resolved.get("value")
            lines[field_id] = disposition if value is None or "blocked" in disposition else _num(value)
    symbols = {}
    for pub in outcome.publications or ():
        short = str(pub.finding.get("symbol") or "").removeprefix(P)
        if short in SYMBOLS:
            symbols[short] = _num(pub.finding.get("value"))
    blocked_rules = []
    for row in report.get("dispositions") or []:
        art = str(row.get("artifact_id") or "")
        if row.get("disposition") == "blocked" and any(
                token in art for token in ("dependents-worksheet", "schedule1a-part-v", "standard-deduction")):
            blocked_rules.append({"rule": art.removeprefix(P + "rule."), "code": row.get("code"),
                                  "missing": [str(m).removeprefix(P) for m in row.get("missing") or []]})
    questions = sorted({s for sentences in asked.values() for s in sentences})
    return {
        "outcome": "success",
        "stop": report.get("stop_reason"),
        "lines": lines,
        "symbols": symbols,
        "questions": questions,
        "blocked_field_count": len(blocked_fields),
        "asked_on": sorted(asked),
        "blocked_rules": blocked_rules,
    }


def execute(c: Any, acts: Acts, run_id: str) -> dict[str, Any]:
    h = harness()
    surface = c.surface()
    with h.loader_entries(c):
        try:
            finished = h._handover(h._finish(readopt(acts, c), package_path=c.package_path,
                                             package_version=c.version, release_path=c.release_path,
                                             release_version=c.release_version, note=run_id),
                                   surface=surface, reconfirm=True)
            with tempfile.TemporaryDirectory() as tmp:
                outcome = h.live_coordinate_run(
                    h.WorkspaceCapability(Path(tmp) / "L"), repo_root=REPO, authoritative_acts=finished,
                    workspace_revision=len(finished), run_scope={"jurisdiction": "us", "year": h.YEAR},
                    scope_user=h.ccr.USER, request={"schema": "run-request.v1"}, run_id=run_id,
                    governance_pins=[], surface=surface, output_name="out.json")
                return summarize(outcome)
        except Exception as exc:  # noqa: BLE001 - a rejected act list is a result
            return {"outcome": "error", "error": type(exc).__name__, "message": scrub(str(exc))[:300]}


# ---- cases -------------------------------------------------------------------------------


def base(status: str = "single") -> Acts:
    p, h = qw_probe(), harness()
    acts = h.say(p.complete(h), P + "f1099b.no-sale-box4-present", "no", "box4-present")
    if status != "single":
        acts = h.say(acts, STATUS, status, "fs")
    return acts


def answer(acts: Acts, answers: dict[str, Any]) -> Acts:
    h = harness()
    for fact, value in answers.items():
        acts = h.say(acts, fact, value, fact.removeprefix(P).replace(".", "-"))
    return acts


MFJ, MFS, HOH, QSS = "married_filing_jointly", "married_filing_separately", "head_of_household", "qualifying_surviving_spouse"

# Each case: circumstances, filing status, extra answers that are not one of the
# four facts, the four facts as the proposed questions are truthfully answered,
# and the hand values from the instructions for those answers.
CASES: list[dict[str, Any]] = [
    {
        "id": "single-born-1961-01-01",
        "says": "Single; born January 1, 1961; not blind. Age 65 is reached the day before the 65th birthday (December 31, 2025).",
        "status": "single", "extra": {SSN: "yes"},
        "truthful": {AGE: True, BLIND: False},
        "hand": {"form1040.line-12e": 17750, "schedule1a.line36a-taxpayer": 6000,
                 "form1040.line-15": 26250, "form1040.line-16": 2915},
        "basis": "chart: single, 1 box 17,750; Schedule 1-A Part V 6,000 (MAGI 50,000 is under 75,000); 50,000 - 17,750 - 6,000 = 26,250; Tax Table 2,915",
    },
    {
        "id": "single-born-1961-01-02",
        "says": "Single; born January 2, 1961; not blind. Not 65 until January 1, 2026.",
        "status": "single", "extra": {},
        "truthful": {AGE: False, BLIND: False},
        "hand": {"form1040.line-12e": 15750, "schedule1a.line36a-taxpayer": 0,
                 "form1040.line-15": 34250, "form1040.line-16": 3875},
        "basis": "standard deduction 15,750; no senior deduction; Tax Table 3,875",
    },
    {
        "id": "single-born-1960-01-01-blind",
        "says": "Single; born January 1, 1960; blind (certified 20/200).",
        "status": "single", "extra": {SSN: "yes"},
        "truthful": {AGE: True, BLIND: True},
        "hand": {"form1040.line-12e": 19750, "schedule1a.line36a-taxpayer": 6000,
                 "form1040.line-15": 24250, "form1040.line-16": 2675},
        "basis": "chart: single, 2 boxes 19,750; senior 6,000; 50,000 - 19,750 - 6,000 = 24,250; Tax Table (24,250-24,300 row) 2,675",
    },
    {
        "id": "joint-one-spouse-65",
        "says": "Joint; taxpayer born March 3, 1958; spouse born May 5, 1970; neither blind.",
        "status": MFJ, "extra": {SSN: "yes"},
        "truthful": {AGE: True, BLIND: False, S_AGE: False, S_BLIND: False},
        "hand": {"form1040.line-12e": 33100, "schedule1a.line36a-taxpayer": 6000,
                 "schedule1a.line36b-spouse": 0, "form1040.line-15": 10900, "form1040.line-16": 1093},
        "basis": "chart: joint, 1 box 33,100; senior 6,000 for the taxpayer only (MAGI under 150,000); 50,000 - 33,100 - 6,000 = 10,900; Tax Table 1,093",
    },
    {
        "id": "joint-spouse-died-2025-02-12",
        "says": "Joint; taxpayer born May 5, 1970; spouse born February 14, 1960, died February 12, 2025 (not yet 65).",
        "status": MFJ, "extra": {},
        "truthful": {AGE: False, BLIND: False, S_AGE: False, S_BLIND: False},
        "hand": {"form1040.line-12e": 31500, "schedule1a.line36b-spouse": 0,
                 "form1040.line-15": 18500, "form1040.line-16": 1853},
        "basis": "line 12d death example: don't check the box; 31,500; no senior deduction; Tax Table 1,853",
    },
    {
        "id": "joint-spouse-died-2025-02-13",
        "says": "Joint; taxpayer born May 5, 1970; spouse born February 14, 1960, died February 13, 2025 (age 65 at death).",
        "status": MFJ, "extra": {S_SSN: "yes"},
        "truthful": {AGE: False, BLIND: False, S_AGE: True, S_BLIND: False},
        "hand": {"form1040.line-12e": 33100, "schedule1a.line36b-spouse": 6000,
                 "form1040.line-15": 10900, "form1040.line-16": 1093},
        "basis": "line 12d death example: check the spouse box; 33,100; senior 6,000 for the spouse; Tax Table 1,093",
    },
    {
        "id": "dependent-65",
        "says": "Single; someone can claim the filer as a dependent; born March 3, 1950; not blind.",
        "status": "single", "extra": {DEPENDENT: "yes", SSN: "yes"},
        "truthful": {AGE: True, BLIND: False},
        "hand": {"dependents-worksheet.line1-box-count": 1, "dependents-worksheet.line4b": 2000,
                 "form1040.line-12e": 17750, "schedule1a.line36a-taxpayer": 6000,
                 "form1040.line-15": 26250, "form1040.line-16": 2915},
        "basis": "dependents worksheet: line 2 50,450, line 3 15,750, 4a 15,750, 4b 1 x 2,000, 4c 17,750; senior 6,000 (Schedule 1-A Part V names no dependent exclusion); Tax Table 2,915",
    },
    {
        "id": "dependent-blind",
        "says": "Single; someone can claim the filer as a dependent; born 1990; blind.",
        "status": "single", "extra": {DEPENDENT: "yes"},
        "truthful": {AGE: False, BLIND: True},
        "hand": {"dependents-worksheet.line1-box-count": 1, "dependents-worksheet.line4b": 2000,
                 "form1040.line-12e": 17750, "schedule1a.line36a-taxpayer": 0,
                 "form1040.line-15": 32250, "form1040.line-16": 3635},
        "basis": "dependents worksheet 4a 15,750 + 4b 2,000 = 17,750; no senior deduction; Tax Table 3,635",
    },
    {
        "id": "separate-spouse-qualifies",
        "says": "Married filing separately; taxpayer born 1970; spouse born 1955 with no income, not filing, and not claimable as a dependent.",
        "status": MFS, "extra": {},
        "truthful": {AGE: False, BLIND: False, S_AGE: True, S_BLIND: False},
        "v88_only": {COND: True},
        "hand": {"form1040.line-12e": 17350, "schedule1a.line36b-spouse": 0,
                 "form1040.line-15": 32650, "form1040.line-16": 3683},
        "basis": "chart: married filing separately, 1 box 17,350 (footnote: spouse with no income, not filing, not claimable); no senior deduction on a separate return; Tax Table 3,683",
    },
    {
        "id": "head-of-household",
        "says": "Head of household; taxpayer born 1970, not blind. The proposed core asks only the taxpayer's two questions.",
        "status": HOH, "extra": {},
        "truthful": {AGE: False, BLIND: False},
        "hand": {"form1040.line-12e": 23625},
        "basis": "standard deduction 23,625; line 12d: no spouse boxes on head of household",
    },
    {
        "id": "qss-spouse-born-1955",
        "says": "Qualifying surviving spouse; taxpayer born 1970; the spouse (died 2024) was born 1955. The chart counts at most 2 boxes for this status: only the taxpayer's.",
        "status": QSS, "extra": {},
        "truthful": {AGE: False, BLIND: False},
        "recorded_on_v86": {AGE: False, BLIND: False, S_AGE: True, S_BLIND: False},
        "hand": {"form1040.line-12e": 31500},
        "basis": "chart: qualifying surviving spouse rows are 1 and 2 boxes only; with no taxpayer box the standard deduction is 31,500",
    },
]


def run_all(c87: Any, c88: Any) -> dict[str, Any]:
    c86 = core(None)
    cores = {"v86": c86, "v87": c87, "v88": c88}
    rows = []
    for case in CASES:
        acts0 = answer(base(case["status"]), case["extra"])
        variants: dict[str, tuple[Acts, tuple[str, ...]]] = {
            "unanswered": (acts0, ("v86", "v87", "v88")),
            "truthful": (answer(acts0, case["truthful"]), ("v86", "v87", "v88")),
        }
        if "recorded_on_v86" in case:
            variants["spouse-recorded"] = (answer(acts0, case["recorded_on_v86"]), ("v86", "v88"))
        if case["status"] in (MFJ, MFS):
            taxpayer_only = {k: v for k, v in case["truthful"].items() if k in (AGE, BLIND)}
            variants["taxpayer-only"] = (answer(acts0, taxpayer_only), ("v88",))
        if case["status"] == "single" and case["truthful"].get(AGE):
            variants["age-only"] = (answer(acts0, {AGE: True}), ("v88",))
        measured: dict[str, dict[str, Any]] = {}
        for variant, (acts, names) in variants.items():
            for name in names:
                run_acts = acts
                if name == "v88" and variant == "truthful" and case.get("v88_only"):
                    run_acts = answer(acts, case["v88_only"])
                run_id = f"demo.aba.p0.{name}.{case['id']}.{variant}"
                measured[f"{variant}@{name}"] = execute(cores[name], run_acts, run_id)
                result = measured[f"{variant}@{name}"]
                print(case["id"], variant, name, result.get("lines", {}).get("form1040.line-12e"),
                      result.get("error") or "", flush=True)
        rows.append({**{k: v for k, v in case.items() if k not in ("extra", "truthful", "recorded_on_v86", "v88_only")},
                     "extra": {k.removeprefix(P): v for k, v in case["extra"].items()},
                     "truthful": {k.removeprefix(P): v for k, v in case["truthful"].items()},
                     "v88_only": {k.removeprefix(P): v for k, v in (case.get("v88_only") or {}).items()},
                     "recorded_on_v86": {k.removeprefix(P): v for k, v in (case.get("recorded_on_v86") or {}).items()},
                     "measured": measured})
    return {"cases": rows}


def mismatches(result: dict[str, Any], hand: dict[str, Any]) -> list[str]:
    bad = []
    for key, expected in hand.items():
        got = (result.get("lines") or {}).get(key, (result.get("symbols") or {}).get(key))
        if _num(got) != expected:
            bad.append(f"{key}={got!r}")
    return bad


def judge(payload: dict[str, Any], questions: dict[str, str]) -> None:
    new_sentences = set(questions.values())
    for row in payload["cases"]:
        verdicts: dict[str, Any] = {}
        for key, result in row["measured"].items():
            variant, name = key.split("@")
            verdict: dict[str, Any] = {}
            if variant == "truthful":
                verdict["hand_mismatches"] = mismatches(result, row["hand"])
            if variant == "unanswered" and name != "v88":
                verdict["silent_default"] = not any(q in new_sentences for q in result.get("questions") or [])
                verdict["hand_mismatches_if_truthful_differs"] = mismatches(result, row["hand"])
            asked = sorted(slug for slug, q in questions.items() if q in (result.get("questions") or []))
            verdict["asked"] = asked
            verdicts[key] = verdict
        row["verdicts"] = verdicts


def main() -> None:
    if len(sys.argv) != 3:
        raise SystemExit(__doc__)
    c87, c88 = core(Path(sys.argv[1])), core(Path(sys.argv[2]))
    build = json.loads((HERE / "prototype-build.json").read_text(encoding="utf-8"))
    payload = run_all(c87, c88)
    judge(payload, build["questions"])
    payload = {
        "cores": {"v86": "published", "v87": "question-wording prototype.py (scratch)", "v88": "prototype.py (scratch)"},
        "law": "law.json",
        "base_return": "question-wording harness wage return: single, wages 50,000, 4,500 withheld, every other question answered",
        **payload,
    }
    text = json.dumps(payload, indent=2) + "\n"
    for needle in ("/Users/", "/private/", "/tmp/", "/var/"):
        if needle in text:
            raise SystemExit(f"probe output contains {needle}")
    (HERE / "probe-output.json").write_text(text, encoding="utf-8")
    summary = {}
    for row in payload["cases"]:
        summary[row["id"]] = {k: v for k, v in row["verdicts"].items() if v.get("hand_mismatches") or v.get("asked")}
    print(json.dumps(summary, indent=1))


if __name__ == "__main__":
    main()
