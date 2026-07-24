# 05 — Technical Findings

Implementation-level. Feeds economy but focuses on what worked / didn't / limits.

## Worked
- **Single-file HTML + frozen `FIXTURE` + single render path** — robust, zero-dep, inspectable; chosen by all 10 builds independently.
- **Absence-of-key** for "no value" — structural (nothing to read), beats null/0 guards.
- **`createElement`/`textContent`** (repo hook-forced) — removes the injection surface entirely; strengthened zero-authority as a side effect.
- **Per-line / per-section `try/catch` + pre-created DOM slots** — blast containment; a failure writes only its own slot [C3+].
- **Live fault injection** — `Object.freeze` monkeypatch or `FIXTURE` mutation via CDP `addScriptToEvaluateOnNewDocument`; forced the real throw path. Caught defects static reading missed (A's `err.message` echo; A/B blast-granularity divergence) [C5].
- **Contrast via `getComputedStyle` + WCAG luminance recompute** — no library, offline, deterministic.
- **Native `<details>/<summary>`** — free keyboard a11y, zero JS [C5 B-B].
- **Two valid identity mechanisms:** deep `Object.freeze` (prevent divergence) [C4 B-A]; runtime signature-cache (detect divergence) [C4 B-B].

## Didn't work / pitfalls
- **`.focus()` for keyboard/focus-visible checks → false negatives.** Must use real CDP `Input.dispatchKeyEvent` [C5]. → any "mechanized" claim must name its driving technique.
- **Hardcoded self-verify ports (`:8934`) → collisions** [C3]; **shared Playwright MCP browser is a singleton → cross-tab bleed even with random ports** [C2, C4]. Fix: own headless Chrome, fresh `--user-data-dir`.
- **`file://` blocked by the MCP browser** → must serve over local HTTP.
- **`chrome --headless --dump-dom` hangs on exit** (Chrome-for-Testing quirk) → background + timed-kill; macOS lacks `timeout`.
- **Error-text echoing rejected values** = leak channel [C3–C4].
- **Single `try/catch` over a multi-part section** = over-broad blast (hides a correct sibling part) [C4 B-A].
- **Derived/diagnostic arithmetic reading live uncached data** = side-channel surfacing tampered-derived numbers [C4 B-B tie-out].
- **`DESIGN.md` self-claims unreliable** — both builders mis-certified "fail-loud" [C2]; blast/salience claims contradicted by measurement [C5]. → never trust, execute.

## What mattered / didn't
- **Mattered:** execution over static analysis; structural enforcement over guards; browser-isolation topology; check technique.
- **Didn't matter (for correctness):** framework (none used); visual theme (light/dark); aesthetic polish.

## Ideas / limitations
- Offline constraint (no network) → no `axe-core`; a11y checks hand-rolled from DOM/computed-style. Adequate but reimplements a subset.
- "Structurally impossible" in a static HTML file bottoms out at "single frozen source + assertions"; a stronger guarantee wants the invariant enforced **upstream at fixture/product-artifact production**, not in the renderer.
- Race-condition class (concurrent writes to shared fact state) untestable via the synchronous mid-script mutation used here.
- Reference implementations (`../reference/prototypes/cycle5-{a,b}`) satisfy all accumulated criteria and differ mainly on identity mechanism (freeze vs signature) and blast granularity — usable as templates and as harness regression targets.
