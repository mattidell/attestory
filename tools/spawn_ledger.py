"""Append-only ledger for sub-agent spawns and owner-launches, so the
otherwise-invisible cost of spawning (count, wall-clock, self-reported turns and
tool calls) becomes a measured baseline instead of a guess.

Sub-agent internals do not appear in the parent's transcript, and Codex/Grok runs
live in their own stores — so this must be recorded at the launch boundary. The
foreman records a `launch` event when it spawns/launches a role; the returning
agent (or the foreman, from the agent's final report) records a `return` event
with wall-clock seconds and the agent's self-reported turn / tool-call counts.

Records are role/kind/timestamps/counts only — no real values, workspace paths, or
personal output (ADR-0031). The ledger is git-ignored by default (operational,
per-machine); commit a snapshot if you want a shared baseline.

Usage:
  python3 tools/spawn_ledger.py record --role builder --kind spawn --event launch
  python3 tools/spawn_ledger.py record --role builder --kind spawn --event return \
      --wall-seconds 830 --turns 22 --tool-calls 41 --outcome ready
  python3 tools/spawn_ledger.py summary
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

DEFAULT_LEDGER = "metrics/spawn-ledger.jsonl"


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def record(path: Path, fields: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    entry = {"ts": _now(), **{k: v for k, v in fields.items() if v is not None}}
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(entry, sort_keys=True) + "\n")


def summary(path: Path) -> str:
    if not path.exists():
        return f"no ledger at {path} yet"
    launches: dict[tuple[str, str], int] = defaultdict(int)
    returns: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            e = json.loads(line)
        except json.JSONDecodeError:
            continue
        key = (e.get("role", "?"), e.get("kind", "?"))
        # `dispatch` is the pre-2026-07-26 name for this event; the ledger is
        # append-only, so old records keep it and are still counted.
        if e.get("event") in ("launch", "dispatch"):
            launches[key] += 1
        elif e.get("event") == "return":
            returns[key].append(e)

    out = [f"# Spawn ledger summary ({path})", ""]
    keys = sorted(set(launches) | set(returns))
    if not keys:
        return "\n".join(out + ["(no launch/return events recorded)"])
    for key in keys:
        role, kind = key
        rets = returns[key]
        walls = [r["wall_seconds"] for r in rets if isinstance(r.get("wall_seconds"), (int, float))]
        turns = [r["turns"] for r in rets if isinstance(r.get("turns"), (int, float))]
        parts = [f"launches={launches[key]}", f"returns={len(rets)}"]
        if walls:
            parts.append(f"median_wall={sorted(walls)[len(walls) // 2]:.0f}s")
        if turns:
            parts.append(f"median_turns={sorted(turns)[len(turns) // 2]:.0f}")
        out.append(f"- {role} / {kind}: " + "  ".join(parts))
    return "\n".join(out)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ledger", default=DEFAULT_LEDGER, help="ledger path (JSONL)")
    sub = parser.add_subparsers(dest="cmd", required=True)

    rec = sub.add_parser("record", help="append a launch or return event")
    rec.add_argument("--role", required=True, help="role launched (builder, reviewer, advisor, …)")
    rec.add_argument("--kind", required=True, choices=("spawn", "owner-launch", "dispatch"),
                     help="spawn = foreman sub-agent; owner-launch = fresh thread")
    rec.add_argument("--event", required=True, choices=("launch", "return", "dispatch"))
    rec.add_argument("--ref", help="git ref/commit the run was oriented against")
    rec.add_argument("--wall-seconds", type=float, dest="wall_seconds", help="return: wall-clock duration")
    rec.add_argument("--turns", type=int, help="return: agent's self-reported turn count")
    rec.add_argument("--tool-calls", type=int, dest="tool_calls", help="return: self-reported tool-call count")
    rec.add_argument("--outcome", help="return: short outcome tag (ready, changes-requested, blocked, …)")
    rec.add_argument("--note", help="short free-text note (no real values / paths)")

    sub.add_parser("summary", help="aggregate the ledger")

    args = parser.parse_args(argv)
    path = Path(args.ledger)
    if args.cmd == "record":
        record(path, {
            "event": args.event, "role": args.role, "kind": args.kind, "ref": args.ref,
            "wall_seconds": args.wall_seconds, "turns": args.turns,
            "tool_calls": args.tool_calls, "outcome": args.outcome, "note": args.note,
        })
        return 0
    print(summary(path))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
