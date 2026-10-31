"""Survey: where each closure question's declared wording lives, for every closure in a core package.

Usage: python3 survey.py [package-path]   (default: core v66)   -> JSON on stdout

For each source-closure-mapping the package pins, records the closure fact type (its title, from the
bundle that declares it), the source family (title, closure_claim) and the mapping's own keys, and
classifies the wording. Reads committed content only; invents nothing.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

CORPUS = Path(__file__).resolve().parents[5] / "packages" / "content" / "tax" / "2025"
DEFAULT = CORPUS / "package.core-calculations.v66.json"


def _load_corpus() -> dict[tuple[str, str, str], dict]:
    index: dict[tuple[str, str, str], dict] = {}
    for path in CORPUS.glob("*.json"):
        try:
            body = json.loads(path.read_text())
        except ValueError:
            continue
        if isinstance(body, dict) and "id" in body and "version" in body:
            index[(body["id"], body["version"], body.get("schema", ""))] = body
    return index


def _by_pin(index: dict, pin_id: str, version: str) -> dict:
    hits = [b for (i, v, _), b in index.items() if (i, v) == (pin_id, version)]
    assert len(hits) == 1, (pin_id, version, len(hits))
    return hits[0]


QUESTION_WORDS = re.compile(r"^(have|has|is|are|do|does|did|was|were)\b", re.IGNORECASE)


def survey(package_path: Path = DEFAULT) -> list[dict]:
    package = json.loads(package_path.read_text())
    index = _load_corpus()
    fact_types: dict[tuple[str, str], tuple[dict, str]] = {}
    for m in package["members"]:
        if m["role"] == "fact-type-bundle":
            bundle = _by_pin(index, m["id"], m["version"])
            for ft in bundle["fact_types"]:
                fact_types[(ft["id"], ft["version"])] = (ft, bundle["id"])
    rows = []
    for m in package["members"]:
        if m["role"] != "source-closure-mapping":
            continue
        mapping = _by_pin(index, m["id"], m["version"])
        fam = _by_pin(index, mapping["family"]["id"], mapping["family"]["version"])
        cid = (mapping["closure_fact_type"]["id"], mapping["closure_fact_type"]["version"])
        ft, bundle_id = fact_types.get(cid, ({}, None))
        title, claim, ftitle = ft.get("title"), fam.get("closure_claim"), fam.get("title")
        rows.append({
            "mapping": m["id"],
            "family": fam["id"],
            "family_version": fam["version"],
            "family_schema": fam["schema"],
            "closure_fact_type": cid[0],
            "closure_fact_type_declared_in": bundle_id,
            "closure_fact_type_title": title,
            "closure_fact_type_has_description_key": "description" in ft,
            "family_title": ftitle,
            "family_closure_claim": claim,
            "mapping_keys": sorted(mapping),
            "mapping_has_wording": any(k in mapping for k in ("title", "question", "wording", "description", "label")),
            "title_is_question": bool(title and QUESTION_WORDS.match(title)),
            "title_ends_with_question_mark": bool(title and title.rstrip().endswith("?")),
        })
    return rows


def main() -> None:
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT
    rows = survey(path)
    summary = {
        "package": path.name,
        "closures": len(rows),
        "closure_fact_type_with_title": sum(bool(r["closure_fact_type_title"]) for r in rows),
        "closure_fact_type_with_description": sum(r["closure_fact_type_has_description_key"] for r in rows),
        "family_with_title": sum(bool(r["family_title"]) for r in rows),
        "family_with_closure_claim": sum(bool(r["family_closure_claim"]) for r in rows),
        "mapping_with_wording": sum(r["mapping_has_wording"] for r in rows),
        "title_is_question": sum(r["title_is_question"] for r in rows),
        "title_ends_with_question_mark": sum(r["title_ends_with_question_mark"] for r in rows),
        "closure_fact_type_not_found": [r["mapping"] for r in rows if not r["closure_fact_type_title"]],
    }
    print(json.dumps({"summary": summary, "families": rows}, indent=1, sort_keys=True))


if __name__ == "__main__":
    main()
