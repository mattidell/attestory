"""Shared graphs preserve incoming pins and reject malformed references."""
import copy
import json
import pytest
from typing import Any
from packages.derivation.explanation import explain
from packages.derivation.explanation_graph import GraphBuilder, validate_graph


def finding(name: str, pins: list[dict[str, str]]) -> dict[str, Any]:
    return {'id': name, 'version': 'v1', 'symbol': name, 'value': '1', 'pins': pins}


def pin(name: str, role: str = 'input', version: str = 'v1') -> dict[str, str]:
    return {'id': name, 'version': version, 'role': role}


def test_diamond_roles_duplicate_edges_and_roots() -> None:
    derived = {f['id']: f for f in [finding('demo.a', [pin('demo.b'), pin('demo.c')]),
        finding('demo.b', [pin('demo.d', 'input'), pin('demo.d', 'choice'), pin('demo.d')]),
        finding('demo.c', [pin('demo.d')]), finding('demo.d', [pin('demo.leaf')])]}
    builder = GraphBuilder(derived)
    builder.add_root('demo.a', role='output', authorization={'status':'first'})
    builder.add_root('demo.c', role='output', authorization={'status':'second'})
    graph = builder.to_dict()
    d = [key for key, value in graph['nodes'].items() if value['id'] == 'demo.d']
    assert len(d) == 1
    b = next(n for n in graph['nodes'].values() if n['id'] == 'demo.b')
    assert [e['pin']['role'] for e in b['edges']] == ['choice', 'input', 'input']
    assert all(e['target'] == d[0] for e in b['edges'])
    assert [r['authorization']['status'] for r in graph['roots']] == ['first', 'second']
    assert 'authorization' not in graph['nodes'][d[0]]
    assert explain('demo.a', role='output', derived=derived).to_dict()['schema'] == 'explanation-graph.v1'


def test_layered_graph_is_linear_and_cycle_is_rejected() -> None:
    derived = {}
    for i in range(30):
        children = [] if i == 0 else [pin(f'demo.{i-1}'), pin(f'demo.{i-1}', 'choice')]
        f = finding(f'demo.{i}', children)
        derived[f['id']] = f
    graph = explain('demo.29', role='output', derived=derived).to_dict()
    assert len(graph['nodes']) == 30
    assert sum(len(n['edges']) for n in graph['nodes'].values()) == 58
    assert len(json.dumps(graph)) < 20000
    derived['demo.0']['pins'].append(pin('demo.29'))
    with pytest.raises(ValueError, match='CYCLIC_DEPENDENCY_ERROR'):
        explain('demo.29', role='output', derived=derived)


def test_provenance_collision_and_dangling_reference() -> None:
    derived = {'demo.a':finding('demo.a', [pin('demo.d'),pin('demo.d','parameter')]), 'demo.d':finding('demo.d',[])}
    graph = explain('demo.a', role='output', derived=derived).to_dict()
    assert {n['kind'] for n in graph['nodes'].values() if n['id']=='demo.d'} == {'derived','reference'}
    bad = copy.deepcopy(graph)
    next(n for n in bad['nodes'].values() if n['id']=='demo.a')['edges'][0]['target'] = 'missing'
    with pytest.raises(ValueError): validate_graph(bad)


def test_npe_v4_run_scoped_blocked_predecessor_and_sparse() -> None:
    from packages.derivation.explanation import walk_npe
    rules = [dict(id='demo.a.rule', version='v1', publishes='demo.a', requires=['demo.b']),
             dict(id='demo.b.rule', version='v1', publishes='demo.b', requires=[])]
    records = [dict(run_id='demo.one', phase='started', workspace_revision=1),
        dict(run_id='demo.one', phase='completed', workspace_revision=1, dispositions=[
            dict(artifact_id='demo.a.rule', disposition='blocked', code='COMPLETENESS_VALUE_VIOLATION', missing=[]),
            dict(artifact_id='demo.b.rule', disposition='published', finding_id='demo.finding')]),
        dict(run_id='demo.two', phase='started', workspace_revision=2),
        dict(run_id='demo.two', phase='interrupted', workspace_revision=2, dispositions=[])]
    derived = {'demo.finding':finding('demo.finding',[pin('demo.source')])}
    derived['demo.finding']['symbol'] = 'demo.b'
    one = walk_npe(run_id='demo.one', symbol='demo.a', rules=rules, records=records, derived=derived)
    assert one['schema'] == 'npe-walk.v4'
    root = one['nodes'][one['root']]
    assert root['code'] == 'COMPLETENESS_VALUE_VIOLATION'
    predecessor = one['nodes'][root['children'][0]]
    assert predecessor['finding_id'] == 'demo.finding'
    assert predecessor['explanation_root'] in one['explanation_graph']['nodes']
    assert any(n['id'] == 'demo.source' for n in one['explanation_graph']['nodes'].values())
    two = walk_npe(run_id='demo.two', symbol='demo.a', rules=rules, records=records, derived=derived)
    assert two['nodes'][two['root']]['node_kind'] == 'no_disposition_recorded'
    assert two['nodes'][two['root']]['closing_phase'] == 'interrupted'
    assert not two['explanation_graph']['nodes']


def test_conflicting_finding_identity_rejected_and_snapshots_isolated() -> None:
    from packages.derivation.explanation import index_derived
    original = finding('demo.a', [])
    changed = dict(original, value='2')
    with pytest.raises(ValueError, match='conflicting finding identity'):
        index_derived([original, changed])
    builder = GraphBuilder({'demo.a':original}, run_id='demo.old')
    original['value'] = '2'
    builder.add_root('demo.a', role='output')
    graph = builder.to_dict()
    assert graph['nodes'][graph['roots'][0]['target']]['value'] == '1'
    newer = GraphBuilder({'demo.a':changed}, run_id='demo.new')
    newer.add_root('demo.a', role='output')
    assert newer.to_dict()['nodes'][newer.roots[0]['target']]['value'] == '2'


def test_npe_validator_rejects_dangling_and_wrong_run() -> None:
    from packages.derivation.explanation import walk_npe, validate_npe
    records = [dict(run_id='demo.run', phase='started', workspace_revision=1)]
    rules = [dict(id='demo.rule', version='v1', publishes='demo.out', requires=[])]
    walk = walk_npe(run_id='demo.run', symbol='demo.out', rules=rules, records=records)
    bad = copy.deepcopy(walk)
    bad['nodes']['demo.out']['children'] = ['demo.missing']
    with pytest.raises(ValueError): validate_npe(bad)
    bad = copy.deepcopy(walk)
    bad['explanation_graph']['run_id'] = 'demo.other'
    with pytest.raises(ValueError): validate_npe(bad)


def test_runtime_boundaries_reject_published_schema_invalid_shapes() -> None:
    from packages.derivation.explanation import validate_npe, walk_npe
    from packages.derivation.presentation_projection import PresentationModelError, validate_presentation_model
    graph = explain('demo.leaf', role='output', derived={}).to_dict()
    graph['roots'][0]['role'] = ''
    with pytest.raises(ValueError): validate_graph(graph)
    walk = walk_npe(run_id='demo.run', symbol='demo.out', rules=[], records=[{'run_id':'demo.run','phase':'started','workspace_revision':0}])
    walk['id'] = ''
    with pytest.raises(ValueError): validate_npe(walk)
    sample = json.loads((__import__('pathlib').Path('packages/sample_data/derivation/explanation_sharing/presentation-model.v2.json')).read_text())
    sample['runId'] = ''
    with pytest.raises(PresentationModelError): validate_presentation_model(sample)


def test_leaf_projection_layered_diamond_expands_each_shared_finding_once() -> None:
    from packages.derivation.presentation_projection import _leaf_pins
    class CountingDict(dict[str, dict[str, Any]]):
        calls = 0
        def get(self, key: str, default: Any = None) -> Any:
            self.calls += 1
            return super().get(key, default)
    publications = CountingDict()
    for i in range(25):
        publications[f'demo.{i}'] = finding(f'demo.{i}', [pin('demo.leaf')] if i == 0 else [pin(f'demo.{i-1}'), pin(f'demo.{i-1}', 'choice')])
    leaves = _leaf_pins([pin('demo.24')], publications_by_id=publications, seen=frozenset())
    assert leaves == {('demo.leaf', 'v1')}
    assert publications.calls <= 51


def test_same_provenance_id_different_versions_and_full_pin_metadata() -> None:
    first = {'id':'demo.parameter', 'version':'v1', 'role':'parameter', 'origin':'demo.first'}
    second = {'id':'demo.parameter', 'version':'v2', 'role':'parameter', 'origin':'demo.second'}
    graph = explain('demo.root', role='output', derived={'demo.root':finding('demo.root',[first, second])}).to_dict()
    root = graph['nodes'][graph['roots'][0]['target']]
    assert [edge['pin'] for edge in root['edges']] == [first, second]
    targets = [graph['nodes'][edge['target']] for edge in root['edges']]
    assert [node['version'] for node in targets] == ['v1', 'v2']
    assert root['edges'][0]['target'] != root['edges'][1]['target']


def test_projection_refuses_ambiguous_published_predecessor() -> None:
    from packages.derivation.presentation_projection import PresentationModelError, build_presentation_model
    from packages.kernel.findings import FindingState
    from tests.test_capital_gain_distributions_line7a_t3_presentation import _numeric_field
    field = _numeric_field()
    root_symbol = field['binds_symbol']
    members = [field, {'id':'demo.rule.root','publishes':root_symbol,'requires':['demo.dep']},
               {'id':'demo.rule.a','publishes':'demo.dep','requires':[]},
               {'id':'demo.rule.b','publishes':'demo.dep','requires':[]}]
    rows = [{'artifact_id':'demo.rule.root','symbol':root_symbol,'disposition':'blocked','code':'DEPENDENCY_ABSENT'},
            {'artifact_id':'demo.rule.a','symbol':'demo.dep','disposition':'published','finding_id':'demo.a'},
            {'artifact_id':'demo.rule.b','symbol':'demo.dep','disposition':'published','finding_id':'demo.b'}]
    with pytest.raises(PresentationModelError, match='ambiguous published disposition predecessor'):
        build_presentation_model(run_id='demo.run', resolved_members=members, state=FindingState(), publications=[], dispositions=rows)


def test_npe_run_scoped_publication_fallback_never_uses_later_run() -> None:
    from packages.derivation.explanation import walk_npe
    rules = [dict(id='demo.rule', version='v1', publishes='demo.output', requires=[])]
    records = [dict(run_id='demo.old', phase='started', workspace_revision=1),
               dict(run_id='demo.old', phase='interrupted', workspace_revision=1, dispositions=[]),
               dict(run_id='demo.new', phase='started', workspace_revision=2)]
    old = finding('demo.old.finding', [])
    old['symbol'] = 'demo.output'
    new = finding('demo.new.finding', [])
    new['symbol'] = 'demo.output'
    acts = [{'kind':'derived-publication','payload':{'run_id':'demo.old','finding':old}},
            {'kind':'derived-publication','payload':{'run_id':'demo.new','finding':new}}]
    result = walk_npe(run_id='demo.old', symbol='demo.output', rules=rules, records=records,
                      act_log=acts, derived={'demo.old.finding':old, 'demo.new.finding':new})
    node = result['nodes'][result['root']]
    assert node['finding_id'] == 'demo.old.finding'
    assert result['explanation_graph']['nodes'][node['explanation_root']]['id'] == 'demo.old.finding'


@pytest.mark.parametrize('mutation', ['kind', 'payload'])
def test_provenance_mutations_are_rejected(mutation: str) -> None:
    graph = explain('demo.a', role='output', derived={
        'demo.a':finding('demo.a', [pin('demo.d'), pin('demo.d', 'parameter')]),
        'demo.d':finding('demo.d', [])}).to_dict()
    node = graph['nodes'][graph['roots'][0]['target']]
    edge = next(edge for edge in node['edges'] if edge['pin']['role'] == 'parameter')
    if mutation == 'kind':
        edge['target'] = next(key for key, value in graph['nodes'].items() if value['id'] == 'demo.d' and value['kind'] == 'derived')
    else:
        graph['nodes'][edge['target']]['symbol'] = 'demo.fabricated'
        graph['nodes'][edge['target']]['value'] = '999'
    with pytest.raises(ValueError):
        validate_graph(graph)
