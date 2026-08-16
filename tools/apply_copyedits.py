"""Reviewed Thai copy changes that are awkward to patch in generated one-line HTML."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
changes={
 'catalog.html':[
  ('href="p0.css"></head>','href="p0.css"><link rel="stylesheet" href="content-status.css"></head>'),
 ],
 'detail.html':[
  ('href="p0.css"></head>','href="p0.css"><link rel="stylesheet" href="content-status.css"></head>'),
  ('<div class="translation-note"><b>เกี่ยวกับคำแปล</b><p>คำศัพท์กลไกบางคำคงชื่ออังกฤษหรือญี่ปุ่นไว้เพื่อให้ค้นหาและเทียบกับหน้าจอในเกมได้ง่าย เนื้อหาที่ต้นฉบับไม่มีข้อมูลจะไม่แต่งเติมขึ้นเอง</p></div>','<div class="translation-note"><b>สถานะเนื้อหา</b><p>ส่วนที่ระบุว่าเป็นต้นฉบับญี่ปุ่นยังไม่ใช่คำแปลภาษาไทย เนื้อหาจะเปลี่ยนเป็นฉบับไทยเมื่อผ่านการตรวจข้อมูลและศัพท์เกมแล้วเท่านั้น</p></div>'),
 ],
 'rights.html':[
  ('หนังสือที่ได้รับยืนยันว่า Game8 มีอำนาจอนุญาต','หนังสืออนุญาตที่โครงการได้รับระบุว่า Game8 มีอำนาจอนุญาต'),
  ('accessibility','การช่วยการเข้าถึง'),
  ('เปิด issue ที่ GitHub Issues','เปิดรายงานปัญหาใน GitHub Issues'),
 ],
 'detail-app.js':[
  ('escapeHtml(item.effect||item.note||"ตรวจรายละเอียดเพิ่มเติมจากหน้าต้นฉบับ")','escapeHtml(item.reviewStatus==="reviewed"?(item.effect||item.note):"ยังไม่มีคำแปลภาษาไทยที่ผ่านการตรวจ — โปรดดูต้นฉบับ Game8")'),
  ('<p>${escapeHtml(item.reviewStatus==="reviewed"?(item.effect||item.note):"ยังไม่มีคำแปลภาษาไทยที่ผ่านการตรวจ — โปรดดูต้นฉบับ Game8")}</p>','<p${item.reviewStatus!=="reviewed"&&item.originalEffect?\' lang="ja"\':""}>${escapeHtml(item.reviewStatus==="reviewed"?(item.effect||item.note):(item.originalEffect||"ยังไม่มีคำแปลภาษาไทยที่ผ่านการตรวจ — โปรดดูต้นฉบับ Game8"))}</p>'),
  ('$("#detailTitle").textContent=item.short||item.name;','$("#detailTitle").textContent=item.short||item.name;$("#detailTitle").lang="ja";'),
 ],
 'catalog-app.js':[
  ('<p>${escapeHtml(cardText(x))}</p>','<p${x.reviewStatus!=="reviewed"&&x.originalEffect?\' lang="ja"\':""}>${escapeHtml(cardText(x))}</p>'),
  ('</p><b>ดูรายละเอียด ${escapeHtml(x.short||x.name)}','</p>${x.reviewStatus!=="reviewed"&&x.originalEffect?\'<small class="source-only-badge">ต้นฉบับญี่ปุ่น · รอตรวจคำแปล</small>\':""}<b>ดูรายละเอียด ${escapeHtml(x.short||x.name)}'),
 ],
}
for filename,pairs in changes.items():
    path=ROOT/filename;text=path.read_text(encoding='utf-8')
    for old,new in pairs:text=text.replace(old,new)
    path.write_text(text,encoding='utf-8')
print('copyedits applied')
