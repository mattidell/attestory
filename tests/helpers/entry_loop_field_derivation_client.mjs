import { CDPClient } from "../../tools/presentation_harness/lib/cdp.mjs";
import { launchChrome } from "../../tools/presentation_harness/lib/chrome.mjs";

// Track 3 repair, F3: proves the rendered page derives from the field
// declaration rather than duplicating it in the template. The caller builds
// the compiled surface from a copy of the fixture whose field declaration has
// been mutated to distinct synthetic text; this script asserts that text
// reached the DOM and that the original, un-mutated text did not.

const pageUrl = process.argv[2];
const expectPresentJson = process.argv[3];
const expectAbsentJson = process.argv[4];
if (!pageUrl || !expectPresentJson || !expectAbsentJson) {
  process.stderr.write("entry-field-derivation-probe-failed\n");
  process.exit(1);
}
const expectPresent = JSON.parse(expectPresentJson);
const expectAbsent = JSON.parse(expectAbsentJson);

let chrome;
let client;
let targetId;

async function evaluate(expression, sessionId) {
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

async function waitUntil(expression, sessionId) {
  const deadline = Date.now() + 10_000;
  while (Date.now() < deadline) {
    if (await evaluate(expression, sessionId)) return;
    await new Promise((resolve) => setTimeout(resolve, 25));
  }
  throw new Error("browser-state-timeout");
}

try {
  chrome = await launchChrome(null);
  client = await CDPClient.connect(chrome.wsUrl);
  ({ targetId } = await client.send("Target.createTarget", { url: "about:blank" }));
  const { sessionId } = await client.send("Target.attachToTarget", {
    targetId,
    flatten: true,
  });
  await client.send("Page.enable", {}, sessionId);
  await client.send("Runtime.enable", {}, sessionId);

  const loaded = client.waitFor("Page.loadEventFired", sessionId, 10_000);
  await client.send("Page.navigate", { url: pageUrl }, sessionId);
  await loaded;
  await waitUntil(
    `document.querySelector("#w2-box1") !== null`,
    sessionId,
  );

  const bodyText = await evaluate("document.body.textContent", sessionId);
  const present = expectPresent.every((text) => bodyText.includes(text));
  const absent = expectAbsent.every((text) => !bodyText.includes(text));

  process.stdout.write(`${JSON.stringify({ present, absent })}\n`);
} catch {
  process.stderr.write("entry-field-derivation-probe-failed\n");
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
