#!/usr/bin/env python3
"""Census committed saved presentation models; optionally replay synthetic v58.

Run at repository root: python3 docs/phases/engineering-health/milestones/
explanation-sharing-evidence/census.py [--v58|--self-test]
Only Git-tracked JSON is read; no golden is regenerated or modified.
"""
from __future__ import annotations
import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT))

def tracked():
    return subprocess.check_output(['git', 'ls-files', '-z', '*.json'], cwd=ROOT).decode().split('\0')[:-1]

def models():
    for name in sorted(tracked()):
        obj = json.loads((ROOT / name).read_bytes())
        if isinstance(obj, dict) and obj.get('schema') == 'presentation-model.v1':
            yield name, obj

def compact(obj):
    return len(json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode())

def metrics(root):
    nodes = list(walk(root))
    ids = {n.finding_id for n in nodes}
    edges = sum(len(n.children) for n in nodes)
    return len(nodes), len(ids), edges, compact(root.to_dict())

def walk(root):
    stack = [root]
    while stack:
        node = stack.pop()
        yield node
        stack.extend(reversed(node.children))

def self_test():
    from packages.derivation.explanation import explain_legacy as explain
    def finding(name, children):
        return {'id':name, 'symbol':name, 'value':'0', 'version':'v1', 'pins':[
            {'id':child, 'role':'input', 'version':'v1'} for child in children]}
    graph = {f['id']:f for f in [finding('a',['b','c']), finding('b',['d']), finding('c',['d']), finding('d',[])]}
    tree = explain('a',role='output',derived=graph)
    assert metrics(tree)[:3] == (5,4,4)
    assert metrics(explain('x',role='output',derived={}))[:3] == (1,1,0)
    graph['d'] = finding('d',['a'])
    try:
        explain('a',role='output',derived=graph)
    except ValueError as e:
        assert str(e) == 'CYCLIC_DEPENDENCY_ERROR'
    else:
        raise AssertionError('cycle was not rejected')
    print('self-test: diamond 5/4/4; missing leaf 1/1/0; cycle rejected')

def tree_count(obj):
    if isinstance(obj, dict):
        return int({'finding_id','role','kind','children'} <= obj.keys()) + sum(map(tree_count, obj.values()))
    if isinstance(obj, list):
        return sum(map(tree_count, obj))
    return 0

def census():
    print('class\tpath\tschema\tfile_bytes\tsections\tpublished_roots\troot_pin_occurrences\tdistinct_root_pin_id_versions\tcitation_occurrences\tdistinct_citation_id_versions\tcitation_json_bytes\tstored_tree_nodes\tlargest_root_pins')
    for name, model in models():
        sections = model.get('sections', [])
        roots = [(s['id'], s.get('resolved',{}).get('act',{})) for s in sections if isinstance(s.get('resolved',{}).get('act'),dict) and isinstance(s['resolved']['act'].get('finding'),dict)]
        pins = [p for _,a in roots for p in a['finding'].get('pins',[])]
        sites = [site for s in sections for site in s.get('citationSites',[])]
        maxroot = max(((len(a['finding'].get('pins',[])),sid) for sid,a in roots),default=(0,'-'))
        kind = 'golden' if name.startswith('packages/sample_data/') and '/presentation/' in name else 'example'
        row = [kind,name,model['schema'],(ROOT/name).stat().st_size,len(sections),len(roots),len(pins),len({(p.get('id'),p.get('version')) for p in pins}),len(sites),len({(p.get('pinId'),p.get('pinVersion')) for p in sites}),compact(sites),tree_count(model),f'{maxroot[1]}:{maxroot[0]}']
        print('\t'.join(map(str,row)))
        for sid,a in roots:
            finding = a['finding']; ps=finding.get('pins',[])
            section = next(s for s in sections if s['id']==sid)
            cs=section.get('citationSites',[])
            print('\t'.join(map(str,['root',name,sid,finding.get('schema','-'),compact(finding),len(ps),len({(p.get('id'),p.get('version')) for p in ps}),len(cs),len({(p.get('pinId'),p.get('pinVersion')) for p in cs}),compact(cs)])))

def v58():
    from packages.derivation.explanation import explain_legacy as explain, index_derived
    from tests import test_dtb_presentation as t
    from packages.derivation.presentation_projection import project_presentation_v1
    for label, acts, run in [('parent',t._acts_single_parent_wins,t.RUN_PARENT_WINS),('grandparent',t._acts_single_grandparent_loses,t.RUN_GRANDPARENT_LOSES)]:
        model, pubs = t._present(acts(),run)
        golden = t._load_golden(t.PARENT_WINS_EXACT if label=='parent' else t.GRANDPARENT_LOSES_EXACT)
        assert project_presentation_v1(model) == golden
        root = explain(str(pubs[t.LINE27A]['id']),role='output',derived=index_derived(list(pubs.values())))
        n, ids, edges, size = metrics(root)
        node_ids = {n.finding_id for n in walk(root)}
        reached_findings = len(node_ids & {str(f['id']) for f in pubs.values()})
        unique = {}
        for item in walk(root):
            unique.setdefault(item.finding_id, item)
        retained_edges = sum(len(item.children) for item in unique.values())
        graph = model['explanationGraph']
        nodes = graph['nodes']
        root = graph['roots'][model['sectionRoots']['line-27a']['root']]
        visited = set()
        pending = [root['target']]
        while pending:
            key = pending.pop()
            if key in visited:
                continue
            visited.add(key)
            pending.extend(edge['target'] for edge in nodes[key]['edges'])
        single = {'schema': graph['schema'], 'run_id': graph['run_id'], 'roots': [root], 'nodes': {key: nodes[key] for key in sorted(visited)}}
        single_edges = sum(len(nodes[key]['edges']) for key in visited)
        print(f"{label}: single_graph_nodes={len(visited)} single_graph_edges={single_edges} single_graph_compact_bytes={compact(single)} all_run_publications={len(pubs)} reachable_published_findings={reached_findings} tree_occurrences={n} unique_ids={ids} edge_occurrences={edges} first_id_retained_edges={retained_edges} compact_tree_bytes={size} graph_all_roots_nodes={len(nodes)} graph_all_roots_edges={sum(len(x['edges']) for x in nodes.values())} graph_all_roots_compact_bytes={compact(graph)} v1_saved_bytes={len(json.dumps(golden, indent=2, sort_keys=True).encode()) + 1} v2_saved_bytes={len(json.dumps(model, indent=2, sort_keys=True).encode()) + 1} saved_v1_projection_matches=yes")

if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--self-test',action='store_true')
    parser.add_argument('--v58',action='store_true')
    args=parser.parse_args()
    if args.self_test: self_test()
    elif args.v58: v58()
    else: census()
