"""The act log: the workspace's sole authoritative store.

Per ADR-0002: one append-only JSON Lines file per workspace. Each line
is a complete, schema-versioned act envelope; a line is committed only
when newline-terminated. An interrupted write therefore leaves a valid
shorter log plus a quarantined partial tail — the workspace is
incomplete, never wrong (Article 6). A malformed line anywhere but the
tail is a misstatement of history and is an error, never repaired
(Article 9).

A revision is a position in the act sequence (Ontology §1, Revision):
revision N is the state after the first N acts, and the act at index k
commits against revision k.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from packages.kernel.schema_registry import SchemaRegistry

ACT_ENVELOPE_SCHEMA = "act.v1"
ACT_LOG_FILENAME = "acts.jsonl"


class ActLogError(Exception):
    """A rejected append: stale revision, invalid act, duplicate id."""


class ActLogCorruption(Exception):
    """The log misstates history: a malformed line before the tail."""


@dataclass(frozen=True)
class LogContents:
    """Committed acts plus any quarantined, uncommitted partial tail."""

    acts: tuple[dict[str, Any], ...]
    incomplete_tail: str | None

    @property
    def revision(self) -> int:
        return len(self.acts)


def _payload_schema_id(kind: str) -> str:
    return f"act-{kind}.v1"


class ActLog:
    """Append-only act log for one workspace directory."""

    def __init__(self, workspace_dir: Path, registry: SchemaRegistry) -> None:
        self._path = workspace_dir / ACT_LOG_FILENAME
        self._registry = registry

    @property
    def path(self) -> Path:
        return self._path

    def read(self) -> LogContents:
        """Read committed acts; quarantine an uncommitted partial tail.

        The commit marker is the terminating newline. A trailing chunk
        without one — whether or not it happens to parse — was never
        committed and is returned for visibility, never as an act.
        """
        if not self._path.exists():
            return LogContents(acts=(), incomplete_tail=None)
        raw = self._path.read_bytes()
        acts: list[dict[str, Any]] = []
        seen_ids: set[str] = set()
        lines = raw.split(b"\n")
        tail = lines[-1]  # b"" when the final line was newline-terminated
        for index, line in enumerate(lines[:-1]):
            act = self._parse_committed_line(index, line)
            if act["committed_against"] != index:
                raise ActLogCorruption(
                    f"act at index {index} commits against revision "
                    f"{act['committed_against']}"
                )
            if act["act_id"] in seen_ids:
                raise ActLogCorruption(f"duplicate act_id: {act['act_id']}")
            seen_ids.add(act["act_id"])
            acts.append(act)
        incomplete_tail = tail.decode("utf-8", errors="replace") if tail else None
        return LogContents(acts=tuple(acts), incomplete_tail=incomplete_tail)

    def _parse_committed_line(self, index: int, line: bytes) -> dict[str, Any]:
        try:
            act: dict[str, Any] = json.loads(line)
        except (json.JSONDecodeError, UnicodeDecodeError) as exc:
            raise ActLogCorruption(
                f"malformed committed line at index {index}: {exc}"
            ) from exc
        self._registry.validate(ACT_ENVELOPE_SCHEMA, act)
        self._registry.validate(_payload_schema_id(act["kind"]), act["payload"])
        return act

    def append(self, act: dict[str, Any], expected_revision: int) -> int:
        """Commit one complete act against an expected revision.

        Returns the new revision. Validation precedes the write; the
        write is a single newline-terminated line, flushed and fsynced,
        so interruption can only lose the act, never corrupt history.
        """
        self._registry.validate(ACT_ENVELOPE_SCHEMA, act)
        self._registry.validate(_payload_schema_id(act["kind"]), act["payload"])
        contents = self.read()
        current = contents.revision
        if expected_revision != current:
            raise ActLogError(
                f"stale revision: expected {expected_revision}, workspace is at {current}"
            )
        if act["committed_against"] != current:
            raise ActLogError(
                f"act commits against revision {act['committed_against']}, "
                f"workspace is at {current}"
            )
        if any(existing["act_id"] == act["act_id"] for existing in contents.acts):
            raise ActLogError(f"duplicate act_id: {act['act_id']}")
        line = json.dumps(act, sort_keys=True, separators=(",", ":"))
        self._path.parent.mkdir(parents=True, exist_ok=True)
        with self._path.open("ab") as handle:
            handle.write(line.encode("utf-8") + b"\n")
            handle.flush()
            os.fsync(handle.fileno())
        return current + 1
