import test from "node:test";
import assert from "node:assert/strict";
import { spawn } from "node:child_process";
import { chmod, mkdtemp, readFile, rm, writeFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { pathToFileURL } from "node:url";
import { acquireStartupSlot } from "../lib/startup-coordinator.mjs";

function run(script, env) {
  const child = spawn(process.execPath, ["--input-type=module", "-e", script], { env: { ...process.env, ...env }, stdio: ["ignore", "pipe", "pipe"] });
  let stderr = ""; child.stderr.on("data", x => { stderr += x; });
  return { child, done: new Promise((resolve, reject) => { child.once("error", reject); child.once("close", code => code === 0 ? resolve() : reject(new Error(`child failed ${code}: ${stderr}`))); }) };
}

test("separate launch processes serialize startup but release before ready-browser work", async () => {
  const root = await mkdtemp(join(tmpdir(), "demo-startup-gate-"));
  try {
    const events = join(root, "events"); const fake = join(root, "chrome");
    await writeFile(fake, `#!/usr/bin/env node\nimport {appendFileSync,writeFileSync} from 'node:fs';\nconst p=process.argv.find(x=>x.startsWith('--user-data-dir=')).slice(16);\nappendFileSync(process.env.DEMO_EVENTS,JSON.stringify({kind:'start',t:Date.now(),pid:process.pid})+'\\n');\nsetTimeout(()=>{writeFileSync(p+'/DevToolsActivePort','12345\\n/demo');appendFileSync(process.env.DEMO_EVENTS,JSON.stringify({kind:'ready',t:Date.now(),pid:process.pid})+'\\n');},700);\nsetInterval(()=>{},1000);`);
    await chmod(fake, 0o755);
    const moduleUrl = process.env.DEMO_LAUNCHER ? pathToFileURL(process.env.DEMO_LAUNCHER).href : new URL("../lib/chrome.mjs", import.meta.url).href;
    const script = `import {launchChrome} from ${JSON.stringify(moduleUrl)}; const b=await launchChrome(process.env.DEMO_FAKE); await new Promise(r=>setTimeout(r,1500)); await b.dispose();`;
    const env = { DEMO_CHROME_STARTUP_DIR: root, DEMO_FAKE: fake, DEMO_EVENTS: events };
    const a = run(script, env), b = run(script, env);
    await Promise.all([a.done, b.done]);
    const rows = (await readFile(events, "utf8")).trim().split("\n").map(JSON.parse);
    assert.equal(rows.length, 4);
    const sorted = rows.sort((x,y) => x.t-y.t);
    assert.deepEqual(sorted.map(x => x.kind), ["start", "ready", "start", "ready"]);
    assert.ok(sorted[2].t - sorted[1].t < 1500, "second start occurs while first ready browser remains alive");
  } finally { await rm(root, { recursive: true, force: true }); }
});

test("queue cancellation and abandoned holder fail without stealing slot", async () => {
  const root = await mkdtemp(join(tmpdir(), "demo-startup-gate-"));
  try {
    const moduleUrl = new URL("../lib/startup-coordinator.mjs", import.meta.url).href;
    const holder = run(`import {acquireStartupSlot} from ${JSON.stringify(moduleUrl)}; await acquireStartupSlot(process.env.DEMO_ROOT); process.stdout.write('ready\\n'); setInterval(()=>{},1000);`, { DEMO_ROOT: root });
    await new Promise(resolve => holder.child.stdout.once("data", resolve));
    let cancelled = false; setTimeout(() => { cancelled = true; }, 100);
    await assert.rejects(acquireStartupSlot(root, { timeoutMs: 1000, cancelled: () => cancelled }), /queue cancelled/);
    holder.child.kill("SIGKILL"); await holder.done.catch(() => {});
    await assert.rejects(acquireStartupSlot(root, { timeoutMs: 150 }), /queue timed out/);
    await assert.rejects(acquireStartupSlot(root, { timeoutMs: 150 }), /queue timed out/);
  } finally { await rm(root, { recursive: true, force: true }); }
});

test("slot release failure cleans a ready browser and preserves original launch failure", async t => {
  if (typeof process.getuid === "function" && process.getuid() === 0) { t.skip("root bypasses directory permissions"); return; }
  const root = await mkdtemp(join(tmpdir(), "demo-gate-release-"));
  const previous = process.env.DEMO_CHROME_STARTUP_DIR;
  process.env.DEMO_CHROME_STARTUP_DIR = root;
  try {
    const moduleUrl = new URL("../lib/chrome.mjs", import.meta.url).href;
    const { launchChrome } = await import(moduleUrl);
    for (const mode of ["ready", "exit"]) {
      const fake = join(root, "fake"); const marker = join(root, "marker");
      await writeFile(fake, `#!/usr/bin/env node\nimport {writeFileSync,chmodSync} from 'node:fs';\nconst p=process.argv.find(x=>x.startsWith('--user-data-dir=')).slice(16);\nwriteFileSync(${JSON.stringify(marker)},JSON.stringify({profile:p,pid:process.pid}));\nchmodSync(${JSON.stringify(root)},0o555);\n${mode === "ready" ? "writeFileSync(p+'/DevToolsActivePort','12345\\n/demo');setInterval(()=>{},1000);" : "process.exit(7);"}`);
      await chmod(fake, 0o755);
      try {
        await assert.rejects(launchChrome(fake, { launchTimeoutMs: 5000 }), mode === "ready" ? /queue release failed/ : /exited before readiness \(code=7/);
      } finally { await chmod(root, 0o755); }
      const { profile, pid } = JSON.parse(await readFile(marker, "utf8"));
      await assert.rejects(import("node:fs/promises").then(fs => fs.stat(profile)), { code: "ENOENT" });
      assert.throws(() => process.kill(pid, 0), { code: "ESRCH" });
      await rm(join(root, "chrome-startup-slot"), { recursive: true, force: true });
    }
  } finally {
    if (previous === undefined) delete process.env.DEMO_CHROME_STARTUP_DIR; else process.env.DEMO_CHROME_STARTUP_DIR = previous;
    await chmod(root, 0o755); await rm(root, { recursive: true, force: true });
  }
});

test("observer records queue wait separately from active startup and queue failure", async () => {
  const root = await mkdtemp(join(tmpdir(), "demo-gate-timing-"));
  const previous = process.env.DEMO_CHROME_STARTUP_DIR;
  process.env.DEMO_CHROME_STARTUP_DIR = root;
  try {
    const { launchChrome } = await import("../lib/chrome.mjs");
    const { createObservation } = await import("../lib/chrome-observation.mjs");
    const output = join(root, "trace"); const fake = join(root, "fake");
    await writeFile(fake, `#!/usr/bin/env node\nimport {writeFileSync} from 'node:fs';\nconst p=process.argv.find(x=>x.startsWith('--user-data-dir=')).slice(16);\nwriteFileSync(p+'/DevToolsActivePort','12345\\n/demo'); setInterval(()=>{},1000);`);
    await chmod(fake, 0o755);
    const held = await acquireStartupSlot(root);
    const pending = launchChrome(fake, { observer: createObservation({ label: "isolated", output }), launchTimeoutMs: 3000 });
    await new Promise(resolve=>setTimeout(resolve, 700)); await held.release();
    const browser = await pending; await browser.dispose();
    const holdAgain = await acquireStartupSlot(root);
    await assert.rejects(launchChrome(fake, { queueTimeoutMs: 150, observer: createObservation({ label: "isolated", output }) }), /queue timed out/);
    await holdAgain.release();
    const traces = (await readFile(output, "utf8")).trim().split("\n").map(JSON.parse);
    assert.ok(traces[0].queue_ms >= 650); assert.ok(traces[0].readiness_ms < 3000);
    assert.equal(traces[1].outcome, "queue_failed"); assert.equal(traces[1].elapsed_ms, null);
    assert.ok(traces[1].queue_ms >= 150);
  } finally {
    if (previous === undefined) delete process.env.DEMO_CHROME_STARTUP_DIR; else process.env.DEMO_CHROME_STARTUP_DIR = previous;
    await rm(root, { recursive: true, force: true });
  }
});

test("dead startup holder cannot be stolen while its browser still runs", async () => {
  const root = await mkdtemp(join(tmpdir(), "demo-gate-crash-"));
  let browserPid = null;
  try {
    const fake = join(root, "chrome"); const marker = join(root, "marker");
    await writeFile(fake, `#!/usr/bin/env node\nimport {writeFileSync} from 'node:fs';\nconst p=process.argv.find(x=>x.startsWith('--user-data-dir=')).slice(16);writeFileSync(${JSON.stringify(marker)},JSON.stringify({pid:process.pid,profile:p}));setInterval(()=>{},1000);`);
    await chmod(fake, 0o755);
    const moduleUrl = new URL("../lib/chrome.mjs", import.meta.url).href;
    const holder = run(`import {launchChrome} from ${JSON.stringify(moduleUrl)}; await launchChrome(process.env.DEMO_FAKE);`, { DEMO_CHROME_STARTUP_DIR: root, DEMO_FAKE: fake });
    let info;
    for (let i=0;i<300;i++) { try { info=JSON.parse(await readFile(marker,"utf8")); break; } catch { await new Promise(r=>setTimeout(r,20)); } }
    assert.ok(info); browserPid = info.pid;
    holder.child.kill("SIGKILL"); await holder.done.catch(()=>{});
    process.kill(browserPid, 0);
    await assert.rejects(acquireStartupSlot(root, { timeoutMs: 150 }), /queue timed out/);
    process.kill(browserPid, "SIGKILL"); browserPid = null;
    await rm(info.profile, { recursive:true, force:true });
  } finally {
    if (browserPid !== null) { try { process.kill(browserPid,"SIGKILL"); } catch {} }
    await rm(root, { recursive:true, force:true });
  }
});
