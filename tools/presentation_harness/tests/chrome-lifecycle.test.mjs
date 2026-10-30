import test from "node:test";
import assert from "node:assert/strict";
import { chmod, mkdtemp, readFile, readdir, rm, stat, writeFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { pathToFileURL } from "node:url";

const launcher = process.env.DEMO_LAUNCHER || new URL("../lib/chrome.mjs", import.meta.url).href;
const { launchChrome } = await import(launcher.startsWith("file:") ? launcher : pathToFileURL(launcher).href);

async function fake(root, body) {
  const path = join(root, "chrome");
  await writeFile(path, `#!/usr/bin/env node\n${body}`, "utf8");
  await chmod(path, 0o755);
  return path;
}
async function absent(path) {
  await assert.rejects(stat(path), { code: "ENOENT" });
}
const setup = `import {writeFileSync} from 'node:fs';\nconst profile=process.argv.find(a=>a.startsWith('--user-data-dir=')).split('=').slice(1).join('=');\nwriteFileSync(process.env.DEMO_MARKER, JSON.stringify({profile,pid:process.pid}));\n`;

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
    for (let i = 0; i < 100; i++) { try { await stat(marker); break; } catch { await new Promise(r => setTimeout(r, 20)); } }
    info = JSON.parse(await readFile(marker, "utf8"));
    const rejected = assert.rejects(pending, /launch cancelled/);
    await cancel();
    await rejected;
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
  const { spawn } = await import("node:child_process");
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
