"""Full-surface replay of the recorded lists: core v106 against v107 (scratch or published).

Run: python3 replay.py <core-b> --variant all|one --part <part-file-outside-repo> [--workers N] [--out summary.json]
     python3 replay.py --census --out census.json

<core-b> is a scratch core.json written by build.py, or `v107` once published.
All recorded lists run in one shared run_full call whose process pool holds
the workers (shards are the pool's workers, not separate processes per list).
Uses tools/recorded_replay.py: every saved page field, attachment,
explanation-graph node and report row on both cores, strict, with every
difference no expectation names failing the list.

The projection orders a line's reasons by their sentence, so a new sentence
can move the other reasons of that line and the question links that point at
them by index. PlainWordsCompare therefore does not bless reasons by position.
On the v106 output it replaces each declared old sentence with its new
sentence (exact whole strings only, counted), re-sorts each reasons list the
projection had sorted, and remaps every reasonIndices under that line through
the same permutation. The transformed v106 output must then equal v107 on
every saved field except the declared version moves. Any other difference,
including a sentence no row declares, fails the list. The census reads every
recorded act list for any act that names an explanation or input-question
citizen (a saved record that would pin one).
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import time
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from tools import recorded_replay as rr  # noqa: E402

P = "tax.us.2025."
ALL_KINDS = ("page", "model", "graph", "row", "report", "attachment")


def _rows(variant: str) -> list[dict]:
    build = json.loads((HERE / f"build-{variant}.json").read_text(encoding="utf-8"))
    changed = {s["id"] for s in build["successors"]}
    return [r for r in json.loads((HERE / "wording.json").read_text(encoding="utf-8"))["replacements"]
            if r["id"] in changed]


def version_expectations(variant: str) -> list[rr.Expectation]:
    build = json.loads((HERE / f"build-{variant}.json").read_text(encoding="utf-8"))
    out = [rr.version_change(s["id"], s["old_version"], s["new_version"]) for s in build["successors"]]
    out.append(rr.version_change(P + "package.core-calculations", "v106", "v107"))
    return out


def _substitute(node, table: dict, found: Counter):
    if isinstance(node, str):
        if node in table:
            found[node] += 1
            return table[node]
        return node
    if isinstance(node, list):
        return [_substitute(item, table, found) for item in node]
    if isinstance(node, dict):
        return {key: _substitute(value, table, found) for key, value in node.items()}
    return node


def _strings(node, out: set) -> None:
    if isinstance(node, str):
        out.add(node)
    elif isinstance(node, list):
        for item in node:
            _strings(item, out)
    elif isinstance(node, dict):
        for value in node.values():
            _strings(value, out)


def _remap(node, mapping: dict) -> None:
    if isinstance(node, dict):
        for key, value in node.items():
            if key == "reasonIndices" and isinstance(value, list):
                node[key] = sorted(mapping[index] for index in value)
            else:
                _remap(value, mapping)
    elif isinstance(node, list):
        for item in node:
            _remap(item, mapping)


def _resort(node, moved: Counter) -> None:
    if isinstance(node, dict):
        reasons = node.get("reasons")
        if (isinstance(reasons, list) and reasons and all(isinstance(r, dict) and isinstance(r.get("sentence"), str)
                                                          for r in reasons)):
            sentences = [r["sentence"] for r in reasons]
            if node.get("_sorted_before"):
                order = sorted(range(len(reasons)), key=lambda i: sentences[i])
                mapping = {old: new for new, old in enumerate(order)}
                if any(old != new for old, new in mapping.items()):
                    moved["lines_with_reordered_reasons"] += 1
                node["reasons"] = [reasons[i] for i in order]
                for key, value in node.items():
                    if key != "reasons":
                        _remap(value, mapping)
            node.pop("_sorted_before", None)
        for key, value in node.items():
            if key != "reasons":
                _resort(value, moved)
    elif isinstance(node, list):
        for item in node:
            _resort(item, moved)


def _mark_sorted(node) -> None:
    if isinstance(node, dict):
        reasons = node.get("reasons")
        if (isinstance(reasons, list) and reasons and all(isinstance(r, dict) and isinstance(r.get("sentence"), str)
                                                          for r in reasons)):
            sentences = [r["sentence"] for r in reasons]
            if sentences == sorted(sentences):
                node["_sorted_before"] = True
        for key, value in list(node.items()):
            _mark_sorted(value)
    elif isinstance(node, list):
        for item in node:
            _mark_sorted(item)


def plain_words(saved: dict, table: dict) -> tuple[dict, Counter]:
    """The v106 saved output with the declared sentences replaced and reasons re-sorted as the projection does."""
    found: Counter = Counter()
    model = json.loads(json.dumps(saved["model"]))
    _mark_sorted(model)
    model = _substitute(model, table, found)
    _resort(model, found)
    report = _substitute(saved["report"], table, found)
    return {**saved, "model": model, "report": report}, found


class PlainWordsCompare:
    """Picklable per-list function: v106 with the declared words applied against v107, strict."""

    def __init__(self, variant: str, max_unexpected: int = 40) -> None:
        self.choices: dict[str, list[str]] = {}
        for r in _rows(variant):
            if r["new"] not in self.choices.setdefault(r["old"], []):
                self.choices[r["old"]].append(r["new"])
        self.table = {old: news[0] for old, news in self.choices.items()}
        self.expectations = version_expectations(variant)
        self.max_unexpected = max_unexpected

    def __call__(self, key: str, acts: list, cores: tuple) -> dict:
        import hashlib
        core_a, core_b = cores
        run_id = "demo.fsr." + hashlib.sha256(key.encode()).hexdigest()[:20]
        saved_a = rr.saved_output(core_a, acts, run_id)
        saved_b = rr.saved_output(core_b, acts, run_id)
        raw_a = rr.snapshot(saved_a["model"], saved_a["report"]) if saved_a["outcome"] == "success" else \
            rr.failure_snapshot(saved_a["outcome"], saved_a["error"], saved_a["message"])
        found: Counter = Counter()
        table = self.table
        ambiguous = 0
        if saved_b["outcome"] == "success" and any(len(v) > 1 for v in self.choices.values()):
            # One old sentence served families that now read differently (a sale with or
            # without a Form 1099-B); take the one new sentence v107 shows, else leave it.
            shown: set = set()
            _strings(saved_b["model"], shown)
            table = {}
            for old, news in self.choices.items():
                present = [n for n in news if n in shown]
                if len(news) == 1:
                    table[old] = news[0]
                elif len(present) == 1:
                    table[old] = present[0]
                elif present:
                    ambiguous += 1
        if saved_a["outcome"] == "success":
            applied, found = plain_words(saved_a, table)
            snap_a = rr.snapshot(applied["model"], applied["report"])
        else:
            snap_a = raw_a
        snap_b = rr.snapshot(saved_b["model"], saved_b["report"]) if saved_b["outcome"] == "success" else \
            rr.failure_snapshot(saved_b["outcome"], saved_b["error"], saved_b["message"])
        verdict = rr.classify_full(snap_a, snap_b, self.expectations)
        unexpected = verdict.pop("unexpected")
        raw = rr.diff_snapshots(raw_a, snap_b)
        verdict["raw_differences"] = len(raw)
        verdict["raw_by_kind_attribute"] = dict(Counter(f"{d['kind']}|{re.sub(r'[0-9]+', 'N', d['attribute'])}"
                                                        for d in raw))
        verdict["sentences_replaced"] = {table[old]: count for old, count in found.items() if old in table}
        verdict["ambiguous_sentences"] = ambiguous
        verdict["lines_with_reordered_reasons"] = found.get("lines_with_reordered_reasons", 0)
        verdict["unexpected_total"] = len(unexpected)
        verdict["unexpected"] = unexpected[: self.max_unexpected]
        verdict["outcomes"] = [snap_a["outcome"], snap_b["outcome"]]
        verdict["sha256"] = [rr.snapshot_sha256(raw_a), rr.snapshot_sha256(snap_b)]
        return verdict


def census() -> dict:
    lists = rr.recorded_lists()
    named: Counter = Counter()
    kinds: Counter = Counter()
    for _key, acts in lists:
        for act in acts:
            kinds[str(act.get("kind"))] += 1
        text = json.dumps(acts)
        for match in re.findall(r"tax\.us\.2025\.(?:input-question|family-block-explanation)\.[\w.-]+", text):
            named[match] += 1
    return {"lists": len(lists), "act_kinds": dict(sorted(kinds.items())),
            "acts_naming_an_explanation_or_input_question": dict(sorted(named.items()))}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("core", nargs="?")
    parser.add_argument("--variant", choices=("all", "one"), default="all")
    parser.add_argument("--part")
    parser.add_argument("--workers", type=int, default=None)
    parser.add_argument("--census", action="store_true")
    parser.add_argument("--keys", default="")
    parser.add_argument("--out")
    args = parser.parse_args()
    if args.census:
        body = census()
        Path(args.out).write_text(json.dumps(body, indent=1) + "\n", encoding="utf-8")
        print(json.dumps(body, indent=1))
        return
    lists = rr.recorded_lists()
    if args.keys:
        wanted = set(args.keys.split(","))
        lists = [item for item in lists if item[0] in wanted]
    started = time.monotonic()
    cores = (rr.resolve_core("v106"), rr.resolve_core(args.core))
    compare = PlainWordsCompare(args.variant)
    results = rr.replay(lists, cores, compare, workers=args.workers, part=args.part)
    summary = summarize(results, compare, cores)
    summary["variant"] = args.variant
    if args.out:
        text = json.dumps(summary, indent=1) + "\n"
        rr._check_no_local_paths(text, "summary")
        Path(args.out).write_text(text, encoding="utf-8")
    print(json.dumps({"wall_time_s": round(time.monotonic() - started, 1),
                      **{k: summary[k] for k in ("lists", "classes", "passing", "failing", "unexpected_differences",
                                                 "expectations_used", "outcomes", "sentence_changes",
                                                 "lines_with_reordered_reasons", "raw_by_kind_attribute")},
                      "unexpected": {k: v["lists"] for k, v in summary["unexpected_by_kind_attribute"].items()}},
                     indent=1))


def summarize(results: dict, compare: PlainWordsCompare, cores: tuple) -> dict:
    specs = compare.expectations
    used = {i for row in results.values() for i in row.get("used", [])}
    by_attribute: dict = {}
    for key, row in results.items():
        for item in row["unexpected"]:
            slot = by_attribute.setdefault(f"{item['kind']}|{item['change']}|{re.sub(r'[0-9]+', 'N', item['attribute'])}",
                                           {"lists": set(), "samples": []})
            slot["lists"].add(key)
            if len(slot["samples"]) < 3:
                slot["samples"].append({"list": key, **item})
    sentence_lists: Counter = Counter()
    sentence_hits: Counter = Counter()
    for row in results.values():
        for sentence, count in row["sentences_replaced"].items():
            sentence_lists[sentence] += 1
            sentence_hits[sentence] += count
    declared = sorted({n for news in compare.choices.values() for n in news})
    return {
        "format": "full-surface-replay.v1", "comparison": "plain-words",
        "cores": [rr.core_fingerprint(core) for core in cores], "lists": len(results),
        "classes": dict(sorted(Counter(row["class"] for row in results.values()).items())),
        "passing": sum(1 for row in results.values() if row["class"] != "unexpected"),
        "failing": sum(1 for row in results.values() if row["class"] == "unexpected"),
        "unexpected_differences": sum(row["unexpected_total"] for row in results.values()),
        "unexpected_by_kind_attribute": {k: {"lists": len(v["lists"]), "samples": v["samples"]}
                                         for k, v in sorted(by_attribute.items())},
        "expectations_declared": len(specs), "expectations_used": len(used),
        "unused_expectations": [rr.describe_expectation(s) for i, s in enumerate(specs) if i not in used],
        "expected_by_note": dict(sorted(sum((Counter(r["expected_by_note"]) for r in results.values()),
                                            Counter()).items())),
        "sentences_declared": len(declared),
        "sentence_changes": {"lists": sum(1 for r in results.values() if r["sentences_replaced"]),
                             "replacements": sum(sentence_hits.values()),
                             "sentences_reached": len(sentence_lists)},
        "sentences_reached": {s: {"lists": sentence_lists[s], "replacements": sentence_hits[s]} for s in declared
                              if s in sentence_lists},
        "sentences_not_reached": [s for s in declared if s not in sentence_lists],
        "ambiguous_sentences": sum(r["ambiguous_sentences"] for r in results.values()),
        "lines_with_reordered_reasons": sum(r["lines_with_reordered_reasons"] for r in results.values()),
        "raw_by_kind_attribute": dict(sorted(sum((Counter(r["raw_by_kind_attribute"]) for r in results.values()),
                                                 Counter()).items())),
        "outcomes": dict(sorted(Counter("/".join(r["outcomes"]) for r in results.values()).items())),
        "list_classes": {k: r["class"] for k, r in sorted(results.items())},
        "failing_lists": {k: r["unexpected_total"] for k, r in sorted(results.items()) if r["class"] == "unexpected"},
    }


if __name__ == "__main__":
    main()
