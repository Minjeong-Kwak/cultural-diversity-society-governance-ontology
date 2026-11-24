#!/usr/bin/env python3
"""Emulate publication/w3id/ids/cdsg/.htaccess for every w3id.org/cdsg IRI used in the
release and check that each redirect target that points into this repository at the
current release tag names a file that exists in the package."""
import re, sys
from pathlib import Path
from rdflib import Graph, URIRef
ROOT = Path(__file__).resolve().parents[1]
rules, cond = [], None
for line in (ROOT / 'publication/w3id/ids/cdsg/.htaccess').read_text().splitlines():
    m = re.match(r'RewriteCond %\{HTTP_ACCEPT\} (\S+)', line)
    if m: cond = m.group(1); continue
    m = re.match(r'RewriteRule (\S+) (\S+) \[(\S+)\]', line)
    if m: rules.append((cond, m.group(1), m.group(2))); cond = None
def resolve(path, accept):
    for c, pat, target in rules:
        if c and not re.search(c, accept): continue
        m = re.match(pat, path)
        if m: return re.sub(r'\$(\d)', lambda g: m.group(int(g.group(1))) or '', target)
    return None
g = Graph()
for f in ['data/cdsg_v1.0.0-rc.2_active_merged.ttl'] + sorted(str(p.relative_to(ROOT)) for p in (ROOT / 'validation/shapes').glob('*.ttl')):
    g.parse(ROOT / f)
iris = {str(x) for t in g for x in t if isinstance(x, URIRef) and str(x).startswith('https://w3id.org/cdsg/')}
tag = 'v1.0.0-rc.2'
bad = 0; seen = {}
for iri in sorted(iris):
    path = iri[len('https://w3id.org/cdsg/'):].split('#')[0]
    for accept in ['text/turtle', 'application/rdf+xml', 'text/html,*/*;q=0.8']:
        t = resolve(path, accept)
        if t is None: print('NO RULE', iri, accept); bad += 1; continue
        m = re.match(r'https://raw\.githubusercontent\.com/[^/]+/[^/]+/(v[^/]+)/(.+)$', t)
        if m and m.group(1) == tag:
            seen[m.group(2)] = seen.get(m.group(2), 0) + 1
            if not (ROOT / m.group(2)).exists(): print('MISSING', iri, '->', m.group(2)); bad += 1
        elif m and 'html' in accept: print('HTML TO RAW', iri); bad += 1
print('IRIs', len(iris), 'targets in this release:', {k: v for k, v in sorted(seen.items())})
print('problems', bad); sys.exit(1 if bad else 0)
