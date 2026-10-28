"""Each CI checkout that executes the suite installs the envelope hooks first.

The shard jobs do not share a checkout with precheck. The clone gate in
tests/test_envelope_hooks.py fails when those hooks are absent. This module
checks the workflow text. It does not collect or run the suite.
"""

from __future__ import annotations

import re
import unittest
from pathlib import Path

WORKFLOW = Path(__file__).resolve().parents[1] / ".github" / "workflows" / "ci.yml"
INSTALL = "python3 tools/install_envelope_hooks.py"
_JOB = re.compile(r"^  ([A-Za-z0-9_-]+):\s*$")
_RUN = re.compile(r"^(\s*)run:\s*(.*)$")
_SUITE = re.compile(r"(^|[|&;])\s*(python3?\s+-m\s+)?pytest(\s|$)")
_BLOCK = {"|", ">", "|-", ">-", "|+", ">+"}


def workflow_jobs(workflow: str) -> dict[str, str]:
    """Return each job body, in file order, excluding the ``jobs:`` key."""
    lines = workflow.splitlines()
    try:
        start = lines.index("jobs:") + 1
    except ValueError as exc:
        raise ValueError("workflow has no jobs") from exc
    jobs: dict[str, str] = {}
    name: str | None = None
    body: list[str] = []
    for line in lines[start:]:
        match = _JOB.match(line)
        if match:
            if name is not None:
                jobs[name] = "\n".join(body)
            name = match.group(1)
            body = []
            continue
        if name is not None:
            body.append(line)
    if name is not None:
        jobs[name] = "\n".join(body)
    return jobs


def run_scripts(job_body: str) -> list[str]:
    """Return ``run`` scripts in the order the job lists them."""
    lines = job_body.splitlines()
    scripts: list[str] = []
    index = 0
    while index < len(lines):
        match = _RUN.match(lines[index])
        if match is None:
            index += 1
            continue
        indent = len(match.group(1))
        rest = match.group(2).strip()
        if rest in _BLOCK or rest == "":
            block: list[str] = []
            index += 1
            while index < len(lines):
                nxt = lines[index]
                if nxt.strip() == "":
                    block.append("")
                    index += 1
                    continue
                if len(nxt) - len(nxt.lstrip(" ")) <= indent:
                    break
                block.append(nxt.strip())
                index += 1
            scripts.append("\n".join(block))
            continue
        scripts.append(rest)
        index += 1
    return scripts


def _code(line: str) -> str:
    return line.split("#", 1)[0].strip()


def executes_suite(line: str) -> bool:
    """True when a shell line runs pytest or one full-suite shard."""
    code = _code(line)
    if "tools.ci_gate run-shard" in code:
        return True
    return _SUITE.search(code) is not None


def suite_jobs(workflow: str) -> list[str]:
    """Job names that execute the suite, in file order."""
    found: list[str] = []
    for name, body in workflow_jobs(workflow).items():
        if any(executes_suite(line) for script in run_scripts(body) for line in script.splitlines()):
            found.append(name)
    return found


def jobs_missing_envelope_install(workflow: str) -> list[str]:
    """Suite jobs that reach pytest before the committed hook installer."""
    missing: list[str] = []
    for name, body in workflow_jobs(workflow).items():
        installed = False
        for script in run_scripts(body):
            for line in script.splitlines():
                code = _code(line)
                if INSTALL in code:
                    installed = True
                if executes_suite(line) and not installed:
                    missing.append(name)
                    installed = True
                    break
            else:
                continue
            break
    return missing


class ShardCheckoutTests(unittest.TestCase):
    def test_detector_requires_the_installer_before_pytest(self) -> None:
        present = """
jobs:
  suite-shard:
    steps:
      - name: Install ADR-0031 envelope git hooks (a proper clone has these)
        run: python3 tools/install_envelope_hooks.py
      - name: Run one full-suite shard
        run: python3 -m tools.ci_gate run-shard --index 0 --count 4
"""
        absent = present.replace(
            "      - name: Install ADR-0031 envelope git hooks (a proper clone has these)\n"
            "        run: python3 tools/install_envelope_hooks.py\n",
            "",
        )
        late = """
jobs:
  suite-shard:
    steps:
      - name: Run one full-suite shard
        run: python3 -m tools.ci_gate run-shard --index 0 --count 4
      - name: Install ADR-0031 envelope git hooks (a proper clone has these)
        run: python3 tools/install_envelope_hooks.py
"""
        mention = """
jobs:
  note:
    steps:
      - run: echo "the word pytest is not a command"
"""
        self.assertEqual(jobs_missing_envelope_install(present), [])
        self.assertEqual(suite_jobs(present), ["suite-shard"])
        self.assertEqual(jobs_missing_envelope_install(absent), ["suite-shard"])
        self.assertEqual(jobs_missing_envelope_install(late), ["suite-shard"])
        self.assertEqual(suite_jobs(mention), [])
        self.assertEqual(jobs_missing_envelope_install(mention), [])

    def test_committed_workflow_installs_hooks_before_every_suite_checkout(self) -> None:
        text = WORKFLOW.read_text(encoding="utf-8")
        self.assertEqual(suite_jobs(text), ["quick", "suite-shard"])
        self.assertEqual(jobs_missing_envelope_install(text), [])
        shard = workflow_jobs(text)["suite-shard"]
        scripts = run_scripts(shard)
        self.assertIn(INSTALL, scripts)
        shard_run = next(script for script in scripts if "tools.ci_gate run-shard" in script)
        self.assertLess(scripts.index(INSTALL), scripts.index(shard_run))
        self.assertNotIn("--deselect", shard_run)
        self.assertNotIn("\n-m ", "\n" + shard_run)
        self.assertNotIn("pytest -m", shard_run)
        self.assertIn("--count 4", shard_run)


if __name__ == "__main__":
    unittest.main()
