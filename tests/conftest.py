"""Test lane routing: separate the live-coordinator integration tests.

The suite has two populations with very different costs. Most modules exercise
the kernel, derivation, and content units directly. A minority drive the whole
coordinator (`live_coordinate_run`) or regenerate committed goldens; those are
integration tests, and they dominate the runtime.

This file routes them into a `live` marker so a development loop can run
`-m "not live"` while the full suite stays the merge gate. Two rules keep the
routing honest:

* The marker is **derived**, never hand-applied. A module that references the
  live coordinator is marked automatically, so adding a module cannot silently
  land it in the fast lane.
* The fast lane **enforces its own premise**. Any unmarked test slower than
  `FAST_LANE_BUDGET_SECONDS` fails. Without this the fast lane quietly decays
  back into the slow one, which is exactly how the full suite drifted from 26s
  to several minutes without anyone noticing.

Routing is not exemption: `-m live` and `-m "not live"` partition the suite,
and the ungated run still executes every test.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest

# Referencing any of these means the module drives the real coordinator, the
# workspace it runs against, or the CLI in a child process. This is a
# convenience so nobody hand-maintains a list of 40-odd files; the duration
# guard below is what actually enforces the lane, and it catches anything this
# heuristic misses in either direction.
#
# `subprocess` earns its place on principle rather than by measurement: a test
# that spawns a process is an integration test by construction, and it pays a
# fresh interpreter start that no in-process memo can ever remove.
LIVE_SOURCE_TOKENS = (
    "live_coordinate_run",
    "live_workspace",
    "LiveWorkspace",
    "subprocess",
)

# Generous next to the ~0.1s a unit test costs here, tight next to the ~5s+ a
# live-coordinator test costs. A test between the two is the interesting case
# and should be looked at, which is what failing does.
FAST_LANE_BUDGET_SECONDS = 3.0

_MODULE_IS_LIVE: dict[str, bool] = {}


def _module_is_live(path: str) -> bool:
    cached = _MODULE_IS_LIVE.get(path)
    if cached is None:
        try:
            source = Path(path).read_text("utf-8")
        except OSError:
            source = ""
        cached = any(token in source for token in LIVE_SOURCE_TOKENS)
        _MODULE_IS_LIVE[path] = cached
    return cached


def pytest_collection_modifyitems(
    config: pytest.Config, items: list[pytest.Item]
) -> None:
    for item in items:
        path = getattr(item, "fspath", None)
        if path is not None and _module_is_live(str(path)):
            item.add_marker(pytest.mark.live)


def _fast_lane_selected(config: pytest.Config) -> bool:
    markexpr = str(getattr(config.option, "markexpr", "") or "")
    return "not live" in markexpr.replace("  ", " ")


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item, call: Any) -> Any:
    outcome = yield
    report = outcome.get_result()
    if report.when != "call" or not report.passed:
        return
    if not _fast_lane_selected(item.config):
        return
    if item.get_closest_marker("live") is not None:
        return
    if report.duration > FAST_LANE_BUDGET_SECONDS:
        report.outcome = "failed"
        report.longrepr = (
            f"fast-lane budget exceeded: {report.duration:.1f}s > "
            f"{FAST_LANE_BUDGET_SECONDS:.1f}s.\n"
            f"{item.nodeid}\n\n"
            "Either make this test fast, or make it an honest integration test "
            "so it is routed to the live lane. If it drives the real "
            "coordinator it should already be detected; if it is slow for "
            "another reason, mark it explicitly with @pytest.mark.live and say "
            "why. Do not raise FAST_LANE_BUDGET_SECONDS to make this pass — "
            "that budget is the only thing keeping the fast lane fast."
        )
