"""Deterministic Japanese-to-Thai effect formatter with locked game terms."""
import json,re,unicodedata
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SETS=[('skillcards.js','skillCards'),('itemdata.js','pItems'),('itemdata.js','pDrinks')]

PHRASES=[
 ('山札か捨て札にあるスキルカードを選択し','เลือกการ์ดสกิล 1 ใบจากกองจั่วหรือกองทิ้ง'),
 ('山札か捨札にあるスキルカードを選択し','เลือกการ์ดสกิล 1 ใบจากกองจั่วหรือกองทิ้ง'),
 ('手札を全てレッスン中強化','อัปเกรดการ์ดทั้งหมดในมือจนจบ Lesson'),
 ('レッスン開始時手札に入る','เพิ่มการ์ดนี้เข้ามือเมื่อเริ่ม Lesson'),
 ('ランダムなスキルカードを強化','อัปเกรดการ์ดสกิลแบบสุ่ม'),
 ('次に使用するアクティブスキルカードの効果をもう1回発動','เอฟเฟกต์ของการ์ดสกิลประเภท Active ใบถัดไปทำงานเพิ่มอีก 1 ครั้ง'),
 ('スキルカード使用数追加','เพิ่มจำนวนครั้งที่ใช้การ์ดสกิล'),
 ('パラメータ上昇量増加','เพิ่มปริมาณค่าพารามิเตอร์'),
 ('アクティブスキルカード使用後','หลังใช้การ์ดสกิลประเภท Active'),
 ('メンタルスキルカード使用後','หลังใช้การ์ดสกิลประเภท Mental'),
 ('スキルカード使用後','หลังใช้การ์ดสกิล'),
 ('スキルカード使用時','เมื่อใช้การ์ดสกิล'),
 ('スキルカードを引く','จั่วการ์ดสกิล'),
 ('スキルカードを選択して強化','เลือกการ์ดสกิล 1 ใบแล้วอัปเกรด'),
 ('スキルカードを選択','เลือกการ์ดสกิล'),
 ('スキルカードを強化','อัปเกรดการ์ดสกิล'),
 ('スキルカード','การ์ดสกิล'),
 ('次の試験開始時','เมื่อเริ่มการสอบครั้งถัดไป'),
 ('次のターン','ในเทิร์นถัดไป'),('ターン開始時','เมื่อเริ่มเทิร์น'),('ターン終了時','เมื่อจบเทิร์น'),
 ('レッスン開始時','เมื่อเริ่ม Lesson'),('レッスン終了時','เมื่อจบ Lesson'),
 ('プロデュース開始時','เมื่อเริ่ม Produce'),('プロデュース終了時','เมื่อจบ Produce'),
 ('レッスン中','ระหว่าง Lesson'),('プロデュース中','ระหว่าง Produce'),
 ('ダンスレッスン','Dance Lesson'),('ビジュアルレッスン','Visual Lesson'),('ボーカルレッスン','Vocal Lesson'),
 ('ダンスターンのみ','เฉพาะเทิร์น Dance'),('ビジュアルターンのみ','เฉพาะเทิร์น Visual'),('ボーカルターンのみ','เฉพาะเทิร์น Vocal'),
 ('保留へ移動','ย้ายไปช่องพัก'),('手札に移動','ย้ายเข้ามือ'),
 ('体力回復','ฟื้นพลังงาน '),('消費体力減少','ลดการใช้พลังงาน '),('消費体力増加','เพิ่มการใช้พลังงาน '),('体力消費','ใช้พลังงาน '),
 ('パラメータ上昇','เพิ่มค่าพารามิเตอร์ '),('パラメータ','ค่าพารามิเตอร์ '),
 ('強化後','\nหลังอัปเกรด:'),('以降','หลังจากนี้'),('使用可','ใช้ได้'),('重複不可','ไม่สามารถซ้อนทับได้'),
 ('強気に変更','เปลี่ยนเป็น 強気'),('温存に変更','เปลี่ยนเป็น 温存'),('全力に変更','เปลี่ยนเป็น 全力'),
 ('強気の場合','ขณะอยู่ใน 強気'),('温存の場合','ขณะอยู่ใน 温存'),('全力の場合','ขณะอยู่ใน 全力'),
 ('好調の場合','ขณะมี 好調'),('絶好調の場合','ขณะมี 絶好調'),
 ('枚引く',' ใบ'),('枚',' ใบ'),('ターン',' เทิร์น'),('回まで',' ครั้งสูงสุด'),('回',' ครั้ง'),
 ('以上の場合',' ขึ้นไป:'),('以下の場合',' หรือต่ำกว่า:'),('の場合',' เมื่อ:'),
 ('増加後','หลังเพิ่ม'),('減少後','หลังลด'),('分',' ส่วน'),('倍適用',' เท่า'),('に変更','เปลี่ยนเป็น'),
 ('上昇','เพิ่ม'),('増加','เพิ่ม'),('減少','ลด'),('選択し','เลือก'),('使用するごとに','ทุกครั้งที่ใช้'),
]
LOCKS=[('全力値','全力値'),('絶好調','絶好調 (ฟอร์มยอดเยี่ยม)'),('好印象','好印象 (ความประทับใจ)'),('やる気','やる気 (แรงจูงใจ)'),('強気','強気 (รุกหนัก)'),('温存','温存 (เก็บแรง)'),('全力','全力 (ทุ่มสุดกำลัง)'),('好調','好調 (ฟอร์มดี)'),('集中','集中 (สมาธิ)'),('元気','Genki (元気)'),('熱意','熱意')]
CANONICAL=json.loads((ROOT/'translation-glossary.json').read_text(encoding='utf-8'))
LOCKS=[(source,CANONICAL.get(source,target)) for source,target in LOCKS]

def localize(value):
    text=unicodedata.normalize('NFKC',value or '').replace('※','หมายเหตุ: ')
    text=re.sub(r'\(レッスン内\s*(\d+)\s*回\)',r'(จำกัด \1 ครั้งต่อ Lesson)',text)
    text=re.sub(r'\(プロデュース中\s*(\d+)\s*回\)',r'(จำกัด \1 ครั้งต่อการ Produce หนึ่งรอบ)',text)
    text=re.sub(r'(強気|温存|全力)に(\d+)段階目に変更',r'เปลี่ยนเป็น \1 ขั้น \2',text)
    for source,target in PHRASES:text=text.replace(source,target)
    locked={}
    for index,(source,target) in enumerate(LOCKS):
        marker=f'__GKM{index}__';text=text.replace(source,marker);locked[marker]=target
    text=text.replace('、',': ').replace('。','\n').replace('・',' / ')
    text=re.sub(r'(?<![+\-\d])(\d+)\s*เทิร์น',r'\1 เทิร์น',text)
    text=re.sub(r'([+\-])\s*(\d+)',r' \1\2',text)
    text=re.sub(r'[ \t]+',' ',text);text=re.sub(r' *\n *','\n',text)
    for marker,target in locked.items():text=text.replace(marker,target)
    return text.strip(' :\n')

def is_complete(value):
    remainder=value
    for _,target in LOCKS:remainder=remainder.replace(target,'')
    return not re.search(r'[\u3041-\u3096\u30a1-\u30fa\u30fc\u4e00-\u9fff]',remainder)

files={};stats={'total':0,'localized':0,'reviewed':0,'draft':0}
for filename,variable in SETS:
    text=files.setdefault(filename,(ROOT/filename).read_text(encoding='utf-8'));match=re.search(rf'(window\.{variable}\s*=\s*)(\[.*?\])(\s*;)',text,re.S);rows=json.loads(match.group(2))
    for row in rows:
        if row.get('originalEffect'):
            row['localizedEffect']=localize(row['originalEffect']);row['translationStatus']='reviewed' if is_complete(row['localizedEffect']) else 'draft';stats['localized']+=1;stats[row['translationStatus']]+=1
        stats['total']+=1
    replacement=match.group(1)+json.dumps(rows,ensure_ascii=False,separators=(',',':'))+match.group(3);files[filename]=text[:match.start()]+replacement+text[match.end():]
for filename,text in files.items():(ROOT/filename).write_text(text,encoding='utf-8')
print(stats)
