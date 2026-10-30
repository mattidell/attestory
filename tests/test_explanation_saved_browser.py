"""Saved graph survives recovery and browser navigation is lazy and bounded."""
from __future__ import annotations
import copy
import json
import subprocess
from pathlib import Path
from typing import Any
from tempfile import TemporaryDirectory
import pytest
from packages.derivation.live_session import _render_page
from packages.derivation.live_workspace import WorkspaceCapability
from packages.derivation.presentation_projection import PresentationModelError, validate_presentation_model
from tests.test_sli_line21_explanation_page import BROWSER

ROOT = Path(__file__).resolve().parents[1]
SAMPLE = ROOT / 'packages/sample_data/derivation/explanation_sharing/presentation-model.v2.json'
PAGE = ROOT / 'packages/presentation/pages/citation-walk.v1.html'


def test_saved_graph_recovery_and_bad_reference_refusal(tmp_path: Path) -> None:
    model = json.loads(SAMPLE.read_text())
    path = tmp_path / 'model.json'
    path.write_text(json.dumps(model))
    validate_presentation_model(json.loads(path.read_text()))
    assert _render_page(ROOT, WorkspaceCapability(tmp_path), path)
    graph = model['explanationGraph']
    root = graph['roots'][0]['target']
    assert graph['nodes'][root]['edges']
    bad = copy.deepcopy(model)
    bad['explanationGraph']['nodes'][root]['edges'][0]['target'] = 'demo.missing'
    path.write_text(json.dumps(bad))
    with pytest.raises(PresentationModelError):
        validate_presentation_model(bad)
    with pytest.raises(Exception):
        _render_page(ROOT, WorkspaceCapability(tmp_path), path)
    published = [s for s in model['sections'] if model['sectionRoots'][s['id']]['kind'] == 'published']
    pair = next((a, b) for a in published for b in published if a['id'] != b['id'] and a['resolved'].get('value') == b['resolved'].get('value') and a['resolved']['act']['finding']['id'] != b['resolved']['act']['finding']['id'])
    bad = copy.deepcopy(model)
    bad['sectionRoots'][pair[0]['id']]['root'] = bad['sectionRoots'][pair[1]['id']]['root']
    path.write_text(json.dumps(bad))
    with pytest.raises(Exception):
        _render_page(ROOT, WorkspaceCapability(tmp_path), path)
    bad = copy.deepcopy(model)
    bad['explanationGraph']['run_id'] = 'demo.other-run'
    path.write_text(json.dumps(bad))
    with pytest.raises(Exception):
        _render_page(ROOT, WorkspaceCapability(tmp_path), path)
    bad = copy.deepcopy(model)
    root = bad['explanationGraph']['roots'][0]['target']
    bad['explanationGraph']['nodes'][root]['edges'][0]['target'] = root
    path.write_text(json.dumps(bad))
    with pytest.raises(Exception):
        _render_page(ROOT, WorkspaceCapability(tmp_path), path)


@pytest.mark.skipif(BROWSER is None, reason='headless Chromium unavailable')
def test_actual_saved_graph_browser_reuse_and_contained_refusal() -> None:
    model = json.loads(SAMPLE.read_text())
    def render(data: dict[str, Any], script: str) -> str:
        assert BROWSER is not None
        page = PAGE.read_text().replace('__MODEL_JSON__', json.dumps(data).replace('</', '<\\/'))
        page = page.replace('</body>', '<script>' + script + '</script></body>')
        with TemporaryDirectory() as temp:
            path = Path(temp) / 'page.html'
            path.write_text(page)
            return subprocess.run([BROWSER, '--headless', '--disable-gpu', '--no-sandbox', '--dump-dom', path.as_uri()], check=True, capture_output=True, text=True, timeout=40).stdout
    script = '''
    const unit = document.getElementById("line-27a");
    const detail = unit.querySelector("details.shared-explanation");
    const initiallyEmpty = unit.querySelectorAll("[data-explanation-node]").length === 0;
    const rootKey = MODEL.explanationGraph.roots[MODEL.sectionRoots["line-27a"].root].target;
    const nodes = MODEL.explanationGraph.nodes;
    const queue = [[rootKey, []]], seen = new Set();
    let path = null;
    while (queue.length) {
      const [key, route] = queue.shift();
      if (seen.has(key)) continue;
      seen.add(key);
      if (nodes[key].id === "demo.cgd.t2.finding.wages") { path = route; break; }
      for (const edge of nodes[key].edges) queue.push([edge.target, route.concat(edge.target)]);
    }
    detail.open = true; detail.dispatchEvent(new Event("toggle"));
    let item = unit.querySelector("[data-explanation-node]");
    for (const target of path || []) {
      const button = [...item.children].find(x => x.dataset && x.dataset.explanationTarget === target);
      if (!button) break;
      button.dataset.clicked = "yes"; button.click(); item = button.nextElementSibling.firstElementChild;
    }
    const sourceReached = item && item.textContent.includes("demo.cgd.t2.finding.wages = 30000");
    const bounded = unit.querySelectorAll("[data-explanation-node]").length <= (path || []).length + 1;
    for (let i=0; i<1000 && !unit.querySelector("[data-explanation-reuse]"); i++) {
      const button = [...unit.querySelectorAll("details.shared-explanation button")].find(b => b.dataset.explanationTarget && !b.dataset.clicked);
      if (!button) break;
      button.dataset.clicked = "yes"; button.click();
    }
    const reuse = unit.querySelector("[data-explanation-reuse]");
    let focusCorrect = false;
    if (reuse) { reuse.click(); focusCorrect = document.activeElement.dataset.explanationNode === reuse.dataset.explanationReuse; }
    document.body.dataset.testResult = initiallyEmpty && sourceReached && bounded && focusCorrect ? "navigation-observed" : "navigation-missing";
    '''
    html = render(model, script)
    assert 'data-test-result="navigation-observed"' in html
    bad = copy.deepcopy(model)
    root_index = bad['sectionRoots']['line-27a']['root']
    root = bad['explanationGraph']['roots'][root_index]['target']
    bad['explanationGraph']['nodes'][root]['edges'][0]['target'] = 'demo.missing'
    html = render(bad, '''const unit=document.getElementById("line-27a"); document.body.dataset.refusal = unit.querySelector(".section-error") && !unit.querySelector(".line-value") && document.querySelector("#line-1a .line-value") ? "contained" : "missing";''')
    assert 'data-refusal="contained"' in html


@pytest.mark.live
def test_real_blocked_saved_model_retains_actual_disposition_dependencies(tmp_path: Path) -> None:
    from packages.derivation.live import live_coordinate_run
    from tools.generate_capital_gain_distributions_line7a_t3_presentation_goldens import canonical_acts, _surface, SCOPE, USER
    acts = canonical_acts(components={'C1':'yes','C2':'yes','C3':'yes','C4':None})
    outcome = live_coordinate_run(WorkspaceCapability(tmp_path / 'L'), repo_root=ROOT,
        authoritative_acts=acts, workspace_revision=len(acts), run_scope=SCOPE,
        scope_user=USER, request={'schema':'run-request.v1'}, run_id='demo.cgd.t3.missing-authority',
        governance_pins=[], surface=_surface(), output_name='out.json')
    assert outcome.refusal is None and outcome.presentation_path is not None and outcome.output_path is not None
    model = json.loads(outcome.presentation_path.read_text())
    report = json.loads(outcome.output_path.read_text())
    validate_presentation_model(model)
    section = next(s for s in model['sections'] if s['id']=='line-7a')
    assert section['resolved']['disposition']=='blocked'
    root = model['sectionRoots']['line-7a']['root']
    node = model['dispositionNodes'][root]
    assert node['records'] and all(row in report['dispositions'] for row in node['records'])
    assert node['children']
    assert all(child in model['dispositionNodes'] for child in node['children'])
    from packages.derivation.records import RecordStream
    from packages.derivation.loader import DerivationSchemas
    from packages.derivation.production_resolver import resolve_production_package, ResolvedGraph
    from packages.derivation.explanation import walk_npe
    schemas = DerivationSchemas()
    records = list(RecordStream(tmp_path / 'L' / 'records', schemas).read().records)
    resolved = resolve_production_package(acts, run_scope=SCOPE, scope_user=USER, workspace_revision=len(acts), surface=_surface(), schemas=schemas)
    assert isinstance(resolved, ResolvedGraph)
    rules = [member for member in resolved.resolved_members if 'publishes' in member and 'requires' in member]
    pubs = {str(p.finding['id']): p.finding for p in (outcome.publications or ())}
    walk = walk_npe(run_id='demo.cgd.t3.missing-authority', symbol=root, rules=rules, records=records, derived=pubs)
    np = walk['nodes'][walk['root']]
    assert np['node_kind'] == 'blocked'
    assert np['code'] in section['resolved']['activeCodes']


def _provenance_mutation(model: dict[str, Any], start: str, mutation: str) -> dict[str, Any]:
    bad = copy.deepcopy(model)
    nodes = bad['explanationGraph']['nodes']
    stack = [start]
    visited: set[str] = set()
    while stack:
        key = stack.pop()
        if key in visited:
            continue
        visited.add(key)
        for edge in nodes[key]['edges']:
            if edge['pin']['role'] == 'parameter' and nodes[edge['target']]['kind'] == 'reference':
                target = nodes[edge['target']]
                if mutation == 'payload':
                    target['symbol'] = 'demo.fabricated'
                    target['value'] = '999'
                else:
                    alternate = f"derived:{len(target['id'])}:{target['id']}:{target['version']}"
                    nodes[alternate] = dict(target, kind='derived')
                    edge['target'] = alternate
                return bad
            stack.append(edge['target'])
    raise AssertionError('no parameter provenance reached')


def _assert_rejected_by_saved_loader(model: dict[str, Any], tmp_path: Path) -> None:
    from packages.derivation.live_session import PresentationSessionError
    path = tmp_path / 'mutated.json'
    path.write_text(json.dumps(model), encoding='utf-8')
    with pytest.raises(PresentationModelError):
        validate_presentation_model(model)
    with pytest.raises(PresentationSessionError, match='presentation-model-unavailable'):
        _render_page(ROOT, WorkspaceCapability(tmp_path), path)


def _assert_browser_refusal(model: dict[str, Any], section_id: str, tmp_path: Path) -> None:
    assert BROWSER is not None
    page = PAGE.read_text().replace('__MODEL_JSON__', json.dumps(model).replace('</', '<\\/'))
    script = f'''<script>const unit = document.getElementById({json.dumps(section_id)});
    document.body.dataset.guard = unit.querySelector('.section-error') && !unit.querySelector('.line-value') ? 'refused' : 'accepted';</script>'''
    page = page.replace('</body>', script + '</body>')
    path = tmp_path / 'mutated-page.html'
    path.write_text(page, encoding='utf-8')
    dom = subprocess.run([BROWSER, '--headless', '--disable-gpu', '--no-sandbox', '--dump-dom', path.as_uri()], check=True, capture_output=True, text=True, timeout=40).stdout
    assert 'data-guard="refused"' in dom


@pytest.mark.skipif(BROWSER is None, reason='headless Chromium unavailable')
@pytest.mark.parametrize('mutation', ['kind', 'payload'])
def test_published_provenance_mutation_refused(mutation: str, tmp_path: Path) -> None:
    model = json.loads(SAMPLE.read_text())
    index = model['sectionRoots']['line-27a']['root']
    start = model['explanationGraph']['roots'][index]['target']
    bad = _provenance_mutation(model, start, mutation)
    _assert_browser_refusal(bad, 'line-27a', tmp_path)
    _assert_rejected_by_saved_loader(bad, tmp_path)


@pytest.mark.live
@pytest.mark.skipif(BROWSER is None, reason='headless Chromium unavailable')
@pytest.mark.parametrize('mutation', ['kind', 'payload'])
def test_blocked_provenance_mutation_refused(mutation: str, tmp_path: Path) -> None:
    from packages.derivation.live import live_coordinate_run
    from tools.generate_capital_gain_distributions_line7a_t3_presentation_goldens import canonical_acts, _surface, SCOPE, USER
    acts = canonical_acts(components={'C1':'yes','C2':'yes','C3':'yes','C4':None})
    outcome = live_coordinate_run(WorkspaceCapability(tmp_path / 'L'), repo_root=ROOT,
        authoritative_acts=acts, workspace_revision=len(acts), run_scope=SCOPE,
        scope_user=USER, request={'schema':'run-request.v1'}, run_id='demo.cgd.t3.missing-authority',
        governance_pins=[], surface=_surface(), output_name='out.json')
    assert outcome.refusal is None and outcome.presentation_path is not None
    model = json.loads(outcome.presentation_path.read_text())
    stack = [model['sectionRoots']['line-15']['root']]
    seen: set[str] = set()
    bad = None
    while stack:
        key = stack.pop()
        if key in seen:
            continue
        seen.add(key)
        node = model['dispositionNodes'][key]
        if 'findingRoot' in node:
            try:
                bad = _provenance_mutation(model, node['findingRoot'], mutation)
                break
            except AssertionError:
                pass
        stack.extend(node['children'])
    assert bad is not None
    _assert_browser_refusal(bad, 'line-15', tmp_path)
    _assert_rejected_by_saved_loader(bad, tmp_path)
