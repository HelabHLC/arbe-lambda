# Kurzversion (für Website / Presse / Marketing)

## Update: ARBE λ* v2.0 jetzt verfügbar

Der **ARBE λ*-Index** ist seit seiner Einführung im Jahr **2025** ([DOI: 10.5281/zenodo.16414720](https://doi.org/10.5281/zenodo.16414720)) ein zentrales Werkzeug für die **spektrometrische Farbanalyse**.

Am **24. Juli 2025** wurde zunächst **ARBE λ* v1.0** veröffentlicht – ein Näherungsverfahren, das in den meisten Fällen präzise Ergebnisse lieferte, in Randbereichen jedoch an Genauigkeit verlor.

Ab dem **4. September 2025** steht mit **ARBE λ* v2.0** ein neues Berechnungsverfahren bereit:
- Brent-Verfahren für robuste Nullstellensuche
- 1-nm-Interpolation mit schneller Integration
- vollständig reproduzierbare, exakte Ergebnisse

---

# Langversion (für Whitepaper / wissenschaftliche Veröffentlichung)

## ARBE λ* v1.0 (2025-07-24) – Näherungsverfahren
Die erste Version von ARBE λ* wurde am **24. Juli 2025** veröffentlicht ([DOI: 10.5281/zenodo.16414720](https://doi.org/10.5281/zenodo.16414720)).  
Die Berechnung erfolgte über diskrete Integrationsverfahren und heuristische Nullstellensuchen.  
- Vorteil: einfache Implementierung, geringe Rechenlast  
- Limitation: bei sehr dunklen oder neutralen Spektren teils instabil  

## ARBE λ* v2.0 (ab 2025-09-04) – Präzise Spektralberechnung
Mit der zweiten Version erfolgt die Berechnung nun **mathematisch exakt und numerisch stabil**:
- Brent-Verfahren zur Nullstellensuche
- 1-nm-Interpolation zwischen Spektraldatenpunkten
- schnelle Trapezregel zur Flächenintegration

### Ergebnisse über den gesamten HLC-Atlas (13 283 Farben):
- Mittelwert: 569 nm (gelbgrüner Bereich)
- Standardabweichung: ±49 nm (Verteilung von Blau bis Rot)
- Valide Werte für 100 % der Farben

## Fazit
- **ARBE λ* v1.0 (2025-07-24)** bleibt für historische Daten gültig und vergleichbar.  
- **ARBE λ* v2.0 (ab 2025-09-04)** ist die neue Referenz für Forschung, Industrie und Design.  
- Empfehlung: Bei allen neuen Projekten den **v2.0-Algorithmus** verwenden.  
