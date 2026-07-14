import sys
from pathlib import Path

def find_project_root(marker: str = ".git") -> Path:
    p = Path(__file__).resolve()
    for parent in p.parents:
        if (parent / marker).exists():
            return parent
    raise RuntimeError(f"Projekt-Root nicht gefunden (kein '{marker}' oberhalb von {p})")

PROJECT_ROOT = find_project_root()

from collections import defaultdict
import numpy as np
from openpyxl import Workbook

THESIS_ROOT = Path(PROJECT_ROOT)
sys.path.append(str(THESIS_ROOT / "05 Evaluation" / "01 Training" / "00 PY"))
sys.path.append(str(THESIS_ROOT / "05 Evaluation" / "02 Test" / "00 PY"))

import evaluator_training as ET
import evaluator_test as ES

PUBLISHER_PREFIXES = {"ibu": "IBU", "ift": "IFT", "iab": "IAB"}

def get_publisher(doc_id: str) -> str:
    prefix = doc_id.split("_")[0].lower()
    return PUBLISHER_PREFIXES.get(prefix, "UNKNOWN")

def aggregate_by_publisher(results) -> dict:
    buckets = defaultdict(lambda: {"are": [], "nld": [], "bool": [],
                                    "present": 0, "omission": 0,
                                    "hallucination": 0, "absent": 0})
    for r in results:
        b = buckets[get_publisher(r.document_id)]
        if r.status == "present":
            b["present"] += 1
            if r.are is not None: b["are"].append(r.are)
            if r.nld is not None: b["nld"].append(r.nld)
            if r.bool_match is not None: b["bool"].append(r.bool_match)
        elif r.status == "omission":
            b["omission"] += 1
            if r.bool_match is not None: b["bool"].append(r.bool_match)
        elif r.status == "hallucination":
            b["hallucination"] += 1
            if r.bool_match is not None: b["bool"].append(r.bool_match)
        else:
            b["absent"] += 1

    out = {}
    for pub, b in buckets.items():
        n = b["present"] + b["omission"] + b["hallucination"] + b["absent"]
        out[pub] = {
            "mean_are": float(np.mean(b["are"])) if b["are"] else None,
            "mean_nld": float(np.mean(b["nld"])) if b["nld"] else None,
            "bool_accuracy": float(np.mean(b["bool"])) if b["bool"] else None,
            "n_present": b["present"], "n_omission": b["omission"],
            "n_hallucination": b["hallucination"], "n_absent": b["absent"],
            "hallucination_rate": b["hallucination"] / n if n else None,
            "omission_rate": b["omission"] / n if n else None,
        }
    return out

def _r(v, d=6): return round(v, d) if v is not None else ""

def run_split(module, split_label: str, ws) -> None:
    gt = module.load_ground_truth(module.GROUND_TRUTH_PATH)
    ws.append([f"— {split_label} —"])
    ws.append(["variant", "publisher", "mean_are", "mean_nld", "bool_accuracy",
                "hallucination_rate", "omission_rate",
                "n_present", "n_omission", "n_hallucination", "n_absent"])
    for variant in module.VARIANTS:
        try:
            results = module.evaluate_variant(variant, gt)
        except FileNotFoundError as e:
            print(f"  [FEHLER] {split_label}/{variant}: {e}")
            continue
        by_pub = aggregate_by_publisher(results)
        for pub in ["IBU", "IFT", "IAB"]:
            d = by_pub.get(pub, {})
            ws.append([
                variant, pub,
                _r(d.get("mean_are")), _r(d.get("mean_nld")), _r(d.get("bool_accuracy")),
                _r(d.get("hallucination_rate")), _r(d.get("omission_rate")),
                d.get("n_present", 0), d.get("n_omission", 0),
                d.get("n_hallucination", 0), d.get("n_absent", 0),
            ])
    ws.append([])

def main() -> None:
    wb = Workbook()
    ws = wb.active
    ws.title = "Herausgeber-Aufschluesselung"
    run_split(ET, "Training", ws)
    run_split(ES, "Test", ws)
    out_path = ET.ROOT / "05 Evaluation" / "publisher_breakdown.xlsx"
    wb.save(out_path)
    print(f"-> {out_path}")

if __name__ == "__main__":
    main()