"""Compare the broad alternative and an unanswered distinguishing boundary.

Run: python3 boundary.py <narrow-core.json> <broad-core.json>
"""
import importlib.util
import json
import multiprocessing
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("l16_boundary_probe", HERE / "probe.py")
probe = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = probe
spec.loader.exec_module(probe)


def run(args):
    variant, core, cases = args
    return variant, {k: probe.compact(v) for k, v in probe.worker((core, cases))}


def main():
    narrow, broad = sys.argv[1:]
    cases = dict(probe.lists())
    common = probe.load(probe.BNQ / "common.py", "common")
    h = common.harness()
    opened = [("open/" + status, h.strip(cases["status/" + status + "/required"],
                 probe.P + "schedule-d-boundary.no-form8949-sources"))
              for status in ("single", "married_filing_jointly", "married_filing_separately")]
    protected = "exception1-no/exception1_personal_loss_8949"
    probe.evidence_loader.finish_all()
    with multiprocessing.get_context("spawn").Pool(3) as pool:
        found = dict(pool.map(run, [("v94", None, opened), ("narrow", narrow, opened),
                                  ("broad", broad, [(protected, cases[protected])])]))
    baseline = probe.read_cases(HERE / "baseline.json")
    candidate = probe.read_cases(HERE / "candidate.json")
    assert baseline[protected] == candidate[protected]
    found["protected"] = {"v94": baseline[protected], "narrow": candidate[protected],
                          "broad": found.pop("broad")[protected]}
    probe.write("boundary.json", found)
    print(json.dumps({"protected_narrow_unchanged": True,
                      "protected_broad_changed": found["protected"]["broad"] != baseline[protected],
                      "open_boundary": {k: {variant: probe.expand(found[variant][k])["fields"]["form1040.line-16"]["row"]
                                            for variant in ("v94", "narrow")}
                                        for k, _ in opened}}, indent=2))


if __name__ == "__main__":
    main()
