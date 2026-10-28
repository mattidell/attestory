"""Pin and compare the event's independent historical parameter baseline.

The historical test can pass or skip without a comparison, so preparation
also compares the bytes and fails closed before the shard runs.
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path
from typing import Sequence

PARAMETER_PATH = "packages/content/tax/2025/parameter.eic-table-2025.json"
REF_SPEC = "refs/heads/main:refs/remotes/origin/main"
LOCAL_REF = "refs/remotes/origin/main"
REMOTE_REF = "refs/heads/main"
_TARGETS = frozenset({"main", "main-ui"})


class HistoricalRefError(RuntimeError):
    """The shard cannot prove it will compare the ratified parameter."""


def target_branch(event_name: str, base_ref: str, ref_name: str) -> str:
    """Return the workflow target for an accounted event.

    Pull requests use ``github.base_ref``. ``github.ref_name`` on that
    event is the merge ref, such as ``226/merge``, and is not a line.
    Pushes use ``github.ref_name``.
    """
    if event_name == "pull_request":
        branch = base_ref
    elif event_name == "push":
        branch = ref_name
    else:
        raise HistoricalRefError(f"unexpected event {event_name!r}")
    if branch not in _TARGETS:
        raise HistoricalRefError(f"unexpected target branch {branch!r}")
    return branch


def historical_refspec(event_name: str, base_ref: str, ref_name: str) -> str:
    """Refspec for every accounted event. ``main-ui`` is not substituted."""
    target_branch(event_name, base_ref, ref_name)
    return REF_SPEC


def fetch_args(remote: str = "origin") -> list[str]:
    """Argv of the fetch. Creating a missing remote-tracking ref is not a force."""
    if remote == "" or remote.startswith("+") or remote.startswith("-"):
        raise HistoricalRefError("unexpected remote name")
    return [
        "git",
        "-c",
        "protocol.version=2",
        "fetch",
        "--depth=1",
        "--no-tags",
        "--no-recurse-submodules",
        remote,
        REF_SPEC,
    ]


def _reject_forced(args: Sequence[str]) -> None:
    for arg in args:
        if (
            arg == "--force"
            or arg.startswith("--force")
            or arg.startswith("+")
            or "main-ui" in arg
        ):
            raise HistoricalRefError("refusing to force or retarget the historical ref")


def _git(
    repo: Path,
    args: list[str],
    *,
    input_bytes: bytes | None = None,
) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(
        ["git", *args],
        cwd=repo,
        check=False,
        capture_output=True,
        input=input_bytes,
    )


def run_git(
    repo: Path, args: Sequence[str]
) -> subprocess.CompletedProcess[bytes]:
    """Run git in ``repo``. Callers use this for the bounded reproduction."""
    return _git(repo, list(args))


def _is_sha(value: str) -> bool:
    if len(value) not in {40, 64}:
        return False
    return all(character in "0123456789abcdef" for character in value)


def _one_sha(result: subprocess.CompletedProcess[bytes], label: str) -> str:
    if result.returncode != 0:
        raise HistoricalRefError(f"{label} does not resolve")
    text = result.stdout.decode("utf-8", "replace").strip()
    if not _is_sha(text):
        raise HistoricalRefError(f"{label} did not resolve to an object")
    return text


def _remote_main(repo: Path, remote: str) -> str:
    result = _git(repo, ["ls-remote", remote, REMOTE_REF])
    if result.returncode != 0:
        raise HistoricalRefError("could not read refs/heads/main from the remote")
    found: list[str] = []
    for line in result.stdout.decode("utf-8", "replace").splitlines():
        sha, separator, ref = line.partition("\t")
        if separator == "\t" and ref == REMOTE_REF and _is_sha(sha):
            found.append(sha)
    if len(found) != 1:
        raise HistoricalRefError("refs/heads/main did not resolve on the remote")
    return found[0]


def _universal(data: bytes) -> str:
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise HistoricalRefError("ratified parameter is not utf-8 text") from exc
    return text.replace("\r\n", "\n").replace("\r", "\n")


def fetch_historical_main(repo: Path, *, remote: str = "origin") -> None:
    args = fetch_args(remote)
    _reject_forced(args)
    result = subprocess.run(args, cwd=repo, check=False, capture_output=True)
    if result.returncode != 0:
        raise HistoricalRefError(
            f"fetch of {REF_SPEC} failed with status {result.returncode}"
        )


def verify_historical_parameter(repo: Path, *, remote: str = "origin", expected: str | None = None) -> str:
    """Return the blob id at ``refs/heads/main`` for the parameter file.

    The ref must identify the selected baseline, and ``git show`` must read
    its nonempty blob. The worktree text must match, because the
    historical test skips when the assertion fails.
    """
    local = _one_sha(
        _git(repo, ["rev-parse", "--verify", f"{LOCAL_REF}^{{commit}}"]),
        LOCAL_REF,
    )
    remote_tip = expected if expected is not None else _remote_main(repo, remote)
    if local != remote_tip:
        raise HistoricalRefError(
            f"{LOCAL_REF} is {local}, remote {REMOTE_REF} is {remote_tip}"
        )
    blob = _one_sha(
        _git(repo, ["rev-parse", "--verify", f"{LOCAL_REF}:{PARAMETER_PATH}"]),
        f"{LOCAL_REF}:{PARAMETER_PATH}",
    )
    kind = _git(repo, ["cat-file", "-t", blob])
    if kind.returncode != 0 or kind.stdout.strip() != b"blob":
        raise HistoricalRefError("ratified parameter is not a blob")
    shown = _git(repo, ["show", f"origin/main:{PARAMETER_PATH}"])
    if shown.returncode != 0:
        raise HistoricalRefError("git show of the ratified parameter failed")
    if shown.stdout == b"":
        raise HistoricalRefError("ratified parameter is empty")
    hashed = _one_sha(
        _git(repo, ["hash-object", "--stdin"], input_bytes=shown.stdout),
        "git show bytes",
    )
    if hashed != blob:
        raise HistoricalRefError("git show bytes are not the blob at refs/heads/main")
    worktree = repo / PARAMETER_PATH
    if not worktree.is_file():
        raise HistoricalRefError("worktree parameter is absent")
    if _universal(worktree.read_bytes()) != _universal(shown.stdout):
        work_hash = _git(
            repo, ["hash-object", "--stdin"], input_bytes=worktree.read_bytes()
        )
        observed = work_hash.stdout.decode("utf-8", "replace").strip()
        raise HistoricalRefError(
            f"worktree parameter differs from refs/heads/main ({observed} != {blob})"
        )
    return blob


def prepare(
    repo: Path,
    *,
    event_name: str,
    base_ref: str,
    ref_name: str,
    remote: str = "origin",
    base_sha: str = "",
    before_sha: str = "",
    after_sha: str = "",
) -> str:
    """Fetch and verify. Return the ratified parameter blob id."""
    branch = target_branch(event_name, base_ref, ref_name)
    head = _one_sha(_git(repo, ["rev-parse", "HEAD^{commit}"]), "HEAD")
    existing = _git(repo, ["rev-parse", "--verify", LOCAL_REF])
    observed_main = ""
    if event_name == "pull_request":
        baseline = base_sha
    elif branch == "main":
        baseline = before_sha
        if not _is_sha(after_sha) or after_sha != head:
            raise HistoricalRefError("push checkout does not match event after")
    else:
        if not _is_sha(after_sha) or after_sha != head or not _is_sha(before_sha) or set(before_sha) == {"0"}:
            raise HistoricalRefError("invalid main-ui push revisions")
        observed_main = _remote_main(repo, remote)
        # When both lines converge, the main tip is the checkout itself.
        # Compare against the event's prior UI commit instead of itself.
        baseline = before_sha if observed_main == head else observed_main
    if not _is_sha(baseline) or set(baseline) == {"0"} or baseline == head:
        raise HistoricalRefError("missing or self-referential baseline")
    # Fetch the target history so ancestry can be proved even in a shallow checkout.
    shallow = _git(repo, ["rev-parse", "--is-shallow-repository"]).stdout.strip() == b"true"
    args = ["fetch", "--no-tags", "--refmap="]
    if shallow:
        args.append("--unshallow")
    args += [remote, f"refs/heads/{branch}"]
    if _git(repo, args).returncode != 0:
        raise HistoricalRefError("cannot fetch target history")
    target_tip = _one_sha(_git(repo, ["rev-parse", "FETCH_HEAD^{commit}"]), "target tip")
    if _git(repo, ["fetch", "--no-tags", remote, baseline]).returncode != 0:
        raise HistoricalRefError("cannot fetch event baseline")
    if event_name == "pull_request":
        first_parent = _one_sha(_git(repo, ["rev-parse", "HEAD^1"]), "merge first parent")
        _one_sha(_git(repo, ["rev-parse", "HEAD^2"]), "merge second parent")
        if first_parent != baseline:
            raise HistoricalRefError("PR checkout does not match recorded base")
        if _git(repo, ["merge-base", "--is-ancestor", baseline, target_tip]).returncode != 0:
            raise HistoricalRefError("PR base is not in target history")
    elif branch == "main":
        if _git(repo, ["merge-base", "--is-ancestor", baseline, head]).returncode != 0:
            raise HistoricalRefError("prior main is not an ancestor of push")
    else:
        if _git(repo, ["fetch", "--no-tags", remote, before_sha]).returncode != 0 or _git(repo, ["merge-base", "--is-ancestor", before_sha, head]).returncode != 0:
            raise HistoricalRefError("prior main-ui is not an ancestor of push")
        if _remote_main(repo, remote) != observed_main:
            raise HistoricalRefError("main moved during baseline fetch")
    if event_name == "push" and _git(repo, ["merge-base", "--is-ancestor", head, target_tip]).returncode != 0:
        raise HistoricalRefError("push is not in target history")
    if existing.returncode == 0:
        prior = _one_sha(existing, LOCAL_REF)
        if prior not in {baseline, head, target_tip}:
            raise HistoricalRefError("unexpected existing historical ref")
    if _git(repo, ["update-ref", LOCAL_REF, baseline]).returncode != 0:
        raise HistoricalRefError("cannot pin historical reference")
    return verify_historical_parameter(repo, remote=remote, expected=baseline)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="ci_historical_ref")
    subparsers = parser.add_subparsers(dest="command", required=True)
    prepare_command = subparsers.add_parser("prepare")
    prepare_command.add_argument("--repo", type=Path, default=Path("."))
    prepare_command.add_argument("--remote", default="origin")
    args = parser.parse_args(list(argv) if argv is not None else None)
    if args.command != "prepare":
        sys.stderr.write("historical ref: unknown command\n")
        return 1
    try:
        blob = prepare(
            args.repo,
            event_name=os.environ.get("CI_EVENT_NAME", ""),
            base_ref=os.environ.get("CI_BASE_REF", ""),
            ref_name=os.environ.get("CI_REF_NAME", ""),
            base_sha=os.environ.get("CI_BASE_SHA", ""),
            before_sha=os.environ.get("CI_BEFORE_SHA", ""),
            after_sha=os.environ.get("CI_AFTER_SHA", ""),
            remote=args.remote,
        )
    except HistoricalRefError as exc:
        sys.stderr.write(f"historical ref: {exc}\n")
        return 1
    sys.stdout.write(f"historical parameter {blob}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
