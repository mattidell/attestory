# Closure Freshness — Incumbent Paper Design (it1)

Rung: paper only. Grounds on Article 7 (derivation/individuation edges — no
third), ADR-0010 (displacement roots = superseded inputs + individuated
entities; derived findings are targets never roots; re-derivation out of scope),
and the ratified source-family semantic contract (a family is a declared claim +
member predicate, coverage presents that claim). All fixtures synthetic.

## The problem, exactly

A closure-backed zero `Z` pins its rule/mapping and the closure attestation `C`,
but **no member finding** (the family was empty). A later member `m1` supersedes
nothing `Z` pinned, so neither existing edge fires: `Z` stays current though the
family is no longer empty. Manual closure withdrawal is not an acceptable
correctness mechanism, and you **cannot pin an absence** to displace on its
arrival.

## CF-P1 — Freshness is horizon-relative

A closure attestation declares a **membership horizon** `H`: the family-scoped
act-log position at attestation (monotonic; not a member set). `C` means "family
F is complete *as of H*." Authority is fresh only while the current family-scoped
act log equals `H`. **Any** later relevant member act on F — assert,
membership-changing correction, or removal — advances F's log past `H`, so
`current(F) ≠ H` and `C` is **stale until re-attestation**. Freshness is
therefore observable and rebuildable purely from acts: `fresh(C) ⇔ latest
relevant F-member-act ⪯ H`. Using a monotonic horizon (not "does the set match
now") is what makes **removal** keep the family stale rather than silently
restoring the old zero.

The horizon is the semantic authority; a family id, label, or coverage rollup
cannot widen or reset it. Re-attestation is the only fresh-making act.

## CF-P2 — Currency reaches the zero through two existing edges

Standing effects, each classified as an existing relation (no third edge, no
reserved derived-finding authority):

- **individuation edge:** each F-member act individuates the entity
  `F-membership(F)`; `C` is individuated over `F-membership(F) @ H`. A later
  member act establishes `F-membership(F) @ H'` (H' ≻ H) that **supersedes** the
  attested individuation → `C` is displaced as an *individuated-entity* root
  (the ADR-0010 root class, reused — not a new edge).
- **derivation edge:** `Z` pins `C` (role `input`), so `C`'s displacement
  propagates `C → Z` along the ordinary derivation edge. `Z` is a target, never a
  root (ADR-0010 dec 5).

So member act → `F-membership(F)` (individuation) → `C` → `Z` (derivation). The
member never needs an edge *to* `Z`; the horizon divergence displaces `C`, and
`C→Z` does the rest.

**The one piece of machinery this needs — named, not hidden.** Displacement must
have a *positively recorded* root; a bare absence cannot be one. So currency must
compute, per family, whether `current(F) ≻ H` and treat that divergence as the
individuation root for `C`. That is a **tiny currency reducer over the act log**
(fold F-member acts → compare to each live closure's horizon → mark divergent
closures displaced). It is exactly the Gate-3 "CF-P2 advances to a small
reducer." It requires **no third edge** (it feeds the existing individuation root
set) and **no reserved T1 derived-finding authority** (it displaces an *input*
attestation via individuation, and never re-derives or re-authors it). The design
does not fail; it succeeds at paper and names the reducer as the next depth.

## Rejected rival (worked to failure)

**Rival: re-derive closure to `false` when members appear.** Model a rule
`members(F) nonempty ⇒ closure(F)=false`, so a derivation edge from members
displaces the zero directly. **Fails on governance, not detail:** closure is an
*attestation* — a user-signed claim (Article 2), and where facts leave an open
path only an act may close it (Article 3). A rule that flips a user's attestation
to `false` makes a judgment operative by computation. So there is no legitimate
derivation edge *member → closure-value*; the only lawful displacement of an
attestation is by supersession or by individuation of what it was attested over.
This is why CF-P1's horizon (individuation) is load-bearing rather than
decorative — the naive derivation-only route is foreclosed.

## Ordered act/state table (synthetic family F; `G` independent)

| # | Act | Effective closure | Zero currency | Coverage of F | Root / edge |
|---|---|---|---|---|---|
| 1 | attest C true, horizon H0=pos0, F empty; run | fresh @H0 | `Z0` **current** | complete @H0 | — (publish; `Z0` pins C) |
| 2 | assert member m1 (pos1) | **stale** (cur≻H0) | `Z0` **noncurrent** | incomplete (m1 ≻ H0) | individ. root `F-membership@pos1` ≻ H0 → C displaced → `C→Z0` |
| 3 | correct m1→m1' (same member id) | stale | `Z0` noncurrent (already) | incomplete | deriv. `m1⊐m1'` displaces the m1 **subtotal** only; membership card. unchanged → **no extra family reopen** |
| 4 | remove/displace m1 (pos3) | **stale** (log ≻ H0) | `Z0` **stays noncurrent** | complete-set but **unattested** | monotonic horizon → **no resurrection** of `Z0` |
| 5 | re-attest C' true, horizon H1=pos3; rerun | fresh @H1 | new `Z1` current; `Z0` still noncurrent | complete @H1 | C' supersedes C; rerun publishes `Z1` pinning C' |
| 6 | rebuild from act log | identical | identical | identical | fold acts → same verdicts (determinism) |
| 7 | on G: assert G-member | G fresh; F per above | G's zero current | G incomplete only if past G's horizon | roots are **per-family**; F-divergence never touches G |

## Producer → authority → edge → currency-consumer → failure map

| Stage | Participant | Carries | Failure |
|---|---|---|---|
| Producer | user asserts member act / attests closure | recorded acts | no act → nothing to fold |
| Authority | closure attestation + declared horizon H (CF-P1) | "complete as of H" | horizon undeclared → divergence undetectable → stale zero survives |
| Edge (individuation) | `F-member act → F-membership(F)@H'` | supersedes attested `@H` | modeled as third edge → Article 7 violation |
| Edge (derivation) | `C → Z` via `Z`'s `input` pin | ADR-0010 propagation | `Z` didn't pin `C` → zero unexplained/undisplaceable |
| Currency consumer | reducer folds acts, flags `current(F)≻H` as C-root | rebuildable currency | reducer absent → the sole real gap; **CF-P2 depth-1 finding** |

Positives: #1 (publish fresh zero), #5 (re-attest → successor). Negatives: #2
(new member → zero noncurrent, no manual withdrawal), #4 (removal → no
resurrection).

## Edge inventory

- Derivation: `member_finding → interest_subtotal`; `closure_C → closure_zero_Z`.
- Individuation: `member_act → F-membership(F)`; `F-membership(F)@H → closure_C`.
- Displacement roots: superseded attestation (re-attestation); **F-membership
  horizon divergence** (the individuation root this design adds to the reducer).
- No third edge; no derived finding acts as a root; no attestation is re-authored.

## Exact pins

`Z0` pins: `{role:field-mapping, rule}`, `{role:adopted, mapping@v}`,
`{role:input, C@v1}`. When stale, `Z0`'s walk still reaches `C@v1` and shows it
displaced by `F-membership(F)@pos1` (individuation). `Z1` (case 5) pins `C'@v1`,
horizon H1 — never the stale `C`. The subtotal (case 3) pins `m1'`, not `m1`.
