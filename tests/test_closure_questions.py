"""Track 1: source-closure-mapping.v3 (a declared closure question) and its admission.

Every admission point reads the one CLOSURE_MAPPING_SCHEMAS set, so a v3 mapping
is admitted alongside v2 and the live coordinator does not drop it.
"""

from __future__ import annotations

import copy
import json
import re
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace
from typing import Any

from packages.derivation.authorization_closure import build_dependency_edges
from packages.derivation.live import _resolved_run_material
from packages.derivation.loader import DerivationSchemas
from packages.derivation.package_validation import (
    CLOSURE_MAPPING_SCHEMAS,
    validate_package,
)
from packages.kernel.schema_registry import SchemaValidationError
from packages.derivation.live import live_coordinate_run
from packages.derivation.live_session import _render_page
from packages.derivation.live_workspace import WorkspaceCapability
from packages.derivation.presentation_projection import validate_presentation_model
from packages.derivation.package_validation import load_published_citizen_checksums
from packages.derivation.production_resolver import PublicationSurface
from packages.kernel.findings import FindingModelError
from packages.tax.loader import TAX_CONTENT_DIR, load_closure_mappings
from tests.test_form_1099_k_income import _handover
from tests import test_collect_closure as cc
from tests import test_w2g_gambling as w2g
from tests.test_interest_cents import IRun, _interest
from tests.test_sli_line21_explanation_page import BROWSER
from tests.test_refund_or_amount_owed_track1 import _finish
from tests.test_withholding_closure import _strip_closure

ROOT = Path(__file__).resolve().parents[1]
RELEASE_DIR = ROOT / "packages/sample_data/student_loan_worksheet_integration/publication_surface/releases"
PACKAGE_V68 = TAX_CONTENT_DIR / "package.core-calculations.v68.json"
PACKAGE_V69 = TAX_CONTENT_DIR / "package.core-calculations.v69.json"
REGISTRY_V66 = TAX_CONTENT_DIR / "published-packages.v66.json"
REGISTRY_V67 = TAX_CONTENT_DIR / "published-packages.v67.json"
RELEASE_V66 = RELEASE_DIR / "demo.release.sli-worksheet-integration.2025.v66.json"
RELEASE_V67 = RELEASE_DIR / "demo.release.sli-worksheet-integration.2025.v67.json"
QUESTIONS_TABLE = ROOT / "docs/phases/engine-breadth/milestones/closure-questions-evidence/questions.md"

# Engine terms a filer should never meet in a question.
FORBIDDEN_TERMS = ("membership", "horizon", "closure", "source set", "family", "attest", "adr-", "adr ", "tax.us.", "fact type")

MAPPING_ID = "tax.us.2025.closure-mapping.f1099g-b4"


def _read(name: str) -> dict[str, Any]:
    value: dict[str, Any] = json.loads((TAX_CONTENT_DIR / name).read_text("utf-8"))
    return value


def _v3() -> dict[str, Any]:
    return _read("closure-mapping.f1099g-b4.v2.json")


def _corpus() -> dict[tuple[str, str], dict[str, Any]]:
    corpus: dict[tuple[str, str], dict[str, Any]] = {}
    for path in TAX_CONTENT_DIR.glob("*.json"):
        try:
            value = json.loads(path.read_text("utf-8"))
        except Exception:
            continue
        if isinstance(value, dict) and isinstance(value.get("id"), str) and isinstance(value.get("version"), str):
            corpus[(value["id"], value["version"])] = value
    return corpus


class ClosureMappingV3Test(unittest.TestCase):
    def test_schema_set_admits_v2_and_v3(self) -> None:
        self.assertEqual(CLOSURE_MAPPING_SCHEMAS, {"source-closure-mapping.v2", "source-closure-mapping.v3"})

    def test_v3_mapping_validates_and_v2_still_does(self) -> None:
        schemas = DerivationSchemas()
        v3 = _v3()
        self.assertEqual(schemas.validate_declared(v3), "source-closure-mapping.v3")
        self.assertTrue(v3["closure_question"])
        self.assertEqual(schemas.validate_declared(_read("closure-mapping.f1099g-b4.json")), "source-closure-mapping.v2")

    def test_empty_or_missing_question_is_refused(self) -> None:
        schemas = DerivationSchemas()
        empty = _v3()
        empty["closure_question"] = ""
        with self.assertRaises(SchemaValidationError):
            schemas.validate_declared(empty)
        missing = _v3()
        del missing["closure_question"]
        with self.assertRaises(SchemaValidationError):
            schemas.validate_declared(missing)

    def test_a_blank_question_is_refused(self) -> None:
        for blank in ("   ", "\t", " \n "):
            mapping = _v3()
            mapping["closure_question"] = blank
            with self.subTest(blank=blank), self.assertRaises(SchemaValidationError):
                DerivationSchemas().validate_declared(mapping)

    def test_v2_with_a_question_is_refused(self) -> None:
        v2 = _read("closure-mapping.f1099g-b4.json")
        v2["closure_question"] = "demo question?"
        with self.assertRaises(SchemaValidationError):
            DerivationSchemas().validate_declared(v2)

    def test_tax_loader_admits_v3_as_latest_version(self) -> None:
        mapping = load_closure_mappings()[MAPPING_ID]
        self.assertEqual(mapping["schema"], "source-closure-mapping.v3")
        self.assertEqual(mapping["version"], "v2")

    def _swapped_package(self) -> tuple[dict[str, Any], dict[tuple[str, str], dict[str, Any]]]:
        package = copy.deepcopy(_read("package.core-calculations.v68.json"))
        for member in package["members"]:
            if member["id"] == MAPPING_ID:
                member["schema"] = "source-closure-mapping.v3"
                member["version"] = "v2"
        corpus = _corpus()
        members = {(m["id"], m["version"]): corpus[(m["id"], m["version"])] for m in package["members"]}
        return package, members

    def test_package_validator_and_closure_admit_v3_member(self) -> None:
        package, members = self._swapped_package()
        result = validate_package(package, members, DerivationSchemas())
        mapping_issues = [i for i in result.issues if i.member_id == MAPPING_ID]
        self.assertEqual(mapping_issues, [], result.issues)
        self.assertNotIn("MEMBER_SCHEMA_UNSUPPORTED", {i.code for i in result.issues})

        corpus = {cid: c for (cid, _v), c in members.items()}
        edges = build_dependency_edges(corpus, package=package)
        self.assertTrue(edges[MAPPING_ID], "v3 mapping contributes dependency edges")
        family_id = _v3()["family"]["id"]
        self.assertIn(MAPPING_ID, edges[family_id], "the family depends on its v3 mapping")

    def test_live_coordinator_keeps_v3_mapping(self) -> None:
        v2 = _read("closure-mapping.f1099g-b4.json")
        graph = SimpleNamespace(resolved_members=[v2, _v3()], package={"input_bindings": []})
        material = _resolved_run_material(graph)
        schemas = [m["schema"] for m in material[3]]
        self.assertEqual(sorted(schemas), ["source-closure-mapping.v2", "source-closure-mapping.v3"])


def _package(path: Path) -> dict[str, Any]:
    value: dict[str, Any] = json.loads(path.read_text("utf-8"))
    return value


def _v69_mappings() -> list[dict[str, Any]]:
    corpus = _corpus()
    package = _package(PACKAGE_V69)
    return [corpus[(m["id"], m["version"])] for m in package["members"] if m["role"] == "source-closure-mapping"]


class EveryMappingInCoreV69AsksItsQuestion(unittest.TestCase):
    def test_every_closure_mapping_is_v3_with_a_question(self) -> None:
        mappings = _v69_mappings()
        self.assertEqual(len(mappings), 51)
        for mapping in mappings:
            with self.subTest(mapping["id"]):
                self.assertEqual(mapping["schema"], "source-closure-mapping.v3")
                self.assertTrue(mapping["closure_question"].strip())

    def test_no_question_uses_an_engine_term(self) -> None:
        for mapping in _v69_mappings():
            question = mapping["closure_question"].lower()
            with self.subTest(mapping["id"]):
                for term in FORBIDDEN_TERMS:
                    self.assertNotIn(term, question)
                self.assertTrue(question.endswith("?"))

    def test_the_forbidden_term_check_is_live(self) -> None:
        self.assertTrue(any(term in "the membership horizon of this family" for term in FORBIDDEN_TERMS))

    def test_questions_are_distinct_and_tabled(self) -> None:
        mappings = _v69_mappings()
        questions = [m["closure_question"] for m in mappings]
        self.assertEqual(len(set(questions)), len(questions))
        table = QUESTIONS_TABLE.read_text("utf-8")
        for mapping in mappings:
            self.assertIn(mapping["closure_question"], table)

    def test_each_successor_changes_only_version_schema_and_question(self) -> None:
        corpus = _corpus()
        old_pins = {m["id"]: m for m in _package(PACKAGE_V68)["members"]}
        for mapping in _v69_mappings():
            old = corpus[(mapping["id"], old_pins[mapping["id"]]["version"])]
            with self.subTest(mapping["id"]):
                changed = {k for k in set(old) | set(mapping) if old.get(k) != mapping.get(k)}
                self.assertLessEqual(changed, {"schema", "version", "closure_question"})

    def test_only_closure_mappings_and_their_entrypoint_pins_differ_from_v68(self) -> None:
        old, new = _package(PACKAGE_V68), _package(PACKAGE_V69)
        old_members = {m["id"]: m for m in old["members"]}
        new_members = {m["id"]: m for m in new["members"]}
        self.assertEqual(set(old_members), set(new_members))
        for member_id, pin in new_members.items():
            if pin != old_members[member_id]:
                self.assertEqual(pin["role"], "source-closure-mapping", member_id)
        self.assertEqual(old["input_bindings"], new["input_bindings"])
        self.assertEqual(len(old["entrypoints"]), len(new["entrypoints"]))


class PackageSchemaV37(unittest.TestCase):
    def _issues(self, package_path: Path, registry: Path) -> list[Any]:
        package = _package(package_path)
        corpus = _corpus()
        members = {(m["id"], m["version"]): corpus[(m["id"], m["version"])] for m in package["members"]}
        result = validate_package(package, members, DerivationSchemas(), load_published_citizen_checksums(registry))
        return list(result.issues)

    def test_v37_validates_v69_and_v36_still_validates_v68(self) -> None:
        self.assertEqual(_package(PACKAGE_V69)["schema"], "artifact-package.v37")
        self.assertEqual(_package(PACKAGE_V68)["schema"], "artifact-package.v36")
        self.assertEqual(self._issues(PACKAGE_V69, REGISTRY_V67), [])
        self.assertEqual(self._issues(PACKAGE_V68, REGISTRY_V66), [])

    def test_v36_still_refuses_a_v3_mapping_and_v37_admits_only_that_more(self) -> None:
        schemas = DerivationSchemas()
        v36 = _package(PACKAGE_V69)
        v36["schema"] = "artifact-package.v36"
        with self.assertRaises(SchemaValidationError):
            schemas.validate_declared(v36)
        v36_doc = json.loads((ROOT / "packages/schemas/derivation/artifact-package.v36.schema.json").read_text("utf-8"))
        v37_doc = json.loads((ROOT / "packages/schemas/derivation/artifact-package.v37.schema.json").read_text("utf-8"))
        text36 = json.dumps(v36_doc, sort_keys=True).replace("artifact-package.v36", "artifact-package.v37")
        text37 = json.dumps(v37_doc, sort_keys=True).replace('"source-closure-mapping.v2", "source-closure-mapping.v3"', '"source-closure-mapping.v2"')
        self.assertEqual(text36, text37)

    def test_registry_v67_only_adds_to_v66(self) -> None:
        old, new = _package(REGISTRY_V66), _package(REGISTRY_V67)
        self.assertEqual(len(new["citizens"]), len(old["citizens"]) + 51)
        old_c = {(c["id"], c["version"]): c["checksum"] for c in old["citizens"]}
        new_c = {(c["id"], c["version"]): c["checksum"] for c in new["citizens"]}
        self.assertTrue(old_c.items() <= new_c.items())
        old_p = {(c["id"], c["version"]): c["checksum"] for c in old["packages"]}
        new_p = {(c["id"], c["version"]): c["checksum"] for c in new["packages"]}
        self.assertTrue(old_p.items() <= new_p.items())
        self.assertEqual(set(new_p) - set(old_p), {("tax.us.2025.package.core-calculations", "v69")})

    def test_release_v67_pins_registry_v67_and_v69_shares_v68s_declaration(self) -> None:
        import hashlib
        from packages.tax.loader import domain_package_companion_declarations

        release = _package(RELEASE_V67)
        self.assertEqual(release["version"], "v67")
        self.assertEqual(release["package_registry_sha256"], hashlib.sha256(REGISTRY_V67.read_bytes()).hexdigest())
        declarations = domain_package_companion_declarations()
        core = "tax.us.2025.package.core-calculations"
        self.assertEqual(declarations[(core, "v69")], declarations[(core, "v68")])


def _run_core(acts: list[dict[str, object]], run_id: str, *, core: str) -> IRun:
    return _present(acts, run_id, core=core)[0]


def _present(acts: list[dict[str, object]], run_id: str, *, core: str) -> tuple[IRun, dict[str, Any], bytes]:
    """Run a return on core v68 or v69 through ``live_coordinate_run`` and return what it published
    and blocked, the saved presentation model and the page built from it; a base "none"
    declaration that a recorded member contradicts is withdrawn first."""
    package, release, rel_version, registry = (
        (PACKAGE_V69, RELEASE_V67, "v67", REGISTRY_V67) if core == "v69" else (PACKAGE_V68, RELEASE_V66, "v66", REGISTRY_V66)
    )
    surface = PublicationSurface(RELEASE_DIR, registry, TAX_CONTENT_DIR)
    for _ in range(5):
        finished = _finish(
            copy.deepcopy(acts), package_path=package, package_version=core,
            release_path=release, release_version=rel_version, note=run_id,
        )
        finished = _handover(finished, surface=surface, reconfirm=True)
        try:
            with TemporaryDirectory() as tmp:
                outcome = live_coordinate_run(
                    WorkspaceCapability(Path(tmp) / "L"),
                    repo_root=ROOT,
                    authoritative_acts=finished,
                    workspace_revision=len(finished),
                    run_scope={"jurisdiction": "us", "year": "2025"},
                    scope_user="demo.user.filer-1",
                    request={"schema": "run-request.v1"},
                    run_id=run_id,
                    governance_pins=[],
                    surface=surface,
                    output_name="out.json",
                )
                if outcome.refusal is not None:
                    raise AssertionError(f"{run_id} refused: {outcome.refusal.reason} {outcome.refusal.detail}")
                pubs = {str(p.finding["symbol"]): p.finding for p in outcome.publications or ()}
                blocked: list[dict[str, Any]] = []
                if outcome.output_path is not None:
                    report = json.loads(outcome.output_path.read_text(encoding="utf-8"))
                    blocked = [r for r in report.get("dispositions", []) if r.get("disposition") == "blocked"]
                assert outcome.presentation_path is not None
                model = json.loads(outcome.presentation_path.read_text(encoding="utf-8"))
                page = _render_page(ROOT, WorkspaceCapability(Path(tmp) / "L"), outcome.presentation_path)
            return IRun(pubs, blocked), model, page
        except FindingModelError as exc:
            found = re.search(r"contradiction: (\S+) is currently", str(exc))
            if not found:
                raise
            acts = _strip_closure(acts, found.group(1))
    raise AssertionError("too many declaration withdrawals")


class CoreV69ValuesAreUnchanged(unittest.TestCase):
    def test_two_complete_returns_publish_the_same_values_and_blocks_on_v68_and_v69(self) -> None:
        for name, acts in (
            ("b1", _interest([100.0, 100.0])),
            ("b1b3", _interest([300.0], [200.0])),
        ):
            with self.subTest(name):
                old = _run_core(acts, f"demo.cq.{name}.v68", core="v68")
                new = _run_core(acts, f"demo.cq.{name}.v69", core="v69")
                self.assertTrue(old.pubs)
                self.assertEqual(new.values(), old.values())
                self.assertEqual(new.blocked_codes(), old.blocked_codes())


P = "tax.us.2025."
G4_QUESTION = "Have you recorded every federal income tax withheld amount in box 4 of every Form 1099-G you or your spouse received for 2025?"
INT1_QUESTION = "Have you recorded every interest income amount in box 1 of every Form 1099-INT you or your spouse received for 2025?"
G4_LINES = ("line-25b", "line-25d", "line-33", "line-34", "line-35a", "line-37")


def _unconfirmed(*families: str) -> list[dict[str, object]]:
    """The base return plus one recorded member in each named family and no closure answer."""
    acts = w2g._w2g_return([])
    for index, family in enumerate(families):
        acts = cc._add_member(acts, P + family, 600.0, close=False, tag=f"cq{index}")
    return acts


def _blocked_sections(model: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {s["id"]: s for s in model["sections"] if s["resolved"]["disposition"] == "blocked"}


def _reasons(section: dict[str, Any]) -> list[dict[str, str]]:
    value: list[dict[str, str]] = section["resolved"].get("reasons", [])
    return value


class BlockedLinesNameTheirQuestion(unittest.TestCase):
    def test_the_mapping_question_matches_the_asserted_text(self) -> None:
        self.assertEqual(_corpus()[("tax.us.2025.closure-mapping.f1099g-b4", "v2")]["closure_question"], G4_QUESTION)
        self.assertEqual(_corpus()[("tax.us.2025.closure-mapping.f1099int-b1", "v2")]["closure_question"], INT1_QUESTION)

    def test_unconfirmed_1099g_box4_names_its_question_on_every_line_it_blocks(self) -> None:
        _run, model, _page = _present(_unconfirmed("f1099g.b4"), "demo.cq.g4.v69", core="v69")
        blocked = _blocked_sections(model)
        for line in G4_LINES:
            with self.subTest(line):
                self.assertIn(line, blocked)
                self.assertEqual(_reasons(blocked[line]), [{"sentence": G4_QUESTION}])
        for section_id, section in blocked.items():
            self.assertTrue(_reasons(section), f"{section_id} blocked without its question")
        validate_presentation_model(model)

    def test_unconfirmed_1099int_box1_names_its_question_on_line_2b_and_every_line_behind_it(self) -> None:
        _run, model, _page = _present(_unconfirmed("f1099int.b1"), "demo.cq.int1.v69", core="v69")
        blocked = _blocked_sections(model)
        self.assertIn("line-2b", blocked)
        self.assertEqual(_reasons(blocked["line-2b"]), [{"sentence": INT1_QUESTION}])
        for section_id, section in blocked.items():
            self.assertEqual(_reasons(section), [{"sentence": INT1_QUESTION}], section_id)
        validate_presentation_model(model)

    def test_a_line_reached_by_two_unconfirmed_families_carries_both_questions_once(self) -> None:
        _run, model, _page = _present(_unconfirmed("f1099g.b4", "f1099int.b1"), "demo.cq.both.v69", core="v69")
        blocked = _blocked_sections(model)
        both = sorted({G4_QUESTION, INT1_QUESTION})
        self.assertEqual([r["sentence"] for r in _reasons(blocked["line-37"])], both)
        self.assertEqual([r["sentence"] for r in _reasons(blocked["line-25b"])], [G4_QUESTION])
        self.assertEqual([r["sentence"] for r in _reasons(blocked["line-2b"])], [INT1_QUESTION])
        for section in blocked.values():
            sentences = [r["sentence"] for r in _reasons(section)]
            self.assertEqual(sentences, sorted(set(sentences)))

    def test_core_v68_with_v2_mappings_adds_no_reason_anywhere(self) -> None:
        for name, acts in (("g4", _unconfirmed("f1099g.b4")), ("int1", _unconfirmed("f1099int.b1"))):
            with self.subTest(name):
                run, model, _page = _present(acts, f"demo.cq.{name}.v68", core="v68")
                self.assertTrue(run.blocked)
                blocked = _blocked_sections(model)
                self.assertTrue(blocked)
                for section in model["sections"]:
                    self.assertNotIn("reasons", section["resolved"])
                saved = json.dumps(model, sort_keys=True)
                self.assertNotIn(G4_QUESTION, saved)
                self.assertNotIn(INT1_QUESTION, saved)

    def test_v69_changes_nothing_but_the_reasons_on_blocked_lines(self) -> None:
        for name, acts in (("g4", _unconfirmed("f1099g.b4")), ("int1", _unconfirmed("f1099int.b1"))):
            with self.subTest(name):
                old_run, old_model, _ = _present(acts, f"demo.cq.{name}.same.v68", core="v68")
                new_run, new_model, _ = _present(acts, f"demo.cq.{name}.same.v69", core="v69")
                self.assertEqual(new_run.values(), old_run.values())
                self.assertEqual(new_run.blocked_codes(), old_run.blocked_codes())
                self.assertEqual([s["id"] for s in new_model["sections"]], [s["id"] for s in old_model["sections"]])
                for old, new in zip(old_model["sections"], new_model["sections"]):
                    stripped = {k: v for k, v in new["resolved"].items() if k != "reasons"}
                    self.assertEqual(stripped["disposition"], old["resolved"]["disposition"])
                    self.assertEqual(stripped.get("activeCodes"), old["resolved"].get("activeCodes"))

    def test_a_complete_return_gains_no_reason(self) -> None:
        acts = _interest([100.0, 100.0])
        _old_run, old_model, _ = _present(acts, "demo.cq.complete.v68", core="v68")
        _new_run, new_model, _ = _present(acts, "demo.cq.complete.v69", core="v69")
        for model in (old_model, new_model):
            for section in model["sections"]:
                self.assertNotIn("reasons", section["resolved"])
        self.assertEqual(
            [(s["id"], s["resolved"]["disposition"]) for s in new_model["sections"]],
            [(s["id"], s["resolved"]["disposition"]) for s in old_model["sections"]],
        )

    def test_the_page_shows_the_question_as_the_reason(self) -> None:
        if BROWSER is None:
            self.skipTest("no headless browser available")
        import subprocess

        _run, _model, page = _present(_unconfirmed("f1099g.b4"), "demo.cq.page.v69", core="v69")
        with TemporaryDirectory() as tmp:
            path = Path(tmp) / "page.html"
            path.write_bytes(page)
            dom = subprocess.run(
                [BROWSER, "--headless", "--disable-gpu", "--no-sandbox", "--dump-dom", path.as_uri()],
                check=True, capture_output=True, text=True, timeout=60,
            ).stdout
        self.assertIn(G4_QUESTION, dom)
        self.assertIn("Why:", dom)


if __name__ == "__main__":
    unittest.main()
