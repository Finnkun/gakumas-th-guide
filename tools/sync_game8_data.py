"""Generate the local Game8-derived card catalogues. Run from the project root."""
import html
import json
import re
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; GakumasTHDataSync/1.0)"}

def fetch(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers=HEADERS), timeout=45).read().decode("utf-8", "ignore")

def clean(fragment):
    value = re.sub(r"<br\s*/?>", " ", fragment, flags=re.I)
    value = re.sub(r"<[^>]+>", " ", value)
    return re.sub(r"\s+", " ", html.unescape(value)).strip()

def cells(row):
    result = []
    for fragment in re.findall(r"<t[hd][^>]*>(.*?)</t[hd]>", row, re.S | re.I):
        result.append((clean(fragment), " ".join(re.findall(r'alt=["\']([^"\']+)', fragment, re.I))))
    return result

def tables(document):
    return re.findall(r"<table[^>]*>.*?</table>", document, re.S | re.I)

def row_meta(row):
    links = [x for x in re.findall(r'href=["\']([^"\']+)', row, re.I) if "game8.jp/gakuen-idolmaster/" in x]
    images = [x for x in re.findall(r'(?:data-src|src)=["\']([^"\']+)', row, re.I) if not x.startswith("data:")]
    def absolute(url):
        return "https:" + url if url.startswith("//") else url
    return (absolute(links[0]) if links else "", absolute(images[0]) if images else "")

def translate_acquire(value):
    mapping = {"恒常":"ถาวร","配布":"แจกฟรี","フェス限定":"Festival Limited","ライブツアー限定":"Live Tour Limited","ユニット限定":"Unit Limited","シーズン限定":"Season Limited","グラビア限定":"Gravure Limited","コンテスト":"Contest","コインガシャ":"Coin Gacha","その他限定":"Limited อื่น ๆ"}
    return mapping.get(value, value)

def translate_effect(value):
    replacements = [("レッスン開始時","เมื่อเริ่ม Lesson"),("レッスン終了時","เมื่อจบ Lesson"),("ターン開始時","เมื่อเริ่มเทิร์น"),("ターン終了時","เมื่อจบเทิร์น"),("試験開始時","เมื่อเริ่มการสอบ"),("プロデュース開始時","เมื่อเริ่ม Produce"),("プロデュース終了時","เมื่อจบ Produce"),("特別指導開始時","เมื่อเริ่มการฝึกพิเศษ"),("相談選択時","เมื่อเลือกปรึกษา"),("お出かけ終了時","เมื่อจบการออกไปข้างนอก"),("授業・営業終了時","เมื่อจบชั้นเรียน/งาน"),("獲得時","เมื่อได้รับ"),("強化時","เมื่ออัปเกรด"),("使用後","หลังใช้"),("使用時","เมื่อใช้"),("強化後","เมื่ออัปเกรด"),("レッスン内","ต่อ Lesson"),("プロデュース中","ระหว่าง Produce"),("アクティブスキルカード","การ์ดสกิล Active"),("メンタルスキルカード","การ์ดสกิล Mental"),("トラブルカード","การ์ด Trouble"),("スキルカード","การ์ดสกิล"),("パラメータ上昇量","ปริมาณเพิ่มค่าพารามิเตอร์"),("パラメータ値","ค่าพารามิเตอร์"),("パラメータ","ค่าพารามิเตอร์"),("体力回復","ฟื้นพลังงาน"),("最大体力","พลังงานสูงสุด"),("体力消費","ใช้พลังงาน"),("消費体力","พลังงานที่ใช้"),("ボーカル","Vocal"),("ダンス","Dance"),("ビジュアル","Visual"),("レッスン","Lesson"),("ターン","เทิร์น"),("元気","Genki"),("やる気","Motivation"),("好印象","Good Impression"),("絶好調","Excellent Condition"),("集中","Focus"),("好調","Good Condition"),("全力値","ค่า Full Power"),("全力","Full Power"),("温存","Conserve"),("強気","Strong"),("手札","การ์ดในมือ"),("山札","กองจั่ว"),("捨札","กองทิ้ง"),("保留","ช่องพัก"),("使用数追加","เพิ่มจำนวนครั้งใช้"),("使用回数","จำนวนครั้งใช้"),("使用数","จำนวนครั้งใช้"),("次の","ถัดไป"),("増加量","ปริมาณที่เพิ่ม"),("増加","เพิ่ม"),("上昇","เพิ่ม"),("減少","ลด"),("削減","ลด"),("変更","เปลี่ยนเป็น"),("選択して","เลือกแล้ว"),("ランダムな","แบบสุ่ม"),("引く","จั่ว"),("生成","สร้าง"),("移動","ย้าย"),("強化","อัปเกรด"),("削除","ลบ"),("除外","นำออกจากเกม"),("無効","ไร้ผล"),("重複不可","ซ้อนทับไม่ได้"),("以降","หลังจากนี้"),("以上の場合","ขึ้นไป"),("以下の場合","หรือต่ำกว่า"),("の場合","เมื่อ"),("のみ","เท่านั้น"),("ごとに","ทุก ๆ"),("回まで","ครั้งสูงสุด"),("枚以上","ใบขึ้นไป"),("回以上","ครั้งขึ้นไป")]
    for jp, th in replacements:
        value = value.replace(jp, th)
    return value

support_url = "https://game8.jp/gakuen-idolmaster/609102"
support_table = tables(fetch(support_url))[2]
supports = []
type_map = {"ボーカル":"Vocal","ダンス":"Dance","ビジュアル":"Visual","サポート":"Support"}
plan_map = {"センス":"Sense","ロジック":"Logic","アノマリー":"Anomaly","フリー":"Free"}
for row in re.findall(r"<tr[^>]*>.*?</tr>", support_table, re.S | re.I)[1:]:
    c = cells(row)
    if len(c) != 6: continue
    tier_match = re.search(r"評価([A-Z]+)", c[1][1])
    source, image = row_meta(row)
    supports.append({"name":c[0][0],"tier":tier_match.group(1) if tier_match else "—","type":type_map.get(c[2][0],"Support"),"plan":plan_map.get(c[3][0],"Free"),"rarity":c[4][0] or re.sub("の画像$","",c[4][1]),"obtain":translate_acquire(c[5][0]),"source":source,"image":image})

skill_url = "https://game8.jp/gakuen-idolmaster/609737"
skill_tables = tables(fetch(skill_url))[:4]
skills = []
for table in skill_tables:
    for row in re.findall(r"<tr[^>]*>.*?</tr>", table, re.S | re.I)[1:]:
        c = cells(row)
        if len(c) != 4: continue
        plan_alt = re.sub("の画像$", "", c[2][1])
        rarity_alt = re.sub("の画像$", "", c[3][1])
        effect = translate_effect(c[1][0]) or "ต้นฉบับแสดงเอฟเฟกต์เป็นภาพ — โปรดเปิดลิงก์ Game8 เพื่อตรวจรายละเอียด"
        source, image = row_meta(row)
        skills.append({"name":c[0][0],"effect":effect,"plan":plan_map.get(c[2][0] or plan_alt, c[2][0] or plan_alt),"rarity":c[3][0] or rarity_alt or "N","source":source,"image":image})

def write_js(name, variable, data, source):
    banner = f"// Generated by tools/sync_game8_data.py\n// Original guide/content: Game8 — {source}\n"
    (ROOT / name).write_text(banner + f"window.{variable} = " + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + ";\n", encoding="utf-8")

def assign_ids(data, prefix):
    used = set()
    for index, entry in enumerate(data):
        candidate = entry.get("source", "").rstrip("/").rsplit("/", 1)[-1] or f"{prefix}-{index + 1}"
        identifier = candidate
        suffix = 2
        while identifier in used:
            identifier = f"{candidate}-{suffix}"
            suffix += 1
        entry["id"] = identifier
        used.add(identifier)

assign_ids(supports, "support")
assign_ids(skills, "skill")
write_js("supportcards.js", "supportCards", supports, support_url)
write_js("skillcards.js", "skillCards", skills, skill_url)

item_url = "https://game8.jp/gakuen-idolmaster/610077"
items = []
for plan, table in zip(("Anomaly","Logic","Sense","Free"), tables(fetch(item_url))[:4]):
    for row in re.findall(r"<tr[^>]*>.*?</tr>", table, re.S | re.I):
        c = cells(row)
        if len(c) < 2: continue
        source, image = row_meta(row)
        items.append({"name":c[0][0],"effect":translate_effect(c[1][0]),"plan":plan,"source":source,"image":image})

drink_url = "https://game8.jp/gakuen-idolmaster/611910"
drinks = []
for plan, table in zip(("Anomaly","Logic","Sense","Free"), tables(fetch(drink_url))[:4]):
    for row in re.findall(r"<tr[^>]*>.*?</tr>", table, re.S | re.I)[1:]:
        c = cells(row)
        if len(c) < 2: continue
        detail = translate_effect(c[1][0])
        level = re.search(r"PLv[：:]\s*([^ ]+)", detail)
        effect = re.sub(r"PLv[：:]\s*[^ ]+", "", detail).strip(" *")
        source, image = row_meta(row)
        drinks.append({"name":c[0][0],"effect":effect,"plan":plan,"unlock":level.group(1) if level else "—","source":source,"image":image})

pidol_url = "https://game8.jp/gakuen-idolmaster/609097"
pidol_table = tables(fetch(pidol_url))[1]
pidols = []
for row in re.findall(r"<tr[^>]*>.*?</tr>", pidol_table, re.S | re.I)[1:]:
    c = cells(row)
    if len(c) != 6: continue
    tier_match = re.search(r"評価([A-Z]+)", c[1][1])
    rarity_alt = re.sub("の画像$", "", c[4][1])
    first_alt = re.findall(r'alt=["\']([^"\']+)', re.findall(r"<t[hd][^>]*>(.*?)</t[hd]>", row, re.S | re.I)[0], re.I)
    full_name = re.sub("画像$", "", first_alt[0]) if first_alt else c[0][0]
    plan_cell_alts = re.findall(r'alt=["\']([^"\']+)', re.findall(r"<t[hd][^>]*>(.*?)</t[hd]>", row, re.S | re.I)[2], re.I)
    style = re.sub("の画像$", "", plan_cell_alts[-1]) if plan_cell_alts else "—"
    style_plan = {"センス":"Sense","ロジック":"Logic","アノマリー":"Anomaly","集中":"Sense","好調":"Sense","絶好調":"Sense","好印象":"Logic","やる気":"Logic","強気":"Anomaly","全力":"Anomaly","温存":"Anomaly"}
    source, image = row_meta(row)
    pidols.append({"name":full_name,"short":c[0][0],"idol":"","tier":tier_match.group(1) if tier_match else "ยังไม่ประเมิน","plan":style_plan.get(style,"Free"),"style":style,"rarity":c[4][0] or rarity_alt,"obtain":translate_acquire(c[5][0]),"note":translate_effect(style),"source":source,"image":image})

assign_ids(items, "item")
assign_ids(drinks, "drink")
write_js("itemdata.js", "pItems", items, item_url)
with (ROOT / "itemdata.js").open("a", encoding="utf-8") as output:
    output.write("window.pDrinks = " + json.dumps(drinks, ensure_ascii=False, separators=(",", ":")) + ";\n")
assign_ids(pidols, "pidol")
write_js("pidols.js", "pidols", pidols, pidol_url)
print(json.dumps({"p_idols":len(pidols),"support_cards":len(supports),"skill_cards":len(skills),"p_items":len(items),"p_drinks":len(drinks)}, ensure_ascii=False))
