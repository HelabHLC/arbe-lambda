# Simulation Gate 0 report

> **SIMULATED DATA — METHOD VALIDATION ONLY — NOT EMPIRICAL EVIDENCE**

Status: `GATE_0_FAILED — FULL GRID STOPPED`

Date: 2026-08-29

## Scope

Gate 0 tested the linear/Gaussian/ICC=0.10 implementation subset with 50 Monte
Carlo replicates in each of nine cells: S0, S1 and S2 at N=100, 400 and 800
references. It qualified code and recovery logic; it was not the full locked
simulation grid.

## Result

| N | Truth | Correct recovery | Mean H1 MAE gain | Mean H3 MAE gain |
|---:|---|---:|---:|---:|
| 100 | S0 | 100% | −2.36% | −1.93% |
| 100 | S1 | 0% | 4.02% | −2.12% |
| 100 | S2 | 2% | 4.67% | 0.17% |
| 400 | S0 | 100% | −0.86% | −0.60% |
| 400 | S1 | 8% | 6.90% | −0.89% |
| 400 | S2 | 0% | 6.58% | 0.66% |
| 800 | S0 | 100% | −0.39% | −0.43% |
| 800 | S1 | 0% | 6.96% | −0.40% |
| 800 | S2 | 0% | 7.09% | 1.08% |

The null was controlled in this small qualification run: all 150 S0 replicates
remained null decisions. Recovery of injected threshold effects failed.

## Diagnosis

Two distinct issues must not be conflated:

1. **Oracle-to-model attenuation.** Injection calibration targeted oracle MAE
   reduction, but the fitted model recovered only about 7% of an injected 10%
   global effect and about 1% of an injected 2% topology effect at larger N.
   Calibration must target realised out-of-sample model effect or explicitly
   report oracle and recoverable effects separately.
2. **Threshold-at-truth problem.** Requiring an estimated improvement of at
   least 10% when the true recoverable effect is exactly 10% cannot generally
   yield 80% pass probability. The same problem applies to a 2% topology truth
   paired with a 2% decision threshold. Power should be evaluated above the
   decision boundary, while boundary cells estimate classification behaviour.

## Decision

`gate_pass = false`. The full simulation grid was not started.

No empirical inference follows. The result does not count against or in favour
of ARBE. It tests only the proposed method-validation machinery.

## Required amendment before restart

Simulation Protocol v0.2 should:

- distinguish injected oracle effect from recoverable model effect;
- calibrate effects on an independent simulation-only calibration split;
- treat exact-threshold cells as boundary-characterisation cells, not 80%
  power requirements;
- define power targets at effects strictly above the decision threshold;
- add explicit tests that S1 signal cannot leak into A2 and vice versa;
- retain the successful null-control test;
- repeat Gate 0 with at least 250 replicates per cell after implementation tests.

Study A Protocol v0.2 remains unchanged and the empirical confirmatory run
remains unauthorised. Any change to its success thresholds would require a
separate transparent Protocol v0.3 amendment and independent review.
