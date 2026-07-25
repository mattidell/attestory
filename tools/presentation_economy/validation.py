"""Dependency-free validation for presentation economy records."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


WORKLOAD_VERSION = "presentation-economy-workload.v1"
OBSERVATION_VERSION = "presentation-economy-observation.v1"
COMPARISON_VERSION = "presentation-economy-comparison.v1"
EVIDENCE_CLASSES = {"historical-observational", "paired-pilot", "repeated"}
ROLES = {"builder", "reviewer", "foreman", "harness"}
TIERS = {"Economy", "Medium", "High", "unrecorded"}
EFFORTS = {"low", "medium", "high", "unrecorded"}
MEASUREMENT_BASES = {"direct", "source-reported", "missing"}
EXECUTION_MODES = {"parallel", "sequential", "inline"}
DEFECT_TIERS = {"T1", "T2", "T3"}


class ValidationError(ValueError):
    """Raised when a presentation-economy document violates its contract."""


def _mapping(value: Any, path: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValidationError(f"{path}: expected object")
    return value


def _sequence(value: Any, path: str) -> list[Any]:
    if not isinstance(value, list):
        raise ValidationError(f"{path}: expected array")
    return value


def _keys(value: dict[str, Any], expected: set[str], path: str) -> None:
    actual = set(value)
    missing = sorted(expected - actual)
    unknown = sorted(actual - expected)
    if missing or unknown:
        details = []
        if missing:
            details.append(f"missing {missing}")
        if unknown:
            details.append(f"unknown {unknown}")
        raise ValidationError(f"{path}: {'; '.join(details)}")


def _text(value: Any, path: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValidationError(f"{path}: expected non-empty string")
    return value


def _repo_path(value: Any, path: str) -> str:
    text = _text(value, path)
    candidate = Path(text)
    if candidate.is_absolute() or ".." in candidate.parts:
        raise ValidationError(f"{path}: expected repository-relative path")
    return text


def _enum(value: Any, allowed: set[str], path: str) -> str:
    text = _text(value, path)
    if text not in allowed:
        raise ValidationError(f"{path}: expected one of {sorted(allowed)}")
    return text


def _nonnegative_int(value: Any, path: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise ValidationError(f"{path}: expected non-negative integer")
    return value


def _unique_texts(value: Any, path: str) -> list[str]:
    items = _sequence(value, path)
    result: list[str] = []
    for index, item in enumerate(items):
        result.append(_text(item, f"{path}[{index}]"))
    if len(result) != len(set(result)):
        raise ValidationError(f"{path}: duplicate values")
    return result


def _measure(value: Any, path: str) -> None:
    item = _mapping(value, path)
    _keys(item, {"value", "approximate", "measurement_basis", "missing_reason"}, path)
    raw = item["value"]
    approximate = item["approximate"]
    if not isinstance(approximate, bool):
        raise ValidationError(f"{path}.approximate: expected boolean")
    basis = _enum(item["measurement_basis"], MEASUREMENT_BASES, f"{path}.measurement_basis")
    reason = item["missing_reason"]
    if raw is None:
        if approximate:
            raise ValidationError(f"{path}: missing measure cannot be approximate")
        if basis != "missing":
            raise ValidationError(f"{path}: null value requires missing measurement_basis")
        _text(reason, f"{path}.missing_reason")
        return
    _nonnegative_int(raw, f"{path}.value")
    if basis == "missing":
        raise ValidationError(f"{path}: populated value cannot have missing measurement_basis")
    if basis == "direct" and approximate:
        raise ValidationError(f"{path}: directly observed value cannot be approximate")
    if reason is not None:
        raise ValidationError(f"{path}.missing_reason: populated value requires null")


def _nullable_text(value: Any, path: str, allowed: set[str] | None = None) -> None:
    item = _mapping(value, path)
    _keys(item, {"value", "missing_reason"}, path)
    raw = item["value"]
    if raw is None:
        _text(item["missing_reason"], f"{path}.missing_reason")
        return
    if allowed is None:
        _text(raw, f"{path}.value")
    else:
        _enum(raw, allowed, f"{path}.value")
    if item["missing_reason"] is not None:
        raise ValidationError(f"{path}.missing_reason: populated value requires null")


def _nullable_text_list(value: Any, path: str) -> None:
    item = _mapping(value, path)
    _keys(item, {"value", "missing_reason"}, path)
    if item["value"] is None:
        _text(item["missing_reason"], f"{path}.missing_reason")
        return
    _unique_texts(item["value"], f"{path}.value")
    if item["missing_reason"] is not None:
        raise ValidationError(f"{path}.missing_reason: populated value requires null")


def _nullable_bool(value: Any, path: str) -> None:
    item = _mapping(value, path)
    _keys(item, {"value", "missing_reason"}, path)
    if item["value"] is None:
        _text(item["missing_reason"], f"{path}.missing_reason")
        return
    if not isinstance(item["value"], bool):
        raise ValidationError(f"{path}.value: expected boolean")
    if item["missing_reason"] is not None:
        raise ValidationError(f"{path}.missing_reason: populated value requires null")


def _cache_status(value: Any, path: str) -> None:
    item = _mapping(value, path)
    _keys(
        item,
        {"value", "directly_observed", "observation_provenance", "missing_reason"},
        path,
    )
    if not isinstance(item["directly_observed"], bool):
        raise ValidationError(f"{path}.directly_observed: expected boolean")
    if item["value"] is None:
        if item["directly_observed"]:
            raise ValidationError(f"{path}: null cache status cannot be directly observed")
        if item["observation_provenance"] is not None:
            raise ValidationError(f"{path}: missing cache status cannot cite observation provenance")
        _text(item["missing_reason"], f"{path}.missing_reason")
        return
    _enum(item["value"], {"hit", "miss"}, f"{path}.value")
    if not item["directly_observed"]:
        raise ValidationError(f"{path}: cache status must be directly observed")
    _repo_path(item["observation_provenance"], f"{path}.observation_provenance")
    if item["missing_reason"] is not None:
        raise ValidationError(f"{path}.missing_reason: populated value requires null")


def _telemetry(value: Any, path: str) -> None:
    item = _mapping(value, path)
    _keys(
        item,
        {
            "task_duration_budget_seconds",
            "observed_task_duration_seconds",
            "dispatch_batch_id",
            "dispatch_batch_size",
            "execution_mode",
            "foreman_idle_gap_seconds",
            "cache_status",
        },
        path,
    )
    _measure(item["task_duration_budget_seconds"], f"{path}.task_duration_budget_seconds")
    _measure(item["observed_task_duration_seconds"], f"{path}.observed_task_duration_seconds")
    _nullable_text(item["dispatch_batch_id"], f"{path}.dispatch_batch_id")
    _measure(item["dispatch_batch_size"], f"{path}.dispatch_batch_size")
    _nullable_text(item["execution_mode"], f"{path}.execution_mode", EXECUTION_MODES)
    _measure(item["foreman_idle_gap_seconds"], f"{path}.foreman_idle_gap_seconds")
    _cache_status(item["cache_status"], f"{path}.cache_status")


def _participant(value: Any, path: str) -> None:
    item = _mapping(value, path)
    _keys(
        item,
        {"id", "role", "tier", "effort", "tokens", "tool_calls", "wall_seconds"},
        path,
    )
    _text(item["id"], f"{path}.id")
    _enum(item["role"], ROLES, f"{path}.role")
    _enum(item["tier"], TIERS, f"{path}.tier")
    _enum(item["effort"], EFFORTS, f"{path}.effort")
    _measure(item["tokens"], f"{path}.tokens")
    _measure(item["tool_calls"], f"{path}.tool_calls")
    _measure(item["wall_seconds"], f"{path}.wall_seconds")


def _resources(value: Any, path: str) -> None:
    item = _mapping(value, path)
    _keys(item, {"agent_count", "browser_count", "session_count"}, path)
    _measure(item["agent_count"], f"{path}.agent_count")
    _measure(item["browser_count"], f"{path}.browser_count")
    _measure(item["session_count"], f"{path}.session_count")


def _outcome(value: Any, path: str) -> None:
    item = _mapping(value, path)
    _keys(
        item,
        {
            "cases_completed",
            "criteria_completed",
            "seeded_defects_detected",
            "verdict",
            "quality_floor_met",
            "rework_events",
            "recheck_events",
        },
        path,
    )
    _measure(item["cases_completed"], f"{path}.cases_completed")
    _nullable_text_list(item["criteria_completed"], f"{path}.criteria_completed")
    _nullable_text_list(item["seeded_defects_detected"], f"{path}.seeded_defects_detected")
    _nullable_text(
        item["verdict"],
        f"{path}.verdict",
        {"pass", "fail", "error", "inconclusive"},
    )
    _nullable_bool(item["quality_floor_met"], f"{path}.quality_floor_met")
    _measure(item["rework_events"], f"{path}.rework_events")
    _measure(item["recheck_events"], f"{path}.recheck_events")


def _workload(value: Any, path: str) -> str:
    item = _mapping(value, path)
    if item["version"] != WORKLOAD_VERSION:
        raise ValidationError(f"{path}.version: expected {WORKLOAD_VERSION}")
    identifier = _text(item["id"], f"{path}.id")
    if item["subject"] != "presentation-ui-ux":
        raise ValidationError(f"{path}.subject: expected presentation-ui-ux")
    kind = _enum(
        item.get("workload_kind"),
        {"historical-cycle", "frozen-comparison"},
        f"{path}.workload_kind",
    )
    common = {"version", "id", "subject", "workload_kind", "description", "provenance"}
    if kind == "historical-cycle":
        _keys(item, common | {"cycle"}, path)
        _enum(item["cycle"], {"C1", "C2", "C3", "C4", "C5"}, f"{path}.cycle")
    else:
        _keys(
            item,
            common
            | {
                "candidate",
                "fixtures",
                "criteria",
                "seeded_defects",
                "required_outputs",
                "quality_floor",
                "role_boundaries",
                "intervention",
            },
            path,
        )
        candidate = _mapping(item["candidate"], f"{path}.candidate")
        _keys(candidate, {"surface", "paths"}, f"{path}.candidate")
        _text(candidate["surface"], f"{path}.candidate.surface")
        candidate_paths = _sequence(candidate["paths"], f"{path}.candidate.paths")
        if not candidate_paths:
            raise ValidationError(f"{path}.candidate.paths: expected at least one path")
        for index, candidate_path in enumerate(candidate_paths):
            _repo_path(candidate_path, f"{path}.candidate.paths[{index}]")

        fixture_ids: set[str] = set()
        fixtures = _sequence(item["fixtures"], f"{path}.fixtures")
        if not fixtures:
            raise ValidationError(f"{path}.fixtures: expected at least one fixture")
        for index, fixture_value in enumerate(fixtures):
            fixture_path = f"{path}.fixtures[{index}]"
            fixture = _mapping(fixture_value, fixture_path)
            _keys(fixture, {"id", "path", "synthetic"}, fixture_path)
            fixture_id = _text(fixture["id"], f"{fixture_path}.id")
            if fixture_id in fixture_ids:
                raise ValidationError(f"{fixture_path}.id: duplicate {fixture_id}")
            fixture_ids.add(fixture_id)
            _repo_path(fixture["path"], f"{fixture_path}.path")
            if fixture["synthetic"] is not True:
                raise ValidationError(f"{fixture_path}.synthetic: expected true")

        criteria = set(_unique_texts(item["criteria"], f"{path}.criteria"))
        defect_ids: set[str] = set()
        defects = _sequence(item["seeded_defects"], f"{path}.seeded_defects")
        for index, defect_value in enumerate(defects):
            defect_path = f"{path}.seeded_defects[{index}]"
            defect = _mapping(defect_value, defect_path)
            _keys(defect, {"id", "tier", "description"}, defect_path)
            defect_id = _text(defect["id"], f"{defect_path}.id")
            if defect_id in defect_ids:
                raise ValidationError(f"{defect_path}.id: duplicate {defect_id}")
            defect_ids.add(defect_id)
            _enum(defect["tier"], DEFECT_TIERS, f"{defect_path}.tier")
            _text(defect["description"], f"{defect_path}.description")
        if {defect["tier"] for defect in defects} != DEFECT_TIERS:
            raise ValidationError(f"{path}.seeded_defects: expected T1, T2, and T3 cases")

        _unique_texts(item["required_outputs"], f"{path}.required_outputs")
        floor = _mapping(item["quality_floor"], f"{path}.quality_floor")
        _keys(
            floor,
            {"required_criteria", "required_seeded_defects", "accepted_verdicts"},
            f"{path}.quality_floor",
        )
        required_criteria = set(
            _unique_texts(floor["required_criteria"], f"{path}.quality_floor.required_criteria")
        )
        required_defects = set(
            _unique_texts(
                floor["required_seeded_defects"],
                f"{path}.quality_floor.required_seeded_defects",
            )
        )
        if not required_criteria <= criteria:
            raise ValidationError(f"{path}.quality_floor.required_criteria: unknown criterion")
        if not required_defects <= defect_ids:
            raise ValidationError(
                f"{path}.quality_floor.required_seeded_defects: unknown seeded defect"
            )
        _unique_texts(floor["accepted_verdicts"], f"{path}.quality_floor.accepted_verdicts")

        boundaries = _sequence(item["role_boundaries"], f"{path}.role_boundaries")
        boundary_roles: set[str] = set()
        for index, boundary_value in enumerate(boundaries):
            boundary_path = f"{path}.role_boundaries[{index}]"
            boundary = _mapping(boundary_value, boundary_path)
            _keys(
                boundary,
                {"role", "count", "tier", "effort", "responsibility"},
                boundary_path,
            )
            role = _enum(boundary["role"], ROLES, f"{boundary_path}.role")
            if role in boundary_roles:
                raise ValidationError(f"{boundary_path}.role: duplicate {role}")
            boundary_roles.add(role)
            count = _nonnegative_int(boundary["count"], f"{boundary_path}.count")
            if count == 0:
                raise ValidationError(f"{boundary_path}.count: expected positive integer")
            _enum(boundary["tier"], TIERS - {"unrecorded"}, f"{boundary_path}.tier")
            _enum(boundary["effort"], EFFORTS - {"unrecorded"}, f"{boundary_path}.effort")
            _text(boundary["responsibility"], f"{boundary_path}.responsibility")

        intervention = _mapping(item["intervention"], f"{path}.intervention")
        _keys(intervention, {"name", "treatments"}, f"{path}.intervention")
        _text(intervention["name"], f"{path}.intervention.name")
        treatments = _sequence(intervention["treatments"], f"{path}.intervention.treatments")
        labels: set[str] = set()
        for index, treatment_value in enumerate(treatments):
            treatment_path = f"{path}.intervention.treatments[{index}]"
            treatment = _mapping(treatment_value, treatment_path)
            _keys(treatment, {"label", "apparatus", "residual_brief"}, treatment_path)
            label = _text(treatment["label"], f"{treatment_path}.label")
            if label in labels:
                raise ValidationError(f"{treatment_path}.label: duplicate {label}")
            labels.add(label)
            _text(treatment["apparatus"], f"{treatment_path}.apparatus")
            _text(treatment["residual_brief"], f"{treatment_path}.residual_brief")
        if labels != {"manual", "harness-assisted"}:
            raise ValidationError(
                f"{path}.intervention.treatments: expected manual and harness-assisted"
            )
    _text(item["description"], f"{path}.description")
    _repo_path(item["provenance"], f"{path}.provenance")
    return identifier


def _observation(value: Any, path: str) -> tuple[str, str]:
    item = _mapping(value, path)
    _keys(
        item,
        {
            "version",
            "id",
            "supersedes",
            "supersession_reason",
            "workload_id",
            "evidence_class",
            "treatment",
            "participants",
            "resources",
            "outcome",
            "orchestration",
            "causal_claim",
            "provenance",
        },
        path,
    )
    if item["version"] != OBSERVATION_VERSION:
        raise ValidationError(f"{path}.version: expected {OBSERVATION_VERSION}")
    identifier = _text(item["id"], f"{path}.id")
    supersedes = item["supersedes"]
    supersession_reason = item["supersession_reason"]
    if supersedes is None:
        if supersession_reason is not None:
            raise ValidationError(f"{path}.supersession_reason: requires supersedes")
    else:
        _text(supersedes, f"{path}.supersedes")
        _text(supersession_reason, f"{path}.supersession_reason")
        if supersedes == identifier:
            raise ValidationError(f"{path}.supersedes: observation cannot supersede itself")
    workload_id = _text(item["workload_id"], f"{path}.workload_id")
    evidence = _enum(item["evidence_class"], EVIDENCE_CLASSES, f"{path}.evidence_class")
    _text(item["treatment"], f"{path}.treatment")
    if not isinstance(item["causal_claim"], bool):
        raise ValidationError(f"{path}.causal_claim: expected boolean")
    if evidence == "historical-observational" and item["causal_claim"]:
        raise ValidationError(f"{path}: historical observation cannot make a causal claim")
    _repo_path(item["provenance"], f"{path}.provenance")
    _resources(item["resources"], f"{path}.resources")
    _outcome(item["outcome"], f"{path}.outcome")
    _telemetry(item["orchestration"], f"{path}.orchestration")
    participants = _sequence(item["participants"], f"{path}.participants")
    if not participants:
        raise ValidationError(f"{path}.participants: expected at least one participant")
    participant_ids: set[str] = set()
    for index, participant in enumerate(participants):
        participant_path = f"{path}.participants[{index}]"
        _participant(participant, participant_path)
        participant_id = participant["id"]
        if participant_id in participant_ids:
            raise ValidationError(f"{participant_path}.id: duplicate {participant_id}")
        participant_ids.add(participant_id)
    if not any(participant["role"] == "foreman" for participant in participants):
        raise ValidationError(f"{path}.participants: foreman cost must be represented explicitly")
    return identifier, workload_id


def _comparison(
    value: Any,
    path: str,
    workload_ids: set[str],
    observations_by_id: dict[str, dict[str, Any]],
) -> None:
    item = _mapping(value, path)
    _keys(
        item,
        {
            "version",
            "id",
            "workload_id",
            "baseline_label",
            "treatment_label",
            "baseline_observation_ids",
            "treatment_observation_ids",
            "evidence_class",
            "causal_claim",
            "quality",
            "measures",
            "raw_observations",
        },
        path,
    )
    if item["version"] != COMPARISON_VERSION:
        raise ValidationError(f"{path}.version: expected {COMPARISON_VERSION}")
    _text(item["id"], f"{path}.id")
    workload_id = _text(item["workload_id"], f"{path}.workload_id")
    if workload_id not in workload_ids:
        raise ValidationError(f"{path}.workload_id: dangling reference {workload_id}")
    _text(item["baseline_label"], f"{path}.baseline_label")
    _text(item["treatment_label"], f"{path}.treatment_label")
    baseline_ids = _unique_texts(
        item["baseline_observation_ids"], f"{path}.baseline_observation_ids"
    )
    treatment_ids = _unique_texts(
        item["treatment_observation_ids"], f"{path}.treatment_observation_ids"
    )
    if not baseline_ids or not treatment_ids:
        raise ValidationError(f"{path}: both comparison arms require observations")
    observation_ids = set(observations_by_id)
    for identifier in baseline_ids + treatment_ids:
        if identifier not in observation_ids:
            raise ValidationError(f"{path}: dangling observation reference {identifier}")
    _enum(item["evidence_class"], EVIDENCE_CLASSES, f"{path}.evidence_class")
    if item["causal_claim"] is not False:
        raise ValidationError(f"{path}.causal_claim: unsupported causal claim")

    quality = _mapping(item["quality"], f"{path}.quality")
    _keys(
        quality,
        {"comparable", "baseline_met", "treatment_met", "reasons"},
        f"{path}.quality",
    )
    for name in ("comparable", "baseline_met", "treatment_met"):
        if not isinstance(quality[name], bool):
            raise ValidationError(f"{path}.quality.{name}: expected boolean")
    _unique_texts(quality["reasons"], f"{path}.quality.reasons")

    measures = _sequence(item["measures"], f"{path}.measures")
    measure_names: set[str] = set()
    for index, measure_value in enumerate(measures):
        measure_path = f"{path}.measures[{index}]"
        measure = _mapping(measure_value, measure_path)
        _keys(
            measure,
            {
                "name",
                "baseline_value",
                "treatment_value",
                "delta",
                "ratio",
                "verdict",
                "reason",
            },
            measure_path,
        )
        name = _text(measure["name"], f"{measure_path}.name")
        if name in measure_names:
            raise ValidationError(f"{measure_path}.name: duplicate {name}")
        measure_names.add(name)
        for field in ("baseline_value", "treatment_value"):
            raw = measure[field]
            if raw is not None:
                _nonnegative_int(raw, f"{measure_path}.{field}")
        delta = measure["delta"]
        if delta is not None and (isinstance(delta, bool) or not isinstance(delta, int)):
            raise ValidationError(f"{measure_path}.delta: expected integer or null")
        ratio = measure["ratio"]
        if ratio is not None and (
            isinstance(ratio, bool) or not isinstance(ratio, (int, float)) or ratio < 0
        ):
            raise ValidationError(f"{measure_path}.ratio: expected non-negative number or null")
        verdict = _enum(
            measure["verdict"],
            {
                "economically-promising",
                "regression",
                "no-interpretable-difference",
                "insufficient-evidence",
            },
            f"{measure_path}.verdict",
        )
        if verdict == "insufficient-evidence":
            _text(measure["reason"], f"{measure_path}.reason")
        elif measure["reason"] is not None:
            raise ValidationError(f"{measure_path}.reason: interpretable result requires null")

    raw = _sequence(item["raw_observations"], f"{path}.raw_observations")
    raw_ids = []
    raw_evidence_classes: set[str] = set()
    for index, observation in enumerate(raw):
        raw_id, raw_workload = _observation(
            observation, f"{path}.raw_observations[{index}]"
        )
        if raw_workload != workload_id:
            raise ValidationError(f"{path}.raw_observations[{index}]: incompatible workload")
        if observation != observations_by_id.get(raw_id):
            raise ValidationError(
                f"{path}.raw_observations[{index}]: must match referenced observation"
            )
        raw_ids.append(raw_id)
        raw_evidence_classes.add(observation["evidence_class"])
    if raw_ids != baseline_ids + treatment_ids:
        raise ValidationError(f"{path}.raw_observations: must preserve referenced observations")
    if raw_evidence_classes != {item["evidence_class"]}:
        raise ValidationError(f"{path}.evidence_class: must match raw observations")


def validate_dataset(value: Any) -> None:
    """Validate a complete workload/observation collection."""

    dataset = _mapping(value, "$")
    _keys(dataset, {"workloads", "observations", "comparisons"}, "$")
    workloads = _sequence(dataset["workloads"], "$.workloads")
    observations = _sequence(dataset["observations"], "$.observations")
    comparisons = _sequence(dataset["comparisons"], "$.comparisons")
    workload_ids: set[str] = set()
    workloads_by_id: dict[str, dict[str, Any]] = {}
    for index, workload in enumerate(workloads):
        identifier = _workload(workload, f"$.workloads[{index}]")
        if identifier in workload_ids:
            raise ValidationError(f"$.workloads[{index}].id: duplicate {identifier}")
        workload_ids.add(identifier)
        workloads_by_id[identifier] = workload

    observation_ids: set[str] = set()
    observation_workloads: dict[str, str] = {}
    observations_by_id: dict[str, dict[str, Any]] = {}
    for index, observation in enumerate(observations):
        identifier, workload_id = _observation(observation, f"$.observations[{index}]")
        if identifier in observation_ids:
            raise ValidationError(f"$.observations[{index}].id: duplicate {identifier}")
        if workload_id not in workload_ids:
            raise ValidationError(
                f"$.observations[{index}].workload_id: dangling reference {workload_id}"
            )
        observation_ids.add(identifier)
        observation_workloads[identifier] = workload_id
        observations_by_id[identifier] = observation
        workload = workloads_by_id[workload_id]
        if workload["workload_kind"] == "frozen-comparison":
            outcome = observation["outcome"]
            criteria_value = outcome["criteria_completed"]["value"]
            defects_value = outcome["seeded_defects_detected"]["value"]
            if criteria_value is not None and not set(criteria_value) <= set(workload["criteria"]):
                raise ValidationError(
                    f"$.observations[{index}].outcome.criteria_completed: unknown criterion"
                )
            known_defects = {defect["id"] for defect in workload["seeded_defects"]}
            if defects_value is not None and not set(defects_value) <= known_defects:
                raise ValidationError(
                    f"$.observations[{index}].outcome.seeded_defects_detected: "
                    "unknown seeded defect"
                )
            if outcome["quality_floor_met"]["value"] is True:
                required_criteria = set(workload["quality_floor"]["required_criteria"])
                required_defects = set(workload["quality_floor"]["required_seeded_defects"])
                accepted_verdicts = set(workload["quality_floor"]["accepted_verdicts"])
                if criteria_value is None or not required_criteria <= set(criteria_value):
                    raise ValidationError(
                        f"$.observations[{index}].outcome.quality_floor_met: "
                        "required criteria incomplete"
                    )
                if defects_value is None or not required_defects <= set(defects_value):
                    raise ValidationError(
                        f"$.observations[{index}].outcome.quality_floor_met: "
                        "required seeded defects missed"
                    )
                if outcome["verdict"]["value"] not in accepted_verdicts:
                    raise ValidationError(
                        f"$.observations[{index}].outcome.quality_floor_met: "
                        "verdict does not meet floor"
                    )
    for index, observation in enumerate(observations):
        supersedes = observation["supersedes"]
        if supersedes is None:
            continue
        if supersedes not in observation_ids:
            raise ValidationError(
                f"$.observations[{index}].supersedes: dangling reference {supersedes}"
            )
        if observation_workloads[supersedes] != observation["workload_id"]:
            raise ValidationError(
                f"$.observations[{index}].supersedes: workload must match superseded observation"
            )
    comparison_ids: set[str] = set()
    for index, comparison in enumerate(comparisons):
        _comparison(
            comparison,
            f"$.comparisons[{index}]",
            workload_ids,
            observations_by_id,
        )
        comparison_id = comparison["id"]
        if comparison_id in comparison_ids:
            raise ValidationError(f"$.comparisons[{index}].id: duplicate {comparison_id}")
        comparison_ids.add(comparison_id)


def load_dataset(path: str | Path) -> dict[str, Any]:
    """Load and validate a JSON dataset."""

    with Path(path).open(encoding="utf-8") as handle:
        value: Any = json.load(handle)
    validate_dataset(value)
    return _mapping(value, "$")


def validate_workload(value: Any) -> None:
    """Validate one strict presentation-economy workload document."""

    _workload(value, "$")


def load_workload(path: str | Path) -> dict[str, Any]:
    """Load and validate one workload JSON document."""

    with Path(path).open(encoding="utf-8") as handle:
        value: Any = json.load(handle)
    validate_workload(value)
    return _mapping(value, "$")
