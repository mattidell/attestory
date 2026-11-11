"""Survey stand-in symbol rules and unwritten selection paths on every core.

Evidence for docs/phases/engine-breadth/milestones/selection-keyed-collect.md.
Charter: docs/reviews/selection-keyed-collect/charter-p0.md.

A stand-in is an adopted rule that publishes a constant under a fact id a
selection path requires so that path can name a collect. An unwritten path
is a selection path whose activity fact types have no publisher and no
input question on that core.

Run from the repository root:

    python3 docs/phases/engine-breadth/milestones/selection-keyed-collect-evidence/survey.py

Writes survey-output.json beside this file. No absolute path is written.
"""

from __future__ import annotations

import json
import re
from collections import defaultdict
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
CONTENT = REPO / "packages" / "content" / "tax" / "2025"
OUT_PATH = HERE / "survey-output.json"
CORE_RE = re.compile(r"^package\.core-calculations\.(v[1-9][0-9]*)\.json$")
RULE_SCHEMAS = tuple(f"rule-artifact.v{n}" for n in range(1, 16))


def walk(node: Any):
    if isinstance(node, dict):
        yield node
        for value in node.values():
            yield from walk(value)
    elif isinstance(node, list):
        for item in node:
            yield from walk(item)


def collect_names(expr: Any) -> list[str]:
    names: list[str] = []
    for node in walk(expr):
        if node.get("op") in {"collect", "count", "collect_categorical_all_equal"}:
            name = node.get("name")
            if isinstance(name, str) and name not in names:
                names.append(name)
    return names


def activity_fact_ids(activity: Any) -> list[str]:
    if not isinstance(activity, dict):
        return []
    ids: list[str] = []
    listed = activity.get("member_fact_types")
    if isinstance(listed, list):
        for pin in listed:
            if isinstance(pin, dict) and isinstance(pin.get("id"), str):
                ids.append(pin["id"])
    single = activity.get("member_fact_type")
    if isinstance(single, dict) and isinstance(single.get("id"), str):
        ids.append(single["id"])
    fact = activity.get("fact_type")
    if isinstance(fact, dict) and isinstance(fact.get("id"), str):
        ids.append(fact["id"])
    family = activity.get("source_family")
    if isinstance(family, dict) and isinstance(family.get("id"), str):
        ids.append("family:" + family["id"])
    out: list[str] = []
    for item in ids:
        if item not in out:
            out.append(item)
    return out


def is_constant(value: Any) -> bool:
    return isinstance(value, (int, float, bool, str)) or value is None


def load_index() -> dict[tuple[str, str], dict[str, Any]]:
    index: dict[tuple[str, str], dict[str, Any]] = {}
    for path in sorted(CONTENT.glob("*.json")):
        try:
            body = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if not isinstance(body, dict):
            continue
        identity, version = body.get("id"), body.get("version")
        if isinstance(identity, str) and isinstance(version, str):
            index[(identity, version)] = body
        if body.get("schema") in ("bundle.v1", "bundle.v2"):
            for fact in body.get("fact_types") or []:
                if not isinstance(fact, dict):
                    continue
                fact_id, fact_version = fact.get("id"), fact.get("version")
                if isinstance(fact_id, str) and isinstance(fact_version, str):
                    index.setdefault((fact_id, fact_version), fact)
    return index


def core_paths() -> list[Path]:
    found: list[tuple[int, Path]] = []
    for path in CONTENT.glob("package.core-calculations.v*.json"):
        match = CORE_RE.match(path.name)
        if match:
            found.append((int(match.group(1)[1:]), path))
    return [path for _rank, path in sorted(found)]


def member_bodies(package: dict[str, Any], index: dict[tuple[str, str], dict[str, Any]]) -> list[dict[str, Any]]:
    bodies: list[dict[str, Any]] = []
    for pin in package.get("members") or []:
        if not isinstance(pin, dict):
            continue
        identity, version = pin.get("id"), pin.get("version")
        if not isinstance(identity, str) or not isinstance(version, str):
            continue
        body = index.get((identity, version))
        if body is not None:
            bodies.append(body)
    return bodies


def survey_core(version: str, bodies: list[dict[str, Any]]) -> dict[str, Any]:
    publishers: dict[str, list[dict[str, Any]]] = defaultdict(list)
    questions: set[str] = set()
    family_members: dict[str, str] = {}
    collected: set[str] = set()
    for body in bodies:
        schema = str(body.get("schema") or "")
        if schema.startswith("rule-artifact.") and isinstance(body.get("publishes"), str):
            publishers[body["publishes"]].append(body)
        if schema == "input-question.v1":
            pin = body.get("fact_type")
            if isinstance(pin, dict) and isinstance(pin.get("id"), str):
                questions.add(pin["id"])
            elif isinstance(body.get("fact_type"), str):
                questions.add(body["fact_type"])
        if schema in ("source-family.v1", "source-family.v2"):
            predicate = body.get("member_predicate") or {}
            member = predicate.get("fact_type") if isinstance(predicate, dict) else None
            if isinstance(body.get("id"), str) and isinstance(member, str):
                family_members[body["id"]] = member
        for node in walk(body):
            if node.get("op") in {"collect", "count", "collect_categorical_all_equal"}:
                name = node.get("name")
                if isinstance(name, str):
                    collected.add(name)
    family_member_ids = set(family_members.values())

    stand_ins: list[dict[str, Any]] = []
    unwritten_paths: list[dict[str, Any]] = []
    one_real_plus_default: list[dict[str, Any]] = []
    two_real: list[dict[str, Any]] = []

    for body in bodies:
        if body.get("schema") not in RULE_SCHEMAS:
            continue
        selection = body.get("selection")
        if not isinstance(selection, dict):
            continue
        paths = [path for path in selection.get("paths") or [] if isinstance(path, dict)]
        default = selection.get("default") if isinstance(selection.get("default"), dict) else None
        written_paths = 0
        unwritten_on_rule: list[dict[str, Any]] = []
        for path in paths:
            activity_ids = [item for item in activity_fact_ids(path.get("activity")) if not item.startswith("family:")]
            writers = []
            for fact_id in activity_ids:
                if (
                    publishers.get(fact_id)
                    or fact_id in questions
                    or fact_id in family_member_ids
                    or fact_id in collected
                ):
                    writers.append(fact_id)
            requires = [name for name in path.get("requires") or [] if isinstance(name, str)]
            path_collects = collect_names(path.get("value")) + collect_names(path.get("when"))
            named = [name for name in requires if name in path_collects]
            inert_named = (
                str(path.get("id")) == "inert"
                or any("inert" in fact_id or "unwritten" in fact_id for fact_id in activity_ids)
            )
            if not writers:
                unwritten_on_rule.append({
                    "path_id": path.get("id"),
                    "fact_types": activity_ids,
                    "requires": requires,
                    "inert_named": inert_named,
                })
            else:
                written_paths += 1
            for name in named:
                member_of = [family for family, member in family_members.items() if member == name]
                for publisher in publishers.get(name, []):
                    if publisher.get("id") == body.get("id"):
                        continue
                    if not is_constant(publisher.get("value")):
                        continue
                    stand_ins.append({
                        "core": version,
                        "publisher": publisher.get("id"),
                        "publisher_version": publisher.get("version"),
                        "publishes": name,
                        "value": publisher.get("value"),
                        "selection_rule": body.get("id"),
                        "selection_version": body.get("version"),
                        "path_id": path.get("id"),
                        "family_members": member_of,
                    })
        if unwritten_on_rule:
            unwritten_paths.append({
                "core": version,
                "rule": body.get("id"),
                "rule_version": body.get("version"),
                "schema": body.get("schema"),
                "paths": unwritten_on_rule,
                "has_default": default is not None,
                "written_path_count": written_paths,
            })
        if default is not None and written_paths == 1:
            one_real_plus_default.append({
                "core": version,
                "rule": body.get("id"),
                "rule_version": body.get("version"),
                "unwritten_path_count": len(unwritten_on_rule),
            })
        if written_paths >= 2:
            two_real.append({
                "core": version,
                "rule": body.get("id"),
                "rule_version": body.get("version"),
                "written_path_count": written_paths,
            })

    return {
        "version": version,
        "member_count": len(bodies),
        "stand_ins": stand_ins,
        "unwritten_paths": unwritten_paths,
        "one_real_plus_default": one_real_plus_default,
        "two_real": two_real,
    }


def first_seen(rows: list[dict[str, Any]], key_fn) -> list[dict[str, Any]]:
    seen: dict[Any, dict[str, Any]] = {}
    cores: dict[Any, list[str]] = defaultdict(list)
    for row in rows:
        key = key_fn(row)
        cores[key].append(str(row.get("core")))
        if key not in seen:
            seen[key] = dict(row)
    out = []
    for key, row in seen.items():
        row["cores"] = cores[key]
        row["first_core"] = cores[key][0]
        row["last_core"] = cores[key][-1]
        out.append(row)
    return out


def main() -> None:
    index = load_index()
    cores = []
    all_stand_ins: list[dict[str, Any]] = []
    all_unwritten: list[dict[str, Any]] = []
    all_one_real: list[dict[str, Any]] = []
    all_two_real: list[dict[str, Any]] = []
    unresolved: list[dict[str, Any]] = []
    for path in core_paths():
        package = json.loads(path.read_text(encoding="utf-8"))
        version = str(package.get("version") or path.name)
        members = package.get("members") or []
        missing = [
            {"id": pin.get("id"), "version": pin.get("version")}
            for pin in members
            if isinstance(pin, dict) and (pin.get("id"), pin.get("version")) not in index
        ]
        if missing:
            unresolved.append({"core": version, "missing_count": len(missing)})
        result = survey_core(version, member_bodies(package, index))
        cores.append({
            "version": version,
            "member_count": result["member_count"],
            "stand_in_count": len(result["stand_ins"]),
            "unwritten_path_rule_count": len(result["unwritten_paths"]),
            "one_real_plus_default_count": len(result["one_real_plus_default"]),
            "two_real_count": len(result["two_real"]),
        })
        all_stand_ins.extend(result["stand_ins"])
        all_unwritten.extend(result["unwritten_paths"])
        all_one_real.extend(result["one_real_plus_default"])
        all_two_real.extend(result["two_real"])

    stand_in_kinds = first_seen(
        all_stand_ins,
        lambda row: (row["publisher"], row["publisher_version"], row["selection_rule"], row["path_id"]),
    )
    unwritten_kinds = first_seen(
        all_unwritten,
        lambda row: (row["rule"], row["rule_version"], tuple(
            (path["path_id"], tuple(path["fact_types"])) for path in row["paths"]
        )),
    )
    one_real_kinds = first_seen(all_one_real, lambda row: (row["rule"], row["rule_version"]))
    two_real_kinds = first_seen(all_two_real, lambda row: (row["rule"], row["rule_version"]))

    output = {
        "cores_surveyed": [row["version"] for row in cores],
        "core_count": len(cores),
        "unresolved_member_cores": unresolved,
        "stand_in_kind_count": len(stand_in_kinds),
        "unwritten_path_kind_count": len(unwritten_kinds),
        "one_real_plus_default_kind_count": len(one_real_kinds),
        "two_real_kind_count": len(two_real_kinds),
        "stand_in_kinds": stand_in_kinds,
        "unwritten_path_kinds": unwritten_kinds,
        "one_real_plus_default_kinds": one_real_kinds,
        "two_real_kinds": two_real_kinds,
        "per_core": cores,
    }
    text = json.dumps(output, indent=2) + "\n"
    for needle in ("/Users/", "/private/", "/tmp/", "/var/"):
        if needle in text:
            raise SystemExit(f"survey output contains {needle}")
    OUT_PATH.write_text(text, encoding="utf-8")
    print(json.dumps({
        "cores": len(cores),
        "stand_in_kinds": len(stand_in_kinds),
        "unwritten_path_kinds": len(unwritten_kinds),
        "one_real_plus_default_kinds": len(one_real_kinds),
        "two_real_kinds": len(two_real_kinds),
        "output": OUT_PATH.name,
    }, indent=2))


if __name__ == "__main__":
    main()
