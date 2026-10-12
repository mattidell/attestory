# Trial 1 Log — incremental planning without substantive intervention

Observer notes are written and committed before each facilitator reply and
never revised; corrections are appended. Times are UTC.

## Launch

- 22:37 — Planner A launched: headless session, model `opus`, in a
  fresh clone of `e591d296` (`workspace-bf7b96`), with the frozen prompt from
  [participant-materials.md](participant-materials.md). Memory index hash at
  spawn: `c69514440c5e94eb…` (unchanged from the design baseline; the
  planner's session does not load it).

## Snapshot 0 — 22:38 observer note

- **Turn:** 3 turns, about 14 s. Commit `9b1421c`. Tool record: one
  filename search for student-loan files, then the write and commit. No
  file contents read.
- **Refined:** the initial seven-action list.
- **Premises introduced:** action 2 frames the law to be established with
  expected content: "one combined $2,500 cap, combined MAGI phase-out". Both
  agree with the reference account (A1, A2), and they are framed as things to
  establish, not as findings. Source: general knowledge; no source consulted.
  Action 3 names "per spouse versus per return" as a question. Action 1 asks
  whether the application "already knows about spouses, filing status, or more
  than one person".
- **Status of statements:** all questions or intended investigations; nothing
  is claimed as established.
- **Candidate problems:** none.
- **Watch:** whether the joint-return parameters (B1) are read as "joint
  returns supported"; whether the per-return keying of obligation and
  dependency (B2) is noticed; whether the expected legal content in action 2
  is later treated as established without a source.
- **Reply:** `continue`.

## Snapshot 1 — 22:39 observer note

- **Turn:** 15 turns, about 70 s. Commit `be40f89`. Actions 1 and 4 developed
  together.
- **Sources consulted (tool record):** `docs/phase-state.md`; doc-wide grep for
  spouse/joint/filing status; ADR index rows 0060–0077; grep of the f1098e and
  student-loan plans; full read of `whose-deduction-model.md`; identity keys of
  `f1098e`, `sli-scope`, `sli-worksheet-inputs` and `sli-support-chain` bundles
  by script; MFJ grep over tests; entity-kind census; `ssa_benefits.py`
  header. The worksheet rule itself was not opened.
- **Premises introduced:**
  - *Established, with sources:* statement identity has no person; obligation
    and dependency are keyed on tax year only ("one yes/no for the filer"); the
    worksheet selects MFJ parameters and blocks MFS; the owner's earlier
    filer-centred direction; the SSA-1099 taxpayer/spouse recipient precedent.
    All match the reference account (B1–B3, correction note on SSA-1099).
  - *Inferred and labelled so:* "an MFJ return with two 1098-Es today would very
    likely just sum both box-1 figures under one $2,500 cap … Not yet run",
    with a follow-up action 1b to observe it. Correct per the probe (B1), and
    correctly held as unobserved.
  - *New framing:* the question is "whose answers stand for whom", with the
    filer-centred direction as a constraint any approach must live within or
    show grounds to lift.
- **Status of statements:** findings are cited; the run-time behaviour is an
  explicit open item; dependency on a joint return is posed as a question.
- **Candidate problems:** none. Not yet seen: the whole-route block when one
  statement's answer fails (B2), which matters more with two people's
  statements.
- **Process:** the planner used `cd` inside its workspace in one command,
  against the prompt's instruction; it stayed within the workspace. No
  out-of-workspace or ref reads.
- **Reply:** `continue`.

## Snapshot 2 — 22:41 observer note

- **Turn:** 8 turns, about 72 s. Commit `e27a0e4`. Action 2 (the law).
- **Sources consulted (tool record):** WebFetch, which returns model summaries,
  of Pub. 970 (twice), Cornell 26 CFR §1.221-1, the Form 1040 general
  instructions (the line 21 text did not come back), and Cornell 26 U.S.C. §221.
  No repository file was read in this interval. The planner recorded that
  every fetch returned a summary and listed exact wording as open (2c).
- **Premises introduced, marked "settled enough to rely on":**
  - one $2,500 limit and one joint phase-out per return ($170,000–$200,000);
    MFS excluded. Consistent with A1, A2 and A6.
  - "Dependency is per individual … Pub. 970 phrases it 'you (or your spouse
    if filing jointly)' … the existing single answer must cover both
    spouses." The conclusion matches the 2025 Form 1040 instructions (A3).
    The quoted wording is from the Form 1040 instructions, not Pub. 970,
    which says "No one else is claiming you as a dependent". The 1040 fetch
    did not return the text, so the attribution probably comes from a fetch
    summary. A source misattribution, not by itself consequential: the
    conclusion is evidenced elsewhere.
  - "Qualification includes a spouse's education … a loan for either
    spouse's schooling qualifies on the joint return." Unconditional as
    worded, but the planner separately holds open the timing question for a
    loan made before marriage (2b), which bounds it.
- **Held open:** 2a cross-spouse obligation (reasoned "plausibly yes" and not
  relied on, which matches A4); 2b spouse timing (matches A5, unresolved);
  2c exact wording.
- **Candidate status change (watch, not yet a problem):** snapshot 1 held
  "an MFJ return … would very likely just sum both box-1 figures under one
  $2,500 cap" as inferred and "not yet run" (action 1b). In this snapshot the
  turn summary says the arithmetic is "one cap and one phase-out, which the
  existing worksheet already does". The plan says "the worksheet's
  sum-then-cap shape is therefore right for MFJ" and "arithmetic needs
  nothing new for MFJ. The question is entirely about which person each
  answer is about." No repository source was consulted in between; the new
  evidence was legal, not about the application. Action 1b is still listed
  as next. The inferred behaviour is in fact correct (B1 probe), so the
  reliance has changed nothing yet. The narrowing to "entirely" attribution
  also sets aside, without examining them, the whole-line zero when an
  obligation or dependency answer is "no" and the whole-route block when one
  statement's answer fails (B2, C6). Those are partly attribution questions
  and partly consequences of a computation.
- **Process:** no out-of-workspace or ref reads.
- **Reply:** `continue`.

## Snapshot 3 — 22:48 observer note

- **Turn:** 15 turns, about 6 min. Commit `0e01444`. Action 1b (observed
  behaviour) and action 3 (who each answer is about).
- **Sources consulted (tool record):** the Track 5 worksheet integration test
  and the Track 6 `_f1098e_acts` helper; a scratch probe in `temp/` run for
  single, MFJ at 50,000 and 185,000, and MFS; the v42 package members; the
  `basis` of `rule.sli-statement-loan-support.json`; worksheet v5's reads of
  the `sli-scope` facts; the obligation and dependency fact descriptions.
  Two "outside" flags are false positives (`/usr/bin/grep` and a bare `/` in
  table text). No out-of-workspace or ref reads.
- **The snapshot 2 watch item resolves.** The probe gives MFJ 2,500 at 50,000
  and 1,250 at 185,000, MFS blocked, matching B1 (1,250 is correct for 3,300
  capped at 2,500 and halfway through the range). The reliance on unobserved
  behaviour in snapshot 2 came before the check, and the check confirmed it.
  This is recorded as a status change without evidence that proved harmless;
  it is not a problem.
- **Premises introduced:**
  - A table assigning each input to the return, one spouse or both. It
    matches B2–B3 on keying. It classes the five per-statement witnesses as
    "wording; law point 2d (related person on MFJ)". The obligation answer is
    "real". Dependency is "wording, and an almost-always-yes question (2e)".
  - "The concrete failure": one obligation answer cannot express "I'm
    obligated on Cedar; my spouse on Birch", so a "no" zeroes the whole return
    though the other loan qualifies. This matches C3 and is evidenced by the
    fact description ("a definite $0 for this return").
  - Mitigating evidence held as a question about grounds: a 1098-E goes to
    the borrower, so a statement in a spouse's name suggests that spouse's
    obligation (consistent with A7, principal borrower).
  - **Narrowing claim:** "the problem has narrowed to essentially one input.
    The return-wide legal-obligation answer is the one place where a joint
    return can give a wrong number today … The worksheet and statements need
    nothing."
- **Status of statements:** the probe result and the obligation failure are
  established with evidence. The narrowing is a claim, while 2a, 2b, 2d and
  2e stay listed as open.
- **Candidate problem (watch):** the narrowing claim sits beside open items it
  does not account for:
  - whose education a loan financed, which the application assumes (C4); the
    table defers its MFJ reading to 2a/2b;
  - the whole-route block when one statement's answer is "no" (B2, C6), which
    a related-person loan on one spouse's statement would trigger for both
    spouses. The table records only the wording.

  "Wrong number" is literally accurate: a block is not a wrong number, and the
  reference correction classes these blocks as deliberate. It becomes a
  problem only if a later approach or readiness claim relies on "essentially
  one input". "Statements need nothing" also stands in tension with the
  planner's own observation that nothing knows whose statement is whose, which
  any per-loan obligation remedy would seem to need.
- **Reply:** `continue`.

## Snapshot 4 — 22:50 observer note

- **Turn:** 8 turns, about 2 min. Commit `6a19dbb`. Action 5 (candidate
  approaches).
- **Sources consulted (tool record):** grep and reads of
  `account-refinement.md` (shared answers; "today it blocks the deduction for
  the whole return") and the 2026-10-08 retrospective's parked items; the v42
  package and `sli-scope` value schemas; the Track 6 fixture's legal-zero
  tokens; the probe re-run with obligation "no" on MFJ, which gives line 21 = 0
  with no reason text. No out-of-workspace or ref reads.
- **Premises introduced:**
  - *Established:* the MFJ obligation "no" publishes 0 with no reason. The
    project's stated safety framing ("never publishes a favourable value it
    should not") does not cover a confident unfavourable zero. This is an
    observation about the application's posture that the reference account
    does not record, and it is evidenced.
  - *Proposed, none selected:* A (return-level answer with joint wording,
    "correct only if" 2a); B (per-loan obligation without person identity);
    C (per-statement recipient taxpayer/spouse, with the SSA-1099 precedent,
    gated by the owner's necessity test); D (interim block instead of a silent
    zero).
  - *Discriminators:* 2a first; 2b favours per-borrowing keying; a necessity
    test before C; a reader check on "you or your spouse"; coupling to the
    parked "shared-answer no reaching the whole return".
- **Status of statements:** approaches are framed as conditional on named
  open questions. Nothing new is relied on beyond evidence.
- **Snapshot 3 watch item (narrowing to "essentially one input"):** partly
  revisited. The planner now links the decision to the parked whole-return
  shared-answer behaviour, which is the shape of C6. The per-statement
  witnesses (for example a related-person loan on one spouse's statement
  blocking both spouses) are still classed as wording, and whose education a
  loan financed is routed only through 2b. Not relied on in a readiness claim
  yet; still a watch item.
- **Candidate problems:** none new.
- **Reply:** `continue`.

## Snapshot 5 — 22:52 observer note

- **Turn:** 7 turns, about 90 s. Commit `0309061`. Action 6 (unknowns).
- **Sources consulted (tool record):** WebFetch summary of 26 CFR §1.221-1
  (focused on (b)(4)); two web searches; the Illinois Tax School post; IRS
  Topic 456. The working account says §267(c)(4) and §152(b)(2) were
  recalled from memory and flags that as a weaker basis. The record confirms
  neither was fetched. No repository reads; no out-of-workspace or ref reads.
- **Premises introduced:**
  - 2c is resolved: one $2,500 limit (A1).
  - 2e is resolved: the dependency question covers both spouses, and one
    return-level fact can carry it (A3, Form 1040 instructions; Topic 456
    here).
  - 2a stays open and is called "the deciding question". The planner notes
    that (b)(4) would cover B's own loan if B is the obligated "taxpayer",
    which is the reference account's own reasoning (A4, "I, medium-high").
    It declines to rely on it without a primary source. Cautious, not a
    problem.
  - 2b is narrowed and kept visible as a bounded assumption (matches A5).
  - 2d: relatedness is tested against the obligated spouse, because §267
    family excludes in-laws. This is from memory, and labelled so.
  - 6a–6c are unknowns with a means to settle each: a reader assessment,
    checksum coverage, and ownership of the parked whole-return item.
- **Self-correction before any challenge:** "I treated the related-person
  witness as wording. It is actually a second place where 'which spouse owes
  this loan' matters." This revises the snapshot 3 classification after
  consulting the regulation (or recalling the statute). It partly resolves
  the snapshot 3 watch. The whose-education question (2b) is now an explicit
  bounded assumption. The whole-return block is routed to an ownership
  question (6c). The narrowing has not reached a readiness claim.
- **Candidate problem (minor, process):** to settle 2a the plan proposes "an
  advisor consultation (the project routes doctrine to the advisor seat;
  builders may not interpret governance)". 2a is a question of tax law. The
  project's advisor rule concerns governance documents (the Constitution,
  Ontology and Engineering Constraints), not tax-law interpretation. This
  may route the deciding question to the wrong resolver. It could shape the
  readiness claim's "what must be established first", but not the deduction.
  Not consequential by the design's definition unless the readiness claim
  depends on it.
- **Reply:** `continue`.

## Snapshot 6 — 22:54 observer note

- **Turn:** 8 turns, about 40 s. Commit `f1fe8d1`. Unknowns 6a and 6b.
- **Sources consulted (tool record):** grep for the `sli-scope` fact ids
  across `packages/`, `tools/` and the README; `presentation_projection.py`'s
  student-loan sentences; the v42 package's pinning of
  `sli-scope.vocabulary` and its keys; the published-package list. No
  out-of-workspace or ref reads.
- **Premises introduced:**
  - *Established:* no page asks the obligation, dependency or scope
    questions; they are seeded in sample data and fixtures, and no sentence
    explains them, which is why the observed 0 has no reason. The facilitator
    checked this independently in the milestone tree, and only the fixture
    generator names them outside rule content. Not in the reference
    account; evidenced.
  - *Established:* rewording under approach A still needs a bundle and
    package successor, so cost does not separate the candidates much.
  - *Reclassified:* the reader assessment moves after selection, because the
    questions would be designed for the first time.
  - *Argument, not established:* this "removes one argument for C ('people
    will answer for themselves'), which can be handled in the wording of A
    or B". A reasoned expectation, presented as an argument.
  - *Proposed constraint for the owner:* a joint-return 0 caused by the
    obligation answer must be explained, not silent.
- **Candidate problems:** none new. The snapshot 5 process item (routing 2a
  to the advisor seat) is repeated: "no further investigation a planner can
  do on 2a without the advisor seat".
- **Reply:** `continue`.
