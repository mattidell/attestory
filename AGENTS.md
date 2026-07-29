# Agent Operating Guide

Audience: Agents. This is a **router**, not a rulebook. Read it once at boot,
then read your seat file and stop reading this one.

It carries only what binds every seat regardless of role. Everything else has a
home named in "Where authority lives" at the bottom.

**Single-source rule (ADR-0045).** Every rule in this project lives in exactly
one document. Other documents reference it by name and do not restate it. If
you find the same rule written twice, that is a defect — say so; do not try to
reconcile the two wordings.

## Which seat are you

You hold exactly one seat. It is determined by how you were launched, not by
what the work looks like.

| Seat | Entry | Seat file |
| --- | --- | --- |
| **Foreman** | Owner says "resume as foreman" (or `/foreman`) | `docs/roles/foreman.md` |
| **Builder** | Owner says "pick up the current task" (or `/pickup`), **or** the foreman dispatches you | `docs/roles/builder.md` |
| **Reviewer** | Same two paths as builder | `docs/roles/reviewer.md` |
| **Advisor** | Owner says "take the advisor seat" | `docs/roles/advisor.md` |

**Builder and reviewer: you do not need to be told which.** Run the orientation
command; the role is auto-detected from phase state's `current_role`:

```sh
python3 tools/build_orientation_block.py --ref HEAD
```

Use `HEAD`, not a line name. Your charter usually has not merged yet, so it
exists only on the branch you are standing on; orienting from `main` loads a
phase state that has never heard of your track and reports a topic mismatch.
The ratified line to corroborate against is a separate question and is derived
for you — see "Check whether you are stale before you work."

This prints one Orientation Block at a resolved commit: your current charter
plus the plan's action-scoped, section-anchored deep reads — only the cited
sections, as Git blob content rather than prose. Then: (1) verify the printed
commit SHA against Git; (2) adopt the seat file for the detected role;
(3) echo back your understood scope, evidence ceiling, and stop conditions;
(4) act. Pass `--role` / `--action` only if detection fails.

If phase state marks a **clean-room / rival** round, the block auto-switches —
no flag. It emits charter, scope, and non-goals but lists deep reads as a
manifest only, and instructs you to reimplement from the spec without reading
any other builder's implementation or thread.

**Foreman:** re-enter with `python3 tools/foreman_context.py --ref HEAD
--format markdown`. Its capsule is **advisory** — reconcile its resolved commit
and worktree report against Git before acting. If it refuses, read the
committed sources it names directly; never replace a refusal with a prose
summary.

Both commands take `--ref HEAD` so they read the committed state of the
worktree being resumed. The tool separately derives the ratified comparison
line from history (`resolve_ratified_ref`); do not substitute a literal
`main` or `main-ui` unless you are intentionally reading that line's tree.
Say which source ref you used.

Do not ask the owner to paste context. Do not reconstruct context from prose
when a command will give it to you from Git.

## How work moves

A milestone runs through these stages. The **foreman owns the loop**; builders
and reviewers execute one chartered unit inside it and nothing more.

1. **Establish scope** — the foreman drafts the milestone plan against the
   phase roadmap and maturity matrix. The plan is committed before
   implementation begins.
2. **Rival prototypes** — for decisions requiring prototype evidence, rival
   builders work from independent contexts. One context may not author both
   competing shapes.
3. **Review and repair** — an author-independent reviewer measures the unit
   against its charter and returns findings. The foreman triages; a repair
   builder addresses them. Reviews are advisory; the owner dispositions.
4. **Establish the scope contract** — the evidence settles into an ADR, or into
   the plan's contracts section, and becomes binding.
5. **Build** — chartered tracks, one commit per completed track.

Not every milestone runs all five. Tooling, exploratory, and process milestones
skip stages by design; **the milestone plan says which apply.** If the plan is
silent on a stage, that is a plan defect to raise, not a stage to improvise.
After the final applicable stage merges, the foreman performs
`PROJECT_PLANNING.md`, "Milestone Closeout", before the repository is ready for
the next foreman.

## Dispatch authorization

**Spawning** means instantiating a sub-agent. **Dispatch** means the foreman
spawning a sub-agent to fulfill the current role in the approved plan. An owner
opening a new thread and supplying the current prompt is an **owner launch**,
not a dispatch.

**Only the foreman may spawn sub-agents. Every other seat: never.**

The foreman may dispatch **only when a message from the owner in this live
thread literally contains the string `I authorize dispatch`.**

- No paraphrase substitutes. Not "go ahead", not "sounds good", not an
  obviously approving reply, not the owner's approval of the plan.
- It is single-use, bound to the role and charter current when granted. It
  does not carry to the next role, to a re-dispatch after a charter revision,
  or to another thread.
- It is ephemeral thread context, **never** repository state — no file, field,
  or plan status can grant it.

**This gates one thing: spawning. It does not gate the work.** Absent the
string, the foreman does its normal job the normal way — charter the unit and
let it run owner-launched. Milestone progress needs no approval, grant, or
permission from the owner: build, review, repair, repeat, keeping project
state such that another foreman can pick up mid-stream. A foreman that
reports a role "prepared but not launchable" and stops has misread this
section. The owner says the string in the rare case they would rather not be
involved in the launch.

**The real precondition on a builder or reviewer is a charter**, committed and
scoped. No charter, no work — that, and not a permission, is what holds a unit.

Record every dispatch and owner launch in `metrics/spawn-ledger.jsonl` via
`tools/spawn_ledger.py`, with its role and prompt lineage, so cost stays
measured rather than guessed.

> **Heading stability.** The section headings in this file are referenced by
> `deep_reads` anchors in milestone plans (`AGENTS.md#Data Safety Rules` and
> friends). A missing anchor does not fail CI — `build_orientation_block.py`
> degrades it to a full-file read. **Renaming a heading here is a breaking
> change**: grep for `AGENTS.md#` and update every plan in the same commit.

## Shared invariants

These bind every seat. Each is normed here and nowhere else.

**CI is the gate of record.** The `verify` workflow (`pytest -n auto` +
`-m mypy` + `governance_lint` + `envelope_scan`) runs on every PR and blocks
merge on red. A green `verify` check on a commit is the tamper-proof record —
reference it.

- **While iterating:** run only the module you touched,
  `python3 -m unittest tests.<module>` (seconds).
- **Before opening or updating a PR:** optionally run `pytest` locally (~26s)
  so CI isn't your first signal.
- **Never re-run the suite to "confirm" a deterministic result**, and never
  substitute a self-reported `pytest: N passed` line for the check.
- **The foreman does not run the suite** — it opens the PR, references the
  check, and merges only on green. A reviewer runs `pytest` only to confirm a
  specific failing claim.

**What reaches `main` is normed in `PROJECT_PLANNING.md`.** Follow "Branch, PR,
and Merge Protocol" for review units and its two named direct-main exceptions,
including "Milestone Closeout"; do not invent another exception.

**Process is the owner's method; ADRs are product contracts (ADR-0045).** How
work is organized — seats, the milestone loop, dispatch, chartering, review
cadence, branch and merge mechanics, context routing, capability tiers — is
changed by owner direction plus an edit to the document that norms it. It needs
no ADR, no ratification, and no evidence. ADRs are for decisions later artifacts
are written against: governance, the kernel, schemas and citizen shapes, the rule
language, composition and closure, data-residency and trust boundaries.

Consequently: **never cite a process ADR against owner direction.** The seven
former process ADRs (0005, 0013, 0030, 0039, 0040, 0042, 0043) are `retired` —
history and rationale, never authority. Where direction and a process document
disagree, the direction governs and the document is updated to match. If you
think a change is unwise, say so once, plainly, then comply.

**History is not editable in place.** Never edit an accepted ADR's decision to
change history — supersede it. Never rewrite `main` without an owner direction
and a `snapshot/<date>-<topic>` ref created and verified first. Published
schemas have their own protocol below.

**`archive/` is never authority.** It holds the pre-governance v2 engine, which
predates the Ontology and violates it in places. Use it for tax-domain
reference only — never for contracts, schemas, or patterns.

**Stop when your unit turns on governance text.** You are not expected to hold
`docs/governance/` in context (ADR-0045). If your work appears to require
interpreting the Constitution, Ontology, or Engineering Constraints, stop and
escalate to the owner, who may call an advisor consultation. Do not improvise
doctrine, and do not build on reserved or deferred ontology entries.

## Data Safety Rules

The data boundary (**ADR-0031**) is absolute. Real values, dispositions,
refusal reasons, workspace locations, credentials, and private outputs never
enter the repo, a branch, a review, a chat, or your output. Only the three-fact
non-descriptive attestation crosses.

Never commit:

- Personal source documents; real uploaded tax documents.
- Personal current-year fact instances; personal manual entries; prior returns.
- Generated artifacts derived from personal data.
- Absolute local machine paths in committed fixtures or manifests.

Personal or ad hoc local work stays under ignored paths: `local-data/`,
`temp/`, `private-archive/`, `uploads/`, `generated/user/`.

Synthetic committed files use demo labels and obviously synthetic IDs
(`demo.*` / `demo-*`). Run the data safety tests when changing fixtures,
manifests, paths, or generated artifacts; a reviewer additionally runs
`python3 tools/envelope_scan.py --range main..HEAD`.

## Fixture Rules

Fixtures must be synthetic and safe to publish.

Use **committed** fixtures for: stable sample source data; stable workspace
scenarios; expected golden artifacts; contract-level tests.

Use **ignored local output** for: ad hoc runner output; personal experiments;
generated scratch files.

Golden fixture changes must be intentional. Regenerate only when the contract
or the expected behavior changed, then inspect the diff.

## Schema Publication Protocol

Article 9 and **ADR-0003** make every published schema version immutable. A
schema file named in any `packages/schemas/*/published.json` is published
history, including its exact bytes. A checksum is an integrity witness, never
permission to revise that history.

- Never edit, reformat, move, delete, or replace an existing published
  `*.vN.schema.json` file. A semantic or byte-level change requires a new,
  unused version filename, with matching `$id` and `schema` discriminator;
  existing instances remain bound to their recorded version unless an explicit
  migration contract says otherwise.
- Never hand-edit an existing checksum in `published.json`. After adding a new
  schema file, use `packages.kernel.schema_registry.write_manifest` for that
  schema directory to append its checksum. If the generated manifest changes an
  existing entry or removes one, **stop**: restore the published file and make
  the change as a new schema version instead.
- Before handing off a schema change, inspect the manifest diff to confirm it
  only adds the new filename, and run
  `python3 -m unittest tests.test_schema_registry` plus the track's schema and
  consumer tests. The registry test proves that a mutated published schema and
  a republished checksum are both rejected.

## Working rules

Bash starts at repo root and cwd persists. **Never `cd` to the root**; use
absolute paths for other directories.

In Claude Code a `[worktree-state]` line is injected at session start by a
SessionStart hook. It is accurate **at that moment only** — another agent may
be working in the same tree. Trust it for your first turn; re-check with
`git status` if the session runs long or you suspect drift. Use `git status` /
`git diff` to verify your own changes after editing.

**Check whether you are stale before you work.** The tree you resume into may
have been overtaken while you were away: a PR of this branch may already be
merged, or the ratified line may have moved past the state
`docs/phase-state.md` describes. Fetch first, then compare — do not infer
freshness from phase state, the plan status, or a hook line. The foreman's
required `tools/foreman_context.py --ref HEAD` call performs this fetch and
reports divergence plus whether the current branch tip is already contained in
the ratified line; that report satisfies the foreman check.

**Compare against the right line.** This repository carries more than one:
`main` for the derivation work and `main-ui` for the surface work. They are
separate continuous records, and a branch cut from one is *expected* to look
wildly behind the other. Comparing surface work against `origin/main` produces
a confident "you are 7 behind and 51 ahead" that means nothing. Do not assume
the line — the tooling derives it from your history
(`resolve_ratified_ref` in `tools/foreman_context.py`), and the capsule prints
which one it used. Other seats run:

```sh
git fetch origin --prune
RATIFIED=$(python3 tools/foreman_context.py --ref HEAD --format json \
  | python3 -c 'import json,sys; print(json.load(sys.stdin)["milestone"]["ratified_line"])')
git rev-list --left-right --count "$RATIFIED"...HEAD   # behind<TAB>ahead
gh pr list --state merged --head "$(git branch --show-current)" --limit 3
```

Read it as: **ahead 0 and a merged PR for this branch** means your work already
landed — this workspace is spent, and continuing on it re-does or reverts
merged history. For a foreman, `spent: true` is the equivalent reachability
proof. **Behind > 0** means your base is stale; rebase or re-cut from the
ratified line before building, and re-verify that the charter still describes
work that remains.

**Both halves of that sentence matter.** A milestone opens with one PR and
closes with another on the same branch, so from the first merge onward there is
*always* a merged PR for the branch you are standing on. That alone means
nothing. It is only a spent workspace when `ahead` is 0 as well. Either way, **say so explicitly** — name the branch, the merged PR when
known, and how far behind you are — and get direction before proceeding.
Silently working in a superseded tree is the failure this rule exists to
prevent.

Keep worktrees to a minimum. Remove worktrees that are clean and no longer
needed, including stale ones left by other agents. Delete merged branches after
confirming their commits are reachable from `main`. Do not leave uncommitted
work in a worktree at hand-off — commit it, snapshot it, or discard it and say
so.

If you resume another agent's interrupted work, say so in the retrospective,
note what you adopted versus reworked, and leave the tree clean.

## Development priorities

In this order: (1) data safety; (2) contract clarity; (3) deterministic
fixtures and tests; (4) small atomic commits; (5) documentation that reflects
actual behavior; (6) product/app work only after stable engine boundaries
exist.

Do not optimize for UI, persistence, or broad tax coverage before the current
engine contracts are stable.

## Where authority lives

Read a document when its **When** column applies to you — not before.

| Document | Norms | When you read it |
| --- | --- | --- |
| `docs/roles/<seat>.md` | Your posture, seed set, disciplines | On boot, always |
| Your charter | Scope, deliverables, stop conditions | On boot; it controls over any capsule |
| `PROJECT_PLANNING.md` | Planning protocol, milestone/track rules, capsule contracts, prototype gates, branch/commit protocol, document layout, ADR and retrospective shapes, archive rules | Foreman, when planning or chartering |
| `docs/adr/INDEX.md` | ADR routing (advisory) | On boot — digests only. Read a full ADR only when acting on its exact text |
| `docs/phases/<phase>/` | Phase overview, roadmap, milestone plans | Foreman. **Builders and reviewers orient from their charter and Orientation Block, never from phase state** |
| `docs/phase-state.md` | Product briefing, active pointer | Foreman and advisor |
| `docs/milestone-retrospectives/` | Completed-milestone lessons | Foreman — when the initial milestone briefing names a specific retrospective as useful follow-up context |
| `docs/governance/` | The sole contract authority | **Advisor only** (ADR-0045). Enforced for every other seat by CI and by the stop condition above |
| `docs/roles/craft-notes.md` | Recurring how-to reminders per seat | When your seat file points you there |
| `README.md` | Current usage and runner commands | When running the product |
| `docs/runner-economy.md` | Owner-facing runner and cache economy | Not an agent instruction |

Accepted ADRs bind whether or not a charter lists them. On any conflict between
a digest and an ADR's text, the text governs. `rejected` / `superseded` /
`proposed` / `retired` ADRs are inert — never load them as authority.
