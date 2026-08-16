"""Regression tests for generated Home, Catalog and Detail translation output."""
import json,re,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
issues=[];checked=0
labels={'pidols':'P Idol','supports':'Support Card','skills':'Skill Card','items':'P Item','drinks':'P Drink'}
for kind,label in labels.items():
 for page in (ROOT/'database'/kind).glob('*/index.html'):
  checked+=1;text=page.read_text(encoding='utf-8')
  title=re.search(r'<title>(.*?)</title>',text,re.S)
  description=re.search(r'<meta name="description" content="(.*?)">',text,re.S)
  if not title or f'— {label} | GAKUMAS TH' not in title.group(1):issues.append(f'{page}: invalid title')
  if not description or not 80<=len(description.group(1))<=160:issues.append(f'{page}: description length')
  if 'game8.jp/gakuen-idolmaster' not in text and 'detailSource' not in text:issues.append(f'{page}: missing source support')
  if 'detail.html?type=' in text:issues.append(f'{page}: legacy internal URL')
for path in [ROOT/'home-data.js',ROOT/'catalog-app.js',ROOT/'detail-app.js']:
 text=path.read_text(encoding='utf-8')
 if '<br>' in text:issues.append(f'{path}: literal br')
print(json.dumps({'generatedDetailsChecked':checked,'issues':len(issues),'sample':issues[:30]},ensure_ascii=False,indent=2))
sys.exit(1 if issues else 0)
