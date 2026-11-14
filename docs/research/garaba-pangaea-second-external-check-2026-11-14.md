# ARBE λ*: Second external dataset check — Garaba et al. (PANGAEA 937105)

**Date:** 2026-11-14  
**Status:** Reproducible exploratory cross-sectional spectral analysis, **not** longitudinal validation or evidence of industrial diagnostic superiority.  
**Source:** Garaba et al. (2021), PANGAEA, https://doi.org/10.1594/PANGAEA.937105  
**Input file:** `Garaba-etal_2021_350-1000.tab`, original PANGAEA tabular export. Cite and observe the source's license for any redistribution.

## Objective and protocol

Independently check whether full-band ARBE V2, EE, and Delta can be calculated from real 1-nm reflectance spectra; compare groups descriptively; test whether the KLUM-derived slope limit transfers to this dataset. Do **not** infer a time-series from unrelated specimens or post-hoc sample matching.

Use 380–730 nm inclusive at 1 nm, reflectance fractions R(λ), trapezoidal integration:

- `V2 = 380 + ∫[380,730] R(λ) dλ` (nm)
- `EE = ∫[380,730] λR(λ)dλ / ∫[380,730] R(λ)dλ` (nm)
- `Delta = V2 - EE` (nm; signed)
- `mean reflectance = ∫R dλ / 350` (dimensionless)
- Observed max adjacent slope = `max(abs(R[i+1]-R[i]))` per nm.
- External comparison threshold `L=0.017072 /nm` from the earlier KLUM 10%-margin exercise. This is **not** a universal physical limit.

## Integrity and dataset structure

- **170/170** usable spectra; **nine** sample-label groups; no missing reflectance values in the selected 351 columns (380–730 nm).
- Raw export spans 350–1000 nm; the ARBE analysis does not extrapolate.
- Group labels distinguish `Virgin` and `Weathered` objects and `Dry`/`Wet` conditions; those labels are not controlled longitudinal observations of identical specimens.
- Recorded observations are from a short campaign on **2019-06-27**. No temporal aging trajectory can be inferred.

## Key group means (nm)

| Group | n | V2 | EE | Delta |
|---|---:|---:|---:|---:|
| PET_Bottles_Dry_Land | 29 | 488.875 | 561.896 | -73.021 |
| PET_Bottles_Floating_Water | 20 | 468.765 | 560.753 | -91.988 |
| LDPE_PMD_Dry_Concrete | 10 | 458.153 | 546.210 | -88.057 |
| LDPE_PMD_Dry_Grass | 20 | 448.756 | 542.971 | -94.215 |
| LDPE_PMD_Floating_Water | 20 | 422.271 | 534.027 | -111.756 |
| Blue_Boat_Land | 20 | 542.282 | 558.195 | -15.913 |
| Orange_Boat_Floating | 20 | 473.981 | 640.251 | -166.270 |
| Asphalt_Dry | 11 | 414.592 | 568.600 | -154.008 |
| Concrete_Klinker_Dry | 20 | 427.025 | 578.255 | -151.230 |

The PET dry-vs-wet **group mean** difference in Delta is approximately -18.97 nm, versus -1.14 nm in EE. These are descriptive differences, **not** a paired causal wetting effect or proof of independent information beyond V2 and EE.

## Negative results and limits

- **11/170** measured spectra exceed the previously used KLUM slope threshold `0.017072 /nm`; largest observed adjacent-point slope `0.02105 /nm`.
- The slope threshold is not a universally transferable material constraint.
- The dataset does **not** validate ARBE detection of reversals in a longitudinal aging sequence, distinguish contaminants, demonstrate superior diagnosis over conventional metrics, or certify incomplete-spectrum bounds.
- Delta is exactly derived from V2 and EE; it cannot contain independent information relative to the ordered pair (V2, EE). Its possible value is a useful monitoring/decision rule, which still requires a predefined endpoint and independent validation.
- No hypothesis test, uncertainty analysis or causal inference was performed; avoid using the group means as evidence of diagnostic sensitivity.

## Reproduction

The original `Garaba-etal_2021_350-1000.tab` plus `garaba_arbe_analysis.py` generate `Garaba_ARBE_170_Einzelwerte.csv` (individual values) and `Garaba_ARBE_9_Gruppen.csv` (group summaries). Python dependencies: pandas and numpy. The calculation script selects the 351 named `Refl (raw at N nm)` columns and integrates on a 1-nm grid. Keep the original PANGAEA metadata and source citation with derivative data.

## Research conclusion

This is the **second external data check** after the Morimoto 359-spectrum exercise. The positive result is independent numerical applicability to all 170 complete spectra and interpretable group differences. The negative result is 11 violations of the transferred KLUM slope assumption. Neither dataset provides a confirmed real longitudinal weathering series establishing incremental diagnostic benefit for Delta.
