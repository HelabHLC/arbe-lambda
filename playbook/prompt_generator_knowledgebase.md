# 🧹 Prompt Generator (ARBE λ*-Optimized Playbook)

## 📌 Purpose
This section documents the **Prompt Generator**, a core tool for creating spectrally optimized color prompts based on the ARBE λ* index. The prompts use the `hlc-connect.playbook.v1` schema and are designed for application across 36 distinct design genres.

## 📄 Section Structure

### 1. Introduction
- The Prompt Generator allows the creation of standardized color prompts.
- It is based on a combinatorial playbook: **36 genres × 10 intents × 10 variations = 3,600 prompts**.
- Primary use cases: design, production, accessibility, and color research.

### 2. Design Genres (36)
- Branding & Corporate Design
- UI/UX & App Design
- Web Design & Landing Pages
- Editorial & Magazine
- Packaging & FMCG
- Infographics & Data Visualization
- Cartography
- Illustration (2D)
- Digital Painting
- 3D/CGI & Materials
- Product Design
- Automotive – Exterior
- Automotive – Interior
- Architecture – Exterior
- Architecture – Interior
- Interior Design & Moodboards
- Lighting Design
- Photography & Retouching
- Film/Video – Color Grading
- Advertising & Social Media
- E-Commerce Listings
- Fashion/Textile – Printing
- Fashion/Textile – Dyeing
- Cosmetics & Make-up
- Ceramics & Glazing
- Coatings & Finishes
- Print Prepress & Color Management
- Accessibility & Contrast Design
- Scientific Visualization
- Medical Imaging/Mapping
- Geology & Remote Sensing
- Environment & Sustainability Signage
- Wayfinding / Sign Systems
- Exhibit & Tradeshow Design
- Games / VR / AR
- Iconography & System UI

### 3. Prompt Structure
Each prompt consists of:

- **Genre**
- **Intent** (target action)
- **Variation** (rendering setup)
- **Constraints** (e.g. ΔE00, λ*)
- **Output**: JSON using `hlc-connect.playbook.v1`

#### Example Prompt (Text):
```
GENRE: Product Design. Cluster HLC Atlas candidates by ARBE λ* (threshold 0.4142) and return 7 harmonized colors (similar cut-wavelengths). Include rationale per color. JSON hlc-connect.playbook.v1.

Settings: Illuminant D50 · 2° Observer · Perceptual Intent · Gamut: PSO Coated v3.

Output: JSON with [title, genre, steps[], colors[], constraints, report].
```

### 4. Parameter Reference
| Parameter   | Description                                  |
|-------------|----------------------------------------------|
| `GENRE`     | Application domain (e.g. UI, Product Design) |
| `INTENT`    | Action: match, cluster, name, etc.           |
| `VARIATION` | Rendering context (observer, ICC, etc.)      |
| `HLC`       | Target color in HLC model                    |
| `Lab`       | CIELAB coordinates                           |
| `ARBE λ*`   | Spectral cut-wavelength (center of balance)   |
| `ΔE00`      | Color difference metric (goal: ≤ 2.0)         |
| `CxF`       | Path to spectral data file (optional)         |

### 5. Use Cases
- 🌍 **Spectral color harmony** (ARBE λ* clustering)
- 🔄 **Multichannel translation** (screen → print → textile)
- 🔍 **Quality control & matching** (CIELAB, ΔE00)
- ♿ **Accessibility optimization** (WCAG 2.2 AAA)
- 🌿 **Eco/material design** (spectral consistency)

## ✅ Implementation Tips
- Use interactive dropdowns for GENRE, INTENT, VARIATION
- Add tooltips for all parameter labels
- Offer JSON schema `hlc-connect.playbook.v1` as a download
- Enable prompt copy/export for integration in other systems

---
Ready to be embedded into UI, documentation, or as an interactive help system.

