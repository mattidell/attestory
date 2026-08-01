"""Generate the production-shaped synthetic market-discount presentation golden."""

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
from tests.test_market_discount_interest_integration import ROOT, USER, SCOPE, _md_acts, _surface


TARGET = ROOT / "packages" / "sample_data" / "market_discount_interest" / "presentation" / "mixed-market-discount.presentation-model.v1.json"


def regenerate() -> dict[str, Any]:
    acts = _md_acts(b10_values=[80], oid5_values=[65])
    with TemporaryDirectory() as tmp:
        outcome = live_coordinate_run(
            WorkspaceCapability(Path(tmp) / "L"),
            repo_root=ROOT,
            authoritative_acts=acts,
            workspace_revision=len(acts),
            run_scope=SCOPE,
            scope_user=USER,
            request={"schema": "run-request.v1"},
            run_id="demo.md.golden.mixed",
            governance_pins=[],
            surface=_surface(),
            output_name="golden.json",
        )
        if outcome.refusal is not None:
            raise RuntimeError(outcome.refusal)
        assert outcome.presentation_path is not None
        return cast(dict[str, Any], json.loads(outcome.presentation_path.read_text("utf-8")))


def main() -> None:
    model = regenerate()
    TARGET.parent.mkdir(parents=True, exist_ok=True)
    TARGET.write_text(json.dumps(model, indent=2, sort_keys=True) + "\n", "utf-8")


if __name__ == "__main__":
    main()
