"""Build the small, route-specific dataset used by the homepage previews."""
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]


def read_array(filename, variable):
    text = (ROOT / filename).read_text(encoding="utf-8")
    match = re.search(rf"window\.{variable}\s*=\s*(\[.*?\]);", text, re.S)
    if not match:
        raise RuntimeError(f"Could not find window.{variable} in {filename}")
    return json.loads(match.group(1))


sources = {
    "pidols": ("pidols.js", "pidols", 10),
    "supportCards": ("supportcards.js", "supportCards", 10),
    "skillCards": ("skillcards.js", "skillCards", 12),
    "pItems": ("itemdata.js", "pItems", 10),
    "pDrinks": ("itemdata.js", "pDrinks", 8),
}

parts = ["/* Generated homepage previews: never load full catalogues on index.html. */"]
search_records = []
for output_name, (filename, variable, limit) in sources.items():
    all_records = read_array(filename, variable)
    records = all_records[:limit]
    parts.append(f"window.{output_name} = {json.dumps(records, ensure_ascii=False, separators=(',', ':'))};")
    kind = {"supportCards":"supports","skillCards":"skills","pItems":"items","pDrinks":"drinks"}.get(output_name, output_name)
    for record in all_records:
        search_records.append({"type":kind,"id":record.get("id"),"name":record.get("short") or record.get("name",""),"text":" ".join(str(record.get(k,"")) for k in ("name","short","idol","effect","note","style","plan","rarity","tier","obtain"))[:600]})

(ROOT / "home-data.js").write_text("\n".join(parts) + "\n", encoding="utf-8")
(ROOT / "search-index.js").write_text("window.searchIndex=" + json.dumps(search_records, ensure_ascii=False, separators=(',', ':')) + ";\n", encoding="utf-8")
print({name: spec[2] for name, spec in sources.items()})
