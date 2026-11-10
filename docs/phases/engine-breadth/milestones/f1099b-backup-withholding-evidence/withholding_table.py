"""Withholding table generator for core v82.

Evidence for docs/phases/engine-breadth/milestones/f1099b-backup-withholding.md (P0).
Lists every source Form 1040 line 25b reads on core v82, its subtotal rule, statement object,
per-statement answer, pairing rule, and Form 1099-B box 4 question and reader rules.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
CONTENT = REPO / "packages/content/tax/2025"

P = "tax.us.2025."


def short(name: str) -> str:
    return name.removeprefix(P)


def load_json(name: str) -> dict[str, Any]:
    return json.loads((CONTENT / name).read_text(encoding="utf-8"))


def build_withholding_table() -> dict[str, Any]:
    pkg_v82 = load_json("package.core-calculations.v82.json")
    members_v82 = {m["id"]: m["version"] for m in pkg_v82["members"]}

    rule_line25b = load_json("rule.form1040-line25b.v6.json")
    field_line25b = load_json("form1040.line-25b.form-field.v4.json")

    # Sources on line 25b
    sources = {
        "1099-INT": {
            "document": "Form 1099-INT",
            "subtotal_symbol": P + "interest.b4-withholding-subtotal",
            "subtotal_rule": {
                "id": P + "rule.f1099int-b4-subtotal",
                "version": members_v82.get(P + "rule.f1099int-b4-subtotal"),
            },
            "source_family": {
                "id": P + "f1099int.b4",
                "version": members_v82.get(P + "f1099int.b4"),
            },
            "closure_mapping": {
                "id": P + "closure-mapping.f1099int-b4",
                "version": members_v82.get(P + "closure-mapping.f1099int-b4"),
            },
            "withholding_fact_type": {
                "id": P + "f1099int.box4-withholding",
                "version": "v1",
                "identity_keys": ["payer", "statement", "tax-year"],
                "value_schema": {"type": "number", "minimum": 0},
            },
            "statement_object_income_types": [
                P + "f1099int.box1-interest",
                P + "f1099int.box3-interest",
                P + "f1099int.box8-tax-exempt-interest",
                P + "f1099int.box10-market-discount",
            ],
            "income_source_set": P + "f1099int.b1",
            "per_statement_question": {
                "id": P + "input-question.f1099int-box4",
                "version": members_v82.get(P + "input-question.f1099int-box4"),
                "question": load_json("input-question.f1099int-box4.v1.json")["question"],
            },
            "pairing_rule": {
                "op": "require_paired",
                "key": "statement",
                "withholding": P + "f1099int.box4-withholding",
                "income_types_count": 4,
            },
        },
        "1099-DIV": {
            "document": "Form 1099-DIV",
            "subtotal_symbol": P + "dividends.b4-withholding-subtotal",
            "subtotal_rule": {
                "id": P + "rule.f1099div-b4-subtotal",
                "version": members_v82.get(P + "rule.f1099div-b4-subtotal"),
            },
            "source_family": {
                "id": P + "f1099div.b4",
                "version": members_v82.get(P + "f1099div.b4"),
            },
            "closure_mapping": {
                "id": P + "closure-mapping.f1099div-b4",
                "version": members_v82.get(P + "closure-mapping.f1099div-b4"),
            },
            "withholding_fact_type": {
                "id": P + "f1099div.box4-withholding",
                "version": "v1",
                "identity_keys": ["payer", "statement", "tax-year"],
                "value_schema": {"type": "number", "minimum": 0},
            },
            "statement_object_income_types": [
                P + "f1099div.box1a-ordinary",
                P + "f1099div.box2a-capital-gain-distribution",
                P + "f1099div.box12-exempt-interest-dividends",
            ],
            "income_source_set": P + "f1099div.1a",
            "per_statement_question": {
                "id": P + "input-question.f1099div-box4",
                "version": members_v82.get(P + "input-question.f1099div-box4"),
                "question": load_json("input-question.f1099div-box4.v1.json")["question"],
            },
            "pairing_rule": {
                "op": "require_paired",
                "key": "statement",
                "withholding": P + "f1099div.box4-withholding",
                "income_types_count": 3,
            },
        },
        "1099-R": {
            "document": "Form 1099-R (IRA)",
            "subtotal_symbol": P + "ira.box4-withholding-subtotal",
            "subtotal_rule": {
                "id": P + "rule.f1099r-box4-subtotal",
                "version": members_v82.get(P + "rule.f1099r-box4-subtotal"),
            },
            "source_family": {
                "id": P + "f1099r.box4",
                "version": members_v82.get(P + "f1099r.box4"),
            },
            "closure_mapping": {
                "id": P + "closure-mapping.f1099r-box4",
                "version": members_v82.get(P + "closure-mapping.f1099r-box4"),
            },
            "withholding_fact_type": {
                "id": P + "f1099r.ira-box4-withholding",
                "version": "v1",
                "identity_keys": ["payer", "statement", "tax-year"],
                "value_schema": {"type": "number", "minimum": 0},
            },
            "statement_object_income_types": [
                P + "f1099r.ira-box1-taxable-distribution",
            ],
            "income_source_set": P + "f1099r.ira-fully-taxable",
            "per_statement_question": {
                "id": P + "input-question.f1099r-box4",
                "version": members_v82.get(P + "input-question.f1099r-box4"),
                "question": load_json("input-question.f1099r-box4.v1.json")["question"],
            },
            "pairing_rule": {
                "op": "require_paired",
                "key": "statement",
                "withholding": P + "f1099r.ira-box4-withholding",
                "income_types_count": 1,
            },
        },
        "1099-G": {
            "document": "Form 1099-G",
            "subtotal_symbol": P + "unemployment.b4-withholding-subtotal",
            "subtotal_rule": {
                "id": P + "rule.f1099g-b4-subtotal",
                "version": members_v82.get(P + "rule.f1099g-b4-subtotal"),
            },
            "source_family": {
                "id": P + "f1099g.b4",
                "version": members_v82.get(P + "f1099g.b4"),
            },
            "closure_mapping": {
                "id": P + "closure-mapping.f1099g-b4",
                "version": members_v82.get(P + "closure-mapping.f1099g-b4"),
            },
            "withholding_fact_type": {
                "id": P + "f1099g.box4-withholding",
                "version": "v1",
                "identity_keys": ["payer", "statement", "tax-year"],
                "value_schema": {"type": "number", "minimum": 0},
            },
            "statement_object_income_types": [
                P + "f1099g.box1-unemployment",
            ],
            "income_source_set": P + "f1099g.1",
            "per_statement_question": {
                "id": P + "input-question.f1099g-box4",
                "version": members_v82.get(P + "input-question.f1099g-box4"),
                "question": load_json("input-question.f1099g-box4.v1.json")["question"],
            },
            "pairing_rule": {
                "op": "require_paired",
                "key": "statement",
                "withholding": P + "f1099g.box4-withholding",
                "income_types_count": 1,
            },
        },
        "SSA-1099": {
            "document": "Form SSA-1099",
            "subtotal_symbol": P + "ssa1099.b6-withholding-subtotal",
            "subtotal_rule": {
                "id": P + "rule.ssa1099-b6-subtotal",
                "version": members_v82.get(P + "rule.ssa1099-b6-subtotal"),
            },
            "source_family": {
                "id": P + "ssa1099.b6",
                "version": members_v82.get(P + "ssa1099.b6"),
            },
            "closure_mapping": {
                "id": P + "closure-mapping.ssa1099-b6",
                "version": members_v82.get(P + "closure-mapping.ssa1099-b6"),
            },
            "withholding_fact_type": {
                "id": P + "ssa1099.box6-voluntary-withholding",
                "version": "v1",
                "identity_keys": ["taxpayer", "statement", "tax-year"],
                "value_schema": {"type": "number", "minimum": 0},
            },
            "statement_object_income_types": [
                P + "ssa1099.box5-net-benefits",
            ],
            "income_source_set": P + "ssa1099.benefits",
            "per_statement_question": {
                "id": P + "input-question.ssa1099-box6",
                "version": members_v82.get(P + "input-question.ssa1099-box6"),
                "question": load_json("input-question.ssa1099-box6.v1.json")["question"],
            },
            "pairing_rule": {
                "op": "require_paired",
                "key": "statement",
                "withholding": P + "ssa1099.box6-voluntary-withholding",
                "income_types_count": 1,
            },
        },
        "1099-B": {
            "document": "Form 1099-B",
            "subtotal_symbol": None,
            "subtotal_rule": None,
            "source_family": None,
            "closure_mapping": None,
            "withholding_fact_type": {
                "id": P + "f1099b.statement-box4-withholding-reported",
                "version": "v1",
                "identity_keys": ["statement", "tax-year"],
                "value_schema": {"enum": ["yes", "no"]},
            },
            "statement_object_income_types": [
                P + "f1099b.covered-st-txn",
                P + "f1099b.covered-lt-txn",
                P + "f1099b.covered-w-st-txn",
                P + "f1099b.covered-w-lt-txn",
                P + "f1099b.noncovered-st-txn",
                P + "f1099b.noncovered-lt-txn",
                P + "f1099b.code-b-st-txn",
                P + "f1099b.code-b-lt-txn",
            ],
            "income_source_set": "Per-family / grouped closures for the 8 transaction families",
            "per_statement_question": {
                "id": P + "input-question.f1099b-statement-box4-withholding-reported",
                "version": members_v82.get(P + "input-question.f1099b-statement-box4-withholding-reported"),
                "question": load_json("input-question.f1099b-statement-box4-withholding-reported.json")["question"],
            },
            "pairing_rule": {
                "op": "require_paired",
                "key": "statement",
                "withholding": P + "f1099b.statement-box4-withholding-reported",
                "income_types_count": 8,
            },
            "rules_reading_box4_question": [
                {
                    "rule_id": P + "rule.form1040-line25b",
                    "version": "v6",
                    "role_in_when": "require_paired on key statement between 8 sale txn types and statement-box4-withholding-reported",
                    "role_in_value": "choose condition: if any sale count > 0 and not collect_categorical_all_equal == 'no', block DEPENDENCY_ABSENT",
                }
            ],
            "carries_box4_amount_today": False,
        },
    }

    return {
        "core_version": "v82",
        "line_25b_symbol": P + "payments.line25b",
        "line_25b_rule_version": "v6",
        "line_25b_field_version": "v4",
        "sources": sources,
        "carries_box4_amount_summary": "No Form 1099-B record (neither the statement fact types nor the sale transaction fact types nor the scalar companion rows) carries a box 4 amount field on core v82.",
    }


def main() -> None:
    data = build_withholding_table()
    out_file = HERE / "withholding-table-v82.json"
    out_file.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {out_file.name}")


if __name__ == "__main__":
    main()
