"""Track 2: Form 1099-R IRA line 4b through line 9 and the tax path."""

from __future__ import annotations

import hashlib
import json
import shutil
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any, cast

from packages.derivation.live import live_coordinate_run
from packages.derivation.live_workspace import WorkspaceCapability
from packages.derivation.package_validation import package_instance_checksum
from packages.derivation.production_resolver import (
    PublicationSurface,
    Refusal,
    ResolvedGraph,
    resolve_production_package,
)
from packages.kernel.findings import FindingModelError
from packages.tax.loader import TAX_CONTENT_DIR
from tests.test_form1099g_box1_schedule1_line7 import (
    _act,
    _attested,
    _disposition,
    _published_numeric,
    _section,
    _ug_acts,
)


ROOT = Path(__file__).resolve().parent.parent
CONTENT = TAX_CONTENT_DIR
FIXTURES = ROOT / "packages" / "sample_data" / "form1099r_ira_line4b"
USER = "demo.user.filer-1"
SCOPE = {"jurisdiction": "us", "year": "2025"}
SCOPE_KEY = {"tax-year": "2025", "subject": "demo.primary"}

IRA_BOX1 = "tax.us.2025.f1099r.ira-box1-taxable-distribution"
IRA_BOX2A = "tax.us.2025.f1099r.ira-box2a-taxable-amount"
IRA_CHECKBOX = "tax.us.2025.f1099r.ira-sep-simple-checkbox"
IRA_CODE = "tax.us.2025.f1099r.distribution-code"
IRA_BOX2B = "tax.us.2025.f1099r.box2b-not-determined"
IRA_CLOSURE = "tax.us.2025.f1099r.ira-fully-taxable.source-closure"
IRA_FAMILY = "tax.us.2025.f1099r.ira-fully-taxable"
IRA_LINE4B = "tax.us.2025.ira.distributions.line4b"


def _load(name: str) -> dict[str, Any]:
    return cast(dict[str, Any], json.loads((CONTENT / name).read_text("utf-8")))


def _ira_acts(
    amounts: list[float] | None = None,
    *,
    close: bool = True,
    qualified_dividends: bool = False,
) -> list[dict[str, object]]:
    """Extend a known production-shaped income corpus with IRA statements."""
    acts = _ug_acts(
        box1_values=[],
        close_box1=True,
        box1a=600 if qualified_dividends else None,
        box1b=150 if qualified_dividends else 0,
        wages=90000,
    )
    acts.pop()  # replace the historical v20 adoption with the Track 2 adoption

    def add(kind: str, payload: dict[str, object]) -> None:
        acts.append(_act(len(acts), kind, payload))

    add("bundle-adoption", {"bundle": _load("f1099r-ira.bundle.v2.json")})
    amounts = [1200.0] if amounts is None else amounts
    payer = "demo.ira.payer.alpha"
    add(
        "entity-introduced",
        {"entity": {"schema": "entity.v1", "id": payer, "kind": "tax.us.ira-payer", "label": "Synthetic IRA payer"}},
    )
    horizon = "demo.ira.h0"
    add(
        "horizon-genesis",
        {"family": {"id": IRA_FAMILY, "version": "v2"}, "scope": SCOPE_KEY, "horizon_id": horizon},
    )
    for index, amount in enumerate(amounts):
        statement = f"demo.ira.statement.{index}"
        add(
            "entity-introduced",
            {"entity": {"schema": "entity.v1", "id": statement, "kind": "tax.us.1099r-statement", "label": "Synthetic Form 1099-R"}},
        )
        for fact_type, value, suffix in (
            (IRA_BOX2A, amount, "box2a"),
            (IRA_CHECKBOX, True, "checkbox"),
            (IRA_CODE, "7", "code"),
            (IRA_BOX2B, False, "box2b"),
        ):
            add(
                "assertion",
                {"finding": _attested(f"demo.ira.finding.{suffix}.{index}", f"{fact_type}|payer={payer},statement={statement},tax-year=2025", value)},
            )
        next_horizon = f"demo.ira.h{index + 1}"
        add(
            "member-transition",
            {
                "family": {"id": IRA_FAMILY, "version": "v2"},
                "scope": SCOPE_KEY,
                "member": {
                    "action": "assert",
                    "finding": _attested(f"demo.ira.finding.box1.{index}", f"{IRA_BOX1}|payer={payer},statement={statement},tax-year=2025", amount),
                },
                "successor": {"id": next_horizon, "predecessor": horizon},
            },
        )
        horizon = next_horizon
    if close:
        add(
            "assertion",
            {"finding": _attested("demo.ira.closure", f"{IRA_CLOSURE}|family-horizon={horizon},tax-year=2025", True)},
        )
    adoption = _load_fixture_adoption()
    adoption["committed_against"] = len(acts)
    acts.append(adoption)
    return acts

def _load_fixture_adoption() -> dict[str, object]:
    return cast(dict[str, object], json.loads((FIXTURES / "adoptions" / "adopt-core-v26-current.json").read_text("utf-8")))


def _run(acts: list[dict[str, object]], run_id: str) -> tuple[dict[str, Any], dict[str, Any]]:
    surface = PublicationSurface(FIXTURES / "publication_surface" / "releases", CONTENT / "published-packages.v21.json", CONTENT)
    with TemporaryDirectory() as tmp:
        result = live_coordinate_run(
            WorkspaceCapability(Path(tmp) / "L"),
            repo_root=ROOT,
            authoritative_acts=acts,
            workspace_revision=len(acts),
            run_scope=SCOPE,
            scope_user=USER,
            request={"schema": "run-request.v1"},
            run_id=run_id,
            governance_pins=[],
            surface=surface,
            output_name="out.json",
        )
        if result.refusal is not None:
            raise AssertionError(result.refusal)
        assert result.output_path is not None and result.presentation_path is not None
        return json.loads(result.output_path.read_text("utf-8")), json.loads(result.presentation_path.read_text("utf-8"))


class Track2Content(unittest.TestCase):
    def _renumber(self, acts: list[dict[str, object]]) -> list[dict[str, object]]:
        for index, act in enumerate(acts):
            act["committed_against"] = index
        return acts

    def _finding_for(self, acts: list[dict[str, object]], fact_type: str) -> dict[str, Any]:
        for act in acts:
            payload = cast(dict[str, Any], act.get("payload", {}))
            finding = cast(dict[str, Any], payload.get("finding", {}))
            if str(finding.get("fact_id", "")).startswith(fact_type + "|"):
                return finding
        raise AssertionError(f"missing fixture finding for {fact_type}")

    def test_line9_v6_consumes_line4b_once_and_does_not_read_raw_members(self) -> None:
        rule = _load("rule.form1040-line9.v6.json")
        self.assertEqual(rule["version"], "v6")
        self.assertEqual([arg["name"] for arg in rule["value"]["args"]][-1], IRA_LINE4B)
        self.assertNotIn(IRA_BOX1, json.dumps(rule))
        self.assertEqual(rule["value"]["args"].count({"name": IRA_LINE4B, "op": "ref"}), 1)
        self.assertFalse((CONTENT / "form1040.line-4a.form-field.json").exists())

    def test_package_and_registry_are_additive_successors(self) -> None:
        package = _load("package.core-calculations.v26.json")
        registry = _load("published-packages.v21.json")
        self.assertEqual(package["schema"], "artifact-package.v20")
        self.assertEqual(package["version"], "v26")
        self.assertIn("quantity-vocabulary.v11", package["admitted_schemas"])
        self.assertIn({"id": "tax.us.2025.rule.form1040-line9", "version": "v6"}, package["entrypoints"])
        self.assertNotIn({"id": "tax.us.2025.rule.form1040-line9", "version": "v5"}, package["entrypoints"])
        self.assertIn(
            {"id": "tax.us.2025.f1099r.ira.vocabulary", "version": "v2"},
            package["entrypoints"],
        )
        self.assertIn(
            {"id": "tax.us.2025.rule.f1099r-ira-fully-taxable-subtotal", "version": "v3"},
            package["entrypoints"],
        )
        self.assertIn(
            {"id": "tax.us.2025.rule.f1099r-ira-fully-taxable-subtotal", "role": "computation", "schema": "rule-artifact.v3", "version": "v3"},
            package["members"],
        )
        self.assertIn({"id": package["id"], "version": "v26", "checksum": package["package_checksum"]}, registry["packages"])
        self.assertIn(
            {
                "id": "tax.us.2025.rule.f1099r-ira-fully-taxable-subtotal",
                "version": "v3",
                "checksum": next(
                    c["checksum"]
                    for c in registry["citizens"]
                    if c["id"] == "tax.us.2025.rule.f1099r-ira-fully-taxable-subtotal" and c["version"] == "v3"
                ),
            },
            registry["citizens"],
        )

    def test_positive_path_resolves_4b_9_11_15_16_and_walks_exact_citations(self) -> None:
        report, model = _run(_ira_acts([1200]), "demo.ira.p5")
        for symbol in ("line-4b", "line-9", "line-11", "line-15", "line-16"):
            self.assertEqual(_disposition(model, symbol), "published_value", symbol)
        self.assertEqual(_published_numeric(model, "line-4b"), 1200)
        self.assertEqual(_published_numeric(model, "line-11"), _published_numeric(model, "line-9"))
        self.assertNotIn("line-4a", {section["id"] for section in model["sections"]})
        line4b = next(item for item in report["dispositions"] if item.get("symbol") == IRA_LINE4B)
        line9 = next(item for item in report["dispositions"] if item.get("symbol") == "tax.us.2025.income.total-income")
        self.assertIn("demo.ira.finding.box1.0", json.dumps(line4b))
        self.assertIn("demo.ira.finding.box2b.0", json.dumps(line4b))
        for pin in ("tax.us.2025.citation.f1099r.box1", "tax.us.2025.citation.f1099r.box2a", "tax.us.2025.citation.f1099r.box2b", "tax.us.2025.citation.f1099r.indicator", "tax.us.2025.citation.f1099r.distribution-code", "tax.us.2025.citation.form1040.line-4b"):
            self.assertIn(pin, json.dumps(_load("rule.f1099r-ira-fully-taxable-subtotal.v3.json")))
        self.assertIn("tax.us.2025.citation.form1040.line-9", json.dumps(line9))

    def test_qualified_dividend_compatibility_keeps_regular_tax_published(self) -> None:
        _, model = _run(_ira_acts([1200], qualified_dividends=True), "demo.ira.p6")
        self.assertEqual(_disposition(model, "line-16"), "published_value")
        self.assertGreaterEqual(_published_numeric(model, "line-16"), 0)
        self.assertEqual(_published_numeric(model, "line-4b"), 1200)

    def test_present_sources_publish_without_closure_and_empty_unclosed_blocks(self) -> None:
        # R1 matrix: present + open/absent publishes the aggregate with no closure pin.
        report, model = _run(_ira_acts([1200], close=False), "demo.ira.r1.present-open")
        self.assertEqual(_disposition(model, "line-4b"), "published_value")
        self.assertEqual(_published_numeric(model, "line-4b"), 1200)
        line4b = next(item for item in report["dispositions"] if item.get("symbol") == IRA_LINE4B)
        pins_blob = json.dumps(line4b.get("pins", line4b))
        self.assertNotIn("tax.us.2025.closure-mapping.f1099r-ira-fully-taxable", pins_blob)
        self.assertNotIn("demo.ira.closure", pins_blob)
        self.assertIn("demo.ira.finding.box1.0", pins_blob)

        # empty + open/absent blocks with no derived value
        empty_report, empty_model = _run(_ira_acts([], close=False), "demo.ira.r1.empty-open")
        self.assertEqual(_disposition(empty_model, "line-4b"), "blocked")
        blocked = next(
            item
            for item in empty_report["dispositions"]
            if item.get("artifact_id") == "tax.us.2025.rule.f1099r-ira-fully-taxable-subtotal"
        )
        self.assertEqual(blocked["disposition"], "blocked")
        self.assertEqual(blocked.get("code"), "SOURCE_SET_UNCLOSED")
        self.assertNotIn("value", blocked)
        self.assertNotIn("finding_id", blocked)

    def test_invalid_box2b_is_blocked_by_companion_contract(self) -> None:
        acts = _ira_acts([1200])
        for act in acts:
            finding = cast(dict[str, Any], cast(dict[str, Any], act.get("payload", {})).get("finding", {}))
            if finding.get("fact_id", "").startswith(IRA_BOX2B):
                finding["value"] = True
        with self.assertRaisesRegex(Exception, "box2b-not-determined"):
            _run(acts, "demo.ira.n6")

    def test_live_route_rejects_missing_box2a_companion(self) -> None:
        acts = _ira_acts([1200])
        acts = [
            act for act in acts
            if not str(cast(dict[str, Any], cast(dict[str, Any], act.get("payload", {})).get("finding", {})).get("fact_id", "")).startswith(IRA_BOX2A + "|")
        ]
        with self.assertRaisesRegex(Exception, "companion presence violated"):
            _run(self._renumber(acts), "demo.ira.repair.missing-box2a")

    def test_live_route_rejects_mismatched_box2a(self) -> None:
        acts = _ira_acts([1200])
        self._finding_for(acts, IRA_BOX2A)["value"] = 1100
        with self.assertRaisesRegex(FindingModelError, "companion equality violated"):
            _run(acts, "demo.ira.repair.mismatched-box2a")

    def test_live_mismatch_is_admission_rejection_without_derived_publication(self) -> None:
        acts = _ira_acts([1200])
        self._finding_for(acts, IRA_BOX2A)["value"] = 1100
        with TemporaryDirectory() as tmp:
            live_root = Path(tmp) / "L"
            with self.assertRaisesRegex(FindingModelError, "companion equality violated"):
                live_coordinate_run(
                    WorkspaceCapability(live_root),
                    repo_root=ROOT,
                    authoritative_acts=acts,
                    workspace_revision=len(acts),
                    run_scope=SCOPE,
                    scope_user=USER,
                    request={"schema": "run-request.v1"},
                    run_id="demo.ira.repair.mismatched-box2a.live",
                    governance_pins=[],
                    surface=PublicationSurface(
                        FIXTURES / "publication_surface" / "releases",
                        CONTENT / "published-packages.v21.json",
                        CONTENT,
                    ),
                    output_name="out.json",
                )
            self.assertFalse(
                any(
                    path.name.endswith(".json")
                    and "derived" in path.read_text("utf-8", errors="ignore")
                    for path in live_root.rglob("*")
                    if path.is_file()
                )
            )

    def test_live_route_rejects_missing_ira_checkbox_companion(self) -> None:
        acts = _ira_acts([1200])
        acts = [
            act for act in acts
            if not str(cast(dict[str, Any], cast(dict[str, Any], act.get("payload", {})).get("finding", {})).get("fact_id", "")).startswith(IRA_CHECKBOX + "|")
        ]
        with self.assertRaisesRegex(Exception, "companion presence violated"):
            _run(self._renumber(acts), "demo.ira.repair.missing-indicator")

    def test_live_route_rejects_missing_and_invalid_code7_witness(self) -> None:
        missing = _ira_acts([1200])
        missing = [
            act for act in missing
            if not str(cast(dict[str, Any], cast(dict[str, Any], act.get("payload", {})).get("finding", {})).get("fact_id", "")).startswith(IRA_CODE + "|")
        ]
        with self.assertRaisesRegex(Exception, "companion presence violated"):
            _run(self._renumber(missing), "demo.ira.repair.missing-code7")

        invalid = _ira_acts([1200])
        self._finding_for(invalid, IRA_CODE)["value"] = "1"
        with self.assertRaises(Exception):
            _run(invalid, "demo.ira.repair.invalid-code7")

    def test_presentation_model_is_compact_and_redacts_blocked_values(self) -> None:
        _, model = _run(_ira_acts([1200]), "demo.ira.p6-presentation")
        selected = {section["id"]: section for section in model["sections"] if section["id"] in {"line-4b", "line-9", "line-11", "line-15", "line-16"}}
        self.assertEqual(set(selected), {"line-4b", "line-9", "line-11", "line-15", "line-16"})
        self.assertTrue(all(section["resolved"].get("value") is not None for section in selected.values()))
        self.assertNotIn("line-4a", json.dumps(model))



class ClosureMatrixAndEntrypointRepairCases(unittest.TestCase):
    """R1 closure matrix + R2 exact-entrypoint validation at production boundary."""

    def test_empty_closed_publishes_zero_with_exact_closure_pins(self) -> None:
        report, model = _run(_ira_acts([], close=True), "demo.ira.r1.empty-closed")
        # Rounding remains a non-source pin, so presentation may label this
        # computed_zero; the contract is the exact closure authority pins.
        self.assertIn(_disposition(model, "line-4b"), {"closure_backed_zero", "computed_zero"})
        self.assertEqual(_published_numeric(model, "line-4b"), 0)
        line4b = next(item for item in report["dispositions"] if item.get("symbol") == IRA_LINE4B)
        pin_ids = {p.get("id") for p in line4b.get("pins", [])}
        self.assertIn("tax.us.2025.closure-mapping.f1099r-ira-fully-taxable", pin_ids)
        self.assertIn("tax.us.2025.f1099r.ira-fully-taxable", pin_ids)
        self.assertIn("demo.ira.closure", pin_ids)

    def test_present_closed_publishes_aggregate_without_closure_pin(self) -> None:
        report, model = _run(_ira_acts([500, 700], close=True), "demo.ira.r1.present-closed")
        self.assertEqual(_disposition(model, "line-4b"), "published_value")
        self.assertEqual(_published_numeric(model, "line-4b"), 1200)
        line4b = next(item for item in report["dispositions"] if item.get("symbol") == IRA_LINE4B)
        pins_blob = json.dumps(line4b.get("pins", line4b))
        self.assertNotIn("demo.ira.closure", pins_blob)
        self.assertNotIn("tax.us.2025.closure-mapping.f1099r-ira-fully-taxable", pins_blob)
        self.assertIn("demo.ira.finding.box1.0", pins_blob)
        self.assertIn("demo.ira.finding.box1.1", pins_blob)

    def test_lifecycle_member_after_old_closure_drops_closure_pin(self) -> None:
        # Empty closed zero first, then a present member on a successor horizon.
        acts = _ira_acts([], close=True)
        # Drop the adoption; rebuild with a late member and re-adopt.
        acts = acts[:-1]
        payer = "demo.ira.payer.alpha"
        statement = "demo.ira.statement.late"
        amount = 333.0
        n = len(acts)

        def add(kind: str, payload: dict[str, object]) -> None:
            nonlocal n
            acts.append(_act(n, kind, payload))
            n += 1

        # Prior empty-closed horizon is demo.ira.h0 (no members).
        add(
            "entity-introduced",
            {
                "entity": {
                    "schema": "entity.v1",
                    "id": statement,
                    "kind": "tax.us.1099r-statement",
                    "label": "Late Form 1099-R",
                }
            },
        )
        for fact_type, value, suffix in (
            (IRA_BOX2A, amount, "box2a"),
            (IRA_CHECKBOX, True, "checkbox"),
            (IRA_CODE, "7", "code"),
            (IRA_BOX2B, False, "box2b"),
        ):
            add(
                "assertion",
                {
                    "finding": _attested(
                        f"demo.ira.finding.late.{suffix}",
                        f"{fact_type}|payer={payer},statement={statement},tax-year=2025",
                        value,
                    )
                },
            )
        add(
            "member-transition",
            {
                "family": {"id": IRA_FAMILY, "version": "v2"},
                "scope": SCOPE_KEY,
                "member": {
                    "action": "assert",
                    "finding": _attested(
                        "demo.ira.finding.box1.late",
                        f"{IRA_BOX1}|payer={payer},statement={statement},tax-year=2025",
                        amount,
                    ),
                },
                "successor": {"id": "demo.ira.h-late", "predecessor": "demo.ira.h0"},
            },
        )
        adoption = _load_fixture_adoption()
        adoption["committed_against"] = len(acts)
        acts.append(adoption)
        report, model = _run(acts, "demo.ira.r1.lifecycle-present-after-closure")
        self.assertEqual(_disposition(model, "line-4b"), "published_value")
        self.assertEqual(_published_numeric(model, "line-4b"), 333)
        line4b = next(item for item in report["dispositions"] if item.get("symbol") == IRA_LINE4B)
        pins_blob = json.dumps(line4b.get("pins", line4b))
        self.assertIn("demo.ira.finding.box1.late", pins_blob)
        self.assertNotIn("demo.ira.closure", pins_blob)
        self.assertNotIn("tax.us.2025.closure-mapping.f1099r-ira-fully-taxable", pins_blob)

    def test_lifecycle_empty_open_or_false_closure_blocks(self) -> None:
        # Empty + no closure blocks (already matrix cell; lifecycle alias).
        report, model = _run(_ira_acts([], close=False), "demo.ira.r1.lifecycle-empty-open")
        self.assertEqual(_disposition(model, "line-4b"), "blocked")
        blocked = next(
            item
            for item in report["dispositions"]
            if item.get("artifact_id") == "tax.us.2025.rule.f1099r-ira-fully-taxable-subtotal"
        )
        self.assertEqual(blocked.get("code"), "SOURCE_SET_UNCLOSED")
        self.assertNotIn("finding_id", blocked)

        # Empty closed, then supersede the closure finding to false -> block.
        acts = _ira_acts([], close=True)[:-1]
        n = len(acts)
        acts.append(
            _act(
                n,
                "assertion",
                {
                    "finding": _attested(
                        "demo.ira.closure.false",
                        f"{IRA_CLOSURE}|family-horizon=demo.ira.h0,tax-year=2025",
                        False,
                    )
                },
            )
        )
        n += 1
        adoption = _load_fixture_adoption()
        adoption["committed_against"] = n
        acts.append(adoption)
        report2, model2 = _run(acts, "demo.ira.r1.lifecycle-false-closure")
        self.assertEqual(_disposition(model2, "line-4b"), "blocked")
        blocked2 = next(
            item
            for item in report2["dispositions"]
            if item.get("artifact_id") == "tax.us.2025.rule.f1099r-ira-fully-taxable-subtotal"
        )
        self.assertEqual(blocked2.get("code"), "SOURCE_SET_UNCLOSED")
        self.assertNotIn("finding_id", blocked2)


class HistoricalEntrypointCompatibilityCases(unittest.TestCase):
    """P1/P2: exact entrypoints only on artifact-package.v20; history preserved."""

    def _adoption_acts(self, path: Path) -> list[dict[str, object]]:
        adoption = cast(dict[str, object], json.loads(path.read_text("utf-8")))
        adoption["committed_against"] = 0
        return [adoption]

    def _surface_for(self, version: int) -> tuple[Path, Path, Path]:
        if version == 17:
            fixture_root = ROOT / "packages" / "sample_data" / "form1099div_box12_line2a"
            registry_name = "published-packages.v12.json"
        else:
            fixture_root = FIXTURES
            registry_name = {
                23: "published-packages.v18.json",
                24: "published-packages.v19.json",
                25: "published-packages.v20.json",
                26: "published-packages.v21.json",
            }[version]
        release_dir = fixture_root / "publication_surface" / "releases"
        adoption_name = f"adopt-core-v{version}-current.json"
        adoption_path = fixture_root / "adoptions" / adoption_name
        return adoption_path, release_dir, CONTENT / registry_name

    def _resolve_published(self, version: int) -> ResolvedGraph:
        adoption_path, release_dir, registry_path = self._surface_for(version)
        result = resolve_production_package(
            self._adoption_acts(adoption_path),
            run_scope=SCOPE,
            scope_user=USER,
            workspace_revision=0,
            surface=PublicationSurface(release_dir, registry_path, CONTENT),
        )
        self.assertIsInstance(result, ResolvedGraph, f"v{version} did not resolve: {result}")
        assert isinstance(result, ResolvedGraph)
        self.assertEqual(result.package["version"], f"v{version}")
        return result

    def _authenticated_mutation_surface(
        self, temporary_root: Path, package: dict[str, Any], mutation: str
    ) -> tuple[PublicationSurface, list[dict[str, object]]]:
        member_dir = temporary_root / "members"
        release_dir = temporary_root / "releases"
        member_dir.mkdir()
        release_dir.mkdir()
        for source in CONTENT.glob("*.json"):
            shutil.copyfile(source, member_dir / source.name)

        mutated = json.loads(json.dumps(package))
        if mutation == "stale":
            for entry in cast(list[dict[str, Any]], mutated["entrypoints"]):
                if entry["id"] == "tax.us.2025.rule.f1099r-ira-fully-taxable-subtotal":
                    entry["version"] = "v1"
                    break
            else:
                self.fail("subtotal entrypoint not found")
        else:
            cast(list[dict[str, Any]], mutated["entrypoints"]).append(
                {"id": "tax.us.2025.rule.nonexistent-entrypoint", "version": "v1"}
            )
        mutated["package_checksum"] = package_instance_checksum(mutated)
        package_path = member_dir / "package.core-calculations.v26.json"
        package_path.write_text(json.dumps(mutated, indent=2, sort_keys=True) + "\n", encoding="utf-8")

        registry = _load("published-packages.v21.json")
        package_entries = cast(list[dict[str, Any]], registry["packages"])
        package_entry = next(
            entry
            for entry in package_entries
            if entry["id"] == mutated["id"] and entry["version"] == mutated["version"]
        )
        package_entry["checksum"] = mutated["package_checksum"]
        registry_path = temporary_root / "published-packages.v21.json"
        registry_bytes = (json.dumps(registry, indent=2, sort_keys=True) + "\n").encode("utf-8")
        registry_path.write_bytes(registry_bytes)

        release_source = FIXTURES / "publication_surface" / "releases" / "demo.release.2025.v19.json"
        release = cast(dict[str, Any], json.loads(release_source.read_text("utf-8")))
        release["package_registry_sha256"] = hashlib.sha256(registry_bytes).hexdigest()
        release_bytes = (json.dumps(release, indent=2, sort_keys=True) + "\n").encode("utf-8")
        (release_dir / release_source.name).write_bytes(release_bytes)

        adoption = cast(
            dict[str, object],
            json.loads((FIXTURES / "adoptions" / "adopt-core-v26-current.json").read_text("utf-8")),
        )
        payload = cast(dict[str, Any], adoption["payload"])
        payload["package"]["checksum"] = mutated["package_checksum"]
        payload["release"]["checksum"] = hashlib.sha256(release_bytes).hexdigest()
        adoption["committed_against"] = 0
        return PublicationSurface(release_dir, registry_path, member_dir), [adoption]

    def test_historical_packages_resolve_through_authentic_publication_chains(self) -> None:
        for version in (17, 23, 24, 25):
            self._resolve_published(version)

    def test_v26_exact_entrypoints_resolve_and_mutations_hard_refuse(self) -> None:
        graph = self._resolve_published(26)
        self.assertEqual(graph.package["schema"], "artifact-package.v20")
        for mutation in ("stale", "dangling"):
            with self.subTest(mutation=mutation), TemporaryDirectory() as directory:
                surface, acts = self._authenticated_mutation_surface(
                    Path(directory), graph.package, mutation
                )
                result = resolve_production_package(
                    acts,
                    run_scope=SCOPE,
                    scope_user=USER,
                    workspace_revision=0,
                    surface=surface,
                )
                self.assertIsInstance(result, Refusal)
                assert isinstance(result, Refusal)
                self.assertEqual(result.reason, "HARD_GATE_REFUSED")
                expected_code = (
                    "ENTRYPOINT_VERSION_MISMATCH" if mutation == "stale" else "ENTRYPOINT_DANGLING"
                )
                self.assertIn(expected_code, {issue["code"] for issue in result.issues})



if __name__ == "__main__":
    unittest.main()
