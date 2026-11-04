"""P0 probe, part 3: the two facts probe_flip.py cannot flip with yes/no (Form 1098 scope boolean, filing status).

Same method as probe_flip.py on core v72: run the base return as built and with the one fact's value changed.
For filing status every other value is tried. Writes ``probe-extra-output.json``. Run from the repository root.
"""
from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(HERE))
import probe_flip as pf  # noqa: E402


def main():
    from tests import test_statement_withholding_answer as swa
    from tests.helpers import current_core_returns as c
    swa.CORES["v72"] = ("package.core-calculations.v72.json", "v72", "demo.release.sli-worksheet-integration.2025.v70.json",
                        "v70", "published-packages.v70.json")
    acts = c.base_return()

    def with_value(ft, value):
        out = copy.deepcopy(acts)
        for a in out:
            f = a["payload"].get("finding")
            if f and str(f["fact_id"]).split("|")[0] == pf.P + ft:
                f["value"] = value
        return out

    def current(ft):
        return [a["payload"]["finding"]["value"] for a in acts
                if a["payload"].get("finding") and str(a["payload"]["finding"]["fact_id"]).split("|")[0] == pf.P + ft][0]

    results = []
    for ft, values in (("f1098-scope.no-mortgage-statement", [False]),
                       ("filing-status", ["single", "married_filing_jointly", "married_filing_separately",
                                          "head_of_household", "qualifying_surviving_spouse"])):
        built = current(ft)
        base = pf.lines(swa.run(copy.deepcopy(acts), f"demo.p0.sa.extra.{ft}.as-built", "v72"))
        for v in values:
            if v == built:
                continue
            try:
                flip = pf.lines(swa.run(with_value(ft, v), f"demo.p0.sa.extra.{ft}.{v}", "v72"))
                diff = {k: {"as_built": base[k], "changed": flip[k]} for k in base
                        if (base[k]["disposition"], base[k]["value"]) != (flip[k]["disposition"], flip[k]["value"])}
                results.append({"root": ft, "as_built_value": built, "new_value": v, "status": "ran", "changed": diff})
            except Exception as exc:
                results.append({"root": ft, "as_built_value": built, "new_value": v, "status": "error",
                                "error": f"{type(exc).__name__}: {exc}"[:500]})
            print(ft, v, results[-1]["status"], len(results[-1].get("changed", {})), flush=True)
    (HERE / "probe-extra-output.json").write_text(json.dumps({"core": "v72", "cases": results}, indent=1) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
