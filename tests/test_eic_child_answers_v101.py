"""A counted member's missing answer is asked, named by that member, on published core v101 (ADR 0087).

Track 1's probe returns (``track1_probe.py``) go through live_coordinate_run,
the real presentation projection and the saved page, on published v100
(registry v98, release v98) and published v101 (registry v99, release v99).
The returns are the P0 returns: one or two children on the earned income,
child tax credit and tie-breaker rosters (and one child whose other parent
could also claim it, so every tie-breaker answer is read), one or two
17-year-olds on the other-dependent child roster, one or two dependent parents
on the relative roster. Each member's entity carries its own recorded label. Where a test is
about an answer, the return leaves that answer out of one member's record:
nothing is pre-filled for it.

Measured reason for the live marker: each live_coordinate_run with page
rendering takes about 5 s, above the fast-lane budget.
"""
from __future__ import annotations

import html
import json
import re
import shutil
import subprocess
import tempfile
from functools import lru_cache
from pathlib import Path
from typing import Any

import pytest

from tests import evidence_loader
from tests.helpers.chrome_startup_slot import browser_startup_slot

pytestmark = pytest.mark.live
REPO = Path(__file__).resolve().parents[1]
EVIDENCE = REPO / "docs/phases/engine-breadth/milestones/eic-child-answers-evidence"
CONTENT = REPO / "packages/content/tax/2025"
P = "tax.us.2025."


@lru_cache(maxsize=1)
def _probe() -> Any:
    return evidence_loader.load(EVIDENCE / "track1_probe.py", "eicc_t1_live_probe")


@lru_cache(maxsize=None)
def _run(case: str, core: str) -> dict[str, Any]:
    probe = _probe()
    n = int(core[1:])
    published = probe.h.Core(core, f"v{n - 2}", f"v{n - 2}")
    assert published.package_path.name == f"package.core-calculations.{core}.json"
    return dict(probe.observe(published, case))


@lru_cache(maxsize=None)
def _question(fact: str) -> str:
    name = "input-question." + fact.removeprefix(P).replace(".", "-") + ".v1.json"
    body = json.loads((CONTENT / name).read_text(encoding="utf-8"))
    assert body["fact_type"]["id"] == fact
    return str(body["question"])


def _expected(case: str) -> list[list[str]]:
    """[member label, question] for each answer the case leaves out, sorted as the page sorts them."""
    probe = _probe()
    out = []
    for part in case.rsplit("/", 1)[1].split("+"):
        short, where = part.split("@")
        out.append([probe.label(probe.member_name(where)), _question(probe.ANSWERS[short][0])])
    return sorted(out)


MISSING = tuple(c for c in (
    *(f"single/kid1/30000/{a}@1" for a in ("age", "res", "joint", "ssn", "dtb-another", "dtb-filer-parent",
                                           "u17", "lived", "support", "citizen")),
    *(f"single/kid2/30000/{a}@2" for a in ("age", "res", "joint", "ssn", "dtb-another", "dtb-filer-parent",
                                           "u17", "lived", "support", "citizen")),
    "single/kid2/30000/age@1",
    # The other eight tie-breaker answers, each read on the path the earlier answers open.
    "single/kid1/30000/dtb-multiple@1", "single/kid1/30000/dtb-other-parent@1",
    *(f"single/kid1pp/30000/{a}@1" for a in ("dtb-8332", "dtb-nights", "dtb-same-nights", "dtb-agi",
                                              "dtb-will-claim", "dtb-same-agi")),
    "single/odckid/30000/odc-tin@1", "single/odckid/30000/ssn@1", "single/odckid2/30000/odc-tin@2",
    "single/odckid2/30000/lived@2",
    *(f"single/parent/30000/{a}@p1" for a in ("rel-relationship", "rel-notqc", "rel-gross", "rel-support",
                                              "rel-tin", "rel-citizen", "rel-notjoint")),
    *(f"single/parent2/30000/{a}@p2" for a in ("rel-relationship", "rel-tin", "rel-notjoint")),
    "mfj/kid1/30000/age@1",
))
TWO_MISSING = ("single/kid2/30000/age@1+age@2", "single/kid2/30000/age@1+res@2",
               "single/parent2/30000/rel-tin@p1+rel-citizen@p2")
ANSWERED = ("single/kid1/30000/-", "single/kid2/30000/-", "single/kid1pp/30000/-", "single/odckid/30000/-",
            "single/odckid2/30000/-", "single/parent/30000/-", "single/parent2/30000/-")
# One case per roster, also run on v100: v101 blocks the same rules and lines, which v100 left silent.
ON_V100 = ("single/kid2/30000/age@2", "single/kid1/30000/u17@1", "single/odckid2/30000/odc-tin@2",
           "single/parent2/30000/rel-tin@p2")


def _asks_on_every_blocked_line(run: dict[str, Any], case: str) -> None:
    assert run["stop"] == "saturated"
    assert run["blocked_page_lines_without_sentence"] == []
    assert run["reasons"], case
    want = _expected(case)
    for line, reasons in run["reasons"].items():
        assert reasons == want, line
    for line, row in run["lines"].items():
        if line in run["reasons"]:
            assert row == {"disposition": "blocked", "value": None}, line


@pytest.mark.parametrize("case", MISSING)
def test_a_members_missing_answer_is_asked_with_that_members_label(case: str) -> None:
    run = _run(case, "v101")
    _asks_on_every_blocked_line(run, case)
    # The credit lines the answer decides still block.
    roster = case.split("/")[1]
    blocked = {line for line, row in run["lines"].items() if row["disposition"] == "blocked"}
    assert "form1040.line-34" in blocked and "form1040.line-35a" in blocked and "form1040.line-37" in blocked
    if roster.startswith("kid") and case.split("/")[3].split("@")[0] in ("age", "res", "joint", "ssn") \
            or case.split("/")[3].startswith("dtb-"):
        assert "form1040.line-27a" in blocked
    if roster.startswith(("odckid", "parent")):
        assert "form1040.line-19" in blocked


@pytest.mark.parametrize("case", TWO_MISSING)
def test_two_members_each_missing_an_answer_are_both_asked_by_name(case: str) -> None:
    run = _run(case, "v101")
    _asks_on_every_blocked_line(run, case)
    assert len({label for reasons in run["reasons"].values() for label, _ in reasons}) == 2


@pytest.mark.parametrize("case", ON_V100)
def test_v101_blocks_what_v100_blocked_and_asks_where_v100_was_silent(case: str) -> None:
    before = _run(case, "v100")
    after = _run(case, "v101")
    assert after["blocked_rules"] == before["blocked_rules"]
    assert after["lines"] == before["lines"] and after["symbols"] == before["symbols"]
    assert before["reasons"] == {}
    assert sorted(after["reasons"]) == before["blocked_page_lines_without_sentence"]


@pytest.mark.parametrize("case", ANSWERED)
def test_a_return_with_every_answer_given_computes_exactly_as_v100(case: str) -> None:
    before = _run(case, "v100")
    after = _run(case, "v101")
    assert after["stop"] == before["stop"] == "saturated"
    assert after["blocked_rules"] == before["blocked_rules"] == []
    assert after["lines"] == before["lines"]
    assert after["symbols"] == before["symbols"]
    assert after["reasons"] == before["reasons"] == {}
    assert all(row["disposition"] != "blocked" for row in after["lines"].values())


def _browser() -> str | None:
    candidates = [
        *sorted(Path.home().glob("Library/Caches/ms-playwright/chromium_headless_shell-*/"
                                 "chrome-headless-shell-*/chrome-headless-shell"), reverse=True),
        *sorted(Path.home().glob(".cache/ms-playwright/chromium_headless_shell-*/"
                                 "chrome-headless-shell-*/chrome-headless-shell"), reverse=True),
        Path("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"),
        Path("/Applications/Chromium.app/Contents/MacOS/Chromium"),
    ]
    found = next((str(path) for path in candidates if path.is_file()), None)
    return found or shutil.which("google-chrome") or shutil.which("chromium") or shutil.which("chromium-browser")


@pytest.mark.skipif(_browser() is None, reason="no headless Chromium available")
def test_the_saved_page_shows_each_members_label_beside_its_question() -> None:
    case = "single/kid2/30000/age@1+res@2"
    probe = _probe()
    with tempfile.TemporaryDirectory(prefix="demo-eicc-page-") as work:
        page = Path(work) / "page.html"
        probe.observe(probe.h.Core("v101", "v99", "v99"), case, page_out=page)
        with browser_startup_slot():
            done = subprocess.run(
                [str(_browser()), "--headless", "--disable-gpu", "--no-sandbox", f"--user-data-dir={work}/profile",
                 "--virtual-time-budget=5000", "--dump-dom", page.as_uri()],
                capture_output=True, text=True, timeout=60, check=True)
    text = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", done.stdout)))
    for label, question in _expected(case):
        shown = f"{label}: {question}"
        # Every blocked line of the earned income credit (9) says it.
        assert text.count(re.sub(r"\s+", " ", shown)) == 9, label
