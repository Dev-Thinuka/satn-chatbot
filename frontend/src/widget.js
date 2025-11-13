// frontend/src/widget.js
(function () {
  const CFG = Object.assign(
    { API_BASE: "http://localhost:8000/api/v1", TIMEOUT_MS: 15000 },
    window.SATN_CONFIG || {}
  );

  // ---- Elements ----
  const $ = (sel) => document.querySelector(sel);
  const chat = $("#chat-widget");
  const toggle = $("#chat-toggle");
  const closeBtn = $("#close-chat");
  const input = document.querySelector(".chat-input");
  const sendBtn = document.querySelector(".send-btn");
  const body = document.querySelector(".chat-body");
  const langSel = $("#lang-select");
  const callBtn = document.querySelector('.quick-replies button'); // existing "Contact an Agent"
  // Add a Download PDF button next to call button
  const qr = document.querySelector(".quick-replies");
  const dlBtn = document.createElement("button");
  dlBtn.textContent = "⬇️ Download PDF";
  dlBtn.title = "Download chat transcript as PDF";
  qr.appendChild(dlBtn);

  // Bot avatar icon (from user-provided asset)
  const brandIconUrl = "boticon.png"; // place file in same public folder

  // ---- State ----
  const transcript = []; // {role:'user'|'assistant', text, ts}
  const userProfile = (() => {
    try { return JSON.parse(localStorage.getItem("satn_user") || "{}"); } catch { return {}; }
  })();

  // ---- UI helpers ----
  function addMsg(role, text, opts = {}) {
    const wrap = document.createElement("div");
    wrap.className = role === "user" ? "user-message" : "bot-message";

    // Optional avatar for bot
    if (role === "bot") {
      const row = document.createElement("div");
      row.style.display = "flex";
      row.style.gap = "8px";
      row.style.alignItems = "flex-start";

      const avatar = document.createElement("img");
      avatar.src = brandIconUrl;
      avatar.alt = "Kalani";
      avatar.className = "chat-avatar";
      row.appendChild(avatar);

      const bubble = document.createElement("div");
      bubble.innerHTML = `<p>${text}</p><span class="timestamp">${timeNow()}</span>`;
      row.appendChild(bubble);
      wrap.appendChild(row);
    } else {
      wrap.innerHTML = `<p>${text}</p><span class="timestamp">${timeNow()}</span>`;
    }

    body.appendChild(wrap);
    body.scrollTop = body.scrollHeight;
  }

  function addTyping() {
    const node = document.createElement("div");
    node.className = "bot-message typing";
    node.dataset.typing = "1";
    node.innerHTML = `
      <div style="display:flex;gap:8px;align-items:center">
        <img src="${brandIconUrl}" class="chat-avatar" alt="Kalani" />
        <div class="typing-dots"><span></span><span></span><span></span></div>
      </div>
    `;
    body.appendChild(node);
    body.scrollTop = body.scrollHeight;
  }

  function removeTyping() {
    document.querySelectorAll('[data-typing="1"]').forEach((n) => n.remove());
  }

  function timeNow() {
    const d = new Date();
    return d.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
  }

  function ensureUserProfile() {
    if (userProfile && userProfile.email) return userProfile;
    // MVP inline prompts
    const name = prompt("Your name (optional):") || "";
    const email = prompt("Your email (required for PDF/email):") || "";
    const phone = prompt("Phone (optional):") || "";
    const up = { name, email, phone };
    localStorage.setItem("satn_user", JSON.stringify(up));
    return up;
  }

  function renderPropertyCard(p) {
    const card = document.createElement("div");
    card.className = "property-card";

    const bed = p.features?.beds ?? "—";
    const bath = p.features?.baths ?? "—";
    const park = p.features?.parking ?? 0;
    const size = p.features?.size_sqm ? `${p.features.size_sqm} sqm` : "";
    const price = (p.price != null) ? (Number(p.price).toLocaleString()) : "—";

    // simple placeholder image if none
    const imgUrl = p.features?.image_url || "https://placehold.co/420x240?text=Property";

    card.innerHTML = `
      <img src="${imgUrl}" alt="${p.title}" />
      <div class="property-info">
        <h4 title="${p.title}">${p.title}</h4>
        <p>${bed} bed • ${bath} bath • ${park} parking ${size ? "• " + size : ""}</p>
        <p class="location">${p.location || ""}</p>
        <span class="price">$${price}</span>
        <div class="prop-actions">
          <button class="property-btn" data-id="${p.id}">View Details</button>
          ${p.agent ? `<span class="agent">Agent: ${p.agent.name}</span>` : ""}
        </div>
      </div>
    `;
    return card;
  }

  function renderSearchResults(answer, results) {
    addMsg("bot", answer);
    if (!Array.isArray(results) || !results.length) return;

    const listWrap = document.createElement("div");
    listWrap.className = "chat-message property-list";
    results.forEach((p) => listWrap.appendChild(renderPropertyCard(p)));
    body.appendChild(listWrap);
    body.scrollTop = body.scrollHeight;
  }

  // ---- Network ----
  async function postJSON(path, payload) {
    const ctrl = new AbortController();
    const t = setTimeout(() => ctrl.abort(), CFG.TIMEOUT_MS);
    try {
      const res = await fetch(`${CFG.API_BASE}${path}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
        signal: ctrl.signal
      });
      if (!res.ok) {
        const txt = await res.text().catch(() => "");
        throw new Error(`HTTP ${res.status}: ${txt}`);
      }
      const ct = res.headers.get("content-type") || "";
      if (ct.includes("application/json")) {
        return await res.json();
      }
      return await res.text();
    } finally {
      clearTimeout(t);
    }
  }

  // ---- Events ----
  toggle?.addEventListener("click", () => {
    chat?.classList.toggle("hidden");
    toggle.style.display = chat.classList.contains("hidden") ? "block" : "none";
  });
  closeBtn?.addEventListener("click", () => {
    chat?.classList.add("hidden");
    toggle.style.display = "block";
  });

  function sendFromInput() {
    const text = (input.value || "").trim();
    if (!text) return;
    input.value = "";

    // record & render user message
    transcript.push({ role: "user", text, ts: new Date().toISOString() });
    addMsg("user", text);

    // make sure we have user profile once
    const up = ensureUserProfile();

    // call chat API
    addTyping();
    const lang = (langSel?.value || "English");
    postJSON("/chat", {
      text,
      lang: lang.startsWith("සිං") ? "si" : lang.startsWith("த") ? "ta" : "en",
      limit: 6,
      name: up.name, email: up.email, phone: up.phone
    })
      .then((data) => {
        removeTyping();
        const answer = data?.answer || "I had trouble understanding that.";
        transcript.push({ role: "assistant", text: answer, ts: new Date().toISOString() });
        renderSearchResults(answer, data?.results || []);
      })
      .catch((err) => {
        removeTyping();
        addMsg("bot", `Sorry — the service is unavailable right now. (${String(err.message || err)})`);
      });
  }

  sendBtn?.addEventListener("click", sendFromInput);
  input?.addEventListener("keydown", (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendFromInput();
    }
  });

  // “Contact an Agent” (kept as is; you can wire later)
  callBtn?.addEventListener("click", () => {
    addMsg("bot", "An agent will reach out to you shortly. (This is a placeholder — hook to /lead soon.)");
  });

  // Download transcript as PDF via /api/v1/pdf/summary
  dlBtn.addEventListener("click", async () => {
    if (!transcript.length) {
      addMsg("bot", "No conversation to export yet. Ask something first 🙂");
      return;
    }
    const up = ensureUserProfile();
    try {
      const resp = await fetch(`${CFG.API_BASE}/pdf/summary`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          name: up.name || "Guest",
          email: up.email || "user@example.com",
          messages: transcript
        })
      });
      if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
      const blob = await resp.blob();
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `SATN-Chat-${new Date().toISOString().slice(0, 10)}.pdf`;
      document.body.appendChild(a);
      a.click();
      a.remove();
      URL.revokeObjectURL(url);
    } catch (e) {
      addMsg("bot", "Couldn’t generate the PDF right now.");
    }
  });

  // First-render greeting (keep your existing seed DOM as you like)
  if (!chat.classList.contains("hidden")) {
    addMsg("bot", "👋 Hello! I’m Kalani from SA Thomson Nerys. How can I help you today?");
  }
})();
