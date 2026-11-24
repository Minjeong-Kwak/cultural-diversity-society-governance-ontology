# CDSG v1.0.0-rc.2

Cultural Diversity Society Governance (CDSG) ontology, release candidate 2.

## What rc.2 contains

| Module | File |
|---|---|
| Core ontology | `ontology/cdsg_core_v1.0.0-rc.2.ttl` (and `.owl`) |
| Analytical layer | `analytics/cdsg_analytics_v1.0.0-rc.2.ttl` |
| Controlled vocabularies | `vocab/cdsg_vocab_v1.0.0-rc.2.ttl` |
| Evidence set | `data/cdsg_data_v1.0.0-rc.2.ttl` |
| Merged graph | `data/cdsg_v1.0.0-rc.2_active_merged.ttl` |
| Quarantined assertions | `quarantine/cdsg_validation_quarantine_v1rc2.ttl` |

The data module of rc.2 is an evidence set, not a policy corpus. It is released under CC BY 4.0, like every module. It holds the 18 source-specified policy-target categories, the 24 source statements that define, constitute, operationalize, classify or name them, their evidence records and source documents with the version of each normative document cited, the jurisdictions and issuing actors involved, and temporal qualifications of those documents. It also holds the 242 research-curated categories formed from target expressions in the policy documents, 21 reviewed alignment assertions between source and curated categories, and one sourcing assessment per curated category. The policy-measure, status, outcome, indicator, observation and actor data of rc.1 are not part of this release.

Each sourcing assessment records, at the reference date 2026-08-27 and relative to the collected corpus, whether a source statement was identified for the curated category, whether one specifies membership, and whether the specifying source was still in force. Executive Order 13166 and its revocation by Executive Order 14224 section 3(b) form the worked case of a membership-specifying source that is no longer in force.

The merged graph is the RDF union of the four modules minus the internal CDSG `owl:imports` triples, which OWLAPI cannot load together with the merged document. The gUFO import is kept. `validation/scripts/run_quality_audit.py` checks this invariant.

## Ontological status of target categories

Target categories are higher-order, non-sortal types. Source-specified categories are `gufo:RoleMixin`, curated categories `gufo:Mixin`; the two are disjoint. Category subtypes are not asserted in the data: HermiT derives them, and the role-mixin status, from each category's link to a source statement. See `docs/MODELING_COMMITMENTS.md`.

## Scope

rc.2 contains 42 CDSG classes. Policy specifications, status and outcome assertions, implementation activities, measure-level actor roles, policy profiles, provenance-bearing membership records and the indicator observation module were separated into a draft extension kept outside this package, because rc.2 has no data that exercises them. The draft is consistent with rc.2 under HermiT but is not part of this release.

## Persistent IRIs and external identifiers

CDSG IRIs start with `https://w3id.org/cdsg/`. The w3id.org redirect rules, the hosting layout and the order of steps are in `publication/`; the namespace resolves once the repository is published and the w3id.org pull request is merged.

Documents and versions carry the identifiers their publishers assign (`cdsg:publisherIdentifier`) and, where the source prints it or the address was confirmed at the publisher, the publisher's address (`cdsg:publisherURI`), including the European Legislation Identifier of Regulation (EU) 2024/1351, legislation.gov.uk, Justice Laws, Légifrance, e-Gov and Federal Register addresses.

## External vocabulary

The release imports **gUFO 1.0.0 only**, vendored at `validation/external/gufo.owl` and resolved through `validation/catalog-v001.xml`. OWL-Time, W3C ORG, PROV-O, SKOS and Dublin Core are not imported: their IRIs are reused and the terms in use are declared locally in the core module.

## Validation

See `validation/cdsg_v1rc2_quality_report.md`. In short: OWL 2 DL profile, HermiT consistency and classification, positive-inference, non-entailment and inconsistency fixtures, classification of the evidence set, pySHACL over the CDSG and gUFO shapes, the structural audit and five competency questions all pass on rc.2. `validation/cq_matrix.csv` lists each CQ with the requirement it tests, its task, whether it needs reasoning, the expected answer and where that expectation comes from.

To reproduce, from the package root:

```
python validation/scripts/run_quality_audit.py
bash validation/run_robot_release_gate.sh path/to/robot.jar
python validation/scripts/check_reasoning_fixture.py
python validation/scripts/run_shacl.py --gufo-shapes validation/external/gufoshapes.ttl
python validation/scripts/run_cq_baseline.py
python validation/scripts/regenerate_release_docs.py
```

`robot.jar` (ROBOT 1.9.10) is not shipped in the package. `regenerate_release_docs.py` recomputes `docs/ontology_metrics.csv`, the count and range columns of the class and property dictionaries, and `SHA256SUMS.txt`; run it last after any change.

## Status of documentation

The manuscript-facing documents of rc.1 (CQ evaluation tables, methods drafts, reviewer traceability matrix, data dictionary, ontology reference) described the rc.1 corpus and are not carried into rc.2. They will be rewritten against rc.2.
