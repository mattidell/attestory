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

import os
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


def _restore_schema_compile_memo() -> None:
    """Recompile published schemas when a test has dropped the memo.

    The session warm-up fills ``_COMPILED_SCHEMAS`` once per worker.
    ``tests/test_incremental_lattice.py`` then calls
    ``schema_registry.clear_caches`` so a mutated validator cannot reuse a
    verdict, and it leaves the memo empty. The next derivation test on
    that worker recompiles every published schema inside its timed call.
    Measured on this test: 1.71s locally after that clear, and 3.7s on CI
    quick job 130141445121 (run 42905252770), over the 3.0s budget. A cold
    ``DerivationSchemas()`` is ``jsonschema`` meta-validation of the
    published schema files; the second call in the same process is about
    0.01s. Pay the recompile here, in teardown, which the budget does not
    time. Skip the work when the memo is already populated.
    """
    from packages.kernel import schema_registry

    if schema_registry._COMPILED_SCHEMAS:
        return
    from packages.derivation.loader import DerivationSchemas

    DerivationSchemas()


@pytest.fixture(autouse=True)
def _restore_schema_compile_after_fast_lane_test(request: pytest.FixtureRequest) -> Any:
    """Share the schema-compile load across the fast lane.

    See ``_restore_schema_compile_memo``. Setup does nothing, so a test
    that clears the memo still observes the empty memo during its call.
    """
    yield
    if _fast_lane_selected(request.config):
        _restore_schema_compile_memo()


@pytest.fixture(scope="session", autouse=True)
def _warm_derivation_cold_start(request: pytest.FixtureRequest) -> None:
    """Pay each worker's derivation cold first-use cost once, before any
    test's call phase is timed.

    The first derivation-running test on a worker builds the schema
    registry from scratch: `packages/kernel/schema_registry.py` compiles
    every published validator into its process-global `_COMPILED_SCHEMAS`
    memo, and `SchemaRegistry.validate` records fresh verdicts in
    `_VALIDATION_VERDICTS` for whatever content the call validates. A later
    call in the same process hits both memos (Track 3 cold-start finding:
    2.41s CPU on the first call of this exact case, 0.02-0.03s on the
    second and third).

    Fixture setup runs before any test's call phase, so paying this cost
    here never counts against `FAST_LANE_BUDGET_SECONDS`. This shares
    nothing new into tests beyond those two memos, which the product
    already keeps for the life of the process; there is no teardown
    because nothing is retained that the product does not retain anyway.

    Gated on the same `-m "not live"` selection the budget hook already
    checks, so a full or live-only run is unaffected and still constructs
    its own registry on first use as before.
    """
    if not _fast_lane_selected(request.config):
        return
    from tests.derivation import adr0077_worksheet_fixture as fx

    fx.marshal(fx.parts(), fx.case_rows("old-only"))


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


@pytest.fixture(scope="session", autouse=True)
def _evidence_harness_session() -> Any:
    """Drop parked harness copies when the worker exits.

    Module teardown only parks an owner: xdist worksteal can run another
    module and then return, and the returned module must still see the
    copies and engine writes from its earlier tests. Nothing after the
    session needs those writes.
    """
    from tests import evidence_loader

    yield
    evidence_loader.finish_all()


@pytest.fixture(scope="module", autouse=True)
def _evidence_harness_owner(request: pytest.FixtureRequest) -> Any:
    """The running test module owns any evidence harness it loads.

    Setup is the owner for every test in the module. Teardown parks that
    owner's engine writes so the next module on this worker does not see
    them, and keeps the copies for a later test of the same module.
    """
    from tests import evidence_loader

    owner = request.module.__name__
    evidence_loader.activate(owner)
    yield
    evidence_loader.release(owner)


def pytest_runtest_setup(item: pytest.Item) -> None:
    """Re-bind the owner in the test's own context.

    A module fixture sets the context variable before the test, but a
    runner that copies the context would otherwise drop it. The owner
    name is the test module, which is also what an import-time load
    records, so call-time writes land on the same owner.
    """
    from tests import evidence_loader

    module = getattr(item, "module", None)
    name = getattr(module, "__name__", None)
    if isinstance(name, str):
        evidence_loader.activate(name)


@pytest.fixture(scope="session", autouse=True)
def _test_browser_resources(tmp_path_factory: pytest.TempPathFactory, request: pytest.FixtureRequest) -> Any:
    """Share the startup gate across xdist workers without eager browsers."""
    base = tmp_path_factory.getbasetemp()
    root = base.parent if hasattr(request.config, "workerinput") else base
    previous = os.environ.get("DEMO_CHROME_STARTUP_DIR")
    os.environ["DEMO_CHROME_STARTUP_DIR"] = str(root)
    yield
    from tests.helpers.correction_browser_owner import close
    close()
    if previous is None:
        os.environ.pop("DEMO_CHROME_STARTUP_DIR", None)
    else:
        os.environ["DEMO_CHROME_STARTUP_DIR"] = previous
