# ATLAS Clarus × ARBE λ* — Study A Protocol v0.2

Status: `LOCK_CANDIDATE — NO CONFIRMATORY RUN AUTHORISED`

Date: 2026-08-29

## 1. Purpose and non-claim

This protocol tests whether global ARBE descriptors and reflectance-difference
topology add reproducible predictive information beyond strong colourimetric
comparators. It does not claim physical causality, industrial validation,
spectral reconstruction from RGB, or replacement of established colourimetry.

PR #9 is a disclosed pilot used to verify the pipeline. Its results shall not be
treated as confirmatory evidence and shall not be used to alter success
thresholds after this protocol is locked.

## 2. Confirmation boundary

The pilot evaluated all 13,283 atlas references. Therefore no subset of that
atlas can honestly be called previously untouched.

Protocol v0.2 separates two evidence levels:

1. **Internal locked replication:** a new, prespecified analysis of the frozen
   atlas with reference-disjoint validation. This tests reproducibility inside
   the atlas but is not a pristine holdout.
2. **External confirmatory holdout:** independently measured spectra that were
   unavailable during protocol development. Only this cohort may support an
   untouched-holdout claim.

No internal split may be relabelled as external confirmation.

## 3. Frozen atlas input

- Schema: `arbe_fp_index_v1`
- Records: 13,283 unique valid references
- Grid: 380–730 nm, 10 nm interval, 36 reflectance values
- Index SHA-256: `2c0682593d09fb5c83884f788e8dbfa8c570380a9a637461d63af7b6830131e0`
- Observer: CIE 1931 2°
- Baseline illuminant: D50
- Alternate illuminants: D65, A, LED-B1, F11
- Weight-table hashes: fixed in `analysis_plan_v0_2.json`

Any input-hash mismatch stops the run.

## 4. Units of analysis and leakage control

The atomic unit is the atlas reference. Pair records are derived units and may
not be split independently. All references in a pair must belong to the same
outer fold. A reference must never occur in both training and evaluation data
within an outer iteration.

Pair construction is deterministic: K=10 nearest eligible neighbours under
D50 ΔE00 inside each reference fold, followed by unordered-pair deduplication.
Counts shall be published by D50 ΔE00, hue, lightness, chroma and topology
strata. No small stratum may be silently removed because of low frequency.

## 5. Endpoint

Primary endpoint for pair AB:

`IIS_AB = max_i [ΔE00_AB(illuminant_i) − ΔE00_AB(D50)]`

where the alternate illuminants are D65, A, LED-B1 and F11.

Secondary endpoints:

- maximum alternate-illuminant pair ΔE00;
- binary high-instability status at thresholds fixed before execution;
- nearest-neighbour rank change across illuminants.

## 6. Predictor blocks

### B0 — minimal colourimetry

- D50 ΔE00 only.

### B1 — strong linear colourimetry

- ordered D50 Lab coordinates for A and B;
- absolute and signed ΔL*, Δa*, Δb*;
- C* and hue for each reference;
- ΔC*, wrapped Δh and D50 ΔE00;
- pair means and absolute differences.

### B2 — strong nonlinear colourimetry

The same B1 variables fitted with a prespecified nonlinear estimator. Candidate
estimators and tuning grids are fixed in the machine-readable analysis plan.
Selection occurs in inner reference-grouped folds only.

No alternate-illuminant Lab value, reflectance value or ARBE-derived value may
enter B0–B2.

### A1 — global ARBE extension

B2 plus absolute and signed pair differences in λ*_V2, λ*_EE, Δλ*, μ2, σ*,
μ3 and γ1.

### A2 — topology extension

A1 plus prespecified difference-curve features: sign-changing crossings,
equality nodes, AREAABSΔR, AREASIGNEDΔR, MAXABSΔR, RMSΔR and MEANABSΔR.

## 7. Validation and tuning

- Five deterministic reference-disjoint outer folds.
- Four grouped inner folds for estimator and hyperparameter selection.
- Preprocessing fitted on training data only.
- Outer-fold predictions written once to an append-only result artifact.
- No feature, threshold or estimator change after outcome inspection.

The internal replication compares B2 → A1 → A2. B0 and B1 are diagnostic
comparators and cannot substitute for B2.

## 8. Bootstrap uncertainty

Confidence intervals use 10,000 cluster-bootstrap replicates. Atlas references,
not pair rows, are resampled. A pair receives the product of the multiplicities
of its two references. The same replicate is applied to every compared model.

Report two-sided percentile 95% intervals for:

- paired MAE difference;
- paired RMSE difference;
- paired R² difference;
- relative MAE reduction.

Random seed: `20260829`.

## 9. Permutation control

Run 2,000 permutations. ARBE feature blocks are permuted at reference level
within the joint D50 hue × lightness × chroma stratum, then pair features are
recomputed. Colourimetric variables, targets, folds and pair membership remain
fixed. The p-value uses `(1 + exceedances) / (1 + permutations)`.

Permutation seed: `20260830`.

## 10. Confirmatory decisions

H1 (global ARBE information gain) passes internally only if A1 versus B2:

- reduces pooled out-of-fold MAE by at least 10%;
- has a 95% cluster-bootstrap interval for MAE improvement excluding zero;
- has permutation p < 0.05; and
- shows MAE improvement in at least four of five outer folds.

H3 (topology increment) passes internally only if A2 versus A1:

- reduces pooled out-of-fold MAE by at least 2%;
- has a 95% cluster-bootstrap interval for MAE improvement excluding zero;
- has permutation p < 0.05; and
- does not materially worsen calibration or any prespecified major stratum.

An R² gain without the required MAE gain is reported as mixed evidence, not a
pass. Failure of H3 does not invalidate a possible H1 result.

These are internal-atlas decisions. External confirmation additionally requires
the same directional comparisons on the new measured cohort, with thresholds
frozen in that cohort's acquisition plan before measurements are revealed.

## 11. Multiplicity and reporting

H1 is primary. H3 is tested only after H1 passes, creating a fixed gatekeeping
sequence. Secondary endpoints use Benjamini–Hochberg false-discovery control.
All folds, strata, negative results, mixed results, exclusions and run failures
shall be published.

## 12. External measured cohort gate

Before external confirmation begins, publish an acquisition manifest defining:

- independent sample source and inclusion criteria;
- instrument, geometry, calibration and repeatability checks;
- wavelength range, interval and interpolation policy;
- sample-size justification and exclusions;
- blinded reference identifiers;
- environmental and substrate conditions;
- locked analysis digest.

The external spectra must not be selected using knowledge of their ARBE
features or endpoint behaviour.

## 13. Protocol lock

The protocol and `analysis_plan_v0_2.json` are jointly locked by SHA-256 in
`PROTOCOL_LOCK.json`. Any amendment requires v0.3, a reason, a timestamp and a
statement declaring whether outcomes had been inspected. Protocol v0.2 does
not authorise the confirmatory run until the lock file and independent review
checklist are committed.
