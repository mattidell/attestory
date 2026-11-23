"""Validation reuses the member cache's checksums (validation-checksum-reuse).

The validation memo key and ``validate_package`` take each corpus body's
canonical checksum from the member cache entry the body was just copied
from, instead of recomputing it. These tests pin the contract on a synthetic
``demo.*`` member directory:

* the reused checksums are the checksums of the corpus bodies, and the memo
  key built from them equals the key built by recomputing;
* a citizen changed after a cached read is still caught: an edited file
  (same size and modification time) is refused at admission, a mutated view
  value or returned body cannot reach the shared parse, and a corpus handed
  to validation without the resolver's checksums is checksummed as before;
* the memo key changes when any member's bytes change;
* the checksums live only in the member cache: the existing clear hooks
  (``clear_member_cache``, ``clear_validation_memo``) clear them.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
import tempfile
import unittest
from typing import Any, Callable, cast
from unittest import mock

from packages.derivation import package_validation as pv
from packages.derivation import production_resolver as pr
from packages.derivation.package_validation import PackageValidation, citizen_checksum, validate_package

_DOCS: dict[str, dict[str, Any]] = {
    "a.json": {"id": "demo.vcr.a", "version": "v1", "schema": "citation.v1", "n": 1,
               "nested": {"xs": [1, 2, "s"]}},
    "b.json": {"id": "demo.vcr.b", "version": "v2", "schema": "citation.v1", "n": 2, "items": [{"k": "v"}]},
    "sub/c.json": {"id": "demo.vcr.c", "version": "v1", "schema": "citation.v1", "n": 3},
    "other.json": {"id": "demo.vcr.unpinned", "version": "v1", "n": 4},
}


class _Schemas:
    """Accepts every document; enough for the checksum step of validate_package."""

    def validate_declared(self, document: Any) -> None:
        return None

    def schema_ids(self) -> list[str]:
        return ["demo.schema.v1"]

    def get(self, schema_id: str) -> Any:
        return {"type": "object"}


def _package() -> dict[str, Any]:
    pins = [{"id": body["id"], "version": body["version"], "role": "citation"}
            for name, body in sorted(_DOCS.items()) if name != "other.json"]
    return {"id": "demo.vcr.package", "version": "v1", "scope": {}, "members": pins}


class _Counter:
    def __init__(self) -> None:
        self.calls = 0
        self.real = pv.citizen_checksum

    def __call__(self, citizen: dict[str, Any]) -> str:
        self.calls += 1
        return self.real(citizen)


class ValidationChecksumReuse(unittest.TestCase):
    def setUp(self) -> None:
        pr.clear_member_cache()
        pr.clear_validation_memo()
        self.addCleanup(pr.clear_member_cache)
        self.addCleanup(pr.clear_validation_memo)
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name)
        (self.root / "sub").mkdir()
        for name, body in _DOCS.items():
            (self.root / name).write_text(json.dumps(body), "utf-8")
        self.surface = pr.PublicationSurface(self.root, self.root / "registry.json", self.root)
        self.schemas = cast(Any, _Schemas())
        self.checks = self.registry()

    def registry(self) -> dict[tuple[str, str], str]:
        """The published checksums of the files as they are now on disk."""
        out = {}
        for path in sorted(self.root.rglob("*.json")):
            body = json.loads(path.read_text("utf-8"))
            out[(body["id"], body["version"])] = citizen_checksum(body)
        return out

    def admit(self) -> tuple[dict[tuple[str, str], dict[str, Any]], dict[tuple[str, str], str]]:
        admitted = pr._resolve_member_corpus(_package(), self.surface, self.checks)
        assert not isinstance(admitted, pr.Refusal), admitted
        return admitted

    def counted(self, call: Callable[[], Any]) -> tuple[Any, int]:
        counter = _Counter()
        with mock.patch.object(pr, "citizen_checksum", counter), mock.patch.object(pv, "citizen_checksum", counter):
            return call(), counter.calls

    def edit_same_size_and_mtime(self, name: str, old: bytes, new: bytes) -> None:
        target = self.root / name
        before = target.read_bytes()
        stat = target.stat()
        after = before.replace(old, new)
        self.assertNotEqual(before, after)
        self.assertEqual(len(before), len(after))
        target.write_bytes(after)
        os.utime(target, ns=(stat.st_atime_ns, stat.st_mtime_ns))

    # --- the reused checksums are the checksums of the bodies ---------------------------------

    def test_reused_checksums_are_the_corpus_bodies_checksums_and_give_the_same_key(self) -> None:
        for _ in range(2):  # a miss, then a hit of every file
            corpus, sums = self.admit()
            self.assertEqual(set(sums), set(corpus))
            self.assertEqual(sums, {key: citizen_checksum(body) for key, body in corpus.items()})
            self.assertEqual(sums, {key: self.checks[key] for key in corpus})
            self.assertEqual(pr._validation_memo_key(_package(), corpus, self.checks, self.schemas, sums),
                             pr._validation_memo_key(_package(), corpus, self.checks, self.schemas))

    def test_a_warm_resolution_and_validation_compute_no_checksum(self) -> None:
        self.admit()  # warms the member cache

        def resolve_and_validate() -> PackageValidation:
            corpus, sums = self.admit()
            return pr._validate_once(_package(), corpus, self.schemas, self.checks, sums)

        warm, calls = self.counted(resolve_and_validate)
        self.assertEqual(calls, 0)
        pr.clear_validation_memo()
        corpus, _ = self.admit()
        plain, plain_calls = self.counted(lambda: validate_package(_package(), corpus, self.schemas, self.checks))
        self.assertEqual(plain_calls, len(corpus))  # the plain call still checksums every member
        self.assertEqual(warm, plain)
        self.assertTrue(warm.ok)

    def test_validate_package_uses_a_given_checksum_and_computes_a_missing_one(self) -> None:
        corpus, sums = self.admit()
        key = sorted(corpus)[0]
        forged = {**sums, key: "0" * 64}
        result = validate_package(_package(), corpus, self.schemas, self.checks, corpus_checksums=forged)
        self.assertEqual([(i.member_id, i.code) for i in result.issues], [(key[0], "MEMBER_CHECKSUM_MISMATCH")])
        partial = {k: v for k, v in sums.items() if k != key}
        corpus[key]["demo_tamper"] = 1
        result = validate_package(_package(), corpus, self.schemas, self.checks, corpus_checksums=partial)
        self.assertEqual([(i.member_id, i.code) for i in result.issues], [(key[0], "MEMBER_CHECKSUM_MISMATCH")])

    # --- a citizen mutated after a cached read is still caught --------------------------------

    def test_a_file_edited_after_a_cached_read_is_refused(self) -> None:
        self.admit()
        self.edit_same_size_and_mtime("b.json", b'"n": 2', b'"n": 9')
        refused = pr._resolve_member_corpus(_package(), self.surface, self.checks)
        self.assertIsInstance(refused, pr.Refusal)
        assert isinstance(refused, pr.Refusal)
        self.assertEqual(refused.reason, "MEMBER_ABSENT_OR_MISMATCH")

    def test_mutating_views_and_returned_bodies_cannot_reach_the_shared_parse(self) -> None:
        corpus, sums = self.admit()
        for candidate in pr._member_candidates(self.root):
            for name in list(candidate.view):
                value = candidate.view[name]
                if isinstance(value, dict):
                    value["poison"] = 1
                elif isinstance(value, list):
                    value.append("poison")
            self.assertIsNone(candidate.view.get("absent"))
            self.assertNotIn("poison", json.dumps(dict(candidate.view)))
        for body in corpus.values():
            body["n"] = 99
            for value in body.values():
                if isinstance(value, dict):
                    value["poison"] = 1
        again, again_sums = self.admit()
        self.assertEqual(again_sums, sums)
        on_disk = {(b["id"], b["version"]): b for b in _DOCS.values()}
        self.assertEqual(again, {key: on_disk[key] for key in again})
        self.assertEqual(again_sums, {key: citizen_checksum(body) for key, body in again.items()})
        for entry in pr._MEMBER_CACHE.values():
            self.assertEqual(entry.checksum(), citizen_checksum(entry._body))
            self.assertIn(entry._body, list(_DOCS.values()))

    def test_a_corpus_mutated_without_the_resolver_checksums_is_still_caught(self) -> None:
        corpus, _ = self.admit()
        key = sorted(corpus)[1]
        corpus[key]["demo_tamper"] = True
        result = pr._validate_once(_package(), corpus, self.schemas, self.checks)
        self.assertFalse(result.ok)
        self.assertEqual([(i.member_id, i.code) for i in result.issues], [(key[0], "MEMBER_CHECKSUM_MISMATCH")])

    # --- the memo key changes when any member's bytes change ----------------------------------

    def test_the_memo_key_changes_when_any_members_bytes_change(self) -> None:
        corpus, sums = self.admit()
        original = pr._validation_memo_key(_package(), corpus, self.checks, self.schemas, sums)
        seen = {original}
        for name, old, new in (("a.json", b'"n": 1', b'"n": 5'), ("b.json", b'"k": "v"', b'"k": "w"'),
                               ("sub/c.json", b'"n": 3', b'"n": 6')):
            with self.subTest(member=name):
                self.edit_same_size_and_mtime(name, old, new)
                self.checks = self.registry()  # republished, so admission accepts the new bytes
                corpus, sums = self.admit()
                key = pr._validation_memo_key(_package(), corpus, self.checks, self.schemas, sums)
                self.assertNotIn(key, seen)
                self.assertEqual(key, pr._validation_memo_key(_package(), corpus, self.checks, self.schemas))
                seen.add(key)
                # the corpus part alone moves too, not only the registry part
                self.assertNotEqual(key[3], original[3])

    def test_changed_bytes_validate_again_instead_of_hitting(self) -> None:
        calls: list[dict[str, Any]] = []
        real = pv.validate_package

        def spy(*args: Any, **kwargs: Any) -> PackageValidation:
            calls.append(dict(kwargs.get("corpus_checksums") or {}))
            return real(*args, **kwargs)

        with mock.patch.object(pr, "validate_package", spy):
            for _ in range(2):
                corpus, sums = self.admit()
                pr._validate_once(_package(), corpus, self.schemas, self.checks, sums)
            self.assertEqual(len(calls), 1)  # identical bytes: one validation
            self.edit_same_size_and_mtime("a.json", b'"n": 1', b'"n": 8')
            self.checks = self.registry()
            corpus, sums = self.admit()
            pr._validate_once(_package(), corpus, self.schemas, self.checks, sums)
        self.assertEqual(len(calls), 2)
        self.assertNotEqual(calls[0], calls[1])
        self.assertEqual(calls[1], {key: citizen_checksum(body) for key, body in corpus.items()})

    # --- cleared where the existing clear hooks clear ------------------------------------------

    def test_the_clear_hooks_clear_the_reused_checksums(self) -> None:
        _, calls = self.counted(self.admit)
        self.assertEqual(calls, len(_DOCS))  # cold: each distinct content checksummed once
        _, calls = self.counted(self.admit)
        self.assertEqual(calls, 0)
        corpus, sums = self.admit()
        pr._validate_once(_package(), corpus, self.schemas, self.checks, sums)
        self.assertTrue(pr._MEMBER_CACHE)
        self.assertTrue(pr._VALIDATION_MEMO)
        pr.clear_member_cache()
        self.assertFalse(pr._MEMBER_CACHE)
        _, calls = self.counted(self.admit)
        self.assertEqual(calls, len(_DOCS))  # nothing outside the member cache kept them
        pr.clear_validation_memo()
        self.assertFalse(pr._VALIDATION_MEMO)


if __name__ == "__main__":
    unittest.main()
