// Process-group cleanup of the harness's Chrome. A synthetic Chrome whose
// helper outlives the main process, holds the inherited stderr pipe and keeps
// writing into the profile reproduces the CI hang without a real browser.
import test from "node:test";
import assert from "node:assert/strict";
import { spawn } from "node:child_process";
import { chmod, mkdir, mkdtemp, readFile, rm, stat, writeFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { fileURLToPath } from "node:url";
import { launchChrome } from "../lib/chrome.mjs";

const fakeChrome = fileURLToPath(new URL("./helpers/fake-chrome-group.mjs", import.meta.url));
const observer = fileURLToPath(new URL("../sale-page-observation.mjs", import.meta.url));

function alive(pid) {
  try { process.kill(pid, 0); return true; } catch (error) { return error.code === "EPERM"; }
}
async function waitFor(predicate, what, timeoutMs = 10000) {
  const deadline = Date.now() + timeoutMs;
  for (;;) {
    const value = await predicate();
    if (value) return value;
    if (Date.now() > deadline) throw new Error(`timed out waiting for ${what}`);
    await new Promise((resolve) => setTimeout(resolve, 25));
  }
}
async function profileOf(stateDir) {
  return waitFor(() => readFile(join(stateDir, "profile.path"), "utf8").catch(() => null), "profile path");
}
async function helperPid(stateDir) {
  return Number(await waitFor(() => readFile(join(stateDir, "helper.pid"), "utf8").catch(() => null), "helper start"));
}
// Never leave the synthetic helper running, whatever the test outcome.
function reap(pid) { if (pid) { try { process.kill(pid, "SIGKILL"); } catch { /* gone */ } } }

test("dispose ends the whole Chrome group, removes a profile a helper was writing into, and frees stderr", async () => {
  const stateDir = await mkdtemp(join(tmpdir(), "demo-group-state-"));
  process.env.DEMO_FAKE_DIR = stateDir;
  process.env.DEMO_FAKE_MODE = "helper";
  let pid = 0;
  try {
    const chrome = await launchChrome(fakeChrome);
    pid = await helperPid(stateDir);
    assert.ok(alive(pid), "helper is running before dispose");
    const profile = await profileOf(stateDir);
    await stat(profile);
    const started = Date.now();
    await chrome.dispose();
    assert.ok(Date.now() - started < 8000, "dispose is bounded");
    assert.equal(alive(pid), false, "helper process was ended");
    await assert.rejects(stat(profile), { code: "ENOENT" }, "profile removed");
  } finally {
    reap(pid);
    await rm(stateDir, { recursive: true, force: true });
    delete process.env.DEMO_FAKE_DIR;
    delete process.env.DEMO_FAKE_MODE;
  }
});

async function runObserver(mode, { cases = 1 } = {}) {
  const cwd = await mkdtemp(join(tmpdir(), "demo-observer-cwd-"));
  const stateDir = join(cwd, "state");
  const outputDir = join(cwd, "temp/sale-page-observation");
  await mkdir(stateDir, { recursive: true });
  await mkdir(outputDir, { recursive: true });
  await writeFile(join(outputDir, "page.html"), "<!doctype html><title>demo</title>");
  await writeFile(join(outputDir, "cases.json"), JSON.stringify({
    timeout_ms: 5000,
    cases: Array.from({ length: cases }, (_, i) => ({
      id: `demo-${i}`, page: "temp/sale-page-observation/page.html", question_text: "demo",
    })),
  }));
  const started = Date.now();
  const child = spawn(process.execPath, [observer, "temp/sale-page-observation/cases.json"], {
    cwd,
    env: { ...process.env, PRESENTATION_HARNESS_CHROME: fakeChrome, DEMO_FAKE_DIR: stateDir, DEMO_FAKE_MODE: mode },
    stdio: ["ignore", "pipe", "pipe"],
  });
  let stdout = ""; let stderr = "";
  child.stdout.on("data", (c) => { stdout += c; });
  child.stderr.on("data", (c) => { stderr += c; });
  // The harness's own bound, so a regression fails here instead of hanging.
  const guard = setTimeout(() => child.kill("SIGKILL"), 30000);
  const { code, signal } = await new Promise((resolve) => child.once("close", (c, s) => resolve({ code: c, signal: s })));
  clearTimeout(guard);
  return { cwd, stateDir, outputDir, elapsedMs: Date.now() - started, code, signal, stdout, stderr };
}

test("observer exits promptly with success once the helper group is ended", async () => {
  const run = await runObserver("helper");
  let pid = 0;
  try {
    pid = await helperPid(run.stateDir);
    assert.equal(run.signal, null, "observer was not killed by the test guard");
    assert.equal(run.code, 0, run.stderr);
    assert.ok(run.elapsedMs < 12000, `observer exit took ${run.elapsedMs} ms`);
    assert.equal(alive(pid), false);
    await assert.rejects(stat(await profileOf(run.stateDir)), { code: "ENOENT" });
    assert.match(run.stdout, /"stage":"cleanup-complete"/);
    const result = JSON.parse(await readFile(join(run.outputDir, "dom-observations.json"), "utf8"));
    assert.equal(result.cleanup_completed, true);
  } finally {
    reap(pid);
    await rm(run.cwd, { recursive: true, force: true });
  }
});

test("observer reports browser-cleanup-failed and exits 2 promptly when the profile cannot be removed", {
  skip: typeof process.getuid === "function" && process.getuid() === 0 ? "root ignores directory permissions" : false,
}, async () => {
  const run = await runObserver("locked");
  try {
    assert.equal(run.signal, null, "observer was not killed by the test guard");
    assert.equal(run.code, 2);
    assert.ok(run.elapsedMs < 12000, `observer exit took ${run.elapsedMs} ms`);
    assert.match(run.stderr, /"reason":"browser-cleanup-failed","category":"cleanup","stage":"cleanup"/);
    assert.match(run.stdout, /"stage":"cleanup-complete"/);
    const result = JSON.parse(await readFile(join(run.outputDir, "dom-observations.json"), "utf8"));
    assert.equal(result.cleanup_completed, false);
  } finally {
    // The unremovable profile is the test's own fixture; remove it here.
    const path = (await readFile(join(run.stateDir, "profile.path"), "utf8").catch(() => "")).trim();
    if (path) {
      await chmod(join(path, "locked"), 0o700).catch(() => {});
      await rm(path, { recursive: true, force: true });
    }
    await rm(run.cwd, { recursive: true, force: true });
  }
});

test("a profile that stays unremovable makes dispose reject instead of hanging", {
  skip: typeof process.getuid === "function" && process.getuid() === 0 ? "root ignores directory permissions" : false,
}, async () => {
  const stateDir = await mkdtemp(join(tmpdir(), "demo-group-state-"));
  process.env.DEMO_FAKE_DIR = stateDir;
  process.env.DEMO_FAKE_MODE = "locked";
  try {
    const chrome = await launchChrome(fakeChrome);
    const started = Date.now();
    await assert.rejects(chrome.dispose(), (error) => ["EACCES", "EPERM", "ENOTEMPTY"].includes(error.code));
    assert.ok(Date.now() - started < 8000);
  } finally {
    const path = (await readFile(join(stateDir, "profile.path"), "utf8").catch(() => "")).trim();
    if (path) {
      await chmod(join(path, "locked"), 0o700).catch(() => {});
      await rm(path, { recursive: true, force: true });
    }
    await rm(stateDir, { recursive: true, force: true });
    delete process.env.DEMO_FAKE_DIR;
    delete process.env.DEMO_FAKE_MODE;
  }
});
