#!/usr/bin/env python3
from pathlib import Path
from rdflib import Graph, Namespace, URIRef, Literal, RDF, RDFS, OWL, SKOS, DCTERMS
from rdflib.compare import isomorphic
from collections import defaultdict
ROOT=Path(__file__).resolve().parents[2]
CORE=Namespace('https://w3id.org/cdsg/core#'); OBS=Namespace('https://w3id.org/cdsg/observation#'); ANA=Namespace('https://w3id.org/cdsg/analytics#'); GUFO=Namespace('http://purl.org/nemo/gufo#')
mods=[ROOT/'ontology/cdsg_core_v1.0.0-rc.2.ttl',ROOT/'analytics/cdsg_analytics_v1.0.0-rc.2.ttl',ROOT/'vocab/cdsg_vocab_v1.0.0-rc.2.ttl',ROOT/'data/cdsg_data_v1.0.0-rc.2.ttl']
errors=[]; warns=[]; gs=[]
for p in mods:
    g=Graph(); g.parse(p,format='turtle'); gs.append(g)
    onts=list(g.subjects(RDF.type,OWL.Ontology))
    if len(onts)!=1: errors.append(f'{p.name}: ontology declarations={len(onts)}')
    for o in onts:
        vis=[str(x) for x in g.objects(o,OWL.versionIRI)]
        if not vis or not all('1.0.0-rc.2' in x for x in vis): errors.append(f'{p.name}: versionIRI={vis}')
        for imp in g.objects(o,OWL.imports):
            si=str(imp)
            if 'w3id.org/cdsg/' in si and '/1.0.0-rc.2' not in si: errors.append(f'{p.name}: stale internal import {si}')
# merged graph isomorphic to the module union minus internal owl:imports.
# An RDF union of the five module documents cannot keep its internal owl:imports
# and still load as one OWL document: OWLAPI resolves each import through the
# catalog and then rejects the load, because the merged document already carries
# those ontology IRIs. The external gUFO import is kept and is checked below.
union=Graph()
for g in gs:
    for t in g: union.add(t)
expected_active=Graph()
for t in union:
    if t[1]==OWL.imports and str(t[2]).startswith('https://w3id.org/cdsg/'): continue
    expected_active.add(t)
merged=Graph().parse(ROOT/'data/cdsg_v1.0.0-rc.2_active_merged.ttl',format='turtle')
if not isomorphic(expected_active,merged): errors.append('active merged graph is not isomorphic to the module union minus internal owl:imports')
if any(str(o).startswith('https://w3id.org/cdsg/') for o in merged.objects(None,OWL.imports)): errors.append('active merged graph still carries an internal owl:imports triple')
if URIRef('http://purl.org/nemo/gufo#') not in set(merged.objects(None,OWL.imports)): errors.append('active merged graph lost the gUFO import')
# no legacy assessment property
p=URIRef('https://w3id.org/cdsg/assessment#assessedByIndicator')
if any(merged.triples((None,p,None))) or any(merged.triples((p,None,None))): errors.append('legacy assessedByIndicator remains active')
# all internal named TBox classes/properties carry label and definitions (excluding ABox-punned classes)
internal_ns=('https://w3id.org/cdsg/core#','https://w3id.org/cdsg/analytics#')
for g in gs[:3]:
    for typ in (OWL.Class,OWL.ObjectProperty,OWL.DatatypeProperty):
        for x in set(g.subjects(RDF.type,typ)):
            if not isinstance(x,URIRef) or not str(x).startswith(internal_ns): continue
            if not list(g.objects(x,RDFS.label)): errors.append(f'missing label: {x}')
            if not list(g.objects(x,SKOS.definition)): errors.append(f'missing definition: {x}')
            if len(list(g.objects(x,SKOS.definition)))>1: warns.append(f'multiple definitions: {x}')
# functional property violations on explicit data
functional=set(merged.subjects(RDF.type,OWL.FunctionalProperty))
for p in functional:
    bys=defaultdict(set)
    for s,o in merged.subject_objects(p): bys[s].add(o)
    for s,vals in bys.items():
        if len(vals)>1: errors.append(f'functional property violation: {p} on {s} ({len(vals)})')
# EvidenceRecord exactly one evidenceDocument (active evidence records)
for s in set(merged.subjects(RDF.type,CORE.EvidenceRecord)):
    n=len(set(merged.objects(s,CORE.evidenceDocument)))
    if n!=1: errors.append(f'EvidenceRecord evidenceDocument count {n}: {s}')
# Named disjointness explicit conflicts under subclass closure for named class assertions
sub=defaultdict(set)
for a,b in merged.subject_objects(RDFS.subClassOf):
    if isinstance(a,URIRef) and isinstance(b,URIRef): sub[a].add(b)
changed=True
while changed:
    changed=False
    for a in list(sub):
        ext=set().union(*(sub.get(b,set()) for b in list(sub[a])))
        if not ext.issubset(sub[a]): sub[a]|=ext;changed=True
pairs=set()
for a,b in merged.subject_objects(OWL.disjointWith):
    if isinstance(a,URIRef) and isinstance(b,URIRef): pairs.add(frozenset((a,b)))
# AllDisjointClasses
for adc in merged.subjects(RDF.type,OWL.AllDisjointClasses):
    head=next(iter(merged.objects(adc,OWL.members)),None)
    vals=[]; cur=head; seen=set()
    while cur and cur!=RDF.nil and cur not in seen:
        seen.add(cur); first=next(iter(merged.objects(cur,RDF.first)),None)
        if isinstance(first,URIRef): vals.append(first)
        cur=next(iter(merged.objects(cur,RDF.rest)),None)
    for i,a in enumerate(vals):
        for b in vals[i+1:]: pairs.add(frozenset((a,b)))
for s in set(merged.subjects(RDF.type,None)):
    types=set(x for x in merged.objects(s,RDF.type) if isinstance(x,URIRef))
    closure=set(types)
    for t in list(types): closure|=sub.get(t,set())
    for pair in pairs:
        if pair.issubset(closure): errors.append(f'disjointness conflict: {s} -> {sorted(map(str,pair))}')
# gUFO categorization pattern equivalent to official SPARQL shape
for hot,base in merged.subject_objects(GUFO.categorizes):
    for inst in merged.subjects(RDF.type,hot):
        if (inst,RDFS.subClassOf,base) not in merged:
            errors.append(f'gUFO CategorizationShape violation: {hot} instance {inst} lacks subClassOf {base}')
# Data TBox declaration hygiene: only punned target categories may be owl:Class; no property declarations
DG=gs[-1]
if any(DG.subjects(RDF.type,OWL.ObjectProperty)): errors.append('data module contains owl:ObjectProperty declarations')
if any(DG.subjects(RDF.type,OWL.DatatypeProperty)): errors.append('data module contains owl:DatatypeProperty declarations')
# punned class declarations should be target-category instances and subclass Endurant
cat_hots=set(h for h,_ in merged.subject_objects(GUFO.categorizes))
for x in set(DG.subjects(RDF.type,OWL.Class)):
    if not any((x,RDF.type,h) in DG for h in cat_hots): errors.append(f'data owl:Class not explained by higher-order categorization: {x}')
    if (x,RDFS.subClassOf,GUFO.Endurant) not in DG: errors.append(f'punned target category lacks gufo:Endurant specialization: {x}')
# every evidence-set individual that is referenced is also described in the data module
_subs=set(DG.subjects())
for _o in {o for o in DG.objects() if isinstance(o,URIRef) and str(o).startswith('https://w3id.org/cdsg/resource/')}-_subs:
    errors.append(f'dangling reference to an undescribed individual: {_o}')
# development notes are not part of the release
if any(merged.triples((None,URIRef('https://w3id.org/cdsg/core#migrationNote'),None))): errors.append('development notes (cdsg:migrationNote) remain in the release')
import re as _re
for _s,_p,_o in merged:
    if isinstance(_o,Literal) and _re.search(r'\balpha\.\d',str(_o),_re.I): errors.append(f'development-stage wording in a literal: {_s} {_p}')
print(f'active_triples={len(merged)}')
print(f'errors={len(errors)} warnings={len(warns)}')
for x in errors[:100]: print('ERROR',x)
for x in warns[:100]: print('WARN',x)
raise SystemExit(1 if errors else 0)
