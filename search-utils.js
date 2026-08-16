window.GakumasSearch = (() => {
  const terminology = {
    "体力":["พลังงาน"],"元気":["Genki","เก็นกิ"],"集中":["สมาธิ","Focus"],
    "好調":["ฟอร์มดี","Good Condition"],"絶好調":["ฟอร์มยอดเยี่ยม","Excellent Condition"],
    "やる気":["แรงจูงใจ","Motivation"],"好印象":["ความประทับใจ","Good Impression"],
    "温存":["เก็บแรง","Conserve"],"強気":["รุกหนัก","Strong"],
    "全力":["ทุ่มสุดกำลัง","Full Power"],"全力値":["ค่า Full Power"],
    "熱意":["แรงมุ่งมั่น"],"スキルカード":["การ์ดสกิล"],"アクティブ":["Active"],
    "手札":["การ์ดในมือ"],"山札":["กองจั่ว"],"捨て札":["กองทิ้ง"],"保留":["ช่องพัก"],
    "レッスン":["Lesson"],"プロデュース":["Produce","การปั้น"]
  };
  const aliases = {
    "花海咲季": ["Hanami Saki", "ฮานามิ ซากิ", "ซากิ"],
    "月村手毬": ["Tsukimura Temari", "สึกิมูระ เทมาริ", "เทมาริ"],
    "藤田ことね": ["Fujita Kotone", "ฟูจิตะ โคโตเนะ", "โคโตเนะ"],
    "有村麻央": ["Arimura Mao", "อาริมูระ มาโอะ", "มาโอะ"],
    "葛城リーリヤ": ["Katsuragi Lilja", "คัตสึรากิ ลิลจา", "ลิลจา", "ลีเลีย"],
    "倉本千奈": ["Kuramoto China", "คุราโมโตะ จินะ", "จินะ", "ชินะ"],
    "紫雲清夏": ["Shiun Sumika", "ชิอุน สุมิกะ", "สุมิกะ"],
    "篠澤広": ["Shinosawa Hiro", "ชิโนซาวะ ฮิโระ", "ฮิโระ"],
    "姫崎莉波": ["Himesaki Rinami", "ฮิเมซากิ รินามิ", "รินามิ"],
    "花海佑芽": ["Hanami Ume", "ฮานามิ อุเมะ", "อุเมะ"],
    "十王星南": ["Juo Sena", "จูโอ เซนะ", "เซนะ"],
    "秦谷美鈴": ["美鈴", "Hataya Misuzu", "ฮาตายะ มิสึสึ", "มิสึสึ", "มิซึสึ", "มิสุสุ", "Misuzu"],
    "雨夜燕": ["Amaya Tsubame", "อามายะ สึบาเมะ", "สึบาเมะ"]
  };
  const normalize = value => String(value ?? "").normalize("NFKC").toLowerCase()
    .replace(/[ァ-ヶ]/g, c => String.fromCharCode(c.charCodeAt(0) - 0x60))
    .replace(/[\s\u3000()[\]{}「」『』【】・･ー―–—&＆'".,!?！？:：/\\_-]+/g, "");
  const enrich = value => {
    let text = typeof value === "string" ? value : Object.values(value || {}).flat(Infinity).join(" ");
    for (const [jp, names] of Object.entries(aliases)) if (text.includes(jp) || names.some(name => normalize(text).includes(normalize(name)))) text += ` ${names.join(" ")}`;
    for (const [jp, names] of Object.entries(terminology)) if (text.includes(jp) || names.some(name => normalize(text).includes(normalize(name)))) text += ` ${jp} ${names.join(" ")}`;
    return text;
  };
  const matches = (value, query) => !normalize(query) || normalize(enrich(value)).includes(normalize(query));
  return { aliases, terminology, normalize, enrich, matches };
})();
