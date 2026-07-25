// Isolated, reusable Chrome process lifecycle: locate an executable, launch
// it against a fresh temporary profile with remote debugging on an
// OS-assigned port, and guarantee cleanup on every exit path.

import { spawn } from "node:child_process";
import { mkdtemp, readFile, rm } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { InfraError } from "./reasons.mjs";

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

async function waitForDevToolsActivePort(profileDir, timeoutMs) {
  const filePath = join(profileDir, "DevToolsActivePort");
  const deadline = Date.now() + timeoutMs;
  for (;;) {
    try {
      const contents = await readFile(filePath, "utf8");
      const [portLine, pathLine] = contents.split("\n");
      const port = Number.parseInt(portLine, 10);
      if (Number.isInteger(port) && port > 0) {
        return { port, browserPath: pathLine ? pathLine.trim() : "" };
      }
    } catch {
      // file not written yet
    }
    if (Date.now() > deadline) {
      throw new InfraError(
        "chrome-launch-failed",
        "Chrome did not write DevToolsActivePort before the launch timeout",
      );
    }
    await new Promise((resolve) => setTimeout(resolve, 25));
  }
}

/**
 * Launch one isolated Chrome process with a fresh temporary profile.
 * Returns a handle with { wsUrl, process, dispose() }.
 */
export async function launchChrome(explicitPath, { launchTimeoutMs = 10000 } = {}) {
  const executable = await resolveChromeExecutable(explicitPath);
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

  let child;
  try {
    child = spawn(executable, args, { stdio: "ignore" });
  } catch (error) {
    await rm(profileDir, { recursive: true, force: true });
    throw new InfraError("chrome-launch-failed", `failed to spawn Chrome: ${error.message}`);
  }

  let exited = false;
  let exitInfo = null;
  child.once("exit", (code, signal) => {
    exited = true;
    exitInfo = { code, signal };
  });

  let devtools;
  try {
    devtools = await waitForDevToolsActivePort(profileDir, launchTimeoutMs);
  } catch (error) {
    child.kill("SIGKILL");
    await rm(profileDir, { recursive: true, force: true });
    throw error;
  }

  if (exited) {
    await rm(profileDir, { recursive: true, force: true });
    throw new InfraError(
      "chrome-launch-failed",
      `Chrome exited during launch (code=${exitInfo?.code}, signal=${exitInfo?.signal})`,
    );
  }

  const wsUrl = `ws://127.0.0.1:${devtools.port}${devtools.browserPath}`;

  async function dispose() {
    if (!exited) {
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
  }

  return {
    wsUrl,
    onExit(handler) {
      child.on("exit", handler);
    },
    isExited() {
      return exited;
    },
    dispose,
  };
}
