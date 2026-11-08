# ARBE λ*_V2 — definition and mathematical clarification

Formal Specification 1.0, with a mathematical clarification dated **2026-11-08**.
The balance equation, 380–730 nm domain, current Δλ* sign, and Brent conformance
requirement below are retained. This clarification corrects the earlier claim
that all mean-based evaluations are mathematically inequivalent.

**Main result:** λ*_V2 is an exact affine encoding of unweighted mean reflectance.
It is not numerically the same quantity as dimensionless reflectance, but the
two contain exactly the same information on the fixed interval:

$$
\lambda^*_{V2}=380\,\mathrm{nm}+350\,\mathrm{nm}\,\overline R,
\qquad \overline R=\frac{\lambda^*_{V2}-380\,\mathrm{nm}}{350\,\mathrm{nm}}.
$$

**Deutsch:** Die Gleichwertigkeit nach dieser Umrechnung ist mathematisch
bewiesen. Gemeint ist das ungewichtete Integral-Mittel auf demselben Intervall,
nicht jeder beliebige Stichprobenmittelwert oder eine beleuchtergewichtete Größe.
Die historische Neuheit der konkreten Δλ*-Kombination ist damit weder bewiesen
noch widerlegt.

- [Proof, assumptions, noise, and counterexamples](docs/research/v2-mean-reflectance-identity.md)
- [Δλ*: novelty review, source history, and search limits](docs/research/delta-lambda-novelty-review-2026-11-08.md)
- [Machine-readable verification result](results/v2_identity_2026-11-08.json)
- [Repository roles and dataset release policy](docs/repository-roles-and-release-policy.md)

## Try your own spectra: three-step CSV quickstart

The [CSV research tool](scripts/delta_lambda_pipeline.py) evaluates one or more
reflectance spectra locally, without writing Python code. It reports area, mean
reflectance, centroid, λ*_V2 and Δλ*. Optional uncertainty propagation follows the
GUM first-order approach for **supplied reflectance errors at fixed wavelengths**;
this is not a full instrument uncertainty budget or an industrial validation.

**1. Download and install.** Install Python 3.12, [download the repository ZIP](https://github.com/HelabHLC/arbe-lambda/archive/refs/heads/main.zip),
extract it, and open a terminal in the extracted folder:

```bash
python -m pip install -r requirements-tools.txt
```

**2. Prepare your CSV.** Use `wavelength_nm` as the first column and one column
per spectrum. Include all measured wavelength rows, strictly increasing from
380 to 730 nm. Use decimal points and reflectance fractions from 0 to 1.
The [synthetic example](examples/delta_synthetic.csv) is a ready-to-run template;
it contains no measured material or HLC reference data.

**3. Run the calculation.** Replace `my_spectra.csv` with your input filename:

```bash
python scripts/delta_lambda_pipeline.py my_spectra.csv --output results.csv
```

For a first check, use `examples/delta_synthetic.csv` instead. The command writes
`results.csv` plus `results.json` with calculation settings and any supplied
uncertainty/covariance information. **Without uncertainty inputs, uncertainty
fields are blank in CSV and `null` in JSON: unknown, not zero.** The calculator
does not upload your spectra; after installing dependencies it runs offline.

[Full guide: CSV layout, percent units, uncertainty files, covariance and interpretation](docs/tools/delta-csv-quickstart.md).
The core uses the proved area identity for V2, not the separately prescribed
Brent–Dekker procedure. Historical threshold code and frozen specifications remain
separate. Mathematical equivalence does not imply a procedure-conformance claim.

## 1. Spectral domain and formal definition

Let $a=380\,\mathrm{nm}$, $b=730\,\mathrm{nm}$ and let $R(\lambda)$ be
dimensionless reflectance, with $0\leq R\leq1$. Implementations claiming
measurement conformance use measured reflectance spectra. Synthetic functions
are permitted as explicitly labelled mathematical test inputs.

The definition is

$$
g(x)=\int_a^x[1-R(\lambda)]\,d\lambda-\int_x^bR(\lambda)\,d\lambda,
\qquad g(\lambda^*_{V2})=0.
$$

Combining the integrals gives, exactly,

$$
g(x)=x-a-\int_a^bR(\lambda)\,d\lambda,
\qquad \lambda^*_{V2}=a+\int_a^bR(\lambda)\,d\lambda.
$$

Consequently $g$ has slope 1 and a unique root in $[a,b]$ for every integrable
$R$ in the stated range. Neither monotonicity nor continuity of $R$ is needed
for this theorem. This is a global integral balance, not a local crossing of
$R=1-R$, a spectral peak, or a dominant perceived wavelength.

Calling $1-R$ physical absorptance requires the appropriate energy accounting,
including negligible transmission and compatible reflection measurement. The
unweighted integral is not a measured radiant-energy integral under an arbitrary
illuminant. These physical qualifications do not change the algebraic identity.

## 2. Numerical determination and conformance

For compatibility with Formal Specification 1.0, implementations claiming
**Brent procedure conformance** SHALL use deterministic Brent–Dekker root-finding
on $[380,730]$ nm, declare numerical tolerance, and ensure reproducibility.
Numerical methods SHALL document input units, interpolation and integration.

Mathematical equivalence and procedure conformance are different claims:

- Exact evaluation of $a+\int R$ solves the same equation and gives the same
  mathematical value. It does not by itself execute the prescribed Brent step.
- A centroid, spectral median or a local threshold crossing is generally a
  different quantity.
- An arithmetic average of sampled values is not automatically the integral
  average. Quadrature weights and the curve model matter.
- Brent's root tolerance is not a material measurement uncertainty or a noise
  filter. The same perturbed spectrum obeys the same identity.

## 3. EE, Δλ*, and structural moments

For positive integrated reflectance, define

$$
c=\lambda^*_{EE}=\frac{\int_a^b\lambda R(\lambda)\,d\lambda}{\int_a^bR(\lambda)\,d\lambda},
\qquad \Delta\lambda^*=\lambda^*_{V2}-\lambda^*_{EE}.
$$

EE is the classical reflectance-weighted centroid. Δλ* combines mean reflectance
and centroid; it is not a pure skewness measure or a universal metamerism index.
EE alone cannot determine Δλ*, but EE together with mean reflectance determines
it exactly. The current sign is **V2 − EE**; the historical v2.1 release used
the reverse sign and must not be mixed silently with current records.

| Field | Definition | Unit |
|---|---|---|
| λ*_V2 | $a+(b-a)\overline R$ | nm |
| λ*_EE | $c$ | nm |
| Δλ* | $a+(b-a)\overline R-c$ | nm |
| μ₂ | $\int(\lambda-c)^2R\,d\lambda/\int R\,d\lambda$ | nm² |
| σ* | $\sqrt{\mu_2}$ | nm |
| μ₃ | $\int(\lambda-c)^3R\,d\lambda/\int R\,d\lambda$ | nm³ |
| γ₁ | $\mu_3/\mu_2^{3/2}$ | dimensionless |

Seven fields encode four underlying quantities: mean reflectance, centroid,
second and third central moments. Normalized moments are undefined at zero
area; normalized skewness also requires positive variance. The width σ* is not
measurement uncertainty. Equal fields do not guarantee equal spectra.

## 4. Reproduce the mathematical audit

```bash
python -m pip install -r requirements-audit.txt
python -m pytest -q
python scripts/verify_v2_identity.py --output /tmp/v2_identity.json
```

The recorded run contains **544 synthetic piecewise-linear spectra** on 1, 5,
10 nm and irregular grids. Brent evaluates the original two integrals using
adaptive quadrature; a separate trapezoidal calculation evaluates the area.
Maximum absolute difference: **2.274 × 10⁻¹³ nm**. The **original 28-test audit** includes
the unchanged historical threshold test plus analytic oracles, invalid inputs,
endpoint roots, a discontinuous function, and counterexamples. These are
numerical checks supporting the proof, not laboratory validation or independent
scientific peer review. [CI workflow](.github/workflows/v2-identity-audit.yml).

**Implementation distinction:** [`arbe_lambda.py`](arbe_lambda.py) computes the
first rising crossing of $R=\sqrt2-1$. It is a historical threshold algorithm,
not an implementation of the V2 integral equation. Its original test is retained
and labelled separately from the new audit. No master or source data are changed.

## 5. Scientific scope and citation

ARBE is a reproducible spectral descriptor framework. A compact representation
can be useful without adding information to the underlying spectrum. Historical
priority and application performance require their own evidence. No industrial
thresholds, device logic, material authentication guarantee, clinical claim or
release criteria follow from the identity or the numerical tests.

Reference definition: Woiwod, N. (2026), ARBE λ*_V2 – Formal Specification 1.0.0,
[DOI 10.5281/zenodo.18644381](https://doi.org/10.5281/zenodo.18644381).
When citing this clarification, additionally cite its Git commit; it does not
alter the archived DOI or existing release tags.

Code: MIT. Specification text: CC-BY 4.0. Source-data rights remain separate.
