"""Apply idempotent shared production shell upgrades to static HTML pages."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]


def update(name, changes):
    path = ROOT / name
    text = path.read_text(encoding="utf-8")
    for old, new in changes:
        if new in text:
            continue
        if old not in text:
            raise RuntimeError(f"Missing marker in {name}: {old[:80]}")
        text = text.replace(old, new, 1)
    path.write_text(text, encoding="utf-8")


update("catalog.html", [
    ("</head><body>", '<link rel="stylesheet" href="p0.css"></head><body><a class="skip-link" href="#main-content">ข้ามไปยังเนื้อหา</a>'),
    ('<main id="top">', '<main id="main-content">'),
    ('href="CONTENT_RIGHTS.md"', 'href="rights.html"'),
])
update("detail.html", [
    ("</head><body>", '<link rel="stylesheet" href="p0.css"></head><body><a class="skip-link" href="#main-content">ข้ามไปยังเนื้อหา</a>'),
    ('<main id="detailRoot">', '<main id="main-content" data-detail-root>'),
    ('href="CONTENT_RIGHTS.md"', 'href="rights.html"'),
])

update("index.html", [
    ("</head>", '  <link rel="stylesheet" href="p0.css" />\n</head>'),
    ("<body>", '<body>\n  <a class="skip-link" href="#main-content">ข้ามไปยังเนื้อหา</a>'),
    ('<main id="top">', '<main id="main-content">'),
    ('href="CONTENT_RIGHTS.md"', 'href="rights.html"'),
])

index_path = ROOT / "index.html"
index_text = index_path.read_text(encoding="utf-8")
index_text = re.sub(
    r'<button class="read-more article-open" data-article="([^"]+)">(.*?)</button>',
    lambda match: f'<a class="read-more article-link" href="guides/{match.group(1)}/" aria-label="{re.sub(r"<[^>]+>", "", match.group(2)).strip()}">{match.group(2)}</a>',
    index_text,
    flags=re.S,
)
index_path.write_text(index_text, encoding="utf-8")

print("updated index.html, catalog.html, detail.html")
