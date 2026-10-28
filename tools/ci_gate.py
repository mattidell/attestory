"""CI gate for an unchanged full suite split across runners.

The required check stays the job named ``verify``. Shard assignment, coverage,
and the pass/fail decision live here so they can be tested without GitHub.

Three clocks are kept apart:

- Elapsed wait is wall-clock time until the gate finishes. The slowest shard
  dominates it.
- CPU is user plus system time of the pytest process tree on each runner,
  summed across shards. GNU ``time -v`` includes waited children, which is
  how the xdist workers are counted.
- Billed runner time follows each runner's wall clock for the whole job,
  including checkout and install, summed across jobs and rounded by GitHub.
  It is not CPU and it is not the workflow's elapsed wait.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import statistics
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Mapping, Sequence, TypedDict

SHARD_COUNT = 4
WORKERS_PER_SHARD = 4
WEIGHTS_PATH = Path(
    "docs/phases/engineering-health/milestones/"
    "test-cost-remaining-evidence/ci-node-durations.json"
)
WEIGHT_CLOCK = (
    "junit testcase time (setup + call + teardown), worker wall seconds, not CPU"
)
SOURCE_RUN = "40515157618"
SOURCE_COMMIT = "a0bc250a67449a347f609550906f229fdd872daa"

_USER_TIME = re.compile(r"^[ \t]*User time \(seconds\): ([0-9.]+)[ \t]*$", re.M)
_SYSTEM_TIME = re.compile(r"^[ \t]*System time \(seconds\): ([0-9.]+)[ \t]*$", re.M)
_ELAPSED_TIME = re.compile(
    r"^[ \t]*Elapsed \(wall clock\) time \(h:mm:ss or m:ss\): ([0-9:.]+)[ \t]*$",
    re.M,
)


class ExecutionRecord(TypedDict):
    nodeid: str
    parent_calls: int
    subtest_calls: int
    setup_terminal: int


class CpuRecord(TypedDict):
    available: bool
    user_seconds: float | None
    system_seconds: float | None
    elapsed_seconds: float | None


class JunitRecord(TypedDict):
    session_seconds: float
    testcase_seconds: float
    tests_attr: int
    testcase_count: int
    failures: int
    errors: int
    skipped: int


class ShardManifest(TypedDict):
    format: int
    shard_index: int
    shard_count: int
    nproc: int | None
    pytest_exit: int
    collection_sha256: str
    collected_count: int
    assigned_count: int
    problems: list[str]
    cpu: CpuRecord
    junit: JunitRecord | None
    executions: list[ExecutionRecord]


@dataclass
class ExecutionTally:
    parent_calls: int = 0
    subtest_calls: int = 0
    setup_terminal: int = 0

    def as_record(self, node_id: str) -> ExecutionRecord:
        return ExecutionRecord(
            nodeid=node_id,
            parent_calls=self.parent_calls,
            subtest_calls=self.subtest_calls,
            setup_terminal=self.setup_terminal,
        )


def observe(
    tallies: dict[str, ExecutionTally],
    *,
    nodeid: str,
    when: str,
    outcome: str,
    subtest: bool,
) -> None:
    """Count one pytest report.

    A unittest subtest is another ``call`` report on the parent node id.
    It is not a separate collected test. A skip or error that never reaches
    ``call`` is counted from ``setup``.
    """

    row = tallies.setdefault(nodeid, ExecutionTally())
    if when == "call" and subtest:
        row.subtest_calls += 1
    elif when == "call":
        row.parent_calls += 1
    elif when == "setup" and outcome != "passed":
        row.setup_terminal += 1


def execution_problem(row: ExecutionRecord) -> str | None:
    parent = row["parent_calls"]
    setup = row["setup_terminal"]
    if parent > 1:
        return "duplicate execution"
    if parent == 1:
        return None
    if parent == 0 and setup == 1 and row["subtest_calls"] == 0:
        return None
    if parent == 0 and setup > 1:
        return "duplicate setup"
    return "missing execution"


def collection_hash(node_ids: Sequence[str]) -> str:
    ordered = sorted(node_ids)
    if len(ordered) != len(set(ordered)):
        raise ValueError("duplicate node ids")
    payload = "\n".join(ordered) + "\n"
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def junit_identity(node_id: str) -> tuple[str, str]:
    file_part, separator, rest = node_id.partition("::")
    if separator != "::" or not file_part.endswith(".py") or rest == "":
        raise ValueError(f"not a pytest node id: {node_id}")
    module = file_part[:-3].replace("/", ".")
    parts = rest.split("::")
    if any(part == "" for part in parts):
        raise ValueError(f"not a pytest node id: {node_id}")
    name = parts[-1]
    if len(parts) == 1:
        classname = module
    else:
        classname = module + "." + ".".join(parts[:-1])
    return classname, name


def read_node_id_lines(text: str) -> list[str]:
    node_ids = [line.strip() for line in text.splitlines() if line.strip()]
    if len(node_ids) != len(set(node_ids)):
        raise ValueError("duplicate node ids")
    return node_ids


def partition_assignment(
    collected: Sequence[str], assigned: Sequence[str]
) -> tuple[list[str], list[str]]:
    assigned_set = set(assigned)
    selected = [node_id for node_id in collected if node_id in assigned_set]
    missing = sorted(assigned_set.difference(selected))
    return selected, missing


def default_weight(durations: Mapping[str, float]) -> float:
    if not durations:
        raise ValueError("duration map is empty")
    return float(statistics.median(list(durations.values())))


def _weight(node_id: str, durations: Mapping[str, float], fallback: float) -> float:
    if node_id in durations:
        return float(durations[node_id])
    return fallback


def assign_shards(
    node_ids: Sequence[str],
    durations: Mapping[str, float],
    shard_count: int,
) -> list[list[str]]:
    """Longest-first packing. Every id is placed once. Ties take the lower index."""

    if shard_count < 1:
        raise ValueError("shard_count must be positive")
    if len(node_ids) != len(set(node_ids)):
        raise ValueError("collected node ids contain duplicates")
    fallback = default_weight(durations)
    shards: list[list[str]] = [[] for _ in range(shard_count)]
    loads = [0.0] * shard_count
    ranked = sorted(node_ids, key=lambda node_id: (-_weight(node_id, durations, fallback), node_id))
    for node_id in ranked:
        index = min(range(shard_count), key=lambda item: (loads[item], item))
        shards[index].append(node_id)
        loads[index] += _weight(node_id, durations, fallback)
    for shard in shards:
        shard.sort()
    return shards


def simulated_wall(
    node_ids: Sequence[str],
    durations: Mapping[str, float],
    workers: int,
) -> float:
    """Lower bound on shard elapsed time if every worker stays busy."""

    if workers < 1:
        raise ValueError("workers must be positive")
    if not node_ids:
        return 0.0
    fallback = default_weight(durations)
    loads = [0.0] * workers
    ranked = sorted(node_ids, key=lambda node_id: (-_weight(node_id, durations, fallback), node_id))
    for node_id in ranked:
        index = min(range(workers), key=lambda item: (loads[item], item))
        loads[index] += _weight(node_id, durations, fallback)
    return max(loads)


def shard_loads(
    shards: Sequence[Sequence[str]],
    durations: Mapping[str, float],
) -> list[float]:
    fallback = default_weight(durations)
    return [
        sum(_weight(node_id, durations, fallback) for node_id in shard) for shard in shards
    ]


def parse_elapsed(value: str) -> float:
    parts = value.split(":")
    if len(parts) == 1:
        return float(parts[0])
    if len(parts) == 2:
        minutes, seconds = parts
        return int(minutes) * 60 + float(seconds)
    if len(parts) == 3:
        hours, minutes, seconds = parts
        return int(hours) * 3600 + int(minutes) * 60 + float(seconds)
    raise ValueError(value)


def parse_gnu_time(text: str) -> CpuRecord:
    user = _USER_TIME.search(text)
    system = _SYSTEM_TIME.search(text)
    elapsed = _ELAPSED_TIME.search(text)
    if user is None or system is None or elapsed is None:
        return unavailable_cpu()
    try:
        return CpuRecord(
            available=True,
            user_seconds=float(user.group(1)),
            system_seconds=float(system.group(1)),
            elapsed_seconds=parse_elapsed(elapsed.group(1)),
        )
    except ValueError:
        return unavailable_cpu()


def unavailable_cpu() -> CpuRecord:
    return CpuRecord(
        available=False,
        user_seconds=None,
        system_seconds=None,
        elapsed_seconds=None,
    )


def cpu_count() -> int | None:
    process_cpu_count = getattr(os, "process_cpu_count", None)
    if callable(process_cpu_count):
        value = process_cpu_count()
        if isinstance(value, int):
            return value
    return os.cpu_count()


def junit_record(path: Path) -> JunitRecord:
    root = ET.parse(path).getroot()
    suite = root if root.tag == "testsuite" else root.find("testsuite")
    if suite is None:
        raise ValueError("junit file has no testsuite")
    cases = list(root.iter("testcase"))
    return JunitRecord(
        session_seconds=float(suite.attrib.get("time", "0")),
        testcase_seconds=sum(float(case.attrib.get("time", "0")) for case in cases),
        tests_attr=int(suite.attrib.get("tests", "0")),
        testcase_count=len(cases),
        failures=int(suite.attrib.get("failures", "0")),
        errors=int(suite.attrib.get("errors", "0")),
        skipped=int(suite.attrib.get("skipped", "0")),
    )


def junit_identities(path: Path) -> list[tuple[str, str]]:
    root = ET.parse(path).getroot()
    identities: list[tuple[str, str]] = []
    for case in root.iter("testcase"):
        identities.append((case.attrib["classname"], case.attrib["name"]))
    return identities


def durations_from_junit(
    node_ids: Sequence[str],
    junit_path: Path,
) -> tuple[dict[str, float], list[str], int, float]:
    """Join collected node ids to junit rows. Return weights, missing ids, stale rows, session seconds."""

    root = ET.parse(junit_path).getroot()
    suite = root if root.tag == "testsuite" else root.find("testsuite")
    if suite is None:
        raise ValueError("junit file has no testsuite")
    by_identity: dict[tuple[str, str], float] = {}
    for case in root.iter("testcase"):
        identity = (case.attrib["classname"], case.attrib["name"])
        if identity in by_identity:
            raise ValueError(f"duplicate junit row: {identity[0]}::{identity[1]}")
        by_identity[identity] = float(case.attrib.get("time", "0"))
    claimed: dict[tuple[str, str], str] = {}
    matched: dict[str, float] = {}
    missing: list[str] = []
    for node_id in node_ids:
        identity = junit_identity(node_id)
        previous = claimed.get(identity)
        if previous is not None:
            raise ValueError(f"node ids collide in junit identity: {previous} and {node_id}")
        claimed[identity] = node_id
        weight = by_identity.get(identity)
        if weight is None:
            missing.append(node_id)
        else:
            matched[node_id] = weight
    stale = len(set(by_identity).difference(claimed))
    return matched, missing, stale, float(suite.attrib.get("time", "0"))


def is_draft(event_name: str, draft_flag: str) -> bool:
    return event_name == "pull_request" and draft_flag.strip().lower() == "true"


def job_result(needs: object, job_id: str) -> str:
    if not isinstance(needs, dict):
        return "missing"
    job = needs.get(job_id)
    if not isinstance(job, dict):
        return "missing"
    result = job.get("result")
    if not isinstance(result, str) or result == "":
        return "missing"
    return result


def prerequisite_problems(
    needs: object,
    *,
    event_name: str,
    draft_flag: str,
) -> list[str]:
    """Fail unless this is a full-gate event and both dependency jobs succeeded.

    ``skipped`` is a success for classic branch protection when it is the
    required check's own conclusion. It is not a successful dependency.
    """

    problems: list[str] = []
    if is_draft(event_name, draft_flag):
        problems.append(
            "draft pull request: the full suite has not run on this head"
        )
    for job_id in ("precheck", "suite-shard"):
        result = job_result(needs, job_id)
        if result != "success":
            problems.append(f"{job_id} result is {result}")
    return problems


def _require_int(data: Mapping[str, object], key: str) -> int:
    value = data.get(key)
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError(f"{key} is not an integer")
    return value


def _require_str(data: Mapping[str, object], key: str) -> str:
    value = data.get(key)
    if not isinstance(value, str) or value == "":
        raise ValueError(f"{key} is not a string")
    return value


def _require_float(value: object, label: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{label} is not a number")
    return float(value)


def parse_manifest(data: object) -> ShardManifest:
    if not isinstance(data, dict):
        raise ValueError("manifest is not an object")
    if data.get("format") != 1:
        raise ValueError("manifest format is not 1")
    cpu_value = data.get("cpu")
    if not isinstance(cpu_value, dict):
        raise ValueError("cpu is not an object")
    available = cpu_value.get("available")
    if not isinstance(available, bool):
        raise ValueError("cpu.available is not a boolean")
    if available:
        cpu = CpuRecord(
            available=True,
            user_seconds=_require_float(cpu_value.get("user_seconds"), "user_seconds"),
            system_seconds=_require_float(cpu_value.get("system_seconds"), "system_seconds"),
            elapsed_seconds=_require_float(cpu_value.get("elapsed_seconds"), "elapsed_seconds"),
        )
    else:
        cpu = unavailable_cpu()
    junit_value = data.get("junit")
    junit: JunitRecord | None
    if junit_value is None:
        junit = None
    elif isinstance(junit_value, dict):
        junit = JunitRecord(
            session_seconds=_require_float(junit_value.get("session_seconds"), "session_seconds"),
            testcase_seconds=_require_float(
                junit_value.get("testcase_seconds"), "testcase_seconds"
            ),
            tests_attr=_require_int(junit_value, "tests_attr"),
            testcase_count=_require_int(junit_value, "testcase_count"),
            failures=_require_int(junit_value, "failures"),
            errors=_require_int(junit_value, "errors"),
            skipped=_require_int(junit_value, "skipped"),
        )
    else:
        raise ValueError("junit is not an object")
    raw_executions = data.get("executions")
    if not isinstance(raw_executions, list):
        raise ValueError("executions is not a list")
    executions: list[ExecutionRecord] = []
    for item in raw_executions:
        if not isinstance(item, dict):
            raise ValueError("execution is not an object")
        executions.append(
            ExecutionRecord(
                nodeid=_require_str(item, "nodeid"),
                parent_calls=_require_int(item, "parent_calls"),
                subtest_calls=_require_int(item, "subtest_calls"),
                setup_terminal=_require_int(item, "setup_terminal"),
            )
        )
    raw_problems = data.get("problems")
    if not isinstance(raw_problems, list) or any(not isinstance(item, str) for item in raw_problems):
        raise ValueError("problems is not a list of strings")
    nproc = data.get("nproc")
    if nproc is not None and (isinstance(nproc, bool) or not isinstance(nproc, int)):
        raise ValueError("nproc is not an integer")
    collection_sha256 = data.get("collection_sha256")
    if not isinstance(collection_sha256, str):
        raise ValueError("collection_sha256 is not a string")
    return ShardManifest(
        format=1,
        shard_index=_require_int(data, "shard_index"),
        shard_count=_require_int(data, "shard_count"),
        nproc=nproc,
        pytest_exit=_require_int(data, "pytest_exit"),
        collection_sha256=collection_sha256,
        collected_count=_require_int(data, "collected_count"),
        assigned_count=_require_int(data, "assigned_count"),
        problems=list(raw_problems),
        cpu=cpu,
        junit=junit,
        executions=executions,
    )


def coverage_problems(
    collected: Sequence[str],
    shards: Sequence[tuple[ShardManifest, list[tuple[str, str]]]],
    *,
    shard_count: int,
) -> list[str]:
    problems: list[str] = []
    try:
        expected_hash = collection_hash(collected)
    except ValueError as exc:
        return [str(exc)]
    if len(shards) != shard_count:
        problems.append(f"shard artifacts {len(shards)} != {shard_count}")
    indexes = [manifest["shard_index"] for manifest, _identities in shards]
    if sorted(indexes) != list(range(shard_count)):
        problems.append(f"shard indexes are {sorted(indexes)}")
    seen: dict[str, int] = {}
    for manifest, identities in shards:
        index = manifest["shard_index"]
        prefix = f"shard {index}"
        if manifest["shard_count"] != shard_count:
            problems.append(f"{prefix} shard_count is {manifest['shard_count']}")
        if manifest["pytest_exit"] != 0:
            problems.append(f"{prefix} pytest_exit is {manifest['pytest_exit']}")
        if manifest["collection_sha256"] != expected_hash:
            problems.append(f"{prefix} collection hash does not match a fresh collection")
        if manifest["collected_count"] != len(collected):
            problems.append(
                f"{prefix} collected_count is {manifest['collected_count']}, fresh collection is {len(collected)}"
            )
        junit = manifest["junit"]
        executions = manifest["executions"]
        if junit is None:
            problems.append(f"{prefix} has no junit record")
        else:
            if junit["failures"] != 0 or junit["errors"] != 0:
                problems.append(
                    f"{prefix} junit failures {junit['failures']} errors {junit['errors']}"
                )
            if junit["testcase_count"] != len(executions):
                problems.append(
                    f"{prefix} junit rows {junit['testcase_count']} != executions {len(executions)}"
                )
            subtests = sum(row["subtest_calls"] for row in executions)
            expected_attr = len(executions) + subtests
            if junit["tests_attr"] != expected_attr:
                problems.append(
                    f"{prefix} junit tests attribute {junit['tests_attr']} != "
                    f"executions {len(executions)} + subtests {subtests}"
                )
        identity_rows = []
        for row in executions:
            problem = execution_problem(row)
            if problem is not None:
                problems.append(f"{prefix} {row['nodeid']} {problem}")
            try:
                identity_rows.append(junit_identity(row["nodeid"]))
            except ValueError as exc:
                problems.append(f"{prefix} {exc}")
            previous = seen.get(row["nodeid"])
            if previous is not None:
                problems.append(
                    f"duplicate {row['nodeid']} on shards {previous} and {index}"
                )
            else:
                seen[row["nodeid"]] = index
        if Counter(identity_rows) != Counter(identities):
            problems.append(f"{prefix} junit identities do not match executed node ids")
    missing = sorted(set(collected).difference(seen))
    extra = sorted(set(seen).difference(collected))
    if missing:
        sample = ", ".join(missing[:8])
        problems.append(f"omissions {len(missing)}: {sample}")
    if extra:
        sample = ", ".join(extra[:8])
        problems.append(f"extras {len(extra)}: {sample}")
    return problems


def accounting(manifests: Sequence[ShardManifest]) -> dict[str, float | int | None]:
    elapsed = [
        manifest["cpu"]["elapsed_seconds"]
        for manifest in manifests
        if manifest["cpu"]["available"] and manifest["cpu"]["elapsed_seconds"] is not None
    ]
    user = [
        manifest["cpu"]["user_seconds"]
        for manifest in manifests
        if manifest["cpu"]["available"] and manifest["cpu"]["user_seconds"] is not None
    ]
    system = [
        manifest["cpu"]["system_seconds"]
        for manifest in manifests
        if manifest["cpu"]["available"] and manifest["cpu"]["system_seconds"] is not None
    ]
    sessions = [
        manifest["junit"]["session_seconds"]
        for manifest in manifests
        if manifest["junit"] is not None
    ]
    testcase_sum = sum(
        manifest["junit"]["testcase_seconds"]
        for manifest in manifests
        if manifest["junit"] is not None
    )
    subtests = sum(
        row["subtest_calls"] for manifest in manifests for row in manifest["executions"]
    )
    return {
        "shard_pytest_elapsed_max_seconds": max(elapsed) if elapsed else None,
        "shard_pytest_elapsed_sum_seconds": sum(elapsed) if elapsed else None,
        "shard_junit_session_max_seconds": max(sessions) if sessions else None,
        "shard_junit_session_sum_seconds": sum(sessions) if sessions else None,
        "worker_wall_seconds": testcase_sum,
        "cpu_user_seconds": sum(user) if user else None,
        "cpu_system_seconds": sum(system) if system else None,
        "cpu_seconds": (sum(user) + sum(system)) if user and system else None,
        "executed_tests": sum(len(manifest["executions"]) for manifest in manifests),
        "subtest_calls": subtests,
    }


def collect_pytest_command(out_path: Path) -> list[str]:
    return [
        sys.executable,
        "-m",
        "pytest",
        "-n0",
        "--collect-only",
        "-q",
        "-p",
        "tools.ci_shard_plugin",
        "--ci-collect-out",
        str(out_path),
        "-p",
        "no:cacheprovider",
    ]


def shard_pytest_command(shard_file: Path, record_path: Path, junit_path: Path) -> list[str]:
    return [
        sys.executable,
        "-m",
        "pytest",
        "-p",
        "tools.ci_shard_plugin",
        "--ci-shard-file",
        str(shard_file),
        "--ci-execution-record",
        str(record_path),
        "--junitxml",
        str(junit_path),
        "--durations=50",
    ]


def gnu_time_available() -> bool:
    if not Path("/usr/bin/time").is_file():
        return False
    probe = subprocess.run(
        ["/usr/bin/time", "-v", "--", "true"],
        check=False,
        capture_output=True,
        text=True,
    )
    return probe.returncode == 0


def run_timed(command: Sequence[str], rusage_path: Path) -> tuple[int, CpuRecord]:
    if gnu_time_available():
        completed = subprocess.run(
            ["/usr/bin/time", "-v", "-o", str(rusage_path), *command],
            check=False,
        )
        if rusage_path.is_file():
            return completed.returncode, parse_gnu_time(rusage_path.read_text(encoding="utf-8"))
        return completed.returncode, unavailable_cpu()
    completed = subprocess.run(list(command), check=False)
    return completed.returncode, unavailable_cpu()


def collect_node_ids() -> list[str]:
    with tempfile.TemporaryDirectory() as tmp:
        out_path = Path(tmp) / "nodeids.txt"
        completed = subprocess.run(
            collect_pytest_command(out_path),
            check=False,
            capture_output=True,
            text=True,
        )
        if completed.returncode != 0 or not out_path.is_file():
            sys.stderr.write(completed.stdout)
            sys.stderr.write(completed.stderr)
            raise RuntimeError(f"collection failed with exit {completed.returncode}")
        return read_node_id_lines(out_path.read_text(encoding="utf-8"))


def load_durations(path: Path) -> dict[str, float]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or data.get("format") != 1:
        raise ValueError("duration file format is not 1")
    raw = data.get("durations")
    if not isinstance(raw, dict) or not raw:
        raise ValueError("duration file has no durations")
    durations: dict[str, float] = {}
    for node_id, weight in raw.items():
        if not isinstance(node_id, str):
            raise ValueError("duration node id is not a string")
        durations[node_id] = _require_float(weight, node_id)
    return durations


def _load_duration_document(path: Path) -> dict[str, object]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("duration file is not an object")
    return data


def plan_report(
    collected: Sequence[str],
    durations: Mapping[str, float],
    *,
    workers: int,
    shard_counts: Sequence[int],
    source_session_seconds: float | None,
) -> str:
    fallback = default_weight(durations)
    unweighted = [node_id for node_id in collected if node_id not in durations]
    lines = [
        f"collected: {len(collected)}",
        f"weighted: {len(collected) - len(unweighted)}",
        f"unweighted: {len(unweighted)}",
        f"default_weight_seconds: {fallback:.6f}",
        f"workers_per_shard_assumed: {workers}",
        "clock: " + WEIGHT_CLOCK,
        (
            "simulated wall packs each shard's tests onto that many workers. "
            "It excludes checkout, interpreter setup, cheap checks, the verify tail, "
            "extra cold starts, and host-speed variation."
        ),
    ]
    if unweighted:
        files = sorted({node_id.split("::", 1)[0] for node_id in unweighted})
        lines.append("unweighted_files: " + ", ".join(files))
    lines.append("shards\tload_max_s\tload_min_s\twall_max_s\twall_min_s\tlongest_s")
    for shard_count in shard_counts:
        shards = assign_shards(collected, durations, shard_count)
        flat = [node_id for shard in shards for node_id in shard]
        if sorted(flat) != sorted(collected) or len(flat) != len(set(flat)):
            raise RuntimeError(f"shard count {shard_count} is not a partition")
        loads = shard_loads(shards, durations)
        walls = [simulated_wall(shard, durations, workers) for shard in shards]
        longest = max(
            _weight(node_id, durations, fallback) for shard in shards for node_id in shard
        )
        lines.append(
            f"{shard_count}\t{max(loads):.1f}\t{min(loads):.1f}\t"
            f"{max(walls):.1f}\t{min(walls):.1f}\t{longest:.1f}"
        )
        if shard_count == 1 and source_session_seconds is not None:
            lines.append(
                f"one_shard_model_seconds: {walls[0]:.1f}",
            )
            lines.append(f"source_session_seconds: {source_session_seconds:.3f}")
    return "\n".join(lines) + "\n"


def _positive_int(value: str) -> int:
    parsed = int(value)
    if parsed < 1:
        raise argparse.ArgumentTypeError("must be positive")
    return parsed


def command_plan(durations_path: Path, *, workers: int, shard_count: int) -> int:
    collected = collect_node_ids()
    document = _load_duration_document(durations_path)
    durations = load_durations(durations_path)
    session = document.get("source_session_seconds")
    session_seconds = float(session) if isinstance(session, (int, float)) else None
    counts = list(range(1, max(shard_count, 1) + 1))
    sys.stdout.write(
        plan_report(
            collected,
            durations,
            workers=workers,
            shard_counts=counts,
            source_session_seconds=session_seconds,
        )
    )
    return 0


def command_import_durations(
    junit_path: Path,
    out_path: Path,
    *,
    source_run: str,
    source_commit: str,
) -> int:
    collected = collect_node_ids()
    matched, missing, stale, session_seconds = durations_from_junit(collected, junit_path)
    document = {
        "format": 1,
        "source_run": source_run,
        "source_commit": source_commit,
        "clock": WEIGHT_CLOCK,
        "source_session_seconds": session_seconds,
        "source_testcase_seconds": sum(matched.values()),
        "matched_node_ids": len(matched),
        "durations": matched,
    }
    out_path.write_text(
        json.dumps(document, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    sys.stdout.write(
        f"matched: {len(matched)}\nmissing: {len(missing)}\nstale: {stale}\n"
        f"session_seconds: {session_seconds:.3f}\n"
    )
    return 0


def _execution_records(data: object) -> tuple[str, int, list[ExecutionRecord]]:
    if not isinstance(data, dict) or data.get("format") != 1:
        raise ValueError("execution record format is not 1")
    collected_hash = data.get("collected_sha256")
    collected_count = data.get("collected_count")
    raw_rows = data.get("executions")
    if not isinstance(collected_hash, str) or collected_hash == "":
        raise ValueError("execution record has no collection hash")
    if isinstance(collected_count, bool) or not isinstance(collected_count, int):
        raise ValueError("execution record count is not an integer")
    if not isinstance(raw_rows, list):
        raise ValueError("execution record has no executions")
    rows: list[ExecutionRecord] = []
    for item in raw_rows:
        if not isinstance(item, dict):
            raise ValueError("execution row is not an object")
        rows.append(
            ExecutionRecord(
                nodeid=_require_str(item, "nodeid"),
                parent_calls=_require_int(item, "parent_calls"),
                subtest_calls=_require_int(item, "subtest_calls"),
                setup_terminal=_require_int(item, "setup_terminal"),
            )
        )
    return collected_hash, collected_count, rows


def command_run_shard(
    *,
    index: int,
    shard_count: int,
    durations_path: Path,
    results_dir: Path,
) -> int:
    if index < 0 or index >= shard_count:
        raise ValueError(f"shard index {index} is outside 0..{shard_count - 1}")
    results_dir.mkdir(parents=True, exist_ok=True)
    problems: list[str] = []
    pytest_exit = 1
    collected: list[str] = []
    executions: list[ExecutionRecord] = []
    cpu = unavailable_cpu()
    junit: JunitRecord | None = None
    assigned_count = 0
    collection_sha = ""
    try:
        collected = collect_node_ids()
        if not collected:
            raise RuntimeError("collection returned no tests")
        durations = load_durations(durations_path)
        assigned = assign_shards(collected, durations, shard_count)[index]
        if not assigned:
            raise RuntimeError(f"shard {index} was assigned no tests")
        assigned_count = len(assigned)
        collection_sha = collection_hash(collected)
        shard_file = results_dir / "shard-nodeids.txt"
        record_path = results_dir / "execution.json"
        junit_path = results_dir / "pytest.xml"
        rusage_path = results_dir / "rusage.txt"
        shard_file.write_text("\n".join(assigned) + "\n", encoding="utf-8")
        pytest_exit, cpu = run_timed(
            shard_pytest_command(shard_file, record_path, junit_path),
            rusage_path,
        )
        if not record_path.is_file():
            raise RuntimeError("execution record was not written")
        record_hash, record_count, executions = _execution_records(
            json.loads(record_path.read_text(encoding="utf-8"))
        )
        if record_hash != collection_sha or record_count != len(collected):
            problems.append("running collection does not match the assignment collection")
        if junit_path.is_file():
            junit = junit_record(junit_path)
            identities = junit_identities(junit_path)
        else:
            identities = []
            problems.append("junit file was not written")
        executed = [row["nodeid"] for row in executions]
        if Counter(executed) != Counter(assigned):
            problems.append("executed node ids are not the assigned shard")
        for row in executions:
            problem = execution_problem(row)
            if problem is not None:
                problems.append(f"{row['nodeid']} {problem}")
        expected_identities = [junit_identity(node_id) for node_id in executed]
        if Counter(expected_identities) != Counter(identities):
            problems.append("junit identities do not match executed node ids")
        if junit is not None:
            subtests = sum(row["subtest_calls"] for row in executions)
            if junit["tests_attr"] != len(executions) + subtests:
                problems.append("junit tests attribute does not match executions plus subtests")
            if pytest_exit == 0 and (junit["failures"] != 0 or junit["errors"] != 0):
                problems.append("junit recorded failures")
    except Exception as exc:
        problems.append(exc.__class__.__name__ + ": " + str(exc).splitlines()[0][:300])
        pytest_exit = 1
    if problems and pytest_exit == 0:
        pytest_exit = 1
    manifest = ShardManifest(
        format=1,
        shard_index=index,
        shard_count=shard_count,
        nproc=cpu_count(),
        pytest_exit=pytest_exit,
        collection_sha256=collection_sha,
        collected_count=len(collected),
        assigned_count=assigned_count,
        problems=problems,
        cpu=cpu,
        junit=junit,
        executions=executions,
    )
    (results_dir / "shard-manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    elapsed = cpu["elapsed_seconds"]
    user = cpu["user_seconds"]
    system = cpu["system_seconds"]
    sys.stdout.write(
        f"shard {index}/{shard_count} assigned {assigned_count} of {len(collected)} "
        f"pytest_exit {pytest_exit} nproc {cpu_count()} "
        f"elapsed {elapsed} user {user} system {system}\n"
    )
    for problem in problems:
        sys.stdout.write(f"problem: {problem}\n")
    return pytest_exit


def command_prerequisites(needs_json: str, *, event_name: str, draft_flag: str) -> int:
    try:
        needs = json.loads(needs_json)
    except json.JSONDecodeError:
        sys.stdout.write("needs JSON is not valid\n")
        return 1
    problems = prerequisite_problems(needs, event_name=event_name, draft_flag=draft_flag)
    if problems:
        for problem in problems:
            sys.stdout.write(problem + "\n")
        return 1
    sys.stdout.write("prerequisites succeeded\n")
    return 0


def _load_artifact_shards(artifacts_dir: Path) -> list[tuple[ShardManifest, list[tuple[str, str]]]]:
    loaded: list[tuple[ShardManifest, list[tuple[str, str]]]] = []
    for manifest_path in sorted(artifacts_dir.glob("pytest-durations-shard-*/shard-manifest.json")):
        directory = manifest_path.parent
        prefix = "pytest-durations-shard-"
        suffix = directory.name[len(prefix) :]
        if not suffix.isdigit():
            raise ValueError(f"artifact name is not a shard index: {directory.name}")
        manifest = parse_manifest(json.loads(manifest_path.read_text(encoding="utf-8")))
        if manifest["shard_index"] != int(suffix):
            raise ValueError(
                f"artifact {directory.name} contains shard index {manifest['shard_index']}"
            )
        junit_path = directory / "pytest.xml"
        identities = junit_identities(junit_path) if junit_path.is_file() else []
        loaded.append((manifest, identities))
    return loaded


def command_coverage(artifacts_dir: Path, *, shard_count: int) -> int:
    collected = collect_node_ids()
    try:
        shards = _load_artifact_shards(artifacts_dir)
    except (OSError, ValueError, json.JSONDecodeError, ET.ParseError) as exc:
        sys.stdout.write(f"artifact load failed: {exc.__class__.__name__}: {exc}\n")
        return 1
    problems = coverage_problems(collected, shards, shard_count=shard_count)
    summary = accounting([manifest for manifest, _identities in shards])
    sys.stdout.write("accounting " + json.dumps(summary, sort_keys=True) + "\n")
    sys.stdout.write(
        "elapsed_wait is the workflow wall clock, dominated by the slowest shard. "
        "shard_pytest_elapsed_sum_seconds adds runner time and is not the wait. "
        "cpu_seconds is process-tree user plus system, not billed minutes.\n"
    )
    if problems:
        for problem in problems[:30]:
            sys.stdout.write(problem + "\n")
        if len(problems) > 30:
            sys.stdout.write(f"{len(problems) - 30} more problems\n")
        return 1
    sys.stdout.write(f"coverage exact for {len(collected)} collected tests\n")
    return 0


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="ci_gate")
    subparsers = parser.add_subparsers(dest="command", required=True)

    plan = subparsers.add_parser("plan")
    plan.add_argument("--durations", type=Path, default=WEIGHTS_PATH)
    plan.add_argument("--workers", type=_positive_int, default=WORKERS_PER_SHARD)
    plan.add_argument("--shard-count", type=_positive_int, default=SHARD_COUNT)

    importer = subparsers.add_parser("import-durations")
    importer.add_argument("--junit", type=Path, required=True)
    importer.add_argument("--out", type=Path, required=True)
    importer.add_argument("--source-run", default=SOURCE_RUN)
    importer.add_argument("--source-commit", default=SOURCE_COMMIT)

    run_shard = subparsers.add_parser("run-shard")
    run_shard.add_argument("--index", type=int, required=True)
    run_shard.add_argument("--count", type=_positive_int, required=True)
    run_shard.add_argument("--durations", type=Path, default=WEIGHTS_PATH)
    run_shard.add_argument("--results-dir", type=Path, required=True)

    prerequisites = subparsers.add_parser("prerequisites")
    prerequisites.add_argument("--needs-json", required=True)
    prerequisites.add_argument("--event-name", required=True)
    prerequisites.add_argument("--draft", default="")

    coverage = subparsers.add_parser("coverage")
    coverage.add_argument("--artifacts", type=Path, required=True)
    coverage.add_argument("--shard-count", type=_positive_int, default=SHARD_COUNT)

    args = parser.parse_args(list(argv) if argv is not None else None)
    command = args.command
    if command == "plan":
        return command_plan(args.durations, workers=args.workers, shard_count=args.shard_count)
    if command == "import-durations":
        return command_import_durations(
            args.junit,
            args.out,
            source_run=args.source_run,
            source_commit=args.source_commit,
        )
    if command == "run-shard":
        return command_run_shard(
            index=args.index,
            shard_count=args.count,
            durations_path=args.durations,
            results_dir=args.results_dir,
        )
    if command == "prerequisites":
        return command_prerequisites(
            args.needs_json,
            event_name=args.event_name,
            draft_flag=args.draft,
        )
    if command == "coverage":
        return command_coverage(args.artifacts, shard_count=args.shard_count)
    return 2


if __name__ == "__main__":
    sys.exit(main())
