# Modeling commitments

This document records the commitments that should be defended in the manuscript rather than inferred from implementation details alone.

## 1. Information content and documents

CDSG distinguishes the documents that express policy content from the content they express. A source statement about a target category is content; the statute or statistical standard that contains it is a document. Evidence records identify the document, page, locator and excerpt that support a statement. Each evidence record supports one claim and cites one page or page range of one file; the excerpt is verbatim, with ' … ' marking omitted text between fragments on the same page. The retrieval time is recorded only where the file states it. Evidence taken from a web page instead of a corpus file carries its address and retrieval time in place of a file and page.

## 2. Source statements and researcher curation

Source-defined target categories are separated from research-curated target categories. Alignments such as close, broader-than-curated, or narrower-than-curated are analytical assertions with their own evidence. They are not `owl:equivalentClass` claims.

## 3. Roles and identity-bearing entities

Organizations and government posts provide identity; document roles (issuer, publisher) are anti-rigid and inferred from issuing or publishing a document, without reclassifying a post as an organization. A document's actors are recorded only as its source names them: the issuer (an enacting clause, an issuing ministry, a notice's agency), the actor that prepared it, or, for Korean statutes, the administering ministry printed in the header. A government post is linked to the organization it belongs to.

Policy target roles are distinct from policy target categories. An endurant typed by a policy target category is not thereby in a target role; rc.2 represents no concrete bearers, and the member and role level is exercised only by fixtures.

## 3a. Disjointness

Every disjointness axiom rests on one of three grounds, recorded as `cdsg:designRationale` on each class involved.

- Different kinds. A document is a concrete object, its content an abstract individual, a cited version a fixed text state; an organization is a functional complex and a government post a position in one; a policy target category is a higher-order type and a policy target role a type of endurants. Nothing can be both.
- One function per statement record. A statement record captures one semantic function of one source passage; a passage that defines and operationalizes is recorded as two statements. Normative and statistical definitions are told apart by the source's institutional status, not its purpose (MighEV is an ordinance serving statistics and counts as normative).
- One specifying statement per source category. Source categories are individuated by the statement that specifies them, and `SourceSpecifiedPolicyTargetCategory` allows at most one specifying statement. The disjointness of the category subtypes follows: with the category-level axioms removed, a category given a definition and an operationalization is still inconsistent, and without the cardinality axiom it is not. A fixture tests the inconsistency.

## 4. Normative content

A normative document is not identical to the normative content it expresses. Definitions and constitution rules about target categories are normative content expressed in a document.

## 4a. Jurisdictions

A jurisdiction lies within a wider one when the wider jurisdiction's law applies in it (`cdsg:withinJurisdiction`, transitive). France and Germany lie within the European Union, each on the evidence of a statute in the corpus that applies or implements EU law.

## 5. Time

The effective period of a normative document, the planning period, coverage period and reference period of a policy document, and the reference date of a sourcing assessment are different relations. The end of an effective period records the document that ended it. Every interval is asserted with evidence from the document whose period it states.

A normative document keeps its identity while it is amended. The text a source statement cites is one version of it (`cdsg:NormativeDocumentVersion`): an original text, or an official consolidation current to a stated point. Every normative document in the evidence set has a recorded version, and every evidence record on a normative document names the version it cites. Version dates are recorded only as the publisher states them. The in-force date of a version is not the effective period of the document: Regulation (EU) 2024/1351 entered into force on 11 June 2024 but applies, Article 2 included, from 1 July 2026.

Three changes in a definition's history are kept apart. Replacement is recorded as a `cdsg:DocumentSupersessionAssertion` only where a later source states that it replaces an earlier document: the 2024 revision of OMB SPD 15 replaces the 1997 race and ethnicity standards from 28 March 2024. Revocation without replacement is the end of an effective period with the ending document (Executive Order 13166). A new concept introduced alongside an old one is not replacement: the Federal Statistical Office introduced immigration history as an additional data offer and continues to publish results by migration background, so no relation is asserted between the two statements. A new edition of a statistical classification (ASCCEG 2025, sixth edition after the 2019 fifth edition) is not recorded as replacement because the source does not state one.

## 6. Scope of rc.2

Policy specifications, status and outcome assertions, implementation activities, measure-level actor roles, policy profiles and indicator observations were separated into a draft extension outside the release. Their commitments (specification versus implementation, reported versus actual status and outcome, observation record versus measurement activity) are retained there but are not evaluated in rc.2.

## 7. Ontological status of target categories

Policy target categories are higher-order types (OWL 2 punning) that classify persons, families, households and organizations. Because their members are of different kinds they are non-sortal. Source-specified categories are `gufo:RoleMixin`: membership holds only while a source statement specifies it, so an individual can cease to fall under the category without ceasing to exist when the norm is revoked or amended. Executive Order 13166, revoked by Executive Order 14224 section 3(b), is the worked case. Research-curated categories are `gufo:Mixin`, the weakest rigidity commitment gUFO offers, because no source fixes their membership. gUFO makes anti-rigid and semi-rigid types disjoint, so no category can be both; an inconsistency fixture tests this.

A category's subtype (normatively defined, statistically defined, normatively constituted, operationalized) is not asserted. The reasoner derives it, and the source-specified and role-mixin status, from the category's link to a source statement.

## 8. Source status relative to the corpus

Each curated category carries one `ana:TargetCategorySourcingAssessment` at the reference date 2026-08-27: whether the corpus contains a source statement for it, whether one specifies membership, and whether the specifying source was in force. "No source statement identified" is relative to the collected corpus. Validity is asserted only where the corpus documents it; otherwise it is recorded as not assessed. The force of all nine membership-specifying sources was checked; the six related-only categories carry no validity judgement.

See `ontological_commitments.csv` for reviewer-facing term-level commitments.
