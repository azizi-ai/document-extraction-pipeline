import json
from pathlib import Path

def find_project_root(marker: str = ".git") -> Path:
    p = Path(__file__).resolve()
    for parent in p.parents:
        if (parent / marker).exists():
            return parent
    raise RuntimeError(f"Projekt-Root nicht gefunden (kein '{marker}' oberhalb von {p})")

PROJECT_ROOT = find_project_root()

ROOT = Path(PROJECT_ROOT)
GT_PATH = ROOT / "05 Evaluation" / "05 Ground Truth" / "ground_truth.json"
EXTRACTION_ROOT = ROOT / "03 Extraktion" / "01 Training"
PLAIN_DIR = EXTRACTION_ROOT / "01 pdfplumber plain"
OPT_DIR = EXTRACTION_ROOT / "02 pdfplumber optimized"

def is_empty(v):
    return v is None or (isinstance(v, str) and not v.strip()) or (isinstance(v, (list, tuple)) and not v)

def load_gt(path):
    data = json.loads(path.read_text(encoding="utf-8"))
    epds = data["epd"] if isinstance(data, dict) and "epd" in data else data
    return {e["document_id"]: e for e in epds}

def load_extractions(folder):
    return {p.stem: json.loads(p.read_text(encoding="utf-8")) for p in sorted(folder.rglob("*.json"))}

def status(gt, pred):
    ge, pe = is_empty(gt), is_empty(pred)
    return "absent" if ge and pe else "hallucination" if ge else "omission" if pe else "present"

def main():
    gt_all = load_gt(GT_PATH)
    plain = load_extractions(PLAIN_DIR)
    opt = load_extractions(OPT_DIR)

    fields = set()
    for e in gt_all.values():
        fields.update(e.keys())
    fields.discard("document_id")

    flips = []
    for doc_id, gt_epd in gt_all.items():
        p_pred = plain.get(doc_id, {})
        o_pred = opt.get(doc_id, {})
        for f in fields:
            gt_v = gt_epd.get(f)
            p_status = status(gt_v, p_pred.get(f))
            o_status = status(gt_v, o_pred.get(f))
            if p_status != o_status:
                flips.append((doc_id, f, p_status, o_status, gt_v, p_pred.get(f), o_pred.get(f)))

    print(f"{len(flips)} Status-Aenderungen zwischen plain und optimized\n")
    for doc_id, f, ps, os_, gt_v, pv, ov in flips:
        print(f"{doc_id:12} {f:55} {ps:>13} -> {os_:<13}  GT={gt_v!r}  plain={pv!r}  opt={ov!r}")

if __name__ == "__main__":
    main()
