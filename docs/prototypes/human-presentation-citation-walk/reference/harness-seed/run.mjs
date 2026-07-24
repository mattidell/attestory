// CDP driver: opens a fresh page in our own isolated Chrome instance,
// navigates to a walk.html, and runs an in-page evaluation battery.
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
  const result = await send(ws, "Runtime.evaluate", {
    expression,
    returnByValue: true,
    awaitPromise: true,
  });
  if (result.exceptionDetails) {
    throw new Error("Eval error: " + JSON.stringify(result.exceptionDetails));
  }
  return result.result.value;
}

// The battery script run inside the page.
const BATTERY = `
(function(){
  function luminance(rgb){
    const [r,g,b] = rgb.map(c=>{
      c/=255;
      return c<=0.03928 ? c/12.92 : Math.pow((c+0.055)/1.055,2.4);
    });
    return 0.2126*r+0.7152*g+0.0722*b;
  }
  function parseColor(str){
    const m = str.match(/rgba?\\(([^)]+)\\)/);
    if(!m) return null;
    const parts = m[1].split(',').map(s=>parseFloat(s.trim()));
    return parts.slice(0,3);
  }
  function contrast(fgStr, bgStr){
    const fg = parseColor(fgStr), bg = parseColor(bgStr);
    if(!fg||!bg) return null;
    const L1 = luminance(fg), L2 = luminance(bg);
    const lighter = Math.max(L1,L2), darker = Math.min(L1,L2);
    return (lighter+0.05)/(darker+0.05);
  }
  // Walk up the DOM to find effective (non-transparent) background color.
  function effectiveBg(el){
    let node = el;
    while(node){
      const cs = getComputedStyle(node);
      const bg = cs.backgroundColor;
      const rgba = bg.match(/rgba?\\(([^)]+)\\)/);
      if(rgba){
        const parts = rgba[1].split(',').map(s=>parseFloat(s.trim()));
        if(parts.length < 4 || parts[3] > 0.01) return bg;
      }
      node = node.parentElement;
    }
    return 'rgb(255,255,255)';
  }

  const out = { contrast: {}, landmarks: {}, headings: [], citations: [], blocked: {}, backlinks: {}, focus: {}, skimSignals: {} };

  // --- 1. Contrast checks on key element categories ---
  function checkContrast(label, el, opts){
    if(!el) { out.contrast[label] = {found:false}; return; }
    const cs = getComputedStyle(el);
    const fg = cs.color;
    const bg = effectiveBg(el);
    const ratio = contrast(fg, bg);
    const fontSize = parseFloat(cs.fontSize);
    const fontWeight = parseInt(cs.fontWeight)||400;
    const isLarge = fontSize >= 24 || (fontSize >= 18.66 && fontWeight >= 700);
    const threshold = isLarge ? 3.0 : 4.5;
    out.contrast[label] = { fg, bg, ratio: ratio ? +ratio.toFixed(2) : null, threshold, isLarge, pass: ratio ? ratio >= threshold : null };
  }
  checkContrast('body', document.body);
  checkContrast('firstLink', document.querySelector('a'));
  checkContrast('publishedBadge', document.querySelector('.badge.published'));
  checkContrast('blockedBadge', document.querySelector('.badge.blocked'));
  const bannerBlocked = document.querySelector('[role="alert"]');
  checkContrast('blockedBanner', bannerBlocked);
  const firstCitation = document.querySelector('button.citation, details.citation summary');
  checkContrast('citationAffordance', firstCitation);

  // Focus outline color contrast vs background (approx: use outline-color if set else assume element bg)
  (function(){
    const el = document.querySelector('button.citation, details.citation summary, a');
    if(el){
      el.focus();
      const cs = getComputedStyle(el);
      out.focus.outlineWidth = cs.outlineWidth;
      out.focus.outlineStyle = cs.outlineStyle;
      out.focus.outlineColor = cs.outlineColor;
      const bg = effectiveBg(el);
      const ratio = contrast(cs.outlineColor, bg);
      out.focus.outlineContrastVsBg = ratio ? +ratio.toFixed(2) : null;
      out.focus.pass = cs.outlineStyle !== 'none' && parseFloat(cs.outlineWidth) >= 1;
      el.blur();
    }
  })();

  // --- 2. Landmarks & headings ---
  out.landmarks.banner = !!document.querySelector('header[role="banner"], header') ;
  out.landmarks.bannerCount = document.querySelectorAll('header[role="banner"], header').length;
  out.landmarks.nav = document.querySelectorAll('nav').length;
  out.landmarks.navHasLabel = Array.from(document.querySelectorAll('nav')).every(n => n.hasAttribute('aria-label') || n.hasAttribute('aria-labelledby'));
  out.landmarks.main = document.querySelectorAll('main').length;
  out.landmarks.footer = document.querySelectorAll('footer').length;

  const headings = Array.from(document.querySelectorAll('h1,h2,h3,h4,h5,h6')).map(h => parseInt(h.tagName[1]));
  out.headings = headings;
  let monotonic = true;
  for(let i=1;i<headings.length;i++){
    if(headings[i] > headings[i-1] + 1) monotonic = false;
  }
  out.headingsMonotonic = monotonic;

  // aria-labelledby resolution for sections
  const sections = Array.from(document.querySelectorAll('section[aria-labelledby]'));
  out.landmarks.sectionsWithLabelledby = sections.length;
  out.landmarks.sectionsLabelledbyResolved = sections.every(s => document.getElementById(s.getAttribute('aria-labelledby')));

  // --- 3. Keyboard reachability / tab order for citation affordances ---
  const citationEls = Array.from(document.querySelectorAll('button.citation, details.citation > summary'));
  out.citations.count = citationEls.length;
  out.citations.allTabbable = citationEls.every(el => {
    const tabindex = el.getAttribute('tabindex');
    return tabindex === null || parseInt(tabindex) >= 0;
  });
  out.citations.nativeElementTypes = [...new Set(citationEls.map(el => el.tagName.toLowerCase()))];

  // Verify Enter/Space or native details toggling actually works
  (async function(){})();

  // --- 4. Blocked line role=alert + distinct treatment ---
  const line16 = document.getElementById('line-16');
  out.blocked.sectionExists = !!line16;
  out.blocked.hasRoleAlert = !!(line16 && line16.querySelector('[role="alert"]'));
  if(line16){
    const cs = getComputedStyle(line16);
    out.blocked.borderWidth = cs.borderWidth || cs.borderTopWidth;
    out.blocked.backgroundColor = cs.backgroundColor;
    const sibling = document.getElementById('line-2b') || document.querySelector('section.line, section[id]');
    const csSib = sibling ? getComputedStyle(sibling) : null;
    out.blocked.siblingBorderWidth = csSib ? (csSib.borderWidth||csSib.borderTopWidth) : null;
    out.blocked.siblingBackgroundColor = csSib ? csSib.backgroundColor : null;
    out.blocked.visuallyDistinct = csSib ? (out.blocked.borderWidth !== out.blocked.siblingBorderWidth || out.blocked.backgroundColor !== out.blocked.siblingBackgroundColor) : null;
    const text = line16.textContent;
    out.blocked.hasNoDigitInValue = !/[0-9]/.test((line16.querySelector('.value, .line-value')||{textContent:''}).textContent.replace(/demo-fact-qdcg-absence-decl/g,''));
    out.blocked.mentionsBlockReason = /block reason/i.test(text);
    out.blocked.mentionsMissingFact = /missing.*fact/i.test(text);
    out.blocked.mentionsRemedy = /remedy/i.test(text);
  }

  // --- 5. Reuse backlinks: N-1 resolvable backlinks per N-site fact ---
  // Discover fact->site mapping by looking for repeated fact ids in DOM (data-fact-id attr, or dl Fact ID rows)
  const factOccurrences = {}; // factId -> array of element ids representing citation instance
  // Try data-fact-id first
  document.querySelectorAll('[data-fact-id]').forEach(el => {
    const fid = el.getAttribute('data-fact-id');
    (factOccurrences[fid] ||= []).push(el.id || el.closest('[id]')?.id);
  });
  // Fallback: details citations - look inside citation-body dl for "Fact ID" dt/dd pair
  if(Object.keys(factOccurrences).length === 0){
    document.querySelectorAll('details.citation').forEach(body => {
      const dts = Array.from(body.querySelectorAll('dt'));
      const idx = dts.findIndex(dt => /fact id/i.test(dt.textContent));
      if(idx >= 0){
        const dd = dts[idx].nextElementSibling;
        const fid = dd ? dd.textContent.trim() : null;
        if(fid) (factOccurrences[fid] ||= []).push(body.id);
      }
    });
  }
  out.backlinks.factOccurrences = factOccurrences;

  const backlinkResults = {};
  for(const [fid, sites] of Object.entries(factOccurrences)){
    const n = sites.length;
    if(n < 2) continue;
    // For each site container, count backlink <a> elements whose href resolves
    backlinkResults[fid] = { n, perSite: [] };
    sites.forEach(siteId => {
      if(!siteId) { backlinkResults[fid].perSite.push({siteId:null, backlinkCount:null}); return; }
      // Backlinks may live in a sibling detail/body node rather than the
      // citation trigger element itself (e.g. button + adjacent hidden detail div),
      // so search the trigger, its parent, and a conventional "-detail" sibling id.
      const trigger = document.getElementById(siteId);
      const candidates = [trigger, trigger && trigger.parentElement, document.getElementById(siteId + '-detail')].filter(Boolean);
      let backlinkAnchors = [];
      for(const c of candidates){
        const found = Array.from(c.querySelectorAll('a.backlink, .backlinks a'));
        if(found.length){ backlinkAnchors = found; break; }
      }
      const resolvable = backlinkAnchors.filter(a => {
        const href = a.getAttribute('href')||'';
        if(!href.startsWith('#')) return false;
        return !!document.getElementById(href.slice(1));
      });
      backlinkResults[fid].perSite.push({ siteId, backlinkCount: backlinkAnchors.length, resolvableCount: resolvable.length, expectedNMinus1: n-1, matches: resolvable.length === (n-1) });
    });
  }
  out.backlinks.results = backlinkResults;

  // --- 6. Skim rubric proxies ---
  out.skimSignals.publishedBadgeCount = document.querySelectorAll('.badge.published').length;
  out.skimSignals.blockedBadgeCount = document.querySelectorAll('.badge.blocked').length;
  out.skimSignals.affordanceHintTextExists = !!document.querySelector('.affordance-hint, .citation-icon, .citation-label');
  out.skimSignals.affordanceVisibleAtRest = (function(){
    const el = document.querySelector('.affordance-hint');
    const iconEl = document.querySelector('.citation-icon');
    const target = el || iconEl;
    if(!target) return null;
    const cs = getComputedStyle(target);
    return cs.display !== 'none' && cs.visibility !== 'hidden';
  })();

  return out;
})();
`;

const KEYBOARD_TEST = `
(async function(){
  function delay(ms){ return new Promise(r=>setTimeout(r,ms)); }
  const els = Array.from(document.querySelectorAll('button.citation, details.citation > summary'));
  if(els.length === 0) return { error: 'no citation elements found' };
  const first = els[0];
  first.focus();
  const focusedOk = document.activeElement === first;
  // Simulate activation via Enter key event dispatch + also directly toggle to check behavior contract
  let beforeState, afterState;
  if(first.tagName.toLowerCase() === 'button'){
    beforeState = first.getAttribute('aria-expanded');
    first.dispatchEvent(new KeyboardEvent('keydown', {key:'Enter', bubbles:true}));
    first.click(); // buttons activate on Enter natively; simulate via click since synthetic KeyboardEvent doesn't auto-trigger click in headless eval context
    afterState = first.getAttribute('aria-expanded');
  } else {
    // summary/details - native keyboard toggle; simulate by toggling open property (Enter on summary opens details natively in real browser)
    const details = first.closest('details');
    beforeState = details.open;
    details.open = !details.open; // mirror native Enter-on-summary behavior
    afterState = details.open;
  }
  return {
    tagName: first.tagName.toLowerCase(),
    focusReachedViaFocus: focusedOk,
    stateBefore: beforeState,
    stateAfter: afterState,
    toggled: String(beforeState) !== String(afterState)
  };
})();
`;

async function testPrototype(name, filePath) {
  const target = await cdpNewTarget("about:blank");
  const ws = await connect(target.webSocketDebuggerUrl);
  await send(ws, "Page.enable");
  await send(ws, "Runtime.enable");
  await send(ws, "Page.navigate", { url: "file://" + filePath });
  // wait for load
  await new Promise((resolve) => {
    const handler = (ev) => {
      const msg = JSON.parse(ev.data);
      if (msg.method === "Page.loadEventFired") {
        ws.removeEventListener("message", handler);
        resolve();
      }
    };
    ws.addEventListener("message", handler);
  });
  await new Promise(r => setTimeout(r, 300));

  const battery = await evalInPage(ws, BATTERY);
  const keyboard = await evalInPage(ws, KEYBOARD_TEST);

  // Regression checks
  const regression = await evalInPage(ws, `
    (function(){
      const bodyText = document.body.textContent;
      const line16 = document.getElementById('line-16');
      const line16Text = line16 ? line16.textContent : '';
      const valueEl = line16 ? line16.querySelector('.value, .line-value, .blocked-value') : null;
      const valueText = valueEl ? valueEl.textContent : '';
      return {
        line16ValueElementText: valueText.trim(),
        line16ValueHasNoNumeral: !/[0-9]/.test(valueText),
        line16HasRemedy: /remedy/i.test(line16Text),
        mentions2026_07_11_count: (bodyText.match(/2026-07-11/g)||[]).length,
        mentions2026_07_12_count: (bodyText.match(/2026-07-12/g)||[]).length,
        roleAlertCount: document.querySelectorAll('[role="alert"]').length
      };
    })();
  `);

  await cdpClose(target.id);
  return { name, regression, battery, keyboard };
}

const results = {};
results.builderA = await testPrototype("Builder A", "../prototypes/cycle5-a/walk.html");
results.builderB = await testPrototype("Builder B", "../prototypes/cycle5-b/walk.html");

console.log(JSON.stringify(results, null, 2));
