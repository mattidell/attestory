"""Table of what core v84 reads for Form 1099-B statements and box 4.

Writes statement-table.json beside this file. Reads the committed package
and content only. Synthetic paths only; no absolute workstation paths.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))
CONTENT = REPO / "packages/content/tax/2025"
TAX = REPO / "packages/tax"
P = "tax.us.2025."
BOX4 = P + "f1099b.statement-box4-withholding"
BOX4_REPORTED = P + "f1099b.statement-box4-withholding-reported"
STATEMENT_KIND = "tax.us.f1099b-statement"
SALE_SLUGS = (
    "covered-st", "covered-lt", "covered-w-st", "covered-w-lt",
    "noncovered-st", "noncovered-lt", "code-b-st", "code-b-lt",
)


def _load(name: str) -> dict[str, Any]:
    return json.loads((CONTENT / name).read_text(encoding="utf-8"))


def _walk(node: Any) -> str:
    return json.dumps(node, sort_keys=True)


def _mentions(body: dict[str, Any], *needles: str) -> list[str]:
    blob = _walk(body)
    return [needle for needle in needles if needle in blob]


def main() -> None:
    package = _load("package.core-calculations.v84.json")
    members = {(m["id"], m["version"]): m for m in package["members"]}
    by_id: dict[str, list[str]] = {}
    for member in package["members"]:
        by_id.setdefault(member["id"], []).append(member["version"])

    def adopted(identity: str, version: str) -> bool:
        return version in by_id.get(identity, [])

    questions = []
    for path in sorted(CONTENT.glob("input-question*.json")):
        body = json.loads(path.read_text(encoding="utf-8"))
        hits = _mentions(body, BOX4, BOX4_REPORTED, STATEMENT_KIND, "Form 1099-B", "f1099b")
        if not hits:
            continue
        questions.append({
            "id": body["id"],
            "version": body["version"],
            "adopted_on_v84": adopted(body["id"], body["version"]),
            "fact_type": (body.get("fact_type") or {}).get("id"),
            "question": body.get("question"),
            "mentions": hits,
            "file": path.name,
        })

    rules = []
    for path in sorted(CONTENT.glob("rule*.json")):
        body = json.loads(path.read_text(encoding="utf-8"))
        hits = _mentions(body, BOX4, BOX4_REPORTED, STATEMENT_KIND, P + "f1099b.b4")
        if not hits:
            continue
        rules.append({
            "id": body["id"],
            "version": body["version"],
            "adopted_on_v84": adopted(body["id"], body["version"]),
            "publishes": body.get("publishes"),
            "mentions": hits,
            "file": path.name,
        })

    families = []
    for slug in SALE_SLUGS:
        family_id = P + f"f1099b.{slug}"
        txn = P + f"f1099b.{slug}-txn"
        families.append({
            "family": family_id,
            "family_version_on_v84": (by_id.get(family_id) or [None])[-1],
            "txn": txn,
            "closes": "sales of this class, not the set of Form 1099-B statements",
            "closure_mapping_on_v84": (by_id.get(P + f"closure-mapping.f1099b-{slug}")
                                       or by_id.get(P + f"closure-mapping.f1099b.{slug.split('-', 1)[0]}")
                                       or []),
        })

    b4_family = _load("family.f1099b-b4.json")
    box4_bundle = _load("f1099b-box4.bundle.json")
    box4_question = _load("input-question.f1099b-box4.v1.json")
    line25b = _load("rule.form1040-line25b.v7.json")
    field = _load("form1040.line-25b.form-field.v5.json")

    pairing_rules = []
    for path in sorted(CONTENT.glob("rule*.json")):
        body = json.loads(path.read_text(encoding="utf-8"))
        blob = _walk(body)
        if '"key": "statement"' not in blob or "f1099b" not in blob:
            continue
        if not adopted(body["id"], body["version"]):
            continue
        pairing_rules.append({
            "id": body["id"],
            "version": body["version"],
            "publishes": body.get("publishes"),
            "file": path.name,
        })

    from packages.tax import loader  # noqa: PLC0415
    v84_decl = loader.domain_package_companion_declarations()[
        (P + "package.core-calculations", "v84")
    ]
    v84_pairs = v84_decl["presence_pairs"]
    f1099b_pairs = [
        {"row": row, "companion": companion}
        for row, companion in sorted(v84_pairs.items())
        if companion is not None and ("f1099b" in row or "f1099b" in str(companion))
    ]
    box4_in_v84_pairs = [
        {"row": row, "companion": companion}
        for row, companion in v84_pairs.items()
        if BOX4 in row or BOX4 in str(companion)
    ]
    refusal = loader.named_covered_flag_refusal_maps()
    v84_map = refusal.get((P + "package.core-calculations", "v84"), {})

    recording = []
    for path in sorted(TAX.glob("*.py")):
        text = path.read_text(encoding="utf-8")
        if "f1099b" in text or STATEMENT_KIND in text:
            recording.append({
                "file": path.name,
                "mentions_statement_kind": STATEMENT_KIND in text,
                "mentions_box4": BOX4 in text or "statement-box4" in text,
            })

    table = {
        "core": {"package": "v84", "registry": "v82", "release": "v82"},
        "box4_amount": {
            "id": BOX4,
            "version": "v1",
            "identity_keys": ["statement", "tax-year"],
            "value_schema": {"type": "number", "minimum": 0},
            "lives_in": box4_bundle["id"] + " " + box4_bundle["version"],
            "source_family": {
                "id": b4_family["id"],
                "version": b4_family["version"],
                "adopted_on_v84": adopted(b4_family["id"], b4_family["version"]),
                "closure_claim": b4_family.get("closure_claim"),
                "require_closed_on_line25b": False,
                "closure_mapping_on_v84": by_id.get(P + "closure-mapping.f1099b-b4", []),
            },
        },
        "legacy_box4_yes_no": {
            "id": BOX4_REPORTED,
            "question_still_a_member": adopted(
                P + "input-question.f1099b-statement-box4-withholding-reported", "v1"),
            "read_by_line25b_v7": BOX4_REPORTED in _walk(line25b),
        },
        "question_that_asks_the_amount": {
            "id": box4_question["id"],
            "version": box4_question["version"],
            "adopted_on_v84": adopted(box4_question["id"], box4_question["version"]),
            "text": box4_question["question"],
            "asked_when": (
                "line 25b v7 require_paired needs a box 4 amount for each recorded sale's "
                "statement. A recorded statement with no sale is not an income row, so the "
                "question is not asked of it."
            ),
        },
        "line25b": {
            "rule": P + "rule.form1040-line25b",
            "version": "v7",
            "form_field": field["id"] + " " + field["version"],
            "pairing": (
                "require_paired on statement between the eight sale transaction types and "
                + BOX4
            ),
            "surplus_amount_without_sale": "allowed, and the subtotal collects it",
            "empty_amount_set": (
                "the subtotal selection default publishes 0; the filer is not asked to "
                "close f1099b.b4"
            ),
            "blocked_explain": field["dispositions"]["blocked"]["explain"],
        },
        "rules_that_read_box4_or_the_b4_family": [
            row for row in rules if row["adopted_on_v84"]
        ],
        "rules_that_pair_on_statement_for_f1099b": pairing_rules,
        "questions_that_ask_box4": [
            row for row in questions if row["adopted_on_v84"]
            and row["fact_type"] in {BOX4, BOX4_REPORTED}
        ],
        "other_adopted_questions_that_name_a_1099b_statement_or_sale": [
            row for row in questions if row["adopted_on_v84"]
            and row["fact_type"] not in {BOX4, BOX4_REPORTED}
        ],
        "sale_families_on_v84": families,
        "what_closes_every_form_1099b_statement": (
            "Nothing. Sale-family closures close sales of each class. f1099b.b4 is not "
            "require_closed. There is no statement-set closure and no return-level "
            "question that asks whether every Form 1099-B was recorded."
        ),
        "how_a_no_sale_statement_is_recorded": {
            "product_recording_module": None,
            "kernel_act": "entity-introduced of kind tax.us.f1099b-statement",
            "side_effect_of_a_sale": (
                "recording a sale introduces broker, statement and transaction entities "
                "as the sale's identity keys"
            ),
            "box4_amount_without_a_sale": (
                "an assertion of statement-box4-withholding on a statement entity is "
                "admitted; line 25b counts it (Decision 6). Nothing asks for that assertion."
            ),
        },
        "loader_entries_that_read_box4": box4_in_v84_pairs,
        "loader_v84_presence_pairs_for_f1099b_sale_scalars": f1099b_pairs,
        "loader_note": (
            "Core v84's companion declaration copies v83: box 4 takes no presence pair. "
            "Scalar pairs require each sale amount row to have its sale object. They do "
            "not introduce or close a statement."
        ),
        "covered_flag_refusal_map_on_v84": {
            "copies": "v83 / v82 map; no box 4 token",
            "objects": sorted(v84_map.keys()),
        },
        "packages_tax_files_that_mention_f1099b": recording,
        "not_a_1099b_statement_reader": [
            "tax.us.2025.citation.f1099div.box7 and f1099div.box7.vocabulary are Form 1099-DIV box 7.",
            "input-question.f8949-no1099b-sold asks about sales with no Form 1099-B.",
        ],
    }
    out = HERE / "statement-table.json"
    text = json.dumps(table, indent=2) + "\n"
    for needle in ("/Users/", "/private/", "/tmp/", "/var/"):
        if needle in text:
            raise SystemExit(f"table contains {needle}")
    out.write_text(text, encoding="utf-8")
    adopted_box4_rules = [r["id"] for r in rules if r["adopted_on_v84"]]
    print(f"box4/b4 rules adopted {len(adopted_box4_rules)}")
    print(f"questions {sum(1 for q in questions if q['adopted_on_v84'])}")
    print(f"pairing rules {len(pairing_rules)}")
    print(f"loader box4 pairs {len(box4_in_v84_pairs)} f1099b scalar pairs {len(f1099b_pairs)}")
    print(f"tax recording files {recording}")


if __name__ == "__main__":
    main()
