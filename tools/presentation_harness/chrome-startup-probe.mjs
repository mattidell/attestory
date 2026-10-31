// Bounded same-runner startup samples. This never retries an application test.
import { execFile } from "node:child_process";
import { appendFile } from "node:fs/promises";
import { availableParallelism, platform } from "node:os";
import { promisify } from "node:util";
import { launchChrome, resolveChromeExecutable } from "./lib/chrome.mjs";
import { createObservation } from "./lib/chrome-observation.mjs";

const output = process.argv[2];
if (!output) throw new Error("diagnostic output required");
const deadline = performance.now() + 165000;
const active = new Set();
const timer = setTimeout(() => { for (const dispose of active) void dispose(); }, 165000);
async function sample(label) {
  if (performance.now() >= deadline) return;
  let owned;
  try {
    const chrome = await launchChrome(null, {
      observer: createObservation({ label, output }),
      onOwnership(dispose) { owned = dispose; active.add(dispose); },
    });
    await chrome.dispose();
  } catch { /* the observer records the bounded result */ }
  finally { if (owned) active.delete(owned); }
}
try {
  for (let i = 0; i < 3; i++) await sample("isolated");
  for (let i = 0; i < 2; i++) await Promise.all([sample("parallel"), sample("parallel")]);
  // Version is measured after startup samples; raw command output is discarded.
  let browserVersion = null;
  try {
    const binary = await resolveChromeExecutable(null);
    const { stdout } = await promisify(execFile)(binary, ["--version"], { timeout: 2000, maxBuffer: 4096 });
    const match = stdout.match(/^(?:Google Chrome|Chromium|Chromium Headless Shell) (\d+)\.(\d+)\.(\d+)\.(\d+)\s*$/);
    if (match) browserVersion = match.slice(1).map(Number);
  } catch { /* unavailable */ }
  const nodeVersion = process.versions.node.split(".").map(Number);
  await appendFile(output, JSON.stringify({ label: "probe_environment", browser_version: browserVersion,
    node_version: nodeVersion, platform: ["linux", "darwin", "win32"].includes(platform()) ? platform() : "other",
    cpu_count: availableParallelism() }) + "\n").catch(() => {});
} finally {
  clearTimeout(timer);
  await Promise.all([...active].map(dispose => dispose().catch(() => {})));
}
