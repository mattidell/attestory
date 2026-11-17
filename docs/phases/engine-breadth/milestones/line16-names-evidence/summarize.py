"""Summarize saved live probes without replaying unchanged runs."""
import importlib.util
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("l16_summary_probe", HERE / "probe.py")
probe = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = probe
spec.loader.exec_module(probe)


def main():
    a, b = [probe.read_cases(HERE / file) for file in ("baseline.json", "candidate.json")]
    reproduction, changes = {}, {}
    for key in a:
        old, new = probe.expand(a[key]), probe.expand(b[key])
        old16, new16 = old["fields"]["form1040.line-16"], new["fields"]["form1040.line-16"]
        reproduction[key] = {"v94": {"line16_missing": old16["row"]["missing"],
                                      "line16_sentences": len(old16["reasons"]),
                                      "other_blocked_field_sentence_counts": {name: len(field["reasons"]) for name, field in old["fields"].items() if field["disposition"] == "blocked"}},
                             "scratch": {"line16_missing": new16["row"]["missing"], "line16_sentences": len(new16["reasons"])}}
        if a[key] == b[key]: continue
        changed_fields = [name for name in set(old["fields"]) | set(new["fields"])
                          if old["fields"].get(name) != new["fields"].get(name)]
        assert set(changed_fields) == probe.WATCH, (key, changed_fields)
        for name in changed_fields:
            x, y = old["fields"][name], new["fields"][name]
            assert x["value"] == y["value"] and x["disposition"] == y["disposition"]
        ar, br = [{r["artifact"]: r for r in v["rows"]} for v in (old, new)]
        assert ar.keys() == br.keys()
        for name in ar:
            assert ar[name]["code"] == br[name]["code"] and ar[name]["disposition"] == br[name]["disposition"]
            if name != "form1040-line16": assert ar[name] == br[name]
        changes[key] = sorted(changed_fields)
    protected = "exception1-no/exception1_personal_loss_8949"
    one_at_a_time = {key: {"line16_changes_on_v94": probe.expand(a[key])["fields"]["form1040.line-16"] != probe.expand(a[protected])["fields"]["form1040.line-16"]}
                       for key in a if key.startswith("protected/") and not key.startswith("protected/cumulative/")}
    assert not any(v["line16_changes_on_v94"] for v in one_at_a_time.values())
    probe.write("summary.json", {"cases": len(a), "changed_cases": len(changes), "changes": changes,
        "all_ten_cases_identical": all(a[key] == b[key] for key in a if key.startswith(("schedule-d-refused/", "code-b-refused/", "exception1-no/", "wash-admission/"))),
        "protected_case_identical": a[protected] == b[protected],
        "computing_neighbours": {key: probe.expand(a[key])["fields"]["form1040.line-16"]["value"]
                                  for key in a if key.startswith("status/") and key.endswith("exception-yes") or key == "neighbour/recorded-sale"},
        "one_at_a_time": one_at_a_time, "reproduction": reproduction})
    print(json.dumps({"cases": len(a), "changed": len(changes), "protected_same": a[protected] == b[protected]}))


if __name__ == "__main__":
    main()
