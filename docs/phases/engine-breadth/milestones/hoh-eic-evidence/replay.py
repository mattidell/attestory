"""Full-surface replay: published v98 against the scratch v99 (the earned income credit asks a head of household with no qualifying child whether they were married).

Run: python3 replay.py <scratch-core.json> --shard I/N --part <part-file-outside-repo>
     python3 replay.py <scratch-core.json> --summarize <part-files...> --out replay-m.json
     python3 replay.py <scratch-core.json> --probe --shard I/N --part <part-file-outside-repo>
     python3 replay.py <scratch-core.json> --probe --summarize <part-files...> --out replay-probe-m.json
     python3 replay.py <scratch-core.json> --paired --out replay-paired.json
     python3 replay.py --census --out census.json

Uses tools/recorded_replay.py (snapshots, diff, strict classify with the
expectations below): every saved page field, attachment, explanation-graph
node and report row on both cores, every difference no expectation names
failing the list. One check is added on top, because an ``@order`` or list
record cannot be declared by an expectation without blessing any reorder:
a list record that differs only by the insertion of the new answer (the
report's row order, the gate-result rule's ``children`` and ``missing``
lists) is counted as ``inserted:<attribute>`` and compared as equal, and the
report's row order may also move the status-class row (it now reads the
counted children, so it is evaluated later) when every other row keeps its
order; any other change to such a list still fails the list. Before that,
a derived finding's alias drops its input-structure digest when its symbol
has one finding on each core (``normalize_aliases``): the gate result's new
input edge would otherwise re-key every finding downstream of it, while the
edges themselves stay compared record by record.
``--probe`` replays the probe.py lists instead (each head of household case
unanswered, answered yes and answered no; the controls once). ``--paired``
compares, for each head of household probe case, the list a v98 filer has
(no answer) on v98 against the same list answered yes and answered no on the
scratch core, and lists every difference outside identity-only records.
The census reads every recorded act list for its filing status and any
child, other dependent or relative it records.
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
NEW = ("eic-answer.not-married", "eic.answer.not-married")
DEPENDENT_PREFIXES = ("eic.child.", "ctc.child.", "odc.child.", "odc.dependent.", "dtb.child.")
INSERTION_ATTRS = re.compile(r"(?:.*@order|dispositionNodes\.tax\.us\.2025\.eic\.gate-result\.children|missing)")
INSERTION_IDENTITY = re.compile(r"^$|eic-gate-result|eic\.gate-result|^dispositionNodes\.tax\.us\.2025\.eic\.gate-result")


def _design():
    return rr._module("hoh_eic_p0_design", HERE / "design.py")


def expectations() -> list[rr.Expectation]:
    d = _design()
    new_row = r"^dispositions\[tax\.us\.2025\.rule\.eic-answer\.not-married(?:\||\])"
    new_node = r"^dispositionNodes\.tax\.us\.2025\.eic\.answer\.not-married\."
    gate_pin = (r"eic-gate-result[^/]*\]/pins\[finding~(?:row~tax\.us\.2025\.rule\.eic-answer\.not-married"
                r"|tax\.us\.2025\.eic\.answer\.not-married~)")
    return [
        rr.version_change(d.CLASS_RULE, "v1", "v2", "status class reads the counted children on head of household"),
        rr.version_change(d.GATE_RULE, "v2", "v3", "gate result reads the new answer"),
        rr.version_change(P + "package.core-calculations", "v98", "v99"),
        rr.Expectation(("row",), r".*", new_row, "added", note="report row of the new answer rule"),
        rr.Expectation(("model",), r".*", new_node, "added", note="disposition node record of the new answer"),
        rr.Expectation(("model",), r"dispositionNodes\.tax\.us\.2025\.eic\.answer\.not-married\..*", r"^$", "added",
                       note="disposition node of the new answer"),
        rr.Expectation(("row", "model"), r"id|origin|role|version", gate_pin, "added",
                       note="gate result pins the new answer"),
        rr.Expectation(("graph",), r".*", r"eic\.answer\.not-married|eic-answer\.not-married", "added",
                       note="explanation graph node and edge of the new answer"),
        # Only on a head of household return that leaves the answer unanswered (the probe lists).
        rr.Expectation(("page", "model"), r"sentence", r"", "added", rr.ANY, d.QUESTION,
                       note="question shown:eic.not-married"),
        # Only on a head of household return: the status class reads the counted children there.
        rr.Expectation(("graph", "row", "model"), r"id|origin|role|version|target",
                       r"eic[.-]status-class[^/]*(?:\]|~\*)/(?:pins\[|edges\[derived:)finding~tax\.us\.2025\.eic\.column-count~",
                       "added", note="status class pins the counted children (head of household)"),
    ]


def _strip_new(value):
    return [x for x in value if not (isinstance(x, str) and any(n in x for n in NEW))]


MOVED = "tax.us.2025.rule.eic-status-class|"


def _unmoved(value):
    return [x for x in value if not (isinstance(x, str) and x.startswith(MOVED))]


def normalize_insertions(left: dict, right: dict) -> Counter:
    """Set each list record of ``right`` that differs from ``left`` only by inserted new-answer items to
    ``left``'s value, and count it; leave every other record untouched."""
    a = {(k, i, t): v for k, i, t, v in left["records"]}
    counted: Counter = Counter()
    for record in right["records"]:
        kind, ident, attribute, value = record
        before = a.get((kind, ident, attribute))
        if not (isinstance(value, list) and isinstance(before, list) and value != before
                and INSERTION_ATTRS.fullmatch(attribute) and INSERTION_IDENTITY.search(ident or "")):
            continue
        if _strip_new(value) == before and len(value) > len(before):
            record[3] = before
            counted[f"inserted:{re.sub(r'[0-9]+', 'N', attribute)}"] += 1
        elif (attribute == "dispositions@order" and sorted(_strip_new(value)) == sorted(before)
              and _unmoved(_strip_new(value)) == _unmoved(before)):
            # The status class rule now reads the counted children, so its report row is evaluated later;
            # every other row keeps its order.
            record[3] = before
            counted["inserted:dispositions@order, status class row moved"] += 1
    return counted


ALIAS = re.compile(r"finding~([A-Za-z0-9_.:-]+?)~([0-9a-f]{10})(#\d+)?")


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


def normalize_aliases(left: dict, right: dict) -> Counter:
    """Drop the input-structure digest from a derived finding's alias when its symbol has exactly one finding on
    each core. ``rr.snapshot`` aliases a derived finding by its symbol and the digest of its inputs' structure, so
    one new input edge (the gate result's) re-keys every finding downstream of it; the edges themselves are still
    compared record by record, so a changed input still shows as a changed or added edge. Counts each symbol whose
    digest differed."""
    a, b = _aliases(left), _aliases(right)
    single = {symbol for symbol in set(a) & set(b) if len(a[symbol]) == 1 and len(b[symbol]) == 1
              and "#" not in next(iter(a[symbol])) + next(iter(b[symbol]))}
    moved = Counter(f"realiased:{symbol}" for symbol in single if a[symbol] != b[symbol])

    def fix(node):
        if isinstance(node, str):
            return ALIAS.sub(lambda m: f"finding~{m.group(1)}~*" if m.group(1) in single else m.group(0), node)
        if isinstance(node, list):
            return [fix(item) for item in node]
        if isinstance(node, dict):
            return {fix(key): fix(value) for key, value in node.items()}
        return node

    for snap in (left, right):
        snap["records"] = [fix(record) for record in snap["records"]]
    return moved if any(moved) else Counter()


class Compare(rr.FullSurfaceCompare):
    """rr.FullSurfaceCompare with the insertion check applied before the strict classification."""

    def __call__(self, key, acts, cores):
        core_a, core_b = cores
        run_id = "demo.fsr." + hashlib.sha256(key.encode()).hexdigest()[:20]
        snap_a = rr.snapshot_run(core_a, acts, run_id)
        snap_b = rr.snapshot_run(core_b, acts, run_id)
        sha = [rr.snapshot_sha256(snap_a), rr.snapshot_sha256(snap_b)]
        inserted = normalize_aliases(snap_a, snap_b) + normalize_insertions(snap_a, snap_b)
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


def census() -> dict:
    lists = rr.recorded_lists()
    status: Counter = Counter()
    dependents: Counter = Counter()
    for key, acts in lists:
        found = None
        kinds: set[str] = set()
        for act in acts:
            payload = act.get("payload") or {}
            finding = payload.get("finding") or (payload.get("member") or {}).get("finding") or {}
            fid = str(finding.get("fact_id", ""))
            if fid.startswith(P + "filing-status|"):
                found = finding.get("value")
            for prefix in DEPENDENT_PREFIXES:
                if fid.startswith(P + prefix):
                    kinds.add(prefix.rstrip("."))
        status[str(found)] += 1
        dependents[f"{found}: " + (", ".join(sorted(kinds)) or "none")] += 1
    return {"lists": len(lists), "filing_status": dict(status.most_common()),
            "status_and_recorded_dependents": dict(dependents.most_common())}


def _probe():
    return rr._module("hoh_eic_p0_probe", HERE / "probe.py")


def probe_lists(core_content: Path) -> list:
    probe = _probe()
    out = []
    for key in probe.KEYS:
        answers = ("none", "yes", "no") if key.startswith("hoh/") else ("none",)
        for answer in answers:
            out.append((f"probe/{key}/{answer}", probe.build(key, core_content, answer)))
    return out


IDENTITY_ONLY = re.compile(r"pins|edges|citationSites|pinId|finding~|act~|records\[|@order|\.children$|findingRoot$|"
                           r"sectionRoots\.|\|(?:finding_id|act_id)$")


def paired(core_spec: str) -> dict:
    core = rr.resolve_core(core_spec)
    probe = _probe()
    out: dict = {"format": "hoh-eic-paired.v1", "cores": [rr.core_fingerprint("v98"), rr.core_fingerprint(core)],
                 "compared": "v98 on the list with no answer, against the scratch core on the same list unanswered, answered yes and answered no",
                 "substantive_filter": "differences outside kind graph whose identity and attribute name no pin, edge, "
                                       "citation site, list order, disposition-node children or finding root, graph section root index, "
                                       "generated finding or act id, "
                                       "or record of the new answer rule",
                 "cases": {}}
    for key in probe.KEYS:
        if not key.startswith("hoh/"):
            continue
        run_id = "demo.fsr.hoheic." + key.replace("/", ".")
        before = rr.snapshot_run("v98", probe.build(key, core.content, "none"), run_id)
        for answer in ("none", "yes", "no"):
            after = rr.snapshot_run(core, probe.build(key, core.content, answer), run_id)
            diffs = rr.diff_snapshots(before, after)
            substantive = [d for d in diffs if d["kind"] != "graph"
                           and not IDENTITY_ONLY.search(d["identity"] + "|" + d["attribute"])
                           and not any(n in d["identity"] + d["attribute"] for n in NEW)
                           and not d["attribute"].endswith("version")]
            out["cases"][f"{key}/{answer}"] = {
                "outcomes": [before["outcome"], after["outcome"]],
                "differences": len(diffs),
                "by_kind_change": dict(sorted(Counter(f"{d['kind']}|{d['change']}" for d in diffs).items())),
                "substantive": len(substantive),
                "substantive_values": sorted({f"{d['kind']}|{d['identity'] or '-'}|{d['attribute']}: {d['before']} -> {d['after']}"[:400]
                                              for d in substantive}),
            }
    return out


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
            slot = by_attribute.setdefault(f"{item['kind']}|{item['change']}|{re.sub(r'[0-9]+', 'N', item['attribute'])}",
                                           {"lists": set(), "samples": []})
            slot["lists"].add(key)
            if len(slot["samples"]) < 3:
                slot["samples"].append({"list": key, **item})
    return {
        "format": "full-surface-replay.v1", "cores": cores, "lists": len(results),
        "classes": dict(sorted(classes.items())),
        "passing": sum(1 for r in results.values() if r["class"] != "unexpected"),
        "failing": sum(1 for r in results.values() if r["class"] == "unexpected"),
        "unexpected_differences": sum(r["unexpected_total"] for r in results.values()),
        "unexpected_by_kind_attribute": {k: {"lists": len(v["lists"]), "samples": v["samples"]} for k, v in sorted(by_attribute.items())},
        "expectations_declared": len(specs), "expectations_used": len(used),
        "unused_expectations": [rr.describe_expectation(s) for i, s in enumerate(specs) if i not in used],
        "expectation_lists": {rr.describe_expectation(s)["note"]: (len(used_by.get(i, [])) if len(used_by.get(i, [])) > 12
                                                                     else sorted(used_by.get(i, [])))
                              for i, s in enumerate(specs)},
        "expected_by_note": dict(sorted(sum((Counter(r["expected_by_note"]) for r in results.values()), Counter()).items())),
        "outcomes": dict(sorted(Counter("/".join(r["outcomes"]) for r in results.values()).items())),
        "list_classes": {k: r["class"] for k, r in sorted(results.items())},
        "failing_lists": {k: r["unexpected_total"] for k, r in sorted(results.items()) if r["class"] == "unexpected"},
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("core", nargs="?")
    parser.add_argument("--shard", default="0/1")
    parser.add_argument("--part")
    parser.add_argument("--workers", type=int, default=None)
    parser.add_argument("--summarize", nargs="*")
    parser.add_argument("--census", action="store_true")
    parser.add_argument("--keys", default="")
    parser.add_argument("--probe", action="store_true", help="the probe.py lists instead of the recorded lists")
    parser.add_argument("--paired", action="store_true")
    parser.add_argument("--out")
    args = parser.parse_args()
    if args.paired:
        body = paired(args.core)
        text = json.dumps(body, indent=1) + "\n"
        rr._check_no_local_paths(text, "paired")
        Path(args.out).write_text(text, encoding="utf-8")
        print(json.dumps({k: {x: v[x] for x in ("outcomes", "differences", "substantive")} for k, v in body["cases"].items()}, indent=1))
        return
    if args.census:
        body = census()
        Path(args.out).write_text(json.dumps(body, indent=1) + "\n", encoding="utf-8")
        print(json.dumps(body, indent=1)[:3000])
        return
    specs = expectations()
    cores = [rr.core_fingerprint("v98"), rr.core_fingerprint(args.core)]
    if args.summarize:
        results: dict = {}
        for part in args.summarize:
            results.update(json.loads(Path(part).read_text(encoding="utf-8"))["results"])
        summary = _summary(results, specs, cores)
        summary["lists_set"] = "probe" if args.probe else "recorded"
        text = json.dumps(summary, indent=1) + "\n"
        rr._check_no_local_paths(text, "summary")
        Path(args.out).write_text(text, encoding="utf-8")
        print(json.dumps({k: summary[k] for k in ("lists", "classes", "passing", "failing", "unexpected_differences",
                                                   "expectations_declared", "expectations_used", "expected_by_note",
                                                   "outcomes")}, indent=1))
        return
    index, total = (int(x) for x in args.shard.split("/"))
    if args.probe:
        lists = probe_lists(rr.resolve_core(args.core).content)  # the scratch content holds the new bundle
        from tests import evidence_loader  # as rr.recorded_lists does, release the loader before spawning workers

        owner = evidence_loader.current_owner()
        if owner:
            evidence_loader.release(owner)
    else:
        lists = rr.recorded_lists()
    if args.keys:
        wanted = set(args.keys.split(","))
        lists = [item for item in lists if item[0] in wanted]
    lists = lists[index::total]
    started = time.monotonic()
    results = rr.replay(lists, (rr.resolve_core("v98"), rr.resolve_core(args.core)), Compare(specs),
                        workers=args.workers, part=args.part)
    summary = _summary(results, specs, cores)
    print(json.dumps({"shard": args.shard, "wall_time_s": round(time.monotonic() - started, 1),
                      **{k: summary[k] for k in ("lists", "classes", "passing", "failing", "unexpected_differences",
                                                 "expected_by_note", "outcomes")},
                      "unexpected": {k: v["lists"] for k, v in summary["unexpected_by_kind_attribute"].items()}}, indent=1))


if __name__ == "__main__":
    main()
