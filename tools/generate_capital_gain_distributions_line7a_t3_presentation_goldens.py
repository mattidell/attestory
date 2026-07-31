"""Regenerate synthetic v8/v3 line-7a/7b presentation goldens.

The three production-shaped act logs deliberately enter only through
``live_coordinate_run``.  They reuse the Track-2 fact choreography while
pinning the Track-3 v8 package through the v3 release registry.
"""

from __future__ import annotations

import json
from copy import deepcopy
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
from tests.test_capital_gain_distributions_line7a_t2_coordinator import _cgd_t2_acts

CONTENT = ROOT / "packages" / "content" / "tax" / "2025"
T3 = ROOT / "packages" / "sample_data" / "frrs_t3"
GOLDEN_DIR = ROOT / "packages" / "sample_data" / "capital_gain_distributions_line7a_t3" / "presentation"
USER = "demo.user.filer-1"
SCOPE = {"jurisdiction": "us", "year": "2057"}


def _surface() -> PublicationSurface:
    return PublicationSurface(T3 / "publication_surface" / "releases", CONTENT / "published-packages.v3.json", CONTENT)


def canonical_acts(*, components: dict[str, str | None] | None = None) -> list[dict[str, object]]:
    acts = _cgd_t2_acts(components=components, box1b=0, cg_dist="yes")
    adoption = cast(dict[str, object], json.loads((T3 / "adoptions" / "adopt-core-v8-current.json").read_text("utf-8")))
    adoption["committed_against"] = len(acts) - 1
    acts[-1] = adoption
    return acts


def run_model(name: str, *, components: dict[str, str | None] | None = None) -> dict[str, Any]:
    acts = canonical_acts(components=components)
    with TemporaryDirectory() as raw:
        outcome = live_coordinate_run(
            WorkspaceCapability(Path(raw) / "L"), repo_root=ROOT, authoritative_acts=acts,
            workspace_revision=len(acts), run_scope=SCOPE, scope_user=USER,
            request={"schema": "run-request.v1"}, run_id=f"demo.cgd.t3.{name}", governance_pins=[],
            surface=_surface(), output_name=f"{name}.json",
        )
        assert outcome.refusal is None, outcome.refusal
        assert outcome.presentation_path is not None
        return cast(dict[str, Any], json.loads(outcome.presentation_path.read_text("utf-8")))


def regenerate() -> dict[str, dict[str, Any]]:
    return {
        "eligible": run_model("eligible"),
        "missing-authority": run_model("missing-authority", components={"C1": "yes", "C2": "yes", "C3": "yes", "C4": None}),
        "schedule-d-required": run_model("schedule-d-required", components={"C1": "yes", "C2": "yes", "C3": "yes", "C4": "no"}),
    }


def main() -> None:
    models = regenerate()
    for name, model in models.items():
        target = GOLDEN_DIR / f"{name}.presentation-model.v1.json"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(model, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    fixtures = {
        "cgd-eligible.v1.json": models["eligible"],
        "cgd-missing-authority-smuggled.v1.json": deepcopy(models["missing-authority"]),
        "cgd-schedule-d-smuggled.v1.json": deepcopy(models["schedule-d-required"]),
        "cgd-broken-line7a.v1.json": deepcopy(models["eligible"]),
    }
    fixtures["cgd-missing-authority-smuggled.v1.json"]["sections"] = [
        dict(section, resolved=dict(section["resolved"], value=999)) if section["id"] == "line-7a" else section
        for section in fixtures["cgd-missing-authority-smuggled.v1.json"]["sections"]
    ]
    fixtures["cgd-schedule-d-smuggled.v1.json"]["sections"] = [
        dict(section, resolved=dict(section["resolved"], value="yes")) if section["id"] == "line-7b" else section
        for section in fixtures["cgd-schedule-d-smuggled.v1.json"]["sections"]
    ]
    fixtures["cgd-broken-line7a.v1.json"]["sections"] = [
        dict(section, resolved=dict(section["resolved"], value="not-a-number")) if section["id"] == "line-7a" else section
        for section in fixtures["cgd-broken-line7a.v1.json"]["sections"]
    ]
    fixture_dir = ROOT / "tools" / "presentation_harness" / "examples" / "pages" / "citation-walk-fixtures"
    for name, model in fixtures.items():
        (fixture_dir / name).write_text(json.dumps(model, indent=2, sort_keys=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
