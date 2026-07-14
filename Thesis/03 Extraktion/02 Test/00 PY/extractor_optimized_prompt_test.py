import os, sys, json, time
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


sys.path.append(str(PROJECT_ROOT / "01 Schema"))
from epd import EPD
import anthropic

BASE_MD  = Path(PROJECT_ROOT / "02 Markdown/02 Test/02 MD")
BASE_OUT = Path(PROJECT_ROOT / "03 Extraktion/02 Test")

SOURCES = [
    (BASE_MD / "01 pdfplumber plain", BASE_OUT / "05 pdfplumber prompt optimized"),
    (BASE_MD / "03 pymupdf4llm plain", BASE_OUT / "06 pymupdf4llm prompt optimized"),
]

FOLDERS = ["01 IBU", "02 IFT", "03 IAB"]

FIELDS = "\n".join(f"- {name}" for name in EPD.model_fields)
SYSTEM = f"""Extract the fields from the markdown file and return them as JSON. Return only the JSON object. No explanation, no markdown formatting.

Pay special attention to the following instructions when filling out the fields:

1. deklariertes_produkt: Extract only the core product name. Exclude quantity/unit prefixes, manufacturer or brand names, and trailing additions like "by ...".
2. herausgeber: Extract the full name of the issuing institution, including its parenthetical abbreviation if present.
3. deklarierte_einheit: Extract only the quantity with unit. Exclude any following product description.
4. gueltigkeitsdatum: Extract the expiry/validity-end date, not the issue date.
5. Indicator fields: Match each value by both its exact row label and its exact life cycle module column header. Never match by position or similar-sounding neighboring labels. Verify the column header explicitly for each value — do not assume column order. If no exact match exists for a module, return null.
6. brennendes_abtropfen, rauchgasentwicklung, baustoffklasse: Extract only the short classification code, excluding parenthetical explanations.
7. holzzertifizierungen: Extract only wood-origin/chain-of-custody certifications as separate list items. Exclude management-system standards and strip suffixes like "®" or "Chain of Custody".
8. Numeric values: Copy each number exactly as written in the document, preserving its original notation including scientific notation. Never convert between scientific and decimal notation.

Fields to extract:
{FIELDS}"""

client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

def ask(msgs, system=None):
    raw = client.messages.create(model="claude-haiku-4-5", max_tokens=16384, temperature=0,
        system=system or anthropic.NOT_GIVEN, messages=msgs).content[0].text.strip()
    return raw.split("\n", 1)[1].rsplit("```", 1)[0].strip() if raw.startswith("```") else raw

def extract_epd(markdown: str):
    """Markdown-Text -> (geparstes Dict, attempt).
    Retry NUR bei JSON-Parsing-Fehler (keine Aufgaben-/Prompt-Modifikation).
    attempt=1 erster Versuch, attempt=2 nach Retry. Identisch zum Plain-Verhalten."""
    raw = ask([{"role": "user", "content": markdown}], SYSTEM)
    try:
        return json.loads(raw), 1
    except json.JSONDecodeError:
        raw = ask([{"role": "user", "content": markdown},
                   {"role": "assistant", "content": raw},
                   {"role": "user", "content": "Return only the JSON object. No explanation, no markdown formatting."}])
        return json.loads(raw), 2

def main():
    first = True
    for in_base, out_base in SOURCES:
        for folder in FOLDERS:
            out_dir = out_base / folder
            out_dir.mkdir(parents=True, exist_ok=True)
            for md in sorted((in_base / folder).glob("*.md")):
                if not first:
                    print("[PAUSE] Waiting 10s before next API call..."); time.sleep(10)
                first = False
                content = md.read_text(encoding="utf-8")
                try:
                    parsed, attempt = extract_epd(content)
                    out = out_dir / md.with_suffix(".json").name
                    out.write_text(json.dumps(parsed, ensure_ascii=False, indent=2), encoding="utf-8")
                    print(f"[OK attempt={attempt}] {in_base.name}/{folder}/{md.name}")
                except Exception as e:
                    print(f"[ERROR] {in_base.name}/{folder}/{md.name}: {e}")

if __name__ == "__main__":
    main()
