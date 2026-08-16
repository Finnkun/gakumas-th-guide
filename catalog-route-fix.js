(() => {
  const root = window.GAKUMAS_ROOT || new URL("./", location.href).href;
  const rewrite = () => document.querySelectorAll('a[href^="detail.html?"]').forEach(link => {
    const url = new URL(link.getAttribute("href"), root);
    const type = url.searchParams.get("type"), id = url.searchParams.get("id");
    if (type && id) link.href = `${root}database/${encodeURIComponent(type)}/${encodeURIComponent(id)}/`;
  });
  rewrite();
  new MutationObserver(rewrite).observe(document.getElementById("catalogGrid"), {childList:true});
})();
