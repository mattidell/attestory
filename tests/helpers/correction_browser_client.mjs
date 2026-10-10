import { CDPClient } from "../../tools/presentation_harness/lib/cdp.mjs";
import { launchChrome } from "../../tools/presentation_harness/lib/chrome.mjs";

// Visible-interaction evidence for Track 1 (plan, "account-review-correction",
// Track 1 integrated review and repairs, and Track 1 corrections): a
// headless-Chrome client, modelled on entry_loop_browser_client.mjs, that
// drives the real served page and reads its DOM back. It makes no admission
// or recorder call directly -- the page's own fetch calls do. Four scenarios
// (argv[3], default "confirmed") drive the four browser-level paths the plan
// names: a normal choose/confirm/calculated correction; an indistinguishable
// choice, refused with nothing saved; a financing change discovered stale at
// confirm, not saved; and an unconfirmed (transport-failed) confirm that
// reloads state and never resubmits.

const pageUrl = process.argv[2];
const scenario = process.argv[3] || "confirmed";
if (!pageUrl) {
  process.stderr.write("correction-browser-probe-failed\n");
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
  if (result.exceptionDetails) {
    throw new Error("browser-evaluation-failed: " + JSON.stringify(result.exceptionDetails));
  }
  return result.result.value;
}

async function waitUntil(expression, sessionId) {
  // This step can include a real recorder save and recalculation under the
  // v42 production surface, run by the server this client drives over
  // loopback; under the full suite's ``-n auto`` contention (this worker's
  // Chrome process competing against the other parallel workers for every
  // core), that step needs more headroom than the W-2 entry loop's single
  // local fact write.
  const deadline = Date.now() + 25_000;
  while (Date.now() < deadline) {
    if (await evaluate(expression, sessionId)) return;
    await new Promise((resolve) => setTimeout(resolve, 25));
  }
  throw new Error("browser-state-timeout: " + expression);
}

async function clickFirstChoice(sessionId) {
  await waitUntil(`document.querySelector("#choice-list button") !== null`, sessionId);
  await evaluate(
    `(() => {
      const button = document.querySelector("#choice-list button");
      if (!button) throw new Error("no-choice");
      button.click();
      return true;
    })()`,
    sessionId,
  );
}

async function clickNamedChoice(name, sessionId) {
  await waitUntil(`document.querySelector("#choice-list button") !== null`, sessionId);
  await evaluate(
    `(() => {
      const buttons = Array.from(document.querySelectorAll("#choice-list button"));
      const target = buttons.find((b) => b.textContent.includes(${JSON.stringify(name)}));
      if (!target) throw new Error("no-matching-choice");
      target.click();
      return true;
    })()`,
    sessionId,
  );
}

async function submitConfirmation(sessionId) {
  await waitUntil(`document.getElementById("confirmation").hidden === false`, sessionId);
  const clueText = await evaluate(`document.getElementById("conf-clues").textContent`, sessionId);
  await evaluate(
    `(() => {
      document.getElementById("conf-response").value = "no";
      document.getElementById("confirm-btn").click();
      return true;
    })()`,
    sessionId,
  );
  return clueText;
}

// Track 1 explanation parity: no text node anywhere on the page may match
// an internal code pattern -- an sli./tax.us./demo. identifier, a standing
// token such as "loan-cost-no" or the bare word "none" used as a standing,
// or "plain-case-supported". Checked case-sensitively against the whole
// body's text, which is a strictly stronger check than any one text node:
// if the combined text carries none of these, no single node can.
const INTERNAL_CODE_PATTERNS = [/sli\./, /tax\.us\./, /demo\./, /loan-cost-no/, /plain-case-supported/, /\bnone\b/];

async function findLeakedCodePatterns(sessionId) {
  // ``innerText``, not ``textContent``: the latter also walks the page's
  // own <script> element, whose source text legitimately contains these
  // same substrings (the declared wording tables themselves) without ever
  // rendering them to a reader. ``innerText`` reflects only what a person
  // actually sees.
  const bodyText = await evaluate(`document.body.innerText`, sessionId);
  return INTERNAL_CODE_PATTERNS.filter((pattern) => pattern.test(bodyText)).map(String);
}

async function runConfirmed(sessionId) {
  // Before choosing: the earlier result's explanation is already visible,
  // naming the borrowing's answer and a support/block sentence -- not just
  // a form label and a standing code.
  await waitUntil(
    `document.querySelector("#choice-list button") !== null &&
      document.getElementById("saved-rows").textContent.includes("Recorded answer")`,
    sessionId,
  );
  const beforeText = await evaluate(`document.getElementById("saved-rows").textContent`, sessionId);
  const beforeLeaks = await findLeakedCodePatterns(sessionId);
  await clickNamedChoice("Cedar", sessionId);
  const clueText = await submitConfirmation(sessionId);
  await waitUntil(
    `document.getElementById("outcome").hidden === false &&
      document.getElementById("outcome").className.includes("saved-and-calculated")`,
    sessionId,
  );
  const afterText = await evaluate(`document.getElementById("outcome-rows").textContent`, sessionId);
  const savedStillText = await evaluate(`document.getElementById("saved-rows").textContent`, sessionId);
  const afterLeaks = await findLeakedCodePatterns(sessionId);
  return {
    complete: true,
    beforeShowsRecordedAnswer: beforeText.includes("Recorded answer"),
    clueShown: clueText.length > 0,
    afterShowsCurrentAndHistory: afterText.includes("Current.") && afterText.includes("History, not current."),
    afterShowsLine21Value: afterText.includes("Line 21:"),
    earlierResultUnchangedAfter: savedStillText === beforeText,
    // Cedar's correction (yes -> no) blocks the row; the new explanation
    // must name the reason, resolved from the saved presentation's own
    // line 21 section (plan, Track 1 explanation parity; defect 4).
    afterShowsReasonSentence: afterText.includes("did not pay only for school costs"),
    afterShowsWhatItAssumed: afterText.includes("What it assumed"),
    afterShowsRecordedNotUsed: afterText.includes("Recorded, not used"),
    noLeakedCodePatternsBefore: beforeLeaks.length === 0,
    noLeakedCodePatternsAfter: afterLeaks.length === 0,
    leakedCodePatterns: beforeLeaks.concat(afterLeaks),
  };
}

async function runIndistinguishable(sessionId) {
  // One choice is shown (an otherwise-unresolvable, confusable borrowing);
  // choosing it is refused by the backend as "indistinguishable". The page
  // must show an error and never show a confirmation or an outcome.
  await clickFirstChoice(sessionId);
  await waitUntil(`document.getElementById("error").hidden === false`, sessionId);
  const errorText = await evaluate(`document.getElementById("error").textContent`, sessionId);
  const confirmationHidden = await evaluate(`document.getElementById("confirmation").hidden`, sessionId);
  const outcomeHidden = await evaluate(`document.getElementById("outcome").hidden`, sessionId);
  return {
    complete: true,
    errorShown: errorText.length > 0,
    confirmationStayedHidden: confirmationHidden === true,
    outcomeStayedHidden: outcomeHidden === true,
  };
}

async function runStaleFinancing(sessionId) {
  // The confirmation is shown correctly, then (server-side, before this
  // script's confirm click) the financing relationship it showed changes.
  // The page's own confirm click must come back "not saved".
  await clickNamedChoice("Cedar", sessionId);
  await submitConfirmation(sessionId);
  await waitUntil(`document.getElementById("outcome").hidden === false`, sessionId);
  const outcomeClasses = await evaluate(
    `Array.from(document.getElementById("outcome").classList)`, sessionId);
  const title = await evaluate(`document.getElementById("outcome-title").textContent`, sessionId);
  return {
    complete: true,
    outcomeShowsNotSaved: outcomeClasses.includes("not-saved"),
    titleText: title,
  };
}

async function runUnconfirmed(sessionId) {
  // The confirm request's response is dropped at the transport level
  // (server-side, in the Python test). The page must say it could not
  // confirm, then reload the saved state -- and never resubmit on its own.
  await clickNamedChoice("Cedar", sessionId);
  await submitConfirmation(sessionId);
  await waitUntil(
    `document.getElementById("outcome").hidden === false &&
      document.getElementById("outcome").className.includes("unconfirmed")`,
    sessionId,
  );
  const title = await evaluate(`document.getElementById("outcome-title").textContent`, sessionId);
  await waitUntil(`document.getElementById("saved-rows").textContent.length > 0`, sessionId);
  const reloadedText = await evaluate(`document.getElementById("saved-rows").textContent`, sessionId);
  // Give any (unwanted) automatic resubmission a moment to have happened.
  await new Promise((resolve) => setTimeout(resolve, 500));
  return {
    complete: true,
    titleMentionsCouldNotConfirm: title.toLowerCase().includes("could not confirm"),
    reloadedStateShown: reloadedText.length > 0,
  };
}

const SCENARIOS = {
  confirmed: runConfirmed,
  indistinguishable: runIndistinguishable,
  "stale-financing": runStaleFinancing,
  unconfirmed: runUnconfirmed,
};

try {
  const run = SCENARIOS[scenario];
  if (!run) throw new Error("unknown-scenario: " + scenario);

  chrome = await launchChrome(null);
  client = await CDPClient.connect(chrome.wsUrl);
  ({ targetId } = await client.send("Target.createTarget", { url: "about:blank" }));
  const { sessionId } = await client.send("Target.attachToTarget", { targetId, flatten: true });
  await client.send("Page.enable", {}, sessionId);
  await client.send("Runtime.enable", {}, sessionId);

  const loaded = client.waitFor("Page.loadEventFired", sessionId, 10_000);
  await client.send("Page.navigate", { url: pageUrl }, sessionId);
  await loaded;

  const output = await run(sessionId);
  process.stdout.write(`${JSON.stringify(output)}\n`);
} catch (err) {
  process.stderr.write("correction-browser-probe-failed: " + String(err && err.message) + "\n");
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
