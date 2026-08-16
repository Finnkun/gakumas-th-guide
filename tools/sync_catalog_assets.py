"""Self-host catalogue thumbnails referenced by generated data files."""
import concurrent.futures
import json
import re
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "catalog"
OUT.mkdir(parents=True, exist_ok=True)
HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; GakumasTHAssetSync/1.0)"}
SOURCES = [("pidols","pidols.js","pidols"),("supports","supportcards.js","supportCards"),("skills","skillcards.js","skillCards"),("items","itemdata.js","pItems"),("drinks","itemdata.js","pDrinks")]

def read_array(filename, variable):
    text = (ROOT / filename).read_text(encoding="utf-8")
    match = re.search(rf"window\.{variable}\s*=\s*(\[.*?\]);", text, re.S)
    return json.loads(match.group(1)) if match else []

jobs = []
for kind, filename, variable in SOURCES:
    for entry in read_array(filename, variable):
        if entry.get("image"):
            jobs.append((kind, str(entry["id"]), entry["image"]))

def download(job):
    kind, identifier, url = job
    safe = re.sub(r"[^a-zA-Z0-9_-]", "-", identifier)
    request = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(request, timeout=45) as response:
        content = response.read()
        media = response.headers.get_content_type()
    extension = {"image/webp":".webp","image/png":".png","image/gif":".gif"}.get(media, ".jpg")
    folder = OUT / kind
    folder.mkdir(exist_ok=True)
    destination = folder / f"{safe}{extension}"
    destination.write_bytes(content)
    return {"key":f"{kind}:{identifier}","file":destination.relative_to(ROOT).as_posix(),"source_image":url,"bytes":len(content)}

manifest, failures = [], []
with concurrent.futures.ThreadPoolExecutor(max_workers=16) as executor:
    future_map = {executor.submit(download, job):job for job in jobs}
    for future in concurrent.futures.as_completed(future_map):
        try: manifest.append(future.result())
        except Exception as error: failures.append({"job":future_map[future],"error":str(error)})

manifest.sort(key=lambda x:x["key"])
(OUT / "manifest.json").write_text(json.dumps({"assets":manifest,"failures":failures}, ensure_ascii=False, indent=2), encoding="utf-8")
asset_map = {x["key"]:x["file"] for x in manifest}
runtime = "window.catalogAssetMap = " + json.dumps(asset_map, ensure_ascii=False, separators=(",", ":")) + ";\n"
runtime += '[["pidols",window.pidols],["supports",window.supportCards],["skills",window.skillCards],["items",window.pItems],["drinks",window.pDrinks]].forEach(([kind,list])=>list.forEach(item=>{item.image=window.catalogAssetMap[`${kind}:${item.id}`]||item.image}));\n'
(ROOT / "catalog-assets.js").write_text(runtime, encoding="utf-8")
print(json.dumps({"requested":len(jobs),"downloaded":len(manifest),"failed":len(failures),"bytes":sum(x["bytes"] for x in manifest)}, ensure_ascii=False))
