"""Track 4 repair: package validation does not silently skip checks for v39.

Core calculations v39 is the first package on ``artifact-package.v35``. The
nominee return cross-checks were keyed to package versions v37 and v38 only,
and the exact entrypoint-pin check to an explicit list of package schemas
that stopped before v35. Each case below mutates the published v39 package
and shows the check now catches it.
"""
from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path
from typing import Any

from packages.derivation.loader import DerivationSchemas
from packages.derivation.package_validation import package_instance_checksum, validate_package

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "packages" / "content" / "tax" / "2025"
V39 = CONTENT / "package.core-calculations.v39.json"
SCHEDULE_B = "tax.us.2025.rule.attachment.schedule-b"


def _corpus() -> dict[tuple[str, str], dict[str, Any]]:
    corpus: dict[tuple[str, str], dict[str, Any]] = {}
    for path in CONTENT.glob("*.json"):
        body = json.loads(path.read_text("utf-8"))
        if isinstance(body, dict) and isinstance(body.get("id"), str) and isinstance(body.get("version"), str):
            corpus[(body["id"], body["version"])] = body
    return corpus


def _package() -> dict[str, Any]:
    package: dict[str, Any] = json.loads(V39.read_text("utf-8"))
    return package


def _codes(package: dict[str, Any], corpus: dict[tuple[str, str], dict[str, Any]] | None = None) -> set[str]:
    package["package_checksum"] = package_instance_checksum(package)
    result = validate_package(package, corpus if corpus is not None else _corpus(), DerivationSchemas())
    return {issue.code for issue in result.issues}


class V39NomineeCrossChecks(unittest.TestCase):
    def test_published_v39_validates(self) -> None:
        self.assertEqual(_codes(_package()), set())

    def test_v39_rejects_split_attachment_and_line2b_pins(self) -> None:
        package = _package()
        package["members"] = [
            {**member, "version": "v6"} if member["id"] == SCHEDULE_B else member
            for member in package["members"]
        ]
        package["entrypoints"] = [
            {**entry, "version": "v6"} if entry["id"] == SCHEDULE_B else entry
            for entry in package["entrypoints"]
        ]
        self.assertIn("NOMINEE_RETURN_SUCCESSOR_GRAPH_MIXED", _codes(package))

    def test_v39_rejects_divergent_schedule_b_and_line2b_nominee_symbols(self) -> None:
        corpus = _corpus()
        schedule_b = copy.deepcopy(corpus[(SCHEDULE_B, "v7")])
        nominee_row = schedule_b["itemizations"][0]["adjustment_rows"][0]
        nominee_row["selection"]["paths"][1]["subtotal_symbol"] = "demo.wrong-derived-nominee-subtotal"
        corpus[(SCHEDULE_B, "v7")] = schedule_b
        self.assertIn("NOMINEE_RETURN_SYMBOL_MISMATCH", _codes(_package(), corpus))

    def test_a_later_version_is_checked_without_another_edit(self) -> None:
        package = _package()
        package["version"] = "v40"
        package["members"] = [
            {**member, "version": "v6"} if member["id"] == SCHEDULE_B else member
            for member in package["members"]
        ]
        self.assertIn("NOMINEE_RETURN_SUCCESSOR_GRAPH_MIXED", _codes(package))


class V35EntrypointPins(unittest.TestCase):
    def test_v35_rejects_a_stale_entrypoint_version(self) -> None:
        package = _package()
        self.assertEqual(package["schema"], "artifact-package.v35")
        package["entrypoints"] = [
            {**entry, "version": "v0"} if entry["id"] == "tax.us.2025.rule.sli-statement-loan-support" else entry
            for entry in package["entrypoints"]
        ]
        self.assertIn("ENTRYPOINT_VERSION_MISMATCH", _codes(package))

    def test_v35_rejects_a_dangling_entrypoint(self) -> None:
        package = _package()
        package["entrypoints"] = [*package["entrypoints"], {"id": "demo.rule.no-such-member", "version": "v1"}]
        self.assertIn("ENTRYPOINT_DANGLING", _codes(package))


if __name__ == "__main__":
    unittest.main()
