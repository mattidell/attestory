import { CDPClient } from "../../tools/presentation_harness/lib/cdp.mjs";
import { launchChrome } from "../../tools/presentation_harness/lib/chrome.mjs";

const pageUrl = process.argv[2];
if (!pageUrl) {
  process.stderr.write("entry-browser-probe-failed\n");
  process.exit(1);
}

let chrome;
let client;
let targetId;

async function evaluate(expression, sessionId) {
  const result = await client.send(
    "Runtime.evaluate",
    {
      expression,
      awaitPromise: true,
      returnByValue: true,
    },
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
  await client.send("Network.enable", {}, sessionId);

  const requests = new Set();
  const stopObserving = client.on(
    "Network.requestWillBeSent",
    ({ request }) => {
      const pathname = new URL(request.url).pathname;
      if (pathname.endsWith("/api/state")) requests.add("state");
      if (pathname.endsWith("/api/contributions")) requests.add("contributions");
    },
    sessionId,
  );

  const loaded = client.waitFor("Page.loadEventFired", sessionId, 10_000);
  await client.send("Page.navigate", { url: pageUrl }, sessionId);
  await loaded;
  await waitUntil(
    `document.querySelector("#w2-box1") !== null &&
      document.body.textContent.includes("1 missing fact · W-2 Box 1")`,
    sessionId,
  );
  await evaluate(
    `(() => {
      const input = document.querySelector("#w2-box1");
      input.value = "83456.78";
      input.dispatchEvent(new Event("input", { bubbles: true }));
      input.form.requestSubmit();
      return true;
    })()`,
    sessionId,
  );
  await waitUntil(
    `document.body.textContent.includes("0 missing facts · fully computed") &&
      document.body.textContent.includes("Accepted. The entry")`,
    sessionId,
  );
  stopObserving();
  process.stdout.write(
    `${JSON.stringify({
      complete: true,
      contributionRequest: requests.has("contributions"),
      stateRequest: requests.has("state"),
    })}\n`,
  );
} catch {
  process.stderr.write("entry-browser-probe-failed\n");
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
