# Round 4 Expressiveness Review — Source Completeness

Date: 2026-07-12  
Seat: expressiveness, Medium tier  
Evidence rung: 4; shape A only

## Method

Read the round-4 and repair4 charters, the repair4 surface module and tests, the repair1 resolver, and the prior round reviews. Per the seat rule, I ran the repair4 test suite before reading `examination-repair4.md`; I did not read any same-round peer review or commit-message bodies.

Commands run:

```bash
cd docs/prototypes/source-completeness/repair4
python3 -m unittest -v test_surface
```

Result: 12 tests passed. I also ran the suite using python3's discovery from the repository root, confirming clean reachability.

## Measurements

| Check | Result | Evidence |
|---|---|---|
| Charter coverage | Pass | The 12 cases in `test_surface.py` map every charter case: `test_true_publishes_zero_with_exact_pin` (true closure/pin), `test_present_members_omit_closure_pins` (present aggregation/input pins), `test_negatives_block_through_publication` (six negatives), `test_duplicate_mapping_entries_block` (duplicate mapping), `test_stale_first_current_second_pins_successor` (stale pin succession), and `test_inputs_are_the_exact_values_used_for_resolution_and_pins` (exact inputs). |
| Reproduction | Pass | My independent runs verified that the 12 tests pass successfully, matching the execution and test results claimed in the builder's examination. |
| Schema authority | Pass | Positive mappings and true closure findings publish and pin correctly. Negative/invalid types, duplicate mapping, and superseded findings block publication inside the single entry point. |
| Hard distinctions | Pass | Explicitly enforces: closure-backed zero (zero sum on empty rows with valid closure) vs. computed zero (handled by normal summation) vs. blocked (raises `Blocked`); true vs. false/absent/superseded findings; and fact values (member rows) vs. findings (`ClosureFinding`) vs. source instances. |
| Honesty audit | Pass | The examination accurately discloses the test-local nature of all mutants, lists blocked negatives, and names the production-only routing residuals. |

## Finding

**The selected shape-A surface successfully collapses the evaluation boundary to one validated entry point with no reachable bypass.**

By replacing the multiple entry points and public helper callables of repair3 with a single public function (`compute`) that handles resolution and evaluation internally in one atomic step, repair4 closes the duck-carrier and alternate-callable bypasses:
1. **No duck-carrier injection:** Because the public `compute` function signature does not accept a carrier object (only the raw mapping and findings), a `DuckAuthority` cannot be passed without raising a `TypeError` (tested in `test_duck_carrier_has_no_public_parameter_to_enter`).
2. **Mutant isolation:** The direct-raw (`_collect`), presence-only, and duck-carrier mutant paths are confined exclusively to the test file. The runtime module (`surface.py`) exports only `compute` via `__all__`, and inspection confirms no alternate evaluator exists.

All prior completeness, value, currency, and pin guarantees are fully retained.

## Disposition

The validated shape-A path reproduces all chartered expressiveness and negative-blocking requirements. The selected surface is **sufficient** for the SC-P1 construction question. The three named residuals (production dispatch, adopted-mapping identity, and persisted displacement) are correctly classified as production-only routing facts. No broader production, schema, or persistence conclusions follow.
