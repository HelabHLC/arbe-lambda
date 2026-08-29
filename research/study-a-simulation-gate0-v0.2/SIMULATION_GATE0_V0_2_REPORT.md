# Simulation Gate 0 v0.2 report

> **SIMULATED DATA — METHOD VALIDATION ONLY — NOT EMPIRICAL EVIDENCE**

Status: `GATE_0_V0_2_PASSED — CORE DESIGN QUALIFIED`

Date: 2026-08-29

## Scope

The authorised restart evaluated the linear/Gaussian/ICC=0.10 core design under
Simulation Protocol v0.2. Each of 12 cells used 250 Monte Carlo replicates:
S0, S1 and S2 at N=100, 400, 800 and 1,600 references.

The injected recoverable effects were 15% for H1 and 5% for H3, both above the
unchanged empirical decision boundaries of 10% and 2% respectively.

## Recovery result

| N | Truth | Correct recovery | Mean observed H1 | Mean observed H3 |
|---:|---|---:|---:|---:|
| 100 | S0 | 100.0% | −5.34% | −6.75% |
| 100 | S1 | 62.8% | 19.60% | −5.41% |
| 100 | S2 | 39.2% | 15.82% | 10.69% |
| 400 | S0 | 100.0% | −1.19% | −1.52% |
| 400 | S1 | 71.2% | 14.29% | −1.20% |
| 400 | S2 | 41.2% | 12.74% | 5.46% |
| 800 | S0 | 100.0% | −0.61% | −0.61% |
| 800 | S1 | 86.4% | 14.27% | −0.69% |
| 800 | S2 | 64.0% | 13.71% | 4.88% |
| 1,600 | S0 | 100.0% | −0.30% | −0.29% |
| 1,600 | S1 | 93.2% | 14.59% | −0.29% |
| 1,600 | S2 | 81.2% | 13.78% | 4.90% |

## Calibration result

At N=1,600 the mean recoverable calibration was:

- H1 global: 15.0000%;
- H3 topology: 5.0000%.

The independent test observations remained close: 14.59% for S1 H1 and 4.90%
for S2 H3. Oracle, recoverable and observed effects were kept separate.

## Null control

Across 1,000 S0 replicates, no H1 false positive occurred. The observed Gate 0
null false-positive rate was 0%. This result is descriptive at 1,000 replicates
and does not replace the full permutation calibration required by the protocol.

## Gate decision

The prespecified Gate 0 requirements were met at the largest feasible N:

- S1 recovery at N=1,600: 93.2% ≥ 80%;
- S2 recovery at N=1,600: 81.2% ≥ 80%;
- null false-positive rate: 0% ≤ 7.5%.

`gate_pass = true`

## Interpretation boundary

This qualifies the implementation only for the linear/Gaussian/ICC=0.10 core
design. It does not establish power under nonlinear or sparse signals,
heavy-tailed, heteroscedastic or contaminated noise, ICC=0.00 or ICC=0.30,
bootstrap coverage or permutation calibration.

It provides no evidence for or against the real ARBE effect and does not
authorise the empirical confirmatory run.

## Next gate

The next simulation stage may evaluate the complete prespecified signal,
noise and ICC grid with bootstrap and permutation inference. Outputs remain
simulation-only and require a separate execution manifest.
