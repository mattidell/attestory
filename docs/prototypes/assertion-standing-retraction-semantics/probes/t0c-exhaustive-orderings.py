"""T0-C probe: exhaust every ordering of retractions within one relation.

The committed test `TestOrderedRetractabilityOnRealContent` executes all 42
*ordered pairs* of the richest declared relation as its backstop, because the
prefix-closure argument already settles the question and a full exhaustion is
too slow for the fast lane. This probe is the full exhaustion the findings
file cites: all 5,040 orderings of the SSA-1099 relation (box 5 plus its six
declared companion witnesses), executed through the real admission boundary.

It reuses the test module's own content-driven fixture builder, so there is
exactly one fixture implementation and this probe cannot drift from the test.

Run from the repository root:  python3 <this file>
"""
from __future__ import annotations

import itertools
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

from tests.test_assertion_standing_track0 import (  # noqa: E402
    _RELATION_GROUPS,
    TestOrderedRetractabilityOnRealContent as Harness,
)


def main() -> int:
    label, types, family = _RELATION_GROUPS[6]
    assert "ssa1099" in label, label

    harness = Harness(methodName="test_every_relation_participant_is_covered")
    harness.setUpClass()
    acts, finding_ids, _, next_index = harness._build(types, family)

    print(f"relation: {label}")
    print(f"participants: {len(types)}")

    admitted: list[tuple[str, ...]] = []
    total = 0
    for length in range(1, len(types) + 1):
        for order in itertools.permutations(types, length):
            total += 1
            outcome = harness._attempt(
                acts, next_index, [finding_ids[t] for t in order]
            )
            if outcome == "admitted":
                admitted.append(order)

    full = len(list(itertools.permutations(types)))
    print(f"orderings tried (all lengths 1..{len(types)}): {total}")
    print(f"  of which full-length orderings: {full}")
    print(f"admitted orderings: {len(admitted)}")
    for order in admitted:
        print("   ADMITTED:", " -> ".join(t.split(".")[-1] for t in order))

    if admitted:
        print("\nRESULT: set B is NON-empty for this relation -- some order works.")
        return 1
    print(
        "\nRESULT: no order of retractions reaches any participant of this "
        "relation. Set B is empty, as the committed test asserts."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
