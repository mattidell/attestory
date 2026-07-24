// Live fault-injection test of fail-loud / blast-containment: monkeypatch
// Object.freeze (called on the FACTS object in both prototypes) to delete
// the demo-fact-int-002 record before it's frozen, forcing renderCitation()
// to hit its "unknown fact id" throw for every site citing that fact, and
// checking that (a) a visible on-page error appears scoped to the affected
// section(s) only, (b) unrelated sections still render correctly, and
// (c) no raw/tampered value leaks into the error text.
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

const INJECT = `
  (function(){
    const origFreeze = Object.freeze;
    Object.freeze = function(obj){
      if (obj && typeof obj === 'object' && obj['demo-fact-int-002']) {
        delete obj['demo-fact-int-002'];
      }
      return origFreeze(obj);
    };
  })();
`;

async function run(filePath) {
  const target = await cdpNewTarget("about:blank");
  const ws = await connect(target.webSocketDebuggerUrl);
  await send(ws, "Page.enable");
  await send(ws, "Page.addScriptToEvaluateOnNewDocument", { source: INJECT });
  await send(ws, "Page.navigate", { url: "file://" + filePath });
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
      const alerts = Array.from(document.querySelectorAll('[role="alert"]')).map(a => ({
        text: a.textContent.trim().slice(0,200),
        scopeId: (a.closest('section')||{}).id || (a.closest('li')||{}).id || null
      }));
      // Check unrelated content (Line 3b value, Line 16 banner) still present/correct
      const line3bValue = (document.getElementById('line-3b-value')||{}).textContent
        || (document.querySelector('#line-3b .line-value')||{}).textContent || null;
      const line3bCitationCount = document.querySelectorAll('#line-3b-citations li, #line-3b button.citation').length;
      const bodyHTML = document.body.innerHTML;
      const leaksRawErrorMessage = /unknown fact id/i.test(bodyHTML) === false ? false : (bodyHTML.match(/unknown fact id/gi)||[]).length;
      return { alerts, line3bValue, line3bCitationCount, mentionsRawErrorText: leaksRawErrorMessage };
    })();
  `);
  await cdpClose(target.id);
  return result;
}
console.log("A:", JSON.stringify(await run("../prototypes/cycle5-a/walk.html"), null, 2));
console.log("B:", JSON.stringify(await run("../prototypes/cycle5-b/walk.html"), null, 2));
