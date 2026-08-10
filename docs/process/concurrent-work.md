# Concurrent Work Protocol

Audience: Agents

This is the normative home for milestone keys, branch names, shared worktrees,
assignment handoff, temporary worktrees, and the cross-milestone schema-intent
ledger. `AGENTS.md` owns dispatch authorization; `PROJECT_PLANNING.md` owns
milestone sequencing, review stages, PRs, and publication.

## Milestone identity and primary workspace

Every milestone establishes a unique, lowercase kebab-case **milestone key** in
its plan before the first build assignment. The key is stable for the life of
the milestone even if its title or scope wording changes.

Every milestone has one primary branch and one primary worktree. A newly
created milestone branch is named:

```text
milestone/<milestone-key>-<purpose>
```

All agents assigned to that milestone work in the primary worktree on that
branch by default. The launcher starts each agent in the established worktree;
the agent verifies `git rev-parse --show-toplevel` and
`git branch --show-current` before acting. A container uses the same absolute
mount path as the host, but no absolute workstation path is committed to the
repository.

An agent does not switch the primary worktree to another branch, check out the
primary milestone branch in a second worktree, move another agent's changes,
or create a substitute milestone branch because the shared tree is dirty.
Dirty state may belong to a collaborator. Inspect it, preserve it, and
coordinate file ownership through the Foreman.

## Branch names

New branches use one of these forms:

- `milestone/<milestone-key>-<purpose>` — the milestone's primary branch.
- `temp/milestone/<milestone-key>-<purpose>` — every temporary branch,
  including prototype, repair, review-record, checkpoint, integration, and
  schema-ledger transaction branches.
- `process/<purpose>` — a process or instruction change outside a milestone.
- `snapshot/<date>-<purpose>` — an owner-directed safety or historical ref.

The ratified lines and the dedicated `milestone-schema-ledger` branch are
standing exceptions. Do not create new `track/`, `builder-`, `repair/`,
`prototype/`, agent-name-prefixed, or tool-default branches. Existing
nonconforming branches do not authorize another one and are cleaned only by
their owner or by an explicitly assigned repository-maintenance task.

## Shared-worktree assignments and commits

A charter defines the assignment's scope and paths; it does not reserve a
private branch. The Foreman avoids simultaneous write ownership of the same
path. Agents recheck `git status --short` before editing and before staging
because the tree may have changed since launch.

The shared index has one writer at a time. Before staging or committing, an
agent atomically acquires the worktree's commit lock:

```sh
collab_lock="$(git rev-parse --git-path collaboration-commit.lock)"
mkdir "$collab_lock"
```

If `mkdir` fails, another agent owns the commit slot; do not stage, unstage, or
commit until that agent releases it. A lock owner stages only its assigned
paths—never `git add -A` or `git add .`—then inspects
`git diff --cached --name-only`. If the index contains an unassigned path, stop
without altering it and coordinate with the Foreman. Release the lock after
the commit:

```sh
rmdir "$collab_lock"
```

An abandoned lock is not removed on assumption. Confirm that its owner is no
longer active and obtain Foreman direction before removing it.

An assignment is handed off only when all of its intended changes are in one
or more named commits reachable from the primary milestone branch and
`git status --short -- <assigned-paths>` is empty. Do not leave assigned work
unstaged, staged, stashed, or committed only on a temporary branch. Unrelated
collaborator changes may keep the whole worktree dirty; identify them without
modifying them.

### Branch-wide operations

Checkout, rebase, reset, merge, cherry-pick, history rewriting, generated-tree
replacement, and force-push affect more than one assignment. The Foreman first
declares an exclusive maintenance window, stops new edits, waits for every
active assignment to commit and report its paths clean, acquires the commit
lock, and verifies the entire primary worktree and index are clean. Only then
may the assigned operator perform the branch-wide operation. Release the lock
and reopen assignments only after the new `HEAD`, branch name, and worktree
state are reported. No agent infers permission to discard, stash, or relocate
another agent's changes in order to make the maintenance window clean.

## Temporary worktrees

A temporary worktree is an exception for isolation that cannot be achieved
safely in the shared tree. Create it only on a
`temp/milestone/<milestone-key>-<purpose>` branch forked from a named primary
milestone commit. Never attach the primary milestone branch itself to the
temporary worktree.

The worktree path must be beneath the creating agent's own hidden directory,
identified by a `/.<agent-name>/` path component. An agent may remove only
worktrees and temporary branches it created beneath that directory. It never
removes, prunes, cleans, switches, stages in, or repairs a worktree outside its
own `/.<agent-name>/` subtree—even if Git reports it clean or its branch
merged. The notation describes a path component such as `/.codex/`; it does not
mean a directory at the filesystem root.

Temporary work is complete only after its reviewed commit is integrated onto
the primary milestone branch during a branch-wide maintenance window, the
integrated result is verified there, and the creating agent removes its own
temporary worktree and branch. A temporary branch never opens an independent
PR.

## Concurrent milestones

Concurrent milestones each keep their own primary branch and primary
worktree. They do not share uncommitted files or integrate one another's WIP.
They coordinate prospective published-schema changes through the schema-intent
ledger below, then reconcile actual committed state against the ratified line
during publication.

### Schema-intent ledger

`milestone-schema-ledger` is a standing operational branch that is never
merged into a milestone or ratified line. It is an append-only visibility
stream, not product authority, a version reservation, a lock, or proof that a
schema change is valid.

As soon as a milestone chooses a schema family and proposed version—or
materially redesigns or withdraws that proposal—append an event before making
the corresponding schema edit. Work need not be complete or rebased. No
schema-changing assignment may be handed off without its current intent in the
ledger. Append at:

```text
schema-ledger/events/<milestone-key>/<event-id>.json
```

Use a globally unique, time-sortable event id such as
`<UTC-basic-timestamp>-<schema-family>-<random-suffix>`. One event occupies one
new file. Never edit, delete, rename, reformat, or replace an earlier event.
A redesign or withdrawal is another event whose `replaces_event` names the
earlier event. A `destructive-redesign` event describes abandonment of WIP; it
never permits mutation of a published schema.

Each event has this shape:

```json
{
  "format": 1,
  "event_id": "20260809T210000Z-artifact-package-a1b2c3",
  "recorded_at": "2026-08-09T21:00:00Z",
  "milestone_key": "demo-milestone",
  "milestone_branch": "milestone/demo-milestone-purpose",
  "milestone_commit": "0123456789abcdef0123456789abcdef01234567",
  "schema_family": "artifact-package",
  "schema_path": "packages/schemas/artifact-package/artifact-package.v99.schema.json",
  "schema_version": "v99",
  "action": "propose",
  "change_kind": "additive",
  "replaces_event": null,
  "summary": "Add a synthetic demonstration field for the bounded milestone."
}
```

`action` is `propose`, `revise`, `withdraw`, or `publish`;
`change_kind` is `additive`, `destructive-redesign`, or `withdrawal`. Values
must remain safe for the repository: no personal facts, credentials, private
outputs, refusal reasons, or absolute workstation paths. `milestone_commit`
is the primary milestone `HEAD` observed when the intent is recorded; it may
precede the schema implementation commit. Append `publish` when the exact
schema commit enters the milestone's curated candidate; append `revise` if a
rebase or collision changes the proposed version or design before then.

Append through a short-lived temporary branch/worktree rooted at the current
`milestone-schema-ledger` tip. Record that starting tip as `ledger_base` before
creating the transaction branch. After committing the one new event,
atomically fast-forward the standing local ref with compare-and-swap:

```sh
git update-ref refs/heads/milestone-schema-ledger HEAD "$ledger_base"
```

If the compare-and-swap fails, another event landed first. Rebase the
transaction branch onto the new ledger tip and retry; do not modify either
event. After the ref advances, return to the primary milestone worktree,
continue the assignment, and remove the agent-owned ledger worktree and
temporary branch. The ledger branch itself is not checked out in a long-lived
worktree.

Agents consult the event stream before selecting a new schema version and at
publication synchronization, but they do not rebase, merge, or redesign their
milestone merely because another milestone has WIP. The Foreman classifies
overlap from the actual candidate states. Published-schema immutability,
manifest generation, final union preservation, and CI remain the gates of
record.
