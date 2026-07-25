import test from "node:test";
import assert from "node:assert/strict";
import { runMatrix } from "../lib/executor.mjs";
import { validateManifest, MANIFEST_VERSION } from "../lib/manifest.mjs";
import { makeFakeCDPClient, makeFakeChromeHandle } from "./helpers/fake-cdp.mjs";

function twoEntryManifest() {
  return validateManifest({
    version: MANIFEST_VERSION,
    id: "demo-executor-test",
    timeout_ms: 50,
    candidates: [{ id: "cand", path: "tools/presentation_harness/examples/pages/demo-candidate.html" }],
    fixtures: [
      {
        id: "fix",
        path: "tools/presentation_harness/examples/pages/demo-fixture-published.json",
        synthetic: true,
      },
    ],
    criteria: [{ id: "crit", check: "dom-text-present", params: { selector: "h1", expected_text: "x" } }],
    tamper_cases: [
      { id: "baseline", injection: null },
      { id: "second", injection: null },
    ],
    matrix: [
      { candidate_id: "cand", fixture_id: "fix", tamper_case_id: "baseline", criteria: ["crit"] },
      { candidate_id: "cand", fixture_id: "fix", tamper_case_id: "second", criteria: ["crit"] },
    ],
  });
}

test("a target/load failure in one tuple does not block the next independent tuple", async () => {
  const manifest = twoEntryManifest();
  let navigateCalls = 0;
  const client = makeFakeCDPClient({
    handlers: {
      "Target.createTarget": () => ({ targetId: `t${navigateCalls}` }),
      "Target.attachToTarget": (params) => ({ sessionId: `s-${params.targetId}` }),
      "Page.navigate": () => {
        navigateCalls += 1;
        if (navigateCalls === 1) throw new Error("connection refused");
        return {};
      },
      "Runtime.evaluate": () => ({ result: { value: { found: true, text: "x" } } }),
    },
  });
  const chromeHandle = makeFakeChromeHandle();
  const results = await runMatrix(chromeHandle, manifest, "http://127.0.0.1:0", () => client);

  assert.equal(results.length, 2);
  assert.equal(results[0].outcome, "error");
  assert.equal(results[0].reason, "target-load-failed");
  assert.equal(results[1].outcome, "pass");
  assert.equal(results[1].reason, null);
});

test("a timed-out criterion is reported as criterion-timeout, not a false pass", async () => {
  const manifest = twoEntryManifest();
  const client = makeFakeCDPClient({
    handlers: {
      "Target.createTarget": () => ({ targetId: "t" }),
      "Target.attachToTarget": () => ({ sessionId: "s" }),
      "Runtime.evaluate": () => new Promise(() => {}), // never resolves
    },
  });
  const chromeHandle = makeFakeChromeHandle();
  const results = await runMatrix(chromeHandle, manifest, "http://127.0.0.1:0", () => client);

  for (const result of results) {
    assert.equal(result.outcome, "error");
    assert.equal(result.reason, "criterion-timeout");
  }
});

test("a thrown check error is reported as criterion-thrown", async () => {
  const manifest = twoEntryManifest();
  const client = makeFakeCDPClient({
    handlers: {
      "Target.createTarget": () => ({ targetId: "t" }),
      "Target.attachToTarget": () => ({ sessionId: "s" }),
      "Runtime.evaluate": () => {
        throw new Error("boom");
      },
    },
  });
  const chromeHandle = makeFakeChromeHandle();
  const results = await runMatrix(chromeHandle, manifest, "http://127.0.0.1:0", () => client);

  for (const result of results) {
    assert.equal(result.outcome, "error");
    assert.equal(result.reason, "criterion-thrown");
  }
});

test("a browser exit mid-batch marks every remaining tuple browser-exit and stops attaching new targets", async () => {
  const manifest = twoEntryManifest();
  let createTargetCalls = 0;
  const client = makeFakeCDPClient({
    handlers: {
      "Target.createTarget": () => {
        createTargetCalls += 1;
        return { targetId: "t" };
      },
      "Target.attachToTarget": () => ({ sessionId: "s" }),
      "Runtime.evaluate": () => ({ result: { value: { found: true, text: "x" } } }),
    },
  });
  let exitedAfterFirst = false;
  const chromeHandle = makeFakeChromeHandle({ exited: () => exitedAfterFirst });
  client.send = new Proxy(client.send, {
    async apply(target, thisArg, args) {
      const result = await Reflect.apply(target, thisArg, args);
      if (args[0] === "Target.closeTarget") exitedAfterFirst = true;
      return result;
    },
  });

  const results = await runMatrix(chromeHandle, manifest, "http://127.0.0.1:0", () => client);
  assert.equal(createTargetCalls, 1);
  assert.equal(results[0].outcome, "pass");
  assert.equal(results[1].outcome, "error");
  assert.equal(results[1].reason, "browser-exit");
});

test("a non-loopback request detected during load is reported and never counted as a pass", async () => {
  const manifest = twoEntryManifest();
  const client = makeFakeCDPClient({
    handlers: {
      "Target.createTarget": () => ({ targetId: "t" }),
      "Target.attachToTarget": () => ({ sessionId: "s" }),
      "Runtime.evaluate": () => ({ result: { value: { found: true, text: "x" } } }),
    },
    waitForImpl: {
      "Page.loadEventFired": (sessionId) => {
        client.emit("Fetch.requestPaused", { requestId: "r1", request: { url: "https://evil.example/" } }, sessionId);
        return {};
      },
    },
  });
  const chromeHandle = makeFakeChromeHandle();
  const results = await runMatrix(chromeHandle, manifest, "http://127.0.0.1:0", () => client);

  for (const result of results) {
    assert.equal(result.outcome, "error");
    assert.equal(result.reason, "non-loopback-request-blocked");
  }
});
