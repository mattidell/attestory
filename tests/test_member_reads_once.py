"""Member files are parsed and checksummed once per distinct content (member-reads-once).

The cache in ``production_resolver`` keys on the bytes a call read. These tests
pin its contract on a synthetic member directory: the cached path equals the
old uncached path, a file whose bytes change is re-parsed (even when its size
and modification time do not), no caller can mutate a shared parse, and the
cache is bounded and clearable. Synthetic ``demo.*`` content only.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest import mock

from packages.derivation import production_resolver as pr
from packages.derivation.package_validation import citizen_checksum


def _reference_candidates(directory: Path) -> tuple[dict[str, object], ...]:
    """The pre-cache implementation, verbatim: read text, parse, keep objects."""
    out = []
    for path in sorted(directory.rglob("*.json")):
        try:
            loaded = json.loads(path.read_text("utf-8"))
            if not isinstance(loaded, dict):
                raise ValueError("JSON document must be an object")
            out.append(loaded)
        except (OSError, UnicodeDecodeError, ValueError, json.JSONDecodeError):
            continue
    return tuple(out)


def _write_members(root: Path) -> None:
    (root / "sub").mkdir()
    docs = {
        "a.json": {"id": "demo.member.a", "version": "v2", "nested": {"xs": [1, 2.5, None, True, "s"]}},
        "b.json": {"id": "demo.member.b", "z": 1, "a": 2},
        "sub/c.json": {"schema": "demo.schema.v1", "id": "demo.member.c", "items": [{"k": "v"}, [1, [2]]]},
        "dup.json": {"id": "demo.member.a", "version": "v2", "nested": {"xs": [1, 2.5, None, True, "s"]}},
    }
    for name, body in docs.items():
        (root / name).write_text(json.dumps(body), "utf-8")
    (root / "crlf.json").write_bytes(b'{\r\n  "id": "demo.member.crlf",\r\n  "n": 1\r\n}\r\n')
    (root / "list.json").write_text("[1, 2]", "utf-8")
    (root / "broken.json").write_text("{not json", "utf-8")
    (root / "bom.json").write_bytes(b"\xef\xbb\xbf" + b'{"id": "demo.member.bom"}')
    (root / "latin1.json").write_bytes(b'{"id": "demo.\xe9"}')
    (root / "ignored.txt").write_text('{"id": "demo.member.txt"}', "utf-8")


class MemberReadsOnceTests(unittest.TestCase):
    def setUp(self) -> None:
        pr.clear_member_cache()
        self.addCleanup(pr.clear_member_cache)
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name)
        _write_members(self.root)

    def test_cached_path_equals_uncached_path(self) -> None:
        expected = _reference_candidates(self.root)
        self.assertGreaterEqual(len(expected), 5)
        for _ in range(3):  # a miss, then hits
            self.assertEqual(pr._json_candidates(self.root), expected)
            candidates = pr._member_candidates(self.root)
            self.assertEqual(tuple(dict(c.view) for c in candidates), expected)
            self.assertEqual(tuple(c.body() for c in candidates), expected)
            self.assertEqual(tuple(c.checksum() for c in candidates),
                             tuple(citizen_checksum(b) for b in expected))
            self.assertEqual([list(c.view) for c in candidates], [list(b) for b in expected])

    def test_each_distinct_content_is_parsed_once(self) -> None:
        real = json.loads
        with mock.patch.object(json, "loads", side_effect=real) as spy:
            pr._member_candidates(self.root)
            # a.json and dup.json hold identical bytes: one parse. Four
            # distinct objects (a/dup, b, c, crlf) plus three files that fail
            # to parse (list.json, broken.json, bom.json; latin1.json fails
            # to decode first). Failures are never cached.
            self.assertEqual(spy.call_count, 4 + 3)
            for _ in range(3):
                pr._member_candidates(self.root)
            self.assertEqual(spy.call_count, 4 + 3 + 3 * 3)

    def test_changed_bytes_are_reparsed_even_with_same_size_and_mtime(self) -> None:
        target = self.root / "b.json"
        before = target.read_bytes()
        stat = target.stat()
        first = {c.view["id"]: c for c in pr._member_candidates(self.root)}
        self.assertIn("demo.member.b", first)
        after = before.replace(b"demo.member.b", b"demo.member.X")
        self.assertEqual(len(before), len(after))
        target.write_bytes(after)
        os.utime(target, ns=(stat.st_atime_ns, stat.st_mtime_ns))
        self.assertEqual(target.stat().st_size, stat.st_size)
        self.assertEqual(target.stat().st_mtime_ns, stat.st_mtime_ns)
        ids = {c.view["id"] for c in pr._member_candidates(self.root)}
        self.assertIn("demo.member.X", ids)
        self.assertNotIn("demo.member.b", ids)
        self.assertEqual(pr._json_candidates(self.root), _reference_candidates(self.root))

    def test_changed_content_with_the_same_id_gets_a_new_checksum(self) -> None:
        # A checksum cached per (id, version) rather than per content would
        # pass the test above, which edits the id itself (review MRO-R3).
        target = self.root / "b.json"
        before = target.read_bytes()
        stat = target.stat()
        first = {c.view["id"]: c for c in pr._member_candidates(self.root)}
        old = first["demo.member.b"].checksum()
        after = before.replace(b'"z": 1', b'"z": 7')
        self.assertNotEqual(before, after)
        self.assertEqual(len(before), len(after))
        target.write_bytes(after)
        os.utime(target, ns=(stat.st_atime_ns, stat.st_mtime_ns))
        again = {c.view["id"]: c for c in pr._member_candidates(self.root)}
        edited = again["demo.member.b"]
        self.assertEqual(edited.view["z"], 7)
        self.assertEqual(edited.checksum(), citizen_checksum(edited.body()))
        self.assertNotEqual(edited.checksum(), old)

    def test_file_that_becomes_malformed_or_missing_is_dropped(self) -> None:
        pr._member_candidates(self.root)
        (self.root / "b.json").write_text("{broken", "utf-8")
        (self.root / "a.json").unlink()
        self.assertEqual(pr._json_candidates(self.root), _reference_candidates(self.root))

    def test_mutating_a_returned_body_cannot_reach_a_later_call(self) -> None:
        clean = _reference_candidates(self.root)
        for body in pr._json_candidates(self.root):
            body["id"] = "demo.mutated"
            body["injected"] = True
            for value in list(body.values()):
                if isinstance(value, dict):
                    value["poison"] = 1
                elif isinstance(value, list):
                    value.append("poison")
        for candidate in pr._member_candidates(self.root):
            copy = candidate.body()
            copy["id"] = "demo.mutated"
            if isinstance(copy.get("nested"), dict):
                copy["nested"]["xs"].append("poison")
        self.assertEqual(pr._json_candidates(self.root), clean)
        self.assertEqual(tuple(c.body() for c in pr._member_candidates(self.root)), clean)

    def test_shared_view_is_read_only_and_checksum_is_not_corrupted(self) -> None:
        candidate = pr._member_candidates(self.root)[0]
        with self.assertRaises(TypeError):
            candidate.view["id"] = "demo.mutated"  # type: ignore[index]
        with self.assertRaises(TypeError):
            del candidate.view["id"]  # type: ignore[attr-defined]
        self.assertEqual(candidate.checksum(), citizen_checksum(candidate.body()))

    def test_clear_and_bound(self) -> None:
        pr._member_candidates(self.root)
        self.assertTrue(pr._MEMBER_CACHE)
        pr.clear_member_cache()
        self.assertFalse(pr._MEMBER_CACHE)
        with mock.patch.object(pr, "_MEMBER_CACHE_LIMIT", 3):
            pr._member_candidates(self.root)
            self.assertEqual(len(pr._MEMBER_CACHE), 3)
            self.assertEqual(pr._json_candidates(self.root), _reference_candidates(self.root))

    def test_unreadable_directory_is_empty(self) -> None:
        self.assertEqual(pr._json_candidates(self.root / "absent"), ())


if __name__ == "__main__":
    unittest.main()
