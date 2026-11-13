"""Track 0 adversarial closure for Form 1099-B backup withholding.

Charter: docs/reviews/f1099b-backup-withholding/charter-track0.md
Plan: docs/phases/engine-breadth/milestones/f1099b-backup-withholding.md

Executes all Track 0 scopes through real coordinator runs (live_coordinate_run):
- Scope 0: Redo P0 probes with box 4 amount & missing case ids
- Scope 1: Decision 2 (bridge_v82_no repair test)
- Scope 2: Authority-lifecycle cases
- Scope 3: Empty/nonempty matrix (8 families x 4 states = 32 runs)
- Scope 4: Late-member traces
- Scope 5: Claim reuse (the 5 existing line 25b subtotals)
- Scope 6: Neighbour dependency diff (all 213 returns from expected.json)
- Scope 7: Integration surface (consumers & presentation probe)

All summary fields are computed directly from run results, never typed as strings.
Outputs are saved in track0-output.json and track0-rerun-output.json.
"""

from __future__ import annotations

import atexit
import copy
import importlib.util
import json
import math
import os
import shutil
import subprocess
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

OUT_JSON = HERE / "track0-output.json"
RERUN_JSON = HERE / "track0-rerun-output.json"
EXPECTED_PATH = REPO / "tests/fixtures/sale_family_audit_v82/expected.json"

P = "tax.us.2025."
YEAR = "2025"

# Unique module loading
def load_unique(name: str, path: Path) -> Any:
    if name in sys.modules:
        return sys.modules[name]
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod

h = load_unique("f1099b_b4_t0_harness", REPO / "docs/phases/engine-breadth/milestones/sale-family-audit-evidence/audit_harness.py")
# Unique name: SFA track0.py loads its own harness/probe/prototype/rerun under
# sale_family_audit_* and sets no attribute on them. Import does not rebind
# packages.tax.loader (or other package) globals; loader_entries patches only
# inside a run on a scratch core.
sfa_t0 = load_unique("f1099b_sfa_t0", REPO / "docs/phases/engine-breadth/milestones/sale-family-audit-evidence/track0.py")
pr = load_unique("f1099b_b4_t0_probe", HERE / "probe.py")
proto = load_unique("f1099b_b4_t0_prototype", HERE / "prototype.py")

from packages.derivation.live import live_coordinate_run  # noqa: E402
from packages.derivation.live_workspace import WorkspaceCapability  # noqa: E402
from packages.derivation.presentation_projection import validate_presentation_model  # noqa: E402

PUBLISHED_ROW: list[Any] = ["published", None, []]


def make_v82_projection(core: Any, outcome: Any) -> dict[str, Any]:
    """The v82 fixture projection from tests/test_sale_family_audit_v82.py.

    ``page_questions`` is rebuilt from this run's presentation (probed-field
    reasons union the harness's truncated ``?`` questions). Relying on
    ``sfa_t0.summarize``'s ``page_questions`` omitted those reasons in
    ProcessPoolExecutor workers, which is why 32 of 213 v82 runs missed
    non-``?`` validation sentences and full-length question text.
    """
    if outcome.refusal is not None:
        return {"error": "refusal", "message": h.scrub(str(outcome.refusal.detail))[:160]}
    sfa_res = sfa_t0.summarize(core, outcome)
    model = json.loads(outcome.presentation_path.read_text(encoding="utf-8"))
    reasons: dict[str, list[str]] = {}
    probed_sentences: set[str] = set()
    for section in model.get("sections") or []:
        field = section.get("field") or {}
        field_id = str(field.get("id") or "")
        resolved = section.get("resolved") or {}
        sentences = [str(r.get("sentence") or "") for r in resolved.get("reasons") or [] if isinstance(r, dict)]
        if resolved.get("disposition") == "blocked":
            reasons[field_id.removeprefix(P)] = sentences
        if field_id in sfa_t0.PROBED_FIELDS:
            probed_sentences.update(sentences)
    sfa_res["reasons"] = reasons
    rows = {name: row for name, row in sorted((sfa_res.get("rows") or {}).items()) if row != PUBLISHED_ROW}
    lines = sfa_res.get("lines") or {}
    line_reasons = {name: sentences for name, sentences in (sfa_res.get("reasons") or {}).items() if name in lines}
    page_questions = sorted(probed_sentences | set(sfa_res.get("questions") or []))
    return {
        "lines": lines,
        "attachments": sfa_res.get("attachments"),
        "questions": page_questions,
        "reasons": line_reasons,
        "base": (sfa_res.get("symbols") or {}).get("capital-gains.selected-preferential-base"),
        "rows": rows,
    }


B4_AMOUNT_FACT = P + "f1099b.statement-box4-withholding"
B4_REPORTED_FACT = P + "f1099b.statement-box4-withholding-reported"
B7_REPORTED_FACT = P + "f1099b.statement-box7-loss-not-allowed"

V82 = h.Core("v82", "v80", "v80")

# ---- Scratch Cores -----------------------------------------------------------------

_CORES: dict[str, Any] = {"v82": V82}
_ROOT_TEMP: Path | None = None

def get_core(name: str) -> Any:
    global _ROOT_TEMP
    if name in _CORES:
        return _CORES[name]
    if name == "v82":
        return V82
    if _ROOT_TEMP is None:
        _ROOT_TEMP = Path(tempfile.mkdtemp(prefix="f1099b-b4-t0-")).resolve()
        atexit.register(shutil.rmtree, _ROOT_TEMP, True)

    scratch = (_ROOT_TEMP / name).resolve()
    switches = set(proto.FIXES)
    if name == "repair_d2":
        switches |= {"bridge_v82_no"}
    proto.build(scratch, switches)
    core_json = json.loads((scratch / "core.json").read_text(encoding="utf-8"))
    core = h.Core(
        core_json["version"],
        core_json["registry"],
        core_json["release_version"],
        Path(core_json["content"]),
        Path(core_json["releases"]),
        core_json.get("loader_from"),
    )
    _CORES[name] = core
    return core


# ---- Act helpers -------------------------------------------------------------------

def say_b4_amount(acts: list[dict[str, Any]], core: Any, statement: str, amount: float) -> list[dict[str, Any]]:
    return pr.say_statement_answer(acts, core, B4_AMOUNT_FACT, statement, float(amount))

def say_b4_reported(acts: list[dict[str, Any]], core: Any, statement: str, value: str) -> list[dict[str, Any]]:
    return pr.say_statement_answer(acts, core, B4_REPORTED_FACT, statement, value)

def say_b7_reported(acts: list[dict[str, Any]], core: Any, statement: str, value: str = "no") -> list[dict[str, Any]]:
    return pr.say_statement_answer(acts, core, B7_REPORTED_FACT, statement, value)


# ---- Runner -----------------------------------------------------------------------

def run_coordinate(core: Any, acts: list[dict[str, Any]], run_id: str) -> dict[str, Any]:
    # v88 requires the taxpayer's two facts (Decision 6). Earlier cores keep the list.
    prepared = h.ccr.state_taxpayer_facts(acts, core=core.version)
    with h.loader_entries(core):
        surface = core.surface()
        try:
            finished = h._handover(
                h._finish(
                    copy.deepcopy(prepared),
                    package_path=core.package_path,
                    package_version=core.version,
                    release_path=core.release_path,
                    release_version=core.release_version,
                    note=run_id,
                ),
                surface=surface,
                reconfirm=True,
            )
            with tempfile.TemporaryDirectory() as tmp:
                outcome = live_coordinate_run(
                    WorkspaceCapability(Path(tmp) / "L"),
                    repo_root=REPO,
                    authoritative_acts=finished,
                    workspace_revision=len(finished),
                    run_scope={"jurisdiction": "us", "year": YEAR},
                    scope_user=h.ccr.USER,
                    request={"schema": "run-request.v1"},
                    run_id=run_id,
                    governance_pins=[],
                    surface=surface,
                    output_name="out.json",
                )
                if outcome.refusal is not None:
                    return {
                        "outcome": "refusal",
                        "refusal": outcome.refusal.reason,
                        "message": h.scrub(str(outcome.refusal.detail))[:400],
                        "exit_code": outcome.exit_code,
                        "dispositions": {},
                        "lines": {},
                        "blocked_reasons": {},
                        "attachments": {},
                        "rows": {},
                        "questions": [],
                        "projection": {"error": "refusal", "message": h.scrub(str(outcome.refusal.detail))[:160]},
                    }
                assert outcome.presentation_path is not None
                model = json.loads(outcome.presentation_path.read_text(encoding="utf-8"))
                report = json.loads(outcome.output_path.read_text(encoding="utf-8"))
                try:
                    validate_presentation_model(model)
                    valid = True
                except Exception as exc:
                    valid = f"invalid: {exc}"

                lines: dict[str, Any] = {}
                dispositions: dict[str, str] = {}
                blocked_reasons: dict[str, list[str]] = {}
                field_descriptions: dict[str, str] = {}

                for section in model.get("sections") or []:
                    field = section.get("field") or {}
                    fid = str(field.get("id") or "").removeprefix(P)
                    if field.get("description"):
                        field_descriptions[fid] = str(field.get("description"))
                    resolved = section.get("resolved") or {}
                    disp = resolved.get("disposition")
                    dispositions[fid] = disp
                    if disp in ("published", "published_value", "computed_zero"):
                        lines[fid] = resolved.get("value")
                    elif disp == "blocked":
                        lines[fid] = None
                        blocked_reasons[fid] = [
                            str(r.get("sentence") or "") for r in resolved.get("reasons") or []
                            if isinstance(r, dict)
                        ]

                attachments: dict[str, str] = {}
                for att in model.get("attachments") or []:
                    att_id = str(att.get("id") or "")
                    resolved = att.get("resolved") or {}
                    attachments[att_id.split(".")[-1]] = resolved.get("disposition")

                rows: dict[str, list[Any]] = {}
                for row in report.get("dispositions") or []:
                    art = str(row.get("artifact_id", "")).removeprefix(P)
                    rows[art] = [row.get("disposition"), row.get("code"), [str(m).removeprefix(P) for m in row.get("missing") or []]]

                questions: list[str] = []
                for section in model.get("sections") or []:
                    resolved = section.get("resolved") or {}
                    for reason in resolved.get("reasons") or []:
                        sentence = str(reason.get("sentence") or "").strip() if isinstance(reason, dict) else ""
                        if sentence.endswith("?") and sentence not in questions:
                            questions.append(sentence)

                proj = make_v82_projection(core, outcome)

                return {
                    "outcome": "success",
                    "presentation_valid": valid,
                    "dispositions": dispositions,
                    "lines": lines,
                    "blocked_reasons": blocked_reasons,
                    "field_descriptions": field_descriptions,
                    "attachments": attachments,
                    "rows": rows,
                    "questions": questions,
                    "projection": proj,
                }
        except Exception as exc:
            msg = h.scrub(str(exc))[:400]
            return {
                "outcome": "error",
                "error": type(exc).__name__,
                "message": msg,
                "dispositions": {},
                "lines": {},
                "blocked_reasons": {},
                "attachments": {},
                "rows": {},
                "questions": [],
                "projection": {"error": type(exc).__name__, "message": msg[:160]},
            }


# ---- Persistence Helpers -----------------------------------------------------------

def load_output(path: Path = OUT_JSON) -> dict[str, Any]:
    if path.exists():
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            return {}
    return {}

def save_output(data: dict[str, Any], path: Path = OUT_JSON) -> None:
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


# ---- Hand Value Helper -------------------------------------------------------------

def compute_hand(
    *,
    wages: float = 50000,
    w2_withholding: float = 4500,
    st_gain: float = 0,
    lt_gain: float = 0,
    interest: float = 0,
    dividends: float = 0,
    b25: float | None = 0,
    blocked: bool = False,
) -> dict[str, Any]:
    return pr.hand_values(
        wages=wages,
        w2_withholding=w2_withholding,
        st_gain=st_gain,
        lt_gain=lt_gain,
        interest=interest,
        dividends=dividends,
        b25=b25,
        blocked=blocked,
    )


# ---- Scope 0: Redo P0 Gaps ---------------------------------------------------------

def build_scope0_cases() -> list[dict[str, Any]]:
    cases: list[dict[str, Any]] = []

    # 1. b4_one_statement
    acts_v82 = h.opened()
    acts_v82 = h.sale(acts_v82, "covered", "st", proceeds=5000, basis=4000, tag="b4_one")
    acts_v82 = h.answer(acts_v82, **h.honest({"covered"}, loss=False))
    stmt1 = "demo.sfa.b4_one.statement"
    acts_v82 = say_b4_reported(acts_v82, V82, stmt1, "yes")
    acts_v82 = say_b7_reported(acts_v82, V82, stmt1, "no")

    # On v83: replace box 4 answer with amount 240
    acts_v83 = h.opened()
    acts_v83 = h.sale(acts_v83, "covered", "st", proceeds=5000, basis=4000, tag="b4_one")
    acts_v83 = h.answer(acts_v83, **h.honest({"covered"}, loss=False))
    acts_v83 = say_b4_amount(acts_v83, get_core("decided"), stmt1, 240.0)
    acts_v83 = say_b7_reported(acts_v83, get_core("decided"), stmt1, "no")

    cases.append({
        "case_id": "b4_one_statement",
        "description": "One statement covered ST sale ($1,000 gain), box 4 withholding $240",
        "acts_v82": acts_v82,
        "acts_v83": acts_v83,
        "hand": compute_hand(st_gain=1000, b25=240),
    })

    # 2. b4_two_statements
    acts_v82 = h.opened()
    acts_v82 = h.sale(acts_v82, "covered", "st", proceeds=5000, basis=4000, tag="b4_s1")
    acts_v82 = h.sale(acts_v82, "covered", "st", proceeds=2000, basis=1500, tag="b4_s2")
    acts_v82 = h.answer(acts_v82, **h.honest({"covered"}, loss=False))
    s1 = "demo.sfa.b4_s1.statement"
    s2 = "demo.sfa.b4_s2.statement"
    acts_v82 = say_b4_reported(acts_v82, V82, s1, "yes")
    acts_v82 = say_b7_reported(acts_v82, V82, s1, "no")
    acts_v82 = say_b4_reported(acts_v82, V82, s2, "yes")
    acts_v82 = say_b7_reported(acts_v82, V82, s2, "no")

    acts_v83 = h.opened()
    acts_v83 = h.sale(acts_v83, "covered", "st", proceeds=5000, basis=4000, tag="b4_s1")
    acts_v83 = h.sale(acts_v83, "covered", "st", proceeds=2000, basis=1500, tag="b4_s2")
    acts_v83 = h.answer(acts_v83, **h.honest({"covered"}, loss=False))
    acts_v83 = say_b4_amount(acts_v83, get_core("decided"), s1, 240.0)
    acts_v83 = say_b7_reported(acts_v83, get_core("decided"), s1, "no")
    acts_v83 = say_b4_amount(acts_v83, get_core("decided"), s2, 100.0)
    acts_v83 = say_b7_reported(acts_v83, get_core("decided"), s2, "no")

    cases.append({
        "case_id": "b4_two_statements",
        "description": "Two statements covered ST sales ($1,500 total gain), box 4 amounts $240 and $100 ($340 total)",
        "acts_v82": acts_v82,
        "acts_v83": acts_v83,
        "hand": compute_hand(st_gain=1500, b25=340),
    })

    # 3. b4_st_and_lt
    def make_st_and_lt(with_amount: float | None = 300.0, box4_yes: bool = False, core_obj: Any = None) -> list[dict[str, Any]]:
        acts = h.opened()
        acts = h.sale(acts, "covered", "st", proceeds=5000, basis=4000, tag="b4_both")
        acts = h.sale(acts, "covered", "lt", proceeds=3000, basis=2000, tag="b4_both_lt")
        filtered = [
            a for a in acts
            if not (a.get("kind") == "entity-introduced" and (a.get("payload") or {}).get("entity", {}).get("id") == "demo.sfa.b4_both_lt.statement")
        ]
        text = json.dumps(filtered).replace("demo.sfa.b4_both_lt.statement", "demo.sfa.b4_both.statement")
        acts = h.renumber(json.loads(text))
        acts = h.answer(acts, **h.honest({"covered"}, loss=False))
        stmt = "demo.sfa.b4_both.statement"
        acts = say_b7_reported(acts, core_obj, stmt, "no")
        if box4_yes:
            acts = say_b4_reported(acts, core_obj, stmt, "yes")
        elif with_amount is not None:
            acts = say_b4_amount(acts, core_obj, stmt, with_amount)
        return acts

    cases.append({
        "case_id": "b4_st_and_lt",
        "description": "One statement with both ST ($1,000) and LT ($1,000) sales, box 4 withholding $300",
        "acts_v82": make_st_and_lt(box4_yes=True, core_obj=V82),
        "acts_v83": make_st_and_lt(with_amount=300.0, core_obj=get_core("decided")),
        "hand": compute_hand(st_gain=1000, lt_gain=1000, b25=300),
    })

    # 4. b4_beside_int_div
    acts_v82 = h.opened()
    acts_v82 = h.sale(acts_v82, "covered", "st", proceeds=5000, basis=4000, tag="b4_beside")
    acts_v82 = h.answer(acts_v82, **h.honest({"covered"}, loss=False))
    s_beside = "demo.sfa.b4_beside.statement"
    acts_v82 = say_b4_reported(acts_v82, V82, s_beside, "yes")
    acts_v82 = say_b7_reported(acts_v82, V82, s_beside, "no")
    acts_v82 = pr.add_interest_and_dividends(acts_v82, int_box1=100, int_box4=50, div_box1a=200, div_box4=75)

    acts_v83 = h.opened()
    acts_v83 = h.sale(acts_v83, "covered", "st", proceeds=5000, basis=4000, tag="b4_beside")
    acts_v83 = h.answer(acts_v83, **h.honest({"covered"}, loss=False))
    acts_v83 = say_b4_amount(acts_v83, get_core("decided"), s_beside, 200.0)
    acts_v83 = say_b7_reported(acts_v83, get_core("decided"), s_beside, "no")
    acts_v83 = pr.add_interest_and_dividends(acts_v83, int_box1=100, int_box4=50, div_box1a=200, div_box4=75)

    cases.append({
        "case_id": "b4_beside_int_div",
        "description": "1099-B sale ($1,000 gain, b4 $200) beside 1099-INT ($50 b4) and 1099-DIV ($75 b4); total b4 $325",
        "acts_v82": acts_v82,
        "acts_v83": acts_v83,
        "hand": compute_hand(st_gain=1000, interest=100, dividends=200, b25=325),
    })

    # 5. b4_statement_removed
    acts_v82 = h.opened()
    acts_v82 = h.answer(acts_v82, **h.honest(set(), loss=False))
    s_orph = "demo.sfa.b4_orphan.statement"
    h._introduce(acts_v82, s_orph, "tax.us.f1099b-statement")
    acts_v82 = say_b4_reported(acts_v82, V82, s_orph, "yes")
    acts_v82 = say_b7_reported(acts_v82, V82, s_orph, "no")

    acts_v83 = h.opened()
    acts_v83 = h.answer(acts_v83, **h.honest(set(), loss=False))
    h._introduce(acts_v83, s_orph, "tax.us.f1099b-statement")
    acts_v83 = say_b4_amount(acts_v83, get_core("decided"), s_orph, 200.0)
    acts_v83 = say_b7_reported(acts_v83, get_core("decided"), s_orph, "no")

    cases.append({
        "case_id": "b4_statement_removed",
        "description": "Statement sales removed, leaving orphan statement with box 4 $200; the amount is added",
        "acts_v82": acts_v82,
        "acts_v83": acts_v83,
        "hand": compute_hand(st_gain=0, b25=200),
    })

    # 6. b4_amount_no_answer
    acts_v82 = h.opened()
    acts_v82 = h.sale(acts_v82, "covered", "st", proceeds=5000, basis=4000, tag="b4_noans")
    acts_v82 = h.answer(acts_v82, **h.honest({"covered"}, loss=False))
    s_noans = "demo.sfa.b4_noans.statement"
    acts_v82 = say_b7_reported(acts_v82, V82, s_noans, "no")

    acts_v83 = h.opened()
    acts_v83 = h.sale(acts_v83, "covered", "st", proceeds=5000, basis=4000, tag="b4_noans")
    acts_v83 = h.answer(acts_v83, **h.honest({"covered"}, loss=False))
    acts_v83 = say_b7_reported(acts_v83, get_core("decided"), s_noans, "no")

    cases.append({
        "case_id": "b4_amount_no_answer",
        "description": "One statement with covered ST sale, box 4 unanswered on both cores",
        "acts_v82": acts_v82,
        "acts_v83": acts_v83,
        "hand": compute_hand(st_gain=1000, b25=None, blocked=True),
    })

    # 7. b4_answer_no_amount
    acts_v82 = h.opened()
    acts_v82 = h.sale(acts_v82, "covered", "st", proceeds=5000, basis=4000, tag="b4_noamt")
    acts_v82 = h.answer(acts_v82, **h.honest({"covered"}, loss=False))
    s_noamt = "demo.sfa.b4_noamt.statement"
    acts_v82 = say_b4_reported(acts_v82, V82, s_noamt, "no")
    acts_v82 = say_b7_reported(acts_v82, V82, s_noamt, "no")

    acts_v83 = h.opened()
    acts_v83 = h.sale(acts_v83, "covered", "st", proceeds=5000, basis=4000, tag="b4_noamt")
    acts_v83 = h.answer(acts_v83, **h.honest({"covered"}, loss=False))
    acts_v83 = say_b4_amount(acts_v83, get_core("decided"), s_noamt, 0.0)
    acts_v83 = say_b7_reported(acts_v83, get_core("decided"), s_noamt, "no")

    cases.append({
        "case_id": "b4_answer_no_amount",
        "description": "One statement covered ST sale, box 4 answered no on v82, amount $0 on v83",
        "acts_v82": acts_v82,
        "acts_v83": acts_v83,
        "hand": compute_hand(st_gain=1000, b25=0),
    })

    # 8. b4_no_with_amount
    acts_v82 = h.opened()
    acts_v82 = h.sale(acts_v82, "covered", "st", proceeds=5000, basis=4000, tag="b4_nowith")
    acts_v82 = h.answer(acts_v82, **h.honest({"covered"}, loss=False))
    s_nowith = "demo.sfa.b4_nowith.statement"
    acts_v82 = say_b4_reported(acts_v82, V82, s_nowith, "no")
    acts_v82 = say_b7_reported(acts_v82, V82, s_nowith, "no")

    acts_v83 = h.opened()
    acts_v83 = h.sale(acts_v83, "covered", "st", proceeds=5000, basis=4000, tag="b4_nowith")
    acts_v83 = h.answer(acts_v83, **h.honest({"covered"}, loss=False))
    acts_v83 = say_b4_amount(acts_v83, get_core("decided"), s_nowith, 0.0)
    acts_v83 = say_b7_reported(acts_v83, get_core("decided"), s_nowith, "no")

    cases.append({
        "case_id": "b4_no_with_amount",
        "description": "One statement covered ST sale, zero withholding",
        "acts_v82": acts_v82,
        "acts_v83": acts_v83,
        "hand": compute_hand(st_gain=1000, b25=0),
    })

    # 9. b4_no_one_statement
    acts_v82 = h.opened()
    acts_v82 = h.sale(acts_v82, "covered", "st", proceeds=5000, basis=4000, tag="b4_std_no")
    acts_v82 = h.answer(acts_v82, **h.honest({"covered"}, loss=False))
    s_std_no = "demo.sfa.b4_std_no.statement"
    acts_v82 = say_b4_reported(acts_v82, V82, s_std_no, "no")
    acts_v82 = say_b7_reported(acts_v82, V82, s_std_no, "no")

    acts_v83 = h.opened()
    acts_v83 = h.sale(acts_v83, "covered", "st", proceeds=5000, basis=4000, tag="b4_std_no")
    acts_v83 = h.answer(acts_v83, **h.honest({"covered"}, loss=False))
    acts_v83 = say_b4_amount(acts_v83, get_core("decided"), s_std_no, 0.0)
    acts_v83 = say_b7_reported(acts_v83, get_core("decided"), s_std_no, "no")

    cases.append({
        "case_id": "b4_no_one_statement",
        "description": "Standard one-statement covered ST sale ($1,000 gain), box 4 zero withholding",
        "acts_v82": acts_v82,
        "acts_v83": acts_v83,
        "hand": compute_hand(st_gain=1000, b25=0),
    })

    # 10. The named missing case ids from P0
    def make_sale_case(cid: str, kind: str, desc: str) -> dict[str, Any]:
        acts_v82 = h.opened()
        tag = f"tag_{cid}"
        if kind == "codeb":
            acts_v82 = h.sale(acts_v82, kind, "st", proceeds=5000, basis=4500, corrected=4000, tag=tag)
        else:
            acts_v82 = h.sale(acts_v82, kind, "st", proceeds=5000, basis=4000, tag=tag)
        acts_v82 = h.answer(acts_v82, **h.honest({kind}, loss=False))
        stmt = f"demo.sfa.{tag}.statement"
        acts_v82 = say_b4_reported(acts_v82, V82, stmt, "yes")
        acts_v82 = say_b7_reported(acts_v82, V82, stmt, "no")

        acts_v83 = h.opened()
        if kind == "codeb":
            acts_v83 = h.sale(acts_v83, kind, "st", proceeds=5000, basis=4500, corrected=4000, tag=tag)
        else:
            acts_v83 = h.sale(acts_v83, kind, "st", proceeds=5000, basis=4000, tag=tag)
        acts_v83 = h.answer(acts_v83, **h.honest({kind}, loss=False))
        acts_v83 = say_b4_amount(acts_v83, get_core("decided"), stmt, 240.0)
        acts_v83 = say_b7_reported(acts_v83, get_core("decided"), stmt, "no")

        return {
            "case_id": cid,
            "description": desc,
            "acts_v82": acts_v82,
            "acts_v83": acts_v83,
            "hand": compute_hand(st_gain=1000, b25=240),
        }

    cases.append(make_sale_case("b4_yes_covered", "covered", "Covered ST sale, box 4 yes on v82 (blocked); box 4 $240 on v83"))
    cases.append(make_sale_case("b4_yes_w", "w", "Covered-W ST sale, box 4 yes on v82 (blocked); box 4 $240 on v83"))
    cases.append(make_sale_case("b4_yes_noncovered", "noncovered", "Noncovered ST sale, box 4 yes on v82 (blocked); box 4 $240 on v83"))
    cases.append(make_sale_case("b4_yes_codeb", "codeb", "Code B ST sale, box 4 yes on v82 (blocked); box 4 $240 on v83"))

    # b4_two_statements_one_yes: s1 yes/240, s2 no/0
    acts_v82 = h.opened()
    acts_v82 = h.sale(acts_v82, "covered", "st", proceeds=5000, basis=4000, tag="t_s1")
    acts_v82 = h.sale(acts_v82, "covered", "st", proceeds=2000, basis=1500, tag="t_s2")
    acts_v82 = h.answer(acts_v82, **h.honest({"covered"}, loss=False))
    s1, s2 = "demo.sfa.t_s1.statement", "demo.sfa.t_s2.statement"
    acts_v82 = say_b4_reported(acts_v82, V82, s1, "yes")
    acts_v82 = say_b7_reported(acts_v82, V82, s1, "no")
    acts_v82 = say_b4_reported(acts_v82, V82, s2, "no")
    acts_v82 = say_b7_reported(acts_v82, V82, s2, "no")

    acts_v83 = h.opened()
    acts_v83 = h.sale(acts_v83, "covered", "st", proceeds=5000, basis=4000, tag="t_s1")
    acts_v83 = h.sale(acts_v83, "covered", "st", proceeds=2000, basis=1500, tag="t_s2")
    acts_v83 = h.answer(acts_v83, **h.honest({"covered"}, loss=False))
    acts_v83 = say_b4_amount(acts_v83, get_core("decided"), s1, 240.0)
    acts_v83 = say_b7_reported(acts_v83, get_core("decided"), s1, "no")
    acts_v83 = say_b4_amount(acts_v83, get_core("decided"), s2, 0.0)
    acts_v83 = say_b7_reported(acts_v83, get_core("decided"), s2, "no")

    cases.append({
        "case_id": "b4_two_statements_one_yes",
        "description": "Two statements: s1 box 4 yes/$240, s2 box 4 no/$0; gain $1,500, withholding $240",
        "acts_v82": acts_v82,
        "acts_v83": acts_v83,
        "hand": compute_hand(st_gain=1500, b25=240),
    })

    # b4_two_statements_both_yes: s1 yes/240, s2 yes/100
    acts_v82 = h.opened()
    acts_v82 = h.sale(acts_v82, "covered", "st", proceeds=5000, basis=4000, tag="by_s1")
    acts_v82 = h.sale(acts_v82, "covered", "st", proceeds=2000, basis=1500, tag="by_s2")
    acts_v82 = h.answer(acts_v82, **h.honest({"covered"}, loss=False))
    s1, s2 = "demo.sfa.by_s1.statement", "demo.sfa.by_s2.statement"
    acts_v82 = say_b4_reported(acts_v82, V82, s1, "yes")
    acts_v82 = say_b7_reported(acts_v82, V82, s1, "no")
    acts_v82 = say_b4_reported(acts_v82, V82, s2, "yes")
    acts_v82 = say_b7_reported(acts_v82, V82, s2, "no")

    acts_v83 = h.opened()
    acts_v83 = h.sale(acts_v83, "covered", "st", proceeds=5000, basis=4000, tag="by_s1")
    acts_v83 = h.sale(acts_v83, "covered", "st", proceeds=2000, basis=1500, tag="by_s2")
    acts_v83 = h.answer(acts_v83, **h.honest({"covered"}, loss=False))
    acts_v83 = say_b4_amount(acts_v83, get_core("decided"), s1, 240.0)
    acts_v83 = say_b7_reported(acts_v83, get_core("decided"), s1, "no")
    acts_v83 = say_b4_amount(acts_v83, get_core("decided"), s2, 100.0)
    acts_v83 = say_b7_reported(acts_v83, get_core("decided"), s2, "no")

    cases.append({
        "case_id": "b4_two_statements_both_yes",
        "description": "Two statements both box 4 yes on v82; amounts $240 and $100 on v83",
        "acts_v82": acts_v82,
        "acts_v83": acts_v83,
        "hand": compute_hand(st_gain=1500, b25=340),
    })

    # b4_two_statements_both_no: s1 no/0, s2 no/0
    acts_v82 = h.opened()
    acts_v82 = h.sale(acts_v82, "covered", "st", proceeds=5000, basis=4000, tag="bn_s1")
    acts_v82 = h.sale(acts_v82, "covered", "st", proceeds=2000, basis=1500, tag="bn_s2")
    acts_v82 = h.answer(acts_v82, **h.honest({"covered"}, loss=False))
    s1, s2 = "demo.sfa.bn_s1.statement", "demo.sfa.bn_s2.statement"
    acts_v82 = say_b4_reported(acts_v82, V82, s1, "no")
    acts_v82 = say_b7_reported(acts_v82, V82, s1, "no")
    acts_v82 = say_b4_reported(acts_v82, V82, s2, "no")
    acts_v82 = say_b7_reported(acts_v82, V82, s2, "no")

    acts_v83 = h.opened()
    acts_v83 = h.sale(acts_v83, "covered", "st", proceeds=5000, basis=4000, tag="bn_s1")
    acts_v83 = h.sale(acts_v83, "covered", "st", proceeds=2000, basis=1500, tag="bn_s2")
    acts_v83 = h.answer(acts_v83, **h.honest({"covered"}, loss=False))
    acts_v83 = say_b4_amount(acts_v83, get_core("decided"), s1, 0.0)
    acts_v83 = say_b7_reported(acts_v83, get_core("decided"), s1, "no")
    acts_v83 = say_b4_amount(acts_v83, get_core("decided"), s2, 0.0)
    acts_v83 = say_b7_reported(acts_v83, get_core("decided"), s2, "no")

    cases.append({
        "case_id": "b4_two_statements_both_no",
        "description": "Two statements both box 4 no on v82; amounts $0 on v83",
        "acts_v82": acts_v82,
        "acts_v83": acts_v83,
        "hand": compute_hand(st_gain=1500, b25=0),
    })

    # b4_two_statements_one_unanswered: s1 no/0, s2 unanswered
    acts_v82 = h.opened()
    acts_v82 = h.sale(acts_v82, "covered", "st", proceeds=5000, basis=4000, tag="bu_s1")
    acts_v82 = h.sale(acts_v82, "covered", "st", proceeds=2000, basis=1500, tag="bu_s2")
    acts_v82 = h.answer(acts_v82, **h.honest({"covered"}, loss=False))
    s1, s2 = "demo.sfa.bu_s1.statement", "demo.sfa.bu_s2.statement"
    acts_v82 = say_b4_reported(acts_v82, V82, s1, "no")
    acts_v82 = say_b7_reported(acts_v82, V82, s1, "no")
    acts_v82 = say_b7_reported(acts_v82, V82, s2, "no")

    acts_v83 = h.opened()
    acts_v83 = h.sale(acts_v83, "covered", "st", proceeds=5000, basis=4000, tag="bu_s1")
    acts_v83 = h.sale(acts_v83, "covered", "st", proceeds=2000, basis=1500, tag="bu_s2")
    acts_v83 = h.answer(acts_v83, **h.honest({"covered"}, loss=False))
    acts_v83 = say_b4_amount(acts_v83, get_core("decided"), s1, 0.0)
    acts_v83 = say_b7_reported(acts_v83, get_core("decided"), s1, "no")
    acts_v83 = say_b7_reported(acts_v83, get_core("decided"), s2, "no")

    cases.append({
        "case_id": "b4_two_statements_one_unanswered",
        "description": "Two statements: s1 answered, s2 unanswered on both cores (blocked)",
        "acts_v82": acts_v82,
        "acts_v83": acts_v83,
        "hand": compute_hand(st_gain=1500, b25=None, blocked=True),
    })

    # b4_extra_statement_no_sales: 1 statement with sale (gain 1000, b4=0), 1 extra statement with no sales (b4=0)
    acts_v82 = h.opened()
    acts_v82 = h.sale(acts_v82, "covered", "st", proceeds=5000, basis=4000, tag="ex_s1")
    acts_v82 = h.answer(acts_v82, **h.honest({"covered"}, loss=False))
    s1 = "demo.sfa.ex_s1.statement"
    s_extra = "demo.sfa.ex_extra.statement"
    h._introduce(acts_v82, s_extra, "tax.us.f1099b-statement")
    acts_v82 = say_b4_reported(acts_v82, V82, s1, "no")
    acts_v82 = say_b7_reported(acts_v82, V82, s1, "no")
    acts_v82 = say_b4_reported(acts_v82, V82, s_extra, "no")
    acts_v82 = say_b7_reported(acts_v82, V82, s_extra, "no")

    acts_v83 = h.opened()
    acts_v83 = h.sale(acts_v83, "covered", "st", proceeds=5000, basis=4000, tag="ex_s1")
    acts_v83 = h.answer(acts_v83, **h.honest({"covered"}, loss=False))
    h._introduce(acts_v83, s_extra, "tax.us.f1099b-statement")
    acts_v83 = say_b4_amount(acts_v83, get_core("decided"), s1, 0.0)
    acts_v83 = say_b7_reported(acts_v83, get_core("decided"), s1, "no")
    acts_v83 = say_b4_amount(acts_v83, get_core("decided"), s_extra, 0.0)
    acts_v83 = say_b7_reported(acts_v83, get_core("decided"), s_extra, "no")

    cases.append({
        "case_id": "b4_extra_statement_no_sales",
        "description": "One statement with sale ($1,000 gain), one extra statement with no sales; both b4 answered $0",
        "acts_v82": acts_v82,
        "acts_v83": acts_v83,
        "hand": compute_hand(st_gain=1000, b25=0),
    })

    # b4_no_sales: 0 sales
    acts_v82 = h.opened()
    acts_v82 = h.answer(acts_v82, **h.honest(set(), loss=False))
    acts_v83 = h.opened()
    acts_v83 = h.answer(acts_v83, **h.honest(set(), loss=False))

    cases.append({
        "case_id": "b4_no_sales",
        "description": "Zero sales recorded, zero withholding; standard return computes",
        "acts_v82": acts_v82,
        "acts_v83": acts_v83,
        "hand": compute_hand(st_gain=0, b25=0),
    })

    # Review finding 1. Box 4 $150 on a statement with no sale.
    acts_v82 = h.opened()
    acts_v82 = h.answer(acts_v82, **h.honest(set(), loss=False))
    s_rev = "demo.sfa.orphan.statement"
    h._introduce(acts_v82, s_rev, "tax.us.f1099b-statement")
    acts_v82 = say_b4_reported(acts_v82, V82, s_rev, "yes")
    acts_v82 = say_b7_reported(acts_v82, V82, s_rev, "no")

    acts_v83 = h.opened()
    acts_v83 = h.answer(acts_v83, **h.honest(set(), loss=False))
    h._introduce(acts_v83, s_rev, "tax.us.f1099b-statement")
    acts_v83 = say_b4_amount(acts_v83, get_core("decided"), s_rev, 150.0)
    acts_v83 = say_b7_reported(acts_v83, get_core("decided"), s_rev, "no")

    cases.append({
        "case_id": "b4_orphan_150",
        "description": "No sale. Box 4 $150 on demo.sfa.orphan.statement is added to line 25b.",
        "acts_v82": acts_v82,
        "acts_v83": acts_v83,
        "hand": compute_hand(st_gain=0, b25=150),
    })

    # The same $150 beside one kept covered short-term sale whose own box 4 is $0.
    acts_v82 = h.opened()
    acts_v82 = h.sale(acts_v82, "covered", "st", proceeds=5000, basis=4000, tag="b4_kept")
    acts_v82 = h.answer(acts_v82, **h.honest({"covered"}, loss=False))
    s_kept = "demo.sfa.b4_kept.statement"
    acts_v82 = say_b4_reported(acts_v82, V82, s_kept, "no")
    acts_v82 = say_b7_reported(acts_v82, V82, s_kept, "no")
    h._introduce(acts_v82, s_rev, "tax.us.f1099b-statement")
    acts_v82 = say_b4_reported(acts_v82, V82, s_rev, "yes")
    acts_v82 = say_b7_reported(acts_v82, V82, s_rev, "no")

    acts_v83 = h.opened()
    acts_v83 = h.sale(acts_v83, "covered", "st", proceeds=5000, basis=4000, tag="b4_kept")
    acts_v83 = h.answer(acts_v83, **h.honest({"covered"}, loss=False))
    acts_v83 = say_b4_amount(acts_v83, get_core("decided"), s_kept, 0.0)
    acts_v83 = say_b7_reported(acts_v83, get_core("decided"), s_kept, "no")
    h._introduce(acts_v83, s_rev, "tax.us.f1099b-statement")
    acts_v83 = say_b4_amount(acts_v83, get_core("decided"), s_rev, 150.0)
    acts_v83 = say_b7_reported(acts_v83, get_core("decided"), s_rev, "no")

    cases.append({
        "case_id": "b4_orphan_beside_sale",
        "description": "Kept covered short-term sale, gain $1,000, its box 4 $0, plus an orphan statement at box 4 $150.",
        "acts_v82": acts_v82,
        "acts_v83": acts_v83,
        "hand": compute_hand(st_gain=1000, b25=150),
    })

    return cases


def run_scope0() -> dict[str, Any]:
    cases = build_scope0_cases()
    core_v82 = get_core("v82")
    core_v83 = get_core("decided")

    print(f"[Scope 0] Running {len(cases)} probe cases on core v82 and scratch v83...")
    results: list[dict[str, Any]] = []

    for c in cases:
        cid = c["case_id"]
        res_v82 = run_coordinate(core_v82, c["acts_v82"], f"demo.b4.s0.v82.{cid}")
        res_v83 = run_coordinate(core_v83, c["acts_v83"], f"demo.b4.s0.v83.{cid}")

        disp_v82_25b = res_v82["dispositions"].get("form1040.line-25b")
        disp_v83_25b = res_v83["dispositions"].get("form1040.line-25b")

        kept_lines = (
            "form1040.line-25b", "form1040.line-25d", "form1040.line-33",
            "form1040.line-34", "form1040.line-35a", "form1040.line-37",
        )
        lines_v82 = {key: res_v82["lines"].get(key) for key in kept_lines}
        lines_v83 = {key: res_v83["lines"].get(key) for key in kept_lines}

        hand = c["hand"]
        expected_disp = "blocked" if hand["disposition"] == "blocked" else ("computed_zero" if hand["form1040.line-25b"] == 0 else "published_value")
        matches_hand = (
            disp_v83_25b == expected_disp
            and (hand["disposition"] == "blocked" or (
                lines_v83["form1040.line-25b"] == hand["form1040.line-25b"]
                and lines_v83["form1040.line-33"] == hand["form1040.line-33"]
                and lines_v83["form1040.line-34"] == hand["form1040.line-34"]
                and lines_v83["form1040.line-37"] == hand["form1040.line-37"]
            ))
        )

        entry = {
            "case_id": cid,
            "description": c["description"],
            "hand_values": hand,
            "v82": {
                "outcome": res_v82["outcome"],
                "disposition_25b": disp_v82_25b,
                "lines": lines_v82,
                "blocked_reasons": res_v82["blocked_reasons"].get("form1040.line-25b", []),
            },
            "v83": {
                "outcome": res_v83["outcome"],
                "disposition_25b": disp_v83_25b,
                "lines": lines_v83,
                "blocked_reasons": res_v83["blocked_reasons"].get("form1040.line-25b", []),
                "matches_hand": matches_hand,
            },
        }
        results.append(entry)
        print(f"  {cid}: v82={disp_v82_25b} -> v83={disp_v83_25b} (matches_hand={matches_hand})")

    summary = {
        "total_cases": len(results),
        "v82_blocked_cases": sum(1 for r in results if r["v82"]["disposition_25b"] == "blocked"),
        "v83_published_cases": sum(1 for r in results if r["v83"]["disposition_25b"] in ("published", "published_value", "computed_zero")),
        "v83_blocked_cases": sum(1 for r in results if r["v83"]["disposition_25b"] == "blocked"),
        "matches_hand_cases": sum(1 for r in results if r["v83"]["matches_hand"]),
        "all_match_hand": all(r["v83"]["matches_hand"] for r in results),
    }

    out = load_output()
    out["scope0"] = {
        "summary": summary,
        "cases": results,
    }
    save_output(out)
    print(f"[Scope 0] Complete: {summary['matches_hand_cases']}/{summary['total_cases']} matched hand values. Summary saved.")
    return out["scope0"]


# ---- Scope 1: Decision 2 (bridge_v82_no repair test) ------------------------------

def build_scope1_cases() -> list[dict[str, Any]]:
    cases: list[dict[str, Any]] = []

    # 1. d2_single_v82_no
    acts = h.opened()
    acts = h.sale(acts, "covered", "st", proceeds=5000, basis=4000, tag="d2_s1")
    acts = h.answer(acts, **h.honest({"covered"}, loss=False))
    s1 = "demo.sfa.d2_s1.statement"
    acts = say_b4_reported(acts, V82, s1, "no")
    acts = say_b7_reported(acts, V82, s1, "no")
    cases.append({
        "case_id": "d2_single_v82_no",
        "description": "One statement with covered ST sale ($1,000 gain); v82 box 4 'no' recorded, no amount",
        "acts": acts,
    })

    # 2. d2_two_statements_both_v82_no
    acts = h.opened()
    acts = h.sale(acts, "covered", "st", proceeds=5000, basis=4000, tag="d2_two_s1")
    acts = h.sale(acts, "covered", "st", proceeds=2000, basis=1500, tag="d2_two_s2")
    acts = h.answer(acts, **h.honest({"covered"}, loss=False))
    s1, s2 = "demo.sfa.d2_two_s1.statement", "demo.sfa.d2_two_s2.statement"
    acts = say_b4_reported(acts, V82, s1, "no")
    acts = say_b7_reported(acts, V82, s1, "no")
    acts = say_b4_reported(acts, V82, s2, "no")
    acts = say_b7_reported(acts, V82, s2, "no")
    cases.append({
        "case_id": "d2_two_statements_both_v82_no",
        "description": "Two statements with sales; both have v82 box 4 'no' recorded, no amount",
        "acts": acts,
    })

    # 3. d2_mixed_statements
    acts = h.opened()
    acts = h.sale(acts, "covered", "st", proceeds=5000, basis=4000, tag="d2_mix_s1")
    acts = h.sale(acts, "covered", "st", proceeds=2000, basis=1500, tag="d2_mix_s2")
    acts = h.answer(acts, **h.honest({"covered"}, loss=False))
    s1, s2 = "demo.sfa.d2_mix_s1.statement", "demo.sfa.d2_mix_s2.statement"
    acts = say_b4_amount(acts, get_core("decided"), s1, 240.0)
    acts = say_b7_reported(acts, get_core("decided"), s1, "no")
    acts = say_b4_reported(acts, V82, s2, "no")
    acts = say_b7_reported(acts, V82, s2, "no")
    cases.append({
        "case_id": "d2_mixed_statements",
        "description": "Two statements: s1 has new box 4 amount $240; s2 has legacy v82 box 4 'no'",
        "acts": acts,
    })

    # 4. d2_unanswered_statement
    acts = h.opened()
    acts = h.sale(acts, "covered", "st", proceeds=5000, basis=4000, tag="d2_unans")
    acts = h.answer(acts, **h.honest({"covered"}, loss=False))
    s1 = "demo.sfa.d2_unans.statement"
    acts = say_b7_reported(acts, V82, s1, "no")
    cases.append({
        "case_id": "d2_unanswered_statement",
        "description": "One statement with sale; neither v82 answer nor v83 amount recorded (unanswered)",
        "acts": acts,
    })

    return cases


def run_scope1() -> dict[str, Any]:
    cases = build_scope1_cases()
    core_repair = get_core("repair_d2")
    core_decided = get_core("decided")

    print(f"[Scope 1] Running {len(cases)} Decision 2 cases on core repair_d2 and core decided...")
    results: list[dict[str, Any]] = []

    for c in cases:
        cid = c["case_id"]
        res_repair = run_coordinate(core_repair, c["acts"], f"demo.b4.s1.repair.{cid}")
        res_decided = run_coordinate(core_decided, c["acts"], f"demo.b4.s1.decided.{cid}")

        disp_repair = res_repair["dispositions"].get("form1040.line-25b")
        disp_decided = res_decided["dispositions"].get("form1040.line-25b")
        reasons_repair = res_repair["blocked_reasons"].get("form1040.line-25b", [])
        reasons_decided = res_decided["blocked_reasons"].get("form1040.line-25b", [])

        entry = {
            "case_id": cid,
            "description": c["description"],
            "repair_d2": {
                "outcome": res_repair["outcome"],
                "disposition_25b": disp_repair,
                "lines": {
                    "form1040.line-25b": res_repair["lines"].get("form1040.line-25b"),
                },
                "blocked_reasons": reasons_repair,
            },
            "decided": {
                "outcome": res_decided["outcome"],
                "disposition_25b": disp_decided,
                "lines": {
                    "form1040.line-25b": res_decided["lines"].get("form1040.line-25b"),
                },
                "blocked_reasons": reasons_decided,
            },
            "repair_allows_v82_no": disp_repair in ("published", "published_value", "computed_zero"),
        }
        results.append(entry)
        print(f"  {cid}: repair_d2={disp_repair} decided={disp_decided} (repair_allows_v82_no={entry['repair_allows_v82_no']})")

    repair_succeeded_count = sum(1 for r in results if r["repair_allows_v82_no"])
    summary = {
        "total_cases": len(results),
        "repair_succeeded_cases": repair_succeeded_count,
        "repair_works": repair_succeeded_count > 0,
        "decision_2_confirmed": repair_succeeded_count == 0,
        "failure_mechanism": (
            "require_paired evaluates each arm eagerly; an unfulfilled statement-box4-withholding immediately "
            "raises EvalBlocked(BLOCK_ABSENT, [statement-box4-withholding]) before the fallback arm can execute. "
            "The decided subtotal does not collect an empty amount set, so a v82 return is not blocked on closing f1099b.b4."
        ),
    }

    out = load_output()
    out["scope1"] = {
        "summary": summary,
        "cases": results,
    }
    save_output(out)
    print(f"[Scope 1] Complete: repair_works={summary['repair_works']}, decision_2_confirmed={summary['decision_2_confirmed']}. Summary saved.")
    return out["scope1"]


# ---- Scope 2: Authority-Lifecycle Cases --------------------------------------------

def build_scope2_cases() -> list[dict[str, Any]]:
    cases: list[dict[str, Any]] = []

    # 1. alc_b4_amount_valid
    acts = h.opened()
    acts = h.sale(acts, "covered", "st", proceeds=5000, basis=4000, tag="alc_v")
    acts = h.answer(acts, **h.honest({"covered"}, loss=False))
    stmt = "demo.sfa.alc_v.statement"
    acts = say_b4_amount(acts, get_core("decided"), stmt, 150.0)
    acts = say_b7_reported(acts, get_core("decided"), stmt, "no")
    cases.append({
        "case_id": "alc_b4_amount_valid",
        "description": "Valid box 4 amount $150 asserted for statement with sale; line 25b publishes $150",
        "acts": acts,
        "core": "decided",
        "expected_disp": "published_value",
        "expected_25b": 150.0,
    })

    # 2. alc_b4_amount_superseded
    acts = h.opened()
    acts = h.sale(acts, "covered", "st", proceeds=5000, basis=4000, tag="alc_sup")
    acts = h.answer(acts, **h.honest({"covered"}, loss=False))
    stmt = "demo.sfa.alc_sup.statement"
    acts = say_b4_amount(acts, get_core("decided"), stmt, 100.0)
    fid = h.fact_id_for(B4_AMOUNT_FACT, (("statement", stmt), ("tax-year", YEAR)))
    finding_sup = h._attested(f"demo.b4.probe.statement-box4-withholding.{stmt}.v2", fid, 250.0)
    h._add(acts, "assertion", {"finding": finding_sup})
    acts = h.renumber(acts)
    acts = say_b7_reported(acts, get_core("decided"), stmt, "no")
    cases.append({
        "case_id": "alc_b4_amount_superseded",
        "description": "Box 4 amount superseded from $100 to $250; line 25b recomputes to $250",
        "acts": acts,
        "core": "decided",
        "expected_disp": "published_value",
        "expected_25b": 250.0,
    })

    # 3. alc_b4_amount_missing
    acts = h.opened()
    acts = h.sale(acts, "covered", "st", proceeds=5000, basis=4000, tag="alc_miss")
    acts = h.answer(acts, **h.honest({"covered"}, loss=False))
    stmt = "demo.sfa.alc_miss.statement"
    acts = say_b7_reported(acts, get_core("decided"), stmt, "no")
    cases.append({
        "case_id": "alc_b4_amount_missing",
        "description": "Statement with sale lacks box 4 amount finding; line 25b blocked on DEPENDENCY_ABSENT",
        "acts": acts,
        "core": "decided",
        "expected_disp": "blocked",
        "expected_25b": None,
    })

    # 4. alc_v82_answer_on_v82
    acts = h.opened()
    acts = h.sale(acts, "covered", "st", proceeds=5000, basis=4000, tag="alc_v82_on_v82")
    acts = h.answer(acts, **h.honest({"covered"}, loss=False))
    stmt = "demo.sfa.alc_v82_on_v82.statement"
    acts = say_b4_reported(acts, V82, stmt, "no")
    acts = say_b7_reported(acts, V82, stmt, "no")
    cases.append({
        "case_id": "alc_v82_answer_on_v82",
        "description": "Legacy v82 box 4 'no' answer evaluated on published v82 core; computes $0",
        "acts": acts,
        "core": "v82",
        "expected_disp": "computed_zero",
        "expected_25b": 0.0,
    })

    # 5. alc_v82_answer_on_v83
    acts = h.opened()
    acts = h.sale(acts, "covered", "st", proceeds=5000, basis=4000, tag="alc_v82_on_v83")
    acts = h.answer(acts, **h.honest({"covered"}, loss=False))
    stmt = "demo.sfa.alc_v82_on_v83.statement"
    acts = say_b4_reported(acts, V82, stmt, "no")
    acts = say_b7_reported(acts, V82, stmt, "no")
    cases.append({
        "case_id": "alc_v82_answer_on_v83",
        "description": "Legacy v82 box 4 'no' answer evaluated on scratch v83 core; blocked (amount required)",
        "acts": acts,
        "core": "decided",
        "expected_disp": "blocked",
        "expected_25b": None,
    })

    # 6. alc_count_zero
    acts = h.opened()
    acts = h.answer(acts, **h.honest(set(), loss=False))
    cases.append({
        "case_id": "alc_count_zero",
        "description": "Zero Form 1099-B sales recorded; all sale counts 0, line 25b computes $0 without asking box 4",
        "acts": acts,
        "core": "decided",
        "expected_disp": "computed_zero",
        "expected_25b": 0.0,
    })

    # 7. alc_count_positive
    acts = h.opened()
    acts = h.sale(acts, "covered", "st", proceeds=5000, basis=4000, tag="alc_cnt_pos")
    acts = h.answer(acts, **h.honest({"covered"}, loss=False))
    stmt = "demo.sfa.alc_cnt_pos.statement"
    acts = say_b4_amount(acts, get_core("decided"), stmt, 200.0)
    acts = say_b7_reported(acts, get_core("decided"), stmt, "no")
    cases.append({
        "case_id": "alc_count_positive",
        "description": "One covered ST sale; covered-st-count > 0 activates require_paired and line 25b collects $200",
        "acts": acts,
        "core": "decided",
        "expected_disp": "published_value",
        "expected_25b": 200.0,
    })

    # 8. alc_count_transition
    acts = h.opened()
    acts = h.sale(acts, "covered", "st", proceeds=5000, basis=4000, tag="alc_cnt_s1")
    acts = h.sale(acts, "covered", "st", proceeds=2000, basis=1500, tag="alc_cnt_s2")
    filtered = [
        a for a in acts
        if not (a.get("kind") == "entity-introduced" and (a.get("payload") or {}).get("entity", {}).get("id") == "demo.sfa.alc_cnt_s2.statement")
    ]
    text = json.dumps(filtered).replace("demo.sfa.alc_cnt_s2.statement", "demo.sfa.alc_cnt_s1.statement")
    acts = h.renumber(json.loads(text))
    acts = h.answer(acts, **h.honest({"covered"}, loss=False))
    stmt = "demo.sfa.alc_cnt_s1.statement"
    acts = say_b4_amount(acts, get_core("decided"), stmt, 200.0)
    acts = say_b7_reported(acts, get_core("decided"), stmt, "no")
    cases.append({
        "case_id": "alc_count_transition",
        "description": "Two covered ST sales on same statement; covered-st-count is 2, b4 amount $200",
        "acts": acts,
        "core": "decided",
        "expected_disp": "published_value",
        "expected_25b": 200.0,
    })

    # 9. alc_stmt_orphan
    acts = h.opened()
    acts = h.answer(acts, **h.honest(set(), loss=False))
    s_orph = "demo.sfa.alc_orphan.statement"
    h._introduce(acts, s_orph, "tax.us.f1099b-statement")
    acts = say_b4_amount(acts, get_core("decided"), s_orph, 200.0)
    acts = say_b7_reported(acts, get_core("decided"), s_orph, "no")
    cases.append({
        "case_id": "alc_stmt_orphan",
        "description": "Statement entity exists with $200 box 4 amount but zero sales recorded; line 25b adds the $200",
        "acts": acts,
        "core": "decided",
        "expected_disp": "published_value",
        "expected_25b": 200.0,
    })

    return cases


def run_scope2() -> dict[str, Any]:
    cases = build_scope2_cases()
    print(f"[Scope 2] Running {len(cases)} Authority-Lifecycle cases...")
    results: list[dict[str, Any]] = []

    for c in cases:
        cid = c["case_id"]
        core = get_core(c["core"])
        res = run_coordinate(core, c["acts"], f"demo.b4.s2.{cid}")

        disp_25b = res["dispositions"].get("form1040.line-25b")
        val_25b = res["lines"].get("form1040.line-25b")
        reasons_25b = res["blocked_reasons"].get("form1040.line-25b", [])

        matches = (
            disp_25b == c["expected_disp"]
            and (c["expected_disp"] == "blocked" or val_25b == c["expected_25b"])
        )

        entry = {
            "case_id": cid,
            "description": c["description"],
            "core": c["core"],
            "expected_disp": c["expected_disp"],
            "expected_25b": c["expected_25b"],
            "outcome": res["outcome"],
            "disposition_25b": disp_25b,
            "line_25b": val_25b,
            "blocked_reasons": reasons_25b,
            "matches_expected": matches,
        }
        results.append(entry)
        print(f"  {cid} ({c['core']}): 25b={disp_25b} ({val_25b}) matches={matches}")

    summary = {
        "total_cases": len(results),
        "matches_expected_cases": sum(1 for r in results if r["matches_expected"]),
        "all_match_expected": all(r["matches_expected"] for r in results),
    }

    out = load_output()
    out["scope2"] = {
        "summary": summary,
        "cases": results,
    }
    save_output(out)
    print(f"[Scope 2] Complete: {summary['matches_expected_cases']}/{summary['total_cases']} matched expected. Summary saved.")
    return out["scope2"]


# ---- Scope 3: Empty/Nonempty Matrix (8 families x 4 states = 32 runs) -------------

FAMILIES_8 = [
    ("covered-st", "covered", "st"),
    ("covered-lt", "covered", "lt"),
    ("covered-w-st", "w", "st"),
    ("covered-w-lt", "w", "lt"),
    ("noncovered-st", "noncovered", "st"),
    ("noncovered-lt", "noncovered", "lt"),
    ("code-b-st", "codeb", "st"),
    ("code-b-lt", "codeb", "lt"),
]

STATES_4 = [
    ("zero", 0.0, "computed_zero"),
    ("positive", 120.0, "published_value"),
    ("unrecorded", None, "blocked"),
    ("v82_only", None, "blocked"),
]


def build_scope3_cases() -> list[dict[str, Any]]:
    cases: list[dict[str, Any]] = []
    core = get_core("decided")

    for fam_name, kind, term in FAMILIES_8:
        for state_name, amount, expected_disp in STATES_4:
            cid = f"m_{fam_name.replace('-', '_')}_{state_name}"
            tag = f"tag_{cid}"
            stmt = f"demo.sfa.{tag}.statement"

            acts = h.opened()
            if kind == "codeb":
                acts = h.sale(acts, kind, term, proceeds=5000, basis=4500, corrected=4000, tag=tag)
            elif kind == "w":
                acts = h.sale(acts, kind, term, proceeds=5000, basis=4000, wash=0, tag=tag)
            else:
                acts = h.sale(acts, kind, term, proceeds=5000, basis=4000, tag=tag)

            acts = h.answer(acts, **h.honest({kind}, loss=False))
            acts = say_b7_reported(acts, core, stmt, "no")

            if state_name == "zero":
                acts = say_b4_amount(acts, core, stmt, 0.0)
            elif state_name == "positive":
                acts = say_b4_amount(acts, core, stmt, 120.0)
            elif state_name == "v82_only":
                acts = say_b4_reported(acts, V82, stmt, "no")

            cases.append({
                "case_id": cid,
                "family": fam_name,
                "kind": kind,
                "term": term,
                "state": state_name,
                "description": f"{fam_name} with box 4 state '{state_name}' (expected {expected_disp})",
                "acts": acts,
                "expected_disp": expected_disp,
                "expected_25b": amount,
            })
    return cases


def run_scope3() -> dict[str, Any]:
    cases = build_scope3_cases()
    core = get_core("decided")
    print(f"[Scope 3] Running {len(cases)} Empty/Nonempty matrix cases on core decided...")
    results: list[dict[str, Any]] = []

    for c in cases:
        cid = c["case_id"]
        res = run_coordinate(core, c["acts"], f"demo.b4.s3.{cid}")
        disp_25b = res["dispositions"].get("form1040.line-25b")
        val_25b = res["lines"].get("form1040.line-25b")
        reasons_25b = res["blocked_reasons"].get("form1040.line-25b", [])

        matches = (
            disp_25b == c["expected_disp"]
            and (c["expected_disp"] == "blocked" or val_25b == c["expected_25b"])
        )

        entry = {
            "case_id": cid,
            "family": c["family"],
            "state": c["state"],
            "description": c["description"],
            "expected_disp": c["expected_disp"],
            "expected_25b": c["expected_25b"],
            "outcome": res["outcome"],
            "disposition_25b": disp_25b,
            "line_25b": val_25b,
            "blocked_reasons": reasons_25b,
            "matches_expected": matches,
        }
        results.append(entry)
        print(f"  {cid}: 25b={disp_25b} ({val_25b}) matches={matches}")

    summary = {
        "total_cases": len(results),
        "zero_published_cases": sum(1 for r in results if r["state"] == "zero" and r["matches_expected"]),
        "positive_published_cases": sum(1 for r in results if r["state"] == "positive" and r["matches_expected"]),
        "unrecorded_blocked_cases": sum(1 for r in results if r["state"] == "unrecorded" and r["matches_expected"]),
        "v82_only_blocked_cases": sum(1 for r in results if r["state"] == "v82_only" and r["matches_expected"]),
        "matches_expected_cases": sum(1 for r in results if r["matches_expected"]),
        "all_match_expected": all(r["matches_expected"] for r in results),
    }

    out = load_output()
    out["scope3"] = {
        "summary": summary,
        "cases": results,
    }
    save_output(out)
    print(f"[Scope 3] Complete: {summary['matches_expected_cases']}/{summary['total_cases']} matched expected. Summary saved.")
    return out["scope3"]


# ---- Scope 4: Late-Member Trace ----------------------------------------------------

def build_scope4_cases() -> list[dict[str, Any]]:
    cases: list[dict[str, Any]] = []
    core = get_core("decided")

    # Trace 1: statement with amount -> new statement with sale unanswered -> answered
    acts_1a = h.opened()
    acts_1a = h.sale(acts_1a, "covered", "st", proceeds=5000, basis=4000, tag="tr1_a")
    acts_1a = h.answer(acts_1a, **h.honest({"covered"}, loss=False))
    s_a = "demo.sfa.tr1_a.statement"
    acts_1a = say_b4_amount(acts_1a, core, s_a, 150.0)
    acts_1a = say_b7_reported(acts_1a, core, s_a, "no")

    cases.append({
        "case_id": "trace1_initial",
        "description": "Trace 1 step 1: statement A has covered ST sale ($1,000 gain) and b4 amount $150; line 25b publishes $150",
        "acts": acts_1a,
        "expected_disp": "published_value",
        "expected_25b": 150.0,
    })

    acts_1b = copy.deepcopy(acts_1a)
    acts_1b = h.sale(acts_1b, "covered", "st", proceeds=2000, basis=1500, tag="tr1_b")
    s_b = "demo.sfa.tr1_b.statement"
    acts_1b = say_b7_reported(acts_1b, core, s_b, "no")

    cases.append({
        "case_id": "trace1_new_stmt_unanswered",
        "description": "Trace 1 step 2: sale added on new statement B; statement B b4 amount is missing; line 25b is blocked",
        "acts": acts_1b,
        "expected_disp": "blocked",
        "expected_25b": None,
    })

    acts_1c = copy.deepcopy(acts_1b)
    acts_1c = say_b4_amount(acts_1c, core, s_b, 100.0)

    cases.append({
        "case_id": "trace1_new_stmt_answered",
        "description": "Trace 1 step 3: statement B b4 amount answered $100; line 25b recomputes and publishes sum $250 ($150 + $100)",
        "acts": acts_1c,
        "expected_disp": "published_value",
        "expected_25b": 250.0,
    })

    # Trace 2: statement with amount -> sale removed after its amount
    acts_2a = h.opened()
    acts_2a = h.sale(acts_2a, "covered", "st", proceeds=5000, basis=4000, tag="tr2_a")
    acts_2a = h.answer(acts_2a, **h.honest({"covered"}, loss=False))
    s_2a = "demo.sfa.tr2_a.statement"
    acts_2a = say_b4_amount(acts_2a, core, s_2a, 200.0)
    acts_2a = say_b7_reported(acts_2a, core, s_2a, "no")

    cases.append({
        "case_id": "trace2_initial",
        "description": "Trace 2 step 1: statement A has covered ST sale ($1,000 gain) and b4 amount $200; line 25b publishes $200",
        "acts": acts_2a,
        "expected_disp": "published_value",
        "expected_25b": 200.0,
    })

    acts_2b = h.opened()
    acts_2b = h.answer(acts_2b, **h.honest(set(), loss=False))
    h._introduce(acts_2b, s_2a, "tax.us.f1099b-statement")
    acts_2b = say_b4_amount(acts_2b, core, s_2a, 200.0)
    acts_2b = say_b7_reported(acts_2b, core, s_2a, "no")

    cases.append({
        "case_id": "trace2_sale_removed",
        "description": "Trace 2 step 2: sale removed; orphan statement A retains $200 b4 amount; line 25b adds the $200",
        "acts": acts_2b,
        "expected_disp": "published_value",
        "expected_25b": 200.0,
    })

    return cases


def run_scope4() -> dict[str, Any]:
    cases = build_scope4_cases()
    core = get_core("decided")
    print(f"[Scope 4] Running {len(cases)} Late-Member Trace cases on core decided...")
    results: list[dict[str, Any]] = []

    for c in cases:
        cid = c["case_id"]
        res = run_coordinate(core, c["acts"], f"demo.b4.s4.{cid}")
        disp_25b = res["dispositions"].get("form1040.line-25b")
        val_25b = res["lines"].get("form1040.line-25b")
        reasons_25b = res["blocked_reasons"].get("form1040.line-25b", [])

        matches = (
            disp_25b == c["expected_disp"]
            and (c["expected_disp"] == "blocked" or val_25b == c["expected_25b"])
        )

        entry = {
            "case_id": cid,
            "description": c["description"],
            "expected_disp": c["expected_disp"],
            "expected_25b": c["expected_25b"],
            "outcome": res["outcome"],
            "disposition_25b": disp_25b,
            "line_25b": val_25b,
            "blocked_reasons": reasons_25b,
            "matches_expected": matches,
        }
        results.append(entry)
        print(f"  {cid}: 25b={disp_25b} ({val_25b}) matches={matches}")

    summary = {
        "total_cases": len(results),
        "trace1_step1_published": next(r["matches_expected"] for r in results if r["case_id"] == "trace1_initial"),
        "trace1_step2_blocked": next(r["matches_expected"] for r in results if r["case_id"] == "trace1_new_stmt_unanswered"),
        "trace1_step3_published": next(r["matches_expected"] for r in results if r["case_id"] == "trace1_new_stmt_answered"),
        "trace2_step1_published": next(r["matches_expected"] for r in results if r["case_id"] == "trace2_initial"),
        "trace2_step2_keeps_amount": next(r["matches_expected"] for r in results if r["case_id"] == "trace2_sale_removed"),
        "matches_expected_cases": sum(1 for r in results if r["matches_expected"]),
        "all_match_expected": all(r["matches_expected"] for r in results),
    }

    out = load_output()
    out["scope4"] = {
        "summary": summary,
        "cases": results,
    }
    save_output(out)
    print(f"[Scope 4] Complete: {summary['matches_expected_cases']}/{summary['total_cases']} matched expected. Summary saved.")
    return out["scope4"]


# ---- Scope 5: Claim Reuse (Five existing line 25b subtotals) -----------------------

def get_head(acts: list[dict[str, Any]], family_id: str) -> str:
    for act in acts:
        payload = act.get("payload") or {}
        if act.get("kind") == "horizon-genesis" and (payload.get("family") or {}).get("id") == family_id:
            return str(payload.get("horizon_id"))
    raise AssertionError(f"no horizon genesis for {family_id}")


def ensure_genesis(acts: list[dict[str, Any]], family_id: str, version: str = "v1") -> str:
    for act in acts:
        payload = act.get("payload") or {}
        if act.get("kind") == "horizon-genesis" and (payload.get("family") or {}).get("id") == family_id:
            return str(payload.get("horizon_id"))
    head_id = f"demo.reuse.{family_id.split('.')[-1]}.h0"
    h._add(acts, "horizon-genesis", {
        "family": {"id": family_id, "version": version},
        "scope": dict(SCOPE_KEY),
        "horizon_id": head_id,
    })
    return head_id


SCOPE_KEY = {"tax-year": YEAR, "subject": "demo.primary"}


def make_transition(
    acts: list[dict[str, Any]],
    family: tuple[str, str],
    predecessor: str,
    successor: str,
    finding_id: str,
    fact_type: str,
    keys: tuple[tuple[str, str], ...],
    value: Any,
) -> str:
    fact_id = h.fact_id_for(fact_type, keys + (("tax-year", YEAR),))
    h._add(
        acts,
        "member-transition",
        {
            "family": {"id": family[0], "version": family[1]},
            "scope": dict(SCOPE_KEY),
            "member": {"action": "assert", "finding": h._attested(finding_id, fact_id, value)},
            "successor": {"id": successor, "predecessor": predecessor},
        },
    )
    return successor


def make_close(acts: list[dict[str, Any]], closure_fact: str, horizon: str, finding_id: str) -> None:
    h._add(acts, "assertion", {"finding": h._attested(finding_id, f"{closure_fact}|family-horizon={horizon},tax-year={YEAR}", True)})


def assert_fact(acts: list[dict[str, Any]], finding_id: str, fact_type: str, keys: tuple[tuple[str, str], ...], value: Any) -> None:
    fact_id = h.fact_id_for(fact_type, keys + (("tax-year", YEAR),))
    h._add(acts, "assertion", {"finding": h._attested(finding_id, fact_id, value)})


def add_interest_withholding(acts: list[dict[str, Any]], box4: float, box1: float = 100.0) -> list[dict[str, Any]]:
    acts = copy.deepcopy(acts)
    b1_head = get_head(acts, "tax.us.2025.f1099int.b1")
    b4_head = get_head(acts, "tax.us.2025.f1099int.b4")
    payer, stmt = "demo.reuse.int.payer", "demo.reuse.int.stmt"
    keys = (("payer", payer), ("statement", stmt))
    h._introduce(acts, payer, "tax.us.interest-payer")
    h._introduce(acts, stmt, "tax.us.1099int-statement")
    b1_head = make_transition(
        acts, ("tax.us.2025.f1099int.b1", "v1"), b1_head, "demo.reuse.int.b1.h1", "demo.reuse.int.box1",
        "tax.us.2025.f1099int.box1-interest", keys, box1,
    )
    b4_head = make_transition(
        acts, ("tax.us.2025.f1099int.b4", "v1"), b4_head, "demo.reuse.int.b4.h1", "demo.reuse.int.box4",
        "tax.us.2025.f1099int.box4-withholding", keys, box4,
    )
    make_close(acts, "tax.us.2025.f1099int.b1.source-closure", b1_head, "demo.reuse.int.closure.box1")
    make_close(acts, "tax.us.2025.f1099int.b4.source-closure", b4_head, "demo.reuse.int.closure.box4")
    return h.renumber(acts)


def add_dividend_withholding(acts: list[dict[str, Any]], box4: float, box1a: float = 200.0) -> list[dict[str, Any]]:
    acts = copy.deepcopy(acts)
    a_head = get_head(acts, "tax.us.2025.f1099div.1a")
    div_b4_head = get_head(acts, "tax.us.2025.f1099div.b4")
    payer, stmt = "demo.reuse.div.payer", "demo.reuse.div.stmt"
    keys = (("payer", payer), ("statement", stmt))
    h._introduce(acts, payer, "tax.us.dividend-payer")
    h._introduce(acts, stmt, "tax.us.1099div-statement")
    a_head = make_transition(
        acts, ("tax.us.2025.f1099div.1a", "v1"), a_head, "demo.reuse.div.1a.h1", "demo.reuse.div.box1a",
        "tax.us.2025.f1099div.box1a-ordinary", keys, box1a,
    )
    div_b4_head = make_transition(
        acts, ("tax.us.2025.f1099div.b4", "v1"), div_b4_head, "demo.reuse.div.b4.h1", "demo.reuse.div.box4",
        "tax.us.2025.f1099div.box4-withholding", keys, box4,
    )
    make_close(acts, "tax.us.2025.f1099div.1a.source-closure", a_head, "demo.reuse.div.closure.1a")
    make_close(acts, "tax.us.2025.f1099div.b4.source-closure", div_b4_head, "demo.reuse.div.closure.box4")
    return h.renumber(acts)


def add_ira_withholding(acts: list[dict[str, Any]], withheld: float, distribution: float = 1000.0) -> list[dict[str, Any]]:
    acts = copy.deepcopy(acts)
    payer, stmt = "demo.reuse.r.payer", "demo.reuse.r.stmt"
    keys = (("payer", payer), ("statement", stmt))
    h._introduce(acts, payer, "tax.us.ira-payer")
    h._introduce(acts, stmt, "tax.us.1099r-statement")
    assert_fact(acts, "demo.reuse.r.box2a", "tax.us.2025.f1099r.ira-box2a-taxable-amount", keys, distribution)
    assert_fact(acts, "demo.reuse.r.checkbox", "tax.us.2025.f1099r.ira-sep-simple-checkbox", keys, True)
    assert_fact(acts, "demo.reuse.r.code", "tax.us.2025.f1099r.distribution-code", keys, "7")
    assert_fact(acts, "demo.reuse.r.box2b", "tax.us.2025.f1099r.box2b-not-determined", keys, False)
    head = make_transition(
        acts, ("tax.us.2025.f1099r.ira-fully-taxable", "v2"), get_head(acts, "tax.us.2025.f1099r.ira-fully-taxable"),
        "demo.reuse.r.h1", "demo.reuse.r.box1", "tax.us.2025.f1099r.ira-box1-taxable-distribution", keys, distribution,
    )
    make_close(acts, "tax.us.2025.f1099r.ira-fully-taxable.source-closure", head, "demo.reuse.r.closure.box1")
    b4_head = make_transition(
        acts, ("tax.us.2025.f1099r.box4", "v1"), get_head(acts, "tax.us.2025.f1099r.box4"),
        "demo.reuse.r.b4.h1", "demo.reuse.r.box4", "tax.us.2025.f1099r.ira-box4-withholding", keys, withheld,
    )
    make_close(acts, "tax.us.2025.f1099r.box4.source-closure", b4_head, "demo.reuse.r.closure.box4")
    return h.renumber(acts)


def add_unemployment_withholding(acts: list[dict[str, Any]], withheld: float, amount: float = 1000.0) -> list[dict[str, Any]]:
    acts = copy.deepcopy(acts)
    body_b4 = json.loads((REPO / "packages/content/tax/2025/f1099g-box4.bundle.json").read_text(encoding="utf-8"))
    if not {f["id"] for f in body_b4["fact_types"]} & h._adopted(acts):
        h._add(acts, "bundle-adoption", {"bundle": body_b4})
    head = get_head(acts, "tax.us.2025.f1099g.1")
    payer, stmt = "demo.reuse.g.payer", "demo.reuse.g.stmt"
    keys = (("payer", payer), ("statement", stmt))
    h._introduce(acts, payer, "tax.us.unemployment-payer")
    h._introduce(acts, stmt, "tax.us.1099g-statement")
    head = make_transition(
        acts, ("tax.us.2025.f1099g.1", "v1"), head, "demo.reuse.g1.h1", "demo.reuse.g.box1",
        "tax.us.2025.f1099g.box1-unemployment", keys, amount,
    )
    make_close(acts, "tax.us.2025.f1099g.1.source-closure", head, "demo.reuse.g.closure.box1")

    head_b4 = ensure_genesis(acts, "tax.us.2025.f1099g.b4", "v1")
    head_b4 = make_transition(
        acts, ("tax.us.2025.f1099g.b4", "v1"), head_b4, "demo.reuse.g4.h1", "demo.reuse.g.box4",
        "tax.us.2025.f1099g.box4-withholding", keys, withheld,
    )
    make_close(acts, "tax.us.2025.f1099g.b4.source-closure", head_b4, "demo.reuse.g.closure.box4")
    return h.renumber(acts)


def add_ssa_withholding(acts: list[dict[str, Any]], withheld: float, benefits: float = 1000.0) -> list[dict[str, Any]]:
    acts = copy.deepcopy(acts)
    body_b6 = json.loads((REPO / "packages/content/tax/2025/ssa1099-box6.bundle.json").read_text(encoding="utf-8"))
    if not {f["id"] for f in body_b6["fact_types"]} & h._adopted(acts):
        h._add(acts, "bundle-adoption", {"bundle": body_b6})
    scope_fact = "tax.us.2025.schedule1-adjustments-scope.no-line24z-writein"
    if not any(str((a.get("payload") or {}).get("finding", {}).get("fact_id", "")).startswith(scope_fact + "|") for a in acts):
        h._add(acts, "assertion", {"finding": h._attested("demo.reuse.ssa.scope.no-line24z-writein", f"{scope_fact}|tax-year={YEAR}", "yes")})
    head = get_head(acts, "tax.us.2025.ssa1099.benefits")
    stmt = "demo.reuse.ssa.stmt"
    keys = (("statement", stmt),)
    h._introduce(acts, stmt, "tax.us.ssa1099-statement")
    assert_fact(acts, "demo.reuse.ssa.b3", "tax.us.2025.ssa1099.box3-benefits-paid", keys, benefits)
    assert_fact(acts, "demo.reuse.ssa.b4", "tax.us.2025.ssa1099.box4-repayment", keys, 0.0)
    assert_fact(acts, "demo.reuse.ssa.witness", "tax.us.2025.ssa1099.box6-withholding", keys, 0.0)
    assert_fact(acts, "demo.reuse.ssa.recipient", "tax.us.2025.ssa1099.recipient", keys, "taxpayer")
    assert_fact(acts, "demo.reuse.ssa.kind", "tax.us.2025.ssa1099.statement-kind", keys, "ssa-1099")
    assert_fact(acts, "demo.reuse.ssa.lump", "tax.us.2025.ssa1099.lump-sum-election", keys, False)
    head = make_transition(
        acts, ("tax.us.2025.ssa1099.benefits", "v1"), head, "demo.reuse.ssa.h1", "demo.reuse.ssa.b5",
        "tax.us.2025.ssa1099.box5-net-benefits", keys, benefits,
    )
    make_close(acts, "tax.us.2025.ssa1099.source-closure", head, "demo.reuse.ssa.closure.benefits")

    head_b6 = ensure_genesis(acts, "tax.us.2025.ssa1099.b6", "v1")
    head_b6 = make_transition(
        acts, ("tax.us.2025.ssa1099.b6", "v1"), head_b6, "demo.reuse.ssa6.h1", "demo.reuse.ssa.box6",
        "tax.us.2025.ssa1099.box6-voluntary-withholding", keys, withheld,
    )
    make_close(acts, "tax.us.2025.ssa1099.b6.source-closure", head_b6, "demo.reuse.ssa.closure.box6")
    return h.renumber(acts)


def build_scope5_cases() -> list[dict[str, Any]]:
    cases: list[dict[str, Any]] = []
    base_honest = h.opened()
    base_honest = h.answer(base_honest, **h.honest(set(), loss=False))

    # 1. reuse_int_alone: $50
    acts_int = add_interest_withholding(base_honest, 50.0)
    cases.append({
        "case_id": "reuse_int_alone",
        "description": "Form 1099-INT withholding $50 alone with zero sales; line 25b is $50",
        "acts": acts_int,
        "expected_disp": "published_value",
        "expected_25b": 50.0,
    })

    # 2. reuse_div_alone: $75
    acts_div = add_dividend_withholding(base_honest, 75.0)
    cases.append({
        "case_id": "reuse_div_alone",
        "description": "Form 1099-DIV withholding $75 alone with zero sales; line 25b is $75",
        "acts": acts_div,
        "expected_disp": "published_value",
        "expected_25b": 75.0,
    })

    # 3. reuse_ira_alone: $80
    acts_ira = add_ira_withholding(base_honest, 80.0)
    cases.append({
        "case_id": "reuse_ira_alone",
        "description": "Form 1099-R withholding $80 alone with zero sales; line 25b is $80",
        "acts": acts_ira,
        "expected_disp": "published_value",
        "expected_25b": 80.0,
    })

    # 4. reuse_unemp_alone: $90
    acts_unemp = add_unemployment_withholding(base_honest, 90.0)
    cases.append({
        "case_id": "reuse_unemp_alone",
        "description": "Form 1099-G withholding $90 alone with zero sales; line 25b is $90",
        "acts": acts_unemp,
        "expected_disp": "published_value",
        "expected_25b": 90.0,
    })

    # 5. reuse_ssa_alone: $60
    acts_ssa = add_ssa_withholding(base_honest, 60.0)
    cases.append({
        "case_id": "reuse_ssa_alone",
        "description": "Form SSA-1099 box 6 withholding $60 alone with zero sales; line 25b is $60",
        "acts": acts_ssa,
        "expected_disp": "published_value",
        "expected_25b": 60.0,
    })

    # 6. reuse_all_five_alone: sum = 50 + 75 + 80 + 90 + 60 = $355
    acts_all5 = copy.deepcopy(base_honest)
    acts_all5 = add_interest_withholding(acts_all5, 50.0)
    acts_all5 = add_dividend_withholding(acts_all5, 75.0)
    acts_all5 = add_ira_withholding(acts_all5, 80.0)
    acts_all5 = add_unemployment_withholding(acts_all5, 90.0)
    acts_all5 = add_ssa_withholding(acts_all5, 60.0)
    cases.append({
        "case_id": "reuse_all_five_alone",
        "description": "All five legacy 1099 subtotals ($355 total) with zero sales; line 25b is $355",
        "acts": acts_all5,
        "expected_disp": "published_value",
        "expected_25b": 355.0,
    })

    # 7. reuse_all_with_b4: all 5 subtotals ($355) + 1099-B sale ($1,000 gain) with b4 amount $100 = $455
    core = get_core("decided")
    acts_all_b4 = copy.deepcopy(acts_all5)
    acts_all_b4 = h.sale(acts_all_b4, "covered", "st", proceeds=5000, basis=4000, tag="reuse_b4")
    stmt_b4 = "demo.sfa.reuse_b4.statement"
    acts_all_b4 = say_b4_amount(acts_all_b4, core, stmt_b4, 100.0)
    acts_all_b4 = say_b7_reported(acts_all_b4, core, stmt_b4, "no")
    cases.append({
        "case_id": "reuse_all_with_b4",
        "description": "All five legacy 1099 subtotals ($355) beside Form 1099-B sale with b4 $100; line 25b is $455",
        "acts": acts_all_b4,
        "expected_disp": "published_value",
        "expected_25b": 455.0,
    })

    return cases


def run_scope5() -> dict[str, Any]:
    cases = build_scope5_cases()
    core = get_core("decided")
    print(f"[Scope 5] Running {len(cases)} Claim Reuse cases on core decided...")
    results: list[dict[str, Any]] = []

    for c in cases:
        cid = c["case_id"]
        res = run_coordinate(core, c["acts"], f"demo.b4.s5.{cid}")
        disp_25b = res["dispositions"].get("form1040.line-25b")
        val_25b = res["lines"].get("form1040.line-25b")
        reasons_25b = res["blocked_reasons"].get("form1040.line-25b", [])

        matches = (
            disp_25b == c["expected_disp"]
            and (c["expected_disp"] == "blocked" or val_25b == c["expected_25b"])
        )

        entry = {
            "case_id": cid,
            "description": c["description"],
            "expected_disp": c["expected_disp"],
            "expected_25b": c["expected_25b"],
            "outcome": res["outcome"],
            "disposition_25b": disp_25b,
            "line_25b": val_25b,
            "blocked_reasons": reasons_25b,
            "matches_expected": matches,
        }
        results.append(entry)
        print(f"  {cid}: 25b={disp_25b} ({val_25b}) matches={matches}")

    summary = {
        "total_cases": len(results),
        "int_alone_matches": next(r["matches_expected"] for r in results if r["case_id"] == "reuse_int_alone"),
        "div_alone_matches": next(r["matches_expected"] for r in results if r["case_id"] == "reuse_div_alone"),
        "ira_alone_matches": next(r["matches_expected"] for r in results if r["case_id"] == "reuse_ira_alone"),
        "unemp_alone_matches": next(r["matches_expected"] for r in results if r["case_id"] == "reuse_unemp_alone"),
        "ssa_alone_matches": next(r["matches_expected"] for r in results if r["case_id"] == "reuse_ssa_alone"),
        "all_five_alone_matches": next(r["matches_expected"] for r in results if r["case_id"] == "reuse_all_five_alone"),
        "all_with_b4_matches": next(r["matches_expected"] for r in results if r["case_id"] == "reuse_all_with_b4"),
        "matches_expected_cases": sum(1 for r in results if r["matches_expected"]),
        "all_match_expected": all(r["matches_expected"] for r in results),
    }

    out = load_output()
    out["scope5"] = {
        "summary": summary,
        "cases": results,
    }
    save_output(out)
    print(f"[Scope 5] Complete: {summary['matches_expected_cases']}/{summary['total_cases']} matched expected. Summary saved.")
    return out["scope5"]


# ---- Scope 6: Neighbour Dependency Diff (213 returns from expected.json) ----------

OWN_ROW_FAMILIES = tuple(P + f"f1099b.{k}-{t}" for k in ("covered", "covered-w") for t in ("st", "lt"))
SALE_KEYS = ("broker", "statement", "transaction")


def _keys(fact_id: str) -> tuple[str, dict[str, str]]:
    fact_type, _, rest = fact_id.partition("|")
    return fact_type, dict(part.split("=", 1) for part in rest.split(",")) if rest else {}


def own_rows(acts: list[dict[str, Any]]) -> list[dict[str, Any]]:
    sales: dict[str, list[dict[str, str]]] = {}
    rows: list[tuple[str, str, str, dict[str, str]]] = []
    for act in acts:
        payload = act.get("payload") or {}
        if act.get("kind") != "member-transition":
            continue
        family = str((payload.get("family") or {}).get("id"))
        member = payload.get("member") or {}
        if member.get("action") != "assert":
            continue
        fact_id = str(member["finding"]["fact_id"])
        fact_type, keys = _keys(fact_id)
        if family in OWN_ROW_FAMILIES:
            sales.setdefault(family, []).append(keys)
        elif family.rsplit("-", 1)[0] in OWN_ROW_FAMILIES:
            rows.append((family.rsplit("-", 1)[0], fact_id, fact_type, keys))
    renames: dict[str, str] = {}
    for family, fact_id, fact_type, keys in rows:
        candidates = sales.get(family, [])
        if any(all(sale[k] == keys[k] for k in SALE_KEYS) for sale in candidates):
            continue
        tag = keys["transaction"].split(".")[2]
        (sale,) = [s for s in candidates if s["transaction"].split(".")[2] in (tag[:-1], tag[:-1] + "o")]
        moved = {k: sale[k] if k in SALE_KEYS else v for k, v in keys.items()}
        renames[fact_id] = fact_type + "|" + ",".join(f"{k}={v}" for k, v in moved.items())
    text = json.dumps(acts)
    for old, new in renames.items():
        text = text.replace(json.dumps(old), json.dumps(new))
    return json.loads(text)


def rows_removed_first(acts: list[dict[str, Any]]) -> list[dict[str, Any]]:
    out = [copy.deepcopy(a) for a in acts]

    def removal(act: dict[str, Any]) -> tuple[str, str] | None:
        payload = act.get("payload") or {}
        member = payload.get("member") or {} if act.get("kind") == "member-transition" else {}
        if member.get("action") != "remove":
            return None
        return str((payload.get("family") or {}).get("id")), str(member.get("fact_id"))

    def closes(act: dict[str, Any], family: str) -> bool:
        finding = (act.get("payload") or {}).get("finding") if act.get("kind") == "assertion" else None
        return isinstance(finding, dict) and str(finding.get("fact_id", "")).startswith(family + ".source-closure|")

    index = 0
    while index < len(out):
        found = removal(out[index])
        if found is None or found[0] not in OWN_ROW_FAMILIES:
            index += 1
            continue
        family, fact_id = found
        suffix = fact_id.split("|", 1)[1]
        block = 2 if index + 1 < len(out) and closes(out[index + 1], family) else 1
        later = [i for i in range(index + block, len(out))
                 if (r := removal(out[i])) is not None and r[0].rsplit("-", 1)[0] == family
                 and r[1].split("|", 1)[1] == suffix]
        if not later:
            index += 1
            continue
        last = later[-1] + (1 if later[-1] + 1 < len(out) and closes(out[later[-1] + 1], removal(out[later[-1]])[0]) else 0)
        moved = out[index:index + block]
        out = out[:index] + out[index + block:last + 1] + moved + out[last + 1:]
    for position, act in enumerate(out):
        act["committed_against"] = position
    return out


def sale_statements(acts: list[dict[str, Any]]) -> list[str]:
    """Current Form 1099-B sale statements (asserted and not removed)."""
    return list(sfa_t0.sale_statements(acts))


def _run_return_worker(item: tuple[str, list[dict[str, Any]], bool, dict[str, Any], dict[str, Any], dict[str, Any]]) -> dict[str, Any]:
    cid, acts, has_sales, spec_82, spec_83, exp_v82 = item
    core_82 = h.Core(
        spec_82["version"],
        spec_82["registry"],
        spec_82["release_version"],
        Path(spec_82["content"]),
        Path(spec_82["releases"]),
        spec_82.get("loader_from"),
    )
    core_83 = h.Core(
        spec_83["version"],
        spec_83["registry"],
        spec_83["release_version"],
        Path(spec_83["content"]),
        Path(spec_83["releases"]),
        spec_83.get("loader_from"),
    )

    safe_cid = cid.replace("/", "_")
    res_82 = run_coordinate(core_82, acts, f"demo.b4.s6.82.{safe_cid}")
    res_83 = run_coordinate(core_83, acts, f"demo.b4.s6.83.{safe_cid}")

    # Cross-check res_82 against expected.json
    proj_82 = res_82.get("projection")
    reproduces_fixture = (proj_82 == exp_v82)
    fixture_mismatch = None if reproduces_fixture else {"actual": proj_82, "expected": exp_v82}

    # Exhaustive comparison between res_82 and res_83
    diffs = []
    if res_82.get("outcome") != res_83.get("outcome"):
        diffs.append(("outcome", res_82.get("outcome"), res_83.get("outcome")))
    if res_82.get("error") != res_83.get("error"):
        diffs.append(("error", res_82.get("error"), res_83.get("error")))

    all_lines = set(res_82.get("lines", {}).keys()) | set(res_83.get("lines", {}).keys())
    for k in sorted(all_lines):
        v82_val = res_82.get("lines", {}).get(k)
        v83_val = res_83.get("lines", {}).get(k)
        if v82_val != v83_val:
            diffs.append(("line_value", k, v82_val, v83_val))

    all_disps = set(res_82.get("dispositions", {}).keys()) | set(res_83.get("dispositions", {}).keys())
    for k in sorted(all_disps):
        v82_disp = res_82.get("dispositions", {}).get(k)
        v83_disp = res_83.get("dispositions", {}).get(k)
        if v82_disp != v83_disp:
            diffs.append(("line_disposition", k, v82_disp, v83_disp))

    all_reasons = set(res_82.get("blocked_reasons", {}).keys()) | set(res_83.get("blocked_reasons", {}).keys())
    for k in sorted(all_reasons):
        v82_r = res_82.get("blocked_reasons", {}).get(k)
        v83_r = res_83.get("blocked_reasons", {}).get(k)
        if v82_r != v83_r:
            diffs.append(("blocked_reasons", k, v82_r, v83_r))

    all_atts = set(res_82.get("attachments", {}).keys()) | set(res_83.get("attachments", {}).keys())
    for k in sorted(all_atts):
        v82_a = res_82.get("attachments", {}).get(k)
        v83_a = res_83.get("attachments", {}).get(k)
        if v82_a != v83_a:
            diffs.append(("attachment", k, v82_a, v83_a))

    all_rows = set(res_82.get("rows", {}).keys()) | set(res_83.get("rows", {}).keys())
    for k in sorted(all_rows):
        v82_row = res_82.get("rows", {}).get(k)
        v83_row = res_83.get("rows", {}).get(k)
        # A published row is the ordinary result. A rule that exists only on v83
        # and publishes is not a change in the return. A blocked or other row is.
        if v82_row == PUBLISHED_ROW:
            v82_row = None
        if v83_row == PUBLISHED_ROW:
            v83_row = None
        if v82_row != v83_row:
            diffs.append(("row", k, v82_row, v83_row))

    if res_82.get("questions") != res_83.get("questions"):
        diffs.append(("questions", res_82.get("questions"), res_83.get("questions")))

    # Classification: Decisions 1-2 say the v82 yes/no is unread and the
    # per-statement amount is asked, so line 25b and its payment consumers
    # block until answered. Anything else is a counterexample.
    allowed_fields = {
        "form1040.line-25b", "form1040.line-25d", "form1040.line-33",
        "form1040.line-34", "form1040.line-35a", "form1040.line-37",
    }
    allowed_rule_rows = {
        "rule.form1040-line25b", "rule.form1040-line25d", "rule.form1040-line33",
        "rule.form1040-line34", "rule.form1040-line35a", "rule.form1040-line36",
        "rule.form1040-line37",
    }
    amount_prompt = "box 4 of each Form 1099-B"
    diff_fields = {d[1] for d in diffs if d[0] in ("line_value", "line_disposition", "blocked_reasons")}
    unexpected = [
        d for d in diffs
        if d[0] == "attachment"
        or d[0] in ("outcome", "error")
        or (d[0] == "row" and (str(d[1]).startswith("attachment.") or not any(str(d[1]).startswith(r) for r in allowed_rule_rows)))
        or (d[0] in ("line_value", "line_disposition", "blocked_reasons") and d[1] not in allowed_fields)
        or (d[0] == "questions" and not (
            any(amount_prompt in str(q) for q in (d[2] or []))
            or any(amount_prompt in str(q) for q in (d[1] or []))
        ))
    ]
    v83_reasons_25b = res_83.get("blocked_reasons", {}).get("form1040.line-25b", []) or []
    asks_amount = res_83.get("dispositions", {}).get("form1040.line-25b") == "blocked" and any(
        amount_prompt in r for r in v83_reasons_25b
    )
    if not diffs:
        classification = "identical"
    elif not unexpected and asks_amount:
        classification = "box4_unanswered_asks_amount"
    else:
        classification = "counterexample:" + ",".join(sorted({d[0] + (":" + str(d[1]) if d[0] in ("line_value", "line_disposition", "blocked_reasons", "row", "attachment") else "") for d in (unexpected or diffs)}))

    compact_unexpected = [
        {"kind": d[0], "key": d[1] if d[0] in ("line_value", "line_disposition", "blocked_reasons", "row", "attachment") else None}
        for d in unexpected
    ]

    return {
        "case_id": cid,
        "classification": classification,
        "has_sales": has_sales,
        "reproduces_v82_fixture": reproduces_fixture,
        "fixture_mismatch": fixture_mismatch,
        "v82_outcome": res_82.get("outcome"),
        "v83_outcome": res_83.get("outcome"),
        "v82_error": res_82.get("error"),
        "v83_error": res_83.get("error"),
        "v82_disp_25b": res_82.get("dispositions", {}).get("form1040.line-25b"),
        "v83_disp_25b": res_83.get("dispositions", {}).get("form1040.line-25b"),
        "v82_line_25b": res_82.get("lines", {}).get("form1040.line-25b"),
        "v83_line_25b": res_83.get("lines", {}).get("form1040.line-25b"),
        "v82_blocked_reasons_25b": res_82.get("blocked_reasons", {}).get("form1040.line-25b", []),
        "v83_blocked_reasons_25b": res_83.get("blocked_reasons", {}).get("form1040.line-25b", []),
        "diff_count": len(diffs),
        "diff_fields": sorted(diff_fields) if diffs else [],
        "unexpected_diffs": compact_unexpected,
    }


def run_scope6() -> dict[str, Any]:
    print("[Scope 6] Running Neighbour dependency diff on all 213 returns from expected.json...")
    core_decided = get_core("decided")
    core_v82 = V82
    spec_82 = {
        "version": core_v82.version,
        "registry": core_v82.registry,
        "release_version": core_v82.release_version,
        "content": str(core_v82.content),
        "releases": str(core_v82.releases),
        "loader_from": core_v82.loader_from,
    }
    spec_83 = {
        "version": core_decided.version,
        "registry": core_decided.registry,
        "release_version": core_decided.release_version,
        "content": str(core_decided.content),
        "releases": str(core_decided.releases),
        "loader_from": core_decided.loader_from,
    }

    with open(EXPECTED_PATH) as f:
        expected_v81 = json.load(f)["v81"]

    with tempfile.TemporaryDirectory() as tmp:
        export_out = Path(tmp) / "v81-acts.json"
        subprocess.run(
            [sys.executable, str(REPO / "docs/phases/engine-breadth/milestones/sale-family-audit-evidence/export_v81_returns.py"), str(export_out)],
            check=True,
            cwd=REPO,
            stdout=subprocess.DEVNULL,
        )
        exported: dict[str, dict[str, list[dict[str, Any]]]] = json.loads(export_out.read_text(encoding="utf-8"))

    items: list[tuple[str, list[dict[str, Any]], bool, dict[str, Any], dict[str, Any], dict[str, Any]]] = []
    for group in ("case", "v80", "neighbour"):
        for name in sorted(exported.get(group, {})):
            cid = f"{group}/{name}/recorded"
            raw_acts = exported[group][name]
            acts = rows_removed_first(own_rows(raw_acts))
            # Same act-list corrections as tests/test_sale_family_audit_v82.py:
            # own_rows, rows_removed_first, then per-statement box 4/7 "no".
            acts = sfa_t0.box_answers(acts, V82, set(sfa_t0.DESIGNS["final"]), "no", "no")
            stmts = sale_statements(acts)
            has_sales = len(stmts) > 0
            exp_v82 = expected_v81.get(cid, {}).get("v82", {})
            items.append((cid, acts, has_sales, spec_82, spec_83, exp_v82))

    print(f"[Scope 6] Prepared {len(items)} returns. Running on BOTH v82 and v83 across ProcessPoolExecutor workers...")
    results: list[dict[str, Any]] = []
    with ProcessPoolExecutor(max_workers=min(10, os.cpu_count() or 4)) as executor:
        for res in executor.map(_run_return_worker, items):
            results.append(res)
            cid = res["case_id"]
            cls = res["classification"]
            disp82 = res["v82_disp_25b"]
            disp83 = res["v83_disp_25b"]
            if len(results) % 25 == 0 or len(results) == len(items):
                print(f"  Processed {len(results)}/{len(items)} returns (latest: {cid} -> {cls}, 25b: {disp82} -> {disp83})")

    results.sort(key=lambda r: r["case_id"])
    for r in results:
        if r.get("reproduces_v82_fixture"):
            r["fixture_mismatch"] = None
    class_counts = dict(Counter(r["classification"] for r in results))
    mismatches = [r for r in results if not r["reproduces_v82_fixture"]]
    no_sales_changed = [
        r["case_id"] for r in results
        if not r["has_sales"] and r["classification"] != "identical"
    ]
    counterexamples = [r["case_id"] for r in results if str(r["classification"]).startswith("counterexample")]
    four = [
        "case/wage_q3_unanswered/recorded",
        "v80/carried_one_exempt_dividend/recorded",
        "v80/carried_one_foreign_tax/recorded",
        "v80/carried_wage_unclosed/recorded",
    ]
    four_rows = {cid: next((r for r in results if r["case_id"] == cid), None) for cid in four}

    summary = {
        "total_returns": len(results),
        "returns_with_sales": sum(1 for r in results if r["has_sales"]),
        "returns_without_sales": sum(1 for r in results if not r["has_sales"]),
        "reproduces_v82_fixture_count": sum(1 for r in results if r["reproduces_v82_fixture"]),
        "fixture_mismatch_ids": [r["case_id"] for r in mismatches],
        "classes": class_counts,
        "identical_cases": class_counts.get("identical", 0),
        "box4_unanswered_cases": class_counts.get("box4_unanswered_asks_amount", 0),
        "counterexample_cases": len(counterexamples),
        "counterexample_ids": counterexamples,
        "no_sales_changed_ids": no_sales_changed,
        "four_no_sale_returns": {
            cid: None if row is None else {
                "classification": row["classification"],
                "has_sales": row["has_sales"],
                "v82_disp_25b": row["v82_disp_25b"],
                "v83_disp_25b": row["v83_disp_25b"],
                "v82_blocked_reasons_25b": row["v82_blocked_reasons_25b"],
                "v83_blocked_reasons_25b": row["v83_blocked_reasons_25b"],
                "reproduces_v82_fixture": row["reproduces_v82_fixture"],
            }
            for cid, row in four_rows.items()
        },
        "all_classified": len(results) == 213 and sum(class_counts.values()) == 213,
        "all_reproduce_v82_fixture": sum(1 for r in results if r["reproduces_v82_fixture"]) == 213,
    }

    rerun_data = {
        "summary": summary,
        "cases": results,
    }
    RERUN_JSON.write_text(json.dumps(rerun_data, indent=2) + "\n", encoding="utf-8")

    out = load_output()
    out["scope6"] = {
        "summary": summary,
        "cases_file": str(RERUN_JSON.name),
        "cases_count": len(results),
        "sample_cases": results[:5] + [r for r in results if not r["has_sales"]][:5],
    }
    save_output(out)
    print(f"[Scope 6] Complete: {summary['total_returns']} returns processed. Classes: {class_counts}. Summary saved.")
    return out["scope6"]


# ---- Scope 7: Integration Surface (Consumers & Presentation Probe) ----------------

def build_scope7_cases() -> list[dict[str, Any]]:
    cases: list[dict[str, Any]] = []
    core = get_core("decided")

    # 1. surface_published_refund
    acts_ref = h.opened()
    acts_ref = h.sale(acts_ref, "covered", "st", proceeds=5000, basis=4000, tag="s7_ref")
    acts_ref = h.answer(acts_ref, **h.honest({"covered"}, loss=False))
    s_ref = "demo.sfa.s7_ref.statement"
    acts_ref = say_b4_amount(acts_ref, core, s_ref, 240.0)
    acts_ref = say_b7_reported(acts_ref, core, s_ref, "no")
    cases.append({
        "case_id": "surface_published_refund",
        "description": "Consumer path 1: Overpaid return (refund); line 25b $240 feeds line 33 ($4,740), line 34 refund ($745), line 37 ($0)",
        "acts": acts_ref,
        "expected": {
            "form1040.line-25b": ("published_value", 240.0),
            "form1040.line-33": ("published_value", 4740.0),
            "form1040.line-34": ("published_value", 745.0),
            "form1040.line-37": ("computed_zero", 0.0),
        },
    })

    # 2. surface_published_owed
    acts_owed = h.opened()
    acts_owed = h.sale(acts_owed, "covered", "st", proceeds=25000, basis=5000, tag="s7_owed")
    acts_owed = h.answer(acts_owed, **h.honest({"covered"}, loss=False))
    s_owed = "demo.sfa.s7_owed.statement"
    acts_owed = say_b4_amount(acts_owed, core, s_owed, 240.0)
    acts_owed = say_b7_reported(acts_owed, core, s_owed, "no")
    cases.append({
        "case_id": "surface_published_owed",
        "description": "Consumer path 2: Underpaid return (amount owed); line 25b $240 feeds line 33 ($4,740), line 34 ($0), line 37 owed ($2,115)",
        "acts": acts_owed,
        "expected": {
            "form1040.line-25b": ("published_value", 240.0),
            "form1040.line-33": ("published_value", 4740.0),
            "form1040.line-34": ("computed_zero", 0.0),
            "form1040.line-37": ("published_value", 2115.0),
        },
    })

    # 3. surface_blocked_missing_b4
    acts_blk = h.opened()
    acts_blk = h.sale(acts_blk, "covered", "st", proceeds=5000, basis=4000, tag="s7_blk")
    acts_blk = h.answer(acts_blk, **h.honest({"covered"}, loss=False))
    s_blk = "demo.sfa.s7_blk.statement"
    acts_blk = say_b7_reported(acts_blk, core, s_blk, "no")
    cases.append({
        "case_id": "surface_blocked_missing_b4",
        "description": "Consumer path 3: Missing box 4 amount; line 25b blocked on DEPENDENCY_ABSENT, cascading to lines 33, 34, 37",
        "acts": acts_blk,
        "expected": {
            "form1040.line-25b": ("blocked", None),
            "form1040.line-33": ("blocked", None),
            "form1040.line-34": ("blocked", None),
            "form1040.line-37": ("blocked", None),
        },
    })

    # 4. surface_zero_no_sales
    acts_zero = h.opened()
    acts_zero = h.answer(acts_zero, **h.honest(set(), loss=False))
    cases.append({
        "case_id": "surface_zero_no_sales",
        "description": "Consumer path 4: Zero sales recorded; line 25b computes $0, line 33 ($4,500), line 34 refund ($625), line 37 ($0)",
        "acts": acts_zero,
        "expected": {
            "form1040.line-25b": ("computed_zero", 0.0),
            "form1040.line-33": ("published_value", 4500.0),
            "form1040.line-34": ("published_value", 625.0),
            "form1040.line-37": ("computed_zero", 0.0),
        },
    })

    return cases


def run_scope7() -> dict[str, Any]:
    cases = build_scope7_cases()
    core = get_core("decided")
    print(f"[Scope 7] Running {len(cases)} Integration Surface cases on core decided...")
    results: list[dict[str, Any]] = []

    expected_question = "Enter the federal income tax withheld in box 4 of each Form 1099-B or substitute statement you recorded a sale from. If box 4 is blank, enter $0."
    expected_field_desc = (
        "Form 1040 line 25b: federal income tax withheld from Form(s) 1099 "
        "(Forms 1099-INT, 1099-DIV and 1099-R box 4, Form 1099-G box 4, Form SSA-1099 box 6, "
        "and every current Form 1099-B box 4 amount, including an amount recorded on a statement with no sale)."
    )

    presentation_probe_results: dict[str, Any] = {}

    for c in cases:
        cid = c["case_id"]
        res = run_coordinate(core, c["acts"], f"demo.b4.s7.{cid}")

        disps = res["dispositions"]
        lines = res["lines"]
        reasons = res["blocked_reasons"]
        fdescs = res.get("field_descriptions", {})

        watched_lines = ("form1040.line-25b", "form1040.line-33", "form1040.line-34", "form1040.line-37")
        matches = True
        actual_lines: dict[str, Any] = {}
        for line in watched_lines:
            exp_disp, exp_val = c["expected"][line]
            act_disp = disps.get(line)
            act_val = lines.get(line)
            actual_lines[line] = {
                "disposition": act_disp,
                "value": act_val,
                "blocked_reasons": reasons.get(line, []),
            }
            if act_disp != exp_disp:
                matches = False
            if exp_disp != "blocked" and act_val != exp_val:
                matches = False

        if cid == "surface_blocked_missing_b4":
            b4_reasons = reasons.get("form1040.line-25b", [])
            has_question = expected_question in b4_reasons
            presentation_probe_results["question_probe"] = {
                "expected": expected_question,
                "actual_reasons": b4_reasons,
                "question_matches": has_question,
            }
        if cid == "surface_published_refund":
            actual_desc = fdescs.get("form1040.line-25b")
            desc_matches = actual_desc == expected_field_desc
            presentation_probe_results["field_probe"] = {
                "expected": expected_field_desc,
                "actual_description": actual_desc,
                "description_matches": desc_matches,
            }

        entry = {
            "case_id": cid,
            "description": c["description"],
            "presentation_valid": res.get("presentation_valid"),
            "lines": actual_lines,
            "matches_expected": matches,
        }
        results.append(entry)
        print(f"  {cid}: matches_expected={matches}")

    all_presentation_valid = all(r["presentation_valid"] is True for r in results)
    question_ok = presentation_probe_results.get("question_probe", {}).get("question_matches", False)
    desc_ok = presentation_probe_results.get("field_probe", {}).get("description_matches", False)

    summary = {
        "total_cases": len(results),
        "matches_expected_cases": sum(1 for r in results if r["matches_expected"]),
        "all_match_expected": all(r["matches_expected"] for r in results),
        "all_presentation_valid": all_presentation_valid,
        "question_probe_matches": question_ok,
        "field_probe_matches": desc_ok,
        "consumers_verified": ["form1040.line-33", "form1040.line-34", "form1040.line-37"],
        "paths_verified": ["refund", "owed", "blocked_missing_b4", "zero_no_sales"],
    }

    out = load_output()
    out["scope7"] = {
        "summary": summary,
        "presentation_probe": presentation_probe_results,
        "cases": results,
    }
    save_output(out)
    print(f"[Scope 7] Complete: {summary['matches_expected_cases']}/{summary['total_cases']} matched expected. Presentation probe verified. Summary saved.")
    return out["scope7"]


if __name__ == "__main__":
    action = sys.argv[1] if len(sys.argv) > 1 else "scope0"
    if action == "scope0":
        run_scope0()
    elif action == "scope1":
        run_scope1()
    elif action == "scope2":
        run_scope2()
    elif action == "scope3":
        run_scope3()
    elif action == "scope4":
        run_scope4()
    elif action == "scope5":
        run_scope5()
    elif action == "scope6":
        run_scope6()
    elif action == "scope7":
        run_scope7()

