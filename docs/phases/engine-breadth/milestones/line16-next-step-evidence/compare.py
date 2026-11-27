"""Compare regenerated probe output for published v108 and v109.

Run probe.py for both cores, then run this script. All three results use the
probe output directory.

For every probe list: every page field's disposition, value and codes, the
three watched rule rows and the question cards must be identical. Every
blocked field must draw exactly its v108 text plus, after it, one bullet per
Exception 1 question the field names whose recorded answer is "no", with that
question's declared answer explanation, sorted, and nothing else. Fields that
name no Exception 1 question draw the same text as on v108.
"""
from __future__ import annotations

import json

from probe import PROBE_OUTPUT
from replay import explanations

P = "tax.us.2025."
SHORT = {"only-box2a-capital-gains": "C1 only-box2a", "no-capital-losses": "C2 no-capital-losses",
         "no-qof-deferral": "C3 no-qof-deferral", "no-boxes-2b-2c-2d": "C4 no-boxes-2b-2c-2d"}


def main() -> int:
    sentences = {fact_type.removeprefix(P + "exception1."): sentence
                 for sentence, (fact_type, _, value) in explanations().items() if value == "no"}
    before = json.loads((PROBE_OUTPUT / "probe-v108.json").read_text(encoding="utf-8"))
    after = json.loads((PROBE_OUTPUT / "probe-v109.json").read_text(encoding="utf-8"))
    assert [before["cores"][0]["version"], after["cores"][0]["version"]] == ["v108", "v109"]
    assert before["cases"].keys() == after["cases"].keys()
    rows, fails = {}, []
    for key in before["cases"]:
        a, b = before["cases"][key]["cores"][0], after["cases"][key]["cores"][0]
        problems = [name for name in ("outcome", "values", "rows", "question_cards", "recorded_answers", "blocked_fields")
                    if a.get(name) != b.get(name)]
        old = {f: g for g in a.get("blocked_field_groups", []) for f in g["fields"]}
        new = {f: g for g in b.get("blocked_field_groups", []) for f in g["fields"]}
        if old.keys() != new.keys():
            problems.append("blocked field set")
        explained, unchanged = 0, 0
        for field in sorted(old.keys() & new.keys()):
            named = [n.removeprefix("exception1.") for n in old[field]["named_questions"] if n.startswith("exception1.")]
            want = sorted({sentences[slug] for slug in named if a["recorded_answers"][SHORT[slug]] == "no"})
            expected = old[field]["text"] + ["- " + s for s in want]
            if new[field]["text"] != expected or new[field]["named_questions"] != old[field]["named_questions"]:
                problems.append("field " + field)
            explained += bool(want)
            unchanged += not want
        stated = b.get("answer_words_stated_on_page", [])
        rows[key] = {"verdict": "FAIL" if problems else "PASS", "problems": problems,
                     "fields_with_explanations": explained, "fields_unchanged": unchanged,
                     "answer_words_stated_on_page": {"v108": a.get("answer_words_stated_on_page", []), "v109": stated}}
        if problems:
            fails.append(key)
    body = {"format": "line16-next-step-probe-compare.v1", "cores": [before["cores"][0], after["cores"][0]],
            "lists": len(rows), "verdict": "FAIL" if fails else "PASS", "failing": fails,
            "lists_with_explanations": sorted(k for k, r in rows.items() if r["fields_with_explanations"]),
            "explanations": sentences, "rows": rows}
    (PROBE_OUTPUT / "probe-compare.json").write_text(json.dumps(body, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({k: body[k] for k in ("lists", "verdict", "failing")}, indent=1),
          len(body["lists_with_explanations"]))
    return int(bool(fails))


if __name__ == "__main__":
    raise SystemExit(main())
