"""Generate unresolved report and enforce publishable translation consistency."""
import json,re,sys
from pathlib import Path
from content_rules import lint_text
ROOT=Path(__file__).resolve().parents[1]
SETS=[('pidols.js','pidols','pidols'),('supportcards.js','supportCards','supports'),('skillcards.js','skillCards','skills'),('itemdata.js','pItems','items'),('itemdata.js','pDrinks','drinks')]
def rows(path,var):
 text=(ROOT/path).read_text(encoding='utf-8');m=re.search(rf'window\.{var}\s*=\s*(\[.*?\])\s*;',text,re.S);return json.loads(m.group(1))
unresolved=[];issues=[];all_rows=[]
for path,var,kind in SETS:
 for row in rows(path,var):
  all_rows.append((kind,row))
  if not row.get('source'):issues.append(f'{kind}:{row.get("id")}: missing source URL')
  if row.get('originalEffect') and row.get('translationStatus')!='reviewed':
   unresolved.append({'type':kind,'id':row.get('id'),'name':row.get('name'),'sourceText':row.get('originalEffect'),'pageUrl':f'https://finnkun.github.io/gakumas-th-guide/database/{kind}/{row.get("id")}/','sourceUrl':row.get('source'),'reason':'เอฟเฟกต์ยังมีโครงสร้างที่ต้องตรวจความหมายจากต้นฉบับ'})
  if row.get('translationStatus')=='reviewed':
   value=row.get('localizedEffect','')
   if not value:issues.append(f'{kind}:{row.get("id")}: reviewed without localizedEffect')
   for problem in lint_text(value):issues.append(f'{kind}:{row.get("id")}: {problem}')
(ROOT/'unresolved-translations.json').write_text(json.dumps({'generated':'2026-08-16','count':len(unresolved),'items':unresolved},ensure_ascii=False,indent=2),encoding='utf-8')
# Home previews must be copied from the canonical normalized records, never translated separately.
home=(ROOT/'home-data.js').read_text(encoding='utf-8');canonical={(k,str(r.get('id'))):r for k,r in all_rows}
for variable,kind in [('homePidols','pidols'),('homeSupportCards','supports'),('homeSkillCards','skills'),('homePItems','items'),('homePDrinks','drinks')]:
 m=re.search(rf'window\.{variable}\s*=\s*(\[.*?\])\s*;',home,re.S)
 for row in json.loads(m.group(1)) if m else []:
  source=canonical.get((kind,str(row.get('id'))),{})
  expected=source.get('localizedEffect') if source.get('translationStatus')=='reviewed' else 'ยังไม่มีคำแปลภาษาไทยที่ตรวจสอบแล้ว'
  if kind in ('skills','items','drinks') and row.get('effect')!=expected:issues.append(f'{kind}:{row.get("id")}: Home preview differs from canonical effect')
print(json.dumps({'records':len(all_rows),'unresolved':len(unresolved),'issues':len(issues),'sample':issues[:50]},ensure_ascii=False,indent=2))
sys.exit(1 if issues else 0)
