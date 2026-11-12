"""The 2025 law this milestone quotes, checked against the irs.gov files.

Evidence for docs/phases/engine-breadth/milestones/age-blindness-asked.md.
Charter: docs/reviews/age-blindness-asked/charter-p0.md.

Fetches each source from irs.gov pub/irs-prior into a directory outside the
repository, checks its sha256 (the two question-wording already recorded must
match question-wording-evidence/law.json), extracts it with
``pdftotext -layout``, and checks that every key phrase of every quote
occurs inside the quote's line range. The extract keeps the page's columns,
so a range can hold text from a neighbouring column and a phrase can be
broken across lines; phrases are matched on the range's words joined with
single spaces and with end-of-line hyphens removed. Writes law.json.

    python3 law.py <download-directory-outside-the-repo>
"""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
import urllib.request
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
QW_LAW = REPO / "docs/phases/engine-breadth/milestones/question-wording-evidence/law.json"
BASE = "https://www.irs.gov/pub/irs-prior/"

SOURCES = {
    "i1040gi--2025.pdf": "2025 Instructions for Form 1040",
    "f1040--2025.pdf": "2025 Form 1040",
    "p501--2025.pdf": "Publication 501 (2025), Dependents, Standard Deduction, and Filing Information",
}

# Each quote: id, source file, line range of the -layout extract, the text
# (the instruction's sentences in order, columns untangled by hand), the key
# phrases checked mechanically, and whether question-wording law.json already
# carries it (same id and range).
QUOTES: list[dict[str, Any]] = [
    {
        "id": "form1040-line12d",
        "file": "f1040--2025.pdf", "lines": [87, 92],
        "location": "Form 1040 (2025), page 1, lines 12a and 12d",
        "text": "12a Someone can claim: You as a dependent; Your spouse as a dependent. d You: Were born before January 2, 1961; Are blind. Spouse: Was born before January 2, 1961; Is blind.",
        "phrases": ["Someone can claim", "You as a dependent", "Your spouse as a dependent",
                    "Were born before January 2, 1961", "Are blind", "Was born before January 2, 1961", "Is blind"],
    },
    {
        "id": "age-65",
        "file": "i1040gi--2025.pdf", "lines": [2183, 2195], "reused": True,
        "location": "Instructions for Form 1040, Line 12d",
        "text": "If you or your spouse (if you are married and filing a joint return) were born before January 2, 1961, or were blind at the end of 2025, check the appropriate box(es) on line 12d. Don't check any boxes for your spouse if your filing status is head of household.",
        "phrases": ["If you or your spouse (if you are married", "and filing a joint return) were born be", "fore January 2, 1961, or were blind at",
                    "the end of 2025, check the appropriate", "Don’t check any boxes for your", "spouse if your filing status is head of"],
    },
    {
        "id": "separate-return-spouse",
        "file": "i1040gi--2025.pdf", "lines": [2117, 2127],
        "location": "Instructions for Form 1040, Line 12d (continued)",
        "text": "If your filing status is married filing separately and your spouse was born before January 2, 1961, or was blind at the end of 2025, you can check the appropriate box(es) on line 12d if your spouse had no income, isn't filing a return, and can't be claimed as a dependent on another person's return.",
        "phrases": ["If your filing status is married filing", "separately and your spouse was born be", "fore January 2, 1961, or was blind at the",
                    "priate box(es) on line 12d if your spouse", "had no income, isn’t filing a return, and", "can’t be claimed as a dependent on an", "other person’s return."],
    },
    {
        "id": "death-2025",
        "file": "i1040gi--2025.pdf", "lines": [2128, 2151], "reused": True,
        "location": "Instructions for Form 1040, Line 12d, Death of spouse in 2025",
        "text": "Death of spouse in 2025. If your spouse was born before January 2, 1961, but died in 2025 before reaching age 65, don't check the box that says \"Spouse was born before January 2, 1961.\" A person is considered to reach age 65 on the day before the person's 65th birthday. Example. Your spouse was born on February 14, 1960, and died on February 13, 2025. Your spouse is considered age 65 at the time of death. Check the appropriate box for your spouse. However, if your spouse died on February 12, 2025, your spouse isn't considered age 65. Don't check the box.",
        "phrases": ["Death of spouse in 2025. If your", "but died in 2025 before reaching age 65,", "65 on the day before the person’s 65th",
                    "February 14, 1960, and died on February", "13, 2025. Your spouse is considered age", "your spouse died on February 12, 2025,", "your spouse isn’t considered age 65."],
    },
    {
        "id": "death-of-taxpayer-pointer",
        "file": "i1040gi--2025.pdf", "lines": [2152, 2157],
        "location": "Instructions for Form 1040, Line 12d, Death of taxpayer in 2025",
        "text": "Death of taxpayer in 2025. If you are preparing a return for someone who died in 2025, see Pub. 501 before completing the standard deduction information.",
        "phrases": ["Death of taxpayer in 2025. If you are", "preparing a return for someone who died", "in 2025, see Pub. 501 before completing", "the standard deduction information."],
    },
    {
        "id": "blindness",
        "file": "i1040gi--2025.pdf", "lines": [2158, 2179], "reused": True,
        "location": "Instructions for Form 1040, Line 12d, Blindness",
        "text": "If you weren't totally blind as of December 31, 2025, you must get a statement certified by your eye doctor (ophthalmologist or optometrist) that: You can't see better than 20/200 in your better eye with glasses or contact lenses, or Your field of vision is 20 degrees or less. If your eye condition isn't likely to improve beyond the conditions listed above, you can get a statement certified by your eye doctor (ophthalmologist or optometrist) to this effect instead. You must keep the statement for your records.",
        "phrases": ["If you weren’t totally blind as of Decem", "certified by your eye doctor (ophthal", "You can't see better than 20/200 in",
                    "your better eye with glasses or contact", "Your field of vision is 20 degrees"],
    },
    {
        "id": "line12e-exceptions",
        "file": "i1040gi--2025.pdf", "lines": [2240, 2284],
        "location": "Instructions for Form 1040, Line 12e, Standard Deduction, Exceptions 1 and 4",
        "text": "Exception 1—Dependent. Line 12a. If you checked a box on line 12a, use the Standard Deduction Worksheet for Dependents to figure your standard deduction. ... Exception 4—Born before January 2, 1961, or blind. Line 12d. If you checked any box on line 12d, figure your standard deduction by using the Standard Deduction Chart for People Who Were Born Before January 2, 1961, or Were Blind if you are filing Form 1040 or by using the chart on the last page of Form 1040-SR.",
        "phrases": ["Exception 1—Dependent. Line 12a. If", "Standard Deduction Worksheet for De", "Exception 4—Born before January 2,",
                    "1961, or blind. Line 12d. If you", "checked any box on line 12d, figure", "Standard Deduction Chart for People"],
    },
    {
        "id": "dependents-worksheet",
        "file": "i1040gi--2025.pdf", "lines": [2288, 2313],
        "location": "Instructions for Form 1040, Standard Deduction Worksheet for Dependents—Line 12e",
        "text": "Use this worksheet only if someone can claim you, or your spouse if filing jointly, as a dependent. 1. Check if: You were born before January 2, 1961. You are blind. Spouse was born before January 2, 1961. Spouse is blind. Total number of boxes checked. 2. Is your earned income more than $900? Yes. Add $450 to your earned income. Enter the total. No. Enter $1,350. 3. Enter the amount shown below for your filing status. Single or married filing separately—$15,750. Married filing jointly—$31,500. Head of household—$23,625. 4. a. Enter the smaller of line 2 or line 3. If born after January 1, 1961, and not blind, stop here and enter this amount on Form 1040 or 1040-SR, line 12e. Otherwise, go to line 4b. b. If born before January 2, 1961, or blind, multiply the number on line 1 by $1,600 ($2,000 if single or head of household). c. Add lines 4a and 4b. Enter the total here and on Form 1040 or 1040-SR, line 12e.",
        "phrases": ["Use this worksheet only if someone can claim you, or your spouse if filing jointly, as a dependent.",
                    "You were born before January 2, 1961.", "Spouse was born before January 2, 1961.", "Add $450 to your earned income.",
                    "Single or married filing separately—$15,750", "Married filing jointly—$31,500", "Head of household—$23,625",
                    "If born after January 1, 1961, and not blind, stop here", "multiply the number on line 1 by $1,600 ($2,000 if single or head of"],
    },
    {
        "id": "chart",
        "file": "i1040gi--2025.pdf", "lines": [2319, 2350],
        "location": "Instructions for Form 1040, Standard Deduction Chart for People Who Were Born Before January 2, 1961, or Were Blind",
        "text": "Don't use this chart if someone can claim you, or your spouse if filing jointly, as a dependent. Instead, use the worksheet above. [Boxes: You were born before January 2, 1961; You are blind; Spouse was born before January 2, 1961; Spouse is blind.] Single: 1 $17,750, 2 19,750. Married filing jointly: 1 $33,100, 2 34,700, 3 36,300, 4 37,900. Qualifying surviving spouse: 1 $33,100, 2 34,700. Married filing separately*: 1 $17,350, 2 18,950, 3 20,550, 4 22,150. Head of household: 1 $25,625, 2 27,625. * You can check the boxes for spouse if your filing status is married filing separately and your spouse had no income, isn't filing a return, and can't be claimed as a dependent on another person's return.",
        "phrases": ["Don’t use this chart if someone can claim you, or your spouse if filing jointly, as a dependent.",
                    "$17,750", "19,750", "$33,100", "34,700", "36,300", "37,900", "Qualifying surviving spouse",
                    "$17,350", "18,950", "20,550", "22,150", "$25,625", "27,625",
                    "You can check the boxes for spouse if your filing status is married filing separately and your spouse had no income, isn’t filing a return, and can’t be claimed as a"],
    },
    {
        "id": "senior-deduction",
        "file": "i1040gi--2025.pdf", "lines": [7876, 7931], "reused": True,
        "location": "Instructions for Form 1040, Schedule 1-A, Part V, Enhanced Deduction for Seniors",
        "text": "Fill out Schedule 1-A, Part V, only if: You (and/or your spouse if filing a joint return) were born before January 2, 1961. You have a valid social security number (SSN). If you are married filing jointly, the spouse who is claiming the enhanced deduction for seniors must have a valid SSN. Death of a taxpayer in 2025. If a taxpayer was born before January 2, 1961, but died in 2025 before reaching age 65, then the taxpayer doesn't qualify for the enhanced deduction for seniors. A person is considered to reach age 65 on the day before the person's 65th birthday. ... The maximum amount of the enhanced deduction for seniors is $6,000 per person. ... Married filing jointly—$150,000. Single, Head of household, or Qualifying surviving spouse—$75,000.",
        "phrases": ["Part V, only if:", "Death of a taxpayer in 2025.", "duction for seniors is $6,000 per person.", "Married filing jointly—$150,000.", "You have a valid social security"],
    },
    {
        "id": "pub501-death-of-taxpayer",
        "file": "p501--2025.pdf", "lines": [1984, 1996],
        "location": "Publication 501 (2025), Higher Standard Deduction for Age (65 or Older), Death of taxpayer",
        "text": "Death of taxpayer. If you are preparing a return for someone who died in 2025, consider the taxpayer to be 65 or older at the end of 2025 only if the taxpayer was 65 or older at the time of death. Even if the taxpayer was born before January 2, 1961, the taxpayer isn't considered 65 or older at the end of 2025 unless the taxpayer was 65 or older at the time of death. A person is considered to reach age 65 on the day before the person's 65th birthday.",
        "phrases": ["Death of taxpayer. If you are preparing a re", "turn for someone who died in 2025, consider",
                    "only if the taxpayer was 65 or older at the time", "payer was 65 or older at the time of death.",
                    "A person is considered to reach age 65 on"],
    },
    {
        "id": "pub501-blindness",
        "file": "p501--2025.pdf", "lines": [2000, 2007],
        "location": "Publication 501 (2025), Higher Standard Deduction for Blindness",
        "text": "If you are blind on the last day of the year and you don't itemize deductions, you are entitled to a higher standard deduction.",
        "phrases": ["If you are blind on the last day of the year and", "a higher standard deduction."],
    },
    {
        "id": "pub501-spouse",
        "file": "p501--2025.pdf", "lines": [2037, 2075],
        "location": "Publication 501 (2025), Spouse 65 or Older or Blind, and Death of spouse",
        "text": "You can take the higher standard deduction if your spouse is age 65 or older or blind and: 1. You file a joint return, or 2. You file a separate return and your spouse had no gross income and can't be claimed as a dependent by another taxpayer. Death of spouse. If your spouse died in 2025 before reaching age 65, you can't take a higher standard deduction because of your spouse. Even if your spouse was born before January 2, 1961, your spouse isn't considered 65 or older at the end of 2025 unless your spouse was 65 or older at the time of death.",
        "phrases": ["Spouse 65 or Older or Blind", "your spouse is age 65 or older or blind and:", "1. You file a joint return, or",
                    "2. You file a separate return and your spouse", "had no gross income and can’t be claimed",
                    "Death of spouse. If your spouse died in 2025", "before reaching age 65, you can’t take a higher"],
    },
]


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _norm(text: str) -> str:
    return re.sub(r"\s+", " ", text.replace("’", "'")).strip()


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    folder = Path(sys.argv[1]).resolve()
    if REPO in folder.parents or folder == REPO:
        raise SystemExit("download directory must be outside the repository")
    folder.mkdir(parents=True, exist_ok=True)
    qw = {s["filename"]: s["sha256"] for s in json.loads(QW_LAW.read_text(encoding="utf-8"))["sources"]}
    qw_quotes = {q["id"]: q for q in json.loads(QW_LAW.read_text(encoding="utf-8"))["quotes"]}
    sources = []
    extracts: dict[str, list[str]] = {}
    for name, document in SOURCES.items():
        path = folder / name
        if not path.exists():
            urllib.request.urlretrieve(BASE + name, path)  # noqa: S310 - fixed irs.gov URL
        digest = _sha(path)
        row = {"document": document, "filename": name, "sha256": digest}
        if name in qw:
            row["matches_question_wording_law_json"] = qw[name] == digest
            if qw[name] != digest:
                raise SystemExit(f"{name}: sha256 differs from question-wording law.json")
        sources.append(row)
        out = folder / (name + ".txt")
        subprocess.run(["pdftotext", "-layout", str(path), str(out)], check=True)
        extracts[name] = out.read_text(encoding="utf-8").split("\n")
    quotes = []
    for quote in QUOTES:
        lines = extracts[quote["file"]][quote["lines"][0] - 1: quote["lines"][1]]
        joined = _norm(" ".join(lines))
        dehyphen = _norm(re.sub(r"-\s*\n\s*", "", "\n".join(line.strip() for line in lines)))
        missing = [p for p in quote["phrases"] if _norm(p) not in joined and _norm(p) not in dehyphen]
        if missing:
            raise SystemExit(f"{quote['id']}: phrases not in lines {quote['lines']}: {missing}")
        row = {
            "id": quote["id"],
            "source": f"{SOURCES[quote['file']]}: {quote['location']}",
            "filename": quote["file"],
            "extract_lines": f"{quote['lines'][0]}-{quote['lines'][1]}",
            "text": quote["text"],
            "phrases_checked": len(quote["phrases"]),
        }
        if quote.get("reused"):
            prior = qw_quotes.get(quote["id"])
            row["question_wording_law_json"] = (
                "same id; range " + str(prior["extract_lines"]) if prior else "absent")
        quotes.append(row)
    payload = {
        "tax_year": 2025,
        "fetched_from": "irs.gov pub/irs-prior",
        "extract": (
            "pdftotext -layout. Line numbers are lines of that extract, not printed page numbers. The extract "
            "keeps the page's columns, so a range can hold neighbouring-column text; each quote's key phrases "
            "were checked inside its range by law.py."
        ),
        "sources": sources,
        "quotes": quotes,
        "reading": [
            "Age: a box is checked for a person born before January 2, 1961. A person reaches 65 on the day before "
            "the 65th birthday, so January 1, 1961 counts and January 2, 1961 does not. A taxpayer or spouse who "
            "died in 2025 counts only if 65 at death (born February 14, 1960: death on February 13, 2025 counts; "
            "February 12 does not). The same test governs the senior deduction.",
            "Blindness: totally blind on December 31, 2025, or the eye doctor's certified 20/200 or 20-degree "
            "statement. The instructions quoted do not say how blindness is judged for a person who died in 2025.",
            "Spouse boxes: on a joint return; on a separate return only if the spouse had no income, isn't "
            "filing and can't be claimed as a dependent (the chart footnote and line 12d); never on head of "
            "household (line 12d). The chart's qualifying surviving spouse rows stop at 2 boxes, so only the "
            "taxpayer's boxes count on that status.",
            "Amounts: chart single 17,750 / 19,750; joint 33,100 to 37,900; qualifying surviving spouse 33,100 / "
            "34,700; separate 17,350 to 22,150; head of household 25,625 / 27,625. The dependents worksheet "
            "adds $2,000 per box (single, head of household) or $1,600 to the smaller of earned income plus $450 "
            "and the base. Senior deduction $6,000 per qualifying person, joint only for a married couple.",
        ],
    }
    text = json.dumps(payload, indent=2, ensure_ascii=False) + "\n"
    for needle in ("/Users/", "/private/", "/tmp/", "/var/"):
        if needle in text:
            raise SystemExit(f"law.json contains {needle}")
    (HERE / "law.json").write_text(text, encoding="utf-8")
    print(json.dumps({"sources": sources, "quotes": len(quotes)}, indent=1))


if __name__ == "__main__":
    main()
