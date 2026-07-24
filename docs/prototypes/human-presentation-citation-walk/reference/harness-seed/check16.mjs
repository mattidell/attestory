const PORT = 9917;
async function cdpNewTarget(url) {
  const res = await fetch(`http://127.0.0.1:${PORT}/json/new?${encodeURIComponent(url)}`, { method: "PUT" });
  return res.json();
}
async function cdpClose(id) {
  await fetch(`http://127.0.0.1:${PORT}/json/close/${id}`);
}
function connect(wsUrl) {
  return new Promise((resolve, reject) => {
    const ws = new WebSocket(wsUrl);
    ws.addEventListener("open", () => resolve(ws));
    ws.addEventListener("error", reject);
  });
}
let msgId = 1;
function send(ws, method, params = {}) {
  return new Promise((resolve, reject) => {
    const id = msgId++;
    const handler = (ev) => {
      const msg = JSON.parse(ev.data);
      if (msg.id === id) {
        ws.removeEventListener("message", handler);
        if (msg.error) reject(new Error(JSON.stringify(msg.error)));
        else resolve(msg.result);
      }
    };
    ws.addEventListener("message", handler);
    ws.send(JSON.stringify({ id, method, params }));
  });
}
async function evalInPage(ws, expression) {
  const result = await send(ws, "Runtime.evaluate", { expression, returnByValue: true, awaitPromise: true });
  if (result.exceptionDetails) throw new Error(JSON.stringify(result.exceptionDetails));
  return result.result.value;
}
async function run(filePath) {
  const target = await cdpNewTarget("about:blank");
  const ws = await connect(target.webSocketDebuggerUrl);
  await send(ws, "Page.enable");
  await send(ws, "Page.navigate", { url: "file://" + filePath });
  await new Promise((resolve) => {
    const handler = (ev) => {
      const msg = JSON.parse(ev.data);
      if (msg.method === "Page.loadEventFired") { ws.removeEventListener("message", handler); resolve(); }
    };
    ws.addEventListener("message", handler);
  });
  await new Promise(r => setTimeout(r, 300));
  const text = await evalInPage(ws, `document.getElementById('line-16').textContent`);
  await cdpClose(target.id);
  return text;
}
console.log("A:", JSON.stringify(await run("../prototypes/cycle5-a/walk.html")));
console.log("B:", JSON.stringify(await run("../prototypes/cycle5-b/walk.html")));
