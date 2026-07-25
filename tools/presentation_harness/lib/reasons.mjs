// Closed reason-code vocabularies for the presentation harness. Every code
// emitted anywhere in a manifest-validation error, a report case, or an
// infrastructure abort must come from one of these sets; nothing else is
// ever produced.

export const MANIFEST_REASONS = Object.freeze(new Set([
  "manifest-unknown-key",
  "manifest-missing-key",
  "manifest-invalid-version",
  "manifest-invalid-type",
  "manifest-duplicate-id",
  "manifest-unknown-candidate-reference",
  "manifest-unknown-fixture-reference",
  "manifest-unknown-criterion-reference",
  "manifest-unknown-tamper-reference",
  "manifest-unknown-check",
  "manifest-remote-url-rejected",
  "manifest-absolute-path-rejected",
  "manifest-path-traversal-rejected",
  "manifest-non-synthetic-fixture-rejected",
  "manifest-invalid-injection",
  "manifest-empty-selection",
  "manifest-empty-matrix-criteria",
  "manifest-empty-matrix",
  "manifest-duplicate-matrix-case",
]));

// Case-level outcomes for one criterion evaluated against one
// candidate/fixture/tamper-case tuple.
export const CASE_FAIL_REASONS = Object.freeze(new Set([
  "criterion-unmet",
]));

export const CASE_ERROR_REASONS = Object.freeze(new Set([
  "target-creation-failed",
  "target-load-timeout",
  "target-load-failed",
  "criterion-timeout",
  "criterion-thrown",
  "injection-failed",
  "non-loopback-request-blocked",
  "browser-exit",
]));

// Whole-run infrastructure failures. These abort before (or independent of)
// any trustworthy criterion result and always exit 2.
export const INFRA_REASONS = Object.freeze(new Set([
  "manifest-not-found",
  "manifest-invalid",
  "chrome-not-found",
  "chrome-launch-failed",
  "server-start-failed",
  "browser-exit",
  "internal-error",
]));

const SAFE_INFRA_MESSAGES = Object.freeze({
  "manifest-not-found": "manifest unavailable",
  "manifest-invalid": "manifest rejected",
  "chrome-not-found": "Chrome unavailable",
  "chrome-launch-failed": "Chrome launch failed",
  "server-start-failed": "loopback server failed",
  "browser-exit": "browser exited unexpectedly",
  "internal-error": "internal harness failure",
});

export function safeInfraMessage(reasonCode) {
  return SAFE_INFRA_MESSAGES[reasonCode] || "harness infrastructure failure";
}

export class ManifestError extends Error {
  constructor(reasonCode, message) {
    if (!MANIFEST_REASONS.has(reasonCode)) {
      throw new Error(`unknown manifest reason code: ${reasonCode}`);
    }
    super(message);
    this.name = "ManifestError";
    this.reasonCode = reasonCode;
  }
}

export class InfraError extends Error {
  constructor(reasonCode, message) {
    if (!INFRA_REASONS.has(reasonCode)) {
      throw new Error(`unknown infra reason code: ${reasonCode}`);
    }
    super(message);
    this.name = "InfraError";
    this.reasonCode = reasonCode;
  }
}
