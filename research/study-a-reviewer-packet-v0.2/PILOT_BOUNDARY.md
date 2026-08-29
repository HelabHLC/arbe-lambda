# Pilot boundary and contamination statement

## What the pilot did

PR #9 ran a disclosed pipeline check over all 13,283 atlas references and
78,702 deterministic reference-disjoint neighbour pairs. It compared a linear
colourimetric model with global ARBE and topology extensions.

Pilot summary:

| Model | Mean MAE | Mean R² | MAE reduction vs pilot M1 |
|---|---:|---:|---:|
| M1 colourimetry | 0.3410 | 0.1444 | 0.00% |
| M2 + global ARBE | 0.2863 | 0.3684 | 16.05% |
| M3 + topology | 0.2877 | 0.4461 | 15.65% |

## What the pilot did not establish

- It was not preregistered before analysis choices were made.
- Its colourimetric comparator was not the final strong nonlinear baseline.
- Predictors and endpoint were derived from the same atlas spectra.
- It did not provide a previously untouched holdout.
- It did not use independently measured physical samples.
- It did not establish physical causality or industrial validity.

## Consequence for Protocol v0.2

Every atlas reference has been indirectly exposed to pilot analysis. Therefore
no atlas subset may be described as a pristine or untouched holdout. The locked
atlas analysis is an internal replication only. A true confirmatory holdout
requires a newly acquired, independently measured cohort unavailable during
protocol development.

Reviewers should assess whether Protocol v0.2 sufficiently prevents favourable
pilot findings from determining the confirmatory design.
