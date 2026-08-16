"""Publish clean Japanese source separately from reviewed Thai sections."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
source=json.loads((ROOT/'deep-details-ja.json').read_text(encoding='utf-8')).get('details',{})
runtime={}
for url,article in source.items():
    runtime[url]={'title':article.get('title',''),'originalTitle':article.get('title',''),'updated':article.get('updated',''),'sections':[],'originalSections':article.get('sections',[]),'extractionStatus':article.get('extractionStatus','unknown'),'reviewStatus':'unreviewed'}
(ROOT/'deep-details.js').write_text('window.deepDetails = '+json.dumps(runtime,ensure_ascii=False,separators=(',',':'))+';\n',encoding='utf-8')
print({'articles':len(runtime),'withOriginalSections':sum(bool(x['originalSections']) for x in runtime.values())})
