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

PARTIAL_SETS = [
    ("P Idol", "pidols.js", "pidols", "pidols"),
    ("Support Card", "supportcards.js", "supportCards", "supports"),
]

ACQUISITION = {
    "ถาวร": "ถาวร",
    "แจกฟรี": "แจกจากอีเวนต์",
    "Gravure Limited": "กราเวียร์ลิมิเต็ด",
    "Festival Limited": "เฟสติวัลลิมิเต็ด",
    "Season Limited": "ซีซันลิมิเต็ด",
    "Live Tour Limited": "ไลฟ์ทัวร์ลิมิเต็ด",
    "Unit Limited": "ยูนิตลิมิเต็ด",
    "Coin Gacha": "Coin Gacha",
    "Contest": "Contest",
    "Limited อื่น ๆ": "ลิมิเต็ดประเภทอื่น",
}

def acquisition_label(value):
    return ACQUISITION.get(str(value or "").strip(), str(value or "ไม่ระบุ").strip())

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

partial = 0
for label, filename, variable, kind in PARTIAL_SETS:
    for row in read_rows(filename, variable):
        url = row.get("source")
        existing = manual.get(url)
        # Never replace hand-written or fully reviewed content.
        if not url or existing and existing.get("reviewStatus") != "partial":
            continue
        article = DEEP.get(url, {})
        if not article.get("sections"):
            continue
        facts = [["ประเภท", label]]
        if label == "P Idol":
            facts.extend([
                ["ตัวละคร", f"{row.get('characterName', '')} ({row.get('characterThai', '')})".strip()],
                ["Plan", row.get("plan", "ไม่ระบุ")],
                ["ความหายาก", row.get("rarity", "ไม่ระบุ")],
                ["Tier", row.get("tier", "ยังไม่ประเมิน")],
                ["กลไกหลัก", row.get("style", row.get("plan", "ไม่ระบุ"))],
                ["วิธีได้รับ", acquisition_label(row.get("obtain"))],
            ])
        else:
            facts.extend([
                ["ประเภทค่าสถานะ", row.get("type", "ไม่ระบุ")],
                ["Plan", "ไม่จำกัด Plan" if row.get("plan") == "Free" else row.get("plan", "ไม่ระบุ")],
                ["ความหายาก", row.get("rarity", "ไม่ระบุ")],
                ["Tier", row.get("tier", "ยังไม่ประเมิน")],
                ["วิธีได้รับ", acquisition_label(row.get("obtain"))],
            ])
        manual[url] = {
            "title": f"{row.get('name', '')} — {label}",
            "updated": "16 สิงหาคม 2026",
            "reviewStatus": "partial",
            "sections": [
                {"level": 2, "title": "ข้อมูลพื้นฐาน", "blocks": [{"type": "table", "rows": facts}]},
                {"level": 2, "title": "สถานะคำแปล", "blocks": [{"type": "p", "text": "ข้อมูลพื้นฐานผ่านการตรวจแล้ว ส่วนบทวิเคราะห์ฉบับเต็มยังไม่มีคำแปลภาษาไทยที่ตรวจสอบแล้ว โปรดดูต้นฉบับภาษาญี่ปุ่นด้านล่าง"}]},
            ],
        }
        partial += 1

OUT.write_text(json.dumps(manual, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

# Keep every omitted source visible to editors instead of silently guessing its text.
catalog_index = {}
for label, filename, variable, kind in SETS + PARTIAL_SETS:
    for row in read_rows(filename, variable):
        if row.get("source"):
            catalog_index[row["source"]] = (kind, row)
unresolved = []
for url, article in DEEP.items():
    if url in manual:
        continue
    kind, row = catalog_index.get(url, ("unknown", {}))
    if not article.get("sections"):
        reason = "ไม่พบ section เนื้อหาต้นฉบับที่แยกได้อย่างปลอดภัย"
    elif kind in ("skills", "items", "drinks") and not row.get("localizedEffect"):
        reason = "ไม่พบ Effect ต้นฉบับหรือ Effect ที่ผ่านการตรวจ"
    elif kind in ("skills", "items", "drinks"):
        reason = "ระบุวิธีได้รับจากต้นฉบับไม่ได้อย่างมั่นใจ"
    else:
        reason = "ข้อมูลต้นฉบับไม่ตรงกับ record ใน Catalog"
    unresolved.append({
        "id": str(row.get("id") or url.rstrip("/").split("/")[-1]),
        "type": kind,
        "sourceText": article.get("title", row.get("name", "")),
        "sourceUrl": url,
        "pageUrl": f"/database/{kind}/{row.get('id', '')}/" if kind != "unknown" else "",
        "reason": reason,
    })
(ROOT / "unresolved-translations.json").write_text(json.dumps(unresolved, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print({"generated": generated, "partial": partial, "total_articles_with_thai": len(manual), "unresolved": len(unresolved)})
