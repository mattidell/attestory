"""Reproduce the blocked-names-question cases on published core v87."""

from __future__ import annotations

import copy
import json
from typing import Any, Callable

import common

h = common.harness()
P = common.P
Acts = common.Acts


def answered(acts: Acts, **overrides: str | None) -> Acts:
    values: dict[str, str | None] = {
        "q1": "no", "q2": "no", "q3": "no", "form8949": "yes", "path_b": None,
        "ic79": None, "ic80": None, "ic81": None,
        "lines_18_19": "yes", "no_other_sd": "yes", "no_da_qof": "yes",
        "exc1_only_2a": "yes", "exc1_no_losses": "yes",
    }
    values.update(overrides)
    acts = h.answer(acts, common.v87().content, **values)
    return h.say(acts, P + "f1099b.no-sale-box4-present", "no", "no-sale-box4", common.v87().content)


def statement_answers(acts: Acts) -> Acts:
    statements = [str(a["payload"]["entity"]["id"]) for a in acts
                  if a.get("kind") == "entity-introduced"
                  and a["payload"]["entity"].get("kind") == "tax.us.f1099b-statement"]
    statements = list(dict.fromkeys(statements))
    if not statements:
        return acts
    bundle = json.loads((common.v87().content / "f1099b-statement-boxes.bundle.json").read_text(encoding="utf-8"))
    if not {f["id"] for f in bundle["fact_types"]} & h._adopted(acts):
        h._add(acts, "bundle-adoption", {"bundle": bundle})
    for statement in statements:
        for slug in ("statement-box4-withholding-reported", "statement-box7-loss-not-allowed"):
            fact = P + "f1099b." + slug
            fact_id = h.fact_id_for(fact, (("statement", statement), ("tax-year", h.YEAR)))
            h._add(acts, "assertion", {"finding": h._attested(
                f"demo.bnq.{slug}.{statement}", fact_id, "no")})
    return h.renumber(acts)


def empty(**answers: str | None) -> Acts:
    return answered(h.opened(), **answers)


def sale(kind: str, *, rows: dict[str, float | None] | None = None,
         form8949: str = "no", path_b: str | None = "no") -> Acts:
    acts = h.opened()
    if kind == "codeb":
        acts = h.sale(acts, kind, "st", tag="bnq-codeb", proceeds=10000, basis=7000,
                      corrected=4000, rows=rows)
        return statement_answers(answered(acts, q3="yes", form8949=form8949, path_b=path_b, ic81="yes",
                                          exc1_only_2a="no"))
    acts = h.sale(acts, kind, "st", tag="bnq-sale", proceeds=2000, basis=8000,
                  wash=1000 if kind == "w" else 0, rows=rows)
    result = answered(acts, q2="yes" if kind == "no1099b" else "no",
                      form8949=form8949, path_b=path_b,
                      ic80="yes" if kind == "no1099b" else None,
                      exc1_only_2a="no", exc1_no_losses="no")
    return statement_answers(result) if kind == "w" else result


def wash_adjustment_open() -> Acts:
    acts = sale("w", form8949="no", path_b="yes")
    return h.strip(acts, P + "f1099b.covered-w-st-adjustment.source-closure")


def personal_loss_8949() -> Acts:
    return empty(form8949="no", path_b="no", exc1_only_2a="no", exc1_no_losses="no")


def closure_open(fact: str) -> Acts:
    return h.strip(empty(), P + fact)


CASES: dict[str, tuple[str, Callable[[], Acts], str]] = {
    "sd_yes_nothing": ("schedule-d-refused", lambda: empty(q1="yes"),
        "Truthful yes that a box B/E sale exists, before that sale is recorded."),
    "sd_8949_no_unadmitted": ("schedule-d-refused", lambda: empty(form8949="no", path_b="no"),
        "Truthful Form 8949 no for work outside every admitted recorded family."),
    "sd_sale_beside_8949_yes": ("schedule-d-refused", lambda: sale("no1099b", form8949="yes", path_b=None),
        "A box C sale added after the earlier no-Form-8949 answer."),
    "sd_amounts_disagree": ("schedule-d-refused", lambda: sale("no1099b", rows={"basis": 2000}),
        "The sale object says basis 8000 while its scalar row says 2000."),
    "sd_path_b_unanswered": ("schedule-d-refused", lambda: sale("no1099b", path_b=None),
        "A complete box C sale with the ADR-0061 Path B answer withheld."),
    "codeb_yes_nothing": ("code-b-refused", lambda: empty(q3="yes"),
        "Truthful yes that a code B sale exists, before that sale is recorded."),
    "codeb_sale_beside_8949_yes": ("code-b-refused", lambda: sale("codeb", form8949="yes", path_b=None),
        "A code B sale added after the earlier no-Form-8949 answer."),
    "codeb_amounts_disagree": ("code-b-refused", lambda: sale("codeb", rows={"adjustment": 2000}),
        "The code B worksheet calls for 3000 while its adjustment row says 2000."),
    "exception1_personal_loss_8949": ("exception1-no", personal_loss_8949,
        "A personal-item loss reported on Form 8949, with no representable sale record."),
    "wash_adjustment_open": ("wash-admission", wash_adjustment_open,
        "A recorded wash sale with only its adjustment family closure removed."),
    "internal_f1099int_b8": ("internal-subtotal", lambda: closure_open("f1099int.b8.source-closure"),
        "Only the Form 1099-INT box 8 family is open."),
    "internal_nominee": ("internal-subtotal", lambda: closure_open("scheduleb.adjustment.nominee.source-closure"),
        "Only the Schedule B nominee-adjustment family is open."),
    "internal_odc_child": ("internal-subtotal", lambda: closure_open("odc.child-roster.source-closure"),
        "Only the other-dependent child roster is open."),
    "internal_odc_relative": ("internal-subtotal", lambda: closure_open("odc.relative-roster.source-closure"),
        "Only the other-dependent relative roster is open."),
}


def public(result: dict[str, Any]) -> dict[str, Any]:
    result = copy.deepcopy(result)
    result.pop("_publications", None)
    blocked = result.pop("blocked", {})
    grouped: dict[str, dict[str, Any]] = {}
    roots: dict[str, dict[str, Any]] = {}
    for field, detail in blocked.items():
        compact = {key: detail[key] for key in ("artifact", "code", "missing", "reasons", "questions")}
        key = json.dumps(compact, sort_keys=True)
        grouped.setdefault(key, {"fields": [], **compact})["fields"].append(field)
        for root in detail.get("roots", []):
            roots[json.dumps(root, sort_keys=True)] = root
    result["blocked"] = sorted(grouped.values(), key=lambda row: row["fields"])
    result["root_blocks"] = sorted(roots.values(), key=lambda row: (row["artifact"], str(row["code"])))
    result["source_set_blocks"] = [
        row for row in result.get("all_blocked", []) if row.get("code") == "SOURCE_SET_UNCLOSED"
    ]
    result.pop("all_blocked", None)
    return result


def main() -> None:
    core = common.core_from_env()
    cases = {}
    for case_id, (group, build, note) in CASES.items():
        result = public(common.run(core, build(), "demo.bnq." + case_id))
        cases[case_id] = {"group": group, "note": note, **result}
    common.write("probe-output.json", {
        "core": {"package": core.version, "registry": core.registry, "release": core.release_version},
        "case_count": len(cases),
        "cases": cases,
    })
    print(json.dumps({"core": core.version, "cases": len(cases)}, indent=2))


if __name__ == "__main__":
    main()
