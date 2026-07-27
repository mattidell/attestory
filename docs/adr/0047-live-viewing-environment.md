# ADR 0047 — Live Viewing Environment

- Status: **accepted** (Track 1 of Presentation — Live Viewing Boundary and
  Invocation Vehicle; owner ratification 2026-07-26 by merge of the Track 1 PR).
  Independent decision review `b1a630a` returned `NOT READY` on one blocking
  finding (clipboard-history retention unclassified) plus one non-blocking
  observation (Class C overstated platform impossibility). Repair `52ef7b0`
  closed both; recheck `a476c40` returned `NOT READY` on one stale
  cross-reference; repair `08eecb6` closed it and second recheck `63c4102`
  returned `READY`.
- Tier: 3
- Date: 2026-07-26
- Plain-language analysis:
  [0047-live-viewing-environment.md](analyses/0047-live-viewing-environment.md)

## Context — a human is not a process

ADR-0044 defines four trust domains and the crossings between them. Every
authority it describes belongs to a *process*: Developer/Supply builds and
publishes, Live-Run Data consults and changes authoritative live state, and
Owner Authorization grants particular acts. Its threat posture is stated against
"an unprivileged Developer/Supply authority, including malicious developer-side
code."

Presentation introduces a channel none of that contemplates. The whole purpose
of a form-field surface is to put real, resolved tax content **in front of a
person's eyes**, on a general-purpose desktop, in a browser the project does not
write. ADR-0031 governs where live bytes live and what may cross; ADR-0046
governs what the surface may render and on whose authority. Neither answers what
the *viewing session itself* is, which of its channels the project claims to
control, or what the owner would truthfully be attesting to afterwards.

The active milestone plan authorizes this direct system-definition ADR from
accepted decisions and completed records, following ADR-0044's own precedent. It
selects no enforcement substrate and lifts no maturity row.

### What the boundary check established before this decision

The milestone was selected with the obvious shape — build a contained headed
browser vehicle — and the owner directed a first-principles check before any
charter, explicitly to avoid repeating the Guarded Transport milestone. That
check rejected the shape:

- Chrome's `--disable-background-networking`, `--disable-sync`,
  `--disable-extensions`, and `--user-data-dir` are **cooperative settings**
  inside a process running under the owner's own authority. ADR-0044 already
  holds that naming directories and wrapping commands does not create a trust
  boundary; the Guarded Transport records establish the same failure mode for a
  mode-600 store readable by a same-UID process.
- macOS exposes no per-process network boundary without root or a third-party
  control. No vehicle this project writes can mechanically prevent a same-UID
  headed browser from reaching the network.

That is a real limit, and this ADR records it as one. It is narrower than it
first appears, because mechanical authority separation is the gate for a
**data-boundary L4** claim (ADR-0044, "future implementation gate"), whereas
Presentation **L3** rests — like every existing L3, per maturity-matrix
footnote 7 — on the in-repo synthetic battery plus the owner's non-descriptive
attestation, under a posture explicitly scoped to accidental leakage rather than
a malicious same-UID process.

The open question is therefore not containment. It is **honesty**: what can the
owner truthfully attest after looking at real output, and what must be true of
the machine for that attestation to hold?

## Decision — the viewing session

A **live viewing session** is a bounded activity **within** the Live-Run Data
domain in which the owner observes live-derived presentation output through a
browser the project invokes. It introduces a human consumer, not a new trust
domain and not a new authority. It is initiated by an Owner Authorization act,
consumes only material already inside the residency, and holds no publication
credential or path.

A viewing session is **not** a crossing. Nothing leaves quarantine by virtue of
being displayed. What the owner subsequently does with what they have seen is
governed by the residual below.

## Decision — total channel classification

Every channel of a viewing session classifies into exactly one of four classes.
The classification is **total**: a channel that is unrecognized, newly
introduced by a browser version, or otherwise unclassified is treated as
boundary-relevant and blocks the session. There is no unclassified remainder and
no advisory class.

### Class A — Named residual (owner-authorized elevation)

Copy and paste, including any system-wide or cross-device pasteboard; the print
dialog and any destination it reaches; save-as and downloads directed outside
the residency by owner action; the share sheet; and screenshots or screen
recording initiated by the owner.

These are **not defects the vehicle introduces**. A person who can read a value
can transcribe it, and ADR-0044 already names owner-authorized elevation across
domains as an explicit residual. Any surface capable of showing live data to a
human carries this class irreducibly; refusing it would refuse Presentation
itself.

The project claims no control here and must not imply otherwise.

**Class A is bounded to the deliberate, one-shot act itself.** It covers the
owner choosing to move a value to a destination they intend. It does **not**
cover background software that silently retains the act — a clipboard-history
manager, or an operating-system clipboard-history feature, converts *any* copy
into a durable record outside the residency without further owner action, even
a copy the owner intends to paste straight back inside the same session with no
external destination in mind. That retention is a workstation property, not an
owner act, and classifies under Class D.

### Class B — Boundary-relevant and controlled

The browser user-data directory, cache, session-restore state, autofill and
form-history stores, the downloads directory default, and the print-to-file
destination default.

These resolve to filesystem paths the invoking vehicle chooses. They belong
inside the residency, constructed from the runtime capability, canonicalized,
and refused if they resolve outside it — including through a symlink. This class
is where the project's mechanical obligation actually lies, and it is
discharged by construction rather than by browser cooperation.

### Class C — Boundary-relevant and not closeable by the vehicle

Non-loopback network egress by the browser process.

The vehicle refuses non-loopback navigation and suppresses background
networking. Both measures are **cooperative**. They reduce accidental traffic;
they do not prevent a same-UID process from reaching the network, and they are
not a Live-Run Data privacy wall.

No artifact of this project — code, comment, test name, review, record, or
maturity claim — may describe this class as prevention. Closing it requires an
enforcement substrate, which ADR-0044 routes to a separate future milestone.
This ADR selects and evaluates none.

**This class is open because nothing is selected, not because nothing exists.**
No per-process network confinement has been chosen, prototyped, or verified for
this project, and this ADR asserts no platform impossibility. In particular, the
base-system Seatbelt facility (`sandbox-exec`, and the sandbox-profile mechanism
Chrome already uses for its own renderer processes) is invocable by an
unprivileged user against a process that user owns, and is **unevaluated** here
— neither foreclosed nor endorsed. A later milestone selecting an enforcement
substrate should treat it as a live candidate rather than read this ADR as
having ruled it out. What the Guarded Transport records establish, and all this
ADR relies on, is narrower: a *cooperative* same-UID mechanism is not a trust
boundary, so a flag-configured browser cannot be one.

### Class D — Workstation precondition

Backup of the residency; content indexing of the residency; **clipboard-history
retention**, whether by a third-party clipboard manager or an operating-system
clipboard-history feature; third-party synchronization software covering the
residency; and third-party screen-capture or screen-recording software holding
the relevant system permission.

These are properties of the owner's machine, not of the vehicle. They are the
class a vehicle-first milestone would have missed, and the first three are
**silently fatal**: a content-indexed residency has already produced a
text-bearing description of live data stored outside the residency; a backed-up
residency has already produced a durable copy of live data outside it; and a
running clipboard-history manager converts the owner's next copy — including a
copy intended only to be pasted back inside the same session — into a retained
record outside the residency, which several shipping products then synchronize
to other devices. ADR-0031 Decision 7 classifies all three `NEVER_CROSSES` by
description or by provenance. None is visible from inside the browser, and no
confinement work addresses any of them.

Clipboard-history retention is filed here, not under Class A, because the
crossing is caused by background software rather than by the owner's act. Class
A's residual is the owner deliberately moving a value to a destination they
intend; clipboard history removes the "destination they intend" and the
"deliberately" alike.

The vehicle observes what it can and refuses fail-closed. What it cannot observe
is recorded below as an owner responsibility.

## Decision — precondition disposition

**Residency backup inclusion and residency content indexing are refusals, not
warnings.** The preflight refuses the session; the owner's remedy is to exclude
the residency from backup and from content indexing, once, and the session then
proceeds.

The alternative — permit the session and fold the exposure into the attestation
— is rejected. A durable copy or a text-bearing index of live data outside the
residency is a completed crossing, not a risk to be acknowledged; ADR-0031
Decision 2 makes uncertainty a rejection rather than a third outcome, and an
owner cannot honestly attest that no artifact crossed when an index describing
the run already exists outside quarantine. The workflow cost is a one-time
exclusion, which does not justify blurring the boundary (ADR-0044, operational
consequences).

**Clipboard-history retention is a refusal where detectable and a named owner
responsibility where not.** Where the preflight can observe it — a running
process matching a known clipboard-manager set, or the operating system's own
clipboard-history feature being enabled — it refuses, on the same reasoning as
indexing and backup. Where it cannot, the owner is responsible for quitting or
disabling such software before a session, and this is condition 4's business
rather than mechanism. That partial detectability is why clipboard history is
listed separately from the two conditions the preflight must always be able to
decide.

Preconditions the preflight **cannot** reliably observe — third-party sync
software, screen-recording permission grants, undetectable clipboard managers,
and equivalents — are owner responsibilities, enumerated here as named limits
rather than silently omitted. They do not block the session mechanically.

## Decision — the attestation and its preconditions

The sole repository-eligible statement about a viewing session remains
ADR-0031 Decision 7's non-descriptive attestation, unchanged in shape: that the
owner performed the session, observed dispositions in quarantine, and that no
artifact crossed.

That attestation is honest only when all of the following hold:

1. the preflight passed, so the residency was neither backed up nor content
   indexed at session time;
2. the vehicle's Class B destinations resolved inside the residency and no
   escape was refused-then-overridden;
3. the owner performed no Class A elevation whose result left quarantine — no
   paste into a document outside the residency, no print to a networked or
   external destination, no screenshot retained outside it — **and no copy was
   performed while clipboard-history retention was in force**, since a retained
   copy leaves the residency without any subsequent paste;
4. no Class D condition the preflight cannot observe was in force to the owner's
   knowledge, including undetectable clipboard-history, synchronization, or
   screen-recording software; and
5. no descriptive detail of the session — values, identifiers, dispositions,
   screenshots, or the residency locator — appears in the repository, a review,
   a pull request, chat, or a retrospective.

Conditions 3 and 4 are owner knowledge, not mechanism. This ADR states them so
that the attestation names something specific rather than a general feeling of
care.

## Decision — locator confinement in diagnostics

A viewing session's preflight, vehicle, and failure paths emit **stable reason
codes**, never paths. The residency locator, any fragment of it, any
canonicalized form, and any derived identifier are absent from logs, error
messages, exception text, test output, and review records, per ADR-0031
Decision 4 and its Decision 5 screen.

This is stated as a decision rather than left to implementation because the
natural implementation of a path-confinement check is to report the offending
path, and that report would itself be a crossing.

## Threat posture and residuals

This ADR does **not** claim that a viewing session is protected against
malicious same-UID code. Class C remains open, no substrate having been selected
or evaluated, and ADR-0044's statement stands: until an implementation creates
and verifies authority separation, same-UID code that can exercise the owner's
live-data capabilities is inside the same effective trust domain.

What it does claim is that the accidental-leakage posture is coherent for a
human surface: the controllable channels are controlled by construction; of the
three silently fatal machine conditions, the two the preflight can always decide
— backup inclusion and content indexing — are refused unconditionally, and
clipboard-history retention is refused where detectable and named as an owner
responsibility where it is not; the irreducible human channels are named as
residuals rather than hidden; and the attestation enumerates what it rests on.

Explicit residuals:

- every Class A channel;
- Class C non-loopback egress by a same-UID process, no confinement substrate
  having been selected or evaluated;
- Class D conditions the preflight cannot observe, including clipboard-history
  retention by software it cannot enumerate;
- administrator, root, hypervisor, or physical-device control; and
- ADR-0044's existing residuals, unchanged.

## Consequences

- The Presentation row remains **L2** and the data-boundary row remains **L3**.
  This ADR makes a viewing session decidable; it implements nothing.
- A later Presentation L3 milestone has a stated bar: the vehicle satisfies
  Class B, the preflight refuses on the observable Class D conditions, and the
  owner performs one session and records only the attestation whose five
  conditions are enumerated above.
- ADR-0044's future implementation gate is unchanged and unscheduled. Closing
  Class C remains its business, not Presentation's.
- Presentation is now the project's first surface whose security claim depends
  partly on owner conduct rather than entirely on mechanism. That is recorded as
  a property of human surfaces, not a weakening of ADR-0031.

## Alternatives considered

- **Treat browser flags as containment and build the vehicle first.** Rejected;
  this is the Guarded Transport failure mode and ADR-0044 already forecloses it.
- **Headless-render to a file inside the residency instead of headed viewing.**
  Rejected as the target. It narrows Class A only until the owner opens the
  file, moving the same residual to an unspecified viewer while leaving the L3
  question unanswered — and it builds the vehicle twice. Retained as an
  available fallback if a later milestone finds headed invocation unworkable.
- **Permit a backed-up or indexed residency and disclose it in the
  attestation.** Rejected; see precedent disposition. A completed crossing is
  not a disclosable risk.
- **Define a fifth "Viewing" trust domain.** Rejected: a viewing session
  exercises Live-Run Data authority and creates no new one. A domain that adds
  no authority adds only vocabulary.
- **Select an enforcement substrate here to close Class C.** Deferred, exactly
  as ADR-0044 defers it. Each candidate carries platform, workflow, and
  enforcement questions belonging to a bounded implementation milestone.

## Links and evidence limits

- No real workspace, residency locator, browser profile, backup configuration,
  indexing state, credential, remote, live run, or owner attestation was
  consulted for this decision.
- The Class C conclusion rests on the Guarded Transport records and on the
  absence of a per-process network boundary on the platform, not on a new
  experiment. It does not claim a general impossibility across isolation
  substrates.
- Class B is a design obligation stated here and discharged in Track 2. This ADR
  provides no implementation evidence.

Direct records:

- Milestone plan:
  `docs/phases/real-return/milestones/presentation-live-viewing-boundary.md`
- Trust domains: `docs/adr/0044-live-run-system-boundary-and-trust-domains.md`
- Residency boundary: `docs/adr/0031-real-data-residency-boundary.md`
- Presentation surface contract: `docs/adr/0046-presentation-surface-contract.md`
- Guarded Transport triage: `docs/prototypes/guarded-transport/round-1-triage.md`
  and `docs/prototypes/guarded-transport/repair1-triage.md`
- Existing launch posture: `tools/presentation_harness/lib/chrome.mjs`
- Governance: Constitution Article 18; Ontology §8; Engineering Constraints
  E18.1 and E18.2
