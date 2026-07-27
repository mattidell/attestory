# Plain-Language Analysis — Live Viewing Environment

Companion to [ADR-0047](../0047-live-viewing-environment.md). The ADR is the
authoritative record.

## What changes

Until now, every security decision in this project has been about programs. The
trust domains in ADR-0044 describe what code may reach what data. The residency
boundary in ADR-0031 describes what bytes may cross which line.

Presentation breaks that pattern, because its entire point is to show real tax
content to a person. This ADR defines what that viewing session is, sorts every
way information can leave it into four classes, and says plainly which classes
the project controls and which it does not.

## Why it is needed

The obvious plan was "build a contained browser." That plan was rejected before
anything was built, because it would have failed for a reason already on record.

Chrome accepts command-line switches that turn off syncing, background network
traffic, and extensions. It is tempting to call that containment. It is not.
Those switches are Chrome agreeing to behave, inside a program running with the
owner's own permissions. Any program running as the owner can ignore them. The
project already learned this the expensive way in the Guarded Transport
milestone, where a file locked to "owner only" turned out to be readable by
every other program running as the owner — a fact visible from first principles,
discovered only after a prototype and a review.

On macOS there is no way to give one process its own network boundary without
administrator control. So this project cannot build a wall there, and this ADR
says so instead of implying otherwise.

## The narrowing that makes it workable

Two different maturity claims were being confused.

- **L4** — the strongest claim — requires that a hostile program running as the
  owner still cannot reach live data. That needs real isolation, and ADR-0044
  already assigns it to a separate future milestone.
- **L3** — the claim Presentation is reaching for — means the capability
  actually operated on real data with the boundary intact. Every existing L3 in
  this project rests on thorough synthetic testing plus the owner's brief
  attestation that a real run happened safely, under a posture aimed at
  *accidents*, not attackers.

Presentation gets the same deal the W-2, interest, and dividend work got. So the
real question is not "can the browser be caged" but "what can the owner
truthfully say afterwards, and what has to be true of the machine for that to be
honest?"

## The four classes

**Class A — things a person can just do.** Copy and paste, print, save a file
somewhere else, take a screenshot. If someone can read a number on screen, they
can write it down. This is inseparable from having a human surface at all, and
ADR-0044 already treats deliberate owner action as an accepted residual. The
project does not pretend to control it.

**Class B — things the vehicle picks.** Where the browser stores its profile,
cache, autofill data, downloads, and printed files. These are just directories,
and the vehicle chooses them. They go inside the quarantined workspace, and the
browser refuses to start if any of them would land outside it. This is the
project's actual mechanical obligation, and it is met by construction rather
than by trusting the browser.

**Class C — network access.** The vehicle blocks navigation to anything but the
local machine and turns off background traffic. Helpful against accidents;
useless against a determined program. The ADR forbids anyone — including future
code comments and test names — from describing this as prevention.

**Class D — facts about the Mac.** Is the workspace being backed up? Is its text
being indexed for search? Is sync software covering it? Is screen-recording
software running?

Class D is the part the original plan would have missed, and two of them are
quietly fatal. If the workspace is content-indexed, a searchable copy of the
text already exists outside the workspace. If it is backed up, a durable copy
already exists outside it — possibly on a network drive. In both cases the leak
has already happened, before the browser ever opens.

## The judgment call

Those two conditions could have been handled two ways: refuse to run, or run
anyway and mention it in the attestation.

The ADR chooses **refuse**. The reasoning is that these are not risks to
disclose — they are crossings that already completed. The owner cannot honestly
say "no artifact crossed" while a search index describing the run sits outside
quarantine. The cost of refusing is that the owner excludes the workspace from
backup and from indexing once, which is a small, one-time chore. The residency
boundary already treats uncertainty as rejection, and this follows the same rule.

## What the owner is actually promising

The attestation itself does not change — the owner ran it, saw the results in
quarantine, nothing crossed. What changes is that the ADR now lists the five
things that have to be true for that sentence to be honest, including two that
are owner knowledge rather than machine checks: that no copy-paste or printout
left quarantine, and that no unobservable sync or recording software was
running.

This is the first place in the project where a security claim depends partly on
what the owner did rather than entirely on what the code enforces. That is
recorded as a property of human-facing surfaces, not as a loosening of the rules.

## One small but important rule

Error messages may not contain the workspace path. The natural way to write a
"that path is outside the workspace" check is to print the offending path — and
that message would itself be a leak, into a log, a test failure, or a bug
report. So the vehicle reports coded reasons instead. A constraint on what the
project is allowed to know shapes what its diagnostics are allowed to say.

## What this does not do

It implements nothing, lifts no maturity level, and chooses no isolation
mechanism. Presentation stays at L2 and the data boundary stays at L3. It makes
a viewing session *decidable*, so the next track can build against a stated bar
and a reviewer has something concrete to check.
