"""Add stable identity/search/source fields without machine-translating names."""
import json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
NAMES=json.loads((ROOT/'proper-names.json').read_text(encoding='utf-8'))
ACQUISITION=json.loads((ROOT/'acquisition-labels.json').read_text(encoding='utf-8'))
SETS=[('pidols.js','pidols','https://game8.jp/gakuen-idolmaster/609099'),('supportcards.js','supportCards','https://game8.jp/gakuen-idolmaster/609102'),('skillcards.js','skillCards','https://game8.jp/gakuen-idolmaster/609737'),('itemdata.js','pItems','https://game8.jp/gakuen-idolmaster/610077'),('itemdata.js','pDrinks','https://game8.jp/gakuen-idolmaster/611910')]

files={}
for filename,variable,default_source in SETS:
    text=files.setdefault(filename,(ROOT/filename).read_text(encoding='utf-8'))
    match=re.search(rf'(window\.{variable}\s*=\s*)(\[.*?\])(\s*;)',text,re.S)
    if not match:raise RuntimeError(f'cannot parse {filename}:{variable}')
    rows=json.loads(match.group(2))
    for row in rows:
        if not row.get('source'):row['source']=default_source
        if row.get('obtain') in ACQUISITION:row['obtain']=ACQUISITION[row['obtain']]
        if variable=='pidols':
            found=[(jp,names) for jp,names in NAMES.items() if jp in row.get('name','')]
            if len(found)==1:
                jp,names=found[0];romaji,thai=names['romaji'],names['thai']
                row['characterId']=re.sub(r'[^a-z]','-',romaji.lower()).strip('-')
                row['characterName']=jp;row['characterRomaji']=romaji;row['characterThai']=thai
                row['searchAliases']=[jp,romaji,thai]
    replacement=match.group(1)+json.dumps(rows,ensure_ascii=False,separators=(',',':'))+match.group(3)
    files[filename]=text[:match.start()]+replacement+text[match.end():]
for filename,text in files.items():(ROOT/filename).write_text(text,encoding='utf-8')
print('catalog normalized')
