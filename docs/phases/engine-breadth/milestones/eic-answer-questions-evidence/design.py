"""The prototype's new content: one input question for each earned income credit answer that has none on core v99.

Evidence for docs/phases/engine-breadth/milestones/eic-answer-questions.md (P0).
Charter: docs/reviews/eic-answer-questions/charter-p0.md.

Four ``input-question.v1`` members, each naming one existing fact type of the
published ``tax.us.2025.eic-questions.vocabulary`` v1 bundle by exact pin. No
rule, bundle, schema or page change: every answer rule reads its fact exactly
as on v99, so the same answers are required on the same paths, and the page
already copies a declared question's sentence onto a line that waits on that
fact (``presentation_projection._closure_question_reasons``).

Each question is written from the 2025 Instructions for Form 1040, line 27a
(EIC), and its Definitions and Special Rules; ``SOURCES`` names the lines of a
``pdftotext`` extraction of that PDF (sha256 in p0.md) and of Pub. 596 (2025).
``POLARITY`` says how the filer's yes is recorded: ``pos`` records the fact's
yes; ``abs`` records the fact's no (the scope-answer-questions convention,
"yes = present", used by the published EIC3 question).
"""
from __future__ import annotations

import json
from typing import Any

P = "tax.us.2025."
BUNDLE = {"id": P + "eic-questions.vocabulary", "version": "v1"}

QUESTIONS: dict[str, str] = {
    "age-25-under-65": (
        "Were you, or your spouse if you file a joint return, at least age 25 but under age 65 at the end of 2025? "
        "Answer yes if you, or your spouse if you file a joint return, were born after December 31, 1960, and "
        "before January 2, 2001. If you or your spouse died in 2025, answer yes if the person who died was at "
        "least age 25 but under age 65 at the time of death (a person reaches age 25 on the day before their 25th "
        "birthday, and age 65 on their 65th birthday)."
    ),
    "main-home-in-us": (
        "Was your main home, and your spouse's if you file a joint return, in the United States for more than "
        "half of 2025? Your main home can be any place where you regularly live, such as a house, apartment, "
        "shelter or temporary lodging, and it need not be the same place all year. The United States means the "
        "50 states and the District of Columbia, not Puerto Rico or a U.S. territory. If you were on extended "
        "active military duty outside the United States, count that time as time your main home was in the "
        "United States."
    ),
    "not-claimable-as-dependent": (
        "Can you be claimed as a dependent on someone else's 2025 tax return (do not count the case where the "
        "person who could claim you is not required to file a 2025 return and is not filing one, or is filing "
        "only to claim a refund of withheld income tax or estimated tax paid)?"
    ),
    "spouse-valid-ssn": (
        "Does your spouse's Social Security number allow your spouse to work in the United States? Answer yes if "
        "it was issued by the Social Security Administration on or before the due date of your 2025 return "
        "(including extensions) and is not marked \"Not Valid for Employment\", or if it is marked \"Valid for Work "
        "Only With DHS Authorization\" and that authorization is still valid."
    ),
}

POLARITY = {"age-25-under-65": "pos", "main-home-in-us": "pos", "not-claimable-as-dependent": "abs",
            "spouse-valid-ssn": "pos"}

# Line numbers in the pdftotext extraction of the 2025 i1040gi (i1040gi) and Pub. 596 (p596).
SOURCES: dict[str, list[str]] = {
    "age-25-under-65": ["i1040gi 4531-4543 (line 27a Step 4 question 2)",
                        "p596 1697-1705, 1719-1749 (Rule 11: age test, death of spouse, death of taxpayer)"],
    "main-home-in-us": ["i1040gi 4548-4558 (line 27a Step 4 question 3)",
                        "i1040gi 4795-4798 (Main home), 4802-4808 (Members of the military), 4911-4912 (United States)",
                        "p596 1912-1924 (Rule 14)"],
    "not-claimable-as-dependent": ["i1040gi 4583-4589 (line 27a Step 4 question 6)",
                                   "p596 1751-1759 (Rule 12)"],
    "spouse-valid-ssn": ["i1040gi 4368-4370 and 4259-4262 (line 27a Step 1 question 2, split across columns)",
                         "i1040gi 4876-4889, 4894-4896 (Social security number (SSN))"],
}


def question_id(name: str) -> str:
    return P + "input-question.eic-" + name


def file_name(name: str) -> str:
    return "input-question.eic-" + name + ".v1.json"


def written() -> dict[str, dict[str, Any]]:
    """Every new file, by name."""
    out: dict[str, dict[str, Any]] = {}
    for name, text in QUESTIONS.items():
        out[file_name(name)] = {
            "fact_type": {"id": P + "eic." + name, "version": "v1"},
            "id": question_id(name),
            "question": text,
            "schema": "input-question.v1",
            "version": "v1",
        }
    return out


def dump(body: Any) -> str:
    return json.dumps(body, indent=2, ensure_ascii=False) + "\n"


if __name__ == "__main__":
    for name, body in written().items():
        print(name)
        print(dump(body))
