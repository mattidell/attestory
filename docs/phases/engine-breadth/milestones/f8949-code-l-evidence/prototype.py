"""Measure whether a content-only successor can emit a Form 8949 code L row.

Writes prototype-stop.json beside this file. Does not generate a core, and does not
edit a package. The published schemas and the attachment row collector are the evidence.

    python3 prototype.py
"""

from __future__ import annotations

import copy
import inspect
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from jsonschema import Draft202012Validator  # noqa: E402
from referencing import Registry, Resource  # noqa: E402
from referencing.jsonschema import DRAFT202012  # noqa: E402

from packages.derivation.runner import _Run  # noqa: E402

CONTENT = REPO / "packages/content/tax/2025"
SCHEMAS = REPO / "packages/schemas" / "tax"


def _validator(name: str) -> Draft202012Validator:
    schema = json.loads((SCHEMAS / name).read_text(encoding="utf-8"))
    resource = Resource.from_contents(schema, default_specification=DRAFT202012)
    registry = Registry().with_resource(schema["$id"], resource)
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema, registry=registry)


def _errors(validator: Draft202012Validator, instance: dict) -> list[str]:
    return sorted(
        f"{'/'.join(str(part) for part in error.absolute_path) or '<root>'}: {error.message}"
        for error in validator.iter_errors(instance)
    )


def main() -> None:
    attachment = json.loads((CONTENT / "attachment.f8949.v6.json").read_text(encoding="utf-8"))
    v8 = _validator("attachment-rule.v8.schema.json")
    v11 = _validator("attachment-rule.v11.schema.json")
    base_errors = _errors(v8, attachment)

    filtered = copy.deepcopy(attachment)
    filtered["itemizations"][0]["row_sets"][0]["rows"]["where"] = {"verdict": "disallowed"}
    filter_errors = _errors(v8, filtered)

    coded = copy.deepcopy(attachment)
    coded["itemizations"][0]["adjustment_rows"] = [{
        "kind": "code_l_nondeductible_loss",
        "label": "column (g), code L",
        "rows": coded["itemizations"][0]["row_sets"][0]["rows"],
        "sign": "negative",
        "subtotal_symbol": "tax.us.2025.demo.code-l-adjustment",
    }]
    kind_errors = _errors(v8, coded)

    signed = copy.deepcopy(attachment)
    signed["itemizations"][0]["adjustment_rows"] = [{
        "kind": "nominee_distribution",
        "label": "column (g), code L",
        "rows": signed["itemizations"][0]["row_sets"][0]["rows"],
        "sign": "positive",
        "subtotal_symbol": "tax.us.2025.demo.code-l-adjustment",
    }]
    sign_errors = _errors(v8, signed)

    derived = copy.deepcopy(attachment)
    derived["schema"] = "attachment-rule.v11"
    derived["itemizations"][0]["row_sets"][0]["rows"] = {
        "op": "enumerate_published",
        "fact_type": {"id": "tax.us.2025.demo.code-l-adjustment", "version": "v1"},
    }
    derived_errors = _errors(v11, derived)
    v11_schema = json.loads((SCHEMAS / "attachment-rule.v11.schema.json").read_text(encoding="utf-8"))
    fragment_validator = Draft202012Validator(
        {"$ref": v11_schema["$id"] + "#/$defs/adjustment_row"},
        registry=Registry().with_resource(
            v11_schema["$id"],
            Resource.from_contents(v11_schema, default_specification=DRAFT202012),
        ),
    )
    enumerated_adjustment = {
        "kind": "nominee_distribution",
        "label": "a single derived amount",
        "sign": "negative",
        "rows": {
            "op": "enumerate_published",
            "fact_type": {"id": "tax.us.2025.demo.code-l-adjustment", "version": "v1"},
        },
        "subtotal_symbol": "tax.us.2025.demo.code-l-adjustment",
    }
    fragment_errors = _errors(fragment_validator, enumerated_adjustment)
    collector = inspect.getsource(_Run._collect_row_source)
    enumerate_row = '{"finding_id": fid, "value": str(finding.get("value"))}'
    collector_emits_single_value = enumerate_row in collector
    collector_names_column_f = "column (f)" in collector or '"code"' in collector

    rule_schema = json.loads(
        (REPO / "packages/schemas/derivation/rule-artifact.v15.schema.json").read_text(encoding="utf-8"))
    collect = next(
        branch for branch in rule_schema["$defs"]["expr"]["oneOf"]
        if (branch.get("properties") or {}).get("op", {}).get("const") == "collect"
    )

    stop = {
        "scratch_core_v86_generated": False,
        "earlier_milestone_harnesses_run": False,
        "why_no_successor_package": (
            "A successor package can change a line's dollars with the operations core v85 "
            "already has. It cannot emit the Form 8949 row Example 2 requires. Building a "
            "core that only zeros column (h) would miss the charter."
        ),
        "published_attachment_validates": base_errors == [],
        "attempts": [
            {
                "change": "Add a where filter on collect_members so only a disallowed sale is itemized.",
                "schema": "attachment-rule.v8",
                "rejected": bool(filter_errors),
                "errors": filter_errors[:4],
            },
            {
                "change": "Add an adjustment row whose kind is code L.",
                "schema": "attachment-rule.v8",
                "rejected": bool(kind_errors),
                "errors": kind_errors[:4],
            },
            {
                "change": "Keep a published adjustment kind and set its sign to positive. Code L column (g) is positive.",
                "schema": "attachment-rule.v8",
                "rejected": bool(sign_errors),
                "errors": sign_errors[:4],
            },
            {
                "change": "On attachment-rule.v11, list a derived amount as a positive itemization row with enumerate_published.",
                "schema": "attachment-rule.v11",
                "rejected": bool(derived_errors),
                "errors": derived_errors[:6],
            },
            {
                "change": "On attachment-rule.v11, an adjustment row of a published kind may list enumerate_published. The sign stays negative and the kind stays closed.",
                "schema": "attachment-rule.v11#/$defs/adjustment_row",
                "rejected": bool(fragment_errors),
                "errors": fragment_errors[:4],
                "fragment_valid": fragment_errors == [],
            },
        ],
        "collector": {
            "method": "packages.derivation.runner._Run._collect_row_source",
            "enumerate_published_row_is_finding_id_and_value": collector_emits_single_value,
            "row_names_a_code_or_column_f": collector_names_column_f,
        },
        "collect_expression": {
            "properties": sorted(collect["properties"]),
            "additionalProperties": collect["additionalProperties"],
        },
        "cause": (
            "Form 8949 rows in this product are recorded family members. Code W and code B "
            "each have a family, and the attachment itemizes that family's proceeds, basis, "
            "and adjustment under a fixed label. collect_members has no filter. Adjustment "
            "kinds on the published attachment schemas are nominee, accrued interest, and "
            "ABP, and the sign is fixed negative. A v11 adjustment row of one of those kinds "
            "may list enumerate_published, and that fragment validates, but the collector "
            "emits one value per finding and the sign is still negative. Positive itemization "
            "rows on v11 still require collect_members. A subject rule can publish the code L "
            "amount, and a line rule can add it, but neither produces columns (d), (e), (f), "
            "(g), and (h) for that sale, and a covered loss stays in the line 1a or 8a family."
        ),
        "smallest_change": (
            "A recording-surface change, then content only. When box 7 is yes and column (h) "
            "before code L is negative, record that sale in a code L family the way a code B "
            "sale is recorded, with proceeds, the basis shown, and the code L amount computed "
            "from those amounts and any wash or code B adjustment already recorded. A successor "
            "attachment itemizes it, and the successor Schedule D lines pick up column (h), "
            "which the instructions put at zero. No new filer amount, no kernel change, and no "
            "edit of a published schema. The other sufficient change is a new attachment schema "
            "that can itemize one derived sale as columns (d) through (h) and a line rule that "
            "can drop that sale from line 1a or 8a. That is a schema and a presentation change."
        ),
    }
    (HERE / "prototype-stop.json").write_text(json.dumps(stop, indent=2) + "\n", encoding="utf-8")
    print(f"base_valid {stop['published_attachment_validates']}")
    for attempt in stop["attempts"]:
        print(f"rejected {attempt['rejected']} {attempt['change'][:60]}")
    print(f"single_value_row {collector_emits_single_value} names_code {collector_names_column_f}")


if __name__ == "__main__":
    main()
