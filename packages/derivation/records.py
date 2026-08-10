"""The derivation record stream: paired run accounts, outside the act log.

ADR-0008. Records are their own citizen kind in their own append-only stream
(`derivation_records.jsonl`), linked to publication acts only by run_id. The
storage discipline is the act log's (ADR-0002): a newline is the commit
marker, the write is flushed and fsynced, and an interrupted write leaves a
valid shorter stream plus a quarantined partial tail.

A run is bounded by a pair: a `started` record, then a separate closing
record (`completed`/`interrupted`/`failed`). The pair closes the orphan
window (decision 2): a start with publications but no close is *detectable*
and recovered by appending a closing record — the start is never mutated.
Records misstating history (a close with no start, a second start, a close
before its start) halt reads; a merely-open run does not.

Adoption gate (milestone scope): a run may only start against an adopted
package. The gate is enforced here before the start record is written.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from packages.derivation.loader import DERIVATION_RECORD_SCHEMA, DerivationSchemas

RECORD_STREAM_FILENAME = "derivation_records.jsonl"

# The current versioned-ledger record schema. v3 carries the reconciled
# block-code vocabulary (SOURCE_SET_UNCLOSED, the code the runner actually
# emits; ADR-0036 production condition 3) and the named tie-out invariant.
# v4 adds COMPLETENESS_VALUE_VIOLATION (ADR-0055 Decision 2). v5 adds
# MULTIPLE_F1098_OUT_OF_SCOPE. v6 adds F1098_SCOPE_CONTRADICTION (Track 2
# repair round 3 finding 1).
CURRENT_RECORD_SCHEMA = "derivation-record.v6"
_VERSIONED_RECORD_SCHEMAS = frozenset(
    {
        "derivation-record.v2",
        "derivation-record.v3",
        "derivation-record.v4",
        "derivation-record.v5",
        "derivation-record.v6",
    }
)

_CLOSING_PHASES = frozenset({"completed", "interrupted", "failed"})


class RecordStreamError(Exception):
    """A rejected append: invalid record or a broken pairing."""


class RecordStreamCorruption(Exception):
    """The stream misstates history: a malformed or mis-paired committed line."""


class AdoptionError(Exception):
    """A run was started against a package that is not adopted."""


@dataclass(frozen=True)
class RecordStreamContents:
    records: tuple[dict[str, Any], ...]
    incomplete_tail: str | None


@dataclass(frozen=True)
class RunStanding:
    """One run's start record and its closing record, if any."""

    run_id: str
    start: dict[str, Any]
    closing: dict[str, Any] | None

    @property
    def is_open(self) -> bool:
        return self.closing is None


class RecordStream:
    """Append-only derivation-record stream for one workspace directory."""

    def __init__(self, workspace_dir: Path, schemas: DerivationSchemas) -> None:
        self._path = workspace_dir / RECORD_STREAM_FILENAME
        self._schemas = schemas

    @property
    def path(self) -> Path:
        return self._path

    def read(self) -> RecordStreamContents:
        if not self._path.exists():
            return RecordStreamContents(records=(), incomplete_tail=None)
        raw = self._path.read_bytes()
        lines = raw.split(b"\n")
        tail = lines[-1]
        records: list[dict[str, Any]] = []
        for index, line in enumerate(lines[:-1]):
            records.append(self._parse_committed_line(index, line))
        self._check_pairing(records)
        incomplete_tail = tail.decode("utf-8", errors="replace") if tail else None
        return RecordStreamContents(records=tuple(records), incomplete_tail=incomplete_tail)

    def _parse_committed_line(self, index: int, line: bytes) -> dict[str, Any]:
        try:
            record: dict[str, Any] = json.loads(line)
        except (json.JSONDecodeError, UnicodeDecodeError) as exc:
            raise RecordStreamCorruption(f"malformed committed record at index {index}: {exc}") from exc
        try:
            self._schemas.validate_declared(record)
        except Exception as exc:  # SchemaValidationError; a committed line must conform
            raise RecordStreamCorruption(f"committed record at index {index} does not conform: {exc}") from exc
        return record

    def _check_pairing(self, records: list[dict[str, Any]]) -> None:
        started: set[str] = set()
        closed: set[str] = set()
        for record in records:
            run_id = record["run_id"]
            if record["phase"] == "started":
                if run_id in started:
                    raise RecordStreamCorruption(f"run started twice: {run_id}")
                started.add(run_id)
            else:
                if run_id not in started:
                    raise RecordStreamCorruption(f"run closed before it started: {run_id}")
                if run_id in closed:
                    raise RecordStreamCorruption(f"run closed twice: {run_id}")
                closed.add(run_id)

    def append(self, record: dict[str, Any]) -> None:
        """Commit one record: validate, then a single fsynced newline write."""
        self._schemas.validate_declared(record)
        contents = self.read()
        self._check_pairing([*contents.records, record])
        line = json.dumps(record, sort_keys=True, separators=(",", ":"))
        self._path.parent.mkdir(parents=True, exist_ok=True)
        with self._path.open("ab") as handle:
            handle.write(line.encode("utf-8") + b"\n")
            handle.flush()
            os.fsync(handle.fileno())

    def standings(self) -> dict[str, RunStanding]:
        """Every run's standing, from the committed stream."""
        starts: dict[str, dict[str, Any]] = {}
        closings: dict[str, dict[str, Any]] = {}
        for record in self.read().records:
            if record["phase"] == "started":
                starts[record["run_id"]] = record
            else:
                closings[record["run_id"]] = record
        return {
            run_id: RunStanding(run_id=run_id, start=start, closing=closings.get(run_id))
            for run_id, start in starts.items()
        }

    def open_runs(self) -> dict[str, RunStanding]:
        """Runs with a start and no closing record — the recovery worklist."""
        return {run_id: s for run_id, s in self.standings().items() if s.is_open}


def started_record(
    *,
    record_id: str,
    run_id: str,
    workspace_revision: int,
    governance_pins: list[dict[str, Any]],
    adoption_pin: dict[str, Any],
    use_v2: bool = False,
) -> dict[str, Any]:
    return {
        "schema": CURRENT_RECORD_SCHEMA if use_v2 else "derivation-record.v1",
        "record_id": record_id,
        "run_id": run_id,
        "phase": "started",
        "workspace_revision": workspace_revision,
        "governance_pins": governance_pins,
        "adoption_pin": adoption_pin,
    }


def closing_record(
    *,
    record_id: str,
    run_id: str,
    phase: str,
    workspace_revision: int,
    governance_pins: list[dict[str, Any]],
    adoption_pin: dict[str, Any],
    stop_reason: str,
    published: list[dict[str, Any]],
    blocked: list[dict[str, Any]],
    dispositions: list[dict[str, Any]],
    use_v2: bool = False,
) -> dict[str, Any]:
    if phase not in _CLOSING_PHASES:
        raise RecordStreamError(f"not a closing phase: {phase}")
    record = {
        "schema": CURRENT_RECORD_SCHEMA if use_v2 else "derivation-record.v1",
        "record_id": record_id,
        "run_id": run_id,
        "phase": phase,
        "workspace_revision": workspace_revision,
        "governance_pins": governance_pins,
        "adoption_pin": adoption_pin,
        "stop_reason": stop_reason,
        "dispositions": dispositions,
    }
    if not use_v2:
        record["published"] = published
        record["blocked"] = blocked
    return record


def start_run(
    stream: RecordStream,
    *,
    record_id: str,
    run_id: str,
    workspace_revision: int,
    governance_pins: list[dict[str, Any]],
    adoption_pin: dict[str, Any],
    adopted_packages: set[str],
    use_v2: bool = False,
) -> dict[str, Any]:
    """Gate on adoption, then write the started record.

    The adoption gate is content, not code posture: the package named by the
    adoption pin must be in the adopted set, or the run never starts.
    """
    if adoption_pin["id"] not in adopted_packages:
        raise AdoptionError(f"package not adopted: {adoption_pin['id']}")
    record = started_record(
        record_id=record_id,
        run_id=run_id,
        workspace_revision=workspace_revision,
        governance_pins=governance_pins,
        adoption_pin=adoption_pin,
        use_v2=use_v2,
    )
    stream.append(record)
    return record


def recover_interrupted(
    stream: RecordStream,
    run_id: str,
    *,
    record_id: str,
) -> dict[str, Any]:
    """Close an open run by appending an `interrupted` record.

    Recovery never mutates the start record (decision 2). The closing record
    reuses the start's provenance and declares an empty output surface with
    stop_reason `interrupted`; the publications that did land remain
    attributable to the started run.
    """
    standing = stream.open_runs().get(run_id)
    if standing is None:
        raise RecordStreamError(f"no open run to recover: {run_id}")
    start = standing.start
    use_v2 = start.get("schema") in _VERSIONED_RECORD_SCHEMAS
    record = closing_record(
        record_id=record_id,
        run_id=run_id,
        phase="interrupted",
        workspace_revision=start["workspace_revision"],
        governance_pins=start["governance_pins"],
        adoption_pin=start["adoption_pin"],
        stop_reason="interrupted",
        published=[],
        blocked=[],
        dispositions=[],
        use_v2=use_v2,
    )
    stream.append(record)
    return record
