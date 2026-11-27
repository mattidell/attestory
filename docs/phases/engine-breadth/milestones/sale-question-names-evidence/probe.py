"""Synthetic Box C and F returns for the sale-question naming design."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import json
from pathlib import Path
import sys
from unittest.mock import patch

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
sys.path.insert(0, str(REPO))

from packages.derivation import live, presentation_projection
from tests.helpers import current_core_returns as ccr
from tools import recorded_replay as rr

P = "tax.us.2025."
CORE = "v109"
TERMS = ("st", "lt")
SALE_TYPES = {P + f"f8949.no1099b-{term}-txn": term for term in TERMS}
SALE_ENTITY = "tax.us.f8949-sale"
KINDS = ("basis", "proceeds", "adjustment")
ALPHA = "demo Alpha shares"
ZULU = "demo Zulu & Sons shares"
PEER = "demo Peer shares"


@dataclass(frozen=True)
class Sale:
    label: str
    term: str = "st"
    condition: str = "good"


def cases() -> dict[str, tuple[Sale, ...]]:
    return {
        "demo.two-fixes": (Sale(ZULU, condition="gain"), Sale(ALPHA, condition="exceeds")),
        "demo.three-with-peer": (
            Sale(ZULU, "lt", "gain"), Sale(ALPHA, "lt", "exceeds"), Sale(PEER, "lt"),
        ),
        "demo.mixed-terms": (Sale(ZULU, condition="gain"), Sale(ALPHA, "lt", "exceeds")),
        "demo.missing-adjustment": (Sale(ZULU, condition="missing-adjustment"), Sale(PEER)),
        "demo.missing-basis": (Sale(ZULU, condition="missing-basis"), Sale(PEER)),
        "demo.missing-proceeds": (Sale(ZULU, condition="missing-proceeds"), Sale(PEER)),
        "demo.amounts-disagree": (
            Sale(ZULU, condition="wrong-proceeds"), Sale(ALPHA, condition="wrong-basis"), Sale(PEER),
        ),
        "demo.holding-period": (Sale(ZULU, condition="wrong-term"), Sale(PEER)),
        "demo.blank-label": (Sale(" ", condition="gain"), Sale(ALPHA, condition="exceeds")),
        "demo.repeated-label": (Sale(ALPHA, condition="gain"), Sale(ALPHA, condition="exceeds")),
        "demo.repeated-with-peer": (Sale(ALPHA, condition="gain"), Sale(ALPHA)),
        "demo.all-valid": (Sale(ZULU), Sale(ALPHA)),
        "demo.single-sale": (Sale(ZULU, condition="gain"),),
    }


def build_sales(sales: tuple[Sale, ...]) -> rr.Acts:
    harness = rr._get_harness()
    precedent = rr._module(
        "sale_names_block_probe", HERE.parent / "sale-block-explanations-evidence/inventory_probe.py",
    )
    acts = harness.opened()
    for index, sale in enumerate(sales):
        tag = f"demo.sale-names.{index}"
        options = {
            "good": {},
            "gain": {"basis": 1000, "wash": 500},
            "exceeds": {"wash": 1500},
            "missing-adjustment": {"wash": 500, "rows": {"adjustment": None}},
            "missing-basis": {"rows": {"basis": None}},
            "missing-proceeds": {"rows": {"proceeds": None}},
            "wrong-basis": {"rows": {"basis": 2500}},
            "wrong-proceeds": {"rows": {"proceeds": 2500}},
            "wrong-term": {"long_term": "yes" if sale.term == "st" else "no"},
        }[sale.condition]
        fields = {"proceeds": 2000, "basis": 3000, **options}
        acts = harness.sale(acts, "no1099b", sale.term, tag=tag, **fields)
        entity = next(
            act["payload"]["entity"] for act in acts if act["kind"] == "entity-introduced"
            and act["payload"]["entity"]["id"] == f"demo.sfa.{tag}.sale"
        )
        entity["label"] = sale.label
    acts = harness.answer(acts, **harness.honest({"no1099b"}, loss=True, new_questions=False))
    return precedent.add_standard_answers(
        acts, rr.resolve_core(CORE), harness, ccr, has_1099b=False, tag="demo.sale-names",
    )


def questions(members):
    return {
        member["fact_type"]["id"]: member["question"] for member in members
        if member.get("schema") == "input-question.v1"
        and member["fact_type"]["id"].rpartition(".")[0] in SALE_TYPES
    }


def observe(acts: rr.Acts, key: str, core: str = CORE) -> dict:
    """Capture question reasons and the already-read evidence in a live run."""
    census = {}

    def projector(**kwargs):
        by_type = questions(kwargs["resolved_members"])
        model = presentation_projection.build_presentation_model(**kwargs)
        found = {}
        groups = {group["id"]: group for group in model["questionGroups"]}
        for section in model["sections"]:
            resolved = section["resolved"]
            for index, reason in enumerate(resolved.get("reasons", ())):
                for fact_type, sentence in by_type.items():
                    if reason["sentence"] != sentence:
                        continue
                    entry = found.setdefault(fact_type, {"sentence": sentence, "sections": [], "refs": []})
                    entry["sections"].append(section["field"]["id"].removeprefix(P))
                    for ref in resolved.get("questionRefs", ()):
                        if index in ref["reasonIndices"]:
                            target = groups[ref["groupId"]]["answerTarget"]["factId"]
                            if target not in entry["refs"]:
                                entry["refs"].append(target)
        census["questions"] = found
        census["rows"] = [
            row for row in kwargs["dispositions"]
            if "no1099b" in row["artifact_id"]
            and (row["disposition"] == "blocked" or "amounts-agree" in row["artifact_id"])
        ]
        census["validation_publications"] = [
            pub.finding for pub in kwargs["publications"]
            if "no1099b" in pub.finding["symbol"] and ".member-validation.synthesized." in pub.finding["symbol"]
        ]
        return model

    with patch.object(live, "build_presentation_model", projector):
        saved = rr.saved_output(core, acts, key)
    if saved["outcome"] != "success":
        raise ValueError(f"{key} did not save: {saved['outcome']} {saved['error']} {saved['message']}")
    return census


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--core", default=CORE)
    parser.add_argument("cases", nargs="*")
    args = parser.parse_args()
    available = cases()
    selected = args.cases or list(available)
    results = {key: observe(build_sales(available[key]), key, args.core) for key in selected}
    args.out.write_text(json.dumps(results, indent=2, sort_keys=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
