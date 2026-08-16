(() => {
  const root = window.GAKUMAS_ROOT || new URL("./", location.href).href;
  const type = document.body.dataset.type || new URLSearchParams(location.search).get("type");
  const id = document.body.dataset.id || new URLSearchParams(location.search).get("id");
  const clean = type && id ? `${root}database/${encodeURIComponent(type)}/${encodeURIComponent(id)}/` : null;
  if (location.pathname.endsWith("/detail.html") && clean) { location.replace(clean); return; }
  document.querySelectorAll('a[href^="detail.html?"]').forEach(link => {const url=new URL(link.getAttribute("href"),root),t=url.searchParams.get("type"),i=url.searchParams.get("id");if(t&&i)link.href=`${root}database/${encodeURIComponent(t)}/${encodeURIComponent(i)}/`});
  document.querySelectorAll('a[href^="catalog.html"],a[href="index.html"],a[href="rights.html"]').forEach(link=>link.href=new URL(link.getAttribute("href"),root).href);
  document.querySelectorAll('img[src^="assets/"]').forEach(image=>image.src=new URL(image.getAttribute("src"),root).href);
  if(clean){let canonical=document.querySelector('link[rel="canonical"]');if(!canonical){canonical=document.createElement("link");canonical.rel="canonical";document.head.append(canonical)}canonical.href=clean}
})();
