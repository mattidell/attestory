"""Track 1 content: one input question for each per-member answer of the four rosters that core v100 never asks.

Evidence for docs/phases/engine-breadth/milestones/eic-child-answers.md, Track 1.
Charter: docs/reviews/eic-child-answers/charter-track1.md. ADR 0087.

Twenty-six ``input-question.v1`` members, each naming one existing fact type of
a published roster or tie-breaker bundle by exact pin: the earned income
child's age, residency, joint-return and SSN tests; the ten tie-breaker
answers; the child tax credit's under-17, lived-with-you, support and
citizenship tests; the other-dependent child's TIN; and the seven relative
answers. No rule, bundle, schema or page change: every rule reads its fact as
on v100, so the same answers are required on the same paths. The projection
(ADR 0087) asks a member's missing answer on the lines it blocks, labelled
with the member's recorded name, so each question says "this child" or "this
person".

Each question is written from the 2025 Instructions for Form 1040 (Who
Qualifies as Your Dependent, line 27a and its Definitions and Special Rules)
and the 2025 Instructions for Schedule 8812; the tie-breaker's equal-AGI case
is from Pub. 596 (2025). ``SOURCES`` names the lines of a ``pdftotext -raw``
extraction of each PDF (sha256 in track1.md). ``POLARITY`` says how the
filer's yes is recorded: ``pos`` records the fact's yes; ``abs`` records the
fact's no. A fact stated as the absence of something ("not", "no") is asked
about that thing, "yes = present", as the published v100 questions do
(scope-answer-questions convention).
"""
from __future__ import annotations

import json
from typing import Any

P = "tax.us.2025."

# Fact type -> its published bundle (each a v100 member, pinned v1).
BUNDLES: dict[str, str] = {
    **{P + f"eic.child.{n}": P + "eic-child-roster.vocabulary" for n in ("age", "residency", "joint-return", "ssn")},
    **{P + f"dtb.child.{n}": P + "dtb-questions" for n in (
        "another-could-claim", "multiple-other-claimants", "filer-is-parent", "other-is-parent",
        "form-8332-released", "more-nights-with-filer", "same-nights", "filer-agi-higher", "same-agi",
        "other-will-claim")},
    **{P + f"ctc.child.{n}": P + "ctc-child-roster.vocabulary" for n in (
        "under-17", "lived-with-you", "no-over-half-support", "citizen-or-resident")},
    P + "odc.child.tin": P + "odc-child-roster.vocabulary",
    **{P + f"odc.dependent.{n}": P + "odc-relative-roster.vocabulary" for n in (
        "relationship", "not-qualifying-child", "gross-income-under-limit", "over-half-support", "tin",
        "citizen-or-resident", "not-joint-return")},
}

_KIDNAPPED = (
    " A kidnapped child is treated as living with you for more than half of the year if the child lived with you "
    "for more than half the part of the year before the date of the kidnapping or following the date of the "
    "child's return. The child must be presumed by law enforcement authorities to have been kidnapped by someone "
    "who isn't a member of your family or the child's family. This treatment applies for all years until the "
    "child is returned, but the last year it can apply is the earlier of the year there is a determination that "
    "the child is dead or the year the child would have reached age 18."
)
_TIME_LIVED = (
    "Count temporary absences for special circumstances, such as school, vacation, business, medical care, "
    "military service, or detention in a juvenile facility, as time the child lived with you. A child who was born"
    " or died in 2025 lived with you for more than half of 2025 if your home was the child's home for more than "
    "half the time the child was alive in 2025. A child you adopted in 2025, who was lawfully placed with you for"
    " legal adoption in 2025, or who was an eligible foster child placed with you during 2025, lived with you for"
    " more than half of 2025 if your main home was the child's main home for more than half the time since the "
    "adoption or placement." + _KIDNAPPED
)
_CITIZEN_EXCEPTION = (
    "Also answer yes if {who} is your adopted child, lived with you all year as a member of your household, and you"
    " are a U.S. citizen or U.S. national."
)
_TIN = (
    "Does {who} have a social security number (SSN), individual taxpayer identification number (ITIN), or "
    "adoption taxpayer identification number (ATIN) issued on or before the due date of your 2025 return "
    "(including extensions)? Answer yes if {they} {has} one, or if you apply for an ITIN or ATIN for {them} on or"
    " before that date. Answer no if {they} {has} none of these numbers."
)
_PARENT = ("For this question, a parent is a biological or adoptive parent; a stepparent or foster parent who has "
           "not adopted the child is not a parent.")

QUESTIONS: dict[str, str] = {
    # Earned income credit, line 27a Step 3 (qualifying child).
    P + "eic.child.age": (
        "Does this child meet the age test for the earned income credit? Answer yes if, at the end of 2025, the "
        "child was under age 19 and younger than you (or your spouse if you file a joint return); or was under "
        "age 24, a full-time student, and younger than you (or your spouse if you file a joint return); or was "
        "any age and permanently and totally disabled. A full-time student is a child who during any part of 5 "
        "calendar months of 2025 was enrolled as a full-time student at a school or took a full-time, on-farm "
        "training course given by a school or a state, county, or local government agency. A school includes a "
        "technical, trade, or mechanical school. It doesn't include an on-the-job training course, correspondence "
        "school, or school offering courses only through the Internet. A person is "
        "permanently and totally disabled if, at any time in 2025, the person couldn't engage in any substantial "
        "gainful activity because of a physical or mental condition and a doctor has determined that this "
        "condition has lasted or can be expected to last continuously for at least a year, or can be expected to "
        "lead to death. Answer no if none of these applies."
    ),
    P + "eic.child.residency": (
        "Did this child live with you in the United States for more than half of 2025? " + _TIME_LIVED + " If you"
        " were on extended active military duty outside the United States (duty ordered for an indefinite period"
        " or for more than 90 days), your main home is considered to be in the United States during that duty. "
        "Once you begin serving extended active duty, you are considered to be on extended active duty even if you"
        " don't serve more than 90 days. "
        "The United States means the 50 states and the District of Columbia, not Puerto Rico or a U.S. territory."
        " Answer yes if the child lived with you in the United States for more than half of 2025. Answer no if "
        "not, even if you paid most of the child's living expenses."
    ),
    P + "eic.child.joint-return": (
        "Does this child meet the joint return test? Answer yes if the child did not file a joint return for "
        "2025, or filed one only to claim a refund of withheld income tax or estimated "
        "tax paid, and, if the child was married at the end of 2025, you can claim the child as your dependent "
        "(or could, except for the special rule for children of divorced or separated parents). Answer no "
        "otherwise."
    ),
    P + "eic.child.ssn": (
        "Does this child have a social security number (SSN) issued by the Social Security Administration on or "
        "before the due date of your 2025 return (including extensions) that is valid for employment? Answer yes"
        " if so. A number with \"Not Valid for Employment\" printed on the card, issued solely to apply for or "
        "receive a federally funded benefit, does not count; a number with \"Valid for Work Only With DHS "
        "Authorization\" counts only while that authorization is still valid. Answer no if the child had no such"
        " number by that date; an ITIN or ATIN is not an SSN."
    ),
    # Qualifying child of more than one person (tie-breaker rules).
    P + "dtb.child.another-could-claim": (
        "Does this child also meet the conditions to be a qualifying child of any other person for 2025, other "
        "than your spouse if you file a joint return? Answer yes if another person could also claim the child as"
        " a qualifying child. Answer no if no other person could."
    ),
    P + "dtb.child.multiple-other-claimants": (
        "Does this child meet the conditions to be a qualifying child of more than one other person for 2025, "
        "not counting your spouse if you file a joint return? Answer yes if two or more other people could also "
        "claim the child as a qualifying child. Answer no if only one other person could."
    ),
    P + "dtb.child.filer-is-parent": (
        "Are you, or your spouse if you file a joint return, this child's parent? " + _PARENT + " Answer yes if "
        "you or your spouse is the child's parent. Answer no if not."
    ),
    P + "dtb.child.other-is-parent": (
        "Is the other person who could claim this child the child's parent? " + _PARENT + " Answer yes if the "
        "other person is the child's parent. Answer no if not."
    ),
    P + "dtb.child.form-8332-released": (
        "Does the special rule for children of divorced or separated parents apply to this child for 2025 "
        "through a release of the claim to the child: the custodial parent signs Form 8332 or a substantially "
        "similar statement that they won't claim the child as a dependent for 2025 (or, for a decree or "
        "agreement that went into effect after 1984 and before 2009, certain pages from it), or a pre-1985 "
        "decree of divorce or separate maintenance or written separation agreement provides that the "
        "noncustodial parent can claim the child and the noncustodial parent provides at least $600 for the "
        "child's support during 2025? Answer yes if such a release applies. Answer no if none does."
    ),
    P + "dtb.child.more-nights-with-filer": (
        "Did this child live with you for more nights in 2025 than with the other parent? Answer yes if the "
        "child lived with you for the greater number of nights. Answer no if not."
    ),
    P + "dtb.child.same-nights": (
        "Did this child live with you and with the other parent for the same number of nights in 2025? Answer "
        "yes if the number of nights was equal. Answer no if the child lived with the other parent for more "
        "nights."
    ),
    P + "dtb.child.filer-agi-higher": (
        "Was your adjusted gross income (AGI) for 2025 higher than the other person's AGI for 2025? Answer yes "
        "if your AGI was higher. Answer no if it was the same or lower."
    ),
    P + "dtb.child.same-agi": (
        "Was your adjusted gross income (AGI) for 2025 the same as the other person's AGI for 2025? Answer yes "
        "if the two were equal. Answer no if yours was lower."
    ),
    P + "dtb.child.other-will-claim": (
        "Will the other person claim this child as a qualifying child on their 2025 tax return? Answer yes if "
        "they will claim the child, or if you do not know. Answer no if they will not."
    ),
    # Child tax credit, Who Qualifies as Your Dependent Steps 1 and 3, and Schedule 8812.
    P + "ctc.child.under-17": (
        "Was this child under age 17 at the end of 2025? Answer yes if so. Answer no if the child was age 17 or "
        "older at the end of 2025."
    ),
    P + "ctc.child.lived-with-you": (
        "Did this child live with you for more than half of 2025? " + _TIME_LIVED + " Answer yes if the child "
        "lived with you for more than half of 2025. Answer no if not."
    ),
    P + "ctc.child.no-over-half-support": (
        "Did this child provide over half of their own support for 2025? Answer yes if the child did. Answer no "
        "if the child did not."
    ),
    P + "ctc.child.citizen-or-resident": (
        "Was this child a U.S. citizen, U.S. national, or U.S. resident alien? Answer yes if so. "
        + _CITIZEN_EXCEPTION.format(who="the child") + " Answer no otherwise, including if the child was only a "
        "resident of Canada or Mexico."
    ),
    # Credit for other dependents: a child who is not counted for the child tax credit.
    P + "odc.child.tin": _TIN.format(who="this child", they="the child", has="has", them="the child"),
    # Credit for other dependents: a qualifying relative, Who Qualifies as Your Dependent Steps 4 and 5.
    P + "odc.dependent.relationship": (
        "Is this person your son, daughter, stepchild, foster child, or a descendant of any of them; your brother,"
        " sister, half brother, half sister, or a son or daughter of any of them; your father, mother, or an "
        "ancestor or sibling of either of them; or your stepbrother, stepsister, stepfather, stepmother, "
        "son-in-law, daughter-in-law, father-in-law, mother-in-law, brother-in-law, or sister-in-law? Answer yes "
        "if so. Also answer yes if this person, other than your spouse, lived with you all year as a member of "
        "your household and your relationship didn't violate local law. Answer no otherwise."
    ),
    P + "odc.dependent.not-qualifying-child": (
        "Was this person a qualifying child of any taxpayer for 2025? For this question, a person isn't a "
        "taxpayer if the person isn't required to file a U.S. income tax return and either doesn't file one or "
        "files only to get a refund of withheld income tax or estimated tax paid. Answer yes if this person was "
        "a qualifying child of any taxpayer. Answer no if not."
    ),
    P + "odc.dependent.gross-income-under-limit": (
        "Did this person have gross income of less than $5,200 in 2025? Answer yes if so. Answer no if it was "
        "$5,200 or more, even if the person was permanently and totally disabled."
    ),
    P + "odc.dependent.over-half-support": (
        "Did you provide over half of this person's support in 2025? Answer yes if you did. Answer no if you did"
        " not, including where you would be treated as providing it only under a multiple support agreement. If "
        "this person is your child who is presumed by law enforcement authorities to have been kidnapped by someone"
        " who isn't a family member, you may be able to take the child into account for the credit for other "
        "dependents."
    ),
    P + "odc.dependent.tin": _TIN.format(who="this person", they="they", has="have", them="them"),
    P + "odc.dependent.citizen-or-resident": (
        "Was this person a U.S. citizen, U.S. national, or U.S. resident alien? Answer yes if so. "
        + _CITIZEN_EXCEPTION.format(who="the person") + " Answer no otherwise, including if the person was only a"
        " resident of Canada or Mexico."
    ),
    P + "odc.dependent.not-joint-return": (
        "Did this person file a joint return for 2025, other than one filed only to claim a refund of withheld "
        "income tax or estimated tax paid? Answer yes if so. Answer no if the person did not file a joint return,"
        " including if the person was married and filed separately, or filed one only to claim such a refund."
    ),
}

POLARITY: dict[str, str] = {fact: "pos" for fact in QUESTIONS}
POLARITY.update({P + "ctc.child.no-over-half-support": "abs", P + "odc.dependent.not-qualifying-child": "abs",
                 P + "odc.dependent.not-joint-return": "abs"})

# Line numbers in the pdftotext -raw extractions: i1040gi (2025 Form 1040 instructions), i1040s8 (2025
# Schedule 8812 instructions), p596 (Pub. 596, 2025).
_DTB = "i1040gi 1943-1976 and 4828-4864 (Qualifying child of more than one person)"
SOURCES: dict[str, list[str]] = {
    P + "eic.child.age": ["i1040gi 4424-4436 (line 27a Step 3, qualifying child: age)",
                          "i1040gi 4788-4794 (Full-time student; school does not include on-the-job training, correspondence or "
                          "Internet-only schools), 4813-4817 (Permanently and totally disabled)"],
    P + "eic.child.residency": ["i1040gi 4444-4449, 4453-4454 (line 27a Step 3: lived with you in the United States)",
                                "i1040gi 4753-4763 (Exception to time lived with you), 4802-4808 (Members of the "
                                "military: extended active duty counts once begun), 4911-4912 (United States)",
                                "i1040gi 4462-4464 and p596 1241-1254 (Kidnapped child)"],
    P + "eic.child.joint-return": ["i1040gi 4439-4441 (line 27a Step 3: joint return)",
                                   "i1040gi 4799-4801 (Married child)"],
    P + "eic.child.ssn": ["i1040gi 4876-4889, 4894-4898 (Social security number (SSN))",
                          "i1040s8 50-51 (TIN types), 70-82 (Valid SSN; qualifying child required to have an SSN)"],
    P + "dtb.child.another-could-claim": ["i1040gi 1499-1501, 4468-4470 (another person's qualifying child)", _DTB],
    P + "dtb.child.multiple-other-claimants": [_DTB, "p596 1343-1368 (Rule 9)"],
    P + "dtb.child.filer-is-parent": [_DTB + "; 1959 and 4847 (parent)"],
    P + "dtb.child.other-is-parent": [_DTB + "; 1959 and 4847 (parent)"],
    P + "dtb.child.form-8332-released": ["i1040gi 1800-1823 (Children of divorced or separated parents)",
                                         "i1040gi 1859-1866 (Post-2008 decree or agreement)"],
    P + "dtb.child.more-nights-with-filer": ["i1040gi 1832-1835 (Custodial and noncustodial parents)",
                                             "i1040gi 1965-1967 (lived with the parent for the longer period)"],
    P + "dtb.child.same-nights": ["i1040gi 1834-1837 (equal number of nights)",
                                  "i1040gi 1967-1969 (same amount of time: the higher AGI)"],
    P + "dtb.child.filer-agi-higher": ["i1040gi 1967-1976 (the higher or highest AGI)"],
    P + "dtb.child.same-agi": ["i1040gi 1967-1976 (the higher or highest AGI)", "p596 1384-1405 (tiebreaker rules)"],
    P + "dtb.child.other-will-claim": ["i1040gi 1973-1976 (a parent can claim but no parent does so claim)",
                                       "p596 1399-1405, 1417-1419 (you and the other person may choose who claims)"],
    P + "ctc.child.under-17": ["i1040gi 1586 (Step 3 question 3)", "i1040s8 140-150 (Credits for Qualifying Children)"],
    P + "ctc.child.lived-with-you": ["i1040gi 1492-1495 (Step 1: lived with you)",
                                     "i1040gi 1881-1896 (Exception to time lived with you)",
                                     "i1040gi 1916-1920 and p596 1241-1254 (Kidnapped child)"],
    P + "ctc.child.no-over-half-support": ["i1040gi 1482 (Step 1: didn't provide over half of their own support)"],
    P + "ctc.child.citizen-or-resident": ["i1040gi 1573-1576 (Step 3 question 2)",
                                          "i1040gi 1871-1873 (Exception to citizen test)",
                                          "i1040gi 1519-1522 (Step 2 question 1: Canada or Mexico)"],
    P + "odc.child.tin": ["i1040gi 1618-1622 (Step 3 question 1)",
                          "i1040s8 97-107 (Dependent required to have a TIN)"],
    P + "odc.dependent.relationship": ["i1040gi 1640-1657 (Step 4: a qualifying relative is your...)"],
    P + "odc.dependent.not-qualifying-child": ["i1040gi 1661-1664 (Step 4: who wasn't a qualifying child)"],
    P + "odc.dependent.gross-income-under-limit": ["i1040gi 1668-1669 (Step 4: gross income)",
                                                   "i1040gi 1874-1877 (Exception to gross income test)"],
    P + "odc.dependent.over-half-support": ["i1040gi 1673-1675 (Step 4: support)",
                                            "i1040gi 1925-1933 (Multiple support agreements)",
                                            "i1040gi 1673-1675 and 1916-1920 (Kidnapped child)"],
    P + "odc.dependent.tin": ["i1040gi 1734-1738 (Step 5 question 2)",
                              "i1040s8 97-107 (Dependent required to have a TIN)"],
    P + "odc.dependent.citizen-or-resident": ["i1040gi 1763-1774 (Step 5 question 3)",
                                              "i1040gi 1871-1873 (Exception to citizen test)",
                                              "i1040s8 170-172, 186-193 (ODC condition 3; Adopted child)"],
    P + "odc.dependent.not-joint-return": ["i1040gi 1752-1756 (Step 4 question 3: was your qualifying relative married)",
                                           "i1040gi 1921-1924 (Married person)"],
}


def question_id(fact: str) -> str:
    return P + "input-question." + fact.removeprefix(P).replace(".", "-")


def file_name(fact: str) -> str:
    return "input-question." + fact.removeprefix(P).replace(".", "-") + ".v1.json"


def written() -> dict[str, dict[str, Any]]:
    assert set(QUESTIONS) == set(BUNDLES) == set(POLARITY) == set(SOURCES)
    return {file_name(fact): {"fact_type": {"id": fact, "version": "v1"}, "id": question_id(fact),
                              "question": QUESTIONS[fact], "schema": "input-question.v1", "version": "v1"}
            for fact in sorted(QUESTIONS)}


def dump(body: Any) -> str:
    return json.dumps(body, indent=2, ensure_ascii=False) + "\n"


if __name__ == "__main__":
    for name, body in written().items():
        print(name, POLARITY[body["fact_type"]["id"]])
        print("  " + body["question"])
