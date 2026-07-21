"""Generate the DSBS Track 3 core-package v6 successor set.

Deterministic, additive over the immutable v5 core-calculations package
(tools/generate_dsbs_t2_schedule_b_content.py): v6 folds in Track 3's line-16
production build (ADR-0038) - the QDCG Worksheet rule-artifact.v3 successor
to line 16 (v1 -> v2, package pin moved from rule-artifact.v2 to
rule-artifact.v3, ADR-0037's conditional_dependency_set node), the two
declared-absence taxpayer-assertion fact types (capital-gain-distributions,
schedule-d-required) bundled per the committed pattern, and the QDCG
preferential-bracket parameter table the ladder folds over. v5 remains
historical; no existing citizen bytes are rewritten in place, only new
citizens/versions are added and a new package version references them.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "packages" / "content" / "tax" / "2025"


def _bytes(value: Any) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode("utf-8")


def _load(name: str) -> dict[str, Any]:
    value = json.loads((CONTENT / name).read_text("utf-8"))
    assert isinstance(value, dict)
    return value


def _checksum(value: dict[str, Any]) -> str:
    body = {key: item for key, item in value.items() if key != "package_checksum"}
    return hashlib.sha256(json.dumps(body, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def _citizen_checksum(value: dict[str, Any]) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


# New citizens introduced directly as committed files (not generated).
_NEW_CITIZEN_FILES = (
    "qdcg.bundle.json",
    "parameter.qdcg-preferential-brackets.json",
    "rule.form1040-line16.v2.json",
)

_NEW_MEMBERS = (
    {"role": "fact-type-bundle", "schema": "bundle.v2", "id": "tax.us.2025.qdcg.vocabulary", "version": "v1"},
    {"role": "parameter", "schema": "parameter-declaration.v1", "id": "demo.parameter.qdcg-preferential-brackets.2025", "version": "v1"},
)


def render() -> dict[str, bytes]:
    rendered: dict[str, bytes] = {}

    package_v6 = _load("package.core-calculations.v5.json")
    package_v6["schema"] = "artifact-package.v4"
    package_v6["version"] = "v6"
    package_v6["members"] = [dict(member) for member in package_v6["members"]]
    for member in package_v6["members"]:
        if member["id"] == "tax.us.2025.rule.form1040-line16":
            member["schema"] = "rule-artifact.v3"
            member["version"] = "v2"
    package_v6["admitted_schemas"] = sorted(
        set(package_v6["admitted_schemas"]) | {"rule-artifact.v3"}
    )
    package_v6["members"].extend(dict(m) for m in _NEW_MEMBERS)
    # The package-graph reachability walker (package_validation.py §8) has no
    # adjacency case connecting an unbound rule-artifact.v3 `when`-embedded
    # ref to its bundle without a declared input_binding (the same situation
    # scheduleb.vocabulary was in for attachment-rule.v1 completeness answers
    # at v5) - the new declared-absence vocabulary is therefore its own
    # declared root, the same sanctioned mechanism v4/v5 already used. The
    # line-16 v2 successor's reachability is unaffected: its own id/version
    # is already an entrypoint (updated below), and the preferential-bracket
    # parameter is reached ordinarily via the rule's own bracket_fold
    # table_id reference (the same path the ordinary tax-brackets table
    # already uses).
    package_v6["entrypoints"] = [
        dict(entry) if entry["id"] != "tax.us.2025.rule.form1040-line16" else {"id": entry["id"], "version": "v2"}
        for entry in package_v6["entrypoints"]
    ] + [
        {"id": "tax.us.2025.qdcg.vocabulary", "version": "v1"},
    ]
    package_v6["package_checksum"] = _checksum(package_v6)
    rendered["package.core-calculations.v6.json"] = _bytes(package_v6)

    registry = _load("published-packages.json")
    package_entries = [
        dict(entry)
        for entry in registry["packages"]
        if (entry["id"], entry["version"]) != (package_v6["id"], package_v6["version"])
    ]
    package_entries.append(
        {"id": package_v6["id"], "version": package_v6["version"], "checksum": package_v6["package_checksum"]}
    )
    citizen_entries = [dict(entry) for entry in registry["citizens"]]
    for name in _NEW_CITIZEN_FILES:
        citizen = _load(name)
        citizen_entries = [
            entry for entry in citizen_entries if (entry["id"], entry["version"]) != (citizen["id"], citizen["version"])
        ]
        citizen_entries.append(
            {"id": citizen["id"], "version": citizen["version"], "checksum": _citizen_checksum(citizen)}
        )
    registry["packages"] = sorted(package_entries, key=lambda entry: (entry["id"], entry["version"]))
    registry["citizens"] = sorted(citizen_entries, key=lambda entry: (entry["id"], entry["version"]))
    rendered["published-packages.json"] = _bytes(registry)
    return rendered


def main() -> None:
    for relative, content in render().items():
        (CONTENT / relative).write_bytes(content)


if __name__ == "__main__":
    main()
