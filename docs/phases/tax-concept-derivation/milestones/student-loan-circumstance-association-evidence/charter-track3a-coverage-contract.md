# Charter — Track 3, stage A Builder: specify the coverage-checked collection contract

One builder unit. **Specification only — no production code, no schema file, no content.**
Authorised by the owner's choice on 2026-09-23 of coverage-checked behaviour for a Form 1098-E
statement's link reductions. Stage B (implementation) is chartered only after this contract is
reviewed.

## Context Capsule

- **Source ref:** `milestone/student-loan-circumstance-association` at `6a97a983` or later; verify
  with `git rev-parse HEAD` and `git branch --show-current`.
- **Milestone:** `student-loan-circumstance-association`; primary branch `main`.
- **Role:** Track 3 stage A Builder.
- **Assigned path:** one new document,
  `docs/phases/tax-concept-derivation/milestones/student-loan-circumstance-association-evidence/track3-coverage-contract.md`.
  Nothing else.
- **Deep reads, complete:** [`a4-bounds.md`](a4-bounds.md) sections "Second pass — P3 result" and
  "P3 repair — what distinguishing …"; `temp/a4-pass2/p3c-report.md`;
  `packages/derivation/subject_dispatch.py`; `packages/derivation/evaluator.py` (`collect`,
  `count`, `Environment`); `packages/derivation/runner.py` (`SourceFact` and its comment on
  rendered ids, `_append_live_source`, `evaluate_subject_scoped_rule`, the v9 declarative branch);
  `packages/derivation/marshal.py` (schema admission, input bindings, `optional_default`);
  `packages/derivation/source_authority.py` (`resolve_closure_admissions`,
  `audit_collect_authority`); `packages/derivation/package_validation.py` (what validates a rule
  and a package); `packages/schemas/derivation/rule-artifact.v9.schema.json`, the latest
  `artifact-package` schema, `packages/schemas/kernel/fact-type.v2.schema.json`, the
  `source-family` and `source-closure-mapping` schemas.
- **Stop conditions:** stop and report if every candidate home would require changing ordinary
  `collect` or `count`, manufacturing or admitting source-family closure, or comparing rendered
  ids.

## The required behaviour (owner, 2026-09-23)

For one statement subject:

1. **No recorded link** → the declared calculation default. This does **not** declare the link set
   complete.
2. **Recorded links, each current link with its own numeric, pinned reduction** → publish (box 1
   minus the reductions), pinning **every** covered link's reduction.
3. **Any uncovered link** — its reduction absent, blocked or **inapplicable** — → that statement
   blocks, and the disposition **names** the uncovered link. Uncovered is never implicitly zero.
4. Unrelated statements unaffected. Ordinary `collect` and `count` unchanged. An **undeclared**
   empty collection still blocks.

## What the contract document must contain

1. **Candidate homes, examined — not assumed.** At least: a new operation in a rule-artifact
   successor; a field on the rule in a successor; a new binding mode in an artifact-package
   successor; a separate content citizen the rule references. For each: what it declares, which
   schema changes, what validates it, what the runner/marshal must admit, and its blast radius.
   Select one, with reasons, and say what evidence would overturn the choice. The prior foreman note
   that a v10 operation is "smallest" is a hypothesis to test, not a finding.
2. **Exact shape** of the selected declaration (field names, types, required/optional), as a schema
   fragment, and one worked example for the statement rule.
3. **Identity.** How "this link" is matched to "its reduction" using **structured** identity (the
   `SourceFact.keys` tuples the kernel lattice and Track 2 carry), never a rendered `fact_id` or
   symbol — noting `SourceFact`'s own warning that renderings are non-injective. What happens when
   keys are missing (fail closed).
4. **Currency.** How a corrected or withdrawn link is handled: only **current** link findings count;
   a withdrawn link is no longer a recorded link.
5. **Semantics of each outcome**, including what is pinned in each (the default's declaration on the
   no-link path, every covered reduction and link on success, the uncovered link on block), and the
   exact `missing` content on block.
6. **The default's declaration** — where the value comes from (e.g. a pinned parameter), how the
   published result records that it came from the default, and why it is not a closure admission.
7. **What does not change**: ordinary `collect`/`count`, source families and closure, other per-
   subject callers, existing rule versions.
8. **Test obligations for stage B**, at least: flip `ObservedUnresolvedLinkDefect`'s two tests to
   the required outcomes; no link; all links resolved; an inapplicable reduction; correction of a
   link; withdrawal of a link; isolation of another statement; the blocked disposition names the
   uncovered link; a successful amount pins every covered link; an undeclared empty collection still
   blocks; and whether the rule validates as a published production rule under the new schema.
9. **Governance.** Gate 1 score with reasons, and whether a Tier 2 ADR is required; if so, the ADR's
   decision statement in one paragraph (the ADR itself is stage B's).
10. **Evidence boundary.** What the P-probes established (hand-assembled runs, synthetic rules not
    validated as published production rules), and that nothing here establishes what a durable
    reader sees — that is P4.

## Hand-off

Do not commit; the foreman reviews and commits. Report to `temp/a4-pass2/track3a-report.md`: a
summary of the selection and anything uncertain.
