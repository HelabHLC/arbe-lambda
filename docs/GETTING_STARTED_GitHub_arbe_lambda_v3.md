# 🚀 Getting Started – ARBE λ* v3

Willkommen! Dieses Dokument hilft dir, das **ARBE λ***‑Projekt lokal zu starten, Daten zu validieren und die wichtigsten Werkzeuge (CLI & Playbooks) produktiv einzusetzen.

> **ARBE λ*** (Absorption–Reflection Balance Edge) ist die physikalisch begründete Wellenlänge (λ* in nm), an der absorbierte und reflektierte Energie eines sichtbaren Spektrums im Gleichgewicht sind. Die Berechnung nutzt ein energetisches Differenzmodell und eine robuste Nullstellensuche (Brent‑Verfahren).

---

## 1) Projektziele in v3

* **Hybrid‑Prinzip**: Offizieller Atlas (HEX & CIE Lab D50/2°) kombiniert mit präzisen **λ***‑Werten (Equal‑Energy, optional D50‑gewichtet).
* **Reproduzierbarkeit**: 1‑nm‑Interpolation, Trapezregel, Solver‑Parameter versioniert.
* **Atlas‑Only Policy**: Alle Ausgaben referenzieren **exakt** Atlas‑Samples (H###_L###_C###).
* **Playbook‑Integration**: JSON‑Schemas für Prompt‑Generator (36 Genres, ΔE00/λ* Constraints).
* **Validierung**: JSON‑Schema + CLI‑Validator + Checksummen.

---

## 2) Ordnerstruktur (Empfehlung)

```
arbe-lambda/
├─ data/
│  ├─ arbe_lambda_star_v2_equal_energy_1nm.csv      # kanonisches λ*‑Mapping (EE, 1 nm)
│  ├─ Hybrid_arbe_lambda_full_export_compact.csv    # Sample, HEX, Lab, λ*_V2
│  └─ HLC-Colour-Atlas-XL_SpectralData_v1-2.cxf     # 36‑Punkt‑Spektren (380–730/10)
├─ schemas/
│  ├─ hybrid_compact.schema.json
│  ├─ lambda_v2_equal_energy_1nm.schema.json
│  └─ spectrum_remission_1nm.schema.json
├─ tools/
│  ├─ make_arbe_lambda_bundles.py
│  ├─ validate_arbe_lambda_dataset.py
│  └─ swatch_generator_spectral→lab→s_rgb_arbe_λ_standard_template.py
├─ playbooks/
│  ├─ prompt_generator_knowledgebase.md
│  └─ prompt_generator_integration_kit_arbe_λ_36_genres_δe_00_λ_json.md
└─ docs/
   └─ GETTING_STARTED_GitHub_arbe_lambda_v3.md  # dieses Dokument
```

> **Hinweis:** In v3 bleiben Dateinamen aus v2 erhalten (Versionierung in Manifests). Das erleichtert Migration.

---

## 3) Installation

**Python ≥ 3.10** wird empfohlen.

```bash
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
python -m pip install -U pip
python -m pip install numpy pandas jsonschema lxml pillow matplotlib
# Optional für D50‑gewichtet: colour-science
python -m pip install colour-science
```

---

## 4) Quick Start: λ*‑Bundles aus CxF erzeugen

Nutze das Batch‑Tool, um **Equal‑Energy** (und optional **D50**) Datensätze zu bauen.

```bash
python tools/make_arbe_lambda_bundles.py --cxf data/HLC-Colour-Atlas-XL_SpectralData_v1-2.cxf
# Auto‑Discovery geht auch: einfach ohne Parameter im Ordner mit genau einer *.cxf ausführen
```

**Ergebnis (Beispiele):**

* `arbe_lambda_star_v2_equal_energy_1nm.csv`
* `arbe_lambda_star_v2_D50_1nm.csv` (falls D50 verfügbar)
* `arbe_lambda_v2_DOI_bundle.zip` inkl. Manifest & Checksums

**Solver‑Parameter (empfohlen):** `range = [380, 730] nm`, `step = 1 nm`, `solver = Brent`, `tol = 1e-6`.

---

## 5) Datenschemata & Validierung

### 5.1 Hybrid Compact (Auszug)

```json
{
  "Sample": "H123_L045_C060",
  "HEX": "#336699",
  "λ*_V2": 505.7
}
```

### 5.2 CSV validieren

```bash
python tools/validate_arbe_lambda_dataset.py \
  --csv data/Hybrid_arbe_lambda_full_export_compact.csv \
  --schema schemas/hybrid_compact.schema.json
```

Wenn alles korrekt ist: `✅ Alles valide!`

---

## 6) Atlas‑Only Policy (Pflicht in v3)

* **Nur Atlas‑Samples** ausgeben (keine freien Farben).
* Jede Ausgabe enthält mindestens: `Sample`, `HEX`, `Lab_D50`, `λ*_V2`.
* Bei Eingaben außerhalb des Atlas: per **ΔE00** auf den nächsten Atlas‑Sample **snappen**.
* **HEX** ist symbolisch/atlas‑kompatibel, **λ*** ist physikalisch.

---

## 7) Swatches & Konvertierung (Spektrum → Lab → sRGB)

Das Swatch‑Script erzeugt farbmetrisch korrekte Previews und JSON‑Metadaten.

```bash
python tools/swatch_generator_spectral→lab→s_rgb_arbe_λ_standard_template.py \
  --in path/to/spectrum.csv --out out/my_color --plot
# Ausgabe: out/my_color_swatch.png, out/my_color.json, optional Spektrums‑Plot
```

**Parameter & Annahmen**

* CIE 1931 2° CMFs & D50 SPD (10 nm, 380–730 nm) konsistent zur Wellenlängentabelle
* XYZ (D50/2°) → Lab (D50) → sRGB (D65, Bradford Adaption)

---

## 8) Prompt‑Generator (Playbooks, 36 Genres)

Die Playbooks liefern standardisierte, **physikalisch fundierte** Prompt‑Texte mit λ*‑/ΔE00‑Constraints.

**TypeScript‑Nutzung (Kurzbeispiel):**

```ts
import { generatePrompt } from './src/arbe-prompt-generator';

const out = generatePrompt({
  genre: 'Branding & Corporate Design',
  intent: 'Accessibility AAA',
  variation: 'v3',
  task: 'Create high‑contrast primary/bg pair.',
  palette: [
    { HEX: '#003366', 'λ*_V2': 470, role: 'primary' },
    { HEX: '#F0F4F8', 'λ*_V2': 610, role: 'bg' }
  ],
  constraints: { contrast_ratio_target: 7.0, deltaE00_max: 3.0, lambda_star_target: 500, lambda_star_tolerance: 25 }
});
console.log(out.prompt_text);
```

---

## 9) Qualitätskontrolle (QC)

* **Schemas prüfen** (JSON/CSV) und **Checksummen** (SHA‑256) in Bundles.
* **Schnellprüfungen**:

  * HLC‑Codes zero‑padded (`H\d{3}_L\d{3}_C\d{3}`)
  * λ* ∈ [380, 730] nm
  * Remission ∈ [0, 1] (bis 1.2 in Fluoreszenz‑Randfällen)
  * Hybrid: vollständige Schlüssel, keine Duplikate

---

## 10) Zitation & Lizenz

* **Zitation (Beispiel):**
  *HelabHLC. (2025). HelabHLC/arbe‑lambda: ARBE λ* v3 (v3.0). Zenodo. DOI folgt im Release.*
* **Lizenzen:**
  Code: MIT/BSD‑3 • Daten: CC BY 4.0 • Atlas‑Quelle: freieFarbe HLC Atlas (Namensnennung erforderlich)

---

## 11) FAQ (Kurz)

**Wieso „v2“ im Dateinamen bei v3?**
Die wissenschaftliche Definition (λ* V2, Brent‑validiert) bleibt stabil. v3 ergänzt Tooling/Docs, ändert aber nicht die Kernformel – daher bleiben Datenartefakte kompatibel.

**Equal‑Energy vs. D50?**
EE ist neutral spektral. D50 gewichtet spektral mit Tageslicht‑SPD – optional für spezielle Anwendungen.

**Farbvorschau ≠ Spektrum?**
Korrekt: HEX/sRGB sind **symbolisch** (medienabhängige Anzeige). λ* bleibt **physikalisch** und medienunabhängig.

---

## 12) Nächste Schritte

1. `make_arbe_lambda_bundles.py` mit deiner CxF ausführen.
2. `Hybrid_…_compact.csv` validieren und in dein System importieren.
3. Prompt‑Playbooks anbinden (TS/Python).
4. **Atlas‑Only** in UIs und Exports durchsetzen.

Viel Erfolg mit ARBE λ* v3! 🎨⚡️

