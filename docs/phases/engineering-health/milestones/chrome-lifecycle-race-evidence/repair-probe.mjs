// One loaded run of the lifecycle file, including the failure probes.
// Foreground only. Kills the load children and the test process group it spawned.
// Writes repair-counts.json with counts and booleans, not machine paths.
import { spawn } from "node:child_process";
import { writeFileSync } from "node:fs";
import { availableParallelism } from "node:os";

const testRel = "tools/presentation_harness/tests/chrome-lifecycle.test.mjs";
const outPath = "docs/phases/engineering-health/milestones/chrome-lifecycle-race-evidence/repair-counts.json";
const workers = 4;
const loadChildren = [];
let testChild = null;

function startLoad() {
  for (let i = 0; i < workers; i += 1) {
    loadChildren.push(spawn(process.execPath, ["-e", "let x=0;for(;;){x=(x+1)|0}"], { stdio: "ignore" }));
  }
}

function killTestGroup() {
  if (!testChild || !Number.isInteger(testChild.pid)) return;
  if (testChild.exitCode !== null || testChild.signalCode !== null) return;
  try { process.kill(-testChild.pid, "SIGKILL"); } catch { /* group already gone */ }
}

async function stopLoad() {
  const children = loadChildren.splice(0);
  await Promise.all(children.map((child) => new Promise((resolve) => {
    if (child.exitCode !== null || child.signalCode !== null) { resolve(); return; }
    child.once("exit", () => resolve());
    try { child.kill("SIGKILL"); } catch { resolve(); }
  })));
  let alive = 0;
  for (const child of children) {
    if (!Number.isInteger(child.pid)) continue;
    try { process.kill(child.pid, 0); alive += 1; } catch { /* reaped */ }
  }
  return alive;
}

function redact(text) {
  return String(text)
    .replace(/\/Users\/[^\s'")\]]+/g, "<abs>")
    .replace(/\/private\/var\/[^\s'")\]]+/g, "<tmp>")
    .replace(/\/var\/folders\/[^\s'")\]]+/g, "<tmp>")
    .replace(/\/tmp\/[^\s'")\]]+/g, "<tmp>");
}

function classify(text) {
  return {
    tests: Number((text.match(/^# tests (\d+)/m) || [])[1] || 0),
    pass: Number((text.match(/^# pass (\d+)/m) || [])[1] || 0),
    fail: Number((text.match(/^# fail (\d+)/m) || [])[1] || 0),
    unhandledRejection: /UnhandledPromiseRejection|unhandledRejection|PromiseRejectionHandledWarning|rejection was not handled/i.test(text),
    lateAsync: /asynchronous activity after the test ended|rejected after the test/i.test(text),
  };
}

function runOnce() {
  const env = { ...process.env };
  for (const name of [
    "DEMO_CHROME_STARTUP_DIR", "DEMO_LAUNCHER", "DEMO_CHROME_TRACE", "NODE_OPTIONS",
    "NODE_TEST_CONTEXT", "FORCE_COLOR", "NO_COLOR", "DEMO_MARKER",
    "DEMO_LIFECYCLE_PROBE", "DEMO_LIFECYCLE_REPORT", "DEMO_SIDE",
  ]) delete env[name];
  const started = Date.now();
  const child = spawn(process.execPath, ["--test", testRel], {
    cwd: process.cwd(),
    env,
    stdio: ["ignore", "pipe", "pipe"],
    detached: true,
  });
  testChild = child;
  let stdout = "";
  let stderr = "";
  const take = (buf, chunk) => {
    const next = buf + chunk;
    return next.length > 80000 ? next.slice(-80000) : next;
  };
  child.stdout.on("data", (chunk) => { stdout = take(stdout, chunk.toString("utf8")); });
  child.stderr.on("data", (chunk) => { stderr = take(stderr, chunk.toString("utf8")); });
  const timer = setTimeout(() => killTestGroup(), 25000);
  return new Promise((resolve, reject) => {
    child.once("error", (error) => { clearTimeout(timer); reject(error); });
    child.once("exit", (code) => {
      clearTimeout(timer);
      killTestGroup();
      testChild = null;
      resolve({ code, ms: Date.now() - started, text: redact(`${stdout}\n${stderr}`) });
    });
  });
}

let run = null;
let alive = null;
try {
  startLoad();
  run = await runOnce();
} finally {
  killTestGroup();
  alive = await stopLoad();
}

const summary = run ? classify(run.text) : { tests: 0, pass: 0, fail: 0, unhandledRejection: false, lateAsync: false };
const record = {
  base_commit: "67c7914e09c69371dc30be4400422b0d64e482af",
  node: process.version,
  cpus: availableParallelism(),
  load_workers: workers,
  command: "node docs/phases/engineering-health/milestones/chrome-lifecycle-race-evidence/repair-probe.mjs",
  test_command: "node --test tools/presentation_harness/tests/chrome-lifecycle.test.mjs",
  code: run ? run.code : null,
  ms: run ? run.ms : null,
  tests: summary.tests,
  pass: summary.pass,
  fail: summary.fail,
  unhandledRejection: summary.unhandledRejection,
  lateAsync: summary.lateAsync,
  load_alive_after_stop: alive,
};
writeFileSync(outPath, `${JSON.stringify(record, null, 2)}\n`);
const ok = record.code === 0 && record.tests === 6 && record.pass === 6 && record.fail === 0
  && record.unhandledRejection === false && record.lateAsync === false && record.load_alive_after_stop === 0;
if (!ok) {
  process.stderr.write(`repair probe failed code=${record.code} tests=${record.tests} pass=${record.pass} fail=${record.fail} unhandled=${record.unhandledRejection} late=${record.lateAsync} alive=${record.load_alive_after_stop}\n`);
  process.exit(1);
}
process.stdout.write(`repair probe pass=${record.pass} ms=${record.ms} alive=${record.load_alive_after_stop}\n`);
