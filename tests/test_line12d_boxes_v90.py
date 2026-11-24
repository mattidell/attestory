"""Published core v90 shows line 12d's four boxes from the recorded answers.

Measured reason: 31 distinct authority, matrix and late runs took 203 s,
the drawn page took 27 s for 2 runs, and the 298 recorded v83 lists took
397 s on 8 workers. Each of those calls the live coordinate run, which is
outside the 3 second fast-lane budget.

Box states and line 12e come from the 2025 instructions (law.json), through
the Track 0 helpers, never from a number the run published. Each case states
the taxpayer's age and blindness through the shared helper. A fact the helper
states is held, including when a spouse box is still blocked. The drawn page
is read with headless Chrome because no no-browser harness asserts this
page's categorical text. The v83 lists are the question-wording neighbour
tasks whose keys start with v83/, read against their fixture in place.
"""

from __future__ import annotations

import copy
import hashlib
import html
import json
import multiprocessing
import re
import shutil
import subprocess
import time
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
from types import ModuleType
from typing import Any, cast

import pytest

from tests import evidence_loader
from tests.helpers.chrome_startup_slot import browser_startup_slot
from tests.helpers.current_core_returns import state_taxpayer_facts
from tests.test_sli_line21_page_reasons import BROWSER
from tools.recorded_replay import ReplayCore, pin_run, recorded_pin_from_expected
from tools.sale_page_observation import _new_owned_chrome_tempdir


pytestmark = pytest.mark.live

REPO = Path(__file__).resolve().parents[1]
EVIDENCE = REPO / "docs/phases/engine-breadth/milestones/line12d-boxes-evidence"
LAW = REPO / "docs/phases/engine-breadth/milestones/age-blindness-asked-evidence/law.json"
QW = REPO / "docs/phases/engine-breadth/milestones/question-wording-evidence"
CONTENT = REPO / "packages/content/tax/2025"
FIXTURE = REPO / "tests/fixtures/f1099b_backup_withholding_v83/expected.json"
LINE12D = ("form1040.line-12d", "form1040-line12d-")
ALERT = "This line is missing display instructions for its status."
BLOCKED = "This line has no result."
HIDDEN = "Not applicable."


def _track() -> ModuleType:
    return evidence_loader.load(EVIDENCE / "track0.py", "l12d_t1_track0")


def _published(track: ModuleType) -> Any:
    return cast(Any, track).pr.harness().Core("v90", "v88", "v88")


def _normalized(node: Any) -> Any:
    if isinstance(node, dict):
        return {key: _normalized(value) for key, value in node.items()}
    if isinstance(node, list):
        return [_normalized(value) for value in node]
    if isinstance(node, str) and node.startswith("demo."):
        return "demo.*"
    return node


def _digest(acts: list[dict[str, Any]]) -> str:
    payload = json.dumps(_normalized(acts), sort_keys=True, default=str).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def _dollars(amount: int) -> str:
    return f"{amount:,}"


def _quotes() -> dict[str, str]:
    body = cast(dict[str, Any], json.loads(LAW.read_text(encoding="utf-8")))
    return {
        str(row["id"]): str(row["text"])
        for row in cast(list[dict[str, Any]], body["quotes"])
    }


def _label(name: str) -> str:
    body = cast(dict[str, Any], json.loads((CONTENT / name).read_text(encoding="utf-8")))
    return str(body["label"])


def _explain(name: str, disposition: str) -> str:
    body = cast(dict[str, Any], json.loads((CONTENT / name).read_text(encoding="utf-8")))
    dispositions = cast(dict[str, Any], body["dispositions"])
    return str(cast(dict[str, Any], dispositions[disposition])["explain"])


def _fact_values(acts: list[dict[str, Any]]) -> dict[str, Any]:
    found: dict[str, Any] = {}
    for act in acts:
        payload = act.get("payload")
        finding = payload.get("finding") if isinstance(payload, dict) else None
        if not isinstance(finding, dict) or "value" not in finding:
            continue
        fact = str(finding.get("fact_id") or "").split("|", 1)[0]
        found[fact] = finding["value"]
    return found


def _boxes_for(count: int, *, spouse_hidden: bool) -> dict[str, str]:
    keys = ("you_age", "you_blind", "spouse_age", "spouse_blind")
    out: dict[str, str] = {}
    seen = 0
    for key in keys:
        if spouse_hidden and key.startswith("spouse"):
            out[key] = "hidden"
            continue
        if seen < count:
            out[key] = "checked"
            seen += 1
        else:
            out[key] = "not_checked"
    return out


def _cases(track: ModuleType) -> list[dict[str, Any]]:
    """The Track 0 authority, matrix and late rows, each fact stated by the helper."""
    module = cast(Any, track)
    pr = module.pr
    age, blind, spouse_age, spouse_blind = pr.AGE, pr.BLIND, pr.S_AGE, pr.S_BLIND
    condition, status_fact = pr.COND, pr.STATUS
    joint, separate, household, surviving = pr.MFJ, pr.MFS, pr.HOH, pr.QSS
    no = False
    rows: list[dict[str, Any]] = []

    def add(
        case_id: str,
        status: str,
        answers: dict[str, Any],
        *,
        dependent: bool = False,
        acts: list[dict[str, Any]] | None = None,
    ) -> list[dict[str, Any]]:
        source = acts if acts is not None else cast(
            list[dict[str, Any]], module.build(status, answers, dependent=dependent)
        )
        stated = cast(list[dict[str, Any]], state_taxpayer_facts(source, core="v88"))
        filled = dict(answers)
        filled.setdefault(age, False)
        filled.setdefault(blind, False)
        boxes = cast(dict[str, str], module.expected_boxes(status, filled, dependent=dependent))
        hand = module.hand_12e(status, boxes, dependent=dependent)
        values = _fact_values(stated)
        held = [age, blind]
        held.extend(fact for fact in (spouse_age, spouse_blind) if fact in answers)
        mismatches = [fact for fact in held if values.get(fact) != filled[fact]]
        rows.append({
            "id": case_id,
            "acts": copy.deepcopy(stated),
            "boxes": boxes,
            "hand": hand,
            "mismatches": mismatches,
            "you_held": boxes["you_age"] in {"checked", "not_checked"} and boxes["you_blind"] in {"checked", "not_checked"},
            "spouse_blocked": boxes["spouse_age"] == "blocked" or boxes["spouse_blind"] == "blocked",
        })
        return stated

    add("auth_you_age_yes", "single", {age: True, blind: no})
    add("auth_you_blind_yes", "single", {age: no, blind: True})
    add("auth_spouse_age_joint", joint, {age: no, blind: no, spouse_age: True, spouse_blind: no})
    add("auth_spouse_blind_joint", joint, {age: no, blind: no, spouse_age: no, spouse_blind: True})
    add("auth_spouse_separate_yes", separate, {age: no, blind: no, spouse_age: no, spouse_blind: True, condition: True})
    add("auth_spouse_separate_no", separate, {age: no, blind: no, spouse_age: no, spouse_blind: True, condition: no})
    add("auth_spouse_recorded_on_hoh", household, {age: no, blind: no, spouse_age: True, spouse_blind: True})
    add("auth_spouse_recorded_on_qss", surviving, {age: no, blind: no, spouse_age: True, spouse_blind: True})

    variants = (
        ("single", "single", None, False),
        ("joint", joint, None, False),
        ("separate_yes", separate, True, False),
        ("separate_no", separate, False, False),
        ("hoh", household, None, False),
        ("qss", surviving, None, False),
        ("dependent", "single", None, True),
    )
    for name, status, cond, dependent in variants:
        spouse_asked = status in (joint, separate) and not dependent
        for answer in ("true", "false", "unanswered"):
            # N1: without a spouse question, "unanswered" is the false-answer run.
            if answer == "unanswered" and not spouse_asked:
                continue
            answers: dict[str, Any] = {}
            if answer != "unanswered":
                value = answer == "true"
                answers = {age: value, blind: value}
                if spouse_asked:
                    answers.update({spouse_age: value, spouse_blind: value})
            if cond is not None:
                answers[condition] = cond
            add(f"m_{name}_{answer}", status, answers, dependent=dependent)

    harness = pr.harness()
    both = {age: no, blind: no, spouse_age: True, spouse_blind: no}
    acts = add("late_joint_to_separate_0", joint, both, acts=cast(list[dict[str, Any]], module.build(joint, both)))
    acts = cast(list[dict[str, Any]], harness.say(acts, status_fact, separate, "fs"))
    add("late_joint_to_separate_1", separate, both, acts=acts)
    acts = cast(list[dict[str, Any]], pr.answer(acts, {condition: True}))
    add("late_joint_to_separate_2", separate, {**both, condition: True}, acts=acts)
    acts = cast(list[dict[str, Any]], pr.answer(acts, {condition: no}))
    add("late_joint_to_separate_3", separate, {**both, condition: no}, acts=acts)

    acts = add("late_joint_to_hoh_0", joint, both, acts=cast(list[dict[str, Any]], module.build(joint, both)))
    acts = cast(list[dict[str, Any]], harness.say(acts, status_fact, household, "fs"))
    add("late_joint_to_hoh_1", household, both, acts=acts)

    single = {age: True, blind: no}
    acts = add("late_answer_replaced_0", "single", single, acts=cast(list[dict[str, Any]], module.build("single", single)))
    acts = cast(list[dict[str, Any]], pr.answer(acts, {age: no}))
    add("late_answer_replaced_1", "single", {age: no, blind: no}, acts=acts)
    acts = cast(list[dict[str, Any]], pr.answer(acts, {blind: True}))
    add("late_answer_replaced_2", "single", {age: no, blind: True}, acts=acts)
    return rows


def _section(dom: str, label: str) -> str:
    """Raw markup from one heading through the next. A citation names the other box."""
    drawn = label + " (Line "
    for chunk in re.split(r"(?=<h2\b)", dom):
        heading = re.search(r"<h2[^>]*>(.*?)</h2>", chunk, flags=re.S)
        if heading is None:
            continue
        plain = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", heading.group(1)))).strip()
        if plain.startswith(drawn) or (plain == label and 'role="alert"' in chunk):
            return chunk
    raise AssertionError("no rendered section for " + label)


def _dump(page: Path, profile: Path) -> str:
    if not BROWSER:
        raise AssertionError("headless Chrome is required to read the drawn page")
    with browser_startup_slot():
        done = subprocess.run(
            [
                BROWSER,
                "--headless",
                "--disable-gpu",
                "--no-sandbox",
                f"--user-data-dir={profile}",
                "--virtual-time-budget=5000",
                "--dump-dom",
                page.as_uri(),
            ],
            capture_output=True,
            text=True,
            timeout=60,
            check=False,
        )
    if done.returncode != 0:
        raise AssertionError(done.stderr[-400:])
    if "<section" not in done.stdout:
        raise AssertionError("the page did not draw a section")
    return done.stdout


def _numbers(pin: dict[str, Any]) -> dict[str, Any]:
    """Line numbers, base and attachments. Row checks name dependencies and are not numbers."""
    if "lines" not in pin:
        return {"error": pin.get("error")}
    lines = cast(dict[str, Any], pin.get("lines") or {})
    kept = {
        name: value
        for name, value in lines.items()
        if not any(token in name for token in LINE12D)
    }
    return {"lines": kept, "base": pin.get("base"), "attachments": pin.get("attachments"), "error": pin.get("error")}


def _number_diffs(fixture: dict[str, Any], pin: dict[str, Any]) -> list[str]:
    left, right = _numbers(fixture), _numbers(pin)
    if left == right:
        return []
    diffs: list[str] = []
    if left.get("error") != right.get("error"):
        diffs.append("error")
    for key in ("base", "attachments"):
        if left.get(key) != right.get(key):
            diffs.append(key)
    left_lines = cast(dict[str, Any], left.get("lines") or {})
    right_lines = cast(dict[str, Any], right.get("lines") or {})
    for name in sorted(set(left_lines) | set(right_lines)):
        if left_lines.get(name) != right_lines.get(name):
            diffs.append(name)
    return diffs[:8]


def _v83_shard(work: list[tuple[str, list[dict[str, Any]]]]) -> dict[str, Any]:
    expected = cast(dict[str, Any], json.loads(FIXTURE.read_text(encoding="utf-8")))
    core = ReplayCore("v90", "v88", "v88")
    diffs: list[dict[str, Any]] = []
    for key, acts in work:
        _group, _slash, rest = key.partition("/")
        prepared = cast(list[dict[str, Any]], state_taxpayer_facts(acts, core="v88"))
        slug = re.sub(r"[^A-Za-z0-9_.-]", ".", key)
        pin = pin_run(core, prepared, "demo.l12d.t1.v90." + slug)
        bad = _number_diffs(recorded_pin_from_expected(expected, rest), pin)
        if bad:
            diffs.append({"id": key, "fields": bad})
    return {"runs": len(work), "diffs": diffs}


@pytest.fixture(scope="module")
def track() -> ModuleType:
    return _track()


def test_instructions_quote_the_chart(track: ModuleType) -> None:
    """Chart and worksheet amounts are the quoted 2025 instructions, not a run."""
    module = cast(Any, track)
    quotes = _quotes()
    chart = quotes["chart"]
    worksheet = quotes["dependents-worksheet"]
    assert "You can check the boxes for spouse if your filing status is married filing separately" in chart
    spouse_hidden = {module.pr.MFJ, module.pr.MFS}
    for status, amounts in cast(dict[str, tuple[int, ...]], module.CHART).items():
        for count, amount in enumerate(amounts):
            boxes = _boxes_for(count, spouse_hidden=status not in spouse_hidden)
            assert module.hand_12e(status, boxes) == amount
            quote = chart if count else worksheet
            assert _dollars(amount) in quote
    hidden = _boxes_for(0, spouse_hidden=True)
    assert module.hand_12e("single", hidden, dependent=True) == 15750
    assert module.hand_12e("single", _boxes_for(2, spouse_hidden=True), dependent=True) == 19750
    assert "$1,350" in worksheet and "$450" in worksheet and "$2,000" in worksheet and "$1,600" in worksheet
    single = module.expected_boxes("single", {module.pr.AGE: True, module.pr.BLIND: False})
    assert single == {
        "you_age": "checked",
        "you_blind": "not_checked",
        "spouse_age": "hidden",
        "spouse_blind": "hidden",
    }


def test_authority_matrix_and_late_on_published_v90(track: ModuleType) -> None:
    """Each distinct act list runs once, through the presentation model."""
    rows = _cases(track)
    assert len(rows) == 34
    groups: dict[str, dict[str, Any]] = {}
    order: list[str] = []
    for row in rows:
        assert row["mismatches"] == []
        assert row["you_held"] is True
        digest = _digest(cast(list[dict[str, Any]], row["acts"]))
        if digest not in groups:
            groups[digest] = {"acts": row["acts"], "rows": []}
            order.append(digest)
        cast(list[dict[str, Any]], groups[digest]["rows"]).append(row)

    core = _published(track)
    module = cast(Any, track)
    started = time.perf_counter()
    failures: list[str] = []
    for index, digest in enumerate(order, start=1):
        group = groups[digest]
        result = cast(dict[str, Any], module.run(core, group["acts"], f"demo.l12d.t1.v90.{digest[:12]}"))
        if "boxes" not in result:
            failures.append(f"{digest[:12]} did not read the presentation model")
            continue
        boxes = cast(dict[str, str], result["boxes"])
        for row in cast(list[dict[str, Any]], group["rows"]):
            bad: list[str] = []
            if result.get("outcome") != "success":
                bad.append(str(result.get("outcome")))
            if boxes != row["boxes"]:
                bad.append(f"boxes {boxes} != {row['boxes']}")
            if result.get("form1040.line-12e") != row["hand"]:
                bad.append(f"line 12e {result.get('form1040.line-12e')} != {row['hand']}")
            if row["spouse_blocked"] and (
                boxes.get("you_age") == "blocked" or boxes.get("you_blind") == "blocked"
            ):
                bad.append("a stated taxpayer box was blocked while a spouse question remained")
            if bad:
                failures.append(f"{row['id']}: {bad}")
        if index % 10 == 0 or index == len(order):
            print(f"L12D_T1_CASES {index}/{len(order)}", flush=True)
    wall = time.perf_counter() - started
    print(f"L12D_T1_CASES runs={len(order)} rows={len(rows)} wall_s={wall:.1f} failed={len(failures)}", flush=True)
    assert failures == []


def test_drawn_page_shows_each_box_text(track: ModuleType) -> None:
    """Checked, not-checked, hidden and blocked box text, and the line 6c alert."""
    module = cast(Any, track)
    pr = module.pr
    core = _published(track)
    filing = _explain("form1040.line-12d-spouse-age.form-field.json", "guard_inapplicable")
    you_age = _label("form1040.line-12d-you-age.form-field.json")
    you_blind_open = _label("form1040.line-12d-you-blind-not-checked.form-field.json")
    spouse_age = _label("form1040.line-12d-spouse-age.form-field.json")
    lump_sum = _label("form1040.line-6c.form-field.json")
    root = _new_owned_chrome_tempdir()
    started = time.perf_counter()
    try:
        page_out = root / "pages"
        single = cast(list[dict[str, Any]], state_taxpayer_facts(
            cast(list[dict[str, Any]], module.build("single", {pr.AGE: True, pr.BLIND: False})),
            core="v88",
        ))
        drawn = cast(dict[str, Any], module.run(
            core, single, "demo.l12d.t1.page.single", pages={"product": REPO}, page_out=page_out,
        ))
        assert drawn.get("outcome") == "success"
        separate_acts = cast(list[dict[str, Any]], state_taxpayer_facts(
            cast(list[dict[str, Any]], module.build(pr.MFS, {pr.AGE: False, pr.BLIND: False})),
            core="v88",
        ))
        blocked = cast(dict[str, Any], module.run(
            core, separate_acts, "demo.l12d.t1.page.separate", pages={"product": REPO}, page_out=page_out,
        ))
        assert blocked.get("outcome") == "success"
        single_dom = _dump(page_out / "demo.l12d.t1.page.single.product.html", root / "profile-single")
        separate_dom = _dump(page_out / "demo.l12d.t1.page.separate.product.html", root / "profile-separate")
    finally:
        shutil.rmtree(root, ignore_errors=True)
    wall = time.perf_counter() - started
    print(f"L12D_T1_PAGE runs=2 wall_s={wall:.1f}", flush=True)

    checked = _section(single_dom, you_age)
    assert f'aria-label="{you_age}: checked"' in checked
    assert ">checked</p>" in checked
    assert ALERT not in checked
    not_checked = _section(single_dom, you_blind_open)
    assert f'aria-label="{you_blind_open}: not checked"' in not_checked
    hidden = _section(single_dom, spouse_age)
    assert HIDDEN in hidden
    assert filing in hidden
    alert = _section(single_dom, lump_sum)
    assert 'role="alert"' in alert
    assert ALERT in alert
    blocked_text = _section(separate_dom, spouse_age)
    assert BLOCKED in blocked_text
    assert ALERT not in blocked_text


def _question(name: str) -> str:
    body = cast(dict[str, Any], json.loads((CONTENT / name).read_text(encoding="utf-8")))
    return str(body["question"])


def test_unanswered_taxpayer_age_and_blindness_block(track: ModuleType) -> None:
    """A single return that leaves age and blindness unstated blocks both You boxes.

    The case does not call the shared helper and does not default those facts.
    The drawn section shows the blocked copy and the question, not "not checked".
    """
    module = cast(Any, track)
    acts = cast(list[dict[str, Any]], module.build("single", {}))
    stated = _fact_values(acts)
    assert module.pr.AGE not in stated
    assert module.pr.BLIND not in stated
    core = _published(track)
    root = _new_owned_chrome_tempdir()
    try:
        page_out = root / "pages"
        result = cast(dict[str, Any], module.run(
            core, acts, "demo.l12d.repair.unanswered", pages={"product": REPO}, page_out=page_out,
        ))
        dom = _dump(page_out / "demo.l12d.repair.unanswered.product.html", root / "profile")
    finally:
        shutil.rmtree(root, ignore_errors=True)
    assert result.get("outcome") == "success"
    boxes = cast(dict[str, str], result["boxes"])
    assert boxes["you_age"] == "blocked"
    assert boxes["you_blind"] == "blocked"
    assert result.get("form1040.line-12e") == "blocked"
    age = _section(dom, _label("form1040.line-12d-you-age.form-field.json"))
    blind = _section(dom, _label("form1040.line-12d-you-blind.form-field.json"))
    age_question = _question("input-question.taxpayer-over-65.v1.json")
    blind_question = _question("input-question.taxpayer-blind.v1.json")
    for section, question in ((age, age_question), (blind, blind_question)):
        assert BLOCKED in section
        assert 'href="#question-group-' in section
        assert question in html.unescape(dom)
        assert ">not checked</p>" not in section
        assert ": not checked\"" not in section


def test_v83_recorded_lists_keep_their_numbers() -> None:
    """The 298 v83 lists on published v90. Line numbers match the fixture.

    A row check may name a dependency the fixture left blank. That list is
    not a number. Line 12d lines are new and are not in the fixture.
    """
    qw = cast(Any, evidence_loader.load(QW / "track0.py", "l12d_t1_qw_track0"))
    work = [
        item
        for item in cast(list[tuple[str, list[dict[str, Any]]]], qw.neighbour_tasks())
        if item[0].startswith("v83/")
    ]
    assert len(work) == 298
    workers = min(8, len(work))
    shards = [work[index::workers] for index in range(workers)]
    started = time.perf_counter()
    context = multiprocessing.get_context("spawn")
    diffs: list[dict[str, Any]] = []
    runs = 0
    with ProcessPoolExecutor(max_workers=workers, mp_context=context) as pool:
        for part in pool.map(_v83_shard, shards):
            runs += int(part["runs"])
            diffs.extend(cast(list[dict[str, Any]], part["diffs"]))
    wall = time.perf_counter() - started
    print(
        f"L12D_T1_V83 runs={runs} wall_s={wall:.1f} workers={workers} diffs={len(diffs)} of={len(work)}",
        flush=True,
    )
    for row in diffs[:12]:
        print(f"L12D_T1_V83_DIFF {row['id']} {row['fields']}", flush=True)
    assert runs == len(work)
    assert diffs == []
