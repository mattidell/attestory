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
