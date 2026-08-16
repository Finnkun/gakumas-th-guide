"""Translate extracted Japanese detail content to Thai with a persistent cache."""
import copy
import concurrent.futures
import html as html_lib
import json
import re
import time
import urllib.parse
import urllib.request
from pathlib import Path
from translators.server import Bing

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'deep-details-ja.json'
CACHE_FILE=ROOT/'translation-cache-ja-th.json'
HEADERS={'User-Agent':'Mozilla/5.0 (compatible; GakumasTHTranslationSync/1.0)','Content-Type':'application/x-www-form-urlencoded'}
JP=re.compile(r'[ぁ-んァ-ヶ一-龯]')
BING=Bing()

def bing_translate(value):
    return BING.bing_api(value,from_language='ja',to_language='th',timeout=45)

payload=json.loads(SOURCE.read_text(encoding='utf-8'))
cache=json.loads(CACHE_FILE.read_text(encoding='utf-8')) if CACHE_FILE.exists() else {}
CATALOG_SOURCES=[('pidols','pidols.js','pidols'),('supports','supportcards.js','supportCards'),('skills','skillcards.js','skillCards'),('items','itemdata.js','pItems'),('drinks','itemdata.js','pDrinks')]
def read_array(filename,variable):
    text=(ROOT/filename).read_text(encoding='utf-8')
    match=re.search(rf'window\.{variable}\s*=\s*(\[.*?\]);',text,re.S)
    return json.loads(match.group(1)) if match else []
catalog_data={kind:read_array(filename,variable) for kind,filename,variable in CATALOG_SOURCES}
strings=[]
def collect(value):
    if isinstance(value,str) and JP.search(value) and value not in cache:strings.append(value)
    elif isinstance(value,dict):
        for child in value.values():collect(child)
    elif isinstance(value,list):
        for child in value:collect(child)
collect(payload['details'])
for entries in catalog_data.values():
    for entry in entries:
        for field in ('name','short','effect','note','style'):
            collect(entry.get(field,''))
strings=list(dict.fromkeys(strings))

def batches(values,limit=550):
    batch=[];size=2
    for value in values:
        extra=len(value)+4
        if batch and size+extra>limit:
            yield batch;batch=[];size=2
        batch.append(value);size+=extra
    if batch:yield batch

def translate_batch(values):
    query=''.join(f'<p data-i="{index}">{html_lib.escape(value)}</p>' for index,value in enumerate(values))
    translated=bing_translate(query)
    result=[html_lib.unescape(value) for value in re.findall(r'<p data-i="\d+">(.*?)</p>',translated,re.S)]
    if len(result)!=len(values):raise ValueError(f'batch size mismatch: {len(values)} -> {len(result)}')
    return result

def translate_single(value):
    return bing_translate(value)

def translate_values(values):
    try:return translate_batch(values)
    except Exception:
        if len(values)==1:return [translate_single(values[0])]
        middle=len(values)//2
        return translate_values(values[:middle])+translate_values(values[middle:])

all_batches=list(batches(strings))
for index,batch in enumerate(all_batches,1):
    for attempt in range(5):
        try:
            translated=translate_values(batch)
            cache.update(zip(batch,translated))
            CACHE_FILE.write_text(json.dumps(cache,ensure_ascii=False,separators=(',',':')),encoding='utf-8')
            print(f'{index}/{len(all_batches)} translated={len(cache)}',flush=True)
            break
        except Exception as error:
            if attempt==4:raise
            time.sleep(2**attempt)

def apply_translation(value):
    if isinstance(value,str):return cache.get(value,value)
    if isinstance(value,list):return [apply_translation(x) for x in value]
    if isinstance(value,dict):return {key:apply_translation(child) for key,child in value.items()}
    return value

translated={}
for url,article in payload['details'].items():
    thai=apply_translation(article)
    thai['originalTitle']=article.get('title','')
    thai['originalSections']=article.get('sections',[])
    translated[url]=thai

out={'details':translated,'failures':payload.get('failures',[]),'translation':{'source':'ja','target':'th','cached_strings':len(cache)}}
(ROOT/'deep-details-th.json').write_text(json.dumps(out,ensure_ascii=False,separators=(',',':')),encoding='utf-8')
(ROOT/'deep-details.js').write_text('window.deepDetails = '+json.dumps(translated,ensure_ascii=False,separators=(',',':'))+';\n',encoding='utf-8')
catalog_translations={}
for kind,entries in catalog_data.items():
    for entry in entries:
        fields={}
        for field in ('name','short','effect','note','style'):
            value=entry.get(field,'')
            if value:fields[field]=cache.get(value,value)
        catalog_translations[f'{kind}:{entry["id"]}']=fields
runtime='window.catalogTranslations = '+json.dumps(catalog_translations,ensure_ascii=False,separators=(',',':'))+';\n'
runtime+='[["pidols",window.pidols],["supports",window.supportCards],["skills",window.skillCards],["items",window.pItems],["drinks",window.pDrinks]].forEach(([kind,list])=>list.forEach(item=>{const translated=window.catalogTranslations[`${kind}:${item.id}`]||{};Object.entries(translated).forEach(([field,value])=>{if(field==="name"||field==="short")return;item[`original${field[0].toUpperCase()+field.slice(1)}`]=item[field];item[field]=value})}));\n'
(ROOT/'catalog-translations.js').write_text(runtime,encoding='utf-8')
remaining=[]
def find_remaining(value):
    if isinstance(value,str) and JP.search(value):remaining.append(value)
    elif isinstance(value,dict):
        for child in value.values():find_remaining(child)
    elif isinstance(value,list):
        for child in value:find_remaining(child)
find_remaining({u:{'title':x['title'],'sections':x['sections']} for u,x in translated.items()})
print(json.dumps({'source_strings':len(cache),'remaining_japanese_strings':len(remaining),'articles':len(translated)},ensure_ascii=False))
