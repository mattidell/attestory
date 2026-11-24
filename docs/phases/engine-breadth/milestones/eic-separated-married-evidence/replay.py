"""Full-surface replay of the 775 recorded lists: published v102 against the scratch v103.

Run: python3 replay.py <scratch-core.json> --part <part> --out <summary>
     python3 replay.py <scratch-core.json> --limit 1 --out <summary>

Declared expectations are the package pin v102 to v103, the two new disposition
rows and their order, the disposition nodes those rules add, the separated-spouse
rule pin v2 to v3, and that rule's missing list naming the new answer symbol.
A recorded list that newly blocks, or that changes a number, is not expected.
Nothing in packages/ or tests/ is edited.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from tools import recorded_replay as rr  # noqa: E402

P = "tax.us.2025."


def expectations() -> list[rr.Expectation]:
    """Differences the 775 single filers show. No number change is declared.

    The package pin moves from v102 to v103. The two new rules add a disposition
    row, and on a return that never publishes eic.questions-required those rows
    are blocked on that absence. Disposition order gains the two rules. The
    separated-spouse rule's pin moves to v3 where the explanation graph carries
    it, and its missing list also names the new answer symbol. A return that
    changes outcome, or that changes a number, is not expected.
    """
    recorded_rule = P + "rule.eic-married-taxpayer-recorded"
    answer_rule = P + "rule.eic-answer.married-taxpayer"
    separated_rule = P + "rule.eic-answer.separated-spouse"
    answer_symbol = P + "eic.answer.married-taxpayer"
    separated_symbol = P + "eic.answer.separated-spouse"
    questions = P + "eic.questions-required"
    separated_children = (
        P + "eic.column-count",
        P + "eic.qualifying-child-present",
        questions,
        P + "eic.status-class",
    )
    rules = (recorded_rule, answer_rule)
    return [
        rr.version_change(P + "package.core-calculations", "v102", "v103", "scratch core is v103"),
        rr.version_change(separated_rule, "v2", "v3", "separated-spouse rule pin moves to v3"),
        rr.Expectation(("row",), r".+", "|".join(re.escape(rule) for rule in rules), "added",
                       note="the two new rules publish a disposition"),
        rr.Expectation(("row",), r"dispositions@order", change="changed",
                       note="disposition order gains the two new rules"),
        rr.Expectation(
            ("model",),
            r"dispositionNodes\.tax\.us\.2025\.eic\.(?:married-taxpayer-recorded|answer\.married-taxpayer)\.(?:children|records@order|symbol)",
            change="added",
            note="the two new symbols add a disposition node",
        ),
        rr.Expectation(("model",), r".+", "|".join(re.escape(rule) for rule in rules), "added",
                       note="fields of the two new disposition records"),
        rr.Expectation(
            ("model",),
            re.escape("dispositionNodes." + separated_symbol + ".children"),
            change="changed",
            before=list(separated_children),
            after=[answer_symbol, *separated_children],
            note="separated-spouse node lists the new answer symbol",
        ),
        rr.Expectation(
            ("model", "row"),
            r"missing",
            re.escape(separated_rule),
            "changed",
            [questions],
            [questions, answer_symbol],
            note="separated-spouse missing list also names the new answer symbol",
        ),
    ]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("core_json")
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--workers", type=int, default=6)
    parser.add_argument("--part", type=Path)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    lists = rr.recorded_lists()
    if args.limit:
        lists = lists[: args.limit]
    summary = rr.run_full("v102", args.core_json, expectations(), workers=args.workers, part=args.part, out=args.out, lists=lists)
    brief = {
        "lists": summary["lists"],
        "classes": summary["classes"],
        "passing": summary["passing"],
        "failing": summary["failing"],
        "outcomes": summary["outcomes"],
        "expectations_declared": summary["expectations_declared"],
        "expectations_used": summary["expectations_used"],
        "unused_notes": [row.get("note") for row in summary["unused_expectations"]],
        "unexpected_kinds": sorted(summary["unexpected_by_kind_attribute"]),
        "failing_lists": len(summary["failing_lists"]),
    }
    print(json.dumps(brief, indent=2))


if __name__ == "__main__":
    main()
