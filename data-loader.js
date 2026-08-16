/* Load only the catalogue dataset required by the current route. */
(() => {
  const script = document.currentScript;
  const rootUrl = new URL("./", script.src).href;
  window.GAKUMAS_ROOT = rootUrl;
  const page = script?.dataset.page === "detail" ? "detail" : "catalog";
  const requested = script?.dataset.type || document.body.dataset.type || new URLSearchParams(location.search).get("type") || "pidols";
  const type = ["pidols", "supports", "skills", "items", "drinks"].includes(requested) ? requested : "pidols";
  const requestedId = document.body.dataset.id || new URLSearchParams(location.search).get("id");
  const source = type === "pidols" ? "pidols.js" : type === "supports" ? "supportcards.js" : type === "skills" ? "skillcards.js" : "itemdata.js";
  const files = [source, "catalog-translations.js", "catalog-assets.js", "search-utils.js"];
  if (page === "detail") files.push(requestedId ? `detail-data/${type}/${encodeURIComponent(requestedId)}.js` : "deep-details.js", "detail-app.js", "detail-route-fix.js");
  else files.push("catalog-app.js", "catalog-route-fix.js");
  document.write(files.map(file => `<script src="${new URL(file,rootUrl).href}" defer><\/script>`).join(""));
})();
