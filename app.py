import os
import json
from typing import List, Optional
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="JanRakshak AI - CivicShield")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure static and demo_assets folders exist and mount them
os.makedirs("static", exist_ok=True)
os.makedirs("demo_assets", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/demo_assets", StaticFiles(directory="demo_assets"), name="demo_assets")

# Structured Output Schema for Multi-Agent Response
class VerifiedScheme(BaseModel):
    scheme_name: str = Field(description="Name of the legitimate central or state government scheme")
    eligibility_bullets: List[str] = Field(description="3 simple bullet points explaining eligibility in target language")
    official_portal: str = Field(description="Official .gov.in or state government portal domain")
    safe_application_steps: List[str] = Field(description="Step-by-step safe application process in target language")

class CybercrimeReportDraft(BaseModel):
    incident_category: str = Field(description="Category e.g. UPI Fraud / Phishing / Digital Arrest Impersonation")
    suspect_identifiers: str = Field(description="Extracted phone numbers, URLs, APK names, or UPI IDs")
    incident_summary: str = Field(description="Formal summary drafted in English for official 1930 portal submission")
    immediate_checklist: List[str] = Field(description="Golden-hour actions in user's selected language")

class CivicShieldResponse(BaseModel):
    intent: str = Field(description="SCAM_CHECK | SCHEME_QUERY | EMERGENCY_REPORT")
    risk_level: str = Field(description="RED_SCAM | YELLOW_SUSPICIOUS | GREEN_SAFE")
    verdict_title: str = Field(description="Short punchy verdict in the requested target language")
    explanation: str = Field(description="Empathetic, clear explanation in the requested target language")
    red_flags: List[str] = Field(default_factory=list, description="Detected psychological manipulation or technical phishing triggers")
    verified_scheme_redirect: Optional[VerifiedScheme] = None
    cybercrime_1930_draft: Optional[CybercrimeReportDraft] = None

SYSTEM_PROMPT = """
You are JanRakshak AI (CivicShield), an elite Multi-Agent Public Safety & Citizen Service Guardian for India.
Analyze the user's text and/or uploaded image and execute three specialized sub-agents simultaneously:

1. [FORENSIC SCAM SHIELD AGENT]:
- Detect phishing URLs, malicious .apk files, fake KYC/electricity disconnection threats, UPI collect request traps, and 'Digital Arrest' police/CBI intimidation.
- Set `risk_level` to RED_SCAM, YELLOW_SUSPICIOUS, or GREEN_SAFE.
- List specific technical and psychological triggers in `red_flags` in the user's selected language.

2. [CIVIC SCHEME NAVIGATOR AGENT]:
- Scammers frequently weaponize real government welfare schemes.
- Whenever a user asks about a government scheme OR submits a scam message mentioning a subsidy/scholarship/pension, populate `verified_scheme_redirect` with the REAL scheme details (e.g., PM-Kisan, Talliki Vandanam / Jagananna Vidya Deevena, Ayushman Bharat, Post-Matric Scholarships), 3 simple eligibility bullets, and the official .gov.in or .ap.gov.in website.

3. [1930 GOLDEN-HOUR CYBER RESPONSE AGENT]:
- Whenever `risk_level` is RED_SCAM or the user reports losing money / facing extortion, populate `cybercrime_1930_draft` with a formal incident summary ready to copy-paste into cybercrime.gov.in (1930 helpline) and immediate golden-hour freezing steps.

CRITICAL LANGUAGE INSTRUCTIONS:
- Write `verdict_title`, `explanation`, `red_flags`, `eligibility_bullets`, and `immediate_checklist` naturally in the user's selected target language (English, Telugu, or Hindi).
- Keep `incident_summary` strictly in formal English so it can be pasted directly into official 1930 police and bank dispute systems.
"""

# Fallback presets for offline / zero-key testing during hackathons
DEMO_PRESETS = {
    "1": {
        "English": {
            "intent": "SCAM_CHECK",
            "risk_level": "RED_SCAM",
            "verdict_title": "🚨 Dangerous Phishing & Malware Scam Detected!",
            "explanation": "This message is a fraudulent phishing trap designed to steal banking credentials via a malicious Android APK file. No legitimate government welfare funds are disbursed via third-party WhatsApp download links.",
            "red_flags": [
                "Unverified sender on WhatsApp using official government acronyms",
                "Requests downloading an unverified .apk file (Trojan banker)",
                "Creates artificial urgency: 'Claim ₹5,000 within 24 hours'",
                "Non-governmental domain imitating official PM-Kisan portal"
            ],
            "verified_scheme_redirect": {
                "scheme_name": "Pradhan Mantri Kisan Samman Nidhi (PM-KISAN)",
                "eligibility_bullets": [
                    "Small and marginal landholding farmer families across India",
                    "Provides financial benefit of ₹6,000 per year in 3 equal four-monthly installments",
                    "Aadhaar-seeded bank account with e-KYC completed on official portal"
                ],
                "official_portal": "https://pmkisan.gov.in",
                "safe_application_steps": [
                    "Visit the official portal https://pmkisan.gov.in directly",
                    "Click on 'Farmers Corner' -> 'New Farmer Registration'",
                    "Never download APK files or share OTP / UPI PIN with anyone"
                ]
            },
            "cybercrime_1930_draft": {
                "incident_category": "Phishing / Fake Government Scheme APK Fraud",
                "suspect_identifiers": "WhatsApp Sender / Download URL: http://pmkisan-direct-claim.apk",
                "incident_summary": "Victim received unsolicited WhatsApp message impersonating PM-Kisan portal offering ₹5,000 instant credit via an APK file. Suspect URL aims to deploy mobile banking malware to siphon funds.",
                "immediate_checklist": [
                    "Do NOT install or open the downloaded APK file",
                    "If already installed, turn on Airplane mode and uninstall the app immediately",
                    "Call 1930 or submit details on cybercrime.gov.in if banking access is compromised",
                    "Report and block the sender contact on WhatsApp"
                ]
            }
        },
        "Telugu": {
            "intent": "SCAM_CHECK",
            "risk_level": "RED_SCAM",
            "verdict_title": "🚨 ప్రమాదకరమైన నకిలీ పథకం & మాల్వేర్ స్కామ్!",
            "explanation": "ఈ సందేశం పూర్తిగా మోసపూరితమైనది. ప్రభుత్వ సంక్షేమ పథకాల డబ్బులు ఎప్పుడూ వాట్సాప్‌లో APK ఫైల్స్ ద్వారా విడుదల చేయబడవు. ఇది మీ బ్యాంకు ఖాతా ఖాళీ చేయడానికి రూపొందించిన సైబర్ మోసం.",
            "red_flags": [
                "ప్రభుత్వ పథకాల పేరిట వాట్సాప్‌లో అనుమానాస్పద APK ఫైల్ లింక్",
                "24 గంటల్లో క్లెయిమ్ చేయాలని కృత్రిమ తొందరపాటు సృష్టించడం",
                "ప్రభుత్వ .gov.in డొమైన్ కాకుండా నకిలీ వెబ్‌సైట్ లింక్ ఉండటం"
            ],
            "verified_scheme_redirect": {
                "scheme_name": "ప్రధాన మంత్రి కిసాన్ సమ్మాన్ నిధి (PM-KISAN)",
                "eligibility_bullets": [
                    "భారతదేశంలోని చిన్న మరియు సన్నకారు రైతు కుటుంబాలు అర్హులు",
                    "ఏటా ₹6,000 నిధులు 3 విడతల్లో నేరుగా DBT ద్వారా జమ చేయబడతాయి",
                    "ఆధార్‌తో లింక్ అయిన బ్యాంక్ ఖాతా మరియు e-KYC పూర్తి చేయాలి"
                ],
                "official_portal": "https://pmkisan.gov.in",
                "safe_application_steps": [
                    "అధికారిక వెబ్‌సైట్ https://pmkisan.gov.in ని మాత్రమే సందర్శించండి",
                    "గ్రామ సచివాలయం లేదా రైతు సేవా కేంద్రాన్ని నేరుగా సంప్రదించండి",
                    "ఎట్టి పరిస్థితుల్లోనూ తెలియని లింక్‌లు లేదా APK ఫైల్స్ డౌన్‌లోడ్ చేయవద్దు"
                ]
            },
            "cybercrime_1930_draft": {
                "incident_category": "Phishing / Fake Government Scheme APK Fraud",
                "suspect_identifiers": "WhatsApp APK link / Fake Portal",
                "incident_summary": "Fraudulent message offering ₹5,000 PM-Kisan payout via untrusted APK download received via messaging app. Intended to harvest banking credentials.",
                "immediate_checklist": [
                    "ఆ APK ఫైల్‌ను ఇన్‌స్టాల్ చేయవద్దు లేదా వెంటనే తొలగించండి",
                    "ఒకవేళ వివరాలు లేదా డబ్బు నష్టపోతే తక్షణమే 1930 కి కాల్ చేయండి",
                    "మీ బ్యాంక్ ఖాతా నెట్ బ్యాంకింగ్ పాస్‌వర్డ్ మరియు UPI పిన్ మార్చండి"
                ]
            }
        },
        "Hindi": {
            "intent": "SCAM_CHECK",
            "risk_level": "RED_SCAM",
            "verdict_title": "🚨 खतरनाक फर्जी सरकारी योजना और एपीके घोटाला!",
            "explanation": "यह संदेश पूरी तरह फर्जी है। सरकार कभी भी व्हाट्सएप पर APK फाइल डाउनलोड करके योजना के पैसे नहीं भेजती। यह आपके बैंक खाते को खाली करने का प्रयास है।",
            "red_flags": [
                "व्हाट्सएप पर अज्ञात नंबर से एपीके डाउनलोड लिंक भेजना",
                "24 घंटे में ₹5,000 पाने की फर्जी जल्दी पैदा करना",
                "असली सरकारी .gov.in पोर्टल की जगह संदिग्ध लिंक का उपयोग"
            ],
            "verified_scheme_redirect": {
                "scheme_name": "प्रधानमंत्री किसान सम्मान निधि (PM-KISAN)",
                "eligibility_bullets": [
                    "देश के पात्र किसान परिवार",
                    "सालाना ₹6,000 की राशि 3 किस्तों में सीधे बैंक में",
                    "आधार लिंक बैंक खाता एवं आधिकारिक पोर्टल पर e-KYC अनिवार्य"
                ],
                "official_portal": "https://pmkisan.gov.in",
                "safe_application_steps": [
                    "केवल आधिकारिक वेबसाइट https://pmkisan.gov.in पर जाएं",
                    "निकटतम सीएससी (CSC) या कृषि कार्यालय से संपर्क करें",
                    "अज्ञात लिंक से कभी कोई फाइल डाउनलोड न करें"
                ]
            },
            "cybercrime_1930_draft": {
                "incident_category": "Phishing / Fake Government Scheme APK Fraud",
                "suspect_identifiers": "Malicious APK WhatsApp distribution",
                "incident_summary": "Unsolicited WhatsApp message offering instant cash subsidy via third-party APK file intended to steal banking credentials.",
                "immediate_checklist": [
                    "एपीके फाइल को कतई इंस्टॉल न करें या तुरंत अनइंस्टॉल करें",
                    "यदि वित्तीय धोखाधड़ी हुई है तो तत्काल 1930 पर कॉल करें",
                    "व्हाट्सएप पर नंबर को ब्लॉक और रिपोर्ट करें"
                ]
            }
        }
    },
    "2": {
        "English": {
            "intent": "SCHEME_QUERY",
            "risk_level": "GREEN_SAFE",
            "verdict_title": "🏛️ Verified Government Welfare Navigator",
            "explanation": "Here are the legitimate Central and Andhra Pradesh State educational support programs for students who completed 12th grade / Intermediate.",
            "red_flags": [],
            "verified_scheme_redirect": {
                "scheme_name": "Jagananna Vidya Deevena / Post-Matric Higher Education Scholarships",
                "eligibility_bullets": [
                    "Students pursuing Polytechnic, ITI, Degree, Engineering, and PG courses",
                    "Family annual income under ₹2.5 Lakh with verification via Navasakam portal",
                    "100% full fee reimbursement paid directly to verified college bank accounts"
                ],
                "official_portal": "https://jnanabhumi.ap.gov.in",
                "safe_application_steps": [
                    "Visit your nearest Village/Ward Secretariat (Grama Sachivalayam)",
                    "Submit Admission confirmation and College allotment letter",
                    "Complete Biometric / Aadhaar e-KYC on the official JnanaBhumi portal"
                ]
            },
            "cybercrime_1930_draft": None
        },
        "Telugu": {
            "intent": "SCHEME_QUERY",
            "risk_level": "GREEN_SAFE",
            "verdict_title": "🏛️ ధృవీకరించబడిన ప్రభుత్వ విద్యా పథకాల మార్గదర్శి",
            "explanation": "12వ తరగతి (ఇంటర్మీడియట్) పూర్తి చేసిన విద్యార్థుల ఉన్నత విద్య కోసం ఆంధ్రప్రదేశ్ మరియు కేంద్ర ప్రభుత్వ అధికారిక పథకాల వివరాలు ఇక్కడ ఉన్నాయి.",
            "red_flags": [],
            "verified_scheme_redirect": {
                "scheme_name": "జగనన్న విద్యా దీవెన / పోస్ట్-మెట్రిక్ స్కాలర్‌షిప్‌లు",
                "eligibility_bullets": [
                    "పాలిటెక్నిక్, ఐటీఐ, డిగ్రీ, ఇంజనీరింగ్ కోర్సులు అభ్యసించే విద్యార్థులు",
                    "కుటుంబ వార్షిక ఆదాయం ₹2.5 లక్షల లోపు ఉండాలి",
                    "పూర్తి ఫీజు రీయింబర్స్‌మెంట్ ప్రభుత్వ అధికారిక పద్ధతిలో లభిస్తుంది"
                ],
                "official_portal": "https://jnanabhumi.ap.gov.in",
                "safe_application_steps": [
                    "మీ గ్రామ/వార్డు సచివాలయంలో ఎడ్యుకేషన్ అసిస్టెంట్‌ను కలవండి",
                    "అడ్మిషన్ అలాట్‌మెంట్ లెటర్ మరియు ఆదాయ ధృవీకరణ పత్రాలు సమర్పించండి",
                    "జ్ఞానభూమి అధికారిక పోర్టల్‌లో ఈ-కేవైసీ పూర్తి చేయండి"
                ]
            },
            "cybercrime_1930_draft": None
        },
        "Hindi": {
            "intent": "SCHEME_QUERY",
            "risk_level": "GREEN_SAFE",
            "verdict_title": "🏛️ सत्यापित सरकारी छात्रवृत्ति मार्गदर्शिका",
            "explanation": "12वीं कक्षा उत्तीर्ण करने वाले विद्यार्थियों के लिए प्रामाणिक उच्च शिक्षा छात्रवृत्ति योजनाएं उपलब्ध हैं।",
            "red_flags": [],
            "verified_scheme_redirect": {
                "scheme_name": "पोस्ट-मैट्रिक उच्च शिक्षा छात्रवृत्ति / विद्या दीवेना",
                "eligibility_bullets": [
                    "डिग्री, इंजीनियरिंग या तकनीकी पाठ्यक्रम में नामांकित छात्र",
                    "परिवार की वार्षिक आय निर्धारित सीमा के अंतर्गत",
                    "सीधे कॉलेज एवं छात्र के आधार-लिंक खाते में छात्रवृत्ति का भुगतान"
                ],
                "official_portal": "https://scholarships.gov.in",
                "safe_application_steps": [
                    "राष्ट्रीय छात्रवृत्ति पोर्टल (NSP) scholarships.gov.in पर जाएं",
                    "संबंधित कॉलेज प्रवेश प्रमाण पत्र एवं मार्कशीट अपलोड करें",
                    "किसी भी बिचौलिये या अनधिकृत एजेंट को पैसे न दें"
                ]
            },
            "cybercrime_1930_draft": None
        }
    },
    "3": {
        "English": {
            "intent": "EMERGENCY_REPORT",
            "risk_level": "RED_SCAM",
            "verdict_title": "🚨 CRITICAL: 'Digital Arrest' & Police Extortion Cyber Fraud!",
            "explanation": "You have been targeted by a dangerous organized crime syndicate using fake CBI/Police video calls and intimidation ('Digital Arrest'). No police department or court conducts trials or demands UPI fund transfers via Skype or WhatsApp.",
            "red_flags": [
                "Impersonation of Police, CBI, Enforcement Directorate, or Telecom Authority",
                "Threat of 'Digital Arrest' via WhatsApp/Skype video call (No legal concept exists)",
                "Coercion to transfer money to a 'safe verification account' via UPI/RTGS",
                "Urgent demand for secrecy: 'Do not tell family or local police'"
            ],
            "verified_scheme_redirect": None,
            "cybercrime_1930_draft": {
                "incident_category": "Digital Arrest / Impersonation & Extortion via UPI",
                "suspect_identifiers": "WhatsApp/Skype ID: Fraudulent Police/CBI Caller; UPI Transaction Amount: ₹15,000",
                "incident_summary": "Victim was coerced under false pretenses of a narcotics/money laundering case via video call impersonating senior law enforcement. Under intense duress of illegal 'Digital Arrest', victim was forced to transfer ₹15,000 to suspect UPI account for 'verification'. Request immediate freeze of suspect account under Golden-Hour protocol.",
                "immediate_checklist": [
                    "CALL 1930 IMMEDIATELY: The first 2-3 hours (Golden Hour) are critical for banks to freeze the siphoned funds",
                    "Contact your bank's 24/7 fraud helpline and report the UPI Transaction Reference Number",
                    "Do NOT answer further calls or pay additional amounts under any threat",
                    "File this generated incident complaint on https://cybercrime.gov.in"
                ]
            }
        },
        "Telugu": {
            "intent": "EMERGENCY_REPORT",
            "risk_level": "RED_SCAM",
            "verdict_title": "🚨 అత్యవసర ప్రమాదం: నకిలీ 'డిజిటల్ అరెస్ట్' & UPI దోపిడీ స్కామ్!",
            "explanation": "మీరు నకిలీ సీబీఐ/పోలీస్ వీడియో కాల్ ద్వారా 'డిజిటల్ అరెస్ట్' బెదిరింపులకు గురయ్యారు. చట్టంలో డిజిటల్ అరెస్ట్ అనే భావన లేదు. పోలీసులు ఎప్పుడూ వీడియో కాల్స్‌లో విచారణ జరపరు లేదా UPI ద్వారా డబ్బులు డిమాండ్ చేయరు.",
            "red_flags": [
                "పోలీస్/CBI యూనిఫాంలో నకిలీ వీడియో కాల్ బెదిరింపు",
                "చట్టవిరుద్ధమైన 'డిజిటల్ అరెస్ట్' పేరుతో భయభ్రాంతులకు గురిచేయడం",
                "వెరిఫికేషన్ పేరుతో UPI ద్వారా డబ్బు బదిలీ చేయించడం"
            ],
            "verified_scheme_redirect": None,
            "cybercrime_1930_draft": {
                "incident_category": "Digital Arrest / Impersonation & Extortion via UPI",
                "suspect_identifiers": "Fake Police Video Call / UPI Reference",
                "incident_summary": "Extortion committed via video impersonation of law enforcement officers threatening fake criminal arrest. Victim coerced into transferring ₹15,000 via UPI. Immediate account freeze requested under 1930 helpline.",
                "immediate_checklist": [
                    "వెంటనే 1930 నంబర్‌కు కాల్ చేయండి - మొదటి 2 గంటల్లో (గోల్డెన్ అవర్) మీ డబ్బు రికవరీ అయ్యే అవకాశం ఎక్కువ",
                    "మీ బ్యాంకు హెల్ప్‌లైన్‌కు కాల్ చేసి మోసపూరిత UPI లావాదేవీని రిపోర్ట్ చేసి స్తంభింపజేయండి",
                    "ఎటువంటి పరిస్థితుల్లోనూ అదనపు డబ్బు చెల్లించవద్దు",
                    "సైబర్‌క్రైమ్ పోర్టల్ cybercrime.gov.in లో ఫిర్యాదు చేయండి"
                ]
            }
        },
        "Hindi": {
            "intent": "EMERGENCY_REPORT",
            "risk_level": "RED_SCAM",
            "verdict_title": "🚨 आपातकालीन चेतावनी: फर्जी 'डिजिटल अरेस्ट' और यूपीआई ब्लैकमेल!",
            "explanation": "यह संगठित साइबर अपराधियों द्वारा किया गया फर्जी सीबीआई/पुलिस वीडियो कॉल फ्रॉड है। भारतीय कानून में 'डिजिटल अरेस्ट' नाम की कोई चीज नहीं है। पुलिस कभी भी वीडियो कॉल पर पूछताछ या यूपीआई ट्रांसफर नहीं मांगती।",
            "red_flags": [
                "फर्जी पुलिस या सीबीआई अधिकारी बनकर वीडियो कॉल पर धमकी देना",
                "अवैध 'डिजिटल अरेस्ट' का डर दिखाकर मानसिक दबाव बनाना",
                "'सत्यापन' के नाम पर बैंक या यूपीआई खाते में तत्काल पैसे ट्रांसफर कराना"
            ],
            "verified_scheme_redirect": None,
            "cybercrime_1930_draft": {
                "incident_category": "Digital Arrest / Impersonation & Extortion via UPI",
                "suspect_identifiers": "Fake Police Video Call / UPI Transaction",
                "incident_summary": "Victim extorted of ₹15,000 under duress of fraudulent 'Digital Arrest' by suspects impersonating CBI/police officers on video call. Request urgent inter-bank lien under 1930 Golden-Hour mechanism.",
                "immediate_checklist": [
                    "तुरंत 1930 पर कॉल करें: शुरुआती 2 घंटे (गोल्डन आवर) में बैंक संदिग्ध खाते को फ्रीज कर सकते हैं",
                    "अपने बैंक के साइबर हेल्पलाइन पर तुरंत यूपीआई ट्रांजेक्शन आईडी दर्ज कराएं",
                    "डरे नहीं और किसी भी अतिरिक्त मांग को न मानें",
                    "cybercrime.gov.in पर आधिकारिक शिकायत दर्ज कराएं"
                ]
            }
        }
    }
}

@app.get("/")
async def serve_home():
    return FileResponse("static/index.html")

@app.post("/api/analyze", response_model=CivicShieldResponse)
async def analyze_input(
    text_input: str = Form(""),
    language: str = Form("English"),
    api_key: str = Form(""),
    demo_id: Optional[str] = Form(None),
    image: Optional[UploadFile] = File(None)
):
    selected_lang = language if language in ["English", "Telugu", "Hindi"] else "English"
    
    # Check if a demo preset is requested and no API key is provided
    final_key = api_key.strip() or os.getenv("GEMINI_API_KEY", "")
    
    if demo_id and demo_id in DEMO_PRESETS and not final_key:
        return DEMO_PRESETS[demo_id][selected_lang]
        
    if not final_key:
        # If neither key nor valid demo, check if text matches one of demo presets
        for key_id, scenarios in DEMO_PRESETS.items():
            if (key_id == "1" and ("pmkisan" in text_input.lower() or "vidya deevena" in text_input.lower() or "5,000" in text_input.lower())) or \
               (key_id == "2" and ("daughter" in text_input.lower() or "scholarship" in text_input.lower() or "12th" in text_input.lower())) or \
               (key_id == "3" and ("police" in text_input.lower() or "cbi" in text_input.lower() or "digital arrest" in text_input.lower() or "15,000" in text_input.lower())):
                return scenarios[selected_lang]
        raise HTTPException(
            status_code=400,
            detail="Gemini API Key is required. Please paste it into the top bar or set GEMINI_API_KEY in your .env file."
        )

    try:
        from google import genai
        from google.genai import types
        
        client = genai.Client(api_key=final_key)
        contents = []

        if image and image.filename:
            img_bytes = await image.read()
            contents.append(
                types.Part.from_bytes(
                    data=img_bytes,
                    mime_type=image.content_type or "image/jpeg"
                )
            )

        prompt_text = (
            f"Target Response Language: {selected_lang}\n"
            f"User Input / Context: {text_input or 'Analyze the uploaded image for scams, digital hazards, or government scheme information.'}"
        )
        contents.append(prompt_text)

        # Candidate models to try with the official google-genai SDK
        candidate_models = ["gemini-2.5-flash", "gemini-2.0-flash", "gemini-1.5-flash", "gemini-3.8-flash"]
        last_error = None

        for model_name in candidate_models:
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=contents,
                    config=types.GenerateContentConfig(
                        system_instruction=SYSTEM_PROMPT,
                        response_mime_type="application/json",
                        response_schema=CivicShieldResponse,
                        temperature=0.2,
                    ),
                )
                if response.text:
                    parsed_json = json.loads(response.text)
                    return parsed_json
            except Exception as ex:
                last_error = ex
                continue

        # If models failed, raise the error
        raise HTTPException(status_code=500, detail=f"Gemini API Error: {str(last_error)}")

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent Error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
