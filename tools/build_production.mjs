import fs from "node:fs";
import path from "node:path";
import vm from "node:vm";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const context = { window: {} };
vm.createContext(context);
vm.runInContext(fs.readFileSync(path.join(root, "articles.js"), "utf8"), context);
const articles = context.window.guideArticles;
for (const filename of ["pidols.js", "supportcards.js", "skillcards.js", "itemdata.js", "catalog-translations.js", "catalog-assets.js"]) vm.runInContext(fs.readFileSync(path.join(root, filename), "utf8"), context);
vm.runInContext(fs.readFileSync(path.join(root, "deep-details.js"), "utf8"), context);
const base = "https://finnkun.github.io/gakumas-th-guide";
const esc = value => String(value).replace(/[&<>"']/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));

for (const [id, article] of Object.entries(articles)) {
  const dir = path.join(root, "guides", id);
  fs.mkdirSync(dir, { recursive: true });
  const url = `${base}/guides/${id}/`;
  const html = `<!doctype html><html lang="th"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>${esc(article.title)} — GAKUMAS TH</title><meta name="description" content="${esc(article.lead)}"><link rel="canonical" href="${url}"><meta property="og:type" content="article"><meta property="og:site_name" content="GAKUMAS TH"><meta property="og:title" content="${esc(article.title)}"><meta property="og:description" content="${esc(article.lead)}"><meta property="og:url" content="${url}"><meta property="og:image" content="${base}/assets/game8/guide-home.png"><meta name="twitter:card" content="summary_large_image"><link rel="icon" href="../../assets/app-icon.svg"><link rel="stylesheet" href="../../site-shell.css"><link rel="stylesheet" href="../../articles.css"><link rel="stylesheet" href="../../p0.css"><script type="application/ld+json">${JSON.stringify({"@context":"https://schema.org","@type":"Article",headline:article.title,description:article.lead,url,dateModified:"2026-08-16",publisher:{"@type":"Organization",name:"GAKUMAS TH"}})}</script></head><body><a class="skip-link" href="#main-content">ข้ามไปยังเนื้อหา</a><header class="site-header"><a class="site-brand" href="../../index.html"><span>G</span>GAKUMAS <b>TH</b></a><nav><a href="../../index.html#guides">คู่มือ</a><a href="../../catalog.html?type=pidols">P Idol</a><a href="../../catalog.html?type=supports">Support Card</a><a href="../../catalog.html?type=skills">Skill Card</a><a href="../../index.html#glossary">คำศัพท์</a></nav></header><main id="main-content" class="article-page"><div class="breadcrumb"><a href="../../index.html">หน้าหลัก</a><span>›</span><a href="../../index.html#guides">คู่มือ</a><span>›</span><span>${esc(article.title)}</span></div><article class="article-content"><div class="article-meta">${esc(article.meta)} · อัปเดต 16 สิงหาคม 2026</div><h1>${esc(article.title)}</h1><p class="lead">${esc(article.lead)}</p>${article.body}<div class="attribution"><b>Translated and localized from Game8</b><br><span>คำแปลแฟนเมด ไม่ใช่เนื้อหาอย่างเป็นทางการของ Game8</span><br><a class="source-link" href="${esc(article.source)}" target="_blank" rel="noreferrer">อ่านบทความต้นฉบับบน Game8 ↗</a></div></article></main><footer class="site-footer"><a href="../../rights.html">สิทธิ์และเครดิต</a><a href="../../index.html">กลับหน้าหลัก</a></footer></body></html>`;
  fs.writeFileSync(path.join(dir, "index.html"), html, "utf8");
}

const groups = { pidols: context.window.pidols, supports: context.window.supportCards, skills: context.window.skillCards, items: context.window.pItems, drinks: context.window.pDrinks };
const detailTemplate = fs.readFileSync(path.join(root, "detail.html"), "utf8");
const detailUrls = [];
for (const [type, items] of Object.entries(groups)) for (const item of items) {
  const id = String(item.id);
  const dir = path.join(root, "database", type, id);
  fs.mkdirSync(dir, { recursive: true });
  const url = `${base}/database/${type}/${encodeURIComponent(id)}/`;
  const name = item.short || item.name;
  const description = `${name} — ${item.plan || ""} ${item.rarity || item.tier || ""} ${item.effect || item.note || ""}`.trim().slice(0, 220);
  const image = String(item.image || "assets/app-icon.svg").replace(/^\.\//, "");
  const jsonLd = {"@context":"https://schema.org","@type":"WebPage",name,description,url,breadcrumb:{"@type":"BreadcrumbList",itemListElement:[{"@type":"ListItem",position:1,name:"หน้าหลัก",item:`${base}/`},{"@type":"ListItem",position:2,name:type,item:`${base}/catalog.html?type=${type}`},{"@type":"ListItem",position:3,name}]}};
  let html = detailTemplate
    .replace("<head>", '<head><base href="../../../">')
    .replace("<title>รายละเอียด — GAKUMAS TH</title>", `<title>${esc(name)} — GAKUMAS TH</title>`)
    .replace('<meta name="description" content="รายละเอียดข้อมูล Gakuen Idolmaster ภาษาไทย">', `<meta name="description" content="${esc(description)}"><link rel="canonical" href="${url}"><meta property="og:type" content="article"><meta property="og:site_name" content="GAKUMAS TH"><meta property="og:title" content="${esc(name)}"><meta property="og:description" content="${esc(description)}"><meta property="og:url" content="${url}"><meta property="og:image" content="${base}/${esc(image)}"><meta name="twitter:card" content="summary_large_image"><script type="application/ld+json">${JSON.stringify(jsonLd)}</script>`)
    .replace("<body>", `<body data-type="${type}" data-id="${esc(id)}">`)
    .replace('data-page="detail"', `data-page="detail" data-type="${type}"`);
  fs.writeFileSync(path.join(dir, "index.html"), html, "utf8");
  const detailDir = path.join(root, "detail-data", type);
  fs.mkdirSync(detailDir, { recursive: true });
  const article = context.window.deepDetails[item.source];
  fs.writeFileSync(path.join(detailDir, `${id}.js`), `window.deepDetails=${JSON.stringify(article ? {[item.source]:article} : {})};\n`, "utf8");
  detailUrls.push(`/database/${type}/${encodeURIComponent(id)}/`);
}

const urls = ["/", "/rights.html", "/catalog.html?type=pidols", "/catalog.html?type=supports", "/catalog.html?type=skills", "/catalog.html?type=items", "/catalog.html?type=drinks", ...Object.keys(articles).map(id => `/guides/${id}/`), ...detailUrls];
const sitemap = `<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">${urls.map(url => `<url><loc>${base}${url.replaceAll("&", "&amp;")}</loc><lastmod>2026-08-16</lastmod></url>`).join("")}</urlset>\n`;
fs.writeFileSync(path.join(root, "sitemap.xml"), sitemap, "utf8");
fs.writeFileSync(path.join(root, "robots.txt"), `User-agent: *\nAllow: /\nSitemap: ${base}/sitemap.xml\n`, "utf8");
console.log({ guides: Object.keys(articles).length, details: detailUrls.length, sitemapUrls: urls.length });
