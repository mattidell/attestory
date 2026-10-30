// Test-session-only startup gate. An abandoned slot is never stolen: waiters
// fail within a bound, since its browser might still be starting.
import { mkdir, rm } from "node:fs/promises";
import { join } from "node:path";
import { InfraError } from "./reasons.mjs";

export async function acquireStartupSlot(root, { timeoutMs = 120000, cancelled = () => false } = {}) {
  const slot = join(root, "chrome-startup-slot");
  const started = performance.now();
  for (;;) {
    if (cancelled()) throw new InfraError("chrome-launch-failed", "Chrome startup queue cancelled");
    try {
      await mkdir(slot);
      let released = false;
      return { queueMs: Math.round(performance.now() - started), async release() {
        if (!released) { released = true; await rm(slot, { recursive: true, force: true }); }
      } };
    } catch (error) {
      if (error.code !== "EEXIST") throw new InfraError("chrome-launch-failed", "Chrome startup queue unavailable");
    }
    if (performance.now() - started >= timeoutMs) throw new InfraError("chrome-launch-failed", "Chrome startup queue timed out");
    await new Promise(resolve => setTimeout(resolve, 25));
  }
}
