# Engineering Health Roadmap

## Opening milestone — Faster Feedback, Cheaper Workspace Replay

[Plan](milestones/test-replay-performance.md).

Improve CI feedback first. Establish a reproducible account of repeated fact
lattice construction and history replay. Reduce that work without changing
accepted records, refusals, current findings or saved results. Keep the full
regression gate and the existing behavioral tests.

## After the opening milestone

The opening milestone delivered bounded fold-local lattice reuse. It reduced
CPU on the measured correction story while missing the fixed construction-count
target by 22. The [measurement note](milestones/test-replay-performance-evidence/measured-performance.md)
records both results and their limits; current publication status belongs to
the pull request and its checks. The owner wants further investigation after
landing; the next milestone and implementation remain unselected.

1. **Locate the remaining cost.** Use completed CI evidence and retained
   profiles first. Where those cannot identify the next bottleneck, measure a
   bounded representative case. Distinguish repeated engine work, repeated
   setup or catalog construction, and genuinely different behavior exercised
   by long tests. Do not rerun the whole suite just to reproduce a passing run.
2. **Ask what each expensive test protects.** Compare actual assertions and
   entrypaths, not test names. Identify whether another retained test catches
   the same defect, or whether a shorter focused test can do so. A shared final
   amount does not make two correction or recovery stories redundant. Retain
   real recording, replay, saved-output and cross-component witnesses where
   they provide distinct assurance.
3. **Examine useful suite boundaries.** Map dependencies between the kernel,
   derivation, content and application code. Consider focused component
   suites alongside integration tests. Test grouping may need no production
   restructuring; separate deployable modules are a larger choice to justify,
   not a prerequisite for quicker feedback. Any selective suite must account
   for changes that affect its neighbors and preserve an authoritative full
   integration gate.
4. **Choose the next bounded change.** Compare expected CPU savings, feedback
   time, implementation cost and assurance lost or retained. Bring back
   specific candidates for further engine work, demonstrably redundant tests,
   or component suites. Finding that a costly test is worth keeping is a
   legitimate result. Review proposed removals and boundary changes before
   implementing them.

CI sharding, broader indexing and partial catalog construction remain options,
not selected mechanisms. Parallel jobs can shorten waiting without reducing
total CPU; report those benefits separately. The investigation should produce
a justified next step, not a mandatory application reorganization.
