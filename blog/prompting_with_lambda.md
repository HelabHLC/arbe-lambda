
# 🤖 Prompting mit ARBE λ*: Farben generieren mit physikalischer Tiefe

> *Wie spektrale Farbwerte deine KI-Prompts intelligenter, harmonischer und medienübergreifend konsistent machen.*

---

## 🎯 Warum Farbpraxis neu denken?

Die meisten Farbpaletten – ob für UI, Print, oder Packaging – basieren auf subjektiven Farbwahrnehmungen oder RGB/HEX-Werten. Doch Farben haben eine **physikalische Realität**: ihre **Remission im Lichtspektrum**.

**ARBE λ*** bringt diese Realität in deine Prompts: durch eine einzige, aber ausdrucksstarke Kennzahl in **nm** (Nanometer).

---

## 🧠 Was ist ein „Spectral Prompt“?

Ein Prompt, der neben Semantik auch **spektrale Informationen** nutzt – vor allem den ARBE λ*-Wert.

Beispiel:
```txt
GENRE: Verpackung & FMCG. Cluster HLC Atlas candidates by ARBE λ* (threshold 0.4142) and select 7 harmonized colors. Include Lab and HEX values. JSON hlc-connect.playbook.v1.
```

Dieser Prompt:
- Wählt nur spektral *harmonische* Farben (ähnlicher λ*)
- Gibt Lab, HEX und λ* aus – ideal für Design-Systeme
- Nutzt reale Farben aus dem HLC Atlas (mit Spektraldaten)

---

## 🎨 Branchenbeispiele

### 🧴 Naturkosmetik Verpackung
```txt
GENRE: Verpackung – Nachhaltige Markenästhetik. Wähle 6 Farben mit λ* zwischen 570–600 nm, die Wärme und Natürlichkeit vermitteln. Nutze Lab-Werte zur Abstimmung mit Recyclingmaterialien.
```

| Name       | λ* (nm) | Lab           | HEX      | Assoziation     |
|------------|---------|---------------|----------|-----------------|
| Tonerde    | 582.4   | (74.1, 7.2,18.5) | #D6B89C | Papier/Karton   |
| Honiglicht | 595.2   | (78.3,10.1,25.6) | #E8C88A | Glas/Cellulose  |

---

### 👁️‍🗨️ UX/UI – Barrierefreies Design
```txt
GENRE: UX/UI – Accessibility Mapping. Generiere 3 Farbkombinationen mit hohem Kontrast und spektraler Distinktheit (Δλ* > 40 nm). Stelle sicher, dass WCAG AAA erfüllt ist.
```

| Vordergrundfarbe | λ* (nm) | Hintergrundfarbe | λ* (nm) | Kontrast |
|------------------|---------|------------------|---------|----------|
| #1A1A1A (Anthrazit) | 480.2 | #F2E8D5 (Sand) | 620.4 | Hoch     |

---

### 🧬 Wissenschaftliche Visualisierung
```txt
GENRE: Wissenschaftliche Visualisierung. Erzeuge ein Farbgradient mit konstantem L* und steigender ARBE λ*. Nutze für Diagramme zur Darstellung von Absorptionsverhalten.
```

| Schritt | λ* (nm) | Lab         | HEX     |
|--------|---------|-------------|---------|
| 1      | 470.1   | (70,−10,5)  | #A9C8D8 |
| 2      | 510.3   | (70, −5,10) | #B5D8C2 |
| 3      | 550.6   | (70, 0,15)  | #C2E8B4 |

---

## ⚙️ Technisches Schema: `hlc-connect.playbook.v1`

Alle Prompts sind maschinenlesbar – ideal für:
- ChatGPT & Copilot
- Generative Design Tools
- Farbformulierung & QA

**JSON Felder:**
- `title`, `genre`, `steps[]`, `colors[]`, `constraints`, `report`
- Optional: `ARBE`, `Lab`, `HEX`, `CxF`

---

## ✨ Fazit

ARBE λ* verleiht deinen Prompts:
- Physikalische Tiefe
- Medienübergreifende Konsistenz
- Emotionale Präzision

Und: Sie sind **voll automatisierbar**.

---

🧪 Jetzt testen:
- Colab: [Notebook öffnen](https://colab.research.google.com)
- Prompt: Siehe `playbook/` Ordner
- Datensatz: `arbe_lambda_full_export.csv`

> **Bereit, Farbe nicht nur zu sehen – sondern zu verstehen?**
