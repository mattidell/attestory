"""Fast-lane size guards for the content rule files.

The credit and worksheet modules each checked a slice of these files, and
conftest marks those modules live, so the fast lane never ran the checks.
This module checks the same files, the same caps, and the same raised-cap
reasons. Its source names none of the live-lane tokens.
"""

from __future__ import annotations

from pathlib import Path

CONTENT = Path(__file__).resolve().parents[1] / "packages" / "content" / "tax" / "2025"

# file, cap, reason. The earned-income glob uses 5,000 bytes except these,
# each with the reason that was written beside the old checks.
EXCEPTIONS: tuple[tuple[str, int, str], ...] = (
    (
        "rule.eic-gate-result.v3.json",
        7000,
        "Core v99 writes the gate result v3 and the no-unsupported-situations "
        "answer v3 with indent=2; v2 of each was hand-compacted (the gate result "
        "v2 re-dumped the same way is 5,944 bytes). The growth is mostly formatting.",
    ),
    (
        "rule.eic-answer.no-unsupported-situations.v3.json",
        7000,
        "Core v99 writes the gate result v3 and the no-unsupported-situations "
        "answer v3 with indent=2; v2 of each was hand-compacted (the gate result "
        "v2 re-dumped the same way is 5,944 bytes). The growth is mostly formatting.",
    ),
    (
        "rule.eic-status-class.v3.json",
        7000,
        "Core v102 status class v3 adds the qualifying-child-present condition for "
        "head of household (eic-no-ssn-child); that is content, 2,730 to 3,263 bytes compacted.",
    ),
    (
        "rule.eic-early-stop.v3.json",
        7000,
        "Core v102 early stop v3 is written with indent=2 (v2 was hand-compacted; v2 "
        "re-dumped that way is 6,031 bytes) and adds the qualifying-child-present condition.",
    ),
)

DEFAULT_CAP = 5000
WORKSHEET_CAP = 6 * 1024
WORKSHEET_LINES = (4, 5, *range(6, 26))
WORKSHEET_NAMES = {
    f"rule.qdcg-worksheet.line-{number}.json" for number in WORKSHEET_LINES
}

# Named by the earned-income guard in addition to the rule.eic-*.json glob.
EARNED_INCOME_ALSO = (
    "rule.form1040-line27a.json",
    "rule.form1040-lines28-31.json",
    "rule.form1040-lines27-31-total.v2.json",
    "rule.form1040-line32.v2.json",
)


def _exception_caps() -> dict[str, int]:
    caps: dict[str, int] = {}
    for name, cap, _reason in EXCEPTIONS:
        caps[name] = cap
    return caps


def _add(caps: dict[str, int], name: str, cap: int) -> None:
    previous = caps.get(name)
    # A file that two guards both checked had to satisfy each cap.
    caps[name] = cap if previous is None else min(previous, cap)


def covered_caps() -> dict[str, int]:
    """Files and caps of the union of the previous guards."""
    exception_caps = _exception_caps()
    caps: dict[str, int] = {}
    for path in CONTENT.glob("rule.eic-*.json"):
        _add(caps, path.name, exception_caps.get(path.name, DEFAULT_CAP))
    for name in EARNED_INCOME_ALSO:
        _add(caps, name, DEFAULT_CAP)
    for path in CONTENT.glob("rule.ctc-*.json"):
        _add(caps, path.name, DEFAULT_CAP)
    for path in CONTENT.glob("rule.odc-*.json"):
        _add(caps, path.name, DEFAULT_CAP)
    for name in WORKSHEET_NAMES:
        _add(caps, name, WORKSHEET_CAP)
    return caps


def test_content_rule_files_stay_within_their_caps() -> None:
    worksheet = {path.name for path in CONTENT.glob("rule.qdcg-worksheet.*.json")}
    assert worksheet == WORKSHEET_NAMES
    for name, cap in sorted(covered_caps().items()):
        size = (CONTENT / name).stat().st_size
        assert size <= cap, name
