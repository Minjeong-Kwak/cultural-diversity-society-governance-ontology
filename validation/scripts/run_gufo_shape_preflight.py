#!/usr/bin/env python3
"""Local SPARQL-equivalent preflight for the six public gufoshapes rules.
This is NOT a substitute for executing pySHACL against the official pinned gufoshapes.ttl.
"""
from pathlib import Path
from rdflib import Graph, Namespace, RDF, RDFS, OWL, URIRef
ROOT=Path(__file__).resolve().parents[2]
g=Graph().parse(ROOT/'data/cdsg_v1.0.0-rc.2_active_merged.ttl',format='turtle')
GUFO=Namespace('http://purl.org/nemo/gufo#')
viol=[]
# 1 Rigid/semi-rigid cannot specialize anti-rigid types
rigid_targets=[GUFO.RigidType,GUFO.Category,GUFO.Kind,GUFO.SubKind,GUFO.SemiRigidType,GUFO.Mixin]
anti=[GUFO.AntiRigidType,GUFO.Phase,GUFO.PhaseMixin,GUFO.Role,GUFO.RoleMixin]
# 2 NonSortal cannot specialize Sortal
nonsortal_targets=[GUFO.NonSortal,GUFO.Category,GUFO.PhaseMixin,GUFO.RoleMixin,GUFO.Mixin]
sortals=[GUFO.Sortal,GUFO.Kind,GUFO.SubKind,GUFO.Phase,GUFO.Role]
# helper: instances of metaclass (gUFO stereotype on OWL classes)
def instances(classes):
    out=set()
    for c in classes: out.update(g.subjects(RDF.type,c))
    return out
for t in instances(rigid_targets):
    for sup in g.objects(t,RDFS.subClassOf):
        if any((sup,RDF.type,a) in g for a in anti): viol.append(('RigidOrSemiRigidShape',t,sup))
for t in instances(nonsortal_targets):
    for sup in g.objects(t,RDFS.subClassOf):
        if any((sup,RDF.type,a) in g for a in sortals): viol.append(('NonSortalShape',t,sup))
# 3 base sortals need superclass typed as Kind/SubKind/Phase/Role
for t in instances([GUFO.SubKind,GUFO.Phase,GUFO.Role]):
    ok=False
    for sup in g.objects(t,RDFS.subClassOf):
        if any((sup,RDF.type,k) in g for k in [GUFO.Kind,GUFO.SubKind,GUFO.Phase,GUFO.Role]): ok=True
    if not ok: viol.append(('BaseSortalShape',t,None))
# 4 Kinds cannot specialize sortals
for t in instances([GUFO.Kind]):
    for sup in g.objects(t,RDFS.subClassOf):
        if any((sup,RDF.type,k) in g for k in [GUFO.SubKind,GUFO.Phase,GUFO.Role,GUFO.Kind]): viol.append(('KindShape',t,sup))
# 5 Endurant types cannot specialize listed disjoint-from-Endurant classes directly
forbidden={GUFO.AbstractIndividual,GUFO.QualityValue,URIRef('http://www.w3.org/2006/time#Instant'),GUFO.Event,GUFO.Participation,GUFO.Situation,GUFO.QualityValueAttributionSituation,GUFO.TemporaryConstitutionSituation,GUFO.TemporaryInstantiationSituation,GUFO.TemporaryParthoodSituation,GUFO.TemporaryRelationshipSituation}
endurant_meta=[GUFO.EndurantType,GUFO.NonRigidType,GUFO.AntiRigidType,GUFO.RigidType,GUFO.SemiRigidType,GUFO.Phase,GUFO.PhaseMixin,GUFO.Role,GUFO.RoleMixin,GUFO.Mixin,GUFO.NonSortal,GUFO.Category,GUFO.Sortal,GUFO.Kind,GUFO.SubKind]
for t in instances(endurant_meta):
    for sup in g.objects(t,RDFS.subClassOf):
        if sup in forbidden: viol.append(('EndurantTypeShape',t,sup))
# 6 CategorizationShape exact logic
for hot,base in g.subject_objects(GUFO.categorizes):
    for inst in g.subjects(RDF.type,hot):
        if (inst,RDFS.subClassOf,base) not in g: viol.append(('CategorizationShape',hot,inst))
# Partition pairwise disjointness if any partitions exist
# equivalence/sameAs and explicit disjoint / AllDisjoint classes considered
pairs=set()
for a,b in g.subject_objects(OWL.disjointWith): pairs.add(frozenset((a,b)))
for adc in g.subjects(RDF.type,OWL.AllDisjointClasses):
    head=next(iter(g.objects(adc,OWL.members)),None); vals=[]; cur=head; seen=set()
    while cur and cur!=RDF.nil and cur not in seen:
        seen.add(cur); x=next(iter(g.objects(cur,RDF.first)),None)
        if x: vals.append(x)
        cur=next(iter(g.objects(cur,RDF.rest)),None)
    for i,a in enumerate(vals):
        for b in vals[i+1:]: pairs.add(frozenset((a,b)))
for hot,base in g.subject_objects(GUFO.partitions):
    ins=list(set(g.subjects(RDF.type,hot)))
    for i,a in enumerate(ins):
        for b in ins[i+1:]:
            if (a,OWL.equivalentClass,b) in g or (b,OWL.equivalentClass,a) in g or (a,OWL.sameAs,b) in g or (b,OWL.sameAs,a) in g: continue
            if frozenset((a,b)) not in pairs: viol.append(('PartitionPairwiseDisjointnessShape',a,b))
from collections import Counter
c=Counter(v[0] for v in viol)
print('gUFO shape-equivalent preflight')
for k in ['RigidOrSemiRigidShape','NonSortalShape','BaseSortalShape','KindShape','EndurantTypeShape','CategorizationShape','PartitionPairwiseDisjointnessShape']:
    print(f'{k}: {c.get(k,0)} violations')
print('total:',len(viol))
for v in viol[:50]: print('VIOLATION',*v)
raise SystemExit(1 if viol else 0)
