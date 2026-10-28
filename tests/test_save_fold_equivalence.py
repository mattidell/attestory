"""Differential admission for one save: fresh projection versus ``append_batch``.

The oracle below is the pre-change save. For each checked act it calls
``project`` on the whole prefix. An unchecked act is not folded while it is
staged. The refused index is the batch position being checked when the
exception leaves that loop, including when the failure is an earlier
unchecked act that the later projection folds. ``append`` still reads a
historical prefix by calling ``project`` once, and only when that one act is
checked.

Both sides see the same synthetic batches. The comparison is exception type
and message, that index, pending-file presence, and the final log bytes.
"""

from __future__ import annotations

import json
import os
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Iterator
from unittest import TestCase, mock

from packages.kernel.act_log import (
    ACT_ENVELOPE_SCHEMA,
    LIFECYCLE_ACT_KINDS,
    PENDING_SUFFIX,
    ActLog,
    ActLogError,
    _SaveFold,
    _enforce_second_genesis_rule,
    _fsync_directory,
    _payload_schema_id,
)
from packages.kernel.facts import fact_id_for
from packages.kernel.findings import (
    FindingModelError,
    apply_act,
    enforce_new_write_invariants,
    member_restoration_is_on_removal_lineage,
    new_write_invariants_may_apply,
    project,
)
from tests.support import (
    act,
    demo_bundle,
    demo_entity,
    demo_evidence,
    demo_fact_type_payment,
    demo_fact_type_rate_choice,
    demo_finding,
    demo_note_act,
    demo_payment_fact_id,
    registry_with_demo_kinds,
)

_FAMILY = {"id": "demo.family.payments", "version": "v1"}
_SCOPE = {"period": "2025"}
_COMMENT_KEYS = (
    ("counterparty", "demo-corp-a"),
    ("period", "2025"),
    ("comment", "noted"),
)
_DECLARATION: dict[str, Any] = {
    "source_fact_type": "demo.counterparty-payment",
    "dependent_fact_type": "demo.payment-comment",
    "dependent_keys_not_identifying_source": ["comment"],
    "reviewed_scope": {
        "evidence_kind": "demo.statement",
        "correction_path": ["correction"],
        "source_field": "source",
        "scope_field": "scope",
        "scopes": ["amount-only"],
        "refresh_field": "refresh",
        "binds": ["reviewed", "amount", "identity"],
        "successor_evidence_kind": "demo.successor-statement",
    },
}


@dataclass(frozen=True)
class _View:
    exc_type: str | None
    message: str | None
    revision: int | None
    log_bytes: bytes
    pending: bool
    tail: str | None
    read_revision: int | None


def _fresh_project_append_batch(
    log: ActLog,
    acts: list[dict[str, Any]],
    expected_revision: int,
    refused_at: list[int],
) -> int:
    """Today's ``append_batch`` decision, projecting the whole prefix each time."""

    refused_at.clear()
    if log._read_only:
        raise ActLogError("read-only act log: append is refused")
    log._check_declaration()
    if not acts:
        raise ActLogError("a batch with no acts is refused")
    for item in acts:
        log._registry.validate(ACT_ENVELOPE_SCHEMA, item)
        log._registry.validate(_payload_schema_id(item["kind"], item["payload"]), item["payload"])
    raw = log._path.read_bytes() if log._path.exists() else b""
    contents = log._contents_of(raw)
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
    for index, item in enumerate(acts):
        try:
            if item["committed_against"] != len(staged):
                raise ActLogError(
                    f"act commits against revision {item['committed_against']}, "
                    f"batch position is revision {len(staged)}"
                )
            if item["act_id"] in known:
                raise ActLogError(f"duplicate act_id: {item['act_id']}")
            proj: Any = None
            if new_write_invariants_may_apply(item, log.registry):
                proj = project(tuple(staged), log.registry)
                enforce_new_write_invariants(proj, item, log.registry)
            if item["kind"] in LIFECYCLE_ACT_KINDS:
                if proj is None:
                    proj = project(tuple(staged), log.registry)
                if item["kind"] == "horizon-genesis":
                    _enforce_second_genesis_rule(proj, item["payload"])
                if (
                    item["kind"] == "member-transition"
                    and not member_restoration_is_on_removal_lineage(proj, item["payload"])
                ):
                    raise FindingModelError(
                        "restored member transition must descend from its recorded removal horizon"
                    )
                apply_act(proj, item, log.registry)
            known.add(item["act_id"])
            staged.append(item)
        except Exception:
            refused_at.append(index)
            raise
    log._path.parent.mkdir(parents=True, exist_ok=True)
    pending = log._path.with_name(log._path.name + PENDING_SUFFIX)
    with pending.open("wb") as handle:
        handle.write(raw)
        for item in acts:
            line = json.dumps(item, sort_keys=True, separators=(",", ":")).encode("utf-8")
            ActLog._write_pending_line(log, handle, line + b"\n")
        handle.flush()
        os.fsync(handle.fileno())
    on_disk = log._path.stat().st_size if log._path.exists() else 0
    if on_disk != len(raw):
        pending.unlink()
        raise ActLogError(
            "stale revision: the act log changed during the save; nothing was written"
        )
    os.replace(pending, log._path)
    _fsync_directory(log._path.parent)
    return current + len(acts)


class SaveFoldEquivalence(TestCase):
    def setUp(self) -> None:
        import tempfile

        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.root = Path(self._tmp.name)
        schema_dir = self.root / "schemas"
        schema_dir.mkdir()
        self.registry = registry_with_demo_kinds(schema_dir)
        self._n = 0

    def _log(self, seed: bytes = b"") -> ActLog:
        self._n += 1
        workspace = self.root / f"ws-{self._n}"
        workspace.mkdir()
        log = ActLog(workspace, self.registry, undeclared_test_log=True)
        if seed:
            log.path.write_bytes(seed)
        return log

    def _commit(self, items: list[dict[str, Any]]) -> bytes:
        log = self._log()
        for index, item in enumerate(items):
            log.append(item, index)
        return log.path.read_bytes()

    def _note(self, index: int) -> dict[str, Any]:
        return demo_note_act(index)

    def _genesis(self, index: int, horizon_id: str = "demo.horizon.genesis") -> dict[str, Any]:
        return act(index, "horizon-genesis", {
            "family": _FAMILY,
            "scope": _SCOPE,
            "horizon_id": horizon_id,
        })

    def _bad_contribution(self, index: int) -> dict[str, Any]:
        return act(index, "contribution", {"contribution": {
            "schema": "contribution.v1",
            "id": "demo-contribution-missing",
            "evidence_id": "demo-evidence-missing",
            "content": {"label": "synthetic"},
        }})

    def _transition(self, index: int) -> dict[str, Any]:
        return act(index, "member-transition", {
            "family": _FAMILY,
            "scope": _SCOPE,
            "member": {"action": "remove", "fact_id": "demo.fact.missing"},
            "successor": {"id": "demo.horizon.successor", "predecessor": "demo.horizon.missing"},
        })

    def _comment_type(self) -> dict[str, Any]:
        return {
            "schema": "fact-type.v1",
            "id": "demo.payment-comment",
            "title": "Comment on a demo payment",
            "nature": "determinable",
            "identity_keys": [
                {"name": "counterparty", "kind": "entity", "entity_kind": "demo.counterparty"},
                {"name": "period", "kind": "literal", "values": ["2025"]},
                {"name": "comment", "kind": "literal", "values": ["noted"]},
            ],
            "value_schema": {"type": "string"},
            "supersession": {"policy": "free"},
        }

    def _comment_fact_id(self) -> str:
        return fact_id_for("demo.payment-comment", _COMMENT_KEYS)

    @contextmanager
    def _intruding(self, expected_revision: int) -> Iterator[None]:
        real = ActLog._write_pending_line
        done = False

        def intrude(log: ActLog, handle: Any, line: bytes) -> None:
            nonlocal done
            if not done:
                done = True
                intruder = ActLog(log.path.parent, self.registry, undeclared_test_log=True)
                intruder.append(demo_note_act(expected_revision), expected_revision)
            real(log, handle, line)

        with mock.patch.object(ActLog, "_write_pending_line", intrude):
            yield

    def _run(
        self,
        log: ActLog,
        call: Callable[[], int],
        intrude: bool,
        expected_revision: int,
    ) -> _View:
        caught: Exception | None = None
        revision: int | None = None
        try:
            if intrude:
                with self._intruding(expected_revision):
                    revision = call()
            else:
                revision = call()
        except Exception as exc:
            caught = exc
            revision = None
        pending = log.path.with_name(log.path.name + PENDING_SUFFIX).exists()
        raw = log.path.read_bytes() if log.path.exists() else b""
        contents = ActLog(log.path.parent, self.registry, read_only=True).read()
        return _View(
            exc_type=None if caught is None else type(caught).__name__,
            message=None if caught is None else str(caught),
            revision=revision,
            log_bytes=raw,
            pending=pending,
            tail=contents.incomplete_tail,
            read_revision=contents.revision,
        )

    def _observed_refused_index(
        self,
        seed: bytes,
        batch: list[dict[str, Any]],
        expected_revision: int,
        intrude: bool,
    ) -> int | None:
        full = self._log(seed)
        try:
            if intrude:
                with self._intruding(expected_revision):
                    full.append_batch(batch, expected_revision)
            else:
                full.append_batch(batch, expected_revision)
        except Exception as exc:
            message = str(exc)
            exc_type = type(exc).__name__
        else:
            return None
        if (
            message.startswith("stale revision: expected")
            or "changed during the save" in message
            or "uncommitted partial tail" in message
        ):
            return None
        for end in range(1, len(batch) + 1):
            earlier = self._log(seed)
            try:
                earlier.append_batch(batch[:end], expected_revision)
            except Exception as exc:
                if type(exc).__name__ == exc_type and str(exc) == message:
                    return end - 1
                return end - 1
        self.fail("the batch refused but no prefix refused")
        return None

    def _compare(
        self,
        seed: bytes,
        batch: list[dict[str, Any]],
        expected_revision: int,
        *,
        intrude: bool = False,
    ) -> tuple[_View, int | None]:
        refused_at: list[int] = []
        oracle_log = self._log(seed)
        impl_log = self._log(seed)
        oracle_view = self._run(
            oracle_log,
            lambda: _fresh_project_append_batch(
                oracle_log, batch, expected_revision, refused_at
            ),
            intrude,
            expected_revision,
        )
        impl_view = self._run(
            impl_log,
            lambda: impl_log.append_batch(batch, expected_revision),
            intrude,
            expected_revision,
        )
        oracle_index = refused_at[0] if refused_at else None
        impl_index = self._observed_refused_index(seed, batch, expected_revision, intrude)
        self.assertEqual(impl_view, oracle_view)
        self.assertEqual(impl_index, oracle_index)
        return impl_view, impl_index

    def test_incremental_fold_matches_fresh_projection_of_each_prefix(self) -> None:
        other = self._genesis(2, "demo.horizon.other")
        other["payload"] = {
            "family": {"id": "demo.family.other", "version": "v1"},
            "scope": _SCOPE,
            "horizon_id": "demo.horizon.other",
        }
        acts = [self._note(0), self._genesis(1), other, self._note(3)]
        fold = _SaveFold(self.registry)
        for end in range(len(acts) + 1):
            self.assertEqual(
                fold.through(acts[:end]),
                project(tuple(acts[:end]), self.registry),
            )
        whole = _SaveFold(self.registry)
        self.assertEqual(whole.through(acts), project(tuple(acts), self.registry))
        failing = _SaveFold(self.registry)
        with self.assertRaises(FindingModelError) as incremental:
            failing.through([self._bad_contribution(0)])
        with self.assertRaises(FindingModelError) as fresh:
            project((self._bad_contribution(0),), self.registry)
        self.assertEqual(str(incremental.exception), str(fresh.exception))

    def test_valid_and_mixed_batches_match_and_prefix_reads_agree(self) -> None:
        valid = [self._note(index) for index in range(3)]
        mixed = [self._note(0), self._genesis(1), self._note(2)]
        for batch in (valid, mixed):
            with self.subTest(kinds=[item["kind"] for item in batch]):
                view, refused = self._compare(b"", batch, 0)
                self.assertIsNone(view.exc_type)
                self.assertIsNone(refused)
                self.assertEqual(view.revision, 3)
                self.assertFalse(view.pending)
                self.assertIsNone(view.tail)
                sequential = self._log()
                for index, item in enumerate(batch):
                    sequential.append(item, index)
                self.assertEqual(view.log_bytes, sequential.path.read_bytes())
                saved = self._log(view.log_bytes).read().acts
                other = sequential.read().acts
                for end in range(len(saved) + 1):
                    self.assertEqual(
                        project(saved[:end], self.registry),
                        project(other[:end], self.registry),
                    )

    def test_stale_revision_duplicate_ids_and_committed_against(self) -> None:
        stale_view, stale_index = self._compare(b"", [self._note(0)], 4)
        self.assertIsNone(stale_index)
        self.assertEqual(stale_view.exc_type, "ActLogError")
        self.assertEqual(stale_view.message, "stale revision: expected 4, workspace is at 0")
        self.assertEqual(stale_view.log_bytes, b"")
        self.assertFalse(stale_view.pending)

        seeded = self._commit([self._note(0)])
        in_log = self._note(1)
        in_log["act_id"] = "demo-act-000"
        log_view, log_index = self._compare(seeded, [in_log], 1)
        self.assertEqual(log_index, 0)
        self.assertEqual(log_view.exc_type, "ActLogError")
        self.assertEqual(log_view.message, "duplicate act_id: demo-act-000")
        self.assertEqual(log_view.log_bytes, seeded)
        self.assertFalse(log_view.pending)

        first = self._note(0)
        second = self._note(1)
        second["act_id"] = first["act_id"]
        batch_view, batch_index = self._compare(b"", [first, second], 0)
        self.assertEqual(batch_index, 1)
        self.assertEqual(batch_view.message, f"duplicate act_id: {first['act_id']}")
        self.assertEqual(batch_view.log_bytes, b"")

        gap = self._note(1)
        gap["committed_against"] = 5
        gap_view, gap_index = self._compare(b"", [self._note(0), gap], 0)
        self.assertEqual(gap_index, 1)
        self.assertEqual(
            gap_view.message,
            "act commits against revision 5, batch position is revision 1",
        )
        self.assertEqual(gap_view.log_bytes, b"")
        self.assertFalse(gap_view.pending)

    def test_lifecycle_and_new_write_failures_later_in_a_batch(self) -> None:
        second = self._genesis(2, "demo.horizon.second")
        chain_view, chain_index = self._compare(
            b"", [self._note(0), self._genesis(1), second], 0
        )
        self.assertEqual(chain_index, 2)
        self.assertEqual(chain_view.exc_type, "HorizonModelError")
        self.assertEqual(chain_view.message, "active chain already exists in scope")
        self.assertEqual(chain_view.log_bytes, b"")
        self.assertFalse(chain_view.pending)
        prefix, prefix_index = self._compare(b"", [self._note(0), self._genesis(1)], 0)
        self.assertIsNone(prefix.exc_type)
        self.assertIsNone(prefix_index)
        self.assertEqual(prefix.revision, 2)

        transition_view, transition_index = self._compare(
            b"", [self._note(0), self._transition(1)], 0
        )
        self.assertEqual(transition_index, 1)
        self.assertEqual(transition_view.exc_type, "HorizonModelError")
        self.assertIn("genesis is required first", transition_view.message or "")
        self.assertEqual(transition_view.log_bytes, b"")

        self.registry.scoped_supersession_declarations = [_DECLARATION]  # type: ignore[attr-defined]
        try:
            comment_id = self._comment_fact_id()
            bundle = demo_bundle()
            bundle["fact_types"] = [
                demo_fact_type_payment(),
                demo_fact_type_rate_choice(),
                self._comment_type(),
            ]
            seed = self._commit([
                act(0, "bundle-adoption", {"bundle": bundle}),
                act(1, "entity-introduced", {"entity": demo_entity("demo-corp-a", "Corp A")}),
                act(2, "evidence-submitted", {"evidence": demo_evidence()}),
                act(3, "assertion", {"finding": demo_finding("demo-finding-original", value=1200)}),
                act(4, "assertion", {"finding": demo_finding(
                    "demo-finding-comment", fact_id=comment_id, value="noted",
                )}),
            ])
            rewritten = act(6, "assertion", {"finding": demo_finding(
                "demo-finding-rewritten",
                fact_id=demo_payment_fact_id(),
                value=1800,
            )})
            view, refused = self._compare(seed, [self._note(5), rewritten], 5)
        finally:
            del self.registry.scoped_supersession_declarations  # type: ignore[attr-defined]
        self.assertEqual(refused, 1)
        self.assertEqual(view.exc_type, "FindingModelError")
        self.assertIn("scoped supersession violated", view.message or "")
        self.assertIn("demo-finding-rewritten", view.message or "")
        self.assertEqual(view.log_bytes, seed)
        self.assertFalse(view.pending)
        self.assertEqual(view.read_revision, 5)

    def test_unchecked_fold_failure_is_admitted_until_a_later_checked_act(self) -> None:
        alone, alone_index = self._compare(b"", [self._bad_contribution(0)], 0)
        self.assertIsNone(alone.exc_type)
        self.assertIsNone(alone_index)
        self.assertEqual(alone.revision, 1)
        self.assertFalse(alone.pending)
        admitted = self._log(alone.log_bytes)
        with self.assertRaises(FindingModelError) as folded:
            project(admitted.read().acts, self.registry)
        self.assertIn("demo-contribution-missing", str(folded.exception))
        self.assertIn("non-current evidence", str(folded.exception))

        followed, followed_index = self._compare(
            b"", [self._bad_contribution(0), self._genesis(1)], 0
        )
        self.assertEqual(followed_index, 1)
        self.assertEqual(followed.exc_type, "FindingModelError")
        self.assertEqual(str(folded.exception), followed.message)
        self.assertEqual(followed.log_bytes, b"")
        self.assertFalse(followed.pending)

        gap = self._genesis(1)
        gap["committed_against"] = 5
        mismatch, mismatch_index = self._compare(
            b"", [self._bad_contribution(0), gap], 0
        )
        self.assertEqual(mismatch_index, 1)
        self.assertEqual(mismatch.exc_type, "ActLogError")
        self.assertEqual(
            mismatch.message,
            "act commits against revision 5, batch position is revision 1",
        )
        self.assertNotIn("non-current evidence", mismatch.message or "")
        self.assertEqual(mismatch.log_bytes, b"")

    def test_a_later_unchecked_save_does_not_fold_an_admitted_failure(self) -> None:
        admitted, _index = self._compare(b"", [self._bad_contribution(0)], 0)
        note_view, note_index = self._compare(admitted.log_bytes, [self._note(1)], 1)
        self.assertIsNone(note_view.exc_type)
        self.assertIsNone(note_index)
        self.assertEqual(note_view.revision, 2)
        self.assertTrue(note_view.log_bytes.startswith(admitted.log_bytes))

        single = self._log(admitted.log_bytes)
        before = single.path.read_bytes()
        self.assertEqual(single.append(self._note(1), 1), 2)
        grown = single.path.read_bytes()
        self.assertTrue(grown.startswith(before))
        with self.assertRaises(FindingModelError) as refused:
            single.append(self._genesis(2), 2)
        self.assertIn("non-current evidence", str(refused.exception))
        self.assertEqual(single.path.read_bytes(), grown)
        batch = self._log(grown)
        with self.assertRaises(FindingModelError) as batched:
            batch.append_batch([self._genesis(2)], 2)
        self.assertEqual(str(batched.exception), str(refused.exception))
        self.assertEqual(batch.path.read_bytes(), grown)
        self.assertFalse(batch.path.with_name(batch.path.name + PENDING_SUFFIX).exists())
        with self.assertRaises(FindingModelError) as historical:
            project(batch.read().acts, self.registry)
        self.assertEqual(str(historical.exception), str(refused.exception))

    def test_incomplete_tail_is_refused_and_left_in_place(self) -> None:
        seed = self._commit([self._note(0), self._note(1)])
        torn = seed + b'{"schema":"act.v1"'
        view, refused = self._compare(torn, [self._note(2)], 2)
        self.assertIsNone(refused)
        self.assertEqual(view.exc_type, "ActLogError")
        self.assertEqual(
            view.message,
            "act log has an uncommitted partial tail; a batch is not written onto it",
        )
        self.assertEqual(view.log_bytes, torn)
        self.assertFalse(view.pending)
        self.assertEqual(view.read_revision, 2)
        self.assertIsNotNone(view.tail)

    def test_size_change_after_pending_creation_unlinks_pending_and_keeps_the_other_write(self) -> None:
        seed = self._commit([self._note(0), self._note(1)])
        view, refused = self._compare(
            seed, [self._note(2), self._note(3)], 2, intrude=True
        )
        self.assertIsNone(refused)
        self.assertEqual(view.exc_type, "ActLogError")
        self.assertEqual(
            view.message,
            "stale revision: the act log changed during the save; nothing was written",
        )
        self.assertFalse(view.pending)
        intruder = self._log(seed)
        intruder.append(self._note(2), 2)
        self.assertEqual(view.log_bytes, intruder.path.read_bytes())
        self.assertEqual(view.read_revision, 3)
        self.assertIsNone(view.tail)


if __name__ == "__main__":
    import unittest

    unittest.main()
