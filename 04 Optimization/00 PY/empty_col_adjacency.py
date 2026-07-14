from pathlib import Path

def find_project_root(marker: str = ".git") -> Path:
    p = Path(__file__).resolve()
    for parent in p.parents:
        if (parent / marker).exists():
            return parent
    raise RuntimeError(f"Projekt-Root nicht gefunden (kein '{marker}' oberhalb von {p})")

PROJECT_ROOT = find_project_root()

import pdfplumber

BASE_IN = Path(PROJECT_ROOT / "02 Markdown/01 Training/01 PDF")
FOLDERS = ["01 IBU", "02 IFT", "03 IAB"]

TABLE_SETTINGS = {
    "vertical_strategy": "lines",
    "horizontal_strategy": "lines",
    "snap_tolerance": 3,
    "join_tolerance": 3,
    "edge_min_length": 3,
    "min_words_vertical": 3,
    "min_words_horizontal": 1,
    "intersection_tolerance": 3,
    "text_tolerance": 3,
}

def is_blank(cell):
    return cell is None or str(cell).strip() == ""

def col_is_empty(rows, c):
    return all(is_blank(r[c] if c < len(r) else None) for r in rows)

def classify_empty_columns(rows):
    if not rows:
        return {"single_between_data": 0, "multi_consecutive": 0, "edge": 0}
    n_cols = max(len(r) for r in rows)
    empty_flags = [col_is_empty(rows, c) for c in range(n_cols)]

    counts = {"single_between_data": 0, "multi_consecutive": 0, "edge": 0}
    c = 0
    while c < n_cols:
        if not empty_flags[c]:
            c += 1
            continue
        start = c
        while c < n_cols and empty_flags[c]:
            c += 1
        run_len = c - start
        left_ok = start > 0          
        right_ok = c < n_cols        
        if not left_ok or not right_ok:
            counts["edge"] += run_len
        elif run_len == 1:
            counts["single_between_data"] += 1
        else:
            counts["multi_consecutive"] += run_len
    return counts

def main():
    totals = {"single_between_data": 0, "multi_consecutive": 0, "edge": 0}
    for folder in FOLDERS:
        for pdf_path in sorted((BASE_IN / folder).glob("*.pdf")):
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    for t in page.find_tables(table_settings=TABLE_SETTINGS):
                        rows = t.extract()
                        if not rows:
                            continue
                        c = classify_empty_columns(rows)
                        for k in totals:
                            totals[k] += c[k]

    total_empty = sum(totals.values())
    print("=== Klassifikation leerer Spalten (ueber alle 12 Trainings-PDFs) ===")
    print(f"Einzelne leere Spalte zwischen zwei Datenspalten (sicherer Merge) : "
          f"{totals['single_between_data']:5d}  ({totals['single_between_data']/total_empty*100:.1f}%)")
    print(f"Mehrere aufeinanderfolgende leere Spalten (Merge riskanter)      : "
          f"{totals['multi_consecutive']:5d}  ({totals['multi_consecutive']/total_empty*100:.1f}%)")
    print(f"Leere Spalte am Rand der Tabelle                                  : "
          f"{totals['edge']:5d}  ({totals['edge']/total_empty*100:.1f}%)")
    print(f"Gesamt leere Spalten                                              : {total_empty:5d}")

if __name__ == "__main__":
    main()
