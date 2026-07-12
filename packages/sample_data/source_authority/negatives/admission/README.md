# Admission negatives

Audience: Agents

Every instance here is **schema-valid by design** — the defect is only visible
against record state, so JSON Schema cannot reject it. Track 1 commits these as
the agreed corpus; Track 2's atomic-admission machinery must reject each one:

- `act.member-transition.wrong-predecessor.json` — successor references a real
  but superseded horizon (`h0` when `h1` is current). ADR-0017 decision 3.
- `act.member-transition.future-predecessor.json` — successor references a
  horizon never recorded for this family/scope.
- `act.member-transition.replayed-successor.json` — successor id collides with
  an already-recorded horizon (`h1`). Succession ids are never reused.
- `act.horizon-genesis.duplicate.json` — genesis for a family/scope that
  already has a horizon chain.

Rejection must be atomic: neither the member half nor the horizon half of a
rejected transition may take effect (ADR-0017 decision 3).
