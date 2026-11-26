"""Write wording.json: the four code B wash-sale explanations name the correct basis (Decision 1).

Run from the repository root:
python3 docs/phases/engine-breadth/milestones/code-b-basis-sentence-evidence/wording.py

Reads the published v2 citizens adopted by core v107. The first sentence of
each explanation is kept; the second becomes the Decision 1 sentence. The row
shape is sale-explanation-wording's wording.json, with "old" the v2 text.
Nothing in packages/ is edited.
"""
from __future__ import annotations

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
CONTENT = REPO / "packages/content/tax/2025"
P = "tax.us.2025."

OLD_CHECK = ("Check what you entered against the proceeds in box 1d and the amount in box 1g of your "
             "Form 1099-B, and fix whichever amount you entered differently.")
NEW_CHECK = ("Check the proceeds and wash-sale loss you entered against box 1d and box 1g of your Form "
             "1099-B, and the correct basis you entered against your own records, then fix whichever "
             "amount is wrong.")
SOURCE = ("2025 Instructions for Schedule D, General Instructions, Wash Sales; 2025 Instructions for Form "
          "8949, Column (g), code W (a wash sale disallows only a loss on a sale at a loss). 2025 "
          "Instructions for Form 8949, Column (f), code B (basis shown in box 1e is incorrect; the "
          "correct basis comes from the filer's own records); Column (g).")
CITIZENS = [f"f1099b-code-b-{term}.{code}" for term in ("st", "lt")
            for code in ("adjustment-exceeds-loss", "code-w-on-gain")]


def main() -> None:
    rows = []
    for stem in CITIZENS:
        path = CONTENT / f"family-block-explanation.{stem}.v2.json"
        body = json.loads(path.read_text(encoding="utf-8"))
        old = body["explanation"]
        assert old.count(OLD_CHECK) == 1 and old.endswith(OLD_CHECK), stem
        new = old[: -len(OLD_CHECK)] + NEW_CHECK
        rows.append({"file": str(path.relative_to(REPO)), "id": body["id"], "version": body["version"],
                     "schema": body["schema"], "family_id": body["family_id"], "block_code": body["block_code"],
                     "property": "explanation", "old": old, "new": new, "irs_source_2025": SOURCE})
    out = {"basis": "Decision 1 of docs/phases/engine-breadth/milestones/code-b-basis-sentence.md; "
                    "first sentence kept, second sentence replaced",
           "replacements": rows}
    (HERE / "wording.json").write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(out, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()
