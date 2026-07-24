# Harness seed (reference only)

Proof-of-concept check scripts extracted from cycle-5 reviewer work. **Not
runnable as-is** — they assume a local headless Chrome over CDP, ephemeral ports,
and Node with WebSocket/fetch; original absolute scratchpad paths were rewritten
to relative references to `../prototypes/cycle5-{a,b}/walk.html`. Value is the
**check logic**, not the plumbing:

- `run.mjs` — full T1/T2/T3 + a11y battery driver over CDP.
- `identity.mjs` — citation-identity-under-reuse: normalized-DOM diff across reused-fact sites.
- `faultinject.mjs` — live fault injection (guard monkeypatch / `FIXTURE` mutation) + on-page-signal / leak scan.
- `checkfocus3.mjs` — keyboard reachability + `:focus-visible` via real CDP `Input.dispatchKeyEvent` (not `.focus()`).
- `checkblockedB.mjs` — blocked-line `role="alert"` + section-vs-banner salience delta.
- `check16.mjs` — blocked line carries no numeral.

The process-economy milestone should reconstruct these as one committed,
path-agnostic, fixture-driven harness (see `../../analysis/04-economy.md`, L1).
All data referenced is synthetic (`demo-*`).
