"""Full-surface replay: published v101 against the scratch v102.

Run: python3 replay.py <scratch-core.json> --shard I/N --part <part-file-outside-repo>
     python3 replay.py <scratch-core.json> --summarize <part-files...> --out replay.json
     python3 replay.py <scratch-core.json> --discover N --part <part-file-outside-repo>

Uses tools/recorded_replay.py. A derived finding's alias drops its input digest
when its symbol has one finding on each core, because a new pin re-keys
downstream findings. A list that differs only by inserted rows of the two new
rules is compared as equal. The report row order may also reorder, provided
the set of rows other than the new rules is unchanged. The age and main-home
disposition children gain exactly qualifying-child-present and status-class;
those two lists are declared with their before and after. A published section
root is an index into the explanation roots. Walking the new
qualifying-child-present finding inserts one root, so every later published
section index is one higher. Those indexes are set back only when every
changed index moved by one and the new finding exists only on the successor.
Any other list or index change still fails the list.
"""
from __future__ import annotations

import argparse
import hashlib
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
NEW = (
    "eic-qualifying-child-present",
    "eic.qualifying-child-present",
    "eic-child.qualifies",
    "eic.child.qualifies",
)
READERS = (
    "status-class|early-stop|questions-required|answer\\.(?:separated-spouse|not-married|"
    "age-25-under-65|main-home-in-us)"
)
INSERTION_ATTRS = re.compile(
    r"(?:.*@order|dispositionNodes\.tax\.us\.2025\.eic\.(?:" + READERS + r"|qualifying-child-present|child\.qualifies)"
    r"(?:\.[^.]*)?\.children|missing|pins)"
)


def _design():
    return rr._module("ens_p0_replay_design", HERE / "design.py")


def expectations() -> list[rr.Expectation]:
    d = _design()
    present_row = r"^dispositions\[tax\.us\.2025\.rule\.eic-qualifying-child-present(?:\||\])"
    qualifies_row = r"^dispositions\[tax\.us\.2025\.rule\.eic-child\.qualifies(?:\||\])"
    present_node = r"^dispositionNodes\.tax\.us\.2025\.eic\.qualifying-child-present\."
    qualifies_node = r"^dispositionNodes\.tax\.us\.2025\.eic\.child\.qualifies\."
    present_pin = (
        r"eic-(?:" + READERS + r")[^/]*\]/pins\[finding~(?:row~tax\.us\.2025\.rule\.eic-qualifying-child-present"
        r"|tax\.us\.2025\.eic\.qualifying-child-present~)"
    )
    class_pin = (
        r"eic-answer\.(?:age-25-under-65|main-home-in-us)[^/]*\]/pins\[finding~"
        r"(?:row~tax\.us\.2025\.rule\.eic-status-class|tax\.us\.2025\.eic\.status-class~)"
    )
    return [
        rr.version_change(d.CLASS_RULE, "v2", "v3", "status class reads whether a qualifying child is present"),
        rr.version_change(d.EARLY_RULE, "v2", "v3", "early stop requires that no qualifying child is present"),
        rr.version_change(d.QUESTIONS_RULE, "v2", "v3", "questions required when a qualifying child is present"),
        rr.version_change(d.SEP_RULE, "v1", "v2", "separated spouse is asked when a qualifying child has no valid SSN"),
        rr.version_change(d.NOT_MARRIED_RULE, "v1", "v2", "step 4 question 1 is skipped when a qualifying child is present"),
        rr.version_change(d.AGE_RULE, "v3", "v4", "age question skips married filers who have a qualifying child"),
        rr.version_change(d.HOME_RULE, "v3", "v4", "main-home question skips married filers who have a qualifying child"),
        rr.version_change(P + "package.core-calculations", "v101", "v102"),
        rr.Expectation(("row",), r".*", present_row, "added", note="report row of qualifying-child-present"),
        rr.Expectation(("row",), r".*", qualifies_row, "added", note="report row of child.qualifies"),
        rr.Expectation(("model",), r".*", present_node, "added", note="disposition node of qualifying-child-present"),
        rr.Expectation(("model",), r".*", qualifies_node, "added", note="disposition node of child.qualifies"),
        rr.Expectation(("model",), r"dispositionNodes\.tax\.us\.2025\.eic\.qualifying-child-present\..*", r"^$", "added",
                       note="disposition node fields of qualifying-child-present"),
        rr.Expectation(("model",), r"dispositionNodes\.tax\.us\.2025\.eic\.child\.qualifies\..*", r"^$", "added",
                       note="disposition node fields of child.qualifies"),
        rr.Expectation(("row", "model"), r"id|origin|role|version", present_pin, "added",
                       note="succeeded rules pin qualifying-child-present"),
        rr.Expectation(("row", "model"), r"id|origin|role|version", class_pin, "added",
                       note="age and main home pin status class"),
        rr.Expectation(("graph",), r".*", r"eic\.qualifying-child-present|eic-qualifying-child-present", "added",
                       note="explanation graph of qualifying-child-present"),
        rr.Expectation(("graph",), r".*", r"eic\.child\.qualifies|eic-child\.qualifies", "added",
                       note="explanation graph of child.qualifies"),
        rr.Expectation(
            ("model",),
            r"dispositionNodes\.tax\.us\.2025\.eic\.answer\.age-25-under-65\.children",
            "", "changed",
            [P + "eic.answer.not-married", P + "eic.column-count", P + "eic.questions-required"],
            [P + "eic.answer.not-married", P + "eic.column-count", P + "eic.qualifying-child-present",
             P + "eic.questions-required", P + "eic.status-class"],
            note="age question reads qualifying-child-present and status class",
        ),
        rr.Expectation(
            ("model",),
            r"dispositionNodes\.tax\.us\.2025\.eic\.answer\.main-home-in-us\.children",
            "", "changed",
            [P + "eic.answer.not-married", P + "eic.column-count", P + "eic.questions-required"],
            [P + "eic.answer.not-married", P + "eic.column-count", P + "eic.qualifying-child-present",
             P + "eic.questions-required", P + "eic.status-class"],
            note="main-home question reads qualifying-child-present and status class",
        ),
    ]


def _is_new(item: object) -> bool:
    return isinstance(item, str) and any(token in item for token in NEW)


def _strip_new(value):
    return [item for item in value if not _is_new(item)]


def normalize_insertions(left: dict, right: dict) -> Counter:
    """Treat an inserted new-rule item, and a pure reorder of the report rows, as no difference."""
    before = {(k, i, t): v for k, i, t, v in left["records"]}
    counted: Counter = Counter()
    for record in right["records"]:
        kind, ident, attribute, value = record
        prior = before.get((kind, ident, attribute))
        if not (isinstance(value, list) and isinstance(prior, list) and value != prior):
            continue
        if not (INSERTION_ATTRS.fullmatch(attribute) or attribute == "dispositions@order"):
            continue
        stripped = _strip_new(value)
        if stripped == prior and len(value) > len(prior):
            record[3] = prior
            counted[f"inserted:{re.sub(r'[0-9]+', 'N', attribute)}"] += 1
        elif attribute == "dispositions@order" and sorted(stripped) == sorted(prior):
            record[3] = prior
            counted["reordered:dispositions@order"] += 1
    return counted


ALIAS = re.compile(r"finding~([A-Za-z0-9_.:|-]+?)~([0-9a-f]{10})(#\d+)?")


def _aliases(snap: dict) -> dict:
    found: dict = {}

    def walk(node):
        if isinstance(node, str):
            for symbol, digest, extra in ALIAS.findall(node):
                found.setdefault(symbol, set()).add(digest + extra)
        elif isinstance(node, list):
            for item in node:
                walk(item)
        elif isinstance(node, dict):
            for key, value in node.items():
                walk(key)
                walk(value)

    walk(snap["records"])
    return found


ROOT_ATTR = re.compile(r"sectionRoots\..+\.root")


def _present_marks(records) -> set:
    found = set()
    for kind, ident, attribute, value in records:
        blob = f"{ident} {attribute}"
        if "qualifying-child-present" in blob or (isinstance(value, str) and "qualifying-child-present" in value):
            found.add((kind, ident, attribute))
    return found


def normalize_section_roots(left: dict, right: dict) -> Counter:
    """Set published section-root indexes back when each one moved by exactly one.

    The index is the position of that section's own root. One new published
    finding inserted earlier shifts every later index by one. A shift of any
    other size, or a shift on a list that did not gain the new finding, stays
    a difference.
    """
    before = {(k, i, t): v for k, i, t, v in left["records"]}
    changed = []
    for record in right["records"]:
        kind, ident, attribute, value = record
        if kind != "model" or ROOT_ATTR.fullmatch(attribute) is None:
            continue
        prior = before.get((kind, ident, attribute))
        if isinstance(value, int) and isinstance(prior, int) and value != prior:
            changed.append((record, prior, value - prior))
    if not changed or any(delta != 1 for _, _, delta in changed):
        return Counter()
    if not (_present_marks(right["records"]) - _present_marks(left["records"])):
        return Counter()
    for record, prior, _delta in changed:
        record[3] = prior
    return Counter({"shifted:sectionRoots.root": len(changed)})


def normalize_aliases(left: dict, right: dict) -> Counter:
    """Drop the input-structure digest when a symbol has one finding on each core."""
    left_alias, right_alias = _aliases(left), _aliases(right)
    single = {
        symbol for symbol in set(left_alias) & set(right_alias)
        if len(left_alias[symbol]) == 1 and len(right_alias[symbol]) == 1
        and "#" not in next(iter(left_alias[symbol])) + next(iter(right_alias[symbol]))
    }
    moved = Counter(f"realiased:{symbol}" for symbol in single if left_alias[symbol] != right_alias[symbol])

    def fix(node):
        if isinstance(node, str):
            return ALIAS.sub(lambda match: f"finding~{match.group(1)}~*" if match.group(1) in single else match.group(0), node)
        if isinstance(node, list):
            return [fix(item) for item in node]
        if isinstance(node, dict):
            return {fix(key): fix(value) for key, value in node.items()}
        return node

    for snap in (left, right):
        snap["records"] = [fix(record) for record in snap["records"]]
    return moved if any(moved) else Counter()


class Compare(rr.FullSurfaceCompare):
    def __call__(self, key, acts, cores):
        core_a, core_b = cores
        run_id = "demo.fsr." + hashlib.sha256(key.encode()).hexdigest()[:20]
        snap_a = rr.snapshot_run(core_a, acts, run_id)
        snap_b = rr.snapshot_run(core_b, acts, run_id)
        sha = [rr.snapshot_sha256(snap_a), rr.snapshot_sha256(snap_b)]
        inserted = (
            normalize_aliases(snap_a, snap_b)
            + normalize_insertions(snap_a, snap_b)
            + normalize_section_roots(snap_a, snap_b)
        )
        verdict = rr.classify_full(snap_a, snap_b, self.expectations)
        if inserted and verdict["class"] == "identical":
            verdict["class"] = "expected_changes"
        verdict["expected_by_note"] = {**verdict["expected_by_note"], **inserted}
        unexpected = verdict.pop("unexpected")
        verdict["unexpected_total"] = len(unexpected)
        verdict["unexpected"] = unexpected[: self.max_unexpected]
        verdict["outcomes"] = [snap_a["outcome"], snap_b["outcome"]]
        verdict["sha256"] = sha
        return verdict


def _summary(results: dict, specs: list, cores: list) -> dict:
    classes = Counter(row["class"] for row in results.values())
    used = {i for row in results.values() for i in row.get("used", [])}
    used_by: dict = {}
    for key, row in results.items():
        for i in row.get("used", []):
            used_by.setdefault(i, []).append(key)
    by_attribute: dict = {}
    for key, row in results.items():
        for item in row["unexpected"]:
            slot = by_attribute.setdefault(
                f"{item['kind']}|{item['change']}|{re.sub(r'[0-9]+', 'N', item['attribute'])}",
                {"lists": set(), "samples": []},
            )
            slot["lists"].add(key)
            if len(slot["samples"]) < 2:
                slot["samples"].append({
                    "list": key,
                    "identity": item.get("identity", "")[:240],
                    "attribute": item.get("attribute", "")[:180],
                    "before": item.get("before") if not isinstance(item.get("before"), (list, dict)) else "…",
                    "after": item.get("after") if not isinstance(item.get("after"), (list, dict)) else "…",
                })
    return {
        "format": "full-surface-replay.v1",
        "cores": cores,
        "lists": len(results),
        "classes": dict(sorted(classes.items())),
        "passing": sum(1 for row in results.values() if row["class"] != "unexpected"),
        "failing": sum(1 for row in results.values() if row["class"] == "unexpected"),
        "unexpected_differences": sum(row["unexpected_total"] for row in results.values()),
        "unexpected_by_kind_attribute": {
            key: {"lists": len(slot["lists"]), "samples": slot["samples"]} for key, slot in sorted(by_attribute.items())
        },
        "expectations_declared": len(specs),
        "expectations_used": len(used),
        "unused_expectations": [rr.describe_expectation(spec) for i, spec in enumerate(specs) if i not in used],
        "expectation_lists": {
            rr.describe_expectation(spec)["note"]: (
                len(used_by.get(i, [])) if len(used_by.get(i, [])) > 12 else sorted(used_by.get(i, []))
            )
            for i, spec in enumerate(specs)
        },
        "expected_by_note": dict(sorted(sum((Counter(row["expected_by_note"]) for row in results.values()), Counter()).items())),
        "outcomes": dict(sorted(Counter("/".join(row["outcomes"]) for row in results.values()).items())),
        "list_classes": {key: row["class"] for key, row in sorted(results.items())},
        "failing_lists": {key: row["unexpected_total"] for key, row in sorted(results.items()) if row["class"] == "unexpected"},
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("core", nargs="?")
    parser.add_argument("--shard", default="0/1")
    parser.add_argument("--part")
    parser.add_argument("--workers", type=int, default=None)
    parser.add_argument("--summarize", nargs="*")
    parser.add_argument("--discover", type=int, default=0)
    parser.add_argument("--keys", default="")
    parser.add_argument("--out")
    args = parser.parse_args()
    specs = [] if args.discover else expectations()
    cores = [rr.core_fingerprint("v101"), rr.core_fingerprint(args.core)]
    if args.summarize:
        results: dict = {}
        for part in args.summarize:
            results.update(json.loads(Path(part).read_text(encoding="utf-8"))["results"])
        summary = _summary(results, expectations(), cores)
        text = json.dumps(summary, indent=1) + "\n"
        rr._check_no_local_paths(text, "summary")
        Path(args.out).write_text(text, encoding="utf-8")
        print(json.dumps({k: summary[k] for k in (
            "lists", "classes", "passing", "failing", "unexpected_differences",
            "expectations_declared", "expectations_used", "outcomes",
        )}, indent=1))
        return
    index, total = (int(part) for part in args.shard.split("/"))
    lists = rr.recorded_lists()
    if args.discover:
        lists = lists[: args.discover]
        specs = []
    if args.keys:
        wanted = set(args.keys.split(","))
        lists = [item for item in lists if item[0] in wanted]
    lists = lists[index::total]
    started = time.monotonic()
    compare = Compare(specs, max_unexpected=4000 if args.discover else 20)
    results = rr.replay(lists, (rr.resolve_core("v101"), rr.resolve_core(args.core)), compare,
                        workers=args.workers, part=args.part)
    summary = _summary(results, specs, cores)
    print(json.dumps({
        "shard": args.shard,
        "wall_time_s": round(time.monotonic() - started, 1),
        **{k: summary[k] for k in ("lists", "classes", "passing", "failing", "unexpected_differences", "outcomes")},
        "unexpected": {k: v["lists"] for k, v in summary["unexpected_by_kind_attribute"].items()},
    }, indent=1))


if __name__ == "__main__":
    main()
