// Builds one presentation-economy-observation.v1 fragment for a harness
// run, structurally matching tools/presentation_economy/validation.py's
// `_observation` rules. This fragment is a diagnostic run artifact: it is
// never committed by the harness itself, and every agent-level cost the
// harness process cannot observe (its own dispatcher/foreman) stays
// explicitly missing rather than estimated.

export const OBSERVATION_VERSION = "presentation-economy-observation.v1";

function directMeasure(value) {
  return { value, approximate: false, measurement_basis: "direct", missing_reason: null };
}

function missingMeasure(reason) {
  return { value: null, approximate: false, measurement_basis: "missing", missing_reason: reason };
}

function populatedText(value) {
  return { value, missing_reason: null };
}

function missingText(reason) {
  return { value: null, missing_reason: reason };
}

function missingCacheStatus(reason) {
  return { value: null, directly_observed: false, observation_provenance: null, missing_reason: reason };
}

const FOREMAN_UNMEASURED_REASON =
  "The harness process cannot observe orchestration-level foreman cost for its own invocation.";

/**
 * @param {object} run
 * @param {string} run.manifestId
 * @param {string} run.manifestProvenancePath repo-relative path to the manifest
 * @param {number} run.wallSeconds observed harness wall-clock duration
 * @param {number} run.sessionCount fresh CDP sessions (targets) created
 * @param {number} run.casesCompleted total per-criterion cases attempted
 * @param {string[]} run.criteriaCompleted unique criterion ids executed
 * @param {"pass"|"fail"|"error"} run.verdict
 * @param {string} run.id observation id
 */
export function buildObservation(run) {
  return {
    version: OBSERVATION_VERSION,
    id: run.id,
    supersedes: null,
    supersession_reason: null,
    workload_id: `harness-manifest:${run.manifestId}`,
    evidence_class: "repeated",
    treatment: "harness-run",
    participants: [
      {
        id: "presentation-harness",
        role: "harness",
        tier: "Economy",
        effort: "low",
        tokens: directMeasure(0),
        tool_calls: directMeasure(run.sessionCount),
        wall_seconds: directMeasure(run.wallSeconds),
      },
      {
        id: "foreman-unmeasured",
        role: "foreman",
        tier: "unrecorded",
        effort: "unrecorded",
        tokens: missingMeasure(FOREMAN_UNMEASURED_REASON),
        tool_calls: missingMeasure(FOREMAN_UNMEASURED_REASON),
        wall_seconds: missingMeasure(FOREMAN_UNMEASURED_REASON),
      },
    ],
    resources: {
      agent_count: directMeasure(1),
      browser_count: directMeasure(1),
      session_count: directMeasure(run.sessionCount),
    },
    outcome: {
      cases_completed: directMeasure(run.casesCompleted),
      criteria_completed: populatedText(run.criteriaCompleted),
      seeded_defects_detected: { value: [], missing_reason: null },
      verdict: populatedText(run.verdict),
      quality_floor_met: missingText(
        "No frozen presentation-economy workload quality floor is declared for this harness self-run.",
      ),
      rework_events: directMeasure(0),
      recheck_events: directMeasure(0),
    },
    orchestration: {
      task_duration_budget_seconds: missingMeasure(
        "No task-duration budget is declared for a direct harness invocation.",
      ),
      observed_task_duration_seconds: directMeasure(run.wallSeconds),
      dispatch_batch_id: populatedText(run.manifestId),
      dispatch_batch_size: directMeasure(1),
      execution_mode: populatedText("sequential"),
      foreman_idle_gap_seconds: missingMeasure(
        "Foreman idle gap is not observable from the harness process.",
      ),
      cache_status: missingCacheStatus("The harness process does not expose cache status."),
    },
    causal_claim: false,
    provenance: run.manifestProvenancePath,
  };
}
