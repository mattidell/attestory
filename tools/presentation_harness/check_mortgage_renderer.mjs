import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import vm from "node:vm";

const html = readFileSync(new URL("../../packages/presentation/pages/citation-walk.v1.html", import.meta.url), "utf8");
function functionText(name, nextMarker) {
  const start = html.indexOf(`function ${name}(`);
  const end = html.indexOf(nextMarker, start);
  assert(start >= 0 && end > start, `could not locate ${name}`);
  return html.slice(start, end);
}

const code = functionText("validateMortgageBorrowingExplanation", "\ndocument.addEventListener");
class SectionError extends Error {}
function el(tag, attributes, children) {
  return { tag, attributes: attributes || {}, children: [...(children || [])], appendChild(child) { this.children.push(child); } };
}
const context = { SectionError, el, Set, Number, String, Object, Array };
vm.runInNewContext(code, context);
const render = context.renderMortgageBorrowingExplanation;
const base = {
  schema: "mortgage-borrowing-explanation.v2", reports: [], groups: [], orphanRelationships: [],
  line8aDispositions: [{ artifact_id: "tax.us.2025.rule.f1098-line8a", disposition: "blocked" }],
  line8aFindings: [],
  calculationChain: { publications: [], dispositions: [], resolvedContent: [] },
};
const blocked = el("root", null, []);
render(blocked, base);
assert.match(JSON.stringify(blocked), /amount unavailable/);
assert.doesNotMatch(JSON.stringify(blocked), /group amount: 0/);

const actualZero = structuredClone(base);
actualZero.line8aDispositions[0] = {
  artifact_id: "tax.us.2025.rule.f1098-line8a", disposition: "published", finding_id: "demo.line8a.zero",
};
actualZero.line8aFindings = [{ id: "demo.line8a.zero", symbol: "tax.us.2025.schedule-a.line8a", value: 0, pins: [] }];
const published = el("root", null, []);
render(published, actualZero);
assert.match(JSON.stringify(published), /group amount: 0/);

const conflict = structuredClone(base);
conflict.reports = [{
  payer: "demo.lender", statement: "demo.statement", taxYear: "2025",
  statementLabel: { lender: "Demo lender", statement: "Demo statement", taxYear: "2025" },
  reportedInterest: { findingId: "demo.box1", value: 22000 }, boxObservations: [],
  reasonChain: null, localAnswers: [], relationships: [], effectiveAnswers: [],
  answerConflicts: [{
    question: "Is this the original loan?",
    local: { scope: "this exact Form 1098", findingId: "demo.local.original", factType: "demo.local", value: "no" },
    shared: { scope: "this named borrowing for 2025", findingId: "demo.shared.original", factType: "demo.shared", value: "yes" },
    correctionGuidance: "Review both answers. Correct the answer at the scope where it is wrong; the application does not choose which account is accurate.",
  }],
}];
const conflictRoot = el("root", null, []);
render(conflictRoot, conflict);
assert.match(JSON.stringify(conflictRoot), /demo\.local\.original/);
assert.match(JSON.stringify(conflictRoot), /demo\.shared\.original/);
assert.match(JSON.stringify(conflictRoot), /Correct the answer at the scope where it is wrong/);

const missingPeer = structuredClone(base);
missingPeer.schema = "mortgage-borrowing-explanation.v4";
missingPeer.reports = [{
  payer: "demo.lender", statement: "demo.statement", taxYear: "2025",
  statementLabel: { lender: "Demo lender", statement: "Demo statement", taxYear: "2025" },
  reportedInterest: { findingId: "demo.box1", value: 22000 }, boxObservations: [],
  reasonChain: null, localAnswers: [], relationships: [], effectiveAnswers: [],
  paymentComparisons: [{
    findingId: "demo.comparison", value: "different-payments", title: "All payments are separate",
    peer: null, peerIdentityStatus: "unavailable", applicability: "unresolved-applicability",
    supportFindingIds: [],
    explanation: "This recorded comparison cannot be used because the peer report identity is unavailable.",
  }],
}];
const missingPeerRoot = el("root", null, []);
render(missingPeerRoot, missingPeer);
assert.match(JSON.stringify(missingPeerRoot), /peer report identity unavailable/);
assert.doesNotMatch(JSON.stringify(missingPeerRoot), /undefined/);

const legacy = structuredClone(base);
legacy.schema = "mortgage-borrowing-explanation.v1";
legacy.reports = [{ payer: "demo.payer", statement: "demo.statement", taxYear: "2025",
  reportedInterest: { findingId: "demo.box1", value: 100 }, reasonChain: null,
  localAnswers: [], relationships: [], effectiveAnswers: [] }];
const legacyRoot = el("root", null, []);
render(legacyRoot, legacy);
assert.match(JSON.stringify(legacyRoot), /demo.statement/);

const malformed = structuredClone(base);
malformed.line8aDispositions = [{ artifact_id: "tax.us.2025.rule.f1098-line8a", disposition: "published" }];
assert.throws(() => render(el("root", null, []), malformed), SectionError);
console.log("mortgage renderer runtime checks passed: blocked, actual zero, v1 legacy, saved conflict, missing peer, malformed correspondence");
