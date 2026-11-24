# Module architecture

| Module | Ontological purpose | What it must not be used for |
|---|---|---|
| Core | Domain commitments: policy documents and their content, source statements about target categories, source-specified target categories, actors and document roles, temporal qualifications, evidence | Comparative research codes or raw controlled vocabularies |
| Analytics | Research-curated target categories, source-to-curated alignments, sourcing assessments | Domain-level identity/subsumption claims |
| Vocabulary | SKOS classifications for domains, instruments, actor types, statuses, facets, etc. | Replacing OWL identity-bearing classes |
| Data | Active ABox/corpus instances | Defining the ontology's conceptual commitments by data convention alone |
| Quarantine | Preserved legacy assertions awaiting adjudication | Active inference/query results |

The physical module boundary is part of the semantic design: analytical aggregation and controlled classification are kept out of the core ontology so that research convenience does not silently become an ontological commitment.


Policy specifications, status and outcome assertions, implementation activities, measure-level actor roles, policy profiles and the observation module were separated from rc.2 into a draft extension kept outside the release package (`cdsg_extension_policy_process`). rc.2 does not evaluate them.
