// Deterministic presentation-evaluation-report.v1 construction and
// serialization. No ephemeral data (ports, timestamps, pids, absolute
// paths, browser versions, page content) ever enters this shape.

export const REPORT_VERSION = "presentation-evaluation-report.v1";

export function buildReport(manifestName, manifest, results) {
  const counts = { pass: 0, fail: 0, error: 0 };
  for (const result of results) {
    counts[result.outcome] += 1;
  }
  const passed = counts.fail === 0 && counts.error === 0;
  return {
    version: REPORT_VERSION,
    manifest_version: manifest.version,
    manifest_name: manifestName,
    cases: results.map((result) => ({
      candidate_id: result.candidateId,
      fixture_id: result.fixtureId,
      tamper_case_id: result.tamperCaseId,
      criterion_id: result.criterionId,
      outcome: result.outcome,
      reason: result.reason,
    })),
    counts: {
      pass: counts.pass,
      fail: counts.fail,
      error: counts.error,
      total: results.length,
    },
    passed,
  };
}

export function serializeReport(report) {
  return `${JSON.stringify(report, null, 2)}\n`;
}

/** 0 all-pass, 1 completed with a failure, 2 any untrustworthy case. */
export function exitCodeForReport(report) {
  if (report.counts.error > 0) return 2;
  if (report.counts.fail > 0) return 1;
  return 0;
}
