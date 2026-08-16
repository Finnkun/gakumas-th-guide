"""Build reviewed Thai detail articles from verified structured catalogue fields.

This intentionally does not translate arbitrary prose. It only publishes records whose
effect has already passed the manual translation gate, while deriving acquisition text
from explicit Japanese source patterns. Existing hand-written reviews always win.
"""
import json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEEP = json.loads((ROOT / "deep-details-ja.json").read_text(encoding="utf-8"))["details"]
OUT = ROOT / "manual-deep-translations.json"
manual = json.loads(OUT.read_text(encoding="utf-8")) if OUT.exists() else {}

SETS = [
    ("Skill Card", "skillcards.js", "skillCards", "skills"),
    ("P Item", "itemdata.js", "pItems", "items"),
    ("P Drink", "itemdata.js", "pDrinks", "drinks"),
]

def read_rows(filename, variable):
    text = (ROOT / filename).read_text(encoding="utf-8")
    match = re.search(rf"window\.{variable}\s*=\s*(\[.*?\]);", text, re.S)
    return json.loads(match.group(1))

def source_text(article):
    values = []
    for section in article.get("sections", []):
        values.append(section.get("title", ""))
        for block in section.get("blocks", []):
            if block.get("type") == "p":
                values.append(block.get("text", ""))
            elif block.get("type") == "list":
                values.extend(block.get("items", []))
            elif block.get("type") == "table":
                values.extend(cell for row in block.get("rows", []) for cell in row)
    return "\n".join(values)

def acquisition(text, row, kind):
    idol = re.search(r"プロデュースアイドル[「『]([^」』]+)[」』]", text)
    support = re.search(r"(?:サポートカード|サポカ)[「『]([^」』]+)[」』]", text)
    level = re.search(r"PLv(?:\([^)]*\))?\s*(?:を)?\s*(\d+)", text) or re.search(r"プロデュースレベルを\s*(\d+)", text)
    if idol:
        return f"ปลดล็อกเมื่อได้รับ P Idol {idol.group(1)}"
    if support and kind == "Skill Card":
        return f"มีโอกาสได้รับจากอีเวนต์ระหว่าง Produce เมื่อจัด Support Card {support.group(1)}"
    if support:
        return f"ปลดล็อกเมื่อได้รับ Support Card {support.group(1)}"
    if level:
        return f"ปลดล็อกเมื่อ Producer Level ถึง PLv {level.group(1)}"
    if "最初から" in text or str(row.get("unlock", "")) in ("---", "—"):
        return "มีให้ใช้ตั้งแต่เริ่มต้น โดยไม่ต้องปลดล็อกเพิ่มเติม"
    if kind == "Skill Card" and "解放条件" not in text:
        return "มีให้ใช้ตั้งแต่เริ่มต้น โดยไม่ต้องปลดล็อกเพิ่มเติม"
    if "HIF編" in text or "H.I.F" in text:
        return "ปลดล็อกจาก Scenario H.I.F ตามเงื่อนไขที่กำหนด"
    if kind == "P Drink":
        return f"พบได้ระหว่าง Produce สาย {row.get('plan', 'ที่รองรับ')}"
    return None

generated = 0
for label, filename, variable, kind in SETS:
    for row in read_rows(filename, variable):
        url = row.get("source")
        existing = manual.get(url)
        structured = existing and [s.get("title") for s in existing.get("sections", [])] == ["ข้อมูลพื้นฐาน", "วิธีได้รับ", "เอฟเฟกต์"]
        if not url or existing and not structured or row.get("translationStatus") != "reviewed" or not row.get("localizedEffect"):
            continue
        article = DEEP.get(url, {})
        if not article.get("sections"):
            continue
        obtain = acquisition(source_text(article), row, label)
        if not obtain:
            if structured:
                manual.pop(url, None)
            continue
        facts = [["ประเภท", label], ["Plan", row.get("plan", "ไม่ระบุ")]]
        if row.get("rarity"):
            facts.append(["ความหายาก", row["rarity"]])
        if row.get("unlock") and str(row["unlock"]) not in ("---", "—"):
            facts.append(["ระดับปลดล็อก", f"PLv {row['unlock']}"])
        manual[url] = {
            "title": f"{row.get('name', '')} — {label}",
            "updated": "16 สิงหาคม 2026",
            "sections": [
                {"level": 2, "title": "ข้อมูลพื้นฐาน", "blocks": [{"type": "table", "rows": facts}]},
                {"level": 2, "title": "วิธีได้รับ", "blocks": [{"type": "p", "text": obtain}]},
                {"level": 2, "title": "เอฟเฟกต์", "blocks": [{"type": "list", "ordered": False, "items": [line.strip() for line in row["localizedEffect"].splitlines() if line.strip()]}]},
            ],
        }
        generated += 1

OUT.write_text(json.dumps(manual, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print({"generated": generated, "total_reviewed_articles": len(manual)})
