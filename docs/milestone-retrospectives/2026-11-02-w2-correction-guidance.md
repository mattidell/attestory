# Retrospective — W-2 Correction Guidance

## Lessons

The v2 surface projects saved W-2 values, calculation disposition, and
authorization currentness from the existing ActLog, coordinator report, and
saved presentation. The legacy v1 surface remains unchanged; no tax route,
second outcome record, or authorization workflow was added.

- A successful save does not prove every line calculated; absent authorization
  is not a calculation failure. A blocked null is unavailable, not zero.
- After a post-save calculation failure, prior figures stay labeled as prior
  and latest calculation/currentness remain unknown.
- Validation rejection is a known pre-save outcome. Network uncertainty and
  unusable successful responses do not confirm a new snapshot.
- HTTP 200 is insufficient: parse and shape-check bounded JSON before
  installation, on both submit and state read. Failed checks keep the last
  confirmed view and prevent resubmission.
- Recovery is a state read in the same running session; it does not restart
  the process or rerun calculation. The earlier v6 and controlled blocked
  cases carried no safe question sentence, so the general fallback remains
  necessary. With the existing v69+ metadata, the v70 saved presentation can
  carry a mapped closure question when every blocked root reached from the
  line is an unconfirmed family with a declared question; the compiled-page
  check confirms that bounded case. This does not make every dependency block
  diagnosable.

## What it cost

Preserving published v1 bytes required a v2 surface successor and its existing
adoption/release/registry/manifest integrity chain. Compiled-page checks used
the synthetic recorder/coordinator and loopback responses to separate saved
state from response state, including malformed-success and recovery-GET cases.
No protocol/schema framework or durable outcome ledger was needed.

## Follow-ups

- Keep exact question guidance tied to a saved outcome's mapped closure root;
  never infer it from a missing derived symbol.
- Decide process-restart recovery and automatic recalculation retry separately,
  with explicit state and authorization boundaries.
- Broaden internal-error guidance only when evidence supplies a useful,
  user-safe next action; do not build a refusal-code catalogue.
- Keep final publication contingent on curated-candidate review and its
  exact-head CI result.

## What future work should carry forward

Treat transport success and payload usability as different conditions. Test
unusable successful bodies after the real save path, assert that recovery does
not duplicate the contribution, and keep saved facts, calculated figures, and
permission to rely on them distinct in both the page and its evidence.
