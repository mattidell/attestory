"""Trace Decision 2 content using the real page's initial/detail/trace DOM.

Run: python3 p0b_scan.py <baseline-census-directory>
All full per-list observations and models stay outside the repository.
"""
from __future__ import annotations
from collections import Counter, defaultdict
import importlib.util
import json
from pathlib import Path
import re
import sys

HERE = Path(__file__).resolve().parent
def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec); sys.modules[name] = mod; spec.loader.exec_module(mod)
    return mod

base = load("plt_p0b_scan_base", HERE / "summarize.py")
census = base.census
PROSE = {"explain", "render", "label", "title", "description", "notes", "question", "sentence", "heading", "tieOutText"}


def main():
    scratch = Path(sys.argv[1])
    observations = json.loads((scratch / "dom-observations.json").read_text())
    results = json.loads((scratch / "census-part.json").read_text())["results"]
    index, _ = base.source_index()
    text_sources = defaultdict(list)
    for text, sources in index.items():
        for source in sources:
            prop = source["property"]
            if prop.rsplit(".", 1)[-1] not in PROSE and not prop.startswith("basis."): continue
            if len(text) < 4: continue
            text_sources[text].append({**source, "old": text, "shown": text})
            if prop == "title" and ":" in text:
                prefix = text.split(":", 1)[0].strip()
                if len(prefix) >= 4: text_sources[prefix].append({**source, "old": text, "shown": prefix})
    pattern = re.compile("|".join(re.escape(s) for s in sorted(text_sources, key=lambda s: (-len(s), s))))
    traced = {}
    alerts = Counter()
    for i, entry in enumerate(observations["cases"], 1):
        case = json.loads((scratch / entry["observation"]).read_text())
        key = case["id"]
        model = json.loads((scratch / results[key]["model"]).read_text())
        fields = {s["id"]: s["field"] for s in model["sections"]}
        alerts.update(case["alerts"])
        # Match content as part of a longer rendered node too: detail panels
        # prefix member notes/title with a citizen identity and version.
        for surface in ("initial", "details", "trace"):
            seen = set()
            for node in case[surface]:
                if node["role"] in {"citation-button", "badge"}: continue
                for match in pattern.finditer(node["text"]):
                    for source in text_sources[match.group()]:
                        field = fields.get(node["section"])
                        if node["role"] == "explain" and (not field or source["id"] != field["id"]): continue
                        identity = (source["file"], source["property"])
                        if identity in seen: continue
                        seen.add(identity)
                        row = traced.setdefault(identity, {**source, "terms": census.matches(source["shown"]),
                            "initial_lists": set(), "details_lists": set(), "trace_lists": set(), "page_fields": set()})
                        row[surface + "_lists"].add(key)
                        if field: row["page_fields"].add(field["id"])
                        else:
                            attachments = [a["id"] for a in model["attachments"] if source["shown"] == a["title"]]
                            row["page_fields"].update(attachments or ["content-detail-panel"])
        if i % 100 == 0: print(f"[{i}/{len(observations['cases'])}] traced", flush=True)
    rows = []
    for row in traced.values():
        row = dict(row)
        visible = row["initial_lists"] | row["details_lists"]
        row["lists"] = sorted(visible)
        row["recorded_lists"] = sum(not k.startswith("demo.plt.") for k in visible)
        row["synthetic_lists"] = sum(k.startswith("demo.plt.") for k in visible)
        row["trace_only"] = not visible and bool(row["trace_lists"])
        row = {k: sorted(v) if isinstance(v, set) else v for k, v in row.items()}
        rows.append(row)
    rows.sort(key=lambda r: (r["file"], r["property"]))
    flagged = [r for r in rows if r["terms"] and r["lists"]]
    summary = {"source": "published v95", "recorded_lists": 775,
        "recorded_outcomes": dict(Counter(r["outcome"] for k, r in results.items() if not k.startswith("demo.plt."))),
        "synthetic_lists": 9, "drawn_pages": len(observations["cases"]),
        "content_properties": len([r for r in rows if r["lists"]]),
        "content_citizens": len({r["id"] for r in rows if r["lists"]}),
        "flagged_properties": len(flagged), "flagged_distinct_drawn_texts": len({r["shown"] for r in flagged}),
        "flagged_citizens": len({r["id"] for r in flagged}),
        "flagged_detail_only_properties": sum(not r["initial_lists"] for r in flagged),
        "trace_only_properties": sum(r["trace_only"] for r in rows),
        "terms": census.TERMS + ["identifier", "version string"],
        "render_alerts": dict(alerts), "non_loopback_requests": sum(e["non_loopback_request"] for e in observations["cases"]),
        "parked_page_text": {"counted_once": "Seven template groups from P0 page-trace.json; no page design or edits.", "template_groups": 7},
        "limits": "84 recorded lists error before a saved page; these have no visible-text census. Source matching records adopted prose properties actually found in DOM, including concatenated detail text; raw graph identity metadata is parked."}
    census.write(scratch / "content-trace-full.json", {"properties": rows})
    def compact(row):
        public = {k: v for k, v in row.items() if k not in ("initial_lists", "details_lists", "trace_lists", "lists")}
        public.update({k + "_count": len(row[k]) for k in ("initial_lists", "details_lists", "trace_lists", "lists")})
        public["example_lists"] = row["lists"][:3]
        return public
    census.write(HERE / "p0b-census.json", summary)
    census.write(HERE / "p0b-content-trace.json", {"properties": [compact(r) for r in rows]})
    census.write(HERE / "p0b-flagged.json", {"properties": [compact(r) for r in flagged]})
    print(json.dumps(summary, indent=2))


if __name__ == "__main__": main()
