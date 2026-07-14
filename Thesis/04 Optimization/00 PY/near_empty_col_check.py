from pathlib import Path

def find_project_root(marker: str = ".git") -> Path:
    """Laeuft vom Skriptpfad aus nach oben, bis der Marker (Standard: .git-Ordner)
    gefunden wird. Funktioniert unabhaengig von Nutzername, Laufwerk und davon,
    wie tief das Skript im Ordnerbaum liegt."""
    p = Path(__file__).resolve()
    for parent in p.parents:
        if (parent / marker).exists():
            return parent
    raise RuntimeError(f"Projekt-Root nicht gefunden (kein '{marker}' oberhalb von {p})")


PROJECT_ROOT = find_project_root()

import pdfplumber
import re

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

STRAY_RE = re.compile(r"^[\W_]{1,2}$", re.UNICODE)

def is_blank(cell):
    return cell is None or str(cell).strip() == ""

def main():
    near_empty_examples = []
    n_nonblank_cols = 0
    n_stray_cols = 0

    for folder in FOLDERS:
        for pdf_path in sorted((BASE_IN / folder).glob("*.pdf")):
            with pdfplumber.open(pdf_path) as pdf:
                for pno, page in enumerate(pdf.pages, 1):
                    for t in page.find_tables(table_settings=TABLE_SETTINGS):
                        rows = t.extract()
                        if not rows:
                            continue
                        n_cols = max(len(r) for r in rows)
                        for c in range(n_cols):
                            col_vals = [r[c] if c < len(r) else None for r in rows]
                            if all(is_blank(v) for v in col_vals):
                                continue  # komplett leer, hier nicht relevant
                            n_nonblank_cols += 1
                            non_blank_vals = [str(v).strip() for v in col_vals if not is_blank(v)]
                            # Spalte gilt als 'stray', wenn ALLE nicht-leeren Werte
                            # kurze Stoerzeichen sind
                            if all(STRAY_RE.match(v) for v in non_blank_vals):
                                n_stray_cols += 1
                                if len(near_empty_examples) < 15:
                                    near_empty_examples.append(
                                        (f"{folder}/{pdf_path.stem}", pno, non_blank_vals[:5]))

    print(f"Nicht-leere Spalten insgesamt : {n_nonblank_cols}")
    print(f"  davon nur Stoerzeichen      : {n_stray_cols}  "
          f"({n_stray_cols/n_nonblank_cols*100:.1f}%)")
    print("\nBeispiele (Dokument, Seite, gefundene Werte):")
    for doc, pno, vals in near_empty_examples:
        print(f"  {doc} S.{pno}: {vals}")

if __name__ == "__main__":
    main()
