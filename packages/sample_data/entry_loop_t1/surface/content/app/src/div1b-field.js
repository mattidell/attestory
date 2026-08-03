import { DIV1B_FORMAT } from "./div1b-format.js";

// entry-field.v1, instantiated for 1099-DIV box 1b -- the second fact
// family, mirroring w2-box1-field.js's shape exactly. See that file's
// header comment for why `format` is the imported binding rather than a
// duplicated literal.
export const DIV1B_FIELD = {
  "schema": "entry-field.v1",
  "id": "tax.us.2025.f1099div.box1b-qualified",
  "version": "v1",
  "source": {
    "document": "Form 1099-DIV",
    "box": "Box 1b",
    "label": "Qualified dividends"
  },
  "destination": {
    "form": "Form 1040",
    "line": "3a"
  },
  "purpose": "resolves the missing qualified dividends needed to compute the record",
  "format": DIV1B_FORMAT,
  "correction": {
    "kind": "same-field-reuse",
    "affordance": "Find the answered fact in the entry panel and choose \"Correct this fact\" to reopen this same field without restarting the session."
  }
};

export function formatSourceLabel(field = DIV1B_FIELD) {
  return `${field.source.document} · ${field.source.box}`;
}

export function formatDestinationPurpose(field = DIV1B_FIELD) {
  return `This amount feeds ${field.destination.form} line ${field.destination.line} and ${field.purpose}.`;
}
