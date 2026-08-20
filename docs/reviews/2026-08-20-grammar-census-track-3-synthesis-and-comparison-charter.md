# Builder Charter — Grammar Census Track 3: Synthesis and Comparison Brief

Audience: Builder (two streams)

Filed by the Foreman 2026-08-20. Track 2 is complete: reconciliation
`f276cc5b` (166 constructs), representative traces `3dba1a80` (6 traces),
tension catalog `5ba385c1` (9 entries). All three were verified in part by the
Foreman against source before acceptance.

One file charters both streams. Read the other stream's section. You may read
the other stream's deliverable if it exists, but do not wait on it and do not
cite it — cite the Track 2 deliverables.

**The milestone's exit-criteria assessment, the owner-facing final report, and
the retrospective are Foreman work and are not yours.** Do not attempt them,
and do not write a "conclusion" that reads like one.

## Shared Context Capsule

- **Source ref:** `HEAD` on `milestone/grammar-census-engine-language-map`.
  Resolve and verify the SHA against Git before acting. Confirm
  `git rev-parse --show-toplevel` and `git branch --show-current`.
- **Milestone key and primary branch:** `grammar-census` /
  `milestone/grammar-census-engine-language-map`. Primary worktree is the one
  you are launched in. Do not create a worktree.
- **Role:** Builder.
- **Evidence-rung ceiling:** committed repository artifacts, the seven inquiry
  deliverables, the Foreman correction record, and executions you actually ran
  and show. **Stream 3b additionally consults external-model knowledge under
  the strict conditions in its own section.**
- **Full reads before acting:**
  - `docs/roles/builder.md`
  - `docs/process/concurrent-work.md`
  - `docs/phases/grammar-census/milestones/engine-language-map.md` —
    `#Objective`, `#Scope`, `#Non-goals`, `#Deliverables`,
    `#External comparison brief`, `#Tracks`, `#Exit criteria`, `#Data safety`
  - `docs/phases/grammar-census/inquiries/track-2-reconciliation.md`
  - `docs/phases/grammar-census/inquiries/track-2-tension-catalog.md`
  - `docs/phases/grammar-census/inquiries/track-2-representative-traces.md`
  - `docs/phases/grammar-census/inquiries/track-0-boundary-and-corpus.md` —
    the boundary map and the amended primary criterion, at minimum
  - `docs/reviews/2026-08-20-grammar-census-foreman-correction-5b-ii-ruling-reasoning.md`
  - your own section of this charter
- **Read as needed:** the three Track 1 deliverables, for the underlying
  record behind a reconciled row.

## Shared constraints — both streams

- **Write exactly one file**, named in your section. Everything else is
  read-only for you.
- **Documentation only.** No production code, schema, package, test, fixture,
  or tax content may change. Your diff must be exactly one file.
- **Exit criterion 8 is a hard constraint on your output**: the result makes
  no grammar change, product contract, ADR, governance interpretation, or
  external-standards claim. You are describing and scoping, not deciding.
  **Track 3 selects nothing.** The phase stays open; the next milestone is
  owner-held.
- Cite every material claim to a committed path with version, to a reconciled
  construct ID (`U-###`), to a catalog entry (`T#`), to a trace, or to an
  execution you ran and show.
- **Do not read anything under `docs/phases/claim-boundary-exploration/`**
  beyond the merged CQ-1 bounded-lens allowance in the plan's
  `#Claim-boundary evidence posture`. Unmerged CQ-2 is off limits. Say if you
  use the lens and what it changed.
- Do not push the branch. Do not open a PR.
- No personal, private, or real filer data. No absolute workstation paths in
  anything you commit.

## Committing

Two streams share one Git index in one worktree. Follow
`docs/process/concurrent-work.md`: acquire the lock
(`collab_lock="$(git rev-parse --git-path collaboration-commit.lock)"`,
`mkdir "$collab_lock"`); **if it fails, do not remove it** — sleep 10s and
retry for up to 5 minutes, then report without removing. Stage only your one
path, inspect `git diff --cached --name-only`, commit, `rmdir` to release even
on failure.

**Commit incrementally.** Write a section, commit it, continue. Two runs in
this milestone were killed by an external limit; the one that had been
committing as it went lost nothing.

Run `python3 tools/governance_lint.py` before handoff. It must print
`governance lint: conformant`.

---

# Track 3a — Plain-language engine language map

**Write only:** `docs/phases/grammar-census/inquiries/track-3-engine-language-map.md`

Produce the reconciled account of the engine-language boundary and its major
layers for a **casual but technically invested reader** — someone who can read
code and JSON but has not read this milestone, does not know this repository,
and will not open the census to check you.

**This deliverable is what exit criterion 1 is judged on**, and it is the only
deliverable in the milestone judged on legibility rather than on evidence
alone. Write accordingly.

- **The reader must be able to answer, from your file alone: what language
  does this engine actually have?** Not what constructs exist — what *kind of
  thing* it is. Where its boundary falls and why that boundary and not a wider
  or narrower one. What its layers are and how they relate. What it can
  express and what it cannot.
- **Do not reproduce the census.** 166 rows already exist one directory over.
  A map that is a shorter table is a failure. Structure, relationships, and
  the shape of the thing are your product; the table is your source.
- **Ground it.** Every claim about the language still traces to a `U-###`, a
  path, a trace, or a shown execution. Legible and unfounded is worse than
  illegible and true.
- **Carry the boundary honestly.** Track 0's boundary rests on an amended
  primary criterion that was fitted to a Foreman ruling after the fact — Track
  0 says so in its own text, and the Foreman correction record says the
  ruling's stated reasoning was later falsified. A reader who rejects the
  enforcement-versus-declaration distinction draws the boundary in a different
  place. **Say that, in the map, in plain language.** Exit criterion 4 is not
  satisfied by burying it in the reconciliation.
- **Say what the language cannot express**, not only what it can. That is the
  question the phase exists to answer and the hardest part of this file.
  Catalog entries T8 and T9 are a starting point, not the answer.

Two cautions specific to your stream:

- **Plain language is not vagueness.** "The engine has a small expression
  language" tells the reader nothing. "The engine has *two* expression
  languages that share no operators and are evaluated by different modules"
  tells them something. Prefer the specific true sentence.
- **You are not writing an advocacy document in either direction.** The census
  found real defects and also found a coherent, largely-working language. A
  map that reads as an indictment and a map that reads as a brochure are both
  wrong.

---

# Track 3b — Bounded external-comparison brief

**Write only:** `docs/phases/grammar-census/inquiries/track-3-comparison-brief.md`

Produce the brief per the plan's `#External comparison brief`. It states:
which semantic dimensions are now worth comparing; which external systems
appear relevant to each dimension; what questions a comparison could answer;
what evidence would change an engine decision; and which comparisons would be
superficial or inapplicable.

**You scope a comparison. You do not conduct one.** Exit criterion 7 is that a
follow-on comparative review can be scoped from your explicit questions rather
than from a generic survey of other languages. A brief that summarises what
Catala or OpenFisca is has failed; a brief that says "compare us to Catala on
X, because our census found Y, and answer Z would change decision W" has
succeeded.

**Dimensions raised by an external model during Track 0, to carry forward.**
These came from a consultation, not from the corpus. Treat each as a
*candidate dimension to assess*, not as an authority and not as an established
gap. For each, say whether this census's evidence makes it worth comparing,
and drop the ones it does not:

- **defeasibility** — whether rules can be overridden by other rules;
- **period and horizon semantics**, as OpenFisca handles them;
- **peer languages versus one grammar with satellites**, as DMN/FEEL is
  situated;
- **embedded versus standalone** language design;
- **object language versus observational theory** — whether the artifacts are
  the law's language or a description of it;
- **constitutive versus prescriptive** rules, as LegalRuleML distinguishes
  them.

**External-model consultation is permitted for this stream, under three
conditions.** You may consult your own knowledge of these systems to
characterise a dimension. But: (1) **no external claim may originate a finding
about this engine** — every statement about what our engine does cites the
census; (2) **mark every external characterisation as external and
unverified**, because you cannot check it against a committed artifact and
this milestone's evidence ceiling does not cover it; (3) **where you are
unsure whether an external system actually works the way you recall, say so
rather than asserting it.** A confidently wrong sentence about Catala is
exactly the failure mode that produced the Q1 error recorded in
`docs/reviews/2026-08-19-grammar-census-track-0-boundary-map-external-critique.md`.

Two more:

- **The dimensions that matter most are the ones our census actually
  pressured.** The tension catalog's expressiveness entries and the map's
  "what it cannot express" question should drive your dimension list harder
  than the external model's suggestions do. If a suggested dimension has no
  purchase on anything the census found, say so and drop it — that is a
  finding about our engine, not a gap in the brief.
- **Name the comparisons that would be superficial.** The plan asks for this
  explicitly and it is the part most likely to be skipped. A brief that only
  says what to compare gives the next unit no way to bound itself.

---

## Stop conditions — both streams

Record and continue on anything short of the following. Return without
completing only if your primary input is unusable — for example if the Track 2
deliverables cannot support a synthesis at all. Say why.

Also return if this charter and the plan disagree about your scope. The plan
controls; do not resolve the conflict yourself.

## Handoff report

Write your report to the absolute scratch path given in your launch brief,
not in chat. Answer:

1. your commit SHAs;
2. what you produced, in structure and counts;
3. what you deliberately left out, and why;
4. what you checked against source yourself, and whether anything in Track 2
   failed that check;
5. **3a only:** the three things you most expect a fresh reader to
   misunderstand from your file, and what you did about each;
6. **3b only:** which carried-forward dimensions you kept, which you dropped
   and why, and every external characterisation you were not confident in;
7. whether you used the CQ-1 lens, and what it changed;
8. anything in the census or the plan your reading suggests is wrong;
9. whether you encountered a held commit lock;
10. your turn count and tool-call count.
