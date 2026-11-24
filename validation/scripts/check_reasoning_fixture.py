#!/usr/bin/env python3
"""Check HermiT outputs written by validation/run_robot_release_gate.sh.
Positive fixture (IT), non-entailment (NT) and checks over the evidence set (DS)."""
from pathlib import Path
import sys, json
from rdflib import Graph, URIRef, RDF, RDFS, OWL
ROOT=Path(__file__).resolve().parents[2]
C='https://w3id.org/cdsg/core#'; A='https://w3id.org/cdsg/analytics#'; G='http://purl.org/nemo/gufo#'; T='https://w3id.org/cdsg/test/'
fx=Graph().parse(ROOT/'validation/results/positive-fixture-inferred.ttl')
mi=Graph().parse(ROOT/'validation/results/merged-inferred-class-assertions.ttl')
asserted=Graph().parse(ROOT/'data/cdsg_v1.0.0-rc.2_active_merged.ttl')
fail=0
def check(tid,ok,msg):
    global fail; fail+=not ok; print('PASS' if ok else 'FAIL',tid,msg)
for tid,i,cl,exp in [('IT01','org1',C+'DocumentIssuerRole',True),('IT02','post1',C+'DocumentPublisherRole',True),
                     ('IT03','cat1',C+'NormativelyDefinedPolicyTargetCategory',True),
                     ('IT05a','cat2',C+'NormativelyDefinedPolicyTargetCategory',True),('IT05b','cat2',C+'SourceSpecifiedPolicyTargetCategory',True),
                     ('IT05c','cat2',G+'RoleMixin',True),('NT03','post1',C+'Organization',False),('IT06','bearer1',G+'Endurant',True),('NT06','bearer1',C+'PolicyTargetRole',False)]:
    got=(URIRef(T+i),RDF.type,URIRef(cl)) in fx
    check(tid,got==exp,f'{i} a {cl.split("#")[-1]} expected {exp} got {got}')
# DS: classification of the evidence set
exp=json.loads((ROOT/'validation/expected/source_category_asserted_types_rc1.json').read_text())
lep='https://w3id.org/cdsg/resource/target/source/category-'
ok=0; bad=[]
for cat,types in exp.items():
    for t in types:
        if (URIRef(cat),RDF.type,URIRef(C+t)) in mi: ok+=1
        else: bad.append((cat,t))
check('DS01',not bad,f'{ok} subtype assertions of rc.1 reproduced by inference from statement links alone; missing {len(bad)}')
src=set(s for s in mi.subjects(RDF.type,URIRef(C+'SourceSpecifiedPolicyTargetCategory')))
asrt=set(s for s in asserted.subjects(RDF.type,URIRef(C+'SourceSpecifiedPolicyTargetCategory')))
check('DS02',len(src)>=18 and not asrt,f'{len(src)} categories inferred source-specified; {len(asrt)} asserted')
rm=set(s for s in mi.subjects(RDF.type,URIRef(G+'RoleMixin')))
check('DS03',src<=rm,f'all {len(src)} source-specified categories inferred gufo:RoleMixin')
cur=set(asserted.subjects(RDF.type,URIRef(A+'CuratedPolicyTargetCategory')))
mx=set(s for s in mi.subjects(RDF.type,URIRef(G+'Mixin')))
check('DS04',cur<=mx,f'all {len(cur)} curated categories inferred gufo:Mixin')
check('NT04',not (src & cur),f'no category is both curated and source-specified after reasoning ({len(src&cur)})')
sys.exit(1 if fail else 0)
