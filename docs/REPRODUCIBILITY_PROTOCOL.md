# Reproducibility protocol

## Required artifacts

The package archives the ontology modules, the data module, the shapes, fixtures, queries, expected baselines, the vendored gUFO and gUFO shapes, the logs of the release run and the checksum manifest. Tool versions and upstream revisions are in `validation/external_dependencies.lock.csv`.

## Execution order

1. Verify `SHA256SUMS.txt`.
2. Install `validation/requirements-validation.txt` in a clean Python environment and place ROBOT 1.9.10 at `validation/external/robot.jar`.
3. Run Gates A to E of `validation/VALIDATION_PROTOCOL.md` in order.
4. Compare the new logs with `validation/results/`.

## Reporting rule

State tool name, version, command, whether imports were resolved through the catalog, whether entailment was used and the expected against the actual result. Do not report the plain-Python preflights as reasoner or pySHACL runs.
