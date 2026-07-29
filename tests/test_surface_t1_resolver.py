"""Track 1 — surface artifact resolver (Legible Entry, Packaging the Surface).

The surface artifact is a second, separate container from `artifact-package.v4`
carrying opaque UI program bytes: a source tree, a lockfile, and a vendored
dependency tree, each entry checked by SHA-256 and never parsed for meaning.
It reuses ADR-0033's release-rooted adoption and release/registry verification
chain (`production_resolver.py`) rather than a second, independently written
one; it diverges only where the shape must — a manifest citizen with raw-file
entries in place of a validated rule-package member graph. All fixtures
synthetic (`demo.*`), no personal data, no residency locator.
"""

from __future__ import annotations

import json
import shutil
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any

from packages.derivation.production_resolver import PublicationSurface, Refusal
from packages.derivation.surface_resolver import ResolvedSurface, resolve_surface_artifact
from tools.generate_surface_t1_fixtures import content_stats, render_fixture_files

REPO = Path(__file__).resolve().parent.parent
SURFACE_T1 = REPO / "packages" / "sample_data" / "surface_t1"
CONTENT_DIR = SURFACE_T1 / "content" / "app"
ADOPTIONS = SURFACE_T1 / "adoptions"

SCOPE_USER = "demo.user.filer-1"
CLEAN_SCOPE = {"jurisdiction": "us", "year": "2025"}

# The vendored dependency tree ships in the surface artifact but is not stored
# in this repository (owner decision 2026-07-28, see .gitignore). Without it the
# manifest names entries that are not on disk, so these tests cannot run. Restore
# it with `npm ci` in the content directory, then regenerate the fixtures.
_VENDORED = (CONTENT_DIR / "node_modules").is_dir()
_NEEDS_VENDORED = "vendored dependency tree absent; run `npm ci` in packages/sample_data/surface_t1/content/app"


def _act(name: str) -> dict[str, Any]:
    value = json.loads((ADOPTIONS / name).read_text("utf-8"))
    assert isinstance(value, dict)
    return value


def _surface(
    member_dir: Path | None = None,
    registry: Path | None = None,
    release_dir: Path | None = None,
) -> PublicationSurface:
    return PublicationSurface(
        release_dir=release_dir or (SURFACE_T1 / "publication_surface" / "releases"),
        package_registry_path=registry or (SURFACE_T1 / "registry" / "published-surface-artifacts.json"),
        member_dir=member_dir or (SURFACE_T1 / "manifest"),
    )


def _resolve(content_dir: Path | None = None, surface: PublicationSurface | None = None) -> ResolvedSurface | Refusal:
    return resolve_surface_artifact(
        [_act("adopt-surface-entry-page-v1.json")],
        run_scope=CLEAN_SCOPE,
        scope_user=SCOPE_USER,
        workspace_revision=10,
        surface=surface or _surface(),
        content_dir=content_dir or CONTENT_DIR,
    )


@unittest.skipUnless(_VENDORED, _NEEDS_VENDORED)
class ProvenanceRegeneration(unittest.TestCase):
    def test_fixtures_regenerate_from_the_content_tree(self) -> None:
        rendered = render_fixture_files()
        on_disk = {relative: (SURFACE_T1 / relative).read_bytes() for relative in rendered}
        self.assertEqual(on_disk, rendered)


class DataSafety(unittest.TestCase):
    """Runs everywhere. The vendored tree's absence must never skip this."""

    def test_content_tree_is_synthetic_and_locator_free(self) -> None:
        paths = [
            *SURFACE_T1.rglob("*.json"),
            REPO / "packages" / "derivation" / "surface_resolver.py",
            REPO / "tools" / "generate_surface_t1_fixtures.py",
        ]
        forbidden = ("/Users/", "/private/", "local-data/", "uploads/", "generated/user/")
        for path in paths:
            with self.subTest(path=path):
                self.assertFalse(any(marker in path.read_text("utf-8") for marker in forbidden))


@unittest.skipUnless(_VENDORED, _NEEDS_VENDORED)
class CleanResolution(unittest.TestCase):
    def test_clean_adoption_resolves_every_verified_entry(self) -> None:
        r = _resolve()
        self.assertIsInstance(r, ResolvedSurface)
        assert isinstance(r, ResolvedSurface)
        self.assertEqual(r.adoption_act_id, "act.adopt.surface.entry-page.v1")
        self.assertEqual(r.release_id, "demo.surface-release.2025")
        count, total = content_stats()
        self.assertEqual(r.entry_count, count)
        self.assertEqual(r.total_bytes, total)
        self.assertGreater(r.entry_count, 900)  # the real vendored svelte tree, not a stub

    def test_measured_cost_is_recorded_and_real(self) -> None:
        count, total = content_stats()
        # A sanity band, not a tight bound: this is the number Track 2's ADR
        # must justify to the owner. It should never silently become a stub.
        self.assertGreater(count, 500)
        self.assertLess(total, 50_000_000)  # a boring page's tree, not a bundler toolchain


@unittest.skipUnless(_VENDORED, _NEEDS_VENDORED)
class DigestMismatchRefusal(unittest.TestCase):
    """The refusal case is part of the deliverable, not a follow-up."""

    def test_corrupted_shipped_byte_refuses(self) -> None:
        with TemporaryDirectory() as tmp:
            content = Path(tmp) / "app"
            shutil.copytree(CONTENT_DIR, content)
            target = content / "src" / "EntryPage.svelte"
            corrupted = target.read_bytes() + b"\n// tampered\n"
            target.write_bytes(corrupted)
            r = _resolve(content_dir=content)
        self.assertIsInstance(r, Refusal)
        assert isinstance(r, Refusal)
        self.assertEqual(r.reason, "SURFACE_ENTRY_CHECKSUM_MISMATCH")

    def test_missing_shipped_entry_refuses(self) -> None:
        with TemporaryDirectory() as tmp:
            content = Path(tmp) / "app"
            shutil.copytree(CONTENT_DIR, content)
            (content / "build.mjs").unlink()
            r = _resolve(content_dir=content)
        self.assertIsInstance(r, Refusal)
        assert isinstance(r, Refusal)
        self.assertEqual(r.reason, "SURFACE_ENTRY_ABSENT")

    def test_path_escaping_entry_is_confined_not_followed(self) -> None:
        with TemporaryDirectory() as tmp:
            content = Path(tmp) / "app"
            shutil.copytree(CONTENT_DIR, content)
            outside = Path(tmp) / "outside.txt"
            outside.write_bytes(b"not part of the artifact")
            # A symlinked entry path pointing outside the confined content
            # root must never be followed and admitted as if it were inside.
            (content / "build.mjs").unlink()
            (content / "build.mjs").symlink_to(outside)
            r = _resolve(content_dir=content)
        self.assertIsInstance(r, Refusal)
        assert isinstance(r, Refusal)
        self.assertEqual(r.reason, "SURFACE_ENTRY_NOT_CONFINED")

    def test_tampered_manifest_body_refuses_before_any_entry_is_read(self) -> None:
        with TemporaryDirectory() as tmp:
            manifest_dir = Path(tmp) / "manifest"
            manifest_dir.mkdir()
            manifest = json.loads((SURFACE_T1 / "manifest" / "surface-artifact.entry-page.v1.json").read_text())
            manifest["entries"] = list(manifest["entries"]) + [
                {"path": "injected.txt", "sha256": "0" * 64, "bytes": 0}
            ]
            (manifest_dir / "surface-artifact.entry-page.v1.json").write_text(json.dumps(manifest))
            r = _resolve(surface=_surface(member_dir=manifest_dir))
        self.assertIsInstance(r, Refusal)
        assert isinstance(r, Refusal)
        self.assertEqual(r.reason, "SURFACE_ABSENT_OR_MISMATCH")

    def test_replaced_registry_bytes_under_honest_release_refuses(self) -> None:
        with TemporaryDirectory() as tmp:
            reg = Path(tmp) / "published-surface-artifacts.json"
            doc = json.loads((SURFACE_T1 / "registry" / "published-surface-artifacts.json").read_text())
            original = doc["packages"][0]["checksum"]
            doc["packages"][0]["checksum"] = original[:-1] + ("0" if original[-1] != "0" else "1")
            reg.write_text(json.dumps(doc, indent=2, sort_keys=True) + "\n")
            r = _resolve(surface=_surface(registry=reg))
        self.assertIsInstance(r, Refusal)
        assert isinstance(r, Refusal)
        self.assertEqual(r.reason, "REGISTRY_CHECKSUM_MISMATCH")


class DistinctAdoptionKind(unittest.TestCase):
    """A surface adoption is a different act kind, never selected as a package adoption."""

    def test_surface_adoption_kind_never_selected_as_a_package_adoption(self) -> None:
        from packages.derivation.production_resolver import select_current_adoption
        from packages.derivation.loader import DerivationSchemas

        r = select_current_adoption(
            [_act("adopt-surface-entry-page-v1.json")],
            run_scope=CLEAN_SCOPE,
            scope_user=SCOPE_USER,
            workspace_revision=10,
            schemas=DerivationSchemas(),
        )  # default expected_kind="package-adoption"
        self.assertIsInstance(r, Refusal)
        assert isinstance(r, Refusal)
        self.assertEqual(r.reason, "ADOPTION_NONE_CURRENT")

    def test_non_user_surface_adoption_refuses(self) -> None:
        act = _act("adopt-surface-entry-page-v1.json")
        act["actor"] = "automation.bot"
        r = resolve_surface_artifact(
            [act], run_scope=CLEAN_SCOPE, scope_user=SCOPE_USER, workspace_revision=10,
            surface=_surface(), content_dir=CONTENT_DIR,
        )
        self.assertIsInstance(r, Refusal)
        assert isinstance(r, Refusal)
        self.assertEqual(r.reason, "ADOPTION_NONE_CURRENT")


if __name__ == "__main__":
    unittest.main()
