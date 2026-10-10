"""Launch the synthetic SLI correction-session evaluation.

This runner composes the existing correction runtime, adopted surface build,
and loopback server. It owns no correction or serving behavior of its own.
It seeds a temporary synthetic workspace under one named state, runs the
starting (saved) result, builds the one adopted surface page, serves the
correction session over loopback, and prints the URL.

The ``--state`` option (plan, "account-review-correction" Track 2 item 1)
selects one of the committed synthetic states, or "historical" (Track 2
item 3), which is not file-backed: it builds on the "base" state's own
committed seed, then applies one correction directly through the reviewed
recorder *before* the session opens, so the session opens on an already-
superseded saved result. That one-off correction is bounded to this runner
script; it is not a general mechanism for navigating between arbitrary runs.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from tempfile import TemporaryDirectory
from threading import Event
from typing import Any, Sequence

from packages.derivation.correction_session import (
    LOAN_COST_QUESTION,
    RUN_SCOPE,
    SCOPE_USER,
    STATE_BASE,
    STATE_DESCRIPTIONS,
    STATE_HISTORICAL,
    STATE_SEED_LOGS,
    CorrectionRuntime,
    CorrectionSessionServer,
    build_correction_surface,
    core_calculations_surface,
    load_seed_acts,
)
from packages.derivation.live import live_coordinate_run
from packages.derivation.live_workspace import WorkspaceCapability, bootstrap_workspace
from packages.derivation.loader import DerivationSchemas
from packages.kernel.act_log import ActLog
from packages.kernel.currency import compute_currency
from packages.kernel.facts import facts_of
from packages.kernel.findings import project
from packages.tax.loader import install_domain_scoped_supersession
from packages.tax.sli_relationship_review import correct_borrowing_answer_review, prepare_borrowing_answer_review

REPO = Path(__file__).resolve().parents[3]

ALL_STATES = tuple(sorted({*STATE_SEED_LOGS, STATE_HISTORICAL}))

_HISTORICAL_BORROWING_LABEL = "Autumn study loan"
_HISTORICAL_FACT_TYPE = "tax.us.2025.sli.loan-paid-only-school-costs"


def _parse_state(argv: Sequence[str]) -> str:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--state", choices=ALL_STATES, default=STATE_BASE,
        help="Which named synthetic state to seed. Each state's own description is "
             "printed once the session starts; see also the README's walkthrough.")
    state: str = parser.parse_args(list(argv)).state
    return state


def _current_loan_cost_target(acts: Sequence[Any], registry: Any, *, borrowing_label: str) -> tuple[str, str]:
    """Find one current loan-cost finding id and its borrowing reference by
    the borrowing's current label -- read-only, the same identity basis
    ``correction_session.py`` uses everywhere else, never a position or a
    count. Raises if there is not exactly one match."""
    state = project(tuple(dict(act) for act in acts), registry)
    current_ids = compute_currency(state).current_finding_ids
    lattice = facts_of(state.fact_state, include_displaced=True)
    entities = state.fact_state.entities
    matches: list[tuple[str, str]] = []
    for finding_id, row in state.findings.items():
        if finding_id not in current_ids or not isinstance(row, dict):
            continue
        fact = lattice.get(str(row.get("fact_id", "")))
        if fact is None or fact.fact_type_id != _HISTORICAL_FACT_TYPE:
            continue
        borrowing_ref = dict(fact.keys).get("borrowing")
        if not isinstance(borrowing_ref, str):
            continue
        lifecycle = entities.get(borrowing_ref)
        label = lifecycle.entity.get("label") if lifecycle is not None else None
        if label == borrowing_label:
            matches.append((finding_id, borrowing_ref))
    if len(matches) != 1:
        raise RuntimeError("historical-seed-target-not-found")
    return matches[0]


def _historical_seed_acts(repo_root: Path, base_acts: Sequence[Any]) -> list[dict[str, Any]]:
    """One correction (Cedar's loan-cost answer, yes -> no) applied directly
    through the reviewed recorder on top of the base seed, in a throwaway
    workspace -- bounded to this runner's "historical" state, never a
    general run-history mechanism."""
    schemas = DerivationSchemas()
    registry = install_domain_scoped_supersession(schemas.registry)
    with TemporaryDirectory(prefix="demo-correction-historical-seed-") as tmp:
        capability = WorkspaceCapability(Path(tmp) / "L")
        workspace = bootstrap_workspace(capability, repo_root=repo_root)
        log = ActLog(workspace.location, registry)
        for expected, act in enumerate(base_acts):
            log.append(dict(act), expected_revision=expected)
        finding_id, borrowing_ref = _current_loan_cost_target(
            log.read().acts, registry, borrowing_label=_HISTORICAL_BORROWING_LABEL)
        review = prepare_borrowing_answer_review(
            log, registry, review_id="demo.correction.historical.review",
            shown_at="2026-10-09T00:30:00Z", borrowing_refs=(borrowing_ref,))
        correct_borrowing_answer_review(
            log, registry, review, finding_id=finding_id, borrowing_ref=borrowing_ref,
            question=LOAN_COST_QUESTION, response="no", actor=SCOPE_USER,
            at="2026-10-09T00:30:01Z", submission_id="demo.correction.historical.submission",
            evidence_id="demo.evidence.correction.historical")
        return list(log.read().acts)


def main(argv: Sequence[str] | None = None) -> int:
    state = _parse_state(argv if argv is not None else sys.argv[1:])
    try:
        with TemporaryDirectory(prefix="demo-correction-saved-") as saved_dir, \
                TemporaryDirectory(prefix="demo-correction-session-") as session_dir:
            is_historical = state == STATE_HISTORICAL
            base_state = STATE_BASE if is_historical else state
            acts = load_seed_acts(REPO, base_state)
            surface = core_calculations_surface(REPO)

            saved_capability = WorkspaceCapability(Path(saved_dir) / "L")
            saved_outcome = live_coordinate_run(
                saved_capability, repo_root=REPO, authoritative_acts=acts,
                workspace_revision=len(acts), run_scope=RUN_SCOPE, scope_user=SCOPE_USER,
                request={"schema": "run-request.v1"}, run_id="demo.correction.run.initial",
                governance_pins=[], surface=surface, output_name="initial.json",
            )
            if saved_outcome.refusal is not None or saved_outcome.presentation_path is None:
                print(f"Starting result refused: {saved_outcome.refusal!r}", file=sys.stderr)
                return 1

            seed_acts_for_session = (
                _historical_seed_acts(REPO, acts) if is_historical else acts)

            session_capability = WorkspaceCapability(Path(session_dir) / "L")
            runtime = CorrectionRuntime(
                session_capability, repo_root=REPO, surface=surface, run_scope=RUN_SCOPE,
                scope_user=SCOPE_USER, saved_presentation_path=saved_outcome.presentation_path,
                saved_run_id="demo.correction.run.initial", seed_acts=seed_acts_for_session,
                is_historical=is_historical,
            )
            dist = build_correction_surface(session_capability, repo_root=REPO)

            with CorrectionSessionServer(runtime, dist) as server:
                print("Synthetic SLI correction-session evaluation")
                print(f"State: {state}")
                print(STATE_DESCRIPTIONS.get(state, "(no description)"))
                print(f"URL: {server.url}")
                print("Stop: press Ctrl-C in this terminal.")
                print("Clean restart: stop this command, then run the same command again "
                      "(add --state NAME to pick a different state; --help lists every name).")
                sys.stdout.flush()
                Event().wait()
    except KeyboardInterrupt:
        print("\nStopped. Run the command again for a clean starting state.")
        return 130
    except Exception:
        print("Evaluation launch failed.", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
