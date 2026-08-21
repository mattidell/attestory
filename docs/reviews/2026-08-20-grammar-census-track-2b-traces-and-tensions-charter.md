# Builder Charter — Grammar Census Track 2b: Representative Traces and Tension Catalog

Audience: Builder (two streams)

Filed by the Foreman 2026-08-20. Track 2's reconciliation is complete and
accepted at `f276cc5b`, carrying 166 reconciled constructs. The Track 2
Builder correctly reported that the plan names three Track 2 deliverables
while its charter produced only one, and recorded that gap rather than
expanding its own scope. This charter closes it.

One file charters both streams. **Charters are not findings** — read the
other stream's section. Reading the other stream's *deliverable* is not
forbidden here, because the independence rule that governed Track 1 has
already served its purpose; but neither stream may wait on the other, and
neither may cite the other. Cite the reconciliation.

## Shared Context Capsule

- **Source ref:** `HEAD` on `milestone/grammar-census-engine-language-map`.
  Resolve and verify the SHA against Git before acting. Confirm
  `git rev-parse --show-toplevel` and `git branch --show-current`.
- **Milestone key and primary branch:** `grammar-census` /
  `milestone/grammar-census-engine-language-map`. Primary worktree is the one
  you are launched in. Do not create a worktree.
- **Role:** Builder.
- **Evidence-rung ceiling:** committed repository artifacts, the five inquiry
  deliverables, the correction record named below, and executions you
  actually ran and show.
- **Full reads before acting:**
  - `docs/roles/builder.md`
  - `docs/process/concurrent-work.md`
  - `docs/phases/grammar-census/milestones/engine-language-map.md` —
    `#Objective`, `#Scope`, `#Non-goals`, `#Census unit`, `#Deliverables`,
    `#Representative traces`, `#Tension catalog`, `#Tracks`,
    `#Claim-boundary evidence posture`, `#Exit criteria`, `#Data safety`
  - `docs/phases/grammar-census/inquiries/track-2-reconciliation.md` — **the
    whole file. It is your primary input.** Its 166-construct table, its
    disagreement entries, its spot-checks, its source verifications, and its
    surviving open questions are what you build from.
  - `docs/reviews/2026-08-20-grammar-census-foreman-correction-5b-ii-ruling-reasoning.md`
    — a Foreman ruling whose reasoning Track 2 falsified. Both streams need
    it; the tension-catalog stream needs it most.
  - your own section of this charter
- **Read as needed, not cover to cover:**
  `track-0-boundary-and-corpus.md` and the three Track 1 deliverables. Track 2
  already reconciled them. Go back to one when you need the underlying record
  behind a reconciled row; do not re-derive Track 2's conclusions.

## Shared constraints — both streams

- **Write exactly one file**, named in your section. Everything else in the
  repository is read-only for you, including `docs/phase-state.md`, the plan,
  this charter, and all five inquiry deliverables.
- **Documentation only.** No production code, schema, package, test, fixture,
  or tax content may change. Your diff must be exactly one file. Every defect
  in the reconciliation is a **finding, not a repair** — including the
  `attachment-rule.v5`/`v3` `$id` collision and the predicate-depth
  divergence. Do not fix anything.
- **Do not read anything under `docs/phases/claim-boundary-exploration/`.**
  You may use merged CQ-1 artifacts as a bounded validation lens per the
  plan's `#Claim-boundary evidence posture`; you may **not** use unmerged
  CQ-2 work; and the lens may not originate a claim. If you use it, say
  exactly where and what it changed.
- Cite every material claim to a committed path — with the version where the
  artifact is versioned — to a reconciled construct ID (`U-###`), or to an
  execution you ran and show.
- **Never classify content by filename** — parse the `schema` field. **Never
  assume a version series is contiguous** — `attachment-rule` has no v7.
- Do not push the branch. Do not open a PR.
- No personal, private, or real filer data. No absolute workstation paths in
  anything you commit.

## Verify before you assert

Track 2 is good work, but it is one reader's synthesis of three readers, and
the Foreman has verified only part of it. Treat a reconciled row as a strong
lead, not as established fact. Anything you place at the centre of a trace or
a catalog entry, check against source yourself and show the check. Track 0
needed five repair rounds and the Foreman's own ruling was falsified by
running code he had only read around.

## Committing — you are not alone in this checkout

Two streams share one Git index in one worktree. Follow
`docs/process/concurrent-work.md`:

1. Before staging, acquire the worktree commit lock:
   `collab_lock="$(git rev-parse --git-path collaboration-commit.lock)"` then
   `mkdir "$collab_lock"`.
2. **If `mkdir` fails, the lock is held by your sibling. Do not remove it.**
   Sleep 10 seconds and retry, for up to 5 minutes. Only if it is still held
   after 5 minutes should you stop and report a possibly-abandoned lock,
   without removing it.
3. Once you hold it, run `git status --short`. Stage **only your one
   deliverable path**.
4. Inspect `git diff --cached --name-only` and confirm it names exactly your
   one file.
5. Commit, then `rmdir "$collab_lock"` to release. Release it even if the
   commit fails.

**Commit incrementally.** Write a section, commit it, continue. Do not hold
the whole document until the end — a long run that dies unwritten loses
everything.

Run `python3 tools/governance_lint.py` before handoff. It must print
`governance lint: conformant`.

---

# Track 2b-i — Representative traces

**Write only:** `docs/phases/grammar-census/inquiries/track-2-representative-traces.md`

Produce roughly four to six traces, selected for **semantic contrast, not tax
coverage**, per the plan's `#Representative traces`. For each, show the path
from declared content, through validation, through evaluation, to the
resulting finding, block, nonpublication, or explanation consequence.

The plan's suggested contrasts are arithmetic composition, conditional
applicability, source-set closure and blocking, categorical reasoning, and a
worksheet-like computation. Treat that as a starting set, not a quota. Choose
from the reconciled census and **say why each trace earns its place** — what
construct or behavior it exhibits that no other trace in your set exhibits.
Stop adding traces once one would repeat an already-described construct.

Three things specific to your stream:

- **Executed evidence and static reading must be visibly distinguished, line
  by line.** This is the plan's explicit requirement and the whole value of a
  trace. Where a step is an actual runner invocation or an existing test, say
  so and show the invocation or name the test. Where it is you reading the
  code and concluding what would happen, mark it as inference and say what
  would falsify it. A trace that blurs the two is worse than no trace.
- **Prefer real committed content over synthetics** where committed content
  exercises the construct. Track 1c recorded frequency; a construct appearing
  in 300 artifacts and one appearing in 1 are different facts, and a trace
  built on the common case tells the reader something a hand-built synthetic
  does not. Use a synthetic where no committed content reaches the behavior —
  and say that is why.
- **At least one trace must end somewhere other than a successful finding.**
  Blocking, nonpublication, and invalidity are part of this language's
  semantics; Track 2 verified several such paths (`SOURCE_SET_UNCLOSED`,
  `DEPENDENCY_ABSENT`, `DEPENDENCY_INVALID`, `inapplicable` with a real
  `guard_result`). A trace set that only shows things working describes a
  different engine than the one that exists.

---

# Track 2b-ii — Tension catalog

**Write only:** `docs/phases/grammar-census/inquiries/track-2-tension-catalog.md`

Build the catalog from the reconciliation, per the plan's `#Tension catalog`,
folding in the Track 0 representational-gap records that survive as
actionable. For each entry state: the evidence, the affected layer, the
possible user or maintenance consequence, the remaining uncertainty, and a
plausible next action.

**The plan's two disciplines are the whole job, and they pull against each
other. Hold both.**

- **"Do not assume these are defects."** Several things this census found are
  deliberate. ADR-0066 allocated depth enforcement away from JSON Schema on
  purpose. A declared-and-unused role value may be a reserved extension point
  rather than dead weight. Say which entries you can establish as intentional
  and which you cannot, and do not import a tone of alarm the evidence does
  not carry.
- **"Do not admit an entry merely to make the catalog look complete."** A
  short catalog of load-bearing tensions is a better artifact than a long one
  padded with observations. If a Track 0 gap or a Track 2 disagreement does
  not plausibly support later action, say you considered it and dropped it,
  and why. That record is itself useful.

Four things specific to your stream:

- **Rank by consequence, and defend the ranking.** Track 3 and the owner will
  read the top of your list hardest. The census has produced at least three
  candidates of visibly different weight: a published ADR contract that
  admission does not enforce as written (see the correction record); two
  published schema files claiming one `$id` with different bytes, making one
  file's content unreachable; and a 14-element `OPERATION_VOCABULARY` that no
  code calls while the evaluator dispatches 23 ops. These are not equally
  consequential. Say which is which and on what basis.
- **A tension between a *contract* and its *enforcement* is a different class
  from a tension between two *implementations*.** The first says the project
  believes something untrue about itself; the second says two code paths
  disagree. Distinguish them — the remedies are different, and so is who
  should decide.
- **Track 2 left eight open questions surviving.** Several are tension
  entries in disguise; several are genuinely just unknowns. Sort them, and
  say which are which.
- **Some tensions are about what the language cannot express, not about a
  disagreement.** The plan names these — tax-specific encodings that may
  conceal a general language need, distinctions one layer collapses,
  grammar choices that limit provenance or user explanation. A census that
  only catalogs internal inconsistencies misses the question the phase
  actually exists to answer. Look for them deliberately.

---

## Stop conditions — both streams

Record and continue on anything short of the following. Return without
completing only if your primary input is unusable — for example if the
reconciliation cannot support trace selection at all, or if the tension
classes the plan names have no instances in it. Say why.

Also return if this charter and the plan disagree about your scope. The plan
controls; do not resolve the conflict yourself. Track 2 hit exactly this and
handled it correctly: it recorded the gap and did not expand scope.

## Handoff report

Write your report to the absolute scratch path given in your launch brief,
not in chat. Answer:

1. the commit SHA (or SHAs, if you committed incrementally — list them);
2. what you produced, in counts: traces, or catalog entries by class;
3. your selection reasoning — what you included and what you deliberately
   left out;
4. what you checked against source yourself, and whether anything in the
   reconciliation failed that check;
5. whether you used the CQ-1 lens, and what it changed;
6. anything in Track 0, the Track 1 deliverables, the reconciliation, the
   correction record, or the plan that your reading suggests is wrong — say
   it plainly;
7. whether you encountered a held commit lock;
8. your turn count and tool-call count.
