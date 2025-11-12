/* SA Thomson Nerys – Widget (Gold theme)
   - Binds to existing DOM
   - Tracks history for PDF export
   - Buttons: Contact Agent & Download Transcript (PDF)
*/

(() => {
  const CFG = window.SATN_CONFIG || {};
  const API_BASE   = CFG.API_BASE   || "http://localhost:8000/api/v1";
  const TIMEOUT_MS = CFG.TIMEOUT_MS || 15000;
  const SALES_EMAIL= CFG.SALES_EMAIL|| "sales@sathomson.com.au";

  const $  = (s, r=document) => r.querySelector(s);
  const el = (t, c) => { const n=document.createElement(t); if(c) n.className=c; return n; };

  const btnToggle = $("#chat-toggle");
  const panel     = $("#chat-widget");
  const btnClose  = $("#close-chat");
  const inputEl   = $(".chat-input");
  const sendBtn   = $(".send-btn");
  const bodyEl    = $(".chat-body");
  const btnPdf    = $("#btn-download-pdf");
  const btnAgent  = $(".contact-agent");

  if (!btnToggle || !panel || !inputEl || !sendBtn || !bodyEl) {
    console.error("[SATN] Missing required chat elements.");
    return;
  }

  // --- transcript memory ---
  const history = [];
  function pushHistory(role, text){
    history.push({ role, text, ts: new Date().toISOString() });
  }

  // If welcome bubble exists from HTML, record it once
  (function seedInitialHistory(){
    const firstBot = bodyEl.querySelector(".bot-message p");
    if (firstBot && firstBot.textContent.trim()){
      pushHistory("assistant", firstBot.textContent.trim());
    }
  })();

  // --- UX helpers ---
  function addMsg(role, text){
    const wrap = el("div", role === "user" ? "user-message" : "bot-message");
    const p = el("p"); p.textContent = text; wrap.appendChild(p);
    const ts = el("span","timestamp"); ts.textContent = new Date().toLocaleTimeString(); wrap.appendChild(ts);
    bodyEl.appendChild(wrap);
    bodyEl.scrollTop = bodyEl.scrollHeight;
    pushHistory(role === "user" ? "user" : "assistant", text);
  }

  function setTyping(on){
    let t = $("#satn-typing");
    if (on){
      if (!t){
        t = el("div","bot-message"); t.id = "satn-typing";
        t.innerHTML = `<p><span class="dot"></span><span class="dot"></span><span class="dot"></span></p>`;
        bodyEl.appendChild(t);
      }
    } else if (t){ t.remove(); }
    bodyEl.scrollTop = bodyEl.scrollHeight;
  }

  function toast(msg){
    let area = $("#satn-toast-area");
    if (!area){ area = el("div","satn-toast-area"); area.id="satn-toast-area"; document.body.appendChild(area); }
    const n = el("div","satn-toast"); n.textContent = msg; area.appendChild(n);
    setTimeout(()=> n.remove(), 3500);
  }

  // Optional property cards if backend returns them
  function renderPropertyCards(items){
    if (!Array.isArray(items) || !items.length) return;
    const wrap = el("div","property-list chat-message");
    items.forEach(p => {
      const card = el("div","property-card");
      const img  = el("img");
      img.src = p.thumbnail || "https://images.unsplash.com/photo-1494526585095-c41746248156?q=80&w=900&auto=format&fit=crop";
      img.alt = p.title || "Property";
      const info = el("div","property-info");
      const title= el("h4"); title.textContent = p.title || "Property";
      const meta = el("p");
      const beds = p.features?.beds ?? "—";
      const baths= p.features?.baths ?? "—";
      const size = p.features?.size_sqm ? `${p.features.size_sqm} sqm` : null;
      meta.textContent = [beds && `${beds} Bed`, baths && `${baths} Bath`, size].filter(Boolean).join(" • ");
      const price= el("span","price"); price.textContent = p.price!=null ? `AUD ${Number(p.price).toLocaleString()}` : "—";
      const btn  = el("button","property-btn"); btn.textContent = "View Details";
      info.appendChild(title); info.appendChild(meta); info.appendChild(price); info.appendChild(btn);
      card.appendChild(img); card.appendChild(info); wrap.appendChild(card);
    });
    bodyEl.appendChild(wrap);
    bodyEl.scrollTop = bodyEl.scrollHeight;
  }

  // --- HTTP helpers ---
  const withTimeout = (p, ms) => Promise.race([p, new Promise((_,rej)=> setTimeout(()=> rej(new Error("Request timed out")), ms))]);

  async function fetchJSON(url, options = {}){
    const res = await withTimeout(fetch(url, { headers: { "Content-Type": "application/json" }, ...options }), TIMEOUT_MS);
    if (!res.ok){
      const tx = await res.text().catch(()=> "");
      throw new Error(tx || `HTTP ${res.status}`);
    }
    return res.json();
  }

  async function fetchPDF(url, payload){
    const res = await withTimeout(fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    }), TIMEOUT_MS);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return res.blob();
  }

  async function apiChat({ name, email, phone, message }){
    return fetchJSON(`${API_BASE}/chat`, {
      method: "POST",
      body: JSON.stringify({ name, email, phone, message })
    });
  }

  // --- Lead (localStorage until dedicated UI fields arrive) ---
  function getLead(){
    const cached = JSON.parse(localStorage.getItem("satn_lead") || "{}");
    if (cached.name && cached.email) return cached;
    const anon = { name: "Web Visitor", email: `visitor+${Date.now()}@example.com`, phone: null };
    localStorage.setItem("satn_lead", JSON.stringify(anon));
    return anon;
  }

  // --- Events: toggle & close ---
  btnToggle.addEventListener("click", () => {
    panel.classList.toggle("hidden");
    btnToggle.style.display = panel.classList.contains("hidden") ? "block" : "none";
  });
  if (btnClose){
    btnClose.addEventListener("click", () => {
      panel.classList.add("hidden"); btnToggle.style.display = "block";
    });
  }

  // --- Send message ---
  sendBtn.addEventListener("click", async () => {
    const msg = inputEl.value.trim(); if (!msg) return;
    addMsg("user", msg); inputEl.value = ""; setTyping(true);

    try {
      const lead = getLead();
      const data = await apiChat({ ...lead, message: msg });
      setTyping(false);
      addMsg("bot", data?.reply || "Thanks! Our team will follow up shortly.");
      if (Array.isArray(data?.properties) && data.properties.length) renderPropertyCards(data.properties);
    } catch (e) {
      setTyping(false); console.error(e);
      addMsg("bot", "Sorry, I couldn’t process that. Please try again."); toast("Chat failed. Please try again.");
    }
  });

  inputEl.addEventListener("keydown", (e) => {
    if (e.key === "Enter" && !e.shiftKey){ e.preventDefault(); sendBtn.click(); }
  });

  // --- Contact Agent ---
  if (btnAgent){
    btnAgent.addEventListener("click", () => {
      const lead = getLead();
      const subject = encodeURIComponent("Chatbot Lead – SA Thomson Nerys");
      const body    = encodeURIComponent(
        `Name: ${lead.name}\nEmail: ${lead.email}\nPhone: ${lead.phone ?? "-"}\n\nRecent message: ${history.slice().reverse().find(h => h.role === "user")?.text ?? "-"}`
      );
      window.location.href = `mailto:${SALES_EMAIL}?subject=${subject}&body=${body}`;
    });
  }

  // --- Download Transcript (PDF) ---
  if (btnPdf){
    btnPdf.addEventListener("click", async () => {
      try{
        const lead = getLead();
        const payload = { name: lead.name, email: lead.email, messages: history };
        const blob = await fetchPDF(`${API_BASE}/pdf/summary`, payload);  // expects application/pdf
        const url = URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url; a.download = "satn-chat-summary.pdf"; document.body.appendChild(a); a.click(); a.remove();
        URL.revokeObjectURL(url);
      }catch(e){
        console.error(e);
        toast("PDF generation failed. Please try again.");
      }
    });
  }
})();
