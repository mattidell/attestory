"""Survey: form fields of a core package whose disposition text names another line or credit.

Usage: python3 survey.py [package-path]   (default: core v63)

A form field is flagged when any disposition ``explain`` (or the description) carries a
text that names another form field's label (a copied explanation) or a "line N" other than
its own line or a line its description names, or a text shared word for word by two fields
with different lines (outside ``GENERIC_PHRASES``). A text that names its own line is accepted.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

CORPUS = Path(__file__).resolve().parents[5] / "packages" / "content" / "tax" / "2025"
LINE_REF = re.compile(r"line\s+(\d+[a-z]?)", re.IGNORECASE)


def form_fields(package: dict) -> dict[tuple[str, str], dict]:
    index: dict[tuple[str, str], dict] = {}
    for path in CORPUS.glob("*form-field*.json"):
        body = json.loads(path.read_text())
        index[(body["id"], body["version"])] = body
    return {
        (m["id"], m["version"]): index[(m["id"], m["version"])]
        for m in package["members"]
        if m["role"] == "form-field"
    }


def own_lines(field: dict) -> set[str]:
    line = field["line"].split("-")[-1].lower()
    return {line} | {r.lower() for r in LINE_REF.findall(field["description"])}


def problems(field: dict, labels: dict[str, str]) -> list[str]:
    """Texts that name another field's label (a copied explanation) or another line."""
    found: list[str] = []
    own_text = (field["label"] + " " + field["description"]).lower()
    own = own_lines(field)
    for code, disposition in sorted(field["dispositions"].items()):
        text = disposition["explain"]
        lowered = text.lower()
        if field["line"].split("-")[-1].lower() in {r.lower() for r in LINE_REF.findall(text)}:
            continue  # the text names its own line, so a mention of an input is not a copy
        for label, owner in labels.items():
            if owner != field["id"] and label in lowered and label not in own_text:
                found.append(f"{code}: names the label {label!r} of {owner}")
        if text != field["description"]:
            other = sorted({r.lower() for r in LINE_REF.findall(text)} - own)
            if other:
                found.append(f"{code}: names line(s) {other}")
    return found


# Generic phrases that name no line or form and are shared by many fields on purpose. They explain
# little (a legibility gap, not a copied explanation). Any other text that two fields with different
# lines share word for word is a copy, even when it names no line.
GENERIC_PHRASES = frozenset({
    "A current derived finding publishes a computed zero from present inputs that net to zero.",
    "A current derived finding publishes a computed zero under complete authority.",
    "A current derived finding publishes a computed zero.",
    "A current derived finding publishes a zero from closure-backed inputs with no recorded members.",
    "A current derived finding publishes zero because the supporting source family is attested closed-empty under complete authority.",
    "A current derived finding publishes zero through honest closed-empty or zero-credit authority on the direct-election path.",
    "Blocked.",
    "Closure-backed zero.",
    "Computed zero.",
    "Current derived finding publishes this line.",
    "Inapplicable.",
    "No value exists because the rule guard is false.",
    "No value is published because a completeness or guard condition is not satisfied.",
    "No value is published because a scope, election, threshold, or creditability component is not satisfied for the bounded class.",
    "blocked",
    "closure zero",
    "computed zero",
    "guard false",
})


def shared_texts(fields: dict[tuple[str, str], dict]) -> list[dict]:
    """Disposition texts identical across two form fields with different lines, outside the
    generic allowlist: a whole-text copy, caught even when it names no line."""
    owners: dict[str, dict[str, set[str]]] = {}
    for field in fields.values():
        for code, disposition in field["dispositions"].items():
            text = disposition["explain"]
            if text not in GENERIC_PHRASES:
                owners.setdefault(text, {}).setdefault(field["id"], set()).add(code)
    out = []
    for text, by_field in sorted(owners.items()):
        lines = {(f["form"]["form_id"], f["line"]) for f in fields.values() if f["id"] in by_field}
        if len(by_field) > 1 and len(lines) > 1:
            out.append({"text": text, "fields": sorted(by_field)})
    return out


def survey(package_path: Path) -> list[dict]:
    package = json.loads(package_path.read_text())
    out = []
    fields = form_fields(package)
    labels = {
        f["label"].lower(): f["id"] for f in fields.values() if len(f["label"]) >= 12
    }
    for (fid, version), field in sorted(fields.items()):
        bad = problems(field, labels)
        if bad:
            out.append({"id": fid, "version": version, "line": field["line"], "problems": bad})
    for copy in shared_texts(fields):
        out.append({"id": "(shared text)", "version": "", "line": "", "problems": [
            f"identical text on {copy['fields']}: {copy['text']!r}"]})
    return out


if __name__ == "__main__":
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else CORPUS / "package.core-calculations.v63.json"
    print(json.dumps(survey(target), indent=2))
