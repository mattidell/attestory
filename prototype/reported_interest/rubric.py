"""Executable checks, later-year consumer, and lifecycle observations."""

from __future__ import annotations

from dataclasses import dataclass, field, replace
from decimal import Decimal
from typing import Any, Callable, Mapping

from .model import CASES, OBLIGATION_ID, OBLIGATION_ID_THIRD, Workspace, case_ti_b2
from .shapes import (
    AUTHORITY,
    COVERAGE_ID,
    COVERAGE_VERSION,
    Artifact,
    Blocked,
    CurrentnessService,
    Displaced,
    ObjectStore,
    Provenance,
    RULE_BASIS,
    RULE_INCLUDIBLE,
    RULE_SOURCE_REPORT,
    SHAPES,
    Store,
    basis_artifact,
    evaluate_basis,
    evaluate_includible,
    project_line_2b,
)

TASK5 = "5 recover the recorded partition explanation"
TASK6 = "6 decide fact-version currentness of used dependencies"

CLASSIFICATION_WORDS = ("taxable", "includible", "excludable", "adjustment", "schedule b")


@dataclass
class ShapeRun:
    shape: str
    workspace: Workspace
    store: Store
    keys: tuple[str, ...] = ()
    blocked: Blocked | None = None
    item: str | None = None

    @property
    def is_blocked(self) -> bool:
        return self.blocked is not None

    def artifacts(self) -> tuple[Artifact, ...]:
        return tuple(self.store.artifacts[k] for k in self.keys)


def run_shape(shape: str, workspace: Workspace) -> ShapeRun:
    store = Store.empty()
    outcome = SHAPES[shape](workspace, store)
    item = workspace.facts[workspace.names.reported_obligation].value
    if isinstance(outcome, Blocked):
        return ShapeRun(
            shape,
            workspace,
            store,
            keys=tuple(store.artifacts),
            blocked=outcome,
            item=item,
        )
    return ShapeRun(shape, workspace, store, keys=outcome, item=item)


Check = Callable[[ShapeRun], tuple[bool, str]]


def statement_report_unmodified(run: ShapeRun) -> tuple[bool, str]:
    names = run.workspace.names
    fact = run.workspace.facts[names.reported_amount]
    return True, (
        f"{names.reported_box} still reads {fact.value} at version {fact.version}; "
        "derivation wrote nothing back"
    )


def ordinary_facts_recoverable(run: ShapeRun) -> tuple[bool, str]:
    names = run.workspace.names
    circumstance = [
        n
        for n in (names.bought_between_dates, names.accrued_paid_to_seller, names.accrued_relates_to)
        if n in run.workspace.facts
    ]
    detail = "; ".join(
        f"{n.rsplit('.', 1)[-1]}={run.workspace.facts[n].value}" for n in circumstance
    )
    return True, f"recoverable as supplied: {detail}"


def rule_supplies_classification(run: ShapeRun) -> tuple[bool, str]:
    offenders = [
        name
        for name, fact in run.workspace.facts.items()
        if any(w in f"{name} {fact.question}".lower() for w in CLASSIFICATION_WORDS)
    ]
    if offenders:
        return False, f"user was asked for a legal conclusion: {offenders}"
    return True, "every user-supplied fact is an ordinary circumstance or a statement reading"


def result_identifies_item(run: ShapeRun) -> tuple[bool, str]:
    if run.is_blocked:
        return True, "no result produced; nothing to mis-attribute"
    items = {a.item for a in run.artifacts()}
    if items != {run.item}:
        return False, f"artifacts attribute to {sorted(items)}, expected {run.item}"
    return True, f"item held as a field on every artifact: {run.item}"


def item_relation_verified(run: ShapeRun) -> tuple[bool, str]:
    names = run.workspace.names
    if names.accrued_relates_to not in run.workspace.facts:
        return True, "no purchase circumstance on record; no relation to verify"
    if run.blocked is not None:
        return True, f"blocked before publication: {run.blocked.code}"
    read_everywhere = all(
        names.accrued_relates_to in a.provenance.reads
        for a in run.artifacts()
        if a.kind != "source-report"
    )
    if not read_everywhere:
        return False, "the declared relation is absent from a treatment artifact's provenance"
    return True, (
        f"relation {run.workspace.facts[names.accrued_relates_to].value} compared by the engine "
        "against the item the statement covers"
    )


def provenance_matches_evaluated_rule(run: ShapeRun) -> tuple[bool, str]:
    """Each artifact's rule id is the expression that produced it, not a relabel."""
    arts = run.artifacts()
    if not arts:
        return True, "blocked; no result to account for"
    expected = {
        "includible-interest": "demo.rule.includible-interest",
        "basis-reduction": "demo.rule.basis-reduction",
        "source-report": "demo.rule.source-report",
        "determination": "demo.rule.accrued-interest-at-purchase",
    }
    for art in run.artifacts():
        want = expected[art.kind]
        if art.provenance.rule_id != want:
            return False, f"{art.key} records {art.provenance.rule_id}, expected {want}"
    return True, "; ".join(f"{a.kind}→{a.provenance.rule_id}.v{a.provenance.rule_version}" for a in run.artifacts())


def copied_fields_carry_producing_provenance(run: ShapeRun) -> tuple[bool, str]:
    """A copied payload field must keep the provenance of the evaluation that made it."""
    if run.is_blocked:
        return True, "blocked; no result to account for"
    names = run.workspace.names
    for art in run.artifacts():
        if "reported" not in art.payload or "includible" not in art.payload:
            continue
        if names.reported_amount in art.provenance.reads:
            continue
        comps = art.payload.get("components")
        if not isinstance(comps, dict):
            return False, f"{art.key} copies partition amounts with no component provenance"
        for field in ("reported", "includible"):
            prov = comps.get(field)
            if not isinstance(prov, Provenance):
                return False, f"{art.key}.{field} has no component provenance"
        expected = {
            "reported": ("demo.rule.source-report", 3),
            "includible": ("demo.rule.includible-interest", 3),
            "amount": ("demo.rule.basis-reduction", 3),
        }
        for field, (rule_id, rule_version) in expected.items():
            prov = comps.get(field)
            if not isinstance(prov, Provenance):
                return False, f"{art.key}.{field} has no component provenance"
            if prov.rule_id != rule_id or prov.rule_version != rule_version:
                return False, (
                    f"{art.key}.{field} producer {prov.rule_id}.v{prov.rule_version} "
                    f"!= {rule_id}.v{rule_version}"
                )
        if names.reported_amount not in comps["reported"].reads:
            return False, f"{art.key}.reported component omits the reported amount"
    return True, "copied fields keep the producing evaluation's provenance"


def provenance_completeness(run: ShapeRun) -> tuple[bool, str]:
    """Every fact the artifact's own evaluation read is accounted for.

    Completeness is per-rule, not a fixture-wide set stamped onto every artifact.
    Source-report accounted() must mark tax authority and coverage omitted;
    treatment accounted() must mark them present.
    """
    arts = run.artifacts()
    if not arts:
        return True, "blocked; no result to account for"
    bits = []
    for art in arts:
        accounted = art.provenance.accounted()
        missing = set(art.provenance.reads) - accounted
        if missing:
            return False, f"{art.key}: reads absent from accounted(): {sorted(missing)}"
        authority_tokens = {t for t in accounted if t.startswith("authority:")}
        coverage_tokens = {t for t in accounted if t.startswith("coverage:")}
        if art.kind == "source-report":
            if authority_tokens != {"authority:omitted"}:
                return False, f"{art.key}: source-report accounted() authority={sorted(authority_tokens)}"
            if coverage_tokens != {"coverage:omitted"}:
                return False, f"{art.key}: source-report accounted() coverage={sorted(coverage_tokens)}"
        else:
            if "authority:omitted" in authority_tokens or not (authority_tokens - {"authority:omitted"}):
                return False, f"{art.key}: treatment accounted() has no present authority"
            if coverage_tokens != {f"coverage:{COVERAGE_ID}.v{COVERAGE_VERSION}"}:
                return False, f"{art.key}: treatment accounted() coverage={sorted(coverage_tokens)}"
        bits.append(f"{art.kind}: {len(art.provenance.reads)} reads")
    return True, "; ".join(bits)


def authority_attached(run: ShapeRun) -> tuple[bool, str]:
    reports = [a for a in run.artifacts() if a.kind == "source-report"]
    tax = [a for a in run.artifacts() if a.kind != "source-report"]
    for art in reports:
        if art.provenance.authority:
            return False, (
                "source-report substantive tax-authority collection is not empty: "
                f"{tuple(a.get('citation') for a in art.provenance.authority)}"
            )
        if art.provenance.coverage_id is not None or art.provenance.coverage_version is not None:
            return False, (
                "source-report carries tax coverage "
                f"{art.provenance.coverage_id!r}.v{art.provenance.coverage_version!r}"
            )
        accounted = art.provenance.accounted()
        if "authority:omitted" not in accounted or "coverage:omitted" not in accounted:
            return False, f"{art.key}: accounted() does not mark omitted authority/coverage"
        if any(t.startswith("authority:") and t != "authority:omitted" for t in accounted):
            return False, f"{art.key}: accounted() still lists tax authority"
        if any(t.startswith("coverage:") and t != "coverage:omitted" for t in accounted):
            return False, f"{art.key}: accounted() still lists tax coverage"
    if not tax:
        if run.is_blocked:
            return True, "treatment refused; source-report authority omitted and coverage omitted"
        return True, "no tax-treatment artifact; source-report authority omitted and coverage omitted"
    expected_cites = {a["citation"] for a in AUTHORITY}
    for art in tax:
        cites = {c["citation"] for c in art.provenance.authority}
        if cites != expected_cites:
            return False, f"{art.kind} authority {sorted(cites)} != {sorted(expected_cites)}"
        if art.provenance.coverage_id != COVERAGE_ID or art.provenance.coverage_version != COVERAGE_VERSION:
            return False, (
                f"{art.kind} coverage {art.provenance.coverage_id!r}.v{art.provenance.coverage_version!r} "
                f"!= {COVERAGE_ID}.v{COVERAGE_VERSION}"
            )
        accounted = art.provenance.accounted()
        if "authority:omitted" in accounted or "coverage:omitted" in accounted:
            return False, f"{art.kind} accounted() marks present authority/coverage as omitted"
        if f"coverage:{COVERAGE_ID}.v{COVERAGE_VERSION}" not in accounted:
            return False, f"{art.kind} accounted() missing present coverage token"
        missing_auth = {f"authority:{c}" for c in expected_cites} - accounted
        if missing_auth:
            return False, f"{art.kind} accounted() missing {sorted(missing_auth)}"
    counts = {a.kind: len(a.provenance.authority) for a in tax}
    return True, (
        "source-report omits tax authority and coverage; "
        f"treatment carries IRC § 61 / Pub. 550 and accrued-interest coverage: {counts}"
    )


def basis_consequence_preserved(run: ShapeRun) -> tuple[bool, str]:
    if run.is_blocked or run.item is None:
        return True, "blocked; no consequence to carry"
    art = basis_artifact(run.store, run.item)
    if art is None:
        return False, "no basis consequence published"
    amount = art.payload.get("basis-reduction", art.payload.get("amount"))
    return True, f"basis consequence carried on {art.kind}: {amount}"


def projection_separate(run: ShapeRun) -> tuple[bool, str]:
    if run.item is None:
        return True, "blocked result projects no line-2b figure"
    line = project_line_2b(run.store, run.item, run.workspace)
    stored = any("line" in k for k in run.store.artifacts)
    if stored:
        return False, "a form line was persisted as if it were the treatment"
    return True, f"line 2b projected as {line} from the treatment, not stored on it"


def explicit_failure(run: ShapeRun) -> tuple[bool, str]:
    if run.blocked is not None:
        return True, f"failed explicitly: {run.blocked.code} {list(run.blocked.missing)}"
    return True, "case is supported; no failure expected"


RUBRIC: dict[str, Check] = {
    "statement report unmodified": statement_report_unmodified,
    "ordinary facts recoverable": ordinary_facts_recoverable,
    "rule supplies classification": rule_supplies_classification,
    "result identifies item": result_identifies_item,
    "item relation verified": item_relation_verified,
    "provenance matches evaluated rule": provenance_matches_evaluated_rule,
    "copied fields carry producing provenance": copied_fields_carry_producing_provenance,
    "provenance completeness": provenance_completeness,
    "authority attached": authority_attached,
    "basis consequence preserved": basis_consequence_preserved,
    "projection separate": projection_separate,
    "explicit failure": explicit_failure,
}


def score(shape: str, workspace: Workspace) -> dict[str, tuple[bool, str]]:
    run = run_shape(shape, workspace)
    return {name: check(run) for name, check in RUBRIC.items()}


# --- Later-year access ------------------------------------------------------


ACCESS_MODES = (
    "artifact-object-only",
    "currentness",
    "object-store-access",
    "full-workspace",
)


@dataclass
class ConsumerReport:
    shape: str
    access: str
    results: dict[str, tuple[bool, str]] = field(default_factory=dict)

    @property
    def passed(self) -> int:
        return sum(1 for ok, _ in self.results.values() if ok)


@dataclass
class LaterYearConsumer:
    """A later-year reader granted an explicit set of capabilities.

    It does not inspect shape names. It does not receive a source workspace
    unless ``access`` is ``full-workspace``.
    """

    artifact: Artifact
    access: str
    currentness: CurrentnessService | None = None
    store: ObjectStore | None = None
    workspace: Workspace | None = None

    def run(self, shape: str) -> ConsumerReport:
        rep = ConsumerReport(shape, self.access)
        carried = self.artifact

        rep.results["1 identify the obligation"] = (
            bool(carried.item),
            f"artifact attributes to {carried.item}",
        )

        amount = carried.payload.get("basis-reduction", carried.payload.get("amount"))
        cites = [a["citation"] for a in carried.provenance.authority]
        rep.results["2 recover the basis reduction with its rule and authority"] = (
            amount is not None and bool(cites),
            f"amount {amount} under {carried.provenance.rule_id}.v{carried.provenance.rule_version}, authority {cites}",
        )

        supplying = [n for n in carried.provenance.reads if n.endswith("accrued-interest-paid-to-seller")]
        rep.results["3 identify the ordinary fact that supplied the amount"] = (
            bool(supplying),
            f"provenance names {supplying or 'nothing'} as the supplying fact",
        )

        used: list = [carried.provenance]

        if self.currentness is None:
            rep.results["4 detect a corrected or displaced source-year fact"] = (
                False,
                "no currentness service granted; cannot detect an amendment",
            )
        else:
            displaced = self.currentness.displaced(carried.provenance)
            changed = sorted(
                n
                for n, v in carried.provenance.versions.items()
                if self.currentness.versions.get(n) != v
            )
            rep.results["4 detect a corrected or displaced source-year fact"] = (
                True,
                f"carried_displaced={displaced}"
                + (f", changed inputs {changed}" if changed else ", no carried input changed"),
            )

        reported, includible, sources, used_extra, task5_block = self._recover_partition(carried)
        used.extend(used_extra)
        if task5_block is not None:
            rep.results[TASK5] = (False, task5_block)
        elif reported is not None and includible is not None and amount is not None:
            ok = (Decimal(str(reported)) - Decimal(str(includible))) == Decimal(str(amount))
            rep.results[TASK5] = (
                ok,
                f"recorded partition: of {reported} reported, {includible} was includible "
                f"and {amount} was the seller's accrued interest; assembled from "
                f"{' + '.join(sources)}. Reconstruction is not a currentness grant.",
            )
        else:
            unavailable = [
                label
                for label, value in (("reported", reported), ("includible", includible))
                if value is None
            ]
            rep.results[TASK5] = (
                False,
                f"the amount {amount}, its rule, and its authority are recoverable, but "
                f"{unavailable} are not under access {self.access!r}",
            )

        if self.currentness is None:
            rep.results[TASK6] = (
                False,
                "no currentness service granted; fact-version currentness is unknown. "
                "A recorded partition (task 5) is not a current explanation. "
                "Does not decide rule, authority, coverage, or reporting succession. "
                "An unamended fixture is harness knowledge, not a consumer capability.",
            )
        else:
            stale = [p for p in used if self.currentness.displaced(p)]
            current = not stale
            meaning = (
                "recorded partition is historical"
                if not current
                else "fact versions of used dependencies match under the granted service"
            )
            rep.results[TASK6] = (
                True,
                f"fact_version_current={current}; "
                f"stale_components={len(stale)}; {meaning}. "
                "A current explanation requires task 5 and fact_version_current=True. "
                "assumed unchanged: rule, authority, coverage declaration, reporting contract. "
                "Does not decide general later-year usability.",
            )
        return rep

    def _component(self, carried: Artifact, field: str):
        comps = carried.payload.get("components")
        if isinstance(comps, dict):
            return comps.get(field)
        return None

    def _resolve_target(
        self,
        key: str,
        expected_kind: str,
        expected_rule: tuple[str, int],
        carried: Artifact,
    ):
        if self.store is None:
            return None, "no-store", None
        art = self.store.get(key)
        if art is None:
            return None, "missing-target", None
        if art.key != key:
            return None, f"self-key-mismatch:{art.key}", None
        if art.item != carried.item:
            return None, f"foreign-item:{art.item}", None
        if art.kind != expected_kind:
            return None, f"wrong-kind:{art.kind}", None
        if art.provenance.rule_id != expected_rule[0]:
            return None, f"wrong-rule:{art.provenance.rule_id}", None
        if art.provenance.rule_version != expected_rule[1]:
            return None, f"wrong-rule-version:{art.provenance.rule_version}", None
        return art.payload.get("amount"), "ok", art

    def _recover_partition(
        self, carried: Artifact
    ) -> tuple[Any, Any, list[str], list, str | None]:
        reported = carried.payload.get("reported")
        includible = carried.payload.get("includible")
        sources = ["the carried artifact"]
        used: list = []
        expected_components = {
            "reported": RULE_SOURCE_REPORT,
            "includible": RULE_INCLUDIBLE,
            "amount": RULE_BASIS,
        }
        for field, expected_rule in expected_components.items():
            prov = self._component(carried, field)
            if not isinstance(prov, Provenance):
                continue
            used.append(prov)
            if prov.rule_id != expected_rule[0] or prov.rule_version != expected_rule[1]:
                return (
                    None,
                    None,
                    sources,
                    used,
                    f"component {field} wrong producer {prov.rule_id}.v{prov.rule_version}",
                )

        if self.store is not None:
            sib_key = carried.payload.get("sibling")
            if includible is None and isinstance(sib_key, str):
                value, reason, art = self._resolve_target(
                    sib_key, "includible-interest", RULE_INCLUDIBLE, carried
                )
                if reason == "ok":
                    includible = value
                    sources.append("object store via sibling")
                    if art is not None:
                        used.append(art.provenance)
                elif reason != "no-store":
                    return None, None, sources, used, f"sibling {reason}"
            rep_key = carried.payload.get("reported_key")
            if reported is None and isinstance(rep_key, str):
                value, reason, art = self._resolve_target(
                    rep_key, "source-report", RULE_SOURCE_REPORT, carried
                )
                if reason == "ok":
                    reported = value
                    sources.append("object store via reported_key")
                    if art is not None:
                        used.append(art.provenance)
                elif reason != "no-store":
                    return None, None, sources, used, f"reported_key {reason}"

        if self.workspace is not None:
            names = self.workspace.names
            if reported is None:
                fact = self.workspace.facts.get(names.reported_amount)
                if fact is not None:
                    reported = Decimal(str(fact.value))
                    sources.append("source-year workspace fact")
            if includible is None and self.store is not None:
                for art in self.store.artifacts.values():
                    if art.kind == "includible-interest" and art.item == carried.item:
                        includible = art.payload.get("amount")
                        sources.append("source-year sibling in the object store")
                        used.append(art.provenance)
                        break
        return reported, includible, sources, used, None


def grant(run: ShapeRun, access: str, later_workspace: Workspace | None) -> LaterYearConsumer:
    """Build a consumer under one named access mode. No undeclared inputs."""
    assert run.item is not None
    carried = basis_artifact(run.store, run.item)
    assert carried is not None
    if access == "artifact-object-only":
        return LaterYearConsumer(carried, access)
    if access == "currentness":
        ws = later_workspace if later_workspace is not None else run.workspace
        return LaterYearConsumer(carried, access, currentness=CurrentnessService.from_workspace(ws))
    if access == "object-store-access":
        return LaterYearConsumer(carried, access, store=run.store.as_object_store())
    if access == "full-workspace":
        ws = later_workspace if later_workspace is not None else run.workspace
        return LaterYearConsumer(
            carried,
            access,
            currentness=CurrentnessService.from_workspace(ws),
            store=run.store.as_object_store(),
            workspace=ws,
        )
    raise ValueError(access)


def later_year_probe() -> dict[str, Any]:
    base = case_ti_b2()
    amended = base.with_correction(base.names.accrued_paid_to_seller, 250)
    out: dict[str, Any] = {}
    for shape in SHAPES:
        run = run_shape(shape, base)
        assert run.item is not None
        for access in ACCESS_MODES:
            unchanged = grant(run, access, base).run(shape)
            after = grant(run, access, amended).run(shape)
            out[f"{shape}/{access}: source year unamended"] = dict(unchanged.results)
            out[f"{shape}/{access}: passed"] = f"{unchanged.passed}/6"
            out[f"{shape}/{access}: after amendment, task 4"] = after.results[
                "4 detect a corrected or displaced source-year fact"
            ]
            out[f"{shape}/{access}: after amendment, task 6"] = after.results[TASK6]
            source = grant(run, access, base.with_correction(base.names.reported_amount, 1000)).run(shape)
            out[f"{shape}/{access}: after source correction, task 4"] = source.results[
                "4 detect a corrected or displaced source-year fact"
            ]
            out[f"{shape}/{access}: after source correction, task 5"] = source.results[TASK5]
            out[f"{shape}/{access}: after source correction, task 6"] = source.results[TASK6]
    return out


def mutate_payload(art: Artifact, **changes: Any) -> Artifact:
    payload = dict(art.payload)
    for key, value in changes.items():
        if value is None:
            payload.pop(key, None)
        else:
            payload[key] = value
    return replace(art, payload=payload)


def currentness_probe() -> dict[str, Any]:
    base = case_ti_b2()
    circ = base.with_correction(base.names.accrued_paid_to_seller, 250)
    source = base.with_correction(base.names.reported_amount, 1000)
    kind = base.with_correction(base.names.obligation_kind, "series-ee-savings-bond")
    out: dict[str, Any] = {}
    for shape in SHAPES:
        run = run_shape(shape, base)
        item = run.item
        assert item is not None
        for label, corrected in (
            ("circumstance correction", circ),
            ("source correction", source),
            ("obligation-kind correction", kind),
        ):
            out[f"{shape}: {label} displaces"] = run.store.displaced_for(item, corrected)
            out[f"{shape}: {label} leaves current"] = tuple(
                sorted(a.key for a in run.store.current_for(item, corrected))
            )
            refused = []
            for key in run.keys:
                try:
                    run.store.serve(key, corrected)
                except Displaced:
                    refused.append(key)
            out[f"{shape}: {label} refused on serve"] = tuple(sorted(refused))
        out[f"{shape}: artifacts published"] = run.keys
    return out


def independent_lifecycle() -> dict[str, tuple[bool, str]]:
    """Per-artifact displacement under each of the eight fixture facts."""
    base = case_ti_b2()
    names = base.names
    corrections: dict[str, tuple[str, Any]] = {
        "reported amount": (names.reported_amount, 1000),
        "payer": (names.reported_payer, "demo.payer.bank-2"),
        "statement obligation": (names.reported_obligation, OBLIGATION_ID_THIRD),
        "bought-between-dates": (names.bought_between_dates, "no"),
        "accrued amount": (names.accrued_paid_to_seller, 250),
        "declared relation": (names.accrued_relates_to, OBLIGATION_ID_THIRD),
        "obligation kind": (names.obligation_kind, "series-ee-savings-bond"),
        "education answer": (names.education_expenses, "yes"),
    }
    out: dict[str, tuple[bool, str]] = {}
    for shape in SHAPES:
        run = run_shape(shape, base)
        assert run.item is not None
        for label, (name, value) in corrections.items():
            corrected = base.with_correction(name, value)
            for art in run.artifacts():
                in_prov = name in art.provenance.reads
                displaced = art.provenance.displaced_by(corrected)
                ok = displaced is in_prov
                out[f"{shape}: {label} vs {art.kind}"] = (
                    ok,
                    f"in_provenance={in_prov}, displaced={displaced}",
                )
    return out


__all__ = [
    "ACCESS_MODES",
    "CLASSIFICATION_WORDS",
    "ConsumerReport",
    "LaterYearConsumer",
    "OBLIGATION_ID",
    "RUBRIC",
    "ShapeRun",
    "TASK5",
    "TASK6",
    "currentness_probe",
    "grant",
    "independent_lifecycle",
    "later_year_probe",
    "mutate_payload",
    "run_shape",
    "score",
]
