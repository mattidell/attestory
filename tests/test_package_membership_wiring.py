"""Package-membership wiring: seam citizens join core-calculations v34.

Additive successor over published v33. ``live_coordinate_run`` of the
current published package (v34 / published-packages v29 / release v27)
must dispatch Seam 2 association, Seam 3 per-pairing and aggregate
accrued-interest supportability, Seam 5's two consequence rules, the
pairing-scoped current-year-adjustment subtotal, and the line-2b v5
aggregator -- not only the isolated ``_execute`` path Integration already
proved. The obligation-acquisition vocabulary member is the real,
arbitrary-cardinality entity-identity bundle
(``obligation-acquisition.bundle.json``, v1), and a single same-payer/year
report is never silently associated without a statement reference or
explicit, specifically-targeted confirmation.
"""

from __future__ import annotations

import hashlib
import json
import unittest
from decimal import Decimal
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any, cast

from packages.derivation.live import live_coordinate_run
from packages.derivation.live_workspace import WorkspaceCapability
from packages.derivation.loader import DerivationSchemas
from packages.derivation.package_validation import (
    load_published_citizen_checksums,
    package_instance_checksum,
    validate_package,
)
from packages.derivation.production_resolver import PublicationSurface
from packages.kernel.findings import project
from packages.tax.identity_association import ASSOCIATION_SYMBOL
from packages.tax.loader import TAX_CONTENT_DIR
from packages.tax.obligation_acquisition_mapping import (
    contribute_ordinary_acquisition,
)
from packages.tax.pairing_consequences import (
    BASIS_SYMBOL_PREFIX,
    CURRENT_YEAR_SUBTOTAL_SYMBOL,
    CURRENT_YEAR_SYMBOL_PREFIX,
)
from packages.tax.supportability import SUPPORTABILITY_SYMBOL
from tests.support import demo_evidence
from tests.test_f1098e_student_loan_interest_agi_track6 import _f1098e_acts
from tests.test_form1099g_box1_schedule1_line7 import _act, _attested
from tests.test_ssa1099_benefits_line6_track2 import SCOPE_KEY
from tools.generate_package_membership_wiring import (
    _NEW_MEMBER_FILES,
    build_package,
    build_registry,
    build_release,
)

ROOT = Path(__file__).resolve().parent.parent
CONTENT = TAX_CONTENT_DIR
FIXTURES = ROOT / "packages" / "sample_data" / "package_membership_wiring"
USER = "demo.user.filer-1"
SCOPE = {"jurisdiction": "us", "year": "2025"}

PACKAGE_FILE = "package.core-calculations.v34.json"
REGISTRY_FILE = "published-packages.v29.json"
RELEASE_FILE = "demo.release.2025.v27.json"
ADOPTION_FILE = "adopt-core-v34-current.json"

SEAM_RULE_IDS = (
    "tax.us.2025.rule.relationship.accrued-supported",
    "tax.us.2025.rule.interest.current-year-adjustment.pairing-scoped",
    "tax.us.2025.rule.basis.item-level-consequence.pairing-scoped",
    "tax.us.2025.rule.interest.current-year-adjustment-subtotal",
    "tax.us.2025.rule.interest.current-year-adjustment.aggregate-supportability",
    "tax.us.2025.rule.form1040-line2b",
)


def _load(name: str) -> dict[str, Any]:
    return cast(dict[str, Any], json.loads((CONTENT / name).read_text("utf-8")))


def _content_corpus() -> dict[tuple[str, str], dict[str, Any]]:
    corpus: dict[tuple[str, str], dict[str, Any]] = {}
    for path in CONTENT.glob("*.json"):
        try:
            value = json.loads(path.read_text("utf-8"))
        except Exception:
            continue
        if isinstance(value, dict) and isinstance(value.get("id"), str) and isinstance(
            value.get("version"), str
        ):
            corpus[(value["id"], value["version"])] = value
    return corpus


def _surface() -> PublicationSurface:
    return PublicationSurface(
        FIXTURES / "publication_surface" / "releases",
        CONTENT / REGISTRY_FILE,
        CONTENT,
    )


def _load_adoption() -> dict[str, Any]:
    return cast(
        dict[str, Any],
        json.loads((FIXTURES / "adoptions" / ADOPTION_FILE).read_text("utf-8")),
    )


def _t2_answers() -> dict[str, Any]:
    return {
        "payer_name": "demo.payer.bank-a",
        "obligation_description": "synthetic municipal bond series demo-2025",
        "obligation_reference": "DEMO-BOND-T2",
        "acquisition_date": "2025-03-14",
        "accrued_interest_paid_to_seller": 42.0,
        "currency": "USD",
        # The single same-payer/year candidate case, which requires an
        # explicit, specifically-targeted confirmation rather than being
        # silently associated.
        "confirmed_report_match": True,
    }


T2_REPORT_FACT_ID = (
    "tax.us.2025.f1099int.box1-interest|"
    "payer=demo.payer.bank-a,statement=demo.1099int-statement.t2,tax-year=2025"
)


def _t2_acts() -> list[dict[str, object]]:
    """Complete production-shaped return plus T2 box-1 and ordinary acquisition.

    T2's acquisition confirms on the coarse tier (no statement reference),
    so it names the report it confirms (``T2_REPORT_FACT_ID``). Shared by
    ``test_legacy_pairing_coexistence_migration.py`` and
    ``test_t9_unsupported_neighbor_live.py`` too -- the vocabulary a
    workspace adopts and the rule package it separately adopts are
    independent axes."""
    acts = _f1098e_acts(statements=[], close=True, wages=90000)
    acts.pop()  # drop the v33 Track-6 adoption

    def add(kind: str, payload: dict[str, object]) -> None:
        acts.append(_act(len(acts), kind, payload))

    add("bundle-adoption", {"bundle": _load("obligation-acquisition.bundle.json")})
    add(
        "entity-introduced",
        {
            "entity": {
                "schema": "entity.v1",
                "id": "demo.payer.bank-a",
                "kind": "tax.us.interest-payer",
                "label": "Synthetic interest payer bank-a",
            }
        },
    )
    add(
        "entity-introduced",
        {
            "entity": {
                "schema": "entity.v1",
                "id": "demo.1099int-statement.t2",
                "kind": "tax.us.1099int-statement",
                "label": "Synthetic Form 1099-INT T2",
            }
        },
    )
    # The acquisition's own identity is now entity-kind (payer, obligation):
    # the payer entity above (also box 1's own payer identity component,
    # same kind and id) already exists, so only the obligation entity is
    # new here.
    from packages.tax.obligation_acquisition_mapping import derive_obligation_entity_id

    add(
        "entity-introduced",
        {
            "entity": {
                "schema": "entity.v1",
                "id": derive_obligation_entity_id(
                    payer_name=_t2_answers()["payer_name"],
                    obligation_reference=_t2_answers()["obligation_reference"],
                    obligation_description=_t2_answers()["obligation_description"],
                ),
                "kind": "tax.us.interest-obligation",
                "label": "Synthetic obligation for T2",
            }
        },
    )
    add(
        "member-transition",
        {
            "family": {"id": "tax.us.2025.f1099int.b1", "version": "v1"},
            "scope": SCOPE_KEY,
            "member": {
                "action": "assert",
                "finding": _attested(
                    "demo.finding.box1.t2",
                    "tax.us.2025.f1099int.box1-interest|"
                    "payer=demo.payer.bank-a,statement=demo.1099int-statement.t2,tax-year=2025",
                    500.0,
                ),
            },
            "successor": {
                "id": "demo.t2.int-b1.h1",
                "predecessor": "demo.cgd.t2.int-b1.h0",
            },
        },
    )
    add(
        "assertion",
        {
            "finding": _attested(
                "demo.t2.closure.int-b1",
                "tax.us.2025.f1099int.b1.source-closure|"
                "family-horizon=demo.t2.int-b1.h1,tax-year=2025",
                True,
            )
        },
    )

    evidence = demo_evidence(
        "demo.evidence.acq.t2",
        "Synthetic ordinary-language acquisition interview",
        {"mode": "ordinary-language-entry", "synthetic": True},
    )
    add("evidence-submitted", {"evidence": evidence})

    schemas = DerivationSchemas()
    for index, act in enumerate(acts):
        act["committed_against"] = index
        act["act_id"] = f"demo.pkg-mem.act.{index:03d}"
        act["actor"] = USER
    base = project(tuple(dict(act) for act in acts), schemas.registry)
    admitted = contribute_ordinary_acquisition(
        base,
        _t2_answers(),
        registry=schemas.registry,
        record_id="demo.crec.acq.t2",
        act_index=len(acts),
        contribution_id="demo.contribution.acq.t2",
        evidence_id="demo.evidence.acq.t2",
        finding_id="demo.finding.acq.t2",
        committed_against=len(acts),
        confirmed_report_fact_id=T2_REPORT_FACT_ID,
    )
    if admitted.terminal_record.get("phase") != "completed":
        raise AssertionError(f"ordinary acquisition was not admitted: {admitted.terminal_record}")
    from packages.tax.obligation_acquisition_mapping import build_ordinary_acquisition_contribution

    built = build_ordinary_acquisition_contribution(
        _t2_answers(),
        act_index=len(acts),
        contribution_id="demo.contribution.acq.t2",
        evidence_id="demo.evidence.acq.t2",
        finding_id="demo.finding.acq.t2",
        committed_against=len(acts),
        confirmed_report_fact_id=T2_REPORT_FACT_ID,
    )
    for extra in (built.contribution_act, built.assertion_act):
        extra["actor"] = USER
        acts.append(extra)

    adoption = _load_adoption()
    adoption["committed_against"] = len(acts)
    acts.append(adoption)
    for index, act in enumerate(acts):
        act["committed_against"] = index
        act["act_id"] = f"demo.pkg-mem.act.{index:03d}"
        act["actor"] = USER
    return acts


class PackagePublication(unittest.TestCase):
    def test_generator_matches_committed_bytes(self) -> None:
        package = build_package()
        registry = build_registry(package)
        committed_pkg = _load(PACKAGE_FILE)
        committed_reg = json.loads((CONTENT / REGISTRY_FILE).read_text("utf-8"))
        self.assertEqual(committed_pkg, package)
        self.assertEqual(committed_reg, registry)
        registry_bytes = (json.dumps(registry, indent=2, sort_keys=True) + "\n").encode("utf-8")
        release = build_release(registry_bytes)
        committed_release = json.loads(
            (FIXTURES / "publication_surface" / "releases" / RELEASE_FILE).read_text("utf-8")
        )
        self.assertEqual(committed_release, release)

    def test_v34_validates_as_exclusive_graph(self) -> None:
        pkg = _load(PACKAGE_FILE)
        self.assertEqual(pkg["schema"], "artifact-package.v26")
        self.assertEqual(pkg["version"], "v34")
        self.assertEqual(pkg["package_checksum"], package_instance_checksum(pkg))
        self.assertIn("rule-artifact.v7", pkg["admitted_schemas"])
        corpus = _content_corpus()
        members = {(m["id"], m["version"]): corpus[(m["id"], m["version"])] for m in pkg["members"]}
        result = validate_package(
            pkg,
            members,
            DerivationSchemas(),
            load_published_citizen_checksums(CONTENT / REGISTRY_FILE),
        )
        self.assertTrue(result.ok, result.issues)

    def test_v34_pins_seam_citizens_and_coexists_with_the_legacy_input_surface(self) -> None:
        """v34 is the coexistence generation: it wires every seam citizen and
        the coexistence line-2b v5, but does not yet retire the legacy
        Schedule B accrued-interest input surface -- that happens only at
        the migrated v35 successor (see
        ``tests.test_legacy_pairing_coexistence_migration``)."""
        pkg = _load(PACKAGE_FILE)
        members = {(m["id"], m["version"]) for m in pkg["members"]}
        self.assertNotIn(("tax.us.2025.rule.form1040-line2b", "v4"), members)
        self.assertIn(("tax.us.2025.rule.form1040-line2b", "v5"), members)
        self.assertIn(("tax.us.2025.rule.attachment.schedule-b", "v4"), members)
        self.assertNotIn(("tax.us.2025.rule.attachment.schedule-b", "v5"), members)
        self.assertIn(("tax.us.2025.rule.scheduleb-adjustment.accrued-interest-subtotal", "v1"), members)
        self.assertIn(("tax.us.2025.scheduleb.adjustment.accrued-interest.vocabulary", "v1"), members)
        self.assertIn(("tax.us.2025.scheduleb.adjustment.accrued-interest", "v1"), members)
        self.assertIn(("tax.us.2025.closure-mapping.scheduleb-adjustment.accrued-interest", "v1"), members)
        self.assertNotIn(("tax.us.2025.scheduleb-accrued-interest.succession", "v1"), members)
        self.assertNotIn(("tax.us.2025.interest.accrued-interest-migrated.vocabulary", "v1"), members)
        for name in _NEW_MEMBER_FILES:
            citizen = _load(name)
            self.assertIn((citizen["id"], citizen["version"]), members, name)
        v33 = _load("package.core-calculations.v33.json")
        v33_members = {(m["id"], m["version"]) for m in v33["members"]}
        self.assertIn(("tax.us.2025.rule.form1040-line2b", "v4"), v33_members)
        self.assertNotIn(("tax.us.2025.rule.form1040-line2b", "v5"), v33_members)
        for rule_id in SEAM_RULE_IDS:
            self.assertNotIn((rule_id, "v1"), v33_members)

    def test_v33_still_validates_unchanged(self) -> None:
        v33 = _load("package.core-calculations.v33.json")
        self.assertEqual(v33["version"], "v33")
        self.assertEqual(v33["schema"], "artifact-package.v25")
        corpus = _content_corpus()
        members = {(m["id"], m["version"]): corpus[(m["id"], m["version"])] for m in v33["members"]}
        result = validate_package(
            v33,
            members,
            DerivationSchemas(),
            load_published_citizen_checksums(CONTENT / "published-packages.v28.json"),
        )
        self.assertTrue(result.ok, result.issues)

    def test_registry_release_adoption_checksums(self) -> None:
        pkg = _load(PACKAGE_FILE)
        registry = json.loads((CONTENT / REGISTRY_FILE).read_text("utf-8"))
        entry = next(
            item
            for item in registry["packages"]
            if item["id"] == pkg["id"] and item["version"] == "v34"
        )
        self.assertEqual(entry["checksum"], pkg["package_checksum"])
        v33_entry = next(
            item
            for item in registry["packages"]
            if item["id"] == pkg["id"] and item["version"] == "v33"
        )
        self.assertEqual(
            v33_entry["checksum"],
            _load("package.core-calculations.v33.json")["package_checksum"],
        )
        release = json.loads(
            (FIXTURES / "publication_surface" / "releases" / RELEASE_FILE).read_text("utf-8")
        )
        self.assertEqual(release["id"], "demo.release.2025")
        self.assertEqual(release["version"], "v27")
        self.assertEqual(
            release["package_registry_sha256"],
            hashlib.sha256((CONTENT / REGISTRY_FILE).read_bytes()).hexdigest(),
        )
        adoption = _load_adoption()
        self.assertEqual(adoption["payload"]["revision"], 34)
        self.assertEqual(adoption["payload"]["package"]["version"], "v34")
        self.assertEqual(adoption["payload"]["package"]["checksum"], pkg["package_checksum"])
        self.assertEqual(adoption["payload"]["release"]["version"], "v27")


class LiveT2AccruedTreatment(unittest.TestCase):
    def test_published_package_dispatches_pairing_scoped_consequences(self) -> None:
        acts = _t2_acts()
        with TemporaryDirectory() as tmp:
            result = live_coordinate_run(
                WorkspaceCapability(Path(tmp) / "L"),
                repo_root=ROOT,
                authoritative_acts=acts,
                workspace_revision=len(acts),
                run_scope=SCOPE,
                scope_user=USER,
                request={"schema": "run-request.v1"},
                run_id="demo.run.package-membership.t2",
                governance_pins=[],
                surface=_surface(),
                output_name="out.json",
            )
            self.assertIsNone(result.refusal, result.refusal)
            self.assertIsNotNone(result.output_path)
            self.assertIsNotNone(result.publications)
            report = json.loads(cast(Path, result.output_path).read_text("utf-8"))
            publications = tuple(result.publications or ())
        def by_prefix(prefix: str) -> list[dict[str, Any]]:
            return [
                pub.finding
                for pub in publications
                if str(pub.finding.get("symbol", "")).startswith(prefix)
            ]
        pairings = by_prefix(ASSOCIATION_SYMBOL)
        current_year = by_prefix(CURRENT_YEAR_SYMBOL_PREFIX + "|")
        basis = by_prefix(BASIS_SYMBOL_PREFIX + "|")
        support = by_prefix(SUPPORTABILITY_SYMBOL + "|")
        self.assertEqual(len(pairings), 1, pairings)
        self.assertEqual(len(support), 1, support)
        self.assertEqual(len(current_year), 1, current_year)
        self.assertEqual(len(basis), 1, basis)
        self.assertEqual(current_year[0]["value"], "42.0")
        self.assertEqual(basis[0]["value"], "42.0")
        self.assertIs(support[0]["value"], True)

        artifact_ids = {row.get("artifact_id") for row in report.get("dispositions", [])}
        self.assertIn("tax.us.2025.rule.interest.current-year-adjustment.pairing-scoped", artifact_ids)
        self.assertIn("tax.us.2025.rule.basis.item-level-consequence.pairing-scoped", artifact_ids)
        symbols = {
            row.get("symbol")
            for row in report.get("dispositions", [])
            if row.get("disposition") == "published"
        }
        self.assertTrue(any(str(s).startswith(CURRENT_YEAR_SYMBOL_PREFIX + "|") for s in symbols), symbols)
        self.assertTrue(any(str(s).startswith(BASIS_SYMBOL_PREFIX + "|") for s in symbols), symbols)
        subtotal = [
            pub.finding
            for pub in publications
            if pub.finding.get("symbol") == CURRENT_YEAR_SUBTOTAL_SYMBOL
        ]
        self.assertEqual(len(subtotal), 1)
        self.assertEqual(subtotal[0]["value"], "42.0")
        taxable = [
            pub.finding
            for pub in publications
            if pub.finding.get("symbol") == "tax.us.2025.interest.taxable-total"
        ]
        self.assertEqual(len(taxable), 1)
        self.assertEqual(Decimal(str(taxable[0]["value"])), Decimal("458"))


if __name__ == "__main__":
    unittest.main()
