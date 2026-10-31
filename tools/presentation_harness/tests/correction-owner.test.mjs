import test from "node:test";
import assert from "node:assert/strict";
import { spawn } from "node:child_process";
import { chmod, mkdtemp, readFile, rm, stat, writeFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { acquireStartupSlot } from "../lib/startup-coordinator.mjs";

const owner = new URL("../../../tests/helpers/correction_browser_owner.mjs", import.meta.url);
async function waitFile(path) { for (let i=0;i<300;i++) { try { return JSON.parse(await readFile(path, "utf8")); } catch { await new Promise(r=>setTimeout(r,20)); } } throw new Error("fake browser did not start"); }
function start(env) { const childEnv = { ...process.env, ...env }; delete childEnv.DEMO_CHROME_TRACE; return spawn(process.execPath, [owner.pathname], { env: childEnv, stdio: ["pipe", "pipe", "pipe"] }); }
function exited(child) { return new Promise(resolve => child.once("close", resolve)); }

test("owner termination during startup and browser crash clean process and profile", async () => {
  const root = await mkdtemp(join(tmpdir(), "demo-owner-test-"));
  try {
    for (const mode of ["starting", "crash"]) {
      const fake = join(root, "chrome"); const marker = join(root, "marker");
      await writeFile(fake, `#!/usr/bin/env node\nimport {writeFileSync} from 'node:fs';\nconst p=process.argv.find(x=>x.startsWith('--user-data-dir=')).slice(16);\nwriteFileSync(${JSON.stringify(marker)},JSON.stringify({profile:p,pid:process.pid}));\n${mode === "crash" ? "writeFileSync(p+'/DevToolsActivePort','12345\\n/demo');" : ""}\nsetInterval(()=>{},1000);`);
      await chmod(fake, 0o755);
      const child = start({ DEMO_CHROME_STARTUP_DIR: root, PRESENTATION_HARNESS_CHROME: fake });
      const done = exited(child);
      const announced = new Promise(resolve => child.stdout.once("data", resolve));
      const info = await waitFile(marker);
      if (mode === "crash") {
        await announced;
        process.kill(info.pid, "SIGKILL");
      } else child.kill("SIGTERM");
      await done;
      await assert.rejects(stat(info.profile), { code: "ENOENT" });
      assert.throws(() => process.kill(info.pid, 0), { code: "ESRCH" });
      await assert.rejects(stat(join(root,"chrome-startup-slot")), { code:"ENOENT" });
      await rm(marker);
    }
  } finally { await rm(root, { recursive: true, force: true }); }
});

test("owner termination while queued does not take or remove another slot", async () => {
  const root = await mkdtemp(join(tmpdir(), "demo-owner-queue-"));
  try {
    const held = await acquireStartupSlot(root);
    const child = start({ DEMO_CHROME_STARTUP_DIR: root }); const done = exited(child);
    await new Promise(resolve=>setTimeout(resolve,200)); child.kill("SIGTERM"); await done;
    await assert.rejects(acquireStartupSlot(root, { timeoutMs: 150 }), /queue timed out/);
    await held.release();
  } finally { await rm(root, { recursive: true, force: true }); }
});
