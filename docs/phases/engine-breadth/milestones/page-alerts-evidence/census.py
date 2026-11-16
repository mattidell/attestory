"""Count safe-render alerts on the recorded lists' presentation models.

Evidence for docs/phases/engine-breadth/milestones/page-alerts.md.
Published core v91 only. The alert reading is the one the twelve drawn
pages confirmed: a categorical render other than checked or not_checked
is missing-instruction; a numeric disposition with no field citation is
missing-field-citation; a drawn categorical with no field citation is
the same citation alert. The page shows the first of those.

Workers import this file, so run it with this directory on PYTHONPATH:

    python3 -c "import census; census.main()" <scratch-directory-outside-the-repo>
"""

from __future__ import annotations

import importlib.util
import json
import math
import os
import sys
import tempfile
import time
from collections import Counter
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from tools import recorded_replay  # noqa: E402

PARKED = ("form1040.line-6c", "schedule1.top-entry.form-field")
DRAWN = {"checked", "not_checked"}
NUMERIC = {"published_value", "computed_zero", "closure_backed_zero"}


def _load(name: str, path: Path) -> Any:
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


probe = _load("pa_census_probe", HERE / "probe.py")


def _citation(field: dict[str, Any]) -> bool:
    citation = field.get("citation")
    return isinstance(citation, dict) and bool(citation.get("id")) and bool(citation.get("version"))


def _finite_number(value: Any) -> bool:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return False
    return math.isfinite(value)


def section_alert(section: dict[str, Any]) -> dict[str, str] | None:
    """The one safe-render alert this section would draw, if any."""
    field = section.get("field") or {}
    resolved = section.get("resolved") or {}
    disposition = resolved.get("disposition")
    dispositions = field.get("dispositions") if isinstance(field.get("dispositions"), dict) else {}
    key = "published_value" if disposition == "published_categorical" else disposition
    if key not in dispositions:
        code = "unrecognized-disposition"
        cause = f"disposition {disposition}"
    else:
        instruction = dispositions.get(key)
        if not isinstance(instruction, dict):
            code = "missing-instruction"
            cause = f"disposition {disposition}"
        elif disposition in NUMERIC:
            if not _finite_number(resolved.get("value")):
                code = "invalid-numeric-value"
                cause = f"disposition {disposition}"
            elif not _citation(field):
                code = "missing-field-citation"
                cause = f"disposition {disposition} has no field citation"
            else:
                return None
        elif disposition == "published_categorical":
            render = instruction.get("render")
            if not isinstance(render, str) or render not in DRAWN:
                code = "missing-instruction"
                cause = f"render {render}"
            elif not _citation(field):
                code = "missing-field-citation"
                cause = f"render {render} has no field citation"
            else:
                return None
        elif disposition == "blocked":
            for reason in resolved.get("reasons") or []:
                sentence = reason.get("sentence") if isinstance(reason, dict) else None
                if not isinstance(sentence, str) or not sentence:
                    code = "unknown-error"
                    cause = "blocked reason has no sentence"
                    break
            else:
                return None
        elif disposition == "guard_inapplicable":
            return None
        else:
            code = "unrecognized-disposition"
            cause = f"disposition {disposition}"
    field_id = str(field.get("id") or section.get("id") or "unknown").removeprefix(probe.P)
    return {"field": field_id, "code": code, "cause": cause}


def scan(core: Any, acts: list[dict[str, Any]], run_id: str) -> dict[str, Any]:
    """Coordinate one list and return only the alerts its model would draw."""
    h = probe.l12d.harness()
    surface = core.surface()
    with h.loader_entries(core):
        try:
            finished = h._handover(
                h._finish(
                    acts,
                    package_path=core.package_path,
                    package_version=core.version,
                    release_path=core.release_path,
                    release_version=core.release_version,
                    note=run_id,
                ),
                surface=surface,
                reconfirm=True,
            )
            with tempfile.TemporaryDirectory() as tmp:
                outcome = h.live_coordinate_run(
                    h.WorkspaceCapability(Path(tmp) / "L"),
                    repo_root=REPO,
                    authoritative_acts=finished,
                    workspace_revision=len(finished),
                    run_scope={"jurisdiction": "us", "year": h.YEAR},
                    scope_user=h.ccr.USER,
                    request={"schema": "run-request.v1"},
                    run_id=run_id,
                    governance_pins=[],
                    surface=surface,
                    output_name="out.json",
                )
                if outcome.refusal is not None:
                    return {"outcome": "refused", "reason": outcome.refusal.reason}
                model = json.loads(outcome.presentation_path.read_text(encoding="utf-8"))
                report = json.loads(outcome.output_path.read_text(encoding="utf-8"))
        except Exception as exc:  # noqa: BLE001 - a rejected list is a census row
            return {"outcome": "error", "error": type(exc).__name__, "message": probe.scrub(str(exc))[:180]}
    alerts = []
    for section in model.get("sections") or []:
        found = section_alert(section)
        if found is not None:
            alerts.append(found)
    return {"outcome": "success", "stop": report.get("stop_reason"), "alerts": alerts}


def per_list_scan(key: str, acts: list[dict[str, Any]], core: Any) -> dict[str, Any]:
    slug = "".join(ch if ch.isalnum() or ch in "._-" else "." for ch in key)[:80]
    return scan(core, acts, f"demo.pa.census.v91.{slug}")


def per_list_scan_core(key: str, acts: list[dict[str, Any]], core: Any) -> dict[str, Any]:
    """Same alert read as the v91 census, with the run id taken from the core."""
    version = str(getattr(core, "version", "core"))
    slug = "".join(ch if ch.isalnum() or ch in "._-" else "." for ch in key)[:80]
    return scan(core, acts, f"demo.pa.t0.census.{version}.{slug}")


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("usage: census.py <scratch-directory-outside-the-repo>")
    scratch = Path(sys.argv[1]).resolve()
    if REPO in scratch.parents or scratch == REPO:
        raise SystemExit("scratch directory must be outside the repository")
    scratch.mkdir(parents=True, exist_ok=True)
    workers = max(1, (os.cpu_count() or 2) - 1)
    # ReplayCore lives in the replay tool, so the worker processes can unpickle it.
    # The harness Core class is loaded under a private module name and cannot be.
    core = recorded_replay.resolve_core("v91")
    lists = recorded_replay.recorded_lists()
    started = time.perf_counter()
    results = recorded_replay.replay(
        lists,
        core,
        per_list_scan,
        workers=workers,
        part=scratch / "census-part.json",
    )
    wall = round(time.perf_counter() - started, 1)
    outcomes: Counter[str] = Counter()
    stops: Counter[str] = Counter()
    per_field: dict[str, Counter[str]] = {}
    causes: dict[str, Counter[str]] = {}
    extras = []
    other_stops = []
    error_types: Counter[str] = Counter()
    computing = 0
    parked_only = 0
    for key, row in sorted(results.items()):
        outcomes[str(row.get("outcome"))] += 1
        if row.get("outcome") != "success":
            if row.get("outcome") == "error":
                error_types[str(row.get("error"))] += 1
            continue
        stop = str(row.get("stop"))
        stops[stop] += 1
        alerts = row.get("alerts") or []
        for item in alerts:
            field = str(item.get("field"))
            code = str(item.get("code"))
            per_field.setdefault(field, Counter())[code] += 1
            causes.setdefault(field, Counter())[str(item.get("cause"))] += 1
        if stop != "saturated":
            if alerts:
                other_stops.append({"id": key, "stop": stop, "alerts": alerts})
            continue
        computing += 1
        extra = [item for item in alerts if item.get("field") not in PARKED]
        if extra:
            extras.append({"id": key, "alerts": extra})
        elif alerts:
            parked_only += 1
    payload = {
        "core": {"package": "v91", "registry": "v89", "release": "v89"},
        "lists": len(results),
        "workers": workers,
        "wall_time_s": wall,
        "outcomes": dict(outcomes),
        "error_types": dict(error_types),
        "stops": dict(stops),
        "computing_returns": computing,
        "computing_with_only_parked_alerts": parked_only,
        "computing_with_no_alert": computing - parked_only - len(extras),
        "alerts_per_field": {field: dict(counts) for field, counts in sorted(per_field.items())},
        "causes": {field: dict(counts) for field, counts in sorted(causes.items())},
        "extra_alert_returns": len(extras),
        "extra_examples": extras[:12],
        "noncomputing_with_alerts": len(other_stops),
        "noncomputing_examples": other_stops[:8],
    }
    probe.write_json(HERE / "census.json", payload)
    print(json.dumps({
        "lists": payload["lists"],
        "computing_returns": computing,
        "alerts_per_field": payload["alerts_per_field"],
        "extra_alert_returns": payload["extra_alert_returns"],
        "wall_time_s": wall,
        "workers": workers,
    }, indent=2))


if __name__ == "__main__":
    main()
