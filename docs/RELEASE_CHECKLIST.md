# CDSG v1.0.0-rc.2 release checklist

All validation gates have been executed for rc.2; logs are in `validation/results/`.

## Validation

- [x] RDF/Turtle/RDF-XML parsing, module import audit and dangling-reference check
- [x] Structural, cardinality and disjointness quality audit
- [x] ROBOT 1.9.10 OWL 2 DL profile, core and merged graph
- [x] HermiT consistency and classification, core and merged graph
- [x] Positive-inference, evidence-set classification and non-entailment fixtures
- [x] Four inconsistency fixtures reported inconsistent
- [x] pySHACL 0.40.1 over the CDSG shapes
- [x] pySHACL 0.40.1 over the vendored gUFO shapes, asserted and with HermiT class assertions
- [x] gUFO and gUFO shapes vendored and pinned to upstream commits
- [x] CQ1–CQ5 checked against expectations from the source analysis and against regression digests
- [x] w3id redirect rules checked against package files
- [x] Checksum manifest regenerated and verified

## Ontological content

- [x] Document and content distinction explicit
- [x] Normative document and cited version distinguished; replacement and revocation recorded
- [x] Organization and government post distinguished
- [x] Statement types disjoint by semantic function; grounds of every disjointness recorded
- [x] Curated and source-specified target categories distinguished and derived by reasoning
- [x] Every evidence record supports one claim with a verbatim excerpt and a file and page or a web address and retrieval date
- [x] Development notes removed from the release

## Publication

- [x] License declared (CC BY 4.0)
- [x] Class and property dictionaries, commitment table and vocabulary inventory regenerated
- [x] Quarantine separated from the active graph
- [ ] Push the repository and tag `v1.0.0-rc.2`
- [ ] Register the w3id redirects
- [ ] Add creator ORCID
- [ ] Create the archival release and DOI
