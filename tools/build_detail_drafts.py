"""Publish clean Japanese source separately from reviewed Thai sections."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
source=json.loads((ROOT/'deep-details-ja.json').read_text(encoding='utf-8')).get('details',{})
manual_file=ROOT/'manual-deep-translations.json'
manual=json.loads(manual_file.read_text(encoding='utf-8')) if manual_file.exists() else {}
runtime={}
for url,article in source.items():
    reviewed=manual.get(url)
    review_status=(reviewed or {}).get('reviewStatus','reviewed') if reviewed else 'unreviewed'
    runtime[url]={'title':reviewed.get('title',article.get('title','')) if reviewed else article.get('title',''),'originalTitle':article.get('title',''),'updated':reviewed.get('updated',article.get('updated','')) if reviewed else article.get('updated',''),'sections':reviewed.get('sections',[]) if reviewed else [],'originalSections':article.get('sections',[]),'extractionStatus':article.get('extractionStatus','unknown'),'reviewStatus':review_status}
(ROOT/'deep-details.js').write_text('window.deepDetails = '+json.dumps(runtime,ensure_ascii=False,separators=(',',':'))+';\n',encoding='utf-8')
print({'articles':len(runtime),'reviewed':sum(x['reviewStatus']=='reviewed' for x in runtime.values()),'partial':sum(x['reviewStatus']=='partial' for x in runtime.values()),'withOriginalSections':sum(bool(x['originalSections']) for x in runtime.values())})
