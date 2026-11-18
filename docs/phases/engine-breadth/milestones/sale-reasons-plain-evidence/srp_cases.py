"""Synthetic demo.* states for the two reasons that the recorded lists may not draw.

Each case is one sale on the audit harness's opened return with the honest
answer set, so the only cause of a block is the state named in its key.
"""
from __future__ import annotations
import importlib.util
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
sys.path.insert(0, str(REPO))
P = "tax.us.2025."


def harness():
    sys.path.insert(0, str(REPO))
    from tools import recorded_replay as rr
    return rr._get_harness()


def one(h, kind, term, tag, *, proceeds, basis, wash=0.0, long_term=None, rows=None, open_adjustment=False):
    acts = h.sale(h.opened(), kind, term, proceeds=proceeds, basis=basis, tag=tag, wash=wash,
                  long_term=long_term, rows=rows)
    if open_adjustment:
        fam = h.family_id(kind, term, "adjustment") + ".source-closure"
        acts = h.renumber(h.strip(acts, fam))
    acts = h.answer(acts, **h.honest({kind}, loss=proceeds < basis, new_questions=False))
    return acts


def cases():
    h = harness()
    out = []
    for kind, term, lt in (("noncovered", "st", "yes"), ("noncovered", "lt", "no"), ("no1099b", "st", "yes"),
                           ("no1099b", "lt", "no"), ("codeb", "lt", "no")):
        extra = {"corrected": 7000.0} if kind == "codeb" else {}
        acts = h.sale(h.opened(), kind, term, proceeds=2000, basis=8000, tag=f"demo.srp.hold.{kind}.{term}",
                      long_term=lt, **extra)
        acts = h.answer(acts, **h.honest({kind}, loss=True, new_questions=False))
        out.append((f"demo.srp.holding.{kind}-{term}", acts))
    # Wash-sale amount above the sale's own loss, covered-W: adjustment family closed, then open.
    out.append(("demo.srp.wash.w-lt-closed", one(h, "w", "lt", "demo.srp.wlt", proceeds=2000, basis=3000, wash=1500)))
    out.append(("demo.srp.wash.w-st-open", one(h, "w", "st", "demo.srp.wsto", proceeds=2000, basis=3000, wash=1500,
                                               open_adjustment=True)))
    # Wash amount on a gain: both CODE_W_ON_GAIN and the loss bound fire.
    out.append(("demo.srp.wash.w-st-gain", one(h, "w", "st", "demo.srp.wgain", proceeds=3000, basis=2000, wash=500)))
    # The same bound on a noncovered sale: which family's sentence the page draws.
    out.append(("demo.srp.wash.noncovered-st", one(h, "noncovered", "st", "demo.srp.ncw", proceeds=2000, basis=3000, wash=1500)))
    return out
