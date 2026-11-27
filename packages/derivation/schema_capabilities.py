"""Single source of truth for derivation schema version capabilities.

Every published ``rule-artifact.v*``, ``attachment-rule.v*``, and
``artifact-package.v*`` schema version has exactly one typed capability row
here. Consumers in ``packages/derivation/`` read named capability columns or
derived ``frozenset[str]`` views rather than scattering literal version lists.

Pure stdlib module (zero package imports) so every derivation module can import
it without circular dependencies.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

FieldRefValidationMode = Literal["none", "top_level", "expression_nodes"]


@dataclass(frozen=True)
class RuleArtifactCapabilities:
    """Capability row for one published ``rule-artifact.v*`` schema."""

    schema: str
    uses_v2_record: bool
    declared_refs_outside_requires: bool
    field_ref_validation: FieldRefValidationMode
    declared_line2b_v9_selection: bool
    supports_link_coverage: bool
    supports_subject_declaration: bool
    subject_optional: bool
    supports_link_count: bool
    supports_reader_role: bool
    supports_shared_key_count: bool
    supports_v13_selection: bool
    supports_require_paired: bool
    # Preserved boundary: v6-v17 schemas omit `accounts_for`, and committed
    # cores v77-v106 include v15/v17 rules reaching constrained families without
    # `accounts_for`, so validation-graph compilation/checking stays v1-v11.
    validation_graph_participant: bool


@dataclass(frozen=True)
class AttachmentRuleCapabilities:
    """Capability row for one published ``attachment-rule.v*`` schema."""

    schema: str
    executable_and_validated: bool
    projection_supported: bool
    legacy_single_row_set: bool
    uses_row_sets: bool
    supports_adjustment_rows: bool
    # Must exclude v11: its exclusive_presence selection paths omit top-level
    # adjustment subtotal_symbol and must not wait for unselected paths.
    eager_adjustment_requires: bool
    projection_reads_row_sets: bool
    # Preserved historical boundary: v1-v5 predate attachment BFS edges in
    # package reachability and rule_scoped_closure digests.
    bfs_reachability_edges: bool
    supports_exclusive_adjustment_selection: bool
    supports_conditional_and_limited_parts: bool


@dataclass(frozen=True)
class ArtifactPackageCapabilities:
    """Capability row for one published ``artifact-package.v*`` schema."""

    schema: str
    exact_entrypoint_pins: bool
    # Preserved historical boundary: stops at v17 (core v29-v106 use collect
    # forms outside the v17 guard, and tests pin the v17 upper bound).
    universe_guard_active: bool
    enforces_reader_role: bool


def _build_rule_artifact_row(version: int) -> RuleArtifactCapabilities:
    field_ref_mode: FieldRefValidationMode
    if version < 7:
        field_ref_mode = "none"
    elif version in (7, 8):
        field_ref_mode = "top_level"
    else:
        field_ref_mode = "expression_nodes"
    return RuleArtifactCapabilities(
        schema=f"rule-artifact.v{version}",
        uses_v2_record=(version >= 2),
        declared_refs_outside_requires=(version >= 3),
        field_ref_validation=field_ref_mode,
        declared_line2b_v9_selection=(version == 9),
        supports_link_coverage=(version >= 10),
        supports_subject_declaration=(version >= 11),
        subject_optional=(version >= 13),
        supports_link_count=(version >= 12),
        supports_reader_role=(version >= 12),
        supports_shared_key_count=(version >= 13),
        supports_v13_selection=(version >= 13),
        supports_require_paired=(version >= 15),
        validation_graph_participant=(version <= 11),
    )


RULE_ARTIFACT_CAPABILITIES: dict[str, RuleArtifactCapabilities] = {
    f"rule-artifact.v{v}": _build_rule_artifact_row(v)
    for v in range(1, 18)
}

# Published attachment-rule versions: v7 and v9 were never published.
# Note: v5 has a published `const: "attachment-rule.v3"` schema typo and is
# retained as executable/row-set compatible without adjustment-row support;
# v10 is projection-only (never admitted by any artifact-package schema).
ATTACHMENT_RULE_CAPABILITIES: dict[str, AttachmentRuleCapabilities] = {
    row.schema: row
    for row in (
        AttachmentRuleCapabilities(
            schema="attachment-rule.v1",
            executable_and_validated=True,
            projection_supported=True,
            legacy_single_row_set=True,
            uses_row_sets=False,
            supports_adjustment_rows=False,
            eager_adjustment_requires=False,
            projection_reads_row_sets=False,
            bfs_reachability_edges=False,
            supports_exclusive_adjustment_selection=False,
            supports_conditional_and_limited_parts=False,
        ),
        AttachmentRuleCapabilities(
            schema="attachment-rule.v2",
            executable_and_validated=True,
            projection_supported=True,
            legacy_single_row_set=False,
            uses_row_sets=True,
            supports_adjustment_rows=False,
            eager_adjustment_requires=False,
            projection_reads_row_sets=False,
            bfs_reachability_edges=False,
            supports_exclusive_adjustment_selection=False,
            supports_conditional_and_limited_parts=False,
        ),
        AttachmentRuleCapabilities(
            schema="attachment-rule.v3",
            executable_and_validated=True,
            projection_supported=True,
            legacy_single_row_set=False,
            uses_row_sets=True,
            supports_adjustment_rows=False,
            eager_adjustment_requires=False,
            projection_reads_row_sets=False,
            bfs_reachability_edges=False,
            supports_exclusive_adjustment_selection=False,
            supports_conditional_and_limited_parts=False,
        ),
        AttachmentRuleCapabilities(
            schema="attachment-rule.v4",
            executable_and_validated=True,
            projection_supported=True,
            legacy_single_row_set=False,
            uses_row_sets=True,
            supports_adjustment_rows=False,
            eager_adjustment_requires=False,
            projection_reads_row_sets=False,
            bfs_reachability_edges=False,
            supports_exclusive_adjustment_selection=False,
            supports_conditional_and_limited_parts=False,
        ),
        AttachmentRuleCapabilities(
            schema="attachment-rule.v5",
            executable_and_validated=True,
            projection_supported=True,
            legacy_single_row_set=False,
            uses_row_sets=True,
            supports_adjustment_rows=False,
            eager_adjustment_requires=False,
            projection_reads_row_sets=False,
            bfs_reachability_edges=False,
            supports_exclusive_adjustment_selection=False,
            supports_conditional_and_limited_parts=False,
        ),
        AttachmentRuleCapabilities(
            schema="attachment-rule.v6",
            executable_and_validated=True,
            projection_supported=True,
            legacy_single_row_set=False,
            uses_row_sets=True,
            supports_adjustment_rows=True,
            eager_adjustment_requires=True,
            projection_reads_row_sets=True,
            bfs_reachability_edges=True,
            supports_exclusive_adjustment_selection=False,
            supports_conditional_and_limited_parts=False,
        ),
        AttachmentRuleCapabilities(
            schema="attachment-rule.v8",
            executable_and_validated=True,
            projection_supported=True,
            legacy_single_row_set=False,
            uses_row_sets=True,
            supports_adjustment_rows=True,
            eager_adjustment_requires=True,
            projection_reads_row_sets=True,
            bfs_reachability_edges=True,
            supports_exclusive_adjustment_selection=False,
            supports_conditional_and_limited_parts=False,
        ),
        AttachmentRuleCapabilities(
            schema="attachment-rule.v10",
            executable_and_validated=False,
            projection_supported=True,
            legacy_single_row_set=False,
            uses_row_sets=True,
            supports_adjustment_rows=True,
            eager_adjustment_requires=False,
            projection_reads_row_sets=True,
            bfs_reachability_edges=False,
            supports_exclusive_adjustment_selection=False,
            supports_conditional_and_limited_parts=False,
        ),
        AttachmentRuleCapabilities(
            schema="attachment-rule.v11",
            executable_and_validated=True,
            projection_supported=True,
            legacy_single_row_set=False,
            uses_row_sets=True,
            supports_adjustment_rows=True,
            eager_adjustment_requires=False,
            projection_reads_row_sets=True,
            bfs_reachability_edges=True,
            supports_exclusive_adjustment_selection=True,
            supports_conditional_and_limited_parts=False,
        ),
        AttachmentRuleCapabilities(
            schema="attachment-rule.v12",
            executable_and_validated=True,
            projection_supported=True,
            legacy_single_row_set=False,
            uses_row_sets=True,
            supports_adjustment_rows=False,
            eager_adjustment_requires=False,
            projection_reads_row_sets=True,
            bfs_reachability_edges=True,
            supports_exclusive_adjustment_selection=False,
            supports_conditional_and_limited_parts=True,
        ),
    )
}

# Published artifact-package versions: v27 was skipped during renumbering.
ARTIFACT_PACKAGE_CAPABILITIES: dict[str, ArtifactPackageCapabilities] = {
    f"artifact-package.v{v}": ArtifactPackageCapabilities(
        schema=f"artifact-package.v{v}",
        exact_entrypoint_pins=(v >= 20),
        universe_guard_active=(3 <= v <= 17),
        enforces_reader_role=(v >= 34),
    )
    for v in range(1, 46)
    if v != 27
}


def rule_artifact_caps(schema: object) -> RuleArtifactCapabilities | None:
    """Return the capability row for a published rule-artifact schema, else ``None``."""
    return RULE_ARTIFACT_CAPABILITIES.get(schema) if isinstance(schema, str) else None


def attachment_rule_caps(schema: object) -> AttachmentRuleCapabilities | None:
    """Return the capability row for a published attachment-rule schema, else ``None``."""
    return ATTACHMENT_RULE_CAPABILITIES.get(schema) if isinstance(schema, str) else None


def artifact_package_caps(schema: object) -> ArtifactPackageCapabilities | None:
    """Return the capability row for a published artifact-package schema, else ``None``."""
    return ARTIFACT_PACKAGE_CAPABILITIES.get(schema) if isinstance(schema, str) else None


# Derived capability sets — never hand-maintained independently.
RULE_ARTIFACT_SCHEMAS: frozenset[str] = frozenset(RULE_ARTIFACT_CAPABILITIES)
RULE_V2_RECORD_SCHEMAS: frozenset[str] = frozenset(
    s for s, c in RULE_ARTIFACT_CAPABILITIES.items() if c.uses_v2_record
)
RULE_DECLARED_REFS_OUTSIDE_REQUIRES: frozenset[str] = frozenset(
    s for s, c in RULE_ARTIFACT_CAPABILITIES.items() if c.declared_refs_outside_requires
)
RULE_FIELD_REF_SCHEMAS: frozenset[str] = frozenset(
    s for s, c in RULE_ARTIFACT_CAPABILITIES.items() if c.field_ref_validation != "none"
)
RULE_FIELD_REF_TOP_LEVEL_SCHEMAS: frozenset[str] = frozenset(
    s for s, c in RULE_ARTIFACT_CAPABILITIES.items() if c.field_ref_validation == "top_level"
)
RULE_LINE2B_V9_SCHEMAS: frozenset[str] = frozenset(
    s for s, c in RULE_ARTIFACT_CAPABILITIES.items() if c.declared_line2b_v9_selection
)
RULE_LINK_COVERAGE_SCHEMAS: frozenset[str] = frozenset(
    s for s, c in RULE_ARTIFACT_CAPABILITIES.items() if c.supports_link_coverage
)
RULE_SUBJECT_SCHEMAS: frozenset[str] = frozenset(
    s for s, c in RULE_ARTIFACT_CAPABILITIES.items() if c.supports_subject_declaration
)
RULE_SUBJECT_OPTIONAL_SCHEMAS: frozenset[str] = frozenset(
    s for s, c in RULE_ARTIFACT_CAPABILITIES.items() if c.subject_optional
)
RULE_LINK_COUNT_SCHEMAS: frozenset[str] = frozenset(
    s for s, c in RULE_ARTIFACT_CAPABILITIES.items() if c.supports_link_count
)
RULE_READER_ROLE_SCHEMAS: frozenset[str] = frozenset(
    s for s, c in RULE_ARTIFACT_CAPABILITIES.items() if c.supports_reader_role
)
RULE_SHARED_KEY_COUNT_SCHEMAS: frozenset[str] = frozenset(
    s for s, c in RULE_ARTIFACT_CAPABILITIES.items() if c.supports_shared_key_count
)
RULE_V13_SELECTION_SCHEMAS: frozenset[str] = frozenset(
    s for s, c in RULE_ARTIFACT_CAPABILITIES.items() if c.supports_v13_selection
)
RULE_REQUIRE_PAIRED_SCHEMAS: frozenset[str] = frozenset(
    s for s, c in RULE_ARTIFACT_CAPABILITIES.items() if c.supports_require_paired
)
RULE_VALIDATION_GRAPH_SCHEMAS: frozenset[str] = frozenset(
    s for s, c in RULE_ARTIFACT_CAPABILITIES.items() if c.validation_graph_participant
)

ATTACHMENT_EXECUTABLE_SCHEMAS: frozenset[str] = frozenset(
    s for s, c in ATTACHMENT_RULE_CAPABILITIES.items() if c.executable_and_validated
)
ATTACHMENT_PROJECTION_SCHEMAS: frozenset[str] = frozenset(
    s for s, c in ATTACHMENT_RULE_CAPABILITIES.items() if c.projection_supported
)
ATTACHMENT_LEGACY_SINGLE_ROW_SET_SCHEMAS: frozenset[str] = frozenset(
    s for s, c in ATTACHMENT_RULE_CAPABILITIES.items() if c.legacy_single_row_set
)
ATTACHMENT_ROW_SET_SCHEMAS: frozenset[str] = frozenset(
    s for s, c in ATTACHMENT_RULE_CAPABILITIES.items()
    if c.executable_and_validated and c.uses_row_sets
)
ATTACHMENT_ADJUSTMENT_ROWS_EXECUTABLE_SCHEMAS: frozenset[str] = frozenset(
    s for s, c in ATTACHMENT_RULE_CAPABILITIES.items()
    if c.executable_and_validated and c.supports_adjustment_rows
)
ATTACHMENT_ADJUSTMENT_ROWS_PROJECTION_SCHEMAS: frozenset[str] = frozenset(
    s for s, c in ATTACHMENT_RULE_CAPABILITIES.items()
    if c.projection_supported and c.supports_adjustment_rows
)
ATTACHMENT_EAGER_ADJUSTMENT_REQUIRES_SCHEMAS: frozenset[str] = frozenset(
    s for s, c in ATTACHMENT_RULE_CAPABILITIES.items() if c.eager_adjustment_requires
)
ATTACHMENT_PROJECTION_ROW_SETS_SCHEMAS: frozenset[str] = frozenset(
    s for s, c in ATTACHMENT_RULE_CAPABILITIES.items() if c.projection_reads_row_sets
)
ATTACHMENT_BFS_SCHEMAS: frozenset[str] = frozenset(
    s for s, c in ATTACHMENT_RULE_CAPABILITIES.items() if c.bfs_reachability_edges
)
ATTACHMENT_EXCLUSIVE_SELECTION_SCHEMAS: frozenset[str] = frozenset(
    s for s, c in ATTACHMENT_RULE_CAPABILITIES.items()
    if c.supports_exclusive_adjustment_selection
)
ATTACHMENT_CONDITIONAL_LIMITED_PART_SCHEMAS: frozenset[str] = frozenset(
    s for s, c in ATTACHMENT_RULE_CAPABILITIES.items()
    if c.supports_conditional_and_limited_parts
)

ALL_VALIDATION_GRAPH_SCHEMAS: frozenset[str] = (
    RULE_VALIDATION_GRAPH_SCHEMAS | ATTACHMENT_EXECUTABLE_SCHEMAS
)
ALL_EXECUTABLE_RULE_AND_ATTACHMENT_SCHEMAS: frozenset[str] = (
    RULE_ARTIFACT_SCHEMAS | ATTACHMENT_EXECUTABLE_SCHEMAS
)

PACKAGE_EXACT_ENTRYPOINT_SCHEMAS: frozenset[str] = frozenset(
    s for s, c in ARTIFACT_PACKAGE_CAPABILITIES.items() if c.exact_entrypoint_pins
)
PACKAGE_UNIVERSE_GUARD_SCHEMAS: frozenset[str] = frozenset(
    s for s, c in ARTIFACT_PACKAGE_CAPABILITIES.items() if c.universe_guard_active
)
PACKAGE_READER_ROLE_SCHEMAS: frozenset[str] = frozenset(
    s for s, c in ARTIFACT_PACKAGE_CAPABILITIES.items() if c.enforces_reader_role
)
