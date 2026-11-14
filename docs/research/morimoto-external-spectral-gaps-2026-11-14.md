# Morimoto external check of KLUM-derived ARBE spectral-gap bounds (2026-11-14)

**Status: exploratory external validation; negative assumption-transfer findings included. Not a certified global optimization or longitudinal weathering study.**

## Source and frozen test
Morimoto et al., Zenodo DOI 10.5281/zenodo.5217752, `Reflectance_v1-2.csv`. Source MD5: `958fe43bab12b62bc8df03b9c77bcd71`. File contains 399 rows, of which 359 have complete valid reflectance data at 380–730 nm (5 nm grid); 40 blank rows were excluded. 307 samples have `Used in analysis=True`; 52 are marked false. All 359 valid spectra were included.

The pre-existing KLUM 10%-safety analysis has two class-exclusion slope thresholds, 0.015763 and 0.017072 per nm. Because external samples have no KLUM material-class mapping, the **largest pre-existing threshold, L=0.017072 per nm**, was fixed for every Morimoto spectrum without calibration on Morimoto data. This choice must be stated when comparing to KLUM's class-specific analysis.

Primary analysis uses piecewise-linear interpolation of the 5 nm samples, the measured central band 400–700 nm, reflectance limits [0,1], and endpoint-based Lipschitz outer envelopes for unknown 380–400 and 700–730 nm bands. Trapezoidal integration is used. The EE bound is obtained by a fractional-ratio bisection over these envelopes; Delta bounds are conservative differences of V2 and EE bounds, **not** the joint global Delta optimizer.

## Results (359 valid spectra)
- Full-range observed 5 nm adjacent-point slope exceeds frozen L: **23/359 (6.41%)**.
- Observed slope exceeds L within masked edge bands: **15/359 (4.18%)**.
- Full-range slope criterion met: **336/359**; edge-band criterion met: **344/359**.
- Full-spectrum V2, EE and Delta values fall inside their corresponding conservative calculated intervals: **359/359 for each descriptor**.
- In the source's 307 `Used in analysis=True` rows: 22 full-range and 14 edge violations; in 52 `False` rows: 1 and 1.
- Strong counterexample: flower `Trifolium incarnatum`, source CSV row 142 (header counted as row 1), observed max adjacent-point slope **0.083300 per nm**, above L=0.017072.
- Violation categories: flowers 18, leaves 4, vegetables 1. No violations in bark, fruit or stone among the available samples.

**Interpretation:** The KLUM-trained slope limit does *not* universally transfer to natural-object reflectances. The observed 100% interval coverage does not repair the violated premise and cannot establish a universal guarantee. These data are independent external spectra, not matched longitudinal weathering pairs; **no change-direction or reversal detection rate is claimed**.

## Limitations
1. 5 nm grid and piecewise-linear model cannot constrain unmeasured sub-grid spectral features without additional assumptions.
2. The global frozen threshold was chosen as the maximum of KLUM's previously used class-specific safety thresholds; it is not an externally certified physical constant.
3. The external Delta bounds are conservative, not sharp jointly optimized or formally certified.
4. No uncertainty model for instrument noise and no validated time-series pairings.
5. Reproduce using the source CSV and local script `morimoto_external_validation.py`; retain all failures rather than exclude them post hoc.

## Research decision
Publish as a **mixed, falsifiable exploratory external check**. Do not claim an independently validated universal Lipschitz assumption, industrial benefit, or certified sharp Delta bounds. Next steps: assess physically justified class-specific priors and test the joint Delta optimizer on independent spectra under explicit solver error bounds.
