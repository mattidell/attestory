"""P0 probe: what the saved page shows for each per-statement Form 1099-B question.

Evidence only (statement-question-labels P0). Run from the repository root:

    python3 docs/phases/engine-breadth/milestones/statement-question-labels-evidence/probe.py inventory-all
    python3 docs/phases/engine-breadth/milestones/statement-question-labels-evidence/probe.py cases

``inventory-all`` runs every recorded list from ``tools/recorded_replay.py``
on published core v106 (registry v104, release v104) and records, per list
(with its number of Form 1099-B statements), every blocked report row that names
one of the three per-statement fact types, every page reason that carries one
of their questions, and every question group whose answer target is one.

``cases`` runs the synthetic cases (``CASES``): recorded lists with chosen
per-statement answers removed, whose statement entities are relabelled
``demo statement 1`` .. ``demo statement N`` in introduction order, so two
statements can be told apart by their recorded label. The recorded corpus
labels every statement ``Synthetic``.

Every run goes through ``live_coordinate_run`` (``recorded_replay.saved_output``).
Output is written under the ignored ``temp/statement-question-labels/`` directory.
Synthetic ``demo.*`` ids
only. ``observe`` and ``relabel`` are importable for tests.
"""

from __future__ import annotations

import copy
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from tools import recorded_replay as rr  # noqa: E402

CORE = "v106"
STATEMENT_KIND = "tax.us.f1099b-statement"
P = "tax.us.2025.f1099b."
BOX4_AMOUNT = P + "statement-box4-withholding"
BOX4_REPORTED = P + "statement-box4-withholding-reported"
BOX7 = P + "statement-box7-loss-not-allowed"
# The three fact types individuated on one Form 1099-B statement that have an
# adopted input question on v106 (every other Form 1099-B question is per sale).
STATEMENT_FACT_TYPES = (BOX4_AMOUNT, BOX4_REPORTED, BOX7)
SHORT = {BOX4_AMOUNT: "box4-amount", BOX4_REPORTED: "box4-reported", BOX7: "box7"}

# Synthetic cases. Each is a recorded list (key) whose statement entities are
# relabelled ``demo statement 1`` .. ``N`` in introduction order (or all one
# label, ``same``), with the answers ``drop`` names removed: (fact type,
# positions). A position counts, in introduction order, the statements that
# have that answer recorded.
BASE2 = "v83/track0/s0/b4_two_statements"  # two statements, each with a sale; amounts and box 7 answered
BASE3 = "v83/returns/case/mixed_a_d_c_direct/recorded"  # five statements, three with a sale; box 4 "no" and box 7 answered on those three
BASE3W = "v82/p0_a3_w_st_family_long_term/honest"  # three statements with a sale; a sale blocked for another reason
CASES: tuple[dict[str, Any], ...] = (
    {"id": "two.control", "key": BASE2, "drop": (), "expect": {}},
    {"id": "two.amount.s2", "key": BASE2, "drop": ((BOX4_AMOUNT, (1,)),), "expect": {"box4-amount": ["demo statement 2"]}},
    {"id": "two.amount.both", "key": BASE2, "drop": ((BOX4_AMOUNT, (0, 1)),), "expect": {"box4-amount": ["demo statement 1", "demo statement 2"]}},
    {"id": "two.amount.both.same-label", "key": BASE2, "drop": ((BOX4_AMOUNT, (0, 1)),), "same": True, "expect": {"box4-amount": ["demo statement", "demo statement"]}},
    {"id": "two.box7.s1", "key": BASE2, "drop": ((BOX7, (0,)),), "expect": {"box7": ["demo statement 1"]}},
    {"id": "two.box7.both", "key": BASE2, "drop": ((BOX7, (0, 1)),), "expect": {"box7": ["demo statement 1", "demo statement 2"]}},
    {"id": "two.amount-and-box7.s2", "key": BASE2, "drop": ((BOX4_AMOUNT, (1,)), (BOX7, (1,))), "expect": {"box4-amount": ["demo statement 2"], "box7": ["demo statement 2"]}},
    {"id": "two.box4-no-beside-yes", "key": "v82/b4_two_statements_one_yes/honest", "drop": (), "expect": {"box4-amount": ["demo statement 2"]}},
    {"id": "two.box4-reported.s2-missing", "key": "v82/b4_two_statements_one_unanswered/honest", "drop": (), "expect": {"box4-amount": ["demo statement 2"]}},
    {"id": "two.late-statement", "key": "v84/late/late_new_statement_unanswered/1", "drop": (), "expect": {"box4-amount": ["demo statement 2"], "box7": ["demo statement 2"]}},
    {"id": "three.control", "key": BASE3, "drop": (), "expect": {}},
    {"id": "three.box7.s3", "key": BASE3, "drop": ((BOX7, (2,)),), "expect": {"box7": ["demo statement 3"]}},
    {"id": "three.box7.all", "key": BASE3, "drop": ((BOX7, (0, 1, 2)),), "expect": {"box7": ["demo statement 1", "demo statement 2", "demo statement 3"]}},
    {"id": "three.reported.s2", "key": BASE3, "drop": ((BOX4_REPORTED, (1,)),), "expect": {"box4-amount": ["demo statement 2"]}},
    {"id": "three.reported.all", "key": BASE3, "drop": ((BOX4_REPORTED, (0, 1, 2)),), "expect": {"box4-amount": ["demo statement 1", "demo statement 2", "demo statement 3"]}},
    {"id": "three.reported-s1.box7-s2-s3", "key": BASE3, "drop": ((BOX4_REPORTED, (0,)), (BOX7, (1, 2))), "expect": {"box4-amount": ["demo statement 1"], "box7": ["demo statement 2", "demo statement 3"]}},
    {"id": "three.other-block.box7.all", "key": BASE3W, "drop": ((BOX7, (0, 1, 2)),), "expect": {}},
    {"id": "three.other-block.reported.s2", "key": BASE3W, "drop": ((BOX4_REPORTED, (1,)),), "expect": {"box4-amount": ["demo statement 2"]}},
)


def labels_by_fact(observed: dict[str, Any]) -> dict[str, list[str]]:
    """The statement labels each per-statement question carries, the same on every line that shows it."""
    per_line: dict[str, dict[str, list[str]]] = {}
    for reason in observed.get("reasons") or []:
        label = (reason.get("statementLabel") or {}).get("statement")
        per_line.setdefault(reason["fact"], {}).setdefault(reason["line"], []).append(label or "-")
    out: dict[str, list[str]] = {}
    for fact, lines in per_line.items():
        shapes = {tuple(sorted(labels)) for labels in lines.values()}
        out[fact] = list(shapes.pop()) if len(shapes) == 1 else ["(differs by line)"]
    return out


def drop_answers(acts: list[dict[str, Any]], drops: Any) -> list[dict[str, Any]]:
    """``acts`` without the named per-statement answers, renumbered."""
    order = statement_entities(acts)
    recorded = {str(((act.get("payload") or {}).get("finding") or {}).get("fact_id")) for act in acts}
    gone: set[str] = set()
    for fact_type, positions in drops:
        answered = [f"{fact_type}|statement={entity},tax-year=2025" for entity in order]
        answered = [fact_id for fact_id in answered if fact_id in recorded]
        gone |= {answered[position] for position in positions}
    kept = []
    for act in acts:
        payload = act.get("payload")
        finding = payload.get("finding") if isinstance(payload, dict) else None
        if isinstance(finding, dict) and finding.get("fact_id") in gone:
            continue
        kept.append(copy.deepcopy(act))
    if len(kept) == len(acts) and gone:
        raise ValueError("no answer was removed")
    return rr._get_harness().renumber(kept)


def case_lists() -> list[tuple[str, list[dict[str, Any]]]]:
    """The synthetic cases as (case id, acts): answers dropped, statements relabelled."""
    by_key = dict(rr.recorded_lists())
    out = []
    for case in CASES:
        acts = drop_answers(by_key[case["key"]], case["drop"])
        labels = ({entity_id: "demo statement" for entity_id in statement_entities(acts)}
                  if case.get("same") else None)
        out.append((case["id"], relabel(acts, labels)))
    return out


def statement_entities(acts: list[dict[str, Any]]) -> list[str]:
    """Statement entity ids in the order they are introduced."""
    found: list[str] = []
    for act in acts:
        payload = act.get("payload")
        entity = payload.get("entity") if isinstance(payload, dict) else None
        if isinstance(entity, dict) and entity.get("kind") == STATEMENT_KIND and entity.get("id") not in found:
            found.append(str(entity["id"]))
    return found


def relabel(acts: list[dict[str, Any]], labels: dict[str, str] | None = None) -> list[dict[str, Any]]:
    """A copy whose statement entities carry distinct labels (default ``demo statement N``)."""
    order = statement_entities(acts)
    chosen = labels or {entity_id: f"demo statement {index + 1}" for index, entity_id in enumerate(order)}
    out = copy.deepcopy(acts)
    for act in out:
        payload = act.get("payload")
        entity = payload.get("entity") if isinstance(payload, dict) else None
        if isinstance(entity, dict) and entity.get("kind") == STATEMENT_KIND and entity.get("id") in chosen:
            entity["label"] = chosen[entity["id"]]
    return out


def _fact_type_of(name: str) -> str | None:
    base = name.split("|", 1)[0]
    return base if base in STATEMENT_FACT_TYPES else None


def observe(model: dict[str, Any], report: dict[str, Any]) -> dict[str, Any]:
    """What a saved output shows and records for the per-statement questions."""
    questions: dict[str, str] = {}
    groups: list[dict[str, Any]] = []
    for group in model.get("questionGroups") or []:
        target = group.get("answerTarget") or {}
        fact_type = target.get("factTypeId")
        if fact_type in STATEMENT_FACT_TYPES:
            questions[group["question"]] = fact_type
            groups.append({
                "fact": SHORT[fact_type],
                "factId": target.get("factId"),
                "statementLabel": target.get("statementLabel"),
                "lines": sorted({section["id"]
                                 for section in model.get("sections") or []
                                 for ref in ((section.get("resolved") or {}).get("questionRefs") or [])
                                 if ref.get("groupId") == group["id"]}),
            })
    rows: list[dict[str, Any]] = []
    for row in report.get("dispositions") or []:
        if row.get("disposition") != "blocked":
            continue
        named = [str(m) for m in row.get("missing") or [] if _fact_type_of(str(m))]
        if named:
            rows.append({
                "artifact": str(row.get("artifact_id", "")).replace("tax.us.2025.rule.", ""),
                "symbol": row.get("symbol"),
                "code": row.get("code"),
                "missing": named,
                "keyed": all("|" in m for m in named),
            })
    reasons: list[dict[str, Any]] = []
    for section in model.get("sections") or []:
        resolved = section.get("resolved") or {}
        refs = resolved.get("questionRefs") or []
        for index, reason in enumerate(resolved.get("reasons") or []):
            sentence = reason.get("sentence")
            fact_type = questions.get(sentence) or _sentence_fact_type(sentence, model)
            if fact_type is None:
                continue
            reasons.append({
                "line": section["id"],
                "fact": SHORT[fact_type],
                "statementLabel": reason.get("statementLabel"),
                "memberLabel": reason.get("memberLabel"),
                "linked": any(index in (ref.get("reasonIndices") or []) for ref in refs),
            })
    return {"rows": rows, "reasons": reasons, "groups": groups}


_QUESTION_TEXT: dict[str, str] | None = None


def _sentence_fact_type(sentence: Any, model: dict[str, Any]) -> str | None:
    global _QUESTION_TEXT
    if _QUESTION_TEXT is None:
        content = REPO / "packages/content/tax/2025"
        _QUESTION_TEXT = {}
        for name in ("input-question.f1099b-box4.v2.json",
                     "input-question.f1099b-statement-box4-withholding-reported.json",
                     "input-question.f1099b-statement-box7-loss-not-allowed.json"):
            body = json.loads((content / name).read_text(encoding="utf-8"))
            _QUESTION_TEXT[body["question"]] = body["fact_type"]["id"]
    return _QUESTION_TEXT.get(sentence) if isinstance(sentence, str) else None


def summarize(observed: dict[str, Any], statements: int) -> dict[str, Any]:
    """Counts per fact: page lines showing the question, labelled reasons, groups, row shapes."""
    out: dict[str, Any] = {"statements": statements}
    for short in SHORT.values():
        reasons = [r for r in observed["reasons"] if r["fact"] == short]
        rows = [r for r in observed["rows"] if any(SHORT[_fact_type_of(m) or ""] == short for m in r["missing"])]
        groups = [g for g in observed["groups"] if g["fact"] == short]
        if not (reasons or rows or groups):
            continue
        out[short] = {
            "lines_with_question": len({r["line"] for r in reasons}),
            "reasons": len(reasons),
            "reasons_labelled": sum(1 for r in reasons if r["statementLabel"] or r["memberLabel"]),
            "reasons_linked": sum(1 for r in reasons if r["linked"]),
            "max_reasons_per_line": max(Counter(r["line"] for r in reasons).values(), default=0),
            "groups": len(groups),
            "groups_labelled": sum(1 for g in groups if g["statementLabel"]),
            "row_shapes": sorted({f"{r['artifact']}|{r['code']}|{'keyed' if r['keyed'] else 'type'}" for r in rows}),
        }
    return out


class Inventory:
    """Picklable per-list callable for ``recorded_replay.replay``.

    With ``both`` the list also runs under the scratch design, and the result
    holds both observations.
    """

    def __init__(self, both: bool = False) -> None:
        self.both = both

    def _one(self, key: str, acts: list[dict[str, Any]], core: Any, statements: int,
             *, scratch: bool = False) -> dict[str, Any]:
        if str(HERE) not in sys.path:
            sys.path.insert(0, str(HERE))
        from replay import save_pre_build

        run_id = "demo.sql." + hashlib.sha256(key.encode()).hexdigest()[:20]
        saved = save_pre_build(core, acts, run_id, scratch=scratch)
        if saved["outcome"] != "success":
            return {"outcome": saved["outcome"], "statements": statements}
        observed = observe(saved["model"], saved["report"])
        return {"outcome": "success", **summarize(observed, statements), "observed": observed}

    def __call__(self, key: str, acts: list[dict[str, Any]], cores: Any) -> dict[str, Any]:
        core = cores[0] if isinstance(cores, (list, tuple)) else cores
        statements = len(statement_entities(acts))
        published = self._one(key, acts, core, statements)
        if not self.both:
            return published
        return {"published": published, "design": self._one(key, acts, core, statements, scratch=True)}


def _multi(lists: list[tuple[str, Any]]) -> list[tuple[str, Any]]:
    return [(key, acts) for key, acts in lists if len(statement_entities(acts)) >= 2]


def main(argv: list[str]) -> None:
    mode = argv[1] if len(argv) > 1 else "inventory-all"
    output_dir = REPO / "temp" / "statement-question-labels"
    core = rr.resolve_core(CORE)
    lists = rr.recorded_lists()
    if mode == "inventory-all":
        chosen = lists
        results = rr.replay(chosen, (core,), Inventory(), workers=9)
        for row in results.values():
            row.pop("observed", None)
        out = output_dir / "inventory-all.json"
    elif mode == "cases":
        results = rr.replay(case_lists(), (core,), Inventory(both=True), workers=8)
        expected = {case["id"]: case["expect"] for case in CASES}
        for case_id, row in results.items():
            shown = {"published": labels_by_fact(row["published"].get("observed") or {}),
                     "design": labels_by_fact(row["design"].get("observed") or {})}
            row["labels"] = shown
            row["expected_design_labels"] = expected[case_id]
            row["design_as_expected"] = shown["design"] == expected[case_id]
            for side in ("published", "design"):
                row[side].pop("observed", None)
        print("design as expected:", sum(row["design_as_expected"] for row in results.values()), "of", len(results))
        out = output_dir / "cases.json"
    else:
        raise SystemExit(f"unknown mode {mode!r}")
    text = json.dumps({"core": CORE, "results": results}, indent=1, sort_keys=True) + "\n"
    rr._check_no_local_paths(text, out.name)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text, encoding="utf-8")
    print(out.name, len(results))


if __name__ == "__main__":
    main(sys.argv)
