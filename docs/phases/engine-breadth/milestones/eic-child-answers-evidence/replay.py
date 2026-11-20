"""Full-surface replay: published v100 against the scratch v101 ``g`` (route 1: guarded roster counts and member questions).

Run: python3 replay.py <scratch-core.json> --shard I/N --part <part-file-outside-repo>
     python3 replay.py <scratch-core.json> --summarize <part-files...> --out replay.json
     python3 replay.py <scratch-core.json> --probe --shard I/N --part <part-file-outside-repo>
     python3 replay.py <scratch-core.json> --probe --summarize <part-files...> --out replay-probe.json

Uses tools/recorded_replay.py unchanged (snapshots, diff, strict
``classify_full`` through ``FullSurfaceCompare``): every saved page field,
attachment, explanation-graph node and report row on both cores; every
difference no expectation below names fails the list. No normalisation is
added.

``--probe`` replays the probe.py lists instead (every case; the named answer
is left unanswered for the named member, nothing is pre-filled for it).
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
BASE = "v100"


def _design():
    return rr._module("eicc_p0_design", HERE / "design.py")


def _probe():
    return rr._module("eicc_p0_probe", HERE / "probe.py")


def expectations() -> list[rr.Expectation]:
    d = _design()
    content = REPO / "packages/content/tax/2025"
    specs = [rr.version_change(P + "package.core-calculations", "v100", "v101")]
    specs += [rr.version_change(rule, "v1", "v2") for rule in d.GUARDS]
    guarded = {subject for _family, _member, tests in d.GUARDS.values() for _symbol, subject in tests}
    for body in d.questions(content).values():
        if body["fact_type"]["id"] not in guarded:
            continue
        # A line that waits only on a guarded count's declared missing answer shows that answer's question
        # (on v100 the same line shows no sentence at all).
        specs.append(rr.Expectation(("page", "model"), r"sentence", r"", "added", rr.ANY, body["question"],
                                    note="question shown:" + body["fact_type"]["id"].removeprefix(P)))
    # The order record of a reasons list that is new on the line; "added" only, so a reorder still fails.
    specs.append(rr.Expectation(("page", "model"), r"resolved\.reasons@order", r"^sections\[", "added", None, rr.ANY,
                                note="reasons list added on a line that had none"))
    # The blocked count row now names the missing answer's fact type with DEPENDENCY_ABSENT instead of the
    # blocked member with DEPENDENCY_INVALID (the rows and graph nodes of the two count rules only).
    for rule in d.GUARDS:
        ident = re.escape(rule)
        specs.append(rr.Expectation(("row", "graph", "report", "model"), r".*(code|missing).*", ident, None, rr.ANY,
                                    rr.ANY, note="blocked count names the answer:" + rule.removeprefix(P + "rule.")))
    return specs


ALIAS_DIGEST = re.compile(r"(finding~[^~\s\"]+~)[0-9a-f]{10}")


def _undigest(value: object) -> str:
    return ALIAS_DIGEST.sub(r"\1D", json.dumps(value, sort_keys=True))


def explain(keys: list[str], lists: list, core: str) -> dict:
    """Every difference on the named lists, sorted into what P0 can account for.

    ``alias``: a structural alias (``finding~<symbol>~<digest>``) whose symbol is unchanged and whose digest
    moved because an input of that finding (or of one upstream) changed; ``count input``: a record added to,
    removed from or reordered on a guarded count's finding (its new declared reads); ``declared``: an expectation
    above matches it; anything else is listed. A value or disposition change is never sorted as alias.
    """
    specs = expectations()
    d = _design()
    counts = [re.escape(s) for s in ("eic.qualifying-child-count", "ctc.child-count", *d.GUARDS)]

    def version_free(item: dict, value: object) -> object:
        # A rekeyed record's package (v100 -> v101) or guarded rule (v1 -> v2) pin is the declared version
        # change; compare the rest of the record.
        if re.search(r"package\.core-calculations|" + "|".join(re.escape(r) for r in d.GUARDS), item["identity"]) \
                and re.fullmatch(r"(?:.*\.)?(?:version|pinVersion)", item["attribute"]):
            return "<declared version>"
        return value
    cores = (rr.resolve_core(BASE), rr.resolve_core(core))
    out: dict = {}
    for key, acts in lists:
        if key not in keys:
            continue
        run_id = "demo.fsr." + __import__("hashlib").sha256(key.encode()).hexdigest()[:20]
        left, right = rr.snapshot_run(cores[0], acts, run_id), rr.snapshot_run(cores[1], acts, run_id)
        tally: Counter = Counter()
        other: list = []
        removed: Counter = Counter()
        added: Counter = Counter()
        pending: list = []
        for item in rr.diff_snapshots(left, right):
            attribute = item["attribute"]
            if any(spec.matches(item) for spec in specs):
                tally["declared"] += 1
            elif item["change"] == "changed" and re.search(r"(^|[.\]])(value|disposition)$", attribute):
                other.append(item)  # a value or disposition that changed in place is never sorted away
            elif item["change"] == "changed" and _undigest(item["before"]) == _undigest(item["after"]):
                tally["alias"] += 1
            elif item["change"] in ("added", "removed"):
                # A record keyed by an alias that moved is removed under the old key and added under the new
                # one; it pairs only when kind, undigested key, attribute and undigested value all agree.
                slot = (item["kind"], _undigest(item["identity"]), attribute,
                        _undigest(version_free(item, item["after"] if item["change"] == "added" else item["before"])))
                (added if item["change"] == "added" else removed)[slot] += 1
                pending.append((slot, item))
            elif any(re.search(c, item["identity"]) for c in counts):
                tally["count input"] += 1
            else:
                other.append(item)
        paired = added & removed
        for slot, item in pending:
            if paired[slot] > 0 and item["change"] == "added":
                tally["alias rekeyed (added half)"] += 1
                continue
            if paired[slot] > 0 and item["change"] == "removed":
                tally["alias rekeyed (removed half)"] += 1
                continue
            if any(re.search(c, item["identity"]) for c in counts) \
                    and not re.search(r"(^|[.\]])(value|disposition)$", item["attribute"]):
                tally["count input"] += 1
            else:
                other.append(item)
        out[key] = {"differences": sum(tally.values()) + len(other), "sorted": dict(tally), "other_total": len(other),
                    "other": other[:30]}
    return out


def probe_lists() -> list:
    probe = _probe()
    return [(f"probe/{case}", probe.build(case)) for case in probe.CASES]


def _summary(results: dict, specs: list, cores: list) -> dict:
    classes = Counter(row["class"] for row in results.values())
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
        "expectations_declared": len(specs), "expectations_used": len(used_by),
        "unused_expectations": [rr.describe_expectation(s)["note"] for i, s in enumerate(specs) if i not in used_by],
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
    parser.add_argument("core")
    parser.add_argument("--shard", default="0/1")
    parser.add_argument("--part")
    parser.add_argument("--workers", type=int, default=None)
    parser.add_argument("--summarize", nargs="*")
    parser.add_argument("--probe", action="store_true", help="the probe.py lists instead of the recorded lists")
    parser.add_argument("--out")
    parser.add_argument("--explain", nargs="*", help="list keys to sort every difference of (see explain())")
    args = parser.parse_args()
    if args.explain is not None:
        lists = probe_lists() if args.probe else rr.recorded_lists()
        keys = args.explain or [k for k, _ in lists]
        text = json.dumps({"core": BASE + " against scratch", "lists": explain(keys, lists, args.core)}, indent=1) + "\n"
        rr._check_no_local_paths(text, "explain")
        Path(args.out).write_text(text, encoding="utf-8")
        print(text[:6000])
        return
    specs = expectations()
    cores = [rr.core_fingerprint(BASE), rr.core_fingerprint(args.core)]
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
                                                   "expectations_declared", "expectations_used", "unused_expectations",
                                                   "expected_by_note", "outcomes")}, indent=1))
        return
    index, total = (int(x) for x in args.shard.split("/"))
    if args.probe:
        lists = probe_lists()
        from tests import evidence_loader  # as rr.recorded_lists does, release the loader before spawning workers

        owner = evidence_loader.current_owner()
        if owner:
            evidence_loader.release(owner)
    else:
        lists = rr.recorded_lists()
    lists = lists[index::total]
    started = time.monotonic()
    results = rr.replay(lists, (rr.resolve_core(BASE), rr.resolve_core(args.core)), rr.FullSurfaceCompare(specs),
                        workers=args.workers, part=args.part)
    summary = _summary(results, specs, cores)
    print(json.dumps({"shard": args.shard, "wall_time_s": round(time.monotonic() - started, 1),
                      **{k: summary[k] for k in ("lists", "classes", "passing", "failing", "unexpected_differences",
                                                 "expected_by_note", "outcomes")},
                      "unexpected": {k: v["lists"] for k, v in summary["unexpected_by_kind_attribute"].items()}}, indent=1))


if __name__ == "__main__":
    main()
