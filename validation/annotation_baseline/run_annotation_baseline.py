# Builds a flat annotation model from the reference graph, runs CQ1-CQ5 equivalents on it, compares with reference rows.
import rdflib, csv, collections
from pathlib import Path
HERE=Path(__file__).resolve().parent
from rdflib import Graph, Namespace, URIRef, Literal, RDF
R=str(HERE.parents[1])+"/"
ref=Graph(); ref.parse(R+"data/cdsg_v1.0.0-rc.2_active_merged.ttl")
def q(p,path=R+"validation/queries/"): return list(ref.query(open(path+p,encoding="utf-8").read()))
cq1=list(csv.DictReader(open(R+"validation/cq_results/CQ1.csv",encoding="utf-8")))
cq2=q("CQ2.rq"); cq3=q("CQ3.rq"); cq4=q("CQ4.rq"); cq5=q("CQ5.rq")
B=Namespace("urn:baseline#")
b=Graph()
def add(s,p,o):
    b.add((URIRef(s),B[p],o if isinstance(o,(URIRef,Literal)) else Literal(str(o))))
# source categories: one class each; flat annotations, no statement, no evidence record entities
st2cat={}
for r in cq1:
    c=r["category"]; add(c,"kind",r["kind"]); add(c,"document",URIRef(r["document"]))
    if r["version"]: add(c,"version",r["version"])
    add(c,"jurisdiction",r["jurisdiction"]); add(c,"evidenceRecords",r["evidenceRecords"])
    st2cat[r["statement"]]=c
# CQ4 history attached to the document of the source category
for r in cq4:
    c=st2cat.get(str(r.statement))
    if not c: continue            # statement defines no source category: no class to carry it
    for p,v in (("version",r.version),("versionKind",r.versionKind),("inForceFrom",r.inForceFrom),("change",r.change),("otherDocument",r.otherDocument),("changeDate",r.changeDate)):
        if v is not None: add(c,"h_"+p,Literal(str(v)))
# curated categories: flat multi-valued annotations
srccats={r["category"] for r in cq1}
for r in cq3:
    cur=str(r.curated)
    add(cur,"alignRelation",str(r.relation))
    if str(r.source) in srccats: add(cur,"alignSource",URIRef(r.source))   # statement-only alignments have no class to point to
    if r.evidence: add(cur,"alignEvidence",URIRef(r.evidence))
A="https://w3id.org/cdsg/analytics#"
for r in cq5:
    c=str(r.curated); add(c,"facet","foreign-national-population"); add(c,"jurisdiction",str(r.jurisdiction))
    add(c,"outcome",str(r.outcome)); 
    if r.validity: add(c,"validity",str(r.validity))
ASS=ref.query('''PREFIX cdsg:<https://w3id.org/cdsg/core#> PREFIX ana:<https://w3id.org/cdsg/analytics#> PREFIX time:<http://www.w3.org/2006/time#>
SELECT ?cur ?outcome ?validity ?endedBy ?end WHERE{?a a ana:TargetCategorySourcingAssessment; ana:assessesCuratedCategory ?cur; ana:sourcingOutcome ?outcome.
 OPTIONAL{?a ana:validityAtReferenceDate ?validity} OPTIONAL{?a ana:assessmentBasis ?p. ?p a cdsg:NormativeEffectivePeriodAssertion; cdsg:periodEndedByNormativeDocument ?endedBy; cdsg:hasTemporalInterval/time:hasEnd/time:inXSDDateTime ?end}}''')
for r in ASS:
    add(str(r.cur),"outcome2",str(r.outcome))
    if r.validity: add(str(r.cur),"validity2",str(r.validity))
    if r.endedBy: add(str(r.cur),"endedBy",str(r.endedBy)); add(str(r.cur),"end",str(r.end))
b.serialize(str(HERE/"annotation_baseline.ttl"),format="turtle")
print("baseline triples",len(b))
# ---- baseline queries ----
P="PREFIX b:<urn:baseline#>\n"
bq1=list(b.query(P+"SELECT ?c ?k ?doc ?ver ?j ?n WHERE{?c b:kind ?k;b:document ?doc;b:jurisdiction ?j;b:evidenceRecords ?n. OPTIONAL{?c b:version ?ver}}"))
bq3=list(b.query(P+"SELECT DISTINCT ?cur ?rel ?src WHERE{?cur b:alignRelation ?rel; b:alignSource ?src}"))
bq5=list(b.query(P+"SELECT ?c ?j ?o ?v WHERE{?c b:facet 'foreign-national-population';b:jurisdiction ?j;b:outcome ?o. OPTIONAL{?c b:validity ?v}}"))
bq4=list(b.query(P+"SELECT DISTINCT ?c ?ver ?ch ?od ?cd WHERE{?c b:document ?d. OPTIONAL{?c b:h_version ?ver} OPTIONAL{?c b:h_change ?ch} OPTIONAL{?c b:h_otherDocument ?od} OPTIONAL{?c b:h_changeDate ?cd}}"))
out=[]
def rep(s): print(s); out.append(s)
# CQ1
refset={(r["category"],r["kind"],r["document"],r["version"],r["jurisdiction"],r["evidenceRecords"]) for r in cq1}
bset={(str(r.c),str(r.k),str(r.doc),str(r.ver) if r.ver else "",str(r.j),str(r.n)) for r in bq1}
rep(f"CQ1 reference rows {len(cq1)}, baseline rows {len(bq1)}, rows equal on all columns except the statement column: {len(refset&bset)}; statement column available in baseline: no")
# CQ3
refpairs={(str(r.curated),str(r.relation),str(r.source)) for r in cq3}
bpairs={(str(r.cur),str(r.rel),str(r.src)) for r in bq3}
rep(f"CQ3 reference rows {len(cq3)}, baseline rows {len(bq3)}, correct rows {len(refpairs&bpairs)}, spurious rows {len(bpairs-refpairs)}, missing rows {len(refpairs-bpairs)}")
# CQ5
r5={(str(r.curated),str(r.jurisdiction),str(r.outcome),str(r.validity) if r.validity else "") for r in cq5}
b5={(str(r.c),str(r.j),str(r.o),str(r.v) if r.v else "") for r in bq5}
rep(f"CQ5 reference rows {len(cq5)}, baseline rows {len(bq5)}, equal rows {len(r5&b5)}")
# CQ4
r4={(str(r.statement),str(r.version) if r.version else "",str(r.change) if r.change else "",str(r.otherDocument) if r.otherDocument else "") for r in cq4}
b4=set()
for r in bq4: b4.add((str(r.c),str(r.ver) if r.ver else "",str(r.ch) if r.ch else "",str(r.od) if r.od else ""))
rep(f"CQ4 reference statements {len({str(r.statement) for r in cq4})}, baseline carriers {len({k[0] for k in b4})}")
# CQ2: outcome/validity per curated category is functional in baseline too
bq2=list(b.query(P+"SELECT ?o ?v (COUNT(DISTINCT ?c) AS ?n) WHERE{?c b:outcome2 ?o. OPTIONAL{?c b:validity2 ?v} } GROUP BY ?o ?v"))
r2={(str(r.outcome),str(r.validity) if r.validity else "",int(r.categories)) for r in cq2}
b2={(str(r.o),str(r.v) if r.v else "",int(r.n)) for r in bq2}
rep(f"CQ2 reference rows {len(cq2)}, baseline rows {len(bq2)}, equal rows {len(r2&b2)}")
open(HERE/"annotation_baseline_results.txt","w",encoding="utf-8").write("\n".join(out))
