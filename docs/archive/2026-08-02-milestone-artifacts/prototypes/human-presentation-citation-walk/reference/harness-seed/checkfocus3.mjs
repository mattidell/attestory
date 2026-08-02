// Uses real keyboard Tab-key dispatch (Input domain) rather than script .focus(),
// to get an accurate :focus-visible reading matching real keyboard-user behavior.
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
async function tabKey(ws) {
  await send(ws, "Input.dispatchKeyEvent", { type: "keyDown", key: "Tab", code: "Tab", windowsVirtualKeyCode: 9 });
  await send(ws, "Input.dispatchKeyEvent", { type: "keyUp", key: "Tab", code: "Tab", windowsVirtualKeyCode: 9 });
}
async function run(filePath, tabCount) {
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
  // body must have focus initially for Tab to move through the doc
  await evalInPage(ws, `document.body.focus(); document.activeElement === document.body`);
  const tabOrder = [];
  for (let i = 0; i < tabCount; i++) {
    await tabKey(ws);
    await new Promise(r => setTimeout(r, 30));
    const info = await evalInPage(ws, `
      (function(){
        const el = document.activeElement;
        if (!el || el === document.body) return { tag: null };
        const cs = getComputedStyle(el);
        return {
          tag: el.tagName,
          cls: el.className,
          id: el.id,
          text: (el.textContent||'').trim().slice(0,40),
          matchesFocusVisible: el.matches(':focus-visible'),
          outlineWidth: cs.outlineWidth,
          outlineStyle: cs.outlineStyle
        };
      })();
    `);
    tabOrder.push(info);
  }
  await cdpClose(target.id);
  return tabOrder;
}
console.log("A:", JSON.stringify(await run("../prototypes/cycle5-a/walk.html", 6), null, 2));
console.log("B:", JSON.stringify(await run("../prototypes/cycle5-b/walk.html", 6), null, 2));
