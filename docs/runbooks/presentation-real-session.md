# Runbook — one real Presentation viewing session

Audience: Owner (this runbook is followed by a human, not an agent).

This file outlives any one milestone: every future real viewing session against
`open_presentation_session` follows it. It has two parts. Part 1 is the exact
sequence for one sitting. Part 2 is the bounded set of things you may say about
a session that failed — read it *before* you sit down, not after, because the
whole point of it is that you cannot improvise a description once you are
looking at real output.

Governing decisions: ADR-0047 (Live Viewing Environment, and its amendment
placing Class C confinement and Class D precondition observation in your own
trust domain), ADR-0031 Decision 7 (the non-descriptive attestation), and
`AGENTS.md`'s Data Safety Rules. Nothing below overrides them; if this runbook
and an ADR ever disagree, the ADR governs.

## Part 1 — the session, start to finish

### Step 1 — the three preflight answers, and where they come from

`open_presentation_session` takes a `PreflightProbes(backup_inclusion,
content_indexing, clipboard_history)` value. This is not an unimplemented
feature — it is ADR-0047's ratified design (see the amendment, "Class D
precondition observation is owner-held"). **The project observes nothing about
your machine.** There is no probe code anywhere in this repository that
inspects backup state, indexing state, or clipboard software; there never will
be, because boundary enforcement is not authored by the supply chain it
constrains. You determine each answer yourself, by whatever means you trust,
entirely outside this repository, and you hand the result to the script as a
plain value.

Each answer is one of `True` (present), `False` (absent), or left as the
default `ProbeState.UNKNOWN`. The defaults refuse — supplying nothing gets
nothing:

- **`backup_inclusion`** — is the live workspace directory included in any
  backup (Time Machine, a cloud backup agent, anything else that copies it
  off-machine or to another volume)? Only `False` passes; `True` or unknown
  refuses.
- **`content_indexing`** — is the live workspace directory covered by Spotlight
  or any other content indexer that would produce a text-bearing description of
  its contents? Only `False` passes; `True` or unknown refuses.
- **`clipboard_history`** — is any clipboard-history manager running, or is the
  operating system's own clipboard-history feature enabled? `True` refuses.
  `False` passes, but the preflight always attaches an owner-responsibility
  note (`viewing-clipboard-history-undetectable-remainder`) alongside a pass,
  because this check is deliberately partial — the two above are things the
  preflight can always decide; this one is not, and a pass here is not a
  clearance claim. Do not read a pass as "clipboard is safe." Read it as "the
  detectable case was not observed"; the residual is still yours to manage (see
  Step 4).

If any answer refuses, the session does not derive anything, does not open a
socket, and does not launch a browser — the refusal is the first thing that
happens.

### Step 2 — pointing the capability at the real residency

The session needs a `WorkspaceCapability(location=<L>)`, where `<L>` is your
real live workspace. This is the one part of this runbook that required a
judgment call rather than an existing decision, so the reasoning is given in
full below the steps ("Open question: how the locator reaches the script").

**The mechanism adopted here: the script never receives the locator at all —
it derives it from its own position.** You place the Step 3 script *inside*
`<L>` (alongside the `runner.py` your derivation workflow already put there),
and it computes `L = Path(__file__).resolve().parent`. The path is therefore
never typed, never an argument, never an environment variable, and never
written into any file you did not already have.

**The rule that makes this hold — read it before Step 3:**

> **Never invoke the script with a path argument.** Run it as a bare
> `python3 view.py` from a terminal already positioned at `<L>`. Running
> `python3 <L>/view.py`, or any other form that spells the residency path on
> the command line, still *works* — and silently discards the entire
> protection, putting the locator in your shell history and in the process
> table exactly as if the script took it as an argument.

The derivation is a property of where the file sits, not of how you invoke it,
so the safety depends on the invocation form and nothing in the code can check
this for you. Getting a terminal positioned at `<L>` without typing the path is
easiest via your file manager's or editor's "open terminal here" on the
directory you already have open from populating `acts/`. If you must `cd <L>`
by hand, that single `cd` leaves the path in shell history; that residual is
discussed below and is yours to accept or to manage (e.g. by clearing that
history entry) — this runbook does not mechanize either.

### Step 3 — running the session

Copy the template below into a file inside `<L>` (for example `<L>/view.py` —
never inside the repository) and run it with `python3 view.py` from a terminal
already positioned at `<L>` (Step 2). It reuses the exact act-log-reading
pattern your derivation `runner.py` already uses, so nothing new is being
learned:

```python
"""Owner-held live viewing script (lives in L, never in the repository)."""
import json
import sys
from pathlib import Path

REPO = Path("<path to your finances repo checkout>")
sys.path.insert(0, str(REPO))

from packages.derivation.live_session import open_presentation_session, PresentationSessionError
from packages.derivation.live_viewing import PreflightProbes

L = Path(__file__).resolve().parent
acts = [json.loads(p.read_text("utf-8")) for p in sorted((L / "acts").glob("*.json"))]
adoption = next(a for a in acts if a["kind"] == "package-adoption")

from packages.derivation.live_workspace import WorkspaceCapability
from packages.derivation.production_resolver import PublicationSurface

probes = PreflightProbes(
    backup_inclusion=False,       # fill in your own answer, Step 1
    content_indexing=False,       # fill in your own answer, Step 1
    clipboard_history=False,      # fill in your own answer, Step 1
)

try:
    session = open_presentation_session(
        WorkspaceCapability(L),
        probes=probes,
        repo_root=REPO,
        authoritative_acts=acts,
        workspace_revision=len(acts),
        run_scope=adoption["payload"]["scope"],
        scope_user=adoption["actor"],
        request={"schema": "run-request.v1"},
        run_id="view.real.2025.session-1",
        governance_pins=[],
        surface=PublicationSurface(
            REPO / "packages/sample_data/frrs_t3/publication_surface/releases",
            REPO / "packages/content/tax/2025/published-packages.json",
            REPO / "packages/content/tax/2025",
        ),
        output_name="view-session-1.presentation.json",
    )
except PresentationSessionError as refusal:
    print("refused:", refusal.reason, refusal.reason_codes)
    sys.exit(1)

input("session open — press Enter here when you are done looking, to tear down: ")
try:
    session.close()
    print("torn down")
except PresentationSessionError as failed:
    print("teardown did not complete:", failed.reason, failed.reason_codes)
    sys.exit(1)
```

Note what this script is and is not: it is a documentation template, not a
shipped tool. It is the same composition `open_presentation_session` already
performs as one call (capability → preflight → derivation → loopback render →
confined browser → teardown), copied here so you type one command instead of
assembling several. `REPO` is a path to your own checkout, a public fact about
your machine layout, not a residency locator, and is fine to fill in literally.

**Why catching `PresentationSessionError` is sufficient, and why that is a
property of the function rather than of this template.** Every failure this
call can produce — including ones originating in the browser vehicle, which
raise `LiveViewingError`, a *sibling* class rather than a subclass — is
classified into a `PresentationSessionError` with a stable reason code before
it reaches you. That wrapping lives in `open_presentation_session` itself, so
it survives your retyping or adapting this template. If you adapt the script,
you do not need to widen this catch, and you should not narrow it: an
unclassified traceback on screen during the real session is exactly the text
Part 2's vocabulary has no legal way for you to describe.

If the preflight refuses, the script prints a reason code and exits — no
browser opens. The reason codes you may see, and what each means:

| Code | Meaning |
| --- | --- |
| `presentation-preflight-refused` | One or more of the three Step 1 answers refused; the specific sub-codes are listed alongside it (see next block). No derivation, no browser. |
| `viewing-capability-unavailable` | `<L>` could not be reached as a directory — check Step 2. |
| `viewing-residency-backup-present` | `backup_inclusion` was `True`. |
| `viewing-residency-backup-indeterminate` | `backup_inclusion` was left `unknown` or came back unreadable. |
| `viewing-residency-index-present` | `content_indexing` was `True`. |
| `viewing-residency-index-indeterminate` | `content_indexing` was left `unknown` or came back unreadable. |
| `viewing-clipboard-history-present` | `clipboard_history` was `True`. |
| `presentation-live-run-failed` | The derivation step raised; nothing about *what* failed is disclosed here — see the failure vocabulary in Part 2. |
| `presentation-live-run-refused` | The derivation itself refused (a kernel-level refusal, not a preflight one); a reason code accompanies it, none of which is a value or disposition. |
| `presentation-model-unavailable` | A presentation model was expected but not produced, or failed to parse/validate. |
| `presentation-page-unavailable` | The repository's product page could not be read, or did not have the expected single model-assignment site. |
| `presentation-page-declares-provenance` | The page being served declares itself synthetic (this should never happen for the real product page — if it does, stop and report exactly this fact, nothing more). |
| `presentation-server-start-failed` | The loopback server could not start. |
| `presentation-viewing-refused` | The browser vehicle refused. One `viewing-*` sub-code from the next four rows accompanies it and says which. |
| `viewing-browser-not-found` | No Chrome/Chromium executable was found in the standard locations. |
| `viewing-browser-launch-failed` / `viewing-browser-start-timeout` / `viewing-browser-exited-during-launch` | The browser process did not come up cleanly. |
| `viewing-workspace-unreadable` | The vehicle could not read or prepare its confined session directory under `<L>`. |
| `viewing-path-not-confined` / `viewing-navigation-non-loopback` | A Class B destination or a navigation attempt fell outside the confined session — refused by construction. |
| `presentation-viewing-failed` | The browser vehicle failed in a way that carries no classification of its own. Deliberately the only thing you are told: an arbitrary exception's message is exactly the surface ADR-0047's locator confinement keeps closed, so its detail is dropped rather than shown. Report this code; see Part 2. |
| `presentation-session-teardown-failed` / `presentation-server-teardown-failed` / `viewing-browser-teardown-failed` | Teardown (Step 5) did not complete cleanly. |

None of these codes ever carries a path, a value, or a disposition — that is
ADR-0047's locator-confinement decision, and it is why this table is safe to
read in full before you sit down. The table is also **closed for this call
path**: `open_presentation_session` classifies every failure it can produce
into one of these codes, so you should never see a raw Python traceback from
it. If you somehow do, that is itself a legal mechanical statement to report
("the session failed without producing a reason code") and a defect in the
classification, not something to describe your way around.

### Step 4 — obligations during the session

**Read this before you look at anything.** Once the browser is open you are
inside the residency's viewing session, and ADR-0047 preconditions 3 and 4
bind you — these are things you must personally do or refrain from, not
something the code enforces:

- **No copy at all, of anything, for the whole session, if any
  clipboard-history retention is in force** — whether a third-party manager, the
  operating system's own history feature, or anything you could not rule out in
  Step 1's clipboard answer. A clipboard-history feature converts *any* copy
  into a durable record outside the residency, even one you intend to paste
  right back into the same page — there is no "safe" copy under retention,
  because the retention itself is the crossing, independent of what you
  eventually do with the paste.
- No paste of anything from this session into a destination outside the
  residency.
- No print to a networked or external destination.
- No screenshot or screen recording that is retained anywhere.

These are the same four items ADR-0047 preconditions 3 and 4 name, and they are
owner knowledge, not mechanism — nothing in the vehicle can observe or enforce
any of them.

### Step 5 — teardown and confirming it completed

The template above tears down when you press Enter at its prompt:
`session.close()` closes the browser and the loopback server and removes the
session's temporary directory under `<L>`. If `close()` raises
`PresentationSessionError` with reason `presentation-session-teardown-failed`
(or a more specific `..._teardown-failed` code from the table above), teardown
did not complete cleanly — this is itself a legal, mechanical statement to make
per Part 2 below (`"teardown did not complete"`), and it is enough to report on
its own. If `close()` returns without raising, teardown completed: the browser
process is gone and the session's temporary directory under `<L>` no longer
exists — check for the latter yourself if you want a second confirmation, since
it is your own filesystem, not a repository-recorded fact.

## Open question: how the locator reaches the script

The runbook must tell you how to point the capability at `<L>` (Step 2), and
the obvious form — typing the path as a command-line argument — creates two
separate exposures at once: the path lands in your shell history (a durable
file, itself a candidate for backup or sync, i.e. the same Class D hazard the
preflight is trying to keep out of the residency, except now applied to a file
*about* the residency rather than the residency itself), and it appears in the
process table (`ps`) for the lifetime of the process, readable by any other
process running as your user — exactly the Developer/Supply domain ADR-0044
says is not mechanically separated from Live-Run Data. This is the identical
hazard shape that killed the `tmutil isexcluded` probe in the previous
milestone (ADR-0047 amendment): a transient argv disclosure to the one domain
the project cannot wall off.

Three alternatives were evaluated, as the charter asked:

1. **Read the locator from a file the runbook never echoes.** This does not
   close the hazard, it relocates it: the file now durably holds the locator
   somewhere on disk *outside* the residency (the residency cannot be the place
   you keep the file that tells you where the residency is), and that file is
   itself a fresh candidate for backup, sync, or indexing that the Step-1
   preflight has no way to know about or refuse on. It trades a transient
   argv/history exposure for a persistent, unguarded one. Worse in practice,
   not better.
2. **Set it as an environment variable "outside history expansion"** (e.g. a
   leading-space `export` under `HISTCONTROL=ignorespace`/`HIST_IGNORE_SPACE`).
   This depends on shell configuration this runbook cannot verify or enforce,
   and even when configured correctly it only suppresses the *history* copy —
   the value is still inherited by the child process's environment for its
   whole lifetime, and same-UID environment inspection is possible on some
   tool/OS combinations, so it does not obviously close the process-table half
   of the hazard either. A control that silently degrades to "no protection at
   all" when a dotfile is missing is worse than one that is visibly absent.
3. **Prompt for the locator interactively** (`input()` at run time). Better
   than an argument — no argv entry, no history entry — but it still requires
   the value to be *typed*, which puts it in terminal echo and therefore in
   scrollback, and in a session transcript if terminal logging is on. It also
   asks you to retype a path correctly at the start of the one session that
   matters.

**Recommendation and adopted mechanism: none of the three. The script derives
the locator from its own position (`Path(__file__).resolve().parent`, Step 3),
so the locator is never supplied to the script at all.** This dominates all
three alternatives on the exposures they were being judged against: no argv
entry, no shell-history entry, no durable locator-bearing file created for the
purpose, no environment variable, and — unlike the interactive prompt — no
terminal echo and no scrollback copy, because nothing is typed. What remains is
the same same-UID residual ADR-0044 and ADR-0047 already accept everywhere else
in this system: a process that can read this program's memory can read the
resolved path, and the script file itself sits inside `<L>`, which is where
locator-bearing material is supposed to live.

**It is not a closure, and two residuals are named rather than papered over:**

- **The protection is invocation-dependent, not structural.** `python3
  <L>/view.py` produces exactly the argv and history exposure this whole
  section exists to avoid, and the script cannot detect or refuse it — by the
  time it runs, the derivation gives the same answer either way. This is why
  Step 2 states the "never invoke with a path argument" rule as a rule, in the
  place you will read before running anything. A safety property that holds
  only for one invocation form is only as good as the instruction that names
  that form.
- **Getting a terminal to `<L>` may still cost a history entry.** If no GUI
  "open terminal here" is available and you `cd <L>` by hand, the path is in
  shell history exactly as before. The mechanism protects the value the script
  receives; it does not protect every step of getting there.

If a future milestone wants to close this fully, the honest options are
narrower than they look: reading from a file only moves the problem, a
shell-configuration-dependent history suppression is fragile by construction,
and a typed prompt trades argv for scrollback. The remaining residuals above
are invocation discipline and shell behavior, neither of which is closeable by
anything this repository can write. The previous milestone's precedent —
accepting a hazard as a named residual rather than building an imperfect
mechanism to paper over it — is what the two bullets above do deliberately.

## Part 2 — the non-descriptive failure vocabulary

This exists because ADR-0047 precondition 5 forbids values, identifiers,
dispositions, and screenshots from chat, reviews, PRs, and the repository — so
**a defect seen during the real session is, by default, unactionable.** This
vocabulary is the only legal channel from a failed real session back to a
repair. It is a data-safety artifact, reviewed as one, not documentation to be
tightened for clarity later.

### The governing line: mechanical, never evaluative

A statement is **legal** if it names only that some observable, structural
event did or did not occur — the page loaded or it did not, a section rendered
or it did not, a link resolved or it did not, a process exited or it did not.
A statement is **illegal** the moment it also carries a judgment about
*correctness*: that something differed from what it should have been, that a
count was wrong, that a value looked off, that a disposition was surprising.

The test to apply to any candidate sentence: **could this sentence be true
regardless of what the correct output actually was?** If yes, it is
mechanical — it describes a structural fact about the session's execution, not
its content. If the sentence's truth depends on knowing what *should* have
happened, it is evaluative, and evaluative is a disposition claim no matter how
neutral its wording sounds.

This is why "a section rendered empty" is legal (true or false independent of
what belongs in that section) while "a section rendered empty that should not
have" is illegal (its truth depends on what should have been there — the
judgment is smuggled into "should not have," not removed by the rest of the
sentence being neutral). The same test catches quieter smugglers:

- "the numbers looked wrong" — illegal (evaluative; also arguably names a
  value's disposition).
- "a section rendered empty" — legal (mechanical; true independent of
  expectation).
- "a citation link resolved to nothing" — legal (mechanical: it either
  resolved or it did not).
- "a citation link resolved to the wrong target" — illegal ("wrong" requires
  knowing the right one).
- "the browser exited before I could look" — legal (a structural event: exit
  before observation).
- "teardown did not complete" — legal (mechanical, matches Step 5 above).

**Counts, and the test that actually governs them.** The question for a count
is not whether it is a number, and not whether it *could* be compared against
an expectation — it is **whether the set being counted is already public in
the repository.**

- "three W-2 slips rendered" — illegal. The number of your W-2s is a
  cardinality of your real fact set. Nothing public bounds it, so the count is
  live content stated numerically.
- "nine sections rendered" — legal but pointless, and best avoided. The page's
  section set is fixed repository content — the same nine 1040 lines pinned in
  `tools/presentation_harness/examples/manifests/citation-walk-production-shaped.v1.json`
  — so this number is already public and reveals nothing about you. It leaks
  rendering mechanics, not tax values. Saying "not every section rendered"
  instead is **not** safer: it conveys nearly the same bound against the same
  public set. Prefer "a section failed to render" because it is the fact you
  actually want repaired, not because the count was dangerous.

The rule to carry away: **never state a count over a set whose size is not
already fixed and public in the repository.** Sections, refusal reason codes,
and form lines are public sets. Slips, payers, statements, entities, and
anything else that exists because your documents exist are not.

**Refusal reason codes.** "A refusal came back with reason code X" is legal for
any `X` in the Step 3 table, and for the sub-codes `presentation-live-run-refused`
carries. The basis, since this is a categorical-sounding claim: the Step 3
codes are the closed `ViewingReason` enumeration in
`packages/derivation/live_viewing.py` plus the `presentation-*` literals in
`packages/derivation/live_session.py`, all of them fixed strings chosen at
authoring time with no interpolation, and ADR-0047's locator-confinement
decision is what keeps them that way. The `presentation-live-run-refused`
sub-codes come from `production_resolver.py`'s `Refusal` codes
(`ADOPTION_AMBIGUOUS`, `HARD_GATE_REFUSED`, and siblings), which were traced
forward and describe package and governance validation state — not taxpayer
values.

That audit covers the codes reachable from this call path as of this writing.
It is **not** a standing guarantee that any string a future code path calls a
"reason code" is safe. If you see a code that is not in the Step 3 table and
not one of the audited sub-codes, report it as *an unenumerated code was
returned* rather than quoting it — a code no one has audited is exactly the
kind of thing that could carry interpolated detail, and quoting it first and
checking afterwards is the wrong order for an unrepeatable session.

### When nothing in the vocabulary fits

**First, report that fact itself.** "What I saw does not match anything in the
runbook's vocabulary" is a true, mechanical, legal statement on its own, and it
is the correct thing to say — not an invitation to improvise a closer-fitting
description. Improvising is exactly the failure mode this vocabulary exists to
prevent: the temptation, when nothing fits cleanly, is to reach for "the
closest true description," and the closest true description of a real defect
is very often evaluative by the time it is specific enough to be useful. Report
the gap, not a workaround for it.

**Then reproduce it synthetically, where description is fully legal.** Reporting
the gap alone would leave a novel failure detectable but not diagnosable — the
project would know to stop trusting the session and still be unable to repair
anything. It does not have to end there. The rehearsal path already exists: run
the same session against a **synthetic** workspace, the way Track 2 of the
milestone that produced this runbook does, and see whether the same failure
appears. A failure observed against synthetic facts is not your data, so
ADR-0047 precondition 5 does not reach it — **describe it in full, without
restriction**, including values, dispositions, screenshots, and anything else
that would be forbidden about the real session. That description is an ordinary
bug report and a repair follows from it normally.

**Be clear about what this does not cover.** Reproduction only helps for
failures whose cause is in the code, the page, or the shape of the model. A
failure that manifests *only* against your real content — a fact pattern the
synthetic set does not produce, a value shape nothing generated hits, an
interaction between real entities that no fixture models — will not reproduce,
and for that class the escape hatch genuinely does not open. What remains legal
there is still only the gap report. This is a real limit; do not treat "try it
synthetically" as if it always works.

A repair to the vocabulary itself — adding a new legal entry — is then a
repository change like any other, made without reference to what you actually
saw in the real session, reviewed on the same mechanical-vs.-evaluative line as
everything above.

### What this vocabulary cannot cleanly express, named rather than resolved

- **Frequency and pattern.** The vocabulary can say a section failed to render
  once; it has no legal way to say it happened on every attempt versus one
  attempt, because "every attempt" is a count across sessions and inherits the
  same disposition-in-numeric-clothing problem a single count does. Whether
  repetition is itself safe to report is left open here rather than decided.
- **Ordering and co-occurrence.** "The page did not load" and "the browser
  exited before I could look" are both legal individually; whether they
  happened together, or in what order, edges toward describing the shape of a
  specific failure rather than a category of one. This runbook does not settle
  where that edge is, beyond noting the same true-independent-of-expectation
  test applies.
- **A structural event with no entry above.** The table in Step 3 and the
  examples here are not claimed to be exhaustive of every possible mechanical
  event a real browser session could produce. The "report the gap" instruction
  plus synthetic reproduction is the vocabulary's designed answer to this, but
  reproduction fails for anything that only manifests against real content, so
  this remains a real limit rather than a closed one.
- **A defect that only appears against real content.** Named again here because
  it is the sharpest gap in the whole design: such a defect is legally
  reportable only as its mechanical shell, cannot be reproduced where
  description would be free, and therefore may be repairable only by reasoning
  about the code rather than about the observation. Nothing in this runbook
  closes that.

## Verification note

This runbook's Step 3 guarantee — that every failure arrives pre-classified as
a stable reason code — is a property of `open_presentation_session`, not of the
template, and is covered by regression tests in
`tests/test_presentation_live_session.py`. The commands that verify nothing
else broke are listed in the milestone charter's Verification section and were
run for this track and its repair.
