# document-extraction-pipeline
## KI-gestützte Extraktion strukturierter Ökobilanzdaten aus Umweltproduktdeklarationen (EPDs)

**Begleitendes Code-Repository zur Bachelorarbeit**

> **Konzeption und Evaluation eines KI-gestützten Ansatzes zur Extraktion und Strukturierung unstrukturierter Bauproduktdaten**
>
> Abdullah Azizi · Hochschule Esslingen, Studiengang Wirtschaftsingenieurwesen · Juli 2026
>
> Erstprüfer: Prof. Dr.-Ing. Philipp Bulling (Hochschule Esslingen)
> Zweitprüfer: Robert Böker, Dipl.-Ing. (WoodenValley gGmbH)
>
> Entstanden im Kontext des Forschungsprojekts **GEFION** („Generierung digitaler Emissionszertifikate für klimapositive Holzsystembauten") und des Demonstrators **ReBuild** am Campus Göppingen der Hochschule Esslingen.

---

## Forschungsfrage

> *Inwiefern lässt sich die Extraktion strukturierter Ökobilanzindikatoren aus heterogen formatierten Umweltproduktdeklarationen mittels eines Zero-Shot-Prompting-Ansatzes methodisch zuverlässig automatisieren, und welchen Einfluss haben Konverterwahl und Prompt-Gestaltung auf die Extraktionsqualität?*

Untersucht anhand dreier Teilfragen: (1) Einfluss der PDF-zu-Markdown-Konverterwahl und ihrer Parameteroptimierung, (2) Reduktion der Halluzinationsrate durch fehlergetriebene Prompt-Regeln und deren Konverterabhängigkeit, (3) Generalisierung von einem Trainings- auf ein unabhängiges Testkorpus.

## Untersuchungsdesign

**2×2-faktorielles Design:** zwei Konverter × zwei Prompt-Stufen, alle übrigen Faktoren fixiert.

| Faktor | Stufe 1 | Stufe 2 |
|---|---|---|
| PDF-zu-Markdown-Konverter | `pdfplumber` (geometrisch, linienbasiert) | `pymupdf4llm` (GNN-basierter Layoutmodus) |
| Prompt (TELeR-Taxonomie) | Level 1 „Basis" (Ein-Satz-Direktive) | Level 3 „prompt optimized" (8 fehlergetriebene Regeln) |

- **Modell:** `claude-haiku-4-5` (Anthropic API), `temperature=0`, fixiert über alle Läufe
- **Daten:** 24 EPDs dreier Programmhalter (IBU, ift Rosenheim, EPD International AB), stratifiziert in **12 Trainings- und 12 Held-out-Testdokumente** (je 4 pro Programmhalter und Split)
- **Zielschema:** flaches Pydantic-Schema mit **269 optionalen Feldern** (17 allgemeine Felder + 21 Indikatoren × 12 Lebenszyklusmodule nach EN 15804+A2), abgeleitet aus den DGNB-Kriterien ENV1.1–ENV1.3 und TEC1.6
- Sämtliche Optimierungsschritte erfolgten ausschließlich auf den Trainingsdaten; das Testset wurde genau einmal, mit eingefrorenen Parametern, evaluiert

## Pipeline-Architektur

```
                                    ┌─────────────────┐
                                    │  Pydantic-Schema │  269 Felder
                                    │   (01 Schema)    │  (deklarativ)
                                    └────────┬────────┘
                                             │ Feldnamen / Typinfo
                                             ▼
┌──────────┐   ┌──────────────────┐   ┌──────────────────┐   ┌─────────────┐
│ PDF (EPD) │ → │ Konvertierung     │ → │ Zero-Shot-        │ → │ JSON-Objekt │
│           │   │ pdfplumber /      │   │ Extraktion        │   │             │
│           │   │ pymupdf4llm       │   │ claude-haiku-4-5  │   │             │
└──────────┘   │ (02 Markdown)     │   │ T=0 (03 Extraktion)│  └──────┬──────┘
               └──────────────────┘   └──────────────────┘          │
                                                                     ▼
                                                          ┌──────────────────┐
                                                          │ Evaluation gegen  │
                                                          │ Ground Truth      │
                                                          │ ARE/NLD/Status    │
                                                          │ (05 Evaluation)   │
                                                          └──────────────────┘
```

Das Pydantic-Schema wird bewusst **rein deklarativ** genutzt: Es liefert dem Extraktionsskript die Feldnamen für den Prompt und dem Evaluator die Typinformation zur Metrikauswahl. Eine Laufzeit-Validierung findet nicht statt, damit Extraktionsfehler (z. B. Koextraktion von Zahl und Einheit) sichtbar bleiben und nicht maskiert werden.

## Zentrale Ergebnisse

### Halluzinationsreduktion durch fehlergetriebene Prompt-Regeln (Held-out-Testset)

| Variante | MARE | MNLD | Halluzination | Omission |
|---|---|---|---|---|
| pdfplumber Basis | 0,0805 | 0,1231 | 9,4 % | 2,0 % |
| pymupdf4llm Basis | 0,0462 | 0,2231 | 16,0 % | 2,1 % |
| pdfplumber prompt optimized | 0,0902 | 0,0453 | **4,3 %** | 3,4 % |
| pymupdf4llm prompt optimized | 0,0321 | 0,0986 | **2,7 %** | 6,2 % |

Die acht fehlergetriebenen TELeR-Level-3-Regeln senken die Halluzinationsrate **konverterübergreifend deutlich**. Da fälschlich extrahierte Werte, anders als fehlende, nicht als Lücke erkennbar sind, ist dies der praxisrelevanteste Effekt für die Ökozertifizierung.

### Dokumentierte Negativbefunde

1. **Optuna-Konverteroptimierung (pdfplumber):** Kein Trial von 20 (TPESampler, seed=42) unterbietet die Default-Baseline. Bei sauberen, linienbasierten Vektor-PDFs erkennt pdfplumber die Tabellenstruktur bereits mit Standardwerten korrekt (kleinste inhaltstragende Zelle: 5,03 pt > Default-Toleranz 3 pt); zusätzlich ist die Zielgröße ARE strukturell blind für den tatsächlichen Wirkungsbereich des Konverters.
2. **Konverteroptimierung (pymupdf4llm):** Strukturell nicht anwendbar — kein geeigneter kontinuierlicher Parameterraum vorhanden (fester GNN-Layoutmodus statt geometrischer Toleranzen).
3. **Deterministisches Post-Processing (Spaltenbereinigung):** Entfernen/Verschmelzen leerer Tabellenspalten verschlechtert die Extraktion (Halluzination: 192 → 362 Fälle). Arbeitshypothese: leere Spalten dienen dem Modell als strukturelles Ausrichtungssignal zwischen Kopfzeilen und Werten.

### Konverterabhängigkeit der Prompt-Wirkung (methodischer Kernbeitrag)

Dieselbe, unveränderte Prompt-Regel wirkt je nach vorgelagerter Konvertierungsstufe unterschiedlich: Bei **intakter Tabellenstruktur** (pdfplumber) adressiert die label-basierte Zeilenzuordnungsregel Fehler wirksam (u. a. vollständige Auflösung einer C3/C4-Spaltenversatz-Regression); bei **strukturell verzerrtem Markdown** (pymupdf4llm, PERT/PENRT-Kernfehler) stößt dieselbe Regel an ihre Grenzen. Der wissenschaftliche Beitrag liegt nicht in der Prompt-Verbesserung selbst, sondern in der **Methodik ihrer fehlergetriebenen Ableitung** und im Nachweis dieser **eingabestrukturabhängigen Adressierbarkeit** von Extraktionsfehlern.

### Generalisierungslücke

Die MARE steigt für alle vier Varianten von Training zu Test (am stärksten pdfplumber prompt optimized: 0,0079 → 0,0902). Klassisches Overfitting scheidet als Erklärung aus (keine Parameteränderung zwischen Training und Test, Optuna-Negativbefund, generische Regeln); ursächlich sind im Testset erstmals auftretende Werteausprägungen (z. B. Freitext oder „ND" in numerischen Feldern), die eine rein auf Trainingsfehlern basierende Regelableitung naturgemäß nicht antizipieren kann — dokumentiert als Grenze fehlergetriebener Prompt-Optimierung bei kleiner Stichprobe.

## Evaluationsmetriken

| Metrik | Anwendung | Quelle |
|---|---|---|
| **ARE / MARE** — `\|g−p\| / max(\|g\|,\|p\|)` | numerische Felder | Moayeri et al., ACM FAccT 2024 (Betragsbildung im Nenner: eigene Ergänzung für negative Ökobilanzwerte) |
| **NLD / MNLD** — `LD / max(len)` | Text-/Listenfelder | Biten et al., ICDAR 2019 (DOI 10.1109/ICDAR.2019.00251) |
| **Bool-Match** | boolesche Felder | — |
| **Vierwertige Statustaxonomie** — present / omission / hallucination / absent | alle Felder, vor Metrikberechnung | eigene Operationalisierung, konzeptionell nach Dušek & Kasner, INLG 2020 |

Bekannte, dokumentierte Metrik-Limitation: ARE = 1 für alle Fälle GT = 0, Extraktion ≠ 0, unabhängig von der Größenordnung — MARE-Werte sind daher als obere Schranke zu lesen.

## Ordnerstruktur

```
document-extraction-pipeline/
├── 01 Schema/
│   └── epd.py                                # Pydantic-Zielschema (269 optionale Felder)
│
├── 02 Markdown/                              # Schritt 1: PDF → Markdown
│   ├── 01 Training/00 PY/
│   │   ├── converter_pdfplumber_plain.py
│   │   ├── converter_pdfplumber_optimized.py # Post-Processing (Negativbefund, s. o.)
│   │   └── converter_pymupdf4llm_plain.py
│   └── 02 Test/00 PY/                        # *_test.py-Pendants
│
├── 03 Extraktion/                            # Schritt 2: Markdown → JSON (Anthropic API)
│   ├── 01 Training/00 PY/
│   │   ├── extractor_plain.py                # TELeR Level 1 (Basis)
│   │   └── extractor_optimized_prompt.py     # TELeR Level 3 (8 Regeln)
│   └── 02 Test/00 PY/                        # *_test.py-Pendants
│
├── 04 Optimization/00 PY/                    # Optuna-Studie + Diagnoseskripte
│   ├── optimizor.py                          # Optuna, TPESampler(seed=42), Suchraum [0, 5.03] pt
│   ├── diagnose_objective.py                 # belegt Sättigung der Median-Zielfunktion
│   ├── diagnose_optimized_regression.py      # belegt Post-Processing-Regression
│   ├── completeness_check.py                 # Statusvergleich pdfplumber vs. pymupdf4llm
│   ├── table_artifact_scan.py                # corpus-weite Quantifizierung leerer Zeilen/Spalten
│   ├── empty_col_adjacency.py                # Klassifikation leerer Spalten (Rand/isoliert/mehrfach)
│   ├── near_empty_col_check.py               # Störzeichen-Kontaminationscheck
│   ├── plot_trials.py                        # Optuna-Trial-Visualisierung (Nullbefund)
│   └── token_vergleich.py                    # Token-Umfang Markdown vs. Rohtext (+34 % im Mittel)
│
└── 05 Evaluation/                            # Schritt 3: Vergleich gegen Ground Truth
    ├── 00 Ground Truth/
    │   ├── ground_truth_training.json        # 12 EPDs, manuell erstellt und QS-geprüft
    │   └── ground_truth_test.json            # 12 Held-out-EPDs, strikt getrennt
    ├── 01 Training/
    │   ├── 00 PY/evaluator_training.py
    │   └── evaluation_comparison_training.xlsx
    ├── 02 Test/
    │   ├── 00 PY/evaluator_test.py
    │   └── evaluation_comparison_test.xlsx
    └── publisher_breakdown.py                # herausgeberspezifische Aufschlüsselung (Kap. 6.4)
```

## Reproduktion

**Voraussetzungen:** Python ≥ 3.11, Anthropic-API-Schlüssel.

```bash
git clone https://github.com/azizi-ai/document-extraction-pipeline.git
cd document-extraction-pipeline
pip install pdfplumber pymupdf4llm anthropic pydantic optuna openpyxl
export ANTHROPIC_API_KEY="sk-..."
```

Alle Skripte lokalisieren den Projekt-Root zur Laufzeit selbst (Suche nach `.git` oberhalb des Skriptpfads) — es sind keine Pfadanpassungen nötig. Ablauf je Split (Training/Test): Konverter-Skript → Extraktor-Skript → Evaluator-Skript. Die EPD-Quelldokumente müssen zuvor aus den unten verlinkten Quellen bezogen und unter `02 Markdown/<Split>/01 PDF/{01 IBU, 02 IFT, 03 IAB}/` abgelegt werden (Dateinamen gemäß Ground-Truth-Schlüsseln, z. B. `ibu_01_bwf.pdf`).

**Hinweis zur Reproduzierbarkeit:** `temperature=0` macht die Extraktion nahezu, aber nicht vollständig deterministisch (Nichtassoziativität von Gleitkommaoperationen, serverseitige Batch-Effekte). Geringfügige Abweichungen einzelner Werte bei Wiederholungsläufen sind möglich.

## Datenquellen (EPDs)

Die verwendeten EPD-PDFs sind aus Urheberrechtsgründen nicht Teil dieses Repositories (Rechte der jeweiligen Programmhalter/Deklarationsinhaber). Alle 24 Quelldokumente sind hier zur Nachvollziehbarkeit verlinkt.

### Training (12 EPDs)

| Code | Programmhalter | Produkt/Dokument | Quelle |
|---|---|---|---|
| `ibu_01_bwf` | IBU | best wood FLEX 50 | [epd-online.com/.../22138](https://epd-online.com/PublishedEpd/Download/22138) |
| `ibu_02_lvl` | IBU | Pollmeier Fichte LVL | [epd-online.com/.../22394](https://epd-online.com/PublishedEpd/Download/22394) |
| `ibu_03_ply` | IBU | Sperrholz aus Laubholzfurnier | [epd-online.com/.../5577](https://epd-online.com/PublishedEpd/Download/5577) |
| `ibu_04_kpb` | IBU | Spanplatte roh, Furnier, Melamin, CPL | [epd-online.com/.../15934](https://epd-online.com/PublishedEpd/Download/15934) |
| `ift_01_hfo` | ift Rosenheim | Haustür (HM Eckelhausen) | [PDF](https://www.ift-rosenheim.de/fileadmin/IFT/Zertifizierung/Nachhaltigkeit/Dokumente/EPDs_Deutsch/2024-07-17_EPD_HMEckelhausen_Haustuer.pdf) |
| `ift_02_sfe` | ift Rosenheim | EPD-SFE-92.0 | [PDF](https://www.ift-rosenheim.de/fileadmin/IFT/Zertifizierung/Nachhaltigkeit/Dokumente/EPDs_Deutsch/EPD-SFE-92.0.pdf) |
| `ift_03_sha` | ift Rosenheim | EPD-SHA-75.0.01 | [PDF](https://www.ift-rosenheim.de/fileadmin/IFT/Zertifizierung/Nachhaltigkeit/Dokumente/EPDs_Deutsch/EPD-SHA-75.0.01.pdf) |
| `ift_04_sis` | ift Rosenheim | EPD-SIS-75.1.01 | [PDF](https://www.ift-rosenheim.de/fileadmin/IFT/Zertifizierung/Nachhaltigkeit/Dokumente/EPDs_Deutsch/EPD-SIS-75.1.01.pdf) |
| `iab_01_bsh` | EPD International AB | environdec Library | [epd17091](https://www.environdec.com/library/epd17091) |
| `iab_02_ntc` | EPD International AB | environdec Library | [epd15637](https://www.environdec.com/library/epd15637) |
| `iab_03_gwf` | EPD International AB | environdec Library | [epd11052](https://environdec.com/library/epd11052) |
| `iab_04_spc` | EPD International AB | environdec Library | [epd28962](https://www.environdec.com/library/epd28962) |

### Test (12 Held-out-EPDs)

| Code | Programmhalter | Produkt/Dokument | Quelle |
|---|---|---|---|
| `ibu_01_bsh` | IBU | epd-online Library | [epd-online.com/.../22140](https://epd-online.com/PublishedEpd/Download/22140) |
| `ibu_02_hfd` | IBU | Holzfaserdämmplatten, Trockenverfahren (Sto) | [PDF](https://www.sto.de/cepcom/de/Dokumente/Service-Tools/EPD/EPD-STE-20200173-IBA1-DE-Holzfaserd%C3%A4mmplatten-aus-dem-Trockenverfahren.pdf) |
| `ibu_03_kvh` | IBU | epd-online Library | [epd-online.com/.../19966](https://epd-online.com/PublishedEpd/Download/19966) |
| `ibu_04_adp` | IBU | Akustikdämmplatte | *kein öffentlicher Link verfügbar* |
| `ift_01_rah` | ift Rosenheim | EPD-RAH-54.0 | [PDF](https://www.ift-rosenheim.de/fileadmin/IFT/Zertifizierung/Nachhaltigkeit/Dokumente/EPDs_Deutsch/EPD-RAH-54.0.pdf) |
| `ift_02_rih` | ift Rosenheim | EPD-RIH-54.0 | [PDF](https://www.ift-rosenheim.de/fileadmin/IFT/Zertifizierung/Nachhaltigkeit/Dokumente/EPDs_Deutsch/EPD-RIH-54.0.pdf) |
| `ift_03_sps` | ift Rosenheim | EPD-SPS-75.1.01 | [PDF](https://www.ift-rosenheim.de/fileadmin/IFT/Zertifizierung/Nachhaltigkeit/Dokumente/EPDs_Deutsch/EPD-SPS-75.1.01.pdf) |
| `ift_04_atd` | ift Rosenheim | EPD-ATD-36.0 | [PDF](https://www.ift-rosenheim.de/fileadmin/IFT/Zertifizierung/Nachhaltigkeit/Dokumente/EPDs_Deutsch/EPD-ATD-36.0.pdf) |
| `iab_01_bsp` | EPD International AB | CLT (Stora Enso) | [epd9949](https://www.environdec.com/library/epd9949) |
| `iab_02_srx` | EPD International AB | environdec Library | [epd14262](https://environdec.com/library/epd14262) |
| `iab_03_swf` | EPD International AB | environdec Library | [epd16520](https://www.environdec.com/library/epd16520) |
| `iab_04_lvt` | EPD International AB | environdec Library | [epd28961](https://www.environdec.com/library/epd28961) |

## Abgrenzung

Dieses Repository enthält den vollständigen Quellcode der Pipeline, die Ground-Truth-Daten und die aggregierten Evaluationsergebnisse. **Nicht enthalten** sind: der Thesistext selbst, die EPD-Quell-PDFs (Rechte Dritter, siehe Verlinkung oben), Markdown-/Extraktions-Zwischenergebnisse sowie verworfene Skript-Zwischenstände aus der Entwicklungsphase.

## Zitation

```bibtex
@thesis{azizi2026epd,
  author = {Azizi, Abdullah},
  title  = {Konzeption und Evaluation eines KI-gest{\"u}tzten Ansatzes zur
            Extraktion und Strukturierung unstrukturierter Bauproduktdaten},
  school = {Hochschule Esslingen},
  type   = {Bachelorarbeit},
  year   = {2026},
  month  = {7}
}
```

## Lizenz

MIT License — siehe [LICENSE](./LICENSE). Die Lizenz gilt für den Quellcode dieses Repositories; die verlinkten EPD-Dokumente unterliegen den Rechten der jeweiligen Programmhalter.
