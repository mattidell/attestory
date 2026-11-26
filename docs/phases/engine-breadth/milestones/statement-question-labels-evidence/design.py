"""Scratch design for statement-question-labels (P0 evidence, not product code).

``install()`` wraps ``presentation_projection._closure_question_reasons`` in
memory, for the life of the calling process, so the design can be run on the
published core through the real ``live_coordinate_run`` and compared with the
unpatched projection in the same process. ``uninstall()`` restores it.
Nothing under ``packages/`` is edited.

What the wrapper does, after the unchanged walk has produced its reasons:

1. For each reason that is the adopted input question of a fact type ``F``
   individuated on one entity key named ``statement`` plus literal keys (on
   core v106: the Form 1099-B box 4 amount, box 4 yes/no and box 7
   questions),
   find the blocked rows the line reaches that name ``F`` bare in ``missing``.
2. For each such row, read every ``require_paired`` node in that row's rule
   whose ``withholding`` is ``F`` and recompute it from the current facts:
   the ``key`` values of current income rows that no current ``F`` row
   covers. This is the evaluator's own test (``evaluator._require_paired``)
   applied to the same current rows.
3. ``NEED_SYMBOLS`` narrows a pairing that content gates per subject. Line
   25b on v106 runs its pairing only when some sale still needs an amount,
   and then over every statement, so the recomputed set also holds a
   statement whose box 4 the filer said shows nothing. The per-sale
   ``*.box4-amount-needed`` results the engine published (1 = needed) are
   that per-statement need; only statements with a sale whose result is 1
   are named.
4. If every reached row resolves to at least one statement with one current
   recorded label, the one unlabelled reason is replaced, in place, by one
   reason per statement carrying ``statementLabel`` ``{statement, taxYear}``
   (identity by fact id, never by label). Otherwise the reason is left as it
   is (fail closed to today's page).

``rows_for`` and ``targets_for`` are importable for tests.
"""

from __future__ import annotations

from decimal import Decimal, InvalidOperation
from typing import Any, Callable, Mapping, Sequence

from packages.derivation import presentation_projection as pp

_ORIGINAL: Callable[..., list[dict[str, Any]]] | None = None
_ORIGINAL_BUILD: Callable[..., dict[str, Any]] | None = None
# Published derived values of the build in progress, by finding id. The real
# change would pass ``publications_by_id`` into the walk; the scratch wrapper
# captures it around ``build_presentation_model``.
_VALUES: dict[str, Any] = {}

STATEMENT_KEY = "statement"
_SALE_KINDS = ("covered-st", "covered-lt", "covered-w-st", "covered-w-lt",
               "noncovered-st", "noncovered-lt", "code-b-st", "code-b-lt")
NEED_SYMBOLS: dict[str, tuple[str, ...]] = {
    "tax.us.2025.f1099b.statement-box4-withholding": tuple(
        f"tax.us.2025.f1099b.{kind}-txn.box4-amount-needed" for kind in _SALE_KINDS),
}


def _positive(value: Any) -> bool:
    """A published count or flag above zero (derived values are decimal strings)."""
    try:
        return not isinstance(value, bool) and Decimal(str(value)) > 0
    except (InvalidOperation, ValueError):
        return False


def _keys(fact_id: str) -> dict[str, str]:
    _, _, rest = fact_id.partition("|")
    out: dict[str, str] = {}
    for part in rest.split(","):
        name, sep, value = part.partition("=")
        if sep:
            out[name] = value
    return out


def _paired_nodes(node: Any, withholding: str) -> list[Mapping[str, Any]]:
    found: list[Mapping[str, Any]] = []
    if isinstance(node, Mapping):
        if node.get("op") == "require_paired" and node.get("withholding") == withholding:
            found.append(node)
        for value in node.values():
            found.extend(_paired_nodes(value, withholding))
    elif isinstance(node, list):
        for item in node:
            found.extend(_paired_nodes(item, withholding))
    return found


def rows_for(row: Mapping[str, Any], fact_type: str,
             by_symbol: Mapping[str, Sequence[Mapping[str, Any]]]) -> list[Mapping[str, Any]]:
    """Blocked rows reachable from ``row`` through ``missing`` that name ``fact_type`` bare."""
    out: list[Mapping[str, Any]] = []
    seen_rows: set[int] = set()
    stack = [row]
    while stack:
        current = stack.pop()
        if id(current) in seen_rows:
            continue
        seen_rows.add(id(current))
        missing = [str(m) for m in current.get("missing") or []]
        if fact_type in missing:
            out.append(current)
        for key in missing:
            stack.extend(r for r in by_symbol.get(key, ()) if r.get("disposition") == "blocked")
    return out


class _Facts:
    def __init__(self, state: Any) -> None:
        from packages.kernel.currency import compute_currency
        from packages.kernel.facts import facts_of

        self.state = state
        current = compute_currency(state).current_finding_ids
        fact_map = facts_of(state.fact_state)
        self.by_type: dict[str, list[dict[str, str]]] = {}
        self.current_fact_ids: set[str] = set()
        for finding_id, finding in state.findings.items():
            fact = fact_map.get(str(finding.get("fact_id"))) if finding_id in current else None
            if fact is None or fact.fact_id in self.current_fact_ids:
                continue
            self.current_fact_ids.add(fact.fact_id)
            self.by_type.setdefault(fact.fact_type_id, []).append(dict(fact.keys))
        self.current = current

    def label(self, entity_id: str) -> str | None:
        lifecycle = self.state.fact_state.entities.get(entity_id)
        if lifecycle is None or lifecycle.status != "current":
            return None
        recorded = lifecycle.entity.get("label")
        return recorded if isinstance(recorded, str) and recorded else None

    def value(self, finding_id: Any) -> Any:
        return _VALUES.get(str(finding_id))


def targets_for(blocked: Mapping[str, Any], fact_type: str, *, rules: Mapping[str, Mapping[str, Any]],
                facts: _Facts, identity: Sequence[Mapping[str, Any]],
                by_symbol: Mapping[str, Sequence[Mapping[str, Any]]]) -> set[str] | None:
    """Fact ids of ``fact_type`` the row is waiting on, or None when it cannot say."""
    rule = rules.get(str(blocked.get("artifact_id")))
    nodes = _paired_nodes(rule, fact_type) if rule is not None else []
    if not nodes:
        return None
    names = [str(k.get("name")) for k in identity]
    targets: set[str] = set()
    for node in nodes:
        key = str(node.get("key"))
        covered = {row.get(key) for row in facts.by_type.get(fact_type, [])}
        for income in node.get("income") or []:
            for row in facts.by_type.get(str(income), []):
                if row.get(key) in covered or not all(name in row for name in names):
                    continue
                targets.add(pp.fact_id_for(fact_type, tuple((name, row[name]) for name in names)))
    need = NEED_SYMBOLS.get(fact_type)
    if need is not None:
        needed: set[str] = set()
        for symbol, rows in by_symbol.items():
            base, sep, subject = symbol.partition("|")
            if not sep or base not in need:
                continue
            for row in rows:
                if row.get("disposition") == "published" and _positive(facts.value(row.get("finding_id"))):
                    subject_keys = _keys(subject)
                    if all(name in subject_keys for name in names):
                        needed.add(pp.fact_id_for(fact_type, tuple((name, subject_keys[name]) for name in names)))
        targets &= needed
    return targets or None


def _entity_identity(fact_type: str, state: Any,
                     resolved_members: Sequence[Mapping[str, Any]] = ()) -> tuple[str, list[Mapping[str, Any]]] | None:
    """The one entity key and the identity keys of ``fact_type``: adopted, else as the package declares it."""
    declaration = state.fact_state.fact_types.get(fact_type)
    if declaration is None:
        declaration = next((ft for member in resolved_members if str(member.get("schema", "")).startswith("bundle.")
                            for ft in member.get("fact_types") or [] if isinstance(ft, Mapping) and ft.get("id") == fact_type), None)
    identity = declaration.get("identity_keys") if isinstance(declaration, Mapping) else None
    if not isinstance(identity, list):
        return None
    entity = [k for k in identity if isinstance(k, Mapping) and k.get("kind") == "entity"]
    if len(entity) != 1 or any(k.get("kind") not in {"entity", "literal"} for k in identity):
        return None
    # ``statementLabel.statement`` names a statement. A fact individuated on
    # another entity (a sale recorded without a Form 1099-B, keyed ``sale``)
    # is not labelled here.
    if entity[0].get("name") != STATEMENT_KEY:
        return None
    return str(entity[0]["name"]), identity


def _input_questions(resolved_members: Sequence[Mapping[str, Any]]) -> dict[str, str]:
    out: dict[str, str] = {}
    for member in resolved_members:
        fact_type = member.get("fact_type")
        if (str(member.get("schema", "")).startswith("input-question.") and isinstance(fact_type, Mapping)
                and isinstance(member.get("question"), str)):
            out[member["question"]] = str(fact_type.get("id"))
    return out


def labelled(row: Mapping[str, Any], reasons: list[dict[str, Any]], kwargs: Mapping[str, Any]) -> tuple[list[dict[str, Any]], dict[int, list[int]]]:
    """The reasons with each per-statement question split by statement, and the index map."""
    roster = kwargs.get("roster_members")
    if roster is None or not reasons:
        return reasons, {}
    state = roster._state
    rules = roster._rules
    by_symbol = kwargs["by_symbol"]
    questions = _input_questions(kwargs["resolved_members"])
    facts: _Facts | None = None
    out: list[dict[str, Any]] = []
    index_map: dict[int, list[int]] = {}
    for index, reason in enumerate(reasons):
        fact_type = questions.get(str(reason.get("sentence")))
        replaced: list[dict[str, Any]] | None = None
        shape = _entity_identity(fact_type, state, kwargs["resolved_members"]) if fact_type and set(reason) == {"sentence"} else None
        if fact_type and shape is not None:
            entity_key, identity = shape
            blocked = rows_for(row, fact_type, by_symbol)
            facts = facts or _Facts(state)
            per_row = [targets_for(b, fact_type, rules=rules, facts=facts, identity=identity, by_symbol=by_symbol)
                       for b in blocked]
            if blocked and all(t for t in per_row):
                targets = sorted(set().union(*[t for t in per_row if t]))
                entries: list[tuple[str, str, dict[str, Any]]] = []
                for target in targets:
                    keys = _keys(target)
                    label = facts.label(keys[entity_key])
                    if label is None:
                        entries = []
                        break
                    statement_label = {"statement": label}
                    if "tax-year" in keys:
                        statement_label["taxYear"] = keys["tax-year"]
                    entries.append((label, target, {"sentence": reason["sentence"], "statementLabel": statement_label}))
                if entries:
                    replaced = [entry for _, _, entry in sorted(entries, key=lambda item: (item[0], item[1]))]
        start = len(out)
        out.extend(replaced if replaced is not None else [reason])
        index_map[index] = list(range(start, len(out)))
    return out, index_map


def _wrapped(row: Mapping[str, Any], **kwargs: Any) -> list[dict[str, Any]]:
    assert _ORIGINAL is not None
    refs_out = kwargs.get("question_refs_out")
    before = len(refs_out) if refs_out is not None else 0
    reasons = _ORIGINAL(row, **kwargs)
    new, index_map = labelled(row, reasons, kwargs)
    if new is not reasons and refs_out is not None:
        for reference in refs_out[before:]:
            reference["reasonIndices"] = [n for i in reference.get("reasonIndices", []) for n in index_map.get(i, [i])]
    return new


def _build(**kwargs: Any) -> dict[str, Any]:
    assert _ORIGINAL_BUILD is not None
    _VALUES.clear()
    for publication in kwargs.get("publications") or ():
        finding = getattr(publication, "finding", None)
        if isinstance(finding, Mapping) and isinstance(finding.get("id"), str):
            _VALUES[finding["id"]] = finding.get("value")
    try:
        return _ORIGINAL_BUILD(**kwargs)
    finally:
        _VALUES.clear()


def install() -> None:
    global _ORIGINAL, _ORIGINAL_BUILD
    from packages.derivation import live

    if _ORIGINAL is None:
        _ORIGINAL = pp._closure_question_reasons
        _ORIGINAL_BUILD = pp.build_presentation_model
        pp._closure_question_reasons = _wrapped
        pp.build_presentation_model = _build
        live.build_presentation_model = _build  # type: ignore[attr-defined]


def uninstall() -> None:
    global _ORIGINAL, _ORIGINAL_BUILD
    from packages.derivation import live

    if _ORIGINAL is not None and _ORIGINAL_BUILD is not None:
        pp._closure_question_reasons = _ORIGINAL
        pp.build_presentation_model = _ORIGINAL_BUILD
        live.build_presentation_model = _ORIGINAL_BUILD  # type: ignore[attr-defined]
        _ORIGINAL = None
        _ORIGINAL_BUILD = None
