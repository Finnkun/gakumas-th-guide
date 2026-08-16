"""Fetch verbatim Japanese catalog effects; never machine-translate this file."""
import html,json,re,time,urllib.request
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];HEADERS={'User-Agent':'Mozilla/5.0 (compatible; GakumasTHSourceSync/2.0)'}
PAGES={'skills':('609737',4),'items':('610077',4),'drinks':('611910',4)}
DETAIL_OVERRIDES={'items':{'新しい、私':'654026','ひみつ特訓カーデ':'610129','ゲーセンの戦利品':'610125','夢にあふれた大荷物':'610138'}}
def fetch(url):
    for attempt in range(5):
        try:return urllib.request.urlopen(urllib.request.Request(url,headers=HEADERS),timeout=45).read().decode('utf-8','ignore')
        except Exception:
            if attempt==4:raise
            time.sleep(3*(attempt+1))
def clean(fragment):
    fragment=re.sub(r'<img\b[^>]*>',' ',fragment,flags=re.I|re.S);fragment=re.sub(r'<br\s*/?>','\n',fragment,flags=re.I);fragment=re.sub(r'<[^>]+>',' ',fragment)
    return re.sub(r'\s+',' ',html.unescape(fragment)).strip()
payload={'version':2,'language':'ja','source':'Game8','categories':{}}
for kind,(page_id,table_count) in PAGES.items():
    url=f'https://game8.jp/gakuen-idolmaster/{page_id}';document=fetch(url);tables=re.findall(r'<table[^>]*>.*?</table>',document,re.S|re.I)[:table_count];items=[]
    for table in tables:
        for row in re.findall(r'<tr[^>]*>.*?</tr>',table,re.S|re.I)[1:]:
            cells=[clean(cell) for cell in re.findall(r'<t[hd][^>]*>(.*?)</t[hd]>',row,re.S|re.I)]
            if len(cells)<2 or not cells[0] or not cells[1]:continue
            links=[x for x in re.findall(r'href=["\']([^"\']+)',row,re.I) if '/gakuen-idolmaster/' in x];source=links[0] if links else url
            if source.startswith('/'):source='https://game8.jp'+source
            effect=cells[1];unlock=''
            if kind=='drinks':
                match=re.search(r'PLv[：:]\s*([^ ]+)',effect);unlock=match.group(1) if match else '';effect=re.sub(r'PLv[：:]\s*[^ ]+','',effect).strip()
            items.append({'name':cells[0],'effect':effect,'unlock':unlock,'source':source})
    payload['categories'][kind]=items;time.sleep(1)
for kind,records in DETAIL_OVERRIDES.items():
    existing={item['name']:item for item in payload['categories'][kind]}
    for name,page_id in records.items():
        url=f'https://game8.jp/gakuen-idolmaster/{page_id}';document=fetch(url);headings=list(re.finditer(r'<h[23][^>]*>.*?</h[23]>',document,re.S|re.I));effect=''
        for index,heading in enumerate(headings):
            title=clean(heading.group(0))
            if title==f'{name}の効果':
                end=next((candidate.start() for candidate in headings[index+1:] if candidate.group(0).lower().startswith('<h2')),len(document))
                effect=clean(document[heading.end():end]);break
        if effect:existing[name]={'name':name,'effect':effect,'unlock':'','source':url}
        time.sleep(.5)
    payload['categories'][kind]=list(existing.values())
(ROOT/'catalog-source-ja.json').write_text(json.dumps(payload,ensure_ascii=False,separators=(',',':')),encoding='utf-8')
print(json.dumps({kind:len(items) for kind,items in payload['categories'].items()},ensure_ascii=False))
