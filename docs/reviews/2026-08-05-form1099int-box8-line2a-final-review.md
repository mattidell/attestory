# Final publication review — Form 1099-INT box 8 → line 2a

**Seat:** author-independent Reviewer (publication re-verification after findings repair)
**Range:** curated `origin/main..HEAD` on `milestone/form1099int-box8-line2a`
**Date:** 2026-08-05

## Verdict

**READY** — prior High/Medium findings repaired; mypy gate and P12 full-golden equality closed.

## Repair disposition

| Finding | Disposition |
| --- | --- |
| High — box-9 correction displacement | Fixed: live marshals companions as collect sources; derivation pins same-statement companions (ADR-0010 edges). |
| Medium — companion provenance can silently disappear | Fixed: fail-closed companion load and pin matching; box-13 unit regression. |
| Medium — presentation evidence honesty | Fixed: N7 drives real projector; P12 requires committed golden and `assertEqual(model, golden)`. |
| Blocking — mypy gate | Fixed: eight errors in `test_form1099int_box8_line2a.py` cleared; `python3 -m mypy` clean. |
| Low — closeout docs | Retrospective records repair cycles; obsolete Form 8949 race language removed. |

## Checks

Focused suite green (34). Form 1099-DIV regression + schema registry green. `python3 -m mypy` clean (172 files). Governance lint clean. CI `verify` on the PR head remains the merge gate.
