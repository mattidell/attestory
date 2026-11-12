"""Track 0 adversarial closure for age and blindness being asked.

Evidence for docs/phases/engine-breadth/milestones/age-blindness-asked.md.
Charter: docs/reviews/age-blindness-asked/charter-track0.md.
Gate: PROJECT_PLANNING.md, "Track 0 Adversarial Closure Gate".

Every case is a live_coordinate_run. Hand values come from the 2025
instructions (law.json and the chart arithmetic in the P0 probes), never from
a run. A question is answered as a truthful filer reads its words. v87 is the
published core. v88 is the scratch core from prototype.py. v88 runs re-adopt
vocabulary bundle v4.

    python3 track0.py authority <scratch>/core-v88.json
    python3 track0.py matrix <scratch>/core-v88.json
    python3 track0.py late <scratch>/core-v88.json
    python3 track0.py reuse <scratch>/core-v88.json
    python3 track0.py neighbour <scratch>/core-v88.json
    python3 track0.py surface <scratch>/core-v88.json

``neighbour`` runs the recorded-list diff in a subprocess. An optional third
argument is a part file to resume. For the other tables, an optional third
argument limits the table to one case id.
"""

from __future__ import annotations

import copy
import importlib.util
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any, Callable

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

QW = REPO / "docs/phases/engine-breadth/milestones/question-wording-evidence"
PUBLISHED = REPO / "packages/content/tax/2025"
P = "tax.us.2025."
Acts = list[dict[str, Any]]

AGE, BLIND = P + "taxpayer-over-65", P + "taxpayer-blind"
S_AGE, S_BLIND = P + "spouse-over-65", P + "spouse-blind"
COND = P + "standard-deduction.spouse-separate-condition"
COND_SLUG = "standard-deduction.spouse-separate-condition"
COND_SYMBOL = "spouse_separate_condition"
SSN, S_SSN = P + "senior-deduction.taxpayer-valid-ssn", P + "senior-deduction.spouse-valid-ssn"
DEPENDENT = P + "standard-deduction.can-be-claimed-as-dependent"
STATUS = P + "filing-status"
MFJ, MFS = "married_filing_jointly", "married_filing_separately"
HOH, QSS = "head_of_household", "qualifying_surviving_spouse"
WAGES = 50000
TAXPAYER_Q = ["taxpayer-blind", "taxpayer-over-65"]
SPOUSE_Q = ["spouse-blind", "spouse-over-65"]
ALL_Q = SPOUSE_Q + TAXPAYER_Q
# Decision 11. On a separate return the spouse is asked only after the condition is yes.
MFS_OPEN = TAXPAYER_Q + [COND_SLUG]
ASKS = {
    "single": TAXPAYER_Q,
    "head_of_household": TAXPAYER_Q,
    "qualifying_surviving_spouse": TAXPAYER_Q,
    "dependent": TAXPAYER_Q,
    MFJ: ALL_Q,
    MFS: MFS_OPEN,
}
# Chart anchors from law.json ``chart`` plus the 2025 base standard deduction
# the P0 probes tie to that chart (one box is base + 2,000 or base + 1,600).
BASE = {
    "single": 15750,
    HOH: 23625,
    MFJ: 31500,
    MFS: 15750,
    QSS: 31500,
}
PER_BOX = {"single": 2000, HOH: 2000, MFJ: 1600, MFS: 1600, QSS: 1600}
# Tax Table amounts already cited from the 2025 table by the P0 probe basis.
TAX = {
    ("single", 34250): 3875,
    ("single", 32250): 3635,
    ("single", 26250): 2915,
    ("single", 24250): 2675,
    (MFJ, 18500): 1853,
    (MFJ, 10900): 1093,
    (MFS, 32650): 3683,
    (MFS, 34250): 3875,
    (QSS, 18500): 1853,
    (HOH, 26375): 2825,
}


def _module(name: str, path: Path) -> Any:
    module = sys.modules.get(name)
    if module is None:
        spec = importlib.util.spec_from_file_location(name, path)
        assert spec is not None and spec.loader is not None
        module = importlib.util.module_from_spec(spec)
        sys.modules[name] = module
        spec.loader.exec_module(module)
    return module


def probe() -> Any:
    return _module("aba_t0_probe", HERE / "probe.py")


def aba_rerun() -> Any:
    return _module("aba_t0_rerun", HERE / "rerun.py")


def qw_track0() -> Any:
    return _module("aba_t0_qw_track0", QW / "track0.py")


def questions() -> dict[str, str]:
    body = json.loads((HERE / "prototype-build.json").read_text(encoding="utf-8"))
    return {str(slug): str(text) for slug, text in body["questions"].items()}


def published_v87() -> Any:
    return probe().harness().Core("v87", "v85", "v85")


def scratch_v88(path: Path) -> Any:
    return probe().core(path)


def scrub(text: str) -> str:
    text = text.replace(str(REPO), ".")
    return re.sub(r"/(?:Users|private|tmp|var|opt)/\S+", "<path>", text)


def write(name: str, payload: dict[str, Any]) -> None:
    text = scrub(json.dumps(payload, indent=2) + "\n")
    for needle in ("/Users/", "/private/", "/tmp/", "/var/"):
        if needle in text:
            raise SystemExit(f"{name} contains {needle}")
    (HERE / name).write_text(text, encoding="utf-8")
    print(name, payload.get("pass"), payload.get("counts"), flush=True)


def slugs_in(sentences: list[str], words: dict[str, str]) -> list[str]:
    return sorted(slug for slug, text in words.items() if text in sentences)


def hand_amounts(status: str, t_age: bool, t_blind: bool, s_age: bool, s_blind: bool, *,
                 dependent: bool = False, condition: bool = True) -> dict[str, Any]:
    """Chart or dependents-worksheet amounts for wages of 50,000 and these boxes.

    A spouse box counts on a joint return, and on a separate return only when
    ``condition`` is yes. The senior deduction is 6,000 for a 65-or-older
    taxpayer except on a separate return, and 6,000 for a 65-or-older spouse
    only on a joint return. MAGI 50,000 is under both phaseout thresholds in law.json.
    """
    if dependent:
        boxes = int(t_age) + int(t_blind)
        line_12e = 15750 + boxes * 2000
        senior_a = 6000 if t_age else 0
        senior_b = 0
        extra = {
            "dependents-worksheet.line1-box-count": boxes,
            "dependents-worksheet.line4b": boxes * 2000,
        }
        tax_status = "single"
    else:
        if status == MFJ or (status == MFS and condition):
            spouse_boxes = int(s_age) + int(s_blind)
        else:
            spouse_boxes = 0
        boxes = int(t_age) + int(t_blind) + spouse_boxes
        if status == QSS:
            boxes = int(t_age) + int(t_blind)
        line_12e = BASE[status] + boxes * PER_BOX[status]
        senior_a = 6000 if t_age and status != MFS else 0
        senior_b = 6000 if s_age and status == MFJ else 0
        extra = {}
        tax_status = status
    senior = senior_a + senior_b
    line_15 = WAGES - line_12e - senior
    hand: dict[str, Any] = {
        "form1040.line-12e": line_12e,
        "form1040.line-13b": senior,
        "form1040.line-15": line_15,
        "schedule1a.line36a-taxpayer": senior_a,
        "schedule1a.line36b-spouse": senior_b,
        **extra,
    }
    tax = TAX.get((tax_status, line_15))
    if tax is not None:
        hand["form1040.line-16"] = tax
    return hand


def build_acts(status: str, answers: dict[str, Any], *, dependent: bool = False) -> Acts:
    pr = probe()
    filing = "single" if dependent else status
    acts = pr.base(filing)
    if dependent:
        acts = pr.harness().say(acts, DEPENDENT, "yes", "dependent")
    return pr.answer(acts, answers)


def answers_for(status: str, t_age: bool | None, t_blind: bool | None,
                s_age: bool | None, s_blind: bool | None, *, dependent: bool = False,
                condition: bool | None = None, omit_spouse: bool = False) -> dict[str, Any]:
    """Facts a truthful filer records. None means the question is not answered."""
    found: dict[str, Any] = {}
    if t_age is not None:
        found[AGE] = t_age
    if t_blind is not None:
        found[BLIND] = t_blind
    asks_spouse = status in (MFJ, MFS) and not dependent and not omit_spouse
    if asks_spouse:
        if s_age is not None:
            found[S_AGE] = s_age
        if s_blind is not None:
            found[S_BLIND] = s_blind
    if status == MFS and not dependent and condition is not None:
        found[COND] = condition
    if t_age and status != MFS:
        found[SSN] = "yes"
    if s_age and status == MFJ:
        found[S_SSN] = "yes"
    return found


def execute(core: Any, acts: Acts, run_id: str) -> dict[str, Any]:
    """probe.execute, plus the blocked-field sentences the surface table needs."""
    pr = probe()
    h = pr.harness()
    surface = core.surface()
    with h.loader_entries(core):
        try:
            finished = h._handover(
                h._finish(pr.readopt(acts, core), package_path=core.package_path,
                          package_version=core.version, release_path=core.release_path,
                          release_version=core.release_version, note=run_id),
                surface=surface, reconfirm=True)
            with tempfile.TemporaryDirectory() as tmp:
                outcome = h.live_coordinate_run(
                    h.WorkspaceCapability(Path(tmp) / "L"), repo_root=REPO, authoritative_acts=finished,
                    workspace_revision=len(finished), run_scope={"jurisdiction": "us", "year": h.YEAR},
                    scope_user=h.ccr.USER, request={"schema": "run-request.v1"}, run_id=run_id,
                    governance_pins=[], surface=surface, output_name="out.json")
                # The workspace is deleted when this block ends. Read it here.
                summary = pr.summarize(outcome)
                if summary.get("outcome") != "success":
                    return summary
                model = json.loads(outcome.presentation_path.read_text(encoding="utf-8"))
                blocked_fields: list[str] = []
                field_sentences: dict[str, list[str]] = {}
                for section in model.get("sections") or []:
                    field_id = str((section.get("field") or {}).get("id") or "").removeprefix(P)
                    resolved = section.get("resolved") or {}
                    if "blocked" not in str(resolved.get("disposition")):
                        continue
                    blocked_fields.append(field_id)
                    sentences = [scrub(str(row.get("sentence") or "").strip()) for row in resolved.get("reasons") or []
                                 if isinstance(row, dict) and str(row.get("sentence") or "").strip()]
                    if sentences:
                        field_sentences[field_id] = sentences
                words = questions()
                summary["blocked_fields"] = sorted(blocked_fields)
                summary["field_sentences"] = {key: value for key, value in sorted(field_sentences.items())}
                summary["asked_slugs"] = slugs_in(summary.get("questions") or [], words)
                summary["missing"] = sorted({
                    symbol for row in summary.get("blocked_rules") or [] for symbol in row.get("missing") or []})
                return summary
        except Exception as exc:  # noqa: BLE001 - a rejected act list is a result
            return {"outcome": "error", "error": type(exc).__name__, "message": scrub(str(exc))[:500]}


def mismatches(result: dict[str, Any], hand: dict[str, Any]) -> list[str]:
    if result.get("outcome") != "success":
        return [f"outcome {result.get('outcome')}: {result.get('error') or result.get('reason')}"]
    bad = []
    for key, expected in hand.items():
        got = (result.get("lines") or {}).get(key, (result.get("symbols") or {}).get(key))
        if probe()._num(got) != expected and got != expected:
            bad.append(f"{key}={got!r}")
    return bad


def without_condition(acts: Acts) -> Acts:
    """A copy of ``acts`` with no assertion of the scratch condition fact.

    Published v87 has no such fact type. A v88 act list may assert it.
    """
    return probe().harness().strip(copy.deepcopy(acts), COND)


def run_pair(case_id: str, acts: Acts, v88: Any, *, also_v87: bool = True,
             acts_v87: Acts | None = None) -> dict[str, Any]:
    """Run one act list on v88 and, unless declined, on published v87.

    Published v87 never receives an assertion of the scratch condition fact.
    ``acts_v87`` replaces that stripped list when the step already has one.
    """
    measured: dict[str, Any] = {}
    cores: list[tuple[str, Any]] = [("v88", v88)]
    if also_v87:
        cores.insert(0, ("v87", published_v87()))
    for name, core in cores:
        if name == "v87":
            use = acts_v87 if acts_v87 is not None else without_condition(acts)
        else:
            use = acts
        measured[name] = execute(core, use, f"demo.aba.t0.{case_id}.{name}")
        line = (measured[name].get("lines") or {}).get("form1040.line-12e")
        print(case_id, name, line, measured[name].get("asked_slugs") or measured[name].get("error") or "", flush=True)
    return measured


def judge_answered(measured: dict[str, Any], hand: dict[str, Any], *, hand_v87: dict[str, Any] | None = None,
                   ask: list[str] | None = None) -> list[str]:
    bad = [f"v88 {item}" for item in mismatches(measured["v88"], hand)]
    if ask is not None and measured["v88"].get("asked_slugs") != sorted(ask):
        bad.append(f"v88 asked {measured['v88'].get('asked_slugs')}")
    if "v87" in measured:
        bad += [f"v87 {item}" for item in mismatches(measured["v87"], hand_v87 or hand)]
    return bad


def judge_open(measured: dict[str, Any], ask: list[str], silent: dict[str, Any]) -> list[str]:
    """v88 blocks and asks ``ask``. v87 publishes the default and asks none of the four."""
    bad = []
    v88 = measured["v88"]
    if v88.get("lines", {}).get("form1040.line-12e") != "blocked":
        bad.append(f"v88 12e {v88.get('lines', {}).get('form1040.line-12e')!r}")
    if v88.get("asked_slugs") != sorted(ask):
        bad.append(f"v88 asked {v88.get('asked_slugs')}")
    words = set(questions().values())
    extra = [sentence for sentence in v88.get("questions") or [] if sentence not in words]
    if extra:
        bad.append(f"v88 extra sentences {len(extra)}")
    if "v87" in measured:
        v87 = measured["v87"]
        if v87.get("asked_slugs"):
            bad.append(f"v87 asked {v87.get('asked_slugs')}")
        bad += [f"v87 {item}" for item in mismatches(v87, silent)]
    return bad


def keep(measured: dict[str, Any]) -> dict[str, Any]:
    """The live output a later reader needs, without the per-field sentence bulk."""
    out = {}
    for name, result in measured.items():
        out[name] = {
            "outcome": result.get("outcome"),
            "lines": result.get("lines"),
            "symbols": result.get("symbols"),
            "asked_slugs": result.get("asked_slugs"),
            "questions": result.get("questions"),
            "blocked_field_count": result.get("blocked_field_count"),
            "blocked_fields": result.get("blocked_fields"),
            "missing": result.get("missing"),
            "blocked_rules": result.get("blocked_rules"),
            "error": result.get("error"),
            "reason": result.get("reason"),
        }
    return out


def finish(name: str, rows: list[dict[str, Any]], *, table: list[dict[str, Any]] | None = None) -> None:
    failed = [row["id"] for row in rows if row["failures"]]
    payload: dict[str, Any] = {
        "counts": {"cases": len(rows), "passed": len(rows) - len(failed), "failed": len(failed)},
        "pass": not failed,
        "failed": failed,
        "cases": rows,
    }
    if table is not None:
        payload["table"] = table
    write(name, payload)


# ---- item 1: authority lifecycle -------------------------------------------------------


def authority_specs() -> list[dict[str, Any]]:
    """One live situation for each cell of the four-question table."""
    silent_single = hand_amounts("single", False, False, False, False)
    silent_joint = hand_amounts(MFJ, False, False, False, False)
    specs = [
        {"id": "alc_taxpayer_age_unanswered", "note": "Single, nothing recorded. Both taxpayer questions are asked; the spouse is not.",
         "open": True, "status": "single", "ask": TAXPAYER_Q, "silent": silent_single,
         "missing": ["taxpayer_over_65", "taxpayer_blind"]},
        {"id": "alc_taxpayer_age_jan1", "note": "Single, born January 1, 1961, not blind. Age 65 is reached on December 31, 2025.",
         "status": "single", "bits": (True, False, False, False)},
        {"id": "alc_taxpayer_age_jan2", "note": "Single, born January 2, 1961, not blind. Not 65 until January 1, 2026.",
         "status": "single", "bits": (False, False, False, False)},
        {"id": "alc_taxpayer_died_before", "note": "Single, born January 1, 1961, died December 30, 2025, before the day age 65 is reached. Truthful answer: no.",
         "status": "single", "bits": (False, False, False, False)},
        {"id": "alc_taxpayer_died_on_day", "note": "Single, born January 1, 1961, died December 31, 2025, the day age 65 is reached. Truthful answer: yes.",
         "status": "single", "bits": (True, False, False, False)},
        {"id": "alc_taxpayer_blind_yes", "note": "Single, born 1990, certified 20/200 in the better eye. Blindness yes, age no.",
         "status": "single", "bits": (False, True, False, False)},
        {"id": "alc_spouse_age_joint_yes", "note": "Joint. Taxpayer born 1970. Spouse born March 3, 1958, living, not blind.",
         "status": MFJ, "bits": (False, False, True, False)},
        {"id": "alc_spouse_age_joint_no", "note": "Joint. Spouse born January 2, 1961. Truthful age answer: no.",
         "status": MFJ, "bits": (False, False, False, False)},
        {"id": "alc_spouse_died_before", "note": "Joint. Spouse born February 14, 1960, died February 12, 2025, before age 65. Truthful answer: no.",
         "status": MFJ, "bits": (False, False, False, False)},
        {"id": "alc_spouse_died_on_day", "note": "Joint. Spouse born February 14, 1960, died February 13, 2025, the day age 65 is reached. Truthful answer: yes.",
         "status": MFJ, "bits": (False, False, True, False)},
        {"id": "alc_spouse_blind_joint_yes", "note": "Joint. Spouse blind on December 31, 2025; neither spouse is 65.",
         "status": MFJ, "bits": (False, False, False, True)},
        {"id": "alc_spouse_separate_qualifies", "note": "Separate return. Spouse born 1955, no income, not filing, not claimable. Age yes, condition yes.",
         "status": MFS, "bits": (False, False, True, False), "condition": True},
        {"id": "alc_spouse_separate_has_income", "note": "Separate return. Spouse born 1955, so age is yes, and the spouse has income, so the condition is no. v87 still counts the age box.",
         "status": MFS, "bits": (False, False, True, False), "condition": False,
         "hand_v87": hand_amounts(MFS, False, False, True, False, condition=True)},
        {"id": "alc_separate_condition_no_spouse_unanswered",
         "note": "Separate return. The condition is no and the spouse's age and blindness are unanswered. Line 12e is 15,750 and the spouse is not asked.",
         "status": MFS, "bits": (False, False, False, False), "condition": False,
         "omit_spouse": True, "expect_ask": []},
        {"id": "alc_spouse_not_on_hoh", "note": "Head of household. Line 12d says not to check a spouse box. Only the taxpayer is asked.",
         "open": True, "status": HOH, "ask": TAXPAYER_Q, "silent": hand_amounts(HOH, False, False, False, False),
         "missing": ["taxpayer_over_65", "taxpayer_blind"]},
        {"id": "alc_spouse_not_on_qss", "note": "Qualifying surviving spouse. The chart has no spouse-box row. Only the taxpayer is asked.",
         "open": True, "status": QSS, "ask": TAXPAYER_Q, "silent": hand_amounts(QSS, False, False, False, False),
         "missing": ["taxpayer_over_65", "taxpayer_blind"]},
        {"id": "alc_qss_ignores_recorded_spouse", "note": "Qualifying surviving spouse with spouse age recorded true. v88 does not count it; v87 does.",
         "status": QSS, "bits": (False, False, True, False), "record_spouse": True,
         "hand_v87": {
             key: value
             for key, value in (
                 hand_amounts(QSS, False, False, True, False)
                 | {"form1040.line-12e": 33100, "form1040.line-15": WAGES - 33100}
             ).items()
             if key != "form1040.line-16"
         }},
        {"id": "alc_dependent_unanswered", "note": "A filer who can be claimed, nothing else recorded. The worksheet waits on the taxpayer's two answers.",
         "open": True, "status": "dependent", "dependent": True, "ask": TAXPAYER_Q,
         "silent": hand_amounts("single", False, False, False, False, dependent=True),
         "missing": ["taxpayer_over_65", "taxpayer_blind"]},
        {"id": "alc_dependent_age_yes", "note": "A filer who can be claimed, born March 3, 1950, not blind.",
         "status": "dependent", "dependent": True, "bits": (True, False, False, False)},
        {"id": "alc_joint_unanswered", "note": "Joint, nothing recorded. All four questions are asked, and line 36b waits on the spouse's age.",
         "open": True, "status": MFJ, "ask": ALL_Q, "silent": silent_joint,
         "missing": ["taxpayer_over_65", "taxpayer_blind", "spouse_over_65", "spouse_blind"]},
        {"id": "alc_separate_unanswered", "note": "Separate return, nothing recorded. The taxpayer's two questions and the condition are asked. The spouse is not asked until the condition is yes. Line 36b publishes 0.",
         "open": True, "status": MFS, "ask": MFS_OPEN, "silent": hand_amounts(MFS, False, False, False, False),
         "missing": ["taxpayer_over_65", "taxpayer_blind", COND_SYMBOL]},
    ]
    return specs


def authority_table() -> list[dict[str, Any]]:
    return [
        {"fact": "taxpayer-over-65",
         "meaning": "The filer was born before January 2, 1961, counting age 65 on the day before the 65th birthday, and a 2025 death only if the filer was already 65.",
         "who_is_asked": "Every return.",
         "what_answers_it": "The filer's yes or no to input-question.taxpayer-over-65.",
         "rule": "dependents-worksheet-line-1 v2 and schedule1a-part-v-line-36a v1.",
         "what_replaces_it": "A later answer in the act list (late_answer_replaced). The binding is required, so an absent answer blocks rather than defaulting.",
         "cases": ["alc_taxpayer_age_unanswered", "alc_taxpayer_age_jan1", "alc_taxpayer_age_jan2",
                   "alc_taxpayer_died_before", "alc_taxpayer_died_on_day", "alc_dependent_age_yes"]},
        {"fact": "taxpayer-blind",
         "meaning": "On December 31, 2025 the filer was totally blind, or an eye doctor's certified statement says 20/200 or a 20-degree field, or a statement that the condition is not likely to improve beyond those limits.",
         "who_is_asked": "Every return.",
         "what_answers_it": "The filer's yes or no to input-question.taxpayer-blind.",
         "rule": "dependents-worksheet-line-1 v2. The senior deduction does not read it.",
         "what_replaces_it": "A later answer in the act list. Blindness for someone who died in 2025 is not stated by either source (Decision 7).",
         "cases": ["alc_taxpayer_age_unanswered", "alc_taxpayer_blind_yes", "alc_taxpayer_age_jan2"]},
        {"fact": "spouse-over-65",
         "meaning": "The spouse was born before January 2, 1961 under the same birthday and 2025-death test. The answer is the spouse's age, on every status that asks it.",
         "who_is_asked": "A joint return, and a separate return only when the condition is yes. Not a single, head of household, qualifying surviving spouse, or dependent return.",
         "what_answers_it": "The filer's yes or no to input-question.spouse-over-65. The v4 title is the v3 age title.",
         "rule": "dependents-worksheet-line-1 v2 on a joint return, and on a separate return only when the condition fact is yes. schedule1a-part-v-line-36b v2 on a joint return only.",
         "what_replaces_it": "A later answer (late_answer_replaced). A filing-status change leaves the answer in place (late_joint_to_separate, late_joint_to_hoh).",
         "cases": ["alc_joint_unanswered", "alc_spouse_age_joint_yes", "alc_spouse_died_before", "alc_spouse_died_on_day",
                   "alc_spouse_separate_qualifies", "alc_spouse_separate_has_income",
                   "alc_separate_condition_no_spouse_unanswered", "alc_spouse_not_on_hoh",
                   "alc_spouse_not_on_qss", "alc_qss_ignores_recorded_spouse"]},
        {"fact": "spouse-blind",
         "meaning": "The spouse meets the December 31, 2025 blindness test, including a statement that the condition is not likely to improve. The answer is blindness only.",
         "who_is_asked": "A joint return, and a separate return only when the condition is yes. Not the other statuses.",
         "what_answers_it": "The filer's yes or no to input-question.spouse-blind. The v4 title adds the instructions' alternative to the v3 blindness title.",
         "rule": "dependents-worksheet-line-1 v2 on a joint return, and on a separate return only when the condition fact is yes. Line 36b does not read blindness.",
         "what_replaces_it": "A later answer. The same parked death question as the taxpayer's blindness.",
         "cases": ["alc_joint_unanswered", "alc_spouse_blind_joint_yes", "alc_separate_unanswered",
                   "alc_separate_condition_no_spouse_unanswered", "alc_spouse_not_on_hoh"]},
        {"fact": COND_SLUG,
         "meaning": "The spouse had no income, isn't filing a return, and can't be claimed as a dependent on another person's return.",
         "who_is_asked": "A separate return only. Not joint, single, head of household, qualifying surviving spouse, or a dependent filer.",
         "what_answers_it": "The filer's yes or no to input-question." + COND_SLUG + ".",
         "rule": "dependents-worksheet-line-1 v2, and only on a separate return. A yes lets the spouse's two boxes count.",
         "what_replaces_it": "A later answer. While it is unanswered on a separate return, line 12e blocks (alc_separate_unanswered, late_joint_to_separate).",
         "cases": ["alc_separate_unanswered", "alc_spouse_separate_qualifies", "alc_spouse_separate_has_income",
                   "alc_separate_condition_no_spouse_unanswered", "alc_joint_unanswered"]},
    ]


def acts_of(spec: dict[str, Any]) -> Acts:
    if spec.get("open") and "bits" not in spec:
        answers: dict[str, Any] = {}
    else:
        bits = spec.get("bits") or (None, None, None, None)
        answers = answers_for(spec["status"] if spec["status"] != "dependent" else "single", *bits,
                              dependent=bool(spec.get("dependent")), condition=spec.get("condition"),
                              omit_spouse=bool(spec.get("omit_spouse")))
    if spec.get("record_spouse"):
        answers[S_AGE] = True
        answers[S_BLIND] = False
    status = spec["status"] if spec["status"] != "dependent" else "single"
    return build_acts(status, answers, dependent=bool(spec.get("dependent")))


def run_authority(core_path: Path, only: str | None) -> None:
    v88 = scratch_v88(core_path)
    rows = []
    for spec in authority_specs():
        if only and spec["id"] != only:
            continue
        measured = run_pair(spec["id"], acts_of(spec), v88)
        if spec.get("open"):
            failures = judge_open(measured, spec["ask"], spec["silent"])
            missing = set(measured["v88"].get("missing") or [])
            for symbol in spec.get("missing") or []:
                if symbol not in missing:
                    failures.append(f"v88 did not block on {symbol}")
        else:
            dependent = bool(spec.get("dependent"))
            status = "single" if dependent else spec["status"]
            bits = spec["bits"]
            spouse = bits[2:] if spec.get("record_spouse") or status in (MFJ, MFS) else (False, False)
            condition = bool(spec.get("condition", True))
            if spec.get("record_spouse"):
                hand = hand_amounts(status, bits[0], bits[1], False, False)
            else:
                hand = hand_amounts(status, bits[0], bits[1], spouse[0], spouse[1], dependent=dependent,
                                    condition=condition)
            ask = spec["expect_ask"] if "expect_ask" in spec else None
            failures = judge_answered(measured, hand, hand_v87=spec.get("hand_v87"), ask=ask)
        rows.append({"id": spec["id"], "note": spec["note"], "failures": failures, "measured": keep(measured)})
    finish("track0-authority.json", rows, table=authority_table())


# ---- item 2: empty / nonempty matrix ---------------------------------------------------


def matrix_specs() -> list[dict[str, Any]]:
    """Status x unanswered / false / true, plus the birthday and 2025 death boundaries."""
    populations = [
        ("single", "single", False, "single"),
        ("joint", MFJ, False, "joint"),
        ("separate_qualifies", MFS, False, "separate, spouse has no income and is not filing or claimable"),
        ("separate_has_income", MFS, False, "separate, spouse has income"),
        ("hoh", HOH, False, "head of household"),
        ("qss", QSS, False, "qualifying surviving spouse"),
        ("dependent", "single", True, "filer who can be claimed as a dependent"),
    ]
    specs = []
    for key, status, dependent, label in populations:
        asks = ASKS["dependent" if dependent else status]
        for variant, bits in (
            ("unanswered", None),
            ("false", (False, False, False, False)),
            ("true", (True, True, True, True)),
            ("born_jan1", (True, False, False, False)),
            ("born_jan2", (False, False, False, False)),
        ):
            if variant == "born_jan2":
                continue  # the same truthful answers as false; born_jan1 is the other birthday
            note = {
                "unanswered": "the age and blindness facts are unanswered",
                "false": "born January 2, 1961 and not blind, so every truthful answer is no",
                "true": "born before January 2, 1961 and blind",
                "born_jan1": "born January 1, 1961 and not blind",
            }[variant]
            condition = None
            if status == MFS and variant == "unanswered":
                note = "the taxpayer's age and blindness and the condition are unanswered; the spouse is not asked"
            if status == MFS and variant != "unanswered":
                # Qualifying spouse: the condition is yes except where every answer is no.
                # Spouse with income: the condition is no, and age and blindness stay what they are.
                condition = key == "separate_qualifies" and variant != "false"
            if key == "separate_has_income" and variant == "true":
                note += "; the spouse is 65 and blind and has income, so the condition answer is no"
            specs.append({
                "id": f"m_{key}_{variant}",
                "note": f"{label}; {note}",
                "status": status,
                "dependent": dependent,
                "open": variant == "unanswered",
                "ask": asks,
                "bits": bits,
                "condition": condition,
            })
    specs += [
        {"id": "m_taxpayer_died_before_jan1_birthday",
         "note": "Single. Born January 1, 1961, died December 30, 2025, the day before age 65 is reached.",
         "status": "single", "bits": (False, False, False, False)},
        {"id": "m_taxpayer_died_on_jan1_birthday",
         "note": "Single. Born January 1, 1961, died December 31, 2025, the day age 65 is reached.",
         "status": "single", "bits": (True, False, False, False)},
        {"id": "m_taxpayer_died_before_on_joint",
         "note": "Joint. Taxpayer born January 1, 1961, died December 30, 2025. Spouse born 1970.",
         "status": MFJ, "bits": (False, False, False, False)},
        {"id": "m_taxpayer_died_on_day_on_joint",
         "note": "Joint. Taxpayer born January 1, 1961, died December 31, 2025. Spouse born 1970.",
         "status": MFJ, "bits": (True, False, False, False)},
        {"id": "m_spouse_died_before",
         "note": "Joint. Spouse born February 14, 1960, died February 12, 2025.",
         "status": MFJ, "bits": (False, False, False, False)},
        {"id": "m_spouse_died_on_day",
         "note": "Joint. Spouse born February 14, 1960, died February 13, 2025.",
         "status": MFJ, "bits": (False, False, True, False)},
        {"id": "m_qss_spouse_age_recorded",
         "note": "Qualifying surviving spouse. Spouse age is recorded true anyway. v88 counts only the taxpayer.",
         "status": QSS, "bits": (False, False, False, False), "record_spouse": True,
         "hand_v87_boxes": (False, False, True, False)},
    ]
    return specs


def run_matrix(core_path: Path, only: str | None) -> None:
    v88 = scratch_v88(core_path)
    rows = []
    for spec in matrix_specs():
        if only and spec["id"] != only:
            continue
        measured = run_pair(spec["id"], acts_of(spec), v88)
        dependent = bool(spec.get("dependent"))
        status = spec["status"]
        if spec.get("open"):
            silent_bits = (False, False, False, False)
            silent = hand_amounts("single" if dependent else status, *silent_bits, dependent=dependent)
            failures = judge_open(measured, spec["ask"], silent)
        else:
            bits = spec["bits"]
            condition = spec.get("condition")
            condition_yes = True if condition is None else bool(condition)
            if spec.get("record_spouse"):
                hand = hand_amounts(status, bits[0], bits[1], False, False)
                v87_hand = hand_amounts(status, *spec["hand_v87_boxes"])
                # v1 counts a spouse age box on a qualifying surviving spouse return: base + 1,600.
                v87_hand = dict(v87_hand)
                v87_hand["form1040.line-12e"] = 33100
                v87_hand["form1040.line-15"] = WAGES - 33100
                v87_hand.pop("form1040.line-16", None)
            else:
                hand = hand_amounts("single" if dependent else status, bits[0], bits[1], bits[2], bits[3],
                                    dependent=dependent, condition=condition_yes)
                v87_hand = None
                if status == MFS and condition is False and (bits[2] or bits[3]):
                    v87_hand = hand_amounts(status, bits[0], bits[1], bits[2], bits[3], condition=True)
            failures = judge_answered(measured, hand, hand_v87=v87_hand)
        rows.append({"id": spec["id"], "note": spec["note"], "failures": failures, "measured": keep(measured)})
    finish("track0-matrix.json", rows)


# ---- item 3: late authority ------------------------------------------------------------


def late_steps() -> list[dict[str, Any]]:
    h = probe().harness()
    joint = build_acts(MFJ, answers_for(MFJ, False, False, True, False))
    separate = h.say(joint, STATUS, MFS, "status-separate")
    separate_no = h.say(separate, COND, False, "condition-no")
    single_yes = build_acts("single", answers_for("single", True, False, False, False))
    return [
        {"id": "late_joint_to_separate",
         "note": "Spouse age was answered yes on a joint return and is not replaced. The status becomes separate, the condition is unanswered, then answered no because the spouse has income.",
         "steps": [
             {"name": "joint_spouse_age_yes", "acts": joint,
              "hand": hand_amounts(MFJ, False, False, True, False)},
             {"name": "status_now_separate", "acts": separate, "open": True, "ask": [COND_SLUG],
              "hand_v87": hand_amounts(MFS, False, False, True, False)},
             {"name": "condition_answered_no", "acts": separate_no, "acts_v87": separate,
              "hand": hand_amounts(MFS, False, False, True, False, condition=False),
              "hand_v87": hand_amounts(MFS, False, False, True, False, condition=True)},
         ]},
        {"id": "late_joint_to_hoh",
         "note": "Spouse age was answered yes on a joint return. Head of household does not check a spouse box, so the recorded yes is no longer read.",
         "steps": [
             {"name": "joint_spouse_age_yes", "acts": joint,
              "hand": hand_amounts(MFJ, False, False, True, False)},
             {"name": "status_now_hoh", "acts": h.say(joint, STATUS, HOH, "status-hoh"),
              "hand": hand_amounts(HOH, False, False, False, False)},
         ]},
        {"id": "late_answer_replaced",
         "note": "The taxpayer's age answer is replaced in the act list. The harness say drops the earlier assertion; no supersession act is recorded.",
         "steps": [
             {"name": "age_yes", "acts": single_yes,
              "hand": hand_amounts("single", True, False, False, False)},
             {"name": "age_replaced_no", "acts": h.say(single_yes, AGE, False, "age-no"),
              "hand": hand_amounts("single", False, False, False, False)},
         ]},
    ]


def run_late(core_path: Path, only: str | None) -> None:
    v88 = scratch_v88(core_path)
    rows = []
    for trace in late_steps():
        if only and trace["id"] != only:
            continue
        steps = []
        failures = []
        previous = None
        for step in trace["steps"]:
            name, acts = step["name"], step["acts"]
            case_id = f"{trace['id']}_{name}"
            measured = run_pair(case_id, acts, v88, acts_v87=step.get("acts_v87"))
            if step.get("open"):
                step_failures = judge_open(measured, step["ask"], step.get("hand_v87") or {})
                if step.get("hand_v87"):
                    # judge_open compares v87 to a silent default. This step's v87 still has the recorded spouse age.
                    step_failures = [item for item in step_failures if not item.startswith("v87 ")]
                    step_failures += [f"v87 {item}" for item in mismatches(measured["v87"], step["hand_v87"])]
            else:
                step_failures = judge_answered(measured, step["hand"], hand_v87=step.get("hand_v87"))
            failures += [f"{name}: {item}" for item in step_failures]
            line = (measured["v88"].get("lines") or {}).get("form1040.line-12e")
            steps.append({
                "step": name,
                "hand": step.get("hand"),
                "line_12e": line,
                "spouse_age_still_yes": any(
                    isinstance(act.get("payload"), dict)
                    and isinstance((act["payload"].get("finding") or {}), dict)
                    and str((act["payload"].get("finding") or {}).get("fact_id", "")).startswith(S_AGE + "|")
                    and (act["payload"].get("finding") or {}).get("value") is True
                    for act in acts
                ),
                "unusable_prior_12e": previous,
                "failures": step_failures,
                "measured": keep(measured),
            })
            previous = line
        rows.append({
            "id": trace["id"],
            "note": trace["note"],
            "supersession_act": False,
            "mechanism": "harness say replaces the earlier assertion in the act list",
            "failures": failures,
            "steps": steps,
        })
    finish("track0-late.json", rows)


# ---- item 4: claim reuse ---------------------------------------------------------------


def _body(content: Path, member: dict[str, Any]) -> dict[str, Any] | None:
    stem = str(member["id"]).removeprefix(P)
    version = member["version"]
    candidates = [f"{stem}.{version}.json", f"{stem}.json"]
    if member.get("role") == "fact-type-bundle":
        base = stem.removesuffix(".vocabulary")
        candidates = [f"{base}.bundle.{version}.json", f"{base}.bundle.json"]
    if member.get("role") == "computation":
        slug = stem.removeprefix("rule.")
        candidates = [f"rule.{slug}.{version}.json", f"rule.{slug}.json", f"{stem}.{version}.json"]
    for name in candidates:
        path = content / name
        if path.exists():
            body = json.loads(path.read_text(encoding="utf-8"))
            if body.get("version") == version or member.get("role") != "fact-type-bundle":
                if body.get("id") == member["id"] or body.get("version") == version:
                    return body
    return None


def run_reuse(core_path: Path, only: str | None) -> None:
    v88_core = scratch_v88(core_path)
    v88_pkg = json.loads((v88_core.content / "package.core-calculations.v88.json").read_text(encoding="utf-8"))
    v87_pkg = json.loads((PUBLISHED / "package.core-calculations.v87.json").read_text(encoding="utf-8"))
    old_m = {member["id"]: member for member in v87_pkg["members"]}
    new_m = {member["id"]: member for member in v88_pkg["members"]}
    changed = sorted(key for key in set(old_m) | set(new_m) if old_m.get(key) != new_m.get(key))
    member_rows = []
    for member_id in changed:
        old, new = old_m.get(member_id), new_m.get(member_id)
        member_rows.append({
            "id": member_id.removeprefix(P),
            "v87": None if old is None else old["version"],
            "v88": None if new is None else new["version"],
            "role": (new or old or {}).get("role"),
        })
    expected = {
        "input-question.taxpayer-over-65", "input-question.taxpayer-blind",
        "input-question.spouse-over-65", "input-question.spouse-blind",
        "input-question.standard-deduction.spouse-separate-condition",
        "rule.dependents-worksheet-line-1", "rule.schedule1a-part-v-line-36b",
        "core_calculations.vocabulary",
    }
    got = {row["id"] for row in member_rows}
    binding_changes = []
    old_b = {row["symbol"]: row for row in v87_pkg["input_bindings"]}
    new_b = {row["symbol"]: row for row in v88_pkg["input_bindings"]}
    for symbol in sorted(set(old_b) | set(new_b)):
        if old_b.get(symbol) != new_b.get(symbol):
            left = {key: value for key, value in (old_b.get(symbol) or {}).items() if key != "mode"}
            right = {key: value for key, value in (new_b.get(symbol) or {}).items() if key != "mode"}
            binding_changes.append({
                "symbol": symbol,
                "v87": None if symbol not in old_b else old_b[symbol].get("mode"),
                "v88": None if symbol not in new_b else new_b[symbol].get("mode"),
                "other_fields_unchanged": left == right,
            })
    needles = ("taxpayer_over_65", "taxpayer_blind", "spouse_over_65", "spouse_blind")
    readers = []
    allowed_rule_diff = {"dependents-worksheet-line-1", "schedule1a-part-v-line-36b"}
    for member in v87_pkg["members"]:
        if member.get("role") != "computation":
            continue
        body = _body(PUBLISHED, member)
        if body is None or not any(needle in json.dumps(body) for needle in needles):
            continue
        slug = str(member["id"]).removeprefix(P + "rule.")
        twin = new_m.get(member["id"])
        new_body = _body(v88_core.content, twin) if twin else None
        readers.append({
            "id": slug,
            "v87": member["version"],
            "v88": None if twin is None else twin["version"],
            "bytes_identical": body == new_body,
        })
    v3 = json.loads((PUBLISHED / "core_calculations.bundle.v3.json").read_text(encoding="utf-8"))
    v4 = json.loads((v88_core.content / "core_calculations.bundle.v4.json").read_text(encoding="utf-8"))
    title_changes = []
    identity_same = True
    by_id = {fact["id"]: fact for fact in v4["fact_types"]}
    for fact in v3["fact_types"]:
        other = by_id.get(fact["id"])
        if other is None:
            identity_same = False
            continue
        if {key: value for key, value in fact.items() if key != "title"} != {
            key: value for key, value in other.items() if key != "title"
        }:
            identity_same = False
        if fact.get("title") != other.get("title"):
            title_changes.append(fact["id"].removeprefix(P))
    mode_rows = [row for row in binding_changes if row["v87"] is not None]
    added_rows = [row for row in binding_changes if row["v87"] is None]
    checks = {
        "only_the_eight_members": got == expected,
        "questions_added": all(row["v87"] is None and row["v88"] == "v1" for row in member_rows if row["role"] == "input-question"),
        "two_rule_successors": {row["id"]: (row["v87"], row["v88"]) for row in member_rows if row["role"] == "computation"} == {
            "rule.dependents-worksheet-line-1": ("v1", "v2"),
            "rule.schedule1a-part-v-line-36b": ("v1", "v2"),
        },
        "bundle_v3_to_v4": any(row["id"] == "core_calculations.vocabulary" and (row["v87"], row["v88"]) == ("v3", "v4") for row in member_rows),
        "four_bindings_became_required": [ {key: row[key] for key in ("symbol", "v87", "v88")} for row in mode_rows ] == [
            {"symbol": "spouse_blind", "v87": "optional_default", "v88": "required"},
            {"symbol": "spouse_over_65", "v87": "optional_default", "v88": "required"},
            {"symbol": "taxpayer_blind", "v87": "optional_default", "v88": "required"},
            {"symbol": "taxpayer_over_65", "v87": "optional_default", "v88": "required"},
        ] and all(row["other_fields_unchanged"] for row in mode_rows),
        "condition_binding_added": [row["symbol"] for row in added_rows] == [COND_SYMBOL]
        and all(row["v88"] == "required" for row in added_rows),
        "other_readers_unchanged": all(row["bytes_identical"] and row["v87"] == row["v88"] for row in readers if row["id"] not in allowed_rule_diff),
        "two_successors_differ": all(not row["bytes_identical"] and row["v88"] == "v2" for row in readers if row["id"] in allowed_rule_diff),
        "blindness_titles_add_the_alternative": sorted(title_changes) == ["spouse-blind", "taxpayer-blind"],
        "existing_facts_unchanged": identity_same,
        "condition_fact_added": {fact["id"] for fact in v4["fact_types"]} - {fact["id"] for fact in v3["fact_types"]} == {COND},
    }
    live = []
    samples = [
        ("reuse_single_false", "single", False, (False, False, False, False), None, None),
        ("reuse_joint_spouse_age", MFJ, False, (False, False, True, False), None, None),
        ("reuse_dependent_age", "single", True, (True, False, False, False), None, None),
        ("reuse_qss_spouse_recorded", QSS, False, (False, False, False, False), (False, False, True, False), None),
        ("reuse_separate_condition_no", MFS, False, (False, False, True, False), (False, False, True, False), False),
    ]
    for case_id, status, dependent, bits, v87_bits, condition in samples:
        if only and case_id != only:
            continue
        spec = {"status": status, "dependent": dependent, "bits": bits, "record_spouse": v87_bits is not None,
                "condition": condition}
        measured = run_pair(case_id, acts_of(spec), v88_core)
        if case_id == "reuse_separate_condition_no":
            hand = hand_amounts(MFS, False, False, True, False, condition=False)
            v87_hand = hand_amounts(MFS, False, False, True, False, condition=True)
            failures = judge_answered(measured, hand, hand_v87=v87_hand)
        elif v87_bits is None:
            hand = hand_amounts("single" if dependent else status, *bits, dependent=dependent)
            failures = judge_answered(measured, hand)
        else:
            hand = hand_amounts(status, False, False, False, False)
            v87_hand = {"form1040.line-12e": 33100, "form1040.line-13b": 0, "form1040.line-15": WAGES - 33100,
                        "schedule1a.line36a-taxpayer": 0, "schedule1a.line36b-spouse": 0}
            failures = judge_answered(measured, hand, hand_v87=v87_hand)
        live.append({"id": case_id, "failures": failures, "measured": keep(measured)})
    live_ok = all(not row["failures"] for row in live)
    checks["live_composition"] = live_ok
    write("track0-reuse.json", {
        "counts": {"changed_members": len(member_rows), "readers": len(readers), "live": len(live),
                   "live_passed": sum(1 for row in live if not row["failures"])},
        "pass": all(checks.values()),
        "checks": checks,
        "changed_members": member_rows,
        "binding_changes": binding_changes,
        "readers": readers,
        "title_changes": title_changes,
        "live": live,
        "failed": [name for name, ok in checks.items() if not ok] + [row["id"] for row in live if row["failures"]],
    })


# ---- item 5: neighbour diff ------------------------------------------------------------


def neighbour_worker(core_path: Path, part: Path) -> None:
    """The 775 recorded lists plus one joint, one separate and one dependent, on published v87 and scratch v88."""
    t0 = qw_track0()
    rr = t0.rerun()
    aba = aba_rerun()
    test = rr.load_test()
    v88 = rr.scratch_core(test, core_path)
    v87 = test.track0().h.Core("v87", "v85", "v85")
    work = t0.neighbour_tasks()
    found: dict[str, Any] = json.loads(part.read_text(encoding="utf-8")) if part.exists() else {}
    found["_total"] = len(work)

    def one(key: str, acts: Acts) -> None:
        if key in found:
            return
        slug = re.sub(r"[^A-Za-z0-9_.-]", ".", key)[:80]
        answers = aba.implied(acts)
        answered_acts = aba.answered(acts, answers)
        pin87 = rr._pin_run(test, v87, without_condition(answered_acts), "demo.aba.t0.nb.v87." + slug)
        pin88 = rr._pin_run(test, v88, aba.adopt_v88(v88, answered_acts), "demo.aba.t0.nb.v88." + slug)
        row = rr.classify(pin87, pin88)
        row["v87_error"] = pin87.get("error") or pin87.get("refusal")
        row["v88_error"] = pin88.get("error") or pin88.get("refusal")
        row["derived"] = key.startswith("derived-")
        found[key] = row
        part.write_text(json.dumps(found) + "\n", encoding="utf-8")
        print(key, row["class"], flush=True)

    base: tuple[str, Acts] | None = None
    for key, acts in work:
        one(key, acts)
        if base is None and key in found and not found[key].get("v87_error") and found[key]["class"] != "numbers_changed":
            # Prefer a list that already agrees, so the derived returns start from a computing return.
            base = (key, acts)
    if base is None:
        for key, acts in work:
            if key in found and not found[key].get("v87_error"):
                base = (key, acts)
                break
    if base is not None:
        h = probe().harness()
        source, acts = base
        derived = {
            f"derived-joint/{source}": h.say(copy.deepcopy(acts), STATUS, MFJ, "aba-derived-joint"),
            f"derived-separate/{source}": h.say(copy.deepcopy(acts), STATUS, MFS, "aba-derived-separate"),
            f"derived-dependent/{source}": h.say(copy.deepcopy(acts), DEPENDENT, "yes", "aba-derived-dependent"),
        }
        for key, body in derived.items():
            one(key, body)
        found["_derived_from"] = source
        part.write_text(json.dumps(found) + "\n", encoding="utf-8")


def neighbour_merge(part: Path) -> None:
    body = json.loads(part.read_text(encoding="utf-8"))
    derived_from = body.pop("_derived_from", None)
    total = int(body.pop("_total", 0))
    changes = []
    counts: dict[str, int] = {}
    for key, row in sorted(body.items()):
        counts[row["class"]] = counts.get(row["class"], 0) + 1
        if row["class"] != "identical":
            changes.append({"id": key, "class": row["class"], "derived": row.get("derived", False),
                            "lines": row.get("lines"), "v87_error": row.get("v87_error"), "v88_error": row.get("v88_error")})
    same_refusal = sorted(key for key, row in body.items()
                          if row.get("v87_error") and row.get("v87_error") == row.get("v88_error"))
    derived = [{"id": key, "class": row["class"]} for key, row in sorted(body.items()) if key.startswith("derived-")]
    write("track0-neighbour.json", {
        "counts": {"lists": len(body), "recorded": total, "derived": len(derived),
                   **counts, "changes": len(changes), "same_refusal": len(same_refusal)},
        "pass": not any(row["class"] == "numbers_changed" for row in body.values()),
        "derived_from": derived_from,
        "derived": derived,
        "answer_rule": (
            "Each list is answered false for the facts v88 asks and the record leaves unstated, "
            "including the separate-return condition on a separate return."
        ),
        "classes": counts,
        "changes": changes,
        "same_refusal": same_refusal,
    })


def run_neighbour(core_path: Path, part: Path | None = None) -> None:
    """Run the diff in a subprocess. Pass ``part`` to resume a part file that already holds some keys."""
    if part is None:
        part = Path(tempfile.mkdtemp(prefix="aba-t0-neighbour-")) / "part.json"
    part.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run([sys.executable, str(Path(__file__).resolve()), "neighbour-worker", str(core_path), str(part)],
                   check=True)
    neighbour_merge(part)


# ---- item 6: integration surface -------------------------------------------------------


def surface_specs() -> list[dict[str, Any]]:
    return [
        {"id": "surface_single", "status": "single", "ask": TAXPAYER_Q},
        {"id": "surface_joint", "status": MFJ, "ask": ALL_Q},
        {"id": "surface_separate", "status": MFS, "ask": MFS_OPEN},
        {"id": "surface_hoh", "status": HOH, "ask": TAXPAYER_Q},
        {"id": "surface_qss", "status": QSS, "ask": TAXPAYER_Q},
        {"id": "surface_dependent", "status": "single", "dependent": True, "ask": TAXPAYER_Q},
        {"id": "surface_age_answered_blind_open", "status": "single", "ask": ["taxpayer-blind"],
         "bits": (True, None, None, None)},
    ]


def run_surface(core_path: Path, only: str | None) -> None:
    v88 = scratch_v88(core_path)
    words = questions()
    rows = []
    for spec in surface_specs():
        if only and spec["id"] != only:
            continue
        bits = spec.get("bits", (None, None, None, None))
        answers = answers_for(spec["status"], *bits, dependent=bool(spec.get("dependent")))
        acts = build_acts(spec["status"], answers, dependent=bool(spec.get("dependent")))
        measured = run_pair(spec["id"], acts, v88)
        expected = [words[slug] for slug in spec["ask"]]
        v88_result = measured["v88"]
        shown = []
        for slug in spec["ask"]:
            text = words[slug]
            fields = [field for field, sentences in (v88_result.get("field_sentences") or {}).items() if text in sentences]
            shown.append({"slug": slug, "fields": fields, "exact": bool(fields) and text in (v88_result.get("questions") or [])})
        new_fields = sorted(set(v88_result.get("blocked_fields") or []) - set((measured.get("v87") or {}).get("blocked_fields") or []))
        unnamed = []
        foreign = []
        for field in new_fields:
            sentences = (v88_result.get("field_sentences") or {}).get(field) or []
            if not sentences:
                unnamed.append(field)
            elif any(sentence not in expected and sentence not in words.values() for sentence in sentences):
                foreign.append(field)
            elif not any(sentence in expected for sentence in sentences):
                unnamed.append(field)
        failures = []
        if any(not row["exact"] for row in shown):
            failures.append("a question was not shown verbatim")
        if unnamed:
            failures.append(f"newly blocked without a question: {unnamed}")
        if foreign:
            failures.append(f"newly blocked with some other sentence: {foreign}")
        if v88_result.get("asked_slugs") != sorted(spec["ask"]):
            failures.append(f"asked {v88_result.get('asked_slugs')}")
        rows.append({
            "id": spec["id"],
            "ask": spec["ask"],
            "shown": shown,
            "newly_blocked": new_fields,
            "failures": failures,
            "measured": keep(measured),
        })
    finish("track0-surface.json", rows)


def main() -> None:
    args = sys.argv[1:]
    if args[:1] == ["neighbour-worker"] and len(args) == 3:
        neighbour_worker(Path(args[1]), Path(args[2]))
        return
    if len(args) < 2:
        raise SystemExit(__doc__)
    command, core_path = args[0], Path(args[1])
    only = args[2] if len(args) > 2 else None
    commands: dict[str, Callable[..., None]] = {
        "authority": run_authority,
        "matrix": run_matrix,
        "late": run_late,
        "reuse": run_reuse,
        "surface": run_surface,
    }
    if command == "neighbour":
        run_neighbour(core_path, Path(only) if only else None)
        return
    if command not in commands:
        raise SystemExit(__doc__)
    commands[command](core_path, only)


if __name__ == "__main__":
    main()
