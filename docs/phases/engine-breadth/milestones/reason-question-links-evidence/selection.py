"""The adopted student-loan selection reasons that explicitly ask for an answer."""

from __future__ import annotations

P = "tax.us.2025."
ANSWER_TAILS = (
    "no-related-person-interest", "no-qualified-employer-plan-interest",
    "no-non-qualified-loan-component", "no-employer-educational-assistance-interest",
    "no-qtp-earnings-used",
)
STATUS_SHAPES = {
    P + "rule.sli-answer-status-" + tail: (P + "sli.answer-status." + tail, P + "f1098e." + tail)
    for tail in ANSWER_TAILS
}
MARKER = P + "rule.sli-applicability-marker-refusal"
MARKER_RESULT = P + "sli.applicability-marker-refusal"
STANDING_TYPES = {P + "sli.statement-combined-standing", P + "sli.statement-line21-standing"}
STANDING_BUNDLES = {P + "sli-combined-standing", P + "sli-worksheet-inputs"}
ASKING_STANDINGS = {
    "applicability-unestablished", "statement-loan-cannot-tell", "inclusion-cannot-tell",
    "inclusion-withdrawn", "no-loan-link", "financing-cannot-tell", "financing-withdrawn",
    "no-schooling-link", "loan-cost-answer-missing", "loan-cost-cannot-tell",
    "enrollment-answer-missing", "enrollment-cannot-tell",
}


def asking_rule(rule):
    if (rule.get("schema"), rule.get("version")) != ("rule-artifact.v13", "v1"):
        return False
    rule_id = rule.get("id")
    if rule_id == MARKER:
        return rule.get("publishes") == MARKER_RESULT
    shape = STATUS_SHAPES.get(rule_id)
    return bool(shape and rule.get("publishes") == shape[0]
                and rule.get("subject") == {"id": P + "f1098e.box1-student-loan-interest", "version": "v1"}
                and rule.get("joined") == {"id": shape[1], "version": "v1"}
                and rule.get("requires") == [shape[1]])


def asking_values(members):
    found = {}
    for member in members:
        if (member.get("id") not in STANDING_BUNDLES
                or (member.get("schema"), member.get("version")) != ("bundle.v2", "v1")):
            continue
        for fact in member["fact_types"]:
            if fact["id"] not in STANDING_TYPES or fact["version"] != "v1":
                continue
            for row in fact["value_schema"]["oneOf"]:
                if row.get("const") in ASKING_STANDINGS and row.get("description"):
                    found[(fact["id"], row["const"])] = (row["description"], member)
    return found


def published_value_prompt(symbol, value, disposition, finding, act_findings, known):
    """Keep the question only when the result and its publication establish it."""
    if not isinstance(value, str) or (symbol, value) not in known or not finding:
        return False
    fid = disposition.get("finding_id")
    return (
        disposition.get("disposition") == "published"
        and isinstance(fid, str)
        and finding.get("id") == fid
        and finding.get("symbol") == disposition.get("symbol")
        and act_findings.get(fid) == finding
    )


def selection_declarations(members):
    for member in members:
        if asking_rule(member) and member.get("wording"):
            yield member["wording"], member
    yield from asking_values(members).values()
