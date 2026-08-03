"""Generate the production-shaped synthetic Schedule B adjustment golden."""

from __future__ import annotations

import json
from pathlib import Path
import sys
from tempfile import TemporaryDirectory
from typing import Any, cast

REPO = Path(__file__).resolve().parent.parent
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from packages.derivation.live import live_coordinate_run
from packages.derivation.live_workspace import WorkspaceCapability
from tests.test_schedule_b_interest_adjustments import ROOT, SCOPE, USER, _adjustment_acts, _surface


TARGET = ROOT / "packages" / "sample_data" / "schedule_b_interest_adjustments" / "presentation" / "mixed-schedule-b-interest-adjustments.presentation-model.v1.json"


def regenerate() -> dict[str, Any]:
    acts = _adjustment_acts(values={"nominee": [100], "accrued-interest": [50], "abp-adjustment": [25]})
    with TemporaryDirectory() as tmp:
        outcome = live_coordinate_run(
            WorkspaceCapability(Path(tmp) / "L"),
            repo_root=ROOT,
            authoritative_acts=acts,
            workspace_revision=len(acts),
            run_scope=SCOPE,
            scope_user=USER,
            request={"schema": "run-request.v1"},
            run_id="demo.sbia.golden.combined",
            governance_pins=[],
            surface=_surface(),
            output_name="golden.json",
        )
        if outcome.refusal is not None:
            raise RuntimeError(outcome.refusal)
        assert outcome.presentation_path is not None
        return cast(dict[str, Any], json.loads(outcome.presentation_path.read_text("utf-8")))


def main() -> None:
    TARGET.parent.mkdir(parents=True, exist_ok=True)
    TARGET.write_text(json.dumps(regenerate(), indent=2, sort_keys=True) + "\n", "utf-8")


if __name__ == "__main__":
    main()
