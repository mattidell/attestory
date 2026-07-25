import test from "node:test";
import assert from "node:assert/strict";
import {
  ManifestError,
  InfraError,
  MANIFEST_REASONS,
  CASE_FAIL_REASONS,
  CASE_ERROR_REASONS,
  INFRA_REASONS,
  safeInfraMessage,
} from "../lib/reasons.mjs";

test("ManifestError rejects a reason code outside the closed vocabulary", () => {
  assert.throws(() => new ManifestError("not-a-real-reason", "boom"));
});

test("InfraError rejects a reason code outside the closed vocabulary", () => {
  assert.throws(() => new InfraError("not-a-real-reason", "boom"));
});

test("each reason-code vocabulary has no internal duplicates", () => {
  for (const set of [MANIFEST_REASONS, CASE_FAIL_REASONS, CASE_ERROR_REASONS, INFRA_REASONS]) {
    const values = [...set];
    assert.equal(new Set(values).size, values.length);
  }
});

test("manifest reasons never overlap with case-level reasons", () => {
  const caseReasons = new Set([...CASE_FAIL_REASONS, ...CASE_ERROR_REASONS]);
  for (const code of MANIFEST_REASONS) {
    assert.ok(!caseReasons.has(code), `${code} should not double as a case-level reason`);
  }
});

test("every declared reason code constructs successfully", () => {
  for (const code of MANIFEST_REASONS) {
    assert.equal(new ManifestError(code, "x").reasonCode, code);
  }
  for (const code of INFRA_REASONS) {
    assert.equal(new InfraError(code, "x").reasonCode, code);
  }
});

test("infrastructure messages are fixed and do not echo error details", () => {
  const message = safeInfraMessage("manifest-invalid");
  assert.equal(message, "manifest rejected");
  assert.equal(safeInfraMessage("internal-error"), "internal harness failure");
});
