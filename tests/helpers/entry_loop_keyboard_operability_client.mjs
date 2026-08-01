import { CDPClient } from "../../tools/presentation_harness/lib/cdp.mjs";
import { launchChrome } from "../../tools/presentation_harness/lib/chrome.mjs";

// Track 1: the accessibility criterion's unmeasured half -- "every action
// must be reachable with Tab and Shift+Tab and operable with the control's
// standard Enter or Space key" -- made mechanical.
//
// Three checks, expressed as rules over whatever is reachable by Tab from
// the rendered, compiled page, never as a hard-coded control list:
//
//   1. Reverse traversal: the set of controls reached by Tab from a blurred
//      start must equal the set reached by Shift+Tab from the last of them.
//      A control in one set and not the other is reported as a finding, not
//      silently dropped.
//   2. Activation by observed effect: every control classified as
//      actionable by its own DOM shape (a link with an href, a button, a
//      submit/button/reset input, or anything with role="button") is
//      focused and sent its standard key -- Enter for a link, Enter-then-
//      Space for a button -- and the check passes only if a page-level
//      fingerprint (URL, focused control, the status heading, the
//      "Accepted" flag, the answered-fact count, the visible error text)
//      changes. No fingerprint change, whether or not an exception was
//      thrown, is a failed activation.
//   3. No mouse: every one of the above is driven exclusively through
//      Input.dispatchKeyEvent. Input.dispatchMouseEvent is counted across
//      the whole run and reported; it must be zero for the run to mean what
//      it claims.
//
// A control added to the page later is covered automatically: it enters
// the Tab order (check 1 sees it), its tag/type/role classifies it (check 2
// sees it), and neither check consults a name or an id.
//
// Optional third argv: a defect name, injected into the live page right
// after load and before any check runs, used only to demonstrate that a
// specific assertion here fails when the behaviour it guards is removed.
// It is never used against the real, unmodified surface.

const pageUrl = process.argv[2];
const defect = process.argv[3] || null;
if (!pageUrl) {
  process.stderr.write("entry-keyboard-operability-probe-failed\n");
  process.exit(1);
}

let chrome;
let client;
let targetId;
let sessionId;
let mouseEventsDispatched = 0;

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

async function dispatchKey(type, key, code, windowsVirtualKeyCode, modifiers) {
  await client.send(
    "Input.dispatchKeyEvent",
    { type, key, code, windowsVirtualKeyCode, modifiers },
    sessionId,
  );
}

async function pressKey(keydownType, key, code, windowsVirtualKeyCode, modifiers = 0) {
  await dispatchKey(keydownType, key, code, windowsVirtualKeyCode, modifiers);
  await dispatchKey("keyUp", key, code, windowsVirtualKeyCode, modifiers);
  await new Promise((resolve) => setTimeout(resolve, 60));
}

// Tab traversal reuses the existing focus-indicator probe's own dispatch
// shape ("rawKeyDown"), proven reliable across both prior tracks. Enter and
// Space, by contrast, must trigger a control's *native default action* --
// following a link, clicking a button -- and Chrome only runs that default
// handling for a "keyDown" event, not "rawKeyDown" (which is reserved for
// keys, like Tab or arrow keys, that never insert text or fire a click).
// Verified directly: dispatching Enter as "rawKeyDown" against the
// wordmark link never navigates and never fires Page.loadEventFired within
// the wait window, while the same key dispatched as "keyDown" navigates
// every time. Using "rawKeyDown" for Enter/Space would make every
// activation check here a false negative against a correct surface --
// exactly the untrue-machinery trap the charter names.
async function pressTab(shift = false) {
  await pressKey("rawKeyDown", "Tab", "Tab", 9, shift ? 8 : 0);
}
async function pressEnter() {
  await pressKey("keyDown", "Enter", "Enter", 13);
}
async function pressSpace() {
  await pressKey("keyDown", " ", "Space", 32);
}

// Injected once: element identity (never a stored id/name list), the
// standing candidate set for Tab order, and the page fingerprint used to
// confirm an observed effect. Nothing here names a control.
const PAGE_HELPERS = `
  function describe(el) {
    if (!el || el === document.body) return null;
    return {
      key: el.tagName + "#" + (el.id || "") + "." + (el.className || "") + ":" +
        (el.textContent || "").trim().slice(0, 40),
      tag: el.tagName,
      type: (el.getAttribute("type") || "").toLowerCase(),
      hasHref: el.tagName === "A" && el.hasAttribute("href"),
      role: el.getAttribute("role") || "",
    };
  }
  function refreshCandidates() {
    window.__kbCandidates = Array.from(
      document.querySelectorAll('button, input, a[href], [tabindex]')
    );
  }
  function focusByKey(key) {
    refreshCandidates();
    const el = window.__kbCandidates.find((e) => {
      const info = describe(e);
      return info && info.key === key;
    });
    if (!el) return false;
    el.focus();
    return true;
  }
  function fingerprint() {
    const statusEl = document.getElementById("status-title");
    const errorEl = document.querySelector(".error");
    const focused = describe(document.activeElement);
    return {
      url: location.href,
      focusedKey: focused ? focused.key : null,
      statusHeading: statusEl ? statusEl.textContent : null,
      accepted: document.body.textContent.includes("Accepted"),
      answeredCount: document.querySelectorAll(".answered").length,
      errorText: errorEl ? errorEl.textContent : null,
    };
  }
  window.__kbProbe = { describe, refreshCandidates, focusByKey, fingerprint };
  true;
`;

async function describeActive() {
  return evaluate(`window.__kbProbe.describe(document.activeElement)`);
}
async function fingerprint() {
  return evaluate(`window.__kbProbe.fingerprint()`);
}
async function focusByKey(key) {
  return evaluate(`window.__kbProbe.focusByKey(${JSON.stringify(key)})`);
}
async function blurActive() {
  // element.blur() alone does not reset Chrome's internal sequential-focus-
  // navigation starting point -- the next Tab continues from wherever focus
  // last was, not from the top of the document. That only surfaces once a
  // control mid-page is left focused across a sweep boundary (exactly what
  // an explanatory panel left open from a prior phase does), so it stayed
  // invisible until the walk could leave state open across phases. Focusing
  // <body> via a temporary tabindex, not just blurring, actually resets it.
  await evaluate(`
    (() => {
      document.activeElement && document.activeElement.blur();
      document.body.setAttribute("tabindex", "-1");
      document.body.focus();
      document.body.removeAttribute("tabindex");
      return true;
    })()
  `);
}

async function waitForFingerprintChange(before, timeoutMs = 3000) {
  const deadline = Date.now() + timeoutMs;
  let after = await fingerprint();
  while (
    Date.now() < deadline &&
    JSON.stringify(after) === JSON.stringify(before)
  ) {
    await new Promise((resolve) => setTimeout(resolve, 40));
    after = await fingerprint();
  }
  return after;
}

// The submit button disables itself synchronously the instant its click
// fires, before the contribution's fetch round-trip resolves -- a real,
// observable effect, but the wrong one to stop on: settling for it as
// "the" observed effect would let a click that fires and then does nothing
// else pass, and it would leave the fetch still in flight while the next
// control's test starts, corrupting that control's own before/after
// reading with a late, unrelated fingerprint change. Every activation
// attempt waits for that in-flight state to clear before either check
// resolves.
async function settle(timeoutMs = 4000) {
  const deadline = Date.now() + timeoutMs;
  while (Date.now() < deadline) {
    const busy = await evaluate(`document.querySelector(".primary[disabled]") !== null`);
    if (!busy) return;
    await new Promise((resolve) => setTimeout(resolve, 40));
  }
}

// Demonstration-only injections. Never run against the real evaluation.
async function injectDefect(name) {
  if (name === "break-reverse-traversal") {
    // Traps focus on "Enter this fact" against Shift+Tab only: forward Tab
    // still lands on it normally, but nothing before it in the order can be
    // reached going backward through it. Reproduces exactly the asymmetry
    // check 1 exists to catch.
    await evaluate(`
      (() => {
        const target = Array.from(document.querySelectorAll("button")).find(
          (b) => b.textContent.trim() === "Enter this fact"
        );
        if (!target) return false;
        target.addEventListener(
          "keydown",
          (e) => {
            if (e.key === "Tab" && e.shiftKey) {
              e.preventDefault();
              e.stopImmediatePropagation();
            }
          },
          true
        );
        return true;
      })()
    `);
  } else if (name === "swallow-activation") {
    // Silently swallows Enter and Space on "Enter this fact" -- the exact
    // failure shape the charter names: no exception, no effect.
    await evaluate(`
      (() => {
        const target = Array.from(document.querySelectorAll("button")).find(
          (b) => b.textContent.trim() === "Enter this fact"
        );
        if (!target) return false;
        target.addEventListener(
          "keydown",
          (e) => {
            if (e.key === "Enter" || e.key === " " || e.key === "Spacebar") {
              e.preventDefault();
              e.stopImmediatePropagation();
            }
          },
          true
        );
        return true;
      })()
    `);
  } else if (name === "scramble-order") {
    // Scrambles Shift+Tab traversal order while preserving the set of
    // reachable controls: re-routes Shift+Tab into a scrambled cycle
    // (seed -> middle control -> ... -> seed).
    await evaluate(`
      (() => {
        document.addEventListener(
          "keydown",
          (e) => {
            if (e.key === "Tab" && e.shiftKey) {
              const active = document.activeElement;
              if (!active) return;
              const desc = window.__kbProbe.describe(active);
              if (!desc) return;
              let targetSelector = null;
              if (active.classList.contains("primary") || desc.key.includes("Add W-2") || desc.key.includes("Update W-2")) {
                targetSelector = "button:not(.primary)";
              } else if (desc.key.includes("Enter this fact")) {
                targetSelector = "#w2-box1";
              } else if (desc.key.includes("w2-box1") || active.id === "w2-box1") {
                targetSelector = "a[href]";
              } else if (desc.key.includes("wordmark") || active.tagName === "A") {
                targetSelector = ".primary";
              }
              if (targetSelector) {
                const target = document.querySelector(targetSelector);
                if (target) {
                  e.preventDefault();
                  e.stopImmediatePropagation();
                  target.focus();
                }
              }
            }
          },
          true
        );
        return true;
      })()
    `);
  }
}

function standardKeysFor(info) {
  if (!info) return [];
  if (info.hasHref) return ["Enter"];
  if (info.tag === "BUTTON") return ["Enter", "Space"];
  if (info.tag === "INPUT" && ["submit", "button", "reset"].includes(info.type)) {
    return ["Enter", "Space"];
  }
  if (info.role === "button") return ["Enter", "Space"];
  return [];
}

async function collectForwardOrder(iterations) {
  const order = [];
  const seen = new Set();
  for (let i = 0; i < iterations; i++) {
    await pressTab(false);
    const focused = await describeActive();
    if (!focused) continue;
    if (seen.has(focused.key)) continue;
    seen.add(focused.key);
    order.push(focused);
  }
  return order;
}

async function collectBackwardOrder(seedKey, maxIterations) {
  const order = [];
  const seen = new Set();
  let returnedToSeed = false;
  for (let i = 0; i < maxIterations; i++) {
    await pressTab(true);
    const focused = await describeActive();
    if (!focused) continue;
    if (focused.key === seedKey) {
      returnedToSeed = true;
      break;
    }
    if (seen.has(focused.key)) break;
    seen.add(focused.key);
    order.push(focused);
  }
  return { backward: order, returnedToSeed };
}

const findings = { reverseTraversal: [], activation: [], navigation: [] };
const navigationQueue = [];

// Must exceed the total number of focusable controls the page can show at
// once. The explanatory walk can leave every line's panel open
// simultaneously (the trail does not collapse on navigation), so this
// scales with how many lines/dependencies/actions exist, not a fixed count.
const SWEEP_ITERATIONS = 80;

async function reverseTraversalCheck(phase) {
  await blurActive();
  const forward = await collectForwardOrder(SWEEP_ITERATIONS);
  if (!forward.length) {
    throw new Error("no-focusable-controls-in-forward-sweep");
  }
  const seedControl = forward[forward.length - 1];
  const seedKey = seedControl.key;
  await focusByKey(seedKey);

  const { backward, returnedToSeed } = await collectBackwardOrder(seedKey, SWEEP_ITERATIONS);

  const forwardKeys = forward.map((f) => f.key);
  const backwardStepKeys = backward.map((b) => b.key);
  const actualBackward = [seedKey, ...backwardStepKeys];
  const expectedBackward = forwardKeys.slice().reverse();

  const backwardSet = new Set(actualBackward);
  const forwardSet = new Set(forwardKeys);
  const forwardOnly = forwardKeys.filter((k) => !backwardSet.has(k));
  const backwardOnly = actualBackward.filter((k) => !forwardSet.has(k));
  const setMatches = forwardOnly.length === 0 && backwardOnly.length === 0;

  let mismatchIndex = null;
  const maxLen = Math.max(expectedBackward.length, actualBackward.length);
  for (let i = 0; i < maxLen; i++) {
    if (expectedBackward[i] !== actualBackward[i]) {
      mismatchIndex = i;
      break;
    }
  }
  const orderMatches = returnedToSeed && mismatchIndex === null;

  findings.reverseTraversal.push({
    phase,
    seedKey,
    returnedToSeed,
    forward: forwardKeys,
    backward: backwardStepKeys,
    expectedBackward,
    actualBackward,
    forwardOnly,
    backwardOnly,
    setMatches,
    orderMatches,
    mismatchIndex,
    matches: setMatches && orderMatches,
  });
  return forward;
}

async function activationChecks(controls, phase) {
  for (const control of controls) {
    if (control.hasHref) {
      if (!navigationQueue.some((c) => c.key === control.key)) {
        navigationQueue.push({ ...control, phase });
      }
      continue;
    }
    const keys = standardKeysFor(control);
    if (!keys.length) {
      findings.activation.push({
        key: control.key,
        phase,
        actionable: false,
        testedKeys: [],
        activatedWith: null,
      });
      continue;
    }
    await focusByKey(control.key);
    const before = await fingerprint();
    let activatedWith = null;
    for (const key of keys) {
      if (key === "Enter") await pressEnter();
      else await pressSpace();
      await settle();
      const after = await waitForFingerprintChange(before);
      if (JSON.stringify(after) !== JSON.stringify(before)) {
        activatedWith = key;
        break;
      }
      await focusByKey(control.key);
    }
    await settle();
    const after = await fingerprint();
    findings.activation.push({
      key: control.key,
      phase,
      actionable: true,
      testedKeys: keys,
      activatedWith,
      before,
      after,
    });
  }
}

async function navigationChecks() {
  for (const control of navigationQueue) {
    await focusByKey(control.key);
    const before = await evaluate(`location.href`);
    // The observed effect of activating a link is a fresh document load --
    // Page.loadEventFired -- not necessarily a changed URL string: this
    // link's href resolves to the same path it is already on, so a correct
    // activation reloads the document without the URL text changing.
    // Comparing URL strings here would silently fail on a link that points
    // at its own page, which is exactly this control; the CDP-level load
    // event is the effect that generalises to any href, same-page or not.
    const navigated = client
      .waitFor("Page.loadEventFired", sessionId, 5000)
      .then(() => true)
      .catch(() => false);
    await pressEnter();
    const loadFired = await navigated;
    let after = before;
    if (loadFired) {
      try {
        after = await evaluate(`location.href`);
      } catch {
        after = null;
      }
    }
    findings.navigation.push({
      key: control.key,
      phase: control.phase,
      before,
      after,
      navigated: loadFired,
    });
  }
}

try {
  chrome = await launchChrome(null);
  client = await CDPClient.connect(chrome.wsUrl);
  const originalSend = client.send.bind(client);
  client.send = (method, params, sid) => {
    if (method === "Input.dispatchMouseEvent") mouseEventsDispatched += 1;
    return originalSend(method, params, sid);
  };
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
  if (defect) {
    const applied = await injectDefect(defect);
    if (applied === false) {
      throw new Error(`defect-injection-target-not-found:${defect}`);
    }
  }

  // Data population only -- not part of any claim under test here, exactly
  // as the existing focus-indicator probe already does to reach the
  // complete state.
  await evaluate(`
    (() => {
      const input = document.querySelector("#w2-box1");
      input.value = "90000";
      input.dispatchEvent(new Event("input", { bubbles: true }));
      return true;
    })()
  `);

  const forwardIncomplete = await reverseTraversalCheck("incomplete");
  await activationChecks(forwardIncomplete, "incomplete");

  await waitUntil(
    `document.body.textContent.includes("0 missing facts") || document.querySelector(".error") !== null`,
  );

  const forwardComplete = await reverseTraversalCheck("complete");
  await activationChecks(forwardComplete, "complete");

  await navigationChecks();

  process.stdout.write(
    `${JSON.stringify({ ...findings, mouseEventsDispatched }, null, 2)}\n`,
  );
} catch (err) {
  process.stderr.write(`entry-keyboard-operability-probe-failed: ${err}\n`);
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
