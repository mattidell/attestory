import { CDPClient } from "../../tools/presentation_harness/lib/cdp.mjs";
import { launchChrome } from "../../tools/presentation_harness/lib/chrome.mjs";
import { completeJourney } from "./entry_loop_journey.mjs";

// Track 4: the one durable focus-indicator check. Enumerates every
// focusable control reachable by Tab from the rendered, compiled page (in
// both the incomplete and complete states), and for each one asserts the
// general invariant rather than a per-control or per-colour rule: the focus
// style must differ from the resting style, and some component of the focus
// indicator (outline or box-shadow) must measure at least 3:1 against the
// background adjacent to the control -- computed from the page's actual
// rendered colours at run time, never against a stored value. A control
// added later that has no focus treatment fails this the same way #w2-box1
// did; a palette change that keeps some component above 3:1 keeps passing.

const pageUrl = process.argv[2];
if (!pageUrl) {
  process.stderr.write("entry-focus-indicator-probe-failed\n");
  process.exit(1);
}

let chrome;
let client;
let targetId;
let sessionId;

async function evaluate(expression) {
  const result = await client.send(
    "Runtime.evaluate",
    { expression, awaitPromise: true, returnByValue: true },
    sessionId,
  );
  if (result.exceptionDetails) {
    throw new Error("browser-evaluation-failed");
  }
  return result.result.value;
}

async function waitUntil(expression, timeoutMs = 10000) {
  const deadline = Date.now() + timeoutMs;
  while (Date.now() < deadline) {
    if (await evaluate(expression)) return;
    await new Promise((resolve) => setTimeout(resolve, 25));
  }
  throw new Error("browser-state-timeout");
}

async function pressTab(shift = false) {
  await client.send(
    "Input.dispatchKeyEvent",
    {
      type: "rawKeyDown",
      key: "Tab",
      code: "Tab",
      windowsVirtualKeyCode: 9,
      modifiers: shift ? 8 : 0,
    },
    sessionId,
  );
  await client.send(
    "Input.dispatchKeyEvent",
    {
      type: "keyUp",
      key: "Tab",
      code: "Tab",
      windowsVirtualKeyCode: 9,
      modifiers: shift ? 8 : 0,
    },
    sessionId,
  );
  await new Promise((resolve) => setTimeout(resolve, 40));
}

// Injected into the page: computes the WCAG contrast ratio between two
// colours, and reads a control's own resting/focus style plus the first
// non-transparent background colour among its ancestors, all from live
// getComputedStyle values -- nothing here is a stored snapshot.
const PAGE_HELPERS = `
  function parseRgb(text) {
    const found = (text || "").match(/rgba?\\(([^)]+)\\)/);
    if (!found) return null;
    const parts = found[1].split(",").map((part) => parseFloat(part.trim()));
    const [r, g, b, a = 1] = parts;
    if (a === 0) return null;
    return [r, g, b];
  }
  function relativeLuminance([r, g, b]) {
    const linear = (c) => {
      const n = c / 255;
      return n <= 0.04045 ? n / 12.92 : Math.pow((n + 0.055) / 1.055, 2.4);
    };
    const [R, G, B] = [linear(r), linear(g), linear(b)];
    return 0.2126 * R + 0.7152 * G + 0.0722 * B;
  }
  function contrastRatio(a, b) {
    const l1 = relativeLuminance(a);
    const l2 = relativeLuminance(b);
    const lighter = Math.max(l1, l2);
    const darker = Math.min(l1, l2);
    return (lighter + 0.05) / (darker + 0.05);
  }
  function adjacentBackground(el) {
    let node = el.parentElement;
    while (node) {
      const rgb = parseRgb(getComputedStyle(node).backgroundColor);
      if (rgb) return rgb;
      node = node.parentElement;
    }
    return [255, 255, 255];
  }
  function describe(el) {
    if (!el || el === document.body) return null;
    const cs = getComputedStyle(el);
    return {
      key: el.tagName + "#" + (el.id || "") + "." + (el.className || "") + ":" +
        (el.textContent || "").trim().slice(0, 40),
      outlineStyle: cs.outlineStyle,
      outlineWidth: cs.outlineWidth,
      outlineColorRgb: parseRgb(cs.outlineColor),
      boxShadow: cs.boxShadow,
      boxShadowColorRgb: cs.boxShadow === "none" ? null : parseRgb(cs.boxShadow),
      backgroundRgb: adjacentBackground(el),
    };
  }
  window.__focusProbe = { describe, contrastRatio };
  true;
`;

async function describeActive() {
  return evaluate(`window.__focusProbe.describe(document.activeElement)`);
}

async function restingStylesByKey() {
  // Every element that could plausibly be in the Tab order, read in its
  // current (unfocused) resting state, before any Tab press touches it.
  // Keyed the same way describe() keys a focused element, so a focus-style
  // reading can be matched back to its own resting style rather than to
  // whatever control happened to hold focus the instant before it.
  return evaluate(`
    (() => {
      const nodes = document.querySelectorAll(
        'button, input, a[href], [tabindex]'
      );
      const map = {};
      for (const el of nodes) {
        const info = window.__focusProbe.describe(el);
        if (info) map[info.key] = info;
      }
      return map;
    })()
  `);
}

function combinedFocusIndicator(focus) {
  const candidates = [];
  const outlineOn =
    focus.outlineStyle !== "none" &&
    parseFloat(focus.outlineWidth) > 0 &&
    focus.outlineColorRgb !== null;
  if (outlineOn) candidates.push({ component: "outline", rgb: focus.outlineColorRgb });
  if (focus.boxShadowColorRgb !== null) {
    candidates.push({ component: "box-shadow", rgb: focus.boxShadowColorRgb });
  }
  return candidates;
}

const report = [];

try {
  chrome = await launchChrome(null);
  client = await CDPClient.connect(chrome.wsUrl);
  ({ targetId } = await client.send("Target.createTarget", { url: "about:blank" }));
  ({ sessionId } = await client.send("Target.attachToTarget", {
    targetId,
    flatten: true,
  }));
  await client.send("Page.enable", {}, sessionId);
  await client.send("Runtime.enable", {}, sessionId);

  const loaded = client.waitFor("Page.loadEventFired", sessionId, 10000);
  await client.send("Page.navigate", { url: pageUrl }, sessionId);
  await loaded;
  await waitUntil(`document.querySelector("#w2-box1") !== null`);
  await evaluate(PAGE_HELPERS);

  async function sweep(phase) {
    const restingByKey = await restingStylesByKey();
    await evaluate(`document.activeElement && document.activeElement.blur(); true`);
    const seen = new Set();
    // Two entry fields, each with its own input, submit button, and
    // missing/correct affordance, plus one explain-toggle per evaluation
    // line once complete -- comfortably under 30, generous over the
    // single-field count of 15 this used to be.
    for (let i = 0; i < 30; i++) {
      await pressTab();
      const focused = await describeActive();
      if (!focused) continue;
      if (seen.has(focused.key)) continue;
      seen.add(focused.key);
      const resting = restingByKey[focused.key];
      if (!resting) {
        throw new Error(
          `focused control ${focused.key} has no matching resting-state reading`,
        );
      }
      report.push({ phase, resting, focus: focused });
    }
  }

  await sweep("incomplete");

  await completeJourney(evaluate, waitUntil);
  await waitUntil(`document.body.textContent.includes("Accepted")`);
  await sweep("complete");

  const seenKeys = new Set();
  const findings = [];
  for (const entry of report) {
    if (seenKeys.has(entry.focus.key)) continue;
    seenKeys.add(entry.focus.key);
    const candidates = combinedFocusIndicator(entry.focus);
    const differsFromResting =
      entry.focus.outlineStyle !== entry.resting.outlineStyle ||
      entry.focus.boxShadow !== entry.resting.boxShadow;
    const ratios = [];
    for (const candidate of candidates) {
      const ratio = await evaluate(
        `window.__focusProbe.contrastRatio(${JSON.stringify(candidate.rgb)}, ${JSON.stringify(entry.focus.backgroundRgb)})`,
      );
      ratios.push({ component: candidate.component, ratio });
    }
    const passes = differsFromResting && ratios.some((r) => r.ratio >= 3.0);
    findings.push({
      key: entry.focus.key,
      phase: entry.phase,
      differsFromResting,
      ratios,
      passes,
    });
  }

  process.stdout.write(`${JSON.stringify(findings, null, 2)}\n`);
} catch {
  process.stderr.write("entry-focus-indicator-probe-failed\n");
  process.exitCode = 1;
} finally {
  if (client && targetId) {
    try {
      await client.send("Target.closeTarget", { targetId });
    } catch {
      // Cleanup continues through the owned browser process.
    }
  }
  if (client) client.close();
  if (chrome) await chrome.dispose();
}
