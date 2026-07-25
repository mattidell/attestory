// Ephemeral loopback-only HTTP server. Serves only the exact
// manifest-declared repository-relative candidate/fixture paths — nothing
// else in the repository is reachable, and the socket only ever binds to
// 127.0.0.1.

import { createServer } from "node:http";
import { readFile, realpath } from "node:fs/promises";
import { join, relative, isAbsolute, sep } from "node:path";
import { InfraError } from "./reasons.mjs";

const FIXTURE_TOKEN = "__FIXTURE_JSON__";

async function readConfinedFile(repoRoot, relativePath) {
  let root;
  let absolutePath;
  try {
    root = await realpath(repoRoot);
    absolutePath = await realpath(join(root, relativePath));
  } catch {
    return null;
  }
  const repoRelative = relative(root, absolutePath);
  if (repoRelative === "" || repoRelative === ".." || repoRelative.startsWith(`..${sep}`) || isAbsolute(repoRelative)) {
    return null;
  }
  try {
    return await readFile(absolutePath, "utf8");
  } catch {
    return null;
  }
}

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
  let body = await readConfinedFile(repoRoot, pathname);
  if (body === null) {
    res.writeHead(404);
    res.end();
    return;
  }

  const fixtureParam = url.searchParams.get("fixture");
  if (fixtureParam !== null) {
    if (!allowedPaths.has(fixtureParam)) {
      res.writeHead(400);
      res.end();
      return;
    }
    const fixtureBody = await readConfinedFile(repoRoot, fixtureParam);
    if (fixtureBody === null) {
      res.writeHead(400);
      res.end();
      return;
    }
    body = body.split(FIXTURE_TOKEN).join(fixtureBody);
  }

  const contentType = pathname.endsWith(".json") ? "application/json" : "text/html";
  res.writeHead(200, { "Content-Type": `${contentType}; charset=utf-8` });
  res.end(body);
}
