"""Published core v92 draws line 6c and cites the Schedule 1 top entry.

Measured reason: five distinct act lists and the SSA-1099 guard each call
the live coordinate run, and three saved pages are drawn in headless Chrome.
The first run of this module took 45 seconds, and one Chrome draw took 21
seconds. Both are outside the 3 second fast-lane budget, so the two added
draws stay in this module.

Line 12e comes from the 2025 instructions through the line 12d hand value.
Line 1a is the recorded Form W-2 box 1 total, which the line 1a field states
is the instruction's amount. Line 6a, when a benefit statement is closed, is
that statement's box 5, which the line 6a field states is the instruction's
amount. Those amounts are held when the lump-sum question is still open and
when the top entry is blocked. The unanswered election leaves its fact out
of the act list.
"""

from __future__ import annotations

import hashlib
import html
import json
import re
import shutil
import subprocess
import tempfile
import time
from pathlib import Path
from types import ModuleType
from typing import Any, cast

import pytest

from tests import evidence_loader
from tests.helpers.chrome_startup_slot import browser_startup_slot
from tests.test_sli_line21_page_reasons import BROWSER
from tools.sale_page_observation import _new_owned_chrome_tempdir


pytestmark = pytest.mark.live

REPO = Path(__file__).resolve().parents[1]
EVIDENCE = REPO / "docs/phases/engine-breadth/milestones/page-alerts-evidence"
L12D = REPO / "docs/phases/engine-breadth/milestones/line12d-boxes-evidence"
CONTENT = REPO / "packages/content/tax/2025"
P = "tax.us.2025."
LUMP = P + "ss-benefits-scope.no-lump-sum-election"
SSA_CLOSURE = P + "ssa1099.source-closure"
K_CLOSURE = P + "f1099k.source-closure"
LINE_6C = "form1040.line-6c"
LINE_6C_CHECKED = "form1040.line-6c-checked"
TOP = "schedule1.top-entry.form-field"
LINE_6A = "form1040.line-6a"
LINE_1A = "form1040.line-1a"
LINE_12E = "form1040.line-12e"
INAPPLICABLE = (
    "This line 6c box does not apply to this return, or the box is the "
    "other checked/not-checked state."
)
ZERO = (
    "No gross payment amount in box 1a of a Form 1099-K for personal items "
    "you sold was recorded for 2025."
)
LOSS = (
    "This sale resulted in a nondeductible personal loss whose "
    "Box 1a gross amount is entered at the top of Schedule 1."
)
ALERT_CAUSES = ("missing-instruction", "missing-field-citation")
SAFE_RENDER = (
    "This line is missing its rendering instruction for the declared disposition.",
    "This line published a value with no citation attached. No value can be shown safely.",
    "This section failed to render safely.",
)
CLOSURE_QUESTION = (
    "Have you recorded every Form SSA-1099 you or your spouse received for 2025 "
    "(not counting a lump-sum election, and not a Form RRB-1099), with its box 3, "
    "box 4 and box 5 amounts?"
)
OLD_HORIZON = "demo.ssa.h0"


def _line12d_names() -> None:
    # The line 12d harness is imported by bare name. Bind those names to this
    # owner's copies by path, so another evidence directory earlier on
    # sys.path cannot supply a different ``probe``.
    evidence_loader.load(L12D / "prototype.py", "prototype")
    evidence_loader.load(L12D / "probe.py", "probe")


def _probe() -> ModuleType:
    _line12d_names()
    return evidence_loader.load(EVIDENCE / "probe.py", "pa_t1_v92_probe")


def _census() -> ModuleType:
    _line12d_names()
    return evidence_loader.load(EVIDENCE / "census.py", "pa_t1_v92_census")


def _boxes() -> ModuleType:
    _line12d_names()
    return evidence_loader.load(L12D / "track0.py", "pa_t1_v92_line12d")


def _core(probe: ModuleType) -> Any:
    return cast(Any, probe).l12d.harness().Core("v92", "v90", "v90")


def _facts(acts: list[dict[str, Any]], fact: str) -> list[dict[str, Any]]:
    found = []
    for act in acts:
        finding = (act.get("payload") or {}).get("finding")
        if isinstance(finding, dict) and str(finding.get("fact_id") or "").startswith(fact + "|"):
            found.append(finding)
    return found


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


def _unanswered(probe: ModuleType, wage: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Benefits recorded, election fact removed. Nothing after this answers it."""
    module = cast(Any, probe)
    recorded = cast(list[dict[str, Any]], module.with_benefits(wage, 12000.0, election="yes"))
    harness = module.l12d.harness()
    return cast(list[dict[str, Any]], harness.renumber(harness.strip(recorded, LUMP)))


def _blocked_top(probe: ModuleType, wage: list[dict[str, Any]]) -> list[dict[str, Any]]:
    module = cast(Any, probe)
    harness = module.l12d.harness()
    return cast(list[dict[str, Any]], harness.renumber(harness.strip(wage, K_CLOSURE)))


def _run(
    probe: ModuleType,
    core: Any,
    acts: list[dict[str, Any]],
    run_id: str,
    page_dir: Path,
    *,
    reconfirm: bool,
) -> dict[str, Any]:
    module = cast(Any, probe)
    harness = module.l12d.harness()
    surface = core.surface()
    with harness.loader_entries(core):
        finished = harness._handover(
            harness._finish(
                acts,
                package_path=core.package_path,
                package_version=core.version,
                release_path=core.release_path,
                release_version=core.release_version,
                note=run_id,
            ),
            surface=surface,
            reconfirm=reconfirm,
        )
        with tempfile.TemporaryDirectory() as tmp:
            capability = harness.WorkspaceCapability(Path(tmp) / "L")
            outcome = harness.live_coordinate_run(
                capability,
                repo_root=REPO,
                authoritative_acts=finished,
                workspace_revision=len(finished),
                run_scope={"jurisdiction": "us", "year": harness.YEAR},
                scope_user=harness.ccr.USER,
                request={"schema": "run-request.v1"},
                run_id=run_id,
                governance_pins=[],
                surface=surface,
                output_name="out.json",
            )
            if outcome.refusal is not None:
                return {"outcome": "refused", "reason": outcome.refusal.reason}
            model = json.loads(outcome.presentation_path.read_text(encoding="utf-8"))
            report = json.loads(outcome.output_path.read_text(encoding="utf-8"))
            page = module._render_page(REPO, capability, outcome.presentation_path)
    page_dir.mkdir(parents=True, exist_ok=True)
    path = page_dir / f"{run_id}.html"
    path.write_bytes(page)
    return {
        "outcome": "success",
        "stop": report.get("stop_reason"),
        "model": model,
        "page": path,
    }


def _saved_model(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    marker = "const MODEL = Object.freeze("
    model, _end = json.JSONDecoder().raw_decode(text, text.index(marker) + len(marker))
    return cast(dict[str, Any], model)


def _field(probe: ModuleType, model: dict[str, Any], field_id: str) -> tuple[dict[str, Any], dict[str, Any]]:
    for section in cast(list[dict[str, Any]], model.get("sections") or []):
        view = cast(dict[str, Any], cast(Any, probe).section_view(section))
        if view["field_id"] == field_id:
            return view, section
    raise AssertionError("missing " + field_id)


def _alert_causes(census: ModuleType, model: dict[str, Any]) -> list[dict[str, str]]:
    found = []
    for section in cast(list[dict[str, Any]], model.get("sections") or []):
        alert = cast(Any, census).section_alert(section)
        if isinstance(alert, dict) and alert.get("code") in ALERT_CAUSES:
            found.append(alert)
    return found


def _hand(boxes: ModuleType) -> int:
    hidden = {
        "you_age": "not_checked",
        "you_blind": "not_checked",
        "spouse_age": "hidden",
        "spouse_blind": "hidden",
    }
    amount = cast(Any, boxes).hand_12e("single", hidden)
    assert amount == 15750
    return int(amount)


def _holds(probe: ModuleType, model: dict[str, Any], *, line_6a: int, line_12e: int) -> None:
    wages, _section = _field(probe, model, LINE_1A)
    benefits, _section = _field(probe, model, LINE_6A)
    deduction, _section = _field(probe, model, LINE_12E)
    assert wages["disposition"] == "published_value"
    assert wages["value"] == 50000
    assert "box 1" in str(wages["explain"])
    if line_6a == 0:
        assert benefits["disposition"] == "computed_zero"
        assert benefits["value"] == 0
    else:
        assert benefits["disposition"] == "published_value"
        assert benefits["value"] == line_6a
        assert "box 5" in str(benefits["explain"])
    assert deduction["disposition"] == "published_value"
    assert deduction["value"] == line_12e


def _expect(view: dict[str, Any], **wanted: Any) -> None:
    for key, value in wanted.items():
        assert view.get(key) == value, (view.get("field_id"), key, view.get(key), value)


def _section(dom: str, label: str) -> str:
    drawn = label + " (Line "
    for chunk in re.split(r"(?=<h2\b)", dom):
        heading = re.search(r"<h2[^>]*>(.*?)</h2>", chunk, flags=re.S)
        if heading is None:
            continue
        plain = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", heading.group(1)))).strip()
        if plain.startswith(drawn):
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


def test_line_6c_and_the_top_entry_on_published_v92() -> None:
    """Each distinct act list once, through the projection and the saved page.

    The wage return draws the zero sentence. Published Form 1099-K content
    is the personal-item family in closure-mapping.f1099k.v3.json. A recorded
    member leaves the closed-empty path, so published content does not reach
    a return that has a Form 1099-K for something else and still draws this
    sentence.
    """
    probe = _probe()
    census = _census()
    line_12e = _hand(_boxes())
    module = cast(Any, probe)
    wage = cast(list[dict[str, Any]], module.wage())
    assert len(_facts(wage, LUMP)) == 1
    assert _facts(wage, LUMP)[0]["value"] == "yes"
    made = cast(list[dict[str, Any]], module.with_benefits(wage, 12000.0, election="no"))
    unanswered = _unanswered(probe, wage)
    assert _facts(unanswered, LUMP) == []
    loss = cast(list[dict[str, Any]], module.with_1099k(wage))
    blocked = _blocked_top(probe, wage)
    lists = {
        "not-made-and-top-zero": wage,
        "election-made": made,
        "election-unanswered": unanswered,
        "personal-item-loss": loss,
        "top-blocked": blocked,
    }
    assert len({_digest(acts) for acts in lists.values()}) == len(lists)

    core = _core(probe)
    root = _new_owned_chrome_tempdir()
    page_dir = root / "pages"
    failures: list[str] = []
    started = time.perf_counter()
    try:
        for name, acts in lists.items():
            result = _run(probe, core, acts, f"demo.pa.t1.v92.{name}", page_dir, reconfirm=True)
            if result.get("outcome") != "success" or result.get("stop") != "saturated":
                failures.append(f"{name} {result.get('outcome')} {result.get('stop') or result.get('reason')}")
                continue
            model = cast(dict[str, Any], result["model"])
            embedded = _saved_model(cast(Path, result["page"]))
            if embedded.get("sections") != model.get("sections"):
                failures.append(f"{name} saved page model differs from the projection")
            causes = _alert_causes(census, model)
            if causes:
                failures.append(f"{name} alert causes {causes}")
            try:
                line_6a = 12000 if name in {"election-made", "election-unanswered"} else 0
                _holds(probe, model, line_6a=line_6a, line_12e=line_12e)
                open_box, open_section = _field(probe, model, LINE_6C)
                checked_box, checked_section = _field(probe, model, LINE_6C_CHECKED)
                top, top_section = _field(probe, model, TOP)
                assert cast(Any, census).section_alert(open_section) is None
                assert cast(Any, census).section_alert(checked_section) is None
                assert cast(Any, census).section_alert(top_section) is None
                if name == "not-made-and-top-zero":
                    _expect(
                        open_box,
                        disposition="published_categorical",
                        render="not_checked",
                        explain="The lump-sum election checkbox is not checked.",
                        citation_id="citation.form1040.line-6c",
                    )
                    _expect(
                        checked_box,
                        disposition="guard_inapplicable",
                        render="",
                        explain=INAPPLICABLE,
                        citation_id="citation.form1040.line-6c",
                    )
                    _expect(
                        top,
                        disposition="closure_backed_zero",
                        value=0,
                        render="{value}",
                        explain=ZERO,
                        citation_id="citation.schedule1.top-entry",
                    )
                elif name == "election-made":
                    _expect(
                        open_box,
                        disposition="guard_inapplicable",
                        render="",
                        explain=INAPPLICABLE,
                        citation_id="citation.form1040.line-6c",
                    )
                    _expect(
                        checked_box,
                        disposition="published_categorical",
                        render="checked",
                        explain="The lump-sum election checkbox is checked.",
                        citation_id="citation.form1040.line-6c",
                    )
                elif name == "election-unanswered":
                    _expect(
                        open_box,
                        disposition="blocked",
                        explain="line 6c is blocked because a worksheet or source dependency is incomplete",
                        citation_id="citation.form1040.line-6c",
                    )
                    _expect(
                        checked_box,
                        disposition="blocked",
                        explain="The checked lump-sum election disposition is blocked because the election answer is missing.",
                        citation_id="citation.form1040.line-6c",
                    )
                    assert "DEPENDENCY_ABSENT" in open_box["active_codes"]
                    assert "DEPENDENCY_ABSENT" in checked_box["active_codes"]
                elif name == "personal-item-loss":
                    _expect(
                        top,
                        disposition="published_value",
                        value=880,
                        render="{value}",
                        explain=LOSS,
                        citation_id="citation.schedule1.top-entry",
                    )
                elif name == "top-blocked":
                    _expect(
                        top,
                        disposition="blocked",
                        explain="Form 1099-K loss entry cannot be computed.",
                        citation_id="citation.schedule1.top-entry",
                    )
            except AssertionError as exc:
                failures.append(f"{name} {exc}")
    finally:
        wall = time.perf_counter() - started
        print(
            f"PA_T1_CASES runs={len(lists)} wall_s={wall:.1f} failed={len(failures)}",
            flush=True,
        )
        shutil.rmtree(root, ignore_errors=True)
    assert failures == []


def test_drawn_page_shows_not_checked_without_a_safe_render_alert() -> None:
    """Chrome draws the wage, election-made, and personal-item-loss pages."""
    probe = _probe()
    module = cast(Any, probe)
    wage = cast(list[dict[str, Any]], module.wage())
    made = cast(list[dict[str, Any]], module.with_benefits(wage, 12000.0, election="no"))
    loss = cast(list[dict[str, Any]], module.with_1099k(wage))
    fields = CONTENT
    not_checked = str(json.loads((fields / "form1040.line-6c.form-field.v2.json").read_text(encoding="utf-8"))["label"])
    checked = str(json.loads((fields / "form1040.line-6c-checked.form-field.json").read_text(encoding="utf-8"))["label"])
    top = str(json.loads((fields / "schedule1.top-entry.form-field.v2.json").read_text(encoding="utf-8"))["label"])
    core = _core(probe)
    root = _new_owned_chrome_tempdir()
    drawn: dict[str, str] = {}
    started = time.perf_counter()
    try:
        for name, acts in (
            ("wage", wage),
            ("election-made", made),
            ("personal-item-loss", loss),
        ):
            result = _run(probe, core, acts, f"demo.pa.t1.v92.page.{name}", root / "pages", reconfirm=True)
            assert result.get("outcome") == "success", name
            drawn[name] = _dump(cast(Path, result["page"]), root / "profile")
    finally:
        wall = time.perf_counter() - started
        print(f"PA_T1_PAGE runs=3 wall_s={wall:.1f}", flush=True)
        shutil.rmtree(root, ignore_errors=True)
    for name, dom in drawn.items():
        # The page script names the alert class. A drawn alert is an element.
        assert 'class="section-error"' not in dom, name
    section = _section(drawn["wage"], not_checked)
    assert f'aria-label="{not_checked}: not checked"' in section
    assert ">not checked</p>" in section
    assert "The lump-sum election checkbox is not checked." in section
    for sentence in SAFE_RENDER:
        assert sentence not in section
    made_section = _section(drawn["election-made"], checked)
    assert "checked" in made_section
    assert ">checked</p>" in made_section
    assert "The lump-sum election checkbox is checked." in made_section
    loss_section = _section(drawn["personal-item-loss"], top)
    assert LOSS in loss_section


def test_closure_left_on_the_old_horizon_blocks_line_6a() -> None:
    """The follow-up's stale SSA-1099 list, with reconfirm left off."""
    probe = _probe()
    module = cast(Any, probe)
    wage = cast(list[dict[str, Any]], module.wage())
    acts = cast(list[dict[str, Any]], module.with_benefits(wage, 12000.0, election="yes", reclose=False))
    closures = _facts(acts, SSA_CLOSURE)
    assert len(closures) == 1
    assert OLD_HORIZON in str(closures[0]["fact_id"])
    assert "handover" not in str(closures[0]["fact_id"])
    for act in acts:
        finding = (act.get("payload") or {}).get("finding") or {}
        assert "reconfirm" not in str(finding.get("fact_id") or "")
    core = _core(probe)
    root = _new_owned_chrome_tempdir()
    try:
        result = _run(
            probe,
            core,
            acts,
            "demo.pa.t1.v92.ssa-old-horizon",
            root / "pages",
            reconfirm=False,
        )
        assert result.get("outcome") == "success"
        page_text = cast(Path, result["page"]).read_text(encoding="utf-8")
    finally:
        shutil.rmtree(root, ignore_errors=True)
    model = cast(dict[str, Any], result["model"])
    line, _section = _field(probe, model, LINE_6A)
    assert line["disposition"] == "blocked"
    assert "SOURCE_SET_UNCLOSED" in line["active_codes"]
    assert CLOSURE_QUESTION in line["reasons"]
    assert CLOSURE_QUESTION in page_text
