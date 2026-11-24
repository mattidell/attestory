"""Hand credit for the separated-spouse P0 cases, from the published 2025 EIC table.

Worksheet A line 6 is the table lookup. At wages 7000 with no other income,
earned income equals AGI, so the credit is the table value for that amount
in the column ``other-N`` (not married filing jointly). ``N`` is how many
qualifying children have a valid SSN. A null upper bound is the open top band.
The lower bound is inclusive and the upper bound is exclusive.

The credit is what the 2025 Form 1040 instructions give, not what published
core v102 computes. Step 3 question 3 asks questions 4 and 5 only of a married
taxpayer whose filing status is married filing separately or head of household.
An unmarried head of household skips those questions and keeps the table
credit. A married head of household or a married filing separately return
with a qualifying child needs one separated-spouse prong. With no qualifying
child, Step 4 question 1 stops a married filer, and an unmarried head of
household who answers the remaining Step 4 questions yes takes the no-child
column.
"""
from __future__ import annotations

import json
from pathlib import Path

WAGES = 7000
HERE = Path(__file__).resolve().parent
TABLE = HERE.parents[4] / "packages/content/tax/2025/parameter.eic-table-2025.v2.json"
KEY = {"0": "other-0", "1": "other-1", "2": "other-2", "3": "other-3"}


def lookup(column: int, amount: int = WAGES) -> int:
    """Table credit for ``amount`` of earned income in the non-joint column."""
    bands = json.loads(TABLE.read_text(encoding="utf-8"))["values"][KEY[str(column)]]
    for row in bands:
        lower = int(row["lower"])
        upper = None if row["upper"] is None else int(row["upper"])
        if amount >= lower and (upper is None or amount < upper):
            return int(row["value"])
    raise KeyError(f"no {KEY[str(column)]} band contains {amount}")


def decide(key: str) -> dict:
    """What the 2025 instructions give this synthetic case. Wages are 7000.

    ``apart`` and ``writing`` are the two statutory separated-spouse prongs.
    The published fact records both as yes. A child with a valid SSN is column
    1. A qualifying child with no valid SSN is still a qualifying child and
    takes column 0. ``none`` is no qualifying child.
    """
    status, kids, *rest = key.split("/")
    sep = rest[0] if rest else None
    assert not rest or rest == [sep]
    separated = sep in ("apart", "writing")
    qualifying = kids in ("ssn", "nossn")
    column = 1 if kids == "ssn" else 0
    married = status in ("hoh-married", "mfs")
    ask_separated = qualifying and married
    ask_not_married = status in ("hoh-married", "hoh-unmarried") and not qualifying
    if not qualifying:
        if married:
            credit = 0
            path = (
                "no qualifying child; Step 4 question 1 stops a married taxpayer "
                "filing as head of household or married filing separately"
            )
        else:
            credit = lookup(0)
            path = "no qualifying child; an unmarried head of household who answers the remaining Step 4 questions yes"
    elif not married:
        credit = lookup(column)
        path = "unmarried head of household; Step 3 question 3 is no, so questions 4 and 5 are skipped"
    elif not separated:
        credit = 0
        path = "qualifying child, and neither separated-spouse prong is met"
    else:
        credit = lookup(column)
        path = "qualifying child and one separated-spouse prong; the column counts only a child with a valid SSN"
    return {
        "credit": credit,
        "path": path,
        "wages": WAGES,
        "column": column if qualifying or not married else 0,
        "table_key": "other-" + str(column if qualifying or credit else 0),
        "qualifying_child": qualifying,
        "married_for_step3_question3": married,
        "ask_separated": ask_separated,
        "ask_not_married": ask_not_married,
        "separated_prongs_are_one_yes": True,
    }


def expect(key: str) -> dict:
    """What the P0b successor should do, and the credit the instructions give.

    The 21 P0 keys still carry a separated-spouse answer and no new answer.
    A recorded no publishes 0. A recorded yes publishes 1. The new question
    is not read. ``q3-no`` answers the new question no and records no
    separated-spouse answer. ``q3-yes`` answers yes and leaves questions 4
    and 5 unanswered, so the run blocks. ``q3-yes-no`` answers yes and then
    separated-spouse no.
    """
    if key.startswith("q3-"):
        kind, kids = key.split("/")
        column = 1 if kids == "ssn" else 0
        table = lookup(column)
        base = {
            "wages": WAGES,
            "column": column,
            "table_key": "other-" + str(column),
            "qualifying_child": True,
            "ask_not_married": False,
            "instruction": table,
        }
        if kind == "q3-no":
            return {**base, "credit": table, "ask_separated": False, "ask_married": True, "blocked": False,
                    "path": "unmarried head of household; Step 3 question 3 is no, so questions 4 and 5 are skipped"}
        if kind == "q3-yes":
            return {**base, "credit": None, "ask_separated": False, "ask_married": True, "blocked": True,
                    "instruction": None,
                    "path": "married head of household; questions 4 and 5 are required and unanswered"}
        if kind == "q3-yes-no":
            return {**base, "credit": 0, "ask_separated": True, "ask_married": False, "blocked": False,
                    "instruction": 0,
                    "path": "married head of household; a recorded separated-spouse no stops the credit"}
        raise KeyError(key)
    source = decide(key)
    status, kids, *rest = key.split("/")
    sep = rest[0] if rest else None
    qualifying = kids in ("ssn", "nossn")
    credit = source["credit"]
    path = source["path"]
    if status == "hoh-unmarried" and qualifying and sep == "no":
        credit = 0
        path = "a recorded separated-spouse no still publishes 0; the new question is not read"
    return {
        "credit": credit,
        "instruction": source["credit"],
        "path": path,
        "wages": WAGES,
        "ask_separated": qualifying,
        "ask_married": False,
        "ask_not_married": source["ask_not_married"],
        "blocked": False,
    }


if __name__ == "__main__":
    print(json.dumps({"other-0": lookup(0), "other-1": lookup(1)}, indent=2))
