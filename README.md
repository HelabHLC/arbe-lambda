ARBE λ*_V2
Formal Specification – Reference Definition (Version 1.0)

This repository defines the normative specification and deterministic reference implementation of λ*_V2 within the ARBE λ* framework.

λ*_V2 is a physical ordering parameter derived from measured reflectance spectra.
It represents the unique energetic balance point between absorption and reflection within the visible spectral interval.

1. Spectral Domain

Let R(λ) denote a physically measured reflectance spectrum with:

380 nm ≤ λ ≤ 730 nm

0 ≤ R(λ) ≤ 1

The computation SHALL be restricted strictly to the interval:

[380 nm, 730 nm]

No UV extension is part of this specification.

2. Formal Definition

Define the balance function:

𝑔
(
𝜆
)
=
∫
380
𝜆
(
1
−
𝑅
(
𝜆
′
)
)
 
𝑑
𝜆
′
−
∫
𝜆
730
𝑅
(
𝜆
′
)
 
𝑑
𝜆
′
g(λ)=∫
380
λ
	​

(1−R(λ′))dλ′−∫
λ
730
	​

R(λ′)dλ′

λ*_V2 is defined as the unique λ ∈ [380, 730] such that:

𝑔
(
𝜆
)
=
0
g(λ)=0

For physically valid, continuous reflectance spectra, this solution exists and is unique.

3. Numerical Determination (Normative)

The zero of g(λ) SHALL be computed using:

Brent–Dekker root-finding method

Requirements:

Deterministic algorithm

Bracketing within [380, 730]

Guaranteed convergence for continuous spectra

Declared numerical tolerance

Reproducible output

The following procedures are NOT equivalent to λ*_V2:

Energy centroids

Weighted means

CDF-based 50% points

Discrete summation heuristics

Linear balancing approximations

Such methods do not satisfy the balance equation definition.

4. Distinction from Related Metrics
4.1 λ*_EE (Equal-Energy Centroid)
𝜆
𝐸
𝐸
∗
=
∫
380
730
𝜆
𝑅
(
𝜆
)
 
𝑑
𝜆
∫
380
730
𝑅
(
𝜆
)
 
𝑑
𝜆
λ
EE
∗
	​

=
∫
380
730
	​

R(λ)dλ
∫
380
730
	​

λR(λ)dλ
	​


λ_EE is a reflected-energy centroid.
It is not identical to λ_V2.

4.2 Δλ*
Δ
𝜆
∗
=
𝜆
𝑉
2
∗
−
𝜆
𝐸
𝐸
∗
Δλ
∗
=λ
V2
∗
	​

−λ
EE
∗
	​


Δλ* describes spectral asymmetry and is a secondary descriptor.
It does not replace λ*_V2.

5. Scope

This repository serves as:

A formal scientific reference

A deterministic computational baseline

A reproducible implementation standard

It does NOT define:

A color space

A generative color model

Industrial thresholds

Device-specific control logic

Normative release criteria

6. Compliance Requirements

Implementations claiming conformity with ARBE λ*_V2 MUST:

Use measured reflectance spectra.

Restrict computation to 380–730 nm.

Apply deterministic Brent root-finding.

Declare numerical tolerance.

Ensure reproducibility.

Failure to meet these conditions constitutes non-conformity with the specification.

7. Citation

If used in research or applied analysis, please cite:

Woiwod, N. (2026).
Formal Specification of λ_V2 (ARBE λ*), Version 1.0.*

8. License

Code: MIT License
Specification text: CC-BY 4.0

λ*_V2 is defined as a physical ordering parameter derived from measured reflectance spectra.
It is not a perceptual coordinate, not a proprietary system, and not a generative model.

