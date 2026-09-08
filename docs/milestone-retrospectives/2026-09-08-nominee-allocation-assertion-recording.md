# Retrospective — Nominee Allocation Assertion Recording

Closed 2026-09-08; owner-directed repairs 2026-09-08. The first production
stage of nominee-interest support: the application can record, correct, retract
from current use, and assert again the ordinary statement that a stated amount
of interest reported on an identified Form 1099-INT is allocated to a named
other person — and recover current allocations and historical retracted
assertions (what was said, who said it, and who later ended current support),
with attribution, from a committed act log alone.

Three tracks; Tracks 1 and 2 were each independently reviewed READY, and
Track 0 was closed by the Foreman on executed evidence rather than by an
independent reviewer. No nominee tax consequence, no
line-2b or Schedule B change, no information-reporting implementation.

## What was delivered

- **Content.** `tax.us.nominee-allocation.amount` (`bundle.v2` / `fact-type.v2`),
  identity keys `payer`, `statement`, `tax-year`, `recipient`, sharing the
  committed box-1 report's own identity components; `exclusiveMinimum: 0`;
  `free` supersession; no admission invariant over the amount.
- **Entity kind.** `tax.us.interest-allocation-recipient` — bounded and
  role-specific, with an application-minted opaque workspace id and the typed
  name as a non-authoritative label.
- **Producer and lifecycle** (`packages/tax/nominee_allocation_recording.py`):
  answer validation, recipient introduction, the persisting assertion path, and
  a separate bounded retraction operation. Before any act is appended, the
  producer requires a *current* evidence citizen whose `content.mode` is
  exactly `ordinary-language-entry`, whose `content.answers` is a valid
  ordinary-language nominee-allocation submission, and whose recorded answers
  correspond to the answers being mapped on every field that determines the
  finding (`circumstance`, `payer_name`, `statement_reference`, `tax_year`,
  `recipient_id`, `amount`). Missing, malformed, document-report, and unrelated
  modes are all refused. A Form 1099-INT copy is evidence of what the payer
  reported, not that the user allocated an amount to another recipient. The
  contribution may record `ordinary-language-entry` as its mode after that
  check; it does not invent whether the underlying interaction was synthetic.
- **Recovery** (`packages/tax/nominee_allocation_recovery.py`): current
  allocations, labels, contribution and evidence provenance, attribution, and
  the report join, rebuilt from a committed log. Retracted records recover the
  original amount, identity, assertion actor/time, and retraction actor/time;
  nothing claims the original actor recanted.
- **Evidence grounding.** Box-1 findings cite a document-report evidence
  citizen. Each distinct allocation answer event — an initial assertion, a
  later correction with a changed amount, a cross-actor assertion, and a
  reassertion after retraction — cites its own ordinary-language evidence
  citizen. That citizen retains the submitted answers in `evidence.v1.content`;
  the finding is the canonical proposition derived from them, not a copy of
  that payload. Synthetic fixtures identify themselves on those evidence
  citizens.
- **Legacy coexistence.** The committed nominee-subtotal rule is exercised
  through projection, marshalling, closure admission, and `run()` before and
  after recording an allocation; the new allocation is neither consumed nor
  pinned. This is not return integration.

## Carry-forward lessons

- **A rebuild onto a better substrate is cheaper than a workaround, and the
  test is whether the workaround was ever honest.** Track 0 first compared an
  individuated-entity route and a source-family route, and both *passed* A2–A6.
  Both failed A11 the same way: they removed the **fact**, so the proposition
  ceased to exist and its identity had to be abandoned to answer again. When the
  retraction milestone landed, the milestone was literally rebased onto it and
  the same cases were re-run — A11 then succeeded at the same fact identity, and
  the entire family/horizon packaging cost evaporated. The earlier candidates
  were not nearly right; they were solving the wrong problem, and only a case
  that discriminated them showed it.

- **A gate cannot be discharged against a stand-in for the thing it guards.**
  Track 0 declared the Payload Instantiation Gate discharged on instances built
  from an invented `demo.report-1099int` entity, and wrote a claim-reuse proof
  asserting the payer report fact "is read as the report identity" — while the
  probe read no report fact at all. Both were false, and neither was caught by
  the reviews that passed them, because both were *internally* consistent. They
  were caught by the owner asking what the probe actually touched. Grounding the
  probe in `report_statement_identity.py` then surfaced two real mechanics for
  free: `tax-year` must be a `literal` key, and same-member correction goes on
  the ordinary assertion path, not a member-transition.

- **Separating the proposition from its speaker is a contract, not a wording
  preference.** The fact's question was originally "the amount the asserting
  person says belongs to…", which embeds the author in the proposition. The
  repair — *the amount of interest reported on this identified Form 1099-INT
  that is allocated to this named other person* — is what makes the finding
  answerable by any recorded actor and the attribution live entirely on the act.
  The same confusion had spread into the cases, where allocation *recipients*
  ("Pat changes $300 to $250") were written as if they were authors.

- **The kernel's meaning and the product's sentence can differ, and the gap must
  be surfaced rather than worded away.** ADR-0073 delivers "a recorded actor
  ended the current support of one identified finding" and explicitly not "the
  original author withdrew." This milestone's A6 was written in the user's
  voice. That gap was the milestone's one genuinely owner-held decision, and it
  resolved into a stated **shared-workspace model**: one current answer per
  report and recipient, any recorded actor may correct or retract it, actor is
  opaque provenance, and no durable text may claim recantation.

- **Prove a negative test is load-bearing by breaking it.** The Track 2
  reviewer confirmed allocations do not surface through
  `untranslated_source_findings` and then set `source_amount: true` to check
  they *would* — converting "the test passes" into "the test can fail." That is
  the cheapest available answer to the standing question of whether a negative
  assertion is doing any work.

- **A negative-only mode check is not a grounding requirement.** Refusing
  `document-report-entry` left missing, malformed, and unrelated modes — and an
  evidence citizen whose answers did not match the mapped finding — able to
  license an allocation. The production contribution then manufactured
  `ordinary-language-entry` plus `synthetic: True`, asserting a provenance it
  had never verified. The load-bearing check is the positive one: current
  ordinary-language-entry evidence whose submitted answers correspond to this
  call, with synthetic identity left on the fixture's own evidence citizen.

- **An unreachable guard is not automatically a vacuous test.** The
  duplicate-current-report case cannot arise from a well-formed log, and the
  test hand-builds a `CurrencyView` to reach it. The earlier ratified lesson —
  a kill condition inherits discriminability from its facts — looked like it
  applied and does not: there, the defining fact could not be *observed*, so
  conforming and non-conforming code both passed forever; here the defining
  state is *injected*, and an implementation that picked the first match fails.
  The distinction is whether the check can fail, not whether the state occurs
  naturally.

## Deferred, with triggers

- **Author-bound recantation and permission rules.** *Trigger:* a concrete
  product case — collaboration, audit, delegation — requiring proof of who may
  remove whose assertion, or a claim of personal recantation.
- **Author-indexed propositions and conflict reconciliation.** *Trigger:* a
  product needing several users' independent assertions to coexist.
- **Recipient display-name correction.** `entity.v1` labels are immutable and
  supersession displaces the facts individuated on the entity. *Trigger:* a
  concrete need to edit a recipient label without displacing recipient-linked
  facts.
- **R-B, the source-independent association model.** *Trigger:* an allocation
  known independently of a particular report, or one that must survive
  report-identity replacement.
- **A10's routing destination.** No module owning document-correction or
  erroneous-report routing exists; this milestone proves only non-capture and
  claims no routing.
- **T0-F5** remains deferred behind its hard production gate, unchanged and not
  repaired here.

## Known limitations

- **Hard gate: interrupted multi-act write is not resumable.**
  `assert_nominee_allocation` appends entity, contribution, and assertion as
  separate `ActLog.append` calls. There is no atomic multi-act append, no
  transaction substrate, and no rollback. An interruption can persist a prefix
  that makes repeating the same call fail (an already-introduced recipient, or
  an already-recorded contribution). Semantic pre-application is not atomicity,
  and the earlier claim that a caller "must re-drive the remaining acts" is
  withdrawn as false. **No user-facing production caller may rely on this
  operation until resumable or idempotent recovery of that prefix is closed.**
- **The committed no-activity test re-reads the same log** and is weaker than
  the property it names. The Track 2 reviewer verified the property under a
  stronger probe (bundle absent vs adopted vs allocated); the committed test was
  not strengthened.
- **The structural rule check inspects `rule-artifact.v2` only** — 35 of 148
  rule files. The property holds and no rule consumes the new fact type, but the
  check is narrower than its claim. Owner decided not to widen it here.
