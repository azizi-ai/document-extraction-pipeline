import os, sys, json, time
from pathlib import Path

def find_project_root(marker: str = ".git") -> Path:
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
    (BASE_MD / "01 pdfplumber plain", BASE_OUT / "01 pdfplumber plain"),
    (BASE_MD / "03 pymupdf4llm plain", BASE_OUT / "03 pymupdf4llm plain"),
]

FOLDERS = ["01 IBU", "02 IFT", "03 IAB"]

FIELDS = "\n".join(f"- {name}" for name in EPD.model_fields)
SYSTEM = f"Extract the fields from the markdown file and return them as JSON. Return only the JSON object. No explanation, no markdown formatting.\n\nFields to extract:\n{FIELDS}"

client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

def ask(msgs, system=None):
    raw = client.messages.create(model="claude-haiku-4-5", max_tokens=16384, temperature=0,
        system=system or anthropic.NOT_GIVEN, messages=msgs).content[0].text.strip()
    return raw.split("\n", 1)[1].rsplit("```", 1)[0].strip() if raw.startswith("```") else raw

def extract_epd(markdown: str):
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
