#!/usr/bin/env python3
from pathlib import Path
import argparse, sys
try:
    from pyshacl import validate
    from rdflib import Graph
except ImportError:
    print('ERROR: pySHACL is not installed. Install validation/requirements-validation.txt',file=sys.stderr);sys.exit(2)
ROOT=Path(__file__).resolve().parents[2]
p=argparse.ArgumentParser();p.add_argument('--gufo-shapes',type=Path);p.add_argument('--no-gufo',action='store_true');args=p.parse_args()
data=Graph();data.parse(ROOT/'data/cdsg_v1.0.0-rc.2_active_merged.ttl',format='turtle')
shapes=Graph()
for f in sorted((ROOT/'validation/shapes').glob('*.ttl')): shapes.parse(f,format='turtle')
conforms, report_graph, report_text=validate(data_graph=data, shacl_graph=shapes, inference='rdfs', advanced=True, allow_warnings=True, meta_shacl=True)
(ROOT/'validation/results').mkdir(exist_ok=True)
report_graph.serialize(destination=ROOT/'validation/results/cdsg-shacl-report.ttl',format='turtle')
(ROOT/'validation/results/cdsg-shacl-report.txt').write_text(report_text,encoding='utf-8')
print('CDSG_SHACL_CONFORMS=',conforms)
failed=not conforms
if not args.no_gufo:
    if not args.gufo_shapes:
        print('ERROR: --gufo-shapes PATH is required for the release gate (or use --no-gufo only for development).',file=sys.stderr);sys.exit(2)
    gs=Graph();gs.parse(args.gufo_shapes,format='turtle')
    c2, rg2, rt2=validate(data_graph=data, shacl_graph=gs, inference='rdfs', advanced=True, allow_warnings=True, meta_shacl=True)
    rg2.serialize(destination=ROOT/'validation/results/gufo-shacl-report.ttl',format='turtle')
    (ROOT/'validation/results/gufo-shacl-report.txt').write_text(rt2,encoding='utf-8')
    print('GUFO_SHACL_CONFORMS=',c2); failed=failed or (not c2)
inf=ROOT/'validation/results/merged-inferred-class-assertions.ttl'
if not args.no_gufo and inf.exists():
    ent=Graph()
    for t in data: ent.add(t)
    ent.parse(inf)
    c3, rg3, rt3=validate(data_graph=ent, shacl_graph=gs, inference='rdfs', advanced=True, allow_warnings=True, meta_shacl=True)
    (ROOT/'validation/results/gufo-shacl-report-entailed.txt').write_text(rt3,encoding='utf-8')
    print('GUFO_SHACL_CONFORMS_WITH_HERMIT_CLASS_ASSERTIONS=',c3); failed=failed or (not c3)
sys.exit(1 if failed else 0)
