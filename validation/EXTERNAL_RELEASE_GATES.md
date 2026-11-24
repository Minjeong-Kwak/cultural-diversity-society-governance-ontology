# Release gates

The gates in `VALIDATION_PROTOCOL.md` were executed for v1.0.0-rc.2 with the tools pinned in `external_dependencies.lock.csv`. Results and logs are in `validation/results/` and summarized in `cdsg_v1rc2_quality_report.md`.

For the final v1.0.0 release:

1. Install `requirements-validation.txt` and place ROBOT 1.9.10 at `validation/external/robot.jar`.
2. Run Gates A to E in order. Any failure blocks the release.
3. Regenerate the documentation, `MANIFEST.md` and `SHA256SUMS.txt` only after all gates pass.
4. Tag the repository and register the w3id redirects as described in `publication/README.md`.

`run_reasoner_owlready.py` and `run_local_baseline.py` belong to rc.1 and are obsolete; they exit with a pointer to the current scripts.
