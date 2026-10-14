# JanRakshak AI (CivicShield) 🛡️
### *The Multilingual AI Guardian for Verified Public Services & Cyber Safety*
*Built with Google Antigravity & the Official Google GenAI SDK for PromptWars*

---

## 🌟 Overview
**JanRakshak AI** addresses two critical, neglected societal challenges in digital India:
1. **The Scheme Literacy Gap**: Millions miss out on genuine government welfare benefits (PM-Kisan, Vidya Deevena, scholarships) due to bureaucratic jargon and confusing portals.
2. **Community Cyber Fraud & Digital Harassment**: Scammers exploit this gap with fake welfare APKs, electricity bill threats, and "Digital Arrest" extortion via WhatsApp and video calls.

JanRakshak AI combines **Forensic Scam Detection**, **Genuine Public Service Redirection**, and **Golden-Hour Cybercrime Reporting (1930)** into a unified, multilingual, voice-first platform.

---

## 🏗️ Architecture & Multi-Agent Design

```
                     ┌────────────────────────────────────────┐
                     │ Citizen Input (Voice / Text / Image)   │
                     └───────────────────┬────────────────────┘
                                         ▼
                     ┌────────────────────────────────────────┐
                     │      FastAPI Multi-Agent Router        │
                     │          (google-genai SDK)            │
                     └───────────────────┬────────────────────┘
                                         │
        ┌────────────────────────────────┼────────────────────────────────┐
        ▼                                ▼                                ▼
┌──────────────────────┐      ┌──────────────────────┐      ┌──────────────────────┐
│  Forensic Scam       │      │ Civic Scheme         │      │ 1930 Golden-Hour     │
│  Shield Agent        │      │ Navigator Agent      │      │ Emergency Response   │
│                      │      │                      │      │                      │
│ - Detects APK traps  │      │ - Identifies real    │      │ - Extracts suspect   │
│ - Psychological cues │      │   schemes            │      │   identifiers        │
│ - Traffic Light      │      │ - 3 simple bullets   │      │ - Pre-drafts 1930    │
│   Risk Verdict       │      │ - Official .gov.in   │      │   formal incident    │
└──────────────────────┘      └──────────────────────┘      └──────────────────────┘
```

---

## 🚀 Quick Start

### 1. Start Server
Run the startup script:
```powershell
.\run.bat
```
Or directly using the virtual environment:
```powershell
.venv\Scripts\python.exe -m uvicorn app:app --reload --host 127.0.0.1 --port 8000
```

### 2. Access the Application
Open your browser and visit:
[http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## ⚡ Hackathon Live Demo Scenarios

The UI includes **3 One-Click Demo Buttons** ready for presentation:
1. **Demo 1: Fake Welfare APK Scam**
   - *Input:* WhatsApp message offering ₹5,000 via a suspicious `.apk` file.
   - *Result:* 🚨 Red Scam alert + Red flags breakdown + Safe redirect to real PM-Kisan portal.
2. **Demo 2: Citizen Scheme Eligibility Navigator**
   - *Input:* 12th-grade student family asking about higher education funding in AP.
   - *Result:* 🏛️ Green Verified Navigator + 3 simple eligibility points for Vidya Deevena & JnanaBhumi.
3. **Demo 3: "Digital Arrest" & UPI Extortion Emergency**
   - *Input:* Panic report of fake police/CBI video call extorting ₹15,000.
   - *Result:* 🚓 Critical Fraud Alert + Formal English 1930 complaint draft + Golden-Hour account freeze checklist.

---

## 🌐 Multilingual & Multimodal Features
- **Supported Languages:** English, తెలుగు (Telugu), हिन्दी (Hindi).
- **Voice-to-Text:** Live speech input via Web Speech API in all 3 languages.
- **Audio Output:** Text-to-Speech playback of verdicts in local languages.
- **Screenshot / Vision:** Upload dubious SMS screenshots or circulars for multimodal inspection.
