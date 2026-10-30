"""Compare the actual launch walker against the current graph on layered reuse."""
import json
import runpy
import subprocess
import tempfile
from pathlib import Path
from packages.derivation.explanation import explain

base = subprocess.check_output(['git', 'show', 'bb9e05e98a390ce12631c5d8fd18025af5300cdd:packages/derivation/explanation.py'])
with tempfile.TemporaryDirectory() as directory:
    path = Path(directory) / 'base.py'
    path.write_bytes(base)
    old = runpy.run_path(str(path))['explain']
for depth in (5, 10):
    derived = {}
    for i in range(depth):
        derived[f'demo.{i}'] = {'id':f'demo.{i}', 'symbol':f'demo.{i}', 'value':'1', 'version':'v1',
            'pins':[] if i == 0 else [{'id':f'demo.{i-1}', 'version':'v1', 'role':role} for role in ('input','choice')]}
    tree = old(f'demo.{depth-1}', role='output', derived=derived, _memo={}).to_dict()
    pending = [tree]
    occurrences = 0
    while pending:
        node = pending.pop()
        occurrences += 1
        pending.extend(node['children'])
    graph = explain(f'demo.{depth-1}', role='output', derived=derived).to_dict()
    byte_count = lambda obj: len(json.dumps(obj, separators=(',', ':')).encode())
    print(f'depth={depth} base_tree_occurrences={occurrences} base_compact_bytes={byte_count(tree)} '
          f'graph_nodes={len(graph["nodes"])} graph_edges={sum(len(n["edges"]) for n in graph["nodes"].values())} '
          f'graph_compact_bytes={byte_count(graph)}')
