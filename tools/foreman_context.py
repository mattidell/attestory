"""Render a validated, advisory foreman context capsule from one Git ref."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any, Sequence


MARKER_OPEN = "<!-- foreman-context-v1\n"
MARKER_CLOSE = "\n-->"


class ContextError(RuntimeError):
    """A selected repository revision cannot produce a trustworthy capsule."""


@dataclass(frozen=True)
class LoadedDocument:
    path: str
    blob: str
    metadata: dict[str, Any]


class GitRepository:
    def __init__(self, root: Path) -> None:
        self.root = root

    def run(self, *args: str, strip: bool = True) -> str:
        result = subprocess.run(
            ["git", "-C", str(self.root), *args],
            check=False,
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            detail = result.stderr.strip() or result.stdout.strip() or "unknown Git failure"
            raise ContextError(detail)
        return result.stdout.strip() if strip else result.stdout

    def commit_for_ref(self, ref: str) -> str:
        if not ref or ref.startswith("-"):
            raise ContextError("selected ref must be a non-option Git revision")
        try:
            return self.run("rev-parse", "--verify", f"{ref}^{{commit}}")
        except ContextError as error:
            raise ContextError(f"selected ref {ref!r} cannot be resolved") from error

    def blob_for_path(self, commit: str, path: str) -> str:
        try:
            return self.run("rev-parse", "--verify", f"{commit}:{path}")
        except ContextError as error:
            raise ContextError(f"selected ref is missing required source {path}") from error

    def content_for_path(self, commit: str, path: str) -> str:
        try:
            return self.run("show", f"{commit}:{path}")
        except ContextError as error:
            raise ContextError(f"selected ref is missing readable source {path}") from error

    def worktree_status(self) -> dict[str, Any]:
        raw_status = self.run("status", "--porcelain=v1", strip=False)
        paths = [line[3:] for line in raw_status.splitlines() if len(line) >= 4]
        branch = self.run("branch", "--show-current") or None
        return {"branch": branch, "dirty": bool(paths), "dirty_paths": paths}

    def fetch(self) -> bool:
        """Best-effort refresh of `origin`. A repository with no remote, or a
        machine with no network, must still render a capsule — the caller
        degrades to last-known refs and says so."""
        try:
            self.run("fetch", "origin", "--prune")
            return True
        except ContextError:
            return False

    def resolve_optional(self, ref: str) -> str | None:
        try:
            return self.run("rev-parse", "--verify", f"{ref}^{{commit}}")
        except ContextError:
            return None

    def path_exists_at(self, commit: str, path: str) -> bool:
        try:
            self.run("rev-parse", "--verify", f"{commit}:{path}")
            return True
        except ContextError:
            return False

    def tracked_paths(self, commit: str, prefix: str) -> list[str]:
        raw = self.run("ls-tree", "-r", "--name-only", commit, "--", prefix)
        return [line for line in raw.splitlines() if line]

    def divergence(self, base: str, head: str) -> tuple[int, int]:
        """(behind, ahead) of `head` relative to `base`."""
        raw = self.run("rev-list", "--left-right", "--count", f"{base}...{head}")
        behind, ahead = raw.split()
        return int(behind), int(ahead)

    def is_ancestor(self, ancestor: str, descendant: str) -> bool:
        result = subprocess.run(
            ["git", "-C", str(self.root), "merge-base", "--is-ancestor", ancestor, descendant],
            check=False,
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            return True
        if result.returncode == 1:
            return False
        detail = result.stderr.strip() or result.stdout.strip() or "unknown Git failure"
        raise ContextError(detail)

    def remote_branches(self, remote: str = "origin") -> list[str]:
        """Remote-tracking branch names under `remote`, without the remote prefix."""
        raw = self.run(
            "for-each-ref", "--format=%(refname:strip=3)", f"refs/remotes/{remote}/"
        )
        return [line for line in raw.splitlines() if line and line != "HEAD"]


def require_relative_path(value: str, source: str) -> str:
    candidate = PurePosixPath(value)
    if not value or candidate.is_absolute() or ".." in candidate.parts:
        raise ContextError(f"{source} must name a repository-relative tracked path")
    return candidate.as_posix()


def parse_metadata(text: str, path: str) -> dict[str, Any]:
    if not text.startswith(MARKER_OPEN):
        raise ContextError(f"{path} is missing foreman-context-v1 front matter")
    end = text.find(MARKER_CLOSE, len(MARKER_OPEN))
    if end == -1:
        raise ContextError(f"{path} has unterminated foreman-context-v1 front matter")
    try:
        decoded = json.loads(text[len(MARKER_OPEN) : end])
    except json.JSONDecodeError as error:
        raise ContextError(f"{path} has invalid JSON front matter: {error.msg}") from error
    if not isinstance(decoded, dict) or decoded.get("version") != 1:
        raise ContextError(f"{path} must contain a version-1 metadata object")
    return decoded


def load_document(repository: GitRepository, commit: str, path: str) -> LoadedDocument:
    normalized = require_relative_path(path, "context source")
    blob = repository.blob_for_path(commit, normalized)
    return LoadedDocument(normalized, blob, parse_metadata(repository.content_for_path(commit, normalized), normalized))


def required_string(metadata: dict[str, Any], key: str, path: str) -> str:
    value = metadata.get(key)
    if not isinstance(value, str) or not value:
        raise ContextError(f"{path} metadata requires non-empty string {key!r}")
    return value


def required_strings(metadata: dict[str, Any], key: str, path: str) -> list[str]:
    value = metadata.get(key)
    if not isinstance(value, list) or not all(isinstance(item, str) and item for item in value):
        raise ContextError(f"{path} metadata requires string list {key!r}")
    return list(value)


def required_path(metadata: dict[str, Any], key: str, path: str) -> str:
    return require_relative_path(required_string(metadata, key, path), f"{path} metadata {key!r}")


def validate_deep_reads(
    repository: GitRepository, commit: str, metadata: dict[str, Any], path: str
) -> dict[str, list[str]]:
    raw = metadata.get("deep_reads")
    if not isinstance(raw, dict) or not raw:
        raise ContextError(f"{path} metadata requires non-empty object 'deep_reads'")
    validated: dict[str, list[str]] = {}
    for action, targets in raw.items():
        if not isinstance(action, str) or not action:
            raise ContextError(f"{path} deep-read action names must be non-empty strings")
        if not isinstance(targets, list) or not all(isinstance(target, str) and target for target in targets):
            raise ContextError(f"{path} deep-read action {action!r} must name a string list")
        for target in targets:
            target_path = require_relative_path(path_of(target), f"{path} deep read {target!r}")
            repository.blob_for_path(commit, target_path)
        validated[action] = list(targets)
    return validated


def path_of(target: str) -> str:
    """Drop a `#Heading` fragment. Pointers name a file and may name a section
    within it; only the file part addresses a blob. Every pointer in this
    format is read through here, so a charter and `deep_reads` cannot disagree
    about whether an anchor is spellable."""
    return target.split("#", 1)[0]


# The repository carries more than one ratified line: `main` for the derivation
# work and `main-ui` for the surface work. They are separate continuous records,
# and a milestone that closes on one never reaches the other. The divergence
# report therefore derives the target line from the checked-out work rather
# than assuming `origin/main`.
RATIFIED_LINE = re.compile(r"^main(-[0-9a-z]+)*$")
DEFAULT_RATIFIED_REF = "origin/main"
FULL_OBJECT_ID = re.compile(r"^[0-9a-f]{40}$")


def resolve_ratified_ref(repository: GitRepository, override: str | None = None) -> str:
    """Which ratified line the checked-out work belongs to.

    A unit branch does not say which line it was cut from, so ask the history.
    Among the ratified lines the remote carries, the one this work branched from
    is the one it has diverged from least: fewest commits on HEAD that the line
    does not already have. Ties — HEAD sitting on a line that another line has
    since built on top of — go to the line that is itself closest to HEAD, which
    is the more general of the two rather than the one that moved past it.

    Falls back to `origin/main` when nothing resolves, which keeps the behaviour
    of a single-line repository and a bare clone unchanged.
    """
    if override is not None:
        return override
    head = repository.resolve_optional("HEAD")
    if head is None:
        return DEFAULT_RATIFIED_REF
    candidates = [
        f"origin/{name}"
        for name in repository.remote_branches()
        if RATIFIED_LINE.match(name)
    ]
    ranked: list[tuple[int, int, str]] = []
    for candidate in candidates:
        if repository.resolve_optional(candidate) is None:
            continue
        behind, ahead = repository.divergence(candidate, head)
        ranked.append((ahead, behind, candidate))
    if not ranked:
        return DEFAULT_RATIFIED_REF
    return min(ranked)[2]

# A milestone's state is read from its plan, not declared beside it: a plan
# that names an existing retrospective is closed; any other plan is open. A
# separate state file had to be rewritten by every closeout, which is what made
# parallel milestones conflict on it.
NEXT_TRANSITION = {
    "open": "continue the milestone's next unfinished track, or its closing unit",
    "closed": "this milestone is closed — the next action is selecting a new milestone",
    "none": "no milestone is active on this branch — select one",
}
PLAN_GLOB_PREFIX = "docs/phases/"
PLAN_DIRECTORY = "/milestones/"
RETROSPECTIVES = "docs/milestone-retrospectives/"
RECENT_RETROSPECTIVES = 3


def plan_for_branch(repository: GitRepository, commit: str, branch: str | None) -> str | None:
    """The milestone plan a branch is working on, by name.

    Branches are `milestone/<milestone-key>-<purpose>` (or the same under
    `temp/`), and a plan is `docs/phases/<phase>/milestones/<milestone-key>.md`.
    The purpose suffix is free text, so the plan is the longest key that the
    branch name equals or extends with `-`.
    """
    if not branch:
        return None
    name = branch.removeprefix("temp/")
    if not name.startswith("milestone/"):
        return None
    rest = name.removeprefix("milestone/")
    best: tuple[int, str] | None = None
    for path in repository.tracked_paths(commit, PLAN_GLOB_PREFIX):
        if PLAN_DIRECTORY not in path or not path.endswith(".md"):
            continue
        key = PurePosixPath(path).stem
        if rest == key or rest.startswith(key + "-"):
            if best is None or len(key) > best[0]:
                best = (len(key), path)
    return best[1] if best else None


def recent_retrospectives(repository: GitRepository, commit: str) -> list[str]:
    paths = [
        path
        for path in repository.tracked_paths(commit, RETROSPECTIVES)
        if path.endswith(".md") and PurePosixPath(path).name[:4].isdigit()
    ]
    return sorted(paths)[-RECENT_RETROSPECTIVES:][::-1]


def resolve_milestone_state(
    repository: GitRepository,
    selected_commit: str,
    plan: LoadedDocument | None,
    ratified_ref: str = DEFAULT_RATIFIED_REF,
) -> dict[str, Any]:
    """Derive the selected commit's milestone state from its plan.

    The target line is reported separately through ratified_ref and the
    worktree divergence report; it cannot veto an honest prospective state
    merely because the milestone PR has not merged yet.
    """
    checks: list[dict[str, Any]] = []
    if plan is None:
        state = "none"
    else:
        checks.append(corroborate_selected(repository, selected_commit, plan.path))
        raw_retrospective = plan.metadata.get("retrospective")
        state = "open"
        if raw_retrospective is not None:
            retrospective = require_relative_path(
                str(raw_retrospective), f"{plan.path} metadata 'retrospective'"
            )
            checks.append(corroborate_selected(repository, selected_commit, retrospective))
            state = "closed"

    ratified = repository.resolve_optional(ratified_ref)
    return {
        "state": state,
        "next_transition": NEXT_TRANSITION[state],
        "ratified_ref": ratified,
        "ratified_line": ratified_ref,
        "checks": checks,
        "note": (
            None
            if ratified is not None
            else f"{ratified_ref} is unavailable — target-line comparison is unavailable"
        ),
    }


def corroborate_selected(repository: GitRepository, selected_commit: str, path: str) -> dict[str, Any]:
    actual = repository.path_exists_at(selected_commit, path)
    if not actual:
        raise ContextError(f"{path} is named by the active plan but absent from the selected commit")
    return {
        "check": "artifact in selected commit",
        "path": path,
        "expected": True,
        "actual": actual,
    }


def divergence_report(
    repository: GitRepository, ratified: str | None, ratified_ref: str = DEFAULT_RATIFIED_REF
) -> dict[str, Any] | None:
    """How far the working ref has drifted from the ratified record. This is the
    other half of the boundary problem: a plan can be honest about its state and
    still be read in a tree that predates the merge which changed it."""
    if ratified is None:
        return None
    head = repository.resolve_optional("HEAD")
    if head is None:
        return None
    behind, ahead = repository.divergence(ratified, head)
    return {"ref": ratified_ref, "behind": behind, "ahead": ahead}


def validate_initial_briefing_follow_up(
    repository: GitRepository,
    plan: LoadedDocument,
    topic: str,
    milestone: dict[str, Any],
) -> dict[str, Any] | None:
    """Validate the active plan's optional, temporary briefing supplement."""
    raw = plan.metadata.get("initial_briefing_follow_up")
    if raw is None:
        return None
    if milestone["state"] == "closed":
        raise ContextError(
            f"{plan.path} is closed but still carries 'initial_briefing_follow_up'; "
            "remove the temporary capsule in the closing unit"
        )
    if not isinstance(raw, dict):
        raise ContextError(f"{plan.path} metadata 'initial_briefing_follow_up' must be an object")
    expected_keys = {"version", "expires", "grounding_commit", "notes", "sources"}
    actual_keys = set(raw)
    if actual_keys != expected_keys:
        missing = sorted(expected_keys - actual_keys)
        extra = sorted(actual_keys - expected_keys)
        detail = []
        if missing:
            detail.append(f"missing {missing}")
        if extra:
            detail.append(f"unknown {extra}")
        raise ContextError(
            f"{plan.path} initial briefing follow-up has invalid keys: {', '.join(detail)}"
        )
    if raw["version"] != 1:
        raise ContextError(f"{plan.path} initial briefing follow-up must have version 1")
    if raw["expires"] != "milestone-close":
        raise ContextError(
            f"{plan.path} initial briefing follow-up must expire at 'milestone-close'"
        )
    grounding_commit = raw["grounding_commit"]
    if not isinstance(grounding_commit, str) or not FULL_OBJECT_ID.fullmatch(grounding_commit):
        raise ContextError(
            f"{plan.path} initial briefing follow-up requires a full grounding commit SHA"
        )
    if repository.commit_for_ref(grounding_commit) != grounding_commit:
        raise ContextError(
            f"{plan.path} initial briefing follow-up grounding commit is not canonical"
        )
    notes = raw["notes"]
    if not isinstance(notes, list) or not notes or not all(
        isinstance(note, str) and note.strip() for note in notes
    ):
        raise ContextError(
            f"{plan.path} initial briefing follow-up requires non-empty string notes"
        )
    raw_sources = raw["sources"]
    if not isinstance(raw_sources, list) or not raw_sources:
        raise ContextError(
            f"{plan.path} initial briefing follow-up requires at least one source"
        )
    sources: list[dict[str, str]] = []
    seen_paths: set[str] = set()
    for index, source in enumerate(raw_sources):
        label = f"{plan.path} initial briefing follow-up source {index}"
        if not isinstance(source, dict) or set(source) != {"path", "blob"}:
            raise ContextError(f"{label} must contain exactly 'path' and 'blob'")
        raw_path = source.get("path")
        if not isinstance(raw_path, str):
            raise ContextError(f"{label} requires a repository-relative path")
        path = require_relative_path(raw_path, label)
        blob = source.get("blob")
        if not isinstance(blob, str) or not FULL_OBJECT_ID.fullmatch(blob):
            raise ContextError(f"{label} requires a full blob SHA")
        if path in seen_paths:
            raise ContextError(f"{label} duplicates {path}")
        seen_paths.add(path)
        actual_blob = repository.blob_for_path(grounding_commit, path)
        if actual_blob != blob:
            raise ContextError(
                f"{label} blob mismatch: records {blob}, but "
                f"{grounding_commit}:{path} is {actual_blob}"
            )
        sources.append({"path": path, "blob": blob})
    return {
        "version": 1,
        "topic": topic,
        "expires": "milestone-close",
        "grounding_commit": grounding_commit,
        "notes": list(notes),
        "sources": sources,
    }


def render_context(
    repository: GitRepository,
    ref: str,
    ratified_ref: str | None = None,
    plan_path: str | None = None,
) -> dict[str, Any]:
    # Resolve the ratified line here rather than defaulting to `origin/main`.
    # This used to take a literal default, and a caller that forgot to pass one
    # got a confident answer against the wrong line: on the surface work, every
    # milestone looks unratified and the capsule refuses. That refusal reads as
    # "your branch is stale" when the branch is current, which is the most
    # expensive kind of wrong. Callers that know the line still pass it.
    if ratified_ref is None:
        ratified_ref = resolve_ratified_ref(repository)
    commit = repository.commit_for_ref(ref)
    worktree = repository.worktree_status()
    if plan_path is None:
        plan_path = plan_for_branch(repository, commit, worktree["branch"])
    plan = (
        load_document(repository, commit, require_relative_path(plan_path, "--plan"))
        if plan_path
        else None
    )

    milestone = resolve_milestone_state(repository, commit, plan, ratified_ref)
    worktree["divergence"] = divergence_report(
        repository, milestone["ratified_ref"], ratified_ref
    )
    drift = worktree["divergence"]
    head = repository.resolve_optional("HEAD")
    ratified = milestone["ratified_ref"]
    branch_tip_reachable = (
        repository.is_ancestor(head, ratified)
        if head is not None and ratified is not None
        else None
    )
    worktree["branch_tip_reachable_from_ratified"] = branch_tip_reachable
    # A branch is spent once its work is in the line it was cut from. Comparing
    # against the derived line, not the literal name "main", is what keeps this
    # from reading every `main-ui` checkout as a spent unit branch.
    worktree["spent"] = bool(
        worktree["branch"]
        and f"origin/{worktree['branch']}" != ratified_ref
        and drift is not None
        and drift["behind"] > 0
        and drift["ahead"] == 0
        and branch_tip_reachable
    )

    state: dict[str, Any] | None = None
    deep_reads: dict[str, list[str]] = {}
    documents: list[dict[str, str]] = []
    if plan is not None:
        topic = required_string(plan.metadata, "topic", plan.path)
        deep_reads = validate_deep_reads(repository, commit, plan.metadata, plan.path)
        briefing_follow_up = validate_initial_briefing_follow_up(
            repository, plan, topic, milestone
        )
        documents.append({"path": plan.path, "blob": plan.blob})
        state = {
            "phase": plan.metadata.get("phase") or PurePosixPath(plan.path).parts[2],
            "topic": topic,
            "active_plan": plan.path,
            "milestone_state": milestone["state"],
            "plan_status": required_string(plan.metadata, "status", plan.path),
            "initial_briefing_follow_up": briefing_follow_up is not None,
            "scope": required_strings(plan.metadata, "scope", plan.path),
            "non_goals": required_strings(plan.metadata, "non_goals", plan.path),
        }
    for path in recent_retrospectives(repository, commit):
        documents.append({"path": path, "blob": repository.blob_for_path(commit, path)})
    return {
        "version": 2,
        "source": {
            "selected_ref": ref,
            "commit": commit,
            "documents": documents,
        },
        "worktree": worktree,
        "milestone": milestone,
        "state": state,
        "deep_reads": deep_reads,
    }


def markdown_capsule(capsule: dict[str, Any]) -> str:
    source = capsule["source"]
    worktree = capsule["worktree"]
    state = capsule["state"]
    milestone = capsule["milestone"]

    drift = worktree["divergence"]
    worktree_line = f"- Worktree: branch `{worktree['branch'] or 'detached'}`; dirty: `{worktree['dirty']}`"
    if drift is not None:
        worktree_line += f"; {drift['behind']} behind / {drift['ahead']} ahead of `{drift['ref']}`"
    worktree_line += f"; spent: `{worktree['spent']}`"

    lines = [
        "# Foreman context capsule (advisory)",
        "",
        f"- Source: `{source['selected_ref']}` → `{source['commit']}`",
        worktree_line,
    ]
    if state is None:
        lines.append("- Active milestone: none on this branch")
    else:
        lines.append(
            f"- Active: {state['phase']} / `{state['topic']}` — `{state['active_plan']}`"
        )
        lines.append(f"- Plan status: {state['plan_status']}")
    lines.append(f"- Milestone state: **{milestone['state']}** (derived from the plan)")
    if milestone["ratified_ref"] is None:
        lines.append(f"- Note: {milestone['note']}")
    lines.append(f"- Next transition: {milestone['next_transition']}")
    if state is not None:
        if state["initial_briefing_follow_up"]:
            lines.append(
                "- Initial briefing follow-up: **available** — run "
                "`python3 tools/foreman_context_followup.py --ref "
                f"{source['selected_ref']} --format markdown`"
            )
        else:
            lines.append("- Initial briefing follow-up: none")
    if milestone["state"] == "open":
        lines.extend(["", "## Read in full before acting", ""])
    else:
        lines.extend([
            "",
            "## Initial briefing checkpoint",
            "",
            "Before loading follow-up context, briefly tell the owner what in this",
            "project position may need clarification or grounding, recommend the",
            "smallest useful retrieval, and stop.",
            "",
            "## Candidate follow-up context",
            "",
        ])
    for action, targets in capsule["deep_reads"].items():
        lines.append(f"- `{action}`: {', '.join(f'`{target}`' for target in targets)}")
    if state is None:
        for document in source["documents"]:
            lines.append(f"- recent retrospective: `{document['path']}`")
    lines.extend(["", "## Source blobs", ""])
    for document in source["documents"]:
        lines.append(f"- `{document['path']}` @ `{document['blob']}`")
    return "\n".join(lines) + "\n"


def parse_arguments(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ref", required=True, help="explicit Git revision to read")
    parser.add_argument("--repo", default=".", help="repository root (default: current directory)")
    parser.add_argument("--format", choices=("json", "markdown"), default="json")
    parser.add_argument(
        "--no-fetch",
        action="store_true",
        help="skip the automatic `git fetch origin` (offline runs use last-known target refs)",
    )
    parser.add_argument(
        "--plan",
        default=None,
        help="milestone plan to read (default: derived from the branch name)",
    )
    parser.add_argument(
        "--ratified-ref",
        default=None,
        help="target line for divergence reporting (default: derived from the checked-out work)",
    )
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    arguments = parse_arguments(sys.argv[1:] if argv is None else argv)
    repository = GitRepository(Path(arguments.repo).resolve())
    # Fetch before reading so target-line divergence is current. A failed fetch
    # is not fatal — it degrades to last-known refs, which the capsule says.
    if not arguments.no_fetch:
        repository.fetch()
    try:
        ratified_ref = resolve_ratified_ref(repository, arguments.ratified_ref)
        capsule = render_context(repository, arguments.ref, ratified_ref, arguments.plan)
    except ContextError as error:
        print(f"foreman context: {error}", file=sys.stderr)
        return 2
    if arguments.format == "json":
        print(json.dumps(capsule, indent=2, sort_keys=True))
    else:
        print(markdown_capsule(capsule), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
