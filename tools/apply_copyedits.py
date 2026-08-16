"""Reviewed Thai copy changes that are awkward to patch in generated one-line HTML."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
changes={
 'rights.html':[
  ('หนังสือที่ได้รับยืนยันว่า Game8 มีอำนาจอนุญาต','หนังสืออนุญาตที่โครงการได้รับระบุว่า Game8 มีอำนาจอนุญาต'),
  ('accessibility','การช่วยการเข้าถึง'),
  ('เปิด issue ที่ GitHub Issues','เปิดรายงานปัญหาใน GitHub Issues'),
 ],
 'detail-app.js':[
  ('escapeHtml(item.effect||item.note||"ตรวจรายละเอียดเพิ่มเติมจากหน้าต้นฉบับ")','escapeHtml(item.reviewStatus==="reviewed"?(item.effect||item.note):"ยังไม่มีคำแปลภาษาไทยที่ผ่านการตรวจ — โปรดดูต้นฉบับ Game8")'),
 ],
}
for filename,pairs in changes.items():
    path=ROOT/filename;text=path.read_text(encoding='utf-8')
    for old,new in pairs:text=text.replace(old,new)
    path.write_text(text,encoding='utf-8')
print('copyedits applied')
