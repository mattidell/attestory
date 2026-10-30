import test from "node:test";
import assert from "node:assert/strict";
import { createServer } from "node:http";
import { spawn } from "node:child_process";
import { CDPClient } from "../lib/cdp.mjs";
import { launchChrome, resolveChromeExecutable } from "../lib/chrome.mjs";

async function target(client, contextId, url) {
  const { targetId } = await client.send("Target.createTarget", { url: "about:blank", browserContextId: contextId });
  const { sessionId } = await client.send("Target.attachToTarget", { targetId, flatten: true });
  await client.send("Page.enable", {}, sessionId);
  const loaded = client.waitFor("Page.loadEventFired", sessionId, 10000);
  await client.send("Page.navigate", { url }, sessionId); await loaded;
  return { targetId, sessionId };
}
async function evalIn(client, sessionId, expression) {
  return (await client.send("Runtime.evaluate", { expression, returnByValue: true }, sessionId)).result.value;
}

test("one real browser isolates same-origin contexts and cleans detached borrowers", async t => {
  try { await resolveChromeExecutable(); } catch { t.skip("no local browser"); return; }
  const server = createServer((req,res) => { res.writeHead(200, { "Content-Type": "text/html" }); res.end(req.url === "/error" ? "<!doctype html><div id=choice-list><button>Other</button></div><div id=saved-rows>Recorded answer</div>" : "<!doctype html><title>demo</title>"); });
  await new Promise(resolve => server.listen(0, "127.0.0.1", resolve));
  const url = `http://127.0.0.1:${server.address().port}/`;
  const chrome = await launchChrome(); const client = await CDPClient.connect(chrome.wsUrl);
  try {
    const first = await client.send("Target.createBrowserContext", { disposeOnDetach: true });
    const second = await client.send("Target.createBrowserContext", { disposeOnDetach: true });
    assert.notEqual(first.browserContextId, second.browserContextId);
    const a = await target(client, first.browserContextId, url);
    const b = await target(client, second.browserContextId, url);
    await evalIn(client, a.sessionId, `document.cookie='demo_cookie=demo_value'; localStorage.setItem('demo_key','demo_value'); sessionStorage.setItem('demo_key','demo_value'); window.demo_state='demo_value'`);
    assert.deepEqual(await evalIn(client, b.sessionId, `({cookie:document.cookie, local:localStorage.getItem('demo_key'), session:sessionStorage.getItem('demo_key'), state:window.demo_state ?? null})`), { cookie:"", local:null, session:null, state:null });
    await client.send("Target.disposeBrowserContext", { browserContextId: first.browserContextId });
    await assert.rejects(client.send("Target.disposeBrowserContext", { browserContextId: first.browserContextId }));
    assert.equal(await evalIn(client, b.sessionId, "document.title"), "demo");
    await client.send("Target.disposeBrowserContext", { browserContextId: second.browserContextId });

    const moduleUrl = new URL("../lib/cdp.mjs", import.meta.url).href;
    const script = `import {CDPClient} from ${JSON.stringify(moduleUrl)}; const c=await CDPClient.connect(process.env.DEMO_WS); await c.send('Target.createBrowserContext',{disposeOnDetach:true}); process.stdout.write('ready\\n'); setInterval(()=>{},1000);`;
    const child = spawn(process.execPath, ["--input-type=module", "-e", script], { env: { ...process.env, DEMO_WS: chrome.wsUrl }, stdio: ["ignore", "pipe", "pipe"] });
    await new Promise(resolve => child.stdout.once("data", resolve));
    assert.equal((await client.send("Target.getBrowserContexts")).browserContextIds.length, 1);
    child.kill("SIGKILL"); await new Promise(resolve => child.once("close", resolve));
    for (let i=0;i<100;i++) { if ((await client.send("Target.getBrowserContexts")).browserContextIds.length === 0) break; await new Promise(resolve=>setTimeout(resolve,25)); }
    assert.equal((await client.send("Target.getBrowserContexts")).browserContextIds.length, 0);

    // Exercise the actual borrowed client: a page-driven error and a killed
    // waiting client both release their contexts without closing the owner.
    const realClient = new URL("../../../tests/helpers/correction_browser_client.mjs", import.meta.url);
    function borrowed(path) {
      const env = { ...process.env, DEMO_SHARED_CHROME_WS: chrome.wsUrl };
      delete env.DEMO_CHROME_TRACE;
      return spawn(process.execPath, [realClient.pathname, url + path, "confirmed"], { env, stdio: ["ignore", "ignore", "pipe"] });
    }
    const bad = borrowed("error");
    const badCode = await new Promise(resolve => bad.once("close", resolve));
    assert.notEqual(badCode, 0);
    assert.equal((await client.send("Target.getBrowserContexts")).browserContextIds.length, 0);
    const timed = borrowed("wait");
    for (let i=0;i<200;i++) { if ((await client.send("Target.getBrowserContexts")).browserContextIds.length === 1) break; await new Promise(resolve=>setTimeout(resolve,25)); }
    assert.equal((await client.send("Target.getBrowserContexts")).browserContextIds.length, 1);
    timed.kill("SIGKILL"); await new Promise(resolve => timed.once("close", resolve));
    for (let i=0;i<100;i++) { if ((await client.send("Target.getBrowserContexts")).browserContextIds.length === 0) break; await new Promise(resolve=>setTimeout(resolve,25)); }
    assert.equal((await client.send("Target.getBrowserContexts")).browserContextIds.length, 0);
    assert.equal(chrome.isExited(), false);
    const doomedContext = await client.send("Target.createBrowserContext", { disposeOnDetach: true });
    const doomed = await target(client, doomedContext.browserContextId, url);
    const pending = client.send("Runtime.evaluate", { expression: "new Promise(()=>{})", awaitPromise: true }, doomed.sessionId);
    const failed = assert.rejects(pending, /connection closed/);
    const killer = await CDPClient.connect(chrome.wsUrl);
    try { await killer.send("Browser.close"); } catch { /* closing may interrupt its reply */ }
    await failed;
    killer.close();
  } finally { client.close(); await chrome.dispose(); await new Promise(resolve => server.close(resolve)); }
});
