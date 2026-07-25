"""Emit a role-scoped, anchor-aware Orientation Block for picking up the current
task — from any runner (Claude, Codex, Grok) via a plain bash call.

Given a Git ref, this resolves the active plan's `deep_reads` (a map of
action -> section-anchored paths), selects the ONE action for the requested role,
and inlines the current prompt/charter plus only the *cited sections* of each
deep-read source, all at one resolved commit. It deliberately does not flatten
every action or inline whole files — the plan already scopes and anchors reads,
and this tool honors that.

Because every byte comes from a named commit's blobs (not prose), it preserves
the builder/reviewer discipline "verify the capsule against Git, do not
reconstruct from handoff prose": the block prints the commit SHA to verify.

Portable: pure standard library; no runner-specific assumptions.

Usage:
  python3 tools/build_orientation_block.py --ref main --role builder
  python3 tools/build_orientation_block.py --ref main --action review
  python3 tools/build_orientation_block.py --ref main --role builder --manifest-only
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from tools.foreman_context import ContextError, GitRepository, render_context

# Which deep_reads action each role picks up. Extend as roles are added.
ROLE_ACTIONS = {"builder": "implementation", "reviewer": "review"}
DEFAULT_MAX_BYTES = 24_000  # per-section guard


def _heading_level(line: str) -> int:
    stripped = line.lstrip()
    if not stripped.startswith("#"):
        return 0
    return len(stripped) - len(stripped.lstrip("#"))


def _heading_text(line: str) -> str:
    return line.lstrip().lstrip("#").strip()


def _norm(text: str) -> str:
    return " ".join(text.split()).casefold()


def extract_section(content: str, anchor: str) -> tuple[str, bool]:
    """Return (section_text, found). A section runs from the matching heading to
    the next heading of the same or higher level. Match is normalized-exact, then
    substring. If not found, returns ("", False) so the caller can flag it."""
    target = _norm(anchor)
    lines = content.splitlines()
    start: int | None = None
    level: int | None = None
    for i, line in enumerate(lines):
        lvl = _heading_level(line)
        if lvl and _norm(_heading_text(line)) == target:
            start, level = i, lvl
            break
    if start is None:  # fall back to substring match
        for i, line in enumerate(lines):
            lvl = _heading_level(line)
            if lvl and target in _norm(_heading_text(line)):
                start, level = i, lvl
                break
    if start is None:
        return "", False
    end = len(lines)
    for j in range(start + 1, len(lines)):
        lvl = _heading_level(lines[j])
        if lvl and level is not None and lvl <= level:
            end = j
            break
    return "\n".join(lines[start:end]).strip(), True


def _cap(body: str, max_bytes: int) -> str:
    raw = body.encode("utf-8")
    if len(raw) <= max_bytes:
        return body
    return raw[:max_bytes].decode("utf-8", "ignore") + f"\n… [truncated at {max_bytes} bytes]"


def _resolve_action(capsule: dict[str, Any], role: str | None, action: str | None) -> str:
    available = list(capsule["deep_reads"])
    chosen = action or (ROLE_ACTIONS.get(role or "") if role else None)
    if not chosen:
        raise ContextError(
            f"role {role!r} has no mapped deep_reads action; pass --action explicitly. "
            f"Available actions: {', '.join(available)}"
        )
    if chosen not in capsule["deep_reads"]:
        raise ContextError(
            f"action {chosen!r} is not in this plan's deep_reads. Available: {', '.join(available)}"
        )
    return chosen


def build_block(
    repo: GitRepository, ref: str, role: str | None, action: str | None,
    max_bytes: int, manifest_only: bool,
) -> str:
    capsule = render_context(repo, ref)
    commit = capsule["source"]["commit"]
    state = capsule["state"]
    wt = capsule["worktree"]
    chosen = _resolve_action(capsule, role, action)

    # dedup by full target (path#anchor): the same file under two anchors is two
    # distinct sections and both are kept; an exact repeat is dropped.
    seen: set[str] = set()
    targets: list[str] = []
    for target in capsule["deep_reads"][chosen]:
        if target not in seen:
            seen.add(target)
            targets.append(target)

    out: list[str] = [
        f"# ORIENTATION BLOCK — {role or chosen} (preloaded; do not re-read these)",
        "",
        f"- Commit: `{commit}`  (verify this SHA against Git before acting)",
        f"- Branch: `{wt['branch'] or 'detached'}`; dirty: `{wt['dirty']}`",
        f"- Phase/topic: {state['phase']} / `{state['topic']}` ({state['plan_status']})",
        f"- Current role (per handoff): {state['current_role']}",
        f"- Deep-reads action selected: `{chosen}` ({len(targets)} sources)",
        f"- Scope: {', '.join(state['scope'])}",
        f"- Non-goals: {', '.join(state['non_goals'])}",
        "",
        "Content below is Git blob content at the commit above — authoritative; "
        "skip the corresponding boot reads. Echo back your understood scope before acting.",
        "",
        "## Current prompt / charter",
        "",
    ]
    cp = state["current_prompt"]
    cp_blob = repo.blob_for_path(commit, cp)
    charter_body = _cap(repo.content_for_path(commit, cp), max_bytes).rstrip()
    out.append(f"### charter: `{cp}` @ `{cp_blob}`\n\n```\n{charter_body}\n```\n")

    out.append(f"## Deep reads for action `{chosen}`\n")
    for target in targets:
        path, _, anchor = target.partition("#")
        blob = repo.blob_for_path(commit, path)
        loc = f"`{path}`" + (f" § `{anchor}`" if anchor else "")
        if manifest_only:
            out.append(f"- {loc} @ `{blob}`")
            continue
        if anchor:
            body, found = extract_section(repo.content_for_path(commit, path), anchor)
            if not found:
                out.append(f"### read {loc} @ `{blob}`\n\n⚠ section not found — read the file for `{anchor}`.\n")
                continue
        else:
            body = repo.content_for_path(commit, path)
        out.append(f"### read {loc} @ `{blob}`\n\n```\n{_cap(body, max_bytes).rstrip()}\n```\n")
    return "\n".join(out) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ref", required=True, help="explicit Git revision to resolve")
    parser.add_argument("--role", choices=sorted(ROLE_ACTIONS), help="role to pick up (maps to a deep_reads action)")
    parser.add_argument("--action", help="deep_reads action to load (overrides --role mapping)")
    parser.add_argument("--max-bytes", type=int, default=DEFAULT_MAX_BYTES, help="per-section inline cap")
    parser.add_argument("--manifest-only", action="store_true", help="list scoped reads instead of inlining them")
    args = parser.parse_args(argv)
    if not args.role and not args.action:
        parser.error("pass --role or --action")
    try:
        block = build_block(
            GitRepository(Path.cwd()), args.ref, args.role, args.action, args.max_bytes, args.manifest_only
        )
    except ContextError as error:
        print(f"orientation block: {error}", file=sys.stderr)
        return 1
    print(block, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
