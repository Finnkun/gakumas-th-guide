"""Extract structured detail content from every referenced Game8 article."""
import concurrent.futures
import html
import json
import re
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HEADERS = {"User-Agent":"Mozilla/5.0 (compatible; GakumasTHDetailSync/1.0)"}
SOURCES = [("pidols.js","pidols"),("supportcards.js","supportCards"),("skillcards.js","skillCards"),("itemdata.js","pItems"),("itemdata.js","pDrinks")]

def read_array(filename, variable):
    text=(ROOT/filename).read_text(encoding="utf-8")
    match=re.search(rf"window\.{variable}\s*=\s*(\[.*?\]);",text,re.S)
    return json.loads(match.group(1)) if match else []

urls=sorted({entry.get("source") for filename,variable in SOURCES for entry in read_array(filename,variable) if entry.get("source")})

def clean(fragment):
    fragment=re.sub(r'<img[^>]+alt=["\']([^"\']*)["\'][^>]*>',r' \1 ',fragment,flags=re.I)
    fragment=re.sub(r'<br\s*/?>','\n',fragment,flags=re.I)
    fragment=re.sub(r'<[^>]+>',' ',fragment)
    value=html.unescape(fragment).replace('\xa0',' ')
    value=re.sub(r'[ \t]+',' ',value)
    value=re.sub(r'\n\s*\n+','\n',value)
    return value.strip()

PHRASES=[("サポートカードの評価","การประเมิน Support Card"),("サポートイベント","Support Event"),("評価と解放条件","การประเมินและเงื่อนไขปลดล็อก"),("評価と効果","การประเมินและเอฟเฟกต์"),("解放条件と効果","เงื่อนไขปลดล็อกและเอฟเฟกต์"),("解放条件","เงื่อนไขปลดล็อก"),("強化状態（+）の効果","เอฟเฟกต์เมื่ออัปเกรด (+)"),("強化状態","สถานะอัปเกรด"),("スキルカードの効果","เอฟเฟกต์ Skill Card"),("Pアイテムの効果","เอฟเฟกต์ P Item"),("Pドリンクの効果","เอฟเฟกต์ P Drink"),("基本情報","ข้อมูลพื้นฐาน"),("ステータス","ค่าสถานะ"),("性能","ความสามารถ"),("入手方法","วิธีได้รับ"),("おすすめ","แนะนำ"),("使い方","วิธีใช้"),("効果","เอฟเฟกต์"),("評価","การประเมิน"),("レベル","ระดับ"),("ボーカル","Vocal"),("ダンス","Dance"),("ビジュアル","Visual"),("センス","Sense"),("ロジック","Logic"),("アノマリー","Anomaly"),("スキルカード","Skill Card"),("サポートカード","Support Card"),("プロデュース","Produce"),("ターン","เทิร์น"),("体力","พลังงาน"),("元気","Genki"),("やる気","Motivation"),("好印象","Good Impression"),("集中","Focus"),("好調","Good Condition"),("全力","Full Power"),("温存","Conserve"),("強気","Strong")]
def localize(value):
    for jp,th in PHRASES:value=value.replace(jp,th)
    return value

def parse_table(fragment):
    rows=[]
    for row in re.findall(r'<tr[^>]*>.*?</tr>',fragment,re.S|re.I):
        cells=[clean(cell) for cell in re.findall(r'<t[hd][^>]*>(.*?)</t[hd]>',row,re.S|re.I)]
        if cells and any(cells):rows.append(cells)
    return rows

def parse_page(url):
    request=urllib.request.Request(url,headers=HEADERS)
    raw=urllib.request.urlopen(request,timeout=45).read().decode('utf-8','ignore')
    title_match=re.search(r'<h1[^>]*itemprop=["\']name["\'][^>]*>(.*?)</h1>',raw,re.S|re.I)
    updated=re.search(r'最終更新日[：:]\s*</?[^>]*>?\s*([0-9.年月日 :]+)',raw,re.I)
    start=re.search(r'<h2[^>]*class=["\'][^"\']*a-header--2[^"\']*["\']',raw,re.I)
    if not start:return url,{"title":clean(title_match.group(1)) if title_match else "","updated":"","sections":[]}
    body=raw[start.start():]
    end=re.search(r'<h2[^>]*>\s*(?:関連記事|学マスプレイヤーにおすすめ)',body,re.S|re.I)
    if end:body=body[:end.start()]
    tokens=re.findall(r'<h[23][^>]*>.*?</h[23]>|<table[^>]*>.*?</table>|<[uo]l[^>]*>.*?</[uo]l>|<p[^>]*>.*?</p>',body,re.S|re.I)
    sections=[];current=None
    for token in tokens:
        lower=token.lower()
        if lower.startswith('<h2') or lower.startswith('<h3'):
            heading=clean(token)
            if not heading or '関連記事' in heading:continue
            current={"level":2 if lower.startswith('<h2') else 3,"title":heading,"blocks":[]}
            sections.append(current)
        elif current is not None and lower.startswith('<table'):
            rows=parse_table(token)
            if rows:current["blocks"].append({"type":"table","rows":rows})
        elif current is not None and (lower.startswith('<ul') or lower.startswith('<ol')):
            items=[clean(x) for x in re.findall(r'<li[^>]*>(.*?)</li>',token,re.S|re.I)]
            items=[x for x in items if x]
            if items:current["blocks"].append({"type":"list","ordered":lower.startswith('<ol'),"items":items})
        elif current is not None:
            text=clean(token)
            if text and len(text)>1 and not text.startswith(('▶','広告')):current["blocks"].append({"type":"p","text":text})
    sections=[s for s in sections if s['blocks']]
    return url,{"title":clean(title_match.group(1)) if title_match else "","updated":updated.group(1).strip() if updated else "","sections":sections}

details={};failures=[]
with concurrent.futures.ThreadPoolExecutor(max_workers=16) as executor:
    futures={executor.submit(parse_page,url):url for url in urls}
    for future in concurrent.futures.as_completed(futures):
        try:
            url,data=future.result();details[url]=data
        except Exception as error:failures.append({"url":futures[future],"error":str(error)})

payload={"details":details,"failures":failures}
(ROOT/'deep-details.json').write_text(json.dumps(payload,ensure_ascii=False,separators=(',',':')),encoding='utf-8')
(ROOT/'deep-details-ja.json').write_text(json.dumps(payload,ensure_ascii=False,separators=(',',':')),encoding='utf-8')
(ROOT/'deep-details.js').write_text('window.deepDetails = '+json.dumps(details,ensure_ascii=False,separators=(',',':'))+';\n',encoding='utf-8')
print(json.dumps({"requested":len(urls),"downloaded":len(details),"failed":len(failures),"with_sections":sum(bool(x['sections']) for x in details.values()),"sections":sum(len(x['sections']) for x in details.values())},ensure_ascii=False))
