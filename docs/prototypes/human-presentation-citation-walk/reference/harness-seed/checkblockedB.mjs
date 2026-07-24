const PORT = 9917;
async function cdpNewTarget(url) {
  const res = await fetch(`http://127.0.0.1:${PORT}/json/new?${encodeURIComponent(url)}`, { method: "PUT" });
  return res.json();
}
async function cdpClose(id) { await fetch(`http://127.0.0.1:${PORT}/json/close/${id}`); }
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
const target = await cdpNewTarget("about:blank");
const ws = await connect(target.webSocketDebuggerUrl);
await send(ws, "Page.enable");
await send(ws, "Page.navigate", { url: "../prototypes/cycle5-b/walk.html" });
await new Promise((resolve) => {
  const handler = (ev) => {
    const msg = JSON.parse(ev.data);
    if (msg.method === "Page.loadEventFired") { ws.removeEventListener("message", handler); resolve(); }
  };
  ws.addEventListener("message", handler);
});
await new Promise(r => setTimeout(r, 300));
const result = await evalInPage(ws, `
  (function(){
    const banner = document.querySelector('.blocked-banner');
    const cs = banner ? getComputedStyle(banner) : null;
    const sibling = document.getElementById('line-2b');
    const csSib = getComputedStyle(sibling);
    return {
      bannerBorder: cs ? cs.border : null,
      bannerBg: cs ? cs.backgroundColor : null,
      bannerRole: banner ? banner.getAttribute('role') : null,
      siblingBorder: csSib.border,
      siblingBg: csSib.backgroundColor,
      distinct: cs ? (cs.backgroundColor !== csSib.backgroundColor || cs.borderWidth !== csSib.borderWidth) : null
    };
  })();
`);
console.log(result);
await cdpClose(target.id);
