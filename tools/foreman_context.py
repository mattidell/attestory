"""Render a validated, advisory foreman context capsule from one Git ref."""

from __future__ import annotations

import argparse
import json
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
            target_path = require_relative_path(target.split("#", 1)[0], f"{path} deep read {target!r}")
            repository.blob_for_path(commit, target_path)
        validated[action] = list(targets)
    return validated


def render_context(repository: GitRepository, ref: str) -> dict[str, Any]:
    commit = repository.commit_for_ref(ref)
    phase = load_document(repository, commit, PHASE_STATE_PATH)
    active_plan_path = required_path(phase.metadata, "active_plan", phase.path)
    handoff_path = required_path(phase.metadata, "handoff", phase.path)
    raw_seat_path = phase.metadata.get("seat")
    if raw_seat_path is not None and not isinstance(raw_seat_path, str):
        raise ContextError(f"{phase.path} metadata 'seat' must be a string when present")
    seat_path = require_relative_path(raw_seat_path, f"{phase.path} metadata 'seat'") if raw_seat_path else None
    handoff = load_document(repository, commit, handoff_path)
    plan = load_document(repository, commit, active_plan_path)
    seat = load_document(repository, commit, seat_path) if seat_path else None

    topic = required_string(phase.metadata, "topic", phase.path)
    documents_to_compare = [handoff, plan]
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
    current_prompt = required_path(handoff.metadata, "current_prompt", handoff.path)
    current_prompt_blob = repository.blob_for_path(commit, current_prompt)
    sources = [phase, handoff, plan]
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
    source_documents.append({"path": current_prompt, "blob": current_prompt_blob})
    return {
        "version": 1,
        "source": {
            "selected_ref": ref,
            "commit": commit,
            "documents": source_documents,
        },
        "worktree": repository.worktree_status(),
        "state": {
            "phase": required_string(phase.metadata, "phase", phase.path),
            "topic": topic,
            "plan_status": required_string(plan.metadata, "status", plan.path),
            "handoff_status": required_string(handoff.metadata, "status", handoff.path),
            "current_role": required_string(handoff.metadata, "current_role", handoff.path),
            "current_prompt": current_prompt,
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
    lines = [
        "# Foreman context capsule (advisory)",
        "",
        f"- Source: `{source['selected_ref']}` → `{source['commit']}`",
        f"- Worktree: branch `{worktree['branch'] or 'detached'}`; dirty: `{worktree['dirty']}`",
        f"- Active: {state['phase']} / `{state['topic']}` ({state['plan_status']})",
        f"- Current role: {state['current_role']}",
        f"- Current prompt: `{state['current_prompt']}`",
        "",
        "## Read in full before acting",
        "",
    ]
    seat = state["seat"]
    if seat is not None:
        lines.insert(5, f"- Seat: `{seat['role']}` — {seat['status']}; rung: {seat['rung']}")
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
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    arguments = parse_arguments(sys.argv[1:] if argv is None else argv)
    try:
        capsule = render_context(GitRepository(Path(arguments.repo).resolve()), arguments.ref)
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
