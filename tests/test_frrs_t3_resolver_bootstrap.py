"""Track 3 — production resolver + live workspace bootstrap (ADR-0033).

Every ADR-0033 authority substitution is an executed kill-test, not a stub: forged
release, replaced registry, changed package/member bytes, adoption currency
(stale/tied/non-user), same-key handling, missing pins, filesystem-order
independence, and the hard gate refusing the un-repaired core package with its
contained issues. The F1 evaluator closure and the D1 workspace gate are exercised.
All fixtures synthetic (`demo.*`); no personal data.
"""

from __future__ import annotations

import json
import shutil
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any, Mapping, Sequence

from packages.derivation.live import live_entrypoint_accepts_raw_inputs, live_run
from packages.derivation.live_workspace import (
    LiveWorkspace,
    ResidencyViolation,
    WorkspaceBootstrapError,
    WorkspaceCapability,
    bootstrap_workspace,
)
from packages.derivation.production_resolver import (
    PublicationSurface,
    Refusal,
    ResolvedGraph,
    resolve_production_package,
    select_current_adoption,
)
from packages.derivation.loader import DerivationSchemas
from packages.kernel.currency import compute_currency
from packages.kernel.findings import FindingState
from tools.generate_frrs_t3_fixtures import render_fixture_files

REPO = Path(__file__).resolve().parent.parent
FRRS_T3 = REPO / "packages" / "sample_data" / "frrs_t3"
CONTENT = REPO / "packages" / "content" / "tax" / "2025"
ADOPTIONS = FRRS_T3 / "adoptions"

SCOPE_USER = "demo.user.filer-1"
CLEAN_SCOPE = {"jurisdiction": "us", "year": "2025"}


def _act(name: str) -> dict[str, Any]:
    value = json.loads((ADOPTIONS / name).read_text("utf-8"))
    assert isinstance(value, dict)
    return value


def _surface(member_dir: Path | None = None, registry: Path | None = None,
             release_dir: Path | None = None) -> PublicationSurface:
    return PublicationSurface(
        release_dir=release_dir or (FRRS_T3 / "publication_surface" / "releases"),
        package_registry_path=registry or (CONTENT / "published-packages.json"),
        member_dir=member_dir or CONTENT,
    )


class ProvenanceRegeneration(unittest.TestCase):
    def test_fixture_corpus_regenerates_from_public_pins(self) -> None:
        rendered = render_fixture_files()
        committed = {
            path.relative_to(FRRS_T3).as_posix(): path.read_bytes()
            for path in FRRS_T3.rglob("*.json")
        }
        self.assertEqual(committed, rendered)

    def test_track_three_artifacts_are_synthetic_and_locator_free(self) -> None:
        paths = [
            *FRRS_T3.rglob("*.json"),
            REPO / "packages" / "derivation" / "production_resolver.py",
            REPO / "packages" / "derivation" / "live_workspace.py",
            REPO / "tools" / "generate_frrs_t3_fixtures.py",
        ]
        forbidden = ("/Users/", "/private/", "local-data/", "uploads/", "generated/user/")
        for path in paths:
            with self.subTest(path=path):
                self.assertFalse(any(marker in path.read_text("utf-8") for marker in forbidden))


class AdoptionCurrency(unittest.TestCase):
    """ADR-0033 Decision 1 — release-rooted current-user adoption."""

    def resolve(
        self,
        names: Sequence[str],
        scope: Mapping[str, str] = CLEAN_SCOPE,
        user: str = SCOPE_USER,
        revision: int = 10,
    ) -> ResolvedGraph | Refusal:
        return resolve_production_package(
            [_act(n) for n in names], run_scope=scope, scope_user=user,
            workspace_revision=revision, surface=_surface(),
        )

    def test_supersession_selects_current_not_stale_or_automation(self) -> None:
        r = self.resolve(["adopt-interest-v1.json", "adopt-interest-v2-current.json", "adopt-automation.json"])
        self.assertIsInstance(r, ResolvedGraph)
        assert isinstance(r, ResolvedGraph)
        self.assertEqual(r.adoption_act_id, "act.adopt.interest.v2")

    def test_tie_at_max_revision_refuses(self) -> None:
        r = self.resolve(["adopt-tie-a.json", "adopt-tie-b.json"], scope={"jurisdiction": "us", "year": "2099"})
        self.assertIsInstance(r, Refusal)
        assert isinstance(r, Refusal)
        self.assertEqual(r.reason, "ADOPTION_AMBIGUOUS")

    def test_non_user_only_refuses(self) -> None:
        r = self.resolve(["adopt-automation.json"])
        self.assertIsInstance(r, Refusal)
        assert isinstance(r, Refusal)
        self.assertEqual(r.reason, "ADOPTION_NONE_CURRENT")

    def test_non_user_never_selects_even_at_higher_revision(self) -> None:
        # automation is revision 9 vs the user's v2 (revision 2); user still wins.
        r = self.resolve(["adopt-interest-v2-current.json", "adopt-automation.json"])
        self.assertIsInstance(r, ResolvedGraph)
        assert isinstance(r, ResolvedGraph)
        self.assertEqual(r.adoption_act_id, "act.adopt.interest.v2")

    def test_wrong_scope_refuses_no_caller_override(self) -> None:
        # A run scope with no matching user act cannot be forced by a caller.
        r = self.resolve(["adopt-interest-v2-current.json"], scope={"jurisdiction": "us", "year": "1999"})
        self.assertIsInstance(r, Refusal)
        assert isinstance(r, Refusal)
        self.assertEqual(r.reason, "ADOPTION_NONE_CURRENT")

    def test_future_committed_act_is_not_current(self) -> None:
        acts = [_act("adopt-interest-v2-current.json")]
        acts[0]["committed_against"] = 5
        r = resolve_production_package(acts, run_scope=CLEAN_SCOPE, scope_user=SCOPE_USER,
                                       workspace_revision=2, surface=_surface())
        self.assertIsInstance(r, Refusal)
        assert isinstance(r, Refusal)
        self.assertEqual(r.reason, "ADOPTION_NONE_CURRENT")

    def test_non_advancing_supersession_refuses_instead_of_erasing_current_authority(self) -> None:
        current = _act("adopt-interest-v2-current.json")
        forged = _act("adopt-interest-v1.json")
        forged["payload"]["supersedes"] = current["act_id"]
        r = resolve_production_package(
            [current, forged], run_scope=CLEAN_SCOPE, scope_user=SCOPE_USER,
            workspace_revision=10, surface=_surface(),
        )
        self.assertIsInstance(r, Refusal)
        assert isinstance(r, Refusal)
        self.assertEqual(r.reason, "ADOPTION_SUPERSESSION_INVALID")

    def test_conflicting_same_act_id_refuses(self) -> None:
        original = _act("adopt-interest-v2-current.json")
        conflicting = _act("adopt-interest-v2-current.json")
        conflicting["payload"]["audit"] = {"note": "different synthetic body"}
        r = resolve_production_package(
            [original, conflicting], run_scope=CLEAN_SCOPE, scope_user=SCOPE_USER,
            workspace_revision=10, surface=_surface(),
        )
        self.assertIsInstance(r, Refusal)
        assert isinstance(r, Refusal)
        self.assertEqual(r.reason, "ADOPTION_AMBIGUOUS")


class ReleaseRegistrySubstitutions(unittest.TestCase):
    """ADR-0033 Decision 2 — three substitutions closed fail-closed."""

    def _clean_current(self, surface: PublicationSurface) -> ResolvedGraph | Refusal:
        return resolve_production_package(
            [_act("adopt-interest-v1.json"), _act("adopt-interest-v2-current.json")],
            run_scope=CLEAN_SCOPE, scope_user=SCOPE_USER, workspace_revision=10, surface=surface,
        )

    def test_forged_release_refuses(self) -> None:
        with TemporaryDirectory() as tmp:
            rel = Path(tmp) / "releases"
            rel.mkdir()
            src = FRRS_T3 / "publication_surface" / "releases" / "demo.release.2025.v1.json"
            doc = json.loads(src.read_text())
            doc["package_registry_sha256"] = "0" * 64  # forged release bytes
            (rel / src.name).write_text(json.dumps(doc, indent=2, sort_keys=True) + "\n")
            r = self._clean_current(_surface(release_dir=rel))
        self.assertIsInstance(r, Refusal)
        assert isinstance(r, Refusal)
        self.assertEqual(r.reason, "RELEASE_ABSENT_OR_MISMATCH")

    def test_identity_matching_schema_invalid_release_is_inert(self) -> None:
        """A bad co-located release cannot interrupt honest pinned authority."""
        with TemporaryDirectory() as tmp:
            rel = Path(tmp) / "releases"
            rel.mkdir()
            src = FRRS_T3 / "publication_surface" / "releases" / "demo.release.2025.v1.json"
            honest = json.loads(src.read_text())
            invalid = dict(honest)
            invalid.pop("package_registry_sha256")  # required by release-registry.v1
            (rel / "aaa-invalid-release.json").write_text(
                json.dumps(invalid, indent=2, sort_keys=True) + "\n"
            )
            shutil.copy2(src, rel / src.name)
            r = self._clean_current(_surface(release_dir=rel))
        self.assertIsInstance(r, ResolvedGraph)

    def test_replaced_registry_bytes_under_honest_release_refuses(self) -> None:
        with TemporaryDirectory() as tmp:
            reg = Path(tmp) / "published-packages.json"
            doc = json.loads((CONTENT / "published-packages.json").read_text())
            doc["packages"][0]["checksum"] = doc["packages"][0]["checksum"][:-1] + "0"  # tamper
            reg.write_text(json.dumps(doc, indent=2, sort_keys=True) + "\n")
            r = self._clean_current(_surface(registry=reg))
        self.assertIsInstance(r, Refusal)
        assert isinstance(r, Refusal)
        self.assertEqual(r.reason, "REGISTRY_CHECKSUM_MISMATCH")

    def test_changed_member_bytes_under_honest_registry_refuses(self) -> None:
        with TemporaryDirectory() as tmp:
            members = Path(tmp) / "content"
            shutil.copytree(CONTENT, members)
            # Mutate one member body's bytes (a rule) without touching the registry.
            for path in members.glob("rule.*.json"):
                body = json.loads(path.read_text())
                body["_tamper"] = "changed bytes"
                path.write_text(json.dumps(body, indent=2, sort_keys=True) + "\n")
                break
            r = self._clean_current(_surface(member_dir=members, registry=members / "published-packages.json"))
        self.assertIsInstance(r, Refusal)
        assert isinstance(r, Refusal)
        # Decision 2 must reject the substituted bytes before the Decision-3
        # hard validator is reached; accepting HARD_GATE_REFUSED here would
        # mask a member-admission failure.
        self.assertEqual(r.reason, "MEMBER_ABSENT_OR_MISMATCH")

    def test_changed_package_bytes_under_honest_registry_refuses(self) -> None:
        with TemporaryDirectory() as tmp:
            members = Path(tmp) / "content"
            shutil.copytree(CONTENT, members)
            package = next(members.glob("package.interest-slice*.json"))
            body = json.loads(package.read_text())
            body["_tamper"] = "changed package body"
            package.write_text(json.dumps(body, indent=2, sort_keys=True) + "\n")
            r = self._clean_current(
                _surface(member_dir=members, registry=members / "published-packages.json")
            )
        self.assertIsInstance(r, Refusal)
        assert isinstance(r, Refusal)
        self.assertEqual(r.reason, "PACKAGE_ABSENT_OR_MISMATCH")


class ExclusiveMemberGraph(unittest.TestCase):
    """ADR-0033 Decision 3 — exclusive verified graph or refuse."""

    def _clean(self, surface: PublicationSurface | None = None) -> ResolvedGraph | Refusal:
        return resolve_production_package(
            [_act("adopt-interest-v2-current.json")], run_scope=CLEAN_SCOPE,
            scope_user=SCOPE_USER, workspace_revision=10, surface=surface or _surface(),
        )

    def test_clean_resolves_exclusive_graph(self) -> None:
        r = self._clean()
        self.assertIsInstance(r, ResolvedGraph)
        assert isinstance(r, ResolvedGraph)
        self.assertGreater(len(r.resolved_members), 0)

    def test_unpinned_co_located_file_is_inert(self) -> None:
        # PC1 golden: an unpinned co-located file never becomes a candidate.
        with TemporaryDirectory() as tmp:
            members = Path(tmp) / "content"
            shutil.copytree(CONTENT, members)
            (members / "demo.evil.unpinned.json").write_text(
                json.dumps({"id": "demo.evil.unpinned", "version": "v1", "schema": "rule-artifact.v1"}) + "\n"
            )
            r = self._clean(_surface(member_dir=members, registry=members / "published-packages.json"))
        self.assertIsInstance(r, ResolvedGraph)
        assert isinstance(r, ResolvedGraph)
        ids = {m.get("id") for m in r.resolved_members}
        self.assertNotIn("demo.evil.unpinned", ids)

    def test_same_key_impostor_ignored_only_verified_body_admitted(self) -> None:
        # PC2/same-key: a co-located file sharing a member id but with different
        # bytes is not checksum-verified and never displaces the real member.
        r0 = self._clean()
        self.assertIsInstance(r0, ResolvedGraph)
        assert isinstance(r0, ResolvedGraph)
        with TemporaryDirectory() as tmp:
            members = Path(tmp) / "content"
            shutil.copytree(CONTENT, members)
            real = next(members.glob("rule.*.json"))
            body = json.loads(real.read_text())
            impostor = dict(body)
            impostor["_impostor"] = True  # same id/version, different bytes
            (members / "zzz-impostor.json").write_text(json.dumps(impostor, indent=2, sort_keys=True) + "\n")
            r = self._clean(_surface(member_dir=members, registry=members / "published-packages.json"))
        self.assertIsInstance(r, ResolvedGraph)
        assert isinstance(r, ResolvedGraph)
        self.assertEqual(len(r.resolved_members), len(r0.resolved_members))

    def test_filesystem_order_independence(self) -> None:
        a = self._clean()
        with TemporaryDirectory() as tmp:
            members = Path(tmp) / "content"
            shutil.copytree(CONTENT, members)
            # Place an exact verified member under a nested path that sorts
            # before its original.  Candidate identity/digest admission, not
            # directory enumeration, must keep the resolved graph unchanged.
            original = next(members.glob("rule.*.json"))
            nested = members / "aaa-before" / original.name
            nested.parent.mkdir()
            shutil.copy2(original, nested)
            b = self._clean(_surface(member_dir=members, registry=members / "published-packages.json"))
        self.assertIsInstance(a, ResolvedGraph)
        assert isinstance(a, ResolvedGraph)
        self.assertIsInstance(b, ResolvedGraph)
        assert isinstance(b, ResolvedGraph)
        self.assertEqual({m.get("id") for m in a.resolved_members}, {m.get("id") for m in b.resolved_members})

    def test_package_adoption_checksum_mismatch_refuses(self) -> None:
        act = _act("adopt-interest-v2-current.json")
        act["payload"]["package"]["checksum"] = "0" * 64
        r = resolve_production_package([act], run_scope=CLEAN_SCOPE, scope_user=SCOPE_USER,
                                       workspace_revision=10, surface=_surface())
        self.assertIsInstance(r, Refusal)
        assert isinstance(r, Refusal)
        self.assertEqual(r.reason, "PACKAGE_ABSENT_OR_MISMATCH")


class HardGateRefusesUnrepairedPackage(unittest.TestCase):
    """ADR-0033 Decision 5 / RG-1 — the gate refuses the un-repaired core package."""

    def test_core_package_refuses_with_contained_issues_no_graph(self) -> None:
        r = resolve_production_package(
            [_act("adopt-core-current.json")], run_scope={"jurisdiction": "us", "year": "2050"},
            scope_user=SCOPE_USER, workspace_revision=10, surface=_surface(),
        )
        self.assertIsInstance(r, Refusal)
        assert isinstance(r, Refusal)
        self.assertEqual(r.reason, "HARD_GATE_REFUSED")
        self.assertEqual(len(r.issues), 8)  # the eight RG-1 issues; never an allowlist
        self.assertFalse(hasattr(r, "resolved_members"))
        codes = {i["code"] for i in r.issues}
        self.assertIn("MEMBER_UNREACHABLE", codes)


class F1EvaluatorClosure(unittest.TestCase):
    """ADR-0032 F1 (inherited) — no production path reaches a hand-assembled input."""

    def test_live_entrypoint_admits_no_raw_input_parameter(self) -> None:
        self.assertFalse(live_entrypoint_accepts_raw_inputs())

    def test_production_modules_do_not_import_the_fixture_adapter(self) -> None:
        for module in ("production_resolver.py", "live.py", "marshal.py"):
            src = (REPO / "packages" / "derivation" / module).read_text("utf-8")
            self.assertNotRegex(src, r"(?m)^from packages\.derivation\.runners import derive$")
            self.assertNotRegex(src, r"(?m)^import packages\.derivation\.runners\.derive$")
        live_source = (REPO / "packages" / "derivation" / "live.py").read_text("utf-8")
        self.assertNotRegex(live_source, r"(?m)^from packages\.derivation\.runner import")

    def test_marshalling_empty_state_yields_no_ghost_findings(self) -> None:
        # A hand-assembled ghost id absent from the record cannot appear on a run.
        result = live_run(
            {"schema": "run-request.v1"}, run_id="demo.run-1", state=FindingState(),
            currency=compute_currency(FindingState()), rules=[], parameters={},
            canon={}, adoption_pin={"id": "demo.pkg", "version": "v1"}, governance_pins=[],
            schemas=DerivationSchemas(),
        )
        self.assertEqual(result.publications, [])


class LiveWorkspaceBootstrap(unittest.TestCase):
    """ADR-0033 Decision 4 / D1 F2 — workspace behind the capability wall + gates."""

    def test_bootstrap_outside_repo_initializes_with_boundary_registry(self) -> None:
        with TemporaryDirectory() as tmp:
            ws = bootstrap_workspace(WorkspaceCapability(Path(tmp) / "L"), repo_root=REPO)
            self.assertIsInstance(ws, LiveWorkspace)
            self.assertTrue(ws.location.exists())
            self.assertIn("classification.v1", ws.registry.schema_ids())  # F2: boundary loaded at runtime

    def test_bootstrap_inside_repo_refuses(self) -> None:
        with self.assertRaises(WorkspaceBootstrapError):
            bootstrap_workspace(WorkspaceCapability(REPO / "packages" / "L"), repo_root=REPO)

    def test_bootstrap_refuses_a_capability_with_publication_or_repository_write(self) -> None:
        with TemporaryDirectory() as tmp:
            with self.assertRaises(WorkspaceBootstrapError):
                bootstrap_workspace(
                    WorkspaceCapability(Path(tmp) / "L", publication_allowed=True), repo_root=REPO
                )
            with self.assertRaises(WorkspaceBootstrapError):
                bootstrap_workspace(
                    WorkspaceCapability(Path(tmp) / "L", repository_write_allowed=True), repo_root=REPO
                )

    def _ws(self, tmp: str) -> LiveWorkspace:
        return bootstrap_workspace(WorkspaceCapability(Path(tmp) / "L"), repo_root=REPO)

    def test_classification_is_total_and_fail_closed(self) -> None:
        with TemporaryDirectory() as tmp:
            ws = self._ws(tmp)
            may = ws.classify({"kind": "independently-constructed synthetic fixture", "public_origin_proof": True})
            self.assertEqual(may.decision, "MAY_CROSS")
            personal = ws.classify({"describes_personal": True})
            self.assertEqual(personal.decision, "NEVER_CROSSES")
            unknown = ws.classify({"kind": "mystery"})  # no proof -> fail closed
            self.assertEqual(unknown.decision, "NEVER_CROSSES")
            inherited = ws.classify({
                "kind": "public-origin contract", "public_origin_proof": True,
                "inputs": [{"describes_personal": True}],
            })
            self.assertEqual(inherited.decision, "NEVER_CROSSES")

    def test_commit_and_push_gates_refuse_never_crosses(self) -> None:
        with TemporaryDirectory() as tmp:
            ws = self._ws(tmp)
            personal = {"name": "w2.pdf", "describes_personal": True}
            with self.assertRaises(ResidencyViolation):
                ws.guard_commit([personal])
            with self.assertRaises(ResidencyViolation):
                ws.guard_push([personal])
            # A proven public synthetic artifact crosses.
            ws.guard_commit([{"name": "fixture.json", "kind": "independently-constructed synthetic fixture", "public_origin_proof": True}])

    def test_live_outputs_cannot_escape_the_residency_root(self) -> None:
        with TemporaryDirectory() as tmp:
            ws = self._ws(tmp)
            self.assertEqual(ws.live_output_path(Path("records/run.json")).parent, ws.location / "records")
            with self.assertRaises(ResidencyViolation):
                ws.live_output_path(Path("../outside.json"))


class ProductionResolverIsFixtureSuperset(unittest.TestCase):
    def test_resolver_refuses_where_fixture_path_would_ignore_ok_false(self) -> None:
        # The fixture adapter tolerates validation.ok == False (derive.py comment);
        # the production resolver refuses it. Strict superset of guarantees.
        r = resolve_production_package(
            [_act("adopt-core-current.json")], run_scope={"jurisdiction": "us", "year": "2050"},
            scope_user=SCOPE_USER, workspace_revision=10, surface=_surface(),
        )
        self.assertIsInstance(r, Refusal)


if __name__ == "__main__":
    unittest.main()
