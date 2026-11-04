import { CDPClient } from "../../tools/presentation_harness/lib/cdp.mjs";
import { launchChrome } from "../../tools/presentation_harness/lib/chrome.mjs";

const pageUrl = process.argv[2];
if (!pageUrl) {
  process.stderr.write("entry-response-boundary-probe-failed\n");
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

async function clickSavedStatus(sessionId) {
  await evaluate(
    `(() => {
      const button = document.querySelector(".outcome-notice button");
      if (!button || button.disabled) throw new Error("missing-status-check");
      button.click();
      return true;
    })()`,
    sessionId,
  );
}

async function waitForCount(readCount, expected) {
  const deadline = Date.now() + 30_000;
  while (Date.now() < deadline) {
    if (readCount() >= expected) return;
    await new Promise((resolve) => setTimeout(resolve, 10));
  }
  throw new Error("browser-response-timeout");
}

async function waitForState(sessionId, expectedAmount, action = "correction") {
  const savedCopy = action === "entry"
    ? "Your W-2 entry was saved"
    : "Your W-2 correction was saved";
  await waitUntil(
    `document.body.innerText.includes("W-2 Box 1: $${expectedAmount}.00") &&
      document.body.innerText.includes(${JSON.stringify(savedCopy)})`,
    sessionId,
  );
}

async function lineLists(sessionId) {
  return await evaluate(
    `Array.from(document.querySelectorAll(".line-list"))
      .map((list) => list.innerText).join("\\n")`,
    sessionId,
  );
}

async function uncertainStatus(sessionId) {
  return await evaluate(
    `document.body.innerText.includes("This update may have been saved") &&
      Array.from(document.querySelectorAll("button")).some((button) =>
        button.textContent.includes("Check saved status")
      ) &&
      Array.from(document.querySelectorAll("button")).some((button) =>
        button.textContent.includes("Check saved status") && !button.disabled
      )`,
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

  let stateResponses = 0;
  let contributionResponses = 0;
  const requestCounts = { state: 0, contribution: 0 };
  const requests = new Map();
  const runtimeExceptions = [];
  const stopRequests = client.on(
    "Network.requestWillBeSent",
    ({ requestId, request }) => {
      const pathname = new URL(request.url).pathname;
      const record = { pathname, method: request.method };
      requests.set(requestId, record);
      if (record.method === "GET" && pathname.endsWith("/api/state")) {
        requestCounts.state += 1;
      }
      if (record.method === "POST" && pathname.endsWith("/api/contributions")) {
        requestCounts.contribution += 1;
      }
    },
    sessionId,
  );
  const stopResponses = client.on(
    "Network.responseReceived",
    ({ requestId }) => {
      const request = requests.get(requestId);
      if (request?.method === "GET" && request.pathname.endsWith("/api/state")) {
        stateResponses += 1;
      }
      if (
        request?.method === "POST" &&
        request.pathname.endsWith("/api/contributions")
      ) {
        contributionResponses += 1;
      }
    },
    sessionId,
  );
  const stopExceptions = client.on(
    "Runtime.exceptionThrown",
    ({ exceptionDetails }) => {
      runtimeExceptions.push(
        exceptionDetails.exception?.description || exceptionDetails.text || "unknown",
      );
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
  await waitForCount(() => contributionResponses, 1);
  await waitForState(sessionId, "90,000", "entry");
  const confirmedNinetyLines = await lineLists(sessionId);

  await enterAmount("91000", sessionId);
  await waitForCount(() => contributionResponses, 2);
  await waitUntil("Boolean(document.querySelector('.outcome-notice'))", sessionId);
  const malformedSubmitUncertainty = await uncertainStatus(sessionId);
  const malformedResponseCopyVisible = await evaluate(
    `document.body.innerText.includes("The server response could not be read")`,
    sessionId,
  );
  const afterMalformedSubmitLines = await lineLists(sessionId);

  let beforeStateResponse = stateResponses;
  await clickSavedStatus(sessionId);
  await waitForCount(() => stateResponses, beforeStateResponse + 1);
  await new Promise((resolve) => setTimeout(resolve, 100));
  const malformedRecoveryPreserved =
    (await uncertainStatus(sessionId)) &&
    (await lineLists(sessionId)) === confirmedNinetyLines;

  beforeStateResponse = stateResponses;
  await clickSavedStatus(sessionId);
  await waitForCount(() => stateResponses, beforeStateResponse + 1);
  await new Promise((resolve) => setTimeout(resolve, 100));
  const unusableRecoveryPreserved =
    (await uncertainStatus(sessionId)) &&
    (await lineLists(sessionId)) === confirmedNinetyLines;

  beforeStateResponse = stateResponses;
  await clickSavedStatus(sessionId);
  await waitForCount(() => stateResponses, beforeStateResponse + 1);
  await waitForState(sessionId, "91,000");
  const recoveredAfterMalformedSubmit = !(await uncertainStatus(sessionId));
  const confirmedNinetyOneLines = await lineLists(sessionId);

  await enterAmount("92000", sessionId);
  await waitForCount(() => contributionResponses, 3);
  await waitUntil("Boolean(document.querySelector('.outcome-notice'))", sessionId);
  const unusableSubmitPreserved =
    (await uncertainStatus(sessionId)) &&
    (await lineLists(sessionId)) === confirmedNinetyOneLines;

  beforeStateResponse = stateResponses;
  await clickSavedStatus(sessionId);
  await waitForCount(() => stateResponses, beforeStateResponse + 1);
  await waitForState(sessionId, "92,000");
  const recoveredAfterUnusableSubmit = !(await uncertainStatus(sessionId));

  const finalReport = {
    malformedSubmitUncertainty,
    malformedResponseCopyVisible,
    malformedSubmitKeptLastConfirmedSnapshot:
      afterMalformedSubmitLines === confirmedNinetyLines,
    malformedRecoveryPreserved,
    unusableRecoveryPreserved,
    recoveredAfterMalformedSubmit,
    unusableSubmitPreserved,
    recoveredAfterUnusableSubmit,
    contributionPosts: requestCounts.contribution,
    stateReads: requestCounts.state,
    contributionResponses,
    stateResponses,
    renderExceptionAbsent: !runtimeExceptions.some((message) =>
      message.includes("Cannot read properties of undefined"),
    ),
  };
  stopRequests();
  stopResponses();
  stopExceptions();
  process.stdout.write(`${JSON.stringify(finalReport)}\n`);
} catch {
  process.stderr.write("entry-response-boundary-probe-failed\n");
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
