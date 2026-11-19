#!/usr/bin/env node
// Synthetic Chrome for process-group cleanup tests. Not a browser: a main
// process that serves just enough of the DevTools protocol for the saved-page
// observer, plus (by mode) a helper process that
//   - outlives the main process and ignores SIGTERM,
//   - inherits the main process's stderr pipe and holds it open,
//   - keeps writing files into the profile directory.
// Modes (DEMO_FAKE_MODE): "helper" (default) or "locked" (an unremovable file
// tree inside the profile). DEMO_FAKE_DIR receives helper.pid.
import { spawn } from "node:child_process";
import { chmodSync, existsSync, mkdirSync, writeFileSync } from "node:fs";
import { createServer } from "node:http";
import { createHash } from "node:crypto";
import { join } from "node:path";
import { fileURLToPath } from "node:url";

const profile = process.argv.find((a) => a.startsWith("--user-data-dir=")).split("=").slice(1).join("=");
const mode = process.env.DEMO_FAKE_MODE || "helper";
const stateDir = process.env.DEMO_FAKE_DIR;
writeFileSync(join(stateDir, "profile.path"), profile);

if (process.argv[2] === "--helper") {
  process.on("SIGTERM", () => {});
  writeFileSync(join(stateDir, "helper.pid"), String(process.pid));
  let n = 0;
  const timer = setInterval(() => {
    for (let k = 0; k < 50; k += 1) {
      try { writeFileSync(join(profile, `late-${n++}`), "x"); } catch { /* profile removed */ }
    }
  }, 1);
  // A bounded lifetime so a failed test cannot leave this process behind.
  setTimeout(() => { clearInterval(timer); process.exit(0); }, 60000);
} else {
  if (mode === "helper") {
    spawn(process.execPath, [fileURLToPath(import.meta.url), "--helper", `--user-data-dir=${profile}`],
      { stdio: ["ignore", "ignore", 2] }).unref();
  } else if (mode === "locked") {
    const locked = join(profile, "locked");
    mkdirSync(locked);
    writeFileSync(join(locked, "pinned"), "x");
    chmodSync(locked, 0o500);
  }
  const answers = {
    "Browser.getVersion": () => ({ product: "Chrome/demo" }),
    "Target.createBrowserContext": () => ({ browserContextId: "demo-context" }),
    "Target.createTarget": () => ({ targetId: "demo-target" }),
    "Target.attachToTarget": () => ({ sessionId: "demo-session" }),
    "Page.navigate": () => ({ frameId: "demo-frame" }),
    "Runtime.evaluate": () => ({ result: { value: { id: "demo-1", lines: [] } } }),
  };
  const server = createServer();
  server.on("upgrade", (request, socket) => {
    const accept = createHash("sha1")
      .update(`${request.headers["sec-websocket-key"]}258EAFA5-E914-47DA-95CA-C5AB0DC85B11`).digest("base64");
    socket.write(`HTTP/1.1 101 Switching Protocols\r\nUpgrade: websocket\r\nConnection: Upgrade\r\nSec-WebSocket-Accept: ${accept}\r\n\r\n`);
    const send = (object) => {
      const body = Buffer.from(JSON.stringify(object));
      const header = body.length < 126 ? Buffer.from([0x81, body.length])
        : Buffer.from([0x81, 126, body.length >> 8, body.length & 255]);
      socket.write(Buffer.concat([header, body]));
    };
    let buffered = Buffer.alloc(0);
    socket.on("data", (chunk) => {
      buffered = Buffer.concat([buffered, chunk]);
      for (;;) {
        if (buffered.length < 2) return;
        let length = buffered[1] & 127;
        let offset = 2;
        if (length === 126) { if (buffered.length < 4) return; length = buffered.readUInt16BE(2); offset = 4; }
        else if (length === 127) { if (buffered.length < 10) return; length = Number(buffered.readBigUInt64BE(2)); offset = 10; }
        if (buffered.length < offset + 4 + length) return;
        const mask = buffered.subarray(offset, offset + 4);
        const payload = Buffer.from(buffered.subarray(offset + 4, offset + 4 + length));
        for (let i = 0; i < payload.length; i += 1) payload[i] ^= mask[i % 4];
        buffered = buffered.subarray(offset + 4 + length);
        if ((payload.length === 0)) continue;
        let message;
        try { message = JSON.parse(payload.toString("utf8")); } catch { continue; }
        const answer = answers[message.method] ? answers[message.method]() : {};
        send({ id: message.id, result: answer, ...(message.sessionId ? { sessionId: message.sessionId } : {}) });
        if (message.method === "Page.navigate") send({ method: "Page.loadEventFired", params: {}, sessionId: message.sessionId });
      }
    });
    socket.on("error", () => {});
  });
  // Advertise readiness only once the helper is running, so a test never
  // observes a cleanup that raced ahead of the helper's start.
  const advertise = () => {
    if (mode === "helper" && !existsSync(join(stateDir, "helper.pid"))) { setTimeout(advertise, 10); return; }
    writeFileSync(join(profile, "DevToolsActivePort"), `${server.address().port}\n/devtools/browser/demo\n`);
  };
  server.listen(0, "127.0.0.1", advertise);
  process.on("SIGTERM", () => process.exit(0));
}
