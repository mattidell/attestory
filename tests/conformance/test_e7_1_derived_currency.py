"""E7.1 (Supersession) - Derived currency.

Detection per the Engineering Constraints: recompute currency from the
act log alone; diff against any materialization; mismatch is the
violation.
"""

import tempfile
import unittest
from pathlib import Path
from typing import Any

from packages.kernel.act_log import ActLog
from packages.kernel.currency import (
    CurrencyMaterializationError,
    assert_materialization_matches,
    compute_currency,
)
from packages.kernel.findings import project
from tests.support import (
    act,
    demo_bundle,
    demo_entity,
    demo_evidence,
    demo_finding,
    registry_with_demo_kinds,
)


class TestE71DerivedCurrency(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        root = Path(self._tmp.name)
        schema_dir = root / "schemas"
        schema_dir.mkdir()
        self.registry = registry_with_demo_kinds(schema_dir)
        self.log = ActLog(root / "workspace", self.registry)

    def _append_workspace(self) -> tuple[dict[str, Any], ...]:
        acts = (
            act(0, "bundle-adoption", {"bundle": demo_bundle()}),
            act(1, "entity-introduced", {"entity": demo_entity("demo-corp-a", "Corp A")}),
            act(2, "evidence-submitted", {"evidence": demo_evidence()}),
            act(3, "assertion", {"finding": demo_finding("finding-old", value=1200)}),
            act(4, "assertion", {"finding": demo_finding("finding-new", value=1300)}),
        )
        for index, workspace_act in enumerate(acts):
            self.log.append(workspace_act, expected_revision=index)
        return acts

    def test_currency_recomputes_from_act_log_and_matches_materialization(self) -> None:
        self._append_workspace()
        contents = self.log.read()
        state = project(contents.acts, self.registry)
        view = compute_currency(state)

        self.assertEqual(contents.revision, 5)
        self.assertEqual(view.current_finding_ids, frozenset({"finding-new"}))
        self.assertEqual(view.displaced_finding_ids, frozenset({"finding-old"}))
        assert_materialization_matches(
            view,
            {
                "findings": {
                    "finding-old": {"current": False},
                    "finding-new": {"current": True},
                }
            },
        )

    def test_mutation_stale_current_flag_is_caught(self) -> None:
        self._append_workspace()
        view = compute_currency(project(self.log.read().acts, self.registry))
        with self.assertRaises(CurrencyMaterializationError):
            assert_materialization_matches(
                view,
                {
                    "findings": {
                        "finding-old": {"current": True},
                        "finding-new": {"current": True},
                    }
                },
            )


if __name__ == "__main__":
    unittest.main()
