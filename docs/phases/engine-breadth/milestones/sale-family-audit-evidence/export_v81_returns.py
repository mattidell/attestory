"""Export the act lists of every return the published core v81 test runs.

Evidence for docs/phases/engine-breadth/milestones/sale-family-audit.md (P0).
The returns are the ones ``tests/test_code_b_sales_v81.py`` pins in
``tests/fixtures/code_b_sales_v81/expected.json``: the 98 Track 0 cases, the
88 v80 returns and the 27 neighbour probes. They are built by that test's own
``build_world`` and ``run`` setup, unchanged, in this process only; this
script is run as its own process so that setup (which pins the code B
harness's module state, as the test does) never shares a process with
``audit_harness.py`` or ``rerun_v81.py``.

    python3 docs/phases/engine-breadth/milestones/sale-family-audit-evidence/export_v81_returns.py <out.json>

``<out.json>`` must be outside the repository: the act lists are large and
are rebuilt on demand, not committed.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
sys.path.insert(0, str(REPO))


def main() -> None:
    out = Path(sys.argv[1]).resolve()
    if REPO in out.parents:
        raise SystemExit("write the act lists outside the repository")
    from tests import test_code_b_sales_v81 as t

    world = t.build_world()
    world.cbp.pin("v81")  # the test's run() pins v81 before it builds and runs a case
    exported: dict[str, dict[str, object]] = {}
    for group in t.GROUPS:
        exported[group] = {}
        for name in sorted(t.EXPECTED[group]):
            exported[group][name] = world.builds[group][name]()
    out.write_text(json.dumps(exported) + "\n", encoding="utf-8")
    print({group: len(cases) for group, cases in exported.items()})


if __name__ == "__main__":
    main()
