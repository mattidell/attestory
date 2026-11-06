"""Scratch core v78 for three form-field explanation successors.

Nothing is written under packages/. The script copies the committed content
and release directories to a temporary directory, writes three form-field v2
files there (the drafted sentences for the generic dispositions only), and
builds package v78 / registry v76 / release v76 with tools/package_successor.py.
An in-process wrapper gives v78 the companion declaration v77 already has.
It does not edit the loader.

The wages return is run on v77 and on the scratch v78. Values and dispositions
must match. The three succeeded explains change. Line 16, which is not
succeeded, keeps its v77 sentence.

    python3 docs/phases/engine-breadth/milestones/line-explanations-evidence/prototype.py

Writes prototype-output.json and the three field files under prototype-fields/.
Synthetic demo.* data only.
"""

from __future__ import annotations

import json
import shutil
import sys
import tempfile
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(HERE))

import probe  # noqa: E402
from packages.tax import loader  # noqa: E402
from tests.helpers import current_core_returns as ccr  # noqa: E402
from tools.package_successor import generate_to_directory  # noqa: E402

PACKAGE_ID = "tax.us.2025.package.core-calculations"
TARGETS = (
    "tax.us.2025.form1040.line-9",
    "tax.us.2025.form1040.line-12e",
    "tax.us.2025.schedule-d.line-7",
)
CONTROL = "tax.us.2025.form1040.line-16"
PATH_LEAK = probe.PATH_LEAK


def _load(path: Path) -> dict[str, Any]:
    body = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(body, dict):
        raise SystemExit(f"expected an object: {path.name}")
    return body


def _find(content: Path, citizen_id: str, version: str) -> Path:
    for path in sorted(content.glob("*.json")):
        try:
            body = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        if isinstance(body, dict) and body.get("id") == citizen_id and body.get("version") == version:
            return path
    raise SystemExit(f"missing {citizen_id} {version}")


def _successor_name(source: Path, old_version: str, new_version: str) -> str:
    name = source.name
    suffixed = f".form-field.{old_version}.json"
    if name.endswith(suffixed):
        return name[: -len(suffixed)] + f".form-field.{new_version}.json"
    plain = ".form-field.json"
    if name.endswith(plain):
        return name[: -len(plain)] + f".form-field.{new_version}.json"
    raise SystemExit(f"unexpected field filename: {name}")


def _drafts(inventory: dict[str, Any]) -> dict[str, dict[str, str]]:
    found: dict[str, dict[str, str]] = {}
    for field in inventory["fields"]:
        if field["id"] not in TARGETS:
            continue
        texts = {}
        for code, item in field["dispositions"].items():
            if item["class"] == "generic":
                texts[code] = item["draft"]["text"]
        found[field["id"]] = texts
    missing = [citizen_id for citizen_id in TARGETS if citizen_id not in found]
    if missing:
        raise SystemExit(f"inventory has no drafts for {missing}")
    return found


def _write_fields(content: Path, drafts: dict[str, dict[str, str]], fields_dir: Path) -> list[dict[str, str]]:
    fields_dir.mkdir(parents=True, exist_ok=True)
    written: list[dict[str, str]] = []
    for citizen_id in TARGETS:
        source = _find(content, citizen_id, "v1")
        body = _load(source)
        body["version"] = "v2"
        replaced = []
        for code, text in drafts[citizen_id].items():
            body["dispositions"][code]["explain"] = text
            replaced.append(code)
        name = _successor_name(source, "v1", "v2")
        text = json.dumps(body, indent=2) + "\n"
        if PATH_LEAK.search(text):
            raise SystemExit(f"field file contains a local path: {name}")
        (content / name).write_text(text, encoding="utf-8")
        (fields_dir / name).write_text(text, encoding="utf-8")
        written.append({
            "id": citizen_id,
            "from_version": "v1",
            "version": "v2",
            "schema": str(body["schema"]),
            "file": name,
            "replaced_dispositions": replaced,
        })
    return written


def _declare_v78() -> None:
    original = loader.domain_package_companion_declarations

    def with_v78() -> dict[tuple[str, str], dict[str, Any]]:
        declarations = dict(original())
        declarations[(PACKAGE_ID, "v78")] = declarations[(PACKAGE_ID, "v77")]
        return declarations

    loader.domain_package_companion_declarations = with_v78  # type: ignore[method-assign]


def _rows(raw: dict[str, Any]) -> dict[str, dict[str, Any]]:
    if not raw.get("reachable"):
        return {}
    return {
        str(view["field_id"]): {
            "disposition": view["disposition"],
            "value": view["value"],
            "explain": view["explain"],
            "line": view["line"],
            "section_id": view["section_id"],
        }
        for view in probe.section_view(raw["model"], None)
    }


def _page_hits(raw: dict[str, Any], wanted: set[str]) -> dict[str, Any]:
    if not raw.get("reachable"):
        return {"browser": False, "rows": {}}
    ids = {str(section.get("id")) for section in raw["model"].get("sections", [])}
    rendered = probe.rendered_text(raw["page"], ids)
    rows = {}
    for view in probe.section_view(raw["model"], rendered):
        if view["field_id"] not in wanted:
            continue
        page_text = view.get("rendered") or ""
        explain = view.get("explain") or ""
        rows[str(view["field_id"])] = {
            "line": view["line"],
            "disposition": view["disposition"],
            "value": view["value"],
            "explain": explain,
            "explain_in_rendered_page": bool(explain) and explain in page_text,
            "browser": rendered is not None,
        }
    return {"browser": rendered is not None, "rows": rows}


def build(scratch: Path, drafts: dict[str, dict[str, str]]) -> tuple[dict[str, Any], list[dict[str, str]]]:
    content, releases = scratch / "content", scratch / "releases"
    shutil.copytree(ccr.CONTENT, content)
    shutil.copytree(ccr.RELEASE_DIR, releases)
    written = _write_fields(content, drafts, HERE / "prototype-fields")
    members = []
    for item in written:
        pin = {"id": item["id"], "role": "form-field", "schema": item["schema"]}
        members.append({
            "op": "replace",
            "old": {**pin, "version": "v1"},
            "new": {**pin, "version": "v2"},
        })
    changes = {
        "package_version": "v78",
        "release_version": "v76",
        "members": members,
        "registry_sort": "id_version",
        "registry_new_key_order": ["checksum", "id", "version"],
    }
    (scratch / "changes.json").write_text(json.dumps(changes, indent=2) + "\n", encoding="utf-8")
    report = generate_to_directory(
        content / "package.core-calculations.v77.json",
        content / "published-packages.v75.json",
        releases / "demo.release.sli-worksheet-integration.2025.v75.json",
        content,
        scratch / "changes.json",
        scratch / "out",
    )
    for folder, source_name, target_name in (
        ("content", "package.json", "package.core-calculations.v78.json"),
        ("content", "registry.json", "published-packages.v76.json"),
        ("releases", "release.json", "demo.release.sli-worksheet-integration.2025.v76.json"),
    ):
        shutil.copy(scratch / "out" / source_name, scratch / folder / target_name)
    _declare_v78()
    return report, written


def main() -> int:
    inventory = _load(HERE / "probe-output.json")
    drafts = _drafts(inventory)
    acts = ccr.base_return()
    before = probe.run_case(acts, "demo.le.p0.prototype-v77")
    with tempfile.TemporaryDirectory() as tmp:
        report, written = build(Path(tmp).resolve() / "s", drafts)
        after = probe.run_case(
            acts,
            "demo.le.p0.prototype-v78",
            content=Path(tmp).resolve() / "s" / "content",
            release_dir=Path(tmp).resolve() / "s" / "releases",
            package_name="package.core-calculations.v78.json",
            package_version="v78",
            registry_name="published-packages.v76.json",
            release_name="demo.release.sli-worksheet-integration.2025.v76.json",
            release_version="v76",
        )
    old, new = _rows(before), _rows(after)
    mismatches = []
    for field_id in sorted(set(old) | set(new)):
        left, right = old.get(field_id), new.get(field_id)
        if left is None or right is None or left["disposition"] != right["disposition"] or left["value"] != right["value"]:
            mismatches.append({
                "field_id": field_id,
                "v77": None if left is None else {"disposition": left["disposition"], "value": left["value"]},
                "v78": None if right is None else {"disposition": right["disposition"], "value": right["value"]},
            })
    explain_changes = []
    for field_id in (*TARGETS, CONTROL):
        left, right = old.get(field_id, {}), new.get(field_id, {})
        explain_changes.append({
            "field_id": field_id,
            "succeeded": field_id in TARGETS,
            "v77_explain": left.get("explain"),
            "v78_explain": right.get("explain"),
            "changed": left.get("explain") != right.get("explain"),
            "v77_disposition": left.get("disposition"),
            "v78_disposition": right.get("disposition"),
            "v77_value": left.get("value"),
            "v78_value": right.get("value"),
        })
    page = _page_hits(after, set(TARGETS) | {CONTROL})
    payload = {
        "case": "demo.le.p0.wages",
        "v77_reachable": bool(before.get("reachable")),
        "v78_reachable": bool(after.get("reachable")),
        "v77_refusal": before.get("refusal"),
        "v78_refusal": after.get("refusal"),
        "successor": {
            "package_version": report["package"]["version"],
            "release_version": report["release"]["version"],
            "inherited_inconsistencies": report["inherited_inconsistencies"],
            "fields": written,
        },
        "fields_compared": len(set(old) | set(new)),
        "value_and_disposition_mismatches": mismatches,
        "explain_changes": explain_changes,
        "v78_page": page,
        "values_and_dispositions_match": not mismatches and bool(before.get("reachable")) and bool(after.get("reachable")),
        "succeeded_explains_changed": all(
            row["changed"] for row in explain_changes if row["succeeded"]
        ),
        "control_explain_unchanged": next(
            row["changed"] is False for row in explain_changes if row["field_id"] == CONTROL
        ),
    }
    text = json.dumps(payload, indent=2) + "\n"
    if PATH_LEAK.search(text):
        raise SystemExit("prototype output contains a local path")
    (HERE / "prototype-output.json").write_text(text, encoding="utf-8")
    print(
        "v77", payload["v77_reachable"],
        "v78", payload["v78_reachable"],
        "match", payload["values_and_dispositions_match"],
        "explains", payload["succeeded_explains_changed"],
        "control", payload["control_explain_unchanged"],
        "mismatches", len(mismatches),
        flush=True,
    )
    if not before.get("reachable"):
        print("v77 refusal", before.get("refusal"), flush=True)
    if not after.get("reachable"):
        print("v78 refusal", after.get("refusal"), flush=True)
    return 0 if payload["values_and_dispositions_match"] and payload["succeeded_explains_changed"] and payload["control_explain_unchanged"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
