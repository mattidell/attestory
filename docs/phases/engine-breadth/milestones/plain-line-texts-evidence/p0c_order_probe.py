"""Check report-observation ordering on published v95, with fixed hash seeds.

Run twice with different PYTHONHASHSEED values and distinct outside-repo
output directories. Uses the real live coordinator, not a simulated page.
"""
from __future__ import annotations
import importlib.util
import os
from pathlib import Path
import sys

HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location("plt_p0c_order_census",HERE/"census.py")
census=importlib.util.module_from_spec(spec);sys.modules[spec.name]=census;spec.loader.exec_module(census)

if __name__=="__main__":
    target=Path(sys.argv[1]).resolve(); assert census.REPO not in target.parents
    target.mkdir(parents=True,exist_ok=False)
    os.environ.update({"PLT_CENSUS_SCRATCH":str(target),"PLT_COMPACT_PART":"1"})
    h=census.rr._get_harness()
    acts=h.ccr.add_mortgage_itemizer(h.ccr.base_return(),18000.0)
    result=census.per_list("demo.plt.mortgage-detail",acts,census.rr.resolve_core("v95"))
    assert result["outcome"]=="success",result
    census.write(target/"result.json",result)
