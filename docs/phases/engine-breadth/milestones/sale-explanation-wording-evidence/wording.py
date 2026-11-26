"""Write wording.json: old, new and the 2025 IRS section for each sale explanation and question.

Run from the repository root: python3 docs/phases/engine-breadth/milestones/sale-explanation-wording-evidence/wording.py

Reads the published core v106 citizens. Each new sentence is chosen by the
kind of sale (what form and box the filer can look at) and the rule that
blocked; short-term and long-term families share one sentence. Nothing in
packages/ is edited.
"""
from __future__ import annotations

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
CONTENT = REPO / "packages/content/tax/2025"
P = "tax.us.2025."

S8949 = "2025 Instructions for Form 8949"
SCHD = "2025 Instructions for Schedule D"

# The kind of sale each family holds.
KIND = {
    "f1099b.covered-w": "covered_w",
    "f1099b.noncovered": "noncovered",
    "f1099b.code-b": "code_b",
    "f8949.no1099b": "no1099b",
}

CHECK = {
    "covered_w": "Check what you entered against the proceeds in box 1d, the basis in box 1e and the amount in box 1g of your Form 1099-B, and fix whichever amount you entered differently.",
    "noncovered": "Check what you entered against the proceeds in box 1d and any amount in box 1g of your Form 1099-B, and the basis you entered for column (e) of Form 8949, then fix whichever of your entries is wrong.",
    "code_b": "Check what you entered against the proceeds in box 1d and the amount in box 1g of your Form 1099-B, and fix whichever amount you entered differently.",
    "no1099b": "Check the net proceeds, basis and wash-sale loss you entered for columns (d), (e) and (g) of Form 8949, and fix whichever of your entries is wrong.",
}

WASH_ON_GAIN = {
    "covered_w": "You entered a wash-sale loss for box 1g, but this sale has no loss, so there is nothing to disallow.",
    "noncovered": "You entered a wash-sale loss for column (g), but this sale has no loss, so there is nothing to disallow.",
    "code_b": "You entered a wash-sale loss, but with the correct basis you entered this sale has no loss, so there is nothing to disallow.",
    "no1099b": "You entered a wash-sale loss for column (g), but this sale has no loss, so there is nothing to disallow.",
}

WASH_TOO_BIG = {
    "covered_w": "The wash-sale loss you entered for box 1g is more than this sale lost.",
    "noncovered": "The wash-sale loss you entered for column (g) is more than this sale lost.",
    "code_b": "The wash-sale loss you entered is more than this sale lost with the correct basis you entered.",
    "no1099b": "The wash-sale loss you entered for column (g) is more than this sale lost.",
}

HOLDING = "You marked this sale long-term but entered it with your short-term sales, or the other way around."
HOLDING_1099B = "Check box 2 of your Form 1099-B, if it is filled in, and the dates you acquired and sold it, since a sale held more than 1 year is long-term."
HOLDING_NO1099B = "Check the dates you acquired and sold it in columns (b) and (c) of Form 8949, since a sale held more than 1 year is long-term."

WASH_SOURCE = (f"{SCHD}, General Instructions, Wash Sales; {S8949}, Column (g), code W "
               "(a wash sale disallows only a loss on a sale at a loss).")
COLUMNS = {
    "covered_w": f"{S8949}, Columns (d) and (e), Form 1099-B boxes 1d and 1e; {SCHD}, Wash Sales, box 1g of Form 1099-B.",
    "noncovered": f"{S8949}, Column (d), box 1d of Form 1099-B; Column (e), basis not reported to the IRS.",
    "code_b": f"{S8949}, Column (f), code B (basis shown in box 1e is incorrect); Column (g).",
    "no1099b": f"{S8949}, Column (d), net proceeds when no Form 1099-B was received; Column (e).",
}


def explanation(kind: str, code: str) -> tuple[str, str]:
    if code == "CODE_W_ON_GAIN":
        return WASH_ON_GAIN[kind] + " " + CHECK[kind], WASH_SOURCE + " " + COLUMNS[kind]
    if code == "ADJUSTMENT_EXCEEDS_LOSS":
        return WASH_TOO_BIG[kind] + " " + CHECK[kind], WASH_SOURCE + " " + COLUMNS[kind]
    if code == "HOLDING_PERIOD_MISMATCH":
        rest = HOLDING_NO1099B if kind == "no1099b" else HOLDING_1099B
        return HOLDING + " " + rest, (f"{S8949}, General Instructions, Short-Term or Long-Term (held more than 1 year "
                                      "is long-term); Part I and Part II; box 2 of Form 1099-B.")
    if code == "BASIS_WAS_REPORTED":
        return ("You said your broker reported this sale's basis to the IRS, but you entered it with sales whose "
                "broker did not report it. If box 12 of your Form 1099-B is checked, enter it with your sales that "
                "have box 12 checked, and if box 12 is blank, change your answer that it was reported."), (
                f"{S8949}, Part I and Part II, box A or D versus box B or E (Form 1099-B showing basis was "
                f"reported to the IRS); {SCHD}, Lines 1a and 8a.")
    if code == "BOX_1G_FLAG_WITHOUT_AMOUNT":
        return ("You said box 1g of your Form 1099-B shows a wash-sale loss disallowed for this sale, but you did not "
                "enter the amount. Enter the amount from box 1g, or if box 1g is blank, change your answer that box 1g "
                "shows one."), (
                f"{SCHD}, General Instructions, Wash Sales (box 1g of Form 1099-B shows the wash sale loss "
                f"disallowed); {S8949}, Column (g), code W.")
    if code == "BOX_1G_AMOUNT_WITHOUT_FLAG":
        return ("You entered a box 1g wash-sale amount for this sale but did not say that box 1g of your Form 1099-B "
                "shows one. If box 1g shows an amount, say that it does, or if box 1g is blank, change your answer "
                "that box 1g shows one and remove the amount."), (
                f"{SCHD}, General Instructions, Wash Sales (box 1g of Form 1099-B shows the wash sale loss "
                f"disallowed); {S8949}, Column (g), code W.")
    if code == "CODE_B_WITHOUT_CORRECTION":
        return ("The correct basis you entered for this sale matches box 1e of your Form 1099-B, so there is nothing "
                "to correct. Enter it with your sales whose box 1e is right instead, and include any wash-sale loss "
                "from box 1g."), (
                f"{S8949}, Column (f), code B (use only when the basis shown in box 1e is incorrect); "
                f"{SCHD}, Exception 1 and Wash Sales.")
    raise KeyError(code)


def question(kind: str, term: str) -> tuple[str, str]:
    if kind == "covered_w":
        return (f"What is the wash-sale loss disallowed in box 1g of your Form 1099-B for this {term} sale? "
                "If box 1g is wrong, enter the correct amount. If box 1g is blank, change your answer that it shows one."), (
                f"{SCHD}, General Instructions, Wash Sales (box 1g of Form 1099-B); {S8949}, Column (g), code W.")
    if kind == "noncovered":
        return ("How much of this sale's loss does a wash sale disallow? Use box 1g of your Form 1099-B if it "
                "shows an amount. If there is none, enter 0."), (
                f"{SCHD}, General Instructions, Wash Sales; {S8949}, Column (g), code W.")
    if kind == "no1099b":
        return (f"What wash-sale loss disallowed do you enter in column (g) of Form 8949 for this {term} sale with "
                "no Form 1099-B? If there is none, enter 0."), (
                f"{SCHD}, General Instructions, Wash Sales; {S8949}, Column (g), code W.")
    if kind == "code_b":
        return (f"What amount goes in column (g) of Form 8949 for this {term} sale whose Form 1099-B shows the "
                "wrong basis in box 1e? Enter the amount in box 1e minus the correct basis, plus the wash-sale "
                "loss in box 1g if there is one."), (
                f"{S8949}, Column (f), code B, and Column (g), the adjustment that corrects the basis shown "
                "in box 1e, with code W for a wash sale loss.")
    raise KeyError(kind)


def kind_of(family_id: str) -> tuple[str, str]:
    stem, term = family_id[len(P):].rsplit("-", 1)
    return KIND[stem], {"st": "short-term", "lt": "long-term"}[term]


def main() -> None:
    rows = []
    for path in sorted(CONTENT.glob("family-block-explanation.*.v1.json")):
        doc = json.loads(path.read_text(encoding="utf-8"))
        kind, _term = kind_of(doc["family_id"])
        new, source = explanation(kind, doc["block_code"])
        rows.append({"file": str(path.relative_to(REPO)), "id": doc["id"], "version": doc["version"],
                     "schema": doc["schema"], "family_id": doc["family_id"], "block_code": doc["block_code"],
                     "property": "explanation", "old": doc["explanation"], "new": new,
                     "irs_source_2025": source})
    questions = []
    for stem in ("f1099b-covered-w", "f1099b-noncovered", "f8949-no1099b", "f1099b-code-b"):
        for term in ("st", "lt"):
            cid = f"{P}input-question.{stem}-{term}-adjustment"
            path = next(p for p in sorted(CONTENT.glob(f"input-question.{stem}-{term}-adjustment*.json"))
                        if json.loads(p.read_text(encoding="utf-8"))["version"] == "v1")
            doc = json.loads(path.read_text(encoding="utf-8"))
            assert doc["id"] == cid
            kind, term_word = kind_of(f"{P}{stem.replace('-', '.', 1)}-{term}")
            new, source = question(kind, term_word)
            questions.append({"file": str(path.relative_to(REPO)), "id": cid, "version": doc["version"],
                              "schema": doc["schema"], "fact_type": doc["fact_type"]["id"],
                              "property": "question", "old": doc["question"], "new": new,
                              "irs_source_2025": source})
    body = {
        "basis": ("Track 1 of sale-explanation-wording: the 30 sale explanations and 8 sale wash-sale adjustment "
                  "questions on core v106, rewritten to the plan's wording bar. Sources are the 2025 Instructions "
                  "for Form 8949 and the 2025 Instructions for Schedule D, by section."),
        "explanations": len(rows), "questions": len(questions),
        "replacements": rows + questions,
    }
    (HERE / "wording.json").write_text(json.dumps(body, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(len(rows), len(questions))


if __name__ == "__main__":
    main()
