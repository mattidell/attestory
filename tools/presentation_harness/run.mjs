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

import { readFile, writeFile, realpath } from "node:fs/promises";
import { isAbsolute, relative, resolve, sep } from "node:path";
import { validateManifest } from "./lib/manifest.mjs";
import { startLoopbackServer } from "./lib/server.mjs";
import { launchChrome } from "./lib/chrome.mjs";
import { runMatrix } from "./lib/executor.mjs";
import { buildReport, serializeReport, exitCodeForReport } from "./lib/report.mjs";
import { buildObservation } from "./lib/observation.mjs";
import { InfraError, ManifestError, safeInfraMessage } from "./lib/reasons.mjs";

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
    `${JSON.stringify({ error: true, reason: error.reasonCode, message: safeInfraMessage(error.reasonCode) }, null, 2)}\n`,
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
  const repoRoot = await realpath(process.cwd());
  const startedAt = Date.now();

  if (typeof args.manifest !== "string" || args.manifest.trim() === "") {
    throw new InfraError("manifest-invalid", "manifest argument is required");
  }

  if (isAbsolute(args.manifest) || /^[a-zA-Z]:[\\/]/.test(args.manifest) || /^(?:[a-zA-Z][a-zA-Z0-9+.-]*:\/\/|\\\\)/.test(args.manifest)) {
    throw new InfraError("manifest-invalid", "manifest must be repository-relative");
  }
  const lexicalSegments = args.manifest.split(/[\\/]+/);
  if (lexicalSegments.some((segment) => segment === "..")) {
    throw new InfraError("manifest-invalid", "manifest traversal rejected");
  }
  const lexicalName = lexicalSegments.filter((segment) => segment !== "." && segment !== "").join("/");
  if (!lexicalName) throw new InfraError("manifest-invalid", "manifest path is empty");

  let manifestPath;
  let manifestName;
  try {
    manifestPath = await realpath(resolve(repoRoot, lexicalName));
    const repoRelative = relative(repoRoot, manifestPath);
    if (repoRelative === "" || repoRelative === ".." || repoRelative.startsWith(`..${sep}`) || isAbsolute(repoRelative)) {
      throw new Error("manifest escapes repository");
    }
    manifestName = repoRelative.split(sep).join("/");
  } catch (error) {
    if (error instanceof InfraError) throw error;
    if (error?.code === "ENOENT" || error?.code === "ENOTDIR") {
      throw new InfraError("manifest-not-found", "manifest could not be resolved");
    }
    throw new InfraError("manifest-invalid", "manifest path is outside the repository");
  }

  let manifestRaw;
  try {
    manifestRaw = await readFile(manifestPath, "utf8");
  } catch {
    throw new InfraError("manifest-not-found", "manifest could not be read");
  }

  let manifestJson;
  try {
    manifestJson = JSON.parse(manifestRaw);
  } catch {
    throw new InfraError("manifest-invalid", "manifest JSON is invalid");
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
  let launchCleanup;
  let cleanedUp = false;
  const cleanup = async () => {
    if (cleanedUp) return;
    cleanedUp = true;
    if (chromeHandle) await chromeHandle.dispose();
    else if (launchCleanup) await launchCleanup();
    if (server) await server.close();
  };

  const onSignal = () => {
    cleanup().finally(() => process.exit(2));
  };
  process.once("SIGINT", onSignal);
  process.once("SIGTERM", onSignal);

  try {
    server = await startLoopbackServer(repoRoot, allowedPaths);
    chromeHandle = await launchChrome(args.chrome, {
      onOwnership(dispose) {
        launchCleanup = dispose;
      },
    });

    const results = await runMatrix(chromeHandle, manifest, server.origin);
    const report = buildReport(manifestName, manifest, results);

    const wallSeconds = Math.max(0, Math.round((Date.now() - startedAt) / 1000));
    const criteriaCompleted = [...new Set(results.map((result) => result.criterionId))].sort();
    const observation = buildObservation({
      id: `harness-run-${manifest.id}-${startedAt}`,
      manifestId: manifest.id,
      manifestProvenancePath: manifestName,
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
