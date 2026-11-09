"""Self-contained harness for the sale family audit (P0).

Evidence for docs/phases/engine-breadth/milestones/sale-family-audit.md.
Builds synthetic ``demo.*`` returns with sales on every Form 1099-B and
Form 8949 family of core v81 and runs them through ``live_coordinate_run``
on a core named by a ``Core`` value.

This module imports no other evidence module and changes no other module's
globals. Every core (the published v81, or the scratch v82 the prototype
builds) is passed explicitly as a ``Core``. The only in-process change is the
two per-package loader entries a scratch core needs (``loader_entries``),
applied inside a context manager for one run and restored afterwards; Track 1
would add them to ``packages/tax/loader.py``.

It reuses only plain act-building functions from ``tests/`` (``_add``,
``_introduce``, ``_attested``, ``_finish``, ``_handover``), which read and
write the act list they are given and nothing else.
"""

from __future__ import annotations

import contextlib
import copy
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any, Callable, Iterator

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from packages.derivation.live import live_coordinate_run  # noqa: E402
from packages.derivation.live_workspace import WorkspaceCapability  # noqa: E402
from packages.derivation.production_resolver import PublicationSurface  # noqa: E402
from packages.kernel.facts import fact_id_for  # noqa: E402
from packages.tax import loader  # noqa: E402
from tests.helpers import current_core_returns as ccr  # noqa: E402
from tests.test_form_1099_k_income import _handover  # noqa: E402
from tests.test_form_1099_withholding import YEAR, _add, _close, _introduce  # noqa: E402
from tests.test_refund_or_amount_owed_track1 import _attested, _finish  # noqa: E402

Acts = list[dict[str, Any]]
P = "tax.us.2025."
PKG = P + "package.core-calculations"
CONTENT = REPO / "packages/content/tax/2025"
RELEASES = REPO / "packages/sample_data/student_loan_worksheet_integration/publication_surface/releases"
RELEASE_STEM = "demo.release.sli-worksheet-integration.2025"


@dataclass(frozen=True)
class Core:
    """One core: package, registry and release, and the directories that hold them."""

    version: str
    registry: str
    release_version: str
    content: Path = CONTENT
    releases: Path = RELEASES
    # Loader entries a scratch core needs: {"from": "v81"} names the published
    # core whose companion declaration and covered-flag map it copies.
    loader_from: str | None = None

    @property
    def package_path(self) -> Path:
        return self.content / f"package.core-calculations.{self.version}.json"

    @property
    def release_path(self) -> Path:
        return self.releases / f"{RELEASE_STEM}.{self.release_version}.json"

    def surface(self) -> PublicationSurface:
        return PublicationSurface(self.releases, self.content / f"published-packages.{self.registry}.json", self.content)


V81 = Core("v81", "v79", "v79")


@contextlib.contextmanager
def loader_entries(core: Core) -> Iterator[None]:
    """For a scratch core, the two loader entries its predecessor has, for one run only."""
    if core.loader_from is None:
        yield
        return
    saved = (loader.domain_package_companion_declarations, loader.named_covered_flag_refusal_maps)
    source = (PKG, core.loader_from)
    target = (PKG, core.version)

    def declarations() -> dict[tuple[str, str], dict[str, Any]]:
        found = dict(saved[0]())
        found[target] = copy.deepcopy(found[source])
        return found

    def refusal() -> dict[tuple[str, str], dict[str, str]]:
        found = dict(saved[1]())
        found[target] = dict(found[source])
        return found

    loader.domain_package_companion_declarations = declarations  # type: ignore[assignment]
    loader.named_covered_flag_refusal_maps = refusal  # type: ignore[assignment]
    try:
        yield
    finally:
        loader.domain_package_companion_declarations, loader.named_covered_flag_refusal_maps = saved  # type: ignore[assignment]


# ---- vocabulary --------------------------------------------------------------------

Q1 = P + "f1099b.noncovered-sold.source-closure"
Q2 = P + "f8949.no1099b-sold.source-closure"
Q3 = P + "f1099b.code-b-sold.source-closure"
IC79 = P + "schedule-d-boundary.noncovered-in-class"
IC80 = P + "schedule-d-boundary.form8949-in-class"
IC81 = P + "schedule-d-boundary.form8949-code-b-in-class"
NO_8949 = P + "schedule-d-boundary.no-form8949-sources"
PATH_B = P + "schedule-d-boundary.no-other-form8949-adjustments"
LINES_18_19 = P + "schedule-d-boundary.no-lines-18-19-sources"
NO_OTHER_SD = P + "schedule-d-boundary.no-other-schedule-d-sources"
NO_DA_QOF = P + "schedule-d-boundary.no-1099da-or-qof"
# Exception 1 (Schedule D not required): one question, "Besides capital gain
# distributions in box 2a of Form 1099-DIV, did you have any other capital gain
# or loss in 2025 ...?". A filer with any sale answers it yes, which records
# only-box2a-capital-gains "no" (and no-capital-losses "no" when a sale is a loss).
EXC1_ONLY_2A = P + "exception1.only-box2a-capital-gains"
EXC1_NO_LOSSES = P + "exception1.no-capital-losses"

# The bundles a v81 return with every sale family open adopts (production files).
OPEN_BUNDLES = (
    "f1099b-noncovered-st.bundle.json", "f1099b-noncovered-lt.bundle.json",
    "schedule-d-boundary-noncovered.bundle.json", "f1099b-noncovered-amounts-check.bundle.json",
    "f8949-no1099b-st.bundle.json", "f8949-no1099b-lt.bundle.json",
    "schedule-d-boundary-form8949-in-class.bundle.json",
    "f1099b-code-b-st.bundle.json", "f1099b-code-b-lt.bundle.json",
    "schedule-d-boundary-form8949-code-b-in-class.bundle.json",
    "schedule-d-boundary-form8949-w.bundle.json",
)
TERMS = ("st", "lt")
KINDS = ("proceeds", "basis", "adjustment")


def _read(name: str) -> dict[str, Any]:
    return json.loads((CONTENT / name).read_text(encoding="utf-8"))


def _bundle_facts() -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    for name in ("schedule-d-boundary.bundle.json", *OPEN_BUNDLES):
        for fact in _read(name)["fact_types"]:
            out[fact["id"]] = fact
    return out


FACTS = _bundle_facts()
BUNDLE_OF = {fact: name for name in ("schedule-d-boundary.bundle.json", *OPEN_BUNDLES)
             for fact in (f["id"] for f in _read(name)["fact_types"])}

# Each sale kind: family stem, member stem, family version, the scalar kinds it has,
# whether its closure is per family (covered) or grouped (the answer named).
SALE_KINDS: dict[str, dict[str, Any]] = {
    "covered": {"family": "f1099b.covered-{t}", "member": "f1099b.covered-{t}-txn", "version": "v1",
                "kinds": ("proceeds", "basis"), "grouped": None, "keys": "broker"},
    "w": {"family": "f1099b.covered-w-{t}", "member": "f1099b.covered-w-{t}-txn", "version": "v2",
          "kinds": KINDS, "grouped": None, "keys": "broker"},
    "noncovered": {"family": "f1099b.noncovered-{t}", "member": "f1099b.noncovered-{t}-txn", "version": "v1",
                   "kinds": KINDS, "grouped": Q1, "keys": "broker"},
    "no1099b": {"family": "f8949.no1099b-{t}", "member": "f8949.no1099b-{t}-txn", "version": "v1",
                "kinds": KINDS, "grouped": Q2, "keys": "sale"},
    "codeb": {"family": "f1099b.code-b-{t}", "member": "f1099b.code-b-{t}-txn", "version": "v1",
              "kinds": KINDS, "grouped": Q3, "keys": "broker"},
}


def family_id(kind: str, term: str, scalar: str | None = None) -> str:
    stem = P + SALE_KINDS[kind]["family"].format(t=term)
    return stem if scalar is None else f"{stem}-{scalar}"


def member_fact(kind: str, term: str, scalar: str | None = None) -> str:
    stem = P + SALE_KINDS[kind]["member"].format(t=term)
    return stem if scalar is None else f"{stem}.{scalar}"


# ---- act building -----------------------------------------------------------------


def _adopted(acts: Acts) -> set[str]:
    return {f["id"] for a in acts if a.get("kind") == "bundle-adoption"
            for f in (a["payload"].get("bundle") or {}).get("fact_types") or []}


def adopt(acts: Acts, name: str) -> None:
    body = _read(name)
    if not {f["id"] for f in body["fact_types"]} & _adopted(acts):
        _add(acts, "bundle-adoption", {"bundle": body})


def horizons(acts: Acts, family: str) -> list[str]:
    out: list[str] = []
    for act in acts:
        payload = act.get("payload") or {}
        fam = payload.get("family") if isinstance(payload, dict) else None
        if not isinstance(fam, dict) or fam.get("id") != family:
            continue
        if act["kind"] == "horizon-genesis":
            out.append(str(payload["horizon_id"]))
        elif act["kind"] == "member-transition":
            out.append(str(payload["successor"]["id"]))
    return out


def strip(acts: Acts, prefix: str) -> Acts:
    """``acts`` without any finding whose fact id starts with ``prefix|``."""
    kept = []
    for act in acts:
        payload = act.get("payload")
        finding = payload.get("finding") if isinstance(payload, dict) else None
        if isinstance(finding, dict) and str(finding.get("fact_id", "")).startswith(prefix + "|"):
            continue
        kept.append(act)
    return kept


def renumber(acts: Acts) -> Acts:
    return ccr._renumbered(acts)


def opened() -> Acts:
    """The harness wage return (single, wages 50,000, 4,500 withheld) with every v81 sale family open.

    Covered and code W families come closed-empty from the base. The
    noncovered, no-1099-B and code B families get a genesis here and are
    closed by their grouped answers (``answer``).
    """
    acts = copy.deepcopy(ccr.base_return())
    for name in OPEN_BUNDLES:
        adopt(acts, name)
    for kind in ("noncovered", "no1099b", "codeb"):
        for term in TERMS:
            for scalar in (None, *SALE_KINDS[kind]["kinds"]):
                fam = family_id(kind, term, scalar)
                _add(acts, "horizon-genesis", {
                    "family": {"id": fam, "version": SALE_KINDS[kind]["version"]},
                    "scope": {"tax-year": YEAR, "subject": "demo.primary"},
                    "horizon_id": f"demo.sfa.{fam.removeprefix(P)}.h0",
                })
    return renumber(acts)


def _identity(acts: Acts, kind: str, tag: str) -> tuple[tuple[str, str], ...]:
    if SALE_KINDS[kind]["keys"] == "sale":
        entity = f"demo.sfa.{tag}.sale"
        if entity not in _entities(acts):
            _introduce(acts, entity, "tax.us.f8949-sale")
        return (("sale", entity), ("tax-year", YEAR))
    declared = []
    for name, entity_kind in (("broker", "tax.us.f1099b-broker"), ("statement", "tax.us.f1099b-statement"),
                              ("transaction", "tax.us.f1099b-transaction")):
        entity = f"demo.sfa.{tag}.{name}"
        if entity not in _entities(acts):
            _introduce(acts, entity, entity_kind)
        declared.append((name, entity))
    return (*declared, ("tax-year", YEAR))


def _entities(acts: Acts) -> set[str]:
    return {str(a["payload"]["entity"]["id"]) for a in acts if a.get("kind") == "entity-introduced"}


def _member(acts: Acts, kind: str, term: str, scalar: str | None, value: object, tag: str) -> Acts:
    fam = family_id(kind, term, scalar)
    closure = fam + ".source-closure"
    per_family = SALE_KINDS[kind]["grouped"] is None
    if per_family:
        acts = strip(acts, closure)
    declared = _identity(acts, kind, tag)
    head = horizons(acts, fam)[-1]
    successor = f"demo.sfa.{tag}.{fam.removeprefix(P)}.h{len(horizons(acts, fam))}"
    _add(acts, "member-transition", {
        "family": {"id": fam, "version": SALE_KINDS[kind]["version"]},
        "scope": {"tax-year": YEAR, "subject": "demo.primary"},
        "member": {"action": "assert", "finding": _attested(
            f"demo.sfa.{tag}.{fam.removeprefix(P)}.member{len(horizons(acts, fam))}",
            fact_id_for(member_fact(kind, term, scalar), declared), value)},
        "successor": {"id": successor, "predecessor": head},
    })
    if per_family:
        _close(acts, closure, successor, f"demo.sfa.{tag}.{fam.removeprefix(P)}.closure")
    return acts


FLAGS = ("box_1f_market_discount", "ordinary_indicated", "qof_indicated", "taxpayer_side_adjustment",
         "collectibles_or_special_rate")


def sale(acts: Acts, kind: str, term: str, *, proceeds: float, basis: float, tag: str, wash: float = 0.0,
         corrected: float | None = None, long_term: str | None = None, rows: dict[str, float | None] | None = None,
         **fields: Any) -> Acts:
    """One sale of ``kind`` with its scalar rows; ``rows`` overrides a row (None leaves it out).

    The sale object's fields follow the v81 bundle for its kind; ``fields``
    overrides any of them (for example a covered flag).
    """
    lt = long_term or ("yes" if term == "lt" else "no")
    value: dict[str, Any]
    if kind in ("covered", "w"):
        value = {"proceeds": proceeds, "basis": basis, "covered_security": "yes", "basis_reported_to_irs": "yes",
                 "long_term": lt, "box_1g_wash_sale_adjustment": "yes" if kind == "w" else "no",
                 **{flag: "no" for flag in FLAGS}}
        if kind == "w":
            value["box_1g_wash_sale_disallowed_amount"] = wash
    elif kind == "noncovered":
        value = {"proceeds": proceeds, "basis": basis, "basis_reported_to_irs": "no", "long_term": lt,
                 "wash_disallowed": wash}
    elif kind == "no1099b":
        value = {"proceeds": proceeds, "basis": basis, "long_term": lt, "wash_disallowed": wash}
    else:
        value = {"proceeds": proceeds, "basis": basis, "long_term": lt, "wash_disallowed": wash,
                 "corrected_basis": basis if corrected is None else corrected}
    value.update(fields)
    acts = _member(acts, kind, term, None, value, tag)
    amounts: dict[str, float | None] = {"proceeds": proceeds, "basis": basis, "adjustment": wash}
    if kind == "codeb":
        amounts["adjustment"] = basis - (basis if corrected is None else corrected) + wash
    if kind == "w" or kind == "covered":
        pass
    amounts.update(rows or {})
    for scalar in SALE_KINDS[kind]["kinds"]:
        if amounts.get(scalar) is not None:
            if kind in ("noncovered", "no1099b") and scalar == "adjustment" and not wash and "adjustment" not in (rows or {}):
                continue
            acts = _member(acts, kind, term, scalar, amounts[scalar], tag)
    return renumber(acts)


_FOUND: dict[tuple[str, str], dict[str, Any] | None] = {}


def bundle_for(fact_type: str, content: Path) -> dict[str, Any] | None:
    """The bundle in ``content`` that declares ``fact_type`` (for a fact a scratch core adds)."""
    key = (str(content), fact_type)
    if key not in _FOUND:
        _FOUND[key] = None
        for path in sorted(content.glob("*.bundle.json")):
            body = json.loads(path.read_text(encoding="utf-8"))
            if any(f.get("id") == fact_type for f in body.get("fact_types") or []):
                _FOUND[key] = body
    return _FOUND[key]


def say(acts: Acts, fact_type: str, value: object, tag: str, content: Path = CONTENT) -> Acts:
    """Assert a return-level answer, replacing any earlier one."""
    acts = strip(acts, fact_type)
    name = BUNDLE_OF.get(fact_type)
    if name is not None:
        adopt(acts, name)
    else:
        body = bundle_for(fact_type, content)
        if body is not None and not {f["id"] for f in body["fact_types"]} & _adopted(acts):
            _add(acts, "bundle-adoption", {"bundle": body})
    _add(acts, "assertion", {"finding": _attested(f"demo.sfa.answer.{tag}", fact_id_for(fact_type, (("tax-year", YEAR),)),
                                                   value)})
    return renumber(acts)


# The honest answer set for a return whose sales are all in class: what a filer
# with only these sales answers. Keys: q1 q2 q3 (grouped closures), form8949
# (no-form8949-sources), path_b, ic79 ic80 ic81, and the three other boundaries.
ANSWER_FACT = {"q1": Q1, "q2": Q2, "q3": Q3, "form8949": NO_8949, "path_b": PATH_B, "ic79": IC79, "ic80": IC80,
               "ic81": IC81, "lines_18_19": LINES_18_19, "no_other_sd": NO_OTHER_SD, "no_da_qof": NO_DA_QOF,
               "exc1_only_2a": EXC1_ONLY_2A, "exc1_no_losses": EXC1_NO_LOSSES,
               # Asked only by the scratch core v82 (prototype.py box4_question, box7_question).
               "box4": P + "f1099b.box4-withholding-reported", "box7": P + "f1099b.box7-loss-not-allowed"}


def answer(acts: Acts, content: Path = CONTENT, **answers: str | None) -> Acts:
    for key, value in answers.items():
        if value is not None:
            acts = say(acts, ANSWER_FACT[key], value, key, content)
    return acts


def honest(kinds: set[str], *, loss: bool = False, new_questions: bool = False) -> dict[str, str | None]:
    """The answers a filer gives when every sale is in class and of these kinds.

    ``loss``: some sale is a loss (Exception 1's no-capital-losses is then "no").
    ``new_questions``: the core asks the Form 1099-B box 4 and box 7 questions.
    """
    form8949 = kinds & {"w", "noncovered", "no1099b", "codeb"}
    form_1099b = bool(kinds & {"covered", "w", "noncovered", "codeb"})
    out: dict[str, str | None] = {
        "box4": "no" if new_questions and form_1099b else None,
        "box7": "no" if new_questions and form_1099b else None,
        "exc1_only_2a": "no" if kinds else None,
        "exc1_no_losses": "no" if loss else None,
        "q1": "yes" if "noncovered" in kinds else "no",
        "q2": "yes" if "no1099b" in kinds else "no",
        "q3": "yes" if "codeb" in kinds else "no",
        "form8949": "no" if form8949 else "yes",
        # Path B: no code other than W and no basis-not-reported source.
        "path_b": None if not form8949 else ("yes" if form8949 <= {"w"} else "no"),
        "ic79": None, "ic80": None, "ic81": None,
    }
    if form8949 - {"w"}:
        out["ic81"] = "yes" if "codeb" in kinds else None
        out["ic80"] = "yes" if "codeb" not in kinds and "no1099b" in kinds else None
        out["ic79"] = "yes" if not kinds & {"codeb", "no1099b"} else None
    return out


# ---- running ------------------------------------------------------------------------

WATCH = tuple(P + f"schedule-d.line-{n}" for n in ("1a", "1b", "2", "3", "7", "8a", "8b", "9", "10", "15", "16", "21")) + \
    tuple(P + f"form1040.line-{n}" for n in ("7a", "9", "15", "16", "24", "25b", "33", "34", "37"))
SYMBOLS = (P + "capital-gains.selected-preferential-base", P + "payments.line25b")
ROW_FILTER = ("schedule-d", "line7a", "preferential", "8949", "f1099b", "f8949", "line25b")


def scrub(text: str) -> str:
    text = text.replace(str(REPO), ".")
    return re.sub(r"/(?:Users|private|tmp|var|opt)/\S+", "<path>", text)


def summarize(outcome: Any) -> dict[str, Any]:
    if outcome.refusal is not None:
        return {"refusal": {"reason": outcome.refusal.reason, "detail": scrub(str(outcome.refusal.detail))[:300]}}
    report = json.loads(outcome.output_path.read_text(encoding="utf-8"))
    model = json.loads(outcome.presentation_path.read_text(encoding="utf-8"))
    lines: dict[str, Any] = {}
    questions: list[str] = []
    for section in model.get("sections") or []:
        field_id = str((section.get("field") or {}).get("id") or "")
        resolved = section.get("resolved") or {}
        for reason in resolved.get("reasons") or []:
            sentence = str(reason.get("sentence") or "").strip() if isinstance(reason, dict) else ""
            if sentence.endswith("?") and sentence not in questions:
                questions.append(sentence)
        if field_id in WATCH:
            value = resolved.get("value")
            if isinstance(value, float) and value.is_integer():
                value = int(value)
            disposition = str(resolved.get("disposition"))
            lines[field_id.removeprefix(P)] = disposition if value is None or "blocked" in disposition else value
    blocked = []
    for row in report.get("dispositions") or []:
        artifact = str(row.get("artifact_id", ""))
        if row.get("disposition") == "blocked" and any(t in artifact for t in ROW_FILTER):
            blocked.append([artifact.removeprefix(P + "rule."), row.get("code"),
                            [str(m).removeprefix(P) for m in row.get("missing") or []][:4]])
    return {
        "stop": report.get("stop_reason"),
        "lines": lines,
        "symbols": {str(p.finding.get("symbol")).removeprefix(P): p.finding.get("value")
                    for p in outcome.publications or () if str(p.finding.get("symbol")) in SYMBOLS},
        "attachments": {str(a.get("id")).split(".")[-1]: (a.get("resolved") or {}).get("disposition")
                        for a in model.get("attachments") or []
                        if "8949" in str(a.get("id")) or "schedule-d" in str(a.get("id"))},
        "blocked": blocked[:20],
        "questions": [scrub(q)[:200] for q in questions[:10]],
    }


def run(core: Core, acts: Acts, run_id: str) -> dict[str, Any]:
    """Adopt ``core`` on ``acts`` and run them through the real coordinator."""
    surface = core.surface()
    with loader_entries(core):
        try:
            finished = _handover(_finish(copy.deepcopy(acts), package_path=core.package_path,
                                         package_version=core.version, release_path=core.release_path,
                                         release_version=core.release_version, note=run_id),
                                 surface=surface, reconfirm=True)
            with TemporaryDirectory() as tmp:
                outcome = live_coordinate_run(
                    WorkspaceCapability(Path(tmp) / "L"), repo_root=REPO, authoritative_acts=finished,
                    workspace_revision=len(finished), run_scope={"jurisdiction": "us", "year": YEAR},
                    scope_user=ccr.USER, request={"schema": "run-request.v1"}, run_id=run_id,
                    governance_pins=[], surface=surface, output_name="out.json")
                return summarize(outcome)
        except Exception as exc:  # noqa: BLE001 — a rejected act list is a result, not a crash
            return {"error": type(exc).__name__, "message": scrub(str(exc))[:400]}


@dataclass
class Case:
    """One probe: how to build it, and the hand values it must show on a correct core."""

    build: Callable[[], Acts]
    hand: dict[str, Any] = field(default_factory=dict)
    note: str = ""
