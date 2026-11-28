"""In-memory P0 overlay of the ratified projector and saved-page renderer."""

from __future__ import annotations

from collections import defaultdict
from functools import cache, cached_property
import subprocess
import sys
from types import ModuleType

from packages.derivation.evaluator import PairedSourceRow, paired_coverage
from packages.derivation.presentation_projection import _StatementQuestions
from packages.kernel.facts import facts_of

from probe import CORE, KINDS, P, SALE_ENTITY, SALE_TYPES

BASE = "0172559abe564a0dc9da0aea521d4dd419e05d8f"
PROJECTION = "packages/derivation/presentation_projection.py"
PAGE = "packages/presentation/pages/citation-walk.v1.html"
PACKAGE = P + "package.core-calculations"
FIX_CODES = {"CODE_W_ON_GAIN", "ADJUSTMENT_EXCEEDS_LOSS"}
VALIDATION = ".member-validation.synthesized"
ANSWER_TYPES = {f"{source}.{kind}": source for source in SALE_TYPES for kind in KINDS}
IDENTITY = [
    {"name": "sale", "kind": "entity", "entity_kind": SALE_ENTITY},
    {"name": "tax-year", "kind": "literal", "values": ["2025"]},
]


def git(*args):
    return subprocess.check_output(["git", *args], text=True, timeout=20)


@cache
def sources():
    git("merge-base", "--is-ancestor", BASE, "HEAD")
    return git("show", f"{BASE}:{PROJECTION}"), git("show", f"{BASE}:{PAGE}")


def replace_once(source, anchor, replacement):
    if source.count(anchor) != 1:
        raise ValueError(f"expected exactly one scratch anchor {anchor!r}")
    return source.replace(anchor, replacement, 1)


def scratch_page(page):
    page = replace_once(
        page, 'const name = typeof reason.memberLabel',
        'const name = reason.saleLabel || (typeof reason.memberLabel',
    )
    return replace_once(
        page,
        '.filter((part) => typeof part === "string" && part).join(", ");\n      const prefixAttrs',
        '.filter((part) => typeof part === "string" && part).join(", "));\n      const prefixAttrs',
    )


def scratch_projection(source):
    edits = [
        (
            "    withholding_reasons_out: dict[str, list[dict[str, Any]]] | None = None,\n) -> list[dict[str, Any]]:",
            "    withholding_reasons_out: dict[str, list[dict[str, Any]]] | None = None,\n"
            "    sales=None,\n) -> list[dict[str, Any]]:",
        ),
        (
            "            frames[-1].facts.add(bound)\n",
            "            frames[-1].facts.add(bound)\n"
            "            if sales is not None and sales.applies(bound):\n"
            "                frames[-1].sale_traces[bound, id(current), key] = (bound, current, key, None)\n",
        ),
        (
            "                frames[-1].facts.add(fact_type)\n",
            "                frames[-1].facts.add(fact_type)\n"
            "                if sales is not None and sales.applies(fact_type):\n"
            "                    frames[-1].sale_traces[fact_type, id(None), key] = (fact_type, None, key, None)\n",
        ),
        (
            '                    fix_ft_id = str(fix_ft["id"])\n',
            '                    fix_ft_id = str(fix_ft["id"])\n'
            '                    if sales is not None and sales.applies(fix_ft_id):\n'
            '                        frames[-1].sale_traces[fix_ft_id, id(current), key] = (fix_ft_id, current, key, declared)\n',
        ),
        # The fixing path records its code and row above, then records the
        # unchanged linked or generic reason through the existing function.
        (
            'def record_input_fact(key: str, bound: str, current: Mapping[str, Any] | None = None)',
            'def record_input_fact(key: str, bound: str, current: Mapping[str, Any] | None = None, *, fixing=False)',
        ),
        (
            "if sales is not None and sales.applies(bound):",
            "if sales is not None and sales.applies(bound) and not fixing:",
        ),
        (
            "record_input_fact(candidate_id, fix_ft_id)",
            "record_input_fact(candidate_id, fix_ft_id, fixing=True)",
        ),
        (
            "record_input_fact(fix_ft_id, fix_ft_id)",
            "record_input_fact(fix_ft_id, fix_ft_id, fixing=True)",
        ),
        (
            "        reasons = []\n        for text in sorted(sentences):",
            "        if sales is not None and root.sale_traces and withholding_reasons_out is not None:\n"
            "            withholding_reasons_out.update(sales.reasons(\n"
            "                root.sale_traces.values(), input_questions,\n"
            "                {questions[family] for family in families} | extras,\n"
            "            ))\n"
            "        reasons = []\n        for text in sorted(sentences):",
        ),
        (
            '"extras", "answer_sentences", "member_facts", "paired", "unattributed", "examined", "hits",',
            '"extras", "answer_sentences", "member_facts", "paired", "unattributed", "examined", "hits", "sale_traces",',
        ),
        (
            "        self.examined: set[str] = set()\n",
            "        self.sale_traces = {}\n        self.examined: set[str] = set()\n",
        ),
        (
            "        self.examined |= other.examined\n",
            "        self.sale_traces.update(other.sale_traces)\n        self.examined |= other.examined\n",
        ),
        (
            "    answer_explanations = _answer_explanation_sentences(\n",
            "    sales = SaleQuestions(adopted_package, state, current_finding_ids,\n"
            "                          resolved_members, publications_by_id, by_symbol)\n"
            "    answer_explanations = _answer_explanation_sentences(\n",
        ),
        (
            '            "withholding_reasons_out": withholding_reasons,',
            '            "withholding_reasons_out": withholding_reasons,\n            "sales": sales,',
        ),
        (
            '"factId", "statementLabel", "statementPayerLabel", "memberLabel", "memberOrdinal",',
            '"factId", "statementLabel", "statementPayerLabel", "memberLabel", "memberOrdinal", "saleLabel",',
        ),
        (
            '                label = reason.get("statementLabel", {})',
            '                if "saleLabel" in reason and (set(reason) != {"sentence", "saleLabel"}\n'
            '                        or not isinstance(reason["saleLabel"], str) or not reason["saleLabel"].strip()):\n'
            '                    raise PresentationModelError(f"{rp}.saleLabel: expected a display-only recorded sale name")\n'
            '                label = reason.get("statementLabel", {})',
        ),
        (
            '                if "statementPayerLabel" in reason:\n                    raise',
            '                if "saleLabel" in reason:\n'
            '                    raise PresentationModelError(f"{p}.reasonIndices: sale names cannot link to a question group")\n'
            '                if "statementPayerLabel" in reason:\n                    raise',
        ),
    ]
    for anchor, replacement in edits:
        source = replace_once(source, anchor, replacement)
    return source


def pin_ids(pins, role, origin=None):
    return [
        pin["id"] for pin in pins if pin.get("role") == role
        and (origin is None or pin.get("origin") == origin)
    ]


class SaleQuestions:
    """Read the exact sale identities behind already reached question leaves."""

    def __init__(self, package, state, current_ids, members, publications, by_symbol):
        self.enabled = (
            package is not None and package[0] == PACKAGE
            and package[1].startswith("v") and package[1][1:].isdigit()
            and int(package[1][1:]) >= int(CORE[1:]) and current_ids is not None
        )
        self.state = state
        self.current_ids = current_ids
        self.members = members
        self.publications = publications
        self.by_symbol = by_symbol
        self.rules = {m["id"]: m for m in members if "publishes" in m}
        self.identities = {}

    def applies(self, fact_type):
        return self.enabled and fact_type in ANSWER_TYPES

    @cached_property
    def facts(self):
        return facts_of(self.state.fact_state)

    @cached_property
    def current(self):
        rows = defaultdict(dict)
        for finding_id in self.current_ids:
            finding = self.state.findings.get(finding_id)
            fact = self.facts.get(finding["fact_id"]) if finding else None
            if fact is not None:
                rows[fact.fact_type_id].setdefault(fact.fact_id, []).append(finding_id)
        return rows

    def identity_contract(self, fact_type):
        if fact_type in self.identities:
            return self.identities[fact_type]
        declarations = [
            item for member in self.members for item in member.get("fact_types", ())
            if item["id"] == fact_type
        ]
        effective = self.state.fact_state.fact_types.get(fact_type)
        self.identities[fact_type] = (
            bool(declarations) and effective is not None
            and all(d.get("version") == "v1" and d.get("identity_keys") == IDENTITY
                    for d in [*declarations, effective])
        )
        return self.identities[fact_type]

    def question_contract(self, answer):
        return [
            member["fact_type"] for member in self.members
            if member.get("schema", "").startswith("input-question.")
            and member.get("fact_type", {}).get("id") == answer
        ] == [{"id": answer, "version": "v1"}]

    def fact(self, canonical_id, fact_type):
        fact = self.facts.get(canonical_id)
        if fact is None or fact.fact_type_id != fact_type:
            return None
        keys = dict(fact.keys)
        if set(keys) != {"sale", "tax-year"} or keys["tax-year"] != "2025":
            return None
        if canonical_id != f"{fact_type}|sale={keys['sale']},tax-year=2025":
            return None
        return fact

    def source_pin(self, pin, fact_type):
        fid = pin.get("id")
        finding = self.state.findings.get(fid)
        if (pin.get("origin") != "assertion" or fid not in self.current_ids or not finding
                or pin.get("version") != "v1" or finding.get("id") != fid):
            return None
        return self.fact(finding["fact_id"], fact_type)

    def source_for_result(self, result, canonical_id, fact_type):
        fact = self.fact(canonical_id, fact_type)
        current = self.current[fact_type].get(canonical_id, [])
        if fact is None or len(current) != 1:
            return None
        sources = [
            pin for pin in result.get("pins", [])
            if pin.get("role") == "input"
            and self.state.findings.get(pin.get("id"), {}).get("fact_id", "").startswith(fact_type + "|")
        ]
        if len(sources) != 1 or sources[0].get("id") != current[0]:
            return None
        return self.source_pin(sources[0], fact_type)

    def fixes(self, row, answer, code, declared):
        source = ANSWER_TYPES[answer]
        family = source.removesuffix("-txn")
        artifact = family + VALIDATION
        if (answer != source + ".adjustment" or row.get("artifact_id") != artifact
                or row.get("code") != "DEPENDENCY_INVALID" or code not in FIX_CODES
                or code not in row.get("missing", ())
                or declared.get("fact_type") != {"id": answer, "version": "v1"}
                or declared.get("schema") != "family-block-explanation.v1"):
            return None
        family_declarations = [
            m for m in self.members if m.get("id") == family and m.get("schema", "").startswith("source-family.")
        ]
        if (len(family_declarations) != 1 or family_declarations[0].get("version") != "v1"
                or family_declarations[0].get("member_predicate") != {"fact_type": source}
                or code not in {c["block_code"] for c in family_declarations[0].get("member_constraints", ())}):
            return None
        seen, targets = set(), set()
        prefix = artifact + "."
        for result in self.publications.values():
            if not result["symbol"].startswith(prefix):
                continue
            fact_id = result["symbol"].removeprefix(prefix)
            value = result.get("value")
            if (fact_id in seen or not isinstance(value, dict) or value.get("member_fact_id") != fact_id
                    or not isinstance(value.get("violations"), list)
                    or not all(isinstance(v, dict) and isinstance(v.get("block_code"), str)
                               for v in value["violations"])
                    or self.source_for_result(result, fact_id, source) is None):
                return None
            seen.add(fact_id)
            if code in {v["block_code"] for v in value["violations"]}:
                targets.add(fact_id)
        return targets if seen == self.current[source].keys() else None

    def amounts_check(self, row, answer, source, rule):
        symbol = source + ".amounts-agree"
        producer = self.rules.get(P + "rule." + symbol.removeprefix(P))
        if (answer != source + ".basis" or row.get("code") != "DEPENDENCY_INVALID"
                or rule.get("version") != "v2" or producer is None or producer.get("version") != "v1"
                or producer.get("subject") != {"id": source, "version": "v1"}
                or producer.get("publishes") != symbol):
            return None
        inputs = [pin for pin in row.get("pins", ()) if pin.get("role") == "input"]
        seen, targets = set(), set()
        for pin in inputs:
            result = self.publications.get(pin.get("id"))
            if pin.get("origin") != "derived" or result is None or pin.get("version") != result.get("version"):
                return None
            _, sep, fact_id = result["symbol"].partition("|")
            scoped_symbol = f"{symbol}|{fact_id}"
            rows = self.by_symbol.get(scoped_symbol, ())
            if (not sep or result["symbol"] != scoped_symbol or fact_id in seen
                    or len(rows) != 1 or rows[0].get("artifact_id") != producer["id"]
                    or rows[0].get("disposition") != "published" or rows[0].get("finding_id") != pin["id"]
                    or result.get("value") not in ("agree", "disagree")
                    or self.source_for_result(result, fact_id, source) is None):
                return None
            seen.add(fact_id)
            if result["value"] == "disagree":
                targets.add(fact_id)
        return targets if seen == self.current[source].keys() else None

    def pairing(self, row, answer, source, rule):
        if (answer not in (source + ".basis", source + ".proceeds")
                or row.get("code") != "DEPENDENCY_ABSENT" or rule.get("version") != "v3"):
            return None
        nodes = _StatementQuestions._paired_nodes(rule, answer)
        if (len(nodes) != 1 or nodes[0] != {
                "op": "require_paired", "key": "sale", "income": [source], "withholding": answer,
        } or _StatementQuestions._mentions_outside_pair(rule, nodes[0], answer)):
            return None
        rows = defaultdict(list)
        seen = defaultdict(set)
        for pin in row.get("pins", ()):
            if pin.get("role") != "input":
                continue
            finding = self.state.findings.get(pin.get("id"))
            if finding is None:
                if pin.get("id") not in self.publications:
                    return None
                continue
            ft = finding["fact_id"].partition("|")[0]
            if ft not in (answer, source):
                continue
            fact = self.source_pin(pin, ft)
            if (fact is None or fact.fact_id in seen[ft]
                    or self.current[ft].get(fact.fact_id) != [pin["id"]]):
                return None
            seen[ft].add(fact.fact_id)
            rows[ft].append(PairedSourceRow(finding_id=pin["id"], keys=fact.keys))
        if any(seen[ft] != self.current[ft].keys() for ft in (answer, source)):
            return None
        coverage = paired_coverage(nodes[0], rows)
        if coverage.bad:
            return None
        return {fid for fid in seen[source] if dict(self.fact(fid, source).keys)["sale"] in coverage.uncovered}

    def targets(self, answer, row, missing, declared):
        if (row is None or row.get("disposition") != "blocked"
                or not self.question_contract(answer) or not self.identity_contract(answer)):
            return None
        source = ANSWER_TYPES[answer]
        if not self.identity_contract(source):
            return None
        if declared is not None:
            return self.fixes(row, answer, missing, declared)
        if missing != answer or row.get("missing") != [answer]:
            return None
        artifact = row.get("artifact_id")
        rule = self.rules.get(artifact)
        if rule is None:
            return None
        if artifact == P + "rule." + source.removeprefix(P) + ".amounts-check":
            return self.amounts_check(row, answer, source, rule)
        line = "3" if SALE_TYPES[source] == "st" else "10"
        if artifact == P + "rule.schedule-d-line" + line:
            return self.pairing(row, answer, source, rule)
        return None

    @cached_property
    def cohort(self):
        labels = {}
        for source in SALE_TYPES:
            if self.current[source] and not self.identity_contract(source):
                return {}
            for fact_id, findings in self.current[source].items():
                fact = self.fact(fact_id, source)
                if fact is None or len(findings) != 1:
                    return {}
                sale = dict(fact.keys)["sale"]
                entity = self.state.fact_state.entities.get(sale)
                if entity is None or entity.status != "current" or entity.entity.get("kind") != SALE_ENTITY:
                    return {}
                label = entity.entity.get("label")
                labels[sale] = label if isinstance(label, str) and label.strip() and label != sale else None
        return labels

    def reasons(self, traces, questions, other_sentences):
        labels = self.cohort if traces else {}
        if len(labels) < 2:
            return {}
        normalized = [" ".join(label.split()).casefold() for label in labels.values() if label is not None]
        collisions = {label for label in normalized if normalized.count(label) > 1}
        matched, unresolved = defaultdict(set), set(other_sentences)
        for answer, row, key, declared in traces:
            sentence = questions.get(answer)
            if sentence in unresolved or not sentence:
                continue
            targets = self.targets(answer, row, key, declared)
            if not targets:
                unresolved.add(sentence)
            else:
                matched[sentence].update(targets)
        out = {}
        for sentence, targets in matched.items():
            if sentence in unresolved:
                continue
            names = []
            for target in targets:
                fact = self.facts[target]
                label = labels.get(dict(fact.keys)["sale"])
                if label is None or " ".join(label.split()).casefold() in collisions:
                    break
                names.append((label, target))
            else:
                out[sentence] = [{"sentence": sentence, "saleLabel": label} for label, _ in sorted(names)]
        return out


@cache
def projectors():
    projection, _ = sources()
    result = []
    package = "packages.derivation"
    for name, code in (("sale_names_base", projection), ("sale_names_scratch", scratch_projection(projection))):
        module = ModuleType(package + "." + name)
        module.__package__ = package
        module.__dict__["SaleQuestions"] = SaleQuestions
        sys.modules[module.__name__] = module
        exec(compile(code, PROJECTION, "exec"), module.__dict__)
        result.append(module)
    return tuple(result)
