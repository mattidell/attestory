import { CDPClient } from "../../tools/presentation_harness/lib/cdp.mjs";
import { launchChrome } from "../../tools/presentation_harness/lib/chrome.mjs";

const pageUrl = process.argv[2];
if (!pageUrl) {
  process.stderr.write("entry-guidance-browser-probe-failed\n");
  process.exit(1);
}

let chrome;
let client;
let targetId;

async function evaluate(expression, sessionId) {
  const result = await client.send(
    "Runtime.evaluate",
    { expression, awaitPromise: true, returnByValue: true },
    sessionId,
  );
  if (result.exceptionDetails) throw new Error("browser-evaluation-failed");
  return result.result.value;
}

async function waitUntil(expression, sessionId) {
  const deadline = Date.now() + 30_000;
  while (Date.now() < deadline) {
    if (await evaluate(expression, sessionId)) return;
    await new Promise((resolve) => setTimeout(resolve, 25));
  }
  throw new Error("browser-state-timeout");
}

async function enterAmount(amount, sessionId) {
  await evaluate(
    `(() => {
      const input = document.querySelector("#w2-box1");
      if (!input) throw new Error("missing-w2-input");
      input.value = ${JSON.stringify(amount)};
      input.dispatchEvent(new Event("input", { bubbles: true }));
      input.form.requestSubmit();
      return true;
    })()`,
    sessionId,
  );
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

  let stateRequests = 0;
  let contributionRequests = 0;
  const stopObserving = client.on(
    "Network.requestWillBeSent",
    ({ request }) => {
      const pathname = new URL(request.url).pathname;
      if (pathname.endsWith("/api/state")) stateRequests += 1;
      if (pathname.endsWith("/api/contributions")) contributionRequests += 1;
    },
    sessionId,
  );

  const loaded = client.waitFor("Page.loadEventFired", sessionId, 10_000);
  await client.send("Page.navigate", { url: pageUrl }, sessionId);
  await loaded;
  await waitUntil(
    `document.querySelector("#w2-box1") !== null &&
      document.body.innerText.includes("W-2 Box 1 is not saved yet")`,
    sessionId,
  );

  await enterAmount("90000", sessionId);
  await waitUntil(
    `document.body.innerText.includes("W-2 Box 1 is saved in this return") &&
      document.body.innerText.includes("More return information is needed")`,
    sessionId,
  );

  await enterAmount("91000", sessionId);
  await waitUntil(
    `document.body.innerText.includes("The connection ended before this update could be confirmed") &&
      Array.from(document.querySelectorAll("button")).some((button) => button.textContent.includes("Check saved status"))`,
    sessionId,
  );
  const uncertainMessageVisible = await evaluate(
    `document.body.innerText.includes("It may have been saved") &&
      document.body.innerText.includes("Check the current entry before trying again")`,
    sessionId,
  );
  await evaluate(
    `(() => {
      const button = Array.from(document.querySelectorAll("button"))
        .find((candidate) => candidate.textContent.includes("Check saved status"));
      if (!button) throw new Error("missing-status-check");
      button.click();
      return true;
    })()`,
    sessionId,
  );
  await waitUntil(
    `document.body.innerText.includes("W-2 Box 1: $91,000.00") &&
      document.body.innerText.includes("Your W-2 correction was saved") &&
      document.body.innerText.includes("No current calculation authorization is recorded")`,
    sessionId,
  );

  const lineRows = await evaluate(
    `(() => {
      return Array.from(document.querySelectorAll(".line-list li"))
        .map((item) => item.innerText);
    })()`,
    sessionId,
  );
  const blockedRow = lineRows.find((row) => row.includes("12E")) || "";
  const bodyText = await evaluate("document.body.innerText", sessionId);

  await enterAmount("92000", sessionId);
  await waitUntil(
    `document.body.innerText.includes("The latest update is saved; no new calculation is available.") &&
      document.body.innerText.includes("W-2 Box 1: $92,000.00") &&
      document.body.innerText.includes("The figures below are from the prior calculation.")`,
    sessionId,
  );
  const postSaveFailureCopyVisible = await evaluate(
    `document.body.innerText.includes("No current calculation authorization is recorded for this result") &&
      document.body.innerText.includes("No authorization status was produced for the latest update")`,
    sessionId,
  );
  await evaluate(
    `(() => {
      const button = Array.from(document.querySelectorAll("button"))
        .find((candidate) => candidate.textContent.includes("Check saved status"));
      if (!button) throw new Error("missing-post-save-status-check");
      button.click();
      return true;
    })()`,
    sessionId,
  );
  await waitUntil(
    `document.body.innerText.includes("W-2 Box 1: $92,000.00") &&
      document.body.innerText.includes("The latest update is saved; no new calculation is available.")`,
    sessionId,
  );
  const finalBodyText = await evaluate("document.body.innerText", sessionId);

  stopObserving();
  process.stdout.write(
    `${JSON.stringify({
      savedAfterRecovery: bodyText.includes("W-2 Box 1: $91,000.00"),
      uncertaintyShown: uncertainMessageVisible,
      noResubmit: contributionRequests === 3,
      stateReadForRecovery: stateRequests >= 3,
      blockedNullNotZero: blockedRow.includes("Unavailable") && !blockedRow.includes("$0.00"),
      genericFallbackVisible: blockedRow.includes("This screen cannot identify which answer"),
      authorizationCurrentnessSeparate: bodyText.includes("No current calculation authorization is recorded"),
      postSaveFailureCopyVisible,
      postSaveAmountRecovered: finalBodyText.includes("W-2 Box 1: $92,000.00"),
      noInternalIdentifiers: !/tax\.us\.|demo\.|DEPENDENCY_ABSENT|standard_deduction/.test(finalBodyText),
    })}\n`,
  );
} catch {
  process.stderr.write("entry-guidance-browser-probe-failed\n");
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
