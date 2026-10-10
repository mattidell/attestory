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
// recovers the outcome for that correction's token and never resubmits.

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

// One step. A confirm, a retry, or the outcome read after a confirm runs a
// real recalculation; state and choose do not, but on a loaded CI runner
// both the confirmation panel and those HTTP calls also missed a short
// deadline. Every page-load event and every DOM wait uses this budget.
// The poll returns as soon as the condition is true. It does not sleep out
// the budget, and a missed condition fails once. Python's subprocess
// timeout counts these steps in _BROWSER_STEPS and must stay above the sum.
const WAIT_MS = 600_000;

async function waitUntil(expression, sessionId) {
  const deadline = Date.now() + WAIT_MS;
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

async function submitConfirmation(sessionId, response = "no") {
  await waitUntil(`document.getElementById("confirmation").hidden === false`, sessionId);
  const clueText = await evaluate(`document.getElementById("conf-clues").textContent`, sessionId);
  await evaluate(
    `(() => {
      document.getElementById("conf-response").value = ${JSON.stringify(response)};
      document.getElementById("confirm-btn").click();
      return true;
    })()`,
    sessionId,
  );
  return clueText;
}

async function choiceTexts(sessionId) {
  await waitUntil(
    `document.querySelector("#choice-list button") !== null ||
      document.getElementById("choice-list").textContent.includes("nothing to correct") ||
      document.getElementById("choice-list").textContent.includes("Nothing here to review")`,
    sessionId,
  );
  return evaluate(
    `Array.from(document.querySelectorAll("#choice-list button")).map((b) => b.textContent)`,
    sessionId,
  );
}

async function leaksOf(sessionId) {
  const leaked = await findLeakedCodePatterns(sessionId);
  return { noLeakedCodePatterns: leaked.length === 0, leakedCodePatterns: leaked };
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

function currentRegion(text) {
  const historyAt = text.indexOf("History, not current.");
  return historyAt < 0 ? text : text.slice(0, historyAt);
}

function showsLoanAnswer(region, answer) {
  return region.includes(
    "This loan paid only for school costs. Recorded answer: " + answer + ".",
  );
}

async function reloadPage(sessionId) {
  const loaded = client.waitFor("Page.loadEventFired", sessionId, WAIT_MS);
  await client.send("Page.reload", { ignoreCache: true }, sessionId);
  await loaded;
}

async function outcomeView(sessionId) {
  const outcomeText = await evaluate(`document.getElementById("outcome-rows").textContent`, sessionId);
  const earlierText = await evaluate(`document.getElementById("saved-rows").textContent`, sessionId);
  const outcomeClass = await evaluate(`document.getElementById("outcome").className`, sessionId);
  const title = await evaluate(`document.getElementById("outcome-title").textContent`, sessionId);
  const retryHidden = await evaluate(`document.getElementById("retry-btn").hidden`, sessionId);
  const checkAgainHidden = await evaluate(
    `document.getElementById("check-again-btn") === null || document.getElementById("check-again-btn").hidden`,
    sessionId,
  );
  return { outcomeText, earlierText, outcomeClass, title, retryHidden, checkAgainHidden };
}

function recoveryFlags(view) {
  const current = currentRegion(view.outcomeText);
  const history = view.outcomeText.slice(current.length);
  return {
    showsCurrentNo: current.includes("Current.") && showsLoanAnswer(current, "no"),
    showsHistoryYes: history.includes("History, not current.") && showsLoanAnswer(history, "yes"),
    showsLine21Blocked: view.outcomeText.includes("Line 21: blocked"),
  };
}

async function runUnconfirmed(sessionId) {
  // The confirm response is dropped after the server has saved. The page
  // must recover that correction's calculated outcome -- current "no",
  // history "yes", line 21 blocked -- leave the earlier result byte-for-byte
  // the text it showed before confirmation, including 2300, and show the
  // same recovery again after a reload in this tab. It never resubmits.
  await waitUntil(
    `document.querySelector("#choice-list button") !== null &&
      document.getElementById("saved-rows").textContent.includes("2300")`,
    sessionId,
  );
  const beforeEarlier = await evaluate(`document.getElementById("saved-rows").textContent`, sessionId);
  await clickNamedChoice("Cedar", sessionId);
  await submitConfirmation(sessionId, "no");
  await waitUntil(
    `document.getElementById("outcome").className.includes("saved-and-calculated")`,
    sessionId,
  );
  const after = await outcomeView(sessionId);
  const afterFlags = recoveryFlags(after);
  await reloadPage(sessionId);
  await waitUntil(
    `document.getElementById("outcome").className.includes("saved-and-calculated") &&
      document.getElementById("saved-rows").textContent.includes("2300")`,
    sessionId,
  );
  const reloaded = await outcomeView(sessionId);
  const reloadedFlags = recoveryFlags(reloaded);
  const leaks = await leaksOf(sessionId);
  return {
    complete: true,
    outcomeShowsCurrentNo: afterFlags.showsCurrentNo,
    outcomeShowsHistoryYes: afterFlags.showsHistoryYes,
    outcomeShowsLine21Blocked: afterFlags.showsLine21Blocked,
    earlierUnchanged: after.earlierText === beforeEarlier && beforeEarlier.includes("2300"),
    reloadedShowsCurrentNo: reloadedFlags.showsCurrentNo,
    reloadedShowsHistoryYes: reloadedFlags.showsHistoryYes,
    reloadedShowsLine21Blocked: reloadedFlags.showsLine21Blocked,
    reloadedEarlierUnchanged: reloaded.earlierText === beforeEarlier,
    retryHidden: after.retryHidden === true && reloaded.retryHidden === true,
    ...leaks,
  };
}

async function runDroppedNotCalculated(sessionId) {
  // The confirm response is dropped after a real save whose calculation
  // refused. "Calculate again" recalculates that same correction.
  await clickNamedChoice("Cedar", sessionId);
  await submitConfirmation(sessionId, "no");
  await waitUntil(
    `document.getElementById("outcome").className.includes("saved-not-calculated") &&
      document.getElementById("retry-btn").hidden === false &&
      document.getElementById("retry-btn").textContent.includes("Calculate again")`,
    sessionId,
  );
  const title = await evaluate(`document.getElementById("outcome-title").textContent`, sessionId);
  await evaluate(`document.getElementById("retry-btn").click()`, sessionId);
  await waitUntil(
    `document.getElementById("outcome").className.includes("saved-and-calculated") &&
      document.getElementById("retry-btn").hidden === true`,
    sessionId,
  );
  const afterText = await evaluate(`document.getElementById("outcome-rows").textContent`, sessionId);
  const current = currentRegion(afterText);
  const leaks = await leaksOf(sessionId);
  return {
    complete: true,
    calculateAgainVisible: true,
    titleSaysCouldNotCalculate: title.includes("could not be calculated"),
    afterShowsCurrentNo: current.includes("Current.") && showsLoanAnswer(current, "no"),
    afterShowsHistory: afterText.includes("History, not current."),
    afterShowsLine21: afterText.includes("Line 21:"),
    ...leaks,
  };
}

async function runUnknownToken(sessionId) {
  // A token this session never issued. The page says it cannot determine
  // the outcome, offers no retry, and does not resubmit.
  await waitUntil(`document.getElementById("saved-rows").textContent.length > 0`, sessionId);
  await evaluate(`sessionStorage.setItem("sli-correction-token", "unknown-token")`, sessionId);
  await reloadPage(sessionId);
  await waitUntil(
    `document.getElementById("outcome-title").textContent.toLowerCase().includes("cannot determine") &&
      document.getElementById("retry-btn").hidden === true &&
      (document.getElementById("check-again-btn") === null ||
        document.getElementById("check-again-btn").hidden === true)`,
    sessionId,
  );
  const view = await outcomeView(sessionId);
  return {
    complete: true,
    statesUnknown: view.title.toLowerCase().includes("cannot determine"),
    retryHidden: view.retryHidden === true,
    checkAgainHidden: view.checkAgainHidden === true,
  };
}

async function runRefreshCalculated(sessionId) {
  // A normal calculated confirm, then a reload in the same tab, shows that
  // outcome again. The earlier result stays the original, including 2300.
  await waitUntil(
    `document.querySelector("#choice-list button") !== null &&
      document.getElementById("saved-rows").textContent.includes("2300")`,
    sessionId,
  );
  const beforeEarlier = await evaluate(`document.getElementById("saved-rows").textContent`, sessionId);
  await clickNamedChoice("Cedar", sessionId);
  await submitConfirmation(sessionId, "no");
  await waitUntil(
    `document.getElementById("outcome").className.includes("saved-and-calculated")`,
    sessionId,
  );
  const before = await outcomeView(sessionId);
  await reloadPage(sessionId);
  await waitUntil(
    `document.getElementById("outcome").className.includes("saved-and-calculated") &&
      document.getElementById("saved-rows").textContent.includes("2300")`,
    sessionId,
  );
  const after = await outcomeView(sessionId);
  const flags = recoveryFlags(after);
  const leaks = await leaksOf(sessionId);
  return {
    complete: true,
    showedCalculatedBeforeReload: before.outcomeClass.includes("saved-and-calculated"),
    showedCalculatedAfterReload: after.outcomeClass.includes("saved-and-calculated"),
    afterShowsCurrentNo: flags.showsCurrentNo,
    afterShowsHistoryYes: flags.showsHistoryYes,
    earlierUnchanged: after.earlierText === beforeEarlier && beforeEarlier.includes("2300"),
    outcomeTextStable: before.outcomeText === after.outcomeText,
    ...leaks,
  };
}

async function runRetry(sessionId) {
  await clickNamedChoice("Cedar", sessionId);
  await submitConfirmation(sessionId, "no");
  await waitUntil(
    `document.getElementById("outcome").hidden === false &&
      document.getElementById("outcome").className.includes("saved-not-calculated") &&
      document.getElementById("retry-btn").hidden === false`,
    sessionId,
  );
  const title = await evaluate(`document.getElementById("outcome-title").textContent`, sessionId);
  const beforeRetryText = await evaluate(`document.body.innerText`, sessionId);
  await evaluate(`document.getElementById("retry-btn").click()`, sessionId);
  await waitUntil(
    `document.getElementById("outcome").className.includes("saved-and-calculated") &&
      document.getElementById("retry-btn").hidden === true`,
    sessionId,
  );
  const afterText = await evaluate(`document.getElementById("outcome-rows").textContent`, sessionId);
  const afterBody = await evaluate(`document.body.innerText`, sessionId);
  const refusalShown = [beforeRetryText, afterBody].some((text) =>
    text.includes("ADOPTION_NONE_CURRENT") || text.includes("no current user adoption in scope"));
  const leaks = await leaksOf(sessionId);
  return {
    complete: true,
    titleSaysCouldNotCalculate: title.includes("could not be calculated"),
    afterShowsRecordedNo: afterText.includes("Recorded answer: no"),
    afterShowsHistory: afterText.includes("History, not current."),
    afterShowsReasonSentence: afterText.includes("did not pay only for school costs"),
    refusalTextAbsent: !refusalShown,
    ...leaks,
  };
}

async function runHistorical(sessionId) {
  await waitUntil(`document.getElementById("historical-banner").hidden === false`, sessionId);
  const banner = await evaluate(`document.getElementById("historical-banner").textContent`, sessionId);
  const heading = await evaluate(`document.getElementById("saved-heading").textContent`, sessionId);
  const buttons = await choiceTexts(sessionId);
  await clickNamedChoice("this answer has since changed", sessionId);
  await waitUntil(`document.getElementById("conf-superseded-note").hidden === false`, sessionId);
  const note = await evaluate(`document.getElementById("conf-superseded-note").textContent`, sessionId);
  const current = await evaluate(`document.getElementById("conf-current").textContent`, sessionId);
  const leaks = await leaksOf(sessionId);
  return {
    complete: true,
    bannerSaysEarlierNotCurrent: banner.includes("earlier result") && banner.includes("not the current"),
    headingSaysNotCurrent: heading.includes("not current"),
    choiceSaysChanged: buttons.some((text) => text.includes("this answer has since changed")),
    noteSaysChangedFromYesToNo: note.includes("has since changed") && note.includes("from yes")
      && note.includes("to no") && note.includes("current answer"),
    currentAnswerIsNo: current.trim() === "no",
    ...leaks,
  };
}

async function runWithdrawn(sessionId) {
  await waitUntil(
    `document.getElementById("historical-banner").hidden === false &&
      document.getElementById("choice-list").textContent.includes("nothing to correct")`,
    sessionId,
  );
  const note = await evaluate(`document.getElementById("choice-list").innerText`, sessionId);
  const buttons = await evaluate(
    `Array.from(document.querySelectorAll("#choice-list button")).map((b) => b.textContent)`,
    sessionId,
  );
  const leaks = await leaksOf(sessionId);
  return {
    complete: true,
    showsNothingToCorrect: note.includes("nothing to correct"),
    namesWithdrawnBorrowing: note.includes("Autumn study loan"),
    noReviewButtonForWithdrawn: !buttons.some((text) => text.includes("Autumn study loan")),
    ...leaks,
  };
}

async function runShared(sessionId) {
  const buttons = await choiceTexts(sessionId);
  await clickFirstChoice(sessionId);
  await waitUntil(`document.getElementById("confirmation").hidden === false`, sessionId);
  const forms = await evaluate(`document.getElementById("conf-forms").textContent`, sessionId);
  await submitConfirmation(sessionId, "no");
  await waitUntil(
    `document.getElementById("outcome").className.includes("saved-and-calculated")`,
    sessionId,
  );
  const afterText = await evaluate(`document.getElementById("outcome-rows").textContent`, sessionId);
  const leaks = await leaksOf(sessionId);
  return {
    complete: true,
    oneChoiceListsBothForms: buttons.length === 1
      && buttons[0].includes("Cedar") && buttons[0].includes("Birch"),
    confirmationListsBothForms: forms.includes("Cedar") && forms.includes("Birch"),
    bothRowsShowRecordedNo: afterText.includes("Cedar Servicing") && afterText.includes("Birch Servicing")
      && afterText.split("Recorded answer: no").length - 1 >= 2,
    bothRowsNameTheSameBorrowing: afterText.includes("Autumn study loan"),
    ...leaks,
  };
}

async function runDuplicateLabels(sessionId) {
  const buttons = await choiceTexts(sessionId);
  const starlight = buttons.filter((text) => text.includes("Starlight study loan"));
  const leaks = await leaksOf(sessionId);
  return {
    complete: true,
    twoStarlightChoices: starlight.length === 2,
    cluesDiffer: starlight.length === 2 && starlight[0] !== starlight[1]
      && starlight.every((text) => text.includes("(")),
    twinNotOffered: !buttons.some((text) => text.includes("Twin study loan")),
    ...leaks,
  };
}

async function runUnblock(sessionId) {
  await waitUntil(`document.getElementById("saved-rows").textContent.includes("blocked")`, sessionId);
  const before = await evaluate(`document.getElementById("saved-rows").textContent`, sessionId);
  await clickNamedChoice("Cedar", sessionId);
  await waitUntil(`document.getElementById("confirmation").hidden === false`, sessionId);
  const current = await evaluate(`document.getElementById("conf-current").textContent`, sessionId);
  await submitConfirmation(sessionId, "yes");
  await waitUntil(
    `document.getElementById("outcome").className.includes("saved-and-calculated")`,
    sessionId,
  );
  const afterText = await evaluate(`document.getElementById("outcome-rows").textContent`, sessionId);
  const leaks = await leaksOf(sessionId);
  return {
    complete: true,
    earlierResultBlocked: before.includes("blocked"),
    currentAnswerIsNo: current.trim() === "no",
    afterShowsRecordedYes: afterText.includes("Recorded answer: yes"),
    afterShowsHistory: afterText.includes("History, not current."),
    afterLine21Calculated: afterText.includes("Line 21:") && !afterText.includes("blocked"),
    ...leaks,
  };
}

async function runD1Visible(sessionId) {
  await waitUntil(
    `document.getElementById("saved-rows").textContent.includes("Spring study loan")`,
    sessionId,
  );
  const bodyText = await evaluate(`document.body.innerText`, sessionId);
  const leaks = await leaksOf(sessionId);
  return {
    complete: true,
    showsAutumn: bodyText.includes("Autumn study loan"),
    showsSpringDenied: bodyText.includes("Spring study loan") && bodyText.includes("denied"),
    showsRecordedNotUsed: bodyText.includes("Recorded, not used"),
    ...leaks,
  };
}

const SCENARIOS = {
  confirmed: runConfirmed,
  indistinguishable: runIndistinguishable,
  "stale-financing": runStaleFinancing,
  unconfirmed: runUnconfirmed,
  "dropped-not-calculated": runDroppedNotCalculated,
  "unknown-token": runUnknownToken,
  "refresh-calculated": runRefreshCalculated,
  retry: runRetry,
  historical: runHistorical,
  withdrawn: runWithdrawn,
  shared: runShared,
  "duplicate-labels": runDuplicateLabels,
  unblock: runUnblock,
  "d1-visible": runD1Visible,
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

  const loaded = client.waitFor("Page.loadEventFired", sessionId, WAIT_MS);
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
  if (client) {
    // Ask Chrome to exit on its own before the harness removes its
    // disposable profile. Under a loaded CI runner a signalled Chrome can
    // still be writing the profile when the removal starts (ENOTEMPTY).
    try {
      await Promise.race([
        client.send("Browser.close", {}),
        new Promise((resolve) => setTimeout(resolve, 10_000)),
      ]);
    } catch {
      // The connection closes as Chrome exits; disposal still runs below.
    }
    client.close();
  }
  if (chrome && !chrome.isExited()) {
    await new Promise((resolve) => {
      const timer = setTimeout(resolve, 30_000);
      chrome.onExit(() => {
        clearTimeout(timer);
        resolve();
      });
    });
  }
  if (chrome) await chrome.dispose();
}
