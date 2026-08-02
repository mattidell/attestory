# Adversary Review — Citation Resolution, Round 1

Reviewer: Medium-tier Adversary (owner-launched independent context), 2026-07-15.

Scope: **CIT-P1** and **CIT-P2** in `it1/design.md` and `it2/design.md`, against the
accepted governance set, accepted ADRs **0003**, **0006**, **0012**, **0027**,
**0028**, and committed form-field / package / rule schemas. Paper/static-contract
analysis only. Throwaway probes outside the repo were not required to ground
these findings.

Independence: **did not read** `reviews/round-1-governance.md`, any ADR-0029
draft or notes, or evaluation text toward a conforming citation ADR.

## Understanding (pre-write)

| Item | Understanding used in this review |
| --- | --- |
| **CIT-P1** | What a citation *is*: citizen vs structured value vs pin (or hybrid); v1 authority families; identity and version; attachment to form-fields and (if in scope) rules under ADR-0012 without reopening dispositions. |
| **CIT-P2** | What “resolved / verifiable” means at load/adoption: structure, display/canonical form if claimed, registry if claimed, contained failure modes; explicit out-of-scope (live fetch, legal correctness, multi-jurisdiction unless paper-cheap). |
| **ADR-0012 floor** | Form-fields are presentation citizens; field→symbol binding is one-way; five dispositions and rendering honesty are settled. `citation_ref` is **inert** today; this topic may structure attachment but must not reopen dispositions, value ownership, or make citations derivation authority. |
| **ADR-0027/0028 floor** | Package is the **sole** membership/adoption authority (no path/`manifest.json` second authority). Exact pins, typed closed graph, role-canon monotony, `admitted_schemas`, package-instance immutability, exclusive execution projection, contained validation (ADR-0006 d3). Fact-surface dual pins, composition obligations, and quantity vocabulary are settled membership law; citation work extends the package, it does not replace it. |
| **Independence exclusions** | Governance review output; any draft toward ADR-0029. |
| **Required output** | This file only. Findings **CIT-A1…**. Concrete input → expected → per-design fail/survive. Classify. Verdict **per proposition per design**. Advisory; no repairs, no other file edits, no ADR decisions. |

**Subjects (paper).** Both designs converge on citation as a versioned package
citizen plus exact attachment pins, and claim both propositions
settled-at-static-level. They diverge on (a) display canonicalization and
“verifiable” depth, and (b) case-5 external-corpus posture.

- **it1:** `citation.v1` with `authority` ∈ {`IRC`,`IRS_AUTHORITY`}, required
  `display`, resolver-side canonical formatter, `citation_refs` pin arrays on
  form-field/rule, package role `citation`, contained issues, package-closure miss
  and rewrite rejects.
- **it2:** `citation.v1` with `authority_family` ∈
  {`us-code`,`irs-form`,`irs-instructions`,`irs-publication`}, closed
  family/locator `oneOf`, **no** display claim, exact single field pin + optional
  rule pins, bidirectional typed closure, registry-backed bytes, term
  `statically_resolved` only (never `legal_verified`).

**Method.** Each finding states input → expected correct result → where each
design fails or survives. A break that hits one design and not the other is
preferred. Classification: **decision-blocking** / **production condition** /
**non-blocking**. No repairs.

---

## Finding index

| Id | Title | Designs | Class |
|---|---|---|---|
| CIT-A1 | Opaque resurrection via admitted form-field.v1 / dual-read co-equality | both (it1 softer) | **decision-blocking** (residual-closed packages); production condition (migration) |
| CIT-A2 | False verifiability: “resolved/verifiable” without corpus or overclaim | it1 fails; it2 survives | **decision-blocking** (it1 CIT-P2) |
| CIT-A3 | Article 11: runner-resident IRC/IRS display formatter as “canon” | it1 fails; it2 survives | **decision-blocking** (it1 CIT-P2) / non-blocking (it2) |
| CIT-A4 | Immutability bypass: same `(id,version)` different citation bytes | it1 incomplete; it2 stronger | **decision-blocking** (it1) / production condition (it2) |
| CIT-A5 | Closure/membership leak: co-location, orphan members, role-canon skip | it1 weaker; it2 stronger | **decision-blocking** (exclusive projection + role canon gaps on it1) |
| CIT-A6 | Attachment leak: rule cite as evaluator input; disposition coupling | it1 softer; it2 survives | production condition (it1) / non-blocking (it2) |
| CIT-A7 | Display/spelling games (it1): generator drift, title ignored, free `doc_id` | it1 fails; it2 N/A survives by non-claim | **decision-blocking** (it1 CIT-P2) |
| CIT-A8 | Locator games (it2 primary): soft family/`oneOf`, baggy IRS, free-string tokens | both (different shapes) | production condition (both); decision-blocking only if “schema-closed” is claimed without discriminator |
| CIT-A9 | Soft package outcome: “never abort load” vs adoption reject | it1 fails; it2 survives | **decision-blocking** (it1 CIT-P2) |

---

## CIT-A1 — Opaque free-text resurrection (co-equal dual-read)

**Class:** decision-blocking for residual-closed packages; production condition for
any temporary migration window.  
**Applies to:** both; it1 is the softer target.

### Attack

**Input A — residual-closed package still carries inert string.**

Package `P@v1` admits `form-field.v2` **or** still admits `form-field.v1`
under `admitted_schemas`. Member form-field body:

```json
{
  "schema": "form-field.v1",
  "id": "tax.form-1040.line-2b",
  "version": "v1",
  "citation_ref": "see IRC §61(a)(4) and 1040 instructions p.16",
  "...": "all other required form-field.v1 fields well-formed"
}
```

No `citation` member pin. No structured pin object.

**Expected:** For a package generation the design calls residual-closed for
citations, **reject** (schema or closure). Free text must not be co-equal with
structured pins at runtime. If a dual-read window exists, it must be an
**explicit, versioned, temporary** package/schema-generation policy with an
expiry generation — not an open-ended “both shapes validate forever.”

**Input B — dual attachment: structured pin plus free-text peer.**

`form-field.v2` with both a valid `citation_refs`/`citation` pin **and** a
retained string field (`citation_ref`, `notes`, or undeclared property smuggled
via a tolerant reader) that a renderer prefers when present.

**Expected:** Residual-closed successor schemas reject undeclared properties
(Article 9). Renderers/resolvers must not treat free text as a second resolution
path when a pin exists.

### Per design

| Design | Result |
| --- | --- |
| **it1** | **Partial survive / residual fail.** Case 3 rejects `"citation_ref": "IRC Sec. 61"` on **`form-field.v2`** (`MEMBER_SCHEMA_INVALID`). Good hard cutover *for that generation*. The design does **not** state that residual-closed packages may not admit `form-field.v1` (committed schema still requires opaque `citation_ref: string`). Under ADR-0027, admission is per package `admitted_schemas`: a package that lists `form-field.v1` resurrects opaque strings as first-class residual content. No dual-read expiry generation is named. Input B depends on `additionalProperties: false` on v2 (sketch has it on pins; full field schema not shown). |
| **it2** | **Stronger survive.** Case 3 rejects opaque residual with `CITATION_OPAQUE_RESIDUAL` and proposes **no** dual read. Boundary text: a migration window, if ever adopted, “must be an explicit schema and package-generation policy; it cannot make `citation_ref` a co-equal runtime input in residual-closed packages.” Still requires production to **forbid** residual-closed packages from admitting `form-field.v1` citation strings — stated as policy, not a full generation matrix. |

### Verdict contribution

CIT-P1 identity work on both sides is citizen+pin, which is the right shape, but
**residual-closed opacity is only as strong as generation admission**. Without a
normative “v1 form-field citation strings are not residual-closed under packages
that claim citation closure,” opaque resurrection remains a package-author
option. it2 names the trap; it1 only tests the successor schema shape.

---

## CIT-A2 — False verifiability (claim “verified” without a checkable external rule)

**Class:** decision-blocking for it1 CIT-P2; it2 survives by design.  
**Applies to:** it1 primary; it2 contrast.

### Attack

**Input.** Citation citizen with well-formed structure for a **nonexistent**
authority point, e.g. IRC title 26 section `99999` subsection `z`, or IRS
`doc_id: "Form 0000 Instructions"` tax year 2099. Package pins it; form-field
pins it; all schema and package-closure checks pass. Display (it1) matches the
design’s formatter: `"IRC Sec. 99999(z)"`.

**Expected:** Static acceptance is allowed **only if** the contract’s term for
success does **not** imply legal or corpus presence. If the design claims
“verifiable” / “resolved” in a way that a product surface can honestly render as
“citation verified,” either (a) a separately adopted authority-corpus contract
must reject the miss, or (b) the design must refuse that language and emit a
qualified status only. Silent false confidence is out of floor (plan case 5 /
review measurements).

### Per design

| Design | Result |
| --- | --- |
| **it1** | **Fails.** Section “Verifiable Resolution” defines resolved as (1) pinned package member + schema validate and (2) display matches resolver formatter. Case 5 is only **package** closure (`CLOSURE_MISSING_CITATION`), not corpus presence. There is no qualified status name. A fictional section with matching display is fully “resolved/verifiable.” That overclaims relative to what is checked. |
| **it2** | **Survives.** Explicitly: structural-and-adoption verifiability only; case 5 neither legal-accepts nor legal-rejects external misses; success term is `statically_resolved`, never `legal_verified`; future corpus is a separate versioned contract that must not silently widen this resolver. |

### Verdict contribution

it1’s CIT-P2 language is the decision-blocking false-confidence surface. it2’s
qualified terminology is the correct residual for “no corpus.”

---

## CIT-A3 — Article 11 overreach (fetch, holdings, runner-resident authority meaning)

**Class:** decision-blocking for it1’s display-canon placement; both survive hard
network/applicability attacks as written.  
**Applies to:** it1 (formatter-in-runner); it2 contrast.

### Attack A — live fetch / applicability (hard overreach)

**Input.** Resolver branch: HTTP GET Cornell LII / IRS PDF for the cited
locator; or evaluate whether §61(a)(4) applies given taxpayer interest facts;
or hardcode “section 61 means gross income includes interest” to accept/reject
a rule’s `when`.

**Expected:** Out of floor. Reject/redesign. Resolver validates structure and
adoption only; tax meaning stays in rule artifacts (Article 11).

### Attack B — authority formatting table as runner canon

**Input.** Two runners at different code versions. Runner R1 formats IRC as
`IRC Sec. {section}({subsection})…`. Runner R2 formats as `I.R.C. §{section}…`
or inserts title `26 U.S.C. §…`. Same published citation bytes; no content
change.

**Expected:** Article 9/11: display canon, if claimed, must be **declared,
versioned content** (schema or adopted rendering contract), not a private
formatter in the loader. Runner swap must not change accept/reject of immutable
citizens. Encoding legal citation orthography only in engine code is hidden
meaning.

### Per design

| Design | Result |
| --- | --- |
| **it1** | **Survives A; fails B.** §2.3 correctly excludes network fetch, legal applicability, and multi-jurisdiction ingestion. Case 6 rejects taxpayer-fact applicability in the loader. But §2.1 places **deterministic display generation in the resolver** (`f"IRC Sec. {section}"`, IRS `f"{doc_id} ({tax_year})"` …). That is a runner-resident orthography table coupled to load-time accept/reject (`CANONICAL_DISPLAY_MISMATCH`). It is not a published schema artifact and is not versioned with the citation citizen. Attack B yields cross-runner non-determinism and hidden canon. |
| **it2** | **Survives A and B.** No display claim; family/locator constraints are declared schema content; live lookup or encoded legal/applicability decision is `CITATION_RESOLVER_OVERREACH`. Explicit: “deleting or changing a rule/citation artifact, not a runner branch, accounts for every tax-meaning difference.” |

### Verdict contribution

Hard Article 11 (fetch/holdings) is paper-clean on both. it1 reintroduces a
thinner Article 11/9 failure mode by making **canonical display enforcement** a
loader behavior rather than adopted content.

---

## CIT-A4 — Immutability bypass (same version, different bytes)

**Class:** decision-blocking for it1’s incomplete check chain; production
condition for it2 (must actually wire registry checks).  
**Applies to:** both; it1 weaker as written.

### Attack

**Input A — citation citizen rewrite.** Publish `cite.demo.61@v1` with body B1.
Later offer body B2 ≠ B1 under the same `(id, version)` (e.g. change section
`61`→`62`, or tweak display/locator). Package pin still says `cite.demo.61@v1`.

**Input B — package pin set rewrite.** Publish package `U@v1` with member set M1.
Offer `U@v1` again with different citation member pins or different
`admitted_schemas` (bytes changed, version string unchanged).

**Expected:** Both reject at publication/adoption (Article 9; ADR-0003 registry;
ADR-0027 decision 6 package-instance immutability). Resolution must trust
**registry-verified content**, not bare id/version string equality against
arbitrary corpus bytes.

### Per design

| Design | Result |
| --- | --- |
| **it1** | **Incomplete — fails a careful reading of A.** Case 7 and §1.1 assert immutability and `PACKAGE_INSTANCE_REWRITE_REJECT` via “publication registry checksum” / “package-checksum validation.” The failure mode described for a **citation display typo** is framed as failing **package** checksum when the **citizen** file changes. If package instance bytes are only the manifest (pins), rewriting the citation member file leaves the package checksum unchanged while id/version still “resolve.” §2.1 resolution steps list structural schema validate + display match — **not** registry-byte verify of the resolved citizen. Input B is intended to be covered; Input A is under-specified and bypassable if only package-level checksums exist. |
| **it2** | **Survives on paper.** Resolution algorithm step 3: resolve pin to published citation, validate schema **and registry bytes**. Defect `CITATION_IMMUTABILITY_VIOLATION` when published package/citation bytes differ. Case 7: offering changed bytes for C@v1 rejects; P@v1 still resolves historical C@v1. Production condition only: the existing publication registry path must cover citation citizens, not merely schema files. |

### Verdict contribution

it1’s lifecycle story names Article 9 but does not close the member-byte trust
path that ADR-0027 already requires for package membership generally. it2
states the missing check.

---

## CIT-A5 — Closure / membership leaks (co-location, orphans, role canon)

**Class:** decision-blocking where exclusive projection or role-canon monotony is
unstated; production condition for inbound-orphan policy.  
**Applies to:** it1 weaker; it2 stronger.

### Attack A — co-located unpinned citation becomes active

**Input.** Closed package `P` pins form-field and rules but **no** citation
member. Corpus directory also contains `cite.irc.extra@v1.json` (well-formed).
Loader/renderer walks the content tree, or a “citation registry” side index
loads every `citation.v1` file, and presents/resolves that cite for the field
because the field’s human label mentions “§61.”

**Expected:** Reject participation. ADR-0027 decisions 1 and 7: paths and
co-location are not membership; exclusive execution/render projection is the
resolved member graph only. Unpinned citizens may sit on disk for authoring but
must not resolve or render as adopted.

### Attack B — second membership authority

**Input.** Side file `citations-manifest.json` or URL cache lists adopted cites
not pinned in `artifact-package` members.

**Expected:** Reject. Package is sole adoption authority (ADR-0027; plan hard
constraint).

### Attack C — role token without role-canon generation

**Input.** Package admits schema generations that both use role token
`citation`, but generation G2 reinterprets `citation` as an executable
dependency / derivation edge rather than explanatory content. Additive role enum
still contains the string `citation`.

**Expected:** Reject load-time role-semantic divergence (ADR-0027 decision 2:
immutable role canon; monotony of token meaning).

### Attack D — citation member with no inbound attachment

**Input.** Package pins `citation` member C but no form-field/rule attaches to
C.

**Expected:** Design choice. If the design claims bidirectional closure for
citation members, reject (`CITATION_CLOSURE_INVALID`). If not claimed, orphan
members are inert content — non-blocking so long as they cannot affect
derivation/render without an attachment.

### Per design

| Design | Result |
| --- | --- |
| **it1** | **Fails A/C as stated; silent on exclusive projection.** Requires outbound pin resolution (case 5 `CLOSURE_MISSING_CITATION`) — good for attached refs. Does **not** restate exclusive projection or forbid directory/side-index adoption of citation citizens. Extends the package role **enum** with `"citation"` but does not pin a new **role-canon generation** or monotony check (the ACM-era hole). Attack D: no inbound rule; orphans allowed. |
| **it2** | **Survives A/B/C/D on paper.** “No directory scan, URL cache, side registry, or co-located file can make a citation adopted.” Package remains only membership authority. “New immutable role-canon generation” for the `citation` role. Bidirectional closure: every citation member must be inbound-reachable from a field or rule attachment (`CITATION_CLOSURE_INVALID`). |

### Verdict contribution

it1’s membership story is “pin the role and resolve outbound,” which is
necessary but not the full ADR-0027 floor (exclusive graph + role-canon
monotony). it2 carries that floor forward for citations.

---

## CIT-A6 — Attachment leak (semantics smuggled through cites)

**Class:** production condition for it1; it2 survives.  
**Applies to:** both; wording gap on it1.

### Attack A — rule citation alters evaluation

**Input.** Rule R publishes `tax.line.2b` with normal `when`/`value`. R also
carries a citation pin to C. A “helpful” evaluator or future resolver refuses to
publish unless C’s locator is “active,” or multiplies confidence, or injects
guard terms derived from C’s details (e.g. treat IRC §61 cite as implying
interest is included).

**Expected:** Citation pins are descriptive/explanatory only. They must not
alter `when`, `value`, `publishes`, blocking, output ownership, or create a
derivation edge (plan attachment leak; Article 11; ADR-0010/0026 posture for
non-derivation joins).

### Attack B — form-field citation alters disposition

**Input.** Field dispositions declare normal `blocked` / `computed_zero`
instructions. Citation pin present. Renderer blanks the cell or swaps
explanation whenever citation resolution is soft-failed, or treats “verified
cite” as permission to invent closure.

**Expected:** ADR-0012: dispositions and rendering honesty unchanged; citation
is source-meaning content, not a sixth disposition or a license to invent state.

### Per design

| Design | Result |
| --- | --- |
| **it1** | **Soft gap.** Introduces rule `citation_refs` “to support tracing rule computation branches to legal authorities” without an explicit non-semantic / non-derivation fence. Form-field path keeps dispositions elsewhere (survive B if renderer stays ADR-0012-pure). Attack A is not foreclosed by contract text — only by hope that implementers stay thin. |
| **it2** | **Survives.** “Rule citations are explanatory metadata only. They neither alter `when`, `value`, blocking, output ownership, nor create a derivation edge.” Field citation “changes no field disposition, symbol binding, or rendering authority.” |

### Verdict contribution

Not a current schema hole so much as a missing normative fence on it1. Classify
production condition: successor ADR text must copy it2’s non-semantic clause if
it1’s pin surface is carried.

---

## CIT-A7 — Display / spelling games (it1)

**Class:** decision-blocking for it1 CIT-P2 (canonicalization claim). it2
survives by **not claiming** display canon.  
**Applies to:** it1 primary (role brief: display games).

### Attack A — generator drift (non-deterministic / code-version canon)

Same as CIT-A3 Attack B, specialized to acceptance tables: published package
that validated under runner 1.0 fails under runner 1.1 after format string
change, without any content act. **Expected:** impossible if display canon is
content; inevitable if canon is loader code.

### Attack B — empty / whitespace display with rich details

**Input.** `display: ""` or `display: "   "` with complete IRC details.

**Expected:** If display is required and canonical, reject. Empty must not
pass as “structured cite present.”

### Attack C — bypass: details fields ignored by formatter

**Input.** IRC details `{title:"99", section:"61", subsection:"a", paragraph:"4"}`
with display exactly `IRC Sec. 61(a)(4)` (formatter ignores `title`).

**Expected:** Either title participates in the canonical string / equality
check, or title is not required structure. A required field that never affects
the advertised canonical check is false structure — authors can park arbitrary
tokens in `title` while the UI shows a clean Sec. 61 cite.

### Attack D — IRS free-string spelling variants as multiple “canons”

**Input.** Two citizens, same real document, different `doc_id` spellings:
`"Form 1040 Instructions"` vs `"1040 Instructions"` vs `"Instr. 1040"`, each
with display generated from its own `doc_id`. Both “canonical.”

**Expected:** If the design claims to prevent “user-visible spelling
inconsistencies,” free `doc_id` without a closed vocabulary or adopted document
registry fails that claim. Structural self-consistency is not spelling
discipline across citizens.

### Attack E — non-canonical lookalikes that match a weak generator

**Input.** Details omit subsection; display `IRC Sec. 61`. Later human expects
`(a)(4)` because id is `cite.irc.26.61.a.4`. Id is opaque (ADR-0003) — OK —
but product surfaces that trust id mnemonics diverge from checked display.

**Expected:** Opaque ids must not be a second display channel. Survive if
only `display`+details are shown; fail if any path renders the id as the cite.

### Per design

| Design | Result |
| --- | --- |
| **it1** | **Fails A, C, D; survives B partially.** `display` `minLength: 1` rejects empty (B empty string); whitespace-only may still pass `minLength` depending on implementation — unspecified. Formatter omits `title` → Attack C passes validation while required `title` is ornamental. IRS `doc_id` is free `minLength: 1` → Attack D. Generator-in-resolver → Attack A. No statement that ids are non-display. |
| **it2** | **Survives by non-claim.** No `display` property; “makes no claim of a canonical display string: that would need a separately adopted rendering contract.” Spelling/display games are out of CIT-P2 scope as written — correctly deferred. |

### Verdict contribution

it1’s headline CIT-P2 mechanism (canonical display) does not withstand its own
advertised goal under A/C/D. That is decision-blocking for accepting it1’s
resolver depth as settled.

---

## CIT-A8 — Locator games (it2 primary; it1 baggy IRS)

**Class:** production condition for honest “schema-closed locator” claims;
escalates to decision-blocking only if a design asserts discrimination is already
settled while the sketch does not enforce it.  
**Applies to:** it2 primary (role brief: locator games); it1 IRS bag.

### Attack A — family / locator mismatch

**Input (it2 sketch).**

```json
{
  "schema": "citation.v1",
  "id": "demo.citation.mismatch",
  "version": "v1",
  "authority_family": "us-code",
  "scope": {"tax_year": 2025, "jurisdiction": "US-FED", "family": "demo"},
  "locator": {
    "document_id": "Form 1040 Instructions",
    "edition_tax_year": 2025
  }
}
```

i.e. US-Code family with IRS-document locator shape (or the reverse).

**Expected:** Hard reject (`CITATION_SCHEMA_INVALID` / structure invalid).
Family and locator must be a closed discriminated pair.

### Attack B — enum expansion without locator schema

**Input.** New authority family token `state-code` or `treas-reg` appears in
runner code or a patched enum while locator `oneOf` still only knows us-code /
irs-document. Or runner special-cases the new family.

**Expected:** Unadmitted schema generation rejects (ADR-0027 d3). Family enum
growth is a **new schema generation + role/content admission**, never a runner
branch (Article 11). Empty “extension hook” that validates any locator under a
new enum value fails closedness.

### Attack C — free-string locator tokens that only look structured

**Input.** `us-code` locator `{title:"26", section:"61 or 62", subdivisions:[]}`
or `section:"61; see also Pub 550"`. Schema type string/integer only.

**Expected:** If the design claims closed structural validation, tighter
patterns / subdivision grammar must reject garbage — or the design must admit
that structure is coarse and legal parsing is out of scope (honest residual).

### Attack D — it1 IRS_AUTHORITY bag encodes anything

**Input (it1).** `authority: "IRS_AUTHORITY"`, `details.doc_id: "26 U.S.C. §61(a)(4)"`,
`tax_year: 2025`, display matching formatter from that doc_id.

**Expected:** Either IRC must use the IRC family (reject cross-encoding) or the
design admits IRS_AUTHORITY is an unstructured bag and does not claim family
discipline beyond two enum labels.

### Per design

| Design | Result |
| --- | --- |
| **it1** | **Survives A-style IRC/IRS `allOf` if/then for the two families; fails D.** IRC vs IRS_AUTHORITY branches constrain `details`. But IRS_AUTHORITY is a **single bag** for forms, instructions, pubs, Rev. Proc., Rev. Rul., Treas. Reg. with only `doc_id`/`tax_year`/(optional page/location). Attack D parks Code text in `doc_id` and still “verifies.” Patterns on IRC section help; IRS side is free text with a costume. |
| **it2** | **Acknowledged sketch risk on A; better family split; C residual.** Design text: “The real successor schema must make the family/locator pairing discriminated” — paper admission that the illustrative `oneOf` is not yet enforcement-grade (JSON Schema properties-only branches are a known soft trap). Families are split more cleanly than it1’s IRS bag. Attack B is correctly pushed to schema generations. Attack C: constraints are promised (“schema-declared”) but not specified — honest residual if not overclaimed; production condition for patterns. |

### Verdict contribution

Neither design is wrecked by locator games if they only claim coarse structure.
it1’s weaker family taxonomy plus “verifiable” language (CIT-A2) compounds.
it2’s discriminator caveat is a production condition on schema authoring, not a
silent hole, **provided** the conforming ADR does not paste the soft sketch as
normative without fixing discrimination.

---

## CIT-A9 — Soft package outcome (“never abort loading”)

**Class:** decision-blocking for it1 CIT-P2.  
**Applies to:** it1; it2 survives.

### Attack

**Input.** Package with one malformed citation member and one perfect
computation graph for line 2b. Validator records `CANONICAL_DISPLAY_MISMATCH`
or `MEMBER_SCHEMA_INVALID` as a `MemberIssue` inside `PackageValidation`.

**Expected:** Contained validation means **continue collecting issues**
(ADR-0006 decision 3), not **adopt/execute an invalid package**. Citation
defects that the design classifies as reject must yield `ok=false` /
not-adopted / not-executable (plan cases 3–5, 7). Soft-loading a package with
unresolved cites resurrects false verifiability at the package boundary.

### Per design

| Design | Result |
| --- | --- |
| **it1** | **Fails as written.** §2.2: “citation resolution failures **never abort package loading**. The validator records defects as `MemberIssue` objects and returns them within `PackageValidation`.” Examination cases say “Rejected,” but the design’s normative resolver section does not say `ok=false` / adoption barred. The tension is implementable as “load with warnings,” which breaks residual-closed integrity. |
| **it2** | **Survives.** Collects all defects, then: “Any citation defect makes the package **invalid for adoption/execution**, but does not abort validation or erase issues for unaffected members.” Matches ADR-0006 d3 correctly. |

### Verdict contribution

it1 conflates **non-aborting validation pass** with **successful load**. That is
a CIT-P2 decision-blocking ambiguity.

---

## Cross-cut: Gate-2 mandatory cases (adversary lens)

| Case | it1 | it2 |
| --- | --- | --- |
| 3 opaque residual | Hard reject on v2 shape only; v1 admission / dual-read not closed (A1) | Hard reject + anti-co-equal migration text (A1) |
| 4 malformed structure | Schema + display mismatch; display path broken (A7) | Family/locator structure; discriminator must be real (A8) |
| 7 lifecycle | Named; member-byte path incomplete (A4) | Named with registry bytes (A4) |
| 5 registry (pref) | Package closure only; “verifiable” overclaim (A2) | Honest static-only; no legal_verified (A2) |
| 6 Article 11 (pref) | Fetch/applicability out; formatter-in-runner in (A3) | Fetch/applicability/overreach issue class (A3) |

---

## Verdicts

| Proposition | it1 | it2 |
| --- | --- | --- |
| **CIT-P1** — identity and authority model | **Conditionally accept** the convergent shape (versioned citation citizen + exact pins + package role), **only if** residual-closed packages cannot admit opaque `form-field.v1` strings as co-equal cites (A1), the `citation` role is admitted through an immutable role-canon generation (A5), exclusive projection forbids co-located/side-index activation (A5), and rule/field attachment is fenced as non-semantic (A6). Family taxonomy (IRC vs baggy `IRS_AUTHORITY`) is weaker than it2 but not by itself decision-blocking for identity. | **Conditionally accept.** Stronger residual-closed and membership story (A1, A5), explicit non-semantic attachment (A6), cleaner family split. Production conditions: real discriminated family/locator schema (A8), residual-closed generation matrix that excludes opaque strings (A1). |
| **CIT-P2** — resolver and load-time integrity | **Reject** as settled. Decision-blocking: false “verifiable/resolved” overclaim without corpus or qualified status (A2); canonical display enforced by runner formatter (A3, A7); incomplete citizen-byte immutability chain (A4); soft “never abort package loading” outcome (A9). Display games A/C/D show the claimed spelling/canonical mechanism does not hold. | **Conditionally accept.** Structural-and-adoption-only resolver, `statically_resolved` terminology, registry-backed bytes, adoption reject on any citation defect, and explicit overreach class match the floor. Production conditions: wire publication-registry checks for citation citizens (A4); finish enforcement-grade locator discrimination and patterns (A8); keep any future corpus as a **separate** versioned contract that cannot silently widen this resolver (A2). |

### Comparative note (high-value split)

The designs **converge** on the P1 citizen+pin+package-member skeleton. The
adversary value is concentrated in **P2 depth**: it1 adds display
canonicalization and “verifiable” language that the attacks break; it2 refuses
those claims and survives. Prefer carrying it2’s resolver honesty and
membership fences; treat it1’s display formatter as **not** ratifiable without
moving canon into versioned content (or dropping the claim).

---

## Advisory boundary

This review is advisory. It does not repair designs, modify other files,
commit, launch seats, or draft ADR-0029. Owner/foreman decide carry-forward
after governance review is available under independent process.
