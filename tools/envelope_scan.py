"""Repo-side ADR-0031 envelope gate: scan commit/push envelopes for residency markers.

This is the hook-layer half of ADR-0031's "installed, integrity-checked
commit/push gates" production condition. It scans the *added lines* and
*staged paths* of a commit or push envelope for path-shaped residency
markers before the crossing happens. It is installed as the `pre-commit`
and `pre-push` hooks by `tools/install_envelope_hooks.py`; the focused
suite (`tests/test_envelope_hooks.py`) requires the installation and
byte-verifies the hook shims in every clone, so a clone without the gate
fails the standard verification battery.

Marker vocabulary: the path-shaped variants of the substrings every track
safety test scans for, plus an SSN-shaped number. Requiring a following
path segment keeps honest documentation that merely *quotes* a bare
marker (review records, the safety tests, this tool) from tripping the
gate while still catching any real path. A line may carry the literal
pragma ``envelope-scan: allow`` to declare a deliberate synthetic
occurrence; the pragma is visible in the diff a reviewer reads.

Exit status: 0 when the envelope is clean, 1 on any finding.
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from collections.abc import Iterable, Iterator
from pathlib import Path

_SEGMENT = r"[\w.~$-]+"

MARKER_PATTERNS: tuple[re.Pattern[str], ...] = tuple(
    re.compile(pattern)
    for pattern in (
        rf"/Users/{_SEGMENT}",
        rf"/private/{_SEGMENT}",
        rf"local-data/{_SEGMENT}",
        rf"uploads/{_SEGMENT}",
        rf"generated/user/{_SEGMENT}",
        r"\b\d{3}-\d{2}-\d{4}\b",
    )
)

PRAGMA = "envelope-scan: allow"

SURFACES = ("pre-commit", "pre-push")


def _git(args: list[str]) -> str:
    return subprocess.run(
        ["git", *args], check=True, capture_output=True, text=True
    ).stdout


def scan_lines(lines: Iterable[tuple[str, str]]) -> list[str]:
    """Scan (origin, text) pairs; return one finding per offending line."""
    findings: list[str] = []
    for origin, text in lines:
        if PRAGMA in text:
            continue
        for pattern in MARKER_PATTERNS:
            match = pattern.search(text)
            if match is not None:
                findings.append(
                    f"{origin}: forbidden residency marker {match.group(0)!r}"
                )
                break
    return findings


def _added_lines(diff_text: str) -> Iterator[tuple[str, str]]:
    current = "<unknown>"
    for line in diff_text.splitlines():
        if line.startswith("+++ b/"):
            current = line[len("+++ b/") :]
        elif line.startswith("+") and not line.startswith("+++"):
            yield current, line[1:]


def staged_findings() -> list[str]:
    diff = _git(["diff", "--cached", "-U0", "--no-color"])
    findings = scan_lines(_added_lines(diff))
    names = _git(["diff", "--cached", "--name-only"]).splitlines()
    findings.extend(scan_lines(("staged path", name) for name in names))
    return findings


def range_findings(rev_range: str) -> list[str]:
    diff = _git(["diff", "-U0", "--no-color", rev_range])
    return scan_lines(_added_lines(diff))


def push_findings(stdin_text: str) -> list[str]:
    """Scan every outgoing ref update git reports on the pre-push stdin."""
    findings: list[str] = []
    for raw in stdin_text.splitlines():
        parts = raw.split()
        if len(parts) != 4:
            continue
        _local_ref, local_sha, _remote_ref, remote_sha = parts
        if set(local_sha) == {"0"}:
            continue  # ref deletion pushes no content
        if set(remote_sha) == {"0"}:
            # New remote ref: scan every commit not already on a remote.
            revs = _git(["rev-list", local_sha, "--not", "--remotes"]).split()
            for rev in revs:
                diff = _git(["show", rev, "-U0", "--no-color", "--format="])
                findings.extend(scan_lines(_added_lines(diff)))
        else:
            findings.extend(range_findings(f"{remote_sha}..{local_sha}"))
    return findings


def expected_hook_bytes(surface: str) -> bytes:
    """The exact shim the installer writes and the suite byte-verifies."""
    mode = "--staged" if surface == "pre-commit" else "--push"
    return (
        "#!/bin/sh\n"
        f"# attestory ADR-0031 repo envelope gate ({surface})\n"
        "# installed by tools/install_envelope_hooks.py; do not edit —\n"
        "# tests/test_envelope_hooks.py byte-verifies this shim.\n"
        f"exec python3 tools/envelope_scan.py {mode}\n"
    ).encode("utf-8")


def hooks_dir() -> Path:
    out = _git(["rev-parse", "--git-path", "hooks"]).strip()
    path = Path(out)
    return path if path.is_absolute() else (Path.cwd() / path).resolve()


def verify_hooks() -> list[str]:
    findings: list[str] = []
    directory = hooks_dir()
    for surface in SURFACES:
        hook = directory / surface
        if not hook.exists():
            findings.append(f"{surface} envelope gate is not installed")
        elif hook.read_bytes() != expected_hook_bytes(surface):
            findings.append(f"{surface} envelope gate does not match the committed gate")
        elif not os.access(hook, os.X_OK):
            findings.append(f"{surface} envelope gate is not executable")
    return findings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--staged", action="store_true", help="scan the staged commit envelope")
    group.add_argument("--push", action="store_true", help="scan pre-push ref updates from stdin")
    group.add_argument("--range", dest="rev_range", help="scan an explicit A..B diff range")
    group.add_argument("--verify", action="store_true", help="verify the installed hook shims")
    args = parser.parse_args(argv)

    if args.verify:
        problems = verify_hooks()
        if problems:
            print("envelope gate: NOT installed")
            for problem in problems:
                print(f"  - {problem}")
            print("remedy: python3 tools/install_envelope_hooks.py")
            return 1
        print("envelope gate: installed and verified")
        return 0

    if args.staged:
        findings = staged_findings()
        surface = "commit"
    elif args.push:
        findings = push_findings(sys.stdin.read())
        surface = "push"
    else:
        findings = range_findings(args.rev_range)
        surface = f"range {args.rev_range}"

    if findings:
        print(f"envelope gate: {surface} refused — residency marker in the envelope")
        for finding in findings:
            print(f"  - {finding}")
        print(f"({PRAGMA!r} on the line declares a deliberate synthetic occurrence)")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
