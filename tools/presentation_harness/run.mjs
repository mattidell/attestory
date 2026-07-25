#!/usr/bin/env node
// Presentation-evaluation harness command. See
// docs/presentation-economy/README.md for the full contract.
//
//   node tools/presentation_harness/run.mjs --manifest <repo-relative-path> \
//     [--chrome <path>] [--observation-out <path>]
//
// Exit status: 0 all criteria passed; 1 completed with a criterion failure;
// 2 the run could not produce trustworthy results (manifest, target,
// browser, server, load, injection, or internal failure).

import { readFile, writeFile } from "node:fs/promises";
import { join, isAbsolute } from "node:path";
import { validateManifest } from "./lib/manifest.mjs";
import { startLoopbackServer } from "./lib/server.mjs";
import { launchChrome } from "./lib/chrome.mjs";
import { runMatrix } from "./lib/executor.mjs";
import { buildReport, serializeReport, exitCodeForReport } from "./lib/report.mjs";
import { buildObservation } from "./lib/observation.mjs";
import { InfraError, ManifestError } from "./lib/reasons.mjs";

function parseArgs(argv) {
  const args = { manifest: null, chrome: null, observationOut: null };
  for (let i = 0; i < argv.length; i += 1) {
    const arg = argv[i];
    if (arg === "--manifest") {
      args.manifest = argv[(i += 1)];
    } else if (arg === "--chrome") {
      args.chrome = argv[(i += 1)];
    } else if (arg === "--observation-out") {
      args.observationOut = argv[(i += 1)];
    } else {
      throw new InfraError("manifest-invalid", `unrecognized argument: ${arg}`);
    }
  }
  if (!args.manifest) {
    throw new InfraError("manifest-invalid", "--manifest <repo-relative-path> is required");
  }
  return args;
}

function writeInfraError(error) {
  process.stderr.write(
    `${JSON.stringify({ error: true, reason: error.reasonCode, message: error.message }, null, 2)}\n`,
  );
}

function humanSummary(report) {
  return (
    `presentation-harness: ${report.counts.total} case(s) — ` +
    `${report.counts.pass} pass, ${report.counts.fail} fail, ${report.counts.error} error\n`
  );
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  const repoRoot = process.cwd();
  const startedAt = Date.now();

  if (isAbsolute(args.manifest)) {
    throw new InfraError("manifest-invalid", "--manifest must be a repository-relative path");
  }

  let manifestRaw;
  try {
    manifestRaw = await readFile(join(repoRoot, args.manifest), "utf8");
  } catch (error) {
    throw new InfraError("manifest-not-found", `cannot read manifest ${args.manifest}: ${error.message}`);
  }

  let manifestJson;
  try {
    manifestJson = JSON.parse(manifestRaw);
  } catch (error) {
    throw new InfraError("manifest-invalid", `manifest is not valid JSON: ${error.message}`);
  }

  let manifest;
  try {
    manifest = validateManifest(manifestJson);
  } catch (error) {
    if (error instanceof ManifestError) {
      throw new InfraError("manifest-invalid", `${error.reasonCode}: ${error.message}`);
    }
    throw error;
  }

  const allowedPaths = new Set();
  for (const candidate of manifest.candidatesById.values()) allowedPaths.add(candidate.path);
  for (const fixture of manifest.fixturesById.values()) allowedPaths.add(fixture.path);

  let server;
  let chromeHandle;
  let cleanedUp = false;
  const cleanup = async () => {
    if (cleanedUp) return;
    cleanedUp = true;
    if (chromeHandle) await chromeHandle.dispose();
    if (server) await server.close();
  };

  const onSignal = () => {
    cleanup().finally(() => process.exit(2));
  };
  process.once("SIGINT", onSignal);
  process.once("SIGTERM", onSignal);

  try {
    server = await startLoopbackServer(repoRoot, allowedPaths);
    chromeHandle = await launchChrome(args.chrome);

    const results = await runMatrix(chromeHandle, manifest, server.origin);
    const report = buildReport(args.manifest, manifest, results);

    const wallSeconds = Math.max(0, Math.round((Date.now() - startedAt) / 1000));
    const criteriaCompleted = [...new Set(results.map((result) => result.criterionId))].sort();
    const observation = buildObservation({
      id: `harness-run-${manifest.id}-${startedAt}`,
      manifestId: manifest.id,
      manifestProvenancePath: args.manifest,
      wallSeconds,
      sessionCount: manifest.matrixEntries.length,
      casesCompleted: results.length,
      criteriaCompleted,
      verdict: report.counts.error > 0 ? "error" : report.passed ? "pass" : "fail",
    });

    process.stdout.write(serializeReport(report));
    process.stderr.write(humanSummary(report));
    process.stderr.write(`${JSON.stringify(observation, null, 2)}\n`);
    if (args.observationOut) {
      await writeFile(args.observationOut, `${JSON.stringify(observation, null, 2)}\n`, "utf8");
    }

    process.exitCode = exitCodeForReport(report);
  } finally {
    process.removeListener("SIGINT", onSignal);
    process.removeListener("SIGTERM", onSignal);
    await cleanup();
  }
}

main().catch((error) => {
  if (error instanceof InfraError) {
    writeInfraError(error);
    process.exitCode = 2;
    return;
  }
  writeInfraError(new InfraError("internal-error", error.stack || String(error)));
  process.exitCode = 2;
});
