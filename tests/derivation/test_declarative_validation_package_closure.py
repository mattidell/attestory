"""ADR-0066 / Track 2: compiler-owned reachability synthesis and package
closure. Reachability, not authored `requires`, creates the
`<family>.member-validation` prerequisite; `accounts_for` is a
relationship-bearing intent assertion checked against reachability, never an
edge source.
"""

import copy
import json
import unittest
from pathlib import Path
from typing import Any, cast

from packages.derivation.package_validation import (
    validate_package,
    PackageValidation,
    compile_validation_graph,
    check_validation_graph,
    MemberIssue,
)
from packages.derivation.loader import DerivationSchemas

SAMPLE_DIR = Path(__file__).resolve().parent.parent.parent / "packages" / "sample_data" / "declarative_validation_contract"

FAMILY_A_ID = "declarativevalidation.demo-family"
FAMILY_B_ID = "declarativevalidation.demo-family-b"
FAMILY_SCALAR_ID = "declarativevalidation.demo-family-scalar"
FAMILY_A_PRODUCER_ID = f"{FAMILY_A_ID}.member-validation.synthesized"
FAMILY_A_SYMBOL = f"{FAMILY_A_ID}.member-validation"


def _load(name: str) -> dict[str, Any]:
    return cast(dict[str, Any], json.loads((SAMPLE_DIR / name).read_text("utf-8")))


class DeclarativeValidationPackageClosureTest(unittest.TestCase):
    schemas: DerivationSchemas

    @classmethod
    def setUpClass(cls) -> None:
        cls.schemas = DerivationSchemas()

    def setUp(self) -> None:
        self.pkg = _load("package.declarativevalidation.v1.json")
        self.sf = _load("source-family.declarativevalidation.demo-family.v1.json")
        self.sfb = _load("source-family.declarativevalidation.demo-family-b.v1.json")
        self.sf_scalar = _load("source-family.declarativevalidation.demo-family-scalar.v1.json")
        self.ra = _load("rule-artifact.declarativevalidation.demo-consumer.v1.json")
        self.ar = _load("attachment-rule.declarativevalidation.demo-attachment.v1.json")
        self.pp = _load("rule-artifact.declarativevalidation.demo-presentation.v1.json")
        self.unrelated = _load("rule-artifact.declarativevalidation.demo-unrelated.v1.json")
        self.ft = _load("fact-type.demo.fact.v1.json")
        self.scalar_rule = _load("rule-artifact.declarativevalidation.demo-scalar-consumer.v1.json")
        self.scalar_attachment = _load("attachment-rule.declarativevalidation.demo-scalar-attachment.v1.json")

        self.citizens = [
            self.sf, self.sfb, self.sf_scalar, self.ra, self.ar, self.pp,
            self.unrelated, self.ft, self.scalar_rule, self.scalar_attachment,
        ]
        self.families_by_id = {
            self.sf["id"]: self.sf,
            self.sfb["id"]: self.sfb,
            self.sf_scalar["id"]: self.sf_scalar,
        }
        self.families_by_subtotal = {
            self.sf["authorizes_subtotal"]: self.sf["id"],
            self.sfb["authorizes_subtotal"]: self.sfb["id"],
            self.sf_scalar["authorizes_subtotal"]: self.sf_scalar["id"],
        }

    def _validate(self, pkg: dict[str, Any], citizens: list[dict[str, Any]]) -> PackageValidation:
        corpus = {(c["id"], c["version"]): c for c in citizens}
        return validate_package(pkg, corpus, self.schemas)

    def _compiled(self) -> list[dict[str, Any]]:
        return compile_validation_graph(self.citizens, self.families_by_id, self.families_by_subtotal, self.schemas)

    def test_baseline_validates(self) -> None:
        res = self._validate(self.pkg, self.citizens)
        self.assertTrue(res.ok, res.issues)

    def test_missing_validation_producer_ambiguous(self) -> None:
        # Instead of manually publishing, we mutate the compiled graph by adding a second producer
        compiled = self._compiled()
        producer = [m for m in compiled if m["id"] == FAMILY_A_PRODUCER_ID][0]
        duplicate_producer = dict(producer)
        duplicate_producer["id"] = f"{FAMILY_A_ID}.member-validation.duplicate"
        compiled.append(duplicate_producer)

        issues = check_validation_graph(compiled, self.families_by_id, self.families_by_subtotal, self.pkg["id"])
        missing_producer = [iss for iss in issues if iss.code == "VALIDATION_PRODUCER_AMBIGUOUS"]
        self.assertEqual(len(missing_producer), 1)

    def test_synthesized_prerequisite_omitted(self) -> None:
        # Remove the synthesized consumer edge (the `.member-validation` require) from the compiled consumer
        compiled = self._compiled()

        for i, member in enumerate(compiled):
            if member["id"] == self.ra["id"]:
                mutated = dict(member)
                mutated["requires"] = [req for req in mutated.get("requires", []) if not req.endswith(".member-validation")]
                compiled[i] = mutated
                break

        issues = check_validation_graph(compiled, self.families_by_id, self.families_by_subtotal, self.pkg["id"])
        omitted_edge = [iss for iss in issues if iss.code == "SYNTHESIZED_PREREQUISITE_OMITTED"]
        self.assertEqual(len(omitted_edge), 1)

    def test_synthesized_prerequisite_omitted_for_attachment(self) -> None:
        # Attachments must receive the same omitted-edge check as rules
        # (Repair 5): removing the compiled `.member-validation` require from
        # an attachment must yield exactly one SYNTHESIZED_PREREQUISITE_OMITTED
        # for that attachment, not silence.
        compiled = self._compiled()

        for i, member in enumerate(compiled):
            if member["id"] == self.ar["id"]:
                mutated = dict(member)
                mutated["requires"] = [req for req in mutated.get("requires", []) if not req.endswith(".member-validation")]
                compiled[i] = mutated
                break

        issues = check_validation_graph(compiled, self.families_by_id, self.families_by_subtotal, self.pkg["id"])
        omitted_edge = [
            iss for iss in issues
            if iss.code == "SYNTHESIZED_PREREQUISITE_OMITTED" and iss.member_id == self.ar["id"]
        ]
        self.assertEqual(len(omitted_edge), 1)

    def test_validation_producer_missing(self) -> None:
        # Remove the compiled producer entirely. Five consumers structurally
        # reach the constrained whole family: the two direct rules (ra, pp),
        # the direct attachment (ar), and the scalar rule/attachment that
        # reach it only by widening through a projected family's
        # `projects_from` pin.
        compiled = self._compiled()
        compiled = [m for m in compiled if m["id"] != FAMILY_A_PRODUCER_ID]

        issues = check_validation_graph(compiled, self.families_by_id, self.families_by_subtotal, self.pkg["id"])
        missing = [iss for iss in issues if iss.code == "VALIDATION_PRODUCER_MISSING"]
        self.assertEqual(len(missing), 5)

    def test_reachability_not_authoring_creates_the_edge(self) -> None:
        # None of the three sample consumers author the validation symbol -
        # the compiler must add it purely from structural reachability.
        for consumer in (self.ra, self.pp):
            self.assertNotIn(FAMILY_A_SYMBOL, consumer.get("requires", []))

    def test_one_family_reached_by_several_consumers_yields_one_producer_and_edges(self) -> None:
        compiled = self._compiled()
        by_id = {m["id"]: m for m in compiled}

        producers = [
            m for m in compiled
            if m.get("publishes") == FAMILY_A_SYMBOL
        ]
        self.assertEqual(len(producers), 1)
        self.assertEqual(producers[0]["id"], FAMILY_A_PRODUCER_ID)

        for consumer_id in (
            self.ra["id"], self.pp["id"], self.ar["id"],
            self.scalar_rule["id"], self.scalar_attachment["id"],
        ):
            self.assertIn(FAMILY_A_SYMBOL, by_id[consumer_id].get("requires", []))

        issues = check_validation_graph(compiled, self.families_by_id, self.families_by_subtotal, self.pkg["id"])
        self.assertEqual(issues, [])

    def test_rule_reaching_projected_scalar_family_gets_widened_edge(self) -> None:
        # A rule that structurally reaches only the projected scalar family
        # must still receive the constrained whole family's synthesized edge -
        # `projects_from` widening, not the scalar family's own id.
        compiled = self._compiled()
        by_id = {m["id"]: m for m in compiled}

        producers = [m for m in compiled if m.get("publishes") == FAMILY_A_SYMBOL]
        self.assertEqual(len(producers), 1)
        self.assertIn(FAMILY_A_SYMBOL, by_id[self.scalar_rule["id"]].get("requires", []))
        self.assertNotIn(f"{FAMILY_SCALAR_ID}.member-validation", by_id[self.scalar_rule["id"]].get("requires", []))

    def test_attachment_reaching_projected_scalar_family_gets_widened_edge(self) -> None:
        compiled = self._compiled()
        by_id = {m["id"]: m for m in compiled}

        producers = [m for m in compiled if m.get("publishes") == FAMILY_A_SYMBOL]
        self.assertEqual(len(producers), 1)
        self.assertIn(FAMILY_A_SYMBOL, by_id[self.scalar_attachment["id"]].get("requires", []))
        self.assertNotIn(f"{FAMILY_SCALAR_ID}.member-validation", by_id[self.scalar_attachment["id"]].get("requires", []))

    def test_unrelated_consumer_receives_no_edge(self) -> None:
        compiled = self._compiled()
        by_id = {m["id"]: m for m in compiled}
        unrelated_compiled = by_id[self.unrelated["id"]]
        self.assertNotIn(FAMILY_A_SYMBOL, unrelated_compiled.get("requires", []))
        self.assertNotIn(f"{FAMILY_B_ID}.member-validation", unrelated_compiled.get("requires", []))

        issues = check_validation_graph(compiled, self.families_by_id, self.families_by_subtotal, self.pkg["id"])
        self.assertFalse(any(iss.member_id == self.unrelated["id"] for iss in issues))

    def test_family_accounting_not_declared(self) -> None:
        mutated = dict(self.ra)
        mutated["accounts_for"] = []
        citizens = [self.sf, self.sfb, mutated, self.ar, self.pp, self.unrelated, self.ft]
        compiled = compile_validation_graph(citizens, self.families_by_id, self.families_by_subtotal, self.schemas)

        issues = check_validation_graph(compiled, self.families_by_id, self.families_by_subtotal, self.pkg["id"])
        hits = [iss for iss in issues if iss.code == "FAMILY_ACCOUNTING_NOT_DECLARED" and iss.member_id == self.ra["id"]]
        self.assertEqual(len(hits), 1)

    def test_family_accounting_unreached_extra_relationship(self) -> None:
        mutated = copy.deepcopy(self.ra)
        mutated["accounts_for"].append({
            "family": {"id": FAMILY_A_ID, "version": "v1"},
            "relationship": "composes_line",
        })
        citizens = [self.sf, self.sfb, mutated, self.ar, self.pp, self.unrelated, self.ft]
        compiled = compile_validation_graph(citizens, self.families_by_id, self.families_by_subtotal, self.schemas)

        issues = check_validation_graph(compiled, self.families_by_id, self.families_by_subtotal, self.pkg["id"])
        hits = [iss for iss in issues if iss.code == "FAMILY_ACCOUNTING_UNREACHED" and iss.member_id == self.ra["id"]]
        self.assertEqual(len(hits), 1)

    def test_family_accounting_unreached_for_absent_family(self) -> None:
        # An accounts_for pair naming a family absent from the package is
        # extra intent like any other unreached pair: FAMILY_ACCOUNTING_UNREACHED,
        # never a separate FAMILY_ACCOUNTING_UNRESOLVED code (Repair 5 removes it).
        mutated = copy.deepcopy(self.ra)
        mutated["accounts_for"].append({
            "family": {"id": "declarativevalidation.nonexistent-family", "version": "v1"},
            "relationship": "reads_subtotal",
        })
        citizens = [self.sf, self.sfb, mutated, self.ar, self.pp, self.unrelated, self.ft]
        compiled = compile_validation_graph(citizens, self.families_by_id, self.families_by_subtotal, self.schemas)

        issues = check_validation_graph(compiled, self.families_by_id, self.families_by_subtotal, self.pkg["id"])
        hits = [iss for iss in issues if iss.code == "FAMILY_ACCOUNTING_UNREACHED" and iss.member_id == self.ra["id"]]
        self.assertEqual(len(hits), 1)
        self.assertFalse(any(iss.code == "FAMILY_ACCOUNTING_UNRESOLVED" for iss in issues))

    def test_family_accounting_wrong_version_yields_missing_and_extra(self) -> None:
        # Keep exact (family id, family version, relationship) comparison: a
        # wrong version is one missing reached pair plus one extra/unreached
        # declared pair, never collapsed into a single result.
        mutated = copy.deepcopy(self.ra)
        mutated["accounts_for"] = [{
            "family": {"id": FAMILY_A_ID, "version": "v2"},
            "relationship": "reads_subtotal",
        }]
        citizens = [self.sf, self.sfb, mutated, self.ar, self.pp, self.unrelated, self.ft]
        compiled = compile_validation_graph(citizens, self.families_by_id, self.families_by_subtotal, self.schemas)

        issues = check_validation_graph(compiled, self.families_by_id, self.families_by_subtotal, self.pkg["id"])
        not_declared = [
            iss for iss in issues
            if iss.code == "FAMILY_ACCOUNTING_NOT_DECLARED" and iss.member_id == self.ra["id"]
        ]
        unreached = [
            iss for iss in issues
            if iss.code == "FAMILY_ACCOUNTING_UNREACHED" and iss.member_id == self.ra["id"]
        ]
        self.assertEqual(len(not_declared), 1)
        self.assertEqual(len(unreached), 1)

    def test_projected_family_wrong_version_fails_deterministically(self) -> None:
        # A `projects_from` pin naming the right id but the wrong version must
        # not be accepted by id alone; it fails deterministically through the
        # existing VALIDATION_PRODUCER_MISSING vocabulary rather than raising.
        broken_family = copy.deepcopy(self.sf_scalar)
        broken_family["projects_from"]["version"] = "v99"
        families_by_id = dict(self.families_by_id)
        families_by_id[broken_family["id"]] = broken_family
        citizens = [
            self.sf, self.sfb, broken_family, self.ra, self.ar, self.pp,
            self.unrelated, self.ft, self.scalar_rule, self.scalar_attachment,
        ]

        compiled = compile_validation_graph(citizens, families_by_id, self.families_by_subtotal, self.schemas)
        issues = check_validation_graph(compiled, families_by_id, self.families_by_subtotal, self.pkg["id"])
        self.assertTrue(
            any(
                iss.code == "VALIDATION_PRODUCER_MISSING" and iss.member_id == self.scalar_rule["id"]
                for iss in issues
            ),
            issues,
        )
        self.assertTrue(
            any(
                iss.code == "VALIDATION_PRODUCER_MISSING" and iss.member_id == self.scalar_attachment["id"]
                for iss in issues
            ),
            issues,
        )

    def test_projected_family_missing_target_fails_deterministically(self) -> None:
        # A `projects_from` pin naming an id absent from the package's
        # selected families must fail the same deterministic way, never raise
        # KeyError/TypeError.
        broken_family = copy.deepcopy(self.sf_scalar)
        broken_family["projects_from"]["id"] = "declarativevalidation.nonexistent-whole-family"
        families_by_id = dict(self.families_by_id)
        families_by_id[broken_family["id"]] = broken_family
        citizens = [
            self.sf, self.sfb, broken_family, self.ra, self.ar, self.pp,
            self.unrelated, self.ft, self.scalar_rule, self.scalar_attachment,
        ]

        compiled = compile_validation_graph(citizens, families_by_id, self.families_by_subtotal, self.schemas)
        issues = check_validation_graph(compiled, families_by_id, self.families_by_subtotal, self.pkg["id"])
        self.assertTrue(
            any(
                iss.code == "VALIDATION_PRODUCER_MISSING" and iss.member_id == self.scalar_rule["id"]
                for iss in issues
            ),
            issues,
        )

    def test_self_projection_cycle_fails_closed(self) -> None:
        # A family whose `projects_from` pin names itself (matching id and
        # version) is a self-cycle. Bounded traversal must terminate and fail
        # closed through VALIDATION_PRODUCER_MISSING for the reaching
        # consumer - not resolve to a silent empty closure - even though the
        # family is not itself constrained.
        family_self = {
            "id": "declarativevalidation.demo-cycle-self", "version": "v1",
            "projects_from": {"id": "declarativevalidation.demo-cycle-self", "version": "v1"},
        }
        families_by_id = dict(self.families_by_id)
        families_by_id[family_self["id"]] = family_self
        families_by_subtotal = dict(self.families_by_subtotal)
        families_by_subtotal["demo.subtotal-cycle-self"] = family_self["id"]

        cycle_consumer = copy.deepcopy(self.ra)
        cycle_consumer["id"] = "declarativevalidation.demo-cycle-self-consumer"
        cycle_consumer["requires"] = ["demo.subtotal-cycle-self"]
        cycle_consumer["accounts_for"] = [{
            "family": {"id": family_self["id"], "version": "v1"},
            "relationship": "reads_subtotal",
        }]

        citizens = self.citizens + [cycle_consumer]
        compiled = compile_validation_graph(citizens, families_by_id, families_by_subtotal, self.schemas)
        issues = check_validation_graph(compiled, families_by_id, families_by_subtotal, self.pkg["id"])

        by_id = {m["id"]: m for m in compiled}
        self.assertIn(f"{family_self['id']}.member-validation", by_id[cycle_consumer["id"]].get("requires", []))

        consumer_issues = [iss for iss in issues if iss.member_id == cycle_consumer["id"]]
        self.assertEqual(len(consumer_issues), 1, consumer_issues)
        self.assertEqual(consumer_issues[0].code, "VALIDATION_PRODUCER_MISSING")
        self.assertIn(f"{family_self['id']}.member-validation", consumer_issues[0].detail)

    def test_two_family_projection_cycle_fails_closed(self) -> None:
        # A mutual two-family projection cycle - neither member independently
        # constrained - must also fail closed for the reaching consumer,
        # never resolve to a silent empty closure (Repair 5 review Finding 1).
        # No hang or recursion error either way.
        family_x = {"id": "declarativevalidation.demo-cycle-x", "version": "v1",
                    "projects_from": {"id": "declarativevalidation.demo-cycle-y", "version": "v1"}}
        family_y = {"id": "declarativevalidation.demo-cycle-y", "version": "v1",
                    "projects_from": {"id": "declarativevalidation.demo-cycle-x", "version": "v1"}}
        families_by_id = dict(self.families_by_id)
        families_by_id[family_x["id"]] = family_x
        families_by_id[family_y["id"]] = family_y
        families_by_subtotal = dict(self.families_by_subtotal)
        families_by_subtotal["demo.subtotal-cycle"] = family_x["id"]

        cycle_consumer = copy.deepcopy(self.ra)
        cycle_consumer["id"] = "declarativevalidation.demo-cycle-consumer"
        cycle_consumer["requires"] = ["demo.subtotal-cycle"]
        cycle_consumer["accounts_for"] = [{
            "family": {"id": family_x["id"], "version": "v1"},
            "relationship": "reads_subtotal",
        }]

        citizens = self.citizens + [cycle_consumer]
        compiled = compile_validation_graph(citizens, families_by_id, families_by_subtotal, self.schemas)
        issues = check_validation_graph(compiled, families_by_id, families_by_subtotal, self.pkg["id"])

        by_id = {m["id"]: m for m in compiled}
        requires = by_id[cycle_consumer["id"]].get("requires", [])
        self.assertIn(f"{family_x['id']}.member-validation", requires)
        self.assertNotIn(f"{family_y['id']}.member-validation", requires)

        consumer_issues = [iss for iss in issues if iss.member_id == cycle_consumer["id"]]
        self.assertEqual(len(consumer_issues), 1, consumer_issues)
        self.assertEqual(consumer_issues[0].code, "VALIDATION_PRODUCER_MISSING")
        self.assertIn(f"{family_x['id']}.member-validation", consumer_issues[0].detail)

    def test_multi_entry_projection_cycle_fails_closed_for_both_origins(self) -> None:
        # Repair 6 review Finding 1: two distinct, directly-reached families
        # (P, Q) that both `projects_from` the same self-cycling family (S)
        # must both remain required and both fail closed through
        # VALIDATION_PRODUCER_MISSING - never just whichever one happens to
        # process first under the process's ambient PYTHONHASHSEED, and never
        # a spurious FAMILY_ACCOUNTING_UNREACHED for the side a hash-seed-
        # dependent implementation would otherwise silently drop.
        family_s = {
            "id": "declarativevalidation.demo-cycle-multi-s", "version": "v1",
            "projects_from": {"id": "declarativevalidation.demo-cycle-multi-s", "version": "v1"},
        }
        family_p = {
            "id": "declarativevalidation.demo-cycle-multi-p", "version": "v1",
            "projects_from": {"id": "declarativevalidation.demo-cycle-multi-s", "version": "v1"},
        }
        family_q = {
            "id": "declarativevalidation.demo-cycle-multi-q", "version": "v1",
            "projects_from": {"id": "declarativevalidation.demo-cycle-multi-s", "version": "v1"},
        }
        families_by_id = dict(self.families_by_id)
        families_by_id[family_s["id"]] = family_s
        families_by_id[family_p["id"]] = family_p
        families_by_id[family_q["id"]] = family_q
        families_by_subtotal = dict(self.families_by_subtotal)
        families_by_subtotal["demo.subtotal-cycle-multi-p"] = family_p["id"]
        families_by_subtotal["demo.subtotal-cycle-multi-q"] = family_q["id"]

        cycle_consumer = copy.deepcopy(self.ra)
        cycle_consumer["id"] = "declarativevalidation.demo-cycle-multi-consumer"
        cycle_consumer["requires"] = ["demo.subtotal-cycle-multi-p", "demo.subtotal-cycle-multi-q"]
        cycle_consumer["accounts_for"] = [
            {"family": {"id": family_p["id"], "version": "v1"}, "relationship": "reads_subtotal"},
            {"family": {"id": family_q["id"], "version": "v1"}, "relationship": "reads_subtotal"},
        ]

        citizens = self.citizens + [cycle_consumer]
        compiled = compile_validation_graph(citizens, families_by_id, families_by_subtotal, self.schemas)
        issues = check_validation_graph(compiled, families_by_id, families_by_subtotal, self.pkg["id"])

        by_id = {m["id"]: m for m in compiled}
        requires = by_id[cycle_consumer["id"]].get("requires", [])
        self.assertIn(f"{family_p['id']}.member-validation", requires)
        self.assertIn(f"{family_q['id']}.member-validation", requires)

        consumer_issues = [iss for iss in issues if iss.member_id == cycle_consumer["id"]]
        self.assertEqual(len(consumer_issues), 2, consumer_issues)
        self.assertTrue(
            all(iss.code == "VALIDATION_PRODUCER_MISSING" for iss in consumer_issues), consumer_issues
        )
        details = " ".join(iss.detail for iss in consumer_issues)
        self.assertIn(f"{family_p['id']}.member-validation", details)
        self.assertIn(f"{family_q['id']}.member-validation", details)
        self.assertFalse(any(iss.code == "FAMILY_ACCOUNTING_UNREACHED" for iss in consumer_issues))

    def test_two_entry_points_converging_on_one_valid_family_yield_one_required_triple(self) -> None:
        # Noncyclic convergence control paired with the regression above: two
        # distinct, directly-reached scalar families that both
        # `projects_from` the same real *constrained* family (never a cycle)
        # must still collapse to that exact whole-family required triple -
        # one producer, one edge, no false cycle failure.
        family_d = {
            "id": "declarativevalidation.demo-converge-d", "version": "v1",
            "projects_from": {"id": FAMILY_A_ID, "version": "v1"},
        }
        family_e = {
            "id": "declarativevalidation.demo-converge-e", "version": "v1",
            "projects_from": {"id": FAMILY_A_ID, "version": "v1"},
        }
        families_by_id = dict(self.families_by_id)
        families_by_id[family_d["id"]] = family_d
        families_by_id[family_e["id"]] = family_e
        families_by_subtotal = dict(self.families_by_subtotal)
        families_by_subtotal["demo.subtotal-converge-d"] = family_d["id"]
        families_by_subtotal["demo.subtotal-converge-e"] = family_e["id"]

        converge_consumer = copy.deepcopy(self.ra)
        converge_consumer["id"] = "declarativevalidation.demo-converge-consumer"
        converge_consumer["requires"] = ["demo.subtotal-converge-d", "demo.subtotal-converge-e"]
        converge_consumer["accounts_for"] = [
            {"family": {"id": FAMILY_A_ID, "version": "v1"}, "relationship": "reads_subtotal"},
        ]

        citizens = self.citizens + [converge_consumer]
        compiled = compile_validation_graph(citizens, families_by_id, families_by_subtotal, self.schemas)
        issues = check_validation_graph(compiled, families_by_id, families_by_subtotal, self.pkg["id"])

        by_id = {m["id"]: m for m in compiled}
        requires = by_id[converge_consumer["id"]].get("requires", [])
        self.assertEqual(requires.count(FAMILY_A_SYMBOL), 1)
        self.assertNotIn(f"{family_d['id']}.member-validation", requires)
        self.assertNotIn(f"{family_e['id']}.member-validation", requires)

        consumer_issues = [iss for iss in issues if iss.member_id == converge_consumer["id"]]
        self.assertEqual(consumer_issues, [], consumer_issues)

    def test_exclusivity_counterpart_absent(self) -> None:
        pkg = copy.deepcopy(self.pkg)
        pkg["members"] = [m for m in pkg["members"] if m["id"] != FAMILY_B_ID]
        pkg["entrypoints"] = [e for e in pkg["entrypoints"] if e["id"] != FAMILY_B_ID]
        citizens = [c for c in self.citizens if c["id"] != FAMILY_B_ID]

        res = self._validate(pkg, citizens)
        self.assertFalse(res.ok)
        self.assertTrue(any(iss.code == "EXCLUSIVITY_COUNTERPART_ABSENT" for iss in res.issues), res.issues)


if __name__ == "__main__":
    unittest.main()
