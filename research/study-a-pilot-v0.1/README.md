# Study A pilot — structural information gain

Status: `PILOT_PIPELINE_CHECK_NOT_CONFIRMATORY`

This pilot tests whether global ARBE λ* descriptors and reflectance-difference
topology add out-of-sample information beyond a D50 colourimetric baseline for
predicting pairwise illuminant instability.

It does **not** validate the research hypothesis. Analysis choices were made
while constructing the pilot and therefore precede neither preregistration nor
a locked holdout. Predictors and endpoints also derive from the same atlas
spectra. Independent measured samples remain mandatory for physical or
industrial claims.

## Frozen inputs

- FP index: `arbe_fp_index_v1`, 13,283 records, 36 values from 380–730 nm / 10 nm
- FP index SHA-256: `2c0682593d09fb5c83884f788e8dbfa8c570380a9a637461d63af7b6830131e0`
- Source URL: `https://arbe-lambda-star.com/wp-content/plugins/arbe-fp-illuminant/assets/arbe_fp_index.json`
- Observer: CIE 1931 2°
- Illuminants: D50 baseline; D65, A, LED-B1 and F11 alternatives
- Weight-table hashes are recorded in `study_a_pilot_result.json`

## Deterministic design

1. Assign each reference to one of five folds by SHA-256 of its reference name.
2. Construct K=10 nearest D50-Lab neighbour pairs inside each fold only.
3. Define the pilot endpoint as the maximum alternate-illuminant pair ΔE00
   minus the D50 pair ΔE00.
4. Tune ridge regularisation only on the four training folds.
5. Evaluate once on the held-out reference fold.

## Pilot result

| Model | Mean MAE | Mean R² | MAE reduction vs M1 |
|---|---:|---:|---:|
| M1 colourimetry | 0.3410 | 0.1444 | 0.00% |
| M2 + global ARBE | 0.2863 | 0.3684 | 16.05% |
| M3 + topology | 0.2877 | 0.4461 | 15.65% |

The global descriptors produced a consistent pilot gain over the linear
colourimetric model. Topology raised mean R² further but did not improve mean
MAE over M2. This mixed result must be retained, not simplified into a blanket
success claim.

## Run

```bash
python study_a_pilot.py \
  --index inputs/arbe_fp_index.json \
  --weights-dir inputs \
  --output study_a_pilot_result.json

python -m unittest test_study_a_pilot.py -v
```

The weights directory must contain `weights_{ILLUMINANT}_1931.json` for D50,
D65, A, LEDB1 and F11, obtained from the public ARBE weights endpoint. Verify
all hashes before analysis.

## Required next step

Freeze Protocol v0.2 before any confirmatory rerun. It must strengthen the
colourimetric comparator, preregister topology encoding and pair strata, add
reference-level bootstrap uncertainty and reserve a genuinely untouched
holdout or external measured cohort.
