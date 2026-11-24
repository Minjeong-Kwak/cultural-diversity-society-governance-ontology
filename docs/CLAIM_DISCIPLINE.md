# Claim discipline for the manuscript

The rc.2 release supports precise claims about the formal artifact and about the evidence set in the data module. It does not support claims about policy reality or about a policy corpus.

## Claims supported by the release

- The core, analytics and vocabulary modules encode explicit distinctions between documents and their content, between normative documents and their cited versions, between organizations and government posts, between source statements by semantic function, and between source-specified and research-curated target categories.
- The data module is an evidence set: 18 source-specified categories, the source statements that specify them, the 242 curated comparison categories and their alignments, the documents, versions, actors and evidence records these rest on. Every evidence record supports one claim and carries a verbatim excerpt with either a file name and page or a web address and retrieval date.
- The merged graph is in the OWL 2 DL profile and consistent under HermiT (ROBOT 1.9.10); four inconsistency fixtures are reported inconsistent and the positive and non-entailment fixtures pass.
- The merged graph conforms to the CDSG shapes and to the vendored gUFO shapes under pySHACL 0.40.1, with and without the class assertions HermiT derives.
- The five competency questions CQ1–CQ5 return the answers fixed in advance from the source analysis, and their normalized results match stored SHA-256 digests. CQ1 needs the HermiT class assertions; the others run over the asserted graph. A flat annotation-model baseline (`validation/annotation_baseline/`) answers CQ1–CQ5 from a model without statement, alignment or evidence individuals; it is a comparison, not a validation of the model.

## Claims that the results do not support

- that a source statement is legally correct or currently operative because it is represented; in-force periods hold only for the cited version and the dates the evidence states;
- that the evidence set is exhaustive or representative of policy documents in any jurisdiction, or that counts over it estimate prevalence, need or effectiveness;
- that a curated category is identical to a source category; alignments state the recorded relation and its evidence only;
- that logical consistency, SHACL conformance or CQ success establishes conceptual adequacy;
- anything about policy measures, implementation, outcomes, indicators or observations; rc.2 carries no such data, and the modules for them are in the separate policy-process extension draft.

## Recommended manuscript verbs

Prefer: represents, distinguishes, records, retrieves, classifies under the stated axioms, is consistent under HermiT, conforms to the tested shapes, returns the baseline results.

Avoid: proves, validates the policy, captures the domain completely, guarantees correctness, demonstrates effectiveness, establishes causality.
