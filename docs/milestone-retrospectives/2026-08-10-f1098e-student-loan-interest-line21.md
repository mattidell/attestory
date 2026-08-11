# Retrospective — 2025 Form 1098-E Student-Loan Interest through Schedule 1 Line 21 and Form 1040 AGI

**Outcome: stopped at design.** The stop condition fired. No implementation was
chartered, no code was written, no schema, rule, package, registry, attachment,
or form-field version number was allocated. The owner ruled the branch
**completed design exploration**, blocked behind a prerequisite milestone.

This is a retrospective on a milestone that did not ship, and the point of
writing it is that the milestone produced real value anyway — in the plan's
non-chronological **Durable findings register**, which is what a re-cut inherits.

## What differed from the plan

- **Track 0 was declared settled and was not.** Owner review returned three
  findings, two at P1, all accepted. Two of the three were **already written
  down in the settlement itself** as "open items carried out of Track 0". The
  defect was not analysis; it was that a recorded semantic coupling was treated
  as a disclosure rather than as an unfinished decision.
- **The charter bounded the milestone in tax-domain language, which cannot
  express reach.** "Form 1098-E → line 21 → AGI" is a complete statement of what
  was being built and says nothing about what it would touch. Every surprise came
  from that gap: sixteen fact types needing re-keying, AGI availability changing
  for returns with no student loans, and shared vocabulary with a just-merged
  milestone. The one reach question the charter *did* ask — "what substrate does
  the engine lack?" — found the missing `multiply`/`divide` before a line was
  written and never surprised the milestone again.
- **The stop condition fired on a dependency nobody had scoped:** the twelve
  Schedule 1 absence propositions the student-loan MAGI base needs already exist,
  but declare Social Security Benefits Worksheet scope in their own titles.
  Reuse fails the claim-reuse test on declared authority scope. Repairing it
  requires a capability the engine does not have.
- **The foreman twice priced a repair on an unverified mechanism.** The first
  time (horizon re-keying) a builder checked and the mechanism was real, so the
  pricing survived by luck. The second time (fact-type succession) it was not:
  `apply_bundle_adoption` (`packages/kernel/facts.py:84-101`) has no deletion
  path, `compute_currency` (`packages/kernel/currency.py:137-174`) admits only
  same-fact correction, member withdrawal, and superseded entities as
  displacement roots, and `supersession: {"policy": "free"}`
  (`packages/kernel/findings.py:556-576`) fires only on the same `fact_id`.
  **The owner disposition that approved "may be superseded by" named a
  capability that does not exist, and the foreman supplied that premise.**
- **The proposed workaround repeated the original defect by a second route.**
  Re-declaring the same twelve identifiers in a successor bundle with neutral
  wording is mechanically permitted — 29 fact-type ids are already declared in
  more than one bundle — but would cause existing findings to be treated as
  answers to a **broader question than the taxpayer asserted**. The W-2 and
  1099-DIV precedents are inapposite: those successions preserved meaning. The
  foreman verified the mechanism before proposing it, having been burned on
  exactly that, and still failed to ask the prior question of whether widening a
  declaration is semantically admissible at all.
- **Three agent units exhausted context or hit a session limit mid-work.** The
  unit that committed per work item preserved four of five items; the units that
  batched lost everything. Per-item commit discipline was made mandatory and the
  remaining units carried the dying agents' last observations forward as leads.
- **The cited federal sources were never in the repository.** Every unit
  re-obtained `p970-2025.pdf` and `i1040gi-2025.pdf` into an ephemeral scratchpad.
  Five load-bearing citations were spot-checked against fresh 2025 editions and
  **all five verified at the cited page**, so this is an availability and
  reproducibility defect, not an evidence-integrity one — but the milestone's
  reasoning is not reproducible from the repo alone.

## What the milestone produced

The **Durable findings register** in
`docs/phases/engine-breadth/milestones/f1098e-student-loan-interest-line21.md`,
which is the artifact a re-cut inherits. It carries, each with the location where
it was verified: substrate facts about the kernel and evaluator; settled
tax-domain results (identity, the seventeen-component eligibility boundary, the
legal-zero-versus-block test, the no-cycle proof, the reported-interest
boundary); standing defects on the ratified line; and method results.

Two defects it surfaced on the **already-ratified** line are worth naming here,
because they are independent of this milestone:

- **`rule.form1040-line9.v7` unconditionally requires
  `tax.us.2025.social-security.line6b`** (`"when": true`), and the SSA worksheet
  is that symbol's only producer corpus-wide. Every return reaching line 9 must
  satisfy all **33** SSA scope declarations whether or not it has any Social
  Security source. The owner directed that this **is not a precedent** and that
  the prerequisite must repair it.
- **A settled T0-4 claim was false**: that every component finding is pinned
  whatever its value. `all` short-circuits (`evaluator.py:173-174`) and pins
  derive from `AccessLog.refs` (`runner.py:343-359`), so components after the
  first `no` were never pinned — the engine would have named one missing answer
  and stayed silent about the rest.

## What changes as a result

- **Five milestone entry questions**, answered before a charter is written and
  carried in it. They are stated in the plan's Durable findings register. The
  operative one is question 1: what will be **modified in place while already
  merged** — a bucket that is empty by default and requires an explicit owner
  decision to fill.
- **"Recorded" is not "settled."** A track may not be marked settled while it
  contains a known semantic coupling unless the plan carries a counterexample
  showing the coupling is correct.
- **Verifying a mechanism is necessary and not sufficient.** Ask whether an
  operation is semantically admissible before asking whether the engine permits
  it. Mechanical permission is not authority over meaning.
- **An allowed-impact envelope gates implementation**, stated explicitly before a
  build track is chartered. It is the same instrument as the entry gate, applied
  at the other end of the milestone.
- **Commit per work item**, not per unit.

## Follow-on

**Blocking prerequisite (unplanned):** a **fact-type succession and
optional-route applicability** milestone, framed as succession rather than
deletion or retirement — history must remain. Its five items are stated in the
plan under "The prerequisite is succession, not deletion", and item 5 requires an
implementation-and-governance cost inventory **before** the build is chartered;
if generic substrate is needed, it is owned openly as that milestone's
architectural decision rather than hidden inside a tax milestone.

**Deferred, not forced by the prerequisite:** the identical consumer-scoped-title
defect in `schedule1-part1-scope.bundle.json`; the `attachment-rule.v5`
provenance defect; durable availability of cited federal sources against
ADR-0031's residency boundary.

**Re-cut:** after the prerequisite merges, prepare a concise handoff and re-cut
1098-E from current `main`, scoped to the first dependency-safe Schedule 1
Part II → Form 1040 AGI vertical slice. The chronological Track 0a/0b/0c
narrative is not carried forward.
