"""What core v85 reads for Form 1099-B box 7, and how Form 8949 codes B and W are pathed.

Writes codel-table.json beside this file. Reads the committed package, content, and
the published attachment schema only.
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
SCHEMAS = REPO / "packages/schemas"
P = "tax.us.2025."
BOX7 = P + "f1099b.statement-box7-loss-not-allowed"

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


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    package = _load(CONTENT / "package.core-calculations.v85.json")
    by_id: dict[str, list[str]] = {}
    for member in package["members"]:
        by_id.setdefault(member["id"], []).append(member["version"])

    question = _load(CONTENT / "input-question.f1099b-statement-box7-loss-not-allowed.json")
    readers = []
    for path in sorted(CONTENT.glob("rule*.json")):
        text = path.read_text(encoding="utf-8")
        if "box7" not in text or "f1099b" not in text:
            continue
        body = json.loads(text)
        if body.get("schema") != "rule-artifact.v15" and not str(body.get("schema", "")).startswith("rule-artifact"):
            continue
        readers.append({
            "id": body["id"],
            "version": body["version"],
            "adopted_on_v85": body["version"] in by_id.get(body["id"], []),
            "publishes": body.get("publishes"),
            "reads_box7_fact": BOX7 in text,
            "reads_box7_verdict_or_check": "box7-verdict" in text or "box7-loss-check" in text,
        })

    families = []
    for slug, line, rule_stem, formula, fields, scalars in FAMILIES:
        family_id = P + f"f1099b.{slug}"
        txn = P + f"f1099b.{slug}-txn"
        rule_id = P + f"rule.{rule_stem}"
        bundle = _load(CONTENT / f"f1099b-{slug}.bundle.json")
        txn_versions = [fact["version"] for fact in bundle["fact_types"] if fact["id"] == txn]
        families.append({
            "family": family_id,
            "family_versions_on_v85": by_id.get(family_id, []),
            "txn": txn,
            "txn_version": txn_versions[-1] if txn_versions else None,
            "object_fields": list(fields),
            "scalar_rows": [f"{txn}.{name}" for name in scalars],
            "column_h": formula,
            "schedule_d_line": line,
            "line_rule": rule_id,
            "line_rule_versions_on_v85": by_id.get(rule_id, []),
            "on_form_8949": slug not in ("covered-st", "covered-lt"),
        })

    from packages.tax.loader import (  # noqa: PLC0415
        domain_companion_presence_pairs,
        named_covered_flag_refusal_maps,
    )
    pairs = domain_companion_presence_pairs()
    box7_pairs = []
    for row, sale in pairs.items():
        companions = sale if isinstance(sale, list) else [sale]
        blob = " ".join([row, *companions])
        if BOX7 in blob or "box7-loss" in blob:
            box7_pairs.append({"row": row, "companions": companions})
    refusal = named_covered_flag_refusal_maps()
    box7_tokens = [
        {"package": list(key), "token": token}
        for key, body in refusal.items()
        for token in body
        if "box7" in token or "box7" in str(body[token])
    ]

    attachment = _load(CONTENT / "attachment.f8949.v6.json")
    labels = [
        {"part_id": part.get("part_id"), "label": part.get("label")}
        for part in attachment.get("itemizations") or []
    ]
    schema_name = attachment["schema"]
    schema = _load(SCHEMAS / "tax" / f"{schema_name}.schema.json")
    kind_enum = schema["$defs"]["adjustment_row"]["properties"]["kind"]["enum"]
    sign = schema["$defs"]["adjustment_row"]["properties"]["sign"]
    collect_keys = sorted(schema["$defs"]["collect_members"]["properties"])
    v11 = _load(SCHEMAS / "tax" / "attachment-rule.v11.schema.json")
    v11_kinds = v11["$defs"]["adjustment_row_direct"]["properties"]["kind"]["enum"]
    v11_sign = v11["$defs"]["adjustment_row_direct"]["properties"]["sign"]
    enumerate_keys = sorted(v11["$defs"]["enumerate_published"]["properties"])

    questions = []
    for path in sorted(CONTENT.glob("input-question*.json")):
        body = json.loads(path.read_text(encoding="utf-8"))
        text = path.read_text(encoding="utf-8")
        fact = (body.get("fact_type") or {}).get("id", "")
        keeps = (
            BOX7 in text
            or fact.endswith("no-other-form8949-adjustments")
            or fact.endswith("form8949-in-class")
            or fact.endswith("form8949-code-b-in-class")
            or fact.endswith("no-form8949-sources")
        )
        if keeps:
            questions.append({
                "id": body.get("id"),
                "version": body.get("version"),
                "adopted_on_v85": body.get("version") in by_id.get(body.get("id"), []),
                "fact_type": fact,
                "text": body.get("question"),
            })

    rule_artifact = _load(SCHEMAS / "derivation" / "rule-artifact.v15.schema.json")
    collect = next(
        branch for branch in rule_artifact["$defs"]["expr"]["oneOf"]
        if isinstance(branch, dict) and (branch.get("properties") or {}).get("op", {}).get("const") == "collect"
    )

    table = {
        "core": {"package": "v85", "registry": "v83", "release": "v83"},
        "fact": {
            "id": BOX7,
            "version": "v1",
            "identity_keys": ["statement", "tax-year"],
            "values": ["yes", "no"],
        },
        "question": {
            "id": question["id"],
            "version": question["version"],
            "adopted_on_v85": question["version"] in by_id.get(question["id"], []),
            "text": question["question"],
        },
        "rules_that_mention_box7": readers,
        "loader_entries_that_mention_box7": box7_pairs,
        "covered_flag_refusal_tokens_for_box7": box7_tokens,
        "sale_families": families,
        "line_16": {
            "id": P + "rule.schedule-d-line16",
            "versions_on_v85": by_id.get(P + "rule.schedule-d-line16", []),
        },
        "form_8949_code_paths": {
            "attachment": {
                "id": attachment["id"],
                "version": attachment["version"],
                "schema": schema_name,
                "adopted_on_v85": attachment["version"] in by_id.get(attachment["id"], []),
            },
            "itemization_labels": labels,
            "code_letter_in_a_label": sorted({
                label["label"] for label in labels if "code" in str(label["label"]).lower()
            }),
            "code_l_label": any("code l" in str(label["label"]).lower() for label in labels),
            "how_b_and_w_are_rows": (
                "Code W is the covered-w family, itemized as wash-sale proceeds, basis, and adjustment, "
                "and posted to Schedule D lines 1b and 8b. Code B is the code-b family, itemized under "
                "labels that say code B, with column (g) the recorded basis correction plus any wash, "
                "and posted to the same lines. Covered sales with no wash and no code B stay on lines "
                "1a and 8a and are not itemized on the attachment."
            ),
            "how_other_codes_are_refused": (
                "The filer must answer that every Form 8949 sale is a broker-reported basis sale with "
                "no adjustment other than a wash-sale loss or a code B basis correction, or a box B, C, "
                "E, or F securities sale with no adjustment other than a wash-sale loss. The fact "
                "no-other-form8949-adjustments is titled as no adjustment code other than W, no "
                "multi-code row, and no basis-not-reported source. A code L row is none of those, so "
                "the honest answer is no, and the return stays refused. There is no code L family."
            ),
            "attachment_rule_v8": {
                "adjustment_kind_enum": kind_enum,
                "adjustment_sign": sign,
                "collect_members_properties": collect_keys,
            },
            "attachment_rule_v11_already_published": {
                "adjustment_kind_enum": v11_kinds,
                "adjustment_sign": v11_sign,
                "enumerate_published_properties": enumerate_keys,
                "note": (
                    "v11 can list published findings of one fact type as single-value rows. "
                    "It does not add a code L kind, a positive adjustment sign, or a per-row filter."
                ),
            },
            "rule_artifact_v15_collect": {
                "properties": sorted(collect["properties"]),
                "additionalProperties": collect["additionalProperties"],
            },
        },
        "questions_touching_box7_or_form_8949": questions,
    }
    out = HERE / "codel-table.json"
    out.write_text(json.dumps(table, indent=2) + "\n", encoding="utf-8")
    adopted = [row["id"] + " " + row["version"] for row in readers if row["adopted_on_v85"]]
    print(f"box7 rules {len(readers)} adopted {len(adopted)}")
    print(f"loader pairs {len(box7_pairs)} refusal tokens {len(box7_tokens)}")
    print(f"attachment parts {len(labels)} code L label {table['form_8949_code_paths']['code_l_label']}")


if __name__ == "__main__":
    main()
