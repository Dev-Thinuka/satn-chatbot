# 🏡 SA Thomson Nerys Real-Estate AI Chatbot System

### 💬 Intelligent, Multilingual Property Assistant for sathomson.com.au

> A self-contained, multilingual AI chatbot that helps users explore property listings, connect with agents, and receive tailored investment insights — all within a modern, embeddable web widget.

---

## 🌐 Project Overview

The **SA Thomson Nerys AI Chatbot** is a secure, multilingual conversational assistant built to enhance client engagement across **English**, **Sinhala**, and **Tamil**.

It operates as an independent, plug-and-play module that can be embedded into any website using a single `<script>` tag.

### 🎯 Core Objectives
- Retrieve **property listings**, **agent details**, and **company information**
- Support **English / Sinhala / Tamil**
- Collect **user contact details** (email & phone)
- Automatically **notify sales teams** via email
- **Email PDF summary** of chat + property info to user
- Integrate securely via **FastAPI middleware + vector search**
- Ready for **multi-tenant white-labeling**

---

## 🧠 System Architecture

```mermaid
graph TD
  A[Website User 🌐] -->|Chat Widget| B[FastAPI Middleware]
  B --> C[Language Layer (langdetect / Google Translate)]
  B --> D[PostgreSQL DB]
  B --> E[Vector DB (Pinecone / Weaviate)]
  B --> F[LLM (OpenAI GPT-4 / Gemini)]
  B --> G[Notification Service (SMTP / SendGrid)]
  B --> H[PDF Generator (ReportLab)]
  I[WordPress / CRM] -->|ETL Sync| D


🧩 Data Flow Summary

1️⃣ User opens chat → enters email + phone
2️⃣ FastAPI stores user in PostgreSQL
3️⃣ Notification email sent to sales@sathomson.com.au

4️⃣ Query translated → embedded → context retrieved
5️⃣ Response generated via GPT-4/Gemini
6️⃣ Interaction logged + optional PDF summary emailed

🔒 Security & Compliance

HTTPS enforced

JWT/OAuth2 for API access

Encrypted storage of PII

Compliance with Australian Privacy Principles (APPs)

Isolated frontend (no direct DB calls)

🧭 Future Roadmap

🧱 Admin Dashboard for Analytics & Lead Management

🌐 White-Label Tenant Support

🗣️ Voice Chat Integration

📊 Chat Insights Dashboard

🔄 Retrainable Embeddings per Client

📱 Responsive UI Enhancements

🧑‍💻 Maintainer

Thinuka [AI Engineer @ SA Thomson Nerys]
📧 thinuka@sathomson.com.au

🌏 https://sathomson.com.au

🏁 License

© 2025 S A Thomson Nerys & Co. Pty. Ltd.
All rights reserved. Unauthorized redistribution is prohibited.