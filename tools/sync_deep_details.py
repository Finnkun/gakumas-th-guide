"""Extract only item-specific article content from referenced Game8 pages."""
import argparse, concurrent.futures, html, json, re, time, urllib.error, urllib.request
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
HEADERS={"User-Agent":"Mozilla/5.0 (compatible; GakumasTHDetailSync/2.0)"}
SOURCES=[("pidols.js","pidols"),("supportcards.js","supportCards"),("skillcards.js","skillCards"),("itemdata.js","pItems"),("itemdata.js","pDrinks")]
STOP_HEADINGS=("関連記事","コメント","おすすめゲーム","人気ゲーム","ランキング","攻略メニュー","権利表記")
JUNK_TEXT=("ガチャシミュレーター","レビューを投稿","保存ボタン")

def read_array(filename,variable):
    text=(ROOT/filename).read_text(encoding="utf-8")
    match=re.search(rf"window\.{variable}\s*=\s*(\[.*?\]);",text,re.S)
    return json.loads(match.group(1)) if match else []

records_by_url={}
for filename,variable in SOURCES:
    for entry in read_array(filename,variable):
        if entry.get("source"):
            records_by_url.setdefault(entry["source"],[]).append({"id":str(entry.get("id","")),"name":entry.get("name",""),"short":entry.get("short","")})

def clean(fragment):
    # Alt text describes UI icons and thumbnails; it is never article prose.
    fragment=re.sub(r'<(?:script|style|svg)[^>]*>.*?</(?:script|style|svg)>',' ',fragment,flags=re.I|re.S)
    fragment=re.sub(r'<img\b[^>]*>',' ',fragment,flags=re.I|re.S)
    fragment=re.sub(r'<br\s*/?>','\n',fragment,flags=re.I)
    fragment=re.sub(r'<[^>]+>',' ',fragment)
    value=html.unescape(fragment).replace('\xa0',' ')
    value=re.sub(r'[ \t]+',' ',value)
    value=re.sub(r'\n\s*\n+','\n',value)
    return value.strip()

def compact(value):
    value=re.sub(r'\([^)]*\)|（[^）]*）','',value or '').replace('はじまる','始まる')
    return re.sub(r'[\s\[\]［］「」『』【】()（）・.!！?？,，。]','',value)

def identity_matches(title,expected):
    page=compact(title)
    for record in expected:
        full,short=compact(record.get('name')),compact(record.get('short'))
        if full and full in page:return True
        if len(short)>=4 and short in page:return True
    return False

def parse_table(fragment):
    rows=[]
    for row in re.findall(r'<tr[^>]*>.*?</tr>',fragment,re.S|re.I):
        cells=[clean(cell) for cell in re.findall(r'<t[hd][^>]*>(.*?)</t[hd]>',row,re.S|re.I)]
        if cells and any(cells):rows.append(cells)
    return rows

def parse_page(url,expected):
    raw=None
    for attempt in range(5):
        try:
            time.sleep(.2)
            raw=urllib.request.urlopen(urllib.request.Request(url,headers=HEADERS),timeout=45).read().decode('utf-8','ignore');break
        except (urllib.error.HTTPError,urllib.error.URLError):
            if attempt==4:raise
            time.sleep(2**attempt)
    title_match=re.search(r'<h1[^>]*itemprop=["\']name["\'][^>]*>(.*?)</h1>',raw,re.S|re.I)
    title=clean(title_match.group(1)) if title_match else ""
    base={"title":title,"updated":"","sections":[],"reviewStatus":"unreviewed"}
    if not identity_matches(title,expected):return url,{**base,"extractionStatus":"source-mismatch"}
    start=re.search(r'<h2[^>]*class=["\'][^"\']*a-header--2[^"\']*["\']',raw,re.I)
    if not start:return url,{**base,"extractionStatus":"no-content"}
    body=raw[start.start():]
    stops=[]
    for match in re.finditer(r'<h2[^>]*>.*?</h2>',body,re.S|re.I):
        if any(heading in clean(match.group(0)) for heading in STOP_HEADINGS):stops.append(match.start())
    if stops:body=body[:min(stops)]
    tokens=re.findall(r'<h[23][^>]*>.*?</h[23]>|<table[^>]*>.*?</table>|<[uo]l[^>]*>.*?</[uo]l>|<p[^>]*>.*?</p>',body,re.S|re.I)
    sections=[];current=None
    for token in tokens:
        lower=token.lower()
        if lower.startswith(('<h2','<h3')):
            heading=clean(token)
            if not heading or any(stop in heading for stop in STOP_HEADINGS):continue
            current={"level":2 if lower.startswith('<h2') else 3,"title":heading,"blocks":[]};sections.append(current)
        elif current is not None and lower.startswith('<table'):
            rows=parse_table(token)
            if rows:current["blocks"].append({"type":"table","rows":rows})
        elif current is not None and lower.startswith(('<ul','<ol')):
            items=[clean(x) for x in re.findall(r'<li[^>]*>(.*?)</li>',token,re.S|re.I)]
            items=[x for x in items if x and not any(j in x for j in JUNK_TEXT)]
            if items:current["blocks"].append({"type":"list","ordered":lower.startswith('<ol'),"items":items})
        elif current is not None:
            text=clean(token)
            if text and len(text)>1 and not any(j in text for j in JUNK_TEXT):current["blocks"].append({"type":"p","text":text})
    base.update({"sections":[s for s in sections if s['blocks']],"extractionStatus":"extracted"})
    return url,base

previous={}
previous_file=ROOT/'deep-details-ja.json'
if previous_file.exists():
    try:previous=json.loads(previous_file.read_text(encoding='utf-8')).get('details',{})
    except (json.JSONDecodeError,OSError):pass
parser=argparse.ArgumentParser();parser.add_argument('--start',type=int,default=0);parser.add_argument('--limit',type=int,default=0);parser.add_argument('--url',action='append',default=[]);args=parser.parse_args()
targets=args.url or sorted(records_by_url)[args.start:args.start+args.limit if args.limit else None]
targets=[url for url in targets if url in records_by_url]
details=dict(previous);failures=[]
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
    futures={executor.submit(parse_page,url,records_by_url[url]):url for url in targets}
    for future in concurrent.futures.as_completed(futures):
        try:
            url,data=future.result();details[url]=data
        except Exception as error:failures.append({"url":futures[future],"error":str(error)})

payload={"details":details,"failures":failures}
for name in ('deep-details.json','deep-details-ja.json'):(ROOT/name).write_text(json.dumps(payload,ensure_ascii=False,separators=(',',':')),encoding='utf-8')
(ROOT/'deep-details.js').write_text('window.deepDetails = '+json.dumps(details,ensure_ascii=False,separators=(',',':'))+';\n',encoding='utf-8')
print(json.dumps({"requested":len(targets),"stored":len(details),"failed":len(failures),"mismatched":sum(x.get('extractionStatus')=='source-mismatch' for x in details.values()),"with_sections":sum(bool(x['sections']) for x in details.values())},ensure_ascii=False))
