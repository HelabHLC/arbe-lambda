# ARBE λ* Toolkit  
**Spectral colour metric and open toolchain for material-based colour analysis**  

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.16877146.svg)](https://doi.org/10.5281/zenodo.16877146)  

---

## What is ARBE λ\*?

**ARBE λ\*** (*Absorption–Reflection Balance Edge*) is a spectral index that describes the balance point between absorption and reflection in the visible range for a given material colour sample.  
It complements CIELAB and HLC colour spaces with a physically grounded scalar λ\* (in nm), computed directly from spectral reflectance data (R(380–730 nm)).  

λ\* is defined as the wavelength where:

\[
R(λ) = \sqrt{2} - 1 \approx 0.4142
\]

on the **first rising edge** of the reflectance curve.

---

## Quick Start — Single Spectrum Demo

You can reproduce λ\* calculation from **just one reflectance curve** using the included demo script:

```bash
# Built-in example spectrum
python demo_lambda_from_single_spectrum.py

# With your own spectrum CSV (either long: wavelength,R or wide: R380..R730)
python demo_lambda_from_single_spectrum.py path/to/spectrum.csv
```

Example output:

```
λ* ≈ 510.0 nm  (R* = √2 − 1 ≈ 0.4142)
```

This will also plot the reflectance curve, the balance line (R ≈ 0.4142), and the λ\* marker:

![ARBE λ* demo: single-spectrum crossing](docs/img/demo_lambda_star.png)

---

## Repository Contents

| File / Folder                  | Description |
|--------------------------------|-------------|
| `arbe_lambda.py`               | Core λ\* computation logic |
| `demo_lambda_from_single_spectrum.py` | Minimal demo using one reflectance curve |
| `example_spectrum.csv`         | Example reflectance spectrum (0–1 scale) |
| `arbe_lambda.ipynb`            | Full Jupyter/Colab workflow (multi-sample support) |
| `arbe_lambda_full_export.csv`  | Complete dataset (~13,283 HLC colours with λ\*) |
| `paper.md`                     | JOSS submission manuscript |
| `LICENSE`                      | License (MIT for code, CC BY-NC 4.0 for data) |

---

## Installation

### Option 1 — Run in Google Colab (no installation)  
*(link coming soon)*

### Option 2 — Local install
```bash
pip install numpy pandas matplotlib scipy plotly
```

---

## How it works

1. Load R(λ) for 380–730 nm (10 nm steps, % or 0–1).
2. Find **first rising edge** crossing R ≈ 0.4142.
3. Use **linear interpolation** if the crossing falls between sample points; otherwise choose nearest λ.

---

## Citation

If you use ARBE λ\* in research, please cite:

> Woiwod, N. (2025). **ARBE λ\***: A Spectral Edge-Based Colour Metric and Open Toolchain for Quality Assurance. *Zenodo*. [https://doi.org/10.5281/zenodo.16877146](https://doi.org/10.5281/zenodo.16877146)  

BibTeX:
```bibtex
@article{woiwod2025arbe,
  title={ARBE λ*: A Spectral Edge-Based Colour Metric and Open Toolchain for Quality Assurance},
  author={Woiwod, Norbert},
  year={2025},
  doi={10.5281/zenodo.16877146},
  url={https://doi.org/10.5281/zenodo.16877146}
}
```

---

## License

- **Code:** MIT License  
- **Data:** Creative Commons Attribution–NonCommercial 4.0 International (CC BY-NC 4.0)  

---

## Contact

For questions, open a GitHub Issue or contact **Norbert Woiwod**  
ORCID: [0009-0000-0772-0084](https://orcid.org/0009-0000-0772-0084)  

