from rdflib import Graph, Namespace, RDF,RDFS,OWL,URIRef,BNode
from rdflib.collection import Collection
from collections import defaultdict
from pathlib import Path
base = Path(__file__).resolve().parents[2]
files=[base/'ontology/cdsg_core_v1.0.0-rc.2.ttl',base/'analytics/cdsg_analytics_v1.0.0-rc.2.ttl',base/'vocab/cdsg_vocab_v1.0.0-rc.2.ttl',base/'data/cdsg_data_v1.0.0-rc.2.ttl']
g=Graph(); [g.parse(f,format='turtle') for f in files]
# collect props excluding annotation-ish? all triples will work
subc=defaultdict(set); subp=defaultdict(set); dom=defaultdict(set); ran=defaultdict(set); inv=defaultdict(set); disj=set()
for c,_,d in g.triples((None,RDFS.subClassOf,None)):
 if isinstance(c,URIRef) and isinstance(d,URIRef): subc[c].add(d)
for p,_,q in g.triples((None,RDFS.subPropertyOf,None)):
 if isinstance(p,URIRef) and isinstance(q,URIRef): subp[p].add(q)
for p,_,c in g.triples((None,RDFS.domain,None)):
 if isinstance(p,URIRef) and isinstance(c,URIRef): dom[p].add(c)
for p,_,c in g.triples((None,RDFS.range,None)):
 if isinstance(p,URIRef) and isinstance(c,URIRef): ran[p].add(c)
for p,_,q in g.triples((None,OWL.inverseOf,None)):
 if isinstance(p,URIRef) and isinstance(q,URIRef): inv[p].add(q); inv[q].add(p)
for a,_,b in g.triples((None,OWL.disjointWith,None)):
 if isinstance(a,URIRef) and isinstance(b,URIRef): disj.add(tuple(sorted((a,b),key=str)))
# AllDisjointClasses
for node in g.subjects(RDF.type,OWL.AllDisjointClasses):
 mem=next(g.objects(node,OWL.members),None)
 if mem:
  xs=[x for x in Collection(g,mem) if isinstance(x,URIRef)]
  for i,a in enumerate(xs):
   for b in xs[i+1:]: disj.add(tuple(sorted((a,b),key=str)))
# transitive closures
changed=True
while changed:
 changed=False
 for c in list(subc):
  add=set().union(*(subc.get(x,set()) for x in list(subc[c]))) - subc[c]
  if add: subc[c]|=add; changed=True
 for p in list(subp):
  add=set().union(*(subp.get(x,set()) for x in list(subp[p]))) - subp[p]
  if add: subp[p]|=add; changed=True
# equiv existential patterns
patterns=[]
for cls,_,eq in g.triples((None,OWL.equivalentClass,None)):
 if not isinstance(cls,URIRef): continue
 inter=next(g.objects(eq,OWL.intersectionOf),None)
 if not inter: continue
 bases=[]; restrictions=[]
 for item in Collection(g,inter):
  if isinstance(item,URIRef): bases.append(item)
  elif (item,RDF.type,OWL.Restriction) in g:
   p=next(g.objects(item,OWL.onProperty),None); sv=next(g.objects(item,OWL.someValuesFrom),None)
   if isinstance(p,URIRef) and isinstance(sv,URIRef): restrictions.append((p,sv))
 if bases and restrictions: patterns.append((cls,tuple(bases),tuple(restrictions)))
# explicit types and property edges
itypes=defaultdict(set)
edges=defaultdict(lambda: defaultdict(set))
for s,_,c in g.triples((None,RDF.type,None)):
 if isinstance(c,URIRef): itypes[s].add(c)
for s,p,o in g:
 if p!=RDF.type and isinstance(p,URIRef): edges[p][s].add(o)
# add superprop+inverse iteratively + domain/range/types/patterns
for iteration in range(20):
 ntype=sum(map(len,itypes.values())); nedge=sum(len(os) for d in edges.values() for os in d.values())
 # superprop & inverse
 newedges=[]
 for p,sm in list(edges.items()):
  supers=subp.get(p,set())
  inverses=inv.get(p,set())
  for s,os in list(sm.items()):
   for o in list(os):
    for q in supers:
     if o not in edges[q][s]: newedges.append((q,s,o))
    if isinstance(o,(URIRef,BNode)):
     for q in inverses:
      if s not in edges[q][o]: newedges.append((q,o,s))
 for p,s,o in newedges: edges[p][s].add(o)
 # domain/range and subclass closure
 for p,sm in list(edges.items()):
  ds=dom.get(p,set()); rs=ran.get(p,set())
  if ds or rs:
   for s,os in sm.items():
    itypes[s]|=ds
    for o in os:
     if isinstance(o,(URIRef,BNode)): itypes[o]|=rs
 for s,ts in list(itypes.items()):
  add=set().union(*(subc.get(t,set()) for t in list(ts))) if ts else set()
  itypes[s]|=add
 # patterns
 for cls,bases,restrs in patterns:
  # candidates that have all bases
  for x,ts in list(itypes.items()):
   if cls in ts: continue
   if not all(b in ts for b in bases): continue
   ok=True
   for p,sv in restrs:
    vals=edges.get(p,{}).get(x,set())
    if not any(sv in itypes.get(v,set()) for v in vals): ok=False; break
   if ok: itypes[x].add(cls)
 ntype2=sum(map(len,itypes.values())); nedge2=sum(len(os) for d in edges.values() for os in d.values())
 print('iter',iteration,'types',ntype2,'edges',nedge2,'delta',ntype2-ntype,nedge2-nedge)
 if ntype2==ntype and nedge2==nedge: break
# check disjoint
viol=[]
for x,ts in itypes.items():
 for a,b in disj:
  if a in ts and b in ts: viol.append((x,a,b))
print('patterns',len(patterns),'disjoint pairs',len(disj),'viol',len(viol))
for v in viol[:50]: print('VIOL',v)
C=Namespace('https://w3id.org/cdsg/core#')
for cls in [C.DocumentIssuerRole,C.DocumentPublisherRole,C.NormativelyDefinedPolicyTargetCategory,C.StatisticallyDefinedPolicyTargetCategory,C.NormativelyConstitutedPolicyTargetCategory,C.OperationalizedPolicyTargetCategory]:
 xs=[x for x,ts in itypes.items() if cls in ts]
 exp=[x for x in xs if (x,RDF.type,cls) in g]
 print(str(cls).split('#')[-1], 'inferred-total',len(xs),'explicit',len(exp),'new',len(xs)-len(exp))
