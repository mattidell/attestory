"""Track 0 adversarial closure for line 12d's boxes being shown.

Evidence for docs/phases/engine-breadth/milestones/line12d-boxes.md.
Charter: docs/reviews/line12d-boxes/charter-track0.md.

Every case is a ``live_coordinate_run`` of synthetic demo.* findings on
published v89 and on scratch v90 (``prototype.py``, built outside the
repository). Expected box states and line 12e come from the 2025
instructions (``age-blindness-asked-evidence/law.json``, quoted in
``trace.json``), coded here as ``expected_boxes`` and ``hand_12e``. They are
never read from what the prototype publishes.

The page change (Decision 1) is ``track0-page.diff``. ``page`` applies it to
a copy of ``packages/presentation/pages/citation-walk.v1.html`` in a scratch
directory; ``packages/`` is never edited.

    python3 track0.py page      <scratch>
    python3 track0.py authority <scratch>/v90/core.json
    python3 track0.py matrix    <scratch>/v90/core.json
    python3 track0.py late      <scratch>/v90/core.json
    python3 track0.py reuse     <scratch>/v90/core.json
    python3 track0.py neighbour <scratch>/v90/core.json
    python3 track0.py surface   <scratch>/v90/core.json <scratch>

Each subcommand writes ``track0-<name>.json`` beside this file.
"""

from __future__ import annotations

import copy
import hashlib
import json
import re
import shutil
import subprocess
import sys
import tempfile
import time
from collections import Counter
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
for entry in (str(REPO), str(HERE)):
    if entry not in sys.path:
        sys.path.insert(0, entry)

import probe as pr  # noqa: E402
import prototype as proto  # noqa: E402

P = "tax.us.2025."
AGE, BLIND, S_AGE, S_BLIND = pr.AGE, pr.BLIND, pr.S_AGE, pr.S_BLIND
COND, STATUS, DEPENDENT, SSN = pr.COND, pr.STATUS, pr.DEPENDENT, pr.SSN
S_SSN = P + "senior-deduction.spouse-valid-ssn"
LIVED_APART = P + "mfs-lived-apart-all-year"  # line 6d's not-checked rule reads "no"
MFJ, MFS, HOH, QSS = pr.MFJ, pr.MFS, pr.HOH, pr.QSS
PAGE = Path("packages/presentation/pages/citation-walk.v1.html")
DIFF = HERE / "track0-page.diff"
BOX_FACT = {"you_age": AGE, "you_blind": BLIND, "spouse_age": S_AGE, "spouse_blind": S_BLIND}
Acts = list[dict[str, Any]]

# 2025 Standard Deduction Chart for People Who Were Born Before January 2,
# 1961, or Were Blind (law.json "chart"), indexed by the number of boxes.
CHART = {
    "single": (15750, 17750, 19750),
    MFJ: (31500, 33100, 34700, 36300, 37900),
    QSS: (31500, 33100, 34700),
    MFS: (15750, 17350, 18950, 20550, 22150),
    HOH: (23625, 25625, 27625),
}


# ---- law -------------------------------------------------------------------

def spouse_shown(status: str, condition: bool | None) -> bool | None:
    """Line 12d: spouse boxes on a joint return, or a separate return whose
    spouse had no income, isn't filing and can't be claimed. None: unknown."""
    if status == MFJ:
        return True
    if status == MFS:
        return condition
    return False


def expected_boxes(status: str, answers: dict[str, Any], *, dependent: bool = False) -> dict[str, str]:
    out: dict[str, str] = {}
    for key, fact in (("you_age", AGE), ("you_blind", BLIND)):
        out[key] = "blocked" if fact not in answers else ("checked" if answers[fact] else "not_checked")
    shown = False if dependent else spouse_shown(status, answers.get(COND))
    for key, fact in (("spouse_age", S_AGE), ("spouse_blind", S_BLIND)):
        if shown is None:
            out[key] = "blocked"
        elif not shown:
            out[key] = "hidden"
        else:
            out[key] = "blocked" if fact not in answers else ("checked" if answers[fact] else "not_checked")
    return out


def hand_12e(status: str, boxes: dict[str, str], *, dependent: bool = False, wages: int = 50000) -> Any:
    if any(state == "blocked" for state in boxes.values()):
        return "blocked"
    count = sum(state == "checked" for state in boxes.values())
    if dependent:
        # Standard Deduction Worksheet for Dependents: greater of 1,350 or
        # earned income plus 450, capped at the basic amount, plus 2,000 a box.
        return min(max(1350, wages + 450), 15750) + 2000 * count
    return CHART[status][count]


# ---- runs ------------------------------------------------------------------

def cores(core_json: Path) -> dict[str, Any]:
    return {"v89": pr.core(None), "v90": pr.core(core_json)}


def build(status: str, answers: dict[str, Any], *, dependent: bool = False) -> Acts:
    acts = pr.base("single" if dependent else status)
    extra: dict[str, Any] = {DEPENDENT: "yes"} if dependent else {}
    if answers.get(AGE) and status != MFS:
        extra[SSN] = "yes"
    if answers.get(S_AGE) and status == MFJ:
        extra[S_SSN] = "yes"
    return pr.answer(acts, {**extra, **answers})


def run(c: Any, acts: Acts, run_id: str, *, pages: dict[str, Path] | None = None,
        page_out: Path | None = None) -> dict[str, Any]:
    """probe.execute, plus the line 12d sections and, optionally, saved pages.

    ``pages`` maps a page name to a directory holding PAGE; each is rendered
    with live_session._render_page, the coordinator's own saved-page step.
    """
    from packages.derivation.live_session import _render_page

    h = pr.harness()
    surface = c.surface()
    with h.loader_entries(c):
        try:
            finished = h._handover(
                h._finish(acts, package_path=c.package_path, package_version=c.version,
                          release_path=c.release_path, release_version=c.release_version, note=run_id),
                surface=surface, reconfirm=True,
            )
            with tempfile.TemporaryDirectory() as tmp:
                capability = h.WorkspaceCapability(Path(tmp) / "L")
                outcome = h.live_coordinate_run(
                    capability, repo_root=REPO, authoritative_acts=finished,
                    workspace_revision=len(finished), run_scope={"jurisdiction": "us", "year": h.YEAR},
                    scope_user=h.ccr.USER, request={"schema": "run-request.v1"}, run_id=run_id,
                    governance_pins=[], surface=surface, output_name="out.json",
                )
                if outcome.refusal is not None:
                    return {"outcome": "refused", "reason": outcome.refusal.reason}
                model = json.loads(outcome.presentation_path.read_text(encoding="utf-8"))
                if pages and page_out is not None:
                    page_out.mkdir(parents=True, exist_ok=True)
                    for name, root in pages.items():
                        page = _render_page(root, capability, outcome.presentation_path)
                        (page_out / f"{run_id}.{name}.html").write_bytes(page)
        except Exception as exc:  # noqa: BLE001 - a rejected act list is a result
            return {"outcome": "error", "error": type(exc).__name__, "message": pr.scrub(str(exc))[:300]}
    sections = {}
    line12e: Any = None
    for section in model.get("sections") or []:
        fid = str((section.get("field") or {}).get("id") or "").removeprefix(P)
        resolved = section.get("resolved") or {}
        disp = resolved.get("disposition")
        value = resolved.get("value")
        if isinstance(value, float) and value.is_integer():
            value = int(value)
        sections[fid] = [disp, value]
        if fid == "form1040.line-12e":
            line12e = value if value is not None else disp
    return {
        "outcome": "success",
        "boxes": pr.boxes_from_model(model),
        "form1040.line-12e": line12e,
        "sections": sections,
    }


def judge(row: dict[str, Any], results: dict[str, Any]) -> dict[str, Any]:
    v89, v90 = results["v89"], results["v90"]
    boxes_ok = v90.get("boxes") == row["boxes_expected"]
    v89_absent = all(state == "absent" for state in (v89.get("boxes") or {}).values())
    hand_ok = v90.get("form1040.line-12e") == row["hand_12e"] == v89.get("form1040.line-12e")
    same = (v89.get("sections") or {}) == {
        k: v for k, v in (v90.get("sections") or {}).items() if not k.startswith("form1040.line-12d-")
    }
    added = sorted(k for k in (v90.get("sections") or {}) if k not in (v89.get("sections") or {}))
    row.update({
        "boxes_v90": v90.get("boxes"),
        "line12e_v89": v89.get("form1040.line-12e"),
        "line12e_v90": v90.get("form1040.line-12e"),
        "v89_sections_unchanged_on_v90": same,
        "v90_added_sections": [k.removeprefix("form1040.") for k in added],
        "outcome": [v89.get("outcome"), v90.get("outcome")],
    })
    row["pass"] = bool(
        boxes_ok and v89_absent and hand_ok and same
        and all(k.startswith("form1040.line-12d-") for k in added)
        and row["outcome"] == ["success", "success"]
    )
    return row


def case(c: dict[str, Any], case_id: str, says: str, status: str, answers: dict[str, Any],
         *, dependent: bool = False, acts: Acts | None = None) -> dict[str, Any]:
    acts = acts if acts is not None else build(status, answers, dependent=dependent)
    boxes = expected_boxes(status, answers, dependent=dependent)
    row: dict[str, Any] = {
        "id": case_id,
        "says": says,
        "status": status + (" (dependent filer)" if dependent else ""),
        "answers": {k.removeprefix(P): v for k, v in answers.items()},
        "boxes_expected": boxes,
        "hand_12e": hand_12e(status, boxes, dependent=dependent),
    }
    results = {name: run(core, acts, f"demo.l12d.t0.{name}.{case_id}") for name, core in c.items()}
    judged = judge(row, results)
    print(case_id, "PASS" if judged["pass"] else "FAIL", judged["boxes_v90"], judged["line12e_v90"], flush=True)
    return judged


def write(name: str, payload: dict[str, Any]) -> None:
    text = json.dumps(payload, indent=2) + "\n"
    for needle in ("/Users/", "/private/", "/tmp/", "/var/"):
        if needle in text:
            raise SystemExit(f"{name} contains {needle}")
    (HERE / f"track0-{name}.json").write_text(text, encoding="utf-8")


def tally(rows: list[dict[str, Any]]) -> dict[str, Any]:
    return {"cases": len(rows), "pass": sum(r["pass"] for r in rows),
            "fail": [r["id"] for r in rows if not r["pass"]]}


# ---- item 0: page ------------------------------------------------------------

def patched_page(scratch: Path) -> Path:
    """Copy the product page under <scratch>/pageroot and apply track0-page.diff."""
    root = scratch / "pageroot"
    target = root / PAGE
    target.parent.mkdir(parents=True, exist_ok=True)
    text = (REPO / PAGE).read_text(encoding="utf-8")
    removed, added = [], []
    for line in DIFF.read_text(encoding="utf-8").splitlines():
        if line.startswith(("---", "+++", "@@")):
            continue
        if line.startswith("-"):
            removed.append(line[1:])
        elif line.startswith("+"):
            added.append(line[1:])
    old, new = "\n".join(removed) + "\n", "\n".join(added) + "\n"
    if text.count(old) != 1:
        raise SystemExit("track0-page.diff does not apply to the product page")
    target.write_text(text.replace(old, new), encoding="utf-8")
    return root


def unmodified_page(scratch: Path) -> Path:
    root = scratch / "pageroot-unmodified"
    (root / PAGE).parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(REPO / PAGE, root / PAGE)
    return root


def cmd_page(scratch: Path) -> None:
    root = patched_page(scratch)
    body = (root / PAGE).read_text(encoding="utf-8")
    start = body.index('  if (disposition === "published_categorical") {')
    branch = body[start:body.index("\n  }\n", start) + 4]
    write("page", {
        "diff": "track0-page.diff",
        "applies_to": str(PAGE),
        "product_page_sha256": hashlib.sha256((REPO / PAGE).read_bytes()).hexdigest(),
        "scratch_page_sha256": hashlib.sha256(body.encode("utf-8")).hexdigest(),
        "categorical_branch_after": branch.splitlines(),
        "reads_finding_value": "finding" in branch.replace("Never read resolved.act.finding.value", ""),
        "changed_outside_categorical_branch": not all(
            line[1:] in branch for line in DIFF.read_text(encoding="utf-8").splitlines()
            if line.startswith("+") and not line.startswith("+++")
        ),
        "harness_copy": {
            "path": "tools/presentation_harness/examples/pages/citation-walk.v1.html",
            "carries_same_branch": 'if (instruction.render !== "checked")' in (
                REPO / "tools/presentation_harness/examples/pages/citation-walk.v1.html"
            ).read_text(encoding="utf-8"),
        },
    })
    print(json.dumps({"branch": branch.splitlines()}, indent=1))


# ---- item 1: authority -------------------------------------------------------

def cmd_authority(core_json: Path) -> None:
    c = cores(core_json)
    F = False
    rows = [
        case(c, "auth_you_age_yes", "Single; born before January 2, 1961; not blind.", "single",
             {AGE: True, BLIND: F}),
        case(c, "auth_you_blind_yes", "Single; not 65; blind.", "single", {AGE: F, BLIND: True}),
        case(c, "auth_you_unanswered", "Single; neither question answered.", "single", {}),
        case(c, "auth_spouse_age_joint", "Joint; only the spouse born before January 2, 1961.", MFJ,
             {AGE: F, BLIND: F, S_AGE: True, S_BLIND: F}),
        case(c, "auth_spouse_blind_joint", "Joint; only the spouse blind.", MFJ,
             {AGE: F, BLIND: F, S_AGE: F, S_BLIND: True}),
        case(c, "auth_spouse_separate_yes", "Separate; spouse blind; condition yes.", MFS,
             {AGE: F, BLIND: F, S_AGE: F, S_BLIND: True, COND: True}),
        case(c, "auth_spouse_separate_no", "Separate; spouse blind recorded; condition no.", MFS,
             {AGE: F, BLIND: F, S_AGE: F, S_BLIND: True, COND: F}),
        case(c, "auth_spouse_recorded_on_hoh", "Head of household; spouse facts recorded true.", HOH,
             {AGE: F, BLIND: F, S_AGE: True, S_BLIND: True}),
        case(c, "auth_spouse_recorded_on_qss", "Qualifying surviving spouse; spouse facts recorded true.", QSS,
             {AGE: F, BLIND: F, S_AGE: True, S_BLIND: True}),
    ]
    # hand_12e for the two recorded-on cases already ignores the spouse boxes
    # because expected_boxes hides them on those statuses.
    write("authority", {"cores": ["v89 published", "v90 scratch"], **tally(rows), "rows": rows})


# ---- item 2: matrix ----------------------------------------------------------

def cmd_matrix(core_json: Path) -> None:
    c = cores(core_json)
    variants = [
        ("single", "single", None, False),
        ("joint", MFJ, None, False),
        ("separate_yes", MFS, True, False),
        ("separate_no", MFS, False, False),
        ("hoh", HOH, None, False),
        ("qss", QSS, None, False),
        ("dependent", "single", None, True),
    ]
    rows = []
    for name, status, cond, dependent in variants:
        spouse_asked = status in (MFJ, MFS) and not dependent
        for answer in ("true", "false", "unanswered"):
            answers: dict[str, Any] = {}
            if answer != "unanswered":
                value = answer == "true"
                answers = {AGE: value, BLIND: value}
                if spouse_asked:
                    answers.update({S_AGE: value, S_BLIND: value})
            if cond is not None:
                answers[COND] = cond
            rows.append(case(c, f"m_{name}_{answer}", f"{name}: the four facts {answer}", status, answers,
                             dependent=dependent))
    write("matrix", {"cores": ["v89 published", "v90 scratch"], **tally(rows), "rows": rows})


# ---- item 3: late ------------------------------------------------------------

def cmd_late(core_json: Path) -> None:
    c = cores(core_json)
    h = pr.harness()
    traces = []

    def step(trace: list[dict[str, Any]], tid: str, n: int, says: str, status: str,
             answers: dict[str, Any], acts: Acts) -> None:
        trace.append(case(c, f"{tid}_{n}", says, status, answers, acts=acts))

    # Joint to separate with a spouse box checked.
    t: list[dict[str, Any]] = []
    a = {AGE: False, BLIND: False, S_AGE: True, S_BLIND: False}
    acts = build(MFJ, a)
    step(t, "late_joint_to_separate", 0, "Joint; spouse born before January 2, 1961.", MFJ, a, acts)
    acts = h.say(acts, STATUS, MFS, "fs")
    step(t, "late_joint_to_separate", 1, "Status changed to separate; condition unanswered.", MFS, a, acts)
    acts = pr.answer(acts, {COND: True})
    step(t, "late_joint_to_separate", 2, "Condition answered yes.", MFS, {**a, COND: True}, acts)
    acts = pr.answer(acts, {COND: False})
    step(t, "late_joint_to_separate", 3, "Condition replaced with no.", MFS, {**a, COND: False}, acts)
    traces.append({"id": "late_joint_to_separate", "steps": t})

    # Joint to head of household.
    t = []
    acts = build(MFJ, a)
    step(t, "late_joint_to_hoh", 0, "Joint; spouse born before January 2, 1961.", MFJ, a, acts)
    acts = h.say(acts, STATUS, HOH, "fs")
    step(t, "late_joint_to_hoh", 1, "Status changed to head of household; spouse facts stay recorded.",
         HOH, a, acts)
    traces.append({"id": "late_joint_to_hoh", "steps": t})

    # An answer replaced.
    t = []
    a = {AGE: True, BLIND: False}
    acts = build("single", a)
    step(t, "late_answer_replaced", 0, "Single; born before January 2, 1961.", "single", a, acts)
    acts = pr.answer(acts, {AGE: False})
    step(t, "late_answer_replaced", 1, "Age answer replaced with no.", "single", {AGE: False, BLIND: False}, acts)
    acts = pr.answer(acts, {BLIND: True})
    step(t, "late_answer_replaced", 2, "Blindness answer replaced with yes.", "single",
         {AGE: False, BLIND: True}, acts)
    traces.append({"id": "late_answer_replaced", "steps": t})

    rows = [s for trace in traces for s in trace["steps"]]
    write("late", {"cores": ["v89 published", "v90 scratch"], **tally(rows), "traces": traces})


# ---- item 4: reuse -----------------------------------------------------------

def cmd_reuse(core_json: Path) -> None:
    body = json.loads(core_json.read_text(encoding="utf-8"))
    content = Path(body["content"])
    v89 = json.loads((proto.CONTENT / "package.core-calculations.v89.json").read_text(encoding="utf-8"))
    v90 = json.loads((content / "package.core-calculations.v90.json").read_text(encoding="utf-8"))
    key = lambda m: (m["id"], m["version"])  # noqa: E731
    m89 = {key(m): m for m in v89["members"]}
    m90 = {key(m): m for m in v90["members"]}
    kept = all(k in m90 and m90[k] == m for k, m in m89.items())
    added = sorted(k for k in m90 if k not in m89)
    new_files = {name for name, _ in proto.artifacts()}
    new_symbols = sorted({b["publishes"] for _, b in proto.artifacts() if "publishes" in b})
    readers: dict[str, list[str]] = {}
    for path in sorted(content.glob("*.json")):
        if path.name in new_files or path.name.startswith(("package.", "published-packages.")):
            continue
        text = path.read_text(encoding="utf-8")
        for symbol in new_symbols:
            if symbol in text or symbol.removeprefix(P) in text:
                readers.setdefault(symbol, []).append(path.name)
    reads = {}
    for name, artifact in proto.artifacts():
        if artifact.get("schema") == "rule-artifact.v3":
            refs = sorted(set(re.findall(r'"name": "([^"]+)"', json.dumps(artifact["when"]))))
            reads[artifact["id"].removeprefix(P)] = {"reads": refs, "publishes": artifact["publishes"].removeprefix(P)}
    binders = {
        a["id"].removeprefix(P): a["binds_symbol"].removeprefix(P)
        for _, a in proto.artifacts() if a.get("schema") == "form-field.v3"
    }
    matrix = json.loads((HERE / "track0-matrix.json").read_text(encoding="utf-8")) if (
        HERE / "track0-matrix.json").exists() else {"rows": []}
    same_12e = [r["id"] for r in matrix["rows"] if r["line12e_v89"] == r["line12e_v90"]]
    payload = {
        "v89_members_unchanged_in_v90": kept,
        "v89_member_count": len(m89),
        "v90_added_members": [[i.removeprefix(P), v] for i, v in added],
        "new_symbols": [s.removeprefix(P) for s in new_symbols],
        "new_symbols_read_by_existing_content": {k.removeprefix(P): v for k, v in readers.items()},
        "new_rules": reads,
        "new_fields_bind": binders,
        "matrix_line12e_equal_on_v89_and_v90": f"{len(same_12e)} of {len(matrix['rows'])}",
    }
    payload["pass"] = bool(kept and not readers and len(same_12e) == len(matrix["rows"]) and matrix["rows"]
                           and all(set(r["reads"]) <= {"filing_status", "spouse_separate_condition",
                                                       "taxpayer_over_65", "taxpayer_blind",
                                                       "spouse_over_65", "spouse_blind"}
                                   for r in reads.values()))
    write("reuse", payload)
    print(json.dumps({k: payload[k] for k in ("pass", "v89_members_unchanged_in_v90",
                                               "new_symbols_read_by_existing_content",
                                               "matrix_line12e_equal_on_v89_and_v90")}, indent=1))


# ---- item 5: neighbour sample -------------------------------------------------

def sample(keys: list[str], per_set: int = 8) -> list[str]:
    by_set: dict[str, list[str]] = {}
    for key in keys:
        by_set.setdefault(key.split("/", 1)[0], []).append(key)
    picked = []
    for _, group in sorted(by_set.items()):
        step = len(group) / per_set
        picked += [group[int(i * step)] for i in range(min(per_set, len(group)))]
    return picked


def cmd_neighbour(core_json: Path) -> None:
    import rerun
    from tools import recorded_replay as rr

    lists = rr.recorded_lists()
    chosen = set(sample([k for k, _ in lists]))
    subset = [(k, a) for k, a in lists if k in chosen]
    core_a, core_b = rr.resolve_core("v89"), rr.resolve_core(core_json)
    part = core_json.resolve().parent / "track0-neighbour-part.json"
    started = time.time()
    results = rr.replay(subset, (core_a, core_b), rerun.per_list, workers=4, part=part)
    wall = round(time.time() - started, 1)

    def drawn_alerts(fids: list[str], content: Path) -> list[str]:
        # The scratch page draws checked and not_checked; anything else alerts.
        return [f for f in fids if rerun._render(str(content), f) not in {"checked", "not_checked"}]

    counts: Counter[str] = Counter()
    by_set: dict[str, Counter[str]] = {}
    rows = {}
    for key, row in results.items():
        cls = rerun.final_class(row)
        counts[cls] += 1
        by_set.setdefault(key.split("/", 1)[0], Counter())[cls] += 1
        rows[key] = {
            "class": cls,
            "pin_class": row["class"],
            "page_changed": row["page_changed"],
            "page_added": [f.removeprefix("form1040.") for f in row["page_added"]],
            "boxes_v90": row["boxes_v90"],
            "outcome": [row["outcome_v89"], row["outcome_v90"]],
            "alerts_v89_unmodified_page": row["alerts_v89"],
            "alerts_v90_unmodified_page": row["alerts_v90"],
            "alerts_v90_scratch_page": drawn_alerts(row["alerts_v90"], core_b.content),
        }
    write("neighbour", {
        "status": (f"SAMPLE: {len(results)} of {len(lists)} recorded lists. The full "
                   f"{len(lists)}-list replay was NOT run (Decision 5); it is owed before the PR goes ready."),
        "sample_rule": "every recorded list's key, grouped by fixture set, 8 evenly spaced per set",
        "answer_rule": "rerun.py: state_taxpayer_facts(acts, core='v88') on both cores",
        "classes_defined": "rerun.py final_class",
        "workers": 4,
        "lists": len(results),
        "live_runs": 2 * len(results),
        "wall_time_s": wall,
        "counts": dict(sorted(counts.items())),
        "by_set": {k: dict(sorted(v.items())) for k, v in sorted(by_set.items())},
        "rows": rows,
    })
    print(json.dumps({"wall": wall, "counts": counts, "by_set": by_set}, default=dict, indent=1))


# ---- item 6: surface ----------------------------------------------------------

SURFACE = [
    ("s_single_both_false", "Single; not 65; not blind.", "single", {AGE: False, BLIND: False}),
    ("s_single_age_true", "Single; born before January 2, 1961; not blind.", "single", {AGE: True, BLIND: False}),
    ("s_joint_spouse_age", "Joint; only the spouse born before January 2, 1961.", MFJ,
     {AGE: False, BLIND: False, S_AGE: True, S_BLIND: False}),
    ("s_separate_condition_no", "Separate; spouse blind recorded; condition no.", MFS,
     {AGE: False, BLIND: False, S_AGE: False, S_BLIND: True, COND: False}),
    ("s_separate_lived_with_spouse",
     "Separate; condition no; lived with the spouse during 2025, so line 6d publishes not_checked.", MFS,
     {AGE: False, BLIND: False, S_AGE: False, S_BLIND: True, COND: False, LIVED_APART: "no"}),
    ("s_hoh", "Head of household; not 65; not blind.", HOH, {AGE: False, BLIND: False}),
    ("s_single_unanswered", "Single; age and blindness unanswered.", "single", {}),
]


def cmd_surface(core_json: Path, scratch: Path) -> None:
    c = cores(core_json)
    patched, plain = patched_page(scratch), unmodified_page(scratch)
    out = scratch / "browser"
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    cases_cfg = []
    meta = {}
    for case_id, says, status, answers in SURFACE:
        acts = build(status, answers)
        res = run(c["v90"], acts, f"demo.l12d.t0.v90.{case_id}", pages={"scratch": patched, "unmodified": plain},
                  page_out=out)
        meta[case_id] = {"says": says, "status": status, "core": "v90",
                         "boxes_expected": expected_boxes(status, answers), "model_boxes": res.get("boxes"),
                         "outcome": res.get("outcome")}
        for name in ("scratch", "unmodified"):
            cases_cfg.append({"id": f"{case_id}@v90.{name}", "page": f"demo.l12d.t0.v90.{case_id}.{name}.html"})
    case_id, says, status, answers = SURFACE[0]
    res = run(c["v89"], build(status, answers), f"demo.l12d.t0.v89.{case_id}",
              pages={"scratch": patched, "unmodified": plain}, page_out=out)
    meta["v89_" + case_id] = {"says": says, "status": status, "core": "v89", "outcome": res.get("outcome")}
    for name in ("scratch", "unmodified"):
        cases_cfg.append({"id": f"v89_{case_id}@v89.{name}", "page": f"demo.l12d.t0.v89.{case_id}.{name}.html"})
    (out / "cases.json").write_text(json.dumps({"root": str(out), "cases": cases_cfg}, indent=1), encoding="utf-8")
    started = time.time()
    proc = subprocess.run(["node", str(HERE / "observe.mjs"), str(out / "cases.json")], cwd=REPO,
                          capture_output=True, text=True, timeout=300)
    if proc.returncode != 0:
        raise SystemExit("browser observation failed: " + pr.scrub(proc.stderr)[-400:])
    dom = json.loads((out / "dom-observations.json").read_text(encoding="utf-8"))
    browser_s = round(time.time() - started, 1)

    observed = {}
    for item in dom["cases"]:
        boxes = {}
        for s in item["sections"]:
            if s["id"].startswith("line-12d-"):
                boxes[s["id"]] = {k: s[k] for k in ("heading", "badge", "value", "value_aria_label", "explain",
                                                    "section_error", "citation_buttons")}
        observed[item["id"]] = {
            "section_count": item["section_count"],
            "non_loopback_request": item["non_loopback_request"],
            "alerts": item["alerts"],
            "line12d_sections": boxes,
            "line6": {s["id"]: {"value": s["value"], "section_error": s["section_error"]}
                      for s in item["sections"] if s["id"].startswith("line-6c") or s["id"].startswith("line-6d")},
            "sections_text_sha256": hashlib.sha256(
                json.dumps([s for s in item["sections"]], sort_keys=True).encode("utf-8")).hexdigest(),
        }

    def drawn_state(sections: dict[str, Any], slug_line: str) -> str:
        on = sections.get(f"line-{slug_line}") or {}
        off = sections.get(f"line-{slug_line}-not-checked") or {}
        if on.get("section_error") or off.get("section_error"):
            return "alert"
        if on.get("value") == "checked" and off.get("value") == "Not applicable.":
            return "checked"
        if off.get("value") == "not checked" and on.get("value") == "Not applicable.":
            return "not_checked"
        if on.get("value") == off.get("value") == "Not applicable.":
            return "hidden"
        if "No value published" in (on.get("value") or "") and "No value published" in (off.get("value") or ""):
            return "blocked"
        return "other"

    verdicts = {}
    for case_id, _, status, answers in SURFACE:
        got = observed[f"{case_id}@v90.scratch"]["line12d_sections"]
        drawn = {box["key"]: drawn_state(got, box["line"]) for box in proto.BOXES}
        l12d_alerts = [a for a in observed[f"{case_id}@v90.scratch"]["alerts"] if a["id"].startswith("line-12d-")]
        verdicts[case_id] = {
            "drawn": drawn,
            "expected": expected_boxes(status, answers),
            "line12d_alerts_scratch_page": l12d_alerts,
            "line12d_alerts_unmodified_page": [
                a["id"] for a in observed[f"{case_id}@v90.unmodified"]["alerts"] if a["id"].startswith("line-12d-")],
            "pass": drawn == expected_boxes(status, answers) and not l12d_alerts,
        }
    v89_same = (observed[f"v89_{SURFACE[0][0]}@v89.scratch"]["sections_text_sha256"]
                == observed[f"v89_{SURFACE[0][0]}@v89.unmodified"]["sections_text_sha256"])
    write("surface", {
        "browser": dom.get("browser_version"),
        "node": dom.get("node_version"),
        "browser_wall_s": browser_s,
        "pages": "rendered by packages.derivation.live_session._render_page from each run's presentation model; "
                 "'scratch' is the product page with track0-page.diff applied, 'unmodified' is the product page",
        "cases": meta,
        "verdicts": verdicts,
        "v89_page_identical_on_scratch_and_unmodified": v89_same,
        "pass": sum(v["pass"] for v in verdicts.values()) == len(verdicts) and v89_same,
        "observed": observed,
    })
    print(json.dumps({"verdicts": verdicts, "v89_same": v89_same}, indent=1))


def main() -> None:
    if len(sys.argv) < 3:
        raise SystemExit(__doc__)
    name, arg = sys.argv[1], Path(sys.argv[2])
    if name == "page":
        cmd_page(arg)
    elif name == "surface":
        cmd_surface(arg, Path(sys.argv[3]))
    else:
        {"authority": cmd_authority, "matrix": cmd_matrix, "late": cmd_late, "reuse": cmd_reuse,
         "neighbour": cmd_neighbour}[name](arg)


if __name__ == "__main__":
    main()
