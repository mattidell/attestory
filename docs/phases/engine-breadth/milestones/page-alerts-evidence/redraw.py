"""Redraw the plan's cases on a scratch core and read the saved pages.

Evidence for docs/phases/engine-breadth/milestones/page-alerts.md.
Uses probe.py's act lists, the real coordinator, and observe.mjs.
Does not edit packages/.

    python3 redraw.py <scratch-directory-outside-the-repo> <core.json>
"""

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]


def _load(name: str, path: Path) -> Any:
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


probe = _load("pa_probe", HERE / "probe.py")

FOCUS = ("form1040.line-6c", "schedule1.top-entry.form-field")


def core_from(path: Path) -> Any:
    body = json.loads(path.read_text(encoding="utf-8"))
    return probe.l12d.harness().Core(
        body["version"],
        body["registry"],
        body["release_version"],
        content=Path(body["content"]),
        releases=Path(body["releases"]),
        loader_from=body.get("loader_from"),
    )


def shown(row: dict[str, Any], observed: dict[str, Any]) -> list[dict[str, Any]]:
    sections = {item.get("id"): item for item in observed.get("sections") or []}
    found = []
    for model in row.get("sections") or []:
        if model.get("field_id") not in FOCUS:
            continue
        dom = sections.get(model.get("section_id")) or {}
        found.append({
            "field_id": model.get("field_id"),
            "disposition": model.get("disposition"),
            "render": model.get("render"),
            "finding_value": model.get("finding_value"),
            "value": model.get("value"),
            "citation_id": model.get("citation_id"),
            "heading": dom.get("heading"),
            "badge": dom.get("badge"),
            "drawn_value": dom.get("value"),
            "drawn_explain": dom.get("explain"),
            "drawn_alert": dom.get("section_error") or None,
            "citation_buttons": dom.get("citation_buttons"),
        })
    return found


def main() -> None:
    if len(sys.argv) != 3:
        raise SystemExit("usage: redraw.py <scratch-directory-outside-the-repo> <core.json>")
    scratch = Path(sys.argv[1]).resolve()
    core_path = Path(sys.argv[2]).resolve()
    if REPO in scratch.parents or scratch == REPO:
        raise SystemExit("scratch directory must be outside the repository")
    scratch.mkdir(parents=True, exist_ok=True)
    page_dir = scratch / "pages"
    core = core_from(core_path)
    built = probe.cases()
    results = []
    manifest = []
    for row in built:
        run_id = f"demo.pa.p0.{core.version}.{row['id']}"
        print(row["id"], flush=True)
        if isinstance(row["acts"], dict):
            measured = row["acts"]
        else:
            measured = probe.run_case(core, row["acts"], run_id, page_dir)
        print(" ", measured.get("outcome"), flush=True)
        results.append({"id": row["id"], "says": row["says"], "run_id": run_id, **measured})
        if measured.get("outcome") == "success":
            manifest.append({"id": row["id"], "page": f"{run_id}.html"})
    browser_dir = scratch / "browser"
    browser_dir.mkdir(parents=True, exist_ok=True)
    (browser_dir / "cases.json").write_text(
        json.dumps({"root": str(page_dir), "cases": manifest}, indent=2) + "\n",
        encoding="utf-8",
    )
    proc = subprocess.run(
        ["node", str(HERE / "observe.mjs"), str(browser_dir / "cases.json")],
        cwd=REPO,
        capture_output=True,
        text=True,
        timeout=300,
    )
    if proc.returncode != 0:
        raise SystemExit("browser observation failed: " + probe.scrub(proc.stderr)[-500:])
    dom = json.loads((browser_dir / "dom-observations.json").read_text(encoding="utf-8"))
    by_id = {item["id"]: item for item in dom.get("cases") or []}
    cases = []
    for row in results:
        observed = by_id.get(row["id"]) or {}
        alerts = []
        sections = {item.get("id"): item for item in observed.get("sections") or []}
        for alert in observed.get("alerts") or []:
            model_section = next(
                (item for item in row.get("sections") or [] if item.get("section_id") == alert.get("id")),
                None,
            )
            alerts.append({
                "section_id": alert.get("id"),
                "alert": alert.get("text"),
                "heading": (sections.get(alert.get("id")) or {}).get("heading"),
                "model": model_section,
            })
        cases.append({
            "id": row["id"],
            "says": row["says"],
            "outcome": row.get("outcome"),
            "stop": row.get("stop"),
            "error": row.get("error"),
            "dom_alert_count": len(observed.get("alerts") or []),
            "other_root_alerts": observed.get("other_root_alerts") or [],
            "drawn_alerts": alerts,
            "focus": shown(row, observed),
        })
    payload = {
        "core": {"package": core.version, "registry": core.registry, "release": core.release_version},
        "page": str(probe.PAGE),
        "browser": dom.get("browser_version"),
        "node": dom.get("node_version"),
        "cases": cases,
    }
    probe.write_json(HERE / "prototype-pages.json", payload)
    for row in cases:
        print(row["id"], row.get("outcome"), row.get("dom_alert_count"), [item.get("drawn_value") for item in row["focus"]], flush=True)


if __name__ == "__main__":
    main()
