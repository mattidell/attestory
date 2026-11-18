"""Trace the partial saved-page census after the charter's page-change stop.

Run: python3 summarize.py <census-scratch-directory>
No new live runs. DOM observations are from the actual unmodified page.
"""
from __future__ import annotations

from collections import Counter, defaultdict
from functools import lru_cache
import importlib.util
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("plt_summary_census", HERE / "census.py")
census = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = census
spec.loader.exec_module(census)
REPO = census.REPO
CONTENT = REPO / "packages/content/tax/2025"
PAGE = "packages/presentation/pages/citation-walk.v1.html"


def strings(node, path=""):
    if isinstance(node, dict):
        for key, value in node.items(): yield from strings(value, path + "." + key)
    elif isinstance(node, list):
        for index, value in enumerate(node): yield from strings(value, path + f"[{index}]")
    elif isinstance(node, str):
        yield path.lstrip("."), node


@lru_cache(maxsize=None)
def source_lines(path):
    return path.read_text().splitlines()


def source_line(path, value):
    lines = source_lines(path)
    for ensure in (False, True):
        literal = json.dumps(value, ensure_ascii=ensure)
        for index, line in enumerate(lines, 1):
            if literal in line: return index
    raise AssertionError((path.name, value))


def source_index():
    package = json.loads((CONTENT / "package.core-calculations.v95.json").read_text())
    adopted = {(m["id"], m["version"]) for m in package["members"]}
    index = defaultdict(list)
    sources = []
    for path in sorted(CONTENT.glob("*.json")):
        body = json.loads(path.read_text())
        if (body.get("id"), body.get("version")) not in adopted: continue
        for prop, text in strings(body):
            source = {"file": path.relative_to(REPO).as_posix(), "line": source_line(path, text),
                      "id": body["id"], "version": body["version"], "property": prop}
            index[text].append(source)
            if census.matches(text): sources.append((text, source))
    return index, sources


def main():
    scratch = Path(sys.argv[1])
    observed = json.loads((scratch / "dom-observations.json").read_text())
    results = json.loads((scratch / "census-part.json").read_text())["results"]
    index, content_strings = source_index()
    content = {}
    page_templates = {}
    all_visible, flagged, flagged_fields, flagged_lists = set(), set(), set(), set()
    roles = defaultdict(set)
    parked = set()
    model_inventory = Counter()
    visible_content = set()
    for case in observed["cases"]:
        key = case["id"]
        model = json.loads((scratch / results[key]["model"]).read_text())
        fields = {s["id"]: s["field"] for s in model["sections"]}
        for prop, text in strings(model):
            if census.matches(text): model_inventory[prop.split(".", 1)[0].split("[", 1)[0]] += 1
        for node in case["initial"] + case["trace"]:
            text, role = node["text"], node["role"]
            all_visible.add(text)
            terms = census.matches(text)
            if not terms: continue
            if role == "citation-button":
                parked.add(text)
                continue
            field = fields.get(node["section"], {})
            field_id = field.get("id", node["section"] or "page")
            if not field:
                attachments = [a for a in model["attachments"] if a["title"] == text]
                if len(attachments) == 1: field_id = attachments[0]["id"]
            if field: flagged_fields.add(field_id)
            flagged.add(text); flagged_lists.add(key)
            roles[role].add(text)
            sources = index.get(text, [])
            if not sources and role == "other":
                # _resolve_attachment copies only title.split(':', 1)[0].
                sources = [s for original, entries in index.items() if original.split(":", 1)[0].strip() == text
                           for s in entries if s["property"] == "title"]
            if role == "explain":
                sources = [s for s in sources if s["id"] == field.get("id") and s["version"] == field.get("version")]
            if sources:
                row = content.setdefault(text, {"text": text, "terms": terms, "sources": {}, "page_fields": set(), "lists": set()})
                row["page_fields"].add(field_id); row["lists"].add(key)
                for source in sources:
                    identity = (source["file"], source["property"])
                    visible_content.add(identity)
                    item = row["sources"].setdefault(identity, {**source, "page_fields": set(), "lists": set()})
                    item["page_fields"].add(field_id); item["lists"].add(key)
            else:
                if role == "support-trace":
                    if text.startswith("Show "): template, line = "Show <pin role> <pin ID> / Show dependency <symbol>", 937
                    elif text.startswith("— "): template, line = "— <producer rule ID>", 935
                    elif text.startswith(("input:", "output:")): template, line = "<role>: <symbol or finding ID>", 934
                    else: template, line = "<symbol>: <recorded disposition>", 955
                elif role == "badge": template, line = "<disposition with underscores replaced by spaces>", 996
                elif "No value published" in text: template, line = text, 1053
                elif "Missing dependency" in text: template, line = text, 1056
                elif "contribute the missing dependency" in text: template, line = text, 1074
                else:
                    template = text
                    candidates = [i for i, s in enumerate((REPO / PAGE).read_text().splitlines(), 1) if text in s]
                    line = candidates[0] if candidates else None
                row = page_templates.setdefault(template, {"template": template, "file": PAGE, "line": line,
                    "version": "citation-walk.v1.html", "role": role, "texts": set(), "page_fields": set(), "lists": set()})
                row["texts"].add(text); row["page_fields"].add(field_id); row["lists"].add(key)
    def finish(row):
        return {key: (sorted(value) if isinstance(value, set) else value) for key, value in row.items()}
    traced = []
    for row in content.values():
        row = dict(row)
        row["sources"] = [finish(s) for s in row["sources"].values()]
        traced.append(finish(row))
    templates = []
    for row in page_templates.values():
        row = dict(row)
        row["distinct_texts"] = len(row["texts"])
        row["examples"] = sorted(row.pop("texts"))[:3]
        templates.append(finish(row))
    # These fields are not drawn by the ordinary renderLine path. This is not
    # a global proof of invisibility in other explanation/citation surfaces.
    unseen = [{"terms": census.matches(text), **source} for text, source in content_strings
              if source["property"] in ("description", "notes")
              and (source["file"], source["property"]) not in visible_content]
    summary = {"status": "stopped", "coverage": "partial synthetic saved-page census; not the 775-list population",
        "live_cases": len(results), "saved_pages": len(observed["cases"]), "recorded_lists_measured": 0,
        "terms": census.TERMS + ["identifier (tax.us.* or demo.*)", "version string (vN or @N)"],
        "flagged_distinct_texts_excluding_parked_citation_buttons": len(flagged),
        "content_sentences": len(traced), "content_citizens": len({s["id"] for r in traced for s in r["sources"]}),
        "flagged_page_fields": len(flagged_fields), "flagged_lists": len(flagged_lists),
        "flagged_texts_by_role": {k: len(v) for k, v in roles.items()},
        "parked_citation_button_texts": len(parked), "visible_distinct_texts": len(all_visible),
        "model_flagged_string_occurrences_by_top_level_property": dict(model_inventory),
        "page_template_groups": len(templates), "browser": observed["browser_version"],
        "render_alerts": sum(len(c["alerts"]) for c in observed["cases"]),
        "non_loopback_requests": sum(c["non_loopback_request"] for c in observed["cases"]),
        "limits": ["Only initial DOM and opened top-level support traces were observed; deeper dependency buttons and other collapsed details were not expanded.",
                   "Model inventory includes metadata and hidden instructions; it is not a visibility count.",
                   "No population census, scratch successor, comparative replay or mutation controls were run after the page-change stop."]}
    census.write(HERE / "census.json", summary)
    census.write(HERE / "content-trace.json", {"sentences": sorted(traced, key=lambda r: r["text"])})
    census.write(HERE / "page-trace.json", {"groups": templates})
    census.write(HERE / "undrawn-descriptions.json", {"limit": "Not seen in six sampled pages; renderLine does not read these properties. Other detail surfaces are not proven invisible.", "count": len(unseen), "entries": unseen})
    print(json.dumps(summary, indent=2))


if __name__ == "__main__": main()
