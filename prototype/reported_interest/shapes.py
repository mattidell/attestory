"""Candidate representations, executed by the real engine evaluator.

Shapes A, C, and E each evaluate an includible rule and a basis rule through
the real evaluator, each with its own AccessLog, rule identity, dependencies,
and refusal. Shape B evaluates one determination rule. A rule id recorded in
provenance is the expression that ran; provenance is never relabelled after
the fact.

Durable packaging of the basis consequence, after those evaluations:

  A — artifact-alone. Payload ``{amount}`` only.
  C — embedded-composite. The carried artifact duplicates ``reported`` and
      ``includible`` amounts. Pointer fields are not used.
  E — relationship-edge. The carried artifact holds ``sibling`` and
      ``reported_key`` pointers and no partition amounts. Following them
      requires an identity-addressable object store that still holds the
      referenced artifacts.
  B — explicit determination. One artifact holding the amounts together.

Later-year access is an explicit capability grant, not a hidden workspace.
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from typing import Any, Mapping

from packages.derivation.evaluator import AccessLog, EvalBlocked, evaluate

from .model import FactNames, Workspace

AUTHORITY = (
    {
        "family": "us-code",
        "citation": "IRC § 61(a)(4)",
        "proposition": "Interest is gross income unless excluded.",
    },
    {
        "family": "irs-publication",
        "citation": "Pub. 550, Bonds Sold Between Interest Dates",
        "proposition": (
            "Interest that accrued before purchase and was paid to the seller is not "
            "the purchaser's income; it is a return of the purchase price and reduces basis."
        ),
    },
)

BLOCK_UNSUPPORTED = "SLICE_COVERAGE_UNSUPPORTED"
BLOCK_ITEM_MISMATCH = "ITEM_RELATION_MISMATCH"
COVERAGE_ID = "demo.coverage.accrued-interest-at-purchase"
COVERAGE_VERSION = 1

RULE_INCLUDIBLE = ("demo.rule.includible-interest", 3)
RULE_BASIS = ("demo.rule.basis-reduction", 3)
RULE_SOURCE_REPORT = ("demo.rule.source-report", 3)
RULE_DETERMINATION = ("demo.rule.accrued-interest-at-purchase", 3)


def _cat_eq(name: str, value: str, fact_type: str | None = None) -> dict[str, Any]:
    return {
        "op": "categorical_compare",
        "cmp": "eq",
        "left": {"op": "ref", "name": name},
        "right": {"op": "category_literal", "fact_type": fact_type or name, "value": value},
    }


def _ref(name: str) -> dict[str, Any]:
    return {"op": "ref", "name": name}


def _coverage(names: FactNames) -> dict[str, Any]:
    return {
        "op": "choose",
        "when": {
            "op": "all",
            "args": [
                _cat_eq(names.obligation_kind, "corporate-bond"),
                _cat_eq(names.education_expenses, "no"),
            ],
        },
        "then": True,
        "else": {"op": "block", "code": BLOCK_UNSUPPORTED},
    }


def _relation(names: FactNames) -> dict[str, Any]:
    return {
        "op": "choose",
        "when": _cat_eq(names.bought_between_dates, "yes"),
        "then": {
            "op": "choose",
            "when": {
                "op": "categorical_compare",
                "cmp": "eq",
                "left": _ref(names.accrued_relates_to),
                "right": _ref(names.reported_obligation),
            },
            "then": True,
            "else": {"op": "block", "code": BLOCK_ITEM_MISMATCH},
        },
        "else": True,
    }


def _required(members: list[dict[str, Any]], condition: Any = True) -> dict[str, Any]:
    return {"op": "conditional_dependency_set", "condition": condition, "members": members}


def _non_includible(names: FactNames) -> dict[str, Any]:
    return {
        "op": "choose",
        "when": _cat_eq(names.bought_between_dates, "yes"),
        "then": _ref(names.accrued_paid_to_seller),
        "else": 0,
    }


def includible_guard(names: FactNames) -> dict[str, Any]:
    """Includible rule reads the statement amount and the purchase facts."""
    return {
        "op": "all",
        "args": [
            _required(
                [
                    _ref(names.reported_amount),
                    _ref(names.reported_payer),
                    _ref(names.reported_obligation),
                    _ref(names.bought_between_dates),
                    _ref(names.obligation_kind),
                    _ref(names.education_expenses),
                ]
            ),
            _required(
                [_ref(names.accrued_paid_to_seller), _ref(names.accrued_relates_to)],
                _cat_eq(names.bought_between_dates, "yes"),
            ),
            _coverage(names),
            _relation(names),
        ],
    }


def basis_guard(names: FactNames) -> dict[str, Any]:
    """Basis rule does not read the reported amount or the payer."""
    return {
        "op": "all",
        "args": [
            _required(
                [
                    _ref(names.reported_obligation),
                    _ref(names.bought_between_dates),
                    _ref(names.obligation_kind),
                    _ref(names.education_expenses),
                ]
            ),
            _required(
                [_ref(names.accrued_paid_to_seller), _ref(names.accrued_relates_to)],
                _cat_eq(names.bought_between_dates, "yes"),
            ),
            _coverage(names),
            _relation(names),
        ],
    }


def reported_guard(names: FactNames) -> dict[str, Any]:
    """Identify and read the statement value. No tax-slice coverage."""
    return _required(
        [
            _ref(names.reported_amount),
            _ref(names.reported_payer),
            _ref(names.reported_obligation),
        ]
    )


@dataclass(frozen=True)
class Blocked:
    code: str
    missing: tuple[str, ...]

    @property
    def is_blocked(self) -> bool:
        return True


@dataclass(frozen=True)
class Provenance:
    reads: tuple[str, ...]
    versions: Mapping[str, int]
    rule_id: str
    rule_version: int
    authority: tuple[Mapping[str, str], ...] = ()
    coverage_id: str | None = None
    coverage_version: int | None = None

    def displaced_by(self, workspace: Workspace) -> bool:
        current = workspace.versions()
        return any(current.get(name) != version for name, version in self.versions.items())

    def accounted(self) -> set[str]:
        """Distinguish omitted tax authority/coverage from a present treatment declaration.

        Source support is the exact reads. Tax authority lives only in
        ``authority``. Tax-slice coverage lives only in the coverage fields.
        Omission is an explicit token, not a missing key.
        """
        out: set[str] = set(self.reads)
        out.add(f"rule:{self.rule_id}.v{self.rule_version}")
        if self.coverage_id is None and self.coverage_version is None:
            out.add("coverage:omitted")
        else:
            cid = "unspecified" if self.coverage_id is None else self.coverage_id
            cver = "unspecified" if self.coverage_version is None else self.coverage_version
            out.add(f"coverage:{cid}.v{cver}")
        if not self.authority:
            out.add("authority:omitted")
        else:
            out.update(f"authority:{a['citation']}" for a in self.authority)
        return out


@dataclass(frozen=True)
class Evaluation:
    values: dict[str, Decimal]
    provenance: Provenance


def _run(
    workspace: Workspace,
    guard: dict[str, Any],
    values: dict[str, Any],
    rule: tuple[str, int],
    *,
    authority: tuple[Mapping[str, str], ...] = AUTHORITY,
    coverage_id: str | None = COVERAGE_ID,
    coverage_version: int | None = COVERAGE_VERSION,
) -> Evaluation | Blocked:
    env = workspace.environment()
    access = AccessLog()
    try:
        evaluate(guard, env, access)
        out = {key: evaluate(expr, env, access) for key, expr in values.items()}
    except EvalBlocked as exc:
        return Blocked(exc.category, tuple(exc.missing))
    reads = tuple(sorted(access.refs))
    versions = {n: workspace.facts[n].version for n in reads if n in workspace.facts}
    return Evaluation(
        values=out,
        provenance=Provenance(
            reads,
            versions,
            rule[0],
            rule[1],
            authority,
            coverage_id=coverage_id,
            coverage_version=coverage_version,
        ),
    )


def evaluate_includible(workspace: Workspace) -> Evaluation | Blocked:
    names = workspace.names
    return _run(
        workspace,
        includible_guard(names),
        {
            "reported": _ref(names.reported_amount),
            "includible": {
                "op": "subtract",
                "left": _ref(names.reported_amount),
                "right": _non_includible(names),
            },
            "non_includible": _non_includible(names),
        },
        RULE_INCLUDIBLE,
    )


def evaluate_basis(workspace: Workspace) -> Evaluation | Blocked:
    names = workspace.names
    return _run(workspace, basis_guard(names), {"basis": _non_includible(names)}, RULE_BASIS)


def evaluate_reported(workspace: Workspace) -> Evaluation | Blocked:
    """Identify the statement reads. No tax authority and no tax-slice coverage."""
    names = workspace.names
    return _run(
        workspace,
        reported_guard(names),
        {"reported": _ref(names.reported_amount)},
        RULE_SOURCE_REPORT,
        authority=(),
        coverage_id=None,
        coverage_version=None,
    )


def evaluate_determination(workspace: Workspace) -> Evaluation | Blocked:
    names = workspace.names
    return _run(
        workspace,
        includible_guard(names),
        {
            "reported": _ref(names.reported_amount),
            "includible": {
                "op": "subtract",
                "left": _ref(names.reported_amount),
                "right": _non_includible(names),
            },
            "non_includible": _non_includible(names),
        },
        RULE_DETERMINATION,
    )


@dataclass(frozen=True)
class Artifact:
    key: str
    item: str
    kind: str
    payload: Mapping[str, Any]
    provenance: Provenance


class Displaced(Exception):
    """Asked for an artifact whose inputs have since changed."""


@dataclass(frozen=True)
class CurrentnessService:
    """Explicit later-year capability: current fact versions, not a workspace."""

    versions: Mapping[str, int]

    def displaced(self, provenance: Provenance) -> bool:
        return any(self.versions.get(name) != version for name, version in provenance.versions.items())

    @classmethod
    def from_workspace(cls, workspace: Workspace) -> "CurrentnessService":
        return cls(dict(workspace.versions()))


@dataclass
class ObjectStore:
    """Identity-addressable retained artifacts. Explicit later-year capability."""

    artifacts: dict[str, Artifact]

    def get(self, key: str) -> Artifact | None:
        return self.artifacts.get(key)


@dataclass
class Store:
    """Source-year publication store. Currentness uses the live workspace."""

    artifacts: dict[str, Artifact]

    @classmethod
    def empty(cls) -> "Store":
        return cls(artifacts={})

    def put(self, artifact: Artifact) -> None:
        self.artifacts[artifact.key] = artifact

    def serve(self, key: str, workspace: Workspace) -> Artifact:
        art = self.artifacts.get(key)
        if art is None:
            raise KeyError(key)
        if art.provenance.displaced_by(workspace):
            raise Displaced(key)
        return art

    def current_for(self, item: str, workspace: Workspace) -> tuple[Artifact, ...]:
        return tuple(
            a
            for a in self.artifacts.values()
            if a.item == item and not a.provenance.displaced_by(workspace)
        )

    def displaced_for(self, item: str, workspace: Workspace) -> tuple[str, ...]:
        return tuple(
            sorted(
                a.key
                for a in self.artifacts.values()
                if a.item == item and a.provenance.displaced_by(workspace)
            )
        )

    def as_object_store(self) -> ObjectStore:
        return ObjectStore(dict(self.artifacts))


def _item(workspace: Workspace) -> str:
    return workspace.facts[workspace.names.reported_obligation].value


def _publish_source_report(workspace: Workspace, store: Store) -> Evaluation | Blocked:
    """Publish the source report independently of tax treatment."""
    reported = evaluate_reported(workspace)
    if isinstance(reported, Blocked):
        return reported
    item = _item(workspace)
    key = f"{item}.source-report"
    store.put(
        Artifact(
            key=key,
            item=item,
            kind="source-report",
            payload={"amount": reported.values["reported"]},
            provenance=reported.provenance,
        )
    )
    return reported


def _blocked_or_pair(workspace: Workspace) -> tuple[Evaluation, Evaluation] | Blocked:
    inc = evaluate_includible(workspace)
    if isinstance(inc, Blocked):
        return inc
    basis = evaluate_basis(workspace)
    if isinstance(basis, Blocked):
        return basis
    return inc, basis


def publish_shape_a(workspace: Workspace, store: Store) -> tuple[str, ...] | Blocked:
    src = _publish_source_report(workspace, store)
    if isinstance(src, Blocked):
        return src
    outcome = _blocked_or_pair(workspace)
    if isinstance(outcome, Blocked):
        return outcome
    inc, basis = outcome
    item = _item(workspace)
    keys = [f"{item}.source-report"]
    for kind, rule_eval, amount in (
        ("includible-interest", inc, inc.values["includible"]),
        ("basis-reduction", basis, basis.values["basis"]),
    ):
        key = f"{item}.{kind}"
        store.put(
            Artifact(
                key=key,
                item=item,
                kind=kind,
                payload={"amount": amount},
                provenance=rule_eval.provenance,
            )
        )
        keys.append(key)
    return tuple(keys)


def publish_shape_c(workspace: Workspace, store: Store) -> tuple[str, ...] | Blocked:
    """Embedded-composite: the carried artifact duplicates the partition amounts."""
    src = _publish_source_report(workspace, store)
    if isinstance(src, Blocked):
        return src
    outcome = _blocked_or_pair(workspace)
    if isinstance(outcome, Blocked):
        return outcome
    inc, basis = outcome
    item = _item(workspace)
    inc_key = f"{item}.includible-interest"
    basis_key = f"{item}.basis-reduction"
    store.put(
        Artifact(
            key=inc_key,
            item=item,
            kind="includible-interest",
            payload={"amount": inc.values["includible"]},
            provenance=inc.provenance,
        )
    )
    store.put(
        Artifact(
            key=basis_key,
            item=item,
            kind="basis-reduction",
            payload={
                "amount": basis.values["basis"],
                "reported": src.values["reported"],
                "includible": inc.values["includible"],
                "components": {
                    "amount": basis.provenance,
                    "reported": src.provenance,
                    "includible": inc.provenance,
                },
            },
            provenance=basis.provenance,
        )
    )
    return (f"{item}.source-report", inc_key, basis_key)


def publish_shape_e(workspace: Workspace, store: Store) -> tuple[str, ...] | Blocked:
    """Relationship-edge: pointers only on the carried artifact.

    Publishes a source-report artifact independently of tax treatment so the
    ``reported_key`` pointer addresses a source-report object. Following
    either pointer requires object-store access; the pointers are not
    self-sufficient.
    """
    src = _publish_source_report(workspace, store)
    if isinstance(src, Blocked):
        return src
    outcome = _blocked_or_pair(workspace)
    if isinstance(outcome, Blocked):
        return outcome
    inc, basis = outcome
    item = _item(workspace)
    inc_key = f"{item}.includible-interest"
    reported_key = f"{item}.source-report"
    basis_key = f"{item}.basis-reduction"
    store.put(
        Artifact(
            key=inc_key,
            item=item,
            kind="includible-interest",
            payload={"amount": inc.values["includible"]},
            provenance=inc.provenance,
        )
    )
    store.put(
        Artifact(
            key=basis_key,
            item=item,
            kind="basis-reduction",
            payload={"amount": basis.values["basis"], "sibling": inc_key, "reported_key": reported_key},
            provenance=basis.provenance,
        )
    )
    return (inc_key, reported_key, basis_key)


def publish_shape_b(workspace: Workspace, store: Store) -> tuple[str, ...] | Blocked:
    src = _publish_source_report(workspace, store)
    if isinstance(src, Blocked):
        return src
    outcome = evaluate_determination(workspace)
    if isinstance(outcome, Blocked):
        return outcome
    item = _item(workspace)
    key = f"{item}.determination"
    store.put(
        Artifact(
            key=key,
            item=item,
            kind="determination",
            payload={
                "reported": outcome.values["reported"],
                "includible": outcome.values["includible"],
                "non_includible": outcome.values["non_includible"],
                "basis-reduction": outcome.values["non_includible"],
            },
            provenance=outcome.provenance,
        )
    )
    return (f"{item}.source-report", key)


SHAPES = {
    "A": publish_shape_a,
    "C": publish_shape_c,
    "E": publish_shape_e,
    "B": publish_shape_b,
}


def project_line_2b(store: Store, item: str, workspace: Workspace) -> Decimal | None:
    for art in store.current_for(item, workspace):
        if art.kind == "includible-interest":
            return Decimal(art.payload["amount"])
        if art.kind == "determination":
            return Decimal(art.payload["includible"])
    return None


def basis_artifact(store: Store, item: str) -> Artifact | None:
    for art in store.artifacts.values():
        if art.item == item and art.kind in ("basis-reduction", "determination"):
            return art
    return None


__all__ = [
    "AUTHORITY",
    "BLOCK_ITEM_MISMATCH",
    "BLOCK_UNSUPPORTED",
    "COVERAGE_ID",
    "COVERAGE_VERSION",
    "Artifact",
    "Blocked",
    "CurrentnessService",
    "Displaced",
    "Evaluation",
    "ObjectStore",
    "Provenance",
    "RULE_BASIS",
    "RULE_DETERMINATION",
    "RULE_INCLUDIBLE",
    "RULE_SOURCE_REPORT",
    "SHAPES",
    "Store",
    "basis_artifact",
    "evaluate_basis",
    "evaluate_determination",
    "evaluate_includible",
    "evaluate_reported",
    "project_line_2b",
    "publish_shape_a",
    "publish_shape_b",
    "publish_shape_c",
    "publish_shape_e",
]
