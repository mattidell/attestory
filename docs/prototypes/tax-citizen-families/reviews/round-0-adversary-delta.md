# Round 0 Adversary Delta-Confirmation

- Reviewer: `codex-adversary-delta-2026-07-11`
- Date: 2026-07-11
- Subject: v1-to-v2 charter amendment against the six prior adversary findings
- Scope: bounded delta-confirmation only; no new design review

I reviewed `charter-it1.md` v2 against the six findings in
`round-0-adversary.md`. I did not read the same-round governance delta or any
commit-message body before submitting this review. The official IRS material
used for the prior attack remains the relevant primary-source context: the
[2025 Form 1099-INT instructions](https://www.irs.gov/instructions/i1099int),
the [2025 Form W-2/W-3 instructions](https://www.irs.gov/pub/irs-prior/iw2w3--2025.pdf),
the [2026 Form W-2/W-3 instructions](https://www.irs.gov/instructions/iw2w3),
and the [2025 Form 1040](https://www.irs.gov/pub/irs-prior/f1040--2025.pdf).

## Prior findings

### A1 — Missing 1099-INT edge fixture

**Status: closed.** F2 now requires a box 1 taxable-interest positive and a
paired negative or blocked non-box-1 case, naming early-withdrawal penalty,
U.S. Savings Bond/Treasury interest, tax-exempt interest, and nominee
allocation as available pressures. It also explicitly forbids relying on
“taxable interest” as an unstated filter. This closes the prior attack at the
charter level; candidate evidence still has to execute the fixture.

### A2 — Document identity versus fact identity

**Status: closed.** F1 now requires same employee, same employer, and same tax
year identity pressure through distinct source instances or a corrected/
reissued source. It also requires an evidence replacement/removal mutation and
requires fact identity and finding content to remain stable while evidentiary
standing changes. This is the requested collision and peerage probe.

### A3 — Absence, zero, invalidity, and non-existence

**Status: partially closed.** F5 now requires the four-state matrix: present
zero, closed empty source set, unclosed source set, and present schema-invalid
value. It requires distinct declared block reasons and no exception text for
unclosed and invalid states. F7 adds blocked-invalid and false-guard cases,
requires the false guard and inapplicable disposition to be named, and forbids
findings for blocked or false-guard non-existence.

The remaining gap is that v2 does not explicitly require an explanation
assertion or explanation-walk result for each of the four matrix states. The
prior disposition requested that assertion so a candidate cannot merely emit
the right status code while leaving the distinction unrecoverable. The
candidate examination should therefore add evidence for all four explanation
paths, or the foreman should amend the charter before builder dispatch.

### A4 — Citation authority and operative meaning

**Status: closed.** F8 now requires a resolved citation with document identity,
tax-year applicability, and a precise locator; it adds locator/year mutation;
and it requires parity showing citation text cannot change evaluation output.
The amendment directly supplies the missing validation and non-operative
boundary checks.

### A5 — Evolution and version boundaries

**Status: closed.** The charter now fixes the main positive slice at tax year
2025 and reserves a later-year source/form change for the evolution probe. F9
requires old-year and later-year positives, a mixed-year negative, an
immutability check for old schemas/artifacts, and an account of persistent ids,
changed versions, new citizens, and generation/migration implications.

### A6 — Coverage recomputation and stale projection

**Status: closed.** F11 now requires deleting and rebuilding coverage from the
act log/read models and derivation records, byte comparison, and a stale
“closed” projection test while the closure act remains open. It requires the
stale projection to be ignored or rejected, which makes the non-authoritative
and recomputable boundary measurable.

## Observations

- The amendment is within the original charter scope; it does not introduce a
  new citizen family or decide the pending contract questions in advance.
- F12 strengthens the evidence gate by requiring strict positive/negative
  validation, declared failure reasons, no coercion, and an undeclared-shape or
  wrong-version negative. This supports the prior attacks but does not replace
  the behavioral probes in F1-F11.
- The remaining A3 gap is evidence-shape precision, not a new fixture family.

## Dissent and recommendation

I do not recommend opening the builder seat yet unless the foreman accepts the
A3 partial closure explicitly and requires the four explanation paths in the
builder examination, or amends F5/F7 to state that requirement. With that
qualification recorded, the v2 amendment closes the other five prior attacks
and is otherwise sufficient for bounded builder dispatch.

