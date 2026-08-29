# ATLAS Clarus × ARBE λ* — Power and Recovery Simulation Protocol v0.2

Status: `LOCK_CANDIDATE — RESTART NOT YET AUTHORISED`

Date: 2026-08-29

## 1. Purpose

This simulation validates the Study A decision procedure. It asks whether the
locked analysis can distinguish:

- `S0_NULL`: no incremental ARBE information;
- `S1_GLOBAL`: global Δλ* and moment information beyond colourimetry;
- `S2_TOPOLOGY`: topology information beyond global ARBE descriptors.

It does not estimate the real ARBE effect and cannot validate ARBE empirically.
Every table and figure must display:

> **SIMULATED DATA — METHOD VALIDATION ONLY — NOT EMPIRICAL EVIDENCE**

Version 0.2 responds to the failed Gate 0 run documented in PR #13. The failed
run and v0.1 remain immutable evidence. No favourable rerun is discarded.

## 2. Separation from existing work

- PR #9 remains the disclosed empirical pilot.
- Study A Protocol v0.2 remains the proposed empirical design.
- Reviewer Packet v0.2 remains the independent-review instrument.
- This protocol creates synthetic outcomes solely for power, error-rate,
  calibration and recovery assessment.

Simulation outputs may inform external-cohort sample-size planning. They may
not be used to change the locked H1/H3 success thresholds in Protocol v0.2
without a declared Protocol v0.3 amendment.

## 3. Empirical design matrix, synthetic outcome

The simulation may reuse the frozen atlas predictor geometry and deterministic
pair structure because realistic correlations are important. It must not use
the observed IIS outcome when generating synthetic outcomes or tuning effects.

Predictor blocks follow Protocol v0.2:

- `B2`: strong nonlinear D50 colourimetry;
- `A1`: global ARBE features after B2;
- `A2`: topology features after A1.

Incremental A1 signal is residualised against B2. Incremental A2 signal is
residualised against B2+A1. Residualisation is fitted within each simulation's
training partition. This prevents an injected topology effect from being only
a disguised global or colourimetric effect.

## 4. Scenario definitions

### S0 — Null

`y = f(B2) + reference effects + noise`

No A1 or A2 component is injected. The primary outputs are false-positive
rates for H1 and H3. H3 is evaluated through the locked gatekeeping rule and
also diagnostically conditional on an artificial H1 pass.

### S1 — Global

`y = f(B2) + g(A1 residual) + reference effects + noise`

No A2 residual component is injected. The required recovery pattern is H1
pass and H3 fail.

### S2 — Global plus topology

`y = f(B2) + g(A1 residual) + h(A2 residual) + reference effects + noise`

The required recovery pattern is H1 pass and H3 pass.

## 5. Effect grid

Injected incremental effects are calibrated to expected relative out-of-sample
MAE reduction against the immediately preceding comparator.

- Global A1 recoverable effect: 0%, 2%, 5%, 10%, 12.5%, 15%, 20% versus B2.
- Topology A2 recoverable effect: 0%, 1%, 2%, 3%, 5%, 7.5%, 10% versus A1.

The 10% global and 2% topology cells are decision-boundary cells. Formal power
targets apply only to the prespecified effects above those boundaries.

Three effects are recorded separately:

1. `oracle_effect`: improvement if the true injected component were known;
2. `recoverable_effect`: improvement achieved by the prespecified fitted model
   on an independent simulation-only calibration partition;
3. `observed_effect`: improvement on untouched simulation test references.

Calibration uses nested bisection on calibration references unavailable to
later training and test stages. The injected coefficient is adjusted until the
recoverable effect, not the oracle effect, is within ±0.5 percentage points of
the requested value. Oracle and recoverable effects are both retained. No
calibration uses observed IIS or final simulation-test outcomes.

For each replicate, references are assigned before outcome generation to
`CALIBRATION` (20%), `TRAINING` (60%) and `TEST` (20%) by a seeded hash. Pairs
are constructed inside one partition only. Calibration models and outcomes are
discarded before the blinded test analysis.

## 6. External-cohort size grid

The primary reference-count grid is:

`N = 100, 200, 400, 800, 1600`

References are sampled first; deterministic K-neighbour pairs are then formed.
Power is indexed by reference count, never by the much larger dependent pair
count. If a requested N exceeds an eligible stratum, sampling is balanced with
replacement and the duplication rate is reported.

N denotes the total references before the fixed 20/60/20 allocation. Power
tables additionally report the realised number of test references and pairs.

## 7. Signal functions

For each Monte Carlo replicate, coefficient directions are generated from a
fixed seeded orthonormal basis. Both linear and nonlinear signal families are
included:

- `LINEAR`: weighted standardised residual features;
- `SMOOTH_NONLINEAR`: spline-like monotonic and interaction terms;
- `SPARSE`: signal concentrated in 20% of eligible features.

The coefficient direction is sampled independently of the model fit and held
constant across B2/A1/A2 comparisons within a replicate.

## 8. Dependence and noise families

Pair outcomes share reference-level random effects. For pair AB:

`u_AB = u_A + u_B`, with reference intraclass contribution in
`ICC = 0.00, 0.10, 0.30`.

Noise families:

1. `GAUSSIAN`: homoscedastic normal noise;
2. `STUDENT_T5`: symmetric heavy-tailed noise;
3. `HETEROSCEDASTIC`: variance increases with the B2 signal magnitude;
4. `CONTAMINATED`: 95% Gaussian plus 5% observations at fourfold scale.

Noise is generated after signal calibration and standardised to a declared
total outcome variance. Negative synthetic outcomes are allowed because IIS
may be negative; no truncation is applied.

## 9. Analysis applied to each replicate

The replicate is analysed without knowledge of its scenario label using the
locked B2 → A1 → A2 ladder, grouped inner tuning and reference-disjoint outer
evaluation from Protocol v0.2.

For computational validation:

- screening stage: 1,000 reference-cluster bootstraps and 500 permutations;
- confirmation stage for boundary cells: the full 10,000 bootstraps and 2,000
  permutations required by Protocol v0.2.

Boundary cells are those within five percentage points of 80% or 90% estimated
power, all S0 cells, and all cells at the H1 10% or H3 2% decision thresholds.
Exact-threshold cells characterise the decision boundary and are not required
to attain 80% or 90% power.

## 10. Monte Carlo repetitions and stopping

Each design cell starts with 250 replicates. Gate 0 also uses at least 250
replicates per cell. Replicates are added in batches of
250 until either:

- the Wilson 95% half-width for the relevant pass probability is ≤0.02; or
- 2,000 replicates are reached.

S0 false-positive cells require at least 1,000 replicates regardless of the
precision rule. Monte Carlo standard errors and final replicate counts are
reported for every cell.

## 11. Recovery outcomes

Primary recovery classes:

| Truth | Correct decision |
|---|---|
| S0 | H1 fail; H3 not opened |
| S1 | H1 pass; H3 fail |
| S2 | H1 pass; H3 pass |

Report:

- complete 3×3 recovery/confusion matrix;
- H1 and H3 power;
- H1 familywise false-positive rate under S0;
- diagnostic H3 false-positive rate under S1;
- probability of R²-only mixed evidence;
- bootstrap interval coverage and mean width;
- permutation p-value uniformity under the relevant null;
- fold-consistency pass probability;
- selected-model and hyperparameter frequencies.

## 12. Method-validation criteria

The decision procedure is considered simulation-adequate only if:

- S0 H1 false-positive rate has a 95% Monte Carlo interval containing 0.05 and
  an upper bound ≤0.075;
- S1 diagnostic H3 false-positive rate has an upper bound ≤0.075;
- 95% bootstrap coverage is between 92.5% and 97.5% in all primary S0/S1 cells;
- recovery reaches at least 80% at one feasible reference count for H1
  recoverable effects of 12.5%, 15% or 20%;
- recovery reaches at least 80% at one feasible reference count for H3
  recoverable effects of 3%, 5% or 7.5%;
- no major noise family shows a recovery collapse exceeding 20 percentage
  points relative to Gaussian noise without explicit qualification.

Failure triggers method revision, not reinterpretation of simulated truth.

The exact H1 10% and H3 2% cells are reported as boundary-characterisation
cells. Their pass probability is descriptive and is not an adequacy criterion.

## 13. Sample-size recommendation

For each scenario and noise family report the smallest N achieving:

- at least 80% recovery power; and
- at least 90% recovery power.

The external acquisition recommendation uses the maximum required N across the
prespecified non-pathological noise families, increased by 15% for exclusions
and measurement failure. If no tested N reaches target power, report
`NOT_ESTIMABLE_WITHIN_GRID`; do not extrapolate silently.

## 14. Seeds and reproducibility

- master seed: `20260903`
- design-cell seeds: SHA-256 of canonical cell JSON plus master seed
- bootstrap seed stream: `20260904`
- permutation seed stream: `20260905`

Software versions, threads, floating-point platform, cell manifests, failures
and reruns are retained. A failed replicate may be rerun only with the same
seed after the implementation defect is documented.

## 15. Prespecified presentation

Required figures:

1. recovery confusion matrix by N;
2. H1 power curves by global effect and noise family;
3. H3 power curves by topology effect and noise family;
4. S0/S1 false-positive calibration plot;
5. bootstrap coverage plot;
6. sample-size decision table;
7. mixed-evidence frequency plot.

Figures use simulated truth labels and never reuse styling that could make them
indistinguishable from empirical results.

## 16. Lock and authorisation

This protocol and `simulation_plan_v0_2.json` are jointly locked in
`SIMULATION_PROTOCOL_V0_2_LOCK.json`. The lock authorises neither simulation
execution nor empirical confirmation. Execution requires implementation tests
for scenario recovery, effect calibration, reference-level dependence and
seed reproducibility.

Gate 0 restart additionally requires tests showing partition isolation,
recoverable-effect calibration within tolerance and absence of injected A1/A2
signal leakage. The Study A empirical decision thresholds remain unchanged.
