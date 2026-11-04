// Foreground reproduction of the Chrome lifecycle marker race.
// Run from the repository root: node <this-file> full|injected80|saturate
// Restores the lifecycle test bytes on exit. Kills only child pids it spawned.
// Writes a redacted JSON report under the system temp directory.
// Injected series replace the one current `const setup` declaration. A change
// to that declaration's publication body does not skip the series.
import { spawn, execFileSync } from "node:child_process";
import { readFileSync, writeFileSync, existsSync } from "node:fs";
import { availableParallelism, tmpdir } from "node:os";
import { join } from "node:path";

const repo = process.cwd();
const testRel = "tools/presentation_harness/tests/chrome-lifecycle.test.mjs";
const testPath = `${repo}/${testRel}`;
const original = readFileSync(testPath);
const reportPath = join(tmpdir(), "chrome-lifecycle-race-report.json");
const loadPidPath = join(tmpdir(), "chrome-lifecycle-race-load-pids.txt");
const mode = process.argv[2] || "full";

function setupStatement(text) {
  const match = text.match(/const setup = `[^`]*`;/);
  if (!match) throw new Error("setup declaration missing");
  const count = text.split(match[0]).length - 1;
  if (count !== 1) throw new Error(`setup occurrences: ${count}`);
  return match[0];
}
function setupSplit(waitMs) {
  return "const setup = `import {closeSync,openSync,writeSync} from 'node:fs';\\nconst profile=process.argv.find(a=>a.startsWith('--user-data-dir=')).split('=').slice(1).join('=');\\nconst fd=openSync(process.env.DEMO_MARKER,'w');\\nAtomics.wait(new Int32Array(new SharedArrayBuffer(4)),0,0," + waitMs + ");\\nwriteSync(fd,JSON.stringify({profile,pid:process.pid}));\\ncloseSync(fd);\\n`;";
}

let patched = false;
let loadChildren = [];
let activeTestPid = null;

function redact(text) {
  return String(text)
    .replace(/\/Users\/[^\s'")\]]+/g, "<abs>")
    .replace(/\/private\/var\/[^\s'")\]]+/g, "<tmp>")
    .replace(/\/var\/folders\/[^\s'")\]]+/g, "<tmp>")
    .replace(/\/tmp\/[^\s'")\]]+/g, "<tmp>");
}

function restoreTest() {
  writeFileSync(testPath, original);
  patched = false;
}

function loadPids() {
  return loadChildren.map((child) => child.pid).filter((pid) => Number.isInteger(pid));
}

function stopLoad() {
  const children = loadChildren.splice(0);
  const pids = children.map((child) => child.pid).filter((pid) => Number.isInteger(pid));
  for (const child of children) {
    try { child.kill("SIGKILL"); } catch { /* already gone */ }
  }
  writeFileSync(loadPidPath, "");
  return pids.filter((pid) => {
    try { process.kill(pid, 0); return true; } catch { return false; }
  });
}

function startLoad(count) {
  stopLoad();
  for (let i = 0; i < count; i += 1) {
    const child = spawn(process.execPath, ["-e", "let x=0;for(;;){x=(x+1)|0}"], { stdio: "ignore" });
    loadChildren.push(child);
  }
  writeFileSync(loadPidPath, loadPids().join("\n"));
  process.stdout.write(`load_pids ${loadPids().join(",")}\n`);
}

function applySetup(waitMs) {
  const current = readFileSync(testPath);
  if (!current.equals(original)) {
    const text = current.toString("utf8");
    const ownPatch = patched && text.includes("Atomics.wait(new Int32Array(new SharedArrayBuffer(4)),0,0,");
    if (!ownPatch) throw new Error("lifecycle test changed outside the runner");
  } else {
    const status = execFileSync("git", ["status", "--short", "--", testRel], { cwd: repo, encoding: "utf8" });
    if (status.trim()) throw new Error("lifecycle test is dirty before instrumentation");
  }
  const text = original.toString("utf8");
  const statement = setupStatement(text);
  writeFileSync(testPath, text.replace(statement, setupSplit(waitMs)));
  patched = true;
}

function hashTest() {
  return execFileSync("git", ["hash-object", testRel], { cwd: repo, encoding: "utf8" }).trim();
}

function runOnce() {
  const env = { ...process.env };
  delete env.DEMO_CHROME_STARTUP_DIR;
  delete env.DEMO_LAUNCHER;
  delete env.DEMO_CHROME_TRACE;
  delete env.NODE_OPTIONS;
  delete env.FORCE_COLOR;
  delete env.NO_COLOR;
  const started = Date.now();
  return new Promise((resolve) => {
    const child = spawn(process.execPath, ["--test", testRel], {
      cwd: repo,
      env,
      stdio: ["ignore", "pipe", "pipe"],
      detached: true,
    });
    activeTestPid = child.pid;
    let stdout = "";
    let stderr = "";
    let settled = false;
    const take = (buf, chunk) => {
      const next = buf + chunk;
      return next.length > 120000 ? next.slice(-120000) : next;
    };
    child.stdout.on("data", (chunk) => { stdout = take(stdout, chunk.toString("utf8")); });
    child.stderr.on("data", (chunk) => { stderr = take(stderr, chunk.toString("utf8")); });
    const finish = (code, timedOut) => {
      if (settled) return;
      settled = true;
      clearTimeout(timer);
      try { process.kill(-child.pid, "SIGKILL"); } catch { /* group already gone */ }
      if (activeTestPid === child.pid) activeTestPid = null;
      resolve({
        code,
        timedOut,
        ms: Date.now() - started,
        stdout: redact(stdout),
        stderr: redact(stderr),
      });
    };
    const timer = setTimeout(() => finish("timeout", true), 20000);
    child.on("exit", (code) => finish(code, false));
    child.on("error", (error) => finish(error && error.code ? String(error.code) : "spawn-error", false));
  });
}

function classify(run) {
  const text = `${run.stdout}\n${run.stderr}`;
  const incomplete = /Unexpected end of JSON input|Unexpected token|SyntaxError:/.test(text);
  const enoent = /ENOENT/.test(text) && /marker|no such file/i.test(text);
  const unhandled = /UnhandledPromiseRejection|unhandledRejection|unhandled rejection|rejection was not handled/i.test(text)
    || /triggerUncaughtException/.test(text);
  const launchMessages = [];
  for (const pattern of [
    /Chrome stayed alive without DevToolsActivePort[^\n]*/,
    /Chrome launch cancelled[^\n]*/,
    /launch cancelled[^\n]*/,
    /exited before readiness[^\n]*/,
  ]) {
    const found = text.match(pattern);
    if (found) launchMessages.push(found[0].slice(0, 240));
  }
  const summary = {
    tests: Number((text.match(/^# tests (\d+)/m) || [])[1] || 0),
    pass: Number((text.match(/^# pass (\d+)/m) || [])[1] || 0),
    fail: Number((text.match(/^# fail (\d+)/m) || [])[1] || 0),
  };
  const notOk = [...text.matchAll(/^not ok \d+ - (.+)$/gm)].map((match) => match[1]);
  const excerpt = text.split("\n").filter((line) => /not ok|SyntaxError|Unexpected|Unhandled|unhandled|triggerUncaught|InfraError|stayed alive|launch cancelled|exited before|ENOENT|AssertionError|fail \d|# /i.test(line)).slice(0, 40).join("\n").slice(0, 4000);
  return {
    code: run.code,
    timedOut: run.timedOut,
    ms: run.ms,
    incompleteJson: incomplete,
    missingMarker: enoent,
    unhandledRejection: unhandled,
    launchMessages: [...new Set(launchMessages)],
    summary,
    notOk,
    excerpt: incomplete || unhandled || run.code !== 0 ? excerpt : "",
  };
}

async function series(spec) {
  if (spec.load) startLoad(spec.load);
  else stopLoad();
  if (spec.waitMs === undefined) restoreTest();
  else applySetup(spec.waitMs);
  const runs = [];
  for (let i = 0; i < spec.iterations; i += 1) {
    const run = classify(await runOnce());
    runs.push(run);
    process.stdout.write(`${spec.label} ${i + 1}/${spec.iterations} code=${run.code} ms=${run.ms} pass=${run.summary.pass} fail=${run.summary.fail} incomplete=${run.incompleteJson} unhandled=${run.unhandledRejection} missing=${run.missingMarker}\n`);
  }
  return { label: spec.label, loadWorkers: spec.load || 0, waitMs: spec.waitMs ?? null, runs };
}

function stopActiveTest() {
  if (!activeTestPid) return;
  try { process.kill(-activeTestPid, "SIGKILL"); } catch { /* group already gone */ }
  activeTestPid = null;
}

function onStop(signal) {
  stopActiveTest();
  restoreTest();
  stopLoad();
  process.exit(signal === "SIGINT" ? 130 : 143);
}
process.on("SIGINT", () => onStop("SIGINT"));
process.on("SIGTERM", () => onStop("SIGTERM"));
process.on("exit", () => {
  try { stopActiveTest(); } catch { /* last-chance test kill */ }
  try { restoreTest(); } catch { /* last-chance restore */ }
  try { stopLoad(); } catch { /* last-chance kill */ }
});

const plans = {
  probe: [
    { label: "natural_noload", iterations: 1, load: 0 },
    { label: "injected_wait_80_noload", iterations: 1, load: 0, waitMs: 80 },
  ],
  injected80: [
    { label: "injected_wait_80_noload", iterations: 6, load: 0, waitMs: 80 },
    { label: "injected_wait_80_load", iterations: 4, load: 4, waitMs: 80 },
  ],
  saturate: [
    { label: "natural_load_all_cores", iterations: 12, load: availableParallelism() },
  ],
  full: [
    { label: "natural_noload", iterations: 4, load: 0 },
    { label: "natural_load", iterations: 30, load: 4 },
    { label: "injected_split_no_wait_load", iterations: 6, load: 4, waitMs: 0 },
    { label: "injected_wait_80_noload", iterations: 6, load: 0, waitMs: 80 },
    { label: "injected_wait_80_load", iterations: 4, load: 4, waitMs: 80 },
  ],
};

const selected = plans[mode];
if (!selected) throw new Error(`unknown mode ${mode}`);

const beforeHash = hashTest();
const present = {
  DEMO_CHROME_STARTUP_DIR: Object.hasOwn(process.env, "DEMO_CHROME_STARTUP_DIR"),
  DEMO_LAUNCHER: Object.hasOwn(process.env, "DEMO_LAUNCHER"),
  DEMO_CHROME_TRACE: Object.hasOwn(process.env, "DEMO_CHROME_TRACE"),
  NODE_OPTIONS: Object.hasOwn(process.env, "NODE_OPTIONS"),
  FORCE_COLOR: Object.hasOwn(process.env, "FORCE_COLOR"),
  NO_COLOR: Object.hasOwn(process.env, "NO_COLOR"),
};
const startedAt = new Date().toISOString();
const results = [];
let failure = null;
try {
  for (const spec of selected) results.push(await series(spec));
} catch (error) {
  failure = redact(error && error.stack ? error.stack : String(error));
} finally {
  restoreTest();
  const survivors = stopLoad();
  const afterHash = hashTest();
  const report = {
    mode,
    startedAt,
    finishedAt: new Date().toISOString(),
    node: process.version,
    cpuCount: availableParallelism(),
    sourceTest: testRel,
    beforeHash,
    afterHash,
    restoredMatch: beforeHash === afterHash && !existsSync(testPath) === false && readFileSync(testPath).equals(original),
    bytesMatch: readFileSync(testPath).equals(original),
    envPresent: present,
    loadCommand: "node -e 'let x=0;for(;;){x=(x+1)|0}'",
    testCommand: "node --test tools/presentation_harness/tests/chrome-lifecycle.test.mjs",
    clearedEnv: ["DEMO_CHROME_STARTUP_DIR", "DEMO_LAUNCHER", "DEMO_CHROME_TRACE", "NODE_OPTIONS", "FORCE_COLOR", "NO_COLOR"],
    loadSurvivors: survivors,
    failure,
    results,
  };
  writeFileSync(reportPath, JSON.stringify(report));
  process.stdout.write(`report bytesMatch=${report.bytesMatch} restoredMatch=${report.restoredMatch} failure=${failure ? "yes" : "no"}\n`);
}
if (failure) process.exitCode = 1;
