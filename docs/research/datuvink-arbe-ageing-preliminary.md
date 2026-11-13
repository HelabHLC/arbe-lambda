# ARBE Δλ* — DATUVINK ink-ageing case study (preliminary)

**Status:** exploratory secondary analysis; independent replication pending.  
**Data source:** [DATUVINK, Mendeley Data, version 1](https://data.mendeley.com/datasets/7h8sntw548/1). Original raw data are **not redistributed** here.

## Research question

Can the ARBE difference descriptor reveal spectral changes that are small in the conventional reflectance-weighted centroid, and does it improve on established spectral metrics?

## Definitions (380–730 nm)

For reflectance fraction `R(λ)` (0–1), with integrals evaluated consistently on the measured wavelength grid:

```text
mean_R = integral(R(λ) dλ) / 350 nm
lambda_V2 = 380 nm + 350 nm * mean_R
lambda_EE = integral(λ R(λ) dλ) / integral(R(λ) dλ)
delta_lambda = lambda_V2 - lambda_EE
```

The V2 coordinate is a *defined mapping of mean reflectance* onto a wavelength scale; it is not a measured reflectance peak. The difference is a signed descriptor and contains no additional information beyond mean reflectance and centroid taken together.

## Exploratory findings reported from DATUVINK

Previous calculations on the supplied dataset associated four Bic blue-ink stages with the source's ageing experiment. The following are **reported, rounded preliminary calculations**, not independently verified in this PR:

| Bic blue ink | Stage 1 | Stage 4 | Difference |
|---|---:|---:|---:|
| Mean reflectance (fraction) | 0.1534 | 0.0752 | -0.0782 |
| λ*V2 (nm) | 433.69 | 406.33 | -27.36 |
| λ*EE (nm) | 557.02 | 556.97 | -0.05 |
| Δλ* (nm) | -123.33 | -150.65 | -27.32 |

Small inconsistencies in subtraction reflect rounding of displayed figures. The Bic observation illustrates that the centroid may remain nearly constant while mean reflectance, λ*V2 and Δλ* change substantially.

Exploratory analyses also reported directional Δλ* changes across five ink series (Bic, Milan, Paper Mate, Staedtler and Sierra IB-B). These observations **do not establish** superior detection over mean reflectance, RMS or full-spectrum metrics. In the examined cases, RMS and mean reflectance also detected changes.

## Interpretation and limitations

- These are real measured ink spectra, but the analysis is retrospective and exploratory.
- Different ageing stages correspond to different prepared samples; do not describe them as repeated longitudinal measurements of one physical mark.
- Stage 1 is not necessarily an unaged zero-hour baseline.
- Measurement noise experiments previously discussed were simulated, not instrument-characterized repeatability measurements.
- This case study does not establish a printing-press release benefit, independent scientific novelty, or a unique information gain of Δλ*.
- Full source data, metadata, preprocessing and the exact sample-to-time mapping must be independently audited before publication-grade claims.
- Charts derived as illustrative schematics must be labeled **“Schematic spectral illustration — not the original DATUVINK spectra.”**

## Reproduction checklist (pending)

1. Download the original DATUVINK files from the cited DOI/dataset page and record version and checksums.
2. Confirm the raw-column-to-ink/stage/time mapping against the paper or dissertation; document ambiguous labels.
3. Restrict spectra to 380–730 nm; record sampling interval and any smoothing or transformations.
4. Integrate consistently (including endpoint weighting); compare with the repository's `scripts/delta_lambda.py` and its tests.
5. Recalculate all per-stage descriptors and full-spectrum comparisons, including RMS and total variation with explicit definitions.
6. Establish uncertainty using instrument repeatability data when available; use prespecified decision criteria for any diagnostic claims.
7. Publish a reproducible script and derived results without republishing restricted raw data.

## References

- [DATUVINK original dataset](https://data.mendeley.com/datasets/7h8sntw548/1)
- [ARBE Δλ* calculation implementation](../../scripts/delta_lambda.py)
- [ARBE CSV evaluation quickstart](../tools/delta-csv-quickstart.md)

**Proposed claim:** “In an exploratory analysis of published ink-ageing reflectance spectra, ARBE Δλ* changed substantially in a Bic blue-ink comparison while the conventional centroid changed only slightly. This demonstrates complementary interpretation relative to centroid-only reporting, not superiority to established full-spectrum analysis.”
