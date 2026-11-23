"""Track 1 census of first-read visible page text across 775 recorded lists + synthetic pages.

Renders every recorded act list on published core v101 (registry v99, release v99)
through live_coordinate_run and live_session._render_page, executes the real page
script via check_page_dom.mjs, and reports per-list leaks of engine enums, raw
symbols, rule/finding/fact IDs, or codes in first-read visible text (outside
collapsed <details class="technical-details"> / <details class="audit-ids"> and
attributes). Also checks synthetic mortgage interest, mortgage borrowing, and
line 21 pages.

Usage:
    python3 track1_census.py <outside-repo-scratch-dir> [--page <path>] [--core v101] [--out <path>]
"""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import time
from typing import Any

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from packages.derivation.live_session import _render_page
from tools import recorded_replay as rr

DEFAULT_PAGE = REPO / "packages/presentation/pages/citation-walk.v1.html"
NODE_CHECKER = HERE / "check_page_dom.mjs"
LOCAL_PATH_RE = re.compile(r"/(?:Users|private|tmp|var|opt)/")


def _check_models_with_node(page_path: Path, items: list[tuple[str, dict[str, Any]]]) -> dict[str, Any]:
    if not items:
        return {}
    payload = "\n".join(json.dumps({"key": k, "model": m}, separators=(",", ":")) for k, m in items) + "\n"
    proc = subprocess.run(
        ["node", str(NODE_CHECKER), str(page_path)],
        input=payload,
        text=True,
        capture_output=True,
        timeout=120,
        check=True,
    )
    return dict(json.loads(proc.stdout))


def _per_list(key: str, acts: list[dict[str, Any]], core: Any) -> dict[str, Any]:
    resolved = rr.resolve_core(core)
    harness = rr._get_harness()
    slug = hashlib.sha256(key.encode("utf-8")).hexdigest()[:20]
    run_id = "demo.ppw.t1." + slug
    page_path = Path(os.environ["PPW_T1_PAGE_PATH"])
    try:
        with harness.loader_entries(resolved):
            finished = harness._finish(
                acts,
                package_path=resolved.package_path,
                package_version=resolved.version,
                release_path=resolved.release_path,
                release_version=resolved.release_version,
                note=run_id,
            )
            finished = harness._handover(finished, surface=resolved.surface(), reconfirm=True)
            with tempfile.TemporaryDirectory() as tmp:
                cap = harness.WorkspaceCapability(Path(tmp) / "L")
                outcome = harness.live_coordinate_run(
                    cap,
                    repo_root=REPO,
                    authoritative_acts=finished,
                    workspace_revision=len(finished),
                    run_scope={"jurisdiction": "us", "year": harness.YEAR},
                    scope_user=harness.ccr.USER,
                    request={"schema": "run-request.v1"},
                    run_id=run_id,
                    governance_pins=[],
                    surface=resolved.surface(),
                    output_name="out.json",
                )
                if outcome.refusal is not None:
                    return {"outcome": "refused", "error": "refusal", "message": str(outcome.refusal.reason)}
                assert outcome.presentation_path is not None
                _render_page(REPO, cap, outcome.presentation_path)
                model = json.loads(outcome.presentation_path.read_text(encoding="utf-8"))
                after = _check_models_with_node(page_path, [(key, model)])[key]
                out: dict[str, Any] = {"outcome": "success", "after": after}
                before_env = os.environ.get("PPW_T1_BEFORE_PAGE_PATH")
                if before_env:
                    out["before"] = _check_models_with_node(Path(before_env), [(key, model)])[key]
                return out
    except Exception as exc:
        clean = re.sub(r"/(?:Users|private|tmp|var|opt)/\S+", "<path>", str(exc))[:400]
        return {"outcome": "error", "error": type(exc).__name__, "message": clean}


def _synthetic_models() -> list[tuple[str, dict[str, Any]]]:
    """Build synthetic mortgage interest, mortgage borrowing, and line 21 models."""
    models: list[tuple[str, dict[str, Any]]] = []
    # 1. Mortgage interest (qualified + box9 default)
    from tests.test_f1098_circumstances_calculation import _run as f1098_run

    _, mort_int_model, _ = f1098_run("demo-ppw-mort-int", 20000.0, omit_box9=True)
    models.append(("synthetic/mortgage-interest-qualified-default", mort_int_model))

    # 2. Mortgage borrowing (v4 with payment comparison, conflict, reasonChain, relationships, effectiveAnswers, groups, orphans)
    mort_borr_model: dict[str, Any] = {
        "schema": "presentation-model.v1",
        "runId": "demo.ppw.mort-borr",
        "sections": [],
        "mortgageBorrowingExplanation": {
            "schema": "mortgage-borrowing-explanation.v4",
            "reports": [{
                "payer": "demo.lender",
                "statement": "demo.statement",
                "taxYear": "2025",
                "statementLabel": {"lender": "Demo lender", "statement": "Demo statement", "taxYear": "2025"},
                "reportedInterest": {"findingId": "demo.box1", "value": 22000},
                "boxObservations": [],
                "reasonChain": {"value": "All criteria satisfied.", "pins": [{"id": "demo.pin.reason"}]},
                "localAnswers": [],
                "paymentComparisons": [{
                    "findingId": "demo.comparison",
                    "value": "different-payments",
                    "title": "All payments are separate",
                    "peer": None,
                    "peerIdentityStatus": "unavailable",
                    "applicability": "unresolved-applicability",
                    "supportFindingIds": ["demo.support.1"],
                    "explanation": "This recorded comparison cannot be used because the peer report identity is unavailable.",
                }],
                "answerConflicts": [{
                    "question": "Is this the original loan?",
                    "local": {"scope": "this exact Form 1098", "findingId": "demo.local.original", "factType": "demo.local", "value": "no"},
                    "shared": {"scope": "this named borrowing for 2025", "findingId": "demo.shared.original", "factType": "demo.shared", "value": "yes"},
                    "correctionGuidance": "Review both answers.",
                }],
                "relationships": [{"disposition": "published", "response": "yes"}],
                "effectiveAnswers": [{
                    "findingId": "demo.eff.1",
                    "title": "Home is collateral",
                    "value": "yes",
                    "pins": [],
                    "consumption": "consumed",
                }],
            }],
            "groups": [{
                "borrowing": "demo.borrowing.1",
                "borrowingLabel": "Main home loan",
                "consumedFindingIds": ["demo.claim.1"],
                "recordedApplicableClaims": {
                    "demo.claim.type": {"findingId": "demo.claim.1", "title": "Loan purpose", "value": "yes"},
                },
            }],
            "line8aDispositions": [{"artifact_id": "tax.us.2025.rule.f1098-line8a", "disposition": "blocked"}],
            "line8aFindings": [],
            "calculationChain": {"publications": [], "dispositions": [], "resolvedContent": []},
            "orphanRelationships": [{"statement": "Prior Form 1098", "taxYear": "2025", "disposition": "withdrawn", "response": "no"}],
        },
    }
    models.append(("synthetic/mortgage-borrowing-v4", mort_borr_model))

    # 3. Line 21 (C1 published with working parameters + run footer)
    from tests.test_sli_line21_explanation_page import _saved_model as line21_saved

    models.append(("synthetic/line21-c1", line21_saved("C1")))
    return models


def _write_clean_json(path: Path, payload: dict[str, Any]) -> None:
    text = json.dumps(payload, indent=2) + "\n"
    if LOCAL_PATH_RE.search(text):
        raise ValueError(f"Refusing to write local path into {path}")
    path.write_text(text, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Track 1 first-read leak census.")
    parser.add_argument("scratch", type=Path, help="Outside-repo directory for resumable part file")
    parser.add_argument("--page", type=Path, default=DEFAULT_PAGE, help="HTML page to evaluate (after)")
    parser.add_argument("--before-page", type=Path, default=None, help="Optional HTML page to evaluate (before)")
    parser.add_argument("--core", default="v101", help="Published core version (default: v101)")
    parser.add_argument("--workers", type=int, default=None)
    parser.add_argument("--part-name", default="track1-census-part.json")
    parser.add_argument("--out", type=Path, default=HERE / "track1-census.json")
    parser.add_argument("--skip-synthetic", action="store_true")
    args = parser.parse_args()

    scratch = args.scratch.resolve()
    if scratch == REPO or REPO in scratch.parents:
        raise SystemExit("scratch directory must be outside the repository")
    scratch.mkdir(parents=True, exist_ok=True)
    os.environ["PPW_T1_PAGE_PATH"] = str(args.page.resolve())
    if args.before_page is not None:
        os.environ["PPW_T1_BEFORE_PAGE_PATH"] = str(args.before_page.resolve())
    else:
        os.environ.pop("PPW_T1_BEFORE_PAGE_PATH", None)

    lists = rr.recorded_lists()
    core = rr.resolve_core(args.core)
    workers = args.workers or max(1, (os.cpu_count() or 2) - 1)
    part_path = scratch / args.part_name

    started = time.monotonic()
    results = rr.replay(lists, core, _per_list, workers=workers, part=part_path)
    wall = round(time.monotonic() - started, 3)

    outcomes = Counter(r["outcome"] for r in results.values())
    errors = Counter(r.get("error") for r in results.values() if r["outcome"] != "success")

    def _aggregate(side: str) -> dict[str, Any]:
        lists_with_leaks = 0
        total_leaks = 0
        lists_with_content_matches = 0
        total_content_matches = 0
        section_errors_total = 0
        leak_kinds: Counter[str] = Counter()
        sample_leaks: list[dict[str, Any]] = []
        sample_content: list[dict[str, Any]] = []
        for key, row in sorted(results.items()):
            if row["outcome"] != "success" or side not in row:
                continue
            item_res = row[side]
            section_errors_total += int(item_res["section_errors"])
            n_leaks = int(item_res["total_first_read_leaks"])
            if n_leaks > 0:
                lists_with_leaks += 1
                total_leaks += n_leaks
                for leak in item_res.get("sample_leaks") or []:
                    leak_kinds[str(leak["kind"])] += 1
                    if len(sample_leaks) < 15:
                        sample_leaks.append({"list": key, **leak})
            n_content = int(item_res.get("content_supplied_matches", 0))
            if n_content > 0:
                lists_with_content_matches += 1
                total_content_matches += n_content
                for cm in item_res.get("sample_content_matches") or []:
                    if len(sample_content) < 10:
                        sample_content.append({"list": key, **cm})
        return {
            "section_errors_total": section_errors_total,
            "lists_with_first_read_leaks": lists_with_leaks,
            "total_first_read_leaks": total_leaks,
            "leak_kinds_sampled": dict(sorted(leak_kinds.items())),
            "sample_leaks": sample_leaks,
            "lists_with_content_supplied_matches": lists_with_content_matches,
            "total_content_supplied_matches": total_content_matches,
            "sample_content_matches": sample_content,
        }

    after_agg = _aggregate("after")
    before_agg = _aggregate("before") if args.before_page is not None else None

    synthetic_after: dict[str, Any] = {}
    synthetic_before: dict[str, Any] | None = None
    if not args.skip_synthetic:
        syn_models = _synthetic_models()
        synthetic_after = _check_models_with_node(args.page.resolve(), syn_models)
        if args.before_page is not None:
            synthetic_before = _check_models_with_node(args.before_page.resolve(), syn_models)

    summary: dict[str, Any] = {
        "format": "page-plain-words-track1-census.v1",
        "source": {
            "core": core.version,
            "registry": core.registry,
            "release": core.release_version,
            "page": "packages/presentation/pages/citation-walk.v1.html",
        },
        "recorded_lists_total": len(lists),
        "lists_rendered": outcomes.get("success", 0),
        "outcomes": dict(sorted(outcomes.items())),
        "non_success_errors": dict(sorted(errors.items())),
        "after": after_agg,
        "synthetic_pages_after": synthetic_after,
        "workers": workers,
        "wall_time_s": wall,
    }
    if before_agg is not None:
        summary["before"] = before_agg
    if synthetic_before is not None:
        summary["synthetic_pages_before"] = synthetic_before
    _write_clean_json(args.out, summary)
    print(json.dumps({
        "lists_rendered": summary["lists_rendered"],
        "before_lists_with_leaks": before_agg["lists_with_first_read_leaks"] if before_agg else None,
        "before_total_leaks": before_agg["total_first_read_leaks"] if before_agg else None,
        "after_section_errors": after_agg["section_errors_total"],
        "after_lists_with_leaks": after_agg["lists_with_first_read_leaks"],
        "after_total_leaks": after_agg["total_first_read_leaks"],
        "synthetic_before_leaks": {k: v["total_first_read_leaks"] for k, v in synthetic_before.items()} if synthetic_before else None,
        "synthetic_after_leaks": {k: v["total_first_read_leaks"] for k, v in synthetic_after.items()},
        "wall_time_s": wall,
    }, indent=2))


if __name__ == "__main__":
    main()
