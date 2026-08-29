# Standardised methodological review checklist

For each item mark `PASS`, `MINOR`, `MAJOR`, `NOT APPLICABLE`, or
`INSUFFICIENT INFORMATION`, and cite the relevant protocol section.

## A. Reviewer independence

- [ ] A1 Reviewer identity, affiliation and relevant expertise are recorded.
- [ ] A2 The reviewer did not author Protocol v0.2 or the pilot analysis.
- [ ] A3 Financial, professional and intellectual conflicts are disclosed.
- [ ] A4 The reviewer received no unpublished confirmatory outcomes.
- [ ] A5 Any prior relationship with the project is described.

## B. Integrity and provenance

- [ ] B1 Package hashes verify.
- [ ] B2 Protocol and analysis-plan hashes match `PROTOCOL_LOCK.json`.
- [ ] B3 Atlas schema, record count, spectral grid and input hash are explicit.
- [ ] B4 Observer, illuminants and weighting-table hashes are explicit.
- [ ] B5 Hash mismatch produces a hard stop.
- [ ] B6 Data licensing and source provenance are sufficient for the study.

## C. Research question and claims

- [ ] C1 The primary question is scientifically testable.
- [ ] C2 Informational utility is distinguished from physical causality.
- [ ] C3 No RGB-to-spectrum reconstruction claim is implied.
- [ ] C4 Internal replication and external confirmation are clearly separated.
- [ ] C5 The pilot contamination boundary is complete and candid.

## D. Units, pairs and leakage

- [ ] D1 The atlas reference is correctly treated as the atomic unit.
- [ ] D2 Pair rows cannot leak reference identity across folds.
- [ ] D3 Pair construction is deterministic and reproducible.
- [ ] D4 Deduplication and K-neighbour handling are unambiguous.
- [ ] D5 Pair dependence is addressed in estimation and uncertainty.
- [ ] D6 Rare or small strata cannot be silently discarded.

## E. Endpoint validity

- [ ] E1 IIS is fully specified and reproducible.
- [ ] E2 The choice of D50 and alternate illuminants is justified.
- [ ] E3 The endpoint is not a direct algebraic restatement of a tested feature.
- [ ] E4 Negative IIS values and ties have a prespecified treatment.
- [ ] E5 Secondary endpoints and thresholds are fixed before use.
- [ ] E6 Circularity risks are adequately disclosed and controlled.

## F. Colourimetric comparators

- [ ] F1 B0, B1 and B2 are defined without ARBE or reflectance leakage.
- [ ] F2 B2 is strong enough to represent a fair nonlinear comparator.
- [ ] F3 Estimator candidates and tuning grids are fixed.
- [ ] F4 Hyperparameter selection occurs only within grouped inner folds.
- [ ] F5 Preprocessing is trained inside each training partition.
- [ ] F6 Model capacity is sufficiently comparable across B2, A1 and A2.

## G. ARBE and topology blocks

- [ ] G1 λ*_V2, λ*_EE, Δλ*, μ2, σ*, μ3 and γ1 are fully defined.
- [ ] G2 Signed versus absolute pair features are prespecified.
- [ ] G3 Crossing and equality tolerances are numerically fixed.
- [ ] G4 Interpolation at crossings is prespecified or explicitly excluded.
- [ ] G5 AREAABSΔR, AREASIGNEDΔR, MAXABSΔR, RMSΔR and MEANABSΔR are reproducible.
- [ ] G6 Feature scaling and missing-value rules are fixed.

## H. Validation and uncertainty

- [ ] H1 Outer folds are reference-disjoint and deterministic.
- [ ] H2 Inner folds preserve reference grouping.
- [ ] H3 Outer predictions are written once and retained.
- [ ] H4 The 10,000-replicate bootstrap resamples references, not pair rows.
- [ ] H5 Pair weighting under repeated bootstrap references is valid.
- [ ] H6 Confidence-interval construction is appropriate.
- [ ] H7 Fold-level heterogeneity and major strata are reported.

## I. Permutation test

- [ ] I1 Permutation occurs at reference level.
- [ ] I2 Colourimetric strata are defined before execution.
- [ ] I3 Pair features are recomputed after permutation.
- [ ] I4 Targets, folds and pair membership remain fixed.
- [ ] I5 The test statistic and exceedance rule are explicit.
- [ ] I6 Two thousand permutations provide adequate resolution.

## J. Decisions and multiplicity

- [ ] J1 H1 is primary and its success rule is complete.
- [ ] J2 H3 is conditional on H1 and tested against A1, not B0/B1.
- [ ] J3 MAE effect-size thresholds are scientifically defensible.
- [ ] J4 R²-only improvement is correctly classified as mixed evidence.
- [ ] J5 Multiplicity handling is adequate.
- [ ] J6 Negative, null, mixed and contradictory results must be published.
- [ ] J7 No post-hoc rescue path remains unspecified.

## K. External measured cohort

- [ ] K1 The external cohort is genuinely unavailable during protocol development.
- [ ] K2 Sample acquisition cannot be conditioned on ARBE or expected outcomes.
- [ ] K3 Instrument, geometry, calibration and repeatability will be recorded.
- [ ] K4 Sample-size justification is required before measurement disclosure.
- [ ] K5 Blinding, exclusions and environmental conditions will be locked.
- [ ] K6 Spectral interpolation and wavelength compatibility are prespecified.
- [ ] K7 External success criteria will be locked before outcomes are revealed.

## L. Reproducibility and governance

- [ ] L1 Software versions, seeds and deterministic settings will be recorded.
- [ ] L2 Intermediate manifests and exclusions are preserved.
- [ ] L3 The analysis can be independently rerun from frozen inputs.
- [ ] L4 Protocol amendments require a new version and outcome-awareness statement.
- [ ] L5 Confirmatory execution remains technically unauthorised at review time.
- [ ] L6 An independent reviewer can identify who may unlock the run and on what evidence.

## Mandatory synthesis

- [ ] S1 List every `MAJOR` finding.
- [ ] S2 List every unresolved `INSUFFICIENT INFORMATION` item.
- [ ] S3 State whether Protocol v0.2 can answer H1.
- [ ] S4 State whether Protocol v0.2 can answer H3 independently of H1.
- [ ] S5 State whether the external cohort design can yield an untouched holdout.
- [ ] S6 Select exactly one final decision class.
