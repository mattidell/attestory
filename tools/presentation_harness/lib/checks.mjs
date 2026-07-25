// Named check modules. Each check receives a `page` handle (see
// lib/executor.mjs) bound to the CDP session for the current fresh target,
// plus the criterion's declared `params`, and returns `{ pass, detail }`.
// `detail` is diagnostic only and is never copied into the deterministic
// report; the report records outcome + a closed reason code, nothing else.
//
// Every check names its driving technique in its own body (ADR-set boundary
// carried by the milestone plan's "Check boundary" section): contrast
// recomputes WCAG luminance from computed style, keyboard checks dispatch
// real CDP key events, and no check trusts a static source claim.

const CONTRAST_SCRIPT = `
(function(sel){
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
    return m[1].split(',').map(s=>parseFloat(s.trim())).slice(0,3);
  }
  function effectiveBg(el){
    let node = el;
    while(node){
      const cs = getComputedStyle(node);
      const m = cs.backgroundColor.match(/rgba?\\(([^)]+)\\)/);
      if(m){
        const parts = m[1].split(',').map(s=>parseFloat(s.trim()));
        if(parts.length < 4 || parts[3] > 0.01) return cs.backgroundColor;
      }
      node = node.parentElement;
    }
    return 'rgb(255,255,255)';
  }
  const el = document.querySelector(sel);
  if(!el) return { found: false };
  const cs = getComputedStyle(el);
  const fg = parseColor(cs.color);
  const bg = parseColor(effectiveBg(el));
  if(!fg || !bg) return { found: true, ratio: null };
  const L1 = luminance(fg), L2 = luminance(bg);
  const lighter = Math.max(L1,L2), darker = Math.min(L1,L2);
  const ratio = (lighter+0.05)/(darker+0.05);
  const fontSize = parseFloat(cs.fontSize);
  const fontWeight = parseInt(cs.fontWeight)||400;
  const isLarge = fontSize >= 24 || (fontSize >= 18.66 && fontWeight >= 700);
  const threshold = isLarge ? 3.0 : 4.5;
  return { found: true, ratio: +ratio.toFixed(2), threshold, pass: ratio >= threshold };
})(%SELECTOR%);
`;

const KEYBOARD_SCRIPT = `
(function(sel){
  const el = document.querySelector(sel);
  if(!el) return { found: false };
  return {
    found: true,
    isActive: document.activeElement === el,
    matchesFocusVisible: el.matches(':focus-visible'),
  };
})(%SELECTOR%);
`;

function jsStringLiteral(value) {
  return JSON.stringify(String(value));
}

async function domTextPresent(page, params) {
  const selector = params.selector;
  const expected = params.expected_text;
  const result = await page.evaluate(`
    (function(sel){
      const el = document.querySelector(sel);
      return el ? { found: true, text: el.textContent } : { found: false, text: null };
    })(${jsStringLiteral(selector)});
  `);
  if (!result.found) return { pass: false, detail: "element not found" };
  return { pass: result.text.includes(expected), detail: "textContent substring match" };
}

async function computedStyleContrast(page, params) {
  const selector = params.selector;
  const script = CONTRAST_SCRIPT.replace("%SELECTOR%", jsStringLiteral(selector));
  const result = await page.evaluate(script);
  if (!result.found) return { pass: false, detail: "element not found" };
  if (result.ratio === null) return { pass: false, detail: "unparseable color" };
  return { pass: result.pass, detail: `ratio ${result.ratio} vs threshold ${result.threshold}` };
}

async function roleAlertPresent(page, params) {
  const selector = params.selector;
  const result = await page.evaluate(`
    (function(sel){
      const el = document.querySelector(sel);
      return { found: !!el, role: el ? el.getAttribute('role') : null };
    })(${jsStringLiteral(selector)});
  `);
  if (!result.found) return { pass: false, detail: "element not found" };
  return { pass: result.role === "alert", detail: "role attribute check" };
}

async function keyboardFocusReachable(page, params) {
  const selector = params.selector;
  const tabPresses = Number.isInteger(params.tab_presses) ? params.tab_presses : 1;
  await page.evaluate("document.body.focus();");
  for (let i = 0; i < tabPresses; i += 1) {
    await page.tabKey();
  }
  const script = KEYBOARD_SCRIPT.replace("%SELECTOR%", jsStringLiteral(selector));
  const result = await page.evaluate(script);
  if (!result.found) return { pass: false, detail: "element not found" };
  return {
    pass: result.isActive && result.matchesFocusVisible,
    detail: "real CDP Input.dispatchKeyEvent Tab traversal",
  };
}

export const CHECKS = Object.freeze({
  "dom-text-present": domTextPresent,
  "computed-style-contrast": computedStyleContrast,
  "role-alert-present": roleAlertPresent,
  "keyboard-focus-reachable": keyboardFocusReachable,
});

export const KNOWN_CHECK_NAMES = Object.freeze(new Set(Object.keys(CHECKS)));
