#!/usr/bin/env python3
"""Run the CDSG competency questions.
Each CQ is checked twice. The expectation check compares the result with values fixed from the
source analysis before the query was run (validation/expected/cq_expected.json, "expected"):
row count and the rows that must appear. The regression check compares the normalized result
with its stored SHA-256 digest, so that later changes to the model or data that alter an
answer are noticed.
Queries whose first line is '# entailment: hermit' run over the merged graph plus the HermiT
class assertions written by validation/run_robot_release_gate.sh; all others run over the
asserted merged graph only (RDFLib, no entailment regime).
--write stores the current digests and writes validation/cq_results/*.csv; it keeps the expectations."""
from pathlib import Path
from rdflib import Graph, URIRef, BNode, Literal
import json, hashlib, sys, csv
ROOT=Path(__file__).resolve().parents[2]
WRITE='--write' in sys.argv
asserted=Graph().parse(ROOT/'data/cdsg_v1.0.0-rc.2_active_merged.ttl',format='turtle')
entailed=Graph()
for t in asserted: entailed.add(t)
inf=ROOT/'validation/results/merged-inferred-class-assertions.ttl'
if inf.exists(): entailed.parse(inf)
def termstr(x):
    if x is None: return ''
    if isinstance(x,URIRef): return f'<{x}>'
    if isinstance(x,BNode): return '_:bnode'
    if isinstance(x,Literal):
        b=str(x).replace('\\','\\\\').replace('\t','\\t').replace('\n','\\n').replace('\r','\\r')
        if x.language: return f'"{b}"@{x.language}'
        if x.datatype: return f'"{b}"^^<{x.datatype}>'
        return f'"{b}"'
    return str(x)
expf=ROOT/'validation/expected/cq_expected.json'
spec=json.loads(expf.read_text(encoding='utf-8'))
failed=0
for qf in sorted((ROOT/'validation/queries').glob('CQ*.rq')):
    text=qf.read_text(encoding='utf-8')
    ent=text.splitlines()[0].strip()=='# entailment: hermit'
    if ent and not inf.exists(): print('SKIP',qf.stem,'needs results/merged-inferred-class-assertions.ttl'); failed+=1; continue
    g=entailed if ent else asserted
    res=g.query(text); vars_=[str(v) for v in res.vars]
    raw=[[('' if v is None else str(v)) for v in row] for row in res]
    rows=[[termstr(v) for v in row] for row in g.query(text)]
    norm='\n'.join(['\t'.join(vars_)]+sorted('\t'.join(r) for r in rows))+'\n'
    h=hashlib.sha256(norm.encode()).hexdigest()
    noent=len(list(asserted.query(text))) if ent else None
    s=spec.setdefault(qf.stem,{}); e=s.get('expected',{})
    problems=[]
    if e.get('rows') is not None and len(rows)!=e['rows']: problems.append(f"rows {len(rows)} != expected {e['rows']}")
    if ent and e.get('rows_without_entailment') is not None and noent!=e['rows_without_entailment']: problems.append(f"rows without entailment {noent} != {e['rows_without_entailment']}")
    for c in e.get('checks',[]):
        idx={v:i for i,v in enumerate(vars_)}
        hit=[r for r in raw if all((r[idx[k]]!="") if v=="*" else r[idx[k]].endswith(v) for k,v in c.get("where",{}).items())]
        if len(hit)!=c['rows']: problems.append(f"{c} matched {len(hit)}")
        for k,v in c.get('equals',{}).items():
            if any(r[idx[k]]!=v for r in hit): problems.append(f"{c}: {k} differs")
    if WRITE:
        s['regression']={'rows':len(rows),'normalized_sha256':h,'variables':vars_,'entailment':'hermit' if ent else 'none'}
        with open(ROOT/f'validation/cq_results/{qf.stem}.csv','w',newline='',encoding='utf-8') as fh:
            w=csv.writer(fh); w.writerow(vars_); w.writerows(raw)
    reg=s.get('regression',{}); regok=reg.get('normalized_sha256')==h
    print(('PASS' if not problems else 'FAIL'),qf.stem,'expectation;',('PASS' if regok else 'FAIL'),'regression; rows=',len(rows),
          ('(without entailment: %d)'%noent) if ent else '', 'sha256=',h)
    for p in problems: print('   ',p)
    failed+=bool(problems)+(not regok)
if WRITE: expf.write_text(json.dumps(spec,indent=2,ensure_ascii=False),encoding='utf-8')
sys.exit(1 if failed else 0)
