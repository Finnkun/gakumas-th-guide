"""Fail when publishable records violate integrity and terminology rules."""
import json,re,sys
from pathlib import Path
from content_rules import CHARACTERS,lint_text
ROOT=Path(__file__).resolve().parents[1]
SOURCES=[('pidols.js','pidols','P Idol'),('supportcards.js','supportCards','Support Card'),('skillcards.js','skillCards','Skill Card'),('itemdata.js','pItems','P Item'),('itemdata.js','pDrinks','P Drink')]
def read_array(filename,variable):
    text=(ROOT/filename).read_text(encoding='utf-8');match=re.search(rf'window\.{variable}\s*=\s*(\[.*?\]);',text,re.S)
    return json.loads(match.group(1)) if match else []
issues=[]
for filename,variable,label in SOURCES:
    seen=set()
    for item in read_array(filename,variable):
        key=str(item.get('id',''))
        if not key or key in seen:issues.append(f'{label}:{key}: missing or duplicate id')
        seen.add(key)
        if not item.get('source'):issues.append(f'{label}:{key}: missing source')
        if not item.get('name'):issues.append(f'{label}:{key}: missing name')
        if label=='P Idol':
            names=[jp for jp in CHARACTERS if jp in item.get('name','')]
            if len(names)!=1:issues.append(f'{label}:{key}: expected one known character, got {names}')
details=json.loads((ROOT/'deep-details-th.json').read_text(encoding='utf-8')).get('details',{})
for url,article in details.items():
    if article.get('reviewStatus')!='reviewed':continue
    values=[]
    for section in article.get('sections',[]):
        values.append(section.get('title',''))
        for block in section.get('blocks',[]):values += [block.get('text',''),*block.get('items',[]),*[c for row in block.get('rows',[]) for c in row]]
    for value in values:
        for problem in lint_text(value):issues.append(f'{url}: {problem}: {value[:80]}')
print(json.dumps({'issues':len(issues),'sample':issues[:100]},ensure_ascii=False,indent=2));sys.exit(1 if issues else 0)
