# Author-supplied information: status at v1.0.0-rc.2

The release records what the files can show. The items marked open need the research protocol or project records and must not be reconstructed from the knowledge graph.

| # | Item | Status | Where it stands |
|---|---|---|---|
| 1 | Corpus boundary and selection criteria | resolved | The evidence set is the documents in the data folder of the project; `README.md` and `docs/CLAIM_DISCIPLINE.md` state that it is purposive and not exhaustive. Selection criterion: the most recently revised multicultural-related policies of the countries covered. Collection period: 20 August 2026 to 10 September 2026. |
| 2 | Exact source versions | resolved | Every statement in a normative document cites a `cdsg:NormativeDocumentVersion` with kind, identifier and in-force dates (CQ4). Publisher identifiers and URIs are recorded where the source prints them. |
| 3 | Retrieval protocol | partly resolved | File-based evidence names the file and page; web evidence records the address and retrieval date (`cdsg:retrievedOn`). Replacement and revocation are recorded as supersession assertions and temporal qualifications (CQ4). Download dates of the PDF files remain open. |
| 4 | Concept and relation extraction procedure | open | Who extracted, how many passes, adjudication. |
| 5 | Expert involvement | open | State the review or its absence. |
| 6 | Competing conceptualizations | partly resolved | Each disjoint class carries `cdsg:designRationale`; `docs/MODELING_COMMITMENTS.md` gives the grounds. The link to the research process remains for the manuscript. |
| 7 | Definition-writing protocol | open | How definitions were drafted and checked. |
| 8 | Reuse decision record | partly resolved | gUFO and gUFO shapes are pinned to upstream commits in `validation/external_dependencies.lock.csv`; SKOS, PROV-O, Dublin Core terms and OWL-Time are W3C or DCMI recommendations used by namespace. Reasons for reuse remain for the manuscript. |
| 9 | Entity-resolution procedure | open | How organizations, posts, documents and categories were deduplicated. |
| 10 | Data-quality protocol | partly resolved | `run_quality_audit.py` checks functional-property violations, evidence records without a document and dangling references; excluded links are kept in `quarantine/`. Correction and translation handling remain open. |
| 11 | Coverage and representativeness | resolved for the release | `docs/CLAIM_DISCIPLINE.md` states that counts over the evidence set estimate nothing about populations or jurisdictions. |
| 12 | Authorship and release metadata | partly resolved | License CC BY 4.0, repository `Minjeong-Kwak/cultural-diversity-society-governance-ontology` and w3id rules are set. ORCID, archival DOI and release date remain open. |
| 13 | Final external validation run | resolved | ROBOT 1.9.10 DL profile and HermiT, pySHACL 0.40.1 over CDSG and pinned gUFO shapes, fixtures and CQ baselines; logs in `validation/results/`. |
| 14 | Journal submission hygiene | open | Manuscript stage. |
