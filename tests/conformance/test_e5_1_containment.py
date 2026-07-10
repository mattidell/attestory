"""E5.1 (Containment) - Destroy and rebuild.

Detection per the Engineering Constraints: destroy every store except
the workspace, rebuild, and diff authoritative state. The projection
cache here is intentionally disposable.
"""

import tempfile
import unittest
from pathlib import Path
from typing import Any

from packages.kernel.act_log import ActLog
from packages.kernel.read_models import build_read_model, read_projection, write_projection
from tests.support import (
    act,
    demo_bundle,
    demo_entity,
    demo_evidence,
    demo_finding,
    registry_with_demo_kinds,
)


class TestE51Containment(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.root = Path(self._tmp.name)
        schema_dir = self.root / "schemas"
        schema_dir.mkdir()
        self.registry = registry_with_demo_kinds(schema_dir)
        self.log = ActLog(self.root / "workspace", self.registry)

    def _append_workspace(self) -> None:
        acts: tuple[dict[str, Any], ...] = (
            act(0, "bundle-adoption", {"bundle": demo_bundle()}),
            act(1, "entity-introduced", {"entity": demo_entity("demo-corp-a", "Corp A")}),
            act(2, "evidence-submitted", {"evidence": demo_evidence()}),
            act(3, "assertion", {"finding": demo_finding("finding-current", value=1200)}),
        )
        for index, workspace_act in enumerate(acts):
            self.log.append(workspace_act, expected_revision=index)

    def test_destroy_projection_cache_and_rebuild_zero_diff(self) -> None:
        self._append_workspace()
        cache_path = self.root / "projection-cache" / "workspace-read-model.json"

        first = build_read_model(self.log.read().acts, self.registry)
        write_projection(cache_path, first)
        cached = read_projection(cache_path)
        self.assertEqual(cached, first)

        cache_path.unlink()
        rebuilt = build_read_model(self.log.read().acts, self.registry)
        write_projection(cache_path, rebuilt)

        self.assertEqual(rebuilt, first)
        self.assertEqual(read_projection(cache_path), first)


if __name__ == "__main__":
    unittest.main()
