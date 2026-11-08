# Δλ* CSV quickstart for measurement partners

Working research tool, 8 November 2026. No programming is needed to run the
commands below. Python 3.12 and NumPy are required. The program processes local
files; it has no data-upload or network calls. Installing dependencies initially
requires internet access unless those packages are already available locally.

This tool implements **Δλ* = λ*_V2 − λ*_EE**. It combines reflectance level and
centroid position. It is not a statistical skewness measure or a validated damage
detector. It reports calculated values, not pass/fail decisions.

## 1. Install

[Download the repository ZIP](https://github.com/HelabHLC/arbe-lambda/archive/refs/heads/main.zip),
extract it, and open a terminal in the extracted folder. With Python 3.12 installed:

```bash
python -m pip install -r requirements-tools.txt
```

On systems that use `python3` or the Windows `py` launcher, use that command
consistently instead of `python`. No pandas, Excel engine or plotting package is
required. Export your spreadsheet to CSV before using this tool.

## 2. Prepare or select a CSV

The first header must be `wavelength_nm`. Each following header is a unique
spectrum ID. Each row contains one wavelength and the reflectance values at that
wavelength. Include the full measured grid, not just selected peaks:

```csv
wavelength_nm,synthetic_constant,synthetic_ramp
380,0.2,0.12
430,0.2,0.17142857142857143
480,0.2,0.22285714285714286
530,0.2,0.2742857142857143
580,0.2,0.32571428571428573
630,0.2,0.3771428571428571
680,0.2,0.4285714285714286
730,0.2,0.48
```

These are **synthetic mathematical examples**, not measured materials or HLC
references. The ready-made file is [examples/delta_synthetic.csv](../../examples/delta_synthetic.csv).

For your data, replace the values and spectrum IDs. Requirements:

- Increasing, finite wavelengths, no duplicates; irregular spacing is supported.
- Default endpoints exactly 380 and 730 nm. Missing endpoints cause an error;
  the tool does not extrapolate or invent missing measurements.
- Dimensionless reflectance fractions from 0 to 1. Percent input needs the
  explicit option below. Values are never silently clipped.
- Complete numeric cells. Empty values, NaN and infinity are rejected.
- Nonempty unique spectrum IDs; IDs starting with `=`, `+`, `-` or `@` are
  rejected to avoid formula-like output when results are opened in a spreadsheet.

## 3. Run and read results

First try the included synthetic example:

```bash
python scripts/delta_lambda_pipeline.py examples/delta_synthetic.csv --output example_results.csv
```

Then replace the input filename with your own CSV:

```bash
python scripts/delta_lambda_pipeline.py my_spectra.csv --output results.csv
```

Two files are written:

- `results.csv`: one row per spectrum, including values, optional standard
  uncertainties, Cov(A,D), units implicit in field names and integration settings.
- `results.json`: full per-spectrum results, sensitivity matrices, covariance
  matrices, sign convention, assumptions and limitations.

If no uncertainty was supplied, the CSV uncertainty fields are blank and the
JSON values are `null`. **Unknown uncertainty is not zero uncertainty.**
Existing output files are protected. Choose a new output filename or explicitly
add `--overwrite` to replace results. Input files remain protected even with that flag.
All spectra are validated before result writing begins.

For the synthetic example, the expected analytic results are:

| Spectrum | A (nm) | Mean reflectance | c (nm) | V2 (nm) | D (nm) |
|---|---:|---:|---:|---:|---:|
| synthetic_constant | 70 | 0.2 | 555 | 450 | −105 |
| synthetic_ramp | 105 | 0.3 | 590 | 485 | −105 |

The same D for these different spectra illustrates its information limit.
The pair (A,D) distinguishes their area and centroid but does not reconstruct
their full spectral shape in general.

## Optional input formats

For reflectance values written as percent, for example 20 rather than 0.20:

```bash
python scripts/delta_lambda_pipeline.py percent.csv --reflectance-unit percent --output results.csv
```

For semicolon-separated CSV with decimal commas:

```bash
python scripts/delta_lambda_pipeline.py spectra.csv --delimiter ";" --decimal "," --output results.csv
```

Do not change the wavelength interval silently. An explicit alternative such as
`--interval 400 700` changes the descriptor's domain and requires data with those
endpoints. Such results must not be compared directly to 380–730 nm records as
though they used the same definition.

## Optional measurement uncertainty

Choose at most one of the following three input methods. No uncertainty is
estimated from one spectrum or invented by default. The input must describe the
uncertainty of the actual supplied measurements. For averaged spectra, uncertainty
of the mean is not automatically the same as the scatter of individual repeats.

### Constant supplied standard uncertainty

Only if your measurement model justifies it:

```bash
python scripts/delta_lambda_pipeline.py spectra.csv --u-reflectance 0.002 --output results.csv
```

Here 0.002 is an absolute standard uncertainty in reflectance fractions, equal
to 0.2 percentage points, not a relative 0.2% error. This option assumes
uncorrelated errors across wavelength nodes. It is a supplied assumption, not
an automatic estimate of instrument performance. With `--reflectance-unit percent`,
the corresponding input would be `--u-reflectance 0.2`.

### Different standard uncertainties at each node

Provide another CSV with exactly the same wavelength rows and spectrum headers,
but standard uncertainties in the data cells:

```bash
python scripts/delta_lambda_pipeline.py spectra.csv --uncertainty-csv uncertainties.csv --output results.csv
```

The same delimiter, decimal and fraction/percent settings apply to both files.
This method also assumes uncorrelated errors across wavelength nodes.

### Correlated reflectance errors

Use a JSON object mapping every spectrum ID to its n×n reflectance covariance
matrix, with rows and columns ordered as the wavelength rows:

```json
{
  "sample_1": [[0.000004, 0.000002], [0.000002, 0.000004]]
}
```

This is a structural example for a two-node, one-spectrum file, not a recommended
measurement grid or an experimentally established covariance. Matrices must be
finite, symmetric and positive semidefinite. For percent input, supply covariance
in percentage-point squared; the tool converts it by dividing by 100².

```bash
python scripts/delta_lambda_pipeline.py spectra.csv --covariance-json covariance.json --output results.csv
```

Shared reference, offset or gain errors can be represented if their effect is
properly included in the supplied reflectance covariance. Cross-spectrum
covariance, including correlations between before/after measurements, is not
evaluated by this interface. Do not infer a significance threshold for a change
from one row's standard uncertainty.

## Calculation model and scope

The default `piecewise_linear` model integrates the linear interpolant of R
and its first moment exactly, up to rounding. If q are area weights and t are
weights of the first moment about the lower endpoint a, then:

$$
A=q^\mathsf TR,\quad c=a+\frac{t^\mathsf TR}{A},\quad V2=a+A,\quad D=V2-c,
$$

$$
\frac{\partial c}{\partial R_i}=\frac{t_i-(c-a)q_i}{A},\qquad
\frac{\partial D}{\partial R_i}=q_i-\frac{\partial c}{\partial R_i}.
$$

This is not the same centroid calculation as applying point trapezoidal weights
to λᵢRᵢ. `--integration point_trapezoid` explicitly selects that alternative.
The mode is recorded in the output. Neither method resolves the unknown true
curve between sampled wavelengths or removes instrument bandpass effects.

The output covariance is ordered **A, c, V2, D**, in nm². Propagation from
reflectance uses the first-order GUM relation JΣR Jᵀ. The complete 4×4 covariance
is rank deficient because V2 and D depend on A,c; use the appropriate 2×2 submatrix
for a two-parameter analysis, not a blind inverse of the full matrix.

For fixed a, the pair (A,D) is an invertible affine transformation of (A,c),
with c=a+A−D. Its covariance therefore transforms exactly once the covariance
of A,c is given. This preserves information; it does not automatically reduce noise.

Wavelength nodes and interval bounds are treated as fixed. Wavelength calibration,
spectral bandwidth, geometry, interpolation/model uncertainty and other instrument
effects need additional models. The implemented propagation is therefore **not a
complete GUM evaluation of a real spectrometer**, even when a full reflectance
covariance is supplied. Large nonlinear effects require a suitable distribution
model and additional checks. No outlier suppression, material diagnosis or
industrial pass/fail rule is implemented.

V2 is computed using the proven area identity. This code does not execute the
separately prescribed Brent–Dekker procedure and does not claim that procedural
conformance. The [historical threshold code](../../arbe_lambda.py) remains a
different algorithm.

## Reproduce the checks

```bash
python -m pip install -r requirements-audit.txt
python -m pytest -q
python scripts/verify_delta_uncertainty.py --output delta_uncertainty_check.json
```

The core is checked against analytic constant/ramp spectra, independent adaptive
integration, finite-difference derivatives, full covariance transformation,
input validation and known information-loss counterexamples. CSV tests cover
the command-line entry point, missing uncertainties, unit conversion and file
protection. A seeded 50,000-draw synthetic simulation checks the first-order
covariance under a stated white-noise/common-offset/common-gain model.

These are software and numerical checks, not laboratory validation. The
[recorded simulation result](../../results/delta_uncertainty_2026-11-08.json)
reports the model, software versions and tolerances. The separate 544-case
[identity audit](../research/v2-mean-reflectance-identity.md) also uses synthetic
curves, not a real measurement series.

## References

- [NIST TN 1297: Law of Propagation of Uncertainty](https://www.nist.gov/pml/nist-technical-note-1297/nist-tn-1297-appendix-law-propagation-uncertainty)
- [JCGM 102:2011: multiple output quantities](https://doi.org/10.59161/JCGM102-2011)
- [NIST TN 1297: Expanded Uncertainty](https://www.nist.gov/pml/nist-technical-note-1297/nist-tn-1297-6-expanded-uncertainty)

These references support the uncertainty method; they do not independently
validate ARBE's application performance or historical novelty.
