# Simulation Protocol v0.2 changelog

Version 0.2 responds to the failed Gate 0 qualification in PR #13.

## Changed

- Separates oracle, recoverable and observed effects.
- Calibrates the requested effect against fitted-model performance on an
  independent calibration partition.
- Fixes calibration/training/test reference allocation at 20/60/20.
- Treats H1=10% and H3=2% as boundary-characterisation cells.
- Moves formal power evaluation above the decision boundaries:
  H1 at 12.5%, 15% and 20%; H3 at 3%, 5% and 7.5%.
- Requires at least 250 Gate 0 replicates per cell.
- Adds partition-isolation and A1/A2 non-leakage tests.
- Uses new, non-overlapping seed streams.

## Unchanged

- S0/S1/S2 truth structure.
- Null-control and false-positive requirements.
- Noise, signal-family and reference-ICC families.
- Mandatory simulated-data labelling.
- Study A empirical decision thresholds.
- Empirical confirmatory-run lock.

No real or simulated favourable outcome motivated a threshold relaxation. The
revision corrects a calibration and power-definition defect exposed by the
failed Gate 0 run.
