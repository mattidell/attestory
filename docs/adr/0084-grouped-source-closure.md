# ADR 0084 — One answer admits several source families

- Status: **accepted** (owner, 2026-11-06, before PR #261 went ready)
- Tier: 2
- Date: 2026-11-06

## Context

ADR-0014 admits one source family from one mapping. The mapping names that
family, and exactly one current closure finding whose value is boolean true,
keyed to that family's current horizon, authorizes an empty close. Eight
noncovered sale families need one yes/no question. Recording that fact once
per family never admits them, and giving them one shared horizon id is
illegal.

A covered sale whose broker did not report basis stays inside its covered
family under that rule, and the covered line still publishes. The filer needs
a block that says to record the sale as noncovered.

## Decision

1. `source-closure-mapping.v4` pins one closure fact, states one question,
   and lists the families it admits. Each listed row names the family, the
   member fact type, and the admitted symbol. `no` means closed-empty.
   `yes` means until a later member. `artifact-package.v41` admits the
   mapping. `source-closure-mapping.v3` and `artifact-package.v40` are
   unchanged.

2. The runner records each current finding of that fact once. It does not
   read a horizon key off the finding, and it does not mint a shared horizon
   id. `no` admits each listed family that has its own current horizon and
   zero current members. `yes` admits each listed family that has its own
   current horizon. A member-transition that adds or reclassifies a member
   of a listed family after that answer strips that family until a later
   answer. A removal does not. The pin for an admitted family is that
   family's current horizon plus the one finding. Any other value, a missing
   answer, or two current answers admits nothing. A repeated horizon id
   stays illegal.

3. A package may name a covered-flag refusal beside its companion
   declaration. The kernel declaration still carries only presence pairs and
   value domains; the map is a sibling keyed by the same package id and
   version. On a package that names it, a current member of a listed covered
   sale object whose `basis_reported_to_irs` is `no` drops that family's
   admission. The blocked row is `DEPENDENCY_INVALID` and its `missing`
   entry is `BASIS_NOT_REPORTED_ON_COVERED`. The page shows: "Record this
   sale as a noncovered sale. The broker did not report its basis to the
   IRS." On that same package, a constraint block shows the meaning the
   family declared, so the page is not blank. A package that does not name
   the map, including core v78 and earlier, does not apply this rule.

This supplements ADR-0014 for v4 mappings. ADR-0014's one-family boolean
true rule remains the rule for earlier mapping versions. This record does
not edit ADR-0014 or any other accepted ADR.

## Consequences

- The first package that carries a v4 mapping and names the refusal map is
  core v79, built after this record. Its map names the four covered sale
  objects core v79 publishes: `covered-st-txn`, `covered-lt-txn`,
  `covered-w-st-txn` and `covered-w-lt-txn`. `covered-ltcg-txn` is not a
  member of core v79, so the map does not name it.

## Links

- Supplements: ADR-0014
- Schemas: `source-closure-mapping.v4`, `artifact-package.v41`
- Plan: `docs/phases/engine-breadth/milestones/noncovered-sales.md`, Decisions 7–9
