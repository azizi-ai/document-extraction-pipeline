import sys, json
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

import numpy as np

sys.path.append(str(PROJECT_ROOT / "05 Evaluation/00 PY"))
from evaluator import (are, to_float, is_empty, ALL_FIELDS, FIELD_TYPES,
                       load_ground_truth, GROUND_TRUTH_PATH, EXTRACTION_ROOT)

# pdfplumber-plain-Extraktionsordner suchen
hits = list(EXTRACTION_ROOT.glob("*pdfplumber plain"))
if not hits:
    raise FileNotFoundError(f"Kein '*pdfplumber plain' unter {EXTRACTION_ROOT}")
EXTRACT_DIR = hits[0]
print(f"Extraktionen aus: {EXTRACT_DIR}\n")

gt = load_ground_truth(GROUND_TRUTH_PATH)
ext = {p.stem: json.loads(p.read_text(encoding="utf-8"))
       for p in sorted(EXTRACT_DIR.rglob("*.json"))}

numeric_fields = [f for f in ALL_FIELDS if FIELD_TYPES[f] == "numeric"]

present = raised = valid = zero = both_zero = 0
valid_ares = []
raised_examples = []

for doc_id, gt_epd in gt.items():
    pred = ext.get(doc_id)
    if pred is None:
        continue
    for f in numeric_fields:
        g, p = gt_epd.get(f), pred.get(f)
        if is_empty(g) or is_empty(p):
            continue  # nicht 'present'
        present += 1
        try:
            a = are(g, p)
        except (ValueError, TypeError) as e:
            raised += 1
            if len(raised_examples) < 8:
                raised_examples.append(f"{doc_id}/{f}: g={g!r} p={p!r} ({e})")
            continue
        valid += 1
        valid_ares.append(a)
        if a == 0.0:
            zero += 1
            try:
                if to_float(g) == 0.0 and to_float(p) == 0.0:
                    both_zero += 1
            except (ValueError, TypeError):
                pass

print(f"present-numerische Vergleiche : {present}")
print(f"  davon ValueError (Einheit)  : {raised}  ({raised/present*100:.1f}%)")
print(f"  davon gueltige ARE (valid)  : {valid}")
print(f"    davon ARE == 0            : {zero}  ({zero/valid*100:.1f}% der gueltigen)")
print(f"      davon beide == 0        : {both_zero}")
print(f"      davon 0 trotz Nicht-0   : {zero - both_zero}")
if valid_ares:
    a = np.array(valid_ares)
    print(f"\nMedian(ARE) ueber valid       : {np.median(a):.6f}")
    print(f"Mean(ARE)   ueber valid       : {np.mean(a):.6f}")
    print(f"Anteil ARE>0                  : {(a>0).mean()*100:.1f}%")

print("\nBeispiele ValueError:")
for ex in raised_examples:
    print(f"  {ex}")
