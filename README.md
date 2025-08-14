# ARBE λ* Toolkit

**Spectral colour metric and open toolchain for material-based colour analysis**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## License

This project is licensed under the **MIT License**.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

---

## About

**ARBE λ\*** (*Absorption-Reflection Balance Edge*) is a spectral index that describes the balance point between absorption and reflection within the visible spectrum for a given colour sample. It complements existing colour models (CIELAB, HLC) with a physically grounded scalar value λ\* (in nm), derived from reflectance data (R(380–730nm)).

This repository provides a fully open workflow for computing and visualizing ARBE λ\*, including:

- ✅ λ\*-computation from spectral reflectance (CSV, JSON, CGATS)
- ✅ Colour space visualizations (CIELAB, HLC)
- ✅ ΔE2000 comparisons between colour groups
- ✅ PDF/CSV export, spectral plots, and quality assurance (QA) reporting
- ✅ Colab/Jupyter-ready environment

---

## Getting Started

### Option 1: Run in Google Colab

No installation needed:

```text
[Open in Colab] (coming soon)
```

### Option 2: Run locally

Install dependencies:

```bash
pip install colour-science pandas numpy scipy plotly matplotlib
```

Open the `arbe_lambda.ipynb` notebook in Jupyter or VS Code.

---

## Repository Contents

| File                          | Description                             |
|------------------------------|-----------------------------------------|
| `arbe_lambda.ipynb`          | Colab/Jupyter notebook (main workflow)  |
| `arbe_lambda_full_export.csv`| Spectral colour dataset with λ\*, Lab, HLC, R380–730nm |
| `paper.md`                   | JOSS manuscript                         |
| `LICENSE`                    | MIT license                             |
| `README.md`                  | This file                               |

---

## Citation

If you use ARBE λ\* in your research, please cite:

> Woiwod, N. (2025). *ARBE λ\*: A Spectral Edge-Based Colour Metric and Open Toolchain for Quality Assurance.* [JOSS submission forthcoming]

---

## Contact

For questions, contact Norbert Woiwod via [GitHub Issues](https://github.com/HelabHLC/arbe-lambda/issues).

---

**Note:** Screen previews (HEX colours) are symbolic. For QA or production decisions, always rely on Lab/λ\* values and spectral data.
