# GAKUMAS TH

เว็บคู่มือ Gakuen Idolmaster ภาษาไทยแบบ static web app

## สถานะเนื้อหา

ฉบับแกนหลักเสร็จแล้ว ครอบคลุมผู้เล่นใหม่, รีโรล, Produce 初, Pro, N.I.A,
H.I.F, Sense, Logic, Anomaly, A+/True End, Memory, 親愛度, Contest, กาชา,
Tier, ตัวละคร, Support Card, Skill Card, P Item และ P Drink

เนื้อหาเป็นบทสรุปภาษาไทยที่เรียบเรียงใหม่ พร้อมวันที่และลิงก์อ้างอิง ไม่ใช่สำเนา
หรือคำแปลตรงของฐานข้อมูล Game8 ทั้งเว็บไซต์

ได้รับอนุญาตให้แปล ดัดแปลง เผยแพร่ และใช้เชิงพาณิชย์กับเนื้อหาที่ครอบคลุมจาก
Game8 ตามหนังสืออนุญาตฉบับล่าสุดซึ่งผู้ดูแลโครงการจัดหาให้ รายละเอียดและลำดับ
หนังสืออนุญาตบันทึกไว้ใน `CONTENT_RIGHTS.md` โปรเจกต์นี้ไม่ใช่เว็บไซต์ทางการ
ของ Game8

หนังสืออนุญาตฉบับล่าสุดครอบคลุมภาพที่ปรากฏในหน้าคู่มือ Gakuen Idolmaster
ที่เกี่ยวข้อง รวมถึงภาพเกม ตัวละคร การ์ด โลโก้ และสื่อประชาสัมพันธ์ โดย Game8
ยืนยันว่ามีอำนาจอนุญาตสำหรับการใช้งานตามขอบเขตดังกล่าว

## เปิดใช้งาน

เปิด `index.html` โดยตรง หรือรัน local server:

```powershell
python -m http.server 5173
```

แล้วเปิด http://127.0.0.1:5173

## โครงสร้าง

- `index.html` — เนื้อหาและโครงหน้าหลัก
- `catalog.html?type=...` — หน้ารวมหมวด P Idol, Support, Skill, P Item และ P Drink
- `detail.html?type=...&id=...` — หน้ารายละเอียดที่แชร์ URL ได้สำหรับทุกรายการ
- `site-shell.css` — design system ของหน้ารวมและหน้ารายละเอียด
- `catalog-app.js` / `detail-app.js` — การค้นหา กรอง breadcrumb และ related content
- `deep-details.js` — หัวข้อ ย่อหน้า ตาราง และรายการจากหน้ารายละเอียด Game8
- `deep-details.css` — รูปแบบสารบัญและเนื้อหาฉบับเต็มในหน้ารายละเอียด
- `styles.css` — งานออกแบบและ responsive layout
- `app.js` — พจนานุกรม การค้นหา แท็บ และ interaction
- `pidols.js` — ฐานข้อมูล P Idol SSR
- `supportcards.js` — ฐานข้อมูล Support Card ครบทุกระดับ
- `skillcards.js` — ฐานข้อมูล Skill Card และคำอธิบายเอฟเฟกต์ฉบับภาษาไทย
- `itemdata.js` — ฐานข้อมูล P Item และ P Drink
- `scenarios.js` — คู่มือเปรียบเทียบ Produce Scenario ภาษาไทย
- `tools/sync_game8_data.py` — ซิงก์ตารางการ์ดจากหน้าต้นฉบับที่ได้รับอนุญาต
- `assets/game8/` — ภาพ self-host จากหน้าคู่มือที่ได้รับอนุญาต พร้อม manifest แหล่งที่มา
- `tools/sync_game8_assets.py` — ซิงก์ภาพหน้าปกและสร้าง asset manifest
- `tools/sync_catalog_assets.py` — self-host รูป catalogue ทั้งหมดและสร้าง runtime asset map
- `tools/sync_deep_details.py` — ซิงก์ข้อมูลเชิงลึกจากหน้ารายบทความทั้งหมด
- `assets/catalog/` — รูปรายการ 1,005 ไฟล์ พร้อม manifest แหล่งที่มา
- `cycle89.css` — รูปแบบภาพหน้าปก เมนูมือถือ และผลการค้นหารวม
- `site.webmanifest` / `assets/app-icon.svg` — metadata สำหรับติดตั้งเป็น web app
- `QA_REPORT.md` — ผลตรวจคุณภาพ Cycle 10 และข้อควรรู้ก่อน deploy
- `articles.js` — บทความภาษาไทยและแหล่งอ้างอิง
- `articles.css` — รูปแบบหน้าบทความ

ข้อมูลเป็นคู่มือแฟนเมดที่เรียบเรียงใหม่ ไม่ใช่เว็บไซต์อย่างเป็นทางการ

## อัปเดตข้อมูลและภาพ

รันตามลำดับจากโฟลเดอร์โปรเจกต์:

```powershell
python tools/sync_game8_data.py
python tools/sync_game8_assets.py
python tools/sync_catalog_assets.py
python tools/sync_deep_details.py
```

คำสั่งแรกสร้างข้อมูลและ ID จากหน้าต้นฉบับ คำสั่งถัดมาดาวน์โหลดภาพหน้าปกและ
ภาพ catalogue มาเก็บในเว็บ หลังซิงก์ควรรัน QA ซ้ำก่อนเผยแพร่
