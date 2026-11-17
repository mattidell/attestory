"""Assess the eight existing sentences against local 2025 IRS instructions.

Run: python3 source_audit.py <1040-instructions.pdf> <schedule-d.pdf> <8949.pdf>
Only safe source identities, page locators and assessments are written.
"""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("l16_law_probe", HERE / "probe.py")
probe = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = probe
spec.loader.exec_module(probe)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("sources", type=Path, nargs=3)
    args = p.parse_args()
    specs = [
        ("2025 Instructions for Form 1040", "https://www.irs.gov/pub/irs-prior/i1040gi--2025.pdf",
         ["You have no capital losses", "Line 16"],
         "Line 7a, Exception 1; line 16 and Qualified Dividends and Capital Gain Tax Worksheet"),
        ("2025 Instructions for Schedule D", "https://www.irs.gov/pub/irs-prior/i1040sd--2025.pdf",
         ["Capital Assets Held for", "Because the loss isn’t"],
         "Capital Assets Held for Personal Use; Certain Nondeductible Losses; Lines 1a and 8a"),
        ("2025 Instructions for Form 8949", "https://www.irs.gov/pub/irs-prior/i8949--2025.pdf",
         ["You have a nondeductible loss other than", "$0 as the gain or loss"],
         "Personal items reported on Form 1099-K; columns (f) and (g), code L; instructions for line 1, boxes B/C/E/F"),
    ]
    sources = []
    for path, (title, url, needles, headings) in zip(args.sources, specs):
        assert path.read_bytes().startswith(b"%PDF-")
        text = subprocess.check_output(["pdftotext", "-layout", str(path), "-"], text=True)
        normalized = " ".join(text.split())
        assert all(needle in normalized for needle in needles), title
        pages = [i + 1 for i, page in enumerate(text.split("\f"))
                 if any(needle in " ".join(page.split()) for needle in needles)]
        sources.append({"title": title, "url": url, "filename": path.name,
                        "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                        "pdf_pages": pages, "headings": headings})
    baseline = probe.read_cases(HERE / "baseline.json")
    candidate = probe.read_cases(HERE / "candidate.json")
    field = probe.expand(candidate["recorded/t4_s1_removed"])["fields"]["form1040.line-16"]
    questions = [r["sentence"] for r in field["reasons"]]
    assert len(questions) == 8
    assessments = [
        (probe.FOUR[0], "Did you sell any securities whose basis", "no", "8949 boxes B/E concern securities with basis not reported; a personal item is not evidence of a securities sale.", [1, 2]),
        (probe.FOUR[1], "Did you sell any stocks or other securities", "no", "8949 boxes C/F also cover other capital assets, but this existing sentence asks about securities. A personal item does not become a security.", [1, 2]),
        (probe.FOUR[2], "Is it true that you had no transaction", "no", "The stipulated item is reported on Form 8949. Nondeductibility does not erase that reporting fact.", [1, 2]),
        (probe.FOUR[3], "Is it true that every Form 8949 adjustment code is W", "no", "Personal nondeductible losses use adjustment code L, not the W-only route. This is evidence for the existing no; the code-L product question stays parked.", [1, 2]),
        (probe.EXC[0], "Is it true that you had no capital gains", "no", "The adopted v3 sentence expressly excludes a personal loss only when it is not reported on Form 8949 (and no Form 1099-S). This case is reported there. Exception 1 yes would contradict it.", [0, 1, 2]),
        (probe.EXC[1], "Is it true that you had no capital losses", "no", "Personal-use property is a capital asset; a loss can be nondeductible and still require reporting and a positive code-L adjustment. Do not turn that item into the supported deductible securities loss.", [0, 1, 2]),
        (probe.EXC[2], "Is it true that you did not defer", "yes", "The stipulated case has no QOF deferral. This accurate Exception 1 criterion is already satisfied; changing it to no supplies another reason to require Schedule D.", [0]),
        (probe.EXC[3], "Is it true that none of your 2025 Forms", "yes", "The stipulated case has none of these distribution boxes. This accurate Exception 1 criterion is already satisfied; changing it to no cannot remove the reported personal item.", [0]),
    ]
    rows = []
    for name, prefix, value, assessment, source_indices in assessments:
        sentence = next(q for q in questions if q.startswith(prefix))
        measured = {}
        for answer in ("yes", "no"):
            case = probe.expand(baseline["protected/" + name + "/" + answer])
            measured[answer] = case["fields"]["form1040.line-16"]
        rows.append({"name": name, "sentence": sentence, "truthful_answer_on_stipulated_case": value,
                     "assessment": assessment, "sources": source_indices, "one_answer_at_a_time": measured})
    probe.write("law.json", {"sources": sources, "questions": rows,
        "conclusion": "The eight sentences are valid domain questions, but the four added Exception 1 questions are not truthful additional ways to resolve this fixed personal-loss case. Preserve its four names. The no-form8949-sources answer (no here, yes on the four recorded target returns) distinguishes them inside the guard.",
        "limit": "Counterfactual answers demonstrate software routing, not permission to change truthful facts. No new question wording or personal-loss support is proposed."})
    print(json.dumps({"sources": len(sources), "sentences_checked": len(rows), "recommendation": "preserve protected case"}))


if __name__ == "__main__":
    main()
