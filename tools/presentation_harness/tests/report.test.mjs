import test from "node:test";
import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";
import { validateManifest } from "../lib/manifest.mjs";
import { buildReport, serializeReport, exitCodeForReport } from "../lib/report.mjs";

const here = dirname(fileURLToPath(import.meta.url));

async function loadManifest() {
  const raw = await readFile(join(here, "..", "examples", "manifests", "smoke.v1.json"), "utf8");
  return validateManifest(JSON.parse(raw));
}

test("report ordering follows manifest matrix order with criterion id as tie-breaker", async () => {
  const manifest = await loadManifest();
  const results = manifest.cases.map((c) => ({
    candidateId: c.candidateId,
    fixtureId: c.fixtureId,
    tamperCaseId: c.tamperCaseId,
    criterionId: c.criterionId,
    outcome: "pass",
    reason: null,
  }));
  const report = buildReport("tools/presentation_harness/examples/manifests/smoke.v1.json", manifest, results);
  const criteriaInBaselineTuple = report.cases
    .filter((c) => c.tamper_case_id === "baseline")
    .map((c) => c.criterion_id);
  const sorted = [...criteriaInBaselineTuple].sort();
  assert.deepEqual(criteriaInBaselineTuple, sorted);
});

test("serialized report is byte-identical for repeated calls on the same input", async () => {
  const manifest = await loadManifest();
  const results = manifest.cases.map((c) => ({
    candidateId: c.candidateId,
    fixtureId: c.fixtureId,
    tamperCaseId: c.tamperCaseId,
    criterionId: c.criterionId,
    outcome: "pass",
    reason: null,
  }));
  const reportA = buildReport("m.json", manifest, results);
  const reportB = buildReport("m.json", manifest, results);
  assert.equal(serializeReport(reportA), serializeReport(reportB));
});

test("exit code mapping: any error outcome forces 2 regardless of fail count", () => {
  assert.equal(exitCodeForReport({ counts: { pass: 5, fail: 0, error: 0 } }), 0);
  assert.equal(exitCodeForReport({ counts: { pass: 3, fail: 2, error: 0 } }), 1);
  assert.equal(exitCodeForReport({ counts: { pass: 3, fail: 0, error: 1 } }), 2);
  assert.equal(exitCodeForReport({ counts: { pass: 0, fail: 5, error: 1 } }), 2);
});

test("counts and passed reconcile with the case list", async () => {
  const manifest = await loadManifest();
  const results = manifest.cases.map((c, index) => ({
    candidateId: c.candidateId,
    fixtureId: c.fixtureId,
    tamperCaseId: c.tamperCaseId,
    criterionId: c.criterionId,
    outcome: index === 0 ? "fail" : "pass",
    reason: index === 0 ? "criterion-unmet" : null,
  }));
  const report = buildReport("m.json", manifest, results);
  assert.equal(report.counts.total, results.length);
  assert.equal(report.counts.fail, 1);
  assert.equal(report.counts.pass, results.length - 1);
  assert.equal(report.passed, false);
});
