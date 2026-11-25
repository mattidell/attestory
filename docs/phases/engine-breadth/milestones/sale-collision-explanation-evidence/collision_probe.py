"""Synthetic probe for cross-family sale identity-exclusivity collisions.

Imports sibling ``audit_harness.py`` by file path under a unique module name so
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

REPO = Path(__file__).resolve().parents[5]
P = "tax.us.2025."
BOX4 = P + "f1099b.statement-box4-withholding-reported"
BOX7 = P + "f1099b.statement-box7-loss-not-allowed"
NO_SALE_BOX4 = P + "f1099b.no-sale-box4-present"

# All 18 declared identity_exclusivity pairs on published core v106:
# (declaring_kind, declaring_term, counterpart_kind, counterpart_term, excl_id)
DECLARED_PAIRS: tuple[tuple[str, str, str, str, str], ...] = (
    ("w", "st", "covered", "st", P + "block.covered-w.identity-key-collision"),
    ("w", "lt", "covered", "lt", P + "block.covered-w.identity-key-collision"),
    ("noncovered", "st", "covered", "st", P + "block.noncovered-st-txn.excludes.covered-st"),
    ("noncovered", "st", "w", "st", P + "block.noncovered-st-txn.excludes.covered-w-st"),
    ("noncovered", "lt", "covered", "lt", P + "block.noncovered-lt-txn.excludes.covered-lt"),
    ("noncovered", "lt", "w", "lt", P + "block.noncovered-lt-txn.excludes.covered-w-lt"),
    ("codeb", "st", "covered", "st", P + "block.code-b-st-txn.excludes.covered-st"),
    ("codeb", "st", "w", "st", P + "block.code-b-st-txn.excludes.covered-w-st"),
    ("codeb", "st", "noncovered", "st", P + "block.code-b-st-txn.excludes.noncovered-st"),
    ("codeb", "st", "covered", "lt", P + "block.code-b-st-txn.excludes.covered-lt"),
    ("codeb", "st", "w", "lt", P + "block.code-b-st-txn.excludes.covered-w-lt"),
    ("codeb", "st", "noncovered", "lt", P + "block.code-b-st-txn.excludes.noncovered-lt"),
    ("codeb", "lt", "covered", "st", P + "block.code-b-lt-txn.excludes.covered-st"),
    ("codeb", "lt", "w", "st", P + "block.code-b-lt-txn.excludes.covered-w-st"),
    ("codeb", "lt", "noncovered", "st", P + "block.code-b-lt-txn.excludes.noncovered-st"),
    ("codeb", "lt", "covered", "lt", P + "block.code-b-lt-txn.excludes.covered-lt"),
    ("codeb", "lt", "w", "lt", P + "block.code-b-lt-txn.excludes.covered-w-lt"),
    ("codeb", "lt", "noncovered", "lt", P + "block.code-b-lt-txn.excludes.noncovered-lt"),
)


def _load_module(name: str, path: Path) -> Any:
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def add_standard_answers(
    acts: list[dict[str, Any]],
    core: Any,
    h: Any,
    ccr: Any,
    *,
    tag: str,
    omit_over_65: bool = False,
) -> list[dict[str, Any]]:
    acts = ccr.state_taxpayer_facts(acts, core="v88")
    if omit_over_65:
        acts = h.strip(acts, P + "taxpayer-over-65")
    acts = h.say(acts, NO_SALE_BOX4, "no", f"{tag}.nsb4", core.content)
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
            h._add(acts, "assertion", {"finding": h._attested(f"demo.sce.{tag}.{short}.{idx}", fact_id, "no")})
    return h.renumber(acts)


def _add_sale_for_kind(
    acts: list[dict[str, Any]],
    h: Any,
    kind: str,
    term: str,
    *,
    tag: str,
    gain_for_w: bool = False,
) -> list[dict[str, Any]]:
    if kind == "covered":
        return h.sale(acts, "covered", term, proceeds=2000, basis=3000, tag=tag)
    if kind == "w":
        proceeds = 4000 if gain_for_w else 2000
        basis = 3000
        return h.sale(acts, "w", term, proceeds=proceeds, basis=basis, wash=500, tag=tag)
    if kind == "noncovered":
        return h.sale(acts, "noncovered", term, proceeds=2000, basis=3000, wash=0, tag=tag)
    if kind == "codeb":
        return h.sale(acts, "codeb", term, proceeds=2000, basis=4000, corrected=3000, wash=0, tag=tag)
    raise ValueError(f"Unsupported sale kind: {kind}")


def build_collision_pair(
    kind_a: str,
    term_a: str,
    kind_b: str,
    term_b: str,
    core: Any,
    h: Any,
    ccr: Any,
    *,
    distinct_identity: bool = False,
    omit_over_65: bool = False,
    gain_for_w: bool = False,
) -> list[dict[str, Any]]:
    tag = f"sce.{kind_a}.{term_a}.vs.{kind_b}.{term_b}"
    if distinct_identity:
        tag += ".distinct"
    if omit_over_65:
        tag += ".no65"
    if gain_for_w:
        tag += ".wgain"
    tag_a = f"{tag}.a" if distinct_identity else tag
    tag_b = f"{tag}.b" if distinct_identity else tag
    acts = h.opened()
    acts = _add_sale_for_kind(acts, h, kind_a, term_a, tag=tag_a, gain_for_w=gain_for_w)
    acts = _add_sale_for_kind(acts, h, kind_b, term_b, tag=tag_b, gain_for_w=gain_for_w)
    acts = h.answer(acts, **h.honest({kind_a, kind_b}, loss=not gain_for_w, new_questions=False))
    return add_standard_answers(acts, core, h, ccr, tag=tag, omit_over_65=omit_over_65)


def build_three_way_collision(core: Any, h: Any, ccr: Any) -> list[dict[str, Any]]:
    """Same sale entered in covered-w-st, noncovered-st, and code-b-st (both noncovered-st and code-b-st block)."""
    tag = "sce.three_way.st"
    acts = h.opened()
    acts = _add_sale_for_kind(acts, h, "w", "st", tag=tag)
    acts = _add_sale_for_kind(acts, h, "noncovered", "st", tag=tag)
    acts = _add_sale_for_kind(acts, h, "codeb", "st", tag=tag)
    acts = h.answer(acts, **h.honest({"w", "noncovered", "codeb"}, loss=True, new_questions=False))
    return add_standard_answers(acts, core, h, ccr, tag=tag)


def run_probe(repo_root: Path, version: str, registry: str, release: str) -> dict[str, Any]:
    if str(repo_root) not in sys.path:
        sys.path.insert(0, str(repo_root))
    from packages.derivation.live import live_coordinate_run
    from packages.derivation.live_workspace import WorkspaceCapability
    from packages.derivation.presentation_projection import validate_presentation_model
    from tests.helpers import current_core_returns as ccr

    h = _load_module(
        "sce_audit_harness",
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
                run_id=f"demo.sce.{core.version}.{name}",
                governance_pins=[],
                surface=surface,
                output_name="out.json",
            )
            if outcome.refusal:
                return {"refusal": outcome.refusal.reason, "detail": str(outcome.refusal.detail)}
            report = json.loads(outcome.output_path.read_text(encoding="utf-8"))
            model = json.loads(outcome.presentation_path.read_text(encoding="utf-8"))
            validate_presentation_model(model)
            mv_blocks = [
                {
                    "artifact_id": row.get("artifact_id"),
                    "code": row.get("code"),
                    "missing": row.get("missing"),
                }
                for row in report.get("dispositions") or []
                if row.get("disposition") == "blocked"
                and str(row.get("artifact_id") or "").endswith(".member-validation.synthesized")
            ]
            blocked = [s for s in model["sections"] if s["resolved"]["disposition"] == "blocked"]
            reason_shapes: dict[str, list[str]] = {}
            for s in blocked:
                key = json.dumps(s["resolved"].get("reasons", []), sort_keys=True)
                reason_shapes.setdefault(key, []).append(s["field"]["id"])
            return {
                "member_validation_blocks": mv_blocks,
                "blocked_sections_count": len(blocked),
                "question_groups_count": len(model.get("questionGroups", [])),
                "question_groups": model.get("questionGroups", []),
                "sample_section": blocked[0]["field"]["id"] if blocked else None,
                "sample_reasons": blocked[0]["resolved"].get("reasons", []) if blocked else [],
                "sample_question_refs": blocked[0]["resolved"].get("questionRefs", []) if blocked else [],
                "distinct_reason_shapes": {k: len(v) for k, v in reason_shapes.items()},
                "attachments_blocked": [
                    a["id"] for a in model.get("attachments", [])
                    if (a.get("resolved") or {}).get("disposition") == "blocked"
                ],
            }

    for kind_a, term_a, kind_b, term_b, _excl_id in DECLARED_PAIRS:
        cname = f"pair.{kind_a}_{term_a}.vs.{kind_b}_{term_b}"
        out[cname] = _exec(cname, build_collision_pair(kind_a, term_a, kind_b, term_b, core, h, ccr))

    out["three_way.w_st.noncovered_st.codeb_st"] = _exec(
        "three_way_st", build_three_way_collision(core, h, ccr)
    )
    out["mixed.w_st.vs.covered_st.unanswered_over_65"] = _exec(
        "mixed_unanswered", build_collision_pair("w", "st", "covered", "st", core, h, ccr, omit_over_65=True)
    )
    out["mixed.w_st.vs.covered_st.code_w_on_gain"] = _exec(
        "mixed_code_w_on_gain", build_collision_pair("w", "st", "covered", "st", core, h, ccr, gain_for_w=True)
    )
    out["control.w_st.vs.covered_st.distinct"] = _exec(
        "control_distinct", build_collision_pair("w", "st", "covered", "st", core, h, ccr, distinct_identity=True)
    )
    return out


def main() -> None:
    parser = argparse.ArgumentParser(description="Probe cross-family sale collisions on synthetic demo.* cases.")
    parser.add_argument("--repo", type=Path, default=REPO)
    parser.add_argument("--core", default="v106")
    parser.add_argument("--registry", default="v104")
    parser.add_argument("--release", default="v104")
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
