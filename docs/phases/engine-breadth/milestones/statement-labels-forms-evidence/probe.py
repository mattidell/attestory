"""Synthetic v109 inputs and adopted question inventory for statement labels."""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass
from functools import cache
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from tests.test_form_1099_withholding import (  # noqa: E402
    _base,
    _dividends,
    _interest,
    _retirements,
    _social_security,
    _social_security_withholding,
    _unemployment,
    _unemployment_withholding,
)
from tests.test_w2g_gambling import _w2g  # noqa: E402
from tests.test_withholding_closure import _set_closure  # noqa: E402
from tools import recorded_replay as rr  # noqa: E402

CORE = "v109"
P = "tax.us.2025."
LINE_25B = P + "rule.form1040-line25b"


@dataclass(frozen=True)
class Form:
    statement_kind: str
    withholding: str
    income: tuple[str, ...]


FORMS = {
    "int": Form("tax.us.1099int-statement", P + "f1099int.box4-withholding", (
        P + "f1099int.box1-interest", P + "f1099int.box3-interest",
        P + "f1099int.box8-tax-exempt-interest", P + "f1099int.box10-market-discount",
    )),
    "div": Form("tax.us.1099div-statement", P + "f1099div.box4-withholding", (
        P + "f1099div.box1a-ordinary", P + "f1099div.box2a-capital-gain-distribution",
        P + "f1099div.box12-exempt-interest-dividends",
    )),
    "ira": Form("tax.us.1099r-statement", P + "f1099r.ira-box4-withholding", (
        P + "f1099r.ira-box1-taxable-distribution",
    )),
    "g": Form("tax.us.1099g-statement", P + "f1099g.box4-withholding", (P + "f1099g.box1-unemployment",)),
    "ssa": Form("tax.us.ssa1099-statement", P + "ssa1099.box6-voluntary-withholding", (
        P + "ssa1099.box5-net-benefits",
    )),
}
LABELS = ("demo Zulu", "demo Alpha", "demo Mike")


@dataclass(frozen=True)
class Case:
    form: str
    acts: rr.Acts
    labels: tuple[str, ...]


@cache
def questions() -> dict[str, tuple[str, str]]:
    """Return adopted question sentences keyed by statement fact type, with its form."""
    core = rr.resolve_core(CORE)
    package = json.loads(core.package_path.read_text(encoding="utf-8"))
    adopted = {(m["id"], m["version"]) for m in package["members"] if m["role"] == "input-question"}
    kinds = {form.statement_kind: key for key, form in FORMS.items()}
    fact_kinds = {}
    for path in core.content.glob("*.bundle*.json"):
        bundle = json.loads(path.read_text(encoding="utf-8"))
        for fact in bundle["fact_types"]:
            for key in fact.get("identity_keys", []):
                if key["name"] == "statement" and key.get("entity_kind") in kinds:
                    fact_kinds[fact["id"], fact["version"]] = kinds[key["entity_kind"]]
    out = {}
    for path in core.content.glob("input-question.*.json"):
        citizen = json.loads(path.read_text(encoding="utf-8"))
        if (citizen["id"], citizen["version"]) not in adopted:
            continue
        fact = citizen["fact_type"]
        kind = fact_kinds.get((fact["id"], fact["version"]))
        if kind:
            out[fact["id"]] = (kind, citizen["question"])
    if set(out) != {form.withholding for form in FORMS.values()}:
        raise ValueError(f"adopted statement question inventory changed: {sorted(out)}")
    if len({text for _, text in out.values()}) != len(out):
        raise ValueError("statement questions share wording")
    return out


def return_with_amounts(key: str, amounts: tuple[float | None, ...]) -> rr.Acts:
    """One income member per statement and a closed withholding family."""
    acts = _base(wages=50000.0, w2_withheld=4500.0)
    # The base retains unused DIV and G entities from its empty-family fixtures.
    unused = {"demo.cgd.t2.stmt", "demo.ug.stmt.0"}
    acts = rr._get_harness().renumber([
        act for act in acts if act["payload"].get("entity", {}).get("id") not in unused
    ])
    size = len(amounts)
    if key == "g":
        _unemployment(acts, [6000.0, 4000.0, 2000.0][:size], authority=None)
    if key == "ssa":
        _social_security(acts, [12000.0, 8000.0, 4000.0][:size], witness=None)
    if key in {"int", "div", "ira"}:
        income = [10000.0, 5000.0, 2500.0] if key == "ira" else [500.0, 300.0, 200.0]
        add_income = {"int": _interest, "div": _dividends, "ira": _retirements}[key]
        add_income(acts, list(zip(income[:size], amounts, strict=True)))
    _unemployment_withholding(acts, list(amounts) if key == "g" else [], close=key != "g")
    _social_security_withholding(acts, list(amounts) if key == "ssa" else [], close=key != "ssa")
    _w2g(acts, [])
    return _set_closure(acts, key, "head")


def statement_entities(acts: rr.Acts, form: str) -> dict[str, dict]:
    """Introduced statements in recorded order. This is input inventory, not currency."""
    entities = {}
    for act in acts:
        entity = act["payload"].get("entity")
        if isinstance(entity, dict) and entity.get("kind") == FORMS[form].statement_kind:
            entities.setdefault(entity["id"], entity)
    return entities


def label_statements(acts: rr.Acts, form: str, labels: tuple[str, ...]) -> None:
    for entity, label in zip(statement_entities(acts, form).values(), labels, strict=True):
        entity["label"] = label


def close_sale_scope(acts: rr.Acts) -> rr.Acts:
    """Keep unrelated sale questions from blocking the line 25b pairing."""
    harness = rr._get_harness()
    acts = list(acts)
    for name in harness.OPEN_BUNDLES:
        harness.adopt(acts, name)
    for act in sale_horizons():
        family = act["payload"]["family"]["id"]
        if not harness.horizons(acts, family):
            acts.append(act)
    acts = harness.answer(acts, **harness.honest(set()))
    return harness.say(acts, rr.PRESENT_NO_SALE_BOX4, "no", "statement-labels-forms")


@cache
def sale_horizons() -> rr.Acts:
    harness = rr._get_harness()
    kinds = ("noncovered", "no1099b", "codeb")
    families = {harness.family_id(kind, term, box)
                for kind in kinds for term in harness.TERMS
                for box in (None, *harness.SALE_KINDS[kind]["kinds"])}
    return [act for act in harness.opened()
            if act["kind"] == "horizon-genesis" and act["payload"]["family"]["id"] in families]


def cases() -> dict[str, Case]:
    out = {}
    for form in FORMS:
        for name, amounts, labels, expected in (
            ("single", (None,), LABELS[:1], ("demo Zulu",)),
            ("two-missing", (None, None), LABELS[:2], ("demo Alpha", "demo Zulu")),
            ("three-one-zero", (None, 0.0, None), LABELS, ("demo Mike", "demo Zulu")),
            ("three-answered", (0.0, 20.0, 0.0), LABELS, ()),
        ):
            acts = return_with_amounts(form, amounts)
            label_statements(acts, form, labels)
            out[f"demo.{form}.{name}"] = Case(form, close_sale_scope(acts), expected)
    duplicate = return_with_amounts("int", (None, None))
    label_statements(duplicate, "int", ("demo shared", "demo shared"))
    out["demo.int.same-label"] = Case("int", close_sale_scope(duplicate), ("demo shared", "demo shared"))

    precedent = rr._module(
        "statement_labels_forms_pairing_probe", HERE.parent / "statement-withholding-pairing-evidence/probe.py",
    )
    offset = precedent._offset("int")
    label_statements(offset, "int", LABELS)
    out["demo.int.withholding-only-offset"] = Case("int", close_sale_scope(offset), ("demo Alpha",))

    unclosed = _set_closure(return_with_amounts("int", (None, 0.0)), "int", "none")
    label_statements(unclosed, "int", LABELS[:2])
    out["demo.int.unclosed"] = Case("int", close_sale_scope(unclosed), ())
    return out
