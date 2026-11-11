# ARBE λ* — Exploratory Characterization of PETa Weathering Using Measured Reflectance Spectra

**Status:** Research draft for technical review; not peer reviewed.  
**Date:** 11 November 2026.  
**Source:** Leone et al., marine-plastics hyperspectral dataset, original DOI [10.14284/530](https://doi.org/10.14284/530), updated DOI [10.14284/750](https://doi.org/10.14284/750). Dataset version, authorship and redistribution conditions require final confirmation.

## Abstract

This exploratory case study tests whether ARBE λ*V2, λ*EE and Δλ* provide an interpretable, compact description of real PETa reflectance changes after dry weathering. Correctly separated pristine and dry-weathered groups are analyzed over 380–730 nm and compared with conventional spectral methods. Simulated independent measurement noise probes numerical sensitivity. ARBE describes changes but **does not demonstrate superior classification or new independent spectral information**.

## Mathematical definitions

For reflectance R(λ) on [380,730] nm:

- **λ*V2 = 380 nm + ∫₃₈₀⁷³⁰ R(λ)dλ**; algebraically equal to 380 nm + 350 nm × mean reflectance. The ARBE balance-equation zero is equivalent; the project's normative root solver may use Brent's method.
- **λ*EE = (∫₃₈₀⁷³⁰ λR(λ)dλ)/(∫₃₈₀⁷³⁰ R(λ)dλ)**; equal to the conventional reflectance-weighted spectral centroid for identical limits and weighting.
- **Δλ* = λ*V2 − λ*EE**.

Trapezoidal integration was used. These three values contain **two independent scalar quantities**.

## Data, grouping and scope

The broader exploratory subset includes PE, PETa, PETc, PP and PS. The corrected pristine-versus-dry subset comprises **129 measured spectra summarized into 25 measurement groups** (two pristine and three dry-weathered groups per polymer). Dry, seawater, dry-dark-control and seawater-dark-control treatments were separated, not pooled. This PETa case study compares only pristine and dry-weathered groups.

Available metadata do **not** establish independent specimens or matched before/after pairs. Group comparisons must not be interpreted as causal paired measurements.

## PETa results

Dry-weathered minus pristine, computed from equally weighted group-mean spectra:

| Descriptor | Change |
| --- | ---: |
| λ*V2 | **+41.2109 nm** |
| λ*EE | **−4.3514 nm** |
| Δλ* | **+45.5622 nm** |

The weathered PETa mean has higher reflectance at each of the 351 wavelengths examined, with a nonuniform wavelength-dependent increase (difference **0.0484614–0.1267020 reflectance units**). λ*V2 captures the integrated rise; λ*EE captures a smaller centroid shift toward shorter wavelengths; Δλ* summarizes their signed difference. This is descriptive evidence, not an independent weathering-detection validation.

## Exploratory comparison with classical analysis

Identical leave-one-group-out nearest-centroid evaluation on the corrected 25 groups:

| Method | Correct classifications |
| --- | ---: |
| Classical normalized full spectral shape | **24 / 25 (96%)** |
| ARBE λ*V2 + λ*EE + Δλ* | **20 / 25 (80%)** |

These are small, within-dataset exploratory results, **not** externally validated predictive accuracies. The full spectrum has much greater information capacity; group independence, model selection and prospective blinding are unresolved. **No ARBE classification advantage was observed.**

## Simulated measurement noise

For each reflectance-noise SD **0.002, 0.010, 0.030**, 3,000 Monte Carlo perturbations were applied using independent Gaussian noise across wavelengths. Both clipped-to-[0,1] and unclipped versions were calculated. Under the clipped model, Δλ* remained positive for the tested perturbations, while the small negative λ*EE change showed about **13.8% sign reversals** at SD 0.030. These simulations are **not** measured instrument repeatability: real noise may be correlated, wavelength-dependent or systematically biased; clipping can introduce bias. Specimen-sampling uncertainty is not included.

## Independent arithmetic check

An independent endpoint-half-weighted integration over the 351-point 1-nm grid reproduced stored λ*V2 and λ*EE values for all 25 corrected groups within **1e−8 nm**. The PETa change estimates above were reproduced. Stored classification totals were checked, but the classification algorithm and Monte Carlo simulations were **not** independently rerun. This is an arithmetic check, not an independent experimental replication.

## Interpretation and limitations

ARBE's possible value is a standardized, compact, signed description of average reflectance and centroid displacement. Compare its interpretability with classical mean reflectance and centroid side by side. Δλ* can emphasize opposing changes or conceal compensating ones. The current data do not establish chemical mechanisms, measurement superiority, industrial diagnostic utility or generalization.

Next requirements: specimen identifiers and treatment audit; independent repeated laboratory measurements and instrument geometry; correlated-noise models; uncertainty across independent specimens; preregistered validation across additional polymers and degradation mechanisms.

## Reproducibility and licensing gate

- [ ] Confirm exact updated dataset citation, version and redistribution rights.
- [ ] Audit specimen independence and treatment labels against original source.
- [ ] Add clean-environment code, dependency versions and checksums.
- [ ] Independently rerun classification and Monte Carlo tests.
- [ ] Publish dataset-derived plots or raw spectral rows **only after licensing clearance**.
- [ ] Retain explicit distinctions between arithmetic checks, simulated uncertainty and independent validation.

**This draft intentionally includes no original spectral rows or dataset-derived figures pending licensing review.**

**Bottom line:** PETa illustrates ARBE's compact description of measured spectral changes. It does not establish additional independent information, superior classification or industrial validation.
