"""Generate the production-shaped synthetic K-1 breadth presentation golden."""

from __future__ import annotations

import json
import copy
from pathlib import Path
import sys
from tempfile import TemporaryDirectory
from typing import Any, cast

REPO = Path(__file__).resolve().parent.parent
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from packages.derivation.live import live_coordinate_run
from packages.derivation.live_workspace import WorkspaceCapability
from tests.test_k1_interest_breadth_integration import ROOT, USER, SCOPE, _k1_acts, _surface


TARGET = ROOT / "packages" / "sample_data" / "k1_interest_breadth" / "presentation" / "mixed-1099int-k1.presentation-model.v1.json"
MALFORMED_TARGET = ROOT / "packages" / "sample_data" / "k1_interest_breadth" / "presentation" / "malformed-k1-line2b.presentation-model.v1.json"


def regenerate() -> dict[str, Any]:
    acts = _k1_acts(k1_values=[600], box1_interest=1000)
    with TemporaryDirectory() as tmp:
        outcome = live_coordinate_run(
            WorkspaceCapability(Path(tmp) / "L"),
            repo_root=ROOT,
            authoritative_acts=acts,
            workspace_revision=len(acts),
            run_scope=SCOPE,
            scope_user=USER,
            request={"schema": "run-request.v1"},
            run_id="demo.k1.golden.mixed",
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
    malformed = copy.deepcopy(model)
    line2b = next(section for section in malformed["sections"] if section["id"] == "line-2b")
    line2b["resolved"]["value"] = "rejected-k1-value"
    MALFORMED_TARGET.write_text(json.dumps(malformed, indent=2, sort_keys=True) + "\n", "utf-8")


if __name__ == "__main__":
    main()
