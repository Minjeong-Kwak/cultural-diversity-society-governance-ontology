# Changelog

## v1.0.0-rc.2 — 2026-10-12

- Repaired the inconsistency of the rc.1 active graph: `sourceInclusionText`, `evidenceText` and `sourceStatementText` had range `xsd:string` while their values carry language tags (4,261 values). Ranges are now `rdfs:Literal`. HermiT now reports the release consistent.
- Narrowed the data module to the evidence set for the source-statement and target-category argument. rc.1 policy-measure, status, outcome, indicator, observation and actor data are not part of rc.2.
- Quarantined two `invalid-legacy-link` alignments and the alignment from the Equality Act definition of race to a curated population category; resolved three `needs-review` alignments (two `related`, one `broader-than-curated`); removed the curated category left without alignment.
- Rewrote `run_robot_release_gate.sh` to use the vendored catalog, run HermiT on the core and merged graph, and run the positive and inconsistency fixtures; added `check_reasoning_fixture.py` and `regenerate_release_docs.py`.
- Added a sourcing assessment for every curated target category (analytics layer), with controlled outcome and source-validity schemes, and `cdsg:periodEndedByNormativeDocument` in the core. Re-added the 226 curated categories formed from policy-document target expressions, linked to those documents by `ana:derivedFromTargetExpressionIn`.
- Added Executive Order 13166 as a normative document with its LEP definition, its effective period ending 1 March 2025, and Executive Order 14224 section 3(b) as the revoking source; CQ08 now returns 18 rows.
- Assessed the force at the reference date of the eight remaining membership-specifying sources (all in force), with six web currency-check evidence records; `ana:assessmentBasis` now also links cited versions and evidence records, and the definition of the `in force` concept covers statistical definitions still applied by the issuing office.
- Changed the range of `cdsg:retrievedOn` from `xsd:date` to `xsd:dateTime`.
- Committed target categories to gUFO metatypes: `PolicyTargetCategory` subClassOf `gufo:NonSortal`, `SourceSpecifiedPolicyTargetCategory` subClassOf `gufo:RoleMixin` and defined by equivalence through `isSpecifiedByTargetCategoryStatement`, `CuratedPolicyTargetCategory` subClassOf `gufo:Mixin`. Removed asserted category subtypes from the data; HermiT now derives them.
- Added `cdsg:designRationale` for policy content, evidence records, policy target roles and institutional actor roles.
- Added fixtures IT05 and the curated-and-source inconsistency fixture, evidence-set classification checks DS01–DS04 and non-entailment check NT04; `run_robot_release_gate.sh` now writes HermiT class assertions of the merged graph.
- Retired CQ01–CQ07 and CQ09 with the rc.1 corpus data; added CQ10–CQ14. CQ14 needs reasoning: 18 rows with HermiT class assertions, 0 without. The CQ runner supports `# entailment: hermit`.
- Removed eight Korean literals on non-Korean resources (language rule) and moved 23 `prov:wasDerivedFrom` links to unpublished identifiers into quarantine.
- Separated policy specifications, status and outcome assertions, implementation activities, measure-level temporal qualifications and actor roles, policy profiles, the observation module and 13 SKOS schemes into a draft extension outside the package (41 classes, 101 properties), including `TargetCategoryMembershipAssertion` with `membershipBearer` and `membershipTargetCategory`. Category membership is now tested by typing an endurant with the punned category (IT06). The positive fixture now tests document roles; NT01 and NT02 moved with the extension; NT06 added.
- Added `cdsg:NormativeDocumentVersion` with `isVersionOf` (subproperty of `prov:specializationOf`), `evidenceDocumentVersion`, `versionKind`, `versionIdentifier`, `versionInForceFrom` and `versionCurrentTo`, and the SKOS `DocumentVersionKindScheme`. Recorded the cited version of all 17 normative documents and linked all evidence on them to it; added shapes, the document-and-version inconsistency fixture and CQ15.
- Added `cdsg:DocumentSupersessionAssertion` with `supersedingDocument`, `supersededDocument` and `supersessionEffectiveFrom`; recorded the replacement of the 1997 OMB race and ethnicity standards by the 2024 revision of SPD 15 with two evidence records; added its shape and CQ16.
- Split evidence records into one record per claim with page, locator, verbatim excerpt and file name (78 records); replaced three ambiguous records on the Korean Ministry of Justice; removed six unused records; recorded `retrievedOn` where the file states it (10 records); made `cdsg:evidencePage` functional and removed `cdsg:evidenceAssociationStatusText`; extended the evidence-record shape.
- Added `cdsg:publisherIdentifier` and `cdsg:publisherURI` with 46 values from the sources, `rdfs:seeAlso` from the document and version classes to the ELI ontology, the replacement of CP 1540 by CP 1559, the w3id.org redirect rules and `publication/check_redirects.py`; normalized shape IRIs to `shapes/target/` and `shapes/actor-jurisdiction/`; added a dangling-reference check to the structural audit and restored six instants it found missing.
- Added `cdsg:evidenceSourceURI` for evidence from web pages and recorded issuers for the five remaining documents from web sources (National Diet, President of the Republic, MHCLG, Immigration Services Agency as publisher), with original-text versions of the two Japanese statutes and of the CESEDA legislative part.
- Recorded the grounds of every disjointness axiom; `SourceSpecifiedPolicyTargetCategory` allows at most one specifying statement, with a fixture for a category given two statements of different types; linked four documents to their files, including the Korean 4th Master Plan for Multicultural Family Policy with its planning period, and removed an unsupported issuer link.
- Added issuers to 15 documents and administering ministries to 2 with 11 institutional actors and 19 evidence records, `cdsg:administeredByInstitutionalActor`, `cdsg:preparedByInstitutionalActor`, `cdsg:withinJurisdiction` (France and Germany within the EU), the actor type `legislature`, the post-to-organization link of the Federal Government Commissioner and the effective period of the Constitution Act, 1982; moved `isNormativelyGroundedIn` and `evidenceItemNumber` to the draft extension and removed the deprecated `issuedBy`.
- Added effective periods for Executive Orders 14224 and 14398 and the applicability of Regulation (EU) 2024/1351; removed five planning or reference periods whose evidence belonged to another document and relinked one; relabelled the EU normative document as Regulation (EU) 2024/1351.
- Retagged or replaced English-tagged titles in Korean or Japanese script and replaced 14 sourcing-assessment labels that used a Korean or Japanese category name with the English one.
- Added `dcterms:license` CC BY 4.0 to every module.
- Corrected the ontology name in the core module description. No module declares `owl:priorVersion`, because rc.1 was not published.
- Removed 314 `cdsg:migrationNote` development notes from the data and the property from the core; the extension keeps its one note as `skos:changeNote`.
- Pinned the vendored gUFO and gUFO shapes to upstream commits and recorded executed tool versions in `external_dependencies.lock.csv`; dropped Owlready2 from the requirements; replaced `run_reasoner_owlready.py` and `run_local_baseline.py` with obsolescence stubs.
- Rewrote the validation protocol, release gates, reproducibility protocol, claim discipline, author-input status and release checklist for rc.2.
- Removed development-stage wording from definitions, design rationales and alignment notes; dropped the unused `cdsg:replacesLegacyResource`; made `cdsg:evidenceText` functional.
- Replaced CQ08 and CQ10–CQ16 with four composite competency questions CQ1–CQ4; the runner now checks each answer against expectations fixed from the source analysis as well as against the regression digest.
- Corrected two design rationales: the replacement of the Destatis migration-background definition is not a case in the evidence set, and curated categories group expressions within one jurisdiction.


## v1.0.0-rc.1 — 2026-09-12

- Executed release-quality RDF/CQ/structural audits and created reproducible quality-audit scripts.
- Corrected the observation-module import from the obsolete vocabulary alpha.6 IRI to the RC1 vocabulary IRI.
- Normalized ontology descriptions and RC1 version metadata.
- Fixed the gUFO higher-order categorization pattern by declaring all 287 punned policy-target category classes as subclasses of `gufo:Endurant`; local official-shape-equivalent violations reduced from 574 to 0.
- Removed 61 redundant legacy `assessment:assessedByIndicator` assertions and the stray property declaration from the data module; canonical `ana:associatedIndicatorSpecification` assertions are retained.
- Added missing definitions for active CDSG properties and removed duplicate definitions from Organization, GovernmentOrganization, and GovernmentPost.
- Marked the unused generic `issuedBy` property deprecated in favor of `issuedByInstitutionalActor`.
- Regenerated the active merged graph, documentation dictionaries/metrics, checksum manifest, and quality report.
- External Pellet/HermiT, pySHACL, and exact gufoshapes-revision gates remain pending because required packages/revisions could not be installed/vendor-pinned in this execution environment.


## v1.0.0-rc.1 — 2026-09-12

Submission-candidate documentation and reproducibility release.

- No intended change to the alpha.9 domain semantics.
- Normalized module metadata/version IRIs to rc.1; corrected the consolidated data module metadata that still identified itself as alpha.7.
- Added class/property dictionaries, ontology metrics, vocabulary inventory, modeling-commitment table, module architecture, corpus data dictionary, reproducibility protocol, and journal release checklist.
- Added exact CQ baseline digests rather than execution-only checks.
- Added pinned validation Python requirements for RDFLib 7.5.0, pySHACL 0.40.1, and Owlready2 0.51.
- Added Pellet fixture runner, ROBOT/HermiT release-gate scaffold, OWL 2 DL profile gate instructions, and internal XML catalog.
- Preserved quarantines and the remaining provenance warning separately from active data.

## 1.0.0-rc.1

- Added reviewer-facing CQ matrix with user/task/formal requirement/entities/query/inference/expected/actual/positive/negative/limit columns.
- Added a full competency-question appendix containing all nine copyable SPARQL queries and sample outputs.
- Added explicit positive-inference and negative/non-entailment test matrix.
- Added reviewer-fit traceability matrix keyed to the review logic that motivated the redesign.
- Added manuscript-ready ontology-engineering methodology and evaluation draft, with unsupported study-protocol details left as explicit author-completion items.
- Added claim-discipline guidance and manuscript CQ results table.
- No domain-semantic redesign relative to alpha.10; ontology/data version metadata advanced to rc.1.