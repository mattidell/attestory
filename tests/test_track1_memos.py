"""Track 1 (rust-kernel-experiment): the memos return what the plain paths return.

Synthetic ``demo.*`` data only. Three things are pinned here:

* the content-keyed validation memo in ``production_resolver`` returns the
  same verdict as an unmemoized call, validates identical bytes once, and a
  changed package, member checksum, schema document or validator misses;
* the closure-question walk memo in ``presentation_projection`` gives the
  same reasons as the walk it replaced (copied below verbatim in shape) on
  many random blocked-row graphs, including cycles and shared rows, and a
  changed row changes the answer rather than hitting a stale entry, and a
  two-path synthesized-meaning graph fails if either cycle guard is dropped;
* the validation memo key covers the corpus actually validated, so the same
  checksums with a different corpus miss;
* the marshal fallback's once-computed union of required symbols equals the
  per-rule check it replaced.

The source-family index of package validation is pinned in
``test_track1_validation_index.py`` (it loads the whole published corpus, so it
is an honest live-lane test).
"""
from __future__ import annotations

import copy
import random
import unittest
from typing import Any, Mapping, cast
from unittest import mock

from packages.kernel.currency import CurrencyView

from packages.derivation import production_resolver as pr
from packages.derivation.marshal import _rule_required_symbols, marshal_run_context
from packages.derivation.package_validation import MemberIssue, PackageValidation
from packages.derivation.presentation_projection import (
    _closure_question_reasons, _constraint_meanings, _missing_mentions)


# --- validation memo ---------------------------------------------------------------------------


class _Schemas:
    def __init__(self, docs: dict[str, Any]) -> None:
        self.docs = docs

    def schema_ids(self) -> list[str]:
        return sorted(self.docs)

    def get(self, schema_id: str) -> Any:
        return self.docs[schema_id]


def _package(version: str = "v1") -> dict[str, Any]:
    return {"id": "demo.package", "version": "v1",
            "members": [{"id": "demo.a", "version": version}, {"id": "demo.b", "version": "v1"}]}


class ValidationMemo(unittest.TestCase):
    def setUp(self) -> None:
        pr.clear_validation_memo()
        self.addCleanup(pr.clear_validation_memo)
        self.calls = 0
        self.checks = {("demo.a", "v1"): "aa", ("demo.a", "v2"): "a2", ("demo.b", "v1"): "bb"}
        self.schemas = _Schemas({"s.v1": {"type": "object"}})

        def fake(package: dict[str, Any], corpus: Any, schemas: Any, checks: Any = None) -> PackageValidation:
            self.calls += 1
            issue = MemberIssue("demo.a", package["members"][0]["version"], "DEMO", f"call {self.calls}")
            return PackageValidation(package["id"], False, (issue,), {"x": "demo.a"}, (),
                                     ({"id": "demo.a", "nested": [1, 2]},))

        self.fake = fake

    def run_once(self, package: dict[str, Any], checks: Mapping[Any, str] | None = None,
                 schemas: Any = None) -> PackageValidation:
        with mock.patch.object(pr, "validate_package", self.fake):
            return pr._validate_once(package, {}, cast(Any, schemas or self.schemas), checks or self.checks)

    def test_identical_bytes_validate_once_and_match_the_plain_call(self) -> None:
        first = self.run_once(_package())
        second = self.run_once(copy.deepcopy(_package()))
        self.assertEqual(self.calls, 1)
        self.assertEqual(first, second)
        plain = self.fake(_package(), {}, self.schemas, self.checks)
        self.assertEqual(first.issues, second.issues)
        self.assertEqual(second.resolved_members, plain.resolved_members)

    def test_a_hit_never_shares_mutable_members(self) -> None:
        first = self.run_once(_package())
        first.resolved_members[0]["nested"].append(99)
        second = self.run_once(_package())
        third = self.run_once(_package())
        self.assertEqual(second.resolved_members[0]["nested"], [1, 2])
        second.resolved_members[0]["nested"].append(7)
        self.assertEqual(third.resolved_members[0]["nested"], [1, 2])

    def test_a_changed_package_misses(self) -> None:
        self.run_once(_package())
        self.run_once(_package("v2"))
        self.assertEqual(self.calls, 2)

    def test_a_changed_member_checksum_misses(self) -> None:
        self.run_once(_package())
        self.run_once(_package(), checks={**self.checks, ("demo.b", "v1"): "changed"})
        self.assertEqual(self.calls, 2)

    def test_the_same_checksums_with_a_different_corpus_miss(self) -> None:
        corpus_a: dict[tuple[str, str], dict[str, Any]] = {("demo.a", "v1"): {"id": "demo.a", "n": 1}}
        corpus_b: dict[tuple[str, str], dict[str, Any]] = {("demo.a", "v1"): {"id": "demo.a", "n": 2}}
        with mock.patch.object(pr, "validate_package", self.fake):
            pr._validate_once(_package(), corpus_a, cast(Any, self.schemas), self.checks)
            pr._validate_once(_package(), copy.deepcopy(corpus_a), cast(Any, self.schemas), self.checks)
            self.assertEqual(self.calls, 1)  # an equal corpus still hits
            pr._validate_once(_package(), corpus_b, cast(Any, self.schemas), self.checks)
        self.assertEqual(self.calls, 2)  # identical checksums, different corpus: a miss

    def test_a_changed_schema_document_misses(self) -> None:
        self.run_once(_package())
        self.run_once(_package(), schemas=_Schemas({"s.v1": {"type": "array"}}))
        self.assertEqual(self.calls, 2)

    def test_a_different_validator_misses(self) -> None:
        self.run_once(_package())

        def other(package: dict[str, Any], corpus: Any, schemas: Any, checks: Any = None) -> PackageValidation:
            self.calls += 1
            return PackageValidation(package["id"], True, (), {}, (), ())

        with mock.patch.object(pr, "validate_package", other):
            result = pr._validate_once(_package(), {}, cast(Any, self.schemas), self.checks)
        self.assertTrue(result.ok)
        self.assertEqual(self.calls, 2)

    def test_the_memo_is_bounded(self) -> None:
        for index in range(pr._VALIDATION_MEMO_LIMIT + 3):
            package = _package()
            package["note"] = f"demo.{index}"
            self.run_once(package)
        self.assertEqual(len(pr._VALIDATION_MEMO), pr._VALIDATION_MEMO_LIMIT)


# --- closure walk memo -------------------------------------------------------------------------


def _reference_reasons(row: Mapping[str, Any], *, resolved_members: Any, by_symbol: Any,
                       symbol_fact_types: Any = None, later_any_arm_refs: bool = False,
                       refusal_sentence: Any = None, refusal_token: Any = None,
                       constraint_meanings: Any = None) -> list[dict[str, Any]]:
    """The closure walk as it stood before the memo: re-walks every path, no index."""
    questions: dict[str, str] = {}
    input_questions: dict[str, str] = {}
    for member in resolved_members:
        schema = str(member.get("schema", ""))
        question = member.get("closure_question")
        family = member.get("family")
        if schema.startswith("source-closure-mapping.") and isinstance(question, str) and question.strip() \
                and isinstance(family, Mapping):
            questions[str(family.get("id"))] = question
        asked = member.get("question")
        fact_type = member.get("fact_type")
        if schema.startswith("input-question.") and isinstance(asked, str) and asked.strip() \
                and isinstance(fact_type, Mapping):
            input_questions[str(fact_type.get("id"))] = asked
    families: set[str] = set()
    facts: set[str] = set()
    extras: set[str] = set()
    meanings = constraint_meanings or {}

    def meaning_for(current: Mapping[str, Any], key: str) -> Any:
        artifact = str(current.get("artifact_id") or "")
        marker = ".member-validation.synthesized"
        if artifact.endswith(marker):
            family_id = artifact[: -len(marker)]
            for member in resolved_members:  # the rescan the index replaced
                if str(member.get("id")) != family_id:
                    continue
                owned = _constraint_meanings([member])
                if key in owned:
                    return owned[key]
        return meanings.get(key)

    def explain(current: Mapping[str, Any], key: str) -> bool:
        sentence = meaning_for(current, key)
        if sentence:
            extras.add(sentence)
            return True
        if refusal_sentence and refusal_token and key == refusal_token:
            extras.add(refusal_sentence)
            return True
        return False

    def reach_mixed(current: Mapping[str, Any], seen: frozenset[str]) -> bool:
        missing = current.get("missing")
        if not isinstance(missing, list) or not missing:
            return False
        for entry in missing:
            key = str(entry)
            if key in seen:
                continue
            if key in questions:
                families.add(key)
                continue
            if explain(current, key):
                continue
            blocked = [r for r in by_symbol.get(key, []) if r.get("disposition") == "blocked"]
            if blocked:
                if not all(reach_mixed(r, seen | {key}) for r in blocked):
                    return False
                continue
            bound = (symbol_fact_types or {}).get(key, key)
            if bound in input_questions:
                facts.add(bound)
                continue
            if current.get("code") == "SOURCE_SET_UNCLOSED":
                continue
            return False
        return True

    def reach(current: Mapping[str, Any], seen: frozenset[str]) -> bool:
        if later_any_arm_refs:
            return reach_mixed(current, seen)
        if current.get("code") == "SOURCE_SET_UNCLOSED":
            missing = current.get("missing")
            if not isinstance(missing, list) or not missing:
                return False
            families.update(str(family) for family in missing)
            return True
        missing = current.get("missing")
        if not isinstance(missing, list) or not missing:
            return False
        for symbol in missing:
            key = str(symbol)
            if key in seen:
                continue
            if explain(current, key):
                continue
            blocked = [r for r in by_symbol.get(key, []) if r.get("disposition") == "blocked"]
            if not blocked:
                bound = (symbol_fact_types or {}).get(key, key)
                if current.get("code") == "DEPENDENCY_ABSENT" and bound in input_questions:
                    facts.add(bound)
                    continue
                return False
            if not all(reach(r, seen | {key}) for r in blocked):
                return False
        return True

    if (not reach(row, frozenset()) or not (families or facts or extras)
            or any(family not in questions for family in families)):
        reasons: list[dict[str, Any]] = []
    else:
        sentences = ({questions[f] for f in families} | {input_questions[f] for f in facts} | extras)
        reasons = [{"sentence": sentence} for sentence in sorted(sentences)]
    if (refusal_sentence and refusal_token and _missing_mentions(row, by_symbol, refusal_token)
            and not any(reason.get("sentence") == refusal_sentence for reason in reasons)):
        reasons = [{"sentence": refusal_sentence}, *reasons]
    return reasons


def _graph(rng: random.Random) -> tuple[dict[str, Any], dict[str, Any]]:
    symbols = [f"demo.s{i}" for i in range(rng.randint(3, 9))]
    families = [f"demo.fam{i}" for i in range(3)]
    by_symbol: dict[str, list[dict[str, Any]]] = {}
    for symbol in symbols:
        for _ in range(rng.choice([0, 1, 1, 2, 3])):
            pool = symbols + families + ["demo.input", "demo.unknown"]
            by_symbol.setdefault(symbol, []).append({
                "disposition": rng.choice(["blocked", "blocked", "blocked", "published"]),
                "code": rng.choice(["DEPENDENCY_ABSENT", "SOURCE_SET_UNCLOSED", "OTHER"]),
                "missing": rng.sample(pool, rng.randint(0, 3)),
                "artifact_id": rng.choice([f"demo.rule.{symbol}", "demo.famA.member-validation.synthesized",
                                           "demo.famB.member-validation.synthesized"]),
            })
    members: list[dict[str, Any]] = [
        {"schema": "source-closure-mapping.v2", "family": {"id": fam}, "closure_question": f"demo question {fam}"}
        for fam in families[: rng.randint(1, 3)]
    ]
    for fam, symbol in (("demo.famA", "demo.s1"), ("demo.famB", "demo.s1"), ("demo.famA", "demo.s3")):
        members.append({"schema": "source-family.v1", "id": fam,
                        "member_constraints": [{"block_code": symbol, "meaning": f"demo {fam} meaning of {symbol}"}]})
    members.append({"schema": "input-question.v1", "fact_type": {"id": "demo.input"}, "question": "demo input question"})
    row = {"disposition": "blocked", "code": "DEPENDENCY_ABSENT", "artifact_id": "demo.rule.top",
           "missing": rng.sample(symbols, rng.randint(1, min(3, len(symbols))))}
    return row, {"resolved_members": members, "by_symbol": by_symbol}


class ClosureWalkMemo(unittest.TestCase):
    def test_matches_the_unmemoized_walk_on_random_graphs(self) -> None:
        rng = random.Random(20251118)
        answered = 0
        for case in range(1500):
            row, base = _graph(rng)
            options: dict[str, Any] = {
                "later_any_arm_refs": rng.random() < 0.5,
                "refusal_sentence": "demo refusal" if rng.random() < 0.3 else None,
                "refusal_token": "demo.unknown" if rng.random() < 0.3 else None,
                "constraint_meanings": {"demo.s1": "demo meaning", "demo.s3": "demo other"} if rng.random() < 0.4 else None,
                "symbol_fact_types": {"demo.s2": "demo.input"} if rng.random() < 0.3 else None,
            }
            with self.subTest(case=case):
                got = _closure_question_reasons(row, **base, **options)
                want = _reference_reasons(row, **base, **options)
                self.assertEqual(got, want)
                answered += bool(want)
        self.assertGreater(answered, 100)  # the random graphs exercise the true branch too

    def test_shared_blocked_rows_are_walked_once(self) -> None:
        """A diamond of shared rows is linear, not one walk per path."""
        layers = 40
        by_symbol: dict[str, list[dict[str, Any]]] = {}
        for layer in range(layers):
            nxt = [f"demo.l{layer + 1}a", f"demo.l{layer + 1}b"]
            for name in ("a", "b"):
                by_symbol[f"demo.l{layer}{name}"] = [
                    {"disposition": "blocked", "code": "DEPENDENCY_ABSENT", "missing": list(nxt)}]
        by_symbol[f"demo.l{layers}a"] = [
            {"disposition": "blocked", "code": "SOURCE_SET_UNCLOSED", "missing": ["demo.fam0"]}]
        by_symbol[f"demo.l{layers}b"] = [
            {"disposition": "blocked", "code": "SOURCE_SET_UNCLOSED", "missing": ["demo.fam0"]}]
        members = [{"schema": "source-closure-mapping.v2", "family": {"id": "demo.fam0"},
                    "closure_question": "demo question"}]
        row = {"disposition": "blocked", "code": "DEPENDENCY_ABSENT", "missing": ["demo.l0a", "demo.l0b"]}
        got = _closure_question_reasons(row, resolved_members=members, by_symbol=by_symbol)
        self.assertEqual(got, [{"sentence": "demo question"}])  # 2**40 paths unmemoized

    def test_two_paths_to_a_synthesized_row_keep_both_cycle_guards_honest(self) -> None:
        """The row C is reached under two different ``seen`` sets.

        Via P -> K -> C the key ``demo.K`` is in ``seen``, so C is walked
        without explaining K and reaches True through ``demo.fam0``. Via
        Q -> C ``demo.K`` is not in ``seen``, so C explains K and adds its
        family meaning. C's first (True) walk skipped a key it was handed, so
        it must not be cached; and a cached walk must not be reused under a
        ``seen`` that holds a key it examined. Dropping either guard loses
        the family meaning sentence.
        """
        synthesized = "demo.famA.member-validation.synthesized"
        by_symbol = {
            "demo.P": [{"disposition": "blocked", "code": "OTHER", "missing": ["demo.K"],
                        "artifact_id": "demo.rule.p"}],
            "demo.K": [{"disposition": "blocked", "code": "OTHER", "missing": ["demo.C"],
                        "artifact_id": "demo.rule.k"}],
            "demo.C": [{"disposition": "blocked", "code": "OTHER", "missing": ["demo.K", "demo.fam0"],
                        "artifact_id": synthesized}],
            "demo.Q": [{"disposition": "blocked", "code": "OTHER", "missing": ["demo.C"],
                        "artifact_id": "demo.rule.q"}],
        }
        members = [
            {"schema": "source-closure-mapping.v2", "family": {"id": "demo.fam0"}, "closure_question": "Q0"},
            {"schema": "source-family.v1", "id": "demo.famA",
             "member_constraints": [{"block_code": "demo.K", "meaning": "famA meaning of K"}]},
        ]
        row = {"disposition": "blocked", "code": "OTHER", "artifact_id": "demo.rule.top",
               "missing": ["demo.P", "demo.Q"]}
        args: dict[str, Any] = {"resolved_members": members, "by_symbol": by_symbol, "later_any_arm_refs": True}
        want = _reference_reasons(row, **args)
        self.assertEqual(want, [{"sentence": "Q0"}, {"sentence": "famA meaning of K"}])
        self.assertEqual(_closure_question_reasons(row, **args), want)

    def test_a_changed_row_changes_the_answer(self) -> None:
        members = [{"schema": "source-closure-mapping.v2", "family": {"id": "demo.fam0"},
                    "closure_question": "demo question"}]
        by_symbol = {"demo.x": [{"disposition": "blocked", "code": "SOURCE_SET_UNCLOSED", "missing": ["demo.fam0"]}]}
        row = {"disposition": "blocked", "code": "DEPENDENCY_ABSENT", "missing": ["demo.x"]}
        self.assertEqual(_closure_question_reasons(row, resolved_members=members, by_symbol=by_symbol),
                         [{"sentence": "demo question"}])
        changed = {"demo.x": [{"disposition": "blocked", "code": "SOURCE_SET_UNCLOSED", "missing": ["demo.fam9"]}]}
        self.assertEqual(_closure_question_reasons(row, resolved_members=members, by_symbol=changed), [])
        other = [{**members[0], "closure_question": "demo other"}]
        self.assertEqual(_closure_question_reasons(row, resolved_members=other, by_symbol=by_symbol),
                         [{"sentence": "demo other"}])


# --- marshal precompute ------------------------------------------------------------------------


class _Horizon:
    current_by_chain: dict[Any, str] = {}


class _State:
    def __init__(self, findings: dict[str, dict[str, Any]]) -> None:
        self.findings = findings
        self.horizon_state = _Horizon()


class MarshalRequiredSymbols(unittest.TestCase):
    """The fallback binds a type exactly when some rule names it, as the per-rule check did."""

    RULES: list[dict[str, Any]] = [
        {"schema": "rule-artifact.v2", "id": "demo.rule.one", "requires": ["demo.t.one"]},
        {"schema": "rule-artifact.v3", "id": "demo.rule.two", "requires": [],
         "when": {"op": "ref", "name": "demo.t.when"}, "value": {"op": "ref", "name": "demo.t.value"}},
        {"schema": "attachment-rule.v1", "id": "demo.rule.three",
         "requirement": {"subtotals": ["demo.t.subtotal"], "triggers": []},
         "completeness": {"required_answers": [{"symbol": "demo.t.answer"}], "branch_requirements": []}},
    ]
    TYPES = ["demo.t.one", "demo.t.when", "demo.t.value", "demo.t.subtotal", "demo.t.answer",
             "demo.t.unrequired"]

    def test_the_union_matches_the_per_rule_path(self) -> None:
        findings = {
            f"demo.finding.{index}": {"id": f"demo.finding.{index}", "fact_id": type_id, "value": index}
            for index, type_id in enumerate(self.TYPES)
        }
        ids = frozenset(findings)
        currency = CurrencyView(current_finding_ids=ids, displaced_finding_ids=frozenset(),
                                current_evidence_ids=frozenset(), displaced_evidence_ids=frozenset())
        context = marshal_run_context(
            run_id="demo.run.marshal", state=cast(Any, _State(findings)), currency=currency,
            rules=copy.deepcopy(self.RULES), parameters={}, canon={},
            adoption_pin={"role": "adoption", "id": "demo.package", "version": "v1"},
            governance_pins=[])
        bound = {item.symbol for item in context.inputs}
        per_rule = {t for t in self.TYPES if any(t in _rule_required_symbols(r) for r in self.RULES)}
        self.assertEqual(bound, per_rule)
        self.assertNotIn("demo.t.unrequired", bound)
        self.assertEqual(len(bound), 5)


if __name__ == "__main__":
    unittest.main()
