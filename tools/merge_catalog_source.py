"""Attach immutable Japanese source effects to runtime records by exact name."""
import json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];SOURCE=json.loads((ROOT/'catalog-source-ja.json').read_text(encoding='utf-8'))['categories']
SETS=[('skillcards.js','skillCards','skills'),('itemdata.js','pItems','items'),('itemdata.js','pDrinks','drinks')]
def key(value):return re.sub(r'[\s　]+','',value or '')
files={};report={}
for filename,variable,kind in SETS:
    text=files.setdefault(filename,(ROOT/filename).read_text(encoding='utf-8'));match=re.search(rf'(window\.{variable}\s*=\s*)(\[.*?\])(\s*;)',text,re.S);rows=json.loads(match.group(2));lookup={key(x['name']):x for x in SOURCE[kind]};miss=[]
    for row in rows:
        source=lookup.get(key(row.get('name')))
        if source:
            row['originalEffect']=source['effect'];row['translationStatus']='source-only'
            if not row.get('source'):row['source']=source['source']
            if kind=='drinks' and source.get('unlock'):row['unlock']=source['unlock']
        else:miss.append(row.get('name'))
    replacement=match.group(1)+json.dumps(rows,ensure_ascii=False,separators=(',',':'))+match.group(3);files[filename]=text[:match.start()]+replacement+text[match.end():];report[kind]={'records':len(rows),'matched':len(rows)-len(miss),'missing':miss}
for filename,text in files.items():(ROOT/filename).write_text(text,encoding='utf-8')
print(json.dumps(report,ensure_ascii=False,indent=2))
