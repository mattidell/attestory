#!/usr/bin/env node
// Draw saved citation-walk pages in headless Chrome and read every
// visible text node. Evidence for plain-line-texts P0.
//
//   node observe.mjs <scratch>/browser/cases.json
//
// cases.json: { "root": <pages directory>, "cases": [{ "id", "page" }] }
// where each page is a path relative to root. Writes dom-observations.json
// next to cases.json. Uses the presentation harness's Chrome launcher,
// loopback server and CDP client. Every case gets a fresh browser context.
// Requests that leave the loopback origin are blocked.

import { readFile, writeFile } from "node:fs/promises";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
const STREAM = process.argv.includes("--p0b");

const HARNESS = join(dirname(fileURLToPath(import.meta.url)), "../../../../../tools/presentation_harness/lib");
const { launchChrome } = await import(join(HARNESS, "chrome.mjs"));
const { startLoopbackServer } = await import(join(HARNESS, "server.mjs"));
const { CDPClient } = await import(join(HARNESS, "cdp.mjs"));

const TIMEOUT_MS = 15000;

function withTimeout(promise, ms, label) {
  let timer;
  const timeout = new Promise((_, reject) => { timer = setTimeout(() => reject(new Error(label)), ms); });
  return Promise.race([promise, timeout]).finally(() => clearTimeout(timer));
}

const READ = `(async () => {
  await new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve)));
  function read() {
    const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
    const texts = [];
    while (walker.nextNode()) {
      const node = walker.currentNode;
      const parent = node.parentElement;
      if (!parent || parent.closest("script, style")) continue;
      const text = node.textContent.trim();
      if (!text) continue;
      let visible = true;
      for (let element = parent; element; element = element.parentElement) {
        const style = getComputedStyle(element);
        if (style.display === "none" || style.visibility === "hidden") visible = false;
        if (element.tagName === "DETAILS" && !element.open && !element.querySelector("summary")?.contains(parent)) visible = false;
      }
      if (!visible) continue;
      texts.push({text, section: parent.closest("#sections-root > div")?.id || null,
        role: parent.closest(".shared-explanation") ? "support-trace" :
          parent.closest("button.citation") ? "citation-button" :
          parent.closest(".blocked-reasons") ? "blocked-reason" :
          parent.closest(".explain") ? "explain" :
          parent.closest(".badge") ? "badge" : "other"});
    }
    return texts;
  }
  const initial = read();
  // These are content-bearing panels, not the parked graph support trace.
  for (const detail of document.querySelectorAll("details:not(.shared-explanation)")) detail.open = true;
  await new Promise(resolve => setTimeout(resolve, 0));
  const details = read().filter(row => row.role !== "support-trace");
  // Opening the actual trace controls invokes the production page listeners.
  for (const detail of document.querySelectorAll("details.shared-explanation")) detail.open = true;
  await new Promise(resolve => setTimeout(resolve, 0));
  const trace = read().filter(row => row.role === "support-trace");
  return {initial, details, trace, alerts: Array.from(document.querySelectorAll(".section-error"), node => node.textContent)};
})()`;

async function observe(client, origin, item) {
  const { browserContextId } = await withTimeout(client.send("Target.createBrowserContext", {}), TIMEOUT_MS, "context");
  let targetId;
  let off = null;
  let blocked = false;
  try {
    ({ targetId } = await client.send("Target.createTarget", { url: "about:blank", browserContextId }));
    const { sessionId } = await client.send("Target.attachToTarget", { targetId, flatten: true });
    await client.send("Page.enable", {}, sessionId);
    await client.send("Runtime.enable", {}, sessionId);
    await client.send("Fetch.enable", { patterns: [{ urlPattern: "*" }] }, sessionId);
    off = client.on("Fetch.requestPaused", (params) => {
      if (params.request.url.startsWith(origin)) {
        client.send("Fetch.continueRequest", { requestId: params.requestId }, sessionId).catch(() => {});
      } else {
        blocked = true;
        client.send("Fetch.failRequest", { requestId: params.requestId, errorReason: "BlockedByClient" }, sessionId).catch(() => {});
      }
    }, sessionId);
    const loaded = client.waitFor("Page.loadEventFired", sessionId, TIMEOUT_MS);
    const url = `${origin}/${item.page.split("/").map(encodeURIComponent).join("/")}`;
    const nav = await withTimeout(client.send("Page.navigate", { url }, sessionId), TIMEOUT_MS, "navigate");
    if (nav.errorText) throw new Error("navigate-failed");
    await withTimeout(loaded, TIMEOUT_MS, "load");
    const evaluated = await withTimeout(
      client.send("Runtime.evaluate", { expression: READ, returnByValue: true, awaitPromise: true }, sessionId),
      TIMEOUT_MS, "evaluate",
    );
    if (evaluated.exceptionDetails) throw new Error("evaluate-failed");
    return { id: item.id, non_loopback_request: blocked, ...evaluated.result.value };
  } finally {
    if (off) off();
    if (targetId) await client.send("Target.closeTarget", { targetId }).catch(() => {});
    await client.send("Target.disposeBrowserContext", { browserContextId }).catch(() => {});
  }
}

async function main() {
  const configPath = process.argv[2];
  const config = JSON.parse(await readFile(configPath, "utf8"));
  const server = await startLoopbackServer(config.root, new Set(config.cases.map((c) => c.page)));
  let chrome;
  let client;
  try {
    chrome = await launchChrome(null, {});
    client = await CDPClient.connect(chrome.wsUrl);
    const browser = await withTimeout(client.send("Browser.getVersion"), TIMEOUT_MS, "version");
    const cases = [];
    for (const item of config.cases) {
      const result = await observe(client, server.origin, item);
      if (STREAM) {
        const observation = item.page.replace(/\.html$/, ".dom.json");
        await writeFile(join(config.root, observation), `${JSON.stringify(result)}\n`);
        cases.push({id: item.id, observation, alerts: result.alerts, non_loopback_request: result.non_loopback_request});
      } else cases.push(result);
      if (cases.length % 25 === 0 || cases.length === config.cases.length) process.stdout.write(`[${cases.length}/${config.cases.length}] drawn\n`);
    }
    await writeFile(join(dirname(configPath), "dom-observations.json"),
      `${JSON.stringify({ browser_version: browser.product || null, node_version: process.versions.node, cases }, null, 2)}\n`);
  } finally {
    client?.close();
    if (chrome) await chrome.dispose();
    await server.close();
  }
}

main().catch((error) => {
  process.stderr.write(`observe failed: ${error instanceof Error ? error.message : "unknown"}\n`);
  process.exitCode = 2;
});
