"""Track 1B lifecycle and presentation evidence for Schedule B adjustments."""

from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any, cast

import jsonschema

from packages.derivation.live import live_coordinate_run
from packages.derivation.live_workspace import WorkspaceCapability
from packages.derivation.loader import DerivationSchemas
from packages.derivation.package_validation import (
    citizen_checksum,
    load_published_citizen_checksums,
    validate_package,
)
from packages.derivation.production_resolver import PublicationSurface
from tests.test_market_discount_interest_integration import _act, _attested, _md_acts


ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "packages" / "content" / "tax" / "2025"
FIXTURES = ROOT / "packages" / "sample_data" / "schedule_b_interest_adjustments"
USER = "demo.user.filer-1"
SCOPE = {"jurisdiction": "us", "year": "2025"}
SCOPE_KEY = {"tax-year": "2025", "subject": "demo.primary"}
CLASSES = (
    ("nominee", "nominee_distribution", "Nominee Distribution"),
    ("accrued-interest", "accrued_interest", "Accrued Interest"),
    ("abp-adjustment", "abp_adjustment", "ABP Adjustment"),
)


def _surface() -> PublicationSurface:
    return PublicationSurface(
        FIXTURES / "publication_surface" / "releases",
        CONTENT / "published-packages.v10.json",
        CONTENT,
    )


def _ids(token: str) -> dict[str, str]:
    prefix = f"tax.us.2025.scheduleb.adjustment.{token}"
    return {
        "family": prefix,
        "amount": f"{prefix}.amount",
        "closure": f"{prefix}.source-closure",
    }


def _adjustment_acts(
    *,
    values: dict[str, list[float]] | None = None,
    close: set[str] | None = None,
    box1_interest: float = 2000,
) -> list[dict[str, object]]:
    values = {} if values is None else values
    close = {token for token, _kind, _label in CLASSES} if close is None else close
    acts = _md_acts(
        b10_values=[],
        oid5_values=[],
        box1_interest=box1_interest,
        dividends=0,
        complete_schedule_b=True,
    )
    acts.pop()  # replace the historical v10 adoption with the v14 route

    def add(kind: str, payload: dict[str, object]) -> None:
        acts.append(_act(len(acts), kind, payload))

    for token, _kind, _label in CLASSES:
        add(
            "bundle-adoption",
            {"bundle": json.loads((CONTENT / f"scheduleb-adjustment.{token}.bundle.json").read_text("utf-8"))},
        )
        add(
            "entity-introduced",
            {
                "entity": {
                    "schema": "entity.v1",
                    "id": f"demo.sbia.{token}.instance.0",
                    "kind": "tax.us.scheduleb-adjustment-instance",
                    "label": f"Synthetic {token} adjustment instance",
                }
            },
        )
        add(
            "horizon-genesis",
            {
                "family": {"id": _ids(token)["family"], "version": "v1"},
                "scope": SCOPE_KEY,
                "horizon_id": f"demo.sbia.{token}.h0",
            },
        )

        horizon = f"demo.sbia.{token}.h0"
        for index, value in enumerate(values.get(token, [])):
            instance = f"demo.sbia.{token}.instance.{index}"
            if index > 0:
                add(
                    "entity-introduced",
                    {
                        "entity": {
                            "schema": "entity.v1",
                            "id": instance,
                            "kind": "tax.us.scheduleb-adjustment-instance",
                            "label": f"Synthetic {token} adjustment instance {index}",
                        }
                    },
                )
            next_horizon = f"demo.sbia.{token}.h{index + 1}"
            add(
                "member-transition",
                {
                    "family": {"id": _ids(token)["family"], "version": "v1"},
                    "scope": SCOPE_KEY,
                    "member": {
                        "action": "assert",
                        "finding": _attested(
                            f"demo.sbia.finding.{token}.{index}",
                            f"{_ids(token)['amount']}|tax-year=2025,adjustment-instance={instance}",
                            value,
                        ),
                    },
                    "successor": {"id": next_horizon, "predecessor": horizon},
                },
            )
            horizon = next_horizon
        if token in close:
            add(
                "assertion",
                {
                    "finding": _attested(
                        f"demo.sbia.closure.{token}",
                        f"{_ids(token)['closure']}|family-horizon={horizon},tax-year=2025",
                        True,
                    )
                },
            )

    adoption = cast(dict[str, object], json.loads((FIXTURES / "adoptions" / "adopt-core-v15-current.json").read_text("utf-8")))
    adoption["committed_against"] = len(acts)
    acts.append(adoption)
    return acts


def _run(acts: list[dict[str, object]], run_id: str) -> tuple[dict[str, Any], dict[str, Any]]:
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
            surface=_surface(),
            output_name="out.json",
        )
        assert result.refusal is None, result.refusal
        assert result.output_path is not None and result.presentation_path is not None
        return json.loads(result.output_path.read_text("utf-8")), json.loads(result.presentation_path.read_text("utf-8"))


def _section(model: dict[str, Any], section_id: str) -> dict[str, Any]:
    return next(section for section in model["sections"] if section["id"] == section_id)


class AdjustmentContractCases(unittest.TestCase):
    def test_each_class_has_exact_identity_and_nonnegative_amount(self) -> None:
        for token, _kind, _label in CLASSES:
            with self.subTest(token=token):
                bundle = json.loads((CONTENT / f"scheduleb-adjustment.{token}.bundle.json").read_text("utf-8"))
                amount = bundle["fact_types"][0]
                self.assertEqual([key["name"] for key in amount["identity_keys"]], ["tax-year", "adjustment-instance"])
                self.assertEqual(amount["value_schema"], {"minimum": 0, "type": "number"})
                self.assertNotIn("evidence", json.dumps(amount["identity_keys"]))
                with self.assertRaises(jsonschema.ValidationError):
                    jsonschema.validate(-1, amount["value_schema"])

    def test_v15_package_admits_all_three_exact_classes(self) -> None:
        package = json.loads((CONTENT / "package.core-calculations.v15.json").read_text("utf-8"))
        corpus = {
            (value["id"], value["version"]): value
            for path in CONTENT.glob("*.json")
            if isinstance((value := json.loads(path.read_text("utf-8"))).get("id"), str)
            and isinstance(value.get("version"), str)
        }
        result = validate_package(
            package,
            corpus,
            DerivationSchemas(),
            load_published_citizen_checksums(CONTENT / "published-packages.v10.json"),
        )
        self.assertTrue(result.ok, result.issues)

    def test_v15_attachment_mutations_reject_each_class_label_or_authority(self) -> None:
        package = json.loads((CONTENT / "package.core-calculations.v15.json").read_text("utf-8"))
        corpus = {
            (value["id"], value["version"]): value
            for path in CONTENT.glob("*.json")
            if isinstance((value := json.loads(path.read_text("utf-8"))).get("id"), str)
            and isinstance(value.get("version"), str)
        }
        registry = load_published_citizen_checksums(CONTENT / "published-packages.v10.json")
        for index, (_token, _kind, label) in enumerate(CLASSES):
            with self.subTest(index=index):
                mutated = copy.deepcopy(corpus)
                attachment = copy.deepcopy(mutated[("tax.us.2025.rule.attachment.schedule-b", "v4")])
                row = attachment["itemizations"][0]["adjustment_rows"][index]
                if index == 0:
                    row["label"] = "Accrued Interest"
                else:
                    row["rows"]["source_family"]["id"] = "tax.us.2025.scheduleb.adjustment.nominee"
                mutated[("tax.us.2025.rule.attachment.schedule-b", "v4")] = attachment
                mutated_registry = dict(registry)
                mutated_registry[(attachment["id"], attachment["version"])] = citizen_checksum(attachment)
                result = validate_package(package, mutated, DerivationSchemas(), mutated_registry)
                codes = {issue.code for issue in result.issues}
                self.assertTrue(
                    {"ATTACHMENT_ADJUSTMENT_LABEL_MISMATCH", "ATTACHMENT_ADJUSTMENT_AUTHORITY_MISMATCH", "ATTACHMENT_ADJUSTMENT_CLASS_SURFACE_MISMATCH"} & codes,
                    (label, result.issues),
                )


class AdjustmentLifecycleCases(unittest.TestCase):
    def test_each_adjustment_family_reaches_line2b_and_schedule_b_label(self) -> None:
        for token, _kind, label in CLASSES:
            with self.subTest(token=token):
                _, model = _run(_adjustment_acts(values={token: [100]}), f"demo.sbia.{token}")
                self.assertEqual(_section(model, "line-2b")["resolved"]["value"], 1900)
                group = next(group for group in model["citationGroups"] if group["id"] == "tax.us.2025.rule.attachment.schedule-b")
                headings = [part["heading"] for part in group["parts"]]
                self.assertIn(label, headings)

    def test_composition_subtracts_all_three_once(self) -> None:
        _, model = _run(
            _adjustment_acts(values={"nominee": [100], "accrued-interest": [50], "abp-adjustment": [25]}),
            "demo.sbia.combined",
        )
        self.assertEqual(_section(model, "line-2b")["resolved"]["value"], 1825)
        group = next(group for group in model["citationGroups"] if group["id"] == "tax.us.2025.rule.attachment.schedule-b")
        self.assertEqual([part["heading"] for part in group["parts"][:4]], ["Part I: Taxable Interest", "Nominee Distribution", "Accrued Interest", "ABP Adjustment"])

    def test_gross_positive_line1_threshold_survives_subtraction(self) -> None:
        """SIA-P7: gross positive line 1 can require Schedule B below net line 2b $1,500."""
        _, model = _run(
            _adjustment_acts(values={"nominee": [200]}, box1_interest=1600),
            "demo.sbia.threshold-after-adjustment",
        )
        self.assertEqual(_section(model, "line-2b")["resolved"]["value"], 1400)
        group = next(group for group in model["citationGroups"] if group["id"] == "tax.us.2025.rule.attachment.schedule-b")
        self.assertIn("Nominee Distribution", [part["heading"] for part in group["parts"]])

    def test_closed_empty_and_correction_are_current(self) -> None:
        _, empty = _run(_adjustment_acts(values={}), "demo.sbia.empty")
        self.assertEqual(_section(empty, "line-2b")["resolved"]["value"], 2000)

        acts = _adjustment_acts(values={"nominee": [100]})
        acts.append(_act(len(acts), "assertion", {"finding": _attested(
            "demo.sbia.finding.nominee.correction",
            f"{_ids('nominee')['amount']}|tax-year=2025,adjustment-instance=demo.sbia.nominee.instance.0",
            140,
        )}))
        _, corrected = _run(acts, "demo.sbia.correction")
        self.assertEqual(_section(corrected, "line-2b")["resolved"]["value"], 1860)

    def test_unclosed_and_late_member_block_until_successor_closure(self) -> None:
        acts = _adjustment_acts(values={"accrued-interest": [100]}, close={"nominee", "abp-adjustment"})
        _, blocked = _run(acts, "demo.sbia.unclosed")
        self.assertEqual(_section(blocked, "line-2b")["resolved"]["disposition"], "blocked")

        acts = _adjustment_acts(values={"nominee": [100]})
        acts.append(_act(len(acts), "entity-introduced", {"entity": {
            "schema": "entity.v1", "id": "demo.sbia.nominee.instance.late",
            "kind": "tax.us.scheduleb-adjustment-instance", "label": "Synthetic late nominee instance",
        }}))
        acts.append(_act(len(acts), "member-transition", {
            "family": {"id": _ids("nominee")["family"], "version": "v1"},
            "scope": SCOPE_KEY,
            "member": {"action": "assert", "finding": _attested(
                "demo.sbia.finding.nominee.late",
                f"{_ids('nominee')['amount']}|tax-year=2025,adjustment-instance=demo.sbia.nominee.instance.late",
                20,
            )},
            "successor": {"id": "demo.sbia.nominee.h2", "predecessor": "demo.sbia.nominee.h1"},
        }))
        _, late = _run(acts, "demo.sbia.late")
        self.assertEqual(_section(late, "line-2b")["resolved"]["disposition"], "blocked")

    def test_overage_never_publishes_negative_line2b(self) -> None:
        _, model = _run(_adjustment_acts(values={"nominee": [1200]}, box1_interest=1000), "demo.sbia.overage")
        line2b = _section(model, "line-2b")["resolved"]
        self.assertNotEqual(line2b.get("value"), -200)
        self.assertEqual(line2b["disposition"], "guard_inapplicable")

    def test_compact_presentation_mutation_keeps_sibling_section(self) -> None:
        _, model = _run(_adjustment_acts(values={"nominee": [100]}), "demo.sbia.malformed")
        malformed = copy.deepcopy(model)
        _section(malformed, "line-2b")["resolved"]["value"] = "rejected-adjustment-value"
        self.assertEqual(_section(malformed, "line-9")["resolved"]["disposition"], "blocked")

    def test_committed_presentation_golden_is_live_deterministic(self) -> None:
        from tools.generate_schedule_b_interest_adjustments_goldens import TARGET, regenerate

        self.assertEqual(json.loads(TARGET.read_text("utf-8")), regenerate())


if __name__ == "__main__":
    unittest.main()
