"""E5.2 (Containment) - No staging of accepted input.

Detection per the Engineering Constraints: kill the session after each
acceptance step; accepted input must already be workspace state.
"""

import tempfile
import unittest
from pathlib import Path

from packages.kernel.act_log import ActLog
from packages.kernel.read_models import build_read_model
from tests.support import (
    act,
    demo_bundle,
    demo_entity,
    demo_evidence,
    demo_finding,
    registry_with_demo_kinds,
)


class TestE52NoStaging(unittest.TestCase):
    def test_accepted_act_survives_session_object_loss(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            schema_dir = root / "schemas"
            schema_dir.mkdir()
            registry = registry_with_demo_kinds(schema_dir)
            workspace = root / "workspace"

            session_log = ActLog(workspace, registry)
            session_log.append(act(0, "bundle-adoption", {"bundle": demo_bundle()}), 0)
            session_log.append(
                act(1, "entity-introduced", {"entity": demo_entity("demo-corp-a", "Corp A")}),
                1,
            )
            session_log.append(
                act(2, "evidence-submitted", {"evidence": demo_evidence()}),
                2,
            )
            session_log.append(
                act(3, "assertion", {"finding": demo_finding("accepted-finding")}),
                3,
            )

            del session_log

            restarted = ActLog(workspace, registry)
            contents = restarted.read()
            self.assertEqual(contents.revision, 4)
            model = build_read_model(contents.acts, registry)
            self.assertEqual(model["current"]["finding_ids"], ["accepted-finding"])


if __name__ == "__main__":
    unittest.main()
