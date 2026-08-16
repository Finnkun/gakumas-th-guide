"""Download covered Game8 guide thumbnails for local self-hosting."""
import json
import re
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "game8"
OUT.mkdir(parents=True, exist_ok=True)
HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; GakumasTHAssetSync/1.0)"}
PAGES = {
    "guide-home": "https://game8.jp/gakuen-idolmaster",
    "pidols": "https://game8.jp/gakuen-idolmaster/609097",
    "supports": "https://game8.jp/gakuen-idolmaster/609102",
    "skills": "https://game8.jp/gakuen-idolmaster/609737",
    "pitems": "https://game8.jp/gakuen-idolmaster/610077",
    "pdrinks": "https://game8.jp/gakuen-idolmaster/611910",
    "hajime-legend": "https://game8.jp/gakuen-idolmaster/752651",
    "nia": "https://game8.jp/gakuen-idolmaster/661665",
    "hif": "https://game8.jp/gakuen-idolmaster/783836",
}

manifest = []
for slug, page in PAGES.items():
    request = urllib.request.Request(page, headers=HEADERS)
    document = urllib.request.urlopen(request, timeout=45).read().decode("utf-8", "ignore")
    match = re.search(r'<meta[^>]+property=["\']og:image["\'][^>]+content=["\']([^"\']+)', document, re.I)
    if not match:
        match = re.search(r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+property=["\']og:image', document, re.I)
    if not match:
        print(f"skip {slug}: no og:image")
        continue
    image_url = match.group(1).replace("&amp;", "&")
    if image_url.startswith("//"):
        image_url = "https:" + image_url
    extension = ".png" if ".png" in image_url.lower() else ".jpg"
    destination = OUT / f"{slug}{extension}"
    image_request = urllib.request.Request(image_url, headers=HEADERS)
    destination.write_bytes(urllib.request.urlopen(image_request, timeout=45).read())
    manifest.append({"slug":slug,"file":destination.relative_to(ROOT).as_posix(),"source_page":page,"source_image":image_url})

(OUT / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps({"downloaded":len(manifest),"directory":str(OUT)}, ensure_ascii=False))
