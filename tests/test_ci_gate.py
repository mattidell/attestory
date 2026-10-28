"""CI shard assignment, coverage, and the fail-closed verify decision.

These tests do not collect or run the suite. They use synthetic node ids,
including parametrized ids and unittest subtest tallies.
"""

import json
import tempfile
import unittest
from pathlib import Path
from typing import cast

from tools.ci_gate import (
    SHARD_COUNT,
    WEIGHTS_PATH,
    CpuRecord,
    ExecutionRecord,
    ExecutionTally,
    JunitRecord,
    ShardManifest,
    assign_shards,
    collection_hash,
    coverage_problems,
    default_weight,
    durations_from_junit,
    execution_problem,
    is_draft,
    junit_identity,
    observe,
    parse_elapsed,
    parse_gnu_time,
    partition_assignment,
    prerequisite_problems,
    read_node_id_lines,
    shard_pytest_command,
    simulated_wall,
)


def _execution(
    node_id: str,
    *,
    parent_calls: int = 1,
    subtest_calls: int = 0,
    setup_terminal: int = 0,
) -> ExecutionRecord:
    return ExecutionRecord(
        nodeid=node_id,
        parent_calls=parent_calls,
        subtest_calls=subtest_calls,
        setup_terminal=setup_terminal,
    )


def _cpu() -> CpuRecord:
    return CpuRecord(
        available=True,
        user_seconds=3.0,
        system_seconds=0.5,
        elapsed_seconds=2.0,
    )


def _junit(
    *,
    tests_attr: int,
    testcase_count: int,
    failures: int = 0,
    errors: int = 0,
    skipped: int = 0,
) -> JunitRecord:
    return JunitRecord(
        session_seconds=2.0,
        testcase_seconds=4.0,
        tests_attr=tests_attr,
        testcase_count=testcase_count,
        failures=failures,
        errors=errors,
        skipped=skipped,
    )


def _manifest(
    index: int,
    executions: list[ExecutionRecord],
    identities: list[tuple[str, str]],
    *,
    shard_count: int,
    collected: list[str],
    pytest_exit: int = 0,
    tests_attr: int | None = None,
) -> tuple[ShardManifest, list[tuple[str, str]]]:
    del identities
    subtests = sum(row["subtest_calls"] for row in executions)
    manifest = ShardManifest(
        format=1,
        shard_index=index,
        shard_count=shard_count,
        nproc=4,
        pytest_exit=pytest_exit,
        collection_sha256=collection_hash(collected),
        collected_count=len(collected),
        assigned_count=len(executions),
        problems=[],
        cpu=_cpu(),
        junit=_junit(
            tests_attr=len(executions) + subtests if tests_attr is None else tests_attr,
            testcase_count=len(executions),
        ),
        executions=executions,
    )
    rows = [junit_identity(row["nodeid"]) for row in executions]
    return manifest, rows


class GateDecisionTests(unittest.TestCase):
    def test_draft_push_ready_and_dependency_results(self) -> None:
        success = {"precheck": {"result": "success"}, "suite-shard": {"result": "success"}}
        self.assertEqual(prerequisite_problems(success, event_name="push", draft_flag=""), [])
        self.assertEqual(
            prerequisite_problems(success, event_name="pull_request", draft_flag="false"),
            [],
        )
        self.assertTrue(is_draft("pull_request", "true"))
        self.assertFalse(is_draft("push", "true"))
        draft = prerequisite_problems(success, event_name="pull_request", draft_flag="true")
        self.assertTrue(any("draft" in problem for problem in draft))
        skipped = {
            "precheck": {"result": "skipped"},
            "suite-shard": {"result": "skipped"},
        }
        problems = prerequisite_problems(skipped, event_name="push", draft_flag="false")
        self.assertIn("precheck result is skipped", problems)
        self.assertIn("suite-shard result is skipped", problems)
        failed = {"precheck": {"result": "failure"}, "suite-shard": {"result": "skipped"}}
        self.assertIn(
            "precheck result is failure",
            prerequisite_problems(failed, event_name="push", draft_flag=""),
        )
        cancelled = {"precheck": {"result": "success"}, "suite-shard": {"result": "cancelled"}}
        self.assertIn(
            "suite-shard result is cancelled",
            prerequisite_problems(cancelled, event_name="push", draft_flag=""),
        )
        self.assertIn(
            "suite-shard result is missing",
            prerequisite_problems({"precheck": {"result": "success"}}, event_name="push", draft_flag=""),
        )

    def test_elapsed_parser_accepts_gnu_time_layouts(self) -> None:
        self.assertAlmostEqual(parse_elapsed("0:03.50"), 3.5)
        self.assertAlmostEqual(parse_elapsed("12:00.00"), 720.0)
        self.assertAlmostEqual(parse_elapsed("1:02:03.25"), 3723.25)
        text = "\n".join(
            [
                "\tUser time (seconds): 12.50",
                "\tSystem time (seconds): 1.25",
                "\tElapsed (wall clock) time (h:mm:ss or m:ss): 0:04.00",
            ]
        )
        parsed = parse_gnu_time(text)
        self.assertTrue(parsed["available"])
        self.assertAlmostEqual(cast(float, parsed["user_seconds"]), 12.5)
        self.assertAlmostEqual(cast(float, parsed["system_seconds"]), 1.25)
        self.assertAlmostEqual(cast(float, parsed["elapsed_seconds"]), 4.0)
        self.assertFalse(parse_gnu_time("no fields")["available"])


class AssignmentTests(unittest.TestCase):
    def test_parametrized_ids_are_a_partition_and_heavy_tests_split(self) -> None:
        node_ids = [
            "tests/test_p.py::test_param[1]",
            "tests/test_p.py::test_param[2]",
            "tests/test_slow.py::Slow::test_a",
            "tests/test_slow.py::Slow::test_b",
            "tests/test_fast.py::test_c",
        ]
        durations = {
            "tests/test_slow.py::Slow::test_a": 10.0,
            "tests/test_slow.py::Slow::test_b": 9.0,
            "tests/test_p.py::test_param[1]": 1.0,
            "tests/test_p.py::test_param[2]": 1.0,
        }
        self.assertAlmostEqual(default_weight(durations), 5.0)
        shards = assign_shards(node_ids, durations, 2)
        flat = [node_id for shard in shards for node_id in shard]
        self.assertEqual(sorted(flat), sorted(node_ids))
        self.assertEqual(len(flat), len(set(flat)))
        homes = {node_id: index for index, shard in enumerate(shards) for node_id in shard}
        self.assertNotEqual(
            homes["tests/test_slow.py::Slow::test_a"],
            homes["tests/test_slow.py::Slow::test_b"],
        )
        self.assertIn("tests/test_p.py::test_param[1]", homes)
        self.assertIn("tests/test_p.py::test_param[2]", homes)
        self.assertGreater(simulated_wall(node_ids, durations, 2), 0.0)
        again = assign_shards(node_ids, durations, 2)
        self.assertEqual(shards, again)

    def test_identity_round_trip_and_duplicate_lines(self) -> None:
        self.assertEqual(
            junit_identity("tests/test_a.py::test_one"),
            ("tests.test_a", "test_one"),
        )
        self.assertEqual(
            junit_identity("tests/pkg/test_b.py::Outer::Inner::test_two[left]"),
            ("tests.pkg.test_b.Outer.Inner", "test_two[left]"),
        )
        with self.assertRaises(ValueError):
            read_node_id_lines("tests/test_a.py::test_one\ntests/test_a.py::test_one\n")
        selected, missing = partition_assignment(
            ["tests/test_a.py::test_one", "tests/test_a.py::test_two"],
            ["tests/test_a.py::test_one", "tests/test_a.py::test_missing"],
        )
        self.assertEqual(selected, ["tests/test_a.py::test_one"])
        self.assertEqual(missing, ["tests/test_a.py::test_missing"])

    def test_junit_join_reports_missing_and_stale_rows(self) -> None:
        junit = """<?xml version="1.0" encoding="utf-8"?>
<testsuite name="pytest" tests="2" failures="0" errors="0" skipped="0" time="3.5">
  <testcase classname="tests.test_a" name="test_one" time="1.5" />
  <testcase classname="tests.test_a" name="test_stale" time="2.0" />
</testsuite>
"""
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "junit.xml"
            path.write_text(junit, encoding="utf-8")
            matched, missing, stale, session = durations_from_junit(
                ["tests/test_a.py::test_one", "tests/test_a.py::test_new"],
                path,
            )
        self.assertEqual(matched, {"tests/test_a.py::test_one": 1.5})
        self.assertEqual(missing, ["tests/test_a.py::test_new"])
        self.assertEqual(stale, 1)
        self.assertAlmostEqual(session, 3.5)


class SubtestAndCoverageTests(unittest.TestCase):
    def test_subtest_reports_stay_on_the_parent(self) -> None:
        tallies: dict[str, ExecutionTally] = {}
        observe(tallies, nodeid="tests/test_s.py::Case::test_subs", when="setup", outcome="passed", subtest=False)
        observe(tallies, nodeid="tests/test_s.py::Case::test_subs", when="call", outcome="passed", subtest=True)
        observe(tallies, nodeid="tests/test_s.py::Case::test_subs", when="call", outcome="passed", subtest=True)
        observe(tallies, nodeid="tests/test_s.py::Case::test_subs", when="call", outcome="passed", subtest=False)
        observe(tallies, nodeid="tests/test_s.py::Case::test_skip", when="setup", outcome="skipped", subtest=False)
        parent = tallies["tests/test_s.py::Case::test_subs"].as_record("tests/test_s.py::Case::test_subs")
        skipped = tallies["tests/test_s.py::Case::test_skip"].as_record("tests/test_s.py::Case::test_skip")
        self.assertIsNone(execution_problem(parent))
        self.assertEqual(parent["subtest_calls"], 2)
        self.assertIsNone(execution_problem(skipped))
        self.assertEqual(
            execution_problem(_execution("tests/test_s.py::Case::test_subs", parent_calls=2)),
            "duplicate execution",
        )

    def test_coverage_accepts_a_partition_and_rejects_gaps(self) -> None:
        collected = [
            "tests/test_a.py::test_one",
            "tests/test_b.py::Case::test_two",
            "tests/test_p.py::test_param[1]",
        ]
        first, first_ids = _manifest(
            0,
            [
                _execution("tests/test_a.py::test_one"),
                _execution("tests/test_b.py::Case::test_two", subtest_calls=3),
            ],
            [],
            shard_count=2,
            collected=collected,
        )
        second, second_ids = _manifest(
            1,
            [_execution("tests/test_p.py::test_param[1]")],
            [],
            shard_count=2,
            collected=collected,
        )
        self.assertEqual(
            coverage_problems(collected, [(first, first_ids), (second, second_ids)], shard_count=2),
            [],
        )
        omitted, omitted_ids = _manifest(
            1,
            [],
            [],
            shard_count=2,
            collected=collected,
        )
        omitted["assigned_count"] = 0
        omitted["junit"] = _junit(tests_attr=0, testcase_count=0)
        problems = coverage_problems(collected, [(first, first_ids), (omitted, omitted_ids)], shard_count=2)
        self.assertTrue(any(problem.startswith("omissions") for problem in problems))
        duplicated, duplicated_ids = _manifest(
            1,
            [_execution("tests/test_a.py::test_one"), _execution("tests/test_p.py::test_param[1]")],
            [],
            shard_count=2,
            collected=collected,
        )
        problems = coverage_problems(
            collected, [(first, first_ids), (duplicated, duplicated_ids)], shard_count=2
        )
        self.assertTrue(any(problem.startswith("duplicate") for problem in problems))
        cancelled = dict(second)
        cancelled["pytest_exit"] = 1
        problems = coverage_problems(
            collected,
            [(first, first_ids), (cast(ShardManifest, cancelled), second_ids)],
            shard_count=2,
        )
        self.assertTrue(any("pytest_exit" in problem for problem in problems))
        only_one = coverage_problems(collected, [(first, first_ids)], shard_count=2)
        self.assertTrue(any("shard artifacts" in problem or "shard indexes" in problem for problem in only_one))


class WorkflowContractTests(unittest.TestCase):
    def test_workflow_keeps_verify_fail_closed_and_the_full_collection(self) -> None:
        text = Path(".github/workflows/ci.yml").read_text(encoding="utf-8")
        self.assertIn("\n  verify:\n    needs: [precheck, suite-shard]\n    if: always()\n", text)
        self.assertIn("Draft PR: the full suite has not run on this head.", text)
        self.assertIn("exit 1", text)
        matrix = "shard: [" + ", ".join(str(index) for index in range(SHARD_COUNT)) + "]"
        self.assertIn(matrix, text)
        self.assertIn(f"--count {SHARD_COUNT}", text)
        self.assertIn(f"--shard-count {SHARD_COUNT}", text)
        self.assertIn(str(WEIGHTS_PATH), text)
        self.assertIn('name: pytest-durations-shard-${{ matrix.shard }}', text)
        self.assertIn('python -m pytest -m "not live"', text)
        self.assertNotIn("pytest --junitxml", text)
        self.assertNotIn("--deselect", text)
        self.assertIn("cancel-in-progress: ${{ github.event_name == 'pull_request' }}", text)
        command = shard_pytest_command(Path("shard"), Path("record"), Path("junit"))
        marker_args = command[command.index("pytest") + 1 :]
        self.assertNotIn("-m", marker_args)
        self.assertNotIn("not live", marker_args)
        self.assertIn("--durations=50", command)
        self.assertIn("--junitxml", command)

    def test_duration_snapshot_is_synthetic_node_ids(self) -> None:
        raw = WEIGHTS_PATH.read_text(encoding="utf-8")
        self.assertNotIn("/Users/", raw)
        self.assertNotIn("/home/", raw)
        self.assertNotIn("MacBook", raw)
        data = json.loads(raw)
        self.assertEqual(data["format"], 1)
        self.assertEqual(data["source_run"], "40515157618")
        self.assertEqual(data["source_commit"], "a0bc250a67449a347f609550906f229fdd872daa")
        self.assertEqual(len(data["durations"]), 3544)
        self.assertAlmostEqual(sum(data["durations"].values()), 13059.8, delta=0.2)
        self.assertAlmostEqual(data["source_session_seconds"], 3298.893, delta=0.01)
        for node_id in data["durations"]:
            self.assertIn("::", node_id)
            self.assertFalse(node_id.startswith("/"))


if __name__ == "__main__":
    unittest.main()
