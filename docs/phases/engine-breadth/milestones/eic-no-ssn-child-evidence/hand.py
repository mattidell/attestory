"""Hand credit for the P0 cases, from the published 2025 EIC table.

Worksheet A line 6 is the table lookup. At wages 7000 with no other income,
earned income equals AGI, so the credit is the table value for that amount
in the column ``other-N`` (not married filing jointly). ``N`` is how many
qualifying children have a valid SSN. A null upper bound is the open top band.
The lower bound is inclusive and the upper bound is exclusive.
"""
from __future__ import annotations

import json
from pathlib import Path

P = "tax.us.2025."
WAGES = 7000
HERE = Path(__file__).resolve().parent
TABLE = HERE.parents[4] / "packages/content/tax/2025/parameter.eic-table-2025.v2.json"
KEY = {"0": "other-0", "1": "other-1", "2": "other-2", "3": "other-3"}


def lookup(column: int, amount: int = WAGES) -> int:
    """Table credit for ``amount`` of earned income in the non-joint column ``column``."""
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
    The published fact records both as yes, so both have the same credit.
    A child is a qualifying child only with residency of more than half the
    year and the age test met. The amount column counts only those who also
    have a valid SSN. With no qualifying child, Step 4 question 1 stops a
    married head of household or a married filing separately return.
    """
    status, kids, sep, lived, *rest = key.split("/")
    age_no = rest == ["age-no"]
    separated = sep in ("apart", "writing")

    def one(ssn: bool, more: bool, age: bool = True) -> dict:
        return {"ssn": ssn, "lived_more_than_half": more, "age": age}

    if kids == "ssn":
        roster = [one(True, lived == "more")]
    elif kids == "nossn":
        roster = [one(False, lived == "more", age=not age_no)]
    elif kids == "both":
        roster = [one(True, lived[0] == "m"), one(False, lived[1] == "m")]
    else:
        raise KeyError(key)
    qualifying = [child for child in roster if child["lived_more_than_half"] and child["age"]]
    column = min(3, sum(1 for child in qualifying if child["ssn"]))
    base = {
        "wages": WAGES,
        "column": column,
        "qualifying_children": len(qualifying),
        "separated_prongs_are_one_yes": True,
        "ask_separated": bool(qualifying),
        "ask_not_married": status == "hoh" and not qualifying,
        "ask_age": False,
        "ask_main_home": False,
    }
    if not qualifying:
        credit = 0
        path = "no qualifying child; Step 4 question 1 stops a married filer"
    elif not separated:
        credit = 0
        path = "qualifying child, separated-spouse rule not met"
    else:
        credit = lookup(column)
        path = "qualifying child and separated; column counts only children with a valid SSN"
    return {"credit": credit, "path": path, **base}


if __name__ == "__main__":
    print(json.dumps({"other-0": lookup(0), "other-1": lookup(1), "other-2": lookup(2)}, indent=2))
