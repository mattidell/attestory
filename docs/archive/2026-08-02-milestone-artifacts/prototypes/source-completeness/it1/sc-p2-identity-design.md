# SC-P2 — 1099-INT Source-Instance Identity (incumbent design, it1)

Rung 1, paper only. Precedent: ADR-0011 §2-3 — a W-2 wage fact is keyed by the
W-2 *slip as a thing* (employer + tax-year + W-2-slip citizen), never by
evidence; two slips are two facts; a corrected value for the same slip
supersedes the same fact.

## The analogue, chosen

W-2 wages arrive on slips; 1099-INT interest arrives on **accounts** at a
**payer**. The account is the thing the box-1 figure is *about* across original
and corrected statements. So the chosen identity key for a box-1 taxable-interest
fact is:

```
identity = payer citizen + account citizen + tax-year   (+ enclosing scope)
```

- **payer citizen** and **account citizen** are peers to evidence (Article 1),
  exactly as the W-2-slip citizen is peer to evidence in ADR-0011 §2. They are
  *things* the user names, not documents. A scan/upload/statement/evidence id is
  forbidden from the key.
- **tax-year** literal, mirroring the closure fact type and the W-2 key.
- **statement / 1099-INT document is deliberately NOT in the key.** That is the
  whole correctness pivot: an original and a corrected 1099-INT for the same
  (payer, account, year) are the *same fact*, answered again.

Fact type: `tax.us.2025.interest.box1` (schema `fact-type.v1`, kernel family per
ADR-0011 §1), `nature: determinable`, `value_schema` numeric, supersession
`free` (correctable attestation).

## Instances

**positive — one payer, two accounts, under the CHOSEN key (distinct).**
Payer `P-first-federal`, accounts `A-checking` and `A-savings`, both 2025.
Keys `(P-first-federal, A-checking, 2025)` and `(P-first-federal, A-savings,
2025)` differ in the account component → **two facts**, aggregated by the
interest rule exactly as two W-2 slips aggregate. This is the W-2 two-slip
fixture translated to interest.

**positive — same-fact correction preserving identity.** Original 1099-INT for
`(P-first-federal, A-checking, 2025)` box 1 = `500.00` → finding `int-v1`.
Payer issues a *corrected* 1099-INT, same account, box 1 = `520.00` → finding
`int-v2`. Same identity key ⇒ `int-v2` **supersedes** `int-v1` under the fact
type's policy (ADR-0011 §3). ADR-0010 currency displaces any derived interest
total pinning `int-v1`; re-derivation publishes the successor total. The
corrected *document* changed evidentiary standing only (Article 1); it did not
rekey the fact.

## Rejected rivals (worked here to show the collisions)

**rival key: payer + tax-year only (no account) — REJECTED, collides.**
Both accounts map to key `(P-first-federal, 2025)` → the two-account positive
case collapses to **one fact**; the second account's box 1 either overwrites or
is lost. This is ADR-0011's rejected "key wages only by employer and year,"
reproduced: two slips / two accounts from one payer collide. Falsifies the key.

**rival key: payer + account + statement-id — REJECTED, breaks correction.**
Original and corrected 1099-INT carry different statement ids, so
`(P, A, 2025, stmt-orig)` ≠ `(P, A, 2025, stmt-corrected)` → the correction
becomes a **new fact**, not a supersession → same-fact history is lost and the
interest total double-counts `500 + 520`. Correction can no longer preserve
identity. Rejected.

**negative — evidence/document-keyed candidate — REJECTED by Article 1.**
Keying by the uploaded 1099-INT scan/document id (or making the statement id a
*document* id) puts evidence in the fact's identity. Forbidden: Article 1
Peerage — "a fact's identity never derives from a file" — and ADR-0011 §2, which
forbids a scan, upload, replacement document, or evidence id in identity keys.
Rekeying on re-upload would rewrite the question. Rejected before it can be
fixtured as positive.

## Lifecycle trace (original → corrected → displacement)

1. `int-v1` = 500.00 for `(P-first-federal, A-checking, 2025)` asserted.
2. Interest total rule collects current box-1 findings → total pins `int-v1`.
3. Corrected 1099-INT → `int-v2` = 520.00, same key, supersedes `int-v1`.
4. `int-v1` superseded ⇒ the total's pin superseded ⇒ total **displaced**
   (ADR-0010, Article 12). History accumulates; nothing edited.
5. Rerun collects current `int-v2` → publishes the successor total (520.00 for
   that account, plus other accounts).

## Interaction with closure (feeds SC-P3, question 4)

"That's all my interest income" is a **source-family** closure over
`tax.us.2025.interest`, not a statement about any one `(payer, account)`
instance. The identity key individuates *members*; closure closes the *family*.
The two are compatible precisely because the family is a named scope (SC-P3),
independent of member keys — so a family with zero current members is still a
well-defined thing a closure finding can close (that is the closure-backed-zero
case in SC-P1 (a)). No member key participates in the closure fact's identity
(its key is tax-year only), so adding/removing accounts never rekeys closure.
