"""P0 path-dependent probe: a pytest plugin that records each published
finding's required-input status, without changing production code.

It wraps two callables at runtime:

* ``packages.derivation.runner._Run.pins_for`` - records, for every rule
  evaluation, the status of each symbol in the rule's declared ``requires``:
  ``pinned`` (the symbol is bound and its pin is in the returned pins, so the
  evaluation read it), ``unpinned`` (bound in this run but not read on this
  path), ``no-source`` (never bound in this run), or ``collected-pinned`` /
  ``collected-unpinned`` for collect names.
* ``packages.derivation.live.live_coordinate_run`` - after each run that
  publishes, matches every published finding to its own ``pins_for`` record
  (same rule, same pins) and appends one JSON line per finding to the
  directory named by ``P0_PROBE_OUT``.

Usage (repository root):

  P0_PROBE_OUT=<dir> PYTHONPATH=<this dir>:<repo root> \
    python3 -m pytest -p p0_path_probe <test files>

Raw dumps are not committed; ``p0_path_scan.py`` reads them.
"""
import json
import os

_OUT = os.environ.get("P0_PROBE_OUT")
_CALLS = {}      # (rule id, rule version) -> list of (canonical pins, statuses)


def _canon(pins):
    return json.dumps(sorted(pins, key=lambda p: json.dumps(p, sort_keys=True)), sort_keys=True)


def _statuses(run, rule, pins):
    from packages.derivation.runner import _Run  # noqa: F401  (type context only)

    out = {}
    symbol_pin = getattr(run, "symbol_pin", {})
    source_fids = getattr(run, "source_fids", {}) or {}
    for sym in rule.get("requires", []) or []:
        if sym in symbol_pin:
            fid, ver, role, provenance = symbol_pin[sym]
            matched = any(p.get("id") == fid and p.get("role") == role for p in pins)
            out[sym] = {
                "status": "pinned" if matched else "unpinned",
                "fid": fid, "role": role, "provenance": provenance,
            }
        elif sym in source_fids:
            ids = set(source_fids[sym])
            matched = any(p.get("id") in ids for p in pins)
            out[sym] = {"status": "collected-pinned" if matched else "collected-unpinned"}
        else:
            out[sym] = {"status": "no-source"}
    return out


def pytest_configure(config):
    if not _OUT:
        return
    import packages.derivation.runner as runner
    import packages.derivation.live as live

    orig_pins_for = runner._Run.pins_for

    def pins_for(self, rule, access):
        pins = orig_pins_for(self, rule, access)
        key = (rule["id"], str(rule["version"]))
        _CALLS.setdefault(key, []).append((_canon(pins), _statuses(self, rule, pins)))
        return pins

    runner._Run.pins_for = pins_for

    orig_live = live.live_coordinate_run

    def wrapper(*args, **kwargs):
        _CALLS.clear()
        outcome = orig_live(*args, **kwargs)
        pubs = getattr(outcome, "publications", None)
        if pubs and outcome.refusal is None:
            worker = os.environ.get("PYTEST_XDIST_WORKER", "main")
            path = os.path.join(_OUT, f"probe-{worker}.jsonl")
            test = os.environ.get("PYTEST_CURRENT_TEST", "?").split(" (")[0]
            with open(path, "a", encoding="utf-8") as fh:
                for pub in pubs:
                    finding = pub.finding
                    pins = finding.get("pins") or []
                    rule_pins = [p for p in pins if p.get("role") == "computation"]
                    record = {
                        "test": test,
                        "finding_id": finding.get("id"),
                        "symbol": finding.get("symbol"),
                        "version": finding.get("version"),
                        "rule_pins": rule_pins,
                        "statuses": None,
                        "matched": False,
                    }
                    target = _canon(pins)
                    for rp in rule_pins:
                        for canon_pins, statuses in _CALLS.get((rp["id"], str(rp["version"])), []):
                            if canon_pins == target:
                                record["statuses"] = statuses
                                record["matched"] = True
                                break
                        if record["matched"]:
                            break
                    fh.write(json.dumps(record, sort_keys=True) + "\n")
        return outcome

    live.live_coordinate_run = wrapper
