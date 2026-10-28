"""Select one CI shard without changing markers, and record what ran.

Loaded only with ``-p tools.ci_shard_plugin``. A normal suite run does not
load it. Unittest subtests emit extra ``call`` reports on the parent node id
and set ``context``; those stay inside the parent.

pytest-xdist collects on the workers. Its controller returns from
``pytest_collection`` before it has items, then receives only the node ids
the workers still hold after ``pytest_collection_modifyitems``. The filter
therefore runs on each worker, after that worker snapshots the full list.
Workers publish one shared snapshot beside the execution record. The
controller writes the record from forwarded reports and reads the snapshot.
"""

from __future__ import annotations

import json
import os
from pathlib import Path

import pytest

from tools.ci_gate import ExecutionTally, collection_hash, observe, read_node_id_lines

_STATES: dict[int, list[str]] = {}


def _option(config: pytest.Config, name: str) -> str | None:
    value = config.getoption(name)
    if isinstance(value, str) and value != "":
        return value
    return None


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption("--ci-shard-file", action="store", default=None)
    parser.addoption("--ci-execution-record", action="store", default=None)
    parser.addoption("--ci-collect-out", action="store", default=None)


def pytest_configure(config: pytest.Config) -> None:
    if hasattr(config, "workerinput"):
        return
    record_path = _option(config, "--ci-execution-record")
    if record_path is None:
        return
    config.pluginmanager.register(_Recorder(config, record_path), "ci-shard-recorder")


def _snapshot_path(record_path: str) -> Path:
    return Path(record_path + ".collection")


def _publish_collection(record_path: str, node_ids: list[str]) -> None:
    """Publish the pre-filter node ids. Every worker must publish the same list."""

    path = _snapshot_path(record_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(sorted(node_ids)) + "\n"
    temporary = path.with_name(f"{path.name}.{os.getpid()}.tmp")
    temporary.write_text(text, encoding="utf-8")
    try:
        os.link(temporary, path)
    except FileExistsError:
        existing = path.read_text(encoding="utf-8")
        if existing != text:
            raise pytest.UsageError("workers collected different node ids")
    finally:
        temporary.unlink(missing_ok=True)


def _read_collection(record_path: Path) -> list[str] | None:
    path = _snapshot_path(str(record_path))
    if not path.is_file():
        return None
    loaded = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(loaded, list) or any(not isinstance(item, str) for item in loaded):
        return []
    return loaded


@pytest.hookimpl(tryfirst=True)
def pytest_collection_modifyitems(config: pytest.Config, items: list[pytest.Item]) -> None:
    # The xdist controller never reaches this hook. Workers do, and so does a
    # process started with ``-n0``. Keep the first snapshot: a later call can
    # see the filtered list.
    if id(config) not in _STATES:
        snapshot = [item.nodeid for item in items]
        _STATES[id(config)] = snapshot
        record_path = _option(config, "--ci-execution-record")
        if record_path is not None:
            _publish_collection(record_path, snapshot)
    shard_file = _option(config, "--ci-shard-file")
    if shard_file is None:
        return
    assigned = read_node_id_lines(Path(shard_file).read_text(encoding="utf-8"))
    assigned_set = set(assigned)
    selected: list[pytest.Item] = []
    deselected: list[pytest.Item] = []
    for item in items:
        if item.nodeid in assigned_set:
            selected.append(item)
        else:
            deselected.append(item)
    missing = assigned_set.difference(item.nodeid for item in selected)
    if missing:
        sample = ", ".join(sorted(missing)[:5])
        raise pytest.UsageError(f"{len(missing)} assigned tests were not collected: {sample}")
    items[:] = selected
    if deselected:
        config.hook.pytest_deselected(items=deselected)


def pytest_collection_finish(session: pytest.Session) -> None:
    if hasattr(session.config, "workerinput"):
        return
    out_path = _option(session.config, "--ci-collect-out")
    if out_path is None:
        return
    node_ids = [item.nodeid for item in session.items]
    Path(out_path).write_text("\n".join(node_ids) + ("\n" if node_ids else ""), encoding="utf-8")


class _Recorder:
    def __init__(self, config: pytest.Config, record_path: str) -> None:
        self._config = config
        self._record_path = Path(record_path)
        self._tallies: dict[str, ExecutionTally] = {}

    def pytest_runtest_logreport(self, report: pytest.TestReport) -> None:
        observe(
            self._tallies,
            nodeid=report.nodeid,
            when=report.when,
            outcome=report.outcome,
            subtest=getattr(report, "context", None) is not None,
        )

    def _resolved_collection(self) -> list[str]:
        memory = _STATES.get(id(self._config))
        recorded = _read_collection(self._record_path)
        if memory is not None and recorded is not None:
            try:
                same = collection_hash(memory) == collection_hash(recorded)
            except ValueError:
                return []
            if not same:
                return []
        if recorded is not None:
            return recorded
        if memory is not None:
            return memory
        return []

    def pytest_sessionfinish(self, session: pytest.Session, exitstatus: int) -> None:
        del session, exitstatus
        collected = self._resolved_collection()
        payload = {
            "format": 1,
            "collected_sha256": collection_hash(collected),
            "collected_count": len(collected),
            "executions": [
                tally.as_record(node_id) for node_id, tally in sorted(self._tallies.items())
            ],
        }
        self._record_path.parent.mkdir(parents=True, exist_ok=True)
        self._record_path.write_text(
            json.dumps(payload, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
