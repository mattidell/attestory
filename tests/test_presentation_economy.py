from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path
from typing import Any

from tools.presentation_economy import (
    ValidationError,
    build_comparison,
    load_dataset,
    load_workload,
    validate_dataset,
    validate_workload,
)


ROOT = Path(__file__).resolve().parents[1]
BASELINE = (
    ROOT
    / "docs"
    / "presentation-economy"
    / "datasets"
    / "presentation-exploratory-baseline.v1.json"
)
FROZEN_WORKLOAD = (
    ROOT
    / "docs"
    / "presentation-economy"
    / "workloads"
    / "presentation-review.v1.json"
)
VALID_OBSERVATIONS = (
    ROOT
    / "docs"
    / "presentation-economy"
    / "examples"
    / "valid-observations.v1.json"
)
INVALID_OBSERVATIONS = (
    ROOT
    / "docs"
    / "presentation-economy"
    / "examples"
    / "invalid"
    / "observation-cases.v1.json"
)
INVALID_COMPARISONS = (
    ROOT
    / "docs"
    / "presentation-economy"
    / "examples"
    / "invalid"
    / "comparison-cases.v1.json"
)


def apply_fixture_mutation(value: Any, mutation: dict[str, Any]) -> None:
    parts = mutation["path"].split(".")
    target = value
    for part in parts[:-1]:
        target = target[int(part)] if isinstance(target, list) else target[part]
    key = parts[-1]
    if mutation["operation"] == "remove":
        if isinstance(target, list):
            target.pop(int(key))
        else:
            del target[key]
    elif isinstance(target, list):
        target[int(key)] = mutation["value"]
    else:
        target[key] = mutation["value"]


class PresentationEconomyBaselineTest(unittest.TestCase):
    def setUp(self) -> None:
        self.dataset = load_dataset(BASELINE)

    def test_source_table_reconciles_every_c1_c5_cell(self) -> None:
        # Direct transcription of analysis/04-economy.md. None represents "–".
        expected: dict[str, dict[str, tuple[int | None, int | None, int | None]]] = {
            "C1": {
                "B-A": (42600, 14, 165),
                "B-B": (46500, 7, 170),
                "R1": (93100, 65, 397),
                "R2": (69000, 29, 220),
            },
            "C2": {
                "B-A": (43800, 7, 136),
                "B-B": (45300, 9, 149),
                "R1": (66900, 46, 176),
                "R2": (73200, 54, 999),
            },
            "C3": {
                "B-A": (57400, 22, 238),
                "B-B": (63500, 26, 312),
                "R1": (65300, 28, 115),
                "R2": (70000, None, None),
            },
            "C4": {
                "B-A": (66200, 29, 313),
                "B-B": (65100, 23, 317),
                "R1": (85200, 57, 246),
                "R2": (127700, 73, 999),
            },
            "C5": {
                "B-A": (76800, 15, 420),
                "B-B": (59900, 13, 281),
                "R1": (111600, 45, 424),
                "R2": (81400, 26, 262),
            },
        }
        workloads = {item["id"]: item for item in self.dataset["workloads"]}
        actual: dict[str, dict[str, tuple[int | None, int | None, int | None]]] = {}
        for observation in self.dataset["observations"]:
            cycle = workloads[observation["workload_id"]]["cycle"]
            rows = {}
            for participant in observation["participants"]:
                if participant["role"] == "foreman":
                    continue
                rows[participant["id"]] = (
                    participant["tokens"]["value"],
                    participant["tool_calls"]["value"],
                    participant["wall_seconds"]["value"],
                )
            actual[cycle] = rows
        self.assertEqual(expected, actual)

    def test_approximate_and_missing_source_cells_remain_honest(self) -> None:
        cycle_three = self.dataset["observations"][2]
        reviewer_two = cycle_three["participants"][3]
        self.assertEqual(70000, reviewer_two["tokens"]["value"])
        self.assertTrue(reviewer_two["tokens"]["approximate"])
        for name in ("tool_calls", "wall_seconds"):
            measure = reviewer_two[name]
            self.assertIsNone(measure["value"])
            self.assertEqual("missing", measure["measurement_basis"])
            self.assertTrue(measure["missing_reason"])

    def test_foreman_and_orchestration_gaps_are_explicit(self) -> None:
        for observation in self.dataset["observations"]:
            foreman = observation["participants"][-1]
            self.assertEqual("foreman", foreman["role"])
            for name in ("tokens", "tool_calls", "wall_seconds"):
                self.assertIsNone(foreman[name]["value"])
                self.assertTrue(foreman[name]["missing_reason"])
            orchestration = observation["orchestration"]
            self.assertIsNone(orchestration["foreman_idle_gap_seconds"]["value"])
            self.assertIsNone(orchestration["cache_status"]["value"])
            self.assertFalse(orchestration["cache_status"]["directly_observed"])
            self.assertTrue(orchestration["cache_status"]["missing_reason"])
            self.assertIsNone(observation["resources"]["agent_count"]["value"])
            self.assertIsNone(observation["outcome"]["criteria_completed"]["value"])
            self.assertIsNone(observation["outcome"]["quality_floor_met"]["value"])


class PresentationEconomyValidationTest(unittest.TestCase):
    def setUp(self) -> None:
        self.dataset: dict[str, Any] = load_dataset(BASELINE)

    def assert_invalid(self, mutation: Any, message: str) -> None:
        candidate = copy.deepcopy(self.dataset)
        mutation(candidate)
        with self.assertRaisesRegex(ValidationError, message):
            validate_dataset(candidate)

    def test_unknown_keys_fail(self) -> None:
        self.assert_invalid(
            lambda value: value["observations"][0].update({"surprise": True}),
            "unknown",
        )

    def test_negative_counts_fail(self) -> None:
        self.assert_invalid(
            lambda value: value["observations"][0]["participants"][0]["tool_calls"].update(
                {"value": -1}
            ),
            "non-negative",
        )

    def test_null_measure_requires_missing_reason(self) -> None:
        self.assert_invalid(
            lambda value: value["observations"][2]["participants"][3]["tool_calls"].update(
                {"missing_reason": None}
            ),
            "non-empty string",
        )

    def test_populated_measure_cannot_claim_missing_basis(self) -> None:
        self.assert_invalid(
            lambda value: value["observations"][0]["participants"][0]["tokens"].update(
                {"measurement_basis": "missing"}
            ),
            "populated value",
        )

    def test_approximate_measure_is_explicit(self) -> None:
        self.assert_invalid(
            lambda value: value["observations"][2]["participants"][3]["tokens"].update(
                {"approximate": None}
            ),
            "boolean",
        )

    def test_cache_status_cannot_be_inferred(self) -> None:
        self.assert_invalid(
            lambda value: value["observations"][0]["orchestration"]["cache_status"].update(
                {
                    "value": "hit",
                    "directly_observed": False,
                    "observation_provenance": None,
                    "missing_reason": None,
                }
            ),
            "must be directly observed",
        )

    def test_direct_cache_status_requires_repository_provenance(self) -> None:
        self.assert_invalid(
            lambda value: value["observations"][0]["orchestration"]["cache_status"].update(
                {
                    "value": "hit",
                    "directly_observed": True,
                    "observation_provenance": str(
                        (ROOT / "demo-invalid-cache.json").resolve()
                    ),
                    "missing_reason": None,
                }
            ),
            "repository-relative",
        )

    def test_invalid_task_budget_and_execution_mode_fail(self) -> None:
        self.assert_invalid(
            lambda value: value["observations"][0]["orchestration"][
                "task_duration_budget_seconds"
            ].update(
                {
                    "value": -1,
                    "approximate": False,
                    "measurement_basis": "direct",
                    "missing_reason": None,
                }
            ),
            "non-negative",
        )
        self.assert_invalid(
            lambda value: value["observations"][0]["orchestration"][
                "execution_mode"
            ].update({"value": "maybe", "missing_reason": None}),
            "expected one of",
        )

    def test_duplicate_and_dangling_references_fail(self) -> None:
        self.assert_invalid(
            lambda value: value["observations"][1].update(
                {"id": value["observations"][0]["id"]}
            ),
            "duplicate",
        )
        self.assert_invalid(
            lambda value: value["observations"][0].update(
                {"workload_id": "demo-missing-workload"}
            ),
            "dangling reference",
        )

    def test_historical_observation_cannot_claim_causality(self) -> None:
        self.assert_invalid(
            lambda value: value["observations"][0].update({"causal_claim": True}),
            "cannot make a causal claim",
        )

    def test_append_only_correction_requires_valid_supersession(self) -> None:
        correction = copy.deepcopy(self.dataset["observations"][0])
        correction["id"] = "demo-historical-c1-correction"
        correction["supersedes"] = "demo-historical-c1"
        correction["supersession_reason"] = "Correct a transcription while retaining the source row."
        self.dataset["observations"].append(correction)
        validate_dataset(self.dataset)

        correction["supersedes"] = "demo-unknown-observation"
        with self.assertRaisesRegex(ValidationError, "dangling reference"):
            validate_dataset(self.dataset)

    def test_supersession_requires_reason_and_same_workload(self) -> None:
        correction = copy.deepcopy(self.dataset["observations"][0])
        correction["id"] = "demo-historical-c1-correction"
        correction["supersedes"] = "demo-historical-c1"
        correction["supersession_reason"] = None
        self.dataset["observations"].append(correction)
        with self.assertRaisesRegex(ValidationError, "non-empty string"):
            validate_dataset(self.dataset)

        correction["supersession_reason"] = "Correction."
        correction["workload_id"] = "demo-historical-c2-workload"
        with self.assertRaisesRegex(ValidationError, "workload must match"):
            validate_dataset(self.dataset)


class PresentationEconomyWorkloadTest(unittest.TestCase):
    def setUp(self) -> None:
        self.workload: dict[str, Any] = load_workload(FROZEN_WORKLOAD)

    def test_frozen_workload_names_equivalent_arms_and_complete_floor(self) -> None:
        labels = {
            treatment["label"]
            for treatment in self.workload["intervention"]["treatments"]
        }
        self.assertEqual({"manual", "harness-assisted"}, labels)
        self.assertEqual(
            set(self.workload["criteria"]),
            set(self.workload["quality_floor"]["required_criteria"]),
        )
        self.assertEqual(
            {"T1", "T2", "T3"},
            {defect["tier"] for defect in self.workload["seeded_defects"]},
        )

    def test_workload_rejects_unknown_floor_reference(self) -> None:
        self.workload["quality_floor"]["required_criteria"].append("demo-unknown")
        with self.assertRaisesRegex(ValidationError, "unknown criterion"):
            validate_workload(self.workload)

    def test_workload_rejects_non_synthetic_or_machine_local_fixture(self) -> None:
        self.workload["fixtures"][0]["synthetic"] = False
        with self.assertRaisesRegex(ValidationError, "expected true"):
            validate_workload(self.workload)
        self.workload = load_workload(FROZEN_WORKLOAD)
        self.workload["fixtures"][0]["path"] = str(
            (ROOT / "demo-invalid-fixture.json").resolve()
        )
        with self.assertRaisesRegex(ValidationError, "repository-relative"):
            validate_workload(self.workload)

    def test_valid_single_paired_and_repeated_examples(self) -> None:
        with VALID_OBSERVATIONS.open(encoding="utf-8") as handle:
            observations = json.load(handle)
        validate_dataset(
            {
                "workloads": [self.workload],
                "observations": observations,
                "comparisons": [],
            }
        )
        self.assertIn("demo-single-run", {item["id"] for item in observations})
        paired = [item for item in observations if item["id"].startswith("demo-paired-")]
        self.assertEqual({"manual", "harness-assisted"}, {item["treatment"] for item in paired})
        repeated = [item for item in observations if item["evidence_class"] == "repeated"]
        self.assertEqual(2, len(repeated))

    def test_committed_invalid_observation_fixtures_fail_as_declared(self) -> None:
        with VALID_OBSERVATIONS.open(encoding="utf-8") as handle:
            observations = json.load(handle)
        with INVALID_OBSERVATIONS.open(encoding="utf-8") as handle:
            cases = json.load(handle)
        for case in cases:
            with self.subTest(case=case["id"]):
                dataset = {
                    "workloads": [copy.deepcopy(self.workload)],
                    "observations": copy.deepcopy(observations),
                    "comparisons": [],
                }
                for mutation in case["mutations"]:
                    apply_fixture_mutation(dataset, mutation)
                with self.assertRaisesRegex(ValidationError, case["expected_error"]):
                    validate_dataset(dataset)


class PresentationEconomyComparisonTest(unittest.TestCase):
    def setUp(self) -> None:
        self.workload: dict[str, Any] = load_workload(FROZEN_WORKLOAD)
        with VALID_OBSERVATIONS.open(encoding="utf-8") as handle:
            all_observations = json.load(handle)
        self.observations = [
            item for item in all_observations if item["id"].startswith("demo-paired-")
        ]

    def test_comparison_gates_quality_then_aggregates_every_role(self) -> None:
        result = build_comparison(
            self.workload, self.observations, "manual", "harness-assisted"
        )
        self.assertTrue(result["quality"]["comparable"])
        self.assertFalse(result["causal_claim"])
        measures = {item["name"]: item for item in result["measures"]}
        self.assertEqual(15200, measures["tokens"]["baseline_value"])
        self.assertEqual(11200, measures["tokens"]["treatment_value"])
        self.assertEqual(-4000, measures["tokens"]["delta"])
        self.assertEqual("economically-promising", measures["tokens"]["verdict"])
        self.assertEqual(
            ["demo-paired-manual", "demo-paired-harness"],
            [item["id"] for item in result["raw_observations"]],
        )

    def test_incomplete_role_cost_blocks_only_that_measure(self) -> None:
        observations = copy.deepcopy(self.observations)
        measure = observations[1]["participants"][-1]["tokens"]
        measure.update(
            {
                "value": None,
                "approximate": False,
                "measurement_basis": "missing",
                "missing_reason": "Manufactured missing participant cost.",
            }
        )
        result = build_comparison(
            self.workload, observations, "manual", "harness-assisted"
        )
        measures = {item["name"]: item for item in result["measures"]}
        self.assertEqual("insufficient-evidence", measures["tokens"]["verdict"])
        self.assertEqual("economically-promising", measures["tool_calls"]["verdict"])

    def test_failed_quality_blocks_every_cost_verdict(self) -> None:
        observations = copy.deepcopy(self.observations)
        observations[1]["outcome"]["seeded_defects_detected"]["value"].pop()
        observations[1]["outcome"]["quality_floor_met"]["value"] = False
        result = build_comparison(
            self.workload, observations, "manual", "harness-assisted"
        )
        self.assertFalse(result["quality"]["comparable"])
        self.assertTrue(all(item["verdict"] == "insufficient-evidence" for item in result["measures"]))

    def test_incompatible_workload_and_dangling_comparison_ref_fail(self) -> None:
        observations = copy.deepcopy(self.observations)
        observations[1]["workload_id"] = "demo-other-workload"
        with self.assertRaisesRegex(ValidationError, "dangling reference"):
            build_comparison(self.workload, observations, "manual", "harness-assisted")

        result = build_comparison(
            self.workload, self.observations, "manual", "harness-assisted"
        )
        result["baseline_observation_ids"][0] = "demo-missing-observation"
        with self.assertRaisesRegex(ValidationError, "dangling observation reference"):
            validate_dataset(
                {
                    "workloads": [self.workload],
                    "observations": self.observations,
                    "comparisons": [result],
                }
            )

    def test_comparison_contract_forbids_causal_claim(self) -> None:
        result = build_comparison(
            self.workload, self.observations, "manual", "harness-assisted"
        )
        result["causal_claim"] = True
        with self.assertRaisesRegex(ValidationError, "unsupported causal claim"):
            validate_dataset(
                {
                    "workloads": [self.workload],
                    "observations": self.observations,
                    "comparisons": [result],
                }
            )

    def test_committed_invalid_comparison_fixtures(self) -> None:
        with INVALID_COMPARISONS.open(encoding="utf-8") as handle:
            cases = json.load(handle)
        for case in cases:
            with self.subTest(case=case["id"]):
                dataset = {
                    "workloads": [copy.deepcopy(self.workload)],
                    "observations": copy.deepcopy(self.observations),
                    "comparisons": [],
                }
                if case["stage"] == "validate-comparison":
                    dataset["comparisons"] = [
                        build_comparison(
                            self.workload,
                            self.observations,
                            "manual",
                            "harness-assisted",
                        )
                    ]
                for mutation in case["mutations"]:
                    apply_fixture_mutation(dataset, mutation)
                if case["stage"] in {"build", "build-result"}:
                    if "expected_error" in case:
                        with self.assertRaisesRegex(
                            ValidationError, case["expected_error"]
                        ):
                            build_comparison(
                                dataset["workloads"][0],
                                dataset["observations"],
                                "manual",
                                "harness-assisted",
                            )
                    else:
                        result = build_comparison(
                            dataset["workloads"][0],
                            dataset["observations"],
                            "manual",
                            "harness-assisted",
                        )
                        measures = {item["name"]: item for item in result["measures"]}
                        self.assertEqual(
                            case["expected_verdict"],
                            measures[case["expected_measure"]]["verdict"],
                        )
                else:
                    with self.assertRaisesRegex(
                        ValidationError, case["expected_error"]
                    ):
                        validate_dataset(dataset)


if __name__ == "__main__":
    unittest.main()
