"""Core v81 is the scratch v81 Track 0 proved, published as successors only.

Static checks on the published package, registry, release and loader entries
for Form 1099-B sales whose reported basis is wrong (code B) and the four
inherited v80 fixes of Decision 6. The cases run through the coordinator in
tests/test_code_b_sales_v81.py.

The successor bodies are rebuilt from ``codeb_prototype.artifacts()``, which
reads only the published predecessors, and compared byte for byte.
"""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path
from typing import Any

import pytest

from packages.tax.loader import (
    COVERED_FLAG_REFUSAL_OBJECTS,
    code_b_scalar_presence_pairs,
    covered_flag_refusal_map,
    domain_package_companion_declarations,
)

REPO = Path(__file__).resolve().parents[1]
CONTENT = REPO / "packages/content/tax/2025"
RELEASES = REPO / "packages/sample_data/student_loan_worksheet_integration/publication_surface/releases"
EVIDENCE = REPO / "docs/phases/engine-breadth/milestones/f8949-code-b-evidence"
CORE = "tax.us.2025.package.core-calculations"
P = "tax.us.2025."


def _load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def prototype() -> tuple[Any, list[tuple[str, dict[str, Any]]], dict[tuple[str, str], tuple[str, str]]]:
    name = "f8949_code_b_prototype"
    module = sys.modules.get(name)
    if module is None:
        spec = importlib.util.spec_from_file_location(name, EVIDENCE / "codeb_prototype.py")
        assert spec is not None and spec.loader is not None
        module = importlib.util.module_from_spec(spec)
        sys.modules[name] = module
        spec.loader.exec_module(module)
    assert module.REPAIRS == set(module.ALL_REPAIRS)
    module.ORIGIN[:] = [CONTENT, RELEASES]
    bodies, old = module.artifacts()
    return module, bodies, old


def test_every_successor_is_the_prototype_byte_for_byte(prototype: Any) -> None:
    _module, bodies, _old = prototype
    assert len(bodies) == 80
    for name, body in bodies:
        assert (CONTENT / name).read_bytes() == (json.dumps(body, indent=2) + "\n").encode("utf-8"), name


def test_core_v81_is_v80_with_exactly_the_prototype_member_edits(prototype: Any) -> None:
    module, bodies, old = prototype
    v80 = _load(CONTENT / "package.core-calculations.v80.json")
    v81 = _load(CONTENT / "package.core-calculations.v81.json")
    assert (v81["id"], v81["version"]) == (CORE, "v81")
    members = {(m["id"], m["version"]): m for m in v80["members"]}
    adds = replaces = 0
    for _name, body in bodies:
        new = {"id": body["id"], "version": body["version"], "schema": body["schema"],
               "role": module.ROLE.get(body["schema"], "computation")}
        key = (body["id"], body["version"])
        if key in old:
            prior_version, prior_schema = old[key]
            assert members.pop((body["id"], prior_version)) == {**new, "version": prior_version, "schema": prior_schema}
            replaces += 1
        else:
            adds += 1
        assert key not in members
        members[key] = new
    assert (adds, replaces) == (50, 30)
    assert sorted(members) == sorted((m["id"], m["version"]) for m in v81["members"])
    for member in v81["members"]:
        assert members[(member["id"], member["version"])] == member


def test_registry_v79_only_adds_to_v78() -> None:
    v78 = _load(CONTENT / "published-packages.v78.json")
    v79 = _load(CONTENT / "published-packages.v79.json")
    for key in ("citizens", "packages"):
        before = {(e["id"], e["version"]): e for e in v78[key]}
        after = {(e["id"], e["version"]): e for e in v79[key]}
        for identity, entry in before.items():
            assert after[identity] == entry, identity
    added = {(e["id"], e["version"]) for e in v79["packages"]} - {(e["id"], e["version"]) for e in v78["packages"]}
    assert added == {(CORE, "v81")}


def test_release_v79_pins_registry_v79() -> None:
    import hashlib

    release = _load(RELEASES / "demo.release.sli-worksheet-integration.2025.v79.json")
    assert release["version"] == "v79"
    registry = (CONTENT / "published-packages.v79.json").read_bytes()
    assert release["package_registry_sha256"] == hashlib.sha256(registry).hexdigest()


def test_core_v81_declares_each_code_b_amount_beside_its_sale() -> None:
    declarations = domain_package_companion_declarations()
    v80, v81 = declarations[(CORE, "v80")], declarations[(CORE, "v81")]
    pairs = code_b_scalar_presence_pairs()
    assert len(pairs) == 6
    assert v81["presence_pairs"] == {**v80["presence_pairs"], **pairs}
    assert v81["value_domains"] == v80["value_domains"]
    for scalar, sale in pairs.items():
        assert scalar.startswith(sale + ".") and "code-b" in sale
        assert scalar not in v80["presence_pairs"]
    assert covered_flag_refusal_map(CORE, "v81") == COVERED_FLAG_REFUSAL_OBJECTS == covered_flag_refusal_map(CORE, "v80")


ELIGIBILITY_FLAGS = ("taxpayer_side_adjustment", "ordinary_indicated", "box_1f_market_discount", "qof_indicated",
                     "collectibles_or_special_rate")


def test_the_flag_parameter_maps_only_yes_and_no() -> None:
    body = _load(CONTENT / "parameter.f1099b-yes-no-flag.json")
    assert body["values"] == {"yes": "1", "no": "0"}
    for kind in ("covered", "covered-w"):
        for term in ("st", "lt"):
            rule = _load(CONTENT / f"rule.f1099b.{kind}-{term}-txn.admission.json")
            text = json.dumps(rule["value"])
            assert P + "parameter.f1099b-yes-no-flag" in text


def test_the_admission_rule_refuses_each_of_the_five_eligibility_flags() -> None:
    """Review S5: ADR-0052 Decision 1 lists all five flags in the eligible-sale predicate."""
    admission = _load(CONTENT / "f1099b-covered-admission.bundle.json")
    for fact in admission["fact_types"]:
        if fact["id"].endswith(".admission"):
            values = [v["const"] for v in fact["value_schema"]["oneOf"]]
            assert values == ["admitted", "taxpayer-side-adjustment", "recorded-twice", "flagged-outside-class"]
    for kind in ("covered", "covered-w"):
        for term in ("st", "lt"):
            rule = _load(CONTENT / f"rule.f1099b.{kind}-{term}-txn.admission.json")
            text = json.dumps(rule["value"])
            for flag in ELIGIBILITY_FLAGS:
                assert text.count(f'"field": "{flag}"') == 1, (kind, term, flag)
            # A flag decides before the cross-term check: refused whatever else is recorded.
            assert rule["value"]["then"]["value"] == "taxpayer-side-adjustment"
            assert rule["value"]["else"]["then"]["value"] == "flagged-outside-class"


def test_a_direct_sale_with_zero_proceeds_requires_schedule_d_and_reaches_line_7a() -> None:
    """Review B1: the line 1a and 8a sale counts, and line 7a v8's two new activity terms."""
    schedule_d = _load(CONTENT / "attachment.schedule-d.v9.json")["requirement"]["subtotals"]
    f8949 = _load(CONTENT / "attachment.f8949.v5.json")["requirement"]["subtotals"]
    for term in ("st", "lt"):
        count = P + f"f1099b.covered-{term}-count"
        assert count in schedule_d and count not in f8949, term
        rule = _load(CONTENT / f"rule.f1099b-covered-{term}-count.json")
        assert rule["publishes"] == count
        assert rule["value"] == {"op": "count", "name": P + f"f1099b.covered-{term}-txn",
                                 "source_set": P + f"f1099b.covered-{term}"}
    v7 = _load(CONTENT / "rule.form1040-line7a.v7.json")
    v8 = _load(CONTENT / "rule.form1040-line7a.v8.json")
    added = [arm for arm in v8["value"]["when"]["args"] if arm not in v7["value"]["when"]["args"]]
    assert added == [{"op": "compare", "cmp": "ne", "left": {"op": "ref", "name": P + f"schedule-d.line-{n}-gain"},
                      "right": 0} for n in ("1a", "8a")]
    assert v8["value"]["then"] == v7["value"]["then"] and v8["value"]["else"] == v7["value"]["else"]
    assert v8["requires"] == [*v7["requires"], P + "schedule-d.line-1a-gain", P + "schedule-d.line-8a-gain"]


@pytest.mark.parametrize("name, cross_terms", [
    ("rule.f1099b.covered-st-txn.admission.json", ["covered-lt"]),
    ("rule.f1099b.covered-lt-txn.admission.json", ["covered-st"]),
    ("rule.f1099b.covered-w-st-txn.admission.json", ["covered-lt", "covered-w-lt"]),
    ("rule.f1099b.covered-w-lt-txn.admission.json", ["covered-st", "covered-w-st"]),
    ("rule.f1099b.noncovered-st-txn.amounts-agree.v2.json", ["covered-lt", "covered-w-lt", "noncovered-lt"]),
    ("rule.f1099b.noncovered-lt-txn.amounts-agree.v2.json", ["covered-st", "covered-w-st", "noncovered-st"]),
])
def test_each_family_checks_the_other_terms_families_at_or_before_it(name: str, cross_terms: list[str]) -> None:
    """Every cross-term pair is checked, and no covered or code W check reads the noncovered closure."""
    text = json.dumps(_load(CONTENT / name)["value"])
    for other in ("covered-st", "covered-lt", "covered-w-st", "covered-w-lt", "noncovered-st", "noncovered-lt"):
        counted = f'"source_set": "{P}f1099b.{other}"' in text
        assert counted == (other in cross_terms), (name, other)


# ---- each new input question against its proposition ---------------------------


Q3 = P + "f1099b.code-b-sold.source-closure"
IC3 = P + "schedule-d-boundary.form8949-code-b-in-class"


def _question(slug: str) -> dict[str, Any]:
    body: dict[str, Any] = _load(CONTENT / f"input-question.{slug}.json")
    return body


def _fact(bundle: str, fact_id: str) -> dict[str, Any]:
    (fact,) = [f for f in _load(CONTENT / bundle)["fact_types"] if f["id"] == fact_id]
    found: dict[str, Any] = fact
    return found


def test_the_code_b_question_asks_exactly_the_closure_it_answers() -> None:
    """Q3's "no" closes the code B families empty; its "yes" admits recorded sales."""
    question = _question("f1099b-code-b-sold")
    fact = _fact("schedule-d-boundary-form8949-code-b-in-class.bundle.json", Q3)
    # "wrong" qualifies the basis, never the sale (review N3).
    text = ("Did any Form 1099-B or substitute statement you received show a cost or other basis, reported to the "
            "IRS, that is wrong?")
    assert question["question"] == fact["title"] == text
    assert question["fact_type"] == {"id": Q3, "version": fact["version"]}
    mapping = _load(CONTENT / "closure-mapping.f1099b-code-b.json")
    assert mapping["closure_question"] == text
    assert mapping["admission"] == {"no": "closed-empty", "yes": "until-later-member"}
    # The families it closes are exactly the code B sale families of boxes A and D, the
    # sales a Form 1099-B reported with a basis.
    assert sorted(row["family"]["id"].removeprefix(P) for row in mapping["families"]) == sorted(
        f"f1099b.code-b-{t}" + k for t in ("st", "lt") for k in ("", "-proceeds", "-basis", "-adjustment"))


def test_the_code_b_in_class_question_asks_exactly_the_proposition() -> None:
    """Each arm of the question carries the proposition's limit.

    The broker-reported arm allows a wash-sale loss or a correction of the
    reported basis, and nothing else. The filer-supplied arm is boxes B, C, E
    and F: securities, entered once, with the correct basis.
    """
    question = _question("schedule-d-boundary-form8949-code-b-in-class")
    fact = _fact("schedule-d-boundary-form8949-code-b-in-class.bundle.json", IC3)
    assert question["fact_type"] == {"id": IC3, "version": fact["version"]}
    title = fact["title"]
    assert "no adjustment other than a wash-sale loss or a correction of a wrong reported basis" in title
    assert "the correct basis even where a Form 1099-B showed another" in title
    text = question["question"]
    # A short list of the two kinds, then the question (review N2).
    intro, rest = text.split(" (1) ")
    covered, rest = rest.split(" (2) ")
    other, ask = rest.split(". Is ")
    assert intro == "Each sale on your Form 8949 should be one of two kinds."
    assert covered == ("A sale your broker reported to the IRS with its basis, with no adjustment other than a "
                       "wash-sale loss or a correction of that basis.")
    for phrase in ("A sale of stocks or other securities", "entered only once and in the one box its statement gives it",
                   "a basis you supply", "the correct basis, even if your Form 1099-B showed a different one",
                   "net proceeds you supply when you got no Form 1099-B",
                   "and no adjustment other than a wash-sale loss"):
        assert phrase in other, phrase
    assert ask == "every sale on your Form 8949 one of these two kinds?"


@pytest.mark.parametrize("term, word", [("st", "short-term"), ("lt", "long-term")])
def test_each_code_b_amount_question_asks_for_its_row(term: str, word: str) -> None:
    """The proceeds and basis rows are what the Form 1099-B shows; column (g) is the worksheet result."""
    bundle = f"f1099b-code-b-{term}.bundle.json"
    what = f"each {word} sale you recorded whose reported basis is wrong"
    expected = {
        "proceeds": (f"What are the proceeds shown on your Form 1099-B for {what}?", "proceeds shown on the Form 1099-B"),
        "basis": (f"What basis does your Form 1099-B show for {what}?", "basis shown on the Form 1099-B"),
        "adjustment": (f"What is the column (g) adjustment for {what}: the basis shown minus the correct basis, "
                       "plus any wash-sale loss disallowed?",
                       "the basis shown minus the correct basis, plus any wash-sale loss disallowed"),
    }
    for kind, (text, proposition) in expected.items():
        fact_id = P + f"f1099b.code-b-{term}-txn.{kind}"
        question = _question(f"f1099b-code-b-{term}-{kind}")
        fact = _fact(bundle, fact_id)
        assert question["question"] == text
        assert question["fact_type"] == {"id": fact_id, "version": fact["version"]}
        assert proposition in fact["title"], (kind, fact["title"])
        assert f"{word} code B sale" in fact["title"]
    sale = _fact(bundle, P + f"f1099b.code-b-{term}-txn")
    assert "basis is the basis the Form 1099-B shows (column (e))" in sale["title"]
    assert "corrected_basis is the correct basis you supply" in sale["title"]
    assert "corrected_basis" in sale["value_schema"]["required"]


FIELDS = (("schedule-d.line-1a.form-field.v3.json", "1a", "long-term"),
          ("schedule-d.line-8a.form-field.v2.json", "8a", "short-term"),
          ("schedule-d.line-1b.form-field.v3.json", "1b", "long-term"),
          ("schedule-d.line-8b.form-field.v3.json", "8b", "short-term"))


@pytest.mark.parametrize("name, line, other", FIELDS)
def test_the_line_fields_name_every_refusal_and_the_code_b_route(name: str, line: str, other: str) -> None:
    """Review S2, S4 and S5: the blocked sentence names the checks, each refusal and the route to code B."""
    explain = _load(CONTENT / name)["dispositions"]["blocked"]["explain"]
    assert explain.startswith(f"Schedule D line {line}, column (h), has no value yet. It is waiting for "), name
    assert "or for each sale recorded there to pass its checks" in explain, name
    assert explain.endswith(
        "A sale your answers place outside this return, a sale flagged as ordinary income, market discount, a "
        "qualified opportunity fund investment, or a collectibles or other special-rate gain, and a sale also "
        f"recorded as a {other} sale are outside what this return computes. So is a sale with an adjustment you "
        "make yourself, unless the adjustment corrects a wrong basis the Form 1099-B reported; record that sale as "
        "a sale whose reported basis is wrong."), name
    if line in ("1b", "8b"):
        assert ("(the column (g) of a sale whose reported basis is wrong must equal the basis shown minus the "
                "correct basis, plus any wash-sale loss disallowed)") in explain


def test_the_zero_sentences_hold_with_no_sales_and_line_8a_is_plain() -> None:
    """Review S1: a code B "yes" makes an empty term compute zero. S3: line 8a in line 1a's words."""
    for line, box, word in (("1b", "A", "short-term"), ("8b", "D", "long-term")):
        body = _load(CONTENT / f"schedule-d.line-{line}.form-field.v3.json")
        assert body["dispositions"]["computed_zero"]["explain"] == (
            f"Schedule D line {line}, column (h), is zero: no {word} Form 8949 box {box} sales with a wash-sale "
            "adjustment or a wrong reported basis are recorded, or their proceeds, basis, and adjustments net to zero.")
    line_1a = _load(CONTENT / "schedule-d.line-1a.form-field.v3.json")["dispositions"]
    line_8a = _load(CONTENT / "schedule-d.line-8a.form-field.v2.json")["dispositions"]
    for disposition in ("published_value", "computed_zero", "closure_backed_zero"):
        assert line_8a[disposition]["explain"] == line_1a[disposition]["explain"].replace(
            "short-term", "long-term").replace("1a", "8a"), disposition
        assert "derived finding" not in line_8a[disposition]["explain"]
