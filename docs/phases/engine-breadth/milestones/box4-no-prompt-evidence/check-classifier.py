"""Exercise the strict classifier on saved real pins and five forbidden mutations.

Run with the retained Track 1 part file as the positional argument. No live runs.
"""
from __future__ import annotations

import argparse
from collections import Counter
from copy import deepcopy
import importlib.util
import json
from pathlib import Path
import time

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('b4n_strict_classifier', HERE / 'classify.py')
classifier = importlib.util.module_from_spec(spec)
spec.loader.exec_module(classifier)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('part', type=Path)
    parser.add_argument('--out', type=Path, default=HERE / 'repair-mutations.json')
    args = parser.parse_args()
    started = time.monotonic()
    results = json.loads(args.part.read_text())['results']
    previous = json.loads((HERE / 'track1-classification.json').read_text())['results']
    counts = Counter()
    witness = None
    for key, acts in classifier.recorded_lists():
        a, b = (results[key]['pins'][v] for v in ('v93', 'v94'))
        facts = classifier.answers(acts)
        label = classifier.classify_pair(a, b, facts, True)
        assert label != 'unexpected', key
        assert label == previous[key]['classification'], (key, label)
        counts[label] += 1
        if label == 'no_without_amount_changed' and witness is None:
            witness = (key, a, b, facts)
    assert witness is not None
    key, a, b, facts = witness
    mutations = {}
    for name in ('25b_disposition', '25b_code', 'value_0_to_999', 'added_row', 'removed_row'):
        mutated = deepcopy(b)
        if name == '25b_disposition':
            mutated['rows']['form1040-line25b'][0] = 'published'
        elif name == '25b_code':
            mutated['rows']['form1040-line25b'][1] = 'demo.unexpected-code'
        elif name == 'value_0_to_999':
            field = next(n for n, value in mutated['lines'].items() if type(value) is int and value == 0)
            mutated['lines'][field] = 999
        elif name == 'added_row':
            mutated['rows']['demo.added-row'] = ['published', None, []]
        else:
            del mutated['rows']['form1040-line25b']
        label = classifier.classify_pair(a, mutated, facts, True)
        assert label == 'unexpected', (name, label)
        mutations[name] = label
    output = {'real_pairs': sum(counts.values()), 'counts': dict(counts),
              'labels_preserved': True, 'witness': key, 'mutations': mutations,
              'wall_seconds': round(time.monotonic() - started, 3)}
    args.out.write_text(json.dumps(output, indent=2) + '\n')
    print(json.dumps(output, indent=2))


if __name__ == '__main__':
    main()
