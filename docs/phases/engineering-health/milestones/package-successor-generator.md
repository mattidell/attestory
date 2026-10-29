<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engineering Health",
  "topic": "package-successor-generator",
  "status": "Completed: the generator constructs and validates package, registry and release candidates from explicit changes; both historical chains reproduce byte for byte. Publication and companion duties remain separate. The next milestone is unselected.",
  "retrospective": "docs/milestone-retrospectives/2026-10-28-package-successor-generator.md",
  "scope": ["generate package, registry and release successors from explicit changes", "reproduce both historical chains in isolated destinations", "reject ambiguous or unsafe changes"],
  "non_goals": ["no new or edited package, registry, release or rule content", "no schema changes", "no companion-declaration redesign", "no rewrite of the existing one-off generator"],
  "deep_reads": {
    "planning": ["docs/process/planning-and-development.md", "docs/phases/engineering-health/engineering-health-roadmap.md"],
    "implementation": ["docs/process/planning-and-development.md", "docs/phases/engineering-health/milestones/package-successor-generator.md", "tools/package_successor.py"],
    "review": ["docs/process/planning-and-development.md", "docs/phases/engineering-health/milestones/package-successor-generator.md"],
    "new_milestone": ["docs/milestone-retrospectives/2026-10-28-package-successor-generator.md", "docs/phases/engineering-health/engineering-health-roadmap.md", "docs/phases/engineering-health/milestones/package-successor-generator.md"]
  }
}
-->

# Package Successor Generator

Milestone key: `package-successor-generator`. Phase: Engineering Health.

## Purpose and result

Content milestones need a consistent successor package, publication registry
and release without rewriting published history. The [generator guide](../../../tools/package-successor.md)
describes the command, importable API, explicit changes and candidate output.
The milestone traced both chains, built the generator, and independently
reviewed and repaired it. Rival prototypes were not applicable to this bounded
tooling milestone.
The tool preserves unchanged selections and fields, resolves additions and
replacements against the corpus, checks both complete registries with the
existing loaders, and validates predecessor and candidate packages and release
schemas. It distinguishes canonical citizen and package checksums from hashes
of formatted registry and release bytes.

## Replacement and historical evidence

A replacement requires one exact old member, the same identity at a later
numeric version, compatible role and scope, and the same schema family. The
new pin must agree with the resolved body and admitted schemas; the complete
candidate must pass validation. Different identities use explicit removal and
addition. This establishes structural eligibility, not preservation of tax
meaning, which remains a content review and testing responsibility.

The published direct-foreign-tax-credit rule has an inherited pin/body schema
mismatch. The generator reports it and preserves it only when the exact
predecessor pin and checksum-verified body remain unchanged; it refuses an
introduced mismatch. No citizen-specific exception or historical repair is
made.

Frozen deltas reproduce all six files byte for byte: package v57, registry
v55 and release v55 to v58/v56/v56; then v58/v56/v56 to v59/v57/v57. The
expected successors are comparison targets, not generation inputs. Ordering
controls account for observed member, binding and registry placement without
copying an expected output. Independent review found malformed unused
registry entries could previously survive validation; both registry arrays
now pass the existing loaders before installation, and the repair was
independently confirmed.

## Candidate installation and boundaries

The tool validates the whole chain before writing, checks inputs again, and
installs the complete candidate directory with an exclusive no-replace rename.
It refuses existing or protected paths, aliases and conflicting changes.
The supported local-filesystem assumptions, cleanup boundary and platform
limits are in the guide. Tests exercise failure and a competing destination;
they do not establish power-loss durability or protection from a hostile
output parent.

These three files are candidates, not publication or adoption. ADR-0082
requires the successor's own package-scoped companion declaration and live
release evidence as separate duties. Generating this chain does not supply
either, and the tool does not create declarations or adoption acts. No
published content, schema or old one-off generator changed in this milestone.
CI's required `verify` remains the publication gate.

## Verification

The single full local suite passed with 3,687 tests, 6,607 subtests and
20 skips in 640.53 seconds. Configured mypy passed 424 source files;
whitespace, governance lint and envelope scans passed. The independent
implementation review confirmed both historical reproductions, installation
collision/failure behavior and the registry-validation repair. Exact-head CI
and final curated-candidate review remain separate publication gates.

## Lessons

The [retrospective](../../../milestone-retrospectives/2026-10-28-package-successor-generator.md)
records the reusable lessons and review dispositions. The next milestone is
unselected.
