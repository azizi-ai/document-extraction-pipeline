import sys, json, re, time, hashlib, tempfile
from pathlib import Path

def find_project_root(marker: str = ".git") -> Path:
    p = Path(__file__).resolve()
    for parent in p.parents:
        if (parent / marker).exists():
            return parent
    raise RuntimeError(f"Projekt-Root nicht gefunden (kein '{marker}' oberhalb von {p})")

PROJECT_ROOT = find_project_root()

import numpy as np
import optuna
from optuna.samplers import TPESampler

sys.path.append(str(PROJECT_ROOT / "02 Markdown/01 Training/00 PY"))
sys.path.append(str(PROJECT_ROOT / "03 Extraktion/01 Training/00 PY"))
sys.path.append(str(PROJECT_ROOT / "05 Evaluation/00 PY"))

from converter_pdfplumber_plain import convert
from extractor_plain import extract_epd
from evaluator import (is_empty, ALL_FIELDS, FIELD_TYPES,
                       load_ground_truth, GROUND_TRUTH_PATH)

PDF_DIR  = Path(PROJECT_ROOT / "02 Markdown/01 Training/01 PDF")
FOLDERS  = ["01 IBU", "02 IFT", "03 IAB"]
MAX_TOL  = 5.03
N_TRIALS = 50
SEED     = 42
SLEEP    = 1.0
BEST_OUT = Path(PROJECT_ROOT / "05 Evaluation/optuna_best_pdfplumber.json")

def build_settings(snap, join, inter, edge):
    return {
        "vertical_strategy": "lines",
        "horizontal_strategy": "lines",
        "snap_tolerance": snap,
        "join_tolerance": join,
        "edge_min_length": edge,
        "min_words_vertical": 3,
        "min_words_horizontal": 1,  
        "intersection_tolerance": inter,
        "text_tolerance": 3,     
    }

def convert_to_string(pdf_path, settings):
    with tempfile.NamedTemporaryFile(suffix=".md", delete=False) as tmp:
        tmp_path = Path(tmp.name)
    try:
        convert(pdf_path, tmp_path, settings)
        return tmp_path.read_text(encoding="utf-8")
    finally:
        tmp_path.unlink(missing_ok=True)

_NUM = re.compile(r"[-+]?\d*[.,]?\d+(?:[eE][-+]?\d+)?")


def _to_float_robust(v):
    if isinstance(v, (int, float)):
        return float(v)
    m = _NUM.search(str(v).strip().replace(",", "."))
    if not m:
        raise ValueError(f"keine Zahl in {v!r}")
    return float(m.group())

def _are_robust(g, p):
    g, p = _to_float_robust(g), _to_float_robust(p)
    m = max(abs(g), abs(p))
    return 0.0 if m == 0 else abs(g - p) / m

def mean_are_objective(gt_all, extractions):
    ares = []
    for doc_id, gt_epd in gt_all.items():
        pred = extractions.get(doc_id)
        if pred is None:
            continue
        for f in ALL_FIELDS:
            if FIELD_TYPES[f] != "numeric":
                continue
            g, p = gt_epd.get(f), pred.get(f)
            if is_empty(g) or is_empty(p):
                continue  
            try:
                ares.append(_are_robust(g, p))
            except (ValueError, TypeError):
                continue
    return float(np.mean(ares)) if ares else 1.0

def main():
    gt = load_ground_truth(GROUND_TRUTH_PATH)
    train_pdfs = [p for folder in FOLDERS for p in sorted((PDF_DIR / folder).glob("*.pdf"))]
    print(f"Ground Truth: {len(gt)} EPDs | Trainings-PDFs: {len(train_pdfs)}\n")

    extract_cache = {} 

    def evaluate_settings(settings):
        extractions = {}
        for pdf_path in train_pdfs:
            doc_id = pdf_path.stem
            try:
                md = convert_to_string(pdf_path, settings)
                h = hashlib.sha256(md.encode("utf-8")).hexdigest()
                if h in extract_cache:
                    extractions[doc_id] = extract_cache[h]
                else:
                    parsed, _ = extract_epd(md)
                    extract_cache[h] = parsed
                    extractions[doc_id] = parsed
                    time.sleep(SLEEP)
            except Exception as e:
                print(f"    [WARN] {doc_id}: {e}")
                extractions[doc_id] = {}
        return mean_are_objective(gt, extractions)

    print("Baseline (Default, alle Toleranzen = 3) ...")
    baseline = evaluate_settings(build_settings(3, 3, 3, 3))
    print(f"  Baseline Mean-ARE: {baseline:.6f}\n")

    def objective(trial):
        snap  = trial.suggest_float("snap_tolerance", 0.0, MAX_TOL)
        join  = trial.suggest_float("join_tolerance", 0.0, MAX_TOL)
        inter = trial.suggest_float("intersection_tolerance", 0.0, MAX_TOL)
        edge  = trial.suggest_float("edge_min_length", 0.0, MAX_TOL)
        return evaluate_settings(build_settings(snap, join, inter, edge))

    study = optuna.create_study(direction="minimize", sampler=TPESampler(seed=SEED))
    study.optimize(objective, n_trials=N_TRIALS)

    print("\n=== Ergebnis ===")
    print(f"Baseline Mean-ARE : {baseline:.6f}")
    print(f"Best     Mean-ARE : {study.best_value:.6f}")
    print(f"Best-Parameter    : {study.best_params}")

    try:
        imp = optuna.importance.get_param_importances(study)
        print("\nParameter-Wichtigkeit (effektive Dimensionalitaet):")
        for k, v in imp.items():
            print(f"  {k:26s} {v:.3f}")
    except Exception as e:
        print(f"\n[Info] Parameter-Wichtigkeit nicht verfuegbar: {e}")

    BEST_OUT.parent.mkdir(parents=True, exist_ok=True)
    BEST_OUT.write_text(json.dumps({
        "converter": "pdfplumber",
        "max_tol": MAX_TOL, "n_trials": N_TRIALS, "seed": SEED,
        "baseline_mean_are": baseline,
        "best_mean_are": study.best_value,
        "best_params": study.best_params,
        "best_settings": build_settings(
            snap=study.best_params["snap_tolerance"],
            join=study.best_params["join_tolerance"],
            inter=study.best_params["intersection_tolerance"],
            edge=study.best_params["edge_min_length"],
        ),
    }, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nGespeichert: {BEST_OUT}")

if __name__ == "__main__":
    main()
