import test from "node:test";
import assert from "node:assert/strict";
import { buildObservation, OBSERVATION_VERSION } from "../lib/observation.mjs";

function sampleRun(overrides = {}) {
  return {
    id: "harness-run-demo-1",
    manifestId: "demo-smoke",
    manifestProvenancePath: "tools/presentation_harness/examples/manifests/smoke.v1.json",
    wallSeconds: 4,
    sessionCount: 3,
    casesCompleted: 6,
    criteriaCompleted: ["a", "b"],
    verdict: "pass",
    ...overrides,
  };
}

function assertMeasureShape(measure) {
  assert.ok(typeof measure === "object" && measure !== null);
  assert.deepEqual(
    new Set(Object.keys(measure)),
    new Set(["value", "approximate", "measurement_basis", "missing_reason"]),
  );
  if (measure.value === null) {
    assert.equal(measure.measurement_basis, "missing");
    assert.equal(measure.approximate, false);
    assert.ok(typeof measure.missing_reason === "string" && measure.missing_reason.length > 0);
  } else {
    assert.ok(Number.isInteger(measure.value) && measure.value >= 0);
    assert.notEqual(measure.measurement_basis, "missing");
    assert.equal(measure.missing_reason, null);
  }
}

test("observation carries the exact top-level keys the Track 0 validator requires", () => {
  const observation = buildObservation(sampleRun());
  assert.equal(observation.version, OBSERVATION_VERSION);
  assert.deepEqual(
    new Set(Object.keys(observation)),
    new Set([
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
    ]),
  );
});

test("a foreman participant is always present with explicitly missing measures", () => {
  const observation = buildObservation(sampleRun());
  const foreman = observation.participants.find((p) => p.role === "foreman");
  assert.ok(foreman, "observation must include a foreman participant");
  for (const key of ["tokens", "tool_calls", "wall_seconds"]) {
    assertMeasureShape(foreman[key]);
    assert.equal(foreman[key].value, null);
  }
});

test("the harness participant carries directly measured, non-approximate values", () => {
  const observation = buildObservation(sampleRun({ wallSeconds: 12, sessionCount: 5 }));
  const harness = observation.participants.find((p) => p.role === "harness");
  assert.ok(harness);
  assertMeasureShape(harness.tokens);
  assertMeasureShape(harness.tool_calls);
  assertMeasureShape(harness.wall_seconds);
  assert.equal(harness.wall_seconds.value, 12);
  assert.equal(harness.wall_seconds.measurement_basis, "direct");
  assert.equal(harness.tool_calls.value, 5);
});

test("cache status is never inferred: it is missing with directly_observed false", () => {
  const observation = buildObservation(sampleRun());
  const cache = observation.orchestration.cache_status;
  assert.equal(cache.value, null);
  assert.equal(cache.directly_observed, false);
  assert.equal(cache.observation_provenance, null);
  assert.ok(cache.missing_reason.length > 0);
});

test("causal_claim is always false for a harness self-run", () => {
  const observation = buildObservation(sampleRun());
  assert.equal(observation.causal_claim, false);
});

test("resources and outcome measures are structurally well-formed", () => {
  const observation = buildObservation(sampleRun());
  assertMeasureShape(observation.resources.agent_count);
  assertMeasureShape(observation.resources.browser_count);
  assertMeasureShape(observation.resources.session_count);
  assertMeasureShape(observation.outcome.cases_completed);
  assertMeasureShape(observation.outcome.rework_events);
  assertMeasureShape(observation.outcome.recheck_events);
  assert.deepEqual(observation.outcome.criteria_completed, { value: ["a", "b"], missing_reason: null });
});
