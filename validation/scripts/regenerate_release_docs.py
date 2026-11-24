#!/usr/bin/env python3
"""Recompute derived release documents from the package files.
Writes docs/ontology_metrics.csv, refreshes the label, definition, count, range and functional columns of
docs/class_dictionary.csv and docs/property_dictionary.csv, and writes
SHA256SUMS.txt last. Changes no ontology content."""
from pathlib import Path
import csv, hashlib, collections
from rdflib import Graph, URIRef, RDF, RDFS, OWL, SKOS
ROOT=Path(__file__).resolve().parents[2]
V='1.0.0-rc.2'
mods={'core':f'ontology/cdsg_core_v{V}.ttl','analytics':f'analytics/cdsg_analytics_v{V}.ttl','vocab':f'vocab/cdsg_vocab_v{V}.ttl','data':f'data/cdsg_data_v{V}.ttl','active_merged':f'data/cdsg_v{V}_active_merged.ttl'}
sha=lambda p: hashlib.sha256((ROOT/p).read_bytes()).hexdigest()
CDSG='https://w3id.org/cdsg/'
rows=[]
for m,f in mods.items():
    g=Graph().parse(ROOT/f)
    own=lambda t: set(x for x in g.subjects(RDF.type,t) if isinstance(x,URIRef) and str(x).startswith(CDSG))
    typed=set(s for s in g.subjects(RDF.type,None) if isinstance(s,URIRef) and '/resource/' in str(s))
    rows.append([m,Path(f).name,len(g),len(own(OWL.Class)),len(own(OWL.ObjectProperty)),len(own(OWL.DatatypeProperty)),len(set(g.subjects(RDF.type,OWL.Ontology))),len(typed),len(set(g.subjects(RDF.type,SKOS.Concept))),sha(f)])
    if m=='active_merged': merged=g
with open(ROOT/'docs/ontology_metrics.csv','w',newline='',encoding='utf-8') as fh:
    w=csv.writer(fh); w.writerow(['module','file','triples','cdsg_owl_classes','object_properties','datatype_properties','ontologies','resource_individuals','skos_concepts','sha256']); w.writerows(rows)
def short(u):
    return str(u)
def refresh(path,key,updates):
    p=ROOT/path
    with open(p,encoding='utf-8') as fh: rs=list(csv.DictReader(fh)); fields=rs[0].keys() if rs else []
    for r in rs: updates(r)
    with open(p,'w',newline='',encoding='utf-8') as fh:
        w=csv.DictWriter(fh,fieldnames=list(fields)); w.writeheader(); w.writerows(rs)
inst=collections.Counter(o for o in merged.objects(None,RDF.type))
use=collections.Counter(p for _,p,_ in merged)
def _text(u,p):
    v=[x for x in merged.objects(u,p) if getattr(x,'language',None) in ('en',None)]
    return str(v[0]) if v else ''
def _common(r):
    u=URIRef(r['iri']); r['label']=(_text(u,RDFS.label) or r['label']) if '#' in r['iri'] else r['label']; r['definition']=_text(u,SKOS.definition) or r['definition']
def cls(r): _common(r); r['explicit_instance_count']=inst.get(URIRef(r['iri']),0)
def prop(r):
    _common(r); u=URIRef(r['iri']); r['usage_count']=use.get(u,0)
    r['functional']=('yes' if (u,RDF.type,OWL.FunctionalProperty) in merged else 'no')
    rg=list(merged.objects(u,RDFS.range))
    if rg and all(isinstance(x,URIRef) for x in rg): r['range']=';'.join(sorted(map(str,rg)))
refresh('docs/class_dictionary.csv','iri',cls)
refresh('docs/property_dictionary.csv','iri',prop)
files=sorted(p for p in ROOT.rglob('*') if p.is_file() and p.name!='SHA256SUMS.txt' and '.venv' not in p.parts and p.suffix!='.bak' and p.name!='robot.jar')
(ROOT/'SHA256SUMS.txt').write_text(''.join(f'{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.relative_to(ROOT).as_posix()}\n' for p in files),encoding='utf-8')
for r in rows: print(*r[:9])
print('checksummed files:',len(files))
