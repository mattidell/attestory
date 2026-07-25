// Ephemeral loopback-only HTTP server. Serves only the exact
// manifest-declared repository-relative candidate/fixture paths — nothing
// else in the repository is reachable, and the socket only ever binds to
// 127.0.0.1.

import { createServer } from "node:http";
import { readFile } from "node:fs/promises";
import { join } from "node:path";
import { InfraError } from "./reasons.mjs";

const FIXTURE_TOKEN = "__FIXTURE_JSON__";

/**
 * @param {string} repoRoot absolute repository root
 * @param {Set<string>} allowedPaths repo-relative paths eligible to serve
 */
export function startLoopbackServer(repoRoot, allowedPaths) {
  return new Promise((resolve, reject) => {
    const server = createServer((req, res) => {
      handleRequest(req, res, repoRoot, allowedPaths).catch(() => {
        if (!res.headersSent) res.writeHead(500);
        res.end();
      });
    });
    server.on("error", (error) => {
      reject(new InfraError("server-start-failed", `loopback server failed: ${error.message}`));
    });
    server.listen(0, "127.0.0.1", () => {
      const { port } = server.address();
      resolve({
        origin: `http://127.0.0.1:${port}`,
        close: () => new Promise((res) => server.close(() => res())),
      });
    });
  });
}

async function handleRequest(req, res, repoRoot, allowedPaths) {
  if (req.method !== "GET") {
    res.writeHead(405);
    res.end();
    return;
  }
  const url = new URL(req.url, "http://127.0.0.1");
  const pathname = decodeURIComponent(url.pathname.replace(/^\//, ""));
  if (!allowedPaths.has(pathname)) {
    res.writeHead(404);
    res.end();
    return;
  }
  let body = await readFile(join(repoRoot, pathname), "utf8");

  const fixtureParam = url.searchParams.get("fixture");
  if (fixtureParam !== null) {
    if (!allowedPaths.has(fixtureParam)) {
      res.writeHead(400);
      res.end();
      return;
    }
    const fixtureBody = await readFile(join(repoRoot, fixtureParam), "utf8");
    body = body.split(FIXTURE_TOKEN).join(fixtureBody);
  }

  const contentType = pathname.endsWith(".json") ? "application/json" : "text/html";
  res.writeHead(200, { "Content-Type": `${contentType}; charset=utf-8` });
  res.end(body);
}
