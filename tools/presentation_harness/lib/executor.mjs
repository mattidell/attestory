// Matrix executor: one fresh CDP target per (candidate, fixture, tamper)
// tuple, reusing the single already-launched browser process across the
// whole batch. A tuple's criteria share that one loaded target. Independent
// tuples continue after a criterion failure; only a genuine
// target/load/browser/injection failure is classified as `error` and forces
// the run's overall exit status to 2.

import { CDPClient } from "./cdp.mjs";
import { CHECKS } from "./checks.mjs";

class Page {
  constructor(client, sessionId) {
    this._client = client;
    this._sessionId = sessionId;
  }

  async evaluate(expression) {
    const result = await this._client.send(
      "Runtime.evaluate",
      { expression, returnByValue: true, awaitPromise: true },
      this._sessionId,
    );
    if (result.exceptionDetails) {
      throw new Error(`page evaluation threw: ${JSON.stringify(result.exceptionDetails)}`);
    }
    return result.result.value;
  }

  async tabKey() {
    for (const type of ["keyDown", "keyUp"]) {
      await this._client.send(
        "Input.dispatchKeyEvent",
        { type, key: "Tab", code: "Tab", windowsVirtualKeyCode: 9 },
        this._sessionId,
      );
    }
    await new Promise((resolve) => setTimeout(resolve, 30));
  }
}

function withTimeout(promise, timeoutMs, onTimeout) {
  let timer;
  const timeout = new Promise((_, reject) => {
    timer = setTimeout(() => reject(onTimeout()), timeoutMs);
  });
  return Promise.race([promise, timeout]).finally(() => clearTimeout(timer));
}

class TimeoutMarker extends Error {}

async function attachFreshTarget(client, origin) {
  const { targetId } = await client.send("Target.createTarget", { url: "about:blank" });
  const { sessionId } = await client.send("Target.attachToTarget", {
    targetId,
    flatten: true,
  });
  await client.send("Page.enable", {}, sessionId);
  await client.send("Runtime.enable", {}, sessionId);
  await client.send("Fetch.enable", { patterns: [{ urlPattern: "*" }] }, sessionId);

  let nonLoopbackDetected = false;
  const offRequestPaused = client.on(
    "Fetch.requestPaused",
    (params) => {
      const { requestId, request } = params;
      if (request.url.startsWith(origin)) {
        client.send("Fetch.continueRequest", { requestId }, sessionId).catch(() => {});
      } else {
        nonLoopbackDetected = true;
        client.send("Fetch.failRequest", { requestId, errorReason: "BlockedByClient" }, sessionId).catch(
          () => {},
        );
      }
    },
    sessionId,
  );

  return {
    targetId,
    sessionId,
    page: new Page(client, sessionId),
    isNonLoopbackDetected: () => nonLoopbackDetected,
    async dispose() {
      offRequestPaused();
      try {
        await client.send("Target.closeTarget", { targetId });
      } catch {
        // target/browser may already be gone
      }
    },
  };
}

function caseResult(entry, criterionId, outcome, reason) {
  return {
    candidateId: entry.candidateId,
    fixtureId: entry.fixtureId,
    tamperCaseId: entry.tamperCaseId,
    criterionId,
    outcome,
    reason,
  };
}

/**
 * Run every matrix entry against the given browser. Returns the flat,
 * manifest-ordered list of per-criterion case results.
 */
export async function runMatrix(chromeHandle, manifest, origin, connect = CDPClient.connect) {
  const client = await connect(chromeHandle.wsUrl);
  const results = [];
  let browserGone = chromeHandle.isExited();

  try {
    for (const entry of manifest.matrixEntries) {
      if (browserGone || chromeHandle.isExited()) {
        browserGone = true;
        for (const criterionId of entry.criteria) {
          results.push(caseResult(entry, criterionId, "error", "browser-exit"));
        }
        continue;
      }

      const candidate = manifest.candidatesById.get(entry.candidateId);
      const fixture = manifest.fixturesById.get(entry.fixtureId);
      const tamper = manifest.tamperById.get(entry.tamperCaseId);
      const url = `${origin}/${candidate.path}?fixture=${encodeURIComponent(fixture.path)}`;

      let handle;
      try {
        handle = await attachFreshTarget(client, origin);
      } catch (error) {
        for (const criterionId of entry.criteria) {
          results.push(caseResult(entry, criterionId, "error", "target-creation-failed"));
        }
        continue;
      }

      let tupleError = null;
      try {
        if (tamper.injection !== null) {
          try {
            await client.send(
              "Page.addScriptToEvaluateOnNewDocument",
              { source: tamper.injection },
              handle.sessionId,
            );
          } catch {
            tupleError = "injection-failed";
          }
        }

        if (!tupleError) {
          let navigateResult;
          try {
            navigateResult = await client.send(
              "Page.navigate",
              { url },
              handle.sessionId,
            );
          } catch {
            tupleError = "target-load-failed";
          }
          if (!tupleError && navigateResult && navigateResult.errorText) {
            tupleError = "target-load-failed";
          }
        }

        if (!tupleError) {
          try {
            await client.waitFor("Page.loadEventFired", handle.sessionId, manifest.timeoutMs);
          } catch {
            tupleError = "target-load-timeout";
          }
        }

        if (!tupleError && handle.isNonLoopbackDetected()) {
          tupleError = "non-loopback-request-blocked";
        }

        if (tupleError) {
          for (const criterionId of entry.criteria) {
            results.push(caseResult(entry, criterionId, "error", tupleError));
          }
          continue;
        }

        for (const criterionId of entry.criteria) {
          const criterion = manifest.criteriaById.get(criterionId);
          const checkFn = CHECKS[criterion.check];
          try {
            const outcome = await withTimeout(
              checkFn(handle.page, criterion.params),
              manifest.timeoutMs,
              () => new TimeoutMarker("criterion timed out"),
            );
            if (handle.isNonLoopbackDetected()) {
              results.push(caseResult(entry, criterionId, "error", "non-loopback-request-blocked"));
            } else if (outcome.pass) {
              results.push(caseResult(entry, criterionId, "pass", null));
            } else {
              results.push(caseResult(entry, criterionId, "fail", "criterion-unmet"));
            }
          } catch (error) {
            if (error instanceof TimeoutMarker) {
              results.push(caseResult(entry, criterionId, "error", "criterion-timeout"));
            } else {
              results.push(caseResult(entry, criterionId, "error", "criterion-thrown"));
            }
          }
        }
      } finally {
        await handle.dispose();
      }
    }
  } finally {
    client.close();
  }

  return results;
}
