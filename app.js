const words = [
  ["攻略", "คู่มือ / แนวทาง", "ข้อมูลแนะนำวิธีเล่นหรือผ่านเนื้อหา", "general", "guide strategy"],
  ["育成", "การปั้นตัวละคร", "การฝึกและพัฒนาไอดอลระหว่าง Produce", "produce", "training"],
  ["編成", "การจัดทีม", "การเลือกตัวละคร การ์ด หรือ Memory เข้าชุด", "produce", "team setup"],
  ["Pアイドル", "ไอดอลที่โปรดิวซ์", "ตัวละครหลักที่เราเลือกมาปั้นในหนึ่งรอบ", "produce", "p idol character"],
  ["サポートカード / サポカ", "การ์ดซัพพอร์ต", "การ์ดสนับสนุนที่ให้โบนัสและอีเวนต์ระหว่างการปั้น", "item", "support card"],
  ["スキルカード", "การ์ดสกิล", "คำสั่งที่ใช้ใน Lesson และการสอบ", "item", "skill card"],
  ["Pアイテム", "P Item", "ไอเทมติดตัวที่สร้างเอฟเฟกต์อัตโนมัติ", "item", "item equipment"],
  ["Pドリンク", "P Drink", "ของใช้ครั้งเดียวระหว่าง Lesson หรือการสอบ", "item", "drink consumable"],
  ["メモリー", "Memory", "ผลจากการปั้นที่ส่งต่อสกิลและโบนัสไปยังรอบใหม่", "item", "memory"],
  ["ボーカル / Vo", "โวคอล / การร้อง", "หนึ่งในสามค่าสถานะการแสดง", "status", "vocal"],
  ["ダンス / Da", "แดนซ์ / การเต้น", "หนึ่งในสามค่าสถานะการแสดง", "status", "dance"],
  ["ビジュアル / Vi", "วิชวล / ภาพลักษณ์", "หนึ่งในสามค่าสถานะการแสดง", "status", "visual"],
  ["体力", "พลังงาน", "ทรัพยากรที่ใช้เล่นการ์ดและทำกิจกรรม", "status", "stamina health"],
  ["元気", "เกราะ / พลังชั่วคราว", "ช่วยรับค่าใช้จ่ายของการ์ดแทนพลังงาน และทำงานร่วมกับ Logic", "status", "genki shield"],
  ["集中", "สมาธิ", "เพิ่มค่าพื้นฐานที่ได้จากการ์ดทำคะแนน", "status", "focus concentration"],
  ["好調", "ฟอร์มดี", "เพิ่มประสิทธิภาพการทำคะแนนของสาย Sense", "status", "good condition"],
  ["絶好調", "ฟอร์มยอดเยี่ยม", "สถานะเสริมที่ยิ่งทำให้โบนัสจาก 好調 มีประสิทธิภาพ", "status", "excellent condition"],
  ["やる気", "แรงจูงใจ", "เพิ่มปริมาณ 元気 ที่ได้รับ เหมาะกับ Logic บางสาย", "status", "motivation"],
  ["好印象", "ความประทับใจ", "เอฟเฟกต์สะสมที่มักสร้างคะแนนตามเทิร์น", "status", "good impression"],
  ["強気", "มั่นใจ / รุกหนัก", "สภาวะของ Anomaly ที่เน้นการเร่งเกม", "status", "confident anomaly"],
  ["全力", "ทุ่มสุดกำลัง", "จังหวะระเบิดพลังสำคัญของ Anomaly", "status", "full power"],
  ["レッスン", "การฝึกซ้อม", "ด่านเล่นการ์ดเพื่อเพิ่มค่าสถานะ", "produce", "lesson"],
  ["SPレッスン", "การฝึกพิเศษ", "Lesson ที่ให้ผลตอบแทนสูงกว่าปกติ", "produce", "special lesson"],
  ["授業", "เข้าเรียน", "กิจกรรมที่ให้เลือกผลตอบแทนหรือเงื่อนไข", "produce", "class"],
  ["おでかけ", "ออกไปข้างนอก", "กิจกรรมฟื้นฟูหรือรับประโยชน์เพิ่มเติม", "produce", "outing"],
  ["おやすみ", "พักผ่อน", "ฟื้นพลังงานระหว่างการปั้น", "produce", "rest"],
  ["相談", "ปรึกษา", "ร้านสำหรับซื้อ อัปเกรด หรือลบการ์ด", "produce", "consult shop"],
  ["中間試験", "สอบกลางภาค", "จุดทดสอบสำคัญช่วงกลางของการปั้น", "produce", "midterm exam"],
  ["最終試験", "สอบปลายภาค", "ด่านตัดสินผลลัพธ์ช่วงท้ายของการปั้น", "produce", "final exam"],
  ["親愛度", "ค่าความสนิท", "ใช้ปลดล็อกเรื่องราวและเนื้อหาของไอดอล", "general", "affection bond"],
  ["才能開花", "ปลดศักยภาพ", "การเพิ่มระดับศักยภาพของ P Idol", "general", "talent awakening"],
  ["上限解放", "ปลดขีดจำกัด", "เพิ่มเพดานหรือประสิทธิภาพของการ์ดซัพพอร์ต", "general", "limit break"],
  ["限定", "ลิมิเต็ด", "สิ่งที่หาได้เฉพาะช่วงเวลาหรือตู้ที่กำหนด", "general", "limited"],
  ["配布", "ของแจก", "ตัวละครหรือการ์ดที่รับจากกิจกรรม", "general", "free distribution"],
  ["開催期間", "ระยะเวลากิจกรรม", "ช่วงเริ่มต้นและสิ้นสุดของกาชาหรือกิจกรรม", "general", "event period"],
  ["入手方法", "วิธีได้รับ", "เงื่อนไขหรือแหล่งที่ใช้หาไอเทม", "general", "obtain method"],
  ["リセマラ", "รีโรล", "เริ่มบัญชีใหม่เพื่อสุ่มผลกาชาที่ต้องการ", "general", "reroll"],
  ["最強", "แข็งแกร่งที่สุด", "มักใช้กับบทความจัดอันดับหรือ Tier List", "general", "strongest tier"],
  ["おすすめ", "แนะนำ", "ตัวเลือกที่เว็บไซต์มองว่าเหมาะหรือคุ้มค่า", "general", "recommended"],
  ["一覧", "รายการทั้งหมด", "หน้ารวมตัวละคร การ์ด หรือไอเทม", "general", "list index"]
];

const systems = {
  sense: { no:"01", jp:"センス", title:"สะสมพลัง แล้วระเบิดคะแนน", text:"บริหาร <b>集中 (สมาธิ)</b> และ <b>好調 (ฟอร์มดี)</b> ก่อนใช้การ์ดทำคะแนนแรงในจังหวะสำคัญ เหมาะกับคนที่ชอบวางคอมโบชัดเจน", flow:["集中","＋","好調","→","SCORE"] },
  logic: { no:"02", jp:"ロジック", title:"ต่อยอดเอฟเฟกต์ให้เติบโต", text:"สะสม <b>好印象 (ความประทับใจ)</b> เพื่อสร้างคะแนนต่อเนื่อง หรือใช้ <b>やる気 (แรงจูงใจ)</b> เพิ่ม 元気 แล้วแปลงเป็นคะแนน", flow:["やる気","＋","元気","→","SCORE"] },
  anomaly: { no:"03", jp:"アノマリー", title:"คุมจังหวะ เปลี่ยนสภาวะ", text:"อ่านลำดับเทิร์นและบริหารสภาวะ เช่น <b>強気</b> กับจังหวะ <b>全力</b> มีความซับซ้อนสูง แต่ให้รางวัลกับการวางแผนที่แม่นยำ", flow:["強気","⇄","温存","→","全力"] }
};

const wordList = document.querySelector("#wordList");
const wordCount = document.querySelector("#wordCount");
const glossarySearch = document.querySelector("#glossarySearch");
const emptyState = document.querySelector("#emptyState");
let currentFilter = "all";

const characterGrid=document.querySelector("#characterGrid");
const characterSearch=document.querySelector("#characterSearch");
const characterEmpty=document.querySelector("#characterEmpty");
function renderCharacters(){
  const q=(characterSearch?.value||"").trim().toLowerCase();
  const list=window.characterProfiles.filter(c=>Object.values(c).join(" ").toLowerCase().includes(q));
  characterGrid.innerHTML=list.map((c,i)=>`<article class="character-card" style="--character:${c.accent}"><div class="character-top"><span class="character-index">${String(i+1).padStart(2,"0")}</span><div class="character-monogram">${c.jp.slice(-1)}</div></div><div class="character-name"><small>${c.kana}</small><h3>${c.jp}</h3><span>${c.roman}</span></div><div class="character-facts"><span><b>${c.age}</b> ปี</span><span><b>${c.height}</b> cm</span><span><b>${c.blood}</b> กรุ๊ปเลือด</span></div><p>${c.bio}</p><details><summary>ข้อมูลเพิ่มเติม</summary><dl><div><dt>วันเกิด</dt><dd>${c.birthday}</dd></div><div><dt>บ้านเกิด</dt><dd>${c.origin}</dd></div><div><dt>ผู้พากย์</dt><dd>${c.cv}</dd></div></dl></details></article>`).join("");
  characterEmpty.hidden=list.length>0;
}
characterSearch?.addEventListener("input",renderCharacters);

const pidolRows=document.querySelector("#pidolRows"),pidolSearch=document.querySelector("#pidolSearch"),pidolPlan=document.querySelector("#pidolPlan"),pidolTier=document.querySelector("#pidolTier"),pidolCount=document.querySelector("#pidolCount"),pidolEmpty=document.querySelector("#pidolEmpty");
function tierClass(t){return t==="SS"?"ss":t==="S"?"s":t==="A"?"a":t==="B"?"b":t==="C"?"c":"pending"}
function renderPidols(){
 const q=(pidolSearch?.value||"").trim().toLowerCase(),plan=pidolPlan?.value||"all",tier=pidolTier?.value||"all";
 const list=window.pidols.filter(p=>(plan==="all"||p.plan===plan)&&(tier==="all"||p.tier===tier)&&Object.values(p).join(" ").toLowerCase().includes(q));
 pidolRows.innerHTML=list.map(p=>`<tr><td><a class="data-detail-link" href="detail.html?type=pidols&id=${encodeURIComponent(p.id)}"><b>${p.short}</b></a><small>${p.name}<br>${p.idol}</small><em>${p.note}</em></td><td><span class="tier-pill ${tierClass(p.tier)}">${p.tier}</span></td><td><span class="plan-pill ${p.plan.toLowerCase()}">${p.plan}</span><small>${p.style}</small></td><td>${p.rarity}</td><td>${p.obtain}</td></tr>`).join("");
 pidolCount.textContent=list.length;pidolEmpty.hidden=list.length>0;
}
[pidolSearch,pidolPlan,pidolTier].forEach(x=>x?.addEventListener("input",renderPidols));
document.querySelector("#pidolReset")?.addEventListener("click",()=>{pidolSearch.value="";pidolPlan.value="all";pidolTier.value="all";renderPidols()});

const supportRows=document.querySelector("#supportRows"),supportSearch=document.querySelector("#supportSearch"),supportPlan=document.querySelector("#supportPlan"),supportType=document.querySelector("#supportType"),supportRarity=document.querySelector("#supportRarity"),supportTier=document.querySelector("#supportTier"),supportCount=document.querySelector("#supportCount"),supportEmpty=document.querySelector("#supportEmpty");
function renderSupports(){
 const q=(supportSearch?.value||"").trim().toLowerCase(),plan=supportPlan?.value||"all",type=supportType?.value||"all",rarity=supportRarity?.value||"all",tier=supportTier?.value||"all";
 const list=window.supportCards.filter(c=>(plan==="all"||c.plan===plan)&&(type==="all"||c.type===type)&&(rarity==="all"||c.rarity===rarity)&&(tier==="all"||c.tier===tier)&&Object.values(c).join(" ").toLowerCase().includes(q));
 supportRows.innerHTML=list.map(c=>`<tr><td><a class="data-detail-link" href="detail.html?type=supports&id=${encodeURIComponent(c.id)}"><b>${c.name}</b></a></td><td><span class="tier-pill ${tierClass(c.tier)}">${c.tier}</span></td><td><span class="type-pill ${c.type.toLowerCase()}">${c.type}</span></td><td><span class="plan-pill ${c.plan.toLowerCase()}">${c.plan}</span></td><td>${c.obtain}</td></tr>`).join("");
 supportCount.textContent=list.length;supportEmpty.hidden=list.length>0;
}
[supportSearch,supportPlan,supportType,supportRarity,supportTier].forEach(x=>x?.addEventListener("input",renderSupports));
document.querySelector("#supportReset")?.addEventListener("click",()=>{supportSearch.value="";supportPlan.value="all";supportType.value="all";supportRarity.value="all";supportTier.value="all";renderSupports()});

const skillGrid=document.querySelector("#skillGrid"),skillSearch=document.querySelector("#skillSearch"),skillPlan=document.querySelector("#skillPlan"),skillRarity=document.querySelector("#skillRarity"),skillCount=document.querySelector("#skillCount"),skillEmpty=document.querySelector("#skillEmpty");
function renderSkills(){
 const q=(skillSearch?.value||"").trim().toLowerCase(),plan=skillPlan?.value||"all",rarity=skillRarity?.value||"all";
 const list=window.skillCards.filter(c=>(plan==="all"||c.plan===plan)&&(rarity==="all"||c.rarity===rarity)&&Object.values(c).join(" ").toLowerCase().includes(q));
 skillGrid.innerHTML=list.map(c=>`<article class="skill-card"><div><span class="plan-pill ${c.plan.toLowerCase()}">${c.plan}</span><span class="rarity-label">${c.rarity}</span></div><h3><a class="data-detail-link dark-link" href="detail.html?type=skills&id=${encodeURIComponent(c.id)}">${c.name}</a></h3><p>${c.effect}</p></article>`).join("");
 skillCount.textContent=list.length;skillEmpty.hidden=list.length>0;
}
[skillSearch,skillPlan,skillRarity].forEach(x=>x?.addEventListener("input",renderSkills));
document.querySelector("#skillReset")?.addEventListener("click",()=>{skillSearch.value="";skillPlan.value="all";skillRarity.value="all";renderSkills()});

const itemGrid=document.querySelector("#itemGrid"),itemSearch=document.querySelector("#itemSearch"),itemPlan=document.querySelector("#itemPlan"),itemCount=document.querySelector("#itemCount"),itemEmpty=document.querySelector("#itemEmpty"),itemSource=document.querySelector("#itemSource");let itemKind="item";
function renderItems(){
 const data=itemKind==="item"?window.pItems:window.pDrinks,q=(itemSearch?.value||"").trim().toLowerCase(),plan=itemPlan?.value||"all";
 const list=data.filter(x=>(plan==="all"||x.plan===plan)&&Object.values(x).join(" ").toLowerCase().includes(q));
 itemGrid.innerHTML=list.map(x=>`<article class="item-card"><div><span class="plan-pill ${x.plan.toLowerCase()}">${x.plan}</span>${x.unlock?`<span class="unlock-label">PLv ${x.unlock}</span>`:""}</div><h3><a class="data-detail-link dark-link" href="detail.html?type=${itemKind==="item"?"items":"drinks"}&id=${encodeURIComponent(x.id)}">${x.name}</a></h3><p>${x.effect}</p></article>`).join("");
 itemCount.textContent=list.length;itemEmpty.hidden=list.length>0;document.querySelector("#itemTotal").textContent=window.pItems.length;document.querySelector("#drinkTotal").textContent=window.pDrinks.length;
 itemSource.innerHTML=itemKind==="item"?'Original guide/content: <a href="https://game8.jp/gakuen-idolmaster/610077" target="_blank" rel="noreferrer">Game8 — Pアイテム一覧 ↗</a>':'Original guide/content: <a href="https://game8.jp/gakuen-idolmaster/611910" target="_blank" rel="noreferrer">Game8 — Pドリンク一覧 ↗</a>';
}
document.querySelectorAll(".item-tab").forEach(btn=>btn.addEventListener("click",()=>{document.querySelectorAll(".item-tab").forEach(x=>x.classList.remove("active"));btn.classList.add("active");itemKind=btn.dataset.kind;renderItems()}));
[itemSearch,itemPlan].forEach(x=>x?.addEventListener("input",renderItems));document.querySelector("#itemReset")?.addEventListener("click",()=>{itemSearch.value="";itemPlan.value="all";renderItems()});

const scenarioGrid=document.querySelector("#scenarioGrid");
function renderScenarios(){scenarioGrid.innerHTML=window.scenarioGuides.map((s,i)=>`<article class="scenario-card"><div class="scenario-index">${String(i+1).padStart(2,"0")}</div><span class="scenario-level">${s.level}</span><small>${s.jp}</small><h3>${s.name}</h3><p>${s.summary}</p><details><summary>ดูแนวทางทีละขั้น</summary><ol>${s.steps.map(x=>`<li>${x}</li>`).join("")}</ol></details><a href="${s.source}" target="_blank" rel="noreferrer">Original guide/content: Game8 ↗</a></article>`).join("")}

function renderWords(){
  const q = glossarySearch.value.trim().toLowerCase();
  const matches = words.filter(w => (currentFilter === "all" || w[3] === currentFilter) && w.join(" ").toLowerCase().includes(q));
  wordList.innerHTML = matches.map(w => `<div class="word-row"><div class="jp">${w[0]}</div><div class="thai">${w[1]}</div><div class="desc">${w[2]}</div></div>`).join("");
  wordCount.textContent = `${matches.length} คำจากทั้งหมด ${words.length} คำ`;
  emptyState.hidden = matches.length > 0;
}

glossarySearch.addEventListener("input", renderWords);
document.querySelectorAll(".filter").forEach(btn => btn.addEventListener("click", () => {
  document.querySelectorAll(".filter").forEach(b => b.classList.remove("active"));
  btn.classList.add("active"); currentFilter = btn.dataset.filter; renderWords();
}));

document.querySelectorAll(".road-step").forEach(btn => btn.addEventListener("click", () => {
  document.querySelectorAll(".road-step").forEach(b => b.classList.remove("active"));
  btn.classList.add("active"); document.querySelector("#roadDetail").textContent = btn.dataset.detail;
}));

document.querySelectorAll(".system-tab").forEach(btn => btn.addEventListener("click", () => {
  document.querySelectorAll(".system-tab").forEach(b => b.classList.remove("active")); btn.classList.add("active");
  const s = systems[btn.dataset.system];
  document.querySelector("#systemPanel").innerHTML = `<div class="system-number">${s.no}</div><div><span class="jp-title">${s.jp}</span><h3>${s.title}</h3><p>${s.text}</p></div><div class="system-flow">${s.flow.map((x,i)=>i===s.flow.length-1?`<strong>${x}</strong>`:x==="＋"||x==="→"||x==="⇄"?`<i>${x}</i>`:`<span>${x}</span>`).join("")}</div>`;
}));

const dialog = document.querySelector("#searchDialog");
const quickSearch = document.querySelector("#quickSearch");
const quickResults = document.querySelector("#quickResults");
const menuToggle=document.querySelector("#menuToggle"),mobileNav=document.querySelector("#mobileNav");
menuToggle?.addEventListener("click",()=>{const open=mobileNav.classList.toggle("open");menuToggle.setAttribute("aria-expanded",String(open))});
mobileNav?.querySelectorAll("a").forEach(a=>a.addEventListener("click",()=>{mobileNav.classList.remove("open");menuToggle.setAttribute("aria-expanded","false")}));
document.querySelector("#searchToggle").addEventListener("click", () => { dialog.showModal(); setTimeout(()=>quickSearch.focus(),80); });
document.querySelector("#dialogClose").addEventListener("click", () => dialog.close());
quickSearch.addEventListener("input", () => {
  const q = quickSearch.value.toLowerCase().trim();
  if(!q){quickResults.innerHTML='<p class="search-hint">ค้นหาได้ทั้ง P Idol, Support, Skill, Item, Drink, Scenario และคำศัพท์</p>'; return;}
  const groups=[
   ["P IDOL","#pidols",window.pidols,p=>`${p.short} — ${p.plan} ${p.tier}`],
   ["SUPPORT","#supports",window.supportCards,p=>`${p.name} — ${p.plan} ${p.rarity}`],
   ["SKILL","#skills",window.skillCards,p=>`${p.name} — ${p.effect.slice(0,70)}`],
   ["P ITEM","#items",window.pItems,p=>`${p.name} — ${p.effect.slice(0,70)}`],
   ["P DRINK","#items",window.pDrinks,p=>`${p.name} — ${p.effect.slice(0,70)}`],
   ["SCENARIO","#scenarios",window.scenarioGuides,p=>`${p.name} — ${p.summary}`],
   ["CHARACTER","#characters",window.characterProfiles,p=>`${p.jp} — ${p.roman}`]
  ];
  let html="",remaining=12;
  groups.forEach(([label,href,data,format])=>{const found=data.filter(x=>Object.values(x).flat().join(" ").toLowerCase().includes(q)).slice(0,Math.min(3,remaining));if(found.length){html+=`<div class="quick-group">${label}</div>`+found.map(x=>`<a class="quick-result" href="${href}">${format(x)}</a>`).join("");remaining-=found.length}});
  const wordMatches=words.filter(x=>x.join(" ").toLowerCase().includes(q)).slice(0,Math.min(3,remaining));if(wordMatches.length)html+='<div class="quick-group">GLOSSARY</div>'+wordMatches.map(x=>`<a class="quick-result" href="#glossary">${x[0]} — ${x[1]}</a>`).join("");
  quickResults.innerHTML=html||'<p class="search-hint">ไม่พบข้อมูล ลองใช้ชื่อญี่ปุ่นหรือคำที่สั้นลง</p>';
  quickResults.querySelectorAll("a").forEach(a=>a.addEventListener("click",()=>dialog.close()));
});
document.addEventListener("keydown", e => { if(e.key === "Escape" && document.activeElement === glossarySearch){glossarySearch.value="";renderWords();} if(e.key === "Escape"&&mobileNav?.classList.contains("open")){mobileNav.classList.remove("open");menuToggle.setAttribute("aria-expanded","false")} if(e.key==="/" && !dialog.open && document.activeElement.tagName!=="INPUT"){e.preventDefault();dialog.showModal();setTimeout(()=>quickSearch.focus(),80);} });

const toast = document.querySelector("#toast"); let toastTimer;
document.querySelectorAll("[data-toast]").forEach(btn=>btn.addEventListener("click",()=>{toast.textContent=btn.dataset.toast;toast.classList.add("show");clearTimeout(toastTimer);toastTimer=setTimeout(()=>toast.classList.remove("show"),2600);}));

renderWords();
renderCharacters();
renderPidols();
renderSupports();
renderSkills();
renderItems();
renderScenarios();

const articleDialog = document.querySelector("#articleDialog");
const articleContent = document.querySelector("#articleContent");
document.querySelector("#articleClose").addEventListener("click",()=>articleDialog.close());
document.querySelectorAll(".article-open").forEach(btn=>btn.addEventListener("click",()=>{
  const a=window.guideArticles[btn.dataset.article];
  articleContent.innerHTML=`<div class="article-meta">${a.meta}</div><h2>${a.title}</h2><p class="lead">${a.lead}</p>${a.body}<div class="attribution"><b>Translated and localized from Game8</b><br><span>คำแปลแฟนเมด ไม่ใช่เนื้อหาอย่างเป็นทางการของ Game8 และไม่มีความเกี่ยวข้องหรือการรับรองอย่างเป็นทางการ</span><br><a class="source-link" href="${a.source}" target="_blank" rel="noreferrer">อ่านบทความต้นฉบับบน Game8 ↗</a></div>`;
  articleDialog.showModal();
  articleDialog.scrollTop=0;
}));
