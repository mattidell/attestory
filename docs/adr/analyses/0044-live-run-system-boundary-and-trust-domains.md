# Plain-Language Analysis — Live-Run System Boundary and Trust Domains

Companion to
[ADR-0044](../0044-live-run-system-boundary-and-trust-domains.md). The ADR is
the authoritative record.

## What changes

The project stops treating “the repository running under the developer's user
account” as the natural security boundary. That is how development happens
today, but it is not the system shape the privacy claim should depend on.

The ADR instead names four trust domains:

- **Developer/Supply** builds and publishes software and synthetic material but
  has no standing access to real data.
- **Publication** holds only material safe to treat as public.
- **Live-Run Data** holds the real workspace and runs the adopted package but
  cannot publish source.
- **Owner Authorization** is the owner's deliberate permission to choose a
  residency, contribute facts, adopt a package, or run the application.

These are logical boundaries first. A later milestone will decide whether they
are enforced with a separate OS user, container, VM, or another mechanism.

## Why it is needed

The earlier security work bundled two different concerns together:

1. preventing personal material from being published accidentally; and
2. preventing malicious code running with developer authority from reading
   personal material at all.

Commit hooks, push hooks, classifiers, and a careful wrapper help with the first
problem. They cannot solve the second problem while the same effective identity
can read both the real workspace and the publication credential.

The stopped guarded-transport prototype provided useful narrow evidence. A
mode-600 file did not hide a synthetic credential from another same-UID
process, and the attempted pipe-release design never completed a reproducible
successful Git transport under independent review. That is enough to reject
those two tested shapes. It is not evidence that all local isolation is
impossible.

## What crosses the boundaries

Developer/Supply may send only publication-eligible material to Publication.
Publication may supply Live-Run Data only with the package the owner adopted,
verified byte-for-byte through its release chain. The owner deliberately
authorizes live operations.

Nothing describing a live run comes back out. The existing three-part,
non-descriptive statement remains the only allowed record: the run happened,
the owner observed its dispositions inside quarantine, and no artifact crossed.

## What it protects

Once mechanically enforced, malicious or compromised developer-side code should
be able to use ordinary development and publication capabilities without being
able to read the live workspace. Accidental-leakage controls remain useful now:
classification still fails closed, personal locators stay out of the
repository, synthetic fixtures remain independently constructed, and envelope
scans run when their hooks are invoked.

The important change is honesty about which protection comes from which
boundary.

## Where guarded transport belongs

Guarded transport is still valuable, but it protects the crossing from
Developer/Supply to Publication. It is about ensuring the outgoing envelope is
checked before a publication credential can send it.

It is not the wall around Live-Run Data. The present hooks are conditional:
the synthetic posture audit proves a hooked marker is rejected and also proves
that `git push --no-verify` can bypass the pre-push hook. Credential confinement
therefore remains unestablished.

## What it does not do

This ADR does not install a separate UID, container, VM, credential store,
proxy, or hosted gate. It does not claim the current same-UID workflow resists
malicious code. It does not make an adopted malicious release safe, and it does
not claim protection against owner-authorized elevation or administrator/root
control.

It also does not use real data or require another real run. The data-boundary
maturity level stays L3.

## What happens next

A later implementation milestone selects one enforcement mechanism and tests
the things that are actually uncertain about it: whether the host enforces the
declared authorities, whether the everyday workflow is acceptable, whether
Developer/Supply truly cannot reach the live workspace, and whether Live-Run
Data truly cannot publish.

Only after those checks and the required owner-run verification can the
data-boundary row move to L4.
