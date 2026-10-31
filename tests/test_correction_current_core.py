"""Track 1: the correction session recalculates on the core the workspace has adopted.

The session's public entry point (``CorrectionRuntime.open`` then ``.calculate``) is
driven over a workspace whose acts adopt core v66 (package v66 / release v64 /
registry v64) and compared with a fresh ``live_coordinate_run`` on that core, for
returns only v66 computes. The v42 workspace (the committed correction seed) is still
served by registry v40, a re-adoption moves the next calculation to v66, and an
adoption the release surface cannot supply still ends in the session's existing
outcomes. Synthetic ``demo.*`` data only.
"""

from __future__ import annotations

import copy
import hashlib
import json
import re
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any

from packages.derivation.correction_session import (
    CORE_CONTENT,
    CORE_RELEASE_DIR,
    RUN_SCOPE,
    SCOPE_USER,
    CorrectionRuntime,
    CorrectionSessionError,
    _line21_view,
    adopted_core_surface,
    load_seed_acts,
)
from packages.derivation.live import live_coordinate_run
from packages.derivation.live_workspace import WorkspaceCapability, bootstrap_workspace
from packages.derivation.loader import DerivationSchemas
from packages.derivation.production_resolver import PublicationSurface, Refusal, resolve_adopted_surface
from packages.kernel.act_log import ActLog
from packages.tax.loader import install_domain_scoped_supersession
from tests import test_w2g_gambling as w2g
from tests.helpers import current_core_returns as ccr
from tests.test_form_1099_k_income import _handover
from tests.test_form_1099_withholding import (
    _base,
    _social_security_withholding,
    _unemployment,
    _unemployment_withholding,
)
from tests.test_refund_or_amount_owed_track1 import _finish

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "packages/content/tax/2025"
RELEASES = ROOT / "packages/sample_data/student_loan_worksheet_integration/publication_surface/releases"
REL_ID = "demo.release.sli-worksheet-integration.2025."
TESTS_USER = "demo.user.filer-1"

# core -> (package file, package version, release version, registry file)
CORES = {
    "v66": ("package.core-calculations.v66.json", "v66", "v64", "published-packages.v64.json"),
    "v42": ("package.core-calculations.v42.json", "v42", "v40", "published-packages.v40.json"),
}
V66_SURFACE = PublicationSurface(RELEASES, CONTENT / CORES["v66"][3], CONTENT)


def _v66_acts(acts: list[dict[str, object]], note: str) -> list[dict[str, object]]:
    pkg, ver, rel, _ = CORES["v66"]
    finished = _finish(
        copy.deepcopy(acts), package_path=CONTENT / pkg, package_version=ver,
        release_path=RELEASES / f"{REL_ID}{rel}.json", release_version=rel, note=note)
    return _handover(finished, surface=V66_SURFACE, reconfirm=True)


def _as_session_user(acts: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows = json.loads(json.dumps(acts).replace(TESTS_USER, SCOPE_USER))
    for index, row in enumerate(rows):
        row["committed_against"] = index
    return rows  # type: ignore[no-any-return]


def _g_return(amounts: list[float | None], *, close: bool) -> list[dict[str, object]]:
    """A complete return with two Forms 1099-G and the given box 4 withholding."""
    acts = _base(wages=50000.0, w2_withheld=4500.0)
    _unemployment(acts, [6000.0, 4000.0], authority=None)
    _unemployment_withholding(acts, amounts, close=close)
    _social_security_withholding(acts, [])
    w2g._w2g(acts, [])
    return acts


def _adoption(acts: list[dict[str, Any]], core: str, act_id: str, *, checksum: str | None = None) -> dict[str, Any]:
    pkg, ver, rel, _ = CORES[core]
    adoption: dict[str, Any] = copy.deepcopy(next(a for a in reversed(acts) if a["kind"] == "package-adoption"))
    adoption["act_id"] = act_id
    adoption["committed_against"] = len(acts)
    adoption["payload"]["revision"] = max(
        a["payload"]["revision"] for a in acts if a["kind"] == "package-adoption") + 1
    adoption["payload"]["package"] = {
        "id": "tax.us.2025.package.core-calculations", "version": ver,
        "checksum": json.loads((CONTENT / pkg).read_text("utf-8"))["package_checksum"]}
    adoption["payload"]["release"] = {
        "id": "demo.release.sli-worksheet-integration.2025", "version": rel,
        "checksum": checksum or hashlib.sha256((RELEASES / f"{REL_ID}{rel}.json").read_bytes()).hexdigest()}
    return adoption


class _Workspace:
    """A session workspace holding ``acts``, opened through the public entry point."""

    def __init__(self, acts: list[dict[str, Any]]) -> None:
        self._tmp = TemporaryDirectory()
        self.capability = WorkspaceCapability(Path(self._tmp.name) / "L")
        schemas = DerivationSchemas()
        registry = install_domain_scoped_supersession(schemas.registry)
        self.log = ActLog(bootstrap_workspace(self.capability, repo_root=ROOT).location, registry)
        for index, act in enumerate(acts):
            row = dict(act)
            row["committed_against"] = index
            self.log.append(row, expected_revision=index)
        self.runtime = CorrectionRuntime.open(self.capability, repo_root=ROOT)

    def close(self) -> None:
        self._tmp.cleanup()


def _fresh(acts: list[dict[str, Any]], run_id: str, surface: PublicationSurface) -> dict[str, Any]:
    with TemporaryDirectory() as tmp:
        outcome = live_coordinate_run(
            WorkspaceCapability(Path(tmp) / "L"), repo_root=ROOT, authoritative_acts=acts,
            workspace_revision=len(acts), run_scope=RUN_SCOPE, scope_user=SCOPE_USER,
            request={"schema": "run-request.v1"}, run_id=run_id, governance_pins=[],
            surface=surface, output_name="out.json")
        assert outcome.refusal is None and outcome.presentation_path is not None, outcome.refusal
        assert outcome.output_path is not None
        report = json.loads(outcome.output_path.read_text("utf-8"))
        return {
            "model": json.loads(outcome.presentation_path.read_text("utf-8")),
            "values": {str(p.finding["symbol"]): json.dumps(p.finding["value"], sort_keys=True)
                       for p in outcome.publications or ()},
            "blocked": sorted(
                (str(r.get("artifact_id")), str(r.get("code")))
                for r in report.get("dispositions", []) if r.get("disposition") == "blocked"),
        }


def _shown(model: dict[str, Any]) -> dict[str, Any]:
    """The lines, values and dispositions of a presentation model, with the run id and the
    ids derived from it replaced (they are the only things that differ between two runs)."""
    text = json.dumps(
        {"sections": model["sections"], "dispositionNodes": model["dispositionNodes"]}, sort_keys=True)
    text = text.replace(str(model["runId"]), "RUN")
    text = re.sub(r"[0-9a-f]{24}", "H", text)
    shown: dict[str, Any] = json.loads(text)
    return shown


class CurrentCoreCalculation(unittest.TestCase):
    def _same_as_fresh(self, acts: list[dict[str, object]], name: str) -> dict[str, Any]:
        v66 = _as_session_user(_v66_acts(acts, name))
        fresh = _fresh(v66, f"demo.cc.{name}.fresh", V66_SURFACE)
        ws = _Workspace(v66)
        self.addCleanup(ws.close)
        self.assertEqual(ws.runtime.calculate(), {"calculated": True})
        saved = ws.runtime._saved_presentation
        self.assertIsNotNone(saved)
        # The session's saved result shows every line, value and blocked row a fresh run shows
        # (the run id and the ids derived from it are the only things that differ).
        assert saved is not None
        self.assertEqual(_shown(saved), _shown(fresh["model"]))
        self.assertTrue(_shown(saved)["sections"])
        return fresh

    def test_form_1099g_withholding_closed_on_v66(self) -> None:
        fresh = self._same_as_fresh(_g_return([600.0, 400.0], close=True), "g")
        self.assertEqual(fresh["blocked"], [])
        self.assertGreater(len(fresh["values"]), 200)

    def test_form_w2g_on_v66(self) -> None:
        fresh = self._same_as_fresh(w2g._w2g_return([(1000.0, 200.0)]), "w2g")
        self.assertEqual(fresh["blocked"], [])

    def test_unconfirmed_family_blocks_in_the_session_as_in_the_fresh_run(self) -> None:
        fresh = self._same_as_fresh(_g_return([600.0, 400.0], close=False), "gopen")
        self.assertIn(
            ("tax.us.2025.rule.form1040-line25b", "SOURCE_SET_UNCLOSED"),
            [(a, c) for a, c in fresh["blocked"]],
        )

    def test_line21_view_tolerates_a_v66_return_that_publishes_no_line_21(self) -> None:
        # A complete v66 return with no student loan interest: the saved model has no
        # line 21 explanation, and the view reports that without raising.
        v66 = _as_session_user(_v66_acts(_g_return([600.0, 400.0], close=True), "l21"))
        ws = _Workspace(v66)
        self.addCleanup(ws.close)
        self.assertEqual(ws.runtime.calculate(), {"calculated": True})
        view = _line21_view(ws.runtime._saved_presentation or {}, ws.log.read().acts, ws.runtime.registry)
        self.assertIsNone(view["line21_value"])
        self.assertEqual(view["line21_rows"], [])

    def test_line21_view_shows_the_line_21_rows_of_a_v66_return_with_student_loan_interest(self) -> None:
        # Live counterpart of the test above: two Forms 1098-E of 100.40 each. The view shows one row
        # per statement at its own amount and the line at the whole-dollar sum, 100.40 + 100.40 = 200.80 -> 201.
        v66 = _as_session_user(_v66_acts(ccr.add_student_loan_interest_1098e(ccr.base_return(), [100.40, 100.40]), "l21live"))
        ws = _Workspace(v66)
        self.addCleanup(ws.close)
        self.assertEqual(ws.runtime.calculate(), {"calculated": True})
        view = _line21_view(ws.runtime._saved_presentation or {}, ws.log.read().acts, ws.runtime.registry)
        self.assertEqual(view["line21_value"], 201)
        self.assertEqual(view["line21_disposition"], "published_value")
        self.assertEqual([row["amount"] for row in view["line21_rows"]], [100.4, 100.4])
        self.assertEqual(
            sorted(row["statementKeys"]["statement"] for row in view["line21_rows"]),
            ["demo.ccr.sli0.statement", "demo.ccr.sli1.statement"])
        # The session's state carries the same rows, as the correction page reads them.
        state = ws.runtime.state()
        self.assertEqual(state["line21_value"], 201)
        self.assertEqual(len(state["line21_rows"]), 2)


class ResolverChoosesFromTheAdoption(unittest.TestCase):
    def _surface(self, acts: list[dict[str, Any]]) -> PublicationSurface | Refusal:
        return adopted_core_surface(ROOT, acts, len(acts))

    def test_v42_seed_resolves_registry_v40(self) -> None:
        surface = self._surface(load_seed_acts(ROOT))
        assert isinstance(surface, PublicationSurface)
        self.assertEqual(surface.package_registry_path, ROOT / CORE_CONTENT / "published-packages.v40.json")
        self.assertEqual(surface.release_dir, ROOT / CORE_RELEASE_DIR)

    def test_v66_adoption_resolves_registry_v64(self) -> None:
        seed = load_seed_acts(ROOT)
        surface = self._surface([*seed, _adoption(seed, "v66", "demo.cc.adopt.v66")])
        assert isinstance(surface, PublicationSurface)
        self.assertEqual(surface.package_registry_path, ROOT / CORE_CONTENT / "published-packages.v64.json")

    def test_no_adoption_unknown_release_and_unknown_registry_refuse(self) -> None:
        seed = load_seed_acts(ROOT)
        none = self._surface([a for a in seed if a["kind"] != "package-adoption"])
        self.assertIsInstance(none, Refusal)
        self.assertEqual(none.reason, "ADOPTION_NONE_CURRENT")  # type: ignore[union-attr]
        unknown = self._surface([*seed, _adoption(seed, "v42", "demo.cc.adopt.bad", checksum="0" * 64)])
        self.assertIsInstance(unknown, Refusal)
        self.assertEqual(unknown.reason, "RELEASE_ABSENT_OR_MISMATCH")  # type: ignore[union-attr]
        # A release the surface holds, with no registry in the member directory to match it.
        with TemporaryDirectory() as empty:
            absent = resolve_adopted_surface(
                [*seed, _adoption(seed, "v66", "demo.cc.adopt.nr")], run_scope=RUN_SCOPE,
                scope_user=SCOPE_USER, workspace_revision=len(seed) + 1,
                release_dir=ROOT / CORE_RELEASE_DIR, member_dir=Path(empty))
        assert isinstance(absent, Refusal)
        self.assertEqual(absent.reason, "REGISTRY_ABSENT")


class SessionOutcomes(unittest.TestCase):
    def test_v42_workspace_still_calculates_on_v40(self) -> None:
        ws = _Workspace(load_seed_acts(ROOT))
        self.addCleanup(ws.close)
        self.assertEqual(ws.runtime.calculate(), {"calculated": True})

    def test_readoption_mid_session_moves_the_next_calculation_to_v66(self) -> None:
        v66 = _as_session_user(_v66_acts(w2g._w2g_return([(1000.0, 200.0)]), "readopt"))
        # The same return while the filer still stands on v42 (adoption is the third from last).
        v42 = [*v66[:-3], *v66[-2:]]
        v42.append(_adoption(v66, "v42", "demo.cc.adopt.v42") | {"committed_against": len(v42)})
        ws = _Workspace(v42)
        self.addCleanup(ws.close)

        def registry() -> str:
            contents = ws.log.read()
            surface = adopted_core_surface(ROOT, contents.acts, contents.revision)
            assert isinstance(surface, PublicationSurface)
            return surface.package_registry_path.name

        self.assertEqual(registry(), "published-packages.v40.json")
        # v42 cannot take the v66 questions: the session says so as it does today.
        self.assertEqual(ws.runtime.calculate(), {"calculated": False})
        contents = ws.log.read()
        ws.log.append(
            _adoption(list(contents.acts), "v66", "demo.cc.adopt.v66.later")
            | {"committed_against": contents.revision},
            expected_revision=contents.revision)
        self.assertEqual(registry(), "published-packages.v64.json")
        self.assertEqual(ws.runtime.calculate(), {"calculated": True})

    def test_a_correction_saved_on_v66_recalculates_on_v66(self) -> None:
        seed = load_seed_acts(ROOT)
        ws = _Workspace([*seed, _adoption(seed, "v66", "demo.cc.adopt.v66.corr")])
        self.addCleanup(ws.close)
        self.assertEqual(ws.runtime.calculate(), {"calculated": True})
        choices = ws.runtime.state()["choices"]
        [cedar] = [c for c in choices.values()
                   if any(f.get("statement", "").startswith("2025 Form 1098-E from Cedar") for f in c["forms"])]
        chosen = ws.runtime.choose(cedar["finding_id"])
        # The save-time recalculation (``_recalculate``) is the run under test.
        result = ws.runtime.confirm(chosen["token"], "no")
        self.assertEqual(result["outcome"], "saved-and-calculated")
        # A later calculation over the post-correction log shows what a fresh v66 run shows.
        self.assertEqual(ws.runtime.calculate(), {"calculated": True})
        acts = list(ws.log.read().acts)
        saved = ws.runtime._saved_presentation
        assert saved is not None
        self.assertEqual(_shown(saved), _shown(_fresh(acts, "demo.cc.corr.fresh", V66_SURFACE)["model"]))

    def test_initialize_on_a_seed_that_adopts_v66(self) -> None:
        from unittest import mock
        from packages.derivation import correction_session as cs

        seed = load_seed_acts(ROOT)
        v66_seed = [*seed, _adoption(seed, "v66", "demo.cc.adopt.v66.init")]
        with TemporaryDirectory() as tmp, mock.patch.object(cs, "load_seed_acts", return_value=v66_seed):
            capability = WorkspaceCapability(Path(tmp) / "L")
            runtime = CorrectionRuntime.initialize(capability, repo_root=ROOT)
            contents = runtime._log.read()
            surface = adopted_core_surface(ROOT, contents.acts, contents.revision)
            assert isinstance(surface, PublicationSurface)
            self.assertEqual(surface.package_registry_path.name, "published-packages.v64.json")
            self.assertEqual(runtime.calculate(), {"calculated": True})

    def test_unsupplied_adoptions_end_in_the_existing_outcome(self) -> None:
        seed = load_seed_acts(ROOT)
        for label, acts in (
            ("none", [a for a in seed if a["kind"] != "package-adoption"]),
            ("unknown-release", [*seed, _adoption(seed, "v42", "demo.cc.adopt.bad", checksum="0" * 64)]),
        ):
            with self.subTest(label):
                ws = _Workspace(acts)
                self.addCleanup(ws.close)
                self.assertEqual(ws.runtime.calculate(), {"calculated": False})

    def test_initialize_refuses_with_the_existing_message_when_no_core_resolves(self) -> None:
        with TemporaryDirectory() as tmp, self.assertRaises(CorrectionSessionError) as ctx:
            from unittest import mock
            from packages.derivation import correction_session as cs
            with mock.patch.object(cs, "adopted_core_surface", return_value=Refusal("X", "x")):
                CorrectionRuntime.initialize(WorkspaceCapability(Path(tmp) / "L"), repo_root=ROOT)
        self.assertEqual(str(ctx.exception), "correction-opening-calculation-refused")


if __name__ == "__main__":
    unittest.main()
