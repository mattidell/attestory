import test from "node:test";
import assert from "node:assert/strict";
import { chmod, mkdtemp, readdir, rm, stat, symlink, writeFile } from "node:fs/promises";
import { dirname, join, relative, resolve, sep } from "node:path";
import { fileURLToPath } from "node:url";
import { tmpdir } from "node:os";
import { spawn } from "node:child_process";

const here = dirname(fileURLToPath(import.meta.url));
const repoRoot = resolve(here, "../../..");
const runner = join(repoRoot, "tools", "presentation_harness", "run.mjs");
const profilePrefix = "presentation-harness-profile-";

function repoRelative(path) {
  return relative(repoRoot, path).split(sep).join("/");
}

async function runHarness(args, { env = {}, timeoutMs = 15000 } = {}) {
  const child = spawn(process.execPath, [runner, ...args], {
    cwd: repoRoot,
    env: { ...process.env, ...env },
    stdio: ["ignore", "pipe", "pipe"],
  });
  let stdout = "";
  let stderr = "";
  child.stdout.on("data", (chunk) => { stdout += chunk; });
  child.stderr.on("data", (chunk) => { stderr += chunk; });
  const result = await new Promise((resolveResult, reject) => {
    const timer = setTimeout(() => {
      child.kill("SIGKILL");
      reject(new Error("repair battery child timed out"));
    }, timeoutMs);
    child.once("error", (error) => {
      clearTimeout(timer);
      reject(error);
    });
    child.once("exit", (code, signal) => {
      clearTimeout(timer);
      resolveResult({ code, signal, stdout, stderr, child });
    });
  });
  return result;
}

async function waitForExit(child, timeoutMs = 10000) {
  return new Promise((resolveExit, reject) => {
    const timer = setTimeout(() => reject(new Error("signal cleanup child timed out")), timeoutMs);
    child.once("exit", (code, signal) => {
      clearTimeout(timer);
      resolveExit({ code, signal });
    });
  });
}

async function profileNames() {
  const entries = await readdir(tmpdir(), { withFileTypes: true });
  return new Set(entries.filter((entry) => entry.name.startsWith(profilePrefix)).map((entry) => entry.name));
}

async function profileReady(name) {
  try {
    await stat(join(tmpdir(), name, "DevToolsActivePort"));
    return true;
  } catch {
    return false;
  }
}

async function writeManifest(root, name, manifest) {
  const path = join(root, name);
  await writeFile(path, `${JSON.stringify(manifest, null, 2)}\n`, "utf8");
  return path;
}

function baseManifest(root, candidateName) {
  const candidatePath = join(root, candidateName);
  const fixturePath = join(root, "fixture.json");
  return {
    version: "presentation-evaluation-manifest.v1",
    id: "demo-repair-battery",
    timeout_ms: 5000,
    candidates: [{ id: "candidate", path: repoRelative(candidatePath) }],
    fixtures: [{ id: "fixture", path: repoRelative(fixturePath), synthetic: true }],
    criteria: [
      { id: "local-clean", check: "dom-text-present", params: { selector: "#local", expected_text: "clean" } },
      { id: "cookie-clean", check: "dom-text-present", params: { selector: "#cookie", expected_text: "clean" } },
      { id: "injection-ran", check: "dom-text-present", params: { selector: "#injection", expected_text: "injected" } },
      { id: "keyboard-shape", check: "keyboard-focus-reachable", params: { selector: "#injection", tab_presses: 1 } },
    ],
    tamper_cases: [
      { id: "tuple-one", injection: null },
      { id: "tuple-two", injection: null },
      {
        id: "valid-injection",
        injection: "document.addEventListener('DOMContentLoaded', function(){ document.getElementById('injection').textContent = 'injected'; });",
      },
    ],
    matrix: [
      { candidate_id: "candidate", fixture_id: "fixture", tamper_case_id: "tuple-one", criteria: ["local-clean", "cookie-clean"] },
      { candidate_id: "candidate", fixture_id: "fixture", tamper_case_id: "tuple-two", criteria: ["local-clean", "cookie-clean"] },
      { candidate_id: "candidate", fixture_id: "fixture", tamper_case_id: "valid-injection", criteria: ["injection-ran"] },
    ],
  };
}

async function makeFakeChrome(root, markerPath) {
  const fake = join(root, "fake-chrome.mjs");
  await writeFile(
    fake,
    `#!/usr/bin/env node\nimport { writeFileSync } from 'node:fs';\nwriteFileSync(${JSON.stringify(markerPath)}, 'started');\nsetInterval(() => {}, 1000);\n`,
    "utf8",
  );
  await chmod(fake, 0o755);
  return fake;
}

test("real-Chrome repair battery closes F1-F6 twice with deterministic correctness output", async () => {
  const root = await mkdtemp(join(repoRoot, "tools/presentation_harness/.repair-battery-"));
  const externalRoot = await mkdtemp(join(tmpdir(), "presentation-harness-external-"));
  const beforeProfiles = await profileNames();
  try {
    await writeFile(join(root, "fixture.json"), "{}\n", "utf8");
    await writeFile(
      join(root, "candidate.html"),
      `<!doctype html><body><div id="local">unknown</div><div id="cookie">unknown</div><div id="injection">untouched</div><script>const localLeak=localStorage.getItem('demo-state')!==null; const cookieLeak=document.cookie.includes('demo-cookie=1'); localStorage.setItem('demo-state','set'); document.cookie='demo-cookie=1; path=/'; document.querySelector('#local').textContent=localLeak?'leaked':'clean'; document.querySelector('#cookie').textContent=cookieLeak?'leaked':'clean';</script></body>`,
      "utf8",
    );
    const manifest = baseManifest(root, "candidate.html");
    const manifestPath = await writeManifest(root, "manifest.json", manifest);
    const manifestName = repoRelative(manifestPath);

    const first = await runHarness(["--manifest", `./${manifestName}`]);
    const second = await runHarness(["--manifest", `./${manifestName}`]);
    assert.equal(first.code, 0, first.stderr);
    assert.equal(second.code, 0, second.stderr);
    assert.equal(first.stdout, second.stdout, "normalized report must be byte-identical across reruns");
    const report = JSON.parse(first.stdout);
    assert.equal(report.manifest_name, manifestName);
    assert.equal(report.counts.pass, 5);
    assert.equal(report.counts.error, 0);
    assert.equal(first.stderr.includes(`"provenance": "${manifestName}"`), true);

    const invalidInjection = structuredClone(manifest);
    invalidInjection.tamper_cases[2].injection = "function {";
    const invalidInjectionPath = await writeManifest(root, "invalid-injection.json", invalidInjection);
    const invalidInjectionRun = await runHarness(["--manifest", repoRelative(invalidInjectionPath)]);
    assert.equal(invalidInjectionRun.code, 2);
    assert.equal(JSON.parse(invalidInjectionRun.stderr).reason, "manifest-invalid");
    assert.equal(invalidInjectionRun.stdout, "");

    const strictMutations = [
      ["missing-parameter", (value) => { delete value.criteria[0].params.expected_text; }],
      ["unknown-parameter", (value) => { value.criteria[0].params.unexpected = "demo-secret"; }],
      ["wrong-selector-type", (value) => { value.criteria[0].params.selector = 4; }],
      ["negative-tabs", (value) => { value.criteria[3].params.tab_presses = -1; }],
      ["empty-matrix", (value) => { value.matrix = []; }],
    ];
    for (const [name, mutate] of strictMutations) {
      const mutated = structuredClone(manifest);
      mutate(mutated);
      const mutatedPath = await writeManifest(root, `${name}.json`, mutated);
      const result = await runHarness(["--manifest", repoRelative(mutatedPath)]);
      assert.equal(result.code, 2, name);
      assert.equal(JSON.parse(result.stderr).reason, "manifest-invalid", name);
      assert.equal(result.stdout, "", name);
    }

    const outsideManifest = await writeManifest(externalRoot, "outside.json", manifest);
    const symlinkPath = join(root, "symlink.json");
    await symlink(outsideManifest, symlinkPath);
    const symlinkRun = await runHarness(["--manifest", repoRelative(symlinkPath)]);
    assert.equal(symlinkRun.code, 2);
    assert.equal(JSON.parse(symlinkRun.stderr).reason, "manifest-invalid");
    assert.equal(symlinkRun.stderr.includes(outsideManifest), false);

    const traversalRun = await runHarness(["--manifest", `${dirname(manifestName)}/../${dirname(manifestName).split("/").at(-1)}/${manifestName.split("/").at(-1)}`]);
    assert.equal(traversalRun.code, 2);
    assert.equal(JSON.parse(traversalRun.stderr).reason, "manifest-invalid");

    const unknownArgument = await runHarness(["--manifest", manifestName, "--demo-rejected-value"]);
    assert.equal(unknownArgument.code, 2);
    assert.equal(JSON.parse(unknownArgument.stderr).message, "manifest rejected");
    assert.equal(unknownArgument.stderr.includes("demo-rejected-value"), false);

    const fakeMarker = join(root, "fake-started");
    const fakeChrome = await makeFakeChrome(root, fakeMarker);
    const launchProfilesBefore = await profileNames();
    const launchChild = spawn(process.execPath, [runner, "--manifest", manifestName, "--chrome", fakeChrome], {
      cwd: repoRoot,
      env: process.env,
      stdio: ["ignore", "pipe", "pipe"],
    });
    for (let i = 0; i < 100; i += 1) {
      try { await stat(fakeMarker); break; } catch { await new Promise((resolveDelay) => setTimeout(resolveDelay, 20)); }
    }
    launchChild.kill("SIGINT");
    const launchExit = await waitForExit(launchChild);
    assert.equal(launchExit.code, 2);
    const launchProfilesAfter = await profileNames();
    assert.deepEqual([...launchProfilesAfter].filter((name) => !launchProfilesBefore.has(name)), []);

    await writeFile(
      join(root, "slow.html"),
      "<!doctype html><body><p id='slow'>slow</p><script>const until=Date.now()+5000; while(Date.now()<until) {}</script></body>",
      "utf8",
    );
    const slowManifest = structuredClone(manifest);
    slowManifest.candidates[0].path = repoRelative(join(root, "slow.html"));
    slowManifest.criteria = [{ id: "slow", check: "dom-text-present", params: { selector: "#slow", expected_text: "slow" } }];
    slowManifest.tamper_cases = [{ id: "slow", injection: null }];
    slowManifest.matrix = [{ candidate_id: "candidate", fixture_id: "fixture", tamper_case_id: "slow", criteria: ["slow"] }];
    const slowManifestPath = await writeManifest(root, "slow.json", slowManifest);
    const postLaunchProfilesBefore = await profileNames();
    const postLaunchChild = spawn(process.execPath, [runner, "--manifest", repoRelative(slowManifestPath)], {
      cwd: repoRoot,
      env: process.env,
      stdio: ["ignore", "pipe", "pipe"],
    });
    let readyProfile = null;
    for (let i = 0; i < 250 && !readyProfile; i += 1) {
      const names = await profileNames();
      for (const name of names) {
        if (!postLaunchProfilesBefore.has(name) && await profileReady(name)) readyProfile = name;
      }
      if (!readyProfile) await new Promise((resolveDelay) => setTimeout(resolveDelay, 20));
    }
    assert.ok(readyProfile, "post-launch signal must observe DevToolsActivePort");
    postLaunchChild.kill("SIGTERM");
    const postLaunchExit = await waitForExit(postLaunchChild);
    assert.equal(postLaunchExit.code, 2);
    const postLaunchProfilesAfter = await profileNames();
    assert.deepEqual([...postLaunchProfilesAfter].filter((name) => !postLaunchProfilesBefore.has(name)), []);
  } finally {
    await rm(root, { recursive: true, force: true });
    await rm(externalRoot, { recursive: true, force: true });
    const afterProfiles = await profileNames();
    assert.deepEqual([...afterProfiles].filter((name) => !beforeProfiles.has(name)), []);
  }
});
