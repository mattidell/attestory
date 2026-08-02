# Adversary Review R1 — D1 Real-Data Residency Boundary

Seat: Adversary (High), crux seat — leak is irreversible. Scope: the CONVERGED
design = union of it1 (incumbent) + it2 (rival). Read: both builds + examinations,
plan, both builder charters, Constitution Art. 18, E18.1–E18.3, Ontology
(quarantine, sensitivity inheritance, synthetic-by-default), ADR-0030 §C.8,
`tests/test_kernel_fixtures.py`. Repo grounding (read-only): `.git/hooks/` holds
only samples (no gate installed); `.gitignore` roots = `local-data/ uploads/
private-archive/ generated/user/`; remote is HTTPS `github.com/mattidell/attestory`
(credentials via helper/keychain, reachable by raw `git`). No files written, no git
writes, all markers synthetic.

## Attack 1 — 17th crossing surface to a remote

Probed the envelope union: it2 scans content, paths, names, modes, symlink targets,
trees/metadata, ref+tag names, patch/bundle/archive members, LFS/gitlink/alternate,
PR/API text, CI artifacts, terminal/telemetry, clipboard; it1 adds tag annotations
(R7), any-ref rev-list (notes), ref names, author fields. Named coverage is
**complete** — no unnamed ref/object surface reaches a remote. Two residuals:
- **`git add` → loose object + `.git/index`, no commit.** Charter target names "its
  index." No git event fires on `add`; both gates trigger only at commit/push. A
  synthetic `w2-JQP.pdf` staged-but-uncommitted sits in `.git/objects` + index with
  no gate. **Not-blocking** — local-only, inside the owner trust boundary; both
  builds' no-carry-to-remote argument holds (it1 surface 15). Flag: the "reaches the
  index" target is technically met ungated.
- **`git bundle` / `format-patch` / outbound API have no git-native hook.** it2
  NAMES them but the "classifier runs before creation/send" gate is a wrapper git
  does not provide. This is the Attack-3 seam, not a new surface. **Not-blocking** at
  Rung 2 (named + deferred to guarded transport), but see Attack 3.

Verdict: surface enumeration holds. Clean bill on remote crossing surfaces.

## Attack 2 — Load-bearing ignore / marker denylist (§C.8) — DECISION-BLOCKING (it1)

it1's R4 is a fixed absolute-prefix denylist `{/Users/,/private/,/home/}` **plus "the
resolved residency pointer value."** Synthetic bootstrap at `/Volumes/tax-live/` (a
plausible external-SSD choice) matches none of the three prefixes. R4 catches it
only if the scan is configured with the resolved pointer value — which lives in the
ignored pointer file / `TAXLIVE_WORKSPACE` env. A **fresh clone or CI** (no pointer,
no env) degrades R4 to the 3-prefix denylist and a report/commit-message containing
`/Volumes/tax-live/JQP-w2.pdf` (synthetic) **crosses**. This makes the scan's
completeness depend on ignored/local mutable state — exactly the load-bearing posture
§C.8 forbids. Force-add and the 3 known prefixes are caught (R1, R4 as probed), so
the *demonstrated* cases pass; the gap is the unanticipated absolute root. **it2**
forbids "any concrete locator/fragment/canonicalized path" categorically by
provenance, not by prefix — stronger — but its detector is still a "private-locator
form" heuristic over content whose provenance attestation may falsely read "public,"
so a novel path form (`\\host\share`, `/mnt/…`) is not guaranteed caught either.
**Decision-blocking against it1's marker screen; the union only mitigates via it2's
provenance rule and is not airtight.** Fix: locator screen must be provenance/allow-list
based (declare the permitted synthetic-path grammar; deny all other absolute forms),
never a prefix denylist, and must not require the ignored pointer value to be complete.

## Attack 3 — Hook bypass: closed or relocated?

`.git/hooks/` is empty of gates today and the remote is HTTPS with cached
credentials → raw `git push` works now. `git push --no-verify` **skips pre-push**;
it1 case 3 only proved commit-side `--no-verify` then relied on pre-push, and never
addresses `push --no-verify`. it1's backstops are the entrypoint hook-presence check
(does not stop `--no-verify`) and **CI detection + "purge-and-rotate"** — a
detective, post-publication remedy on a third-party remote that §C.8 says cannot
un-publish. **it1's purge-and-rotate reliance is decision-blocking-adjacent** (treats
the private remote as a safety net). **it2** is the only real closure: "remote
credentials/transport available only through the guarded push path" — moving the
boundary from *is a hook present?* to *are raw transport credentials reachable
outside the wrapper?* This **relocates, and only closes if credentials are
genuinely unreachable by raw git** — which the current keychain/helper setup
violates. Both correctly name guarded transport as a production condition (Gate 7).
**Not-blocking for Rung-2 CONTRACT ratification only if the ADR adopts it2's
credential-custody framing and drops it1's remote purge-and-rotate as load-bearing.**
As the incumbent stands, the push seam is not closed.

## Attack 4 — Shape alone carries a real value (D1-P2) — DECISION-BLOCKING (it1)

it1's D1-P2 is extract-then-fill: real doc → shape descriptor (field names, kinds,
**observed list cardinality**, **observed closure structure**) → synthetic fill. Its
token-intersection check guards VALUES only; it1 states "field names cross by
design." Three shape channels each carry a real datum:
- **Field-name channel.** Real doc field `acct_9921_JQP` (synthetic stand-in for a
  payer/account-derived key) crosses verbatim — it is "the shape," value-check exempt.
- **Cardinality channel.** Real doc with N=7 foreign-account lines → it1 fixture
  reproduces exactly 7; a sensitive count is a real value carried as shape.
- **Closure-topology channel.** Observed present-box set {A,F,K} unique to the real
  person's circumstances is copied into the fixture — a fingerprint that "discloses
  the shape of their circumstances" (Ontology §sensitivity inheritance).

**it2 closes all three:** its shape grammar is declared from **public** form specs/
schemas, **excludes any feature whose only authority is a live document, observed
strings, and observed string lengths**, and uses **cardinality classes** + a
public covering array; the live doc may only SELECT a public profile inside
quarantine and is never a generator input. Observed field names, exact counts, and
observed closure never cross. **Length channel is closed by BOTH** (it1's descriptor
omits lengths; it2 excludes them explicitly). Because D1-P2 ratifies as ONE rule and
it1's leaks by design, **the union does not rescue it** — the committee must adopt
it2's independent-construction rule (or amend it1 to bar observed field names /
exact cardinality / observed closure). **it1's D1-P2 does not survive; it2's does.**

## Attack 5 — Ambiguity → third class (fail-closed totality)

Both collapse "cannot decide" to `NEVER_CROSSES` (it1 default-deny R0; it2 rule 4:
missing/overlapping/unknown/unreadable → `NEVER_CROSSES:missing_may_cross_proof`).
I could not exhibit an artifact that yields no decision — **totality holds; the
third class is genuinely unrepresentable.** The reachable weakness is *wrongly-decided*,
not *undecided*: an artifact whose personal provenance is hidden behind a false
"public-origin" attestation is decided `MAY_CROSS`, backed only by content screens
that Attacks 2/4 already evade. One subtle synthetic case: it2 D1-P2 lets a live doc
"reveal a coverage defect" so the owner expands the public grammar — the SET of
profiles added right after each live session leaks which boxes the real doc had.
it2's rule decides this fixture `MAY_CROSS` (the generator input was public), so
totality still holds, but a personal shape-selection channel survives the decision.
**Not-blocking on the totality claim** (it holds); flag the selection-pattern channel
as a D1-P2 residual to name in the ADR (require the coverage-expansion decision log
to stay in quarantine).

## Rung-2 survival verdict

- **D1-P1 — SURVIVES ONLY AS THE UNION, WITH TWO BINDING CONDITIONS.** The residency
  location rule, the total fail-closed binary classifier, and commit+independent-push
  gate contracts are sound (Attacks 1, 5). But (a) the locator screen must be
  provenance/allow-list based, not it1's prefix denylist, and must not depend on the
  ignored pointer value (Attack 2, decision-blocking against the incumbent); and (b)
  the push seam is closed only by it2's guarded-transport credential-custody — it1's
  purge-and-rotate on the remote is not load-bearing-safe under §C.8 (Attack 3).
  With both adopted, D1-P1 is settled at Rung 2; on it1's design alone it is **not**.
- **D1-P2 — SURVIVES ONLY AS it2's RULE.** it1's extract-then-fill leaks observed
  field names, exact cardinality, and observed closure topology as shape (Attack 4,
  decision-blocking). it2's independent-construction-from-public-grammar rule
  (live doc selects, never supplies) closes them and settles D1-P2 at Rung 2,
  provided the coverage-expansion decision log stays quarantined (Attack 5 residual).

Two decision-blocking findings (Attack 2 incumbent locator screen; Attack 4 incumbent
D1-P2) and one blocking-adjacent (Attack 3 incumbent remote-purge reliance). The
converged subset converges only if the committee takes it2's provenance-based locator
rule, it2's guarded-transport framing, and it2's independent-construction D1-P2 —
not the incumbent's on those three points.
