"""Core v72: a blocked line names the question for a missing amount (missing-input-questions).

``input-question.v1`` declares, per fact type, what a filer enters; ``artifact-package.v39`` admits it;
the presentation projection copies the sentence verbatim as the reason on a line whose every cause has
one (a missing amount, an unconfirmed family, or both). Every case runs through ``live_coordinate_run``
on the committed packages and reads the saved presentation model. Hand expectations are the P0 design's
(``missing-input-questions-evidence/p0-survey-and-design.md``, section 7). Synthetic ``demo.*`` data only.
"""

from __future__ import annotations

import copy
import json
import unittest
from functools import lru_cache
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any, Callable
from unittest import mock

from packages.derivation import presentation_projection as pp
from packages.derivation.authorization_closure import build_dependency_edges
from packages.derivation.live import live_coordinate_run
from packages.derivation.live_workspace import WorkspaceCapability
from packages.derivation.loader import DerivationSchemas
from packages.derivation.package_validation import (
    INPUT_QUESTION_SCHEMAS,
    load_published_citizen_checksums,
    validate_package,
)
from packages.derivation.production_resolver import PublicationSurface
from packages.kernel.findings import FindingModelError
from packages.kernel.schema_registry import SchemaValidationError
from packages.tax.loader import TAX_CONTENT_DIR, domain_package_companion_declarations
from tests import test_w2g_gambling as w2g  # noqa: F401  (adopts the W-2G answers the builders need)
from tests.helpers import current_core_returns as c
from tests.test_form_1099_k_income import _handover
from tests.test_form_1099_withholding import YEAR
from tests.test_refund_or_amount_owed_track1 import _finish
from tests.test_statement_withholding_answer import _no_withholding, family_return
from tests.test_withholding_closure import _set_closure

ROOT = Path(__file__).resolve().parents[1]
CONTENT = c.CONTENT
RELEASE_DIR = c.RELEASE_DIR
P = c.P
CORES = {  # core vN pairs with registry and release v(N-2)
    f"v{n}": (f"package.core-calculations.v{n}.json", f"v{n}", f"demo.release.sli-worksheet-integration.2025.v{n - 2}.json",
              f"v{n - 2}", f"published-packages.v{n - 2}.json")
    for n in (68, 69, 70, 71, 72)
}
CORE = "tax.us.2025.package.core-calculations"

# The wording the foreman decided (plan, Decisions 2), verbatim.
QUESTION = {
    "w2.box2-withholding": "Enter the federal income tax withheld in box 2 of each Form W-2 you or your spouse received for 2025. If box 2 is blank, enter $0.",
    "f1099int.box4-withholding": "Enter the federal income tax withheld in box 4 of each Form 1099-INT you or your spouse received for 2025. If box 4 is blank, enter $0.",
    "f1099div.box4-withholding": "Enter the federal income tax withheld in box 4 of each Form 1099-DIV you or your spouse received for 2025. If box 4 is blank, enter $0.",
    "f1099r.ira-box4-withholding": "Enter the federal income tax withheld in box 4 of each Form 1099-R you or your spouse received for 2025. If box 4 is blank, enter $0.",
    "f1099g.box4-withholding": "Enter the federal income tax withheld in box 4 of each Form 1099-G you or your spouse received for 2025. If box 4 is blank, enter $0.",
    "ssa1099.box6-voluntary-withholding": "Enter the voluntary federal income tax withheld in box 6 of each Form SSA-1099 you or your spouse received for 2025. If box 6 is blank, enter $0.",
    "payments.estimated-and-prior-year-applied": "Enter the estimated tax payments you made for 2025, plus any 2024 overpayment you applied to 2025. If there were none, enter $0.",
    "payments.overpayment-applied-to-2026": "Enter how much of your 2025 overpayment you want applied to your 2026 estimated tax. If none, enter $0.",
}
CLOSURE_INT_B4 = ("Have you recorded every federal income tax withheld amount in box 4 of every Form 1099-INT "
                  "you or your spouse received for 2025?")
CLOSURE_DIV_B4 = ("Have you recorded every federal income tax withheld amount in box 4 of every Form 1099-DIV "
                  "you or your spouse received for 2025?")
CHAIN_25B = ["25b", "25d", "33", "34", "35a", "37"]
CHAIN_25A = ["25a", "25d", "33", "34", "35a", "37"]


def run_model(acts: list[dict[str, object]], name: str, core: str) -> dict[str, Any]:
    """The saved presentation model of one run through the real coordinator."""
    package, version, release, rel_version, registry = CORES[core]
    surface = PublicationSurface(RELEASE_DIR, CONTENT / registry, CONTENT)
    finished = _handover(
        _finish(copy.deepcopy(acts), package_path=CONTENT / package, package_version=version,
                release_path=RELEASE_DIR / release, release_version=rel_version, note=name),
        surface=surface, reconfirm=True)
    with TemporaryDirectory() as tmp:
        outcome = live_coordinate_run(
            WorkspaceCapability(Path(tmp) / "L"), repo_root=ROOT, authoritative_acts=finished,
            workspace_revision=len(finished), run_scope={"jurisdiction": "us", "year": YEAR},
            scope_user=c.USER, request={"schema": "run-request.v1"}, run_id=name, governance_pins=[],
            surface=surface, output_name="out.json")
        assert outcome.refusal is None, f"{name} refused: {outcome.refusal}"
        assert outcome.presentation_path is not None
        model: dict[str, Any] = json.loads(outcome.presentation_path.read_text(encoding="utf-8"))
    return model


def drop(acts: list[dict[str, object]], *fact_types: str) -> list[dict[str, object]]:
    kept = [a for a in acts if str(a["payload"].get("finding", {}).get("fact_id", "")).split("|")[0] not in fact_types]  # type: ignore[attr-defined]
    assert len(kept) < len(acts), fact_types
    return c._renumbered(copy.deepcopy(kept))


def blocked(model: dict[str, Any]) -> dict[str, list[str] | None]:
    """Blocked line -> its reason sentences (None when it keeps the generic text)."""
    out: dict[str, list[str] | None] = {}
    for section in model["sections"]:
        resolved = section["resolved"]
        if resolved["disposition"] == "blocked":
            reasons = resolved.get("reasons")
            out[str(section["field"]["line"])] = [r["sentence"] for r in reasons] if reasons else None
    return out


def only(model: dict[str, Any], lines: list[str], sentences: list[str]) -> None:
    got = blocked(model)
    assert sorted(got) == sorted(lines), (sorted(got), sorted(lines))
    for line in lines:
        assert got[line] == sentences, (line, got[line], sentences)


def base() -> list[dict[str, object]]:
    return _no_withholding()


# --- builders ---------------------------------------------------------------------------------


def ira_box4_missing() -> list[dict[str, object]]:
    return family_return("ira", 1, [None])


def box2_missing() -> list[dict[str, object]]:
    return drop(base(), P + "w2.box2-withholding")


def box2_missing_and_int_b4_unconfirmed() -> list[dict[str, object]]:
    return drop(_set_closure(family_return("int", 1, [50.0]), "int", "none"), P + "w2.box2-withholding")


def line26_missing() -> list[dict[str, object]]:
    return drop(base(), P + "payments.estimated-and-prior-year-applied")


def line36_missing() -> list[dict[str, object]]:
    return drop(base(), P + "payments.overpayment-applied-to-2026")


def sli_witness_missing() -> list[dict[str, object]]:
    acts = c.add_student_loan_interest_1098e(c.base_return(), [500.0])
    return drop(acts, P + "f1098e.no-related-person-interest")


def sli_witness_and_box2_missing() -> list[dict[str, object]]:
    return drop(sli_witness_missing(), P + "w2.box2-withholding")


def rounding_missing() -> list[dict[str, object]]:
    return drop(base(), "rounding.convention")


def scope_answer_missing() -> list[dict[str, object]]:
    return drop(base(), P + "line2a-scope.no-amt-form-6251")


def div_b4_unconfirmed() -> list[dict[str, object]]:
    return _set_closure(family_return("int", 1, [None]), "div", "none")


BUILDERS: dict[str, Callable[[], list[dict[str, object]]]] = {
    "ira-box4": ira_box4_missing,
    "box2": box2_missing,
    "mixed": box2_missing_and_int_b4_unconfirmed,
    "line26": line26_missing,
    "line36": line36_missing,
    "sli": sli_witness_missing,
    "sli+box2": sli_witness_and_box2_missing,
    "rounding": rounding_missing,
    "scope": scope_answer_missing,
    "div-b4": div_b4_unconfirmed,
    "int-box4": lambda: family_return("int", 1, [None]),
    "div-box4": lambda: family_return("div", 1, [None]),
    "g-box4": lambda: family_return("g", 1, [None]),
    "ssa-box6": lambda: family_return("ssa", 1, [None]),
    "two-int-second-missing": lambda: family_return("int", 2, [50.0, None]),
    "complete": base,
}


@lru_cache(maxsize=None)
def model(case: str, core: str = "v72") -> str:
    return json.dumps(run_model(BUILDERS[case](), f"demo.miq.{case}.{core}", core), sort_keys=True)


def loaded(case: str, core: str = "v72") -> dict[str, Any]:
    value: dict[str, Any] = json.loads(model(case, core))
    return value


class CasesOnV72(unittest.TestCase):
    def test_e1_a_missing_1099_r_box4_names_the_box_and_that_zero_counts(self) -> None:
        question = QUESTION["f1099r.ira-box4-withholding"]
        self.assertIn("box 4", question)
        self.assertIn("$0", question)
        only(loaded("ira-box4"), CHAIN_25B, [question])

    def test_e2_a_missing_w2_box2_names_it_on_25a_and_every_total_behind(self) -> None:
        only(loaded("box2"), CHAIN_25A, [QUESTION["w2.box2-withholding"]])

    def test_e3_each_other_withholding_amount_names_its_own_question(self) -> None:
        for case, fact in (("int-box4", "f1099int.box4-withholding"), ("div-box4", "f1099div.box4-withholding"),
                           ("g-box4", "f1099g.box4-withholding"), ("ssa-box6", "ssa1099.box6-voluntary-withholding")):
            with self.subTest(case=case):
                only(loaded(case), CHAIN_25B, [QUESTION[fact]])

    def test_a_second_statement_without_its_answer_names_the_same_question(self) -> None:
        only(loaded("two-int-second-missing"), CHAIN_25B, [QUESTION["f1099int.box4-withholding"]])

    def test_e4_a_line_with_a_missing_amount_and_an_unconfirmed_family_names_both_sorted(self) -> None:
        got = blocked(loaded("mixed"))
        self.assertEqual(sorted(got), ["25a", "25b", "25d", "33", "34", "35a", "37"])
        self.assertEqual(got["25a"], [QUESTION["w2.box2-withholding"]])
        self.assertEqual(got["25b"], [CLOSURE_INT_B4])
        both = [QUESTION["w2.box2-withholding"], CLOSURE_INT_B4]  # string order: "Enter ..." before "Have ..."
        self.assertEqual(both, sorted(both))
        for line in ("25d", "33", "34", "35a", "37"):
            self.assertEqual(got[line], both, line)

    def test_e5_a_missing_estimated_payments_amount_names_line_26_and_the_totals(self) -> None:
        only(loaded("line26"), ["26", "33", "34", "35a", "37"], [QUESTION["payments.estimated-and-prior-year-applied"]])

    def test_a_missing_amount_applied_to_2026_names_line_35a(self) -> None:
        only(loaded("line36"), ["35a"], [QUESTION["payments.overpayment-applied-to-2026"]])

    def test_e6_a_derived_cause_keeps_the_generic_text(self) -> None:
        got = blocked(loaded("sli"))
        self.assertGreater(len(got), 20)
        reasoned = {line for line, reasons in got.items() if reasons}
        # the originating line keeps the statement reason it already had; nothing else gains one
        self.assertEqual(reasoned, {"sch1-21"})
        self.assertNotIn(None, [got["sch1-21"]])

    def test_e7_a_derived_cause_beside_a_missing_amount_names_only_where_every_cause_has_a_sentence(self) -> None:
        got = blocked(loaded("sli+box2"))
        for line in ("25a", "25d"):
            self.assertEqual(got[line], [QUESTION["w2.box2-withholding"]], line)
        for line in ("33", "34", "35a", "37"):
            self.assertIsNone(got[line], line)

    def test_e8_a_fact_the_application_supplies_keeps_the_generic_text(self) -> None:
        got = blocked(loaded("rounding"))
        self.assertTrue(got)
        self.assertEqual({r for r in got.values() if r}, set())

    def test_e9_a_scope_answer_has_no_question_yet_and_keeps_the_generic_text(self) -> None:
        got = blocked(loaded("scope"))
        self.assertIn("2a", got)
        self.assertEqual({r for r in got.values() if r}, set())

    def test_a_line_held_only_by_an_unconfirmed_family_is_as_on_v71(self) -> None:
        got = blocked(loaded("div-b4"))
        self.assertEqual(sorted(got), CHAIN_25B)
        for line in CHAIN_25B:
            self.assertEqual(got[line], [CLOSURE_DIV_B4])

    def test_e11_a_negative_box4_is_refused_before_any_run(self) -> None:
        with self.assertRaises(FindingModelError):
            run_model(family_return("int", 1, [-5.0]), "demo.miq.negative", "v72")

    def test_a_complete_return_blocks_nothing(self) -> None:
        self.assertEqual(blocked(loaded("complete")), {})


# --- earlier cores render exactly as before -----------------------------------------------------


def _reference_closure_question_reasons(row: Any, *, resolved_members: Any, by_symbol: Any) -> list[dict[str, Any]]:
    """The v69 algorithm as it stood before the input question (the closure roots only)."""
    questions: dict[str, str] = {}
    for member in resolved_members:
        question = member.get("closure_question")
        family = member.get("family")
        if (str(member.get("schema", "")).startswith("source-closure-mapping.")
                and isinstance(question, str) and question.strip() and isinstance(family, dict)):
            questions[str(family.get("id"))] = question
    families: set[str] = set()

    def reach(current: Any, seen: frozenset[str]) -> bool:
        if current.get("code") == "SOURCE_SET_UNCLOSED":
            missing = current.get("missing")
            if not isinstance(missing, list) or not missing:
                return False
            families.update(str(family) for family in missing)
            return True
        missing = current.get("missing")
        if not isinstance(missing, list) or not missing:
            return False
        for symbol in missing:
            if symbol in seen:
                continue
            blocked_rows = [r for r in by_symbol.get(str(symbol), []) if r.get("disposition") == "blocked"]
            if not blocked_rows or not all(reach(r, seen | {str(symbol)}) for r in blocked_rows):
                return False
        return True

    if not reach(row, frozenset()) or not families or any(family not in questions for family in families):
        return []
    return [{"sentence": sentence} for sentence in sorted({questions[family] for family in families})]


class EarlierCoresAreUnchanged(unittest.TestCase):
    CASES = ("box2", "mixed", "div-b4", "int-box4", "ira-box4", "sli", "scope", "line26", "complete")

    def test_v68_to_v71_saved_presentations_are_byte_identical_to_the_previous_projection(self) -> None:
        for core in ("v68", "v69", "v70", "v71"):
            for case in self.CASES:
                with self.subTest(core=core, case=case):
                    after = model(case, core)
                    with mock.patch.object(pp, "_closure_question_reasons", _reference_closure_question_reasons):
                        before = json.dumps(run_model(BUILDERS[case](), f"demo.miq.{case}.{core}", core), sort_keys=True)
                    self.assertEqual(after, before)

    def test_v71_names_no_missing_amount(self) -> None:
        got = blocked(loaded("box2", "v71"))
        self.assertEqual(sorted(got), sorted(CHAIN_25A))
        self.assertEqual({r for r in got.values() if r}, set())

    def test_v69_to_v71_still_name_a_line_held_only_by_a_closure(self) -> None:
        for core in ("v69", "v70", "v71"):
            got = blocked(loaded("div-b4", core))
            self.assertEqual({tuple(r or ()) for r in got.values()}, {(CLOSURE_DIV_B4,)}, core)

    def test_v72_blocks_exactly_the_lines_v71_does(self) -> None:
        for case in ("box2", "ira-box4", "mixed", "sli", "scope"):
            with self.subTest(case=case):
                self.assertEqual(sorted(blocked(loaded(case, "v71"))), sorted(blocked(loaded(case, "v72"))))


# --- the declaration --------------------------------------------------------------------------


def _citizen(slug: str) -> dict[str, Any]:
    value: dict[str, Any] = json.loads((CONTENT / f"input-question.{slug}.v1.json").read_text("utf-8"))
    return value


def _package(name: str) -> dict[str, Any]:
    value: dict[str, Any] = json.loads((CONTENT / name).read_text("utf-8"))
    return value


def _corpus() -> dict[tuple[str, str], dict[str, Any]]:
    out: dict[tuple[str, str], dict[str, Any]] = {}
    for path in CONTENT.glob("*.json"):
        try:
            body = json.loads(path.read_text("utf-8"))
        except ValueError:
            continue
        if isinstance(body, dict) and "id" in body and "version" in body:
            out[(body["id"], body["version"])] = body
    return out


class Declaration(unittest.TestCase):
    def test_the_admitted_schema_set(self) -> None:
        self.assertEqual(INPUT_QUESTION_SCHEMAS, {"input-question.v1"})

    def test_a_citizen_validates_and_a_blank_or_missing_question_is_refused(self) -> None:
        schemas = DerivationSchemas()
        good = _citizen("w2-box2")
        self.assertEqual(schemas.validate_declared(good), "input-question.v1")
        for blank in ("", "   ", "\t", " \n "):
            bad = copy.deepcopy(good)
            bad["question"] = blank
            with self.subTest(blank=blank), self.assertRaises(SchemaValidationError):
                schemas.validate_declared(bad)
        missing = copy.deepcopy(good)
        del missing["question"]
        with self.assertRaises(SchemaValidationError):
            schemas.validate_declared(missing)
        extra = copy.deepcopy(good)
        extra["note"] = "x"
        with self.assertRaises(SchemaValidationError):
            schemas.validate_declared(extra)

    def test_eight_citizens_carry_the_decided_wording_verbatim(self) -> None:
        corpus = _corpus()
        package = _package("package.core-calculations.v72.json")
        pinned = [m for m in package["members"] if m["role"] == "input-question"]
        self.assertEqual(len(pinned), 8)
        got = {}
        for pin in pinned:
            body = corpus[(pin["id"], pin["version"])]
            self.assertEqual(body["schema"], "input-question.v1")
            got[body["fact_type"]["id"].removeprefix(P)] = body["question"]
        self.assertEqual(got, QUESTION)

    def test_v72_validates_and_v71_still_does(self) -> None:
        corpus = _corpus()
        for name, registry, schema in (("package.core-calculations.v72.json", "published-packages.v70.json", "artifact-package.v39"),
                                       ("package.core-calculations.v71.json", "published-packages.v69.json", "artifact-package.v38")):
            package = _package(name)
            self.assertEqual(package["schema"], schema)
            members = {(m["id"], m["version"]): corpus[(m["id"], m["version"])] for m in package["members"]}
            result = validate_package(package, members, DerivationSchemas(),
                                      load_published_citizen_checksums(CONTENT / registry))
            self.assertEqual(list(result.issues), [], name)

    def test_v38_refuses_an_input_question_and_v39_differs_only_by_it(self) -> None:
        v72 = _package("package.core-calculations.v72.json")
        v72["schema"] = "artifact-package.v38"
        with self.assertRaises(SchemaValidationError):
            DerivationSchemas().validate_declared(v72)
        d = ROOT / "packages/schemas/derivation"
        t38 = json.dumps(json.loads((d / "artifact-package.v38.schema.json").read_text("utf-8")), sort_keys=True)
        t39 = json.dumps(json.loads((d / "artifact-package.v39.schema.json").read_text("utf-8")), sort_keys=True)
        t39 = (t39.replace("artifact-package.v39", "artifact-package.v38")
               .replace('"input-question.v1", ', "").replace('"input-question", ', ""))
        self.assertEqual(t38, t39)

    def test_a_wrong_role_or_an_unadmitted_fact_type_is_refused(self) -> None:
        corpus = _corpus()
        package = copy.deepcopy(_package("package.core-calculations.v72.json"))
        for member in package["members"]:
            if member["id"] == "tax.us.2025.input-question.w2-box2":
                member["role"] = "citation"
        members = {(m["id"], m["version"]): corpus[(m["id"], m["version"])] for m in package["members"]}
        codes = {i.code for i in validate_package(package, members, DerivationSchemas()).issues}
        self.assertIn("ROLE_MISMATCH", codes)

        package = _package("package.core-calculations.v72.json")
        members = {(m["id"], m["version"]): copy.deepcopy(corpus[(m["id"], m["version"])]) for m in package["members"]}
        members[("tax.us.2025.input-question.w2-box2", "v1")]["fact_type"] = {"id": "tax.us.2025.no-such-fact", "version": "v1"}
        codes = {i.code for i in validate_package(package, members, DerivationSchemas()).issues}
        self.assertIn("INPUT_QUESTION_FACT_TYPE_NOT_ADMITTED", codes)

    def test_authorization_closure_gives_an_input_question_an_edge_to_its_fact_type(self) -> None:
        corpus = _corpus()
        package = _package("package.core-calculations.v72.json")
        members = {m["id"]: corpus[(m["id"], m["version"])] for m in package["members"]}
        edges = build_dependency_edges(members, package=package)
        self.assertTrue(edges["tax.us.2025.input-question.w2-box2"])

    def test_registry_v70_only_adds_to_v69_and_release_v70_pins_it(self) -> None:
        import hashlib
        old, new = _package("published-packages.v69.json"), _package("published-packages.v70.json")
        self.assertEqual(len(new["citizens"]), len(old["citizens"]) + 8)
        old_c = {(x["id"], x["version"]): x["checksum"] for x in old["citizens"]}
        new_c = {(x["id"], x["version"]): x["checksum"] for x in new["citizens"]}
        self.assertTrue(old_c.items() <= new_c.items())
        old_p = {(x["id"], x["version"]): x["checksum"] for x in old["packages"]}
        new_p = {(x["id"], x["version"]): x["checksum"] for x in new["packages"]}
        self.assertTrue(old_p.items() <= new_p.items())
        self.assertEqual(set(new_p) - set(old_p), {(CORE, "v72")})
        release = json.loads((RELEASE_DIR / CORES["v72"][2]).read_text("utf-8"))
        self.assertEqual(release["version"], "v70")
        self.assertEqual(release["package_registry_sha256"],
                         hashlib.sha256((CONTENT / "published-packages.v70.json").read_bytes()).hexdigest())

    def test_v72_changes_only_what_it_adds_and_shares_v71s_companion_declaration(self) -> None:
        v71, v72 = _package("package.core-calculations.v71.json"), _package("package.core-calculations.v72.json")
        pins71 = {(m["id"], m["version"]) for m in v71["members"]}
        pins72 = {(m["id"], m["version"]) for m in v72["members"]}
        self.assertEqual(pins71 - pins72, set())
        self.assertEqual(len(pins72 - pins71), 8)
        self.assertEqual(v71["input_bindings"], v72["input_bindings"])
        declarations = domain_package_companion_declarations()
        self.assertEqual(declarations[(CORE, "v72")], declarations[(CORE, "v71")])
        self.assertTrue(TAX_CONTENT_DIR.exists())


if __name__ == "__main__":
    unittest.main()
