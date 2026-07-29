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
reconstruct from prose": the block prints the commit SHA to verify.

Portable: pure standard library; no runner-specific assumptions.

Usage:
  python3 tools/build_orientation_block.py --ref HEAD --role builder
  python3 tools/build_orientation_block.py --ref HEAD --action review
  python3 tools/build_orientation_block.py --ref HEAD --role builder --manifest-only
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from tools.foreman_context import ContextError, GitRepository, render_context

# Which deep_reads action each role picks up. Extend as roles are added.
ROLE_ACTIONS = {"builder": "implementation", "reviewer": "review"}
DEFAULT_MAX_BYTES = 24_000  # per-section guard


def detect_role(current_role: str) -> str | None:
    """Infer the role from phase state's free-text current_role (e.g. 'Track 1
    ... Builder' -> 'builder'). Returns None if zero or more than one role word
    matches, so the caller can ask for an explicit --role."""
    hits = [role for role in ROLE_ACTIONS if role in current_role.casefold()]
    return hits[0] if len(hits) == 1 else None


# Phrasings that mark a clean-room / independent rival round. Detected
# from the current_role so the owner never has to pass a flag.
CLEAN_ROOM_MARKERS = ("clean-room", "clean room", "rival", "independent")


def detect_clean_room(current_role: str) -> bool:
    role = current_role.casefold()
    return any(marker in role for marker in CLEAN_ROOM_MARKERS)


# The governance set writes its articles and constraints as bold-lead
# paragraphs (`**Article 18 — Quarantine.** Personal data lives ...`) rather
# than ATX headings. Plans anchor deep reads to those names, so without this
# they resolve to nothing and the caller falls back to inlining the whole file
# — silently turning a 200-word scoped read into a 12 KB one. Treat a bold lead
# as the deepest possible heading: it never terminates a real `#` section, but
# it is addressable and it terminates its own.
_BOLD_LEAD = re.compile(r"^\*\*(?P<text>[^*\n]+?)\*\*(?:\s|$)")
_BOLD_LEAD_LEVEL = 9


def _bold_lead_text(line: str) -> str | None:
    match = _BOLD_LEAD.match(line.lstrip())
    return match.group("text").strip().rstrip(".").strip() if match else None


def _heading_level(line: str) -> int:
    stripped = line.lstrip()
    if not stripped.startswith("#"):
        return _BOLD_LEAD_LEVEL if _bold_lead_text(line) else 0
    return len(stripped) - len(stripped.lstrip("#"))


def _heading_text(line: str) -> str:
    bold = _bold_lead_text(line)
    if bold is not None:
        return bold
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
    max_bytes: int, manifest_only: bool, clean_room: bool | None = None,
) -> str:
    capsule = render_context(repo, ref)
    commit = capsule["source"]["commit"]
    state = capsule["state"]
    wt = capsule["worktree"]

    # Auto-detect the role from phase state when the owner didn't specify one.
    detected = None
    if not role and not action:
        detected = detect_role(state["current_role"])
        if not detected:
            resting = state["current_role"].strip().casefold().startswith("foreman")
            hint = (
                "no builder or reviewer work is chartered right now — this is the "
                "resting state between milestones, not an error to route around. "
                "Re-enter the foreman seat via tools/foreman_context.py instead"
                if resting
                else f"pass --role ({'/'.join(sorted(ROLE_ACTIONS))}) or --action explicitly"
            )
            raise ContextError(
                f"could not infer role from current_role {state['current_role']!r}; {hint}"
            )
        role = detected
    # Clean-room is auto-detected from phase state (no owner-facing flag); the
    # optional CLI override is only for tests and forced runs.
    if clean_room is None:
        clean_room = detect_clean_room(state["current_role"])
    chosen = _resolve_action(capsule, role, action)

    # Clean-room: a rival builder reimplements from the spec without the curated
    # reading set that would anchor it to the primary's framing. Give the charter,
    # scope, and non-goals; list the deep reads as a manifest but do NOT inline
    # them — the rival decides independently what to consult.
    if clean_room:
        manifest_only = True

    # dedup by full target (path#anchor): the same file under two anchors is two
    # distinct sections and both are kept; an exact repeat is dropped.
    seen: set[str] = set()
    targets: list[str] = []
    for target in capsule["deep_reads"][chosen]:
        if target not in seen:
            seen.add(target)
            targets.append(target)

    label = f"{role or chosen}" + (" · CLEAN ROOM" if clean_room else "")
    role_line = f"- Role: `{role or chosen}`" + (" (auto-detected from phase state)" if detected else "")
    out: list[str] = [
        f"# ORIENTATION BLOCK — {label}",
        "",
        f"- Commit: `{commit}`  (verify this SHA against Git before acting)",
        f"- Branch: `{wt['branch'] or 'detached'}`; dirty: `{wt['dirty']}`",
        f"- Phase/topic: {state['phase']} / `{state['topic']}` ({state['plan_status']})",
        role_line,
        f"- Current role (per phase state): {state['current_role']}",
        f"- Deep-reads action selected: `{chosen}` ({len(targets)} sources)",
        f"- Scope: {', '.join(state['scope'])}",
        f"- Non-goals: {', '.join(state['non_goals'])}",
        "",
    ]
    if clean_room:
        out.append(
            "CLEAN ROOM: reimplement from the charter and scope below. Deep reads "
            "are listed as a manifest only, not inlined — consult them independently "
            "if needed. Do not read any other builder's implementation, thread, or "
            "rationale; your value is an independent solution to the same spec.\n"
        )
    else:
        out.append(
            "Content below is Git blob content at the commit above — authoritative; "
            "skip the corresponding boot reads. Echo back your understood scope before acting.\n"
        )
    out += ["## Current prompt / charter", ""]
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
    parser.add_argument(
        "--clean-room", dest="clean_room", action="store_const", const=True, default=None,
        help="force clean-room mode (normally auto-detected from the phase-state role; override for tests/forced runs)",
    )
    args = parser.parse_args(argv)
    try:
        block = build_block(
            GitRepository(Path.cwd()), args.ref, args.role, args.action,
            args.max_bytes, args.manifest_only, args.clean_room,
        )
    except ContextError as error:
        print(f"orientation block: {error}", file=sys.stderr)
        return 1
    print(block, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
