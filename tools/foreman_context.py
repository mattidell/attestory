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
PHASE_STATE_PATH = "docs/phase-state.md"


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
    format is read through here, so `current_prompt` and `deep_reads` cannot
    disagree about whether an anchor is spellable."""
    return target.split("#", 1)[0]


RATIFIED_REF = "origin/main"
TRACK_STATE = re.compile(r"^track-(\d+)$")
FULL_OBJECT_ID = re.compile(r"^[0-9a-f]{40}$")

# Each lifecycle state implies two facts about the ratified record. Both are
# file-presence questions, because the two artifacts that mark a milestone's
# boundaries — its plan and its retrospective — reach `main` in the merges that
# *are* those boundaries. A declared state that disagrees with the ratified
# record is the beginning/end confusion this table exists to catch.
#
#   state       plan on origin/main   retrospective on origin/main
#   planning    no                    (not yet named)
#   planned     yes                   no
#   track-N     yes                   no
#   closing     yes                   no
#   closed      yes                   yes
STATE_EXPECTATIONS = {
    "planning": (False, None),
    "planned": (True, False),
    "closing": (True, False),
    "closed": (True, True),
}
NEXT_TRANSITION = {
    "planning": "owner merges the plan PR, which moves this milestone to `planned`",
    "planned": "start the milestone's first track",
    "closing": "owner merges the closing PR, which closes this milestone",
    "closed": "this milestone is closed — the next action is selecting a new milestone",
}


def milestone_state_of(metadata: dict[str, Any], path: str) -> str:
    state = required_string(metadata, "milestone_state", path)
    if state not in STATE_EXPECTATIONS and not TRACK_STATE.match(state):
        allowed = ", ".join(sorted(STATE_EXPECTATIONS)) + ", track-<n>"
        raise ContextError(f"{path} milestone_state {state!r} is not one of: {allowed}")
    return state


def resolve_milestone_state(
    repository: GitRepository, plan: LoadedDocument, metadata_path: str
) -> dict[str, Any]:
    """Check the plan's declared lifecycle state against the ratified record.

    Returns the state plus the checks that corroborated it. Raises when the
    declaration and `origin/main` disagree: a foreman resuming into a tree whose
    plan PR merged (or whose closing PR merged) an hour ago must be told, not
    left to infer it from a status sentence written before the merge.
    """
    state = milestone_state_of(plan.metadata, plan.path)
    track = TRACK_STATE.match(state)
    expect_plan, expect_retrospective = (True, False) if track else STATE_EXPECTATIONS[state]

    raw_retrospective = plan.metadata.get("retrospective")
    if raw_retrospective is None and state in {"closing", "closed"}:
        # The closing unit is the retrospective's merge, so its path is known as
        # soon as the milestone starts closing. Requiring it here is what makes
        # the end-of-milestone transition mechanically checkable.
        raise ContextError(f"{plan.path} milestone_state {state!r} requires a 'retrospective' path")
    retrospective = (
        require_relative_path(str(raw_retrospective), f"{plan.path} metadata 'retrospective'")
        if raw_retrospective
        else None
    )

    ratified = repository.resolve_optional(RATIFIED_REF)
    if ratified is None:
        return {
            "state": state,
            "next_transition": next_transition(state, track),
            "ratified_ref": None,
            "checks": [],
            "note": f"{RATIFIED_REF} is unavailable — state is declared but NOT corroborated",
        }

    checks: list[dict[str, Any]] = [
        corroborate("plan on origin/main", repository, ratified, plan.path, expect_plan, state)
    ]
    if retrospective is not None and expect_retrospective is not None:
        checks.append(
            corroborate(
                "retrospective on origin/main",
                repository,
                ratified,
                retrospective,
                expect_retrospective,
                state,
            )
        )
    return {
        "state": state,
        "next_transition": next_transition(state, track),
        "ratified_ref": ratified,
        "checks": checks,
        "note": None,
    }


def corroborate(
    label: str,
    repository: GitRepository,
    ratified: str,
    path: str,
    expected: bool,
    state: str,
) -> dict[str, Any]:
    actual = repository.path_exists_at(ratified, path)
    if actual != expected:
        raise ContextError(
            f"milestone_state {state!r} contradicts the ratified record: it requires "
            f"{path} to be {'present on' if expected else 'absent from'} {RATIFIED_REF}, "
            f"but it is {'present' if actual else 'absent'}. Either the state is stale "
            f"(a boundary PR merged) or the declaration is wrong — reconcile before acting."
        )
    return {"check": label, "path": path, "expected": expected, "actual": actual}


def divergence_report(repository: GitRepository, ratified: str | None) -> dict[str, Any] | None:
    """How far the working ref has drifted from the ratified record. This is the
    other half of the boundary problem: a plan can be honest about its state and
    still be read in a tree that predates the merge which changed it."""
    if ratified is None:
        return None
    head = repository.resolve_optional("HEAD")
    if head is None:
        return None
    behind, ahead = repository.divergence(ratified, head)
    return {"ref": RATIFIED_REF, "behind": behind, "ahead": ahead}


def next_transition(state: str, track: re.Match[str] | None) -> str:
    if track is not None:
        number = int(track.group(1))
        return f"complete Track {number}, then Track {number + 1} or the closing unit"
    return NEXT_TRANSITION[state]


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


def render_context(repository: GitRepository, ref: str) -> dict[str, Any]:
    commit = repository.commit_for_ref(ref)
    phase = load_document(repository, commit, PHASE_STATE_PATH)
    active_plan_path = required_path(phase.metadata, "active_plan", phase.path)
    raw_seat_path = phase.metadata.get("seat")
    if raw_seat_path is not None and not isinstance(raw_seat_path, str):
        raise ContextError(f"{phase.path} metadata 'seat' must be a string when present")
    seat_path = require_relative_path(raw_seat_path, f"{phase.path} metadata 'seat'") if raw_seat_path else None
    plan = load_document(repository, commit, active_plan_path)
    seat = load_document(repository, commit, seat_path) if seat_path else None

    topic = required_string(phase.metadata, "topic", phase.path)
    documents_to_compare = [plan]
    if seat is not None:
        documents_to_compare.append(seat)
    for document in documents_to_compare:
        actual_topic = required_string(document.metadata, "topic", document.path)
        if actual_topic != topic:
            raise ContextError(
                f"topic mismatch: {phase.path} names {topic!r}, "
                f"but {document.path} names {actual_topic!r}"
            )

    raw_plan_seat = plan.metadata.get("seat")
    if seat_path is None:
        if raw_plan_seat is not None:
            raise ContextError(f"seat mismatch: {plan.path} names a seat but {phase.path} does not")
    elif required_path(plan.metadata, "seat", plan.path) != seat_path:
        raise ContextError(f"seat mismatch: {plan.path} does not name {seat_path}")

    deep_reads = validate_deep_reads(repository, commit, plan.metadata, plan.path)
    current_prompt = required_string(phase.metadata, "current_prompt", phase.path)
    current_prompt_path = require_relative_path(
        path_of(current_prompt), f"{phase.path} metadata 'current_prompt'"
    )
    current_prompt_blob = repository.blob_for_path(commit, current_prompt_path)
    sources = [phase, plan]
    if seat is not None:
        sources.append(seat)
    seat_state: dict[str, Any] | None = None
    if seat is not None:
        seat_state = {
            "role": required_string(seat.metadata, "role", seat.path),
            "status": required_string(seat.metadata, "status", seat.path),
            "rung": required_string(seat.metadata, "rung", seat.path),
            "stop_conditions": required_strings(seat.metadata, "stop_conditions", seat.path),
        }
    source_documents = [{"path": item.path, "blob": item.blob} for item in sources]
    source_documents.append({"path": current_prompt_path, "blob": current_prompt_blob})
    milestone = resolve_milestone_state(repository, plan, plan.path)
    briefing_follow_up = validate_initial_briefing_follow_up(
        repository, plan, topic, milestone
    )
    worktree = repository.worktree_status()
    worktree["divergence"] = divergence_report(repository, milestone["ratified_ref"])
    drift = worktree["divergence"]
    head = repository.resolve_optional("HEAD")
    ratified = milestone["ratified_ref"]
    branch_tip_reachable = (
        repository.is_ancestor(head, ratified)
        if head is not None and ratified is not None
        else None
    )
    worktree["branch_tip_reachable_from_ratified"] = branch_tip_reachable
    worktree["spent"] = bool(
        worktree["branch"]
        and worktree["branch"] != "main"
        and drift is not None
        and drift["behind"] > 0
        and drift["ahead"] == 0
        and branch_tip_reachable
    )
    return {
        "version": 1,
        "source": {
            "selected_ref": ref,
            "commit": commit,
            "documents": source_documents,
        },
        "worktree": worktree,
        "milestone": milestone,
        "state": {
            "phase": required_string(phase.metadata, "phase", phase.path),
            "topic": topic,
            "active_plan": active_plan_path,
            "plan_status": required_string(plan.metadata, "status", plan.path),
            "status": required_string(phase.metadata, "status", phase.path),
            "current_role": required_string(phase.metadata, "current_role", phase.path),
            "current_prompt": current_prompt,
            "initial_briefing_follow_up": briefing_follow_up is not None,
            "scope": required_strings(plan.metadata, "scope", plan.path),
            "non_goals": required_strings(plan.metadata, "non_goals", plan.path),
            "seat": seat_state,
        },
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

    if milestone["ratified_ref"] is None:
        corroboration = milestone["note"]
    else:
        corroboration = f"corroborated against `{RATIFIED_REF}` @ `{milestone['ratified_ref'][:10]}`"

    lines = [
        "# Foreman context capsule (advisory)",
        "",
        f"- Source: `{source['selected_ref']}` → `{source['commit']}`",
        worktree_line,
        f"- Active: {state['phase']} / `{state['topic']}` ({state['plan_status']})",
        f"- Milestone state: **{milestone['state']}** — {corroboration}",
        f"- Next transition: {milestone['next_transition']}",
    ]
    seat = state["seat"]
    if seat is not None:
        lines.append(f"- Seat: `{seat['role']}` — {seat['status']}; rung: {seat['rung']}")
    lines.extend([
        f"- Current role: {state['current_role']}",
        f"- Current prompt: `{state['current_prompt']}`",
    ])
    if state["initial_briefing_follow_up"]:
        lines.append(
            "- Initial briefing follow-up: **available** — run "
            "`python3 tools/foreman_context_followup.py --ref "
            f"{source['selected_ref']} --format markdown`"
        )
    else:
        lines.append("- Initial briefing follow-up: none")
    if milestone["state"] == "closed":
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
    else:
        lines.extend(["", "## Read in full before acting", ""])
    for action, targets in capsule["deep_reads"].items():
        lines.append(f"- `{action}`: {', '.join(f'`{target}`' for target in targets)}")
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
        help="skip the automatic `git fetch origin` (offline runs; corroboration then uses last-known refs)",
    )
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    arguments = parse_arguments(sys.argv[1:] if argv is None else argv)
    repository = GitRepository(Path(arguments.repo).resolve())
    # Fetch before reading. The capsule's boundary checks compare a declared
    # milestone state against `origin/main`, and a stale `origin/main` would
    # confirm exactly the outdated picture those checks exist to catch. A failed
    # fetch is not fatal — it degrades to last-known refs, which the capsule says.
    if not arguments.no_fetch:
        repository.fetch()
    try:
        capsule = render_context(repository, arguments.ref)
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
