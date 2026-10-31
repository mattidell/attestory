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
    graph = explain('demo.leaf', role='output', derived={'demo.leaf': finding('demo.leaf', [])}).to_dict()
    graph['roots'][0]['role'] = ''
    with pytest.raises(ValueError): validate_graph(graph)
    walk = walk_npe(run_id='demo.run', symbol='demo.out', rules=[], records=[{'run_id':'demo.run','phase':'started','workspace_revision':0}])
    walk['id'] = ''
    with pytest.raises(ValueError): validate_npe(walk)
    sample = json.loads((__import__('pathlib').Path('packages/sample_data/derivation/explanation_sharing/presentation-model.exact-pins.v2.json')).read_text())
    validate_presentation_model(sample)
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


def test_derived_dependency_requires_exact_snapshot_version_even_when_memoized() -> None:
    parent = finding('demo.parent', [pin('demo.child', version='v2')])
    child = dict(finding('demo.child', []), version='v2')
    bad_parent = finding('demo.bad', [pin('demo.child', version='v1')])
    builder = GraphBuilder({'demo.parent': parent, 'demo.bad': bad_parent, 'demo.child': child})
    builder.add_root('demo.parent', role='output')
    direct = GraphBuilder({'demo.bad': bad_parent, 'demo.child': child})
    with pytest.raises(ValueError, match='version'):
        direct.add_root('demo.bad', role='output')
    with pytest.raises(ValueError, match='version'):
        builder.add_root('demo.bad', role='output')


def test_saved_graph_rejects_derived_pin_version_mismatch() -> None:
    graph = explain('demo.parent', role='output', derived={
        'demo.parent': finding('demo.parent', [pin('demo.child')]),
        'demo.child': finding('demo.child', []),
    }).to_dict()
    edge = graph['nodes'][graph['roots'][0]['target']]['edges'][0]
    edge['pin']['version'] = 'v2'
    with pytest.raises(ValueError, match='pin mismatch'):
        validate_graph(graph)


def test_missing_explanation_root_is_rejected() -> None:
    with pytest.raises(ValueError, match='root'):
        GraphBuilder({}).add_root('demo.absent', role='output')


def _add_valid_bare_reference(graph: dict[str, Any], identifier: str) -> str:
    key = f'reference:{len(identifier)}:{identifier}:v1'
    graph['nodes'][key] = {'id': identifier, 'version': 'v1', 'kind': 'reference',
                           'symbol': None, 'value': None, 'produced_by': None, 'edges': []}
    validate_graph(graph)
    return key


def test_npe_published_finding_cannot_point_to_bare_reference() -> None:
    from packages.derivation.explanation import validate_npe, walk_npe
    rules = [dict(id='demo.rule', version='v1', publishes='demo.output', requires=[])]
    records = [dict(run_id='demo.run', phase='started', workspace_revision=1),
               dict(run_id='demo.run', phase='completed', workspace_revision=1, dispositions=[
                   dict(artifact_id='demo.rule', disposition='published', finding_id='demo.finding')])]
    walk = walk_npe(run_id='demo.run', symbol='demo.output', rules=rules, records=records,
                    derived={'demo.finding': finding('demo.finding', [])})
    target = _add_valid_bare_reference(walk['explanation_graph'], 'demo.finding')
    walk['nodes'][walk['root']]['explanation_root'] = target
    with pytest.raises(ValueError, match='finding reference'):
        validate_npe(walk)


def test_disposition_finding_cannot_point_to_bare_reference() -> None:
    from packages.derivation.presentation_projection import PresentationModelError, validate_presentation_model
    graph: dict[str, Any] = {'schema': 'explanation-graph.v1', 'run_id': 'demo.run', 'roots': [], 'nodes': {}}
    model: dict[str, Any] = {'schema': 'presentation-model.v2', 'runId': 'demo.run', 'pinLabels': {},
             'sections': [], 'citationGroups': [], 'attachments': [], 'unsupportedSourceFindings': [],
             'explanationGraph': graph, 'sectionRoots': {}, 'dispositionNodes': {}}
    target = _add_valid_bare_reference(graph, 'demo.finding')
    model['dispositionNodes']['demo.symbol'] = {'symbol': 'demo.symbol', 'children': [],
        'records': [{'disposition': 'published', 'finding_id': 'demo.finding'}], 'findingRoot': target}
    with pytest.raises(PresentationModelError, match='invalid shared explanation'):
        validate_presentation_model(model)


def test_collect_and_subject_count_preserve_each_source_finding_version() -> None:
    from packages.derivation.evaluator import AccessLog
    from packages.derivation.runner import SourceFact, _Run
    from packages.derivation.subject_dispatch import _assemble_pins
    from tests.derivation.test_runner import RunnerFixture
    fixture = RunnerFixture()
    fixture.setUp()
    sources = [SourceFact('demo.member', '1', 'demo.asserted', finding_version='v1'),
               SourceFact('demo.member', '2', 'demo.derived', finding_version='v2')]
    run = _Run(fixture.context(sources=sources), fixture.schemas)
    access = AccessLog()
    access.collects.add('demo.member')
    access.shared_key_count_findings.update({'demo.asserted', 'demo.derived'})
    collected = run.dependency_pins_for_access(access)
    assert {(p['id'], p['version']) for p in collected if p['role'] == 'input'} == {
        ('demo.asserted', 'v1'), ('demo.derived', 'v2')}
    pins = _assemble_pins(run, fixture.wages, access, {}, run.sources, run.source_fids,
                          run.source_fact_ids, 'demo.subject')
    assert {(p['id'], p['version']) for p in pins if p['role'] == 'input'} == {
        ('demo.asserted', 'v1'), ('demo.derived', 'v2')}


def test_graph_root_cannot_be_a_bare_reference() -> None:
    graph: dict[str, Any] = {'schema': 'explanation-graph.v1', 'run_id': 'demo.run', 'roots': [], 'nodes': {}}
    target = _add_valid_bare_reference(graph, 'demo.finding')
    graph['roots'].append({'target': target, 'role': 'output'})
    with pytest.raises(ValueError, match='root'):
        validate_graph(graph)


def test_source_finding_version_conflicts_and_missing_are_rejected() -> None:
    from packages.derivation.runner import SourceFact, _Run
    from tests.derivation.test_runner import RunnerFixture
    fixture = RunnerFixture()
    fixture.setUp()
    sources = [SourceFact('demo.one', '1', 'demo.same', finding_version='v1'),
               SourceFact('demo.two', '2', 'demo.same', finding_version='v2')]
    with pytest.raises(ValueError, match='conflicting source finding versions'):
        _Run(fixture.context(sources=sources), fixture.schemas)
    run = _Run(fixture.context(sources=[]), fixture.schemas)
    with pytest.raises(ValueError, match='missing source finding version'):
        run.source_finding_version('demo.missing')
    with pytest.raises(ValueError, match='missing derived finding version'):
        GraphBuilder({'demo.no-version': {'id': 'demo.no-version', 'pins': []}}).add_root('demo.no-version', role='output')


def test_replaced_live_sources_index_exact_versions_and_reject_conflicts() -> None:
    from packages.derivation.runner import SourceFact, _Run
    from tests.derivation.test_runner import RunnerFixture
    fixture = RunnerFixture()
    fixture.setUp()
    run = _Run(fixture.context(sources=[]), fixture.schemas)
    run.live_sources = [SourceFact('demo.member', '1', 'demo.asserted', finding_version='v1'),
                        SourceFact('demo.member', '2', 'demo.derived', finding_version='v2')]
    assert run.source_finding_version('demo.asserted') == 'v1'
    assert run.source_finding_version('demo.derived') == 'v2'
    original_sources = run.live_sources
    original_versions = run.source_finding_versions.copy()
    for invalid, message in [
        (SourceFact('demo.member', '2', 'demo.derived', finding_version='v1'),
         'conflicting source finding versions'),
        (SourceFact('demo.member', '3', 'demo.missing', finding_version=''),
         'missing source finding version'),
    ]:
        with pytest.raises(ValueError, match=message):
            run.live_sources = [SourceFact('demo.member', '4', 'demo.new', finding_version='v1'), invalid]
        assert run.live_sources is original_sources
        assert run.source_finding_versions == original_versions
    with pytest.raises(ValueError, match='missing source finding version'):
        run.source_finding_version('demo.new')
    run.live_sources = [*original_sources,
                        SourceFact('demo.member', '4', 'demo.new', finding_version='v2')]
    assert run.source_finding_version('demo.new') == 'v2'


def test_collected_attachment_rows_and_pairing_preserve_finding_versions() -> None:
    from packages.derivation.pairing_dispatch import PairingPublish, evaluate_pairing_scoped_rule
    from packages.derivation.runner import SourceFact, _Run
    from tests.derivation.test_runner import RunnerFixture
    fixture = RunnerFixture()
    fixture.setUp()
    sources = [SourceFact('demo.member', '1', 'demo.asserted', finding_version='v1'),
               SourceFact('demo.member', '2', 'demo.derived', finding_version='v2')]
    run = _Run(fixture.context(sources=sources), fixture.schemas)
    _, pins = run._collect_row_source({'op': 'collect_members', 'member_fact_type': {'id': 'demo.member'}})
    assert {(p['id'], p['version']) for p in pins} == {('demo.asserted', 'v1'), ('demo.derived', 'v2')}
    pairing = SourceFact('demo.pair', json.dumps({'left_fact_id':'demo.left.fact', 'right_fact_id':'demo.right.fact'}),
                         'demo.pair.finding', fact_id='demo.pair.fact', finding_version='v2')
    left = SourceFact('demo.left', '1', 'demo.left.finding', fact_id='demo.left.fact', finding_version='v1')
    right = SourceFact('demo.right', '2', 'demo.right.finding', fact_id='demo.right.fact', finding_version='v2')
    result = evaluate_pairing_scoped_rule(sources=[pairing, left, right], pairing_type='demo.pair',
        left_type='demo.left', right_type='demo.right', rule_id='demo.rule', rule_version='v1',
        symbol_for=lambda _: 'demo.output', evaluate_one=lambda _: PairingPublish('1'), schemas=fixture.schemas)
    assert {(p['id'], p['version']) for p in result.publications[0]['pins'] if p['role'] == 'input'} == {
        ('demo.pair.finding', 'v2'), ('demo.left.finding', 'v1'), ('demo.right.finding', 'v2')}


def test_new_publication_retains_exact_version_through_later_collect() -> None:
    from packages.derivation.evaluator import AccessLog
    from packages.derivation.runner import _Run
    from tests.derivation.test_runner import RunnerFixture
    fixture = RunnerFixture()
    fixture.setUp()
    run = _Run(fixture.context(sources=[]), fixture.schemas)
    run.use_v2 = True
    source = run.publish_symbol_finding(rule_id='demo.source.rule', symbol='demo.source', value='1',
        pins=[pin('demo.source.rule', 'computation')], source_name='demo.source', source_fact_id='demo.source.fact')
    access = AccessLog()
    access.collects.add('demo.source')
    dependencies = run.dependency_pins_for_access(access)
    assert dependencies == [{'role': 'input', 'id': source['id'], 'version': 'v2', 'origin': 'assertion'}]
    dependent = run.publish_symbol_finding(rule_id='demo.dependent.rule', symbol='demo.dependent', value='1',
        pins=[pin('demo.dependent.rule', 'computation'), *dependencies],
        source_name='demo.dependent', source_fact_id='demo.dependent.fact')
    builder = GraphBuilder({source['id']: source, dependent['id']: dependent})
    builder.add_root(dependent['id'], role='output')
    graph = builder.to_dict()
    edge = next(e for e in graph['nodes'][graph['roots'][0]['target']]['edges'] if e['pin']['role'] == 'input')
    assert edge['pin']['version'] == graph['nodes'][edge['target']]['version'] == 'v2'
    with pytest.raises(KeyError):
        run._append_live_source_from_finding({'id': 'demo.no-version', 'symbol': 'demo.no-version', 'value': '1'})
    wrong_pin = {'role': 'input', 'id': source['id'], 'version': 'v1', 'origin': 'assertion'}
    malformed = run.publish_symbol_finding(rule_id='demo.bad.rule', symbol='demo.bad', value='1',
        pins=[pin('demo.bad.rule', 'computation'), wrong_pin], source_name='demo.bad', source_fact_id='demo.bad.fact')
    assert wrong_pin in malformed['pins']
    with pytest.raises(ValueError):
        GraphBuilder({source['id']: source, malformed['id']: malformed}).add_root(malformed['id'], role='output')


def test_historical_mismatched_saved_graph_is_preserved_and_refused() -> None:
    import hashlib
    from pathlib import Path
    from packages.derivation.presentation_projection import PresentationModelError, validate_presentation_model
    path = Path('packages/sample_data/derivation/explanation_sharing/presentation-model.v2.json')
    assert hashlib.sha256(path.read_bytes()).hexdigest() == 'cdeab129beca7a5c7e347249c3116e8e5b8d38991529d4f13b68809f430163ca'
    with pytest.raises(PresentationModelError):
        validate_presentation_model(json.loads(path.read_text()))
