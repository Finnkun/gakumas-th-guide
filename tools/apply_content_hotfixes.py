"""Mechanical source fixes; kept as code so future syncs remain repeatable."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def replace(path,old,new):
    target=ROOT/path;text=target.read_text(encoding='utf-8')
    if old not in text:raise RuntimeError(f'missing expected text in {path}: {old[:80]}')
    target.write_text(text.replace(old,new),encoding='utf-8')
replace('pidols.js','"name":"［初恋］紫雲清夏","short":"初恋莉波"','"name":"［初恋］紫雲清夏","short":"初恋清夏"')
replace('catalog-app.js','$("#catalogLoadMore").hidden=shown.length>=list.length;', '$("#catalogLoadMore").hidden=shown.length>=list.length;const remaining=Math.max(0,list.length-shown.length);$("#catalogLoadMore").textContent=`โหลดอีก ${Math.min(pageSize,remaining)} รายการ`;')
replace('catalog-app.js','${escapeHtml(cardText(x)).slice(0,145)}','${escapeHtml(cardText(x))}')
replace('detail-app.js','${article.originalSections?.length?`<button class="language-toggle"','${reviewed&&article.originalSections?.length?`<button class="language-toggle"')
with (ROOT/'deep-details.css').open('a',encoding='utf-8') as stream:
    stream.write('\n.translation-status{padding:16px 20px;background:#fff3c7;border:1px solid #d9a800}.translation-status p{margin:5px 0 0;line-height:1.7}\n')
print('content hotfixes applied')
