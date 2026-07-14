import sys, io, contextlib
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

sys.path.append(str(PROJECT_ROOT / "05 Evaluation/00 PY"))
sys.path.append(str(PROJECT_ROOT / "01 Schema"))

from evaluator import (load_ground_truth, GROUND_TRUTH_PATH,
                       evaluate_variant, summarize, ALL_FIELDS)

VARIANTS = ["01 pdfplumber plain", "03 pymupdf4llm plain"]

gt = load_ground_truth(GROUND_TRUTH_PATH)

report_lines = [f"Ground Truth: {len(gt)} EPDs\n"]

for variant in VARIANTS:
    lines = [f"=== {variant} ==="]
    try:
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            results = evaluate_variant(variant, gt)
    except FileNotFoundError as e:
        lines.append(f"  [FEHLER] {e}\n")
        report_lines.extend(lines)
        continue
    sums, vm = summarize(results)

    present = sum(s.n_present for s in sums)
    omission = sum(s.n_omission for s in sums)
    halluc = sum(s.n_hallucination for s in sums)
    absent = sum(s.n_absent for s in sums)
    total = present + omission + halluc + absent

    lines.append(f"  present       : {present:4d}  ({present/total*100:5.1f}%)")
    lines.append(f"  omission      : {omission:4d}  ({omission/total*100:5.1f}%)")
    lines.append(f"  hallucination : {halluc:4d}  ({halluc/total*100:5.1f}%)")
    lines.append(f"  absent        : {absent:4d}  ({absent/total*100:5.1f}%)")
    lines.append(f"  total         : {total:4d}")
    lines.append(f"  mean_are      : {vm.mean_are}")
    lines.append(f"  median_are    : {vm.median_are}")
    lines.append("")
    report_lines.extend(lines)

print("\n\n" + "="*60)
print("ZUSAMMENFASSUNG (beide Varianten)")
print("="*60)
for line in report_lines:
    print(line)
