#!/usr/bin/env node
// Draw saved citation-walk pages in headless Chrome and read every
// safe-render alert. Evidence for page-alerts.md.
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

const READ = `(() => {
  const normalize = (node) => (node?.innerText || "").replace(/\\s+/g, " ").trim();
  const root = document.getElementById("sections-root");
  if (!root) throw new Error("sections-root-missing");
  return new Promise((resolve) => requestAnimationFrame(() => requestAnimationFrame(() => {
    const sections = Array.from(root.children).map((wrap) => {
      const line = wrap.querySelector("section.line");
      return {
        id: wrap.id,
        heading: normalize(line?.querySelector("h2")),
        badge: normalize(line?.querySelector(".badge")),
        value: normalize(line?.querySelector(".line-value")),
        value_aria_label: line?.querySelector(".line-value")?.getAttribute("aria-label") || null,
        explain: normalize(line?.querySelector("p.explain")),
        section_error: normalize(line?.querySelector(".section-error")),
        citation_buttons: line ? line.querySelectorAll("button.citation").length : 0,
        citation_button_labels: line
          ? Array.from(line.querySelectorAll("button.citation")).map((button) => normalize(button))
          : [],
        text: normalize(line).slice(0, 500),
      };
    });
    const attachments = Array.from(document.getElementById("attachment-status-root")?.children || []).map((wrap) => ({
      id: wrap.id,
      heading: normalize(wrap.querySelector("h2")),
      explain: normalize(wrap.querySelector("p.explain, .blocked-banner")),
      section_error: normalize(wrap.querySelector(".section-error")),
    }));
    const other = ["attachment-status-root", "mortgage-explanation-root", "citation-groups-root", "diagnostics-root"]
      .flatMap((elementId) => Array.from(document.getElementById(elementId)?.querySelectorAll(".section-error") || []).map((node) => ({
        id: node.closest("[id]")?.id || elementId,
        text: normalize(node),
      })));
    resolve({
      title: document.title,
      section_count: sections.length,
      alerts: Array.from(document.querySelectorAll(".section-error")).map((node) => ({
        id: node.closest("#sections-root > div")?.id || node.closest("[id]")?.id || "",
        text: normalize(node),
      })),
      other_root_alerts: other,
      attachments,
      sections,
    });
  })));
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
    for (const item of config.cases) cases.push(await observe(client, server.origin, item));
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
