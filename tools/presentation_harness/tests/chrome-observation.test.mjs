import test from "node:test";
import assert from "node:assert/strict";
import { chmod, mkdtemp, readFile, rm, writeFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { pathToFileURL } from "node:url";
const launcher = process.env.DEMO_LAUNCHER || new URL("../lib/chrome.mjs", import.meta.url).href;
const { launchChrome } = await import(launcher.startsWith("file:") ? launcher : pathToFileURL(launcher).href);
import { createObservation, PROGRESS_RECORD_LIMIT, PROCESS_TREE_LIMIT } from "../lib/chrome-observation.mjs";
import { parseResourceTrace, readResourceTrace } from "../chrome-resource-probe.mjs";

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
test("resource trace parser preserves complete snapshots before an incomplete trailing append", () => {
  const first = { label: "resource-controls", readiness_ms: null, progress_sequence: 1 };
  const second = { label: "resource-controls", readiness_ms: 12, progress_sequence: 2 };
  const parsed = parseResourceTrace(JSON.stringify(first) + "\n" + JSON.stringify(second) + '\n{"demo-private-tail":');
  assert.deepEqual(parsed.records, [first, second]);
  assert.equal(parsed.trace_status, "read");
  assert.equal(parsed.incomplete_trailing_record, true);
  assert.equal(parsed.unterminated_trailing_record, true);
  assert.equal(parsed.malformed_records, 0);
  assert.doesNotMatch(JSON.stringify(parsed), /demo-private-tail/);
});
test("resource trace parser distinguishes malformed complete records and an undelimited valid record", () => {
  const row = { label: "resource-controls", progress_sequence: 1 };
  const parsed = parseResourceTrace('demo-private-bad\nnull\n[]\n' + JSON.stringify(row));
  assert.deepEqual(parsed.records, [row]);
  assert.equal(parsed.malformed_records, 3);
  assert.equal(parsed.incomplete_trailing_record, false);
  assert.equal(parsed.unterminated_trailing_record, true);
  assert.doesNotMatch(JSON.stringify(parsed), /demo-private-bad/);
  assert.equal(parseResourceTrace("").trace_status, "read");
  assert.deepEqual(parseResourceTrace('{"label":"correction-other"}\n').records, []);
});
test("resource trace reader distinguishes missing and unreadable files without leaking paths", async () => {
  const root = await mkdtemp(join(tmpdir(), "demo-reader-private-"));
  try {
    const missing = await readResourceTrace(join(root, "missing"));
    assert.equal(missing.trace_status, "missing"); assert.equal(missing.trace_read_error, "ENOENT");
    const unreadable = await readResourceTrace(root);
    assert.equal(unreadable.trace_status, "unreadable"); assert.equal(unreadable.trace_read_error, "EISDIR");
    assert.deepEqual(missing.records, []); assert.deepEqual(unreadable.records, []);
    assert.doesNotMatch(JSON.stringify([missing, unreadable]), /demo-reader-private/);
    const output = join(root, "trace");
    await writeFile(output, '{"label":"resource-controls","progress_sequence":1}\n{"demo-private-tail":');
    const recovered = await readResourceTrace(output);
    assert.equal(recovered.records.length, 1); assert.equal(recovered.incomplete_trailing_record, true);
  } finally { await rm(root, { recursive: true, force: true }); }
});
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

async function launchedUrl(body, timeout = 2000) {
  const root = await mkdtemp(join(tmpdir(), "demo-observation-"));
  try {
    const binary = join(root, "chrome");
    await writeFile(binary, `#!/usr/bin/env node\nimport {renameSync,writeFileSync} from 'node:fs';\nconst p=process.argv.find(x=>x.startsWith('--user-data-dir=')).slice(16);\n${body}\n`);
    await chmod(binary, 0o755);
    const chrome = await launchChrome(binary, { launchTimeoutMs: timeout });
    try { return chrome.wsUrl; } finally { await chrome.dispose(); }
  } finally { await rm(root, { recursive: true, force: true }); }
}

test("a complete decimal port line keeps the advertised browser path", async () => {
  const url = await launchedUrl(`writeFileSync(p+'/DevToolsActivePort','12345\\n/devtools/browser/demo-path\\n'); setInterval(()=>{},1000);`);
  assert.equal(url, "ws://127.0.0.1:12345/devtools/browser/demo-path");
});

test("readiness waits for a complete port line instead of a positive prefix", async () => {
  const url = await launchedUrl(`writeFileSync(p+'/DevToolsActivePort','9222'); setTimeout(()=>{writeFileSync(p+'/DevToolsActivePort.complete','12345\\n/devtools/browser/demo-path\\n'); renameSync(p+'/DevToolsActivePort.complete', p+'/DevToolsActivePort');},180); setInterval(()=>{},1000);`, 2000);
  assert.equal(url, "ws://127.0.0.1:12345/devtools/browser/demo-path");
});

test("a stuck positive port prefix is not an advertised port", async () => {
  const { result, trace } = await caseRun(`writeFileSync(p+'/DevToolsActivePort','9222'); setInterval(()=>{},1000);`, 500, 100);
  assert.match(result, /stayed alive without DevToolsActivePort before the launch timeout/);
  assert.equal(trace.outcome, "not_ready_after_grace");
  assert.ok(trace.file_states.some(state => state.state === "malformed"));
  assert.equal(trace.file_states.some(state => state.state === "ready"), false);
  assert.ok(trace.file_metadata && trace.file_metadata.size > 0);
  assert.ok(trace.deadline_wall_ms >= 500);
});

test("a digit prefix before trailing junk is not a complete port line", async () => {
  const { result, trace } = await caseRun(`writeFileSync(p+'/DevToolsActivePort','9222xyz\\n/devtools/browser/demo-path\\n'); setInterval(()=>{},1000);`, 500, 100);
  assert.match(result, /stayed alive without DevToolsActivePort before the launch timeout/);
  assert.equal(trace.outcome, "not_ready_after_grace");
  assert.equal(trace.file_states.some(state => state.state === "ready"), false);
  assert.ok(trace.deadline_wall_ms >= 500);
});

async function progressRows(output) {
  return (await readFile(output, "utf8")).trim().split("\n").map(JSON.parse);
}
test("zero-grace progress survives an unfinished startup and remains bounded and sanitized", async () => {
  const root = await mkdtemp(join(tmpdir(), "demo-progress-"));
  let cancel;
  try {
    const { binary, marker } = await fakeWithMarker(root, `process.stderr.write('demo-private-value'.repeat(100000)); ${live}`);
    const output = join(root, "trace");
    const observer = createObservation({ label: "resource-controls", output, graceMs: 0, progress: true });
    observer.stage("test_started");
    const pending = launchChrome(binary, { launchTimeoutMs: 5000, observer, onOwnership: dispose => { cancel = dispose; } });
    const rejected = assert.rejects(pending, /cancelled/);
    let rows;
    for (let i = 0; i < 200; i++) {
      try { rows = await progressRows(output); await readFile(marker, "utf8"); if (rows.some(row => row.samples.length)) break; } catch { /* process/write in flight */ }
      await new Promise(resolve => setTimeout(resolve, 10));
    }
    assert.ok(rows.some(row => row.outcome === null && row.file_states.some(x => x.state === "missing")));
    assert.equal(observer.graceMs, 0);
    for (let i = 0; i < 300; i++) { observer.stage("child_wait_started"); observer.stage("demo-private-value"); }
    await cancel(); await rejected; observer.close(); await observer.flushed();
    await assertClean(marker);
    rows = await progressRows(output);
    assert.ok(rows.length <= PROGRESS_RECORD_LIMIT);
    assert.ok(rows.every(row => row.stages.length <= 32 && row.samples.length <= 40));
    assert.ok(Buffer.byteLength(await readFile(output, "utf8")) <= PROGRESS_RECORD_LIMIT * 65537);
    assert.doesNotMatch(JSON.stringify(rows), /demo-private-value|demo-progress-|ws:\/\//);
  } finally { if (cancel) await cancel(); await rm(root, { recursive: true, force: true }); }
});

test("progress output failure preserves original success and zero-grace timeout cleanup", async () => {
  const root = await mkdtemp(join(tmpdir(), "demo-progress-io-"));
  try {
    for (const mode of ["success", "timeout"]) {
      const { binary, marker } = await fakeWithMarker(root, `${mode === "success" ? ready : ""} ${live}`);
      const observer = createObservation({ label: "resource-controls", output: root, graceMs: 0, progress: true });
      observer.stage("test_started");
      try {
        if (mode === "success") { const chrome = await launchChrome(binary, { observer, launchTimeoutMs: 2000 }); await chrome.dispose(); }
        else await assert.rejects(launchChrome(binary, { observer, launchTimeoutMs: 500 }), /launch timeout/);
      } finally { observer.close(); await observer.flushed(); }
      await assertClean(marker);
    }
  } finally { await rm(root, { recursive: true, force: true }); }
});

test("CPU-work and timer-delay calibration separates elapsed from available process counters", async () => {
  const root = await mkdtemp(join(tmpdir(), "demo-calibration-"));
  const measurements = [];
  try {
    for (const busy of [false, true]) {
      const { binary } = await fakeWithMarker(root, `${busy ? "const end=Date.now()+2400; while(Date.now()<end) Math.sqrt(Math.random());" : ""}
        ${busy ? ready : `setTimeout(()=>{${ready}},2400);`} ${live}`);
      const output = join(root, busy ? "busy" : "waiting");
      const observer = createObservation({ label: "resource-controls", output, graceMs: 0, progress: true });
      try { const chrome = await launchChrome(binary, { observer, launchTimeoutMs: 5000 }); await chrome.dispose(); }
      finally { observer.close(); await observer.flushed(); }
      const rows = await progressRows(output), last = rows.at(-1);
      assert.ok(last.readiness_ms >= 2000);
      assert.ok(last.samples.length >= 2);
      assert.ok(last.samples.every(x => x.sample_gap_ms === null || x.sample_gap_ms >= 0));
      assert.ok(last.samples.every(x => !x.tree.available || x.tree.sampled_processes <= PROCESS_TREE_LIMIT));
      if (process.platform === "linux") {
        const samples = last.samples.filter(x => x.tree.available);
        assert.ok(samples.length >= 2);
        measurements.push(samples.at(-1).tree.cpu_user_ticks + samples.at(-1).tree.cpu_system_ticks - samples[0].tree.cpu_user_ticks - samples[0].tree.cpu_system_ticks);
      } else assert.ok(last.samples.every(x => x.available === false && x.tree.available === false));
    }
    if (process.platform === "linux") assert.ok(measurements[1] > measurements[0] + 20);
  } finally { await rm(root, { recursive: true, force: true }); }
});
