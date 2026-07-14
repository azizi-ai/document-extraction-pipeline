import os
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

import anthropic

# ANPASSEN: Pfade zu den 12 Trainings-PDFs bzw. den zugehoerigen Markdown-Dateien
PDF_DIR = Path(PROJECT_ROOT / "02 Markdown/01 Training/01 PDF")
MD_DIR  = Path(PROJECT_ROOT / "02 Markdown/01 Training/02 MD/01 pdfplumber plain")
FOLDERS = ["01 IBU", "02 IFT", "03 IAB"]

client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
MODEL = "claude-haiku-4-5"

def count_tokens(text: str) -> int:
    resp = client.messages.count_tokens(
        model=MODEL,
        messages=[{"role": "user", "content": text}],
    )
    return resp.input_tokens

def extract_raw_text(pdf_path: Path) -> str:
    import pdfplumber
    with pdfplumber.open(pdf_path) as pdf:
        return "\n".join(page.extract_text() or "" for page in pdf.pages)

def main():
    results = []
    for folder in FOLDERS:
        pdf_folder = PDF_DIR / folder
        md_folder = MD_DIR / folder
        if not pdf_folder.exists():
            print(f"[WARNUNG] Ordner nicht gefunden: {pdf_folder}")
            continue
        for pdf_file in sorted(pdf_folder.glob("*.pdf")):
            md_file = md_folder / pdf_file.with_suffix(".md").name
            if not md_file.exists():
                print(f"[WARNUNG] Keine Markdown-Datei fuer {pdf_file.name}")
                continue

            raw_text = extract_raw_text(pdf_file)
            md_text = md_file.read_text(encoding="utf-8")

            raw_tokens = count_tokens(raw_text)
            md_tokens = count_tokens(md_text)
            reduction = 1 - (md_tokens / raw_tokens) if raw_tokens else 0

            results.append((pdf_file.name, raw_tokens, md_tokens, reduction))
            print(f"{pdf_file.name}: Rohtext={raw_tokens} Tok, Markdown={md_tokens} Tok, "
                  f"Reduktion={reduction:.1%}")

    if results:
        avg_raw = sum(r[1] for r in results) / len(results)
        avg_md = sum(r[2] for r in results) / len(results)
        avg_reduction = 1 - (avg_md / avg_raw) if avg_raw else 0
        print(f"\n--- Mittelwerte ueber {len(results)} Dokumente ---")
        print(f"Rohtext:  {avg_raw:.0f} Token")
        print(f"Markdown: {avg_md:.0f} Token")
        print(f"Mittlere Reduktion: {avg_reduction:.1%}")

if __name__ == "__main__":
    main()
