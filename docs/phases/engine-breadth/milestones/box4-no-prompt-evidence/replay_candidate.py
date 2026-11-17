"""Replay a revised candidate using recorded_replay and its saved v93 pins.

The initial full comparison is tools/recorded_replay.py neighbour v93 <core>.
This follow-up avoids re-running an unchanged deterministic baseline. Input
lists and tools/tests/packages are unchanged. Both part files stay outside Git.
"""
from __future__ import annotations
import argparse
from collections import Counter
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import sys
import time

HERE=Path(__file__).resolve().parent
REPO=HERE.parents[4]
sys.path.insert(0,str(REPO))
from tools import recorded_replay as rr
CACHE={}

def worker(key,acts,cores):
    baseline,candidate=cores
    cache_path=os.environ["B4N_BASELINE_PART"]
    if cache_path not in CACHE:
        CACHE[cache_path]=json.loads(Path(cache_path).read_text())['results']
    before=CACHE[cache_path][key]['pins']['v93']
    import re
    slug=re.sub(r'[^A-Za-z0-9_.-]','.',key)
    after=rr.pin_run(candidate,acts,'demo.replay.nb.v94.'+slug)
    row=rr.classify(before,after,name_a='v93',name_b='v94')
    row['pins']={'v93':before,'v94':after}
    return row

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('core',type=Path)
    parser.add_argument('--baseline-part',required=True,type=Path)
    parser.add_argument('--part',required=True,type=Path)
    args=parser.parse_args()
    started=time.monotonic()
    baseline=rr.resolve_core('v93');candidate=rr.resolve_core(args.core)
    old=json.loads(args.baseline_part.read_text())
    assert old['_metadata']['cores'][0]==rr.core_fingerprint(baseline)
    lists=rr.recorded_lists()
    assert set(old['results'])=={k for k,_ in lists}
    workers=max(1,(os.cpu_count() or 2)-1)
    os.environ["B4N_BASELINE_PART"]=str(args.baseline_part.resolve())
    results=rr.replay(lists,(baseline,candidate),worker,
                      workers=workers,part=args.part)
    # The final file uses the normal two-core fingerprint, so Track 0 can
    # reuse it with the standard neighbour command on the identical cores.
    metadata={'cores':[rr.core_fingerprint(baseline),rr.core_fingerprint(candidate)],
              'baseline_pin_reuse':{'source_part_sha256':hashlib.sha256(args.baseline_part.read_bytes()).hexdigest(),
                                   'unchanged_source_ref':'0f4658ab90070cbcb815e1917d7b1248de48988a'}}
    rr._write_part(args.part,results,metadata)
    changes=[{'id':k,**{x:y for x,y in v.items() if x!='pins'}} for k,v in sorted(results.items()) if v['class']!='identical']
    output={'distinct_lists':len(results),'runs':len(results),'workers':workers,
            'wall_time_s':round(time.monotonic()-started,3),
            'baseline':'v93 pins from the original foreground neighbour replay; unchanged inputs',
            'candidate':'revised scratch v94, replayed live',
            'counts':dict(Counter(r['class'] for r in results.values())),
            'changes':changes,'classes':{k:r['class'] for k,r in sorted(results.items())},
            'baseline_pin_reuse':metadata['baseline_pin_reuse']}
    spec=importlib.util.spec_from_file_location('b4n_replay_writer',HERE/'probe.py')
    m=importlib.util.module_from_spec(spec);sys.modules[spec.name]=m;spec.loader.exec_module(m)
    m.write(HERE/'rerun-output.json',output)
    print(json.dumps({k:v for k,v in output.items() if k not in ('changes','classes')},indent=2),flush=True)

if __name__=='__main__':main()
