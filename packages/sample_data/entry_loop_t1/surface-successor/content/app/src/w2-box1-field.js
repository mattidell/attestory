import { W2_BOX1_FORMAT } from "./w2-box1-format.js";

// The entry-field.v1 shape (packages/schemas/entry/entry-field.v1.schema.json),
// instantiated for this field. Keys and string values are quoted so this
// object is valid JSON everywhere except the `format` property, which is the
// imported binding rather than a duplicated literal; the Python-side loader
// substitutes the already-parsed w2-box1-format.js spec there before
// decoding the rest as JSON (see entry_loop.py's seam recommendation).
export const W2_BOX1_FIELD = {
  "schema": "entry-field.v1",
  "id": "tax.us.2025.w2.box1-wages",
  "version": "v1",
  "source": {
    "document": "Form W-2",
    "box": "Box 1",
    "label": "Wages, tips, other compensation"
  },
  "destination": {
    "form": "Form 1040",
    "line": "1a"
  },
  "purpose": "resolves the missing wages needed to compute income",
  "format": W2_BOX1_FORMAT,
  "correction": {
    "kind": "same-field-reuse",
    "affordance": "Find the answered fact in the entry panel and choose \"Correct this fact\" to reopen this same field without restarting the session."
  }
};

export function formatSourceLabel(field = W2_BOX1_FIELD) {
  return `${field.source.document} · ${field.source.box}`;
}

export function formatDestinationPurpose(field = W2_BOX1_FIELD) {
  return `This amount feeds ${field.destination.form} line ${field.destination.line} and ${field.purpose}.`;
}
