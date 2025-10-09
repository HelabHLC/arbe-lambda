# 🌈 ARBE λ* v3.0 – Equal-Energy (UV + Vis, 300–730 nm)
### Physically grounded spectral balance wavelength analysis  
**Developed by HelabHLC / freieFarbe e.V.**

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

## ⚖️ License

- **Code:** MIT / BSD-3-Clause  
- **Data:** CC BY 4.0  
- **DOI:** [10.5281/zenodo.17038866](https://doi.org/10.5281/zenodo.17038866)

---

## 🧩 Acknowledgements

Developed by the  
**HelabHLC Spectral Research Group**  
in collaboration with **freieFarbe e.V.**  

> “Ein Licht mehr sehen — auch unter 380 nm.”  
> — ARBE λ\* Team

