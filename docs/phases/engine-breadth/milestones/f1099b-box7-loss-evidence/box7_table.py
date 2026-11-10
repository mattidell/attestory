"""Table of what core v83 reads for Form 1099-B box 7, and what a per-sale loss test reads.

Writes box7-table.json beside this file. Reads the committed package and content only.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))
CONTENT = REPO / "packages/content/tax/2025"
P = "tax.us.2025."
BOX7 = P + "f1099b.statement-box7-loss-not-allowed"

# Schedule D line each family posts to on the v83 line rules, and column (h).
FAMILIES = (
    ("covered-st", "1a", "schedule-d-line1a-gain", "proceeds - basis",
     ("proceeds", "basis"), ()),
    ("covered-lt", "8a", "schedule-d-line8a-gain", "proceeds - basis",
     ("proceeds", "basis"), ()),
    ("covered-w-st", "1b", "schedule-d-line1b",
     "proceeds - basis + box_1g_wash_sale_disallowed_amount",
     ("proceeds", "basis", "box_1g_wash_sale_disallowed_amount"), ("proceeds", "basis", "adjustment")),
    ("covered-w-lt", "8b", "schedule-d-line8b",
     "proceeds - basis + box_1g_wash_sale_disallowed_amount",
     ("proceeds", "basis", "box_1g_wash_sale_disallowed_amount"), ("proceeds", "basis", "adjustment")),
    ("noncovered-st", "2", "schedule-d-line2", "proceeds - basis + wash_disallowed",
     ("proceeds", "basis", "wash_disallowed"), ("proceeds", "basis", "adjustment")),
    ("noncovered-lt", "9", "schedule-d-line9", "proceeds - basis + wash_disallowed",
     ("proceeds", "basis", "wash_disallowed"), ("proceeds", "basis", "adjustment")),
    ("code-b-st", "1b", "schedule-d-line1b", "proceeds - corrected_basis + wash_disallowed",
     ("proceeds", "basis", "corrected_basis", "wash_disallowed"), ("proceeds", "basis", "adjustment")),
    ("code-b-lt", "8b", "schedule-d-line8b", "proceeds - corrected_basis + wash_disallowed",
     ("proceeds", "basis", "corrected_basis", "wash_disallowed"), ("proceeds", "basis", "adjustment")),
)


def _load(name: str) -> dict:
    return json.loads((CONTENT / name).read_text(encoding="utf-8"))


def main() -> None:
    package = _load("package.core-calculations.v83.json")
    members = {(m["id"], m["version"]): m for m in package["members"]}
    by_id: dict[str, list[str]] = {}
    for member in package["members"]:
        by_id.setdefault(member["id"], []).append(member["version"])

    question = _load("input-question.f1099b-statement-box7-loss-not-allowed.json")
    readers = []
    for path in sorted(CONTENT.glob("rule*.json")):
        body = json.loads(path.read_text(encoding="utf-8"))
        if BOX7 not in path.read_text(encoding="utf-8"):
            continue
        adopted = body["version"] in by_id.get(body["id"], [])
        readers.append({
            "id": body["id"],
            "version": body["version"],
            "adopted_on_v83": adopted,
            "publishes": body.get("publishes"),
        })

    families = []
    for slug, line, rule_stem, formula, fields, scalars in FAMILIES:
        family_id = P + f"f1099b.{slug}"
        txn = P + f"f1099b.{slug}-txn"
        versions = by_id.get(family_id, [])
        rule_id = P + f"rule.{rule_stem}"
        rule_versions = by_id.get(rule_id, [])
        bundle_name = f"f1099b-{slug}.bundle.json"
        bundle = _load(bundle_name)
        txn_versions = [
            fact["version"] for fact in bundle["fact_types"] if fact["id"] == txn
        ]
        families.append({
            "family": family_id,
            "family_version_on_v83": versions[-1] if versions else None,
            "txn": txn,
            "txn_version": txn_versions[-1] if txn_versions else None,
            "txn_lives_in": bundle["id"] + " " + bundle["version"],
            "txn_is_its_own_package_member": txn in by_id,
            "object_fields_a_loss_test_reads": list(fields),
            "scalar_rows": [f"{txn}.{name}" for name in scalars],
            "scalar_note": (
                "The noncovered adjustment row is omitted when the wash amount is zero. "
                "The loss test reads the sale object, which always carries wash_disallowed."
                if slug.startswith("noncovered") else
                "Code B adjustment scalar is (basis - corrected_basis) + wash, recorded even when zero. "
                "Column (h) uses corrected_basis."
                if slug.startswith("code-b") else
                "Covered rows with no wash have no adjustment scalar."
                if slug.startswith("covered-st") or slug.startswith("covered-lt") else
                "The wash amount is its own object field and is always recorded, including zero."
            ),
            "column_h": formula,
            "schedule_d_line": line,
            "line_rule": rule_id,
            "line_rule_version_on_v83": rule_versions[-1] if rule_versions else None,
        })

    from packages.tax.loader import (  # noqa: PLC0415
        domain_companion_presence_pairs,
        named_covered_flag_refusal_maps,
    )
    pairs = domain_companion_presence_pairs()
    box7_pairs = []
    other_box7_strings = []
    for row, sale in pairs.items():
        companions = sale if isinstance(sale, list) else [sale]
        blob = " ".join([row, *companions])
        if BOX7 in blob or "box7-loss" in blob:
            box7_pairs.append({"row": row, "companions": companions})
        elif "box7" in blob:
            other_box7_strings.append({"row": row, "companions": companions})
    refusal = named_covered_flag_refusal_maps()
    box7_tokens = [
        {"package": list(key), "token": token, "sentence_key": sentence}
        for key, body in refusal.items()
        for token, sentence in body.items()
        if "box7" in token or "box7" in str(sentence)
    ]

    table = {
        "core": {"package": "v83", "registry": "v81", "release": "v81"},
        "fact": {
            "id": BOX7,
            "version": "v1",
            "identity_keys": ["statement", "tax-year"],
            "values": ["yes", "no"],
        },
        "question": {
            "id": question["id"],
            "version": question["version"],
            "adopted_on_v83": question["version"] in by_id.get(question["id"], []),
            "text": question["question"],
            "changes_in_the_recommended_design": False,
        },
        "rules_that_read_the_answer": readers,
        "loader_entries_that_read_the_answer": box7_pairs,
        "loader_pairs_that_mention_some_other_box7": other_box7_strings,
        "covered_flag_refusal_tokens_for_box7": box7_tokens,
        "sale_families": families,
        "not_a_1099b_box7_reader": [
            "tax.us.2025.citation.f1099div.box7 and f1099div.box7.vocabulary are Form 1099-DIV box 7.",
            "The loader presence pair for f1099div.box7-foreign-tax-paid is not this fact.",
        ],
    }
    out = HERE / "box7-table.json"
    out.write_text(json.dumps(table, indent=2) + "\n", encoding="utf-8")
    print(f"rules {len(readers)} adopted {[r['id'] for r in readers if r['adopted_on_v83']]}")
    print(f"loader pairs {len(box7_pairs)} refusal tokens {len(box7_tokens)} families {len(families)}")


if __name__ == "__main__":
    main()
