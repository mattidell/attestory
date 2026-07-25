import test from "node:test";
import assert from "node:assert/strict";
import { mkdtemp, writeFile, rm } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { startLoopbackServer } from "../lib/server.mjs";

async function withRepoRoot(fn) {
  const root = await mkdtemp(join(tmpdir(), "presentation-harness-server-test-"));
  try {
    await fn(root);
  } finally {
    await rm(root, { recursive: true, force: true });
  }
}

test("the server only binds to the loopback interface", async () => {
  await withRepoRoot(async (root) => {
    const server = await startLoopbackServer(root, new Set());
    assert.match(server.origin, /^http:\/\/127\.0\.0\.1:\d+$/);
    await server.close();
  });
});

test("a path outside the allowlist is refused even if it exists on disk", async () => {
  await withRepoRoot(async (root) => {
    await writeFile(join(root, "secret.html"), "<html>should not be served</html>");
    const server = await startLoopbackServer(root, new Set());
    const response = await fetch(`${server.origin}/secret.html`);
    assert.equal(response.status, 404);
    await server.close();
  });
});

test("an allowlisted candidate is served with fixture content substituted in", async () => {
  await withRepoRoot(async (root) => {
    await writeFile(join(root, "candidate.html"), "<script>const F = __FIXTURE_JSON__;</script>");
    await writeFile(join(root, "fixture.json"), '{"heading":"demo"}');
    const server = await startLoopbackServer(
      root,
      new Set(["candidate.html", "fixture.json"]),
    );
    const response = await fetch(`${server.origin}/candidate.html?fixture=${encodeURIComponent("fixture.json")}`);
    const body = await response.text();
    assert.equal(response.status, 200);
    assert.match(body, /const F = \{"heading":"demo"\};/);
    await server.close();
  });
});

test("a fixture reference outside the allowlist is refused", async () => {
  await withRepoRoot(async (root) => {
    await writeFile(join(root, "candidate.html"), "<script>const F = __FIXTURE_JSON__;</script>");
    await writeFile(join(root, "outside.json"), '{"leak":true}');
    const server = await startLoopbackServer(root, new Set(["candidate.html"]));
    const response = await fetch(`${server.origin}/candidate.html?fixture=outside.json`);
    assert.equal(response.status, 400);
    await server.close();
  });
});
