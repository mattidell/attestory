#!/usr/bin/env node
// Throwaway retention probe. Not product code — see README.md.
//
// Track 1 of the Entry Boundary milestone
// (docs/archive/2026-08-02-milestone-artifacts/reviews/charter-2026-07-28-entry-boundary-track1.md) drove the
// *headless* synthetic evaluation harness
// (tools/presentation_harness/lib/chrome.mjs + lib/server.mjs, unmodified).
// Track 1b (docs/archive/2026-08-02-milestone-artifacts/reviews/charter-2026-07-28-entry-boundary-track1b.md) adds a
// second vehicle: the *headed* one a person actually types into,
// packages/derivation/live_viewing.py (ADR-0047), driven against a synthetic
// workspace directory via the throwaway tools/entry_probe/headed_launch.py
// bridge. Neither packages/derivation/live_viewing.py nor
// tools/presentation_harness/lib/chrome.mjs or lib/server.mjs is modified by
// this file.
//
// Both modes exercise the same fixture, the same five channels, the same
// synthetic tokens, the same binary-safe grep, and the same network capture:
// type distinctive synthetic tokens into a throwaway form, exercise a clean
// close and a crash-simulated close, and grep the resulting profile
// directory for those tokens. Prints a JSON report to stdout.
//
// Run by hand only. Not wired into CI or verify. Deletes every scratch
// profile/workspace it inspects before exiting.
//
//   node tools/entry_probe/probe.mjs                  # both modes (default)
//   node tools/entry_probe/probe.mjs --mode=headless
//   node tools/entry_probe/probe.mjs --mode=headed

import { randomBytes } from "node:crypto";
import { execFileSync, spawn, spawnSync } from "node:child_process";
import { mkdtemp, readdir, rm, stat } from "node:fs/promises";
import { existsSync, statSync, writeFileSync, unlinkSync } from "node:fs";
import { tmpdir, homedir } from "node:os";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import { startLoopbackServer } from "../presentation_harness/lib/server.mjs";
import { launchChrome } from "../presentation_harness/lib/chrome.mjs";
import { CDPClient } from "../presentation_harness/lib/cdp.mjs";

const HERE = dirname(fileURLToPath(import.meta.url));
const REPO_ROOT = join(HERE, "..", "..");
const FORM_PATH = "tools/entry_probe/form.html";
const HEADED_LAUNCHER = join(HERE, "headed_launch.py");

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
 * Find the OS pid and --user-data-dir (plus --disk-cache-dir and
 * --download-default-directory, if present) of the one Chrome process
 * matching `marker` somewhere in its command line, by reading `ps` output.
 * This is external process inspection only — it does not require either
 * vehicle to expose its internal profile-directory or pid, and it does not
 * modify chrome.mjs or live_viewing.py.
 *
 * For the headless vehicle, `marker` is the "presentation-harness-profile-"
 * mkdtemp prefix chrome.mjs uses. For the headed vehicle, `marker` is the
 * synthetic workspace directory this probe created — unique per run — since
 * live_viewing.py's --user-data-dir, --disk-cache-dir, and
 * --download-default-directory are all confined somewhere underneath it.
 */
function findChromeProcess(marker) {
  const out = execFileSync("ps", ["-axww", "-o", "pid,command"], { encoding: "utf8" });
  const lines = out.split("\n").filter(
    (l) =>
      l.includes("--user-data-dir=") &&
      l.includes(marker) &&
      !l.includes("--type="), // exclude GPU/renderer/utility helper subprocesses; keep only the main browser process
  );
  if (lines.length !== 1) {
    throw new Error(
      `expected exactly one matching Chrome process for marker ${JSON.stringify(marker)}, found ${lines.length}: ${JSON.stringify(lines)}`,
    );
  }
  const line = lines[0].trim();
  const pid = Number.parseInt(line.split(/\s+/)[0], 10);
  const profileMatch = line.match(/--user-data-dir=(\S+)/);
  if (!profileMatch) throw new Error("could not parse --user-data-dir from ps output");
  const cacheMatch = line.match(/--disk-cache-dir=(\S+)/);
  const downloadsMatch = line.match(/--download-default-directory=(\S+)/);
  return {
    pid,
    profileDir: profileMatch[1],
    cacheDir: cacheMatch ? cacheMatch[1] : null,
    downloadsDir: downloadsMatch ? downloadsMatch[1] : null,
  };
}

/** Read one newline-terminated line from a stream, then stop listening. */
function readFirstLine(stream) {
  return new Promise((resolve, reject) => {
    let buf = "";
    function onData(chunk) {
      buf += chunk.toString("utf8");
      const idx = buf.indexOf("\n");
      if (idx !== -1) {
        stream.off("data", onData);
        stream.off("error", onError);
        resolve(buf.slice(0, idx));
      }
    }
    function onError(err) {
      stream.off("data", onData);
      reject(err);
    }
    stream.on("data", onData);
    stream.on("error", onError);
  });
}

/**
 * Launch packages/derivation/live_viewing.py's LiveViewingVehicle against a
 * synthetic workspace directory, via the throwaway headed_launch.py bridge
 * (tools/entry_probe/headed_launch.py). Neither live_viewing.py nor
 * live_workspace.py is modified; the bridge imports them unmodified and
 * reports only the one public `websocket_url` field.
 */
async function launchHeadedVehicle(workspaceDir) {
  const child = spawn("python3", [HEADED_LAUNCHER, workspaceDir], {
    stdio: ["pipe", "pipe", "inherit"],
  });
  const firstLine = await readFirstLine(child.stdout);
  const parsed = JSON.parse(firstLine);
  return { launcherProcess: child, websocketUrl: parsed.websocket_url };
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

// --- Track 2 repair: widened, off-vehicle filesystem search -----------------
//
// Everything above searches only inside the directory the vehicle itself
// manages (--user-data-dir / --disk-cache-dir / --download-default-directory
// and their shared session root). That is exactly the region the Track 2
// review found undetermined: it does not tell us whether the resolved Chrome
// binary writes anything to a fixed, per-user-account location no flag
// redirects. The functions below search real per-user macOS locations
// outside the confined session directory, using a before/after marker file
// rather than a full directory enumeration (these directories can be huge and
// carry pre-existing, unrelated content this run must not read).
//
// Method: touch a marker file immediately before launching the browser, then
// after the crash/close, ask the filesystem which entries under each
// candidate root have a *creation* time (`stat -f %B`, birthtime — not mtime)
// at or after the marker's. Birthtime, not mtime, is used deliberately: this
// machine's own, real Chrome install may be running for unrelated reasons
// (confirmed true for this run — see the findings note), and a running real
// browser continuously *modifies* pre-existing files in its own profile
// (History, Preferences, LevelDB logs) without *creating* new ones most of
// the time. Filtering on birthtime keeps the signal to "something new
// appeared here during this exact window" rather than "something in a
// directory a real, unrelated process also uses got touched."
//
// Any file the scan turns up is grepped for the same synthetic tokens the
// rest of this probe uses (`-rla`, the corrected flag — see the positive
// control above). A token match here is decisive regardless of anything
// else. Absence of a token match is not: it means "nothing new held a typed
// value," not "nothing new appeared" — both are reported.

function wideSearchRoots() {
  const home = homedir();
  return [
    { category: "os-crash-report-directory", path: join(home, "Library", "Logs", "DiagnosticReports") },
    { category: "os-crash-report-directory", path: join(home, "Library", "Application Support", "CrashReporter") },
    { category: "per-user-caches-directory", path: join(home, "Library", "Caches") },
    { category: "temp-directory", path: tmpdir() },
    { category: "temp-directory", path: "/tmp" },
    { category: "chrome-or-chromium-application-support", path: join(home, "Library", "Application Support", "Google") },
    { category: "chrome-or-chromium-application-support", path: join(home, "Library", "Application Support", "Chromium") },
  ];
}

/** macOS creation time (birthtime) of `p` in epoch ms, or null if unavailable. */
function statBirthEpochMs(p) {
  try {
    const out = execFileSync("stat", ["-f", "%B", p], { encoding: "utf8" }).trim();
    const seconds = Number(out);
    return Number.isFinite(seconds) ? seconds * 1000 : null;
  } catch {
    return null;
  }
}

/**
 * Scan every wideSearchRoots() location for entries created at or after
 * `markerPath`'s own creation time, excluding anything under `excludePaths`
 * (this run's own confined session directory and temp dirs, already covered
 * by the rest of this probe). Returns a report keyed by location category,
 * naming only the category and a relative, non-identifying description of
 * what was found — never a real absolute path under the user's home
 * directory.
 */
function wideFilesystemScan(markerPath, excludePaths) {
  const markerBirth = statBirthEpochMs(markerPath) ?? Date.now();
  const results = [];
  for (const root of wideSearchRoots()) {
    if (!existsSync(root.path)) {
      results.push({ category: root.category, rootExisted: false, newEntries: [] });
      continue;
    }
    const findArgs = [root.path, "-maxdepth", "5", "-newer", markerPath];
    for (const ex of excludePaths.filter(Boolean)) {
      findArgs.push("-not", "-path", `${ex}*`);
    }
    // spawnSync, not execFileSync: several of these roots contain
    // OS-protected subdirectories (Caches/com.apple.*, TemporaryItems under
    // sandboxed daemons' TMPDIR entries) this process has no permission to
    // stat. `find` prints "Operation not permitted" for those to its own
    // stderr and continues, but still exits non-zero overall — execFileSync
    // throws on a non-zero exit and discards the good matches it already
    // printed to stdout before that. spawnSync never throws; its stdout is
    // used regardless of exit status, and stderr is discarded (not this
    // run's concern — permission noise about unrelated OS daemon
    // directories, not a probe finding).
    const findResult = spawnSync("find", findArgs, { encoding: "utf8", maxBuffer: 64 * 1024 * 1024 });
    const candidates = (findResult.stdout || "").split("\n").filter(Boolean);
    const newEntries = [];
    for (const p of candidates) {
      if (p === markerPath) continue;
      const birth = statBirthEpochMs(p);
      // Require birthtime >= marker's own birthtime (with 1s slack for
      // filesystem timestamp granularity): this is what separates "created
      // during our window" from "pre-existing, merely modified by something
      // else while we were running" — the latter is not a finding.
      if (birth === null || birth < markerBirth - 1000) continue;
      let isFile = false;
      try {
        isFile = statSync(p).isFile();
      } catch {
        isFile = false;
      }
      let tokenHit = null;
      if (isFile) {
        tokenHit = false;
        for (const token of Object.values(TOKENS)) {
          try {
            // Same corrected flag as grepDirForTokens above: -rla, never -I.
            execFileSync("grep", ["-la", token, p], { encoding: "utf8" });
            tokenHit = true;
            break;
          } catch (error) {
            if (error.status !== 1) {
              tokenHit = null;
              break;
            }
          }
        }
      }
      newEntries.push({
        // Path relative to the category root only, never the real absolute
        // path under the user's home directory — the category plus this
        // relative tail is enough to know what appeared without naming the
        // residency.
        relativeToRoot: p.slice(root.path.length).replace(/^\//, "") || "(root itself)",
        isFile,
        tokenHit,
      });
    }
    results.push({ category: root.category, rootExisted: true, newEntryCount: newEntries.length, newEntries });
  }
  return results;
}

async function runOneSession({ label, killSignal }) {
  log(`\n=== headless session: ${label} ===`);
  const chromeHandle = await launchChrome(null, {});
  const { pid, profileDir } = findChromeProcess("presentation-harness-profile-");
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
    vehicle: "headless (tools/presentation_harness/lib/chrome.mjs)",
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

/**
 * Same method as runOneSession, against the headed vehicle
 * (packages/derivation/live_viewing.py) instead of chrome.mjs. Launched via
 * the throwaway headed_launch.py bridge against a fresh synthetic workspace
 * directory (a bare temp directory standing in for a real one — never a
 * real workspace). Chrome is found and signalled directly by pid (the same
 * external-`ps`-inspection method runOneSession uses), bypassing
 * LiveViewingSession.close() (whose own last act deletes the confined
 * .live-view/session-<uuid> directory) so the profile can be inspected
 * before deletion, then the whole synthetic workspace is deleted by this
 * probe itself — not by calling back into live_viewing.py.
 */
async function runHeadedSession({ label, killSignal, wideSearch }) {
  log(`\n=== headed session: ${label} ===`);
  const workspaceDir = await mkdtemp(join(tmpdir(), "entry-probe-headed-workspace-"));

  // Track 2 repair: marker file for the widened, off-vehicle filesystem
  // search (see wideFilesystemScan above). Created before launch, deleted
  // after the scan runs. A short sleep guards against same-second mtime/
  // birthtime granularity making a genuinely-new file indistinguishable from
  // the marker itself.
  let wideSearchMarker = null;
  if (wideSearch) {
    wideSearchMarker = join(tmpdir(), `entry-probe-wide-marker-${randomBytes(4).toString("hex")}`);
    writeFileSync(wideSearchMarker, "entry-probe wide-search marker\n");
    await sleep(1100);
  }

  const { launcherProcess, websocketUrl } = await launchHeadedVehicle(workspaceDir);

  const { pid, profileDir, cacheDir, downloadsDir } = findChromeProcess(workspaceDir);
  log(`${label}: pid=${pid} profileDir=${profileDir} cacheDir=${cacheDir}`);

  const client = await CDPClient.connect(websocketUrl);
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

  // Deliberately do NOT let LiveViewingSession.close() run (this probe never
  // called it — the bridge process only ever printed the websocket_url and
  // blocked). Signal Chrome directly by pid, the same "bypass the vehicle's
  // own teardown, inspect, then clean up ourselves" method runOneSession
  // uses against chrome.mjs's dispose().
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
    execFileSync("pkill", ["-9", "-f", workspaceDir], { stdio: "ignore" });
  } catch {
    /* pkill exits non-zero when nothing matched */
  }

  let profileStat;
  try {
    profileStat = await stat(profileDir);
  } catch {
    profileStat = null;
  }

  // Grep the whole synthetic workspace, not just profileDir: unlike
  // chrome.mjs (which never sets a separate cache directory, so cache lived
  // inside the profile dir it grepped), live_viewing.py confines cache and
  // downloads to sibling directories under the same session root
  // (--disk-cache-dir, --download-default-directory). Grepping the workspace
  // root covers profile, cache, downloads, and the print-to-pdf destination
  // in one pass.
  const hits = profileStat ? grepDirForTokens(workspaceDir) : [];
  let topLevelEntries = [];
  let sessionsEntries = [];
  let sessionStorageEntries = [];
  let cacheDirEntries = [];
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
    if (cacheDir) {
      try {
        cacheDirEntries = await readdir(cacheDir);
      } catch {
        cacheDirEntries = [];
      }
    }
  }

  // Stop the launcher bridge process. It never called session.close() itself
  // (by design — see headed_launch.py), so this does not touch the
  // directory; the probe deletes the whole synthetic workspace itself next,
  // the same way runOneSession deletes profileDir itself rather than calling
  // chrome.mjs's dispose().
  try {
    launcherProcess.stdin.end();
  } catch {
    /* already closed */
  }
  launcherProcess.kill("SIGTERM");

  // Track 2 repair: run the widened search before deleting the workspace (it
  // does not need the workspace to still exist, but doing it before deletion
  // keeps the ordering "capture everything, then clean up" consistent with
  // the rest of this function), excluding this run's own confined directory
  // and this probe's own temp-dir droppings from the result.
  let wideSearchResults = null;
  if (wideSearch && wideSearchMarker) {
    wideSearchResults = wideFilesystemScan(wideSearchMarker, [workspaceDir, wideSearchMarker]);
    try {
      unlinkSync(wideSearchMarker);
    } catch {
      /* already gone */
    }
  }

  await rm(workspaceDir, { recursive: true, force: true });

  return {
    label,
    vehicle: "headed (packages/derivation/live_viewing.py)",
    pid,
    profileDirExistedAfterKill: Boolean(profileStat),
    defaultProfileTopLevelEntries: topLevelEntries,
    sessionsDirEntries: sessionsEntries,
    sessionStorageDirEntries: sessionStorageEntries,
    cacheDirIsSeparateFromProfile: Boolean(cacheDir),
    cacheDirEntries,
    downloadsDirNoted: Boolean(downloadsDir),
    tokenHits: hits,
    nonLoopbackRequests,
    undoProbe: { valueAfterClear, valueAfterUndo, postNavigationUndoValue: postNavigationValue.result?.value },
    wideSearchResults,
  };
}

const GLOBAL = {};

async function main() {
  const modeArg = process.argv.slice(2).find((a) => a.startsWith("--mode="));
  const mode = modeArg ? modeArg.slice("--mode=".length) : "both";
  if (!["headless", "headed", "both"].includes(mode)) {
    throw new Error(`unknown --mode=${JSON.stringify(mode)}; expected headless, headed, or both`);
  }
  // Track 2 repair: --wide-search extends the headed vehicle's runs with the
  // widened, off-vehicle filesystem search (see wideFilesystemScan above).
  // Headless-only runs never use this — the headed vehicle is the one a
  // person actually types into, and is what Part 1 of the repair charter
  // asks about.
  const wideSearch = process.argv.slice(2).includes("--wide-search");

  log("tokens", TOKENS);
  log("mode", mode);
  const server = await startLoopbackServer(REPO_ROOT, new Set([FORM_PATH]));
  GLOBAL.serverOrigin = server.origin;
  log("server origin", server.origin);

  const results = [];
  try {
    if (mode === "headless" || mode === "both") {
      results.push(await runOneSession({ label: "headless: clean-ish (SIGTERM by probe, not dispose())", killSignal: "SIGTERM" }));
      results.push(await runOneSession({ label: "headless: unclean (SIGKILL, simulated crash)", killSignal: "SIGKILL" }));
    }
    if (mode === "headed" || mode === "both") {
      results.push(
        await runHeadedSession({ label: "headed: clean-ish (SIGTERM by probe, not close())", killSignal: "SIGTERM", wideSearch }),
      );
      results.push(
        await runHeadedSession({ label: "headed: unclean (SIGKILL, simulated crash)", killSignal: "SIGKILL", wideSearch }),
      );
    }
  } finally {
    await server.close();
  }

  for (const r of results) {
    const severeEgress = r.nonLoopbackRequests.some((req) => req.urlContainsToken || req.postDataContainsToken);
    if (severeEgress) {
      log(`\n!!! STOP CONDITION: typed token observed in a non-loopback network request in session "${r.label}" !!!`);
      log(JSON.stringify(r.nonLoopbackRequests, null, 2));
      process.stdout.write(`${JSON.stringify({ stopCondition: "network-egress-of-typed-content", mode, results }, null, 2)}\n`);
      process.exitCode = 3;
      return;
    }
    const wideTokenHit = (r.wideSearchResults || []).some((cat) => cat.newEntries.some((e) => e.tokenHit === true));
    if (wideTokenHit) {
      log(`\n!!! STOP CONDITION: typed token found outside the confined session directory in session "${r.label}" !!!`);
      log(JSON.stringify(r.wideSearchResults, null, 2));
      process.stdout.write(`${JSON.stringify({ stopCondition: "typed-content-outside-confinement", mode, results }, null, 2)}\n`);
      process.exitCode = 4;
      return;
    }
  }

  process.stdout.write(`${JSON.stringify({ tokens: TOKENS, mode, results }, null, 2)}\n`);
}

main().catch((error) => {
  log("FATAL", error.stack || String(error));
  process.exitCode = 1;
});
