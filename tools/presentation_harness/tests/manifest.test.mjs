import test from "node:test";
import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";
import { validateManifest } from "../lib/manifest.mjs";
import { ManifestError, MANIFEST_REASONS } from "../lib/reasons.mjs";

const here = dirname(fileURLToPath(import.meta.url));
const examplesDir = join(here, "..", "examples", "manifests");

async function loadJson(name) {
  const text = await readFile(join(examplesDir, name), "utf8");
  return JSON.parse(text);
}

function applyMutation(root, mutation) {
  const segments = mutation.path.split(".");
  const last = segments.pop();
  let node = root;
  for (const segment of segments) {
    node = Array.isArray(node) ? node[Number(segment)] : node[segment];
  }
  const key = Array.isArray(node) ? Number(last) : last;
  if (mutation.operation === "set") {
    node[key] = mutation.value;
  } else if (mutation.operation === "remove") {
    if (Array.isArray(node)) node.splice(key, 1);
    else delete node[key];
  } else if (mutation.operation === "push") {
    node[key].push(mutation.value);
  } else {
    throw new Error(`unknown mutation operation ${mutation.operation}`);
  }
}

test("the committed smoke manifest validates and normalizes", async () => {
  const raw = await loadJson("smoke.v1.json");
  const manifest = validateManifest(raw);
  assert.equal(manifest.cases.length, 6);
  assert.equal(manifest.matrixEntries.length, 3);
});

test("every committed invalid manifest mutation fails with its declared reason code", async () => {
  const base = await loadJson("smoke.v1.json");
  const cases = await loadJson("invalid-cases.v1.json");
  for (const testCase of cases) {
    const candidate = JSON.parse(JSON.stringify(base));
    for (const mutation of testCase.mutations) {
      applyMutation(candidate, mutation);
    }
    assert.ok(
      MANIFEST_REASONS.has(testCase.expected_reason),
      `${testCase.id}: ${testCase.expected_reason} must be a closed manifest reason code`,
    );
    assert.throws(
      () => validateManifest(candidate),
      (error) => {
        assert.ok(error instanceof ManifestError, `${testCase.id}: expected a ManifestError`);
        assert.equal(error.reasonCode, testCase.expected_reason, testCase.id);
        return true;
      },
      testCase.id,
    );
  }
});

test("manifest validation never throws a reason code outside the closed vocabulary", async () => {
  const base = await loadJson("smoke.v1.json");
  const malformed = JSON.parse(JSON.stringify(base));
  malformed.candidates = "not-an-array";
  try {
    validateManifest(malformed);
    assert.fail("expected validateManifest to throw");
  } catch (error) {
    assert.ok(error instanceof ManifestError);
    assert.ok(MANIFEST_REASONS.has(error.reasonCode));
  }
});

test("every named check requires its exact parameter shape", async () => {
  const base = await loadJson("smoke.v1.json");
  const mutations = [
    ["missing required text", (manifest) => { delete manifest.criteria[0].params.expected_text; }],
    ["unknown parameter", (manifest) => { manifest.criteria[0].params.extra = "demo"; }],
    ["wrong selector type", (manifest) => { manifest.criteria[0].params.selector = 7; }],
    ["negative tab count", (manifest) => { manifest.criteria[3].params.tab_presses = -1; }],
    ["too many tab presses", (manifest) => { manifest.criteria[3].params.tab_presses = 101; }],
  ];
  for (const [label, mutate] of mutations) {
    const candidate = JSON.parse(JSON.stringify(base));
    mutate(candidate);
    assert.throws(() => validateManifest(candidate), ManifestError, label);
  }
});

test("empty trustworthy selections and syntactically invalid injections are rejected", async () => {
  const base = await loadJson("smoke.v1.json");
  for (const [path, expectedReason] of [
    ["candidates", "manifest-empty-selection"],
    ["fixtures", "manifest-empty-selection"],
    ["criteria", "manifest-empty-selection"],
    ["tamper_cases", "manifest-empty-selection"],
    ["matrix", "manifest-empty-matrix"],
  ]) {
    const candidate = JSON.parse(JSON.stringify(base));
    candidate[path] = [];
    assert.throws(
      () => validateManifest(candidate),
      (error) => error instanceof ManifestError && error.reasonCode === expectedReason,
      path,
    );
  }
  const invalidInjection = JSON.parse(JSON.stringify(base));
  invalidInjection.tamper_cases[0].injection = "function {";
  assert.throws(
    () => validateManifest(invalidInjection),
    (error) => error instanceof ManifestError && error.reasonCode === "manifest-invalid-injection",
  );
});
