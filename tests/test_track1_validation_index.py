"""Track 1 (rust-kernel-experiment): package validation's source-family index.

Loads the whole published v96 corpus (about 16 s), so it is an honest live-lane
test. It pins the issue multiset, the output owners and the resolved members
that the unindexed validator (commit 0763f572) gave on the published v96
package and on four invalid mutations of it.
"""
from __future__ import annotations

import copy
import unittest
from typing import Any

import pytest

pytestmark = pytest.mark.live

# Digests initially recorded from the unindexed validator at commit 0763f572
# and updated for artifact-package.v43 exact-entrypoint enforcement (v96 uses
# artifact-package.v43, so the three invalid mutations additionally report +41
# ENTRYPOINT_DANGLING, +75 ENTRYPOINT_DANGLING, and +2
# ENTRYPOINT_VERSION_MISMATCH respectively; non-entrypoint issues,
# resolved_members, and output_owners are identical). Each is (issue count,
# multiset digest, resolved-members digest, output-owners digest).
_PRISTINE = {
    "published_v96": (0, "e3b0c44298fc1c14", "a2bdf1bc3f1c1aa4", "d6d653b4820066a5"),
    "mutation_remove_source_families": (252, "6801ac05944388ad", "c15e47fa7ce18028", "d6d653b4820066a5"),
    "mutation_drop_every_seventh": (402, "1d602e1dc5c116b3", "9b1131bb1a7bfabc", "66630d57a868f597"),
    "mutation_unknown_versions": (5, "22a606d28c2c6076", "c6eb61717bd07560", "072f3f4aa0373e7b"),
    "mutation_tampered_citizens": (9, "6a99c9579ebbc23b", "a218fdb14f5cc57a", "d6d653b4820066a5"),
}


def _sha(value: Any) -> str:
    import hashlib
    import json
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":"), default=repr)
                          .encode("utf-8")).hexdigest()


class SourceFamilyIndex(unittest.TestCase):
    def test_validation_matches_the_unindexed_validator(self) -> None:
        import hashlib
        import json
        from packages.derivation.loader import DerivationSchemas
        from packages.derivation.package_validation import load_published_citizen_checksums, validate_package
        from tools import recorded_replay as rr
        from tools.package_successor import load_corpus

        core = rr.resolve_core("v96")
        corpus, _ = load_corpus(rr.CONTENT)
        schemas = DerivationSchemas()
        checks = load_published_citizen_checksums(core.content / f"published-packages.{core.registry}.json")
        package = json.loads(core.package_path.read_text(encoding="utf-8"))
        members = package["members"]

        cases: dict[str, tuple[dict[str, Any], dict[Any, Any]]] = {"published_v96": (package, corpus)}
        pkg1 = copy.deepcopy(package)
        pkg1["members"] = [m for m in pkg1["members"]
                           if not (corpus.get((m["id"], m["version"])) or {}).get("schema", "").startswith("source-family")]
        cases["mutation_remove_source_families"] = (pkg1, corpus)
        pkg2 = copy.deepcopy(package)
        pkg2["members"] = [m for i, m in enumerate(pkg2["members"]) if i % 7 != 3]
        cases["mutation_drop_every_seventh"] = (pkg2, corpus)
        pkg3 = copy.deepcopy(package)
        pkg3["members"][5]["version"] = "v999"
        pkg3["members"][len(pkg3["members"]) // 2]["version"] = "v998"
        cases["mutation_unknown_versions"] = (pkg3, corpus)
        corp4 = dict(corpus)
        for index in (1, 17, 41, 103):
            pin = members[index]
            body = copy.deepcopy(corp4[(pin["id"], pin["version"])])
            body["demo_tamper"] = index
            corp4[(pin["id"], pin["version"])] = body
        cases["mutation_tampered_citizens"] = (package, corp4)

        for name, (pkg, corp) in cases.items():
            with self.subTest(case=name):
                result = validate_package(pkg, corp, schemas, checks)
                rows = sorted(json.dumps([i.member_id, i.version, i.code, i.detail]) for i in result.issues)
                got = (len(rows), hashlib.sha256("\n".join(rows).encode()).hexdigest()[:16],
                       _sha(result.resolved_members)[:16], _sha(result.output_owners)[:16])
                self.assertEqual(got, _PRISTINE[name])


if __name__ == "__main__":
    unittest.main()
