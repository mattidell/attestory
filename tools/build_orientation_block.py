"""Emit a builder Orientation Block: the foreman capsule plus the *inlined*
content of the current prompt and the plan's deep_reads, all resolved at one
Git commit.

Why: transcripts show sub-agents are spawned cold (all 60 measured were generic)
and spend their first turns re-reading the same canonical set the foreman already
holds. This tool lets the foreman *push* that context into the spawn prompt once,
deterministically, instead of each builder *pulling* it turn by turn. Because
every byte is read from a named commit's blobs (not prose), it preserves the
builder discipline "verify the capsule against Git, do not reconstruct from
handoff prose" — the builder still checks the printed commit SHA.

This also subsumes the clerk's mechanical dispatch-prompt assembly: the block is
deterministic and pass/fail-checkable, so it is a script, not an agent spawn.

Usage:  python3 tools/build_orientation_block.py --ref <git-ref> [--max-bytes N]
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from tools.foreman_context import ContextError, GitRepository, render_context

DEFAULT_MAX_BYTES = 24_000  # per-file guard so a stray large file can't bloat the block


def _fenced(title: str, path: str, blob: str, body: str) -> str:
    return f"### {title}: `{path}` @ `{blob}`\n\n```\n{body.rstrip()}\n```\n"


def build_block(repo: GitRepository, ref: str, max_bytes: int, manifest_only: bool) -> str:
    capsule = render_context(repo, ref)
    commit = capsule["source"]["commit"]
    state = capsule["state"]
    wt = capsule["worktree"]

    # Dedup deep_reads by resolved path (the source map lists many files under
    # several actions; a builder needs each file's bytes once). Record which
    # actions cited each path, and count duplicates so authoring bloat is visible.
    first_action: dict[str, str] = {}
    dup_hits: dict[str, int] = {}
    for action, targets in capsule["deep_reads"].items():
        for target in targets:
            path = target.split("#", 1)[0]
            if path in first_action:
                dup_hits[path] = dup_hits.get(path, 1) + 1
            else:
                first_action[path] = action

    unique_paths = list(first_action)
    sizes = {p: len(repo.content_for_path(commit, p).encode("utf-8")) for p in unique_paths}
    total = sum(sizes.values())
    listed = sum(dup_hits.get(p, 1) for p in unique_paths)

    out: list[str] = [
        "# BUILDER ORIENTATION BLOCK (preloaded — do not re-read these files)",
        "",
        f"- Commit: `{commit}`  (verify this SHA against Git before acting)",
        f"- Branch: `{wt['branch'] or 'detached'}`; dirty: `{wt['dirty']}`",
        f"- Phase/topic: {state['phase']} / `{state['topic']}` ({state['plan_status']})",
        f"- Current role: {state['current_role']}",
        f"- Scope: {', '.join(state['scope'])}",
        f"- Non-goals: {', '.join(state['non_goals'])}",
        "",
        f"- Deep reads: {len(unique_paths)} unique files, {total} bytes "
        f"(~{total // 4} tokens); source map listed {listed} entries.",
    ]
    if dup_hits:
        dups = ", ".join(f"`{p}`×{c}" for p, c in sorted(dup_hits.items(), key=lambda kv: -kv[1]))
        out.append(f"- ⚠ deep_reads duplication in the plan (deduped here): {dups}")
    out += [
        "",
        "Content below is Git blob content at the commit above, not prose — treat "
        "it as authoritative and skip the corresponding boot reads.",
        "",
        "## Current prompt / charter",
        "",
    ]

    cp = state["current_prompt"]
    cp_blob = repo.blob_for_path(commit, cp)
    out.append(_fenced("prompt", cp, cp_blob, _read(repo, commit, cp, max_bytes)))

    out.append("\n## Deep reads (deduped)\n")
    if manifest_only:
        for path in unique_paths:
            blob = repo.blob_for_path(commit, path)
            out.append(f"- `{path}` @ `{blob}` ({sizes[path]} bytes) — cited by action `{first_action[path]}`")
    else:
        for path in unique_paths:
            blob = repo.blob_for_path(commit, path)
            out.append(_fenced(f"read ({first_action[path]})", path, blob, _read(repo, commit, path, max_bytes)))
    return "\n".join(out) + "\n"


def _read(repo: GitRepository, commit: str, path: str, max_bytes: int) -> str:
    body = repo.content_for_path(commit, path)
    if len(body.encode("utf-8")) > max_bytes:
        clipped = body.encode("utf-8")[:max_bytes].decode("utf-8", "ignore")
        return clipped + f"\n… [truncated at {max_bytes} bytes — read the file for the rest]"
    return body


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ref", required=True, help="explicit Git revision to resolve")
    parser.add_argument("--max-bytes", type=int, default=DEFAULT_MAX_BYTES)
    parser.add_argument(
        "--manifest-only",
        action="store_true",
        help="list deduped deep reads (path/blob/size) instead of inlining their content",
    )
    args = parser.parse_args(argv)
    try:
        block = build_block(GitRepository(Path.cwd()), args.ref, args.max_bytes, args.manifest_only)
    except ContextError as error:
        print(f"orientation block: {error}", file=sys.stderr)
        return 1
    print(block, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
