"""Published core v86 runs the family-collect Track 0 cases, and the 298 recorded v83 runs.

v86 is package core-calculations v86, registry v84 and release v84. Unique act
lists come from this milestone's track0.py. The 298 recorded v83 runs are
compared with ``tests/fixtures/f1099b_backup_withholding_v83/expected.json``
in place; the 91 that v85 asks are restored with present=no. The fixture is
not copied.

Each case is one live_coordinate_run. One run is several seconds, over the
3.0 s fast-lane budget, so this module is live.
"""

from __future__ import annotations

import copy
import importlib.util
import json
import sys
from pathlib import Path
from types import ModuleType
from typing import Any, cast

import pytest

from tests import evidence_loader

# One live_coordinate_run is several seconds, over the 3.0 s fast-lane budget.
pytestmark = pytest.mark.live

REPO = Path(__file__).resolve().parents[1]
EVIDENCE = REPO / "docs/phases/engine-breadth/milestones/selection-keyed-collect-evidence"
BOX4_EVIDENCE = REPO / "docs/phases/engine-breadth/milestones/f1099b-box4-only-evidence"
AUDIT = REPO / "docs/phases/engine-breadth/milestones/sale-family-audit-evidence/audit_harness.py"
RECORDED_PATH = REPO / "tests/fixtures/f1099b_backup_withholding_v83/expected.json"
TRACK0_NAME = "skc_t1_v86_live_track0"
RECORDED_NAME = "skc_t1_v86_recorded"
HARNESS_NAME = "skc_t1_v86_harness"
PRESENT = "tax.us.2025.f1099b.no-sale-box4-present"
AMOUNT = "f1099b.statement-box4-withholding"
SUBTOTAL = "f1099b.b4-withholding-subtotal"
SYMBOL = "rule.f1099b-b4-amount-symbol"

TRACK0_SPECS = (
    ("no_box4_amount", "cases_empty", (), 0, 0),
    ("one_amount", "cases_one", (150,), 150, 150),
    ("zero_amount", "cases_zero", (0,), 0, 0),
    ("two_statements", "cases_two", (150, 40), 190, 190),
    ("superseded", "cases_superseded", (250,), 250, 250),
    ("withdrawn", "cases_withdrawn", (), "blocked", 0),
)


def _module(name: str, path: Path) -> ModuleType:
    module = sys.modules.get(name)
    if module is None:
        if str(REPO) not in sys.path:
            sys.path.insert(0, str(REPO))
        spec = importlib.util.spec_from_file_location(name, path)
        assert spec is not None and spec.loader is not None
        module = importlib.util.module_from_spec(spec)
        sys.modules[name] = module
        spec.loader.exec_module(module)
    return module


def load_track0() -> ModuleType:
    """This milestone's Track 0 harness, under a name no other test uses. Nothing on it is assigned."""
    if str(REPO) not in sys.path:
        sys.path.insert(0, str(REPO))
    return evidence_loader.load(EVIDENCE / "track0.py", TRACK0_NAME)


def load_recorded() -> ModuleType:
    """The published v83 live module, under a name no other test uses. Nothing on it is assigned."""
    return _module(RECORDED_NAME, REPO / "tests/test_f1099b_backup_withholding_v83.py")


def load_harness() -> ModuleType:
    """The sale-family audit harness, under a name no other test uses. Nothing on it is assigned."""
    if str(REPO) not in sys.path:
        sys.path.insert(0, str(REPO))
    return evidence_loader.load(AUDIT, HARNESS_NAME)


def published(harness: Any) -> Any:
    """Published core v86. The loader entries live in packages/tax/loader.py."""
    core = harness.Core("v86", "v84", "v84")
    assert core.loader_from is None and core.content == REPO / "packages/content/tax/2025"
    return core


def _recorded() -> dict[str, Any]:
    return cast(dict[str, Any], json.loads(RECORDED_PATH.read_text(encoding="utf-8")))


def _neighbour() -> dict[str, Any]:
    return cast(dict[str, Any], json.loads((BOX4_EVIDENCE / "track0-neighbour.json").read_text(encoding="utf-8")))


RECORDED = _recorded()
NEIGHBOUR = _neighbour()
ASKS = tuple(NEIGHBOUR["asks_no_sale_present_ids"])
IDENTICAL = tuple(NEIGHBOUR["identical_ids"])


def test_recorded_split_is_207_identical_and_91_asks() -> None:
    assert len(IDENTICAL) == 207
    assert len(ASKS) == 91
    assert len(set(IDENTICAL) & set(ASKS)) == 0
    fixture_ids = (
        [f"track0/{key}" for key in RECORDED["track0"]]
        + [f"returns/{key}" for key in RECORDED["returns"]]
        + [f"zero/{key}" for key in RECORDED["zero_sample"]]
    )
    assert len(fixture_ids) == 298
    assert set(fixture_ids) == set(IDENTICAL) | set(ASKS)


@pytest.mark.parametrize("case_id,builder,amounts,expect_25b,expect_subtotal", TRACK0_SPECS)
def test_track0_unique_acts_on_published_v86(
        case_id: str, builder: str, amounts: tuple[int, ...], expect_25b: Any, expect_subtotal: Any) -> None:
    track0 = load_track0()
    probe = track0.load_probe()
    core = published(probe._harness())
    spec = getattr(track0, builder)(probe, core)[0]
    assert spec["id"] == case_id
    result = track0.execute(core, spec["acts"], "demo.skc.t1.v86." + case_id)
    assert result.get("outcome") == "success", (case_id, result.get("error") or result.get("reason"), result.get("message"))
    assert result.get("presentation_valid") is True
    assert track0.line_ok(result, expect_25b) == [], case_id
    assert track0.subtotal_ok(result, expect_subtotal) == [], case_id
    assert (result.get("rows") or {}).get(SYMBOL) is None, case_id
    assert track0.pub_values(result, AMOUNT) == [], case_id
    walk = (result.get("walks") or {}).get(SUBTOTAL) or {}
    assert walk.get("walk_has_amount_symbol") is not True, case_id
    blob = "\n".join(walk.get("walk") or [])
    assert "f1099b-b4-amount-symbol" not in blob, case_id
    if amounts:
        failures = track0.walk_claims(result, amounts=list(amounts), want_symbol=False)
        assert failures == [], (case_id, failures)
    amount_walk = (result.get("walks") or {}).get(AMOUNT)
    if not amounts:
        assert amount_walk is None or amount_walk.get("walk_has_amount_symbol") is not True, case_id


def _neighbour_acts(catalog: dict[str, Any], neighbour_id: str) -> list[dict[str, Any]]:
    test = catalog["test"]
    if neighbour_id.startswith("track0/"):
        return cast(list[dict[str, Any]], catalog["track0"][neighbour_id[len("track0/"):]])
    if neighbour_id.startswith("returns/"):
        return cast(list[dict[str, Any]], catalog["returns"][neighbour_id[len("returns/"):]])
    if neighbour_id.startswith("zero/"):
        key = neighbour_id[len("zero/"):]
        return cast(list[dict[str, Any]], test.with_zero(catalog["harness"], catalog["returns"][key], catalog["core"]))
    raise AssertionError(neighbour_id)


def _recorded_pin(neighbour_id: str) -> dict[str, Any]:
    if neighbour_id.startswith("track0/"):
        return cast(dict[str, Any], RECORDED["track0"][neighbour_id[len("track0/"):]])
    if neighbour_id.startswith("returns/"):
        return cast(dict[str, Any], RECORDED["returns"][neighbour_id[len("returns/"):]]["v83"])
    if neighbour_id.startswith("zero/"):
        return cast(dict[str, Any], RECORDED["zero_sample"][neighbour_id[len("zero/"):]]["v83"])
    raise AssertionError(neighbour_id)


@pytest.fixture(scope="module")
def recorded_acts(tmp_path_factory: pytest.TempPathFactory) -> dict[str, Any]:
    test = load_recorded()
    harness = test.track0()
    exported = test.export_returns(tmp_path_factory.mktemp("skc-t1-v86"))
    harness_mod = load_harness()
    return {
        "test": test,
        "harness": harness,
        "harness_mod": harness_mod,
        "track0": dict(test.decided_cases(harness)),
        "returns": test.return_acts(harness, exported),
        "core": published(harness_mod),
    }


def _assert_recorded(catalog: dict[str, Any], neighbour_id: str, acts: list[dict[str, Any]]) -> None:
    test = catalog["test"]
    got = test.pin(test.track0().run_coordinate(
        catalog["core"], acts, "demo.skc.t1.v86.recorded." + neighbour_id.replace("/", ".")))
    assert got == _recorded_pin(neighbour_id), neighbour_id


@pytest.mark.parametrize("neighbour_id", [key for key in IDENTICAL if key.startswith("track0/")])
def test_recorded_track0_identical(recorded_acts: dict[str, Any], neighbour_id: str) -> None:
    _assert_recorded(recorded_acts, neighbour_id, _neighbour_acts(recorded_acts, neighbour_id))


@pytest.mark.parametrize("neighbour_id", [key for key in IDENTICAL if key.startswith("returns/")])
def test_recorded_return_identical(recorded_acts: dict[str, Any], neighbour_id: str) -> None:
    _assert_recorded(recorded_acts, neighbour_id, _neighbour_acts(recorded_acts, neighbour_id))


@pytest.mark.parametrize("neighbour_id", [key for key in ASKS if key.startswith("track0/")])
def test_recorded_track0_restore_present_no(recorded_acts: dict[str, Any], neighbour_id: str) -> None:
    acts = recorded_acts["harness_mod"].say(
        copy.deepcopy(_neighbour_acts(recorded_acts, neighbour_id)), PRESENT, "no", "t1.restore")
    _assert_recorded(recorded_acts, neighbour_id, acts)


@pytest.mark.parametrize("neighbour_id", [key for key in ASKS if key.startswith("returns/")])
def test_recorded_return_restore_present_no(recorded_acts: dict[str, Any], neighbour_id: str) -> None:
    acts = recorded_acts["harness_mod"].say(
        copy.deepcopy(_neighbour_acts(recorded_acts, neighbour_id)), PRESENT, "no", "t1.restore")
    _assert_recorded(recorded_acts, neighbour_id, acts)


@pytest.mark.parametrize("neighbour_id", [key for key in ASKS if key.startswith("zero/")])
def test_recorded_zero_restore_present_no(recorded_acts: dict[str, Any], neighbour_id: str) -> None:
    acts = recorded_acts["harness_mod"].say(
        copy.deepcopy(_neighbour_acts(recorded_acts, neighbour_id)), PRESENT, "no", "t1.restore")
    _assert_recorded(recorded_acts, neighbour_id, acts)
