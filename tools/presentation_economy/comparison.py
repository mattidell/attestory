"""Quality-gated, deterministic presentation economy comparisons."""

from __future__ import annotations

from typing import Any, Callable

from .validation import ValidationError, validate_dataset, validate_workload


COMPARISON_VERSION = "presentation-economy-comparison.v1"


def _measure_value(record: dict[str, Any], path: tuple[str, ...]) -> int | None:
    value: Any = record
    for part in path:
        value = value[part]
    result = value["value"]
    return result if isinstance(result, int) and not isinstance(result, bool) else None


def _participant_total(observation: dict[str, Any], name: str) -> int | None:
    total = 0
    for participant in observation["participants"]:
        value = participant[name]["value"]
        if isinstance(value, bool) or not isinstance(value, int):
            return None
        total += value
    return total


def _aggregate(
    observations: list[dict[str, Any]],
    extractor: Callable[[dict[str, Any]], int | None],
) -> int | None:
    values = [extractor(observation) for observation in observations]
    if any(value is None for value in values):
        return None
    return sum(value for value in values if value is not None)


def _quality_reasons(
    workload: dict[str, Any], observations: list[dict[str, Any]], arm: str
) -> list[str]:
    floor = workload["quality_floor"]
    required_criteria = set(floor["required_criteria"])
    required_defects = set(floor["required_seeded_defects"])
    accepted_verdicts = set(floor["accepted_verdicts"])
    reasons: list[str] = []
    for observation in observations:
        outcome = observation["outcome"]
        criteria = outcome["criteria_completed"]["value"]
        defects = outcome["seeded_defects_detected"]["value"]
        verdict = outcome["verdict"]["value"]
        if criteria is None or not required_criteria <= set(criteria):
            reasons.append(f"{arm}:{observation['id']}:required criteria incomplete")
        if defects is None or not required_defects <= set(defects):
            reasons.append(f"{arm}:{observation['id']}:required seeded defects missed")
        if verdict not in accepted_verdicts:
            reasons.append(f"{arm}:{observation['id']}:verdict does not meet quality floor")
        if outcome["quality_floor_met"]["value"] is not True:
            reasons.append(f"{arm}:{observation['id']}:quality floor not affirmed")
    return reasons


def build_comparison(
    workload: dict[str, Any],
    observations: list[dict[str, Any]],
    baseline_label: str,
    treatment_label: str,
) -> dict[str, Any]:
    """Build one strict comparison without making a causal claim."""

    validate_workload(workload)
    if workload["workload_kind"] != "frozen-comparison":
        raise ValidationError("comparison requires a frozen-comparison workload")
    validate_dataset(
        {"workloads": [workload], "observations": observations, "comparisons": []}
    )
    baseline = [item for item in observations if item["treatment"] == baseline_label]
    treatment = [item for item in observations if item["treatment"] == treatment_label]
    if not baseline or not treatment:
        raise ValidationError("comparison requires observations for both labels")
    selected = baseline + treatment
    evidence_classes = {item["evidence_class"] for item in selected}
    if len(evidence_classes) != 1:
        raise ValidationError("selected observations must share one evidence class")
    evidence_class = next(iter(evidence_classes))

    quality_reasons = _quality_reasons(workload, baseline, "baseline")
    quality_reasons.extend(_quality_reasons(workload, treatment, "treatment"))
    quality_comparable = not quality_reasons

    extractors: list[tuple[str, Callable[[dict[str, Any]], int | None]]] = [
        ("tokens", lambda item: _participant_total(item, "tokens")),
        ("tool_calls", lambda item: _participant_total(item, "tool_calls")),
        ("wall_seconds", lambda item: _participant_total(item, "wall_seconds")),
        ("agent_count", lambda item: _measure_value(item, ("resources", "agent_count"))),
        ("browser_count", lambda item: _measure_value(item, ("resources", "browser_count"))),
        ("session_count", lambda item: _measure_value(item, ("resources", "session_count"))),
        ("rework_events", lambda item: _measure_value(item, ("outcome", "rework_events"))),
        ("recheck_events", lambda item: _measure_value(item, ("outcome", "recheck_events"))),
        (
            "task_duration_budget_seconds",
            lambda item: _measure_value(
                item, ("orchestration", "task_duration_budget_seconds")
            ),
        ),
        (
            "observed_task_duration_seconds",
            lambda item: _measure_value(
                item, ("orchestration", "observed_task_duration_seconds")
            ),
        ),
        (
            "dispatch_batch_size",
            lambda item: _measure_value(item, ("orchestration", "dispatch_batch_size")),
        ),
        (
            "foreman_idle_gap_seconds",
            lambda item: _measure_value(
                item, ("orchestration", "foreman_idle_gap_seconds")
            ),
        ),
    ]
    measures: list[dict[str, Any]] = []
    for name, extractor in extractors:
        baseline_value = _aggregate(baseline, extractor)
        treatment_value = _aggregate(treatment, extractor)
        reason: str | None = None
        delta: int | None = None
        ratio: float | None = None
        if not quality_comparable:
            verdict = "insufficient-evidence"
            reason = "quality floor failed before cost interpretation"
        elif baseline_value is None or treatment_value is None:
            verdict = "insufficient-evidence"
            reason = "one or more participating-role or observation values are missing"
        else:
            delta = treatment_value - baseline_value
            ratio = None if baseline_value == 0 else treatment_value / baseline_value
            if delta < 0:
                verdict = "economically-promising"
            elif delta > 0:
                verdict = "regression"
            else:
                verdict = "no-interpretable-difference"
        measures.append(
            {
                "name": name,
                "baseline_value": baseline_value,
                "treatment_value": treatment_value,
                "delta": delta,
                "ratio": ratio,
                "verdict": verdict,
                "reason": reason,
            }
        )

    return {
        "version": COMPARISON_VERSION,
        "id": f"demo-comparison-{workload['id']}-{baseline_label}-{treatment_label}",
        "workload_id": workload["id"],
        "baseline_label": baseline_label,
        "treatment_label": treatment_label,
        "baseline_observation_ids": [item["id"] for item in baseline],
        "treatment_observation_ids": [item["id"] for item in treatment],
        "evidence_class": evidence_class,
        "causal_claim": False,
        "quality": {
            "comparable": quality_comparable,
            "baseline_met": not _quality_reasons(workload, baseline, "baseline"),
            "treatment_met": not _quality_reasons(workload, treatment, "treatment"),
            "reasons": quality_reasons,
        },
        "measures": measures,
        "raw_observations": selected,
    }
