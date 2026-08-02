# Examination: Dividend Composition (D3, Incumbent It1)

**D3-P2 (Ordinary-Dividend Composition & Universe): Settled at Rung 1**
**D3-P3 (Qualified Subset Enforcement): Settled at Rung 2**

## Cases Examined

1. **Two positives:** (a) Single statement 1a=900, 1b=600. Fact is admitted, composes to 3b=900, 3a=600. (b) Two statements (900/600 and 400/0). Facts admit. Summing over the closed family yields 3b=1300, 3a=600. Both lines publish.
2. **Subset kill-case (mandatory):** A statement with 1b=600, 1a=400.
   - *Claim:* Dies at admission via new `invariants` check.
   - *Probe:* A throwaway probe against `_validate_finding` confirms JSON schema cannot block it natively, but a fact-type invariant expression throws `FindingModelError("finding ... violates invariant: box_1b <= box_1a")`. The statement is never recorded.
3. **Line-level subset by construction:** 
   - *Claim:* 3a <= 3b holds by construction because the composition definition atomically reads a single family horizon. Summing A and B where every b_i <= a_i guarantees sum(b_i) <= sum(a_i). The single-horizon guard prevents divergence.
4. **Out-of-universe box 2a (mandatory):** A statement with 1a=900, 1b=600, 2a=100.
   - *Claim:* Admits and records. Composition ignores 2a. Lines 3a and 3b publish normally. D2's contradiction check queries the family for `box_2a > 0` and produces a return-level blocked disposition with a trace back to the statement. Box 7 acts identically but lacks the D2 query.
5. **Empty family closes honestly:** A declared family with no statements closes on the current horizon. Subtotals evaluate to 0, publishing 3a=0, 3b=0. An undeclared family fails the closure read, blocking the lines.
6. **Universe creep (mandatory):** Composing 2a into any line is unrepresentable. The composition schema explicitly defines `div_ordinary` mapped to `box_1a` and `div_qualified` mapped to `box_1b`. There is no slot for `box_2a`, making it structurally impossible to compose it into a line without redefining the canonical schema.
