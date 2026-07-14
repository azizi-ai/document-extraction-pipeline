from pathlib import Path

def find_project_root(marker: str = ".git") -> Path:
    p = Path(__file__).resolve()
    for parent in p.parents:
        if (parent / marker).exists():
            return parent
    raise RuntimeError(f"Projekt-Root nicht gefunden (kein '{marker}' oberhalb von {p})")

PROJECT_ROOT = find_project_root()

rom pathlib import Path
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

def analyze_table(rows):
    if not rows:
        return 0, 0, 0, 0
    n_rows = len(rows)
    n_cols = max(len(r) for r in rows)
    empty_rows = sum(1 for r in rows if all(is_blank(c) for c in r))
    empty_cols = 0
    for c in range(n_cols):
        col_vals = [r[c] if c < len(r) else None for r in rows]
        if all(is_blank(v) for v in col_vals):
            empty_cols += 1
    return empty_rows, empty_cols, n_rows, n_cols


def main():
    totals = {"tables": 0, "rows": 0, "cols": 0, "empty_rows": 0, "empty_cols": 0}
    per_doc = []

    for folder in FOLDERS:
        for pdf_path in sorted((BASE_IN / folder).glob("*.pdf")):
            doc_id = f"{folder}/{pdf_path.stem}"
            d_tables = d_rows = d_cols = d_er = d_ec = 0
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    for t in page.find_tables(table_settings=TABLE_SETTINGS):
                        rows = t.extract()
                        if not rows:
                            continue
                        er, ec, nr, nc = analyze_table(rows)
                        d_tables += 1
                        d_rows += nr
                        d_cols += nc
                        d_er += er
                        d_ec += ec
            per_doc.append((doc_id, d_tables, d_rows, d_er, d_cols, d_ec))
            for k, v in zip(totals, (d_tables, d_rows, d_cols, d_er, d_ec)):
                totals[k] += v

    print(f"{'Dokument':<20} {'Tabellen':>8} {'Zeilen':>7} {'leer%':>7} {'Spalten':>8} {'leer%':>7}")
    for doc_id, nt, nr, er, nc, ec in per_doc:
        row_pct = er / nr * 100 if nr else 0
        col_pct = ec / nc * 100 if nc else 0
        print(f"{doc_id:<20} {nt:>8} {nr:>7} {row_pct:>6.1f}% {nc:>8} {col_pct:>6.1f}%")

    print("\n=== Gesamt ===")
    print(f"Tabellen erkannt      : {totals['tables']}")
    print(f"Zeilen gesamt         : {totals['rows']}")
    print(f"  davon leer (Split)  : {totals['empty_rows']}  ({totals['empty_rows']/totals['rows']*100:.1f}%)")
    print(f"Spalten gesamt        : {totals['cols']}")
    print(f"  davon leer (Blaeh.) : {totals['empty_cols']}  ({totals['empty_cols']/totals['cols']*100:.1f}%)")

if __name__ == "__main__":
    main()
