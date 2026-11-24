"""P0 trace: a code W adjustment on a gain, a break-even and a loss.

Evidence for docs/phases/engine-breadth/milestones/code-w-gain-question.md.
Charter: docs/reviews/code-w-gain-question/charter-p0.md.

Twelve synthetic demo.* returns, one sale each: covered code W (Form 8949
box A or D) and noncovered (box B or E), short and long term, with a
positive box 1g amount on a gain (proceeds above basis), a break-even
(proceeds equal basis) and a loss the adjustment does not exceed. Each
runs once through live_coordinate_run on published core v103 (registry
v101, release v101). The saved page is the real renderer. Root tuples are
blocked rows whose missing names are not themselves blocked symbols.

Run: python3 trace.py [--only KEY] [--workers N] [--out PATH]
Nothing in packages/ or tests/ is edited. The audit harness is loaded by
path under a unique name.
"""
from __future__ import annotations

import argparse
import copy
import importlib.util
import json
import multiprocessing
import os
import sys
import time
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))


def _load(name: str, path: Path) -> Any:
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


h = _load(
    "cwg_p0_audit_harness",
    REPO / "docs/phases/engine-breadth/milestones/sale-family-audit-evidence/audit_harness.py",
)

from packages.derivation.live import live_coordinate_run  # noqa: E402
from packages.derivation.live_session import _render_page  # noqa: E402

P = h.P
CORE = h.Core("v103", "v101", "v101")

# proceeds, basis, box 1g. Gain and break-even are the ADR-0062 bound
# (g > 0 and proceeds >= basis). The loss keeps g inside the loss.
SHAPES: dict[str, dict[str, float]] = {
    "gain": {"proceeds": 25000.0, "basis": 5000.0, "wash": 500.0},
    "break-even": {"proceeds": 8000.0, "basis": 8000.0, "wash": 500.0},
    "loss": {"proceeds": 1000.0, "basis": 4000.0, "wash": 500.0},
}
PATHS = ("covered", "noncovered")
TERMS = ("st", "lt")

# Where the page walk turns a block into a sentence or a question group.
WALK = {
    "constraint_meanings": "packages/derivation/presentation_projection.py:419",
    "meaning_for": "packages/derivation/presentation_projection.py:766",
    "explain": "packages/derivation/presentation_projection.py:819",
    "reach_mixed": "packages/derivation/presentation_projection.py:829",
    "reach_plain": "packages/derivation/presentation_projection.py:875",
    "question_refs": "packages/derivation/presentation_projection.py:1010",
    "field_reasons": "packages/derivation/presentation_projection.py:5561",
    "question_groups": "packages/derivation/presentation_projection.py:5634",
    "validation_missing": "packages/derivation/runner.py:1915",
    "recorded_code": "packages/derivation/runner.py:2545",
    "synthesized_rule": "packages/derivation/package_validation.py:1677",
    "expression_block_missing": "packages/derivation/evaluator.py:512",
}


def keys() -> list[str]:
    return [f"{path}/{term}/{shape}" for path in PATHS for term in TERMS for shape in SHAPES]


def kind_of(path: str) -> str:
    return "w" if path == "covered" else "noncovered"


def build(key: str) -> h.Acts:
    path, term, shape = key.split("/")
    spec = SHAPES[shape]
    kind = kind_of(path)
    acts = h.opened()
    acts = h.sale(
        acts, kind, term,
        proceeds=spec["proceeds"], basis=spec["basis"], wash=spec["wash"],
        tag=f"cwg-{path}-{term}-{shape}",
    )
    answers = h.honest({kind}, loss=spec["proceeds"] < spec["basis"])
    answers.update(h.honest_exception1(acts))
    answers.update({"lines_18_19": "yes", "no_other_sd": "yes", "no_da_qof": "yes"})
    acts = h.answer(acts, **answers)
    acts = h.say(acts, P + "f1099b.no-sale-box4-present", "no", "cwg-no-sale-box4")
    acts = statement_answers(acts)
    acts = h.say(acts, P + "filing-status", "single", "cwg-status")
    for fact in ("taxpayer-over-65", "taxpayer-blind"):
        acts = h.say(acts, P + fact, False, "cwg-" + fact)
    return h.renumber(acts)


def statement_answers(acts: h.Acts) -> h.Acts:
    """Box 4 and box 7 on each recorded Form 1099-B statement: no and no."""
    statements = list(dict.fromkeys(
        str(a["payload"]["entity"]["id"]) for a in acts
        if a.get("kind") == "entity-introduced"
        and a["payload"]["entity"].get("kind") == "tax.us.f1099b-statement"
    ))
    if not statements:
        return acts
    h.adopt(acts, "f1099b-statement-boxes.bundle.json")
    for statement in statements:
        for slug in ("statement-box4-withholding-reported", "statement-box7-loss-not-allowed"):
            fact_id = h.fact_id_for(
                P + "f1099b." + slug, (("statement", statement), ("tax-year", h.YEAR)),
            )
            h._add(acts, "assertion", {
                "finding": h._attested(f"demo.cwg.{slug}.{statement}", fact_id, "no"),
            })
    return h.renumber(acts)


def _roots(model: dict[str, Any]) -> list[dict[str, Any]]:
    nodes = model.get("dispositionNodes") or {}
    blocked: dict[str, list[dict[str, Any]]] = {}
    for symbol, node in nodes.items():
        if not isinstance(node, dict):
            continue
        for record in node.get("records") or []:
            if isinstance(record, dict) and record.get("disposition") == "blocked":
                blocked.setdefault(str(symbol), []).append(record)
    roots = []
    for symbol, records in blocked.items():
        for record in records:
            missing = [str(item) for item in record.get("missing") or []]
            if any(name in blocked for name in missing):
                continue
            roots.append({
                "symbol": symbol.removeprefix(P),
                "artifact": str(record.get("artifact_id") or "").removeprefix(P),
                "code": record.get("code"),
                "missing": missing,
            })
    roots.sort(key=lambda row: (row["artifact"], row["symbol"], row["code"] or ""))
    return roots


def _page(model: dict[str, Any]) -> list[dict[str, Any]]:
    groups = {
        str(group.get("id")): group
        for group in model.get("questionGroups") or []
        if isinstance(group, dict)
    }
    rows = []
    for section in model.get("sections") or []:
        if not isinstance(section, dict):
            continue
        resolved = section.get("resolved") or {}
        reasons = [
            str(reason.get("sentence") or "")
            for reason in resolved.get("reasons") or []
            if isinstance(reason, dict) and str(reason.get("sentence") or "").strip()
        ]
        refs = resolved.get("questionRefs") or []
        if not reasons and not refs and resolved.get("disposition") != "blocked":
            continue
        field = section.get("field") or {}
        fid = str(field.get("id") or "").removeprefix(P)
        if not any(token in fid for token in ("schedule-d.", "form1040.line-7a", "form1040.line-15", "form1040.line-16")):
            if not reasons and not refs:
                continue
        linked = []
        for ref in refs:
            if not isinstance(ref, dict):
                continue
            group = groups.get(str(ref.get("groupId")))
            target = (group or {}).get("answerTarget") or {}
            linked.append({
                "question": ref.get("question"),
                "factTypeId": str(target.get("factTypeId") or "").removeprefix(P),
                "status": (group or {}).get("answerStatus"),
            })
        if reasons or linked or "schedule-d.line-1" in fid or "schedule-d.line-2" in fid or "schedule-d.line-8" in fid or "schedule-d.line-9" in fid or "schedule-d.line-16" in fid or "form1040.line-7a" in fid:
            rows.append({
                "field": fid,
                "disposition": resolved.get("disposition"),
                "sentences": [h.scrub(text)[:240] for text in reasons],
                "questions": linked,
            })
    return rows


LINE_FIELDS = (
    "schedule-d.line-1b",
    "schedule-d.line-2",
    "schedule-d.line-7",
    "schedule-d.line-8b",
    "schedule-d.line-9",
    "schedule-d.line-16",
    "schedule-d.line-21",
    "form1040.line-7a",
    "form1040.line-16",
)


def _lines(model: dict[str, Any]) -> list[dict[str, Any]]:
    rows = []
    for section in model.get("sections") or []:
        if not isinstance(section, dict):
            continue
        field = section.get("field") or {}
        fid = str(field.get("id") or "").removeprefix(P)
        if fid not in LINE_FIELDS:
            continue
        resolved = section.get("resolved") or {}
        row: dict[str, Any] = {"field": fid, "disposition": resolved.get("disposition")}
        if "value" in resolved:
            row["value"] = resolved["value"]
        rows.append(row)
    return rows


def observe(key: str, core: Any | None = None) -> dict[str, Any]:
    chosen = CORE if core is None else core
    acts = build(key)
    run_id = "demo.cwg.p0." + key.replace("/", ".")
    surface = chosen.surface()
    finished = h._handover(
        h._finish(
            copy.deepcopy(acts),
            package_path=chosen.package_path,
            package_version=chosen.version,
            release_path=chosen.release_path,
            release_version=chosen.release_version,
            note=run_id,
        ),
        surface=surface,
        reconfirm=True,
    )
    with TemporaryDirectory() as tmp:
        capability = h.WorkspaceCapability(Path(tmp) / "L")
        with h.loader_entries(chosen):
            outcome = live_coordinate_run(
                capability, repo_root=REPO, authoritative_acts=finished,
                workspace_revision=len(finished),
                run_scope={"jurisdiction": "us", "year": h.YEAR},
                scope_user=h.ccr.USER, request={"schema": "run-request.v1"},
                run_id=run_id, governance_pins=[], surface=surface, output_name="out.json",
            )
        if outcome.refusal is not None:
            return {"refusal": outcome.refusal.reason, "detail": h.scrub(str(outcome.refusal.detail))[:300]}
        report = json.loads(outcome.output_path.read_text(encoding="utf-8"))
        model = json.loads(outcome.presentation_path.read_text(encoding="utf-8"))
        page = Path(tmp) / "page.html"
        page.write_bytes(_render_page(REPO, capability, outcome.presentation_path))
        text = page.read_text(encoding="utf-8")
        marker = "const MODEL = Object.freeze("
        saved, _ = json.JSONDecoder().raw_decode(text, text.index(marker) + len(marker))
        assert saved == model, "saved page model differs from the presentation model"
    validation = [
        {
            "artifact": str(row.get("artifact_id") or "").removeprefix(P),
            "code": row.get("code"),
            "missing": list(row.get("missing") or []),
        }
        for row in report.get("dispositions") or []
        if isinstance(row, dict)
        and str(row.get("artifact_id") or "").endswith(".member-validation.synthesized")
        and row.get("disposition") == "blocked"
    ]
    interesting = []
    for row in report.get("dispositions") or []:
        if not isinstance(row, dict) or row.get("disposition") != "blocked":
            continue
        missing = [str(item) for item in row.get("missing") or []]
        artifact = str(row.get("artifact_id") or "")
        if any(token in artifact for token in ("member-validation", "schedule-d-line", "form1040-line7a", "form1040-line16")) or any(
            token in " ".join(missing) for token in ("CODE_W", "ADJUSTMENT_EXCEEDS", "BOX_1G")
        ):
            interesting.append({
                "artifact": artifact.removeprefix(P),
                "code": row.get("code"),
                "missing": missing,
            })
    return {
        "stop": report.get("stop_reason"),
        "validation": validation,
        "blocked_focus": interesting,
        "roots": _roots(model),
        "page": _page(model),
        "lines": _lines(model),
        "question_group_count": len(model.get("questionGroups") or []),
    }


def worker(shard: list[str]) -> list[tuple[str, dict[str, Any]]]:
    out = []
    for key in shard:
        try:
            out.append((key, observe(key)))
        except Exception as exc:  # noqa: BLE001 - a rejected return is a result
            out.append((key, {"error": type(exc).__name__, "message": h.scrub(str(exc))[:500]}))
    return out


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--only", action="append")
    parser.add_argument("--workers", type=int, default=max(1, (os.cpu_count() or 2) - 1))
    parser.add_argument("--out", default=str(HERE / "trace.json"))
    args = parser.parse_args()
    todo = args.only or keys()
    started = time.monotonic()
    workers = min(args.workers, len(todo))
    if workers <= 1:
        found = dict(worker(todo))
    else:
        with multiprocessing.get_context("spawn").Pool(workers) as pool:
            found = dict(
                pair
                for part in pool.map(worker, [todo[i::workers] for i in range(workers)])
                for pair in part
            )
    body = {
        "core": {"package": CORE.version, "registry": CORE.registry, "release": CORE.release_version},
        "walk": WALK,
        "wall_time_s": round(time.monotonic() - started, 1),
        "runs": {key: found[key] for key in todo},
    }
    text = json.dumps(body, indent=2, sort_keys=True) + "\n"
    json.loads(text)
    Path(args.out).write_text(text, encoding="utf-8")
    print(json.dumps({"runs": len(found), "bytes": len(text), "wall_time_s": body["wall_time_s"]}))


if __name__ == "__main__":
    main()
