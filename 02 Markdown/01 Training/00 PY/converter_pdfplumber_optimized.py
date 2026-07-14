from pathlib import Path

def find_project_root(marker: str = ".git") -> Path:
    p = Path(__file__).resolve()
    for parent in p.parents:
        if (parent / marker).exists():
            return parent
    raise RuntimeError(f"Projekt-Root nicht gefunden (kein '{marker}' oberhalb von {p})")

PROJECT_ROOT = find_project_root()

import pdfplumber

BASE_IN  = Path(PROJECT_ROOT / "02 Markdown/01 Training/01 PDF")
BASE_OUT = Path(PROJECT_ROOT / "02 Markdown/01 Training/02 MD/02 pdfplumber optimized")
FOLDERS = ["01 IBU", "02 IFT", "03 IAB"]

TABLE_SETTINGS = {
    "vertical_strategy": "lines",
    "horizontal_strategy": "lines",
    "snap_x_tolerance": 3,
    "snap_y_tolerance": 3,
    "join_x_tolerance": 3,
    "join_y_tolerance": 3,
    "edge_min_length": 3,
    "min_words_vertical": 3,
    "min_words_horizontal": 1,
    "intersection_x_tolerance": 3,
    "intersection_y_tolerance": 3,
    "text_x_tolerance": 3,
    "text_y_tolerance": 3,
}

def is_empty(cell):
    return cell is None or str(cell).strip() == ""

def drop_edge_empty_columns(rows):
    if not rows or not rows[0]:
        return rows
    n_cols = len(rows[0])
    empty = [all(is_empty(r[j]) for r in rows if j < len(r)) for j in range(n_cols)]
    left = 0
    while left < n_cols and empty[left]:
        left += 1
    right = n_cols
    while right > left and empty[right - 1]:
        right -= 1
    if left >= right:
        return rows  # komplett leere Tabelle: unveraendert lassen (sonst keine Trennzeile mehr)
    return [r[left:right] for r in rows]

def merge_isolated_empty_columns(rows):
    if not rows or not rows[0]:
        return rows
    n_cols = len(rows[0])
    empty = [all(is_empty(r[j]) for r in rows if j < len(r)) for j in range(n_cols)]
    drop = set()
    merged = [list(r) for r in rows]
    for j in range(1, n_cols - 1):
        if not empty[j] or empty[j - 1] or empty[j + 1]:
            continue
        if any(not is_empty(r[j - 1]) and not is_empty(r[j + 1]) for r in rows if j + 1 < len(r)):
            continue  # Konflikt: Spalte unveraendert lassen
        for r in merged:
            if j + 1 < len(r) and is_empty(r[j - 1]) and not is_empty(r[j + 1]):
                r[j - 1] = r[j + 1]
        drop |= {j, j + 1}
    keep = [j for j in range(n_cols) if j not in drop]
    return [[r[j] for j in keep if j < len(r)] for r in merged]

def to_md(rows):
    c = lambda v: "" if v is None else str(v).replace("\n", " ").strip()
    line = lambda r: "| " + " | ".join(c(x) for x in r) + " |"
    head, *body = rows
    return "\n".join([line(head), "| " + " | ".join("---" for _ in head) + " |", *map(line, body)])

def gaps(tables, page_h):
    merged = []
    for a, b in sorted((t.bbox[1], t.bbox[3]) for t in tables):
        if merged and a <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], b)
        else:
            merged.append([a, b])
    out, prev = [], 0.0
    for a, b in merged:
        if a > prev:
            out.append((prev, a))
        prev = b
    if prev < page_h:
        out.append((prev, page_h))
    return out

def convert(pdf_path, out_path, settings):
    blocks = []
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages):
            tables = [t for t in page.find_tables(table_settings=settings) if t.extract()]
            items = [(t.bbox[1], to_md(merge_isolated_empty_columns(drop_edge_empty_columns(t.extract())))) for t in tables]
            for y0, y1 in gaps(tables, page.height):
                txt = (page.crop((0, y0, page.width, y1)).extract_text() or "").strip()
                if txt:
                    items.append((y0, txt))
            items.sort(key=lambda x: x[0])
            body = "\n\n".join(c for _, c in items) or (page.extract_text() or "").strip()
            blocks.append(f"## Page {i + 1}\n\n{body}")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n\n---\n\n".join(blocks), encoding="utf-8")

def main():
    for folder in FOLDERS:
        for pdf_path in sorted((BASE_IN / folder).glob("*.pdf")):
            out_path = BASE_OUT / folder / (pdf_path.stem + ".md")
            try:
                convert(pdf_path, out_path, TABLE_SETTINGS)
                print(f"[OK] {folder}/{pdf_path.name}")
            except Exception as e:
                print(f"[ERROR] {folder}/{pdf_path.name}: {e}")

if __name__ == "__main__":
    main()
