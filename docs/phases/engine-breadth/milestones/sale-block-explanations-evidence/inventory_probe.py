"""Synthetic probe for sale-family member-validation blocks and fixes.

Imports sibling `audit_harness.py` by file path under a unique module name so
tests and evidence scripts never rely on bare package imports.
"""

from __future__ import annotations

import argparse
import copy
import importlib.util
import json
import sys
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any

REPO = Path(__file__).resolve().parents[4]
P = "tax.us.2025."
BOX4 = P + "f1099b.statement-box4-withholding-reported"
BOX7 = P + "f1099b.statement-box7-loss-not-allowed"
NO_SALE_BOX4 = P + "f1099b.no-sale-box4-present"


def _load_module(name: str, path: Path) -> Any:
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def add_standard_answers(acts: list[dict[str, Any]], core: Any, h: Any, ccr: Any, *, has_1099b: bool, tag: str) -> list[dict[str, Any]]:
    acts = ccr.state_taxpayer_facts(acts, core="v88")
    acts = h.say(acts, NO_SALE_BOX4, "no", f"{tag}.nsb4", core.content)
    if has_1099b:
        stmts: list[str] = []
        for a in acts:
            if a.get("kind") == "member-transition":
                fid = str(((a.get("payload") or {}).get("member") or {}).get("finding", {}).get("fact_id") or "")
                if "statement=" in fid:
                    stmt = fid.split("statement=", 1)[1].split(",", 1)[0]
                    if stmt not in stmts:
                        stmts.append(stmt)
        for idx, stmt in enumerate(stmts):
            for ft, short in ((BOX4, "box4"), (BOX7, "box7")):
                body = h.bundle_for(ft, core.content)
                if body is not None and not {f["id"] for f in body["fact_types"]} & h._adopted(acts):
                    h._add(acts, "bundle-adoption", {"bundle": body})
                fact_id = h.fact_id_for(ft, (("statement", stmt), ("tax-year", h.YEAR)))
                h._add(acts, "assertion", {"finding": h._attested(f"demo.sbe.{tag}.{short}.{idx}", fact_id, "no")})
    return h.renumber(acts)


def build_sale_case(kind: str, term: str, variant: str, core: Any, h: Any, ccr: Any) -> list[dict[str, Any]]:
    tag = f"sbe.{kind}.{term}.{variant}"
    acts = h.opened()
    has_1099b = kind != "no1099b"
    if variant == "valid_loss":
        if kind == "codeb":
            acts = h.sale(acts, kind, term, proceeds=2000, basis=4000, corrected=3000, wash=500, tag=tag)
        else:
            acts = h.sale(acts, kind, term, proceeds=2000, basis=3000, wash=500, tag=tag)
        loss = True
    elif variant == "BOX_1G_FLAG_WITHOUT_AMOUNT":
        acts = h.sale(acts, kind, term, proceeds=2000, basis=3000, wash=0, tag=tag, rows={"adjustment": None})
        for a in acts:
            if a.get("kind") == "member-transition":
                f = (a["payload"].get("member") or {}).get("finding") or {}
                if f.get("fact_id", "").startswith(P + f"f1099b.covered-w-{term}-txn|"):
                    f["value"].pop("box_1g_wash_sale_disallowed_amount", None)
                    f["value"]["box_1g_wash_sale_adjustment"] = "yes"
        loss = True
    elif variant == "BOX_1G_AMOUNT_WITHOUT_FLAG":
        acts = h.sale(
            acts, kind, term, proceeds=2000, basis=3000, wash=500, tag=tag,
            box_1g_wash_sale_adjustment="no", box_1g_wash_sale_disallowed_amount=500,
        )
        loss = True
    elif variant == "BASIS_WAS_REPORTED":
        acts = h.sale(acts, kind, term, proceeds=3000, basis=2000, wash=0, tag=tag, basis_reported_to_irs="yes")
        loss = False
    elif variant == "HOLDING_PERIOD_MISMATCH":
        wrong_lt = "yes" if term == "st" else "no"
        extra = {"corrected": 7000.0} if kind == "codeb" else {}
        acts = h.sale(acts, kind, term, proceeds=2000, basis=8000, wash=0, tag=tag, long_term=wrong_lt, **extra)
        loss = True
    elif variant == "CODE_B_WITHOUT_CORRECTION":
        acts = h.sale(acts, kind, term, proceeds=2000, basis=3000, corrected=3000, wash=0, tag=tag)
        loss = True
    elif variant in ("CODE_W_ON_GAIN", "CODE_W_ON_BREAKEVEN"):
        if kind == "codeb":
            proceeds = 4000 if variant == "CODE_W_ON_GAIN" else 2500
            acts = h.sale(acts, kind, term, proceeds=proceeds, basis=3000, corrected=2500, wash=500, tag=tag)
        else:
            proceeds = 3000 if variant == "CODE_W_ON_GAIN" else 2000
            acts = h.sale(acts, kind, term, proceeds=proceeds, basis=2000, wash=500, tag=tag)
        loss = False
    elif variant == "ADJUSTMENT_EXCEEDS_LOSS":
        if kind == "codeb":
            acts = h.sale(acts, kind, term, proceeds=2000, basis=4000, corrected=3000, wash=1500, tag=tag)
        else:
            acts = h.sale(acts, kind, term, proceeds=2000, basis=3000, wash=1500, tag=tag)
        loss = True
    else:
        raise ValueError(f"Unknown variant: {variant}")

    acts = h.answer(acts, **h.honest({kind}, loss=loss, new_questions=False))
    return add_standard_answers(acts, core, h, ccr, has_1099b=has_1099b, tag=tag)


def build_two_sale_case(core: Any, h: Any, ccr: Any) -> list[dict[str, Any]]:
    acts = h.opened()
    acts = h.sale(acts, "w", "st", proceeds=2000, basis=3000, wash=500, tag="demo.sbe.two.good")
    acts = h.sale(acts, "w", "st", proceeds=3000, basis=2000, wash=500, tag="demo.sbe.two.bad")
    acts = h.answer(acts, **h.honest({"w"}, loss=True, new_questions=False))
    return add_standard_answers(acts, core, h, ccr, has_1099b=True, tag="two")


CASES = [
    ("w", "st", ["valid_loss", "BOX_1G_FLAG_WITHOUT_AMOUNT", "BOX_1G_AMOUNT_WITHOUT_FLAG", "CODE_W_ON_GAIN", "ADJUSTMENT_EXCEEDS_LOSS"]),
    ("w", "lt", ["valid_loss", "BOX_1G_FLAG_WITHOUT_AMOUNT", "BOX_1G_AMOUNT_WITHOUT_FLAG", "CODE_W_ON_GAIN", "ADJUSTMENT_EXCEEDS_LOSS"]),
    ("noncovered", "st", ["valid_loss", "BASIS_WAS_REPORTED", "HOLDING_PERIOD_MISMATCH", "CODE_W_ON_GAIN", "ADJUSTMENT_EXCEEDS_LOSS"]),
    ("noncovered", "lt", ["valid_loss", "BASIS_WAS_REPORTED", "HOLDING_PERIOD_MISMATCH", "CODE_W_ON_GAIN", "ADJUSTMENT_EXCEEDS_LOSS"]),
    ("no1099b", "st", ["valid_loss", "HOLDING_PERIOD_MISMATCH", "CODE_W_ON_GAIN", "ADJUSTMENT_EXCEEDS_LOSS"]),
    ("no1099b", "lt", ["valid_loss", "HOLDING_PERIOD_MISMATCH", "CODE_W_ON_GAIN", "ADJUSTMENT_EXCEEDS_LOSS"]),
    ("codeb", "st", ["valid_loss", "HOLDING_PERIOD_MISMATCH", "CODE_B_WITHOUT_CORRECTION", "CODE_W_ON_GAIN", "ADJUSTMENT_EXCEEDS_LOSS"]),
    ("codeb", "lt", ["valid_loss", "HOLDING_PERIOD_MISMATCH", "CODE_B_WITHOUT_CORRECTION", "CODE_W_ON_GAIN", "ADJUSTMENT_EXCEEDS_LOSS"]),
]


def run_probe(repo_root: Path, version: str, registry: str, release: str) -> dict[str, Any]:
    if str(repo_root) not in sys.path:
        sys.path.insert(0, str(repo_root))
    from packages.derivation.live import live_coordinate_run
    from packages.derivation.live_workspace import WorkspaceCapability
    from tests.helpers import current_core_returns as ccr

    h = _load_module(
        "sbe_audit_harness",
        repo_root / "docs/phases/engine-breadth/milestones/sale-family-audit-evidence/audit_harness.py",
    )
    core = h.Core(version, registry, release)
    surface = core.surface()
    out: dict[str, Any] = {}

    def _exec(name: str, acts: list[dict[str, Any]]) -> dict[str, Any]:
        finished = h._handover(
            h._finish(
                copy.deepcopy(acts),
                package_path=core.package_path,
                package_version=core.version,
                release_path=core.release_path,
                release_version=core.release_version,
                note=name,
            ),
            surface=surface,
            reconfirm=True,
        )
        with TemporaryDirectory() as tmp:
            outcome = live_coordinate_run(
                WorkspaceCapability(Path(tmp) / "L"),
                repo_root=repo_root,
                authoritative_acts=finished,
                workspace_revision=len(finished),
                run_scope={"jurisdiction": "us", "year": h.YEAR},
                scope_user=ccr.USER,
                request={"schema": "run-request.v1"},
                run_id=f"demo.sbe.{core.version}.{name}",
                governance_pins=[],
                surface=surface,
                output_name="out.json",
            )
            if outcome.refusal:
                return {"refusal": outcome.refusal.reason, "detail": str(outcome.refusal.detail)}
            model = json.loads(outcome.presentation_path.read_text(encoding="utf-8"))
            blocked = [s for s in model["sections"] if s["resolved"]["disposition"] == "blocked"]
            return {
                "blocked_sections_count": len(blocked),
                "question_groups_count": len(model.get("questionGroups", [])),
                "sample_section": blocked[0]["field"]["id"] if blocked else None,
                "sample_reasons": blocked[0]["resolved"].get("reasons", []) if blocked else [],
                "sample_question_refs": blocked[0]["resolved"].get("questionRefs", []) if blocked else [],
                "question_groups": model.get("questionGroups", []),
            }

    for kind, term, variants in CASES:
        for variant in variants:
            cname = f"{kind}.{term}.{variant}"
            out[cname] = _exec(cname, build_sale_case(kind, term, variant, core, h, ccr))
    out["two_sale_disambiguation"] = _exec("two_sale_disambig", build_two_sale_case(core, h, ccr))
    return out


def main() -> None:
    parser = argparse.ArgumentParser(description="Probe sale-family member-validation blocks on synthetic demo.* cases.")
    parser.add_argument("--repo", type=Path, default=REPO)
    parser.add_argument("--core", default="v105")
    parser.add_argument("--registry", default="v103")
    parser.add_argument("--release", default="v103")
    parser.add_argument("--out", type=Path, default=None)
    args = parser.parse_args()

    result = run_probe(args.repo.resolve(), args.core, args.registry, args.release)
    payload = json.dumps(result, indent=2) + "\n"
    if args.out is not None:
        args.out.write_text(payload, encoding="utf-8")
    else:
        print(payload)


if __name__ == "__main__":
    main()
