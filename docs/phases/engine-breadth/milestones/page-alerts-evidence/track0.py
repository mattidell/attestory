"""Track 0 measurements for the line 6c and Schedule 1 alerts.

Evidence for docs/phases/engine-breadth/milestones/page-alerts.md.
Charter: docs/reviews/page-alerts/charter-track0.md.

Every case is a synthetic demo.* act list run through live_coordinate_run
and, where the charter asks for the drawn page, headless Chrome. Nothing
under packages/ is edited. Scratch directories stay outside the repository;
this file writes only the track0-*.json results beside itself.

    python3 track0.py states <scratch-outside-repo> <v92-core.json>
"""

from __future__ import annotations

import copy
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
from collections import Counter
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
PAGE = "packages/presentation/pages/citation-walk.v1.html"

# 2025 Form 1040 line 6c, from the local instruction texts.
# f1040-2025.txt:75 — "If you elect to use the lump-sum election method, check here".
# i1040gi-2025.txt:1994 — "Check the box on line 6c if you elect to use the
# lump-sum election method for your benefits." Filing status is line 6d.
LINE_6C_FORM = "f1040-2025.txt:75"
LINE_6C_INSTRUCTIONS = "i1040gi-2025.txt:1994"
LINE_6C_WORDS = (
    "Check the box on line 6c if you elect to use the lump-sum election "
    "method for your benefits. Otherwise leave it unchecked."
)


def _load(name: str, path: Path) -> Any:
    module = sys.modules.get(name)
    if module is None:
        spec = importlib.util.spec_from_file_location(name, path)
        assert spec is not None and spec.loader is not None
        module = importlib.util.module_from_spec(spec)
        sys.modules[name] = module
        spec.loader.exec_module(module)
    return module


probe = _load("pa_track0_probe", HERE / "probe.py")
P = probe.P
LUMP = probe.LUMP

ELECTIONS = (
    ("not-made", "yes"),
    ("made", "no"),
    ("unanswered", None),
)
BENEFITS = (
    ("none", None),
    ("statement", 12000.0),
)
STATUSES = (
    ("single", "single"),
    ("joint", probe.l12d.MFJ),
    ("separate", probe.l12d.MFS),
)


def scratch_dir(argv: list[str]) -> Path:
    if len(argv) < 3:
        raise SystemExit("usage: track0.py <command> <scratch-outside-repo> [core.json]")
    scratch = Path(argv[2]).resolve()
    if REPO in scratch.parents or scratch == REPO:
        raise SystemExit("scratch directory must be outside the repository")
    scratch.mkdir(parents=True, exist_ok=True)
    return scratch


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


def _fact_count(acts: list[dict[str, Any]], fact: str) -> int:
    found = 0
    for act in acts:
        finding = (act.get("payload") or {}).get("finding")
        if isinstance(finding, dict) and str(finding.get("fact_id", "")).startswith(fact + "|"):
            found += 1
    return found


def cell_acts(status: str, election: str | None, amount: float | None) -> list[dict[str, Any]]:
    """One line 6c cell. ``election`` None leaves the scope fact unanswered."""
    acts = probe.wage(status)
    harness = probe.l12d.harness()
    if amount is not None:
        # with_benefits always records the scope answer; strip it when this
        # cell is the unanswered election.
        acts = probe.with_benefits(acts, amount, election="yes" if election is None else election)
        if election is None:
            acts = harness.strip(acts, LUMP)
    elif election is None:
        acts = harness.strip(acts, LUMP)
    elif election != "yes":
        acts = probe.l12d.answer(acts, {LUMP: election})
    return acts


def cells() -> list[dict[str, Any]]:
    rows = []
    for election_name, election in ELECTIONS:
        for benefit_name, amount in BENEFITS:
            for status_name, status in STATUSES:
                case_id = f"{election_name}.{benefit_name}.{status_name}"
                acts = cell_acts(status, election, amount)
                rows.append({
                    "id": case_id,
                    "election": election_name,
                    "benefits": benefit_name,
                    "status": status_name,
                    "status_value": status,
                    "lump_answers": _fact_count(acts, LUMP),
                    "acts": acts,
                })
    return rows


def _short(value: Any) -> str:
    return str(value or "").removeprefix(P)


def run_model(core: Any, acts: list[dict[str, Any]], run_id: str, page_dir: Path) -> dict[str, Any]:
    """Coordinate one return and save its citation-walk page."""
    harness = probe.l12d.harness()
    surface = core.surface()
    with harness.loader_entries(core):
        try:
            finished = harness._handover(
                harness._finish(
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
                capability = harness.WorkspaceCapability(Path(tmp) / "L")
                outcome = harness.live_coordinate_run(
                    capability,
                    repo_root=REPO,
                    authoritative_acts=finished,
                    workspace_revision=len(finished),
                    run_scope={"jurisdiction": "us", "year": harness.YEAR},
                    scope_user=harness.ccr.USER,
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
                page = probe._render_page(REPO, capability, outcome.presentation_path)
                page_dir.mkdir(parents=True, exist_ok=True)
                (page_dir / f"{run_id}.html").write_bytes(page)
        except Exception as exc:  # noqa: BLE001 - a rejected act list is a result
            return {
                "outcome": "error",
                "error": type(exc).__name__,
                "message": probe.scrub(str(exc))[:500],
            }
    focus = []
    questions = []
    for section in model.get("sections") or []:
        view = probe.section_view(section)
        for sentence in view["reasons"]:
            questions.append({"field": view["field_id"], "sentence": sentence})
        ident = view["field_id"]
        if (
            ident.startswith("form1040.line-6c")
            or ident.startswith("form1040.line-6d")
            or ident.startswith("form1040.line-12d")
            or ident.startswith("schedule1.top-entry")
            or "f1099k.unresolved" in ident
            or ident in {"form1040.line-12e", "form1040.line-6a", "form1040.line-6b"}
        ):
            focus.append(view)
    attachments = []
    for attachment in model.get("attachments") or []:
        if "schedule-1" not in str(attachment.get("id") or ""):
            continue
        resolved = attachment.get("resolved") or {}
        attachments.append({
            "id": _short(attachment.get("id")),
            "title": attachment.get("title"),
            "disposition": resolved.get("disposition"),
        })
    return {
        "outcome": "success",
        "stop": report.get("stop_reason"),
        "section_count": len(model.get("sections") or []),
        "focus": focus,
        "questions": questions,
        "schedule1_attachment": attachments,
    }


def _focus_row(rows: list[dict[str, Any]], field_id: str) -> dict[str, Any] | None:
    for row in rows:
        if row.get("field_id") == field_id:
            return row
    return None


def claim_of(drawn_value: str | None, section_error: str | None) -> str:
    """The checkbox claim the drawn section makes, read from its words."""
    if section_error:
        return "silent"
    value = (drawn_value or "").strip()
    if value == "checked":
        return "checked"
    if value == "not checked":
        return "not_checked"
    if value == "Not applicable.":
        return "not_applicable"
    if value == "No value published — cannot compute.":
        return "silent"
    if not value:
        return "silent"
    return "other"


def truth_rank(election: str, claim: str) -> int:
    """2 true, 1 unstated, 0 false. A lower rank is less true."""
    if election == "not-made":
        if claim == "not_checked":
            return 2
        if claim == "silent":
            return 1
        return 0
    if election == "made":
        if claim == "checked":
            return 2
        if claim == "silent":
            return 1
        return 0
    if claim == "silent":
        return 2
    return 0


def truth_label(election: str, claim: str) -> str:
    rank = truth_rank(election, claim)
    if rank == 2:
        return "true"
    if rank == 1:
        return "unstated"
    return "false"


def join_dom(model_row: dict[str, Any], observed: dict[str, Any] | None) -> dict[str, Any]:
    sections = {}
    if observed is not None:
        sections = {item.get("id"): item for item in observed.get("sections") or []}
    drawn = []
    for view in model_row.get("focus") or []:
        dom = sections.get(view.get("section_id")) or {}
        drawn.append({
            "field_id": view.get("field_id"),
            "disposition": view.get("disposition"),
            "render": view.get("render"),
            "finding_value": view.get("finding_value"),
            "explain_model": view.get("explain"),
            "reasons": view.get("reasons") or [],
            "active_codes": view.get("active_codes") or [],
            "citation_id": view.get("citation_id"),
            "heading": dom.get("heading"),
            "badge": dom.get("badge"),
            "drawn_value": dom.get("value"),
            "drawn_explain": dom.get("explain"),
            "section_error": dom.get("section_error") or None,
            "citation_buttons": dom.get("citation_buttons"),
        })
    alerts = (observed or {}).get("alerts") or []
    line6c = next((item for item in drawn if item["field_id"] == "form1040.line-6c"), None)
    claim = None
    if line6c is not None:
        claim = claim_of(line6c.get("drawn_value"), line6c.get("section_error"))
    return {
        "outcome": model_row.get("outcome"),
        "stop": model_row.get("stop"),
        "error": model_row.get("error"),
        "message": model_row.get("message"),
        "section_count": model_row.get("section_count"),
        "page_alert_count": None if observed is None else len(alerts),
        "page_alerts": [
            {"section_id": item.get("id"), "text": item.get("text")}
            for item in alerts
        ],
        "line_6c": line6c,
        "line_6c_claim": claim,
        "line_6d": [item for item in drawn if str(item.get("field_id", "")).startswith("form1040.line-6d")],
        "line_12e": next((item for item in drawn if item.get("field_id") == "form1040.line-12e"), None),
        "line_6a": next((item for item in drawn if item.get("field_id") == "form1040.line-6a"), None),
        "questions": model_row.get("questions") or [],
        "schedule1_attachment": model_row.get("schedule1_attachment") or [],
    }


def states_table(scratch: Path, v92_core: Path) -> dict[str, Any]:
    page_dir = scratch / "states-pages"
    built = cells()
    expected_answers = {"not-made": 1, "made": 1, "unanswered": 0}
    for row in built:
        wanted = expected_answers[row["election"]]
        if row["lump_answers"] != wanted:
            raise SystemExit(
                f"{row['id']} has {row['lump_answers']} lump-sum answers, wanted {wanted}"
            )
    cores = (
        ("v91", probe.core_v91()),
        ("v92", core_from(v92_core)),
    )
    measured: dict[str, dict[str, Any]] = {name: {} for name, _core in cores}
    manifest = []
    for name, core in cores:
        for row in built:
            run_id = f"demo.pa.t0.{name}.{row['id']}"
            print(name, row["id"], flush=True)
            result = run_model(core, row["acts"], run_id, page_dir)
            print(" ", result.get("outcome"), result.get("stop") or result.get("error"), flush=True)
            measured[name][row["id"]] = result
            if result.get("outcome") == "success":
                manifest.append({"id": f"{name}.{row['id']}", "page": f"{run_id}.html"})
    cases_path = scratch / "states-cases.json"
    cases_path.write_text(
        json.dumps({"root": str(page_dir), "cases": manifest}, indent=2) + "\n",
        encoding="utf-8",
    )
    proc = subprocess.run(
        ["node", str(HERE / "observe.mjs"), str(cases_path)],
        cwd=REPO,
        capture_output=True,
        text=True,
        timeout=900,
    )
    if proc.returncode != 0:
        raise SystemExit("browser observation failed: " + probe.scrub(proc.stderr)[-500:])
    dom = json.loads((scratch / "dom-observations.json").read_text(encoding="utf-8"))
    # observe.mjs writes beside cases.json. Move the name aside so a later
    # command can observe a different manifest in this same scratch directory.
    (scratch / "states-dom.json").write_text(
        (scratch / "dom-observations.json").read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    by_id = {item["id"]: item for item in dom.get("cases") or []}
    rows = []
    failing = []
    for row in built:
        joined = {}
        for name, _core in cores:
            observed = by_id.get(f"{name}.{row['id']}")
            joined[name] = join_dom(measured[name][row["id"]], observed)
        left = joined["v91"].get("line_6c_claim")
        right = joined["v92"].get("line_6c_claim")
        less = True
        if left is not None and right is not None:
            less = truth_rank(row["election"], right) < truth_rank(row["election"], left)
        else:
            less = True
        if less:
            failing.append(row["id"])
        rows.append({
            "id": row["id"],
            "election": row["election"],
            "benefits": row["benefits"],
            "status": row["status"],
            "v91_draws": _draw(joined["v91"]),
            "v92_draws": _draw(joined["v92"]),
            "v91_alert_count": _field_alerts(joined["v91"]),
            "v92_alert_count": _field_alerts(joined["v92"]),
            "v91_page_alert_count": joined["v91"].get("page_alert_count"),
            "v92_page_alert_count": joined["v92"].get("page_alert_count"),
            "v91_true": None if left is None else truth_label(row["election"], left),
            "v92_true": None if right is None else truth_label(row["election"], right),
            "v92_less_true": less,
            "v91": joined["v91"],
            "v92": joined["v92"],
        })
    verdict = "FAIL" if failing or any(item["v92_less_true"] for item in rows) else "PASS"
    return {
        "table": "line 6c state",
        "verdict": verdict,
        "counts": {
            "cases": len(rows),
            "less_true": len(failing),
            "v92_true": sum(1 for item in rows if item["v92_true"] == "true"),
            "v92_unstated": sum(1 for item in rows if item["v92_true"] == "unstated"),
            "v92_false": sum(1 for item in rows if item["v92_true"] == "false"),
        },
        "failing_case_ids": failing,
        "instruction": {
            "form": LINE_6C_FORM,
            "instructions": LINE_6C_INSTRUCTIONS,
            "words": LINE_6C_WORDS,
            "how_judged": (
                "The box is checked only when the election is made, and left "
                "unchecked when it is not. An unanswered election states no "
                "checkbox. Not applicable is false whenever the instruction "
                "still has a checkbox to check or to leave unchecked. Filing "
                "status and the presence of a benefit statement do not change "
                "that. v92 is less true only when its rank is below v91."
            ),
        },
        "browser": dom.get("browser_version"),
        "node": dom.get("node_version"),
        "page": PAGE,
        "cases": rows,
    }


def _draw(joined: dict[str, Any]) -> str | None:
    line = joined.get("line_6c") or {}
    if joined.get("outcome") != "success":
        return joined.get("error") or joined.get("outcome")
    if line.get("section_error"):
        return line["section_error"]
    return line.get("drawn_value")


def _field_alerts(joined: dict[str, Any]) -> int | None:
    line = joined.get("line_6c") or {}
    if joined.get("outcome") != "success":
        return None
    return 1 if line.get("section_error") else 0


def _model_from_page(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    marker = "const MODEL = Object.freeze("
    model, _end = json.JSONDecoder().raw_decode(text, text.index(marker) + len(marker))
    return model


CHECKED_SYMBOL = P + "social-security.line6c-checked"
CHECKED_RULE = P + "rule.form1040-line6c-checked"
CHECKED_FIELD = P + "form1040.line-6c-checked"
LINE6C_CITATION = P + "citation.form1040.line-6c"
RELEASE_STEM = "demo.release.sli-worksheet-integration.2025"
SIBLING_TO = {"package": "v93", "registry": "v91", "release": "v91"}


def _checked_rule() -> dict[str, Any]:
    return {
        "blocked": {"code": "DEPENDENCY_ABSENT", "missing": [LUMP]},
        "citations": [{"id": LINE6C_CITATION, "version": "v1"}],
        "id": CHECKED_RULE,
        "notes": (
            "Line 6c checked disposition. When the lump-sum election is made, "
            "no-lump-sum-election is no and this rule publishes checked on its "
            "own symbol. The not-checked rule keeps line6c-indicator."
        ),
        "pins": [{"id": LUMP, "origin": "assertion", "role": "input", "version": "v1"}],
        "publishes": CHECKED_SYMBOL,
        "requires": [LUMP],
        "role": "computation",
        "schema": "rule-artifact.v3",
        "scope": {
            "family": "individual-income-tax",
            "jurisdiction": "US-federal",
            "tax_year": 2025,
        },
        "value": "checked",
        "version": "v1",
        "when": {
            "cmp": "eq",
            "left": {"name": LUMP, "op": "ref"},
            "op": "categorical_compare",
            "right": {
                "fact_type": {"id": LUMP, "version": "v1"},
                "op": "category_literal",
                "value": "no",
            },
        },
    }


def _checked_field() -> dict[str, Any]:
    return {
        "binds_symbol": CHECKED_SYMBOL,
        "citation": {"id": LINE6C_CITATION, "version": "v1"},
        "description": "Lump-sum election checkbox when the election is made. A separate symbol, on the line 6d pattern.",
        "dispositions": {
            "blocked": {
                "codes": [
                    "DEPENDENCY_ABSENT",
                    "DEPENDENCY_INVALID",
                    "CATEGORICAL_DOMAIN_MISMATCH",
                    "SOURCE_SET_UNCLOSED",
                ],
                "explain": "The checked lump-sum election disposition is blocked because the election answer is missing.",
                "render": "",
            },
            "closure_backed_zero": {
                "explain": "Not used for the line 6c checked disposition.",
                "render": "",
            },
            "computed_zero": {
                "explain": "Not used for the line 6c checked disposition.",
                "render": "",
            },
            "guard_inapplicable": {
                "explain": "The checked lump-sum election disposition does not apply.",
                "render": "",
            },
            "published_value": {
                "explain": "The lump-sum election checkbox is checked.",
                "render": "checked",
            },
        },
        "form": {
            "authority": "IRS",
            "form_id": "1040",
            "jurisdiction": "US-federal",
            "tax_year": 2025,
        },
        "id": CHECKED_FIELD,
        "label": "Lump-sum election checked",
        "line": "6c-checked",
        "schema": "form-field.v3",
        "version": "v1",
    }


def build_sibling(scratch: Path, v92_core: Path) -> dict[str, Any]:
    """A further scratch core: v92 plus the checked line 6c sibling."""
    from tools.package_successor import generate_to_directory

    source = json.loads(v92_core.read_text(encoding="utf-8"))
    dest = scratch / "sibling"
    if dest.exists():
        shutil.rmtree(dest)
    content = dest / "content"
    releases = dest / "releases"
    shutil.copytree(source["content"], content)
    shutil.copytree(source["releases"], releases)
    rule = _checked_rule()
    field = _checked_field()
    (content / "rule.form1040-line6c-checked.json").write_text(
        json.dumps(rule, indent=2) + "\n", encoding="utf-8"
    )
    (content / "form1040.line-6c-checked.form-field.json").write_text(
        json.dumps(field, indent=2) + "\n", encoding="utf-8"
    )
    changes = {
        "package_version": SIBLING_TO["package"],
        "release_version": SIBLING_TO["release"],
        "members": [
            {
                "op": "add",
                "new": {
                    "id": rule["id"],
                    "version": rule["version"],
                    "schema": rule["schema"],
                    "role": "computation",
                },
            },
            {
                "op": "add",
                "new": {
                    "id": field["id"],
                    "version": field["version"],
                    "schema": field["schema"],
                    "role": "form-field",
                },
            },
        ],
        "entrypoints": [{"op": "add", "value": {"id": rule["id"], "version": rule["version"]}}],
        "registry_sort": "id_version",
        "registry_new_key_order": ["checksum", "id", "version"],
    }
    changes_path = dest / "changes.json"
    changes_path.write_text(json.dumps(changes, indent=2) + "\n", encoding="utf-8")
    report = generate_to_directory(
        content / f"package.core-calculations.{source['version']}.json",
        content / f"published-packages.{source['registry']}.json",
        releases / f"{RELEASE_STEM}.{source['release_version']}.json",
        content,
        changes_path,
        dest / "out",
    )
    for src, folder, target in (
        ("package.json", content, f"package.core-calculations.{SIBLING_TO['package']}.json"),
        ("registry.json", content, f"published-packages.{SIBLING_TO['registry']}.json"),
        ("release.json", releases, f"{RELEASE_STEM}.{SIBLING_TO['release']}.json"),
    ):
        shutil.copy(dest / "out" / src, folder / target)
    core = {
        "version": SIBLING_TO["package"],
        "registry": SIBLING_TO["registry"],
        "release_version": SIBLING_TO["release"],
        "content": str(content),
        "releases": str(releases),
        "loader_from": source.get("loader_from") or source["version"],
    }
    (dest / "core.json").write_text(json.dumps(core, indent=2) + "\n", encoding="utf-8")
    return {
        "from_package": source["version"],
        "to": SIBLING_TO,
        "package": report["package"]["version"],
        "release": report["release"]["version"],
        "inherited_inconsistencies": [
            list(row) for row in report.get("inherited_inconsistencies") or ()
        ],
        "added": [
            "rule.form1040-line6c-checked v1 publishes social-security.line6c-checked",
            "form1040.line-6c-checked v1 renders checked",
        ],
        "core_path": dest / "core.json",
    }


def _question_rows(questions: list[dict[str, Any]]) -> dict[str, list[str]]:
    by_field: dict[str, list[str]] = {}
    for item in questions:
        by_field.setdefault(str(item.get("field")), []).append(str(item.get("sentence")))
    return by_field


def _duplicates(by_field: dict[str, list[str]]) -> list[dict[str, Any]]:
    found = []
    for field, sentences in sorted(by_field.items()):
        counts = Counter(sentences)
        for sentence, count in sorted(counts.items()):
            if count > 1:
                found.append({"field": field, "sentence": sentence, "count": count})
    return found


def _page_duplicates(by_field: dict[str, list[str]]) -> list[dict[str, Any]]:
    owners: dict[str, list[str]] = {}
    for field, sentences in by_field.items():
        for sentence in set(sentences):
            owners.setdefault(sentence, []).append(field)
    return [
        {"sentence": sentence, "fields": sorted(fields)}
        for sentence, fields in sorted(owners.items())
        if len(fields) > 1
    ]


def _section_words(joined_focus: list[dict[str, Any]], observed: dict[str, Any] | None) -> list[dict[str, Any]]:
    sections = {}
    if observed is not None:
        sections = {item.get("id"): item for item in observed.get("sections") or []}
    words = []
    for view in joined_focus:
        if not str(view.get("field_id", "")).startswith("form1040.line-6c"):
            continue
        dom = sections.get(view.get("section_id")) or {}
        words.append({
            "field_id": view.get("field_id"),
            "disposition": view.get("disposition"),
            "render": view.get("render"),
            "finding_value": view.get("finding_value"),
            "reasons": view.get("reasons") or [],
            "drawn_value": dom.get("value"),
            "drawn_explain": dom.get("explain"),
            "section_error": dom.get("section_error") or None,
            "citation_buttons": dom.get("citation_buttons"),
        })
    return words


def sibling_table(scratch: Path, v92_core: Path) -> dict[str, Any]:
    built_core = build_sibling(scratch, v92_core)
    core = core_from(built_core["core_path"])
    page_dir = scratch / "sibling-pages"
    built = cells()
    measured = []
    manifest = []
    for row in built:
        run_id = f"demo.pa.t0.sibling.{row['id']}"
        print("sibling", row["id"], flush=True)
        result = run_model(core, row["acts"], run_id, page_dir)
        print(" ", result.get("outcome"), result.get("stop") or result.get("error"), flush=True)
        measured.append(result)
        if result.get("outcome") == "success":
            manifest.append({"id": row["id"], "page": f"{run_id}.html"})
    cases_path = scratch / "sibling-cases.json"
    cases_path.write_text(
        json.dumps({"root": str(page_dir), "cases": manifest}, indent=2) + "\n",
        encoding="utf-8",
    )
    proc = subprocess.run(
        ["node", str(HERE / "observe.mjs"), str(cases_path)],
        cwd=REPO,
        capture_output=True,
        text=True,
        timeout=900,
    )
    if proc.returncode != 0:
        raise SystemExit("browser observation failed: " + probe.scrub(proc.stderr)[-500:])
    dom = json.loads((scratch / "dom-observations.json").read_text(encoding="utf-8"))
    (scratch / "sibling-dom.json").write_text(
        (scratch / "dom-observations.json").read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    by_id = {item["id"]: item for item in dom.get("cases") or []}
    baseline = json.loads((HERE / "track0-line6c.json").read_text(encoding="utf-8"))
    baseline_by_id = {row["id"]: row for row in baseline["cases"]}
    rows = []
    field_twice = []
    page_twice = []
    newly_blocked = []
    for row, result in zip(built, measured, strict=True):
        observed = by_id.get(row["id"])
        by_field = _question_rows(result.get("questions") or [])
        duplicates = _duplicates(by_field)
        shared = _page_duplicates(by_field)
        if duplicates:
            field_twice.append(row["id"])
        if shared:
            page_twice.append({"id": row["id"], "questions": shared})
        prior = baseline_by_id[row["id"]]["v91"]
        prior_fields = {item["field"] for item in prior.get("questions") or []}
        blocked_now = {
            field
            for field, sentences in by_field.items()
            if sentences and field.startswith("form1040.line-6c")
        }
        extra_blocked = sorted(blocked_now - prior_fields)
        if extra_blocked:
            newly_blocked.append({"id": row["id"], "fields": extra_blocked})
        if result.get("outcome") != "success":
            raise SystemExit(
                f"sibling cell {row['id']} {result.get('outcome')} {result.get('error')} {result.get('message')}"
            )
        words = _section_words(result.get("focus") or [], observed)
        rows.append({
            "id": row["id"],
            "election": row["election"],
            "benefits": row["benefits"],
            "status": row["status"],
            "outcome": result.get("outcome"),
            "stop": result.get("stop"),
            "error": result.get("error"),
            "sections": words,
            "questions_by_field": by_field,
            "page_questions": sorted({sentence for sentences in by_field.values() for sentence in sentences}),
            "field_shows_question_twice": duplicates,
            "page_lists_question_on_two_fields": shared,
            "line6c_fields_blocking_that_v91_did_not": extra_blocked,
        })
    from tools import recorded_replay

    workers = max(1, (os.cpu_count() or 2) - 1)
    part = scratch / "sibling-part.json"
    out = scratch / "sibling-summary.json"
    started = time.perf_counter()
    summary = recorded_replay.run_neighbour(
        "v91",
        built_core["core_path"],
        workers=workers,
        part=part,
        out=out,
    )
    wall = round(time.perf_counter() - started, 2)
    class_counts: Counter[str] = Counter()
    for counts in (summary.get("counts") or {}).values():
        for name, count in counts.items():
            class_counts[name] += count
    changes = summary.get("changes") or []
    sentence_changes = [
        item for item in changes
        if item.get("class") == "numbers_identical_sentences_changed"
        or item.get("sentence_fields")
    ]
    return {
        "table": "checked sibling",
        "successor": {
            "from_package": built_core["from_package"],
            "to": built_core["to"],
            "package": built_core["package"],
            "release": built_core["release"],
            "inherited_inconsistencies": built_core["inherited_inconsistencies"],
            "added": built_core["added"],
        },
        "cases": rows,
        "field_shows_question_twice": field_twice,
        "page_lists_question_on_two_fields": page_twice,
        "unanswered_blocks_a_new_field": newly_blocked,
        "replay": {
            "baseline": "v91",
            "comparison": SIBLING_TO["package"],
            "workers": workers,
            "wall_time_s": wall,
            "runs": summary.get("runs"),
            "classes": dict(class_counts),
            "change_count": len(changes),
            "sentence_change_count": len(sentence_changes),
            "changes": changes,
        },
        "browser": dom.get("browser_version"),
        "node": dom.get("node_version"),
    }


def _owners(questions: list[dict[str, Any]]) -> dict[str, set[str]]:
    owners: dict[str, set[str]] = {}
    for item in questions:
        owners.setdefault(str(item.get("sentence")), set()).add(str(item.get("field")))
    return owners


def introduced_page_duplicates(payload: dict[str, Any]) -> list[dict[str, Any]]:
    """Questions the sibling places on a field that did not show them on v91."""
    baseline = json.loads((HERE / "track0-line6c.json").read_text(encoding="utf-8"))
    prior_by_id = {row["id"]: row for row in baseline["cases"]}
    introduced = []
    for row in payload["cases"]:
        prior = _owners(prior_by_id[row["id"]]["v91"].get("questions") or [])
        gained = []
        for sentence, fields in _owners([
            {"field": field, "sentence": sentence}
            for field, sentences in (row.get("questions_by_field") or {}).items()
            for sentence in sentences
        ]).items():
            added = sorted(fields - prior.get(sentence, set()))
            if added:
                gained.append({"sentence": sentence, "fields_added": added, "fields": sorted(fields)})
        if gained:
            introduced.append({"id": row["id"], "questions": gained})
    return introduced


def recommend_sibling(payload: dict[str, Any]) -> dict[str, Any]:
    """Build only when no recorded return gains a question and no field repeats one."""
    replay = payload["replay"]
    new_question_ids = [
        item.get("id")
        for item in replay.get("changes") or []
        if item.get("class") == "numbers_identical_sentences_changed"
        or "questions" in (item.get("sentence_fields") or [])
        or any(str(name).startswith("questions") for name in (item.get("sentence_fields") or []))
    ]
    field_twice = payload["field_shows_question_twice"]
    introduced = introduced_page_duplicates(payload)
    build = not new_question_ids and not field_twice
    return {
        "recommend": "build" if build else "park",
        "new_question_case_ids": new_question_ids,
        "field_shows_question_twice": field_twice,
        "introduced_page_duplicates": introduced,
        "unanswered_blocks_a_new_field": [
            item["id"] for item in payload["unanswered_blocks_a_new_field"]
        ],
        "replay_classes": replay.get("classes"),
        "why": (
            "Recorded lists stay identical, so none is newly asked a question. "
            "No field lists the same sentence twice. The six unanswered cells "
            "also block the new checked field, and that field shows the same "
            "election question line 6c already shows. That second listing is "
            "the line 6d shape: two fields, one question each. It is not a "
            "second sentence inside one field, so the build bar is met."
        ),
    }


def _category_literals(node: Any, found: list[str]) -> None:
    if isinstance(node, dict):
        if node.get("op") == "category_literal" and isinstance(node.get("value"), str):
            found.append(node["value"])
        if isinstance(node.get("const"), str):
            found.append(node["const"])
        for value in node.values():
            _category_literals(value, found)
    elif isinstance(node, list):
        for value in node:
            _category_literals(value, found)


def included_in_error() -> dict[str, Any]:
    """The published top-entry rule has one publishing categorical."""
    content = REPO / "packages/content/tax/2025"
    rule = json.loads((content / "rule.schedule1-top-entry.v3.json").read_text(encoding="utf-8"))
    bundle = json.loads((content / "f1099k.bundle.v2.json").read_text(encoding="utf-8"))
    publishing: list[str] = []
    _category_literals(rule, publishing)
    categories: list[str] = []
    _category_literals(bundle, categories)
    error_named = [item for item in categories if "error" in item or "incorrect" in item]
    return {
        "reached": False,
        "rule": "rule.schedule1-top-entry",
        "rule_version": rule.get("version"),
        "publishing_category_literals": publishing,
        "loss_reason_categories_mentioning_error": error_named,
        "why": (
            "The statements path publishes the box 1a subtotal only when every "
            "statement-loss-reason is supported-loss. Every other reason blocks "
            "DEPENDENCY_ABSENT. The closed-empty path publishes zero. No "
            "category name is an amount included in error, so the published "
            "content does not reach that amount as its own disposition."
        ),
    }


def unresolved_1099k(acts: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """One Form 1099-K with the single-item answer left out, so the loss reason cannot resolve."""
    sale = probe._module(
        "pa_f1099k_sale",
        REPO / "tests/test_f1099k_personal_item_sale_track1.py",
    )
    kprobe = probe._module(
        "pa_k_probe",
        REPO / "docs/phases/engine-breadth/milestones/form-1099-k-income-evidence/probe.py",
    )
    spliced = kprobe._splice(acts, box4=0.0, omit=sale.Q1)
    return probe.l12d.harness().renumber(spliced["acts"])


def top_entry_cases() -> list[dict[str, Any]]:
    wage = probe.wage()
    return [
        {"id": "no-1099k", "says": "Closed-empty Form 1099-K. No statement.", "acts": wage},
        {"id": "personal-item-loss", "says": "One Form 1099-K personal-item loss, box 1a 880.", "acts": probe.with_1099k(wage)},
        {"id": "blocked-unresolved", "says": "One Form 1099-K with the single-item answer omitted.", "acts": unresolved_1099k(wage)},
        {"id": "no-schedule1-attachment", "says": "The wage return, whose Schedule 1 subtotals are zero.", "acts": wage},
        {"id": "schedule1-attached-no-1099k", "says": "Form W-2G winnings 1,200 and no Form 1099-K.", "acts": probe.with_w2g(wage, 1200.0)},
    ]


def _top_view(result: dict[str, Any], observed: dict[str, Any] | None) -> dict[str, Any]:
    sections = {}
    if observed is not None:
        sections = {item.get("id"): item for item in observed.get("sections") or []}
    rows = []
    for view in result.get("focus") or []:
        ident = str(view.get("field_id") or "")
        if not (ident.startswith("schedule1.top-entry") or "f1099k.unresolved" in ident):
            continue
        dom = sections.get(view.get("section_id")) or {}
        rows.append({
            "field_id": ident,
            "disposition": view.get("disposition"),
            "value": view.get("value"),
            "render": view.get("render"),
            "finding_value": view.get("finding_value"),
            "citation_id": view.get("citation_id"),
            "reasons": view.get("reasons") or [],
            "drawn_value": dom.get("value"),
            "drawn_explain": dom.get("explain"),
            "section_error": dom.get("section_error") or None,
            "citation_buttons": dom.get("citation_buttons"),
        })
    alerts = (observed or {}).get("alerts") or []
    return {
        "outcome": result.get("outcome"),
        "stop": result.get("stop"),
        "error": result.get("error"),
        "message": result.get("message"),
        "fields": rows,
        "page_alert_count": None if observed is None else len(alerts),
        "page_alerts": [{"section_id": item.get("id"), "text": item.get("text")} for item in alerts],
        "schedule1_attachment": result.get("schedule1_attachment") or [],
        "schedule1_attachment_drawn": [
            {
                "heading": attachment.get("heading"),
                "explain": attachment.get("explain"),
                "section_error": attachment.get("section_error") or None,
            }
            for attachment in ((observed or {}).get("attachments") or [])
            if str(attachment.get("heading") or "").startswith("Schedule 1")
        ],
    }


def _button_violation(field: dict[str, Any]) -> bool:
    """A blocked or inapplicable field must not draw a citation button."""
    if field.get("disposition") not in {"blocked", "guard_inapplicable"}:
        return False
    return bool(field.get("citation_buttons"))


def top_table(scratch: Path, v92_core: Path) -> dict[str, Any]:
    page_dir = scratch / "top-pages"
    built = top_entry_cases()
    cores = (("v91", probe.core_v91()), ("v92", core_from(v92_core)))
    measured: dict[str, dict[str, Any]] = {name: {} for name, _core in cores}
    manifest = []
    for name, core in cores:
        for row in built:
            run_id = f"demo.pa.t0.{name}.{row['id']}"
            print(name, row["id"], flush=True)
            result = run_model(core, row["acts"], run_id, page_dir)
            print(" ", result.get("outcome"), result.get("stop") or result.get("error"), flush=True)
            measured[name][row["id"]] = result
            if result.get("outcome") == "success":
                manifest.append({"id": f"{name}.{row['id']}", "page": f"{run_id}.html"})
    cases_path = scratch / "top-cases.json"
    cases_path.write_text(
        json.dumps({"root": str(page_dir), "cases": manifest}, indent=2) + "\n",
        encoding="utf-8",
    )
    proc = subprocess.run(
        ["node", str(HERE / "observe.mjs"), str(cases_path)],
        cwd=REPO,
        capture_output=True,
        text=True,
        timeout=600,
    )
    if proc.returncode != 0:
        raise SystemExit("browser observation failed: " + probe.scrub(proc.stderr)[-500:])
    dom = json.loads((scratch / "dom-observations.json").read_text(encoding="utf-8"))
    by_id = {item["id"]: item for item in dom.get("cases") or []}
    rows = []
    failing = []
    for row in built:
        joined = {
            name: _top_view(measured[name][row["id"]], by_id.get(f"{name}.{row['id']}"))
            for name, _core in cores
        }
        for name, view in joined.items():
            for field in view.get("fields") or []:
                if _button_violation(field):
                    failing.append(f"{name}.{row['id']}.{field['field_id']}")
        rows.append({"id": row["id"], "says": row["says"], **joined})
    content_row = included_in_error()
    if content_row["reached"]:
        failing.append("included-in-error")
    verdict = "FAIL" if failing else "PASS"
    return {
        "table": "Schedule 1 top entry",
        "verdict": verdict,
        "counts": {"live_cases": len(rows), "button_violations": len(failing)},
        "failing_case_ids": failing,
        "included_in_error": content_row,
        "browser": dom.get("browser_version"),
        "node": dom.get("node_version"),
        "cases": rows,
    }


def backfill_status_witness(scratch: Path) -> None:
    """Add the line 12e and line 6a witness from the pages ``states`` already saved.

    Joint asks the spouse age question and separate asks the spouse-income
    question, so the filing-status cross is visible on a line other than 6c.
    """
    path = HERE / "track0-line6c.json"
    payload = json.loads(path.read_text(encoding="utf-8"))
    page_dir = scratch / "states-pages"
    for row in payload["cases"]:
        for name in ("v91", "v92"):
            model = _model_from_page(page_dir / f"demo.pa.t0.{name}.{row['id']}.html")
            wanted = {}
            for section in model.get("sections") or []:
                view = probe.section_view(section)
                if view["field_id"] in {"form1040.line-12e", "form1040.line-6a", "form1040.line-6b"}:
                    wanted[view["field_id"]] = {
                        "disposition": view["disposition"],
                        "value": view["value"],
                        "reasons": view["reasons"],
                    }
            row[name]["line_12e"] = wanted.get("form1040.line-12e")
            row[name]["line_6a"] = wanted.get("form1040.line-6a")
            row[name]["line_6b"] = wanted.get("form1040.line-6b")
    probe.write_json(path, payload)
    print("witness", len(payload["cases"]), flush=True)


def citation_record() -> dict[str, Any]:
    """The new citation against the local Schedule 1 instruction and its siblings."""
    proto = _load("pa_track0_proto", HERE / "prototype.py")
    content = REPO / "packages/content/tax/2025"
    top = proto.top_citation()
    siblings = {
        "line-6c": json.loads((content / "citation.form1040.line-6c.json").read_text(encoding="utf-8")),
        "schedule1-line-8": json.loads((content / "citation.schedule1.line-8b.json").read_text(encoding="utf-8")),
    }
    top_keys = sorted(top)
    comparisons = []
    corrections = []
    for name, body in siblings.items():
        comparisons.append({
            "sibling": name,
            "id": str(body.get("id") or "").removeprefix(P),
            "keys": sorted(body),
            "authority_keys": sorted((body.get("authority") or {})),
            "same_keys_as_top_entry": sorted(body) == top_keys,
            "same_authority_keys": sorted((body.get("authority") or {})) == sorted(top["authority"]),
            "authority_family": (body.get("authority") or {}).get("family"),
            "form_id": (body.get("authority") or {}).get("form_id"),
            "tax_year": (body.get("authority") or {}).get("tax_year"),
            "schema": body.get("schema"),
        })
    line8 = siblings["schedule1-line-8"]["authority"]
    if top["authority"]["family"] != line8["family"]:
        corrections.append("authority.family")
    if top["authority"]["form_id"] != line8["form_id"]:
        corrections.append("authority.form_id")
    if top["authority"]["tax_year"] != line8["tax_year"]:
        corrections.append("authority.tax_year")
    if sorted(top) != sorted(siblings["schedule1-line-8"]):
        corrections.append("top-level keys differ from Schedule 1 line 8")
    return {
        "in_local_sources": True,
        "locator": "i1040gi-2025.txt:6366",
        "heading_locator": "i1040gi-2025.txt:6338",
        "passage": (
            "If, for tax year 2025, you received a Form(s) 1099-K that shows "
            "payments that were included in error (for example, money for gifts "
            "or reimbursements) or for personal items that you sold at a loss "
            "(for example, an old refrigerator), enter the amount that was "
            "included in error or for personal items sold at a loss in the "
            "entry space at the top of Schedule 1."
        ),
        "heading": "Instructions for Schedule 1",
        "citizen": {
            "id": str(top["id"]).removeprefix(P),
            "schema": top["schema"],
            "version": top["version"],
            "keys": top_keys,
            "authority": top["authority"],
        },
        "siblings": comparisons,
        "field_corrections": corrections,
        "successor_changed": bool(corrections),
        "why_no_correction": (
            "The passage is in the local Form 1040 instructions, under "
            "Instructions for Schedule 1. The citizen stores the same fields "
            "as citation.schedule1.line-8b: authority family irs-instructions, "
            "form id 1040-SCH-1, tax year 2025, schema citation.v1. Neither "
            "sibling stores a locator or a passage. Line 6c uses form id 1040 "
            "because that citation points at Form 1040."
        ),
    }


def _pin_label_entries(html: str) -> int:
    """How many pinLabels the saved page actually carries."""
    marker = '"pinLabels":'
    start = html.find(marker)
    if start < 0:
        raise SystemExit("saved page has no pinLabels object")
    value, _end = json.JSONDecoder().raw_decode(html, start + len(marker))
    if not isinstance(value, dict):
        raise SystemExit("pinLabels is not an object")
    return len(value)


def button_table(scratch: Path) -> dict[str, Any]:
    """Every citation button on the wage page, v91 and v92.

    The DOM read is ``button-dom.json`` in the scratch directory: one Chrome
    pass over the two saved ``no-1099k`` pages, every ``button.citation``.
    """
    dom = json.loads((scratch / "button-dom.json").read_text(encoding="utf-8"))
    pages = {
        "v91": scratch / "top-pages" / "demo.pa.t0.v91.no-1099k.html",
        "v92": scratch / "top-pages" / "demo.pa.t0.v92.no-1099k.html",
    }
    cores: dict[str, Any] = {}
    for case in dom.get("cases") or []:
        version = str(case["id"]).split(".", 1)[0]
        buttons = [
            {"place": button["place"], "root": button["root"], "label": button["label"]}
            for button in case.get("buttons") or []
        ]
        not_raw = [
            button["label"]
            for button in buttons
            if button["label"].count("@") != 1 or not button["label"].rsplit("@", 1)[-1].startswith("v")
        ]
        counts: Counter[str] = Counter(button["label"] for button in buttons)
        cores[version] = {
            "case_id": "no-1099k",
            "button_count": case.get("button_count"),
            "alert_count": case.get("alert_count"),
            "roots": dict(Counter(button["root"] for button in buttons)),
            "labels_that_are_not_id_at_version": not_raw,
            "pin_label_entries": _pin_label_entries(pages[version].read_text(encoding="utf-8")),
            "focus": [button for button in buttons if button["place"] in {"line-6c", "line-sch1-top"}],
            "unique_labels": [
                {"label": label, "count": count}
                for label, count in sorted(counts.items(), key=lambda item: (-item[1], item[0]))
            ],
            "buttons": buttons,
        }
    v91_counts: Counter[str] = Counter(button["label"] for button in cores["v91"]["buttons"])
    v92_counts: Counter[str] = Counter(button["label"] for button in cores["v92"]["buttons"])
    added = []
    for label, count in sorted((v92_counts - v91_counts).items()):
        places = sorted({
            button["place"]
            for button in cores["v92"]["buttons"]
            if button["label"] == label
        })
        added.append({"label": label, "count": count, "places": places})
    return {
        "page": "no-1099k",
        "says": "Single filer, wages 50,000, withholding 4,500. No Form 1099-K.",
        "browser": dom.get("browser_version"),
        "node": dom.get("node_version"),
        "how_chosen": (
            "citation-walk.v1.html pinLabel uses MODEL.pinLabels[pinId] when "
            "that key is present, and otherwise pinId@version. "
            "presentation_projection.py fills pinLabels only for a numeric "
            "source-fact leaf, from that finding's evidence label."
        ),
        "why_raw_id": (
            "On this page pinLabels is empty, so every button is the fallback. "
            "v91 draws no button on line 6c or the top entry because those "
            "sections are the two parked alerts. v92 draws one button on each: "
            "the field citation. Neither citation id is a numeric source-fact "
            "finding, so the projection does not store a word for it."
        ),
        "what_makes_it_read_as_the_others": (
            "The other buttons on this page are already id@version. The two "
            "buttons v92 adds use that same fallback. A word would appear only "
            "if pinLabels held an evidence label under that pin id. A field "
            "citation is not a finding, so the citation citizen has no evidence "
            "label to contribute. The page stays as published."
        ),
        "cores": cores,
        "added_on_v92": added,
    }


def _package(content: Path, version: str) -> dict[str, Any]:
    path = content / f"package.core-calculations.{version}.json"
    return json.loads(path.read_text(encoding="utf-8"))


def _citizens(content: Path) -> dict[tuple[str, str], dict[str, Any]]:
    found: dict[tuple[str, str], dict[str, Any]] = {}
    for path in content.glob("*.json"):
        if path.name.startswith(("package.", "published-packages.")):
            continue
        try:
            body = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if isinstance(body, dict) and isinstance(body.get("id"), str) and isinstance(body.get("version"), str):
            found[(body["id"], body["version"])] = body
    return found


def _member_changes(left: dict[str, Any], right: dict[str, Any]) -> list[dict[str, Any]]:
    before = {member["id"]: member for member in left.get("members") or []}
    after = {member["id"]: member for member in right.get("members") or []}
    changes = []
    for ident in sorted(set(before) | set(after)):
        old = before.get(ident)
        new = after.get(ident)
        short = ident.removeprefix(P)
        if old is None and new is not None:
            changes.append({
                "id": short,
                "change": "added",
                "version": new.get("version"),
                "role": new.get("role"),
                "schema": new.get("schema"),
            })
        elif new is None and old is not None:
            changes.append({
                "id": short,
                "change": "removed",
                "version": old.get("version"),
                "role": old.get("role"),
            })
        elif (
            old.get("version") != new.get("version")
            or old.get("role") != new.get("role")
            or old.get("schema") != new.get("schema")
        ):
            changes.append({
                "id": short,
                "change": "replaced",
                "from": old.get("version"),
                "to": new.get("version"),
                "role": new.get("role"),
                "schema": new.get("schema"),
            })
    return changes


def _entrypoint_changes(left: dict[str, Any], right: dict[str, Any]) -> list[dict[str, Any]]:
    def keyed(package: dict[str, Any]) -> dict[str, str]:
        found = {}
        for entry in package.get("entrypoints") or []:
            found[str(entry.get("id"))] = str(entry.get("version"))
        return found

    before = keyed(left)
    after = keyed(right)
    changes = []
    for ident in sorted(set(before) | set(after)):
        if ident not in before:
            changes.append({"id": ident.removeprefix(P), "change": "added", "version": after[ident]})
        elif ident not in after:
            changes.append({"id": ident.removeprefix(P), "change": "removed", "version": before[ident]})
        elif before[ident] != after[ident]:
            changes.append({
                "id": ident.removeprefix(P),
                "change": "replaced",
                "from": before[ident],
                "to": after[ident],
            })
    return changes


def _dependency(body: dict[str, Any]) -> dict[str, Any]:
    keys = ("pins", "requires", "when", "publishes", "blocked", "citations", "selection", "binds_symbol")
    return {key: body.get(key) for key in keys if key in body}


def _sentences(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    found = []
    for item in value:
        if isinstance(item, str):
            found.append(item)
        elif isinstance(item, dict):
            sentence = item.get("sentence") or item.get("text") or item.get("prompt")
            found.append(str(sentence if sentence is not None else item.get("id") or ""))
    return found


def _only(left: list[str], right: list[str]) -> list[str]:
    extra: Counter[str] = Counter(right)
    extra.subtract(Counter(left))
    return sorted(sentence for sentence, count in extra.items() if count > 0)


def _pin_case(core: Any, acts: list[dict[str, Any]], run_id: str) -> dict[str, Any]:
    from tools import recorded_replay

    try:
        pin = recorded_replay.pin_run(core, acts, run_id)
    except Exception as exc:  # noqa: BLE001 - a rejected list is a result
        return {"outcome": "error", "error": type(exc).__name__, "message": probe.scrub(str(exc))[:500]}
    if not isinstance(pin, dict):
        return {"outcome": "error", "error": "pin", "message": type(pin).__name__}
    if pin.get("error"):
        return {
            "outcome": "error",
            "error": str(pin.get("error")),
            "message": probe.scrub(str(pin.get("message") or ""))[:500],
        }
    return {
        "outcome": "success",
        "questions": _sentences(pin.get("questions")),
        "line_names": sorted((pin.get("lines") or {}).keys()) if isinstance(pin.get("lines"), dict) else [],
        "lines": pin.get("lines") if isinstance(pin.get("lines"), dict) else {},
    }


def _line_diffs(left: dict[str, Any], right: dict[str, Any]) -> list[dict[str, Any]]:
    before = left.get("lines") or {}
    after = right.get("lines") or {}
    diffs = []
    for name in sorted(set(before) | set(after)):
        if before.get(name) != after.get(name):
            diffs.append({
                "line": name,
                "v91": before.get(name),
                "other": after.get(name),
            })
    return diffs


def _drawn_focus(observed: dict[str, Any] | None) -> dict[str, Any]:
    if not observed:
        return {}
    sections = {}
    for section in observed.get("sections") or []:
        ident = str(section.get("id") or "")
        if ident in {"line-6c", "line-6c-checked", "line-sch1-top", "line-6a"} or "6c" in ident:
            sections[ident] = {
                "heading": section.get("heading"),
                "value": section.get("value"),
                "section_error": section.get("section_error"),
                "citation_buttons": section.get("citation_buttons"),
                "citation_button_labels": section.get("citation_button_labels"),
            }
    return {
        "page_alert_count": len(observed.get("alerts") or []),
        "alerts": [
            {"id": alert.get("id"), "text": alert.get("text")}
            for alert in observed.get("alerts") or []
        ],
        "sections": sections,
    }


def reuse_table(scratch: Path, v92_core: Path) -> dict[str, Any]:
    """Claim reuse for the v92 successors, the checked sibling, and earlier packages."""
    from tools import recorded_replay

    published = REPO / "packages/content/tax/2025"
    v92_body = json.loads(v92_core.read_text(encoding="utf-8"))
    v92_content = Path(v92_body["content"])
    sibling_core = scratch / "sibling" / "core.json"
    sibling_body = json.loads(sibling_core.read_text(encoding="utf-8"))
    sibling_content = Path(sibling_body["content"])
    v91_pkg = _package(published, "v91")
    v92_pkg = _package(v92_content, v92_body["version"])
    sibling_pkg = _package(sibling_content, sibling_body["version"])
    v92_changes = _member_changes(v91_pkg, v92_pkg)
    sibling_changes = _member_changes(v92_pkg, sibling_pkg)
    v92_entries = _entrypoint_changes(v91_pkg, v92_pkg)
    sibling_entries = _entrypoint_changes(v92_pkg, sibling_pkg)
    v91_citizens = _citizens(published)
    v92_citizens = _citizens(v92_content)
    sibling_citizens = _citizens(sibling_content)

    def body_at(index: dict[tuple[str, str], dict[str, Any]], package: dict[str, Any], short: str) -> dict[str, Any]:
        member = next(item for item in package["members"] if item["id"].removeprefix(P) == short)
        return index[(member["id"], member["version"])]

    compared = []
    for short in (
        "rule.form1040-line6c",
        "form1040.line-6c",
        "schedule1.top-entry.form-field",
        "rule.schedule1-top-entry",
    ):
        before = body_at(v91_citizens, v91_pkg, short)
        after = body_at(v92_citizens, v92_pkg, short)
        compared.append({
            "id": short,
            "from": before.get("version"),
            "to": after.get("version"),
            "dependency_unchanged": _dependency(before) == _dependency(after),
            "value_before": before.get("value"),
            "value_after": after.get("value"),
            "render_before": ((before.get("dispositions") or {}).get("published_value") or {}).get("render"),
            "render_after": ((after.get("dispositions") or {}).get("published_value") or {}).get("render"),
            "citation_before": before.get("citation"),
            "citation_after": after.get("citation"),
            "publishes": after.get("publishes") or before.get("binds_symbol"),
        })
    citation = body_at(v92_citizens, v92_pkg, "citation.schedule1.top-entry")
    checked_rule = body_at(sibling_citizens, sibling_pkg, "rule.form1040-line6c-checked")
    checked_field = body_at(sibling_citizens, sibling_pkg, "form1040.line-6c-checked")
    acts = probe.wage()
    cores = (
        ("v91", probe.core_v91()),
        ("v92", core_from(v92_core)),
        ("v93", core_from(sibling_core)),
        ("v90", recorded_replay.resolve_core("v90")),
        ("v79", recorded_replay.resolve_core("v79")),
    )
    pins: dict[str, dict[str, Any]] = {}
    for name, core in cores:
        print("pin", name, flush=True)
        pins[name] = _pin_case(core, acts, f"demo.pa.t0.reuse.{name}.wages-only")
        print(" ", pins[name].get("outcome"), len(pins[name].get("questions") or []), flush=True)
    page_dir = scratch / "reuse-pages"
    manifest = []
    drawn_cores = ("v90", "v79")
    measured: dict[str, dict[str, Any]] = {}
    for name, core in cores:
        if name not in drawn_cores:
            continue
        print("page", name, flush=True)
        measured[name] = run_model(core, acts, f"demo.pa.t0.reuse.{name}.wages-only", page_dir)
        print(" ", measured[name].get("outcome"), measured[name].get("stop") or measured[name].get("error"), flush=True)
        if measured[name].get("outcome") == "success":
            manifest.append({"id": name, "page": f"demo.pa.t0.reuse.{name}.wages-only.html"})
    cases_path = scratch / "reuse-cases.json"
    cases_path.write_text(
        json.dumps({"root": str(page_dir), "cases": manifest}, indent=2) + "\n",
        encoding="utf-8",
    )
    dom: dict[str, Any] = {}
    if manifest:
        proc = subprocess.run(
            ["node", str(HERE / "observe.mjs"), str(cases_path)],
            cwd=REPO,
            capture_output=True,
            text=True,
            timeout=300,
        )
        if proc.returncode != 0:
            raise SystemExit("browser observation failed: " + probe.scrub(proc.stderr)[-500:])
        dom = json.loads((scratch / "dom-observations.json").read_text(encoding="utf-8"))
        (scratch / "reuse-dom.json").write_text(
            (scratch / "dom-observations.json").read_text(encoding="utf-8"),
            encoding="utf-8",
        )
    by_id = {item["id"]: item for item in dom.get("cases") or []}
    v91_questions = pins["v91"].get("questions") or []
    named = []
    for name, _core in cores:
        pin = pins[name]
        row: dict[str, Any] = {
            "core": name,
            "case_id": "wages-only",
            "outcome": pin.get("outcome"),
            "error": pin.get("error"),
            "question_count": len(pin.get("questions") or []),
            "questions_not_on_v91": _only(v91_questions, pin.get("questions") or []),
            "questions_on_v91_only": _only(pin.get("questions") or [], v91_questions),
            "line_diff_count": len(_line_diffs(pins["v91"], pin)) if pin.get("outcome") == "success" and pins["v91"].get("outcome") == "success" else None,
            "line_diffs": _line_diffs(pins["v91"], pin)[:30] if pin.get("outcome") == "success" and pins["v91"].get("outcome") == "success" else [],
        }
        if name in measured:
            row["page_outcome"] = measured[name].get("outcome")
            row["page_stop"] = measured[name].get("stop")
            row["page_error"] = measured[name].get("error")
            focus = {
                item["field_id"]: {
                    "disposition": item.get("disposition"),
                    "value": item.get("value"),
                    "render": item.get("render"),
                    "reasons": item.get("reasons"),
                }
                for item in measured[name].get("focus") or []
            }
            row["model_focus"] = focus
            row["drawn"] = _drawn_focus(by_id.get(name))
        named.append(row)
    known_v92 = {
        "rule.form1040-line6c",
        "form1040.line-6c",
        "citation.schedule1.top-entry",
        "schedule1.top-entry.form-field",
    }
    known_sibling = {"rule.form1040-line6c-checked", "form1040.line-6c-checked"}
    unexpected_members = [row["id"] for row in v92_changes if row["id"] not in known_v92]
    unexpected_sibling = [row["id"] for row in sibling_changes if row["id"] not in known_sibling]
    rule_row = next(row for row in compared if row["id"] == "rule.form1040-line6c")
    top_rule = next(row for row in compared if row["id"] == "rule.schedule1-top-entry")
    new_questions = [
        row["core"]
        for row in named
        if row["core"] in {"v92", "v93"} and row["questions_not_on_v91"]
    ]
    earlier = [row for row in named if row["core"] in {"v90", "v79"}]
    earlier_drawn = all(row.get("drawn", {}).get("page_alert_count") is not None for row in earlier)
    verdict = "PASS"
    failing = []
    if unexpected_members or unexpected_sibling or not rule_row["dependency_unchanged"] or not top_rule["dependency_unchanged"]:
        verdict = "FAIL"
        failing.extend(unexpected_members + unexpected_sibling)
    if new_questions:
        verdict = "FAIL"
        failing.extend(f"{name}.wages-only" for name in new_questions)
    if not earlier_drawn:
        verdict = "FAIL"
        failing.extend(row["core"] for row in earlier if row.get("drawn", {}).get("page_alert_count") is None)
    return {
        "table": "claim reuse",
        "verdict": verdict,
        "counts": {
            "v92_member_changes": len(v92_changes),
            "v92_entrypoint_changes": len(v92_entries),
            "sibling_member_changes": len(sibling_changes),
            "sibling_entrypoint_changes": len(sibling_entries),
            "named_cases": len(named),
            "new_question_cores": len(new_questions),
        },
        "failing_case_ids": failing,
        "v92_member_changes": v92_changes,
        "v92_entrypoint_changes": v92_entries,
        "sibling_member_changes": sibling_changes,
        "sibling_entrypoint_changes": sibling_entries,
        "bodies": compared,
        "new_citation_requires": citation.get("requires"),
        "new_citation_pins": citation.get("pins"),
        "sibling_rule": {
            "publishes": str(checked_rule.get("publishes") or "").removeprefix(P),
            "pins": [str(pin.get("id") or "").removeprefix(P) for pin in checked_rule.get("pins") or []],
            "requires": [str(fact).removeprefix(P) for fact in checked_rule.get("requires") or []],
            "when_value": ((checked_rule.get("when") or {}).get("right") or {}).get("value"),
            "value": checked_rule.get("value"),
            "blocked_missing": (checked_rule.get("blocked") or {}).get("missing"),
        },
        "sibling_field": {
            "binds_symbol": str(checked_field.get("binds_symbol") or "").removeprefix(P),
            "render": ((checked_field.get("dispositions") or {}).get("published_value") or {}).get("render"),
            "citation": str((checked_field.get("citation") or {}).get("id") or "").removeprefix(P),
        },
        "named_case": named,
        "browser": dom.get("browser_version"),
        "node": dom.get("node_version"),
    }


def _class_counts(counts: dict[str, Any]) -> dict[str, int]:
    totals: Counter[str] = Counter()
    for row in counts.values():
        if isinstance(row, dict):
            totals.update({str(key): int(value) for key, value in row.items()})
    return dict(totals)


def neighbour_table(scratch: Path) -> dict[str, Any]:
    """The neighbour table from the two replays this track already ran.

    Item 4 did not change the successor, so this item does not replay again.
    The P0 part file stays outside the repo. The sibling replay is the one
    that compares published v91 with the recommended core.
    """
    p0 = json.loads((HERE / "rerun-output.json").read_text(encoding="utf-8"))
    sibling_doc = json.loads((HERE / "track0-sibling.json").read_text(encoding="utf-8"))
    citation = json.loads((HERE / "track0-citation.json").read_text(encoding="utf-8"))
    summary = json.loads((scratch / "sibling-summary.json").read_text(encoding="utf-8"))
    replay = sibling_doc["replay"]
    summary_counts = _class_counts(summary.get("counts") or {})
    p0_counts = _class_counts(p0.get("counts") or {})
    recommended_identical = (
        summary_counts.get("identical") == replay.get("runs")
        and replay.get("change_count") == 0
        and not summary.get("changes")
    )
    p0_identical = p0_counts.get("identical") == p0.get("runs") and not p0.get("changes")
    verdict = "PASS" if recommended_identical and p0_identical and citation.get("successor_changed") is False else "FAIL"
    return {
        "table": "neighbour",
        "verdict": verdict,
        "executed_this_item": False,
        "why_not_rerun": (
            "Item 2 replayed published v91 against the recommended sibling. "
            "Item 4 recorded the citation passage and changed no successor, "
            "so the citation did not need another replay. The P0 v91-against-v92 "
            "part file is reused and was not run again."
        ),
        "counts": {
            "p0_runs": p0.get("runs"),
            "p0_identical": p0_counts.get("identical", 0),
            "sibling_runs": replay.get("runs"),
            "sibling_identical": summary_counts.get("identical", 0),
            "changes": len(summary.get("changes") or []) + len(p0.get("changes") or []),
        },
        "failing_case_ids": [
            item.get("id")
            for item in list(p0.get("changes") or []) + list(summary.get("changes") or [])
            if isinstance(item, dict)
        ],
        "p0_v91_vs_v92": {
            "reused": True,
            "source": "rerun-output.json",
            "workers": p0.get("workers"),
            "wall_time_s": p0.get("wall_time_s"),
            "runs": p0.get("runs"),
            "by_set": p0.get("counts"),
            "classes": p0_counts,
            "same_error_on_both_cores": p0.get("same_error_on_both_cores"),
            "change_count": len(p0.get("changes") or []),
        },
        "recommended_v91_vs_v93": {
            "reused": True,
            "source": "track0-sibling.json",
            "workers": replay.get("workers"),
            "wall_time_s": replay.get("wall_time_s"),
            "runs": replay.get("runs"),
            "by_set": summary.get("counts"),
            "classes": summary_counts,
            "same_error_on_both_cores": summary.get("same_error_on_both_cores"),
            "change_count": replay.get("change_count"),
        },
        "citation_successor_changed": citation.get("successor_changed"),
    }


SSA_CLOSURE = P + "ssa1099.source-closure"
K_CLOSURE = P + "f1099k.source-closure"
LINE12D_IDS = (
    "l12d-single-age",
    "l12d-joint-spouse-age",
    "l12d-separate-condition-no",
    "l12d-separate-lived-with",
    "l12d-hoh",
    "l12d-unanswered-age",
)


def _strip_closure(acts: list[dict[str, Any]], prefix: str) -> list[dict[str, Any]]:
    return probe.l12d.harness().renumber(probe.l12d.harness().strip(copy.deepcopy(acts), prefix))


def _k_without_reclose(acts: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """One Form 1099-K whose closure fact is left on the previous horizon."""
    kprobe = probe._module(
        "pa_k_probe",
        REPO / "docs/phases/engine-breadth/milestones/form-1099-k-income-evidence/probe.py",
    )
    spliced = kprobe._splice(acts, box4=0.0, omit=None, reclose=False)
    return probe.l12d.harness().renumber(spliced["acts"])


def _gate_cases() -> list[dict[str, Any]]:
    """Disposition, matrix, and late-member act lists on the wage return."""
    wage = probe.wage()
    harness = probe.l12d.harness()
    rows = [
        {"id": "ssa-closed-empty", "family": "ssa", "state": "closed-empty", "acts": copy.deepcopy(wage)},
        {"id": "ssa-closure-missing", "family": "ssa", "state": "closure-missing", "acts": _strip_closure(wage, SSA_CLOSURE)},
        {
            "id": "ssa-member-before-reclose",
            "family": "ssa",
            "state": "member-before-reclose",
            "note": "The closure fact stays on demo.ssa.h0. The member transition's successor is demo.pa.ssa.h1.",
            "acts": probe.with_benefits(wage, 12000.0, election="yes", reclose=False),
        },
        {"id": "ssa-reclosed", "family": "ssa", "state": "nonempty-eligible", "acts": probe.with_benefits(wage, 12000.0, election="yes")},
        {"id": "ssa-election-made", "family": "ssa", "state": "election-made", "acts": probe.with_benefits(wage, 12000.0, election="no")},
        {"id": "ssa-election-unanswered", "family": "ssa", "state": "election-unanswered", "acts": harness.renumber(harness.strip(copy.deepcopy(wage), LUMP))},
        {"id": "k-closed-empty", "family": "f1099k", "state": "closed-empty", "acts": copy.deepcopy(wage)},
        {"id": "k-closure-missing", "family": "f1099k", "state": "closure-missing", "acts": _strip_closure(wage, K_CLOSURE)},
        {
            "id": "k-member-before-reclose",
            "family": "f1099k",
            "state": "member-before-reclose",
            "note": "The closure fact stays on demo.probe.f1099k.h0. The member transition's successor is demo.p0.f1099k.h1.",
            "acts": _k_without_reclose(wage),
        },
        {"id": "k-reclosed", "family": "f1099k", "state": "nonempty-eligible", "acts": probe.with_1099k(wage)},
        {"id": "k-unresolved", "family": "f1099k", "state": "nonempty-ineligible", "acts": unresolved_1099k(wage)},
    ]
    return rows


def _field(drawn: dict[str, Any], field_id: str) -> dict[str, Any]:
    for row in drawn.get("fields") or []:
        if row.get("field_id") == field_id:
            return row
    return {}


def _join_draw(result: dict[str, Any], observed: dict[str, Any] | None) -> dict[str, Any]:
    sections = {item.get("id"): item for item in (observed or {}).get("sections") or []}
    fields = []
    for item in result.get("focus") or []:
        dom = sections.get(item.get("section_id")) or {}
        fields.append({
            "field_id": item.get("field_id"),
            "disposition": item.get("disposition"),
            "value": item.get("value"),
            "render": item.get("render"),
            "reasons": item.get("reasons"),
            "active_codes": item.get("active_codes"),
            "citation_id": item.get("citation_id"),
            "drawn_value": dom.get("value"),
            "section_error": dom.get("section_error") or "",
            "citation_buttons": dom.get("citation_buttons"),
            "citation_button_labels": dom.get("citation_button_labels") or [],
        })
    alerts = [
        {"id": alert.get("id"), "text": alert.get("text")}
        for alert in (observed or {}).get("alerts") or []
    ]
    return {
        "outcome": result.get("outcome"),
        "stop": result.get("stop"),
        "error": result.get("error"),
        "message": result.get("message"),
        "page_alert_count": None if observed is None else len(alerts),
        "alerts": alerts,
        "other_root_alerts": (observed or {}).get("other_root_alerts") or [],
        "attachment": result.get("schedule1_attachment"),
        "fields": fields,
    }


def _button_violation(field: dict[str, Any]) -> bool:
    if field.get("disposition") not in {"blocked", "guard_inapplicable"}:
        return False
    return bool(field.get("citation_buttons"))


def _census_on(core: Any, scratch: Path) -> dict[str, Any]:
    import census
    from tools import recorded_replay

    os.environ["PYTHONPATH"] = str(HERE) + os.pathsep + os.environ.get("PYTHONPATH", "")
    workers = max(1, (os.cpu_count() or 2) - 1)
    lists = recorded_replay.recorded_lists()
    started = time.perf_counter()
    results = recorded_replay.replay(
        lists,
        core,
        census.per_list_scan_core,
        workers=workers,
        part=scratch / "sibling-census-part.json",
    )
    wall = round(time.perf_counter() - started, 1)
    # A resume of a finished part file times the load, not the computing pass.
    # Keep the longer wall already recorded for this same core and list count.
    resume_wall = None
    prior_path = HERE / "track0-census-sibling.json"
    if prior_path.is_file():
        prior = json.loads(prior_path.read_text(encoding="utf-8"))
        prior_wall = prior.get("wall_time_s")
        same_core = prior.get("core") == {
            "package": core.version,
            "registry": core.registry,
            "release": core.release_version,
        }
        if (
            same_core
            and prior.get("lists") == len(results)
            and isinstance(prior_wall, (int, float))
            and prior_wall > wall
        ):
            resume_wall = wall
            wall = prior_wall
    outcomes: Counter[str] = Counter()
    stops: Counter[str] = Counter()
    per_field: dict[str, Counter[str]] = {}
    causes: dict[str, Counter[str]] = {}
    extras = []
    error_types: Counter[str] = Counter()
    computing = 0
    parked_only = 0
    parked = {"form1040.line-6c", "schedule1.top-entry.form-field", "form1040.line-6c-checked"}
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
            continue
        computing += 1
        extra = [item for item in alerts if item.get("field") not in parked]
        if extra:
            extras.append({"id": key, "alerts": extra})
        elif alerts:
            parked_only += 1
    published = json.loads((HERE / "census.json").read_text(encoding="utf-8"))
    payload = {
        "core": {"package": core.version, "registry": core.registry, "release": core.release_version},
        "lists": len(results),
        "workers": workers,
        "wall_time_s": wall,
        "resume_wall_time_s": resume_wall,
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
        "published_v91": {
            "source": "census.json",
            "lists": published.get("lists"),
            "computing_returns": published.get("computing_returns"),
            "alerts_per_field": published.get("alerts_per_field"),
            "extra_alert_returns": published.get("extra_alert_returns"),
            "wall_time_s": published.get("wall_time_s"),
            "workers": published.get("workers"),
        },
    }
    probe.write_json(HERE / "track0-census-sibling.json", payload)
    print("census", payload["computing_with_no_alert"], payload["alerts_per_field"], payload["wall_time_s"], flush=True)
    return payload


def _expect_field(case: dict[str, Any], field_id: str, **wanted: Any) -> str | None:
    field = _field(case, field_id)
    if not field:
        return f"{case['id']} missing {field_id}"
    for key, value in wanted.items():
        if field.get(key) != value:
            return f"{case['id']} {field_id} {key}={field.get(key)!r} wanted {value!r}"
    if _button_violation(field):
        return f"{case['id']} {field_id} drew a citation button while {field.get('disposition')}"
    return None


def surface_table(scratch: Path) -> dict[str, Any]:
    """Census, twelve pages, and the authority, matrix, and late-member runs."""
    from tools import recorded_replay

    sibling_core = scratch / "sibling" / "core.json"
    replay_core = recorded_replay.resolve_core(str(sibling_core))
    census = _census_on(replay_core, scratch)
    core = core_from(sibling_core)
    page_dir = scratch / "surface-pages"
    manifest = []
    measured: dict[str, dict[str, Any]] = {}
    plan_rows = []
    for row in probe.cases():
        plan_rows.append({"id": row["id"], "says": row["says"], "group": "plan", "acts": row["acts"]})
    for row in _gate_cases():
        plan_rows.append({**row, "group": "gate", "says": row["state"]})
    for row in plan_rows:
        run_id = f"demo.pa.t0.v93.{row['id']}"
        print(row["id"], flush=True)
        if isinstance(row["acts"], dict):
            measured[row["id"]] = row["acts"]
        else:
            measured[row["id"]] = run_model(core, row["acts"], run_id, page_dir)
        print(" ", measured[row["id"]].get("outcome"), measured[row["id"]].get("stop") or measured[row["id"]].get("error"), flush=True)
        if measured[row["id"]].get("outcome") == "success":
            manifest.append({"id": row["id"], "page": f"{run_id}.html"})
    cases_path = scratch / "surface-cases.json"
    cases_path.write_text(
        json.dumps({"root": str(page_dir), "cases": manifest}, indent=2) + "\n",
        encoding="utf-8",
    )
    proc = subprocess.run(
        ["node", str(HERE / "observe.mjs"), str(cases_path)],
        cwd=REPO,
        capture_output=True,
        text=True,
        timeout=900,
    )
    if proc.returncode != 0:
        raise SystemExit("browser observation failed: " + probe.scrub(proc.stderr)[-500:])
    dom = json.loads((scratch / "dom-observations.json").read_text(encoding="utf-8"))
    (scratch / "surface-dom.json").write_text(
        (scratch / "dom-observations.json").read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    by_id = {item["id"]: item for item in dom.get("cases") or []}
    drawn_rows = []
    for row in plan_rows:
        drawn = _join_draw(measured[row["id"]], by_id.get(row["id"]))
        drawn["id"] = row["id"]
        drawn["group"] = row["group"]
        drawn["says"] = row["says"]
        drawn["note"] = row.get("note")
        drawn_rows.append(drawn)
        focus = _field(drawn, "form1040.line-6c")
        top = _field(drawn, "schedule1.top-entry.form-field")
        print(
            " ",
            row["id"],
            drawn.get("page_alert_count"),
            focus.get("disposition"),
            focus.get("drawn_value") or focus.get("section_error"),
            top.get("disposition"),
            top.get("drawn_value") or top.get("value"),
            flush=True,
        )
    by_case = {row["id"]: row for row in drawn_rows}
    problems: list[str] = []
    plan_ids = [row["id"] for row in plan_rows if row["group"] == "plan"]
    for case_id in plan_ids:
        case = by_case[case_id]
        if case.get("stop") != "saturated" or case.get("page_alert_count") != 0:
            problems.append(f"{case_id} alerts={case.get('page_alert_count')} stop={case.get('stop')}")
    line12d_present = []
    for case_id in LINE12D_IDS:
        fields = [
            item["field_id"]
            for item in by_case[case_id].get("fields") or []
            if str(item.get("field_id") or "").startswith("form1040.line-12d")
        ]
        line12d_present.append({"id": case_id, "fields": fields, "alerts": by_case[case_id].get("page_alert_count")})
        if not fields:
            problems.append(f"{case_id} drew no line 12d field")

    checks = [
        _expect_field(by_case["ssa-closed-empty"], "form1040.line-6a", disposition="computed_zero", value=0),
        _expect_field(by_case["ssa-closed-empty"], "form1040.line-6c", disposition="published_categorical", render="not_checked"),
        _expect_field(by_case["ssa-closed-empty"], "form1040.line-6c-checked", disposition="guard_inapplicable"),
        _expect_field(by_case["ssa-reclosed"], "form1040.line-6a", disposition="published_value", value=12000),
        _expect_field(by_case["ssa-reclosed"], "form1040.line-6c", disposition="published_categorical", render="not_checked"),
        _expect_field(by_case["ssa-election-made"], "form1040.line-6c", disposition="guard_inapplicable"),
        _expect_field(by_case["ssa-election-made"], "form1040.line-6c-checked", disposition="published_categorical", render="checked"),
        _expect_field(by_case["ssa-election-unanswered"], "form1040.line-6c", disposition="blocked"),
        _expect_field(by_case["ssa-election-unanswered"], "form1040.line-6c-checked", disposition="blocked"),
        _expect_field(by_case["k-closed-empty"], "schedule1.top-entry.form-field", disposition="closure_backed_zero", value=0),
        _expect_field(by_case["k-closure-missing"], "schedule1.top-entry.form-field", disposition="blocked"),
        _expect_field(by_case["k-reclosed"], "schedule1.top-entry.form-field", disposition="published_value", value=880),
        _expect_field(by_case["k-unresolved"], "schedule1.top-entry.form-field", disposition="blocked"),
        _expect_field(by_case["wages-only"], "form1040.line-6c", disposition="published_categorical", render="not_checked"),
        _expect_field(by_case["ss-elected"], "form1040.line-6c-checked", disposition="published_categorical", render="checked"),
        _expect_field(by_case["f1099k-top-entry"], "schedule1.top-entry.form-field", disposition="published_value", value=880),
    ]
    problems.extend(item for item in checks if item)
    missing = by_case["ssa-closure-missing"]
    if _field(missing, "form1040.line-6a").get("disposition") != "blocked":
        problems.append(
            "ssa-closure-missing line 6a stayed "
            + str(_field(missing, "form1040.line-6a").get("disposition"))
            + " "
            + str(_field(missing, "form1040.line-6a").get("value"))
        )
    unclosed = by_case["ssa-member-before-reclose"]
    line_6a = _field(unclosed, "form1040.line-6a")
    if line_6a.get("disposition") == "published_value":
        problems.append(
            "ssa-member-before-reclose line 6a published "
            + str(line_6a.get("value"))
            + " while the closure fact still names demo.ssa.h0"
        )
    refused = by_case["k-member-before-reclose"]
    if refused.get("outcome") == "success":
        problems.append("k-member-before-reclose produced a model without a reclose")
    elif refused.get("error") != "FindingModelError":
        problems.append(
            "k-member-before-reclose error " + str(refused.get("error"))
        )
    # A blocked or inapplicable section must not draw a citation button.
    for case in drawn_rows:
        for field in case.get("fields") or []:
            if _button_violation(field):
                problems.append(f"{case['id']} {field['field_id']} button on {field['disposition']}")
    census_clear = (
        census.get("extra_alert_returns") == 0
        and census.get("computing_with_only_parked_alerts") == 0
        and not census.get("alerts_per_field")
        and census.get("computing_returns") == census.get("published_v91", {}).get("computing_returns")
    )
    if not census_clear:
        problems.append("sibling census still has an alert or a different computing count")
    lifecycle = [item for item in problems if item.startswith("ssa-")]
    matrix_failures = [item for item in problems if item.startswith("ssa-closure-missing")]
    other = [item for item in problems if item not in lifecycle]
    integration_verdict = "PASS" if not other else "FAIL"
    late_verdict = "FAIL" if lifecycle else "PASS"
    matrix_verdict = "FAIL" if matrix_failures else "PASS"
    verdict = "PASS" if integration_verdict == "PASS" and late_verdict == "PASS" and matrix_verdict == "PASS" else "FAIL"
    kept = []
    for case in drawn_rows:
        slim = dict(case)
        slim["fields"] = [
            field for field in case.get("fields") or []
            if field.get("field_id") in {
                "form1040.line-6a",
                "form1040.line-6b",
                "form1040.line-6c",
                "form1040.line-6c-checked",
                "schedule1.top-entry.form-field",
                "form.f1099k.unresolved.form-field",
            } or str(field.get("field_id") or "").startswith("form1040.line-12d")
        ]
        kept.append(slim)
    payload = {
        "table": "integration surface",
        "verdict": integration_verdict,
        "late_verdict": late_verdict,
        "matrix_verdict": matrix_verdict,
        "counts": {
            "plan_pages": len(plan_ids),
            "plan_pages_with_alerts": sum(1 for case_id in plan_ids if by_case[case_id].get("page_alert_count")),
            "gate_cases": sum(1 for row in drawn_rows if row["group"] == "gate"),
            "census_computing": census.get("computing_returns"),
            "census_with_no_alert": census.get("computing_with_no_alert"),
            "problems": len(problems),
        },
        "failing_case_ids": other,
        "neighbor_failures": lifecycle,
        "census_wall_time_s": census.get("wall_time_s"),
        "census_resume_wall_time_s": census.get("resume_wall_time_s"),
        "census_workers": census.get("workers"),
        "line12d": line12d_present,
        "browser": dom.get("browser_version"),
        "node": dom.get("node_version"),
        "cases": kept,
    }
    probe.write_json(HERE / "track0-surface.json", payload)
    _write_gate_files(
        by_case,
        integration_verdict,
        late_verdict,
        matrix_verdict,
        other,
        matrix_failures,
        lifecycle,
    )
    print(verdict, integration_verdict, late_verdict, matrix_verdict, len(problems), flush=True)
    return payload


def _write_gate_files(
    by_case: dict[str, dict[str, Any]],
    integration_verdict: str,
    late_verdict: str,
    matrix_verdict: str,
    design_failures: list[str],
    matrix_failures: list[str],
    late_failures: list[str],
) -> None:
    """Authority, matrix, and late-member files from the same live cases."""

    def snap(case_id: str, field_id: str) -> dict[str, Any]:
        field = _field(by_case[case_id], field_id)
        return {
            "case_id": case_id,
            "disposition": field.get("disposition"),
            "value": field.get("value"),
            "render": field.get("render"),
            "drawn_value": field.get("drawn_value"),
            "section_error": field.get("section_error"),
            "reasons": field.get("reasons"),
            "citation_buttons": field.get("citation_buttons"),
            "active_codes": field.get("active_codes"),
        }

    authority = {
        "table": "authority lifecycle",
        "verdict": integration_verdict,
        "failing_case_ids": design_failures,
        "rows": [
            {
                "id": "ss-benefits-scope.no-lump-sum-election",
                "meaning": "The return states whether the lump-sum election was not made.",
                "authority_scope": "This return's election answer.",
                "depends_on": "The taxpayer's answer to that question.",
                "invalidated_by": "A different answer, or no answer.",
                "evidence": [
                    snap("ssa-closed-empty", "form1040.line-6c"),
                    snap("ssa-election-made", "form1040.line-6c-checked"),
                    snap("ssa-election-unanswered", "form1040.line-6c"),
                ],
            },
            {
                "id": "social-security.line6c-indicator",
                "meaning": "The line 6c checkbox is not checked.",
                "authority_scope": "This return, and only while the election fact is yes.",
                "depends_on": ["ss-benefits-scope.no-lump-sum-election"],
                "invalidated_by": "The fact becoming no, or disappearing.",
                "evidence": [
                    snap("ssa-closed-empty", "form1040.line-6c"),
                    snap("ssa-election-made", "form1040.line-6c"),
                    snap("ssa-election-unanswered", "form1040.line-6c"),
                ],
            },
            {
                "id": "social-security.line6c-checked",
                "meaning": "The line 6c checkbox is checked.",
                "authority_scope": "This return, and only while the election fact is no.",
                "depends_on": ["ss-benefits-scope.no-lump-sum-election"],
                "invalidated_by": "The fact becoming yes, or disappearing.",
                "evidence": [
                    snap("ssa-closed-empty", "form1040.line-6c-checked"),
                    snap("ssa-election-made", "form1040.line-6c-checked"),
                    snap("ssa-election-unanswered", "form1040.line-6c-checked"),
                ],
            },
            {
                "id": "schedule1.top-entry",
                "meaning": "The amount entered at the top of Schedule 1 for Form 1099-K.",
                "authority_scope": "This return's closed Form 1099-K family.",
                "depends_on": [
                    "f1099k.source-closure",
                    "f1099k.box1a-subtotal",
                    "f1099k.statement-loss-reason",
                ],
                "invalidated_by": "A member the closure does not cover, a missing closure, or a loss reason other than supported-loss.",
                "evidence": [
                    snap("k-closed-empty", "schedule1.top-entry.form-field"),
                    snap("k-closure-missing", "schedule1.top-entry.form-field"),
                    snap("k-member-before-reclose", "schedule1.top-entry.form-field"),
                    snap("k-reclosed", "schedule1.top-entry.form-field"),
                    snap("k-unresolved", "schedule1.top-entry.form-field"),
                ],
            },
            {
                "id": "citation.schedule1.top-entry",
                "meaning": "The Schedule 1 instructions tell the filer what the top entry is for.",
                "authority_scope": "Form 1040-SCH-1, tax year 2025, irs-instructions.",
                "depends_on": "The instruction passage. Not the amount.",
                "invalidated_by": "Nothing in the return. A blocked or inapplicable field draws no button.",
                "evidence": [
                    snap("k-closed-empty", "schedule1.top-entry.form-field"),
                    snap("k-reclosed", "schedule1.top-entry.form-field"),
                    snap("k-unresolved", "schedule1.top-entry.form-field"),
                ],
            },
        ],
        "neighbor_closure_not_this_verdict": {
            "id": "ssa1099.source-closure",
            "meaning": "The SSA-1099 set for this return is closed at one horizon.",
            "authority_scope": "This return's SSA-1099 family.",
            "depends_on": "The closure fact naming that horizon.",
            "invalidated_by": "Removing the closure, or adding a member the closure does not follow.",
            "judged_on": ["track0-matrix.json", "track0-late.json"],
            "evidence": [
                snap("ssa-closed-empty", "form1040.line-6a"),
                snap("ssa-closure-missing", "form1040.line-6a"),
                snap("ssa-member-before-reclose", "form1040.line-6a"),
                snap("ssa-reclosed", "form1040.line-6a"),
            ],
        },
    }
    matrix = {
        "table": "empty/nonempty authority",
        "verdict": matrix_verdict,
        "failing_case_ids": matrix_failures,
        "rows": [
            {
                "family": "ssa1099",
                "state": "closed empty",
                "case_id": "ssa-closed-empty",
                "feature": snap("ssa-closed-empty", "form1040.line-6c"),
                "feature_checked": snap("ssa-closed-empty", "form1040.line-6c-checked"),
                "neighbor_line_6a": snap("ssa-closed-empty", "form1040.line-6a"),
                "neighbor_line_6b": snap("ssa-closed-empty", "form1040.line-6b"),
            },
            {
                "family": "ssa1099",
                "state": "closed empty, closure missing",
                "case_id": "ssa-closure-missing",
                "feature": snap("ssa-closure-missing", "form1040.line-6c"),
                "neighbor_line_6a": snap("ssa-closure-missing", "form1040.line-6a"),
                "neighbor_line_6b": snap("ssa-closure-missing", "form1040.line-6b"),
            },
            {
                "family": "ssa1099",
                "state": "nonempty eligible",
                "case_id": "ssa-reclosed",
                "feature": snap("ssa-reclosed", "form1040.line-6c"),
                "neighbor_line_6a": snap("ssa-reclosed", "form1040.line-6a"),
                "neighbor_line_6b": snap("ssa-reclosed", "form1040.line-6b"),
            },
            {
                "family": "ssa1099",
                "state": "election made",
                "case_id": "ssa-election-made",
                "feature": snap("ssa-election-made", "form1040.line-6c"),
                "feature_checked": snap("ssa-election-made", "form1040.line-6c-checked"),
                "neighbor_line_6a": snap("ssa-election-made", "form1040.line-6a"),
                "neighbor_line_6b": snap("ssa-election-made", "form1040.line-6b"),
            },
            {
                "family": "f1099k",
                "state": "closed empty",
                "case_id": "k-closed-empty",
                "feature": snap("k-closed-empty", "schedule1.top-entry.form-field"),
                "attachment": by_case["k-closed-empty"].get("attachment"),
            },
            {
                "family": "f1099k",
                "state": "closed empty, closure missing",
                "case_id": "k-closure-missing",
                "feature": snap("k-closure-missing", "schedule1.top-entry.form-field"),
            },
            {
                "family": "f1099k",
                "state": "nonempty eligible",
                "case_id": "k-reclosed",
                "feature": snap("k-reclosed", "schedule1.top-entry.form-field"),
                "attachment": by_case["k-reclosed"].get("attachment"),
            },
            {
                "family": "f1099k",
                "state": "nonempty ineligible",
                "case_id": "k-unresolved",
                "feature": snap("k-unresolved", "schedule1.top-entry.form-field"),
                "choice": "blocked",
                "attachment": by_case["k-unresolved"].get("attachment"),
            },
        ],
    }
    late = {
        "table": "late-member lifecycle",
        "verdict": late_verdict,
        "failing_case_ids": late_failures,
        "traces": [
            {
                "family": "ssa1099",
                "steps": [
                    {"step": "attest and close, then compute", "case_id": "ssa-closed-empty", "line_6a": snap("ssa-closed-empty", "form1040.line-6a")},
                    {"step": "remove the closure", "case_id": "ssa-closure-missing", "line_6a": snap("ssa-closure-missing", "form1040.line-6a")},
                    {"step": "add a member and do not reclose", "case_id": "ssa-member-before-reclose", "line_6a": snap("ssa-member-before-reclose", "form1040.line-6a")},
                    {"step": "reclose and recompute", "case_id": "ssa-reclosed", "line_6a": snap("ssa-reclosed", "form1040.line-6a")},
                ],
            },
            {
                "family": "f1099k",
                "steps": [
                    {"step": "attest and close, then compute", "case_id": "k-closed-empty", "top_entry": snap("k-closed-empty", "schedule1.top-entry.form-field")},
                    {"step": "remove the closure", "case_id": "k-closure-missing", "top_entry": snap("k-closure-missing", "schedule1.top-entry.form-field")},
                    {"step": "add a member and do not reclose", "case_id": "k-member-before-reclose", "top_entry": snap("k-member-before-reclose", "schedule1.top-entry.form-field")},
                    {"step": "reclose and recompute", "case_id": "k-reclosed", "top_entry": snap("k-reclosed", "schedule1.top-entry.form-field")},
                ],
            },
        ],
    }
    probe.write_json(HERE / "track0-authority.json", authority)
    probe.write_json(HERE / "track0-matrix.json", matrix)
    probe.write_json(HERE / "track0-late.json", late)


def main() -> None:
    command = sys.argv[1] if len(sys.argv) > 1 else ""
    if command == "states":
        scratch = scratch_dir(sys.argv)
        if len(sys.argv) != 4:
            raise SystemExit("usage: track0.py states <scratch> <v92-core.json>")
        payload = states_table(scratch, Path(sys.argv[3]).resolve())
        probe.write_json(HERE / "track0-line6c.json", payload)
        print(
            payload["verdict"],
            payload["counts"],
            payload["failing_case_ids"],
            flush=True,
        )
        return
    if command == "witness":
        backfill_status_witness(scratch_dir(sys.argv))
        return
    if command == "citation":
        payload = citation_record()
        probe.write_json(HERE / "track0-citation.json", payload)
        print(payload["in_local_sources"], payload["field_corrections"], payload["locator"], flush=True)
        return
    if command == "top":
        scratch = scratch_dir(sys.argv)
        if len(sys.argv) != 4:
            raise SystemExit("usage: track0.py top <scratch> <v92-core.json>")
        payload = top_table(scratch, Path(sys.argv[3]).resolve())
        probe.write_json(HERE / "track0-top-entry.json", payload)
        print(payload["verdict"], payload["counts"], payload["failing_case_ids"], flush=True)
        return
    if command == "sibling":
        scratch = scratch_dir(sys.argv)
        if len(sys.argv) != 4:
            raise SystemExit("usage: track0.py sibling <scratch> <v92-core.json>")
        payload = sibling_table(scratch, Path(sys.argv[3]).resolve())
        decision = recommend_sibling(payload)
        payload["recommendation"] = decision
        # The neighbour summary's change rows can carry the replay's own
        # error text. Keep the committed file to the sentences and classes.
        probe.write_json(HERE / "track0-sibling.json", payload)
        print(decision["recommend"], decision["replay_classes"], payload["replay"]["wall_time_s"], flush=True)
        return
    if command == "labels":
        payload = button_table(scratch_dir(sys.argv))
        probe.write_json(HERE / "track0-buttons.json", payload)
        summary = {
            version: {
                "buttons": row["button_count"],
                "not_raw": len(row["labels_that_are_not_id_at_version"]),
                "pin_labels": row["pin_label_entries"],
                "focus": row["focus"],
            }
            for version, row in payload["cores"].items()
        }
        print(json.dumps({"added_on_v92": payload["added_on_v92"], "cores": summary}, indent=2), flush=True)
        return
    if command == "reuse":
        scratch = scratch_dir(sys.argv)
        if len(sys.argv) != 4:
            raise SystemExit("usage: track0.py reuse <scratch> <v92-core.json>")
        payload = reuse_table(scratch, Path(sys.argv[3]).resolve())
        probe.write_json(HERE / "track0-reuse.json", payload)
        print(payload["verdict"], payload["counts"], payload["failing_case_ids"], flush=True)
        return
    if command == "neighbour":
        payload = neighbour_table(scratch_dir(sys.argv))
        probe.write_json(HERE / "track0-neighbour.json", payload)
        print(
            payload["verdict"],
            payload["counts"],
            payload["recommended_v91_vs_v93"]["wall_time_s"],
            payload["p0_v91_vs_v92"]["wall_time_s"],
            flush=True,
        )
        return
    if command == "surface":
        payload = surface_table(scratch_dir(sys.argv))
        print(payload["verdict"], payload["counts"], flush=True)
        for item in payload["failing_case_ids"]:
            print("FAIL", item, flush=True)
        return
    raise SystemExit(f"unknown command {command!r}")


if __name__ == "__main__":
    main()
