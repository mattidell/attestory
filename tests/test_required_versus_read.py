"""Static required-versus-read check: fast lane, runs on the latest core package.

The seeded-defect test for the path mode runs a live coordinator and lives in
``tests/test_required_versus_read_path.py``, so that this module stays in the
fast lane.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from tools.required_versus_read import (  # noqa: E402
    load_allowlist,
    rule_static_misses,
    static_check,
)


def test_latest_core_package_has_no_unallowed_required_symbol() -> None:
    result = static_check()
    assert result["unallowed"] == [], (
        f"{result['package']} requires symbols no part of the rule reads, "
        f"and they are not in tools/required_versus_read_allowlist.json: {result['unallowed']}"
    )


def test_every_allowlist_entry_still_matches_a_current_miss() -> None:
    result = static_check()
    assert result["stale_allowlist"] == [], (
        "allowlist entries that no longer match a miss; remove them: "
        f"{result['stale_allowlist']}"
    )


def test_every_computation_member_of_the_latest_core_package_resolves() -> None:
    result = static_check()
    assert result["unresolved"] == [], (
        "computation members with no matching rule file; the static check "
        f"cannot see them: {result['unresolved']}"
    )


def test_seeded_rule_requiring_a_symbol_it_never_references_is_a_miss() -> None:
    rule = {
        "id": "demo.rule.never-read",
        "version": "v1",
        "requires": ["demo.answer.read", "demo.answer.never-read"],
        "value": {"op": "ref", "name": "demo.answer.read"},
    }
    assert rule_static_misses(rule) == [("demo.answer.never-read", "top")]


def test_seeded_selection_path_requirement_that_nothing_reads_is_a_miss() -> None:
    rule = {
        "id": "demo.rule.selection",
        "version": "v1",
        "value": {"op": "ref", "name": "demo.answer.read"},
        "selection": {
            "paths": [{"id": "demo-path", "requires": ["demo.answer.path-only"]}],
            "default": {"requires": []},
        },
    }
    assert rule_static_misses(rule) == [("demo.answer.path-only", "selection-path:demo-path")]


def test_every_symbol_reading_operation_counts_as_a_read() -> None:
    names = [
        "demo.ref",
        "demo.collect",
        "demo.count",
        "demo.bound",
        "demo.categorical",
        "demo.links",
        "demo.reductions",
        "demo.link-count",
        "demo.fact-type",
        "demo.dependency-member",
        "demo.subject-result",
        "demo.activity-member",
    ]
    rule = {
        "id": "demo.rule.every-op",
        "version": "v1",
        "requires": list(names),
        "value": {
            "op": "choose",
            "when": {"op": "all", "args": [
                {"op": "ref", "name": "demo.ref"},
                {"op": "conditional_dependency_set",
                 "condition": {"op": "ref", "name": "demo.ref"},
                 "members": [{"op": "ref", "name": "demo.dependency-member"}]},
            ]},
            "then": {"op": "add", "args": [
                {"op": "collect", "name": "demo.collect"},
                {"op": "count", "name": "demo.count", "source_set": "demo.set"},
                {"op": "bound_sources", "name": "demo.bound"},
                {"op": "link_coverage", "links": "demo.links", "reductions": "demo.reductions"},
                {"op": "link_count", "links": "demo.link-count"},
                {"op": "shared_key_count", "fact_type": "demo.fact-type", "key": "k"},
            ]},
            "else": {"op": "collect_categorical_all_equal", "name": "demo.categorical",
                     "value": {"op": "category_literal", "fact_type": "demo.fact-type", "value": "yes"}},
        },
        "selection": {
            "paths": [{
                "id": "demo-path",
                "reads_subject_results": [{"symbol": "demo.subject-result"}],
                "requires": [],
            }],
            "default": {"requires": []},
        },
        "activity": {"member_fact_types": [{"id": "demo.activity-member"}]},
    }
    assert rule_static_misses(rule) == []


def test_allowlist_entry_without_a_reason_is_rejected(tmp_path: Path) -> None:
    path = tmp_path / "allowlist.json"
    path.write_text(
        '{"entries": [{"rule_id": "demo.rule", "version": "v1", "symbol": "demo.s", "reason": " "}]}',
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="reason"):
        load_allowlist(path)
