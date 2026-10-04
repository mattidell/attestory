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
from typing import IO, Any, Sequence

from packages.kernel.findings import (
    declares_new_write_invariants,
    enforce_new_write_invariants,
    new_write_invariants_may_apply,
    project,
)
from packages.kernel.schema_registry import SchemaRegistry

ACT_ENVELOPE_SCHEMA = "act.v1"
ACT_LOG_FILENAME = "acts.jsonl"
# ``append_batch`` writes a whole save here, then renames it over the log.
PENDING_SUFFIX = ".pending"


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


def _payload_schema_id(kind: str, payload: dict[str, Any] | None = None) -> str:
    """Resolve the published payload schema for an act kind.

    Successor carrier acts (assertion / member-transition / bundle-adoption)
    admit their published successor payloads. The nested citizen's declared
    schema (or, for member-transition's ``remove``/``reclassify`` actions,
    the presence of the v3-only ``corresponds_to_fact_id`` field) selects the
    payload schema so finding.v2 / bundle.v2 / act-member-transition.v3 acts
    admit without inventing a second envelope channel (ADR-0032 successor
    carriers).
    """
    if payload is not None:
        if kind == "assertion":
            finding = payload.get("finding")
            if isinstance(finding, dict) and finding.get("schema") == "finding.v2":
                return "act-assertion.v2"
        elif kind == "member-transition":
            member = payload.get("member")
            if isinstance(member, dict):
                if isinstance(member.get("corresponds_to_fact_id"), str):
                    return "act-member-transition.v3"
                finding = member.get("finding")
                if isinstance(finding, dict) and finding.get("schema") == "finding.v2":
                    return "act-member-transition.v2"
        elif kind == "bundle-adoption":
            bundle = payload.get("bundle")
            if isinstance(bundle, dict) and bundle.get("schema") == "bundle.v2":
                return "act-bundle-adoption.v2"
    return f"act-{kind}.v1"


class ActLog:
    """Append-only act log for one workspace directory."""

    def __init__(
        self,
        workspace_dir: Path,
        registry: SchemaRegistry,
        *,
        read_only: bool = False,
        undeclared_test_log: bool = False,
    ) -> None:
        """Open one workspace's act log.

        ADR 0077 Part 5, acceptance condition: a writable log is built only
        over a registry that carries a well-formed new-write declaration
        (``scoped_supersession_declarations``, installed by a domain loader),
        so the new-write step in ``append`` cannot be skipped by registry
        choice. Any other registry fails here, loudly. Two explicit
        exceptions: ``read_only=True`` opens a log that refuses every
        ``append``; ``undeclared_test_log=True`` is for tests only and is
        never used under ``packages/``.
        """
        self._path = workspace_dir / ACT_LOG_FILENAME
        self._registry = registry
        self._read_only = read_only
        self._requires_declaration = not (read_only or undeclared_test_log)
        self._check_declaration()

    def _check_declaration(self) -> None:
        if self._requires_declaration and not declares_new_write_invariants(self._registry):
            raise ActLogError(
                "registry carries no well-formed new-write declaration "
                "(scoped_supersession_declarations); a writable ActLog requires one "
                "(ADR 0077 Part 5); open it read_only=True to read"
            )

    @property
    def path(self) -> Path:
        return self._path

    @property
    def registry(self) -> SchemaRegistry:
        return self._registry

    def read(self) -> LogContents:
        """Read committed acts; quarantine an uncommitted partial tail.

        The commit marker is the terminating newline. A trailing chunk
        without one — whether or not it happens to parse — was never
        committed and is returned for visibility, never as an act.
        """
        if not self._path.exists():
            return LogContents(acts=(), incomplete_tail=None)
        return self._contents_of(self._path.read_bytes())

    def _contents_of(self, raw: bytes) -> LogContents:
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
        self._registry.validate(_payload_schema_id(act["kind"], act["payload"]), act["payload"])
        return act

    def append(self, act: dict[str, Any], expected_revision: int) -> int:
        """Commit one complete act against an expected revision.

        Returns the new revision. Validation precedes the write; the
        write is a single newline-terminated line, flushed and fsynced,
        so interruption can only lose the act, never corrupt history.

        ADR 0077 Part 5: after the envelope, payload and revision checks and
        before the write, the new-write step runs on the projection of the
        acts already in the log. A refusal raises ``FindingModelError`` and
        writes nothing. ``read`` and ``project`` never run the step.
        """
        if self._read_only:
            raise ActLogError("read-only act log: append is refused")
        # The registry is mutable; a declaration removed after construction
        # must not let a write skip the step.
        self._check_declaration()
        self._registry.validate(ACT_ENVELOPE_SCHEMA, act)
        self._registry.validate(_payload_schema_id(act["kind"], act["payload"]), act["payload"])
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
        if new_write_invariants_may_apply(act, self._registry):
            enforce_new_write_invariants(
                project(contents.acts, self._registry), act, self._registry
            )
        line = json.dumps(act, sort_keys=True, separators=(",", ":"))
        self._path.parent.mkdir(parents=True, exist_ok=True)
        with self._path.open("ab") as handle:
            handle.write(line.encode("utf-8") + b"\n")
            handle.flush()
            os.fsync(handle.fileno())
        return current + 1

    def append_batch(self, acts: Sequence[dict[str, Any]], expected_revision: int) -> int:
        """Commit several acts as one save: all of them, or none.

        Every act is validated, its revision and identity checked, and the
        ADR 0077 Part 5 new-write step run against the acts staged before it,
        before anything is written. A refusal of any act writes nothing.

        The write is the committed log plus the new lines in a pending file
        beside it, fsynced, then renamed over the log. An interruption before
        the rename leaves the log byte for byte as it was; after it, the whole
        save is committed. The committed prefix is copied unchanged, so the log
        only grows. A log with an uncommitted partial tail is refused, never
        written onto. A log that changed while the save was being written is
        refused and left as the other writer left it.
        """
        if self._read_only:
            raise ActLogError("read-only act log: append is refused")
        self._check_declaration()
        if not acts:
            raise ActLogError("a batch with no acts is refused")
        for act in acts:
            self._registry.validate(ACT_ENVELOPE_SCHEMA, act)
            self._registry.validate(_payload_schema_id(act["kind"], act["payload"]), act["payload"])
        raw = self._path.read_bytes() if self._path.exists() else b""
        contents = self._contents_of(raw)
        if contents.incomplete_tail is not None:
            raise ActLogError(
                "act log has an uncommitted partial tail; a batch is not written onto it"
            )
        current = contents.revision
        if expected_revision != current:
            raise ActLogError(
                f"stale revision: expected {expected_revision}, workspace is at {current}"
            )
        staged = list(contents.acts)
        known = {existing["act_id"] for existing in staged}
        for act in acts:
            if act["committed_against"] != len(staged):
                raise ActLogError(
                    f"act commits against revision {act['committed_against']}, "
                    f"batch position is revision {len(staged)}"
                )
            if act["act_id"] in known:
                raise ActLogError(f"duplicate act_id: {act['act_id']}")
            if new_write_invariants_may_apply(act, self._registry):
                enforce_new_write_invariants(project(tuple(staged), self._registry), act, self._registry)
            known.add(act["act_id"])
            staged.append(act)
        self._path.parent.mkdir(parents=True, exist_ok=True)
        pending = self._path.with_name(self._path.name + PENDING_SUFFIX)
        with pending.open("wb") as handle:
            handle.write(raw)
            for act in acts:
                line = json.dumps(act, sort_keys=True, separators=(",", ":")).encode("utf-8")
                self._write_pending_line(handle, line + b"\n")
            handle.flush()
            os.fsync(handle.fileno())
        # Single writer per workspace (ADR-0002). Another writer that committed
        # while this save was written is not overwritten.
        on_disk = self._path.stat().st_size if self._path.exists() else 0
        if on_disk != len(raw):
            pending.unlink()
            raise ActLogError("stale revision: the act log changed during the save; nothing was written")
        os.replace(pending, self._path)
        _fsync_directory(self._path.parent)
        return current + len(acts)

    def _write_pending_line(self, handle: IO[bytes], line: bytes) -> None:
        """Write one newline-terminated act line of a batch to its pending file."""
        handle.write(line)


def _fsync_directory(directory: Path) -> None:
    """Make a rename in ``directory`` durable where the platform allows it."""
    try:
        descriptor = os.open(directory, os.O_RDONLY)
    except OSError:
        return
    try:
        os.fsync(descriptor)
    except OSError:
        pass
    finally:
        os.close(descriptor)
