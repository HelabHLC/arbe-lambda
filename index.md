
# 🌍 ARBE λ* – Global Launch Pack (Copilot-ready)

Welcome to the official starter kit for **ARBE λ*** – the Absorption-Reflection Balance Edge index. This repository helps you use, test, and extend ARBE λ* across design, science, and production contexts.

---

## 🔍 What is ARBE λ*

ARBE λ* (Lambda-Star) is a **spectral index** that captures the balance point between light absorption and reflection in the visible spectrum. Unlike RGB or Lab, it is **based on physical spectral data** and works across media: print, textile, digital.

**Core output:**
- ARBE λ* (in nm) as balance indicator
- Lab D50/2°, sRGB preview
- JSON-Export with color metadata

Full whitepaper: [https://doi.org/10.5281/zenodo.16414720](https://doi.org/10.5281/zenodo.16414720)

---

## 📦 Repository Contents

| File | Description |
|------|-------------|
| `arbe_lambda_gradio_app_vFinal.ipynb` | Gradio Web App for λ* analysis from spectral input |
| `arbe_lambda_full_export.csv` | Full export of HLC Atlas colors with computed λ* |
| `swatch_generator_spectral→lab→s_rgb_arbe_λ_standard_template.py` | Core script for spectral→Lab→sRGB + λ* computation |
| `hlc_connect_playbook_36_x_100_template.json` | Prompt playbook for 36 design genres × 10 actions |
| `prompt_generator_knowledgebase.md` | Documentation of the ARBE λ* prompt generator |
| `liesmich_v1-2.txt` | License and background for HLC Colour Atlas XL (CC-BY-ND 4.0) |
| `docs/grid-atlas.html` | Interaktive Grid-Ansicht des kompletten HLC Atlas mit λ*-Filtern |

---

## 🤖 Copilot / Prompt Usage

Use with Copilot Chat (GitHub/VS Code):

```
Prompt:
GENRE: Product Design. Clustere Kandidaten aus HLC Atlas nach ARBE λ* (Schwelle 0,4142) und wähle 7 harmonische Farben. JSON hlc-connect.playbook.v1.
```

See full schema: https://helabhlc.github.io/arbe-lambda/playbook/hlc_connect_playbook.json

---

## 🧪 Quickstart (Colab)

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com)

1. Open the notebook `arbe_lambda_gradio_app_vFinal.ipynb`
2. Upload your spectral file (`.csv`, `.cxf`, `.cgats`)
3. Get: λ*, Lab, sRGB preview, PNG & JSON export

---

## 🔄 Use Cases

- 🎨 Spectral palette clustering for harmony
- 🏭 Quality control in coatings, textile, packaging
- 🌐 Web/app colors with physical consistency
- ♿ Accessibility & WCAG replacement mapping
- 🔬 Scientific visualization & material R&D
- 🗂️ Grid Atlas für schnelle Farbbrowse-Erlebnisse – inspiriert von Pantone Connect

---

## 🌐 License & Attribution

- ARBE λ* index and tools © 2024–2025, [Norbert Woiwod / freieFarbe e.V.](https://www.freiefarbe.de)
- Data: HLC Colour Atlas XL (CC-BY-ND 4.0)

> Cite: Woiwod, N. (2024). *ARBE λ* – A Spectral Index for Balanced Color*. Zenodo. [https://doi.org/10.5281/zenodo.16414720](https://doi.org/10.5281/zenodo.16414720)

---

## 📤 Export Targets

- JSON (for UI & tool integration)
- PNG (swatch + spectrum)
- CSV/TSV (batch mode)
- PDF (report-ready)

---

## 📣 Get Involved

- 🧵 Join discussions via [GitHub Issues]
- 🔄 Translate prompts to other languages (DE/EN/FR/ES/JP…)
- 🔧 Fork & build your own spectral tools

Let’s bring physically grounded color communication to every screen, print, and surface.

---

**Next step?**
> Fork this repo • Open the Notebook • Try your first ARBE λ* color!

👉 **Neu:** Öffne [`docs/grid-atlas.html`](docs/grid-atlas.html) lokal oder via GitHub Pages und blättere durch 13 283 HLC-Farben in einer modernen Grid-Oberfläche mit λ*-Filtern.
