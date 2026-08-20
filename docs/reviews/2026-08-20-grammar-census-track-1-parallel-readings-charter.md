# Builder Charter — Grammar Census Track 1: Three Independent Parallel Readings

Audience: Builder (three streams)

Filed by the Foreman 2026-08-20. Track 0 is complete, verified, and accepted
at `4f66bc83` after five repair rounds. Its corpus is binding.

This one file charters all three streams. **Charters are not findings** —
reading a sibling's charter section is permitted and expected. Reading a
sibling's *deliverable* is not, and that is the independence rule this
milestone depends on.

## Why three readings that cannot see each other

The census's whole method rests on this. If one reader produced all three
construct sets, a misreading would be identical in all three and would survive
reconciliation looking like agreement. Isolated readings make a shared error
visible as a disagreement in Track 2 instead of invisible as consensus.

Track 0 supplied direct evidence that this is not a theoretical concern. Two
independent readers — an external model and the Foreman — both concluded the
term/predicate vocabulary had no schema. A third reader found it, in
`source-family.v2.schema.json`, a citizen whose name gives no hint it is
there. Expect this repository to hide things in plausible-looking places.

## Shared Context Capsule

- **Source ref:** `HEAD` on `milestone/grammar-census-engine-language-map`.
  Resolve and verify the SHA against Git before acting. Confirm
  `git rev-parse --show-toplevel` and `git branch --show-current`.
- **Milestone key and primary branch:** `grammar-census` /
  `milestone/grammar-census-engine-language-map`.
- **Role:** Builder.
- **Evidence-rung ceiling:** committed repository artifacts, plus a synthetic
  execution you actually ran and show. Nothing else.
- **Full reads before acting:**
  - `docs/roles/builder.md`
  - `docs/process/concurrent-work.md`
  - `docs/phases/grammar-census/milestones/engine-language-map.md` —
    `#Objective`, `#Scope`, `#Non-goals`, `#Census unit`, `#Evidence layers`,
    `#Tracks`, `#Parallel Work Manifest`, `#Data safety`
  - `docs/phases/grammar-census/inquiries/track-0-boundary-and-corpus.md` —
    **the whole file.** Its boundary map tells you which surfaces are in
    scope; its bounded corpus tells you exactly what to read. Do not
    re-derive either.
  - your own section of this charter

## Shared constraints — all three streams

- **Write exactly one file**, named in your section. Everything else in the
  repository is read-only for you, including `docs/phase-state.md`, the
  milestone plan, this charter, the Track 0 deliverable, and any sibling
  deliverable.
- **Documentation only.** No production code, schema, package, test, fixture,
  or tax content may change. Your diff must be exactly one file.
- **Do not read a sibling stream's deliverable** —
  `track-1a-declared-constructs.md`, `track-1b-implemented-constructs.md`,
  `track-1c-observed-usage.md` — even if it exists on the branch when you
  look. If you find one, do not open it. Report that you saw it.
- **Do not read anything under `docs/phases/claim-boundary-exploration/`.**
- **A question only another layer can answer is an open question, not a
  blocker.** Record it in your deliverable and continue. The Foreman will not
  relay another stream's findings to you, including as a clarification.
- Do not push the branch. Do not open a PR. Do not create a worktree.
- No personal, private, or real filer data. No absolute workstation paths.

## Census-unit records

Use the plan's `#Census unit` fields. **Leave every `status` field set to
`pending-reconciliation`.** Assigning a construct's status is Track 2's
exclusive job, and so is every claim of the form "declared but not
implemented," "implemented but unused," or "used but undeclared." You have
read one layer. You are not in a position to make a set-difference claim, and
making one anyway is the specific failure this track structure exists to
prevent.

Record what your layer shows. Where your layer is silent, say it is silent
rather than filling the gap from inference about another layer.

## Verify before you assert

The Track 0 deliverable needed five repair rounds. Round 1 shipped three
confidently stated file counts that were all wrong. Rounds 3, 4, and 5 each
found citation defects inherited from the round before. So:

- Every path, line number, version, and count you write must be checked by
  running the check. `grep -n`, `sed -n`, `python3 -c`, `git`.
- **Never classify content by filename.** Track 0 established that
  `packages/content/tax/2025/` filename prefixes do not identify citizen
  families — `rule.*.json` spans two families and the `attachment-rule`
  family spans two naming conventions. Parse the `schema` field.
- **Never assume a version series is contiguous.** `attachment-rule` has no
  v7. Enumerate what exists; do not write a range you have not listed.
- Distinguish what you read from what you inferred. Where you infer, say so
  and say what would falsify it.

## Committing — read this carefully, you are not alone in this checkout

Three streams share one Git index in one worktree. Follow
`docs/process/concurrent-work.md`:

1. Before staging, acquire the worktree commit lock:
   `collab_lock="$(git rev-parse --git-path collaboration-commit.lock)"` then
   `mkdir "$collab_lock"`.
2. **If `mkdir` fails, the lock is held by a sibling. Do not remove it.**
   Wait and retry — sleep 10 seconds and try again, for up to 5 minutes.
   Sibling commits take seconds, so a retry will almost certainly succeed.
   Only if it is still held after 5 minutes should you stop and report a
   possibly-abandoned lock, without removing it.
3. Once you hold it, run `git status --short` — a sibling may have committed
   since you started. Stage **only your one deliverable path**.
4. Inspect `git diff --cached --name-only` and confirm it names exactly your
   one file.
5. Commit, then `rmdir "$collab_lock"` to release. Release it even if the
   commit fails.

Run `python3 tools/governance_lint.py` before handoff. It must print
`governance lint: conformant`.

---

# Track 1a — Contracts and schema

**Write only:** `docs/phases/grammar-census/inquiries/track-1a-declared-constructs.md`

Produce the **declared** construct set — what the contracts and schemas say
the language is, independent of whether any code implements it or any content
uses it.

Read `docs/adr/` and every schema version in the Track 0 corpus for the
surfaces Track 0 classified grammar proper. For each construct record: its
name, its layer, its accepted syntax, its source of authority (ADR decision
and/or schema `$defs`/`enum`, cited exactly), whether it is separately
versioned, and the declared evaluation, blocking, invalidity, and
nonpublication behavior **where the contract actually states it**.

Two things specific to your reading:

- **Where a contract is silent, that silence is your finding.** If a schema
  admits a construct but no ADR fixes its meaning, say so. Do not go read the
  implementation to fill the gap — that is Track 1b's layer, and borrowing
  from it destroys the independence this track is for.
- **Version drift within a series is in scope.** Where a construct's declared
  form changes between `rule-artifact.v3` and `.v6`, or between
  `operation-semantics.v1` and `.v2`, record the change and both forms. Do
  not silently read only the highest version — Track 0 was explicit that
  highest-numbered does not mean current.

---

# Track 1b — Runtime

**Write only:** `docs/phases/grammar-census/inquiries/track-1b-implemented-constructs.md`

Produce the **implemented** construct set — what the running code actually
interprets, independent of what any schema declares or any content uses.

Read the evaluators, validators, resolvers, and runtime consumers in the
Track 0 corpus. For each construct record: which forms the runtime actually
interprets, what each interpretation does, its evaluation/blocking/
invalidity/nonpublication behavior, and what provenance survives its
execution.

Three things specific to your reading:

- **Read the code, not the docstrings.** A comment naming an ADR is evidence
  about intent, not about behavior. Where a docstring and the control flow
  disagree, the control flow is what you record, and the disagreement is a
  finding worth stating plainly.
- **Runtime behavior carrying semantic weight that you cannot locate in any
  schema is one of your most valuable outputs.** The plan asks for it by
  name. A dispatch table, a hardcoded constant, a default applied when a
  field is absent, a validation that fires before anything declared gets to
  run — record these and say you could not find a schema for them.
- **Do not read schemas to decide what the runtime "should" do.** You will
  necessarily open some schema files to understand a data shape; that is
  fine. Deciding a construct exists because a schema declares it is not —
  that is Track 1a's answer and you must reach yours from the code.

---

# Track 1c — Content and tests

**Write only:** `docs/phases/grammar-census/inquiries/track-1c-observed-usage.md`

Produce the **observed usage** set — what actually appears in committed
content and what the test suite actually demonstrates.

Read committed rule content under `packages/` per the Track 0 corpus, and the
test suite. Record: which constructs actually appear, representative
citations by path, frequency context, and which behaviors are demonstrated by
an existing test or by a synthetic execution you ran and show.

**Your scope restriction is the tightest of the three, and it is deliberate.**
You report observation only. You may not claim a construct is unused,
unreachable, undeclared, or unimplemented, and you may not compare what you
found against any schema or any runtime module. Every such set difference
belongs to Track 2.

Concretely: "the `bracket_fold` op appears in 4 committed artifacts, cited
here" is your finding. "`bracket_fold` is declared but unused" is not, and
neither is "no content uses `X`" — you cannot distinguish *absent from the
corpus* from *absent from your search* without the declared set to check
against, and you do not have it.

What you **can** say, and should: that you searched for something specific
and did not find it, stating exactly what you searched and how. That is an
observation about your search. Frame it that way and Track 2 can use it.

Two more:

- **Frequency context, not just presence.** A construct in 1 artifact and a
  construct in 300 are different facts about the language. Count them.
- **A test that asserts a behavior and a test that merely exercises a code
  path are different evidence.** Distinguish them where you can tell.

---

## Handoff report — all three streams

Report to the Foreman:

1. the commit SHA;
2. how many constructs you recorded, and the shape of your record;
3. the most consequential thing your layer shows;
4. every open question you recorded that only another layer can answer;
5. anything in the Track 0 corpus or the plan that your reading suggests is
   wrong, missing, or unworkable — say it plainly rather than working around
   it silently;
6. whether you encountered a held commit lock or a sibling deliverable;
7. your turn count and tool-call count.
