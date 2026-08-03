"""Regenerate synthetic Track 3 Schedule D presentation goldens.

Every named class enters exclusively through ``live_coordinate_run`` against
package v13 / published-packages v8. Reuses Track 2's act-log choreography
(``tests.test_schedule_d_covered_ltcg_8a_t2_coordinator._sdcl_t2_acts``).
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
from tests.test_schedule_d_covered_ltcg_8a_t2_coordinator import _sdcl_t2_acts, BOUNDARY_DECLARATIONS

CONTENT = ROOT / "packages" / "content" / "tax" / "2025"
FIXTURES = ROOT / "packages" / "sample_data" / "schedule_d_covered_ltcg_8a_t2"
GOLDEN_DIR = FIXTURES / "presentation"
SCOPE = {"jurisdiction": "us", "year": "2059"}


def _surface() -> PublicationSurface:
    return PublicationSurface(
        FIXTURES / "publication_surface" / "releases", CONTENT / "published-packages.v8.json", CONTENT
    )


def run_model(name: str, acts: list[dict[str, object]]) -> dict[str, Any]:
    with TemporaryDirectory() as raw:
        outcome = live_coordinate_run(
            WorkspaceCapability(Path(raw) / "L"), repo_root=ROOT, authoritative_acts=acts,
            workspace_revision=len(acts), run_scope=SCOPE, scope_user="demo.user.filer-1",
            request={"schema": "run-request.v1"}, run_id=f"demo.sdcl.t3.{name}", governance_pins=[],
            surface=_surface(), output_name=f"{name}.json",
        )
        assert outcome.refusal is None, outcome.refusal
        assert outcome.presentation_path is not None
        return cast(dict[str, Any], json.loads(outcome.presentation_path.read_text("utf-8")))


def regenerate() -> dict[str, dict[str, Any]]:
    violated = {name: "yes" for name in BOUNDARY_DECLARATIONS}
    violated["tax.us.2025.schedule-d-boundary.no-current-capital-losses"] = "no"
    missing = {name: "yes" for name in BOUNDARY_DECLARATIONS}
    missing["tax.us.2025.schedule-d-boundary.no-form8949-sources"] = None

    return {
        "eligible": run_model("eligible", _sdcl_t2_acts(
            box2a=None, close_2a=True, eligible_txn=True, adoption_file="adopt-core-v13-current.json",
        )),
        "violated-declaration": run_model("violated-declaration", _sdcl_t2_acts(
            box2a=None, close_2a=True, eligible_txn=True, boundary=violated,
            adoption_file="adopt-core-v13-current.json",
        )),
        "missing-declaration": run_model("missing-declaration", _sdcl_t2_acts(
            box2a=None, close_2a=True, eligible_txn=True, boundary=missing,
            adoption_file="adopt-core-v13-current.json",
        )),
        "not-required": run_model("not-required", _sdcl_t2_acts(
            box2a=1500, eligible_txn=False, adoption_file="adopt-core-v13-current.json",
        )),
        "both-gains": run_model("both-gains", _sdcl_t2_acts(
            box2a=500, close_2a=True, eligible_txn=True, adoption_file="adopt-core-v13-current.json",
        )),
    }


def main() -> None:
    models = regenerate()
    GOLDEN_DIR.mkdir(parents=True, exist_ok=True)
    for name, model in models.items():
        target = GOLDEN_DIR / f"{name}.presentation-model.v1.json"
        target.write_text(json.dumps(model, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    fixture_dir = ROOT / "tools" / "presentation_harness" / "examples" / "pages" / "citation-walk-fixtures"
    fixture_dir.mkdir(parents=True, exist_ok=True)
    (fixture_dir / "sdcl-eligible.v1.json").write_text(
        json.dumps(models["eligible"], indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
