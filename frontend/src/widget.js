// frontend/src/widget.js
(function () {
  "use strict";

  // ---------- Config ----------
  const CFG = Object.assign(
    { API_BASE: "http://localhost:8000/api/v1", TIMEOUT_MS: 15000 },
    window.SATN_CONFIG || {}
  );

  // ---------- Helpers ----------
  const $ = (sel) => document.querySelector(sel);

  function escapeHtml(str) {
    return String(str || "")
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function formatInlineMarkdown(escaped) {
    // bold: **text**
    let s = escaped.replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>");
    // italic: *text*
    s = s.replace(/\*(.+?)\*/g, "<em>$1</em>");
    return s;
  }

  // Very simple markdown: paragraphs, bullets, numbered lists
  function renderMarkdown(text) {
    const lines = String(text || "").split(/\r?\n/);
    let html = "";
    let inUl = false;
    let inOl = false;

    const closeLists = () => {
      if (inUl) {
        html += "</ul>";
        inUl = false;
      }
      if (inOl) {
        html += "</ol>";
        inOl = false;
      }
    };

    for (const rawLine of lines) {
      const line = rawLine.trim();

      if (!line) {
        // blank → paragraph break
        closeLists();
        html += "<p></p>";
        continue;
      }

      // Bullet: "- item" or "• item"
      let m = line.match(/^[-•]\s+(.*)$/);
      if (m) {
        const content = formatInlineMarkdown(escapeHtml(m[1]));
        if (!inUl) {
          closeLists();
          html += "<ul>";
          inUl = true;
        }
        html += `<li>${content}</li>`;
        continue;
      }

      // Numbered: "1. item"
      m = line.match(/^\d+\.\s+(.*)$/);
      if (m) {
        const content = formatInlineMarkdown(escapeHtml(m[1]));
        if (!inOl) {
          closeLists();
          html += "<ol>";
          inOl = true;
        }
        html += `<li>${content}</li>`;
        continue;
      }

      // Normal paragraph
      closeLists();
      const content = formatInlineMarkdown(escapeHtml(line));
      html += `<p>${content}</p>`;
    }

    closeLists();
    return html;
  }

  // ---------- Elements ----------
  const chat = $("#chat-widget");
  const toggle = $("#chat-toggle");
  const overlay = $("#chat-overlay");
  const closeBtn = $("#close-chat");

  const input = $(".chat-input");
  const sendBtn = $(".send-btn");
  const body = $(".chat-body");

  const quickRowStatic = $(".quick-replies");

  // Dynamic quick replies row (under the static row)
  let quickRowDynamic = document.querySelector(".quick-replies-dynamic");
  if (!quickRowDynamic && quickRowStatic && quickRowStatic.parentElement) {
    quickRowDynamic = document.createElement("div");
    quickRowDynamic.className = "quick-replies quick-replies-dynamic";
    quickRowStatic.parentElement.insertBefore(
      quickRowDynamic,
      quickRowStatic.nextSibling
    );
  }

  const contactBtn =
    quickRowStatic && quickRowStatic.querySelector('[data-quick="contact"]');
  const browseBtn =
    quickRowStatic && quickRowStatic.querySelector('[data-quick="browse"]');
  const summaryBtn =
    quickRowStatic && quickRowStatic.querySelector('[data-quick="summary"]');

  // Inject PDF button into static quick row
  const dlBtn = document.createElement("button");
  dlBtn.type = "button";
  dlBtn.className = "btn btn-gold";
  dlBtn.textContent = "📄 Download PDF";
  dlBtn.title = "Download chat transcript as PDF";
  if (quickRowStatic) {
    quickRowStatic.appendChild(dlBtn);
  }

  // Bot avatar icon (match index.html)
  const brandIconUrl = "./assets/bot-icon.png";

  // ---------- Lead popup (STATIC markup in index.html) ----------
  const leadOverlayEl = $("#lead-overlay");
  const leadModalEl = $("#lead-modal");
  const leadNameEl = $("#lead-name");
  const leadEmailEl = $("#lead-email");
  const leadPhoneEl = $("#lead-phone");
  const leadSubmitBtn = $("#lead-submit");

  // ---------- State ----------
  const transcript = []; // { role: 'user' | 'assistant', text, ts }
  const MIN_MESSAGES_FOR_PDF = 3;
  let hasShownPdfUnavailable = false;
  let hasSentFirstUserMessage = false;
  let leadModalShown = false;

  let userProfile = (() => {
    try {
      return JSON.parse(localStorage.getItem("satn_user") || "{}");
    } catch {
      return {};
    }
  })();

  function saveUserProfile(up) {
    userProfile = up;
    localStorage.setItem("satn_user", JSON.stringify(up));
  }

  // ---------- Time & scroll helpers ----------
  function timeNow() {
    const d = new Date();
    return d.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
  }

  function scrollToBottom() {
    if (!body) return;
    body.scrollTo({ top: body.scrollHeight, behavior: "smooth" });
  }

  // ---------- Chat message rendering ----------
  function addMsg(role, text) {
    if (!body) return;

    const wrap = document.createElement("div");
    wrap.className =
      (role === "user" ? "user-message" : "bot-message") + " chat-message";

    if (role === "bot") {
      const row = document.createElement("div");
      row.style.display = "flex";
      row.style.gap = "8px";
      row.style.alignItems = "flex-start";

      const avatar = document.createElement("img");
      avatar.src = brandIconUrl;
      avatar.alt = "Neryx";
      avatar.className = "chat-avatar";
      row.appendChild(avatar);

      const bubble = document.createElement("div");
      bubble.className = "bot-bubble";

      const html = renderMarkdown(text);

      bubble.innerHTML = `
        <div class="bot-text">${html}</div>
        <span class="timestamp">${timeNow()}</span>
      `;
      row.appendChild(bubble);
      wrap.appendChild(row);
    } else {
      const html = renderMarkdown(text);
      wrap.innerHTML = `
        <div class="user-text">${html}</div>
        <span class="timestamp">${timeNow()}</span>
      `;
    }

    body.appendChild(wrap);
    scrollToBottom();
  }

  function addTyping() {
    if (!body) return;
    const node = document.createElement("div");
    node.className = "bot-message chat-message";
    node.dataset.typing = "1";
    node.innerHTML = `
      <div style="display:flex;gap:8px;align-items:center">
        <img src="${brandIconUrl}" class="chat-avatar" alt="Neryx" />
        <div class="typing-dots">
          <span class="dot"></span><span class="dot"></span><span class="dot"></span>
        </div>
      </div>
    `;
    body.appendChild(node);
    scrollToBottom();
  }

  function removeTyping() {
    document.querySelectorAll('[data-typing="1"]').forEach((n) => n.remove());
  }

  // ---------- Property rendering ----------
  function renderPropertyCard(p) {
    const card = document.createElement("div");
    card.className = "property-card";

    const bed = p.features?.beds ?? "—";
    const bath = p.features?.baths ?? "—";
    const park = p.features?.parking ?? 0;
    const size = p.features?.size_sqm ? `${p.features.size_sqm} sqm` : "";
    const price = p.price != null ? Number(p.price).toLocaleString() : "—";

    const imgUrl =
      p.features?.image_url || "https://placehold.co/420x240?text=Property";

    card.innerHTML = `
      <img src="${imgUrl}" alt="${escapeHtml(p.title)}" />
      <div class="property-info">
        <h4 title="${escapeHtml(p.title)}">${escapeHtml(p.title)}</h4>
        <p>${bed} bed • ${bath} bath • ${park} parking ${
      size ? "• " + size : ""
    }</p>
        <p class="location">${escapeHtml(p.location || "")}</p>
        <span class="price">$${price}</span>
        <div class="prop-actions">
          <button class="property-btn" data-id="${p.id}">View Details</button>
          ${
            p.agent
              ? `<span class="agent">Agent: ${escapeHtml(p.agent.name)}</span>`
              : ""
          }
        </div>
      </div>
    `;
    return card;
  }

  function renderSearchResults(answer, results) {
    addMsg("bot", answer);
    if (!Array.isArray(results) || !results.length || !body) return;

    const listWrap = document.createElement("div");
    listWrap.className = "chat-message property-list";
    results.forEach((p) => listWrap.appendChild(renderPropertyCard(p)));
    body.appendChild(listWrap);
    scrollToBottom();
  }

  // ---------- Dynamic quick replies ----------
  function renderDynamicQuickReplies(list) {
    if (!quickRowDynamic) return;

    quickRowDynamic.innerHTML = "";
    if (!Array.isArray(list) || !list.length) return;

    list.forEach((label) => {
      const btn = document.createElement("button");
      btn.type = "button";
      btn.className = "btn btn-outline";
      btn.textContent = label;
      btn.addEventListener("click", () => {
        input.value = label;
        input.focus();
      });
      quickRowDynamic.appendChild(btn);
    });
  }

  // ---------- Network ----------
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

    // ---------- Lead popup logic (STATIC modal) ----------
  function openLeadModal() {
    if (!leadOverlayEl || !leadModalEl) return;
    leadOverlayEl.classList.remove("hidden");
    leadModalEl.classList.remove("hidden");
    // animate in
    requestAnimationFrame(() => {
      leadModalEl.classList.add("show");
    });
  }

  function closeLeadModal() {
    if (!leadOverlayEl || !leadModalEl) return;
    leadModalEl.classList.remove("show");
    setTimeout(() => {
      leadModalEl.classList.add("hidden");
      leadOverlayEl.classList.add("hidden");
    }, 180); // match CSS transition
  }

  // ALWAYS show once per page load when chat opens
  function maybeShowLeadModal() {
    if (leadModalShown) return;
    leadModalShown = true;
    openLeadModal();
  }


  // Click on lead overlay background → close (optional)
  if (leadOverlayEl) {
    leadOverlayEl.addEventListener("click", (e) => {
      if (e.target === leadOverlayEl) {
        closeLeadModal();
      }
    });
  }

  // Handle "Continue" in lead modal
  if (leadSubmitBtn) {
    leadSubmitBtn.addEventListener("click", async () => {
      const fullName = (leadNameEl?.value || "").trim();
      const email = (leadEmailEl?.value || "").trim();
      const phone = (leadPhoneEl?.value || "").trim();

      if (!email) {
        alert("Please enter your email.");
        return;
      }

      let firstName = null;
      let lastName = null;
      if (fullName) {
        const parts = fullName.split(/\s+/, 2);
        firstName = parts[0];
        lastName = parts.length > 1 ? parts[1] : "";
      }

      // Save to local profile
      const up = { name: fullName, email, phone };
      saveUserProfile(up);

      // Send to backend /leads (matches your FastAPI lead schema)
      try {
        await postJSON("/leads", {
          first_name: firstName,
          last_name: lastName,
          email,
          phone,
          source: "chatbot"
        });
      } catch (err) {
        console.warn("Lead capture failed:", err);
      }

      closeLeadModal();
    });
  }

  // ---------- Open / Close with overlay + slide ----------
  function openChat() {
    if (!chat) return;
    chat.classList.remove("hidden");
    requestAnimationFrame(() => {
      chat.classList.add("chat-open");
    });

    if (overlay) {
      overlay.classList.remove("hidden");
      overlay.classList.add("overlay-visible");
    }
    if (toggle) toggle.style.display = "none";

    // Show lead modal as soon as chat opens, if we don't know the user yet
    maybeShowLeadModal();
  }

  function closeChat() {
    if (!chat) return;

    chat.classList.remove("chat-open");
    if (overlay) overlay.classList.remove("overlay-visible");

    setTimeout(() => {
      chat.classList.add("hidden");
      if (overlay) overlay.classList.add("hidden");
      if (toggle) toggle.style.display = "block";
    }, 220); // match CSS transition
  }

  toggle && toggle.addEventListener("click", openChat);
  closeBtn && closeBtn.addEventListener("click", closeChat);
  overlay && overlay.addEventListener("click", closeChat);

  // ---------- Conversation history payload ----------
  const MAX_HISTORY = 8;
  function buildHistoryPayload() {
    const recent = transcript.slice(-MAX_HISTORY - 1, -1);
    return recent.map((m) => ({
      role: m.role === "assistant" ? "assistant" : "user",
      content: m.text
    }));
  }

  // ---------- Chat send logic ----------
  function sendFromInput() {
    const text = (input.value || "").trim();
    if (!text) return;
    input.value = "";

    // First user message → ensure we tried to capture lead at least once
    if (!hasSentFirstUserMessage) {
      hasSentFirstUserMessage = true;
      if (!userProfile || !userProfile.email) {
        maybeShowLeadModal();
      }
    }

    transcript.push({ role: "user", text, ts: new Date().toISOString() });
    addMsg("user", text);

    const up = userProfile || { name: "", email: "", phone: "" };

    addTyping();
    const lang = "en";
    const historyPayload = buildHistoryPayload();

    postJSON("/chat", {
      text,
      lang,
      limit: 6,
      name: up.name,
      email: up.email,
      phone: up.phone,
      history: historyPayload
    })
      .then((data) => {
        removeTyping();
        const answer =
          data?.answer ||
          "I had trouble understanding that. Please try asking in a simpler way.";
        transcript.push({
          role: "assistant",
          text: answer,
          ts: new Date().toISOString()
        });

        renderSearchResults(answer, data?.results || []);
        renderDynamicQuickReplies(data?.quick_replies || []);
      })
      .catch((err) => {
        removeTyping();
        addMsg(
          "bot",
          `Sorry — the service is unavailable right now. (${String(
            err.message || err
          )})`
        );
      });
  }

  sendBtn && sendBtn.addEventListener("click", sendFromInput);
  input &&
    input.addEventListener("keydown", (e) => {
      if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault();
        sendFromInput();
      }
    });

  // ---------- Static quick actions ----------
  contactBtn &&
    contactBtn.addEventListener("click", () => {
      addMsg(
        "bot",
        "Share your preferred city, budget and timeline, and I’ll guide you on what an SA Thomson Nerys adviser would typically recommend."
      );
    });

  browseBtn &&
    browseBtn.addEventListener("click", () => {
      addMsg(
        "bot",
        'Tell me the city, budget and bedrooms (e.g. "2BR apartment in Sydney under $800k") and whether it’s for investment or to live in.'
      );
    });

  summaryBtn &&
    summaryBtn.addEventListener("click", () => {
      addMsg(
        "bot",
        'Once we’ve discussed some options, say "Summarise this for me" and I’ll give you a short investor-friendly recap.'
      );
    });

  // ---------- Download transcript as PDF ----------
  dlBtn.addEventListener("click", async () => {
    if (transcript.length < MIN_MESSAGES_FOR_PDF) {
      addMsg(
        "bot",
        "Let’s chat a bit more first. I need a short conversation before I can prepare a summary PDF."
      );
      return;
    }

    const up = userProfile || {};
    if (!up.email) {
      maybeShowLeadModal();
      addMsg(
        "bot",
        "Please share your email so we can attach this summary to your profile."
      );
      return;
    }

    try {
      const res = await fetch(`${CFG.API_BASE}/pdf/summary`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          name: up.name || "Guest",
          email: up.email,
          phone: up.phone || "",
          transcript
        })
      });

      if (!res.ok) {
        if (res.status === 404) {
          if (!hasShownPdfUnavailable) {
            hasShownPdfUnavailable = true;
            addMsg(
              "bot",
              "PDF export isn’t enabled in this demo yet. For now, you can copy or screenshot this chat, or I can create a short text summary instead."
            );
          }
          return;
        }
        const txt = await res.text().catch(() => "");
        throw new Error(`HTTP ${res.status}: ${txt}`);
      }

      const blob = await res.blob();
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = "sa-thomson-summary.pdf";
      document.body.appendChild(a);
      a.click();
      a.remove();
      URL.revokeObjectURL(url);

      addMsg(
        "bot",
        "I’ve generated a PDF summary for you. You can also share it with your adviser or mortgage broker."
      );
    } catch (err) {
      addMsg(
        "bot",
        "I couldn’t generate the PDF right now. Please try again later, or ask me for a brief text summary instead."
      );
      console.error("PDF export error:", err);
    }
  });
})();
