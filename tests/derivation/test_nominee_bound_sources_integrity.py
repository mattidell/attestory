"""ADR-0074 declaration and dependency-integrity kills 1, 2, 4, 5, 7."""

from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path
from typing import Any

from packages.derivation.authorization_closure import (
    package_boundary_digest,
    rule_scoped_closure,
)
from packages.derivation.loader import DerivationSchemas
from packages.derivation.package_validation import validate_package
from packages.tax.nominee_consequences import RULE_ID

CONTENT = Path(__file__).resolve().parents[2] / "packages" / "content" / "tax" / "2025"
EXAMPLES = (
    Path(__file__).resolve().parents[2]
    / "packages"
    / "sample_data"
    / "derivation"
    / "examples"
)
ALLOCATION_VOCAB = "tax.us.nominee-allocation.vocabulary"
REDUCTION_VOCAB = "tax.us.2025.interest.nominee-reduction.vocabulary"


def _load_content(name: str) -> dict[str, Any]:
    loaded: dict[str, Any] = json.loads((CONTENT / name).read_text("utf-8"))
    return loaded


def _load_example(name: str) -> dict[str, Any]:
    loaded: dict[str, Any] = json.loads((EXAMPLES / name).read_text("utf-8"))
    return loaded


def _tiny_package(members: list[dict[str, Any]], entrypoints: list[dict[str, Any]]) -> dict[str, Any]:
    package = _load_example("artifact-package.v28.json")
    package["id"] = "demo.package.nominee-integrity"
    package["members"] = members
    package["entrypoints"] = entrypoints
    package["admitted_schemas"] = sorted(
        {
            "rule-artifact.v8",
            "bundle.v2",
            "citation.v1",
        }
    )
    return package


def _pin(citizen: dict[str, Any], *, role: str) -> dict[str, Any]:
    return {
        "id": citizen["id"],
        "role": role,
        "schema": citizen["schema"],
        "version": citizen["version"],
    }


class BoundSourcesIntegrity(unittest.TestCase):
    def setUp(self) -> None:
        self.schemas = DerivationSchemas()
        self.rule = _load_content("rule.interest.nominee-reduction.json")
        self.alloc_vocab = _load_content("nominee-allocation.bundle.json")
        self.reduction_vocab = _load_content("nominee-reduction.bundle.json")
        self.citation = _load_content("citation.interest.nominee-reduction.json")

    def _corpus(self, *citizens: dict[str, Any]) -> dict[tuple[str, str], dict[str, Any]]:
        return {(c["id"], c["version"]): c for c in citizens}

    def _codes(self, result: Any) -> set[str]:
        return {issue.code for issue in result.issues}

    def test_kill_1_unknown_bound_sources_name(self) -> None:
        rule = copy.deepcopy(self.rule)
        blob = json.dumps(rule)
        rule = json.loads(blob.replace("tax.us.nominee-allocation.amount", "tax.us.nominee-allocation.amont"))
        package = _tiny_package(
            [
                _pin(rule, role="computation"),
                _pin(self.alloc_vocab, role="fact-type-bundle"),
                _pin(self.reduction_vocab, role="fact-type-bundle"),
                _pin(self.citation, role="citation"),
            ],
            [
                {"id": rule["id"], "version": rule["version"]},
                {"id": REDUCTION_VOCAB, "version": "v1"},
            ],
        )
        result = validate_package(
            package,
            self._corpus(rule, self.alloc_vocab, self.reduction_vocab, self.citation),
            self.schemas,
        )
        self.assertIn("BOUND_SOURCE_TARGET_UNDECLARED", self._codes(result))

    def test_kill_2_omitted_allocation_vocabulary(self) -> None:
        package = _tiny_package(
            [
                _pin(self.rule, role="computation"),
                _pin(self.reduction_vocab, role="fact-type-bundle"),
                _pin(self.citation, role="citation"),
            ],
            [
                {"id": RULE_ID, "version": "v1"},
                {"id": REDUCTION_VOCAB, "version": "v1"},
            ],
        )
        result = validate_package(
            package,
            self._corpus(self.rule, self.reduction_vocab, self.citation),
            self.schemas,
        )
        self.assertFalse(result.ok, result.issues)
        self.assertIn("BOUND_SOURCE_TARGET_UNDECLARED", self._codes(result))

    def test_kill_7_no_binding_path(self) -> None:
        demo_rule = _load_example("rule-artifact.v8.bound-sources.json")
        package = _load_example("artifact-package.v28.json")
        result = validate_package(package, self._corpus(demo_rule), self.schemas)
        self.assertIn("MEMBER_NO_BINDING_PATH", self._codes(result))

    def test_kill_4_and_5_authorization_closure(self) -> None:
        corpus = {
            self.rule["id"]: self.rule,
            self.alloc_vocab["id"]: self.alloc_vocab,
            self.reduction_vocab["id"]: self.reduction_vocab,
            self.citation["id"]: self.citation,
        }
        package = {
            "version": "synthetic",
            "entrypoints": [{"id": RULE_ID, "version": "v1"}],
            "input_bindings": [],
        }
        closure = rule_scoped_closure({RULE_ID}, corpus, package=package)
        ids = {cid for cid, _version in closure}
        self.assertIn(ALLOCATION_VOCAB, ids)
        digest = package_boundary_digest({RULE_ID}, corpus, package=package)
        mutated = copy.deepcopy(self.alloc_vocab)
        mutated["label"] = mutated["label"] + " mutated"
        corpus_mutated = dict(corpus)
        corpus_mutated[ALLOCATION_VOCAB] = mutated
        digest_mutated = package_boundary_digest({RULE_ID}, corpus_mutated, package=package)
        self.assertNotEqual(digest, digest_mutated)

    def test_missing_or_malformed_citation_fails_loudly(self) -> None:
        """No manufactured citation pin.

        A pin is a provenance claim. Inventing CITATION_ID when the adopted
        citizen declares nothing would assert an authority the run never read,
        so the coordinator refuses instead of papering over a content defect.
        The adopted v1 rule and v36 package are unchanged and still declare it.
        """
        from packages.tax.nominee_consequences import NomineeCitationError, _citation_pin

        adopted = json.loads(
            (
                Path(__file__).resolve().parents[2]
                / "packages"
                / "content"
                / "tax"
                / "2025"
                / "rule.interest.nominee-reduction.json"
            ).read_text("utf-8")
        )
        pin = _citation_pin(adopted)
        self.assertEqual(pin["role"], "citation")
        self.assertEqual(pin["id"], adopted["citations"][0]["id"])
        self.assertEqual(pin["version"], adopted["citations"][0]["version"])

        for broken in (
            {"id": "demo.rule", "citations": []},
            {"id": "demo.rule"},
            {"id": "demo.rule", "citations": [{"version": "v1"}]},
            {"id": "demo.rule", "citations": [{"id": "demo.cite"}]},
            {"id": "demo.rule", "citations": [{"id": "", "version": "v1"}]},
            {"id": "demo.rule", "citations": ["not-a-mapping"]},
        ):
            with self.assertRaises(NomineeCitationError):
                _citation_pin(broken)

    def test_kill_4_authorization_closure_on_the_real_v36_package(self) -> None:
        """Kill 4 computed on the concrete v36, not a synthetic four-citizen corpus.

        The companion test above proves the edge exists in isolation; this one
        proves it survives the real member graph, which is what the plan's kill 4
        actually claims (Track 1 review, non-blocking 2).
        """
        content = Path(__file__).resolve().parents[2] / "packages" / "content" / "tax" / "2025"
        package = json.loads((content / "package.core-calculations.v36.json").read_text("utf-8"))
        corpus: dict[str, dict[str, Any]] = {}
        for path in sorted(content.glob("*.json")):
            value = json.loads(path.read_text("utf-8"))
            if isinstance(value, dict) and "id" in value and "schema" in value:
                corpus[value["id"]] = value
        closure = rule_scoped_closure({RULE_ID}, corpus, package=package)
        ids = {cid for cid, _version in closure}
        self.assertIn(ALLOCATION_VOCAB, ids)


if __name__ == "__main__":
    unittest.main()
