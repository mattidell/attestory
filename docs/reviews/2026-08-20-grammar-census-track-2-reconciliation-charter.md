# Builder Charter — Grammar Census Track 2: Adversarial Reconciliation

Audience: Builder

Filed by the Foreman 2026-08-20. Tracks 1a, 1b, and 1c are complete and
accepted at `983b6102`, `495adeac`, and `bb5ea26b`. Independence held: each
stream saw sibling deliverables appear in the working tree and none opened
one. **Independence now ends.** You read all three.

This charter covers the reconciliation only. Representative traces and the
tension catalog are chartered separately, from your output.

## Context Capsule

- **Source ref:** `HEAD` on `milestone/grammar-census-engine-language-map`.
  Resolve and verify the SHA against Git before acting.
- **Milestone key and primary branch:** `grammar-census` /
  `milestone/grammar-census-engine-language-map`. Primary worktree is the one
  you are launched in.
- **Assigned path — write exactly one file:**
  `docs/phases/grammar-census/inquiries/track-2-reconciliation.md`.
  Everything else is read-only for you, including all four inquiry
  deliverables, the plan, `docs/phase-state.md`, and this charter.
- **Role:** Builder.
- **Evidence-rung ceiling:** committed repository artifacts, the four inquiry
  deliverables, and a synthetic execution you actually ran and show.
- **Full reads before acting:**
  - `docs/roles/builder.md`
  - `docs/process/concurrent-work.md`
  - `docs/phases/grammar-census/milestones/engine-language-map.md` —
    `#Objective`, `#Scope`, `#Non-goals`, `#Census unit`, `#Tracks`,
    `#Claim-boundary evidence posture`, `#Exit criteria`, `#Data safety`
  - `docs/phases/grammar-census/inquiries/track-0-boundary-and-corpus.md`
  - `docs/phases/grammar-census/inquiries/track-1a-declared-constructs.md`
    (108 constructs)
  - `docs/phases/grammar-census/inquiries/track-1b-implemented-constructs.md`
    (90 constructs)
  - `docs/phases/grammar-census/inquiries/track-1c-observed-usage.md`
    (84 constructs)
  - this charter

## Goal

Compare the three construct sets and produce the reconciled census. **You are
the only track permitted to make set-difference claims** — declared but not
implemented, implemented but not declared, used but neither, and every other
cross-layer statement. Tracks 1a–1c were each forbidden from making them, so
every such claim in this milestone originates with you and must be reasoned
here.

You also assign each construct's final `status`. Every Track 1 record carries
`pending-reconciliation`; none of them may keep it.

## What to produce

1. **A reconciled construct table.** One row per construct, showing which of
   the three layers attests it, the final `status`, and a citation. Where the
   three streams named the same thing differently, unify the name and record
   both original names — a naming difference is not a set difference, and
   collapsing them silently would manufacture agreement.

2. **Explicit treatment of every disagreement.** For each: what each layer
   says, which is right if that is determinable from source, and what would
   settle it if it is not. **Do not silently prefer one layer's account.** In
   particular, do not treat the schema as authoritative merely because it is
   declarative, or the runtime as authoritative merely because it executes.

3. **Resolution of the open questions the three streams recorded.** They
   recorded roughly thirty between them, each being a question one layer could
   not answer alone. Most should now be answerable because you hold all three.
   Answer the ones you can, from source. For the rest, say what is still
   missing.

4. **A verification of the disagreements that matter.** Where two layers
   conflict on something consequential, go to source and settle it yourself
   rather than adjudicating between two reports. Show the check.

## What the Foreman has already verified — do not redo, do not assume more

The Foreman independently confirmed these against source. Treat them as
established and build on them:

- `attachment-rule.v5.schema.json` declares `"$id": "tax/attachment-rule.v3"`,
  the same `$id` as `attachment-rule.v3.schema.json`, with a different
  SHA-256. Two published files claim one schema identity.
- `selected_producer` appears nowhere in `packages/derivation/runner.py`.
- `loader.OPERATION_VOCABULARY` is a 14-element frozenset; the evaluator
  dispatches substantially more ops than that.
- All 59 `round` nodes in committed `rule-artifact` content take a `ref` to
  `rounding.convention` as `mode`; none uses a literal mode string.
- `accounts_for` is present in `rule-artifact.v5` and absent in `.v6`.
- Track 0's evaluator citations are off by two lines: the blocking constants
  are at `evaluator.py:24-28` and `_ROUND_MODES` at `:30`. Track 1b caught
  this; it is a citation defect in Track 0, not a substantive error.

Everything else in the three deliverables is **unverified by the Foreman.**
Do not treat a Track 1 claim as established because it is committed.

## The specific failure this track exists to prevent

Three readings can agree and all be wrong. Track 0 demonstrated it: two
independent readers concluded the term/predicate vocabulary had no schema,
and a third found it in `source-family.v2.schema.json` — a citizen whose name
gives no hint it is there. Agreement between your three inputs is evidence,
not proof.

So: **where all three layers agree on something load-bearing, spot-check it
against source anyway.** Not all of it — say how you chose your sample and
what you found. If a three-way agreement turns out to be wrong, that is the
single most valuable finding this milestone can produce.

## Constraints

- **Documentation only.** No production code, schema, package, test, fixture,
  or tax content may change. Your diff must be exactly one file. The
  `attachment-rule.v5` `$id` collision is a **finding, not a repair** — do
  not fix it, and do not let any other defect you find tempt you into a code
  change.
- Cite every material claim to a committed path, with the version where the
  artifact is versioned, or to a synthetic execution you ran and show.
- **Never classify content by filename** — parse the `schema` field. **Never
  assume a version series is contiguous** — `attachment-rule` has no v7.
- You **may** use merged CQ-1 claim-boundary artifacts as a bounded validation
  lens, per the plan's `#Claim-boundary evidence posture`. You may **not** use
  unmerged CQ-2 work, and you may not let that lens originate a census claim —
  it checks conclusions you reached from the corpus, nothing more. If you use
  it, say exactly where and what it changed.
- Do not push the branch. Do not open a PR. Do not create a worktree.
- No personal, private, or real filer data. No absolute workstation paths in
  anything you commit.

## Stop conditions

Record and continue on anything short of the following. Return without
completing only if the three construct sets cannot be reconciled at all —
for example if they are describing incommensurable things and no construct
correspondence can be established. Say why.

Also return if this charter and the plan disagree about your scope. The plan
controls; do not resolve the conflict yourself.

## Committing

You are the only Builder running. Still follow
`docs/process/concurrent-work.md`: acquire the worktree commit lock, stage
only your one path, inspect `git diff --cached --name-only`, commit, release.

Run `python3 tools/governance_lint.py` before handoff. It must print
`governance lint: conformant`.

## Handoff report

Write your report to the absolute scratch path given in your launch brief,
not in chat. Answer:

1. the commit SHA;
2. how many constructs the reconciled census carries, and the `status`
   distribution across them;
3. the most consequential agreements, mismatches, and unknowns;
4. which three-way agreements you spot-checked, how you chose them, and
   whether any failed;
5. which of the streams' open questions you resolved and which survive;
6. whether you used the CQ-1 lens, and what it changed;
7. anything in Track 0, the Track 1 deliverables, or the plan that your
   reading suggests is wrong — say it plainly;
8. your turn count and tool-call count.
