"""Shared runner and summary for the blocked-names-question P0 evidence.

Evidence for docs/phases/engine-breadth/milestones/blocked-names-question.md.
Charter: docs/reviews/blocked-names-question/charter-p0.md.

Every run is one ``live_coordinate_run`` of synthetic ``demo.*`` acts on a
core named by an audit-harness ``Core``: published core v87, or a scratch
core that prototype.py builds outside the repository. The summary records,
for each blocked line the page shows, its disposition row (code and
``missing``), the reason sentences on the page, the questions among them,
and the root rows the line waits on (a blocked row none of whose ``missing``
names has a blocked row of its own). Nothing here edits packages/ or tests/.
"""

from __future__ import annotations

import copy
import json
import os
import re
import sys
import tempfile
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

P = "tax.us.2025."
HARNESS = REPO / "docs/phases/engine-breadth/milestones/sale-family-audit-evidence/audit_harness.py"
Acts = list[dict[str, Any]]

WATCH = (
    "form1040.line-7a", "form1040.line-7b", "form1040.line-9", "form1040.line-11a", "form1040.line-15",
    "form1040.line-16", "form1040.line-24", "form1040.line-33", "form1040.line-37",
    "schedule-d.line-1a", "schedule-d.line-1b", "schedule-d.line-2", "schedule-d.line-3",
    "schedule-d.line-7", "schedule-d.line-8a", "schedule-d.line-8b", "schedule-d.line-9",
    "schedule-d.line-10", "schedule-d.line-15", "schedule-d.line-16", "schedule-d.line-21",
    "schedule-b.line-2", "schedule-b.line-4", "form1040.line-2a", "form1040.line-2b", "form1040.line-19",
)


def module(name: str, path: Path) -> Any:
    from tests import evidence_loader

    if evidence_loader.current_owner() is None:
        evidence_loader.activate("bnq_evidence")
    return evidence_loader.load(path, name)


def harness() -> Any:
    return module("bnq_harness", HARNESS)


def v87() -> Any:
    return harness().Core("v87", "v85", "v85")


def scratch(core_path: Path) -> Any:
    body = json.loads(core_path.read_text(encoding="utf-8"))
    return harness().Core(body["version"], body["registry"], body["release_version"],
                          content=Path(body["content"]), releases=Path(body["releases"]),
                          loader_from=body.get("loader_from"))


def core_from_env() -> Any:
    named = os.environ.get("BNQ_CORE")
    return scratch(Path(named)) if named else v87()


def scrub(text: str) -> str:
    text = text.replace(str(REPO), ".")
    return re.sub(r"/(?:Users|private|tmp|var|opt)/\S+", "<path>", text)


def num(value: Any) -> Any:
    if isinstance(value, str):
        try:
            number = float(value)
        except ValueError:
            return value
        return int(number) if number.is_integer() else number
    if isinstance(value, float) and value.is_integer():
        return int(value)
    return value


def short(name: Any) -> str:
    return str(name).removeprefix(P + "rule.").removeprefix(P)


def rule_publishes(core: Any) -> dict[str, str]:
    package = json.loads(core.package_path.read_text(encoding="utf-8"))
    found: dict[str, str] = {}
    for member in package["members"]:
        if member.get("role") != "computation":
            continue
        slug = str(member["id"]).removeprefix(P + "rule.")
        for name in (f"rule.{slug}.{member['version']}.json", f"rule.{slug}.json"):
            path = core.content / name
            if path.exists():
                body = json.loads(path.read_text(encoding="utf-8"))
                if body.get("version") == member["version"]:
                    found[str(member["id"])] = str(body.get("publishes"))
                    break
    return found


_PUBLISHES: dict[str, dict[str, str]] = {}


def roots_of(row: dict[str, Any], by_symbol: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    """The blocked rows ``row`` reaches whose ``missing`` names reach no further blocked row."""
    found: dict[tuple[str, str, str], dict[str, Any]] = {}
    seen: set[str] = set()

    def walk(current: dict[str, Any]) -> None:
        deeper = False
        for item in current.get("missing") or []:
            key = str(item)
            children = [r for r in by_symbol.get(key, []) if r.get("disposition") == "blocked"]
            if children:
                deeper = True
                if key in seen:
                    continue
                seen.add(key)
                for child in children:
                    walk(child)
        leaf = [str(m) for m in current.get("missing") or []
                if not [r for r in by_symbol.get(str(m), []) if r.get("disposition") == "blocked"]]
        if leaf or not deeper:
            entry = {"artifact": short(current.get("artifact_id")), "code": current.get("code"),
                     "missing": [short(m) for m in leaf][:12]}
            found[(entry["artifact"], str(entry["code"]), json.dumps(entry["missing"]))] = entry

    walk(row)
    return sorted(found.values(), key=lambda e: (e["artifact"], str(e["code"])))


def summarize(core: Any, outcome: Any) -> dict[str, Any]:
    if outcome.refusal is not None:
        return {"outcome": "refused", "reason": outcome.refusal.reason,
                "detail": scrub(str(outcome.refusal.detail))[:300]}
    key = str(core.package_path)
    if key not in _PUBLISHES:
        _PUBLISHES[key] = rule_publishes(core)
    publishes = _PUBLISHES[key]
    report = json.loads(outcome.output_path.read_text(encoding="utf-8"))
    model = json.loads(outcome.presentation_path.read_text(encoding="utf-8"))
    rows = report.get("dispositions") or []
    by_symbol: dict[str, list[dict[str, Any]]] = {}
    for row in rows:
        symbol = row.get("symbol") or publishes.get(str(row.get("artifact_id")))
        if symbol:
            by_symbol.setdefault(str(symbol), []).append(row)
    lines: dict[str, Any] = {}
    blocked: dict[str, Any] = {}
    questions: set[str] = set()
    for section in model.get("sections") or []:
        field = section.get("field") or {}
        field_id = short(field.get("id"))
        resolved = section.get("resolved") or {}
        disposition = str(resolved.get("disposition"))
        if field_id in WATCH:
            value = resolved.get("value")
            lines[field_id] = disposition if value is None or "blocked" in disposition else num(value)
        if "blocked" not in disposition:
            continue
        sentences = [scrub(str(r.get("sentence") or "").strip()) for r in resolved.get("reasons") or []
                     if isinstance(r, dict) and str(r.get("sentence") or "").strip()]
        asked = [s for s in sentences if "?" in s]
        questions.update(asked)
        symbol = str(field.get("binds_symbol"))
        own = [r for r in by_symbol.get(symbol, []) if r.get("disposition") == "blocked"]
        row = own[0] if own else {}
        blocked[field_id] = {
            "artifact": short(row.get("artifact_id")),
            "code": row.get("code"),
            "missing": [short(m) for m in row.get("missing") or []][:8],
            "reasons": sentences,
            "questions": asked,
            "roots": roots_of(row, by_symbol) if row else [],
        }
    publications = {short(p.finding.get("symbol")): num(p.finding.get("value")) for p in outcome.publications or ()}
    all_blocked = []
    all_dispositions = []
    for row in rows:
        symbol = row.get("symbol") or publishes.get(str(row.get("artifact_id")))
        all_dispositions.append({
            "artifact": short(row.get("artifact_id")),
            "symbol": short(symbol),
            "disposition": row.get("disposition"),
            "code": row.get("code"),
            "missing": [short(m) for m in row.get("missing") or []][:12],
        })
        if row.get("disposition") != "blocked":
            continue
        all_blocked.append({
            "artifact": short(row.get("artifact_id")),
            "symbol": short(symbol),
            "code": row.get("code"),
            "missing": [short(m) for m in row.get("missing") or []][:12],
        })
    return {
        "outcome": "success",
        "stop": report.get("stop_reason"),
        "lines": lines,
        "blocked": blocked,
        "questions": sorted(questions),
        "silent_blocked": sorted(f for f, b in blocked.items() if not b["questions"]),
        "reason_no_question": sorted(f for f, b in blocked.items() if b["reasons"] and not b["questions"]),
        "all_blocked": sorted(all_blocked, key=lambda item: (item["artifact"], str(item["code"]))),
        "all_dispositions": sorted(all_dispositions, key=lambda item: (
            item["artifact"], str(item["disposition"]), str(item["code"]))),
        "_publications": publications,
    }


def run(core: Any, acts: Acts, run_id: str, *, schemas: Any = None) -> dict[str, Any]:
    h = harness()
    surface = core.surface()
    with h.loader_entries(core):
        from packages.derivation import loader

        original_schemas = loader.DerivationSchemas
        if schemas is not None:
            loader.DerivationSchemas = lambda: schemas  # type: ignore[assignment]
        try:
            finished = h._handover(h._finish(copy.deepcopy(acts), package_path=core.package_path,
                                             package_version=core.version, release_path=core.release_path,
                                             release_version=core.release_version, note=run_id),
                                   surface=surface, reconfirm=True)
            with tempfile.TemporaryDirectory() as tmp:
                outcome = h.live_coordinate_run(
                    h.WorkspaceCapability(Path(tmp) / "L"), repo_root=REPO, authoritative_acts=finished,
                    workspace_revision=len(finished), run_scope={"jurisdiction": "us", "year": h.YEAR},
                    scope_user=h.ccr.USER, request={"schema": "run-request.v1"}, run_id=run_id,
                    governance_pins=[], surface=surface, output_name="out.json", schemas=schemas)
                return summarize(core, outcome)
        except Exception as exc:  # noqa: BLE001 - a rejected act list is a result
            return {"outcome": "error", "error": type(exc).__name__, "message": scrub(str(exc))[:300]}
        finally:
            loader.DerivationSchemas = original_schemas  # type: ignore[assignment]


def write(name: str, payload: Any) -> None:
    text = json.dumps(payload, indent=2) + "\n"
    for needle in ("/" + name + "/" for name in ("Users", "private", "tmp", "var")):
        if needle in text:
            raise SystemExit(f"{name} contains {needle}")
    (HERE / name).write_text(text, encoding="utf-8")
