# Δλ*: mathematical status, source history, and novelty review

Prüfdatum: **8. November 2026**. Ausgangsstand:
`cb566dddca3adeecbd8ac3b8ac352d270d7df585`.
Diese Recherche ist eine dokumentierte Projektprüfung mit ChatGPT-Unterstützung,
keine unabhängige Begutachtung und kein patentrechtliches Neuheitsgutachten.

## 1. Ergebnis und Reichweite

| Frage | Befund |
|---|---|
| Ist V2 mit der ungewichteten mittleren Reflexion gleichwertig? | **Bewiesen:** exakt umkehrbare affine Umrechnung auf demselben Intervall. |
| Ist EE der klassische reflexionsgewichtete Schwerpunkt? | **Ja**, nach der angegebenen Gleichung. |
| Kann EE allein Δλ* allgemein ersetzen? | **Nein**, analytische Gegenbeispiele liegen vor. |
| Liegt in Δλ* zusätzliche Information gegenüber Mittelreflexion **und** EE vor? | **Nein**, daraus exakt rekonstruierbar. |
| Sind die sieben Felder sieben unabhängige Größen? | **Nein**, sie sind aus vier Grundgrößen bestimmbar. |
| Ist Δλ* ein reines Asymmetriemaß? | **Nein**, es reagiert auch auf das Reflexionsniveau symmetrischer Kurven. |
| Wurde die konkrete Kombination in ARBE bereits öffentlich beschrieben? | **Ja**, im eingesehenen v2.1-Release vom 07.11.2025, mit umgekehrtem Vorzeichen. |
| Gibt es einen identischen externen Vorläufer? | In den hier geprüften Fremdquellen **nicht nachgewiesen**. |
| Ist historische Erstheit damit bewiesen? | **Nein.** Die begrenzte Recherche erlaubt keinen universellen Ausschluss früherer Arbeiten. |
| Belegt dies einen besonderen Anwendungsnutzen? | **Nein.** Die mathematische Prüfung misst keine praktische Überlegenheit. |

Die Rückführbarkeit auf klassische Größen widerlegt nicht automatisch die
Neuheit einer konkreten Kombination oder Anwendung. Umgekehrt begründet die
Benennung einer Kombination weder zusätzliche unabhängige Information noch
historische Erstheit. Diese Fragen müssen getrennt beantwortet werden.

## 2. Exakt geprüfter Gegenstand

Für $a=380$ nm, $b=730$ nm, $L=b-a$, dimensionsloses $R\in[0,1]$ und
positive Fläche gilt:

$$
D=\Delta\lambda^*=a+\int_a^bR(\lambda)d\lambda
-\frac{\int_a^b\lambda R(\lambda)d\lambda}{\int_a^bR(\lambda)d\lambda}.
$$

Nach Normierung $t=(\lambda-a)/L$ und $M_k=\int_0^1t^kR(a+Lt)dt$:

$$
D/L=M_0-M_1/M_0.
$$

Gesucht wurde nach derselben Funktion, auch mit anderem Namen, Vorzeichen oder
Einheit. Ein bloßes Vorkommen von „delta“, „centroid“, „moments“ oder „balance“
reicht nicht. Gemeinsame Verwendung von Fläche und Schwerpunkt ist ein
methodischer Vorläufer, aber nicht automatisch dieselbe skalare Kombination.
Der [Beweis mit Gegenbeispielen](v2-mean-reflectance-identity.md) klärt den
Informationsgehalt unabhängig von der Literaturrecherche.

## 3. Eigene Quellen: notwendige Versionsunterscheidungen

| Datum / Quelle | Nachgelesener Inhalt | Konsequenz |
|---|---|---|
| 24.07.2025, [Zenodo 16414720](https://doi.org/10.5281/zenodo.16414720), Originaldatei `arbe_lambda_top_whitepaper.txt` | Lokale Bedingung $R=\sqrt2-1$ aus einem Kubelka–Munk-Fixpunkt | Belegt diesen historischen Ansatz, nicht automatisch die spätere Integraldefinition oder D. |
| 09.10.2025, [README bei Commit 3816c52](https://github.com/HelabHLC/arbe-lambda/blob/3816c52/README.md) und [Release v3.0](https://github.com/HelabHLC/arbe-lambda/releases/tag/v3.0) | Bereits explizit $\lambda^*=\lambda_{min}+\int R$; dort Bereich 300–730 nm | Die geschlossene Integralform war schon im eigenen Projekt dokumentiert. Der andere Bereich und das dortige UV-Δλ sind keine heutige Core-Definition. |
| 07.11.2025, [Release v2.1](https://github.com/HelabHLC/arbe-lambda/releases/tag/v2.1) | Δλ* = EE − V2 | Öffentliche Projektbeschreibung dieser Kombination spätestens im so datierten Release; kein externer Erstheitsbeweis. Für heutige Vergleiche Vorzeichen umkehren. |
| 14.02.2026, [Formal Specification 1.0.0](https://github.com/HelabHLC/arbe-lambda/releases/tag/lambdaV2-1.0.0), [Zenodo 18644381](https://doi.org/10.5281/zenodo.18644381) | Ungewichtete Integralbilanz auf 380–730 nm, Brent-Vorgabe | Grundlage der jetzigen Prüfung. |
| Aktueller Ausgangscommit, [README](https://github.com/HelabHLC/arbe-lambda/blob/cb566dddca3adeecbd8ac3b8ac352d270d7df585/README.md) | D = V2 − EE; pauschaler Ausschluss von Mittelwertverfahren; Bezeichnung als Asymmetrie | Vorzeichen ausdrücklich festhalten; mathematisch zu weitgehende Ausschlüsse und Interpretation klarstellen. |
| Derselbe Commit, [arbe_lambda.py](https://github.com/HelabHLC/arbe-lambda/blob/cb566dddca3adeecbd8ac3b8ac352d270d7df585/arbe_lambda.py) | Erster ansteigender Schnitt mit $\sqrt2-1$ | Dessen bestandene Tests sind keine V2-Integraltests. |

Release-Beschreibungen können nach Veröffentlichung bearbeitet werden. Die
eingesehenen Veröffentlichungsdaten und Texte begründen daher eine dokumentierte
Projektchronologie, keine forensisch gesicherte früheste Priorität jeder Formel.
Der Inhaltsbefund des alten README ist zusätzlich über seinen Git-Commit prüfbar.
Die Zenodo-API-Metadaten wurden gelesen; die Originaldatei von 16414720 ebenfalls.
Die ZIP-Dateien von 17038866 und 18644381 wurden in dieser Prüfung nicht erneut
entpackt. Auffällig: DOI 17038866 gehört laut Metadaten zum v2.0-Release vom
04.09.2025, obwohl spätere v3.0/v2.1-Release-Texte ihn ebenfalls zitieren.
Ein solcher DOI-Link allein belegt nicht den Inhalt einer späteren Erweiterung.

## 4. Vergleich mit externen Primärquellen

Die folgenden Aussagen betreffen die tatsächlich eingesehenen Abschnitte oder
Formeln; sie sind keine Behauptung, den gesamten Publikationsbestand abzudecken.

| Quelle | Vergleich | Bewertung für den exakten D-Ausdruck |
|---|---|---|
| [NIST Dataplot: Skewness](https://www.itl.nist.gov/div898/software/dataplot/refman2/auxillar/skewness.htm), Implementierung laut Seite vor 1987 | Standardisiertes drittes zentrales Moment | Klassischer Vorläufer der Momentenbegriffe; keine identische D-Definition. |
| James M. Palmer, [Bandwidth Normalization by Moments](https://wp.optics.arizona.edu/jpalmer/wp-content/uploads/sites/65/2017/03/MOMENTS-BANDWIDTH-NORMALIZATION-.pdf), University of Arizona, undatierte PDF | Fläche, Schwerpunkt $M_1/M_0$, Varianz und äquivalente Bandgrenzen aus spektraler Empfindlichkeit | Sehr verwandte mathematische Bausteine; andere Größe und Kombination. Kein Publikationsdatum aus dem URL-Pfad als Prioritätsbeweis abgeleitet. |
| [MathWorks: Spectral Descriptors](https://www.mathworks.com/help/audio/ug/spectral-descriptors.html), aktuelle Herstellerdokumentation, mit Verweis auf Peeters 2004 | Schwerpunkt, Breite und Schiefe eines Spektrums | Etablierte Beschreibung, hier Audio; kein identischer D-Ausdruck. Der aktuelle Text ist kein historischer Erstbeleg. |
| Salas & Henebry, [Moment Distance Method](https://doi.org/10.3390/rs6010020), online 19.12.2013, Band 2014, §2.2, Gleichungen 1–3 | Differenz der Summen geometrischer Abstände zu zwei Randpunkten | Ähnlicher Zweck und Differenzbildung, andere Funktion. Bei konstantem R und symmetrischem Raster ist MDI null; D ist für R=0.2 gleich −105 nm. Keine allgemeine Identität. |
| [A generalized approach to characterize optical properties of natural objects](https://doi.org/10.1093/biolinnean/blac064), 2022, Tabelle 2 | Integrierte und mittlere Reflexion als bestehende Kenngrößen | Belegt die Flächen-/Mittelwert-Bausteine; kein identischer D-Ausdruck in der eingesehenen Tabelle. |
| Zeaieanfirouzabadi & Salahian, [DSRC](https://doi.org/10.5194/isprs-annals-X-5-W2-2025-725-2025), veröffentlicht 19.12.2025, §§1.2.1–1.2.3 | Fläche unter Reflexionskurve, Flächenschwerpunkt, Dreiecksflächen und euklidischer Abstand des Schwerpunkts zum Koordinatenursprung | Besonders naher Anwendungsansatz, aber die angegebenen Merkmale enthalten nicht D. Veröffentlichung liegt nach dem datierten ARBE-v2.1-Release; deshalb nicht als früherer D-Beleg behandelt. |

Die DSRC-Gleichungen wurden im PDF einschließlich der Abbildungen geprüft.
Ein Flächenschwerpunkt in x-Richtung entspricht bei einer unter R liegenden
Fläche dem reflexionsgewichteten Schwerpunkt; der dortige euklidische Abstand
und die Dreiecksflächen sind dennoch andere Merkmale als $a+I_0-c$.
Ein entsprechendes gemeinsames Merkmalsset kann mehr Informationen enthalten
als D allein, ohne dieselbe einzelne Kennzahl zu definieren.

## 5. Suchumfang und Grenzen

Am 08.11.2026 wurden zwei Web-Suchsysteme verwendet. Das
[Suchprotokoll](delta-lambda-search-log-2026-11-08.json) enthält 30 Anfragen aus
diesem Prüflauf, darunter Namenssuche, mathematische Umschreibungen und
benachbarte spektrale Verfahren. Danach wurden einschlägige Primärquellen,
Git-Historie, Release-Texte und die genannten Zenodo-Metadaten nachgelesen.
Suchtreffer aus Social Media oder Sekundärportalen wurden nicht als unabhängige
Bestätigung der Neuheit übernommen.

Zugriffsgrenzen: Die Original-Peeters-PDF ließ sich über beide geprüften
IRCAM-Adressen nicht öffnen. Der MDPI-Volltextzugriff gab HTTP 429 zurück;
§2.2 einschließlich der Formeln war über die indexierte Verlagsquelle lesbar.
Bei Oxford war die Verlags-Tabelle indexiert, der direkte Volltextzugriff
scheiterte. Diese Beschränkungen werden nicht als Negativbeweise gewertet.
Es erfolgte keine vollständige Recherche in Scopus/Web of Science, keine
erschöpfende Suche nicht indexierter oder fremdsprachiger Literatur und keine
patentjuristische Prüfung. Öffentlich datierte Eigenbeschreibungen sind keine
unabhängige Validierung. Später auffindbare Quellen können den Befund ändern.

**Recherchebefund:** Kein identischer externer Vorläufer des exakt definierten
D wurde im dokumentierten Umfang gefunden. Das rechtfertigt weder „weltweit
erstmals“ noch „bewiesen nicht neu“. Der Neuheitsstatus bleibt offen.

## 6. Belastbare wissenschaftliche Formulierung

> ARBE λ*_V2 kodiert die ungewichtete mittlere Reflexion eines festgelegten
> Spektralintervalls als Wellenlängenkoordinate. Δλ* kombiniert diese Größe mit
> dem reflexionsgewichteten Schwerpunkt. Die Kombination ist im ARBE-Projekt
> dokumentiert und aus klassischen Integralgrößen exakt rekonstruierbar. Die
> bisherige Recherche hat keinen identischen externen Vorläufer nachgewiesen;
> historische Erstheit und ein besonderer Anwendungsnutzen sind nicht belegt.

Ein sinnvoller Beitrag kann in nachvollziehbarer Darstellung, Reproduzierbarkeit
oder einer konkreten Anwendung liegen. Die mathematische Herleitung ist dafür
eine geklärte Grundlage, kein Ersatz für den Anwendungsnachweis.

Für eine externe Prüfung lassen sich nun zwei präzise Fragen stellen:

1. Findet sich eine datierte frühere Quelle für dieselbe Funktion, auch mit
   anderem Namen, Vorzeichen oder Skalierung?
2. Verbessert D bei einer vorab bestimmten Aufgabe ein vorab bestimmtes
   Ergebnis gegenüber den fairen Vergleichsgrößen Mittelreflexion und EE
   gemeinsam sowie passenden etablierten Verfahren?

Diese Fragen wurden nicht an Dritte versandt. Ein GitHub-Eintrag oder eine
bestandene Softwareprüfung darf nicht als deren externe Bestätigung bezeichnet
werden. Es wurden keine Masterdaten, alten Release-Texte, DOI-Archive oder
bereits bestehenden Forschungsprotokolle verändert.
