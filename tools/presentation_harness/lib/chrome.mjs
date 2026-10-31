// Isolated, reusable Chrome process lifecycle: locate an executable, launch
// it against a fresh temporary profile with remote debugging on an
// OS-assigned port, and guarantee cleanup on every exit path.

import { spawn } from "node:child_process";
import { mkdtemp, readFile, rm, stat } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { InfraError } from "./reasons.mjs";
import { acquireStartupSlot } from "./startup-coordinator.mjs";

const CANDIDATE_PATHS = [
  "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
  "/Applications/Chromium.app/Contents/MacOS/Chromium",
  "/usr/bin/google-chrome",
  "/usr/bin/google-chrome-stable",
  "/usr/bin/chromium",
  "/usr/bin/chromium-browser",
];

async function pathIsExecutable(path) {
  try {
    const { access, constants } = await import("node:fs/promises");
    await access(path, constants.X_OK);
    return true;
  } catch {
    return false;
  }
}

/** Resolve a Chrome executable. Never downloads or installs one. */
export async function resolveChromeExecutable(explicitPath) {
  const candidates = [];
  if (explicitPath) candidates.push(explicitPath);
  if (process.env.PRESENTATION_HARNESS_CHROME) {
    candidates.push(process.env.PRESENTATION_HARNESS_CHROME);
  }
  candidates.push(...CANDIDATE_PATHS);
  for (const candidate of candidates) {
    if (await pathIsExecutable(candidate)) return candidate;
  }
  throw new InfraError(
    "chrome-not-found",
    "no installed Chrome executable found; pass --chrome <path> or set PRESENTATION_HARNESS_CHROME",
  );
}

async function waitForDevToolsActivePort(profileDir, timeoutMs, state, observer) {
  const filePath = join(profileDir, "DevToolsActivePort");
  const deadline = Date.now() + timeoutMs;
  let originalError = null;
  let graceDeadline = null;
  for (;;) {
    if (state.cancelled()) {
      if (observer) await observer.finish("cancelled", false, state.details()).catch(() => {});
      throw originalError || new InfraError("chrome-launch-failed", "Chrome launch cancelled");
    }
    const failure = state.failure();
    if (failure) {
      if (observer) await observer.finish(originalError ? "exit_after_deadline" : "exit_before_ready", false, state.details()).catch(() => {});
      throw originalError || new InfraError("chrome-launch-failed", failure);
    }
    let fileState = "missing";
    let result = null;
    let metadata = null;
    try {
      const contents = await readFile(filePath, "utf8");
      if (observer) { try { const info = await stat(filePath); metadata = { size: info.size, mtime_wall_ms: info.mtimeMs }; } catch { /* unavailable */ } }
      const [portLine, pathLine] = contents.split("\n");
      const port = Number.parseInt(portLine, 10);
      if (Number.isInteger(port) && port > 0) {
        fileState = "ready";
        result = { port, browserPath: pathLine ? pathLine.trim() : "" };
      } else fileState = "malformed";
    } catch (error) {
      const code = ["EACCES", "EPERM", "EISDIR", "EIO"].includes(error.code) ? error.code : "other";
      fileState = error.code === "ENOENT" ? "missing" : `unreadable:${code}`;
    }
    if (observer) await observer.observe(fileState, state.pid(), true, metadata).catch(() => {});
    const now = Date.now();
    if (result && !originalError) {
      if (observer) await observer.finish("ready_accepted", true, state.details()).catch(() => {});
      return result;
    }
    if (!originalError && now > deadline) {
      if (observer) { try { observer.deadline(); } catch { /* diagnostic only */ } }
      originalError = new InfraError("chrome-launch-failed", `Chrome stayed alive without DevToolsActivePort before the launch timeout; ${state.diagnostics()}`);
      if (!observer) throw originalError;
      graceDeadline = performance.now() + observer.graceMs;
    }
    if (result) {
      if (observer) await observer.finish("ready_after_deadline", true, state.details()).catch(() => {});
      throw originalError;
    }
    if (originalError && performance.now() >= graceDeadline) {
      await observer.finish("not_ready_after_grace", false, state.details()).catch(() => {});
      throw originalError;
    }
    await new Promise(resolve => setTimeout(resolve, 25));
  }
}

/**
 * Launch one isolated Chrome process with a fresh temporary profile.
 * Returns a handle with { wsUrl, process, dispose() }.
 */
async function launchChromeOwned(explicitPath, { launchTimeoutMs = 10000, onOwnership = null, observer = null } = {}) {
  let executable;
  try { executable = await resolveChromeExecutable(explicitPath); }
  catch (error) { if (observer) await observer.finish("resolve_failure", false, { exit_kind: "resolve_error", stderr_bytes: 0 }).catch(() => {}); throw error; }
  const profileDir = await mkdtemp(join(tmpdir(), "presentation-harness-profile-"));

  const args = [
    "--headless=new",
    "--disable-gpu",
    "--no-first-run",
    "--no-default-browser-check",
    "--disable-extensions",
    "--disable-background-networking",
    "--disable-sync",
    "--disable-translate",
    "--mute-audio",
    `--user-data-dir=${profileDir}`,
    "--remote-debugging-port=0",
    "about:blank",
  ];
  if (typeof process.getuid === "function" && process.getuid() === 0) {
    args.unshift("--no-sandbox");
  }

  let child = null;
  let exited = false;
  let exitInfo = null;
  let disposePromise = null;
  let spawnError = null;
  // Drain stderr continuously, retaining only fixed diagnostic categories. Never
  // emit raw browser output, paths or data; memory stays bounded under a flood.
  let stderrTail = "";
  let stderrBytes = 0;
  const categories = new Set();
  // Only fixed phrases are emitted; unknown output is represented by its
  // byte count. This prevents paths, URLs and arbitrary stderr entering logs.
  const patterns = [
    ["devtools-active-port-write-error", /Error writing DevTools active port to file/],
    ["devtools-http-server-start-error", /Cannot start http server for devtools\./],
    ["pthread-create-resource-unavailable", /pthread_create[^\n]{0,120}resource temporarily unavailable/i],
    ["thread-start-resource-unavailable", /(?:failed to start|start_thread)[^\n]{0,120}resource temporarily unavailable/i],
    ["cannot-allocate-memory", /cannot allocate memory/i],
    ["out-of-memory", /out of memory/i],
    ["too-many-open-files", /too many open files/i],
    ["no-usable-sandbox", /no usable sandbox/i],
    ["running-as-root-without-no-sandbox", /running as root without --no-sandbox/i],
    ["failed-to-move-to-new-namespace", /failed to move to new namespace/i],
    ["user-namespace-operation-not-permitted", /(?:user namespace|unshare)[^\n]{0,120}operation not permitted/i],
    ["profile-in-use", /(?:profile|user data directory)[^\n]{0,120}(?:already in use|appears to be in use)/i],
    ["singleton-lock-failed", /failed to create[^\n]{0,120}singletonlock/i],
    ["devtools-bind-address-in-use", /(?:bind|address)[^\n]{0,120}address already in use/i],
    ["missing-x-server", /missing x server or \$display/i],
    ["crashpad-handler-failed", /crashpad[^\n]{0,120}(?:failed|error)/i],
    ["zygote-fork-failed", /(?:fork|zygote)[^\n]{0,120}(?:failed|resource temporarily unavailable)/i],
  ];
  function captureStderr(chunk) {
    stderrBytes = Math.min(Number.MAX_SAFE_INTEGER, stderrBytes + chunk.length);
    const text = stderrTail + chunk.toString("utf8");
    if (observer && /DevTools listening on\s/i.test(text)) { try { observer.advertised(); } catch { /* diagnostic only */ } }
    for (const [name, pattern] of patterns) if (pattern.test(text)) { categories.add(name); if (observer) { try { observer.recognize(name); } catch { /* diagnostic only */ } } }
    stderrTail = text.slice(-256);
  }
  const diagnostics = () => `stderr_bytes=${stderrBytes}; stderr_categories=${[...categories].sort().join(",") || "none"}`;
  const state = {
    cancelled: () => Boolean(disposePromise),
    pid: () => child?.pid || null,
    details: () => ({ stderr_bytes: stderrBytes,
      exit_kind: spawnError ? "spawn_error" : exited ? "exited" : "alive",
      exit_code: Number.isInteger(exitInfo?.code) ? exitInfo.code : null,
      exit_signal: ["SIGTERM", "SIGKILL", "SIGABRT", "SIGSEGV", "SIGTRAP", "SIGILL", "SIGBUS"].includes(exitInfo?.signal) ? exitInfo.signal : null,
      spawn_code: ["ENOENT", "EACCES", "ENOEXEC", "ENOMEM", "EMFILE", "ENFILE", "EAGAIN"].includes(spawnError) ? spawnError : null }),
    diagnostics,
    failure: () => spawnError ? `Chrome spawn failed (code=${spawnError}); ${diagnostics()}` :
      exited ? `Chrome exited before readiness (code=${exitInfo.code}, signal=${exitInfo.signal}); ${diagnostics()}` : null,
  };

  async function dispose() {
    if (disposePromise) return disposePromise;
    disposePromise = (async () => {
      if (child && !exited) {
        child.kill("SIGTERM");
        await new Promise((resolve) => {
          const timer = setTimeout(() => {
            if (!exited) child.kill("SIGKILL");
            resolve();
          }, 3000);
          child.once("exit", () => {
            clearTimeout(timer);
            resolve();
          });
        });
      }
      await rm(profileDir, { recursive: true, force: true });
    })();
    return disposePromise;
  }

  // The profile is owned before spawn, and the child is covered immediately
  // after it exists. The runner can therefore clean both while the launch
  // handshake is still waiting for DevToolsActivePort.
  try {
    if (onOwnership) onOwnership(dispose);
  } catch (error) {
    await dispose();
    throw error;
  }
  if (disposePromise) {
    if (observer) await observer.finish("cancelled", false, state.details()).catch(() => {});
    await dispose(); throw new InfraError("chrome-launch-failed", "Chrome launch cancelled");
  }

  try {
    child = spawn(executable, args, { stdio: ["ignore", "ignore", "pipe"] });
  } catch (error) {
    if (observer) await observer.finish("spawn_failure", false, { stderr_bytes: 0, exit_kind: "spawn_error", spawn_code: ["ENOENT", "EACCES", "ENOEXEC", "ENOMEM", "EMFILE", "ENFILE", "EAGAIN"].includes(error.code) ? error.code : null }).catch(() => {});
    await dispose();
    throw new InfraError("chrome-launch-failed", `failed to spawn Chrome (code=${error.code || "unknown"})`);
  }

  child.stderr.on("data", captureStderr);
  child.once("error", (error) => { spawnError = error.code || "unknown"; exited = true; });
  child.once("exit", (code, signal) => {
    exited = true;
    exitInfo = { code, signal };
  });

  let devtools;
  try {
    devtools = await waitForDevToolsActivePort(profileDir, launchTimeoutMs, state, observer);
  } catch (error) {
    await dispose();
    throw error;
  }

  if (exited || disposePromise) {
    await dispose();
    throw new InfraError(
      "chrome-launch-failed",
      `Chrome exited during launch (code=${exitInfo?.code}, signal=${exitInfo?.signal})`,
    );
  }

  const wsUrl = `ws://127.0.0.1:${devtools.port}${devtools.browserPath}`;

  return {
    wsUrl,
    pid: child.pid,
    onExit(handler) {
      child.on("exit", handler);
    },
    isExited() {
      return exited;
    },
    dispose,
  };
}

// No gate is installed for standalone callers. Queue time is outside the
// existing active launch timeout and the slot covers failed-launch cleanup.
export async function launchChrome(explicitPath, options = {}) {
  const root = process.env.DEMO_CHROME_STARTUP_DIR;
  if (!root) return launchChromeOwned(explicitPath, options);
  let cancelled = false;
  let disposeOwned = null;
  if (options.onOwnership) options.onOwnership(async () => {
    cancelled = true;
    if (disposeOwned) await disposeOwned();
  });
  const queueStarted = performance.now();
  let slot;
  try { slot = await acquireStartupSlot(root, { cancelled: () => cancelled, timeoutMs: options.queueTimeoutMs ?? 120000 }); }
  catch (error) {
    if (options.observer) await options.observer.finish("queue_failed", false, {
      queue_ms: Math.round(performance.now() - queueStarted), exit_kind: "queue_error", stderr_bytes: 0,
    }).catch(() => {});
    throw error;
  }
  if (options.observer) { try { options.observer.beginActive(slot.queueMs); } catch { /* diagnostic only */ } }
  let chrome = null;
  let failure = null;
  try {
    if (cancelled) throw new InfraError("chrome-launch-failed", "Chrome startup queue cancelled");
    chrome = await launchChromeOwned(explicitPath, { ...options, onOwnership(dispose) {
      disposeOwned = dispose;
      if (cancelled) void dispose();
    } });
  } catch (error) { failure = error; }
  try { await slot.release(); }
  catch {
    if (chrome) await chrome.dispose();
    if (failure) throw failure;
    throw new InfraError("chrome-launch-failed", "Chrome startup queue release failed");
  }
  if (failure) throw failure;
  return chrome;
}
