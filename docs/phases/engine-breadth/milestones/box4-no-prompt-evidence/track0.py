"""Track 0 on the unchanged P0 scratch core, through real live coordination.

Run: python3 <this-file> --core "$B4N_SCRATCH/core.json" --part "$B4N_SCRATCH/replay-part.json"
Only synthetic demo.* inputs and evidence outputs; no content mutations.
"""
from __future__ import annotations
import argparse
import copy
from collections import Counter
import hashlib
import importlib.util
import json
import multiprocessing
import os
from pathlib import Path
import re
import sys
import tempfile
import time

HERE=Path(__file__).resolve().parent
REPO=HERE.parents[4]
sys.path.insert(0,str(REPO))
P='tax.us.2025.'
AMOUNT=P+'f1099b.statement-box4-withholding'
REPORTED=P+'f1099b.statement-box4-withholding-reported'
PRESENT=P+'f1099b.no-sale-box4-present'
WATCH=('25b','25d','33','37')

def load(name,path):
    if name not in sys.modules:
        spec=importlib.util.spec_from_file_location(name,path)
        m=importlib.util.module_from_spec(spec);sys.modules[name]=m;spec.loader.exec_module(m)
    return sys.modules[name]

def p0():return load('b4n_t0_p0',HERE/'probe.py')

def mods():
    b=p0().old();h,_=b._mods()
    return b,h

def write(name,body):p0().write(HERE/name,body)

def make(answers,*,status='single',kind='covered',term='st',repeated=1,present='no',level=None):
    b,h=mods()
    acts=h.opened()
    n=repeated if repeated>1 else len(answers)
    for i in range(n):
        acts=h.sale(acts,kind,term,proceeds=5000+i*1000,basis=4000+i*1000,
                    tag=f'b4nt0.s{i}',wash=0)
    if repeated>1:
        # Join the input identities before admission: distinct transactions,
        # one broker/statement. Keep each genuine family transition intact.
        text=json.dumps(acts)
        for i in range(1,n):
            for name in ('broker','statement'):
                text=text.replace(f'demo.sfa.b4nt0.s{i}.{name}',f'demo.sfa.b4nt0.s0.{name}')
        acts=json.loads(text);seen=set();kept=[]
        for a in acts:
            entity=(a.get('payload')or{}).get('entity')or{}
            if a['kind']=='entity-introduced':
                if entity['id'] in seen:continue
                seen.add(entity['id'])
            kept.append(a)
        acts=h.renumber(kept)
    honest=h.honest({kind} if n else set());honest.update(h.honest_exception1(acts))
    acts=h.answer(acts,**{k:v for k,v in honest.items() if v is not None})
    acts=b.strip_fact(acts,REPORTED)
    for i,(answer,amount) in enumerate(answers):
        stmt=f'demo.sfa.b4nt0.s{i}.statement'
        acts=b.say_stmt(acts,b.BOX7,stmt,'no','t0.box7')
        if answer is not None:acts=b.say_stmt(acts,REPORTED,stmt,answer,'t0.reported')
        if amount is not None:acts=b.say_stmt(acts,AMOUNT,stmt,amount,'t0.amount')
    acts=h.say(acts,PRESENT,present,'t0.present') if present is not None else h.strip(acts,PRESENT)
    if level is not None:acts=h.say(acts,b.RETURN_AMT,level,'t0.level')
    spouse_fact=P+'standard-deduction.spouse-separate-condition'
    if spouse_fact not in h._adopted(acts):
        h._add(acts,'bundle-adoption',{'bundle':json.loads((h.CONTENT/'core_calculations.bundle.v4.json').read_text())})
    for fact,value in (('filing-status',status),('taxpayer-over-65',False),('taxpayer-blind',False),
                       ('spouse-over-65',False),('spouse-blind',False),('mfs-lived-apart-all-year','yes'),
                       ('standard-deduction.spouse-separate-condition',True)):
        acts=h.say(acts,P+fact,value,'t0.'+fact)
    return h.renumber(acts)

def matrix():
    rows=[]
    def add(ident,item,answers,expect,**kwargs):
        rows.append({'id':ident,'item':item,'answers':answers,'expected_25b':expect,
                     'acts':make(answers,**kwargs)})
    shapes=[('no-yes-amount',[('no',None),('yes',200)],200),
            ('no-unanswered',[('no',None),(None,None)],'blocked'),
            ('no-yes-absent',[('no',None),('yes',None)],'blocked'),
            ('no-no',[('no',None),('no',None)],0),
            ('no-yes-amount-no',[('no',None),('yes',200),('no',None)],200),
            ('no-yes-amount-unanswered',[('no',None),('yes',200),(None,None)],'blocked'),
            ('no-yes-absent-no',[('no',None),('yes',None),('no',None)],'blocked'),
            ('three-no',[('no',None)]*3,0)]
    for name,answers,expect in shapes:
        add('local.'+name,1,answers,expect)
        if answers!=list(reversed(answers)):
            add('local.reverse-'+name,1,list(reversed(answers)),expect)
    for n in (2,3):
        for answer,amount in (('no',None),('yes',200)):
            add(f'repeated.{n}.{answer}',2,[(answer,amount)],amount or 0,repeated=n)
    for answer,amount in (('no',0),('no',200),('yes',0)):
        add(f'contradiction.{answer}.{amount}',3,[(answer,amount)],amount)
    for kind in ('covered','w','noncovered','codeb'):
        for term in ('st','lt'):
            add(f'type.{kind}.{term}',5,[('no',None)],0,kind=kind,term=term)
    for name,answers,present,level in (
        ('no-return-unanswered',[('no',None)],None,None),
        ('three-no-return-unanswered',[('no',None)]*3,None,None),
        ('no-return-yes-no-amount',[('no',None)],'yes',None),
        ('mixed-amount-needed-return-no',[('no',None),('yes',None)],'no',None),
        ('mixed-unanswered-return-unanswered',[('no',None),(None,None)],None,None)):
        add('next.'+name,6,answers,'blocked',present=present,level=level)
    for status in p0().STATUSES:
        for name,answers in (('no-1099b',[]),('sale-yes-200',[('yes',200)]),('sale-no-zero',[('no',0)])):
            add('neighbour.'+status+'.'+name,7,answers,200 if name=='sale-yes-200' else 0,status=status)
    return rows

def field_views(model):
    return {s['field']['id']:{'disposition':s.get('resolved',{}).get('disposition'),
              'value':s.get('resolved',{}).get('value'),
              'sentences':[r.get('sentence') for r in s.get('resolved',{}).get('reasons',[]) if 'sentence' in r]}
            for s in model.get('sections',[])}

def run(acts,core,ident,*,capture=False):
    from tools.recorded_replay import resolve_core
    core=resolve_core(core);b,h=mods();surface=core.surface()
    with h.loader_entries(core):
        finished=h._handover(h._finish(copy.deepcopy(acts),package_path=core.package_path,package_version=core.version,
            release_path=core.release_path,release_version=core.release_version,note='demo.b4nt0.'+ident),surface=surface,reconfirm=True)
        with tempfile.TemporaryDirectory() as tmp:
            outcome=h.live_coordinate_run(h.WorkspaceCapability(Path(tmp)/'L'),repo_root=REPO,authoritative_acts=finished,
                workspace_revision=len(finished),run_scope={'jurisdiction':'us','year':h.YEAR},scope_user=h.ccr.USER,
                request={'schema':'run-request.v1'},run_id='demo.b4nt0.'+core.version+'.'+ident,
                governance_pins=[],surface=surface,output_name='out.json')
            if outcome.refusal:return {'outcome':'refused','reason':outcome.refusal.reason}
            model=json.loads(outcome.presentation_path.read_text());report=json.loads(outcome.output_path.read_text())
            pubs=[copy.deepcopy(p.finding) for p in outcome.publications or ()]
    fields=field_views(model);watch={k:fields[P+'form1040.line-'+k] for k in WATCH}
    rows={r['artifact_id']:r for r in report.get('dispositions',[]) if r['artifact_id'] in
          {P+'rule.form1040-line'+k for k in WATCH}}
    prompt=json.loads((b.CONTENT/'input-question.f1099b-box4.v1.json').read_text())['question']
    result={'outcome':'success','lines':watch,
            'rows':{k:{x:r.get(x) for x in ('disposition','code','missing')} for k,r in rows.items()},
            'page_has_amount_prompt':any(prompt in f['sentences'] for f in fields.values()),
            'fields':fields}
    if capture:result.update(finished=finished,publications=pubs)
    return result

def worker(payload):
    row,core=payload
    try:
        result=run(row['acts'],core,row['id'])
        if result['outcome']=='success':
            actual=result['lines']['25b'];expected=row['expected_25b']
            passed=actual['disposition']=='blocked' if expected=='blocked' else actual['value']==expected and actual['disposition']!='blocked'
            if expected=='blocked' and row['item']==1:
                blocked=result['rows'][P+'rule.form1040-line25b']
                passed &= blocked['code']=='DEPENDENCY_ABSENT' and AMOUNT in (blocked['missing'] or [])
            if expected!='blocked':passed &= result['lines']['25d']['value']==4500+expected
            if row['item']==7:
                before=run(row['acts'],'v93',row['id']+'.baseline')
                changes={k:{'v93':before['fields'].get(k),'successor':result['fields'].get(k)}
                         for k in set(before.get('fields',{}))|set(result['fields']) if before.get('fields',{}).get(k)!=result['fields'].get(k)}
                passed &= before['outcome']=='success' and not changes
                passed &= result['lines']['33']['disposition']!='blocked' and result['lines']['37']['disposition']!='blocked'
                result['baseline_fields']=before.get('fields');result['field_differences']=changes
            result['pass']=bool(passed)
        else:result['pass']=False
        # Full page fields are required for neighbours only. All four watched
        # fields retain every raw reason sentence in every other case.
        if row['item']!=7:result.pop('fields',None)
        return {**{k:v for k,v in row.items() if k!='acts'},**result}
    except Exception as exc:
        return {'id':row['id'],'item':row['item'],'pass':False,'outcome':'error','error':type(exc).__name__,
                'message':re.sub(r'/(?:Users|private|tmp|var)/\S+','<path>',str(exc))[:700]}

def dependency_ids(finding,pubs):
    found=set();pending=[finding['id']]
    by_id={p['id']:p for p in pubs}
    while pending:
        current=pending.pop()
        for pin in by_id.get(current,{}).get('pins',[]):
            if pin['role'] not in ('input','choice') or pin['id'] in found:continue
            found.add(pin['id']);pending.append(pin['id'])
    return found

def lifecycle(core):
    from tools.recorded_replay import resolve_core
    from packages.derivation.loader import DerivationSchemas
    from packages.derivation.projection import workspace_currency
    from packages.tax import loader
    b,h=mods();core=resolve_core(core)
    initial=make([('no',None)])
    before=run(initial,core,'lifecycle.before',capture=True)
    no=next(a['payload']['finding'] for a in initial if a['kind']=='assertion' and a['payload']['finding']['fact_id'].startswith(REPORTED+'|'))
    pubs=before['publications'];old={k:next(p for p in pubs if p['symbol']==P+'payments.line'+k) for k in ('25b','25d')}
    history=copy.deepcopy(before['finished'])
    for pub in pubs:h._add(history,'derived-publication',{'run_id':'demo.b4nt0.lifecycle.before','finding':pub})
    registry=DerivationSchemas().registry
    loader.install_domain_companion_presence(registry);loader.install_domain_companion_equalities(registry)
    loader.install_domain_declaration_signal_contradictions(registry)
    scenarios=[]
    for name in ('correct-no-to-yes','withdraw-no','amount-after-no'):
        acts=copy.deepcopy(initial);hist=copy.deepcopy(history)
        if name=='correct-no-to-yes':
            payload={'finding':h._attested('demo.b4nt0.corrected-yes',no['fact_id'],'yes')};kind='assertion'
        elif name=='withdraw-no':payload={'finding_id':no['id']};kind='finding-retracted'
        else:
            acts=b.say_stmt(acts,AMOUNT,'demo.sfa.b4nt0.s0.statement',200,'t0.later-amount')
            payload=copy.deepcopy(acts[-1]['payload']);kind='assertion'
        if name!='amount-after-no':h._add(acts,kind,payload)
        if name=='amount-after-no':
            for a in acts[len(initial):]:h._add(hist,a['kind'],copy.deepcopy(a['payload']))
        else:h._add(hist,kind,payload)
        acts=h.renumber(acts);hist=h.renumber(hist)
        with h.loader_entries(core):
            kernel,derived=workspace_currency(tuple(hist),registry)
        after=run(acts,core,'lifecycle.'+name,capture=True)
        expected=200 if name=='amount-after-no' else 'blocked'
        passed=after['outcome']=='success' and (after['lines']['25b']['value']==expected if isinstance(expected,int)
                  else after['lines']['25b']['disposition']=='blocked' and after['page_has_amount_prompt'])
        source_pinned=all(no['id'] in dependency_ids(p,pubs) for p in old.values())
        old_displaced={k:p['id'] in derived.displaced_derived_ids for k,p in old.items()}
        if name!='amount-after-no':passed &= source_pinned and all(old_displaced.values()) and no['id'] in kernel.displaced_finding_ids
        after_pubs=after['publications'];new25=next((p for p in after_pubs if p['symbol']==P+'payments.line25b'),None)
        if name=='amount-after-no':passed &= new25 is not None and payload['finding']['id'] in dependency_ids(new25,after_pubs)
        if name=='withdraw-no':
            baseline=run(acts,'v93','lifecycle.withdraw.baseline')
            passed &= after['fields']==baseline['fields']
        scenarios.append({'id':name,'pass':bool(passed),'before_source':no['id'],'before_source_pinned':source_pinned,
            'source_current_after':no['id'] in kernel.current_finding_ids,'old_payment_publications_displaced':old_displaced,
            'old_payment_finding_ids':{k:p['id'] for k,p in old.items()},
            'displacement_reasons':{k:[{'kind':x.kind,'by':x.by} for x in derived.reasons.get(p['id'],())] for k,p in old.items()},
            'after_lines':after['lines'],'after_rows':after['rows'],'page_has_amount_prompt':after['page_has_amount_prompt'],
            'after_payment_finding_id':new25['id'] if new25 else None,
            'new_amount_pinned':payload.get('finding',{}).get('id') in dependency_ids(new25,after_pubs) if new25 and name=='amount-after-no' else None})
    return scenarios

def addition_control():
    """Observe the amount-addition currency boundary on published v93 too."""
    from packages.derivation.loader import DerivationSchemas
    from packages.derivation.projection import workspace_currency
    from packages.tax import loader
    b,h=mods();initial=make([])
    before=run(initial,'v93','addition-control.before',capture=True)
    acts=b.introduce(copy.deepcopy(initial),'b4nt0.control')
    acts=b.say_stmt(acts,AMOUNT,'demo.sfa.b4nt0.control.statement',200,'t0.control-amount')
    after=run(acts,'v93','addition-control.after',capture=True)
    history=copy.deepcopy(before['finished'])
    for pub in before['publications']:
        h._add(history,'derived-publication',{'run_id':'demo.b4nt0.addition-control.before','finding':pub})
    for a in acts[len(initial):]:h._add(history,a['kind'],copy.deepcopy(a['payload']))
    registry=DerivationSchemas().registry
    loader.install_domain_companion_presence(registry);loader.install_domain_companion_equalities(registry)
    loader.install_domain_declaration_signal_contradictions(registry)
    _kernel,derived=workspace_currency(tuple(h.renumber(history)),registry)
    old={k:next(p for p in before['publications'] if p['symbol']==P+'payments.line'+k) for k in ('25b','25d')}
    return {'core':'v93','before_lines':before['lines'],'after_lines':after['lines'],
            'old_payment_finding_ids':{k:p['id'] for k,p in old.items()},
            'old_payment_publications_displaced':{k:p['id'] in derived.displaced_derived_ids for k,p in old.items()},
            'observation':'Adding a new amount while leaving earlier source findings unchanged does not displace the previous zero payment publications on v93 either. Both cores recompute the new page correctly. This is not evidence that amount additions invalidate old results.'}


def replay_reuse(core,part):
    from tools.recorded_replay import resolve_core,core_fingerprint
    started=time.monotonic();saved=json.loads(part.read_text())
    expected=[core_fingerprint(resolve_core('v93')),core_fingerprint(resolve_core(core))]
    assert saved['_metadata']['cores']==expected,'saved replay fingerprint mismatch'
    prototype=load('b4n_t0_approved_prototype',HERE/'prototype.py')
    adopted=resolve_core(core)
    content_hashes={}
    for filename,body,_role in prototype.artifacts():
        actual=(adopted.content/filename).read_bytes()
        assert actual==(json.dumps(body,indent=2)+'\n').encode(),'P0 content bytes differ: '+filename
        content_hashes[filename]=hashlib.sha256(actual).hexdigest()
    recorded=json.loads((HERE/'classification-output.json').read_text())
    assert set(saved['results'])==set(recorded['results']) and len(saved['results'])==775
    result={'reused':True,'new_live_runs':0,'wall_time_s':round(time.monotonic()-started,3),
            'part_sha256':hashlib.sha256(part.read_bytes()).hexdigest(),'cores':expected,
            'counts':dict(Counter(r['class'] for r in saved['results'].values())),
            'p0_classification':recorded['counts'],'content_bytes_changed':False,'p0_content_hashes':content_hashes}
    write('track0-replay.json',result);return result

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--core',type=Path,required=True)
    parser.add_argument('--part',type=Path);parser.add_argument('--smoke',action='store_true');parser.add_argument('--lifecycle-only',action='store_true');parser.add_argument('--addition-control',action='store_true');parser.add_argument('--wording-base',action='store_true');parser.add_argument('--neighbours-only',action='store_true')
    args=parser.parse_args();start=time.monotonic()
    if not args.neighbours_only:
        if args.part is None:parser.error('--part is required outside neighbours-only mode')
        replay_reuse(args.core,args.part)
    if args.wording_base:
        started=time.monotonic();ident='local.no-yes-amount-unanswered'
        row=next(r for r in matrix() if r['id']==ident)
        before=run(row['acts'],'v93',ident+'.wording-base')
        saved=json.loads((HERE/'track0-matrix.json').read_text())
        after=next(r for r in saved['cases'] if r['id']==ident)
        write('track0-wording-base.json',{'case':ident,'baseline':'published v93',
            'baseline_lines':before['lines'],'successor_lines':after['lines'],
            'four_lines_identical':before['lines']==after['lines'],
            'wall_time_s':round(time.monotonic()-started,3)})
        print('Wording witness matches v93:',before['lines']==after['lines'],flush=True)
        return
    if args.addition_control:
        started=time.monotonic();control=addition_control()
        control['wall_time_s']=round(time.monotonic()-started,3)
        write('track0-addition-control.json',control)
        print(json.dumps(control,indent=2),flush=True)
        return
    if args.lifecycle_only:
        started=time.monotonic();traces=lifecycle(args.core)
        write('track0-lifecycle.json',{'wall_time_s':round(time.monotonic()-started,3),'traces':traces})
        print('Lifecycle:',[(r['id'],r['pass']) for r in traces],flush=True)
        return
    rows=matrix()
    if args.neighbours_only:rows=[r for r in rows if r['item']==7]
    if args.smoke:rows=[rows[0],next(r for r in rows if r['id']=='repeated.3.yes'),next(r for r in rows if r['id']=='type.codeb.lt'),rows[-1]]
    from tests import evidence_loader
    owner=evidence_loader.current_owner()
    if owner:evidence_loader.release(owner)
    workers=max(1,(os.cpu_count() or 2)-1)
    with multiprocessing.get_context('spawn').Pool(workers) as pool:
        results=pool.map(worker,[(r,str(args.core)) for r in rows])
    write('track1-neighbours.json' if args.neighbours_only else 'track0-smoke.json' if args.smoke else 'track0-matrix.json',{'workers':workers,'wall_time_s':round(time.monotonic()-start,3),'cases':results})
    print(json.dumps({'cases':len(results),'passes':sum(r['pass'] for r in results),
          'fails':[{k:v for k,v in r.items() if k in ('id','error','message','outcome')} for r in results if not r['pass']]},indent=2),flush=True)
    if not args.smoke and not args.neighbours_only:
        started=time.monotonic();traces=lifecycle(args.core)
        write('track0-lifecycle.json',{'wall_time_s':round(time.monotonic()-started,3),'traces':traces})
        print('Lifecycle:',[(r['id'],r['pass']) for r in traces],flush=True)

if __name__=='__main__':main()
