"""Track 1 production evidence for the coherent v38 nominee return graph.

The fixtures in this module stay synthetic and drive the published package,
the real coordinator, Schedule B attachment, and durable presentation model.
They deliberately assert the bounded ``taxable-total`` path only; this is not
complete 2025 interest or filing support.
"""

from __future__ import annotations

import copy
import hashlib
import json
import unittest
from decimal import Decimal
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any, Mapping, Sequence, cast

from packages.derivation.live import live_coordinate_run
from packages.derivation.live_workspace import WorkspaceCapability
from packages.derivation.loader import DerivationSchemas
from packages.derivation.package_validation import (
    load_published_citizen_checksums,
    package_instance_checksum,
    validate_package,
)
from packages.derivation.production_resolver import PublicationSurface
from packages.tax.nominee_consequences import (
    BOTH_PRESENT_MISSING,
    DERIVED_NOMINEE_SYMBOL,
    DEPENDENCY_ABSENT,
    DEPENDENCY_INVALID,
    NOMINEE_ALLOCATIONS_EXCEED_REPORT,
    PUBLISHES as NOMINEE_PUBLISHES,
    RULE_ID as NOMINEE_RULE_ID,
)
from packages.tax.report_statement_identity import (
    derive_1099int_box1_fact_id,
    derive_reported_payer_entity_id,
    derive_reported_statement_entity_id,
)
from tests.support import demo_evidence
from tests.test_form1099g_box1_schedule1_line7 import _act, _attested
from tests.test_nominee_consequences_live import (
    CONTENT,
    FIXTURES,
    _alloc,
    _c1_workspace,
    _load,
    _report,
    _workspace_acts,
)
from tests.test_package_membership_wiring import ROOT, SCOPE, USER
from tests.test_ssa1099_benefits_line6_track2 import SCOPE_KEY
from tests.test_t8_statement_selection_live import _t8_acts


REGISTRY_FILE = "published-packages.v33.json"
RELEASE_FILE = "demo.release.2025.v31.json"
ADOPTION_FILE = "adopt-core-v38-current.json"
PACKAGE_FILE = "package.core-calculations.v38.json"

BOX1_FAMILY = "tax.us.2025.f1099int.b1"
BOX1_CLOSURE_TYPE = "tax.us.2025.f1099int.b1.source-closure"
LEGACY_NOMINEE_FAMILY = "tax.us.2025.scheduleb.adjustment.nominee"
LEGACY_NOMINEE_AMOUNT = "tax.us.2025.scheduleb.adjustment.nominee.amount"
LEGACY_NOMINEE_CLOSURE = "tax.us.2025.scheduleb.adjustment.nominee.source-closure"
LEGACY_NOMINEE_SUBTOTAL = "tax.us.2025.interest.scheduleb-nominee-subtotal"
LINE2B_SYMBOL = "tax.us.2025.interest.taxable-total"
DERIVED_SUBTOTAL = "tax.us.2025.interest.derived-nominee-subtotal"
ACCRUED_SUBTOTAL = "tax.us.2025.interest.current-year-adjustment-subtotal"
SCHEDULE_B_SYMBOL = "tax.us.2025.scheduleb.disposition"
SCHEDULE_B_RULE_ID = "tax.us.2025.rule.attachment.schedule-b"


def _load_v38_adoption() -> dict[str, Any]:
    return cast(
        dict[str, Any],
        json.loads((FIXTURES / "adoptions" / ADOPTION_FILE).read_text("utf-8")),
    )


def _v38_acts(acts: Sequence[Mapping[str, Any]], *, prefix: str = "demo.track1.act") -> list[dict[str, object]]:
    """Replace a helper fixture's package adoption with the coherent v38 one."""
    finalized = [copy.deepcopy(dict(act)) for act in acts]
    adoption = _load_v38_adoption()
    if finalized and finalized[-1].get("kind") == "package-adoption":
        finalized[-1] = adoption
    else:
        finalized.append(adoption)
    for index, act in enumerate(finalized):
        act["committed_against"] = index
        act["act_id"] = f"{prefix}.{index:03d}"
        act["actor"] = USER
    return finalized


def _surface_v38() -> PublicationSurface:
    return PublicationSurface(
        FIXTURES / "publication_surface" / "releases",
        CONTENT / REGISTRY_FILE,
        CONTENT,
    )


def _run(acts: Sequence[Mapping[str, Any]], run_id: str) -> tuple[Any, dict[str, Any], dict[str, Any]]:
    with TemporaryDirectory() as tmp:
        result = live_coordinate_run(
            WorkspaceCapability(Path(tmp) / "L"),
            repo_root=ROOT,
            authoritative_acts=[dict(act) for act in acts],
            workspace_revision=len(acts),
            run_scope=SCOPE,
            scope_user=USER,
            request={"schema": "run-request.v1"},
            run_id=run_id,
            governance_pins=[],
            surface=_surface_v38(),
            output_name="out.json",
        )
        if result.refusal is not None:
            return result, {}, {}
        report = json.loads(cast(Path, result.output_path).read_text("utf-8"))
        presentation = json.loads(cast(Path, result.presentation_path).read_text("utf-8"))
        return result, report, presentation


def _publication(result: Any, symbol: str) -> dict[str, Any] | None:
    for publication in result.publications or ():
        if publication.finding.get("symbol") == symbol:
            return cast(dict[str, Any], publication.finding)
    return None


def _publications_with_prefix(result: Any, prefix: str) -> list[dict[str, Any]]:
    return [
        cast(dict[str, Any], publication.finding)
        for publication in result.publications or ()
        if str(publication.finding.get("symbol", "")).startswith(prefix)
    ]


def _disposition(report: Mapping[str, Any], artifact_id: str, *, symbol: str | None = None) -> dict[str, Any]:
    for row in report.get("dispositions", []):
        if row.get("artifact_id") != artifact_id:
            continue
        if symbol is not None and row.get("symbol") != symbol:
            continue
        return cast(dict[str, Any], row)
    raise AssertionError(f"missing disposition for {artifact_id!r} ({symbol!r})")


def _nominee_dispositions(report: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        cast(dict[str, Any], row)
        for row in report.get("dispositions", [])
        if row.get("artifact_id") == NOMINEE_RULE_ID
    ]


def _replace_report_amount(acts: Sequence[Mapping[str, Any]], amount: float) -> list[dict[str, object]]:
    """Change the synthetic T8 report while retaining its pairing facts."""
    result = [copy.deepcopy(dict(act)) for act in acts]

    def visit(node: Any) -> None:
        if isinstance(node, dict):
            if str(node.get("fact_id", "")).startswith("tax.us.2025.f1099int.box1-interest|"):
                node["value"] = amount
            for child in node.values():
                visit(child)
        elif isinstance(node, list):
            for child in node:
                visit(child)

    for act in result:
        visit(act)
    return result


def _append_nominee_group(
    acts: Sequence[Mapping[str, Any]],
    *,
    report_value: float = 1200.0,
    allocation_value: float = 450.0,
    report_finding: str = "demo.track1.i6.box1",
    allocation_finding: str = "demo.track1.i6.alloc",
    payer: str = "demo.payer.track1.i6",
    stmt: str = "demo.stmt.track1.i6",
    recipient: str = "demo.recipient.track1.i6",
    predecessor: str = "demo.t8-live.int-b1.h1",
    horizon: str = "demo.track1.i6.int-b1.h2",
) -> list[dict[str, object]]:
    """Append one current report/allocation group to an existing return."""
    result = [copy.deepcopy(dict(act)) for act in acts]

    def add(kind: str, payload: dict[str, object]) -> None:
        result.append(_act(len(result), kind, payload))

    add("bundle-adoption", {"bundle": _load("nominee-allocation.bundle.json")})
    payer_id = derive_reported_payer_entity_id(payer)
    statement_id = derive_reported_statement_entity_id(
        payer_name=payer, statement_reference=stmt
    )
    add(
        "entity-introduced",
        {
            "entity": {
                "schema": "entity.v1",
                "id": payer_id,
                "kind": "tax.us.interest-payer",
                "label": "Synthetic Track 1 interest payer",
            }
        },
    )
    add(
        "entity-introduced",
        {
            "entity": {
                "schema": "entity.v1",
                "id": statement_id,
                "kind": "tax.us.1099int-statement",
                "label": "Synthetic Track 1 Form 1099-INT",
            }
        },
    )
    add(
        "entity-introduced",
        {
            "entity": {
                "schema": "entity.v1",
                "id": recipient,
                "kind": "tax.us.interest-allocation-recipient",
                "label": "Synthetic Track 1 allocation recipient",
            }
        },
    )
    report_fact_id = derive_1099int_box1_fact_id(
        payer_name=payer, statement_reference=stmt, tax_year=2025
    )
    add(
        "member-transition",
        {
            "family": {"id": BOX1_FAMILY, "version": "v1"},
            "scope": SCOPE_KEY,
            "member": {
                "action": "assert",
                "finding": _attested(report_finding, report_fact_id, report_value),
            },
            "successor": {"id": horizon, "predecessor": predecessor},
        },
    )
    add(
        "assertion",
        {
            "finding": _attested(
                f"{report_finding}.closure",
                f"{BOX1_CLOSURE_TYPE}|family-horizon={horizon},tax-year=2025",
                True,
            )
        },
    )
    evidence_id = f"{allocation_finding}.evidence"
    add(
        "evidence-submitted",
        {
            "evidence": demo_evidence(
                evidence_id,
                "Synthetic Track 1 nominee allocation interview",
                {"mode": "ordinary-language-entry", "synthetic": True},
            )
        },
    )
    add(
        "assertion",
        {
            "finding": {
                "schema": "finding.v2",
                "id": allocation_finding,
                "fact_id": (
                    "tax.us.nominee-allocation.amount|"
                    f"payer={payer_id},statement={statement_id},tax-year=2025,"
                    f"recipient={recipient}"
                ),
                "value": allocation_value,
                "basis": "attested",
                "evidence_ids": [evidence_id],
            }
        },
    )
    return result


def _append_legacy_nominee(
    acts: Sequence[Mapping[str, Any]], *, amount: float = 100.0
) -> list[dict[str, object]]:
    """Advance the existing empty legacy nominee horizon with one amount."""
    result = [copy.deepcopy(dict(act)) for act in acts]
    if result and result[-1].get("kind") == "package-adoption":
        result.pop()

    def add(kind: str, payload: dict[str, object]) -> None:
        result.append(_act(len(result), kind, payload))

    instance = "demo.track1.legacy.nominee.1"
    horizon = "demo.track1.legacy.nominee.h1"
    add(
        "entity-introduced",
        {
            "entity": {
                "schema": "entity.v1",
                "id": instance,
                "kind": "tax.us.scheduleb-adjustment-instance",
                "label": "Synthetic Track 1 legacy nominee adjustment instance",
            }
        },
    )
    add(
        "member-transition",
        {
            "family": {"id": LEGACY_NOMINEE_FAMILY, "version": "v1"},
            "scope": SCOPE_KEY,
            "member": {
                "action": "assert",
                "finding": _attested(
                    "demo.track1.legacy.nominee.finding",
                    f"{LEGACY_NOMINEE_AMOUNT}|tax-year=2025,adjustment-instance={instance}",
                    amount,
                ),
            },
            "successor": {"id": horizon, "predecessor": "demo.ug.sb-nom.h0"},
        },
    )
    add(
        "assertion",
        {
            "finding": _attested(
                "demo.track1.legacy.nominee.closure",
                f"{LEGACY_NOMINEE_CLOSURE}|family-horizon={horizon},tax-year=2025",
                True,
            )
        },
    )
    return result


def _add_part3_absence(acts: Sequence[Mapping[str, Any]]) -> list[dict[str, object]]:
    absent = {"demo.ug.scheduleb.foreign-account", "demo.ug.scheduleb.foreign-trust"}
    return [
        copy.deepcopy(dict(act))
        for act in acts
        if not (
            act.get("kind") == "assertion"
            and isinstance(act.get("payload"), dict)
            and isinstance(act["payload"].get("finding"), dict)
            and act["payload"]["finding"].get("id") in absent
        )
    ]


def _v38_content_corpus() -> dict[tuple[str, str], dict[str, Any]]:
    """Load the synthetic production corpus keyed by exact citizen identity."""
    corpus: dict[tuple[str, str], dict[str, Any]] = {}
    for path in CONTENT.glob("*.json"):
        citizen = json.loads(path.read_text("utf-8"))
        if not (
            isinstance(citizen, dict)
            and isinstance(citizen.get("id"), str)
            and isinstance(citizen.get("version"), str)
            and not ("citizens" in citizen and "packages" in citizen)
        ):
            continue
        corpus[(citizen["id"], citizen["version"])] = citizen
    return corpus


def _validate_v38_package(
    package: Mapping[str, Any],
    *,
    corpus: dict[tuple[str, str], dict[str, Any]] | None = None,
    check_publication_registry: bool = True,
) -> Any:
    package_copy = copy.deepcopy(dict(package))
    corpus = corpus or _v38_content_corpus()
    members = {
        (member["id"], member["version"]): corpus[(member["id"], member["version"])]
        for member in package_copy["members"]
    }
    return validate_package(
        package_copy,
        members,
        DerivationSchemas(),
        (
            load_published_citizen_checksums(CONTENT / REGISTRY_FILE)
            if check_publication_registry
            else None
        ),
    )


class CoherentReturnPackage(unittest.TestCase):
    def test_v38_package_registry_release_and_graph_are_coherent(self) -> None:
        package = json.loads((CONTENT / PACKAGE_FILE).read_text("utf-8"))
        registry = json.loads((CONTENT / REGISTRY_FILE).read_text("utf-8"))
        release_path = FIXTURES / "publication_surface" / "releases" / RELEASE_FILE
        release = json.loads(release_path.read_text("utf-8"))
        self.assertEqual(package["schema"], "artifact-package.v30")
        self.assertEqual(package["version"], "v38")
        self.assertEqual(package_instance_checksum(package), package["package_checksum"])
        self.assertEqual(
            release["package_registry_sha256"], hashlib.sha256((CONTENT / REGISTRY_FILE).read_bytes()).hexdigest()
        )
        entry = next(
            item
            for item in registry["packages"]
            if item["id"] == package["id"] and item["version"] == "v38"
        )
        self.assertEqual(entry["checksum"], package["package_checksum"])
        corpus = _v38_content_corpus()
        members = {(member["id"], member["version"]): corpus[(member["id"], member["version"])] for member in package["members"]}
        result = validate_package(
            package,
            members,
            DerivationSchemas(),
            load_published_citizen_checksums(CONTENT / REGISTRY_FILE),
        )
        self.assertTrue(result.ok, result.issues)

    def test_successor_graph_rejects_split_attachment_and_line2b_pins(self) -> None:
        package = json.loads((CONTENT / PACKAGE_FILE).read_text("utf-8"))
        corpus = _v38_content_corpus()
        members = {(member["id"], member["version"]): corpus[(member["id"], member["version"])] for member in package["members"]}
        package["members"] = [
            {**member, "version": "v6"}
            if member["id"] == "tax.us.2025.rule.attachment.schedule-b"
            else member
            for member in package["members"]
        ]
        result = validate_package(
            package,
            members,
            DerivationSchemas(),
            load_published_citizen_checksums(CONTENT / REGISTRY_FILE),
        )
        self.assertIn("NOMINEE_RETURN_SUCCESSOR_GRAPH_MIXED", {issue.code for issue in result.issues})

    def test_v38_rejects_omitted_or_misowned_aggregate_producer(self) -> None:
        package = json.loads((CONTENT / PACKAGE_FILE).read_text("utf-8"))
        aggregate_id = "tax.us.2025.rule.interest.derived-nominee-subtotal"

        omitted = copy.deepcopy(package)
        omitted["members"] = [
            member for member in omitted["members"] if member["id"] != aggregate_id
        ]
        omitted["package_checksum"] = package_instance_checksum(omitted)
        omitted_result = _validate_v38_package(omitted)
        self.assertIn(
            "NOMINEE_AGGREGATE_PRODUCER_MISSING",
            {issue.code for issue in omitted_result.issues},
        )

        misowned = copy.deepcopy(package)
        wrong_id = "demo.rule.misowned-nominee-aggregate"
        misowned["members"] = [
            {**member, "id": wrong_id}
            if member["id"] == aggregate_id
            else member
            for member in misowned["members"]
        ]
        misowned["package_checksum"] = package_instance_checksum(misowned)
        corpus = _v38_content_corpus()
        wrong_aggregate = copy.deepcopy(corpus[(aggregate_id, "v1")])
        wrong_aggregate["id"] = wrong_id
        corpus[(wrong_id, "v1")] = wrong_aggregate
        misowned_result = _validate_v38_package(
            misowned, corpus=corpus, check_publication_registry=False
        )
        misowned_codes = {issue.code for issue in misowned_result.issues}
        self.assertIn("NOMINEE_AGGREGATE_PRODUCER_MISSING", misowned_codes)
        self.assertIn("NOMINEE_AGGREGATE_ID_INVALID", misowned_codes)

    def test_v38_rejects_copied_v9_selection_without_exact_identity(self) -> None:
        package = json.loads((CONTENT / PACKAGE_FILE).read_text("utf-8"))
        corpus = _v38_content_corpus()
        line2b_id = "tax.us.2025.rule.form1040-line2b"
        copied_id = "demo.rule.copied-v9-selection"
        copied = copy.deepcopy(corpus[(line2b_id, "v8")])
        copied["id"] = copied_id
        package["members"] = [
            {**member, "id": copied_id} if member["id"] == line2b_id else member
            for member in package["members"]
        ]
        package["entrypoints"] = [
            {**entrypoint, "id": copied_id}
            if entrypoint["id"] == line2b_id
            else entrypoint
            for entrypoint in package["entrypoints"]
        ]
        package["package_checksum"] = package_instance_checksum(package)
        corpus[(copied_id, "v8")] = copied
        result = _validate_v38_package(
            package, corpus=corpus, check_publication_registry=False
        )
        self.assertIn("RULE_SELECTION_UNAUTHORIZED", {issue.code for issue in result.issues})

    def test_v38_rejects_divergent_schedule_b_and_line2b_nominee_symbols(self) -> None:
        package = json.loads((CONTENT / PACKAGE_FILE).read_text("utf-8"))
        corpus = _v38_content_corpus()
        schedule_b = copy.deepcopy(
            corpus[("tax.us.2025.rule.attachment.schedule-b", "v7")]
        )
        nominee_row = schedule_b["itemizations"][0]["adjustment_rows"][0]
        nominee_row["selection"]["paths"][1]["subtotal_symbol"] = (
            "demo.wrong-derived-nominee-subtotal"
        )
        corpus[(schedule_b["id"], schedule_b["version"])] = schedule_b
        result = _validate_v38_package(package, corpus=corpus)
        self.assertIn(
            "NOMINEE_RETURN_SYMBOL_MISMATCH",
            {issue.code for issue in result.issues},
        )


class CoherentReturnIntegration(unittest.TestCase):
    def test_i0_and_i1_publish_only_current_nominee_aggregate(self) -> None:
        i0_result, i0_report, i0_presentation = _run(
            _v38_acts(
                _workspace_acts(
                    reports=[_report(payer="demo.payer.a", stmt="demo.stmt.a", finding="demo.f.box1.i0", value=1200.0)],
                    close_box1=True,
                )
            ),
            "demo.run.track1.i0",
        )
        self.assertIsNone(i0_result.refusal, i0_result.refusal)
        self.assertIsNone(_publication(i0_result, DERIVED_SUBTOTAL))
        self.assertIsNone(_publication(i0_result, NOMINEE_PUBLISHES))
        self.assertEqual(Decimal(str(cast(dict[str, Any], _publication(i0_result, LINE2B_SYMBOL))["value"])), Decimal("1200"))
        i0_schedule_b = next(
            attachment
            for attachment in i0_presentation["attachments"]
            if attachment["id"] == "tax.us.2025.rule.attachment.schedule-b"
        )
        self.assertEqual(i0_schedule_b["resolved"]["disposition"], "guard_inapplicable")
        self.assertEqual(i0_presentation.get("provenanceGroups", []), [])

        i1_result, i1_report, i1_presentation = _run(
            _v38_acts(_c1_workspace()),
            "demo.run.track1.i1",
        )
        self.assertIsNone(i1_result.refusal, i1_result.refusal)
        self.assertEqual(
            Decimal(str(cast(dict[str, Any], _publication(i1_result, DERIVED_SUBTOTAL))["value"])),
            Decimal("450"),
        )
        self.assertEqual(
            Decimal(str(cast(dict[str, Any], _publication(i1_result, LINE2B_SYMBOL))["value"])),
            Decimal("750"),
        )
        schedule_b = cast(dict[str, Any], _publication(i1_result, SCHEDULE_B_SYMBOL))
        self.assertTrue(schedule_b["value"]["required"])
        part = schedule_b["value"]["itemizations"][0]
        self.assertEqual(part["adjustment_rows"][0]["kind"], "nominee_distribution")
        self.assertEqual(part["adjustment_rows"][0]["subtotal"]["value"], "450.0")
        self.assertEqual(part["tie_out"]["line_value"], "750.0")
        self.assertEqual(len(i1_presentation["provenanceGroups"]), 1)
        group = i1_presentation["provenanceGroups"][0]
        self.assertEqual(
            {site["pinId"] for site in group["citationSites"]},
            {"demo.f.box1.a1", "demo.f.pat.1", NOMINEE_RULE_ID, "tax.us.2025.citation.interest.nominee-reduction"},
        )
        self.assertEqual(_disposition(i1_report, SCHEDULE_B_RULE_ID)["disposition"], "published")

    def test_i1_missing_part3_answers_stays_required_and_incomplete(self) -> None:
        result, report, presentation = _run(
            _v38_acts(_add_part3_absence(_c1_workspace())),
            "demo.run.track1.i1-missing-part3",
        )
        self.assertIsNone(result.refusal, result.refusal)
        self.assertEqual(Decimal(str(cast(dict[str, Any], _publication(result, LINE2B_SYMBOL))["value"])), Decimal("750"))
        self.assertIsNone(_publication(result, SCHEDULE_B_SYMBOL))
        self.assertEqual(_disposition(report, SCHEDULE_B_RULE_ID)["disposition"], "blocked")
        schedule_b = next(
            attachment
            for attachment in presentation["attachments"]
            if attachment["id"] == "tax.us.2025.rule.attachment.schedule-b"
        )
        self.assertEqual(schedule_b["resolved"]["disposition"], "blocked")

    def test_i2_and_i3_sum_form_amount_but_keep_report_local_groups(self) -> None:
        i2_acts = _workspace_acts(
            reports=[_report(payer="demo.payer.a", stmt="demo.stmt.a", finding="demo.f.box1.i2", value=1200.0)],
            allocations=[
                _alloc(payer="demo.payer.a", stmt="demo.stmt.a", recipient="demo.recipient.pat", finding="demo.f.i2.pat", value=300.0, evidence="demo.evidence.i2.pat"),
                _alloc(payer="demo.payer.a", stmt="demo.stmt.a", recipient="demo.recipient.kim", finding="demo.f.i2.kim", value=150.0, evidence="demo.evidence.i2.kim"),
            ],
            close_box1=True,
        )
        i2_result, _i2_report, i2_presentation = _run(_v38_acts(i2_acts), "demo.run.track1.i2")
        self.assertIsNone(i2_result.refusal, i2_result.refusal)
        self.assertEqual(Decimal(str(cast(dict[str, Any], _publication(i2_result, DERIVED_SUBTOTAL))["value"])), Decimal("450"))
        self.assertEqual(len(i2_presentation["provenanceGroups"]), 1)
        self.assertEqual(
            {site["pinId"] for site in i2_presentation["provenanceGroups"][0]["citationSites"]},
            {"demo.f.box1.i2", "demo.f.i2.pat", "demo.f.i2.kim", NOMINEE_RULE_ID, "tax.us.2025.citation.interest.nominee-reduction"},
        )

        i3_acts = _workspace_acts(
            reports=[
                _report(payer="demo.payer.i3.a", stmt="demo.stmt.i3.a", finding="demo.f.i3.a", value=1200.0),
                _report(payer="demo.payer.i3.b", stmt="demo.stmt.i3.b", finding="demo.f.i3.b", value=900.0),
            ],
            allocations=[
                _alloc(payer="demo.payer.i3.a", stmt="demo.stmt.i3.a", recipient="demo.recipient.i3.a", finding="demo.f.i3.alloc.a", value=450.0, evidence="demo.evidence.i3.a"),
                _alloc(payer="demo.payer.i3.b", stmt="demo.stmt.i3.b", recipient="demo.recipient.i3.b", finding="demo.f.i3.alloc.b", value=300.0, evidence="demo.evidence.i3.b"),
            ],
            close_box1=True,
        )
        i3_result, _i3_report, i3_presentation = _run(_v38_acts(i3_acts), "demo.run.track1.i3")
        self.assertIsNone(i3_result.refusal, i3_result.refusal)
        self.assertEqual(Decimal(str(cast(dict[str, Any], _publication(i3_result, DERIVED_SUBTOTAL))["value"])), Decimal("750"))
        groups = i3_presentation["provenanceGroups"]
        self.assertEqual(len(groups), 2)
        group_pins = [{site["pinId"] for site in group["citationSites"]} for group in groups]
        self.assertIn({"demo.f.i3.a", "demo.f.i3.alloc.a", NOMINEE_RULE_ID, "tax.us.2025.citation.interest.nominee-reduction"}, group_pins)
        self.assertIn({"demo.f.i3.b", "demo.f.i3.alloc.b", NOMINEE_RULE_ID, "tax.us.2025.citation.interest.nominee-reduction"}, group_pins)

    def test_i4_unrelated_group_remains_but_dependents_block(self) -> None:
        acts = _workspace_acts(
            reports=[
                _report(payer="demo.payer.i4.a", stmt="demo.stmt.i4.a", finding="demo.f.i4.a", value=1200.0),
                _report(payer="demo.payer.i4.c", stmt="demo.stmt.i4.c", finding="demo.f.i4.c", value=900.0),
            ],
            allocations=[
                _alloc(payer="demo.payer.i4.a", stmt="demo.stmt.i4.a", recipient="demo.recipient.i4.a", finding="demo.f.i4.alloc.a1", value=800.0, evidence="demo.evidence.i4.a1"),
                _alloc(payer="demo.payer.i4.a", stmt="demo.stmt.i4.a", recipient="demo.recipient.i4.a2", finding="demo.f.i4.alloc.a2", value=450.0, evidence="demo.evidence.i4.a2"),
                _alloc(payer="demo.payer.i4.c", stmt="demo.stmt.i4.c", recipient="demo.recipient.i4.c", finding="demo.f.i4.alloc.c", value=300.0, evidence="demo.evidence.i4.c"),
            ],
            close_box1=True,
        )
        result, report, presentation = _run(_v38_acts(acts), "demo.run.track1.i4")
        self.assertIsNone(result.refusal, result.refusal)
        group_rows = [
            row
            for row in _nominee_dispositions(report)
            if row.get("symbol") not in {DERIVED_SUBTOTAL}
        ]
        self.assertEqual(len(group_rows), 2)
        blocked = next(row for row in group_rows if row.get("symbol", "").endswith("demo.payer.i4.a::statement::demo.stmt.i4.a,tax-year=2025"))
        self.assertEqual(blocked["code"], NOMINEE_ALLOCATIONS_EXCEED_REPORT)
        self.assertEqual(blocked["disposition"], "blocked")
        surviving = next(row for row in group_rows if row.get("disposition") == "published")
        self.assertIn("demo.f.i4.alloc.c", json.dumps(surviving))
        self.assertIsNone(_publication(result, DERIVED_SUBTOTAL))
        line2b = _disposition(report, "tax.us.2025.rule.form1040-line2b")
        self.assertEqual(line2b["code"], DEPENDENCY_ABSENT)
        schedule_b = _disposition(report, SCHEDULE_B_RULE_ID)
        self.assertEqual(schedule_b["code"], DEPENDENCY_ABSENT)
        self.assertEqual(presentation.get("provenanceGroups", []), [])

    def test_i5_and_i6_keep_accrued_and_nominee_authority_distinct(self) -> None:
        i5_acts = _replace_report_amount(_t8_acts(), 2000.0)
        i5_result, i5_report, i5_presentation = _run(_v38_acts(i5_acts), "demo.run.track1.i5")
        self.assertIsNone(i5_result.refusal, i5_result.refusal)
        self.assertEqual(Decimal(str(cast(dict[str, Any], _publication(i5_result, ACCRUED_SUBTOTAL))["value"])), Decimal("500"))
        self.assertEqual(Decimal(str(cast(dict[str, Any], _publication(i5_result, LINE2B_SYMBOL))["value"])), Decimal("1500"))
        i5_schedule_b = cast(dict[str, Any], _publication(i5_result, SCHEDULE_B_SYMBOL))
        i5_adjustments = {
            row["kind"]: row
            for row in i5_schedule_b["value"]["itemizations"][0]["adjustment_rows"]
        }
        self.assertEqual(i5_adjustments["accrued_interest"]["subtotal"]["value"], "500.0")
        self.assertEqual(i5_schedule_b["value"]["itemizations"][0]["tie_out"]["line_value"], "1500.0")
        self.assertEqual(
            {group["adjustmentKind"] for group in i5_presentation.get("provenanceGroups", [])},
            {"accrued_interest"},
        )
        self.assertEqual(_disposition(i5_report, SCHEDULE_B_RULE_ID)["disposition"], "published")

        i6_acts = _append_nominee_group(_replace_report_amount(_t8_acts(), 2000.0))
        i6_result, _i6_report, i6_presentation = _run(_v38_acts(i6_acts), "demo.run.track1.i6")
        self.assertIsNone(i6_result.refusal, i6_result.refusal)
        self.assertEqual(Decimal(str(cast(dict[str, Any], _publication(i6_result, DERIVED_SUBTOTAL))["value"])), Decimal("450"))
        self.assertEqual(Decimal(str(cast(dict[str, Any], _publication(i6_result, ACCRUED_SUBTOTAL))["value"])), Decimal("500"))
        self.assertEqual(Decimal(str(cast(dict[str, Any], _publication(i6_result, LINE2B_SYMBOL))["value"])), Decimal("2250"))
        i6_schedule_b = cast(dict[str, Any], _publication(i6_result, SCHEDULE_B_SYMBOL))
        rows = i6_schedule_b["value"]["itemizations"][0]["adjustment_rows"]
        self.assertEqual([(row["kind"], row["subtotal"]["value"]) for row in rows], [("nominee_distribution", "450.0"), ("accrued_interest", "500.0"), ("abp_adjustment", "0")])
        self.assertEqual(i6_schedule_b["value"]["itemizations"][0]["tie_out"]["line_value"], "2250.0")
        self.assertEqual({group["adjustmentKind"] for group in i6_presentation["provenanceGroups"]}, {"nominee_distribution", "accrued_interest"})

    def test_i7_legacy_only_uses_legacy_path_and_i8_refuses_both(self) -> None:
        i7_acts = _append_legacy_nominee(
            _workspace_acts(
                reports=[_report(payer="demo.payer.i7", stmt="demo.stmt.i7", finding="demo.f.i7.report", value=600.0)],
                close_box1=True,
            )
        )
        i7_result, _i7_report, _i7_presentation = _run(_v38_acts(i7_acts), "demo.run.track1.i7")
        self.assertIsNone(i7_result.refusal, i7_result.refusal)
        self.assertEqual(Decimal(str(cast(dict[str, Any], _publication(i7_result, LEGACY_NOMINEE_SUBTOTAL))["value"])), Decimal("100"))
        self.assertIsNone(_publication(i7_result, DERIVED_SUBTOTAL))
        self.assertEqual(Decimal(str(cast(dict[str, Any], _publication(i7_result, LINE2B_SYMBOL))["value"])), Decimal("500"))

        i8_acts = _append_legacy_nominee(_c1_workspace())
        i8_result, i8_report, i8_presentation = _run(_v38_acts(i8_acts), "demo.run.track1.i8")
        self.assertIsNone(i8_result.refusal, i8_result.refusal)
        line2b = _disposition(i8_report, "tax.us.2025.rule.form1040-line2b")
        self.assertEqual(line2b["disposition"], "blocked")
        self.assertEqual(line2b["code"], DEPENDENCY_INVALID)
        self.assertEqual(line2b["missing"], [BOTH_PRESENT_MISSING])
        schedule_b = _disposition(i8_report, SCHEDULE_B_RULE_ID)
        self.assertEqual(schedule_b["disposition"], "blocked")
        self.assertEqual(schedule_b["code"], DEPENDENCY_INVALID)
        self.assertEqual(schedule_b["missing"], [BOTH_PRESENT_MISSING])
        self.assertEqual(i8_presentation.get("provenanceGroups", []), [])
        self.assertIsNone(_publication(i8_result, LINE2B_SYMBOL))


if __name__ == "__main__":
    unittest.main()
