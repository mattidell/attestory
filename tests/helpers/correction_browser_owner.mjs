// One private browser per worker, created on first eligible request.
import { devNull } from "node:os";
import { launchChrome } from "../../tools/presentation_harness/lib/chrome.mjs";
import { createObservation } from "../../tools/presentation_harness/lib/chrome-observation.mjs";

// Only fixed labels and bounded numeric fields cross the process boundary.
let observation = { outcome: "unknown", stderr_bytes: null, exit_kind: null, exit_code: null, exit_signal: null, spawn_code: null, queue_ms: null, categories: [] };
let chrome;
let disposeOwned;
let stopping = false;
let resolveStop;
const stopped = new Promise(resolve => { resolveStop = resolve; });
function stop() {
  if (stopping) return;
  stopping = true;
  if (disposeOwned) void disposeOwned();
  resolveStop();
}
process.stdin.once("data", stop);
process.stdin.once("end", stop);
process.stdin.once("close", stop);
process.stdin.resume();
process.once("SIGTERM", stop);
process.once("SIGINT", stop);
try {
  const observer = createObservation({ label: "correction-other", output: process.env.DEMO_CHROME_TRACE || devNull, graceMs: process.env.DEMO_CHROME_TRACE ? 60000 : 0 });
  const originalBeginActive = observer.beginActive;
  observer.beginActive = queueMs => { observation.queue_ms = queueMs; originalBeginActive(queueMs); };
  const originalRecognize = observer.recognize;
  observer.recognize = name => { originalRecognize(name); if (!observation.categories.includes(name)) observation.categories.push(name); };
  const originalFinish = observer.finish;
  observer.finish = async (outcome, ready, details = {}) => {
    observation = { ...observation, outcome, ...details };
    await originalFinish(outcome, ready, details);
  };
  chrome = await launchChrome(null, { observer, onOwnership(dispose) { disposeOwned = dispose; if (stopping) void dispose(); } });
  if (!stopping) {
    process.stdout.write(JSON.stringify({ wsUrl: chrome.wsUrl, pid: chrome.pid }) + "\n");
    chrome.onExit(() => { process.exitCode = 1; stop(); });
    await stopped;
  }
} catch (error) {
  if (!stopping) {
    const reason = ["chrome-not-found", "chrome-launch-failed"].includes(error?.reasonCode) ? error.reasonCode : "unknown";
    process.stdout.write(JSON.stringify({ status: "error", reason, observation }) + "\n");
  }
  process.exitCode = 1;
} finally {
  if (chrome) await chrome.dispose();
  else if (disposeOwned) await disposeOwned();
  process.stdin.destroy();
}
