"""The evidence loader's three isolation guarantees.

Harnesses live in a throwaway directory whose name ends in ``-evidence``
so the loader treats them as evidence. Nothing here is a committed path.
"""

from __future__ import annotations

import sys
import tempfile
from collections.abc import Iterator
from pathlib import Path
from typing import Any

import pytest

from tests import evidence_loader


@pytest.fixture
def harness_dir() -> Iterator[Path]:
    saved_path = list(sys.path)
    with tempfile.TemporaryDirectory(suffix="-evidence") as directory:
        yield Path(directory)
    sys.path[:] = saved_path


def test_the_running_module_is_the_owner() -> None:
    assert evidence_loader.current_owner() == __name__


def test_two_owners_get_different_objects(harness_dir: Path) -> None:
    (harness_dir / "probe.py").write_text("VALUE = 1\n", encoding="utf-8")
    evidence_loader.activate("owner-a")
    try:
        first: Any = evidence_loader.load(harness_dir / "probe.py", "probe", owner="owner-a")
        again = evidence_loader.load(harness_dir / "probe.py", "probe", owner="owner-a")
        evidence_loader.activate("owner-b")
        second: Any = evidence_loader.load(harness_dir / "probe.py", "probe", owner="owner-b")
        first.VALUE = 9
        assert second.VALUE == 1
        assert first is again
        assert first is not second
    finally:
        evidence_loader.finish("owner-a")
        evidence_loader.finish("owner-b")


def test_nested_bare_import_resolves_to_the_owners_copy(harness_dir: Path) -> None:
    (harness_dir / "sibling.py").write_text("MARK = 'base'\n", encoding="utf-8")
    (harness_dir / "probe.py").write_text(
        "import sys\n"
        "from pathlib import Path\n"
        "sys.path.insert(0, str(Path(__file__).resolve().parent))\n"
        "import sibling\n"
        "MARK = sibling.MARK\n",
        encoding="utf-8",
    )
    evidence_loader.activate("owner-a")
    try:
        first: Any = evidence_loader.load(harness_dir / "probe.py", "probe", owner="owner-a")
        evidence_loader.activate("owner-b")
        second: Any = evidence_loader.load(harness_dir / "probe.py", "probe", owner="owner-b")
        assert first.sibling is not second.sibling
        first.sibling.MARK = "changed"
        assert second.sibling.MARK == "base"
        assert second.MARK == "base"
    finally:
        evidence_loader.finish("owner-a")
        evidence_loader.finish("owner-b")


def test_engine_attribute_is_restored_when_the_owner_finishes(harness_dir: Path) -> None:
    (harness_dir / "writer.py").write_text(
        "import packages.tax.loader as loader\n"
        "loader._lhi_sentinel = 'written'\n",
        encoding="utf-8",
    )
    from packages.tax import loader as loader_mod

    sentinel = "_lhi_sentinel"
    assert not hasattr(loader_mod, sentinel)
    evidence_loader.activate("owner-engine")
    try:
        evidence_loader.load(harness_dir / "writer.py", "writer", owner="owner-engine")
        assert getattr(loader_mod, sentinel) == "written"
    finally:
        evidence_loader.finish("owner-engine")
    assert not hasattr(loader_mod, sentinel)


def test_class_attribute_is_restored_when_the_owner_finishes(harness_dir: Path) -> None:
    (harness_dir / "writer.py").write_text(
        "import packages.derivation.runner as runner\n"
        "runner._Run._lhi_sentinel = 'written'\n",
        encoding="utf-8",
    )
    from packages.derivation.runner import _Run

    sentinel = "_lhi_sentinel"
    assert sentinel not in _Run.__dict__
    evidence_loader.activate("owner-class")
    try:
        evidence_loader.load(harness_dir / "writer.py", "class_writer", owner="owner-class")
        assert _Run.__dict__[sentinel] == "written"
    finally:
        evidence_loader.finish("owner-class")
        if sentinel in _Run.__dict__:
            delattr(_Run, sentinel)
    assert sentinel not in _Run.__dict__


def test_a_package_import_binding_survives_when_the_owner_is_parked(harness_dir: Path) -> None:
    (harness_dir / "writer.py").write_text(
        "from packages.tax import loader\n"
        "loader._lhi_sentinel = 'written'\n",
        encoding="utf-8",
    )
    evidence_loader.activate("owner-bind")
    try:
        evidence_loader.load(harness_dir / "writer.py", "bind_writer", owner="owner-bind")
        evidence_loader.release("owner-bind")
        from packages.tax import loader as loader_mod

        assert loader_mod.__name__ == "packages.tax.loader"
        assert not hasattr(loader_mod, "_lhi_sentinel")
        evidence_loader.activate("owner-bind")
        assert getattr(loader_mod, "_lhi_sentinel") == "written"
    finally:
        evidence_loader.finish("owner-bind")
        from packages.tax import loader as loader_mod

        if hasattr(loader_mod, "_lhi_sentinel"):
            delattr(loader_mod, "_lhi_sentinel")


def test_an_active_owner_keeps_a_load_from_another_named_test_file(
    harness_dir: Path, tmp_path: Path,
) -> None:
    (harness_dir / "probe.py").write_text("VALUE = 1\n", encoding="utf-8")
    caller = tmp_path / "test_caller.py"
    caller.write_text(
        "from tests import evidence_loader\n"
        "def go(path):\n"
        "    return evidence_loader.load(path, 'inner_probe')\n",
        encoding="utf-8",
    )
    import importlib.util

    spec = importlib.util.spec_from_file_location("not_a_pytest_module", caller)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    evidence_loader.activate(__name__)
    try:
        loaded: Any = module.go(harness_dir / "probe.py")
        assert loaded.VALUE == 1
        assert evidence_loader.current_owner() == __name__
    finally:
        evidence_loader.finish(__name__)
        evidence_loader.activate(__name__)


@pytest.mark.live
def test_in_process_evidence_loads_use_the_loader() -> None:
    """The inventory reads every test module and evidence file.

    That pass takes about twenty seconds, over the fast-lane budget, so
    this check is an integration test. The budget is unchanged.
    """
    repo = Path(__file__).resolve().parents[1]
    inventory_path = (
        repo
        / "docs"
        / "phases"
        / "engine-breadth"
        / "milestones"
        / "live-harness-isolation-evidence"
        / "inventory.py"
    )
    tool: Any = evidence_loader.load(inventory_path, "live_harness_isolation_inventory")
    report = tool.build_report(tool.scan(repo))
    tests = report["tests"]
    assert isinstance(tests, list)
    missed: list[str] = []
    bare: list[str] = []
    for item in tests:
        assert isinstance(item, dict)
        direct = item["direct_loads"]
        assert isinstance(direct, list)
        for load in direct:
            assert isinstance(load, dict)
            if load["evidence"] and not load["isolated"] and load["mechanism"] != "loader":
                missed.append(f"{item['file']}:{load['line']} {load['path']}")
        writes = item["engine_unrestored"]
        assert isinstance(writes, list)
        for write in writes:
            assert isinstance(write, dict)
            target = str(write["target"])
            if not evidence_loader.restores_engine_write(target):
                bare.append(f"{item['file']} {target}")
    assert missed == []
    assert bare == []


def _inventory_tool() -> Any:
    repo = Path(__file__).resolve().parents[1]
    return evidence_loader.load(
        repo
        / "docs"
        / "phases"
        / "engine-breadth"
        / "milestones"
        / "live-harness-isolation-evidence"
        / "inventory.py",
        "live_harness_isolation_inventory",
    )


@pytest.mark.parametrize(
    "body",
    [
        'exec(Path("docs/phases/demo-evidence/probe.py").read_text(encoding="utf-8"))\n',
        'exec(compile(Path("docs/phases/demo-evidence/probe.py").read_bytes(), "probe", "exec"))\n',
        'exec(open("docs/phases/demo-evidence/probe.py").read())\n',
    ],
)
def test_exec_of_an_evidence_file_is_a_load_outside_the_loader(body: str) -> None:
    tool = _inventory_tool()
    repo = Path(__file__).resolve().parents[1]
    source = "from pathlib import Path\n" + body
    facts = tool.Analyzer(repo, "tests/test_demo_exec.py", source).run()
    loads = [
        load
        for load in facts.loads
        if load.evidence and not load.isolated and load.mechanism != "loader"
    ]
    assert [load.path for load in loads][:1] == ["docs/phases/demo-evidence/probe.py"]


def test_a_value_set_outside_the_harness_survives_an_owner_switch(harness_dir: Path) -> None:
    (harness_dir / "writer.py").write_text(
        "import packages.tax.loader as loader\n"
        "loader._lhi_outside = 'harness'\n",
        encoding="utf-8",
    )
    from packages.tax import loader as loader_mod

    name = "_lhi_outside"
    assert not hasattr(loader_mod, name)
    evidence_loader.activate("owner-outside")
    try:
        evidence_loader.load(harness_dir / "writer.py", "writer", owner="owner-outside")
        evidence_loader.release("owner-outside")
        assert not hasattr(loader_mod, name)
        setattr(loader_mod, name, "outside")
        evidence_loader.activate("owner-outside")
        evidence_loader.release("owner-outside")
        assert getattr(loader_mod, name) == "outside"
    finally:
        evidence_loader.finish("owner-outside")
        if hasattr(loader_mod, name):
            delattr(loader_mod, name)
        evidence_loader.activate(__name__)


def test_datetime_strptime_imports_while_an_owner_is_active() -> None:
    """C ``datetime.strptime`` looks the helper up in the interpreter dict.

    Drop any cached helper so the import runs while the overlay is installed.
    """
    import datetime

    sys.modules.pop("_strptime", None)
    real = evidence_loader._interpreter_modules
    assert real is not None
    real.pop("_strptime", None)
    parsed = datetime.datetime.strptime("2020-01-01", "%Y-%m-%d")
    assert parsed == datetime.datetime(2020, 1, 1)


def test_restores_engine_write_rejects_stores_it_cannot_put_back() -> None:
    assert evidence_loader.restores_engine_write("loader.domain_package_companion_declarations")
    assert evidence_loader.restores_engine_write("runner_mod._Run._record_blocked")
    assert not evidence_loader.restores_engine_write("loader.cache[]")
    assert not evidence_loader.restores_engine_write("loader.add()")
    assert not evidence_loader.restores_engine_write("bare")


def test_load_without_an_owner_names_the_calling_module(harness_dir: Path) -> None:
    (harness_dir / "probe.py").write_text("VALUE = 1\n", encoding="utf-8")
    evidence_loader.release(__name__)
    try:
        module: Any = evidence_loader.load(harness_dir / "probe.py", "owned_probe")
        assert module.VALUE == 1
        assert evidence_loader.current_owner() == __name__
        again: Any = evidence_loader.load(harness_dir / "probe.py", "owned_probe")
        assert again is module
    finally:
        evidence_loader.finish(__name__)
        evidence_loader.activate(__name__)
