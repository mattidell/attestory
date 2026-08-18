"""Regenerate Track 8 Form 1098-E / Student Loan Interest presentation
goldens: three genuinely distinct disposition paths, run through
``live_coordinate_run`` against the real production surface Track 6 already
wired (``package.core-calculations.v33`` / ``published-packages.v28`` /
release ``demo.release.2025.v26``). Reuses Track 6's own act choreography
(``tests.test_f1098e_student_loan_interest_agi_track6``) and fixtures
(``packages/sample_data/f1098e_student_loan_interest_track6``) directly --
no new package version is needed, so goldens live alongside Track 6's own
fixtures under a ``presentation/`` subdirectory, matching the
``schedule_d_covered_ltcg_8a_t2``/Track 3 precedent (same package version
reused across tracks) rather than the ``capital_gain_distributions_line7a``
precedent (a new package version per track, hence a new top-level fixture
directory).

Scenarios, chosen to be genuinely distinct rather than exhaustive (Track 6's
ten paths already cover the full disposition matrix):

* ``below-floor`` -- path (b): single statement, full eligibility, MAGI
  below the phaseout floor. Full $2,500-capped deduction computes and
  publishes; the Schedule 1 attachment is required and published.
* ``closed-empty`` -- path (a): closed family with zero current members.
  Line 21 is a closure-backed computed zero; line 26/AGI unaffected.
* ``universal-violation`` -- path (f): a universal eligibility component
  (``no-related-person-interest``) answers "no". The whole route blocks
  with ``SLI_UNIVERSAL_COMPONENT_VIOLATION``, never a silent zero or a
  silent full-box-1 pass-through.

Each golden's presentation model is asserted (by the paired test) to carry
exactly one section per form-field-bound symbol: ``form1040.line-10``,
``-11a``, ``-11b``, ``schedule1.line-21``.
"""

from __future__ import annotations

import json
from pathlib import Path
import sys
from tempfile import TemporaryDirectory
from typing import Any, cast

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from packages.derivation.live import live_coordinate_run
from packages.derivation.live_workspace import WorkspaceCapability
from packages.derivation.production_resolver import PublicationSurface
from packages.tax.loader import TAX_CONTENT_DIR
from tests.test_f1098e_student_loan_interest_agi_track6 import Statement, _f1098e_acts, _renumber

CONTENT = TAX_CONTENT_DIR
FIXTURES = ROOT / "packages" / "sample_data" / "f1098e_student_loan_interest_track6"
GOLDEN_DIR = FIXTURES / "presentation"
USER = "demo.user.filer-1"
SCOPE = {"jurisdiction": "us", "year": "2025"}


def _surface() -> PublicationSurface:
    return PublicationSurface(
        FIXTURES / "publication_surface" / "releases",
        CONTENT / "published-packages.v28.json",
        CONTENT,
    )


def run_model(name: str, acts: list[dict[str, object]]) -> dict[str, Any]:
    acts = _renumber(list(acts))
    with TemporaryDirectory() as raw:
        outcome = live_coordinate_run(
            WorkspaceCapability(Path(raw) / "L"), repo_root=ROOT, authoritative_acts=acts,
            workspace_revision=len(acts), run_scope=SCOPE, scope_user=USER,
            request={"schema": "run-request.v1"}, run_id=f"demo.f1098e.t8.{name}", governance_pins=[],
            surface=_surface(), output_name=f"{name}.json",
        )
        assert outcome.refusal is None, outcome.refusal
        assert outcome.presentation_path is not None
        return cast(dict[str, Any], json.loads(outcome.presentation_path.read_text("utf-8")))


def regenerate() -> dict[str, dict[str, Any]]:
    below_floor = [Statement(lender="demo.f1098e.t8.lender.bf", stmt="demo.f1098e.t8.stmt.bf", box1=3000.0)]
    closed_empty: list[Statement] = []
    universal_violation = [
        Statement(
            lender="demo.f1098e.t8.lender.uv", stmt="demo.f1098e.t8.stmt.uv", box1=1000.0,
            witnesses={"no-related-person-interest": "no"},
        )
    ]
    return {
        "below-floor": run_model(
            "below-floor", _f1098e_acts(statements=below_floor, close=True, wages=50000)
        ),
        "closed-empty": run_model(
            "closed-empty", _f1098e_acts(statements=closed_empty, close=True, wages=90000)
        ),
        "universal-violation": run_model(
            "universal-violation", _f1098e_acts(statements=universal_violation, close=True, wages=50000)
        ),
    }


def main() -> None:
    models = regenerate()
    GOLDEN_DIR.mkdir(parents=True, exist_ok=True)
    for name, model in models.items():
        target = GOLDEN_DIR / f"{name}.presentation-model.v1.json"
        target.write_text(json.dumps(model, indent=2, sort_keys=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
