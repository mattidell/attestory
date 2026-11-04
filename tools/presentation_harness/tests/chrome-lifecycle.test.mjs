import test from "node:test";
import assert from "node:assert/strict";
import { spawn } from "node:child_process";
import { chmod, mkdtemp, readFile, readdir, rm, stat, writeFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";

const launcher = process.env.DEMO_LAUNCHER || new URL("../lib/chrome.mjs", import.meta.url).href;
const { launchChrome } = await import(launcher.startsWith("file:") ? launcher : pathToFileURL(launcher).href);
const testFile = fileURLToPath(import.meta.url);
const repoRoot = fileURLToPath(new URL("../../../", import.meta.url));

async function fake(root, body) {
  const path = join(root, "chrome");
  await writeFile(path, `#!/usr/bin/env node\n${body}`, "utf8");
  await chmod(path, 0o755);
  return path;
}
async function absent(path) {
  await assert.rejects(stat(path), { code: "ENOENT" });
}
const setup = `import {renameSync,writeFileSync} from 'node:fs';\nconst profile=process.argv.find(a=>a.startsWith('--user-data-dir=')).split('=').slice(1).join('=');\nconst markerBody=JSON.stringify({profile,pid:process.pid});\nconst markerTemp=process.env.DEMO_MARKER+'.tmp';\nwriteFileSync(markerTemp,markerBody);\nrenameSync(markerTemp,process.env.DEMO_MARKER);\n`;

function combineFailures(errors) {
  const present = errors.filter((error) => error != null);
  if (present.length <= 1) return present[0] ?? null;
  return new AggregateError(present, "marker poll and launch assertion both failed");
}

// The promise returned by assert.rejects can reject while the marker poll is
// still awaiting. Record that settlement in the handler and do not throw there.
// Disposal and the await of this observation stay in finally, which then surfaces
// the recorded mismatch. A marker failure does not discard it.
async function drainOwnedLaunch({ pending, takeCancel, marker, polls, intervalMs }) {
  const rejected = assert.rejects(pending, /launch cancelled/);
  const assertion = { error: undefined, duringPoll: false };
  let phase = "before";
  const observed = rejected.then(
    () => {
      assertion.error = null;
      assertion.duringPoll = phase === "poll";
    },
    (error) => {
      assertion.error = error;
      assertion.duringPoll = phase === "poll";
    },
  );
  phase = "poll";
  let markerFailure = null;
  let info = null;
  try {
    let lastReadError = null;
    for (let i = 0; i < polls; i += 1) {
      try {
        info = JSON.parse(await readFile(marker, "utf8"));
        break;
      } catch (error) {
        info = null;
        lastReadError = error;
        await new Promise((resolve) => setTimeout(resolve, intervalMs));
      }
    }
    if (!info) markerFailure = lastReadError ?? new Error(`marker was not usable within ${polls} polls`);
  } catch (error) {
    markerFailure = error;
  } finally {
    phase = "after";
    let disposeFailure = null;
    try {
      const cancel = takeCancel();
      if (cancel) await cancel();
    } catch (error) {
      disposeFailure = error;
    }
    try { await observed; }
    catch (error) { if (assertion.error == null) assertion.error = error; }
    markerFailure = combineFailures([markerFailure, disposeFailure, assertion.error]);
    if (markerFailure) markerFailure.assertionDuringPoll = assertion.duringPoll;
  }
  if (markerFailure) throw markerFailure;
  return info;
}

function redact(text) {
  return String(text)
    .replace(/\/Users\/[^\s'")\]]+/g, "<abs>")
    .replace(/\/private\/var\/[^\s'")\]]+/g, "<tmp>")
    .replace(/\/var\/folders\/[^\s'")\]]+/g, "<tmp>")
    .replace(/\/tmp\/[^\s'")\]]+/g, "<tmp>");
}

function walkErrors(error, out = []) {
  if (!error || out.includes(error)) return out;
  out.push(error);
  if (error instanceof AggregateError) {
    for (const inner of error.errors) walkErrors(inner, out);
  }
  return out;
}

function errorText(error) {
  const parts = [error.message];
  if (error.actual && typeof error.actual === "object" && typeof error.actual.message === "string") {
    parts.push(error.actual.message);
  }
  return parts.join("\n");
}

async function probeCase(kind) {
  const root = await mkdtemp(join(tmpdir(), "demo-lifecycle-probe-"));
  const marker = join(root, "marker");
  process.env.DEMO_MARKER = marker;
  const early = kind === "early-noncancellation";
  const body = early
    ? "import {writeFileSync} from 'node:fs';\nconst profile=process.argv.find(a=>a.startsWith('--user-data-dir=')).split('=').slice(1).join('=');\nwriteFileSync(process.env.DEMO_SIDE, JSON.stringify({profile,pid:process.pid}));\nprocess.exit(7);"
    : "import {writeFileSync} from 'node:fs';\nconst profile=process.argv.find(a=>a.startsWith('--user-data-dir=')).split('=').slice(1).join('=');\nwriteFileSync(process.env.DEMO_SIDE, JSON.stringify({profile,pid:process.pid}));\nsetInterval(()=>{}, 1000);";
  try {
    const binary = await fake(root, body);
    let cancel;
    const pending = launchChrome(binary, { launchTimeoutMs: 5000, onOwnership: (dispose) => { cancel = dispose; } });
    let thrown = null;
    try {
      await drainOwnedLaunch({
        pending,
        takeCancel: () => cancel,
        marker,
        polls: 50,
        intervalMs: 20,
      });
    } catch (error) {
      thrown = error;
    }
    let owner = null;
    try { owner = JSON.parse(await readFile(process.env.DEMO_SIDE, "utf8")); } catch { owner = null; }
    let profileGone = false;
    let pidGone = false;
    if (owner) {
      try { await stat(owner.profile); } catch (error) { profileGone = error.code === "ENOENT"; }
      try { process.kill(owner.pid, 0); } catch (error) { pidGone = error.code === "ESRCH"; }
    }
    const errors = walkErrors(thrown);
    const leaves = errors.filter((error) => !(error instanceof AggregateError));
    await writeFile(process.env.DEMO_LIFECYCLE_REPORT, JSON.stringify({
      name: thrown ? thrown.name : null,
      duringPoll: Boolean(thrown && thrown.assertionDuringPoll),
      profileGone,
      pidGone,
      leaves: leaves.length,
      markerCode: errors.some((error) => error.code === "ENOENT") ? "ENOENT" : null,
      assertionName: errors.some((error) => error.name === "AssertionError") ? "AssertionError" : null,
      sawExit: errors.some((error) => /exited before readiness \(code=7, signal=null\)/.test(errorText(error))),
      messages: errors.map((error) => redact(error.message)),
    }));
    if (!profileGone || !pidGone) throw new Error("cleanup incomplete");
    if (thrown) throw thrown;
    throw new Error("launch poll resolved");
  } finally {
    delete process.env.DEMO_MARKER;
    await rm(root, { recursive: true, force: true });
  }
}

function failureTypes(stdout) {
  return [...stdout.matchAll(/failureType: '([^']+)'/g)].map((match) => match[1]);
}

function assertNoAsyncLeak(text) {
  if (/unhandledRejection|UnhandledPromiseRejection|PromiseRejectionHandledWarning|asynchronous activity after the test ended|rejected after the test/i.test(text)) {
    throw new Error(`probe observed unhandled or late async: ${redact(text).slice(0, 500)}`);
  }
}

async function runProbe(kind) {
  const root = await mkdtemp(join(tmpdir(), "demo-lifecycle-runner-"));
  const reportPath = join(root, "report.json");
  const sidePath = join(root, "owner.json");
  const env = {
    ...process.env,
    DEMO_LIFECYCLE_PROBE: kind,
    DEMO_LIFECYCLE_REPORT: reportPath,
    DEMO_SIDE: sidePath,
  };
  for (const name of ["DEMO_CHROME_STARTUP_DIR", "DEMO_LAUNCHER", "DEMO_CHROME_TRACE", "NODE_OPTIONS", "NODE_TEST_CONTEXT", "FORCE_COLOR", "NO_COLOR", "DEMO_MARKER"]) {
    delete env[name];
  }
  const child = spawn(process.execPath, ["--test", "--test-reporter=tap", testFile], {
    cwd: repoRoot,
    env,
    stdio: ["ignore", "pipe", "pipe"],
    detached: true,
  });
  let stdout = "";
  let stderr = "";
  const killGroup = () => {
    if (!Number.isInteger(child.pid)) return;
    if (child.exitCode !== null || child.signalCode !== null) return;
    try { process.kill(-child.pid, "SIGKILL"); } catch { /* group already gone */ }
  };
  const timer = setTimeout(killGroup, 8000);
  try {
    child.stdout.on("data", (chunk) => { stdout += chunk; });
    child.stderr.on("data", (chunk) => { stderr += chunk; });
    const code = await new Promise((resolve, reject) => {
      child.once("error", reject);
      child.once("exit", resolve);
    });
    let reportText = "";
    try { reportText = await readFile(reportPath, "utf8"); }
    catch {
      throw new Error(`probe ${kind} produced no report (code=${code}): ${redact(`${stdout}\n${stderr}`).slice(0, 500)}`);
    }
    return { code, stdout, stderr, report: JSON.parse(reportText) };
  } finally {
    clearTimeout(timer);
    killGroup();
    await rm(root, { recursive: true, force: true });
  }
}

const probe = process.env.DEMO_LIFECYCLE_PROBE ?? "";
if (probe === "early-noncancellation" || probe === "poll-expiry") {
  test(`probe ${probe}`, async () => { await probeCase(probe); });
} else if (probe !== "") {
  throw new Error("unknown lifecycle probe");
} else {

test("early exit reports status and sanitized stderr, drains floods, removes profile", async () => {
  const root = await mkdtemp(join(tmpdir(), "demo-chrome-test-"));
  const marker = join(root, "marker"); process.env.DEMO_MARKER = marker;
  try {
    const binary = await fake(root, setup + `process.stderr.write('pthread_create: Resource temporarily unavailable demo-private-value\\n' + 'x'.repeat(200000)); process.stderr.end(()=>process.exit(7));`);
    const start = Date.now();
    await assert.rejects(launchChrome(binary, { launchTimeoutMs: 5000 }), (err) => {
      assert.match(err.message, /exited before readiness \(code=7, signal=null\)/);
      assert.match(err.message, /pthread-create-resource-unavailable/);
      assert.doesNotMatch(err.message, /demo-private-value/);
      return true;
    });
    assert.ok(Date.now() - start < 3000);
    const { profile, pid } = JSON.parse(await readFile(marker, "utf8"));
    await absent(profile); assert.throws(() => process.kill(pid, 0), { code: "ESRCH" });
  } finally { delete process.env.DEMO_MARKER; await rm(root, { recursive: true, force: true }); }
});

test("live timeout and cancellation clean process and profile", async () => {
  const root = await mkdtemp(join(tmpdir(), "demo-chrome-test-"));
  const marker = join(root, "marker"); process.env.DEMO_MARKER = marker;
  try {
    const binary = await fake(root, setup + `process.stderr.write("demo-unknown-private-value"); setInterval(()=>{}, 1000);`);
    await assert.rejects(launchChrome(binary, { launchTimeoutMs: 1500 }), (err) => {
      assert.match(err.message, /stayed alive without DevToolsActivePort/);
      assert.match(err.message, /stderr_categories=none/);
      assert.doesNotMatch(err.message, /demo-unknown-private-value/);
      return true;
    });
    let info = JSON.parse(await readFile(marker, "utf8"));
    await absent(info.profile); assert.throws(() => process.kill(info.pid, 0), { code: "ESRCH" });
    await rm(marker);
    let cancel;
    const pending = launchChrome(binary, { launchTimeoutMs: 5000, onOwnership: (dispose) => { cancel = dispose; } });
    info = await drainOwnedLaunch({ pending, takeCancel: () => cancel, marker, polls: 100, intervalMs: 20 });
    await absent(info.profile); assert.throws(() => process.kill(info.pid, 0), { code: "ESRCH" });
  } finally { delete process.env.DEMO_MARKER; await rm(root, { recursive: true, force: true }); }
});

test("spawn failure and immediate cancellation release ownership", async () => {
  const root = await mkdtemp(join(tmpdir(), "demo-chrome-test-"));
  const originalTmpdir = process.env.TMPDIR;
  process.env.TMPDIR = root;
  try {
    const bad = join(root, "invalid");
    await writeFile(bad, "#!/demo-nonexistent-chrome-interpreter\n"); await chmod(bad, 0o755);
    let cleanup;
    await assert.rejects(launchChrome(bad, { onOwnership: fn => { cleanup = fn; } }), /(?:failed to spawn Chrome|Chrome spawn failed).*ENOENT/);
    await cleanup();
    const binary = await fake(root, "setInterval(()=>{}, 1000);");
    await assert.rejects(launchChrome(binary, { onOwnership: fn => { void fn(); } }), /launch cancelled/);
    assert.equal((await readdir(root)).filter(name => name.startsWith("presentation-harness-profile-")).length, 0);
  } finally {
    if (originalTmpdir === undefined) delete process.env.TMPDIR; else process.env.TMPDIR = originalTmpdir;
    await rm(root, { recursive: true, force: true });
  }
});

test("correction client exposes only sanitized startup diagnostics", async () => {
  const root = await mkdtemp(join(tmpdir(), "demo-chrome-test-"));
  try {
    const binary = await fake(root, `process.stderr.write('cannot allocate memory demo-private-value'); process.exit(9);`);
    const client = new URL("../../../tests/helpers/correction_browser_client.mjs", import.meta.url);
    const env = { ...process.env, PRESENTATION_HARNESS_CHROME: binary, DEMO_CHROME_TRACE: join(root, "unexpected-trace") };
    delete env.DEMO_CHROME_TRACE;
    const child = spawn(process.execPath, [client.pathname, "http://127.0.0.1:1", "calculate-dropped"], {
      env, stdio: ["ignore", "ignore", "pipe"],
    });
    let stderr = ""; child.stderr.on("data", chunk => { stderr += chunk; });
    const code = await new Promise((resolve, reject) => { child.once("error", reject); child.once("close", resolve); });
    assert.equal(code, 1);
    assert.match(stderr, /exited before readiness \(code=9, signal=null\)/);
    assert.match(stderr, /cannot-allocate-memory/);
    assert.doesNotMatch(stderr, /demo-private-value|demo-chrome-test-/);
    await absent(join(root, "unexpected-trace"));
  } finally { await rm(root, { recursive: true, force: true }); }
});

test("early noncancellation during marker poll is an ordinary failure", async () => {
  const result = await runProbe("early-noncancellation");
  assert.equal(result.code, 1);
  assert.deepEqual(failureTypes(result.stdout), ["testCodeFailure"]);
  assertNoAsyncLeak(`${result.stdout}\n${result.stderr}`);
  assert.equal(result.report.name, "AggregateError");
  assert.equal(result.report.duringPoll, true);
  assert.equal(result.report.profileGone, true);
  assert.equal(result.report.pidGone, true);
  assert.equal(result.report.leaves, 2);
  assert.equal(result.report.markerCode, "ENOENT");
  assert.equal(result.report.assertionName, "AssertionError");
  assert.equal(result.report.sawExit, true);
});

test("marker poll expiry while launch is pending cleans up without a late rejection", async () => {
  const result = await runProbe("poll-expiry");
  assert.equal(result.code, 1);
  assert.deepEqual(failureTypes(result.stdout), ["testCodeFailure"]);
  assertNoAsyncLeak(`${result.stdout}\n${result.stderr}`);
  assert.equal(result.report.name, "Error");
  assert.equal(result.report.duringPoll, false);
  assert.equal(result.report.profileGone, true);
  assert.equal(result.report.pidGone, true);
  assert.equal(result.report.leaves, 1);
  assert.equal(result.report.markerCode, "ENOENT");
  assert.equal(result.report.assertionName, null);
  assert.equal(result.report.sawExit, false);
});

}
