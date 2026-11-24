import { readFileSync } from "node:fs";
import vm from "node:vm";

class FakeClassList {
  constructor(el) {
    this._el = el;
  }
  _tokens() {
    const raw = this._el.attributes.class || "";
    return raw ? raw.split(/\s+/).filter(Boolean) : [];
  }
  add(...names) {
    const set = new Set(this._tokens());
    for (const n of names) set.add(n);
    this._el.attributes.class = [...set].join(" ");
  }
  contains(name) {
    return this._tokens().includes(name);
  }
}

class FakeElement {
  constructor(tag) {
    this.tagName = tag.toUpperCase();
    this.attributes = {};
    this.children = [];
    this.listeners = {};
    this.classList = new FakeClassList(this);
    this.dataset = {};
  }
  get className() {
    return this.attributes.class || "";
  }
  set className(v) {
    this.attributes.class = String(v);
  }
  get id() {
    return this.attributes.id || "";
  }
  set id(v) {
    this.attributes.id = String(v);
  }
  get hidden() {
    return Object.prototype.hasOwnProperty.call(this.attributes, "hidden");
  }
  set hidden(v) {
    if (v) this.attributes.hidden = "";
    else delete this.attributes.hidden;
  }
  get open() {
    return Object.prototype.hasOwnProperty.call(this.attributes, "open");
  }
  set open(v) {
    if (v) this.attributes.open = "";
    else delete this.attributes.open;
  }
  get firstChild() {
    return this.children.length ? this.children[0] : null;
  }
  setAttribute(k, v) {
    this.attributes[k] = String(v);
    if (k.startsWith("data-")) {
      const camel = k.slice(5).replace(/-([a-z])/g, (_, c) => c.toUpperCase());
      this.dataset[camel] = String(v);
    }
  }
  getAttribute(k) {
    return Object.prototype.hasOwnProperty.call(this.attributes, k) ? this.attributes[k] : null;
  }
  appendChild(child) {
    this.children.push(child);
    return child;
  }
  removeChild(child) {
    const idx = this.children.indexOf(child);
    if (idx >= 0) this.children.splice(idx, 1);
    return child;
  }
  addEventListener(type, fn) {
    (this.listeners[type] ||= []).push(fn);
  }
  dispatchEvent(evt) {
    for (const fn of this.listeners[evt.type] || []) fn(evt);
  }
  click() {
    this.dispatchEvent({ type: "click", target: this });
  }
  focus() {}
  scrollIntoView() {}
}

class FakeText {
  constructor(text) {
    this.textContent = String(text);
  }
}

function walkElements(root, fn) {
  fn(root);
  for (const child of root.children || []) {
    if (child instanceof FakeElement) walkElements(child, fn);
  }
}

const BADGE_ENUM_TEXT = new Set([
  "published_value",
  "computed_zero",
  "closure_backed_zero",
  "published_categorical",
  "guard_inapplicable",
  "blocked",
  "published",
  "inapplicable",
  "published value",
  "computed zero",
  "closure backed zero",
  "published categorical",
  "guard inapplicable",
]);

function accessibleName(node) {
  if (!(node instanceof FakeElement)) return [];
  const label = node.attributes["aria-label"];
  return label ? [label] : [];
}

function collectVisibleText(node, opts = {}) {
  const { expandTrace = false } = opts;
  if (node instanceof FakeText) return [node.textContent];
  if (!(node instanceof FakeElement)) return [];
  if (node.hidden) return [];
  if (node.tagName === "DETAILS") {
    const isCollapsedAudit =
      node.classList.contains("technical-details") ||
      node.classList.contains("audit-ids");
    const isTrace = node.classList.contains("shared-explanation");
    const own = accessibleName(node);
    if (isCollapsedAudit && !node.open) {
      // Only summary is visible when collapsed. Its accessible name is judged.
      const sum = node.children.find((c) => c instanceof FakeElement && c.tagName === "SUMMARY");
      return [...own, ...(sum ? collectVisibleText(sum, opts) : [])];
    }
    if (!node.open && !(expandTrace && isTrace)) {
      const sum = node.children.find((c) => c instanceof FakeElement && c.tagName === "SUMMARY");
      return [...own, ...(sum ? collectVisibleText(sum, opts) : [])];
    }
  }
  const out = [...accessibleName(node)];
  for (const child of node.children) {
    out.push(...collectVisibleText(child, opts));
  }
  return out;
}

function extractShellText(html) {
  const parts = [];
  const titleMatch = html.match(/<title>([\s\S]*?)<\/title>/i);
  if (titleMatch) parts.push(titleMatch[1].replace(/\s+/g, " ").trim());
  const headerMatch = html.match(/<header[^>]*>([\s\S]*?)<\/header>/i);
  if (headerMatch) {
    parts.push(headerMatch[1].replace(/<[^>]+>/g, " ").replace(/\s+/g, " ").trim());
  }
  return parts;
}

function extractScript(html) {
  const m = html.match(/<script>([\s\S]*?)<\/script>/);
  if (!m) throw new Error("No <script> block found in page HTML");
  return m[1];
}

const LEAK_RULES = [
  { name: "raw_enum_underscore", re: /\b(?:published_value|computed_zero|closure_backed_zero|published_categorical|guard_inapplicable)\b/ },
  { name: "raw_enum_spaced", re: /\b(?:published value|computed zero|closure backed zero|published categorical|guard inapplicable)\b/i },
  { name: "raw_blocked_code", re: /\b(?:DEPENDENCY_ABSENT|DEPENDENCY_INVALID|SOURCE_SET_UNCLOSED|ITEMIZATION_TIE_OUT_VIOLATION|COMPLETENESS_VALUE_VIOLATION|CATEGORICAL_DOMAIN_MISMATCH|F1098_SCOPE_CONTRADICTION|SLI_MFS_INELIGIBLE|SLI_SCHEDULE1_PART_II_OUT_OF_SCOPE|SLI_UNIVERSAL_COMPONENT_VIOLATION|ACCRUED_EXCEEDS_ASSOCIATED_REPORT|AGGREGATE_ACCRUED_EXCEEDS_REPORT|NOMINEE_ALLOCATIONS_EXCEED_REPORT|SUPPORTABILITY_NOT_ESTABLISHED|EXCLUSIVE_PRESENCE_CONFLICT)\b/ },
  { name: "raw_tax_id", re: /\btax\.us\.\d{4}\.[A-Za-z0-9._-]+/ },
  { name: "raw_demo_id", re: /\bdemo\.[A-Za-z0-9._-]+/ },
  { name: "raw_pin_version", re: /[A-Za-z0-9._-]+@v\d+\b/ },
  {
    name: "old_engine_phrase",
    re: /(?:No value published — cannot compute|Missing dependency code\(s\)|Missing or violated condition code\(s\)|Trace recorded support|Show recorded predecessor|Show dependency |Pin id|Pin version|Combined class:|Currency:|for this scope|This scope needs|consumed by published|consumed by the published|application default|Current declared defaults|What the application derived|not published\.|Form 1040 — Citation Walk)/,
  },
];

function collectContentSupplied(modelObj) {
  const supplied = new Set();
  const add = (v) => {
    if (typeof v === "string" && v.trim()) supplied.add(v.replace(/\s+/g, " ").trim());
  };
  for (const s of modelObj.sections || []) {
    const f = s && s.field;
    if (f) {
      add(f.label);
      for (const inst of Object.values(f.dispositions || {})) {
        if (inst && typeof inst === "object") add(inst.explain);
      }
    }
    const r = s && s.resolved;
    if (r) {
      for (const reason of r.reasons || []) {
        if (reason && typeof reason === "object") add(reason.sentence);
      }
    }
  }
  for (const g of modelObj.questionGroups || []) {
    if (g && typeof g === "object") add(g.question);
  }
  return supplied;
}

function findLeaks(texts, badgeTexts, contentSupplied) {
  const leaks = [];
  const contentMatches = [];
  for (const raw of texts) {
    const t = raw.replace(/\s+/g, " ").trim();
    if (!t) continue;
    const isContent = contentSupplied && contentSupplied.has(t);
    for (const rule of LEAK_RULES) {
      const m = t.match(rule.re);
      if (m) {
        const rec = { kind: rule.name, match: m[0], snippet: t.slice(0, 140) };
        if (isContent) contentMatches.push(rec);
        else leaks.push(rec);
      }
    }
  }
  for (const b of badgeTexts) {
    const t = b.replace(/\s+/g, " ").trim().toLowerCase();
    if (BADGE_ENUM_TEXT.has(t)) {
      leaks.push({ kind: "raw_badge_enum", match: t, snippet: b.slice(0, 80) });
    }
  }
  return { leaks, contentMatches };
}

function renderAndCheck(pageHtml, modelObj) {
  const scriptSrc = extractScript(pageHtml).replace(
    "const MODEL = Object.freeze(__MODEL_JSON__);",
    "const MODEL = Object.freeze(__INJECTED_MODEL__);",
  );
  const rootIds = [
    "question-groups-root",
    "sections-root",
    "mortgage-explanation-root",
    "attachment-status-root",
    "citation-groups-root",
    "diagnostics-root",
  ];
  const mainEl = new FakeElement("main");
  const byId = new Map();
  for (const id of rootIds) {
    const div = new FakeElement("div");
    div.id = id;
    mainEl.appendChild(div);
    byId.set(id, div);
  }
  const registerIds = (node) => {
    if (node instanceof FakeElement) {
      if (node.id) byId.set(node.id, node);
      for (const c of node.children) registerIds(c);
    }
  };
  const origAppend = FakeElement.prototype.appendChild;
  const document = {
    createElement(tag) {
      return new FakeElement(tag);
    },
    createTextNode(text) {
      return new FakeText(text);
    },
    getElementById(id) {
      registerIds(mainEl);
      return byId.get(id) || null;
    },
    addEventListener() {},
  };
  const context = {
    __INJECTED_MODEL__: modelObj,
    document,
    Set,
    Map,
    Number,
    String,
    Object,
    Array,
    JSON,
    Error,
    RegExp,
    Boolean,
  };
  vm.runInNewContext(scriptSrc, context);
  void origAppend;

  // Count section errors and collect badges
  let sectionErrors = 0;
  const badgeTexts = [];
  walkElements(mainEl, (el) => {
    if (el.classList.contains("section-error")) sectionErrors += 1;
    if (el.classList.contains("badge")) badgeTexts.push(collectVisibleText(el).join(" "));
  });

  const contentSupplied = collectContentSupplied(modelObj);

  // 1. Initial first-read visible text (collapsed <details> only show summary)
  //    plus aria-label on those same visible nodes.
  const initialTexts = [...extractShellText(pageHtml), ...collectVisibleText(mainEl, { expandTrace: false })];
  const initialFound = findLeaks(initialTexts, badgeTexts, contentSupplied);
  const initialLeaks = initialFound.leaks;
  const contentMatches = [...initialFound.contentMatches];

  // 2. Open support traces and click first-level trace buttons to check first-read trace text
  //    (still keeping collapsed .audit-ids and .technical-details closed!)
  const traces = [];
  walkElements(mainEl, (el) => {
    if (el.tagName === "DETAILS" && el.classList.contains("shared-explanation")) {
      traces.push(el);
    }
  });
  for (const tr of traces) {
    tr.open = true;
    tr.dispatchEvent({ type: "toggle", target: tr });
    // Expand up to 25 buttons per trace to cover node/edge/disposition/reuse captions
    let clicks = 0;
    const clicked = new Set();
    while (clicks < 25) {
      let nextBtn = null;
      walkElements(tr, (el) => {
        if (nextBtn) return;
        if (el.tagName === "BUTTON" && !clicked.has(el) && !el.attributes["data-explanation-reuse"]) {
          nextBtn = el;
        }
      });
      if (!nextBtn) break;
      clicked.add(nextBtn);
      nextBtn.click();
      clicks += 1;
    }
  }
  const traceTexts = [];
  for (const tr of traces) {
    traceTexts.push(...collectVisibleText(tr, { expandTrace: true }));
  }
  const traceFound = findLeaks(traceTexts, [], contentSupplied);
  const traceLeaks = traceFound.leaks;
  contentMatches.push(...traceFound.contentMatches);

  // 3. Also check expanded non-audit <details> in line21 / mortgage panels
  //    (still keeping .technical-details and .audit-ids collapsed, and calculationChain audit panel collapsed)
  const panelTexts = [];
  walkElements(mainEl, (el) => {
    if (el.tagName === "DETAILS" && !el.classList.contains("technical-details") && !el.classList.contains("audit-ids") && !el.classList.contains("shared-explanation") && !el.classList.contains("line21-citations")) {
      const sum = el.children.find((c) => c instanceof FakeElement && c.tagName === "SUMMARY");
      const sumText = sum ? collectVisibleText(sum).join(" ").trim() : "";
      if (sumText.includes("(for audit)") || sumText.startsWith("Saved calculation evidence")) {
        return;
      }
      el.open = true;
      panelTexts.push(...collectVisibleText(el, { expandTrace: false }));
    }
  });
  const panelFound = findLeaks(panelTexts, [], contentSupplied);
  const panelLeaks = panelFound.leaks;
  contentMatches.push(...panelFound.contentMatches);

  const reasonCodes = [];
  walkElements(mainEl, (el) => {
    if (el.attributes["data-reason-code"]) reasonCodes.push(el.attributes["data-reason-code"]);
  });
  const result = {
    section_errors: sectionErrors,
    initial_leak_count: initialLeaks.length,
    trace_leak_count: traceLeaks.length,
    panel_leak_count: panelLeaks.length,
    total_first_read_leaks: initialLeaks.length + traceLeaks.length + panelLeaks.length,
    content_supplied_matches: contentMatches.length,
    sample_leaks: [...initialLeaks, ...traceLeaks, ...panelLeaks].slice(0, 10),
    sample_content_matches: contentMatches.slice(0, 5),
    badge_texts: badgeTexts,
    reason_codes: reasonCodes,
  };
  if (process.env.PPW_CHECK_DETAIL === "1") {
    const firstRead = [...initialTexts, ...traceTexts, ...panelTexts].join("\n");
    result.first_read_text = firstRead.length > 20000 ? firstRead.slice(0, 20000) : firstRead;
  }
  return result;
}

// CLI mode: node check_page_dom.mjs <page-html-path> < ndjson-of-{key,model}
const pagePath = process.argv[2];
if (!pagePath) {
  console.error("Usage: node check_page_dom.mjs <page-html-path>");
  process.exit(2);
}
const pageHtml = readFileSync(pagePath, "utf8");
const chunks = [];
for await (const chunk of process.stdin) chunks.push(chunk);
const input = Buffer.concat(chunks).toString("utf8").trim();
const out = {};
for (const line of input ? input.split("\n") : []) {
  const { key, model } = JSON.parse(line);
  out[key] = renderAndCheck(pageHtml, model);
}
process.stdout.write(JSON.stringify(out) + "\n");
