#!/usr/bin/env node
// Throwaway retention probe. Not product code — see README.md. Track 1 of the
// Entry Boundary milestone (docs/reviews/charter-2026-07-28-entry-boundary-track1.md).
//
// Drives the *existing* confined invocation vehicle
// (tools/presentation_harness/lib/chrome.mjs + lib/server.mjs, unmodified),
// types distinctive synthetic tokens into a throwaway form, exercises a clean
// close and a crash-simulated close, and greps the resulting Chrome profile
// directories for those tokens. Prints a JSON report to stdout.
//
// Run by hand only. Not wired into CI or verify. Deletes every scratch
// profile it inspects before exiting.
//
//   node tools/entry_probe/probe.mjs

import { randomBytes } from "node:crypto";
import { execFileSync } from "node:child_process";
import { readdir, rm, stat } from "node:fs/promises";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import { startLoopbackServer } from "../presentation_harness/lib/server.mjs";
import { launchChrome } from "../presentation_harness/lib/chrome.mjs";
import { CDPClient } from "../presentation_harness/lib/cdp.mjs";

const HERE = dirname(fileURLToPath(import.meta.url));
const REPO_ROOT = join(HERE, "..", "..");
const FORM_PATH = "tools/entry_probe/form.html";

const base = randomBytes(6).toString("hex");
const TOKENS = {
  fullName: `ENTRYPROBE-NAME-${base}`,
  ssn: `ENTRYPROBE-SSNFIELD-${base}`,
  wages: `ENTRYPROBE-WAGES-${base}`,
  email: `entryprobe-${base}@example.invalid`,
  notes: `ENTRYPROBE-NOTES-${base} wagess recieved teh amoutn`,
};
const ALL_TOKEN_VALUES = Object.values(TOKENS);

function log(...args) {
  process.stderr.write(`${args.map((a) => (typeof a === "string" ? a : JSON.stringify(a))).join(" ")}\n`);
}

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

/**
 * Find the OS pid and --user-data-dir of the one Chrome process this probe
 * just launched, by reading `ps` output. This is external process
 * inspection only — it does not require chrome.mjs to expose its internal
 * profile-directory or pid, and it does not modify chrome.mjs.
 */
function findChromeProcess() {
  const out = execFileSync("ps", ["-axww", "-o", "pid,command"], { encoding: "utf8" });
  const lines = out.split("\n").filter(
    (l) =>
      l.includes("--user-data-dir=") &&
      l.includes("presentation-harness-profile-") &&
      !l.includes("--type="), // exclude GPU/renderer/utility helper subprocesses; keep only the main browser process
  );
  if (lines.length !== 1) {
    throw new Error(
      `expected exactly one matching Chrome process, found ${lines.length}: ${JSON.stringify(lines)}`,
    );
  }
  const line = lines[0].trim();
  const pid = Number.parseInt(line.split(/\s+/)[0], 10);
  const match = line.match(/--user-data-dir=(\S+)/);
  if (!match) throw new Error("could not parse --user-data-dir from ps output");
  return { pid, profileDir: match[1] };
}

function processAlive(pid) {
  try {
    process.kill(pid, 0);
    return true;
  } catch {
    return false;
  }
}

async function waitForProcessExit(pid, timeoutMs) {
  const deadline = Date.now() + timeoutMs;
  while (processAlive(pid)) {
    if (Date.now() > deadline) return false;
    await sleep(50);
  }
  return true;
}

/** Dispatch real (CDP-trusted) keystrokes into a focused element. */
async function typeInto(client, sessionId, elementId, text) {
  const focusResult = await client.send(
    "Runtime.evaluate",
    { expression: `document.getElementById(${JSON.stringify(elementId)}).focus()`, awaitPromise: true },
    sessionId,
  );
  if (focusResult.exceptionDetails) {
    throw new Error(`focus failed for ${elementId}: ${JSON.stringify(focusResult.exceptionDetails)}`);
  }
  // One "char" event per character carries the text; keyDown/keyUp carry
  // none, matching how a real keypress is represented in three events. This
  // is the flow Puppeteer's own type() uses. Sending `text` on all three
  // event types double-inserts each character (verified against this
  // vehicle: an earlier version of this probe did that and the DOM value
  // came back with every character doubled).
  for (const ch of text) {
    await client.send("Input.dispatchKeyEvent", { type: "keyDown", key: ch }, sessionId);
    await client.send("Input.dispatchKeyEvent", { type: "char", text: ch, unmodifiedText: ch, key: ch }, sessionId);
    await client.send("Input.dispatchKeyEvent", { type: "keyUp", key: ch }, sessionId);
  }
}

/**
 * Attach one target/session with the same non-loopback-blocking discipline
 * used by the harness's own executor.mjs (attachFreshTarget), reused here
 * rather than reimplemented differently, plus recording of every
 * non-loopback request the browser attempts (URL, method, and any postData)
 * so a spellcheck- or telemetry-service egress attempt is both blocked and
 * reported rather than silently allowed through.
 */
async function attachInstrumentedTarget(client, origin) {
  const { browserContextId } = await client.send("Target.createBrowserContext", {});
  const { targetId } = await client.send("Target.createTarget", { url: "about:blank", browserContextId });
  const { sessionId } = await client.send("Target.attachToTarget", { targetId, flatten: true });
  await client.send("Page.enable", {}, sessionId);
  await client.send("Runtime.enable", {}, sessionId);
  await client.send("Fetch.enable", { patterns: [{ urlPattern: "*" }] }, sessionId);

  const nonLoopbackRequests = [];
  const offRequestPaused = client.on(
    "Fetch.requestPaused",
    (params) => {
      const { requestId, request } = params;
      if (request.url.startsWith(origin)) {
        client.send("Fetch.continueRequest", { requestId }, sessionId).catch(() => {});
        return;
      }
      nonLoopbackRequests.push({
        url: request.url,
        method: request.method,
        hasPostData: Boolean(request.postData),
        postDataContainsToken: ALL_TOKEN_VALUES.some((t) => (request.postData || "").includes(t)),
        urlContainsToken: ALL_TOKEN_VALUES.some((t) => request.url.includes(t)),
      });
      client.send("Fetch.failRequest", { requestId, errorReason: "BlockedByClient" }, sessionId).catch(() => {});
    },
    sessionId,
  );

  return {
    sessionId,
    nonLoopbackRequests,
    async dispose() {
      offRequestPaused();
      try {
        await client.send("Target.closeTarget", { targetId });
      } catch {
        /* already gone */
      }
      try {
        await client.send("Target.disposeBrowserContext", { browserContextId });
      } catch {
        /* already gone */
      }
    },
  };
}

/** Recursively, binary-safely grep a directory for each token. */
function grepDirForTokens(dir) {
  const hits = [];
  for (const [field, token] of Object.entries(TOKENS)) {
    let out;
    try {
      // -r recursive, -l list matching files only, -a force binary-safe
      // text-mode scanning (do NOT add -I — that flag means "treat binary
      // files as non-matching", the opposite of what this probe needs, and
      // an earlier version of this script had that bug: it silently
      // suppressed every match inside SQLite/LevelDB stores).
      out = execFileSync("grep", ["-rla", token, dir], { encoding: "utf8" });
    } catch (error) {
      // grep exits 1 when no match; that's a real "not found" result, not an error.
      if (error.status === 1) {
        out = "";
      } else {
        out = `<grep error: ${error.message}>`;
      }
    }
    const files = out.split("\n").filter(Boolean);
    hits.push({ field, token, files });
  }
  return hits;
}

async function runOneSession({ label, killSignal }) {
  log(`\n=== session: ${label} ===`);
  const chromeHandle = await launchChrome(null, {});
  const { pid, profileDir } = findChromeProcess();
  log(`${label}: pid=${pid} profileDir=${profileDir}`);

  const client = await CDPClient.connect(chromeHandle.wsUrl);
  const target = await attachInstrumentedTarget(client, GLOBAL.serverOrigin);

  await client.send("Page.navigate", { url: `${GLOBAL.serverOrigin}/${FORM_PATH}` }, target.sessionId);
  await client.waitFor("Page.loadEventFired", target.sessionId, 10000);

  for (const [field, value] of Object.entries(TOKENS)) {
    await typeInto(client, target.sessionId, field, value);
  }

  // Sanity readback: confirm the DOM actually holds the intended tokens
  // verbatim before relying on a grep-for-exact-token search downstream.
  const readback = await client.send(
    "Runtime.evaluate",
    {
      expression: `Object.fromEntries(${JSON.stringify(Object.keys(TOKENS))}.map((id) => [id, document.getElementById(id).value]))`,
      returnByValue: true,
      awaitPromise: true,
    },
    target.sessionId,
  );
  for (const [field, expected] of Object.entries(TOKENS)) {
    const actual = readback.result?.value?.[field];
    if (actual !== expected) {
      log(`${label}: WARNING readback mismatch for ${field}: expected ${JSON.stringify(expected)} got ${JSON.stringify(actual)}`);
    }
  }

  // Undo-buffer probe: clear one field's content, then ask the browser's own
  // in-page undo manager whether it can restore it, all before any
  // navigation or close.
  const clearResult = await client.send(
    "Runtime.evaluate",
    {
      expression: `(() => {
        const el = document.getElementById('notes');
        el.focus();
        el.setSelectionRange(0, el.value.length);
        document.execCommand('delete');
        return el.value;
      })()`,
      returnByValue: true,
      awaitPromise: true,
    },
    target.sessionId,
  );
  const valueAfterClear = clearResult.result?.value;
  const undoResult = await client.send(
    "Runtime.evaluate",
    {
      expression: `(() => { document.execCommand('undo'); return document.getElementById('notes').value; })()`,
      returnByValue: true,
      awaitPromise: true,
    },
    target.sessionId,
  );
  const valueAfterUndo = undoResult.result?.value;

  // Submit the form (a real GET navigation) — this is the moment autofill /
  // form-history heuristics in real browsers key off.
  const submitResult = await client.send(
    "Runtime.evaluate",
    { expression: `document.getElementById('probeForm').requestSubmit()`, awaitPromise: true },
    target.sessionId,
  );
  if (submitResult.exceptionDetails) {
    log(`${label}: submit threw`, submitResult.exceptionDetails);
  }
  await client.waitFor("Page.loadEventFired", target.sessionId, 10000).catch((e) => log(`${label}: post-submit load wait: ${e.message}`));

  // Post-navigation undo persistence: does the undo history survive
  // navigating the same tab away and reloading the original form?
  await client.send("Page.navigate", { url: `${GLOBAL.serverOrigin}/${FORM_PATH}` }, target.sessionId);
  await client.waitFor("Page.loadEventFired", target.sessionId, 10000);
  const postNavigationValue = await client.send(
    "Runtime.evaluate",
    {
      expression: `(() => { document.getElementById('notes').focus(); document.execCommand('undo'); return document.getElementById('notes').value; })()`,
      returnByValue: true,
      awaitPromise: true,
    },
    target.sessionId,
  );

  await sleep(1500); // let any async writer (WebData, prefs, session backend) flush.

  const nonLoopbackRequests = target.nonLoopbackRequests.slice();
  await target.dispose();
  client.close();

  // Deliberately do NOT call chromeHandle.dispose() — its own cleanup path
  // deletes the entire profile directory as its last act, which would erase
  // the evidence before we can inspect it. Instead we send the signal
  // ourselves and wait for the OS process to exit, then inspect, then clean
  // up ourselves. This does not modify chrome.mjs; it simply does not
  // invoke its convenience dispose() wrapper for these two runs.
  process.kill(pid, killSignal);
  const exited = await waitForProcessExit(pid, 5000);
  if (!exited) {
    log(`${label}: process ${pid} did not exit after ${killSignal} within 5s; forcing SIGKILL`);
    try {
      process.kill(pid, "SIGKILL");
    } catch {
      /* already gone */
    }
    await waitForProcessExit(pid, 5000);
  }

  await sleep(300); // let the OS finish releasing file handles before we grep.

  // Sweep any orphaned helper subprocesses (GPU/renderer/utility) left
  // behind by the main process's death — hygiene only, does not affect the
  // grep below since evidence was captured from disk, not from these.
  try {
    execFileSync("pkill", ["-9", "-f", profileDir], { stdio: "ignore" });
  } catch {
    /* pkill exits non-zero when nothing matched */
  }

  let profileStat;
  try {
    profileStat = await stat(profileDir);
  } catch {
    profileStat = null;
  }

  const hits = profileStat ? grepDirForTokens(profileDir) : [];
  let topLevelEntries = [];
  let sessionsEntries = [];
  let sessionStorageEntries = [];
  if (profileStat) {
    try {
      topLevelEntries = await readdir(join(profileDir, "Default"));
    } catch {
      topLevelEntries = [];
    }
    try {
      sessionsEntries = await readdir(join(profileDir, "Default", "Sessions"));
    } catch {
      sessionsEntries = [];
    }
    try {
      sessionStorageEntries = await readdir(join(profileDir, "Default", "Session Storage"));
    } catch {
      sessionStorageEntries = [];
    }
  }

  await rm(profileDir, { recursive: true, force: true });

  return {
    label,
    pid,
    profileDirExistedAfterKill: Boolean(profileStat),
    defaultProfileTopLevelEntries: topLevelEntries,
    // Named explicitly because they are the crash-recovery / session-restore
    // stores the charter asks about; an empty array means the directory
    // existed but the browser wrote no entries into it, not that we didn't
    // look.
    sessionsDirEntries: sessionsEntries,
    sessionStorageDirEntries: sessionStorageEntries,
    tokenHits: hits,
    nonLoopbackRequests,
    undoProbe: { valueAfterClear, valueAfterUndo, postNavigationUndoValue: postNavigationValue.result?.value },
  };
}

const GLOBAL = {};

async function main() {
  log("tokens", TOKENS);
  const server = await startLoopbackServer(REPO_ROOT, new Set([FORM_PATH]));
  GLOBAL.serverOrigin = server.origin;
  log("server origin", server.origin);

  const results = [];
  try {
    results.push(await runOneSession({ label: "clean-ish (SIGTERM by probe, not dispose())", killSignal: "SIGTERM" }));
    results.push(await runOneSession({ label: "unclean (SIGKILL, simulated crash)", killSignal: "SIGKILL" }));
  } finally {
    await server.close();
  }

  for (const r of results) {
    const severeEgress = r.nonLoopbackRequests.some((req) => req.urlContainsToken || req.postDataContainsToken);
    if (severeEgress) {
      log(`\n!!! STOP CONDITION: typed token observed in a non-loopback network request in session "${r.label}" !!!`);
      log(JSON.stringify(r.nonLoopbackRequests, null, 2));
      process.stdout.write(`${JSON.stringify({ stopCondition: "network-egress-of-typed-content", results }, null, 2)}\n`);
      process.exitCode = 3;
      return;
    }
  }

  process.stdout.write(`${JSON.stringify({ tokens: TOKENS, results }, null, 2)}\n`);
}

main().catch((error) => {
  log("FATAL", error.stack || String(error));
  process.exitCode = 1;
});
