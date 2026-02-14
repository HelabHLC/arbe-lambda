# ARBE λ*_V2 – Formal Reference Implementation

This repository provides the normative specification and deterministic reference implementation of λ*_V2 within the ARBE λ* framework.

λ*_V2 is defined as the unique energetic balance point of a measured reflectance spectrum over the wavelength interval 380–730 nm.

---

## 1. Formal Definition

Let R(λ) denote a physically measured reflectance spectrum with:

380 nm ≤ λ ≤ 730 nm  
0 ≤ R(λ) ≤ 1

Define the balance function:

g(λ) =
∫₃₈₀^λ (1 − R(λ′)) dλ′ − ∫_λ^₇₃₀ R(λ′) dλ′

λ*_V2 is defined as the unique λ ∈ [380,730] such that:

g(λ) = 0

---

## 2. Numerical Determination (Normative)

The zero of g(λ) SHALL be computed using:

**Brent–Dekker root-finding method**

Requirements:

- Deterministic algorithm
- Bracketing within [380,730]
- Guaranteed convergence for continuous spectra
- Declared numerical tolerance

Centroid methods, weighted means, CDF medians, or heuristic balancing procedures are not equivalent to λ*_V2.

---

## 3. Distinction from Related Metrics

### λ*_EE (Equal-Energy Centroid)

λ*_EE is defined as:

λ*_EE = ( ∫ λ R(λ) dλ ) / ( ∫ R(λ) dλ )

λ*_EE is a reflected-energy centroid and not identical to λ*_V2.

### Δλ*

Δλ* = λ*_V2 − λ*_EE

Δλ* describes spectral asymmetry and is a secondary descriptor.

---

## 4. Scope

This repository serves as:

- A formal scientific reference
- A deterministic computational example
- A reproducible implementation baseline

It does not define:

- A color space
- A generative color model
- Industrial thresholds
- Device-specific control logic

---

## 5. Reproducibility

Implementations claiming compliance with ARBE λ*_V2 MUST:

1. Use measured reflectance spectra.
2. Restrict computation to 380–730 nm.
3. Apply deterministic Brent root-finding.
4. Declare numerical tolerance.
5. Produce reproducible results.

---

## 6. Citation

If this framework is used in research or applied analysis, please cite:

Woiwod, N. (2026). Formal Specification of λ*_V2 (ARBE λ*), Version 1.0.

---

## 7. License

Code: MIT License  
Specification text: CC-BY 4.0

---

λ*_V2 is defined as a physical ordering parameter derived from measured reflectance spectra.  
It is not a perceptual color coordinate, nor a proprietary system.


---

## 🧬 Overview

**ARBE λ\*** (“Absorption–Reflection Balance Edge”) describes  
the wavelength λ\* at which absorbed and reflected energy  
in the visible (and now UV) spectrum are in equilibrium.

Version **v3.0** expands the range from the visible (380–730 nm)  
to **UV + Vis (300–730 nm)** for deeper spectral accuracy  
in colorimetry, pigment analysis, and optical material research.

---

### 🔬 What’s new in v3.0

| Feature | Description |
|----------|--------------|
| **λ\*_V3** | Equal-Energy Integration 300–730 nm |
| **Δλ Metric** | UV absorption sensitivity (λ\*_V3 − λ\*_V2) |
| **QC System** | Schema validation for hybrid datasets |
| **Plots** | Histograms, Δλ vs L\*, spectral balance |
| **Full CI/CD** | Automated via GitHub Actions and Pages |

---

## 🔄 Workflow Diagram

![ARBE λ* v3 Flow](docs/arbe_lambda_v3_flow.svg)

> End-to-end pipeline from CxF spectra → λ\*_V3 → Hybrid merge → QC →  
> Visualization → Reproducible release bundles.

---

## 📘 Getting Started Guide

If you want to **run the ARBE λ\* v3 Equal-Energy pipeline directly in GitHub**,  
follow the full setup steps here:  

👉 [**Open the GitHub Getting Started Guide →**](docs/GETTING_STARTED_GitHub_arbe_lambda_v3.md)

---

## 📊 Example Outputs

| Sample | λ\*_V2 (nm) | λ\*_V3 (nm) | Δλ (nm) | Interpretation |
|---------|-------------|-------------|----------|----------------|
| H005_L065_C025 | 516.2 | 507.8 | −8.4 | Slight UV absorption shift |
| H070_L080_C030 | 590.3 | 582.5 | −7.8 | Weak UV activity |
| H095_L045_C045 | 614.5 | 615.1 | +0.6 | Stable, UV-inert |

---

## 🧩 Repository Structure


---

## ⚙️ Automation

| Task | Script / Action |
|------|------------------|
| Compute λ\*_V3 | `make_arbe_lambda_bundles_uv.py` |
| Merge Hybrid Data | `merge_arbe_lambda_versions.py` |
| Validate QC | `validate_hybrid_with_v3.py` |
| Visualize | `plot_arbe_lambda_deltas.py` |
| Build Bundle | `make_arbe_lambda_v3_bundle.py` |
| Full CI/CD | `.github/workflows/arbe_v3_pipeline.yml` |

---

## 🧮 Mathematical Definition

\[
\lambda^* = \lambda_\text{min} + \int_{\lambda_\text{min}}^{\lambda_\text{max}} R(\lambda)\,d\lambda
\]

- **Integration:** Equal-energy weighting  
- **Solver:** Brent’s root-finding  
- **Range:** 300–730 nm  
- **Δλ:** Difference between v2 (Vis) and v3 (UV + Vis)

---

## 📈 Visualisation Overview

| Diagram | Description |
|----------|--------------|
| Histogram | Distribution of Δλ (UV shift) |
| Boxplot | λ\*_V2 vs λ\*_V3 comparison |
| Scatter L\* vs Δλ | Brightness correlation |
| Spectrum plot | Energy balance visualization |

---

## 🧠 Applications

| Domain | Example | Use |
|---------|----------|-----|
| **Print & Paper** | OBA-whitened media | UV correction |
| **Pigments & Coatings** | Photostable colors | Energy analysis |
| **Material Science** | Reflective composites | λ\* equilibrium |
| **Teaching** | Colorimetry education | Spectral interpretation |

---

## 🧾 Citation

> **HelabHLC (2025).** *ARBE λ\* v3.0 – Equal-Energy (UV + Vis, 300–730 nm).*  
> Zenodo. [https://doi.org/10.5281/zenodo.17038866](https://doi.org/10.5281/zenodo.17038866)

See also: [`docs/CITATION.cff`](docs/CITATION.cff)

---

## ⚖️ Licensing

- **Code (software, scripts, tools):** Apache License 2.0  
  (includes an explicit patent grant)

- **Data, documentation, and conceptual content  
  (including ARBE λ*, Δλ*, models, datasets, and descriptions):**  
  Creative Commons Attribution–ShareAlike 4.0 (CC BY-SA 4.0)

- **DOI (defensive publication / prior art):**  
  https://doi.org/10.5281/zenodo.17038866

---

## 🧩 Acknowledgements

Developed by the  
**HelabHLC Spectral Research Group**  
in collaboration with **freieFarbe e.V.**  

> “Ein Licht mehr sehen — auch unter 380 nm.”  
> — ARBE λ\* Team

