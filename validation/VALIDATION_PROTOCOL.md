# Validation protocol

CDSG separates structural audit, query regression, constraint validation, logical reasoning and foundational-ontology well-formedness. A pass in one layer is not evidence for another. All gates below were executed for rc.2; their logs are in `validation/results/` and the tool versions in `external_dependencies.lock.csv`.

## Gate A: structural audit

```bash
python validation/scripts/run_quality_audit.py > validation/results/quality-audit-run.txt
```

Checks parsing, module imports, the merged graph against the module union, cardinalities, disjointness, labels and definitions, evidence completeness and dangling references to undescribed individuals.

## Gate B: OWL 2 DL profile and HermiT

```bash
bash validation/run_robot_release_gate.sh validation/external/robot.jar > validation/results/robot-release-gate.txt
```

ROBOT 1.9.10 with the catalog `validation/catalog-v001.xml`, which resolves the gUFO import to `validation/external/gufo.owl`. The script checks the OWL 2 DL profile of the core and the merged graph, runs HermiT on both, writes the inferred class assertions of the merged graph and of the positive fixture, and requires all four inconsistency fixtures in `validation/reasoning/` to be reported inconsistent.

```bash
python validation/scripts/check_reasoning_fixture.py > validation/results/reasoning-fixture-check.txt
```

Evaluates the positive-inference, evidence-set classification and non-entailment tests against the HermiT output.

## Gate C: SHACL

```bash
python validation/scripts/run_shacl.py --gufo-shapes validation/external/gufoshapes.ttl > validation/results/shacl-run.txt
python validation/scripts/run_gufo_shape_preflight.py > validation/results/gufo-preflight-run.txt
```

pySHACL 0.40.1 validates the merged graph against the CDSG shapes and against the vendored gUFO shapes, the latter both on the asserted graph and on the graph with the HermiT class assertions. The preflight repeats the gUFO checks in plain Python as a cross-check.

## Gate D: competency questions

```bash
python validation/scripts/run_cq_baseline.py > validation/results/cq-baseline-run.txt
```

Checks each answer against the expectations in `validation/expected/cq_expected.json`, which were fixed from the source analysis (row counts and rows that must appear), and separately against the stored normalized SHA-256 digest. A query with the header `# entailment: hermit` runs over the asserted graph plus `results/merged-inferred-class-assertions.ttl`, so Gate B must run first.

## Gate E: publication

```bash
python publication/check_redirects.py
sha256sum -c SHA256SUMS.txt
```

Checks that every CDSG IRI resolves through the w3id rules to a file in the package and that the package matches its checksum manifest.

## Order and reporting

Run A, B, C, D, E in that order after any change, then `validation/scripts/regenerate_release_docs.py` and the checksum manifest. Report tool name, version, command, whether imports were resolved and whether entailment was used.
