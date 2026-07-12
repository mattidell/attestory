# Round 1 Adversary Review — Source Completeness

Date: 2026-07-12
Seat: adversary, High tier / high effort
Evidence rung: 1 (paper only)

## Method and observations

I ran all seven declared attacks with equal effort against both exhibits. An
attack passes only when the paper contract itself closes the path; production
intent is not execution evidence. Observations, separate from measurements:

- Production still accepts caller-supplied `RunContext.closed_sets`, passes the
  bare set unchanged to `Environment`, and pins no closure finding for an empty
  collect (`runner.py:63-73,134-160`; `runners/derive.py:23-34`). Both designs
  disclose that their replacement is not implemented.
- IRS Form 1099-INT instructions distinguish taxable interest in box 1 from
  Treasury interest in box 3 and tax-exempt interest in box 8. They require an
  account number for multiple same-recipient accounts, but the general
  instructions describe that number as payer-assigned and allow more than bank
  accounts. General correction instructions preserve a supplied account number
  on a correction. These sources pressure, but do not dictate, workspace fact
  identity.
- “That’s all my interest income” is ordinary-language income-universe wording;
  neither design declares a presentation boundary that narrows it to box 1 or
  furnished 1099-INT statements.

## Measurements: attack → outcome → exhibit

### A1 — False-closure trap

- **it1: paper resists; execution unmeasured.** The resolver admits only an
  exact current boolean `true`; false, absent, and displaced cases block. The
  bare-set adapter after resolution remains precisely the unexecuted seam, so
  paper cannot establish that it is the sole writer. **Exhibit:**
  `it1/sc-p1-mapping-design.md`, “resolver — sole writer,” negatives (c)/(d);
  `examination-it1.md`, SC-P1 enforcement disposition.
- **it2: paper resists; execution unmeasured.** Four predicates include exact
  value equality and currency; false/absent/displaced block. Its projection to
  membership is likewise only specified. **Exhibit:** `it2/design.md`, SC-P1
  candidate shape and negative fixtures; `examination-it2.md`, SC-P1 caveat.

### A2 — Caller-set smuggle

- **it1: paper resists, with a production-condition exposure.** The resolver is
  declared the sole writer and replaces scenario `closed_sets`; injection would
  violate the contract. But its output is still a bare `frozenset[str]`, so an
  unchanged alternate `RunContext` constructor can smuggle membership unless
  the old field/API is eliminated. **Exhibit:** `it1/sc-p1-mapping-design.md`,
  resolver signature and open adoption-surface question.
- **it2: paper resists, with the same boundary exposure.** Caller injection is
  explicitly rejected/ignored and only adopted rule projection may populate
  L2. The design does not declare the replacement `RunContext` type or prove
  that no additive runtime set survives. **Exhibit:** `it2/design.md`, “Caller
  injection” and producer/authority/consumer map.

### A3 — Identity trap

- **it1: attack succeeds.** `(year, subject, payer, account)` collides when one
  payer furnishes two independently correctable 1099-INT information returns
  concerning the same account. Both box-1 amounts answer one fact and become
  rivals rather than additive sources. The design rejects statement identity
  categorically, so it has no tie-breaker. **Exhibit:**
  `it1/sc-p2-identity-design.md`, chosen key and rejected statement-id rival.
- **it2: attack partially succeeds.** Statement citizens distinguish the above
  returns and the two-account fixture. But “individuated when the user asserts
  which logical statement” supplies no declared sameness key: re-upload can
  accidentally mint a second statement citizen for the same logical return,
  duplicating facts without literally keying on evidence. **Exhibit:**
  `it2/design.md`, chosen key; `examination-it2.md`, stated production condition.

### A4 — Rekeying trap

- **it1: attack succeeds at account correction.** If an asserted account
  citizen was misidentified and later corrected, the account identity component
  changes. A box-value correction that should answer the same economic question
  can become succession/new individuation. The paper covers amount correction
  only when account identity is already right. **Exhibit:**
  `it1/sc-p2-identity-design.md`, correction lifecycle.
- **it2: paper resists ordinary correction; edge unresolved.** Original and
  corrected copies remain one logical statement citizen and evidence changes no
  key. A correction requiring the payer to void one return and issue another is
  not classified as correction versus succession, but the paper does not itself
  force evidence rekeying. **Exhibit:** `it2/design.md`, chosen key and
  same-fact correction lifecycle.

### A5 — Family-boundary trap

- **it1: attack succeeds.** `tax.us.2025.interest` is defined as the family of
  `interest.box1` findings, while the user-facing sentence says “all my interest
  income.” Treasury interest (1099-INT box 3), other taxable-interest fact
  types, and non-1099 interest fall outside mapping membership and coverage.
  The attestation therefore closes more than both consumers believe. **Exhibit:**
  `it1/sc-p2-identity-design.md`, closure interaction;
  `it1/sc-p3-source-family.md`, definition and interest example.
- **it2: attack succeeds.** The family is “1099-INT statement instance,” not all
  interest income. A user with no furnished 1099-INT but reportable interest can
  truthfully complete that document family while the natural-language claim is
  false; conversely, “all income” does not say all statement instances were
  enumerated. **Exhibit:** `it2/design.md`, SC-P3 definition and family table.

### A6 — Stale-pin trap

- **it1: attack succeeds under duplicate mapping entries.** Authority is keyed
  only by `source_family`; the paper declares neither uniqueness of mapping
  entries nor rejection of two adopted mappings for one family/scope. One pin
  can overwrite/displace the other in the dictionary, letting explanation
  reach a different closure finding than admission used. **Exhibit:**
  `it1/sc-p1-mapping-design.md`, mapping entries and `authority` dictionary.
- **it2: paper resists.** Resolution requires exactly one fact match, and the
  published zero pins that exact closure finding plus the rule bytes containing
  the parameter and adoption. Ambiguity blocks. **Exhibit:** `it2/design.md`,
  four projection predicates and required explanation pins.

### A7 — Evolution trap

- **it1: mapping shape resists; identity/family do not.** A next-year box can
  reuse one family mapping, but a new independently reported item on the same
  payer/account collides unless the fact model adds a discriminator; broadening
  beyond box 1 also changes the declared member fact type/family meaning.
  **Exhibit:** `it1/sc-p2-identity-design.md`, chosen key;
  `it1/sc-p3-source-family.md`, tuple definition.
- **it2: identity resists; mapping duplicates evolution work.** Statement
  identity accommodates a new box without rekeying, but every collecting rule
  embeds its own closure parameter. A new or revised rule repeats/version-bumps
  the mapping, creating divergence pressure rather than one mapping rewrite.
  **Exhibit:** `it2/design.md`, adopted-rule parameter and paper disposition.

## Dissent and recommendations

I dissent from both examinations’ conclusion that SC-P3 is supported at paper:
the closure utterance, member universe, mapping unit, and coverage unit are not
extensionally equal. This is decision-blocking for any contract that presents
the quoted attestation without a narrower declared claim.

I also dissent from it1’s “SC-P2 settled” conclusion: same-account multiple
returns and correction of misidentified account identity are unhandled
collisions/rekeying paths. It2 is stronger on those attacks, but its logical
statement individuation needs a declared anti-duplication rule as a production
condition. Recommend the foreman classify; do not enlarge this round’s scope.
