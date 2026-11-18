"""Check every replacement in actual successor initial/detail DOM text.

Run: python3 p0c_drawn_check.py <successor-results-directory>
Page-owned trace/citation captions remain parked. Each property's case
coverage must match the independently measured P0b census exactly.
"""
from __future__ import annotations
import json
from pathlib import Path
import sys

HERE=Path(__file__).resolve().parent

def main():
    scratch=Path(sys.argv[1])
    manifest=json.loads((HERE/"p0c-wording.json").read_text())["replacements"]
    observations=json.loads((scratch/"dom-observations.json").read_text())
    found=[set() for _ in manifest]; old=[set() for _ in manifest]
    alerts=[]; blocked=[]
    for entry in observations["cases"]:
        case=json.loads((scratch/entry["observation"]).read_text())
        alerts.extend(case["alerts"])
        if case["non_loopback_request"]: blocked.append(case["id"])
        text=[n["text"] for n in case["initial"]+case["details"]
              if n["role"] not in ("support-trace","citation-button","badge")]
        for i,row in enumerate(manifest):
            if any(row["new_shown"] in s for s in text): found[i].add(case["id"])
            if any(row["shown"] in s for s in text): old[i].add(case["id"])
    checks=[{"id":r["id"],"property":r["property"],"expected_lists":r["lists_count"],
             "new_text_lists":len(found[i]),"old_text_lists":len(old[i])}
            for i,r in enumerate(manifest)]
    failures=[c for c in checks if c["new_text_lists"]!=c["expected_lists"] or c["old_text_lists"]]
    output={"status":"pass" if not failures and not alerts and not blocked else "fail",
            "pages":len(observations["cases"]),"browser":observations["browser_version"],
            "replacement_properties":len(checks),"all_new_texts_drawn":all(found),
            "retained_old_text_properties":sum(bool(x) for x in old),
            "render_alerts":alerts,"non_loopback_requests":len(blocked),"checks":checks,"failures":failures}
    (HERE/"p0c-drawn-check.json").write_text(json.dumps(output,indent=2)+"\n")
    print(json.dumps({k:v for k,v in output.items() if k!="checks"},indent=2))
    assert output["status"]=="pass",failures


if __name__=="__main__": main()
