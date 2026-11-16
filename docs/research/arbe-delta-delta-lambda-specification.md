# ARBE longitudinal ΔΔλ* and optional ε classification — proposed specification

Status: **proposed mathematical extension**, not a validated material-diagnostic method. This document does not change the existing ARBE Δλ* implementation.

## 1. Scope and definitions

For reflectance R(λ) in [0,1] over a fixed interval [a,b] (default a=380 nm, b=730 nm), with positive integrated reflectance:

- Mean reflectance: R̄ = (1/(b−a)) ∫[a,b] R(λ) dλ.
- λ*_V2 = a + (b−a) R̄, in nm. This is a linear rescaling of mean reflectance, **not** a reflectance-weighted centroid.
- λ*_EE = ∫[a,b] λ R(λ) dλ / ∫[a,b] R(λ) dλ, in nm.
- Δλ*(t) = λ*_V2(t) − λ*_EE(t), in nm. **Sign convention: V2 minus EE.**

For observations at ordered times t₀ < t₁ < …, define the signed interval change:

**ΔΔλ*_i = Δλ*(t_i) − Δλ*(t_{i−1}) [nm].**

Positive values indicate an increase in Δλ*, negative values a decrease, and zero no change in this descriptor. This is a descriptor trend, not necessarily the direction of a material's physical ageing or degradation. The same wavelength interval, sampling/integration method, and measurement conditions must be maintained or harmonized.

## 2. Direction reversal

An observed trend reversal between adjacent intervals occurs when ΔΔλ*_i and ΔΔλ*_{i+1} have opposite nonzero signs. A reversal is a change in the **slope direction of the sampled Δλ* trajectory**; it does not establish an underlying physical process reversal. Sampling may miss reversals between measurement times.

## 3. Optional noise-aware decision rule

Let ε_i ≥ 0 nm be a pre-specified, empirically calibrated threshold for interval i, reflecting uncertainty in ΔΔλ*_i.

- ΔΔλ*_i > +ε_i: positive change exceeding threshold.
- ΔΔλ*_i < −ε_i: negative change exceeding threshold.
- |ΔΔλ*_i| ≤ ε_i: direction **indeterminate under this decision rule** (not proof of zero change).

A threshold-qualified reversal requires two consecutive intervals classified with opposite signs. Equality with a threshold is indeterminate. ε=0 recovers strict mathematical sign classification but does **not** establish measurement reliability. The word 'statistically significant' is inappropriate without a defined probability model, calibration procedure and error criterion.

For D_i=Δλ*(t_i) and δ_i=D_i−D_{i−1}, the variance is

Var(δ_i) = Var(D_i) + Var(D_{i−1}) − 2 Cov(D_i,D_{i−1}).

Adjacent δ_i share D_i, so their errors are generally correlated. Any uncertainty model for reversal decisions should account for this dependence and for spectral channel covariance, instrumental drift and repeated-measurement conditions. A universal numerical ε is **not** specified here. Replicate measurements and an explicit false-positive criterion are required before an operational threshold is adopted.

## 4. Relationship to RMS

The conventional RMS spectral difference between two sampled spectra is nonnegative. Its magnitude alone does not encode the sign of the change in Δλ*. The signed ΔΔλ* answers a different, specifically defined question. This does **not** imply that directional information is absent from the original spectra or from other established signed statistics; it does not establish diagnostic superiority over RMS or other descriptors.

## 5. Implementation and validation status

The base Δλ* definition and its sign convention are already documented in the repository. This document **proposes** the longitudinal descriptor and ε decision rule; it does not assert that a production feature or empirically calibrated ε classifier exists. Synthetic mathematical tests can establish algebraic consistency and boundary behavior, but cannot validate material-specific diagnostic utility. Validation requires independent longitudinal spectra, replicate measurements, an uncertainty model, pre-specified endpoints and comparison against relevant baseline methods.

## 6. Minimal synthetic acceptance cases

Given successive Δλ* values [10, 12, 9] nm, the interval changes are [+2, −3] nm: a mathematical reversal. With ε=1 nm on both intervals, it is threshold-qualified. With ε=2 nm, the first interval is indeterminate (boundary equality), so no threshold-qualified reversal is declared. Given [10, 10, 9] nm, the first interval is zero and no adjacent-interval reversal is declared.

These are constructed descriptor values, **not experimental spectral measurements**.

## 7. References

- [Repository README and Δλ* sign convention](../../README.md)
- [CSV tool quickstart and uncertainty limitations](../tools/delta-csv-quickstart.md)
- [PET reproducibility and validation limits](pet-reproduction/README.md)
