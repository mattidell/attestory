import test from "node:test";
import assert from "node:assert/strict";
import { chmod, mkdtemp, readFile, rm, writeFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { pathToFileURL } from "node:url";
const launcher = process.env.DEMO_LAUNCHER || new URL("../lib/chrome.mjs", import.meta.url).href;
const { launchChrome } = await import(launcher.startsWith("file:") ? launcher : pathToFileURL(launcher).href);
import { createObservation } from "../lib/chrome-observation.mjs";

async function caseRun(body, timeout = 3000, graceMs = 5000) {
  const root = await mkdtemp(join(tmpdir(), "demo-observation-"));
  try {
    const binary = join(root, "chrome"); const output = join(root, "trace");
    await writeFile(binary, `#!/usr/bin/env node\nimport {writeFileSync} from 'node:fs';\nconst p=process.argv.find(x=>x.startsWith('--user-data-dir=')).slice(16);\n${body}\n`);
    await chmod(binary, 0o755);
    const observer = createObservation({ label: "isolated", output, graceMs });
    let result = "success";
    try { const chrome = await launchChrome(binary, timeout === null ? { observer } : { launchTimeoutMs: timeout, observer }); await chrome.dispose(); }
    catch (error) { result = error.message; }
    return { result, trace: JSON.parse(await readFile(output, "utf8")) };
  } finally { await rm(root, { recursive: true, force: true }); }
}
const live = `setInterval(()=>{},1000);`;
const ready = `writeFileSync(p+'/DevToolsActivePort','12345\\n/devtools/browser/demo-secret');`;
test("early readiness succeeds, records timing and hides endpoint", async () => {
  const { result, trace } = await caseRun(`process.stderr.write('DevTools listening on ws://demo-secret'); ${ready} ${live}`, 5000);
  assert.equal(result, "success"); assert.equal(trace.outcome, "ready_accepted");
  assert.ok(trace.readiness_ms >= 0); assert.ok(trace.advertised_ms >= 0);
  assert.doesNotMatch(JSON.stringify(trace), /demo-secret|ws:\/\//);
});
test("the default launch allowance is 45 s and fits the owner's 210 s wait", async () => {
  const { CHROME_LAUNCH_TIMEOUT_MS } = await import(pathToFileURL(new URL("../lib/chrome.mjs", import.meta.url).pathname).href);
  assert.equal(CHROME_LAUNCH_TIMEOUT_MS, 45000);
  assert.ok(120000 + CHROME_LAUNCH_TIMEOUT_MS + 60000 < 240000);
});
test("a launch with no timeout argument resolves to the 45 s allowance", async () => {
  const mod = await import(pathToFileURL(new URL("../lib/chrome.mjs", import.meta.url).pathname).href);
  assert.equal(mod.resolveLaunchTimeoutMs({}), 45000);
  assert.equal(mod.resolveLaunchTimeoutMs({ DEMO_CHROME_LAUNCH_TIMEOUT_MS: "2000" }), 2000);
  assert.equal(mod.launchTimeoutFor({}), process.env.DEMO_CHROME_LAUNCH_TIMEOUT_MS ? Number(process.env.DEMO_CHROME_LAUNCH_TIMEOUT_MS) : 45000);
  assert.equal(mod.launchTimeoutFor({ launchTimeoutMs: 1234 }), 1234);
});
async function stderrOf(body, slowLaunchMs) {
  const root = await mkdtemp(join(tmpdir(), "demo-slow-"));
  const original = process.stderr.write; let seen = "";
  try {
    const binary = join(root, "chrome");
    await writeFile(binary, `#!/usr/bin/env node\nimport {writeFileSync} from 'node:fs';\nconst p=process.argv.find(x=>x.startsWith('--user-data-dir=')).slice(16);\n${body}\n`);
    await chmod(binary, 0o755);
    process.stderr.write = function(chunk) { seen += String(chunk); return true; };
    const chrome = await launchChrome(binary, { launchTimeoutMs: 5000, slowLaunchMs });
    await chrome.dispose();
  } finally { process.stderr.write = original; await rm(root, { recursive: true, force: true }); }
  return seen;
}
test("a late-but-accepted launch writes one slow-launch line; a fast one does not", async () => {
  const slow = await stderrOf(`setTimeout(()=>{${ready}},900); ${live}`, 400);
  assert.match(slow, /^slow Chrome launch: \d+ ms\n$/);
  const fast = await stderrOf(`${ready} ${live}`, 4000);
  assert.equal(fast, "");
});
test("readiness before the injected allowance succeeds", async () => {
  const { result, trace } = await caseRun(`setTimeout(()=>{${ready}},800); ${live}`, 3000);
  assert.equal(result, "success"); assert.equal(trace.outcome, "ready_accepted");
  assert.ok(trace.readiness_ms >= 500);
});
test("late readiness is measured but original deadline still fails", async () => {
  const { result, trace } = await caseRun(`writeFileSync(p+'/DevToolsActivePort','bad'); setTimeout(()=>{${ready}},4200); ${live}`);
  assert.match(result, /launch timeout/); assert.equal(trace.outcome, "ready_after_deadline");
  assert.ok(trace.readiness_ms >= 3000); assert.ok(trace.deadline_wall_ms >= 3000);
  assert.ok(trace.deadline_monotonic_ms >= 0); assert.ok(trace.file_metadata.size > 0); assert.ok(trace.file_states.some(x=>x.state === "malformed"));
});
test("never-ready and exit are distinct and bounded", async () => {
  const never = await caseRun(live, 2000, 500);
  assert.match(never.result, /launch timeout/); assert.equal(never.trace.outcome, "not_ready_after_grace");
  assert.ok(never.trace.file_states.some(x=>x.state === "missing"));
  const exit = await caseRun("process.exit(7);", 5000);
  assert.match(exit.result, /code=7/); assert.equal(exit.trace.outcome, "exit_before_ready");
  assert.equal(exit.trace.exit_kind, "exited"); assert.equal(exit.trace.exit_code, 7);
});

test("unreadable file and fixed startup clauses remain safe", async () => {
  const { trace } = await caseRun(`import {mkdirSync} from 'node:fs'; mkdirSync(p+'/DevToolsActivePort'); process.stderr.write('Error writing DevTools active port to file demo-private-value\\nCannot start http server for devtools.'); ${live}`, 2000, 500);
  assert.ok(trace.file_states.some(x => x.state === "unreadable:EISDIR"));
  assert.ok(trace.stderr_categories.includes("devtools-active-port-write-error"));
  assert.ok(trace.stderr_categories.includes("devtools-http-server-start-error"));
  assert.doesNotMatch(JSON.stringify(trace), /demo-private-value/);
});

async function fakeWithMarker(root, body) {
  const binary = join(root, "chrome");
  const marker = join(root, "marker");
  await writeFile(binary, `#!/usr/bin/env node\nimport {writeFileSync} from 'node:fs';\nconst p=process.argv.find(x=>x.startsWith('--user-data-dir=')).slice(16);\nwriteFileSync(${JSON.stringify(marker)}, JSON.stringify({profile:p,pid:process.pid}));\n${body}`);
  await chmod(binary, 0o755);
  return { binary, marker };
}
async function assertClean(marker) {
  const { profile, pid } = JSON.parse(await readFile(marker, "utf8"));
  await assert.rejects(import("node:fs/promises").then(fs => fs.stat(profile)), { code: "ENOENT" });
  assert.throws(() => process.kill(pid, 0), { code: "ESRCH" });
}

test("cancelling during observed grace preserves original timeout and cleans ownership", async () => {
  const root = await mkdtemp(join(tmpdir(), "demo-observed-cancel-"));
  try {
    const { binary, marker } = await fakeWithMarker(root, `process.stderr.write('demo-private-cancel'); ${live}`);
    const output = join(root, "trace");
    const observer = createObservation({ label: "isolated", output, graceMs: 5000 });
    let deadlineReached;
    const deadline = new Promise(resolve => { deadlineReached = resolve; });
    const originalDeadline = observer.deadline;
    observer.deadline = () => { originalDeadline(); deadlineReached(); };
    let cancel;
    const pending = launchChrome(binary, { launchTimeoutMs: 2000, observer, onOwnership: dispose => { cancel = dispose; } });
    const rejected = assert.rejects(pending, error => {
      assert.match(error.message, /stayed alive without DevToolsActivePort before the launch timeout/);
      assert.doesNotMatch(error.message, /demo-private-cancel/);
      return true;
    });
    await deadline;
    await cancel();
    await rejected;
    await assertClean(marker);
    const trace = JSON.parse(await readFile(output, "utf8"));
    assert.equal(trace.outcome, "cancelled");
    assert.ok(trace.deadline_monotonic_ms >= 2000);
    assert.doesNotMatch(JSON.stringify(trace), /demo-private-cancel/);
  } finally { await rm(root, { recursive: true, force: true }); }
});

test("failed observation writes preserve success and timeout and clean ownership", async () => {
  const root = await mkdtemp(join(tmpdir(), "demo-observed-writer-"));
  const originalWrite = process.stderr.write;
  let diagnostics = "";
  process.stderr.write = function(chunk, ...args) { diagnostics += String(chunk); return true; };
  try {
    for (const mode of ["success", "timeout"]) {
      const markerRoot = join(root, mode);
      await import("node:fs/promises").then(fs => fs.mkdir(markerRoot));
      const { binary, marker } = await fakeWithMarker(markerRoot,
        `process.stderr.write('demo-private-writer'); ${mode === "success" ? ready : ""} ${live}`);
      // A directory is not writable as the trace file; appendFile fails deterministically.
      const observer = createObservation({ label: "isolated", output: root, graceMs: 500 });
      if (mode === "success") {
        const chrome = await launchChrome(binary, { launchTimeoutMs: 5000, observer });
        await chrome.dispose();
      } else {
        await assert.rejects(launchChrome(binary, { launchTimeoutMs: 2000, observer }), error => {
          assert.match(error.message, /stayed alive without DevToolsActivePort before the launch timeout/);
          assert.doesNotMatch(error.message, /demo-private-writer/);
          return true;
        });
      }
      await assertClean(marker);
    }
    assert.equal(diagnostics, "chrome-observation-write-failed\n".repeat(2));
    assert.doesNotMatch(diagnostics, /demo-private-writer|demo-observed-writer/);
  } finally {
    process.stderr.write = originalWrite;
    await rm(root, { recursive: true, force: true });
  }
});
