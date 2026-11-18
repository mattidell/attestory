"""Key choice and copy cost, measured on the published member directory.

Run: python3 mro_key.py
Times, for one listing of the content directory (1813 files), the uncached
read+parse(+checksum of every object with a string id, as _resolve_member_corpus
does), the byte-keyed cache (read, SHA-256 of the bytes, reuse), and a stat-keyed
cache (path, size, mtime_ns, inode; no read). Also the copy cost of a private
body (deepcopy against the JSON-tree copy used) and the memory a full cache
holds. Writes key-measurements.json beside this file.
"""
from __future__ import annotations

import copy
import gc
import hashlib
import json
import os
from pathlib import Path
import resource
import statistics
import sys
import tempfile
import time

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
sys.path.insert(0, str(REPO))

from packages.derivation import production_resolver as pr  # noqa: E402
from packages.derivation.package_validation import citizen_checksum  # noqa: E402

CONTENT = REPO / "packages/content/tax/2025"


def best(fn, repeats: int = 5) -> float:  # type: ignore[no-untyped-def]
    times = []
    for _ in range(repeats):
        t = time.perf_counter()
        fn()
        times.append(time.perf_counter() - t)
    return statistics.median(times)


def uncached() -> None:
    for path in sorted(CONTENT.rglob("*.json")):
        try:
            body = json.loads(path.read_text("utf-8"))
        except ValueError:
            continue
        if isinstance(body, dict) and isinstance(body.get("id"), str):
            citizen_checksum(body)


def byte_keyed() -> None:
    for cand in pr._member_candidates(CONTENT):
        if isinstance(cand.view.get("id"), str):
            cand.checksum()


_STAT: dict[tuple[str, int, int, int], tuple[dict, str | None]] = {}


def stat_keyed() -> None:
    for path in sorted(CONTENT.rglob("*.json")):
        st = path.stat()
        key = (str(path), st.st_size, st.st_mtime_ns, st.st_ino)
        hit = _STAT.get(key)
        if hit is None:
            try:
                body = json.loads(path.read_text("utf-8"))
            except ValueError:
                continue
            if not isinstance(body, dict):
                continue
            hit = (body, citizen_checksum(body) if isinstance(body.get("id"), str) else None)
            _STAT[key] = hit


def listing_only() -> None:
    for _ in sorted(CONTENT.rglob("*.json")):
        pass


def main() -> None:
    out: dict = {"files": len(list(CONTENT.rglob("*.json"))), "content_bytes": sum(p.stat().st_size for p in CONTENT.rglob("*.json"))}
    out["listing_only_s"] = round(best(listing_only), 4)
    out["uncached_listing_s"] = round(best(uncached), 4)
    rss0 = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    pr.clear_member_cache()
    t = time.perf_counter(); byte_keyed(); out["byte_keyed_first_call_s"] = round(time.perf_counter() - t, 4)
    rss1 = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    out["byte_keyed_warm_listing_s"] = round(best(byte_keyed), 4)
    out["cache_entries"] = len(pr._MEMBER_CACHE)
    out["cache_rss_growth_mib"] = round((rss1 - rss0) / (1024 * 1024 if sys.platform == "darwin" else 1024), 1)
    stat_keyed()
    out["stat_keyed_warm_listing_s"] = round(best(stat_keyed), 4)
    read_hash = lambda: [hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(CONTENT.rglob("*.json"))]  # noqa: E731
    out["read_and_hash_all_files_s"] = round(best(read_hash), 4)
    # a call is 4 per replayed list (two resolutions, two callers each)
    out["per_list_uncached_s"] = round(4 * out["uncached_listing_s"], 3)
    out["per_list_byte_keyed_warm_s"] = round(4 * out["byte_keyed_warm_listing_s"], 3)
    out["per_list_stat_keyed_warm_s"] = round(4 * out["stat_keyed_warm_listing_s"], 3)
    # copy cost for the 1053 corpus-sized selection
    bodies = [c._entry._body for c in pr._member_candidates(CONTENT) if isinstance(c.view.get("id"), str)][:1053]
    out["copy_bodies"] = len(bodies)
    out["deepcopy_s"] = round(best(lambda: [copy.deepcopy(b) for b in bodies], 3), 4)
    out["json_tree_copy_s"] = round(best(lambda: [pr._copy_json(b) for b in bodies], 3), 4)
    raws = [p.read_bytes() for p in sorted(CONTENT.rglob("*.json"))][:1053]
    out["reparse_same_bodies_s"] = round(best(lambda: [json.loads(r) for r in raws], 3), 4)
    # staleness: same size and mtime, different bytes
    with tempfile.TemporaryDirectory() as tmp:
        f = Path(tmp) / "demo.json"
        f.write_text('{"id": "demo.a1"}', "utf-8")
        st = f.stat()
        key = (str(f), st.st_size, st.st_mtime_ns, st.st_ino)
        first = json.loads(f.read_text("utf-8"))
        f.write_text('{"id": "demo.b2"}', "utf-8")
        os.utime(f, ns=(st.st_atime_ns, st.st_mtime_ns))
        st2 = f.stat()
        out["stat_key_unchanged_after_same_size_same_mtime_edit"] = key == (str(f), st2.st_size, st2.st_mtime_ns, st2.st_ino)
        pr.clear_member_cache()
        pr._member_candidates(Path(tmp))
        f.write_text('{"id": "demo.a1"}', "utf-8"); os.utime(f, ns=(st.st_atime_ns, st.st_mtime_ns))
        out["byte_key_sees_edit"] = pr._member_candidates(Path(tmp))[0].view["id"] == "demo.a1" and first["id"] == "demo.a1"
    (HERE / "key-measurements.json").write_text(json.dumps(out, indent=1, sort_keys=True) + "\n")
    print(json.dumps(out, indent=1, sort_keys=True))


if __name__ == "__main__":
    main()
