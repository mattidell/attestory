"""Regenerate the production-shaped Form 1099-G box-1 presentation golden.

Run from repo root:

    python3 tools/generate_form1099g_box1_schedule1_line7_goldens.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any, cast

REPO = Path(__file__).resolve().parent.parent
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from packages.derivation.live import live_coordinate_run
from packages.derivation.live_workspace import WorkspaceCapability
from tests.test_form1099g_box1_schedule1_line7 import (
    FIXTURES,
    ROOT,
    SCOPE,
    USER,
    _surface,
    _ug_acts,
)

TARGET = (
    FIXTURES
    / "presentation"
    / "form1099g-box1-line8.presentation-model.v1.json"
)
GOLDEN_RUN_ID = "demo.ug.p16"


def regenerate() -> dict[str, Any]:
    acts = _ug_acts(box1_values=[1400])
    with TemporaryDirectory() as tmp:
        outcome = live_coordinate_run(
            WorkspaceCapability(Path(tmp) / "L"),
            repo_root=ROOT,
            authoritative_acts=acts,
            workspace_revision=len(acts),
            run_scope=SCOPE,
            scope_user=USER,
            request={"schema": "run-request.v1"},
            run_id=GOLDEN_RUN_ID,
            governance_pins=[],
            surface=_surface(),
            output_name="golden.json",
        )
        if outcome.refusal is not None:
            raise RuntimeError(str(outcome.refusal))
        assert outcome.presentation_path is not None
        return cast(
            dict[str, Any],
            json.loads(outcome.presentation_path.read_text("utf-8")),
        )


def main() -> None:
    model = regenerate()
    TARGET.parent.mkdir(parents=True, exist_ok=True)
    TARGET.write_text(json.dumps(model, indent=2, sort_keys=True) + "\n", "utf-8")
    print(f"wrote {TARGET.relative_to(REPO)}")


if __name__ == "__main__":
    main()
