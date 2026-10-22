"""Diagnostic-only synthetic P0 probe; not a test or a production entrypoint."""
from __future__ import annotations

import copy
import hashlib
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any

ROOT = Path(__file__).resolve().parents[5]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from packages.derivation.live import live_coordinate_run
from packages.derivation.live_workspace import WorkspaceCapability
from packages.derivation.loader import DerivationSchemas
from packages.derivation.production_resolver import PublicationSurface
from packages.derivation.records import RecordStream
from packages.kernel.act_log import ActLog
from packages.kernel.facts import fact_id_for
from packages.tax.f1098_statement_review import (
    F1098ReviewRefused,
    prepare_f1098_statement_review,
    review_f1098_statement_with_saved_presentation,
    save_f1098_statement_review,
)
from packages.tax.loader import TAX_CONTENT_DIR, load_f1098_circumstances_bundle, tax_registry
from packages.tax.f1098_statement_recording import (
    F1098RecordingRefused,
    record_f1098_statement_answers_durably,
)
from tests.test_f1098_circumstances_calculation import (
    _acts as mortgage_fixture_acts,
    RELEASE_DIR,
    ROOT as TEST_ROOT,
    SCOPE,
    USER as RUN_USER,
)
from tests.test_f1098_statement_review import BASE_ANSWERS, USER as ANSWER_ACTOR
from tests.test_f1099k_personal_item_sale_track1 import _make_base_acts
from tests.test_multiple_statement_candidate_repairs import _finish_acts_v49

CONTENT = TAX_CONTENT_DIR
PACKAGE_PATH = CONTENT / "package.core-calculations.v49.json"
REGISTRY_PATH = CONTENT / "published-packages.v47.json"
RELEASE_PATH = RELEASE_DIR / "demo.release.sli-worksheet-integration.2025.v47.json"
SURFACE = PublicationSurface(RELEASE_DIR, REGISTRY_PATH, CONTENT)
ANSWERS_V2 = {
    **{key: value for key, value in BASE_ANSWERS.items()
       if key not in {"owns-the-home", "lives-there-most-of-the-time"}},
    "filing-unit-owns-home": "yes",
    "shared-main-home": "yes",
}


def _attested(finding_id: str, fact_id: str, value: object) -> dict[str, Any]:
    return {"schema": "finding.v2", "id": finding_id, "fact_id": fact_id, "value": value,
            "basis": "attested", "evidence_ids": []}


def _f1098_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Keep only the mortgage-specific synthetic source setup from the v44 fixture."""
    kept: list[dict[str, Any]] = []
    for row in rows:
        payload = row.get("payload", {})
        if not isinstance(payload, dict):
            continue
        kind = row.get("kind")
        bundle = payload.get("bundle")
        if kind == "bundle-adoption" and isinstance(bundle, dict) and bundle.get("id") in {
            "tax.us.2025.f1098.vocabulary",
            "tax.us.2025.f1098-scope.vocabulary",
        }:
            kept.append(copy.deepcopy(row))
            continue
        entity = payload.get("entity")
        if kind == "entity-introduced" and isinstance(entity, dict) and str(entity.get("id", "")).startswith(
            ("demo.f1098.lender.", "demo.f1098.stmt.")
        ):
            kept.append(copy.deepcopy(row))
            continue
        family = payload.get("family")
        if kind == "horizon-genesis" and isinstance(family, dict) and family.get("id") == "tax.us.2025.f1098":
            kept.append(copy.deepcopy(row))
            continue
        member = payload.get("member")
        finding = member.get("finding") if isinstance(member, dict) else payload.get("finding")
        fact_id = finding.get("fact_id") if isinstance(finding, dict) else None
        if kind == "member-transition" and isinstance(family, dict) and family.get("id") == "tax.us.2025.f1098":
            kept.append(copy.deepcopy(row))
        elif kind == "assertion" and isinstance(fact_id, str):
            report_fact = any(fact_id.startswith(f"tax.us.2025.f1098.{suffix}|") for suffix in (
                "box1-mortgage-interest", "box2-outstanding-principal", "box3-origination-date",
                "box4-overpaid-refund", "box5-mortgage-insurance", "box6-points",
                "box9-number-of-properties", "box11-other", "source-closure",
            ))
            scope_fact = fact_id.startswith("tax.us.2025.f1098-scope.no-mortgage-statement|")
            if report_fact or scope_fact:
                kept.append(copy.deepcopy(row))
    return kept


def _latest_acts(*, box2: float = 200000.0, second_report: bool = False,
                 second_box2: float = 180000.0, fixture_answers: bool = False) -> list[dict[str, Any]]:
    """Compose latest closed-empty return base with the historical mortgage source facts."""
    mortgage = mortgage_fixture_acts(20000.0, second_interest=5000.0 if second_report else None,
                                     box2=box2, filing_status="single")
    if second_report:
        second_fact = fact_id_for("tax.us.2025.f1098.box2-outstanding-principal",
                                  (("payer", "demo.f1098.lender.b"), ("statement", "demo.f1098.stmt.b"),
                                   ("tax-year", "2025")))
        for row in mortgage:
            finding = row.get("payload", {}).get("finding", {})
            if finding.get("fact_id") == second_fact:
                finding["value"] = second_box2
    rows = _make_base_acts()
    rows.extend(_f1098_rows(mortgage))
    registry = tax_registry()
    rows.append({
        "schema": "act.v1",
        "act_id": "demo.f1098.p0.answer-vocabulary.v2",
        "kind": "bundle-adoption",
        "actor": "demo.taxpayer",
        "at": "2026-10-21T12:00:00Z",
        "committed_against": len(rows),
        "payload": {"bundle": load_f1098_circumstances_bundle(registry, version="v2")},
    })
    if fixture_answers:
        # Coordinator-only normalized synthetic answers; these do not come
        # from the review or recorder and do not establish a shared loan.
        for payer, statement in (("demo.f1098.lender.a", "demo.f1098.stmt.a"),
                                 ("demo.f1098.lender.b", "demo.f1098.stmt.b")):
            if payer.endswith(".b") and not second_report:
                continue
            keys = (("payer", payer), ("statement", statement), ("tax-year", "2025"))
            for question, answer in ANSWERS_V2.items():
                fact_id = fact_id_for(f"tax.us.2025.f1098.{question}", keys)
                finding = _attested(f"demo.f1098.p0.fixture.{statement}.{question}", fact_id, answer)
                rows.append({"schema": "act.v1", "act_id": f"demo.f1098.p0.fixture-act.{statement}.{question}",
                             "kind": "assertion", "actor": "demo.taxpayer",
                             "at": "2026-10-21T12:00:30Z", "committed_against": len(rows),
                             "payload": {"finding": finding}})
    latest = _finish_acts_v49(rows)
    package_adoption = latest[-1]
    package_adoption["payload"]["revision"] = len(latest) - 1
    package_adoption["payload"]["audit"] = {"note": "synthetic Form 1098 P0 v49/v47 diagnostic"}
    for index, act in enumerate(latest):
        act["committed_against"] = index
    return latest


def _run_case(case: str, *, box2: float = 200000.0, second_report: bool = False,
              second_box2: float = 180000.0) -> dict[str, Any]:
    started = time.perf_counter()
    registry = tax_registry()
    case_dir = OUT_DIR / case
    case_dir.mkdir(parents=True, exist_ok=False)
    workspace_tmp = TemporaryDirectory(prefix=f"demo-f1098-p0-{case}-")
    workspace = Path(workspace_tmp.name) / "workspace"
    capability = WorkspaceCapability(workspace)
    log = ActLog(workspace, registry)
    seed = _latest_acts(box2=box2, second_report=second_report, second_box2=second_box2,
                        fixture_answers=second_report)
    log.append_batch(seed, expected_revision=0)
    seed_revision = log.read().revision
    ordinary_questions_absent_before_save = None
    refusal_observation: dict[str, Any] | None = None
    if second_report:
        try:
            prepare_f1098_statement_review(log, registry, review_id=f"demo.f1098.p0.{case}.review.before",
                                           shown_at="2026-10-21T12:01:00Z")
        except F1098ReviewRefused as exc:
            review = None
            review_refusal = str(exc)
        else:
            review_refusal = None
        revision_before = log.read().revision
        direct: list[dict[str, Any]] = []
        for payer, statement in (("demo.f1098.lender.a", "demo.f1098.stmt.a"),
                                 ("demo.f1098.lender.b", "demo.f1098.stmt.b")):
            try:
                record_f1098_statement_answers_durably(
                    log, registry, statement_keys={"payer": payer, "statement": statement, "tax-year": "2025"},
                    answers=ANSWERS_V2, submission_id=f"demo.f1098.p0.{case}.direct.{statement}",
                    evidence_ids={key: f"demo.f1098.p0.{case}.direct-evidence.{statement}.{key}" for key in ANSWERS_V2},
                    actor=ANSWER_ACTOR, at="2026-10-21T12:02:00Z", expected_revision=revision_before,
                    bundle_version="v2")
            except F1098RecordingRefused as exc:
                direct.append({"statement": statement, "refusal": str(exc)})
            else:
                direct.append({"statement": statement, "refusal": None})
        refusal_observation = {"review_refusal": review_refusal, "direct_exact_key_attempts": direct,
                               "revision_before": revision_before, "revision_after": log.read().revision}
        review = None
        save = None
        current = None
    else:
        review = prepare_f1098_statement_review(log, registry, review_id=f"demo.f1098.p0.{case}.review.before",
                                               shown_at="2026-10-21T12:01:00Z")
        ordinary_questions_absent_before_save = {
            key: value["state"] == "absent" for key, value in review["questions"].items()
            if key in ANSWERS_V2
        }
        save = save_f1098_statement_review(
            log, registry, review, answers=ANSWERS_V2,
            submission_id=f"demo.f1098.p0.{case}.answers",
            evidence_ids={key: f"demo.f1098.p0.{case}.evidence.{key}" for key in ANSWERS_V2},
            actor=ANSWER_ACTOR, at="2026-10-21T12:02:00Z",
        )
        current = prepare_f1098_statement_review(log, registry, review_id=f"demo.f1098.p0.{case}.review.after",
                                                 shown_at="2026-10-21T12:03:00Z")
    contents = log.read()
    contents = log.read()
    # Retain inspectable synthetic audit trails before the ephemeral workspace ends.
    (case_dir / "synthetic-seed-acts.json").write_text(json.dumps(seed, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (case_dir / "synthetic-final-acts.json").write_text(json.dumps(contents.acts, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    result = live_coordinate_run(
        capability, repo_root=ROOT, authoritative_acts=contents.acts,
        workspace_revision=contents.revision, run_scope=SCOPE, scope_user=RUN_USER,
        request={"schema": "run-request.v1"},
        run_id=f"demo.f1098.p0.{case}.v49-v47", governance_pins=[],
        surface=SURFACE, output_name=f"{case}.json",
    )
    summary: dict[str, Any] = {
        "case": case,
        "fixture": "synthetic facts composed from the v44/v42 mortgage fixture and the v49/v47 closed-empty latest return fixture",
        "latest_route": {
            "package": {"id": "tax.us.2025.package.core-calculations", "version": "v49",
                        "checksum": json.loads(PACKAGE_PATH.read_text("utf-8"))["package_checksum"]},
            "registry": str(REGISTRY_PATH.relative_to(ROOT)),
            "release": {"id": "demo.release.sli-worksheet-integration.2025", "version": "v47",
                        "checksum": hashlib.sha256(RELEASE_PATH.read_bytes()).hexdigest()},
            "adoption_index": next((index for index, row in enumerate(seed)
                                     if row.get("kind") == "package-adoption"
                                     and row.get("payload", {}).get("package", {}).get("id") ==
                                     "tax.us.2025.package.core-calculations"), None),
            "seed_revision": seed_revision,
            "seed_length": len(seed),
        },
        "seed_deltas": {
            "from_historical_mortgage_helper": [
                "Use the latest sale-route closed-empty base and its v49/v47 adoption, rather than the v44/v42 all-return seed.",
                "Take only the mortgage report facts, scope declaration and family closure from the v44/v42 mortgage helper; strip its ordinary/timing answers and v1 successor-vocabulary adoption.",
                "Adopt the currently selected f1098-successor vocabulary v2 before the real review/save.",
                "Set the package-adoption payload revision to its actual pre-adoption ActLog index.",
            ],
            "mortgage_closure": "Preserved the mortgage helper's original one-report family v1 horizon and true closure; no mortgage closure substitution.",
            "unrelated_closed_empty": "Uses the latest sale-route helper's closed-empty setup and adopted versions, including Form 1099-K v2 family / v2 closure mapping and v3 vocabulary selection; not silently changed after a run.",
        },
        "review_offered": ({
            "bundle_version": review["bundleVersion"],
            "statement": review["statement"],
            "questions": {key: {"state": value["state"], "answer": value["answer"],
                                "defaultPolicy": value.get("defaultPolicy")}
                          for key, value in review["questions"].items()},
        } if review is not None else {"refused": refusal_observation["review_refusal"]}),
        "ordinary_questions_absent_before_save": ordinary_questions_absent_before_save,
        "recorded": ({"revision_before": review["revision"], "revision_after": save["revision"],
                      "finding_ids": save["finding_ids"],
                      "answers": {key: current["questions"][key]["answer"] for key in ANSWERS_V2}}
                     if save is not None else None),
        "two_report_refusals": refusal_observation,
        "synthetic_fixture_answers": "Coordinator-only normalized facts for both report identities; not real recorder values or a same-loan relationship." if second_report else None,
        "coordinator": {"refusal": repr(result.refusal),
                        "workspace_topology": "ephemeral synthetic ActLog/records outside repo, required by live workspace residency guard",
                        "output_copy": "coordinator-report.json" if result.output_path else None,
                        "presentation_copy": "presentation-model.json" if result.presentation_path else None},
        "elapsed_seconds": round(time.perf_counter() - started, 3),
    }
    if result.output_path is not None:
        (case_dir / "coordinator-report.json").write_bytes(result.output_path.read_bytes())
        report = json.loads(result.output_path.read_text("utf-8"))
        summary["report_keys"] = sorted(report.keys())
        summary["mortgage_dispositions"] = [row for row in report.get("dispositions", [])
                                             if "f1098" in row.get("artifact_id", "")
                                             or row.get("artifact_id") == "tax.us.2025.rule.schedule-a-total"]
        summary["observed_pins_from_mortgage_dispositions"] = sorted({
            (pin.get("id"), pin.get("role"), pin.get("version"))
            for disposition in summary["mortgage_dispositions"]
            for pin in disposition.get("pins", [])
        })
        summary["observed_pins_from_mortgage_dispositions"] = [
            {"id": pin[0], "role": pin[1], "version": pin[2]}
            for pin in summary["observed_pins_from_mortgage_dispositions"]
        ]
    if result.presentation_path is not None:
        (case_dir / "presentation-model.json").write_bytes(result.presentation_path.read_bytes())
        records = RecordStream(capability.location / "records", DerivationSchemas())
        record_contents = records.read()
        (case_dir / "synthetic-records.json").write_text(json.dumps(record_contents.records, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        fresh_log = ActLog(workspace, registry, read_only=True)
        try:
            combined = review_f1098_statement_with_saved_presentation(
                fresh_log, registry, result.presentation_path, records,
                review_id=f"demo.f1098.p0.{case}.review.saved", shown_at="2026-10-21T12:04:00Z",
            )
        except F1098ReviewRefused as exc:
            summary["saved_review"] = {"reloaded_revision": fresh_log.read().revision,
                                       "refused": str(exc),
                                       "presentation_retained": True}
        else:
            summary["saved_review"] = {
                "reloaded_revision": fresh_log.read().revision,
                "association": combined["calculationAssociation"],
                "state": combined.get("savedCalculationState"),
                "calculation": combined.get("savedCalculation"),
                "unresolved": combined.get("savedUnresolvedExplanation"),
            }
    workspace_tmp.cleanup()
    return summary


if __name__ == "__main__":
    if TEST_ROOT != ROOT:
        raise RuntimeError("probe must run from its own worktree root")
    OUT_DIR = ROOT / "temp" / "mortgage-statement-borrowing" / datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    OUT_DIR.mkdir(parents=True, exist_ok=False)
    if sys.argv[1:] == ["--case", "two-reports-agreeing-box2"]:
        summaries = [_run_case("two-reports-agreeing-box2", second_report=True, second_box2=200000.0)]
    elif sys.argv[1:]:
        raise SystemExit("supported selector: --case two-reports-agreeing-box2")
    else:
        summaries = [
            _run_case("one-report-baseline"),
            _run_case("two-reports-differing-box2", second_report=True),
            _run_case("one-report-over-limit-principal", box2=800000.0),
        ]
    for summary in summaries:
        (OUT_DIR / f"{summary['case']}-summary.json").write_text(
            json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
    print(json.dumps({"output_directory": str(OUT_DIR.relative_to(ROOT)), "summaries": summaries}, indent=2, sort_keys=True))
