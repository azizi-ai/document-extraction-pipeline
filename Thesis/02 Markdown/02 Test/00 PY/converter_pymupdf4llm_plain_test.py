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

import pymupdf4llm

BASE_IN  = Path(PROJECT_ROOT / "02 Markdown/02 Test/01 PDF")
BASE_OUT = Path(PROJECT_ROOT / "02 Markdown/02 Test/02 MD/03 pymupdf4llm plain")
FOLDERS = ["01 IBU", "02 IFT", "03 IAB"]

def main():
    for folder in FOLDERS:
        for pdf_path in sorted((BASE_IN / folder).glob("*.pdf")):
            out_path = BASE_OUT / folder / (pdf_path.stem + ".md")
            out_path.parent.mkdir(parents=True, exist_ok=True)
            try:
                md = pymupdf4llm.to_markdown(str(pdf_path))
                out_path.write_text(md, encoding="utf-8")
                print(f"[OK] {folder}/{pdf_path.name}")
            except Exception as e:
                print(f"[ERROR] {folder}/{pdf_path.name}: {e}")

if __name__ == "__main__":
    main()
