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
class SolutionPathway(BaseModel):
    title: str = Field(description="Title of the solution method (e.g. Device Quarantine, Official CSC / Sachivalayam Verification, RBI Banking Chargeback, Cyber Police Helpline)")
    action_type: str = Field(description="IMMEDIATE_ACTION | OFFICIAL_PORTAL | FINANCIAL_RECOVERY | LEGAL_POLICE")
    step_by_step: List[str] = Field(description="Detailed step-by-step instructions to execute this solution in target language")
    contact_or_link: str = Field(description="Official helpline number, website URL, or department office")

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
    explanation: str = Field(description="Deep, comprehensive, multi-paragraph educational explanation covering technical mechanics, legal reality, citizen rights, and psychological urgency traps in target language")
    red_flags: List[str] = Field(default_factory=list, description="Detected psychological manipulation or technical phishing triggers")
    solution_pathways: List[SolutionPathway] = Field(default_factory=list, description="All possible concrete ways to solve and handle this problem")
    verified_scheme_redirect: Optional[VerifiedScheme] = None
    cybercrime_1930_draft: Optional[CybercrimeReportDraft] = None

SYSTEM_PROMPT = """
You are JanRakshak AI (CivicShield), an elite Multi-Agent Public Safety & Citizen Service Guardian for India.
Analyze the user's text and/or uploaded image and execute three specialized sub-agents simultaneously.

IN-DEPTH EXPLANATION REQUIREMENT:
- Provide a rich, thorough, multi-paragraph explanation in `explanation`.
- Explain EXACTLY how this scam works technically (e.g. Android trojan overlays, SMS harvesting, spoofed caller IDs, fake FIR intimidations), why the claim is legally or administratively impossible (e.g. no court trials via WhatsApp, no power disconnection without 15-day notice under Electricity Act 2003, no direct cash schemes through APKs), and how citizens can protect their rights.

ALL POSSIBLE WAYS TO SOLVE THE PROBLEM (`solution_pathways`):
Provide 3 to 4 distinct, concrete solution pathways in `solution_pathways`:
1. IMMEDIATE ACTION / CONTAINMENT: What the user must do right this second (e.g. Airplane mode, app deletion, WhatsApp reporting, blocking sender).
2. OFFICIAL VERIFICATION PATHWAY: Where to go or call to verify the legitimate status (e.g. Grama/Ward Sachivalayam, CSC Center, Official State/Central Portal, Electricity Board Sub-division office).
3. FINANCIAL & BANKING RECOVERY: If money was touched or credentials shared, exact steps under RBI's Limited Liability Circular (Calling 1930, contacting bank nodal officer within 3 days for zero-liability protection, freezing UPI handle).
4. LEGAL & STATUTORY GRIEVANCE: Filing complaints on cybercrime.gov.in, National Consumer Helpline (1915), or state electricity ombudsman.

CRITICAL LANGUAGE INSTRUCTIONS:
- Write `verdict_title`, `explanation`, `red_flags`, `eligibility_bullets`, `immediate_checklist`, and all `solution_pathways` naturally and authoritatively in the user's selected target language (English, Telugu, or Hindi).
- Keep `incident_summary` inside `cybercrime_1930_draft` strictly in formal English so it can be pasted directly into official police and bank systems.
"""

# Rich Fallback presets for offline / zero-key testing during hackathons
DEMO_PRESETS = {
    "1": {
        "English": {
            "intent": "SCAM_CHECK",
            "risk_level": "RED_SCAM",
            "verdict_title": "🚨 Dangerous Phishing & Trojan Malware Attack Detected!",
            "explanation": "This message is a malicious phishing campaign deploying banking trojan malware disguised as the official PM-Kisan government app. Cybercriminals use fraudulent WhatsApp forwards promising instant ₹5,000 welfare disbursements to trick beneficiaries into downloading an untrusted '.apk' installation package.\n\nOnce installed on an Android device, this malware requests intrusive accessibility and SMS permissions. It intercepts two-factor authentication OTPs from your bank, reads your UPI notification tokens, and silently siphons funds while overlaying fake screens. Under Government of India Direct Benefit Transfer (DBT) guidelines, legitimate welfare subsidies are NEVER distributed via standalone APK links sent on WhatsApp; they are deposited directly into your Aadhaar-seeded bank account (NPCI mapper) without requiring third-party app installations.",
            "red_flags": [
                "Unsolicited WhatsApp forward from an unverified personal number (+91)",
                "Requests downloading an external .apk file bypassing the Google Play Store (Trojan banker payload)",
                "Artificial urgency tactic: 'Must claim within 24 hours or subsidy expires'",
                "Unofficial, spoofed domain name attempting to mimic official government portals",
                "Promises cash hand-outs directly via app install, violating official DBT protocols"
            ],
            "solution_pathways": [
                {
                    "title": "Immediate Device Containment & Malware Quarantine",
                    "action_type": "IMMEDIATE_ACTION",
                    "step_by_step": [
                        "Do NOT click the link, and do NOT install the APK package.",
                        "If you already downloaded it, do NOT open it: immediately delete the file from your 'Downloads' folder.",
                        "If installed, immediately switch on Airplane Mode to sever command-and-control server connection, then navigate to Settings > Apps > Uninstall.",
                        "Block and report the sender contact directly within WhatsApp."
                    ],
                    "contact_or_link": "Device Settings > Apps > Uninstall Unknown Apps"
                },
                {
                    "title": "Legitimate Government Verification Pathway",
                    "action_type": "OFFICIAL_PORTAL",
                    "step_by_step": [
                        "Check your genuine PM-Kisan status only on the verified portal: https://pmkisan.gov.in.",
                        "Click 'Know Your Status' and enter your Registration Number or Aadhaar Number.",
                        "Alternatively, visit your nearest Grama / Ward Sachivalayam (Village Secretariat) or Common Service Centre (CSC) to inspect the beneficiary list in person."
                    ],
                    "contact_or_link": "Official Helpline: 155261 / 011-24300606 (pmkisan.gov.in)"
                },
                {
                    "title": "Financial Account Safeguarding & RBI Protection",
                    "action_type": "FINANCIAL_RECOVERY",
                    "step_by_step": [
                        "If you entered UPI PIN, ATM card details, or internet banking passwords, call your bank's 24/7 fraud helpline immediately.",
                        "Request a temporary freeze on your UPI services and net banking transactions.",
                        "Change your UPI MPIN and net banking passwords from a separate, uninfected device.",
                        "Under RBI Circular DBR.No.Leg.BC.78/09.07.005/2017-18, reporting unauthorized transactions within 3 working days grants zero-liability protection."
                    ],
                    "contact_or_link": "Bank Customer Care (Back of ATM Card) or National Cyber Helpline: 1930"
                },
                {
                    "title": "National Cybercrime & CERT-In Reporting",
                    "action_type": "LEGAL_POLICE",
                    "step_by_step": [
                        "Report the phishing link and APK URL to the Indian Computer Emergency Response Team (CERT-In) at incident@cert-in.org.in to get the malicious domain taken down.",
                        "File an online complaint on the National Cyber Crime Portal (https://cybercrime.gov.in) under the 'Financial Fraud / Phishing' category."
                    ],
                    "contact_or_link": "Helpline: 1930 / Website: https://cybercrime.gov.in"
                }
            ],
            "verified_scheme_redirect": {
                "scheme_name": "Pradhan Mantri Kisan Samman Nidhi (PM-KISAN)",
                "eligibility_bullets": [
                    "All small and marginal landholding farmer families with cultivable land holdings",
                    "Direct financial benefit of ₹6,000 per year transferred in 3 equal installments of ₹2,000 each",
                    "Mandatory Aadhaar-seeding of bank account with e-KYC completed on the official portal"
                ],
                "official_portal": "https://pmkisan.gov.in",
                "safe_application_steps": [
                    "Visit official portal https://pmkisan.gov.in (look for the .gov.in domain)",
                    "Navigate to 'Farmers Corner' -> click 'New Farmer Registration'",
                    "Enter Aadhaar number, state, and land record details (Khata/Survey numbers)",
                    "Never pay fees or download third-party applications; enrollment is completely free at your local agriculture office"
                ]
            },
            "cybercrime_1930_draft": {
                "incident_category": "Phishing / Mobile Banking Trojan APK Distribution",
                "suspect_identifiers": "WhatsApp Sender: +91-98765-43210; Malicious URL: http://pmkisan-direct-claim.apk",
                "incident_summary": "Complainant was targeted via unsolicited WhatsApp message imitating the official Government of India PM-Kisan welfare portal. The message promised instant credit of Rs 5,000 upon downloading an unverified Android APK package. The payload is designed to harvest banking OTPs and UPI tokens. Suspect URL requested for domain suspension and blocking under IT Act Section 69A.",
                "immediate_checklist": [
                    "Do NOT install or open the APK file under any circumstances",
                    "Turn on Airplane Mode immediately if the app was opened, then uninstall",
                    "Change bank net-banking passwords and UPI MPIN from an alternate phone",
                    "Dial 1930 immediately if any unauthorized fund transfer has taken place"
                ]
            }
        },
        "Telugu": {
            "intent": "SCAM_CHECK",
            "risk_level": "RED_SCAM",
            "verdict_title": "🚨 ప్రమాదకరమైన నకిలీ పథకం & బ్యాంకింగ్ మాల్వేర్ దాడి!",
            "explanation": "ఈ సందేశం పూర్తిగా మోసపూరితమైన సైబర్ దాడి. ప్రధాన మంత్రి కిసాన్ లేదా విద్యా దీవెన పేరుతో వాట్సాప్‌లో వచ్చే APK ఫైల్స్ ద్వారా ప్రజల బ్యాంక్ ఖాతాలను దోచుకోవడానికి సైబర్ నేరగాళ్లు రూపొందించిన పన్నాగం ఇది.\n\nమీరు ఈ APK ఫైల్‌ను ఫోన్‌లో ఇన్‌స్టాల్ చేస్తే, అది మీ ఎస్ఎంఎస్ (SMS) మరియు యాక్సెసిబిలిటీ అనుమతులను దొంగిలిస్తుంది. మీ బ్యాంక్ నుండి వచ్చే ఓటీపీలను (OTP), యూపీఐ పిన్‌లను తస్కరించి క్షణాల్లో మీ ఖాతాలోని డబ్బును ఖాళీ చేస్తుంది. భారత ప్రభుత్వ ప్రత్యక్ష నగదు బదిలీ (DBT) నిబంధనల ప్రకారం, ఏ ప్రభుత్వ సంక్షేమ నిధులు కూడా వాట్సాప్‌లో APK ఫైల్స్ ద్వారా విడుదల చేయబడవు; నిధులు నేరుగా మీ ఆధార్ లింక్ అయిన బ్యాంక్ ఖాతాలో మాత్రమే జమ అవుతాయి.",
            "red_flags": [
                "అపరిచిత నంబర్ నుండి వాట్సాప్‌లో వచ్చిన సందేశం",
                "గూగుల్ ప్లేస్టోర్ కాకుండా బయటి లింక్ నుండి .apk ఫైల్ డౌన్‌లోడ్ చేయమని కోరడం",
                "24 గంటల్లో క్లెయిమ్ చేయకపోతే రద్దవుతుందనే కృత్రిమ భయాన్ని సృష్టించడం",
                "ప్రభుత్వ అధికారిక .gov.in డొమైన్ కాకుండా నకిలీ వెబ్‌సైట్ లింక్ ఉండటం"
            ],
            "solution_pathways": [
                {
                    "title": "తక్షణ ఫోన్ రక్షణ & మాల్వేర్ తొలగింపు",
                    "action_type": "IMMEDIATE_ACTION",
                    "step_by_step": [
                        "ఆ లింక్‌ను ఎట్టి పరిస్థితుల్లోనూ క్లిక్ చేయవద్దు, APK ఫైల్‌ను డౌన్‌లోడ్ చేయవద్దు.",
                        "ఒకవేళ డౌన్‌లోడ్ అయి ఉంటే, ఫైల్ మేనేజర్‌లోని 'Downloads' ఫోల్డర్‌కు వెళ్లి వెంటనే డిలీట్ చేయండి.",
                        "ఇన్‌స్టాల్ చేసి ఉంటే, వెంటనే ఫోన్‌ను 'Airplane Mode' లో ఉంచి Settings > Apps లోకి వెళ్లి ఆ యాప్‌ను అన్‌ఇన్‌స్టాల్ చేయండి.",
                        "వాట్సాప్‌లో ఆ నంబర్‌ను బ్లాక్ చేసి రిపోర్ట్ చేయండి."
                    ],
                    "contact_or_link": "Settings > Apps > Uninstall"
                },
                {
                    "title": "అధికారిక ప్రభుత్వ ధృవీకరణ మార్గం",
                    "action_type": "OFFICIAL_PORTAL",
                    "step_by_step": [
                        "మీ PM-కిసాన్ స్టేటస్‌ను కేవలం అధికారిక వెబ్‌సైట్ https://pmkisan.gov.in లో మాత్రమే తనిఖీ చేయండి.",
                        "మీ సమీప గ్రామ/వార్డు సచివాలయంలో వ్యవసాయ సహాయకుడిని (Agriculture Assistant) లేదా డిజిటల్ అసిస్టెంట్‌ను కలవండి.",
                        "పథకం అర్హుల జాబితాను సచివాలయ నోటీస్ బోర్డులో ఉచితంగా ధృవీకరించుకోవచ్చు."
                    ],
                    "contact_or_link": "టోల్‌ఫ్రీ హెల్ప్‌లైన్: 155261 / 1800-180-1551"
                },
                {
                    "title": "బ్యాంకు ఖాతా రక్షణ & ఆర్బీఐ నియమాలు",
                    "action_type": "FINANCIAL_RECOVERY",
                    "step_by_step": [
                        "ఒకవేళ మీరు బ్యాంక్ వివరాలు లేదా యూపీఐ పిన్ నమోదు చేసి ఉంటే, వెంటనే మీ బ్యాంక్ కస్టమర్ కేర్‌కు కాల్ చేసి యూపీఐని బ్లాక్ చేయించండి.",
                        "మీ నెట్ బ్యాంకింగ్ పాస్‌వర్డ్ మరియు యూపీఐ పిన్‌ను వేరే ఫోన్ నుండి మార్చండి.",
                        "ఆర్బీఐ నిబంధనల ప్రకారం మోసపూరిత లావాదేవీ జరిగిన 3 రోజుల్లోపు బ్యాంకుకు సమాచారం ఇస్తే వినియోగదారుడికి పూర్తి రక్షణ లభిస్తుంది."
                    ],
                    "contact_or_link": "జాతీయ సైబర్ హెల్ప్‌లైన్: 1930 / మీ బ్యాంక్ హెల్ప్‌లైన్"
                },
                {
                    "title": "సైబర్ క్రైమ్ పోలీసులకు ఫిర్యాదు",
                    "action_type": "LEGAL_POLICE",
                    "step_by_step": [
                        "వెంటనే 1930 నంబర్‌కు కాల్ చేసి మోసపూరిత APK లింక్ మరియు వాట్సాప్ నంబర్‌ను నమోదు చేయించండి.",
                        "cybercrime.gov.in పోర్టల్‌లో ఈ వివరాలతో ఆన్‌లైన్ ఫిర్యాదును నమోదు చేయండి."
                    ],
                    "contact_or_link": "హెల్ప్‌లైన్: 1930 / https://cybercrime.gov.in"
                }
            ],
            "verified_scheme_redirect": {
                "scheme_name": "ప్రధాన మంత్రి కిసాన్ సమ్మాన్ నిధి (PM-KISAN)",
                "eligibility_bullets": [
                    "భారతదేశంలోని సాగుభూమి కలిగిన చిన్న మరియు సన్నకారు రైతు కుటుంబాలు",
                    "ఏటా ₹6,000 ఆర్థిక సాయం, మూడు విడతల్లో ₹2,000 చొప్పున నేరుగా ఖాతాలో జమ",
                    "ఆధార్ సీడింగ్ అయిన బ్యాంక్ ఖాతా మరియు అధికారిక పోర్టల్‌లో ఈ-కేవైసీ తప్పనిసరి"
                ],
                "official_portal": "https://pmkisan.gov.in",
                "safe_application_steps": [
                    "అధికారిక వెబ్‌సైట్ https://pmkisan.gov.in ని మాత్రమే సందర్శించండి",
                    "'Farmers Corner' లో 'New Farmer Registration' పై క్లిక్ చేయండి",
                    "మీ ఆధార్ నంబర్, భూమి పట్టాదారు పాస్‌బుక్ వివరాలు నమోదు చేయండి",
                    "ఎటువంటి మధ్యవర్తులకు రుసుము చెల్లించాల్సిన అవసరం లేదు; సచివాలయంలో ఉచితంగా దరఖాస్తు చేసుకోవచ్చు"
                ]
            },
            "cybercrime_1930_draft": {
                "incident_category": "Phishing / Fake Government Scheme APK Fraud",
                "suspect_identifiers": "WhatsApp APK link / Fake Portal",
                "incident_summary": "Fraudulent message offering Rs 5,000 PM-Kisan payout via untrusted APK download received via messaging app. Intended to harvest banking credentials.",
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
            "verdict_title": "🚨 खतरनाक फर्जी सरकारी योजना और मैलवेयर हमला!",
            "explanation": "यह संदेश पूरी तरह फर्जी है और बैंकिंग ट्रोजन मैलवेयर फैलाने की सोची-समझी साजिश है। साइबर अपराधी पीएम-किसान योजना के नाम पर ₹5,000 तुरंत मिलने का लालच देकर व्हाट्सएप पर एक अज्ञात APK फाइल डाउनलोड करने को कहते हैं।\n\nयदि आप इस फाइल को फोन में इंस्टॉल करते हैं, तो यह आपके फोन के मैसेज (SMS) और पासवर्ड को चुरा लेती है, जिससे आपके बैंक के गुप्त OTP साइबर ठगों तक पहुंच जाते हैं और खाता खाली हो जाता है। प्रत्यक्ष लाभ अंतरण (DBT) नियमों के तहत भारत सरकार कभी भी व्हाट्सएप पर APK डाउनलोड करवाकर पैसे नहीं भेजती; राशि सीधे आपके आधार से जुड़े बैंक खाते में जमा होती है।",
            "red_flags": [
                "व्हाट्सएप पर अज्ञात नंबर द्वारा सरकारी योजनाओं का दावा",
                "गूगल प्ले स्टोर के बाहर से असुरक्षित .apk फाइल डाउनलोड कराने का प्रयास",
                "24 घंटे में पैसा न लेने पर योजना समाप्त होने का झूठा डर दिखाना",
                "असली सरकारी .gov.in पोर्टल की जगह फर्जी वेब लिंक"
            ],
            "solution_pathways": [
                {
                    "title": "तत्काल फोन सुरक्षा एवं फाइल डिलीट",
                    "action_type": "IMMEDIATE_ACTION",
                    "step_by_step": [
                        "लिंक पर क्लिक न करें और एपीके फाइल डाउनलोड न करें।",
                        "यदि फाइल डाउनलोड हो गई है, तो उसे बिना खोले फाइल मैनेजर से तुरंत डिलीट करें।",
                        "यदि इंस्टॉल हो चुका है, तो फोन को एयरप्लेन मोड में डालें और Settings > Apps में जाकर अनइंस्टॉल करें।",
                        "व्हाट्सएप पर उस नंबर को ब्लॉक और रिपोर्ट करें।"
                    ],
                    "contact_or_link": "Settings > Apps > Uninstall"
                },
                {
                    "title": "सत्यापित सरकारी पोर्टल द्वारा जांच",
                    "action_type": "OFFICIAL_PORTAL",
                    "step_by_step": [
                        "केवल आधिकारिक पोर्टल https://pmkisan.gov.in पर जाएं।",
                        "'Know Your Status' पर क्लिक करके अपना आधार या रजिस्ट्रेशन नंबर दर्ज करें।",
                        "निकटतम सीएससी (CSC) केंद्र या ब्लॉक कृषि कार्यालय जाकर लाभार्थी सूची में नाम जांचें।"
                    ],
                    "contact_or_link": "आधिकारिक हेल्पलाइन: 155261 / 1800-115-526"
                },
                {
                    "title": "बैंक सुरक्षा एवं आरबीआई रिफंड नियम",
                    "action_type": "FINANCIAL_RECOVERY",
                    "step_by_step": [
                        "यदि आपने यूपीआई पिन या बैंक विवरण दर्ज किया है, तो बैंक को फोन करके तत्काल यूपीआई और नेटबैंकिंग ब्लॉक कराएं।",
                        "किसी अन्य सुरक्षित फोन से अपना यूपीआई पिन और पासवर्ड बदलें।",
                        "आरबीआई के दिशा-निर्देशों के अनुसार 3 दिनों के भीतर बैंक को अनधिकृत कटौती की सूचना देने पर ग्राहक को शून्य देनदारी (Zero Liability) का लाभ मिलता है।"
                    ],
                    "contact_or_link": "बैंक 24/7 हेल्पलाइन या राष्ट्रीय हेल्पलाइन: 1930"
                },
                {
                    "title": "राष्ट्रीय साइबर अपराध पोर्टल पर रिपोर्ट",
                    "action_type": "LEGAL_POLICE",
                    "step_by_step": [
                        "तत्काल 1930 पर कॉल करें ताकि साइबर सेल संदिग्ध बैंक खातों को फ्रीज कर सके।",
                        "वेबसाइट https://cybercrime.gov.in पर जाकर धोखाधड़ी की शिकायत दर्ज करें।"
                    ],
                    "contact_or_link": "हेल्पलाइन: 1930 / https://cybercrime.gov.in"
                }
            ],
            "verified_scheme_redirect": {
                "scheme_name": "प्रधानमंत्री किसान सम्मान निधि (PM-KISAN)",
                "eligibility_bullets": [
                    "देश के सभी पात्र छोटे एवं सीमांत किसान परिवार",
                    "सालाना ₹6,000 की वित्तीय सहायता, 3 किस्तों में सीधे बैंक खाते में",
                    "आधार लिंक बैंक खाता एवं आधिकारिक पोर्टल पर e-KYC अनिवार्य"
                ],
                "official_portal": "https://pmkisan.gov.in",
                "safe_application_steps": [
                    "केवल आधिकारिक वेबसाइट https://pmkisan.gov.in पर जाएं",
                    "'Farmers Corner' -> 'New Farmer Registration' पर क्लिक करें",
                    "आधार एवं भूमि अभिलेख विवरण दर्ज करें",
                    "किसी भी बिचौलिये या अनधिकृत ऐप को पैसे न दें"
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
            "verdict_title": "🏛️ Verified Government Welfare & Higher Education Navigator",
            "explanation": "Your inquiry regarding financial aid for a student completing 12th grade / Intermediate is a legitimate civic entitlement covered under state and central educational welfare policies.\n\nIn Andhra Pradesh, the state government operates flagship schemes including Jagananna Vidya Deevena (100% full fee reimbursement for Polytechnic, ITI, Degree, Engineering, Medicine, and PG courses) alongside Jagananna Vasathi Deevena (covering hostel and mess expenses up to ₹20,000 annually). Additionally, the Government of India operates the National Scholarship Portal (NSP) for Central Sector Scheme of Scholarships for College and University Students. Both schemes transfer funds directly to accredited college accounts or verified student/mother Aadhaar-linked bank accounts via DBT without any intermediary charges.",
            "red_flags": [],
            "solution_pathways": [
                {
                    "title": "Grama / Ward Sachivalayam (Village Secretariat) Route",
                    "action_type": "OFFICIAL_PORTAL",
                    "step_by_step": [
                        "Visit your local Grama / Ward Sachivalayam and meet the Education & Welfare Assistant.",
                        "Bring the student's 12th Grade / Intermediate Marks Memo, College Allotment Order, Integrated Caste/Income Certificate, and Mother's Aadhaar Card.",
                        "Verify your family's eligibility on the Navasakam beneficiary database."
                    ],
                    "contact_or_link": "Local Village/Ward Secretariat or Toll-Free 1902"
                },
                {
                    "title": "Online Digital Application via JnanaBhumi Portal",
                    "action_type": "OFFICIAL_PORTAL",
                    "step_by_step": [
                        "Log on to the official higher education portal: https://jnanabhumi.ap.gov.in.",
                        "Submit student admission registration and link college admission code.",
                        "Complete Biometric or IRIS authentication at the college scholarship desk during admission verification."
                    ],
                    "contact_or_link": "Portal: https://jnanabhumi.ap.gov.in / Helpline: 08645-274025"
                },
                {
                    "title": "Central National Scholarship Portal (NSP) Option",
                    "action_type": "OFFICIAL_PORTAL",
                    "step_by_step": [
                        "If the student scored above 80th percentile in 12th board exams, register on https://scholarships.gov.in.",
                        "Apply under 'Central Sector Scheme of Scholarships for College and University Students'.",
                        "Upload income certificate (family income < ₹4.5 Lakh) and bank passbook with Aadhaar NPCI seeding."
                    ],
                    "contact_or_link": "National Scholarship Portal: https://scholarships.gov.in (Helpdesk: 0120-6619540)"
                },
                {
                    "title": "Citizen Rights & Anti-Bribery Redressal",
                    "action_type": "LEGAL_POLICE",
                    "step_by_step": [
                        "No government official, college clerk, or agent can demand bribes or processing fees for scholarship applications.",
                        "If any college withholds original certificates demanding upfront fees before government reimbursement, lodge an immediate grievance on Spandana Portal (1902).",
                        "Track the grievance resolution timeline guaranteed under Public Services Guarantee."
                    ],
                    "contact_or_link": "AP CM Public Grievance Helpline: 1902 / spandana.ap.gov.in"
                }
            ],
            "verified_scheme_redirect": {
                "scheme_name": "Jagananna Vidya Deevena & Post-Matric Higher Education Scholarships",
                "eligibility_bullets": [
                    "Students admitted into Polytechnic, ITI, Degree, Engineering, and PG courses through government convenor quota",
                    "Family total annual income under ₹2.5 Lakh per annum verified through Navasakam survey",
                    "Minimum 75% aggregate class attendance required to maintain semester fee disbursements"
                ],
                "official_portal": "https://jnanabhumi.ap.gov.in",
                "safe_application_steps": [
                    "Visit your nearest Grama/Ward Secretariat with college admission allotment order",
                    "Submit Aadhaar, Rice Card / Income Certificate, and bank account passbook",
                    "Complete Biometric / Aadhaar e-KYC on the official JnanaBhumi portal",
                    "Track sanction status directly on navasakam2.apcfss.in"
                ]
            },
            "cybercrime_1930_draft": None
        },
        "Telugu": {
            "intent": "SCHEME_QUERY",
            "risk_level": "GREEN_SAFE",
            "verdict_title": "🏛️ ధృవీకరించబడిన ప్రభుత్వ విద్యా పథకాలు & దరఖాస్తు మార్గాలు",
            "explanation": "12వ తరగతి (ఇంటర్మీడియట్) పూర్తి చేసుకున్న విద్యార్థుల ఉన్నత విద్య కోసం ఆంధ్రప్రదేశ్ మరియు కేంద్ర ప్రభుత్వాలు అనేక ప్రామాణిక సంక్షేమ పథకాలను అందిస్తున్నాయి.\n\nఆంధ్రప్రదేశ్‌లో 'జగనన్న విద్యా దీవెన' పథకం ద్వారా పాలిటెక్నిక్, ఐటీఐ, డిగ్రీ, ఇంజనీరింగ్, ఫార్మసీ మరియు పీజీ కోర్సుల పూర్తి ట్యూషన్ ఫీజు రీయింబర్స్‌మెంట్ లభిస్తుంది. దీనితో పాటు హాస్టల్, మెస్ ఖర్చుల కోసం 'జగనన్న వసతి దీవెన' ద్వారా ఏటా ₹20,000 వరకు నేరుగా తల్లుల ఖాతాల్లో జమ చేయబడుతుంది. అలాగే జాతీయ స్థాయిలో 'నేషనల్ స్కాలర్‌షిప్ పోర్టల్ (NSP)' ద్వారా మెరిట్ విద్యార్థులకు కేంద్ర ప్రభుత్వ ఉపకార వేతనాలు లభిస్తాయి.",
            "red_flags": [],
            "solution_pathways": [
                {
                    "title": "గ్రామ/వార్డు సచివాలయం ద్వారా దరఖాస్తు",
                    "action_type": "OFFICIAL_PORTAL",
                    "step_by_step": [
                        "మీ సమీప గ్రామ/వార్డు సచివాలయానికి వెళ్లి 'వెల్ఫేర్ & ఎడ్యుకేషన్ అసిస్టెంట్'ను కలవండి.",
                        "విద్యార్థి 12వ తరగతి మార్కుల మెమో, కాలేజ్ అలాట్‌మెంట్ ఆర్డర్, ఆదాయ/కుల ధృవీకరణ పత్రాలు మరియు ఆధార్ కార్డు అందించండి.",
                        "నవశకం పోర్టల్‌లో మీ కుటుంబ అర్హతను పరిశీలించి నమోదు చేయించుకోండి."
                    ],
                    "contact_or_link": "గ్రామ/వార్డు సచివాలయం / హెల్ప్‌లైన్: 1902"
                },
                {
                    "title": "జ్ఞానభూమి ఆన్‌లైన్ పోర్టల్ విధానం",
                    "action_type": "OFFICIAL_PORTAL",
                    "step_by_step": [
                        "అధికారిక వెబ్‌సైట్ https://jnanabhumi.ap.gov.in ను సందర్శించండి.",
                        "కాలేజీ అడ్మిషన్ వివరాలు మరియు విద్యార్థి వివరాలను పోర్టల్‌లో నమోదు చేయండి.",
                        "కాలేజీ స్కాలర్‌షిప్ కౌంటర్‌లో బయోమెట్రిక్ ఈ-కేవైసీ పూర్తి చేయండి."
                    ],
                    "contact_or_link": "జ్ఞానభూమి పోర్టల్: https://jnanabhumi.ap.gov.in"
                },
                {
                    "title": "జాతీయ స్కాలర్‌షిప్ పోర్టల్ (NSP) మార్గం",
                    "action_type": "OFFICIAL_PORTAL",
                    "step_by_step": [
                        "ఇంటర్మీడియట్‌లో అత్యుత్తమ మార్కులు సాధించినట్లయితే https://scholarships.gov.in లో దరఖాస్తు చేయండి.",
                        "'Central Sector Scheme of Scholarships' కింద రిజిస్టర్ అవ్వండి.",
                        "బ్యాంక్ ఖాతాకు ఆధార్ లింక్ (NPCI Mapping) అయ్యిందో లేదో నిర్ధారించుకోండి."
                    ],
                    "contact_or_link": "NSP పోర్టల్: scholarships.gov.in (హెల్ప్‌డెస్క్: 0120-6619540)"
                },
                {
                    "title": "సమస్యలు లేదా లంచం అడిగితే ఫిర్యాదు మార్గం",
                    "action_type": "LEGAL_POLICE",
                    "step_by_step": [
                        "స్కాలర్‌షిప్‌ల కోసం ఎవరికీ ఒక్క రూపాయి కూడా లంచం ఇవ్వవలసిన అవసరం లేదు.",
                        "ఒకవేళ ఏ కాలేజీ అయినా సర్టిఫికెట్లు నిలిపివేసినా లేదా అనధికారిక రుసుములు అడిగినా స్పందన పోర్టల్ లేదా 1902 హెల్ప్‌లైన్‌లో ఫిర్యాదు చేయండి."
                    ],
                    "contact_or_link": "స్పందన టోల్‌ఫ్రీ నంబర్: 1902 / spandana.ap.gov.in"
                }
            ],
            "verified_scheme_redirect": {
                "scheme_name": "జగనన్న విద్యా దీవెన & పోస్ట్-మెట్రిక్ ఉన్నత విద్యా ఉపకార వేతనాలు",
                "eligibility_bullets": [
                    "కన్వీనర్ కోటా ద్వారా డిగ్రీ, ఇంజనీరింగ్, పాలిటెక్నిక్ తదితర కోర్సుల్లో ప్రవేశం పొందిన విద్యార్థులు",
                    "కుటుంబ వార్షిక ఆదాయం ₹2.5 లక్షల లోపు ఉండాలి (నవశకం సర్వే ద్వారా నిర్ధారణ)",
                    "సెమిస్టర్ నిధుల విడుదల కోసం కాలేజీలో కనీసం 75% హాజరు తప్పనిసరి"
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
            "verdict_title": "🏛️ सत्यापित सरकारी उच्च शिक्षा छात्रवृत्ति एवं समाधान मार्ग",
            "explanation": "12वीं कक्षा (इंटरमीडिएट) उत्तीर्ण करने वाले विद्यार्थियों के लिए केंद्र एवं राज्य सरकार द्वारा प्रामाणिक उच्च शिक्षा छात्रवृत्ति योजनाएं संचालित हैं।\n\nआंध्र प्रदेश में 'विद्या दीवेना' योजना के तहत डिग्री, इंजीनियरिंग, पॉलिटेक्निक और पीजी कोर्सेज की पूरी कॉलेज ट्यूशन फीस सरकार वहन करती है, तथा 'वसति दीवेना' द्वारा हॉस्टल और मेस का खर्च प्रदान किया जाता है। केंद्र स्तर पर 'नेशनल स्कॉलरशिप पोर्टल (NSP)' के जरिए उच्च शिक्षा के लिए मेरिट-कम-मीन्स छात्रवृत्तियां सीधे छात्र के बैंक खाते में DBT के माध्यम से भेजी जाती हैं।",
            "red_flags": [],
            "solution_pathways": [
                {
                    "title": "सचिवालय / सीएससी (CSC) द्वारा आवेदन",
                    "action_type": "OFFICIAL_PORTAL",
                    "step_by_step": [
                        "अपने स्थानीय ग्राम/वार्ड सचिवालय या सीएससी केंद्र पर जाएं।",
                        "12वीं की मार्कशीट, कॉलेज अलॉटमेंट लेटर, आय प्रमाण पत्र और आधार कार्ड प्रस्तुत करें।",
                        "नवशकम डेटाबेस पर पात्रता सत्यापित कराएं।"
                    ],
                    "contact_or_link": "हेल्पलाइन: 1902"
                },
                {
                    "title": "ज्ञानभूमि आधिकारिक ऑनलाइन पोर्टल",
                    "action_type": "OFFICIAL_PORTAL",
                    "step_by_step": [
                        "आधिकारिक वेबसाइट https://jnanabhumi.ap.gov.in पर जाएं।",
                        "कॉलेज प्रवेश विवरण अपलोड करें और बायोमेट्रिक ई-केवाईसी पूरी करें।"
                    ],
                    "contact_or_link": "https://jnanabhumi.ap.gov.in"
                },
                {
                    "title": "राष्ट्रीय छात्रवृत्ति पोर्टल (NSP) आवेदन",
                    "action_type": "OFFICIAL_PORTAL",
                    "step_by_step": [
                        "यदि 12वीं में उच्च अंक हैं, तो https://scholarships.gov.in पर जाएं।",
                        "Central Sector Scholarship योजना में ऑनलाइन फॉर्म भरें।"
                    ],
                    "contact_or_link": "https://scholarships.gov.in"
                },
                {
                    "title": "भ्रष्टाचार या कॉलेज उत्पीड़न की शिकायत",
                    "action_type": "LEGAL_POLICE",
                    "step_by_step": [
                        "छात्रवृत्ति आवेदन पूरी तरह निःशुल्क है। किसी भी बिचौलिये को पैसे न दें।",
                        "यदि कोई कॉलेज मूल प्रमाण पत्र रोके तो स्पंदना हेल्पलाइन 1902 पर शिकायत करें।"
                    ],
                    "contact_or_link": "हेल्पलाइन: 1902"
                }
            ],
            "verified_scheme_redirect": {
                "scheme_name": "पोस्ट-मैट्रिक उच्च शिक्षा छात्रवृत्ति / विद्या दीवेना",
                "eligibility_bullets": [
                    "डिग्री, इंजीनियरिंग या तकनीकी पाठ्यक्रम में नामांकित छात्र",
                    "परिवार की वार्षिक आय ₹2.5 लाख से कम",
                    "सीधे कॉलेज एवं छात्र के आधार-लिंक खाते में छात्रवृत्ति का भुगतान"
                ],
                "official_portal": "https://jnanabhumi.ap.gov.in",
                "safe_application_steps": [
                    "सचिवालय या कॉलेज के छात्रवृत्ति काउंटर से संपर्क करें",
                    "दस्तावेज सत्यापित कराएं और बायोमेट्रिक ई-केवाईसी पूरी करें"
                ]
            },
            "cybercrime_1930_draft": None
        }
    },
    "3": {
        "English": {
            "intent": "EMERGENCY_REPORT",
            "risk_level": "RED_SCAM",
            "verdict_title": "🚨 CRITICAL EMERGENCY: 'Digital Arrest' & Law Enforcement Impersonation Extortion!",
            "explanation": "You are facing an organized, highly dangerous transnational cybercrime syndicate executing a fraudulent 'Digital Arrest'. In this modus operandi, criminals impersonate senior officers of the CBI, Mumbai/Delhi Police, Customs, or Enforcement Directorate wearing fake uniforms on Skype or WhatsApp video calls against realistic official backdrops.\n\nThey falsely claim that an illegal parcel containing narcotics, passports, or forged bank cards has been intercepted in your Aadhaar name. Under extreme psychological duress, threats of imminent physical arrest, and forced 24-hour video surveillance, they coerce victims into liquidating fixed deposits and transferring funds to a fraudulent 'RBI safe verification escrow account' via RTGS or UPI.\n\nLEGAL FACT: Under the Indian Code of Criminal Procedure (CrPC) and Bharatiya Nagarik Suraksha Sanhita (BNSS), there is NO CONCEPT of 'Digital Arrest'. No police officer, judge, or government agency has the legal authority to interrogate citizens over Skype video calls, place them under digital detention, or demand money transfer for 'clearance'.",
            "red_flags": [
                "Impersonation of Police, CBI, ED, NIA, or TRAI officials on video calls (Skype / WhatsApp)",
                "Claim of 'Digital Arrest' or 24-hour video confinement (Completely illegal and non-existent under Indian law)",
                "Demand to transfer money to a 'Reserve Bank verification account' via UPI or RTGS",
                "Threats of immediate arrest warrant, asset seizure, and severe coercion to maintain absolute secrecy from family and local police",
                "Forged arrest warrants and supreme court orders sent via WhatsApp with fake stamps"
            ],
            "solution_pathways": [
                {
                    "title": "Immediate Golden-Hour Cyber Helpline Dialing (1930)",
                    "action_type": "IMMEDIATE_ACTION",
                    "step_by_step": [
                        "DIAL 1930 IMMEDIATELY: In cyber financial fraud, the first 2 hours are the 'Golden Hour'.",
                        "Explain that you were coerced into transferring money to a fraud syndicate.",
                        "Provide the Transaction ID (UTR), your bank account number, and the recipient suspect's UPI ID / Account details.",
                        "The 1930 Citizen Financial Cyber Fraud Reporting System triggers an automated inter-bank lien to freeze the suspect's mule bank account before cash is withdrawn at an ATM."
                    ],
                    "contact_or_link": "DIAL 1930 (National Cyber Crime Helpline - 24/7)"
                },
                {
                    "title": "Bank 24/7 Fraud Desk & Urgent Lien Request",
                    "action_type": "FINANCIAL_RECOVERY",
                    "step_by_step": [
                        "Call your bank's dedicated 24/7 fraud helpline (number on back of your debit card).",
                        "Report the exact transaction as fraudulent extortion and request an immediate recall of funds.",
                        "Ask the bank's nodal officer to email the beneficiary bank's nodal officer requesting an immediate debit freeze.",
                        "Visit your home branch with the written police report acknowledgement to submit an official fraud claim."
                    ],
                    "contact_or_link": "Bank 24/7 Emergency Fraud Desk (e.g. SBI: 1800111109 / HDFC: 18001600)"
                },
                {
                    "title": "Sever All Contact & Psychological Safety",
                    "action_type": "IMMEDIATE_ACTION",
                    "step_by_step": [
                        "DISCONNECT THE CALL IMMEDIATELY. Do not entertain any further calls or messages.",
                        "Block the caller on WhatsApp, Skype, and phone dialer.",
                        "Do NOT transfer any additional money under any circumstance, no matter how severe the threats sound.",
                        "Inform a trusted family member or visit your local police station in person. Real police will reassure you immediately."
                    ],
                    "contact_or_link": "Local Police Emergency: 112"
                },
                {
                    "title": "Formal National Cybercrime Portal Filing (cybercrime.gov.in)",
                    "action_type": "LEGAL_POLICE",
                    "step_by_step": [
                        "Visit https://cybercrime.gov.in and click on 'Report Cyber Crime'.",
                        "Copy and paste the pre-drafted incident report generated by JanRakshak AI below.",
                        "Upload screenshots of the WhatsApp chat, the fake arrest order PDF, and the bank transaction debit SMS.",
                        "Obtain the formal National Cybercrime Acknowledgement Number for insurance and legal documentation."
                    ],
                    "contact_or_link": "Portal: https://cybercrime.gov.in"
                }
            ],
            "verified_scheme_redirect": None,
            "cybercrime_1930_draft": {
                "incident_category": "Digital Arrest / Law Enforcement Impersonation & Extortion via UPI",
                "suspect_identifiers": "WhatsApp / Skype Video Caller Impersonating CBI/Mumbai Police; Transaction: Rs 15,000 via UPI",
                "incident_summary": "Complainant was subjected to severe psychological coercion and extortion by organized cyber syndicate impersonating senior CBI and Police officers via video call. Suspects falsely claimed complainant's Aadhaar was implicated in international narcotics trafficking and imposed an illegal 'Digital Arrest'. Under duress of fabricated arrest warrants, complainant was extorted into transferring Rs 15,000 via UPI to suspect account for 'verification'. Immediate inter-bank freeze requested under 1930 Golden-Hour mechanism.",
                "immediate_checklist": [
                    "CALL 1930 IMMEDIATELY: The first 2 hours (Golden Hour) are vital to freeze funds in mule accounts",
                    "Call your bank's 24/7 fraud desk and report the UPI UTR reference number",
                    "Sever contact and do not transfer any more funds under any threats",
                    "File the incident draft generated on https://cybercrime.gov.in"
                ]
            }
        },
        "Telugu": {
            "intent": "EMERGENCY_REPORT",
            "risk_level": "RED_SCAM",
            "verdict_title": "🚨 అత్యవసర హెచ్చరిక: నకిలీ 'డిజిటల్ అరెస్ట్' & పోలీసుల పేరిట భయంకరమైన దోపిడీ!",
            "explanation": "మీరు అత్యంత ప్రమాదకరమైన వ్యవస్థీకృత సైబర్ నేరగాళ్ల ముఠా పన్నిన 'డిజిటల్ అరెస్ట్' ఉచ్చులో పడ్డారు. ఈ రకమైన మోసంలో, నేరస్థులు ముంబై/ఢిల్లీ పోలీసులు లేదా సీబీఐ అధికారుల వలె నకిలీ యూనిఫాంలు ధరించి స్కైప్ లేదా వాట్సాప్ వీడియో కాల్స్ చేస్తారు.\n\nమీ ఆధార్ నంబర్‌తో డ్రగ్స్ లేదా నకిలీ పాస్‌పోర్ట్‌లతో కూడిన పార్సిల్ దొరికిందని తీవ్రంగా భయపెడతారు. ఎవరికీ చెప్పకూడదని, 'డిజిటల్ అరెస్ట్' లో ఉన్నారని బెదిరిస్తూ, 'రహస్య వెరిఫికేషన్ ఖాతా' పేరుతో మీ చేత బలవంతంగా యూపీఐ లేదా బ్యాంకు ద్వారా లక్షల రూపాయలను బదిలీ చేయిస్తారు.\n\nచట్టపరమైన వాస్తవం: భారతీయ శిక్షాస్మృతి లేదా కొత్త క్రిమినల్ చట్టాలలో (BNSS) 'డిజిటల్ అరెస్ట్' అనే భావనే లేదు. ఏ పోలీసు అధికారి లేదా కోర్టు కూడా వీడియో కాల్స్‌లో విచారణ జరపరు, డిజిటల్ అరెస్ట్ చేయరు, వెరిఫికేషన్ పేరుతో డబ్బులు డిమాండ్ చేయరు.",
            "red_flags": [
                "పోలీస్, సీబీఐ, ఈడీ పేరుతో వాట్సాప్ లేదా స్కైప్ వీడియో కాల్స్ చేయడం",
                "చట్టంలో లేని 'డిజిటల్ అరెస్ట్' పేరుతో ఫోన్ ముందే ఉండాలని ఆదేశించడం",
                "ధృవీకరణ పేరుతో యూపీఐ లేదా బ్యాంక్ ఖాతాకు డబ్బు పంపాలని డిమాండ్ చేయడం",
                "కుటుంబ సభ్యులకు లేదా స్థానిక పోలీసులకు చెప్పవద్దని భయభ్రాంతులకు గురిచేయడం"
            ],
            "solution_pathways": [
                {
                    "title": "వెంటనే 1930 సైబర్ హెల్ప్‌లైన్‌కు కాల్ చేయడం (గోల్డెన్ అవర్)",
                    "action_type": "IMMEDIATE_ACTION",
                    "step_by_step": [
                        "వెంటనే 1930 నంబర్‌కు కాల్ చేయండి: డబ్బు పోయిన మొదటి 2 గంటలను 'గోల్డెన్ అవర్' అంటారు.",
                        "పోలీస్ వేధింపులతో బలవంతంగా డబ్బు బదిలీ చేయించారని వివరించండి.",
                        "మీ బ్యాంక్ ఖాతా, లావాదేవీ UTR నంబర్ మరియు మోసగాడి యూపీఐ ఐడీ వివరాలను అందించండి.",
                        "1930 వ్యవస్థ వెంటనే ఆ మోసగాడి బ్యాంక్ ఖాతాను స్తంభింపజేసి మీ డబ్బును రికవరీ చేయడానికి చర్యలు తీసుకుంటుంది."
                    ],
                    "contact_or_link": "హెల్ప్‌లైన్: 1930 (24 గంటలు అందుబాటులో ఉంటుంది)"
                },
                {
                    "title": "బ్యాంకుకు తక్షణ సమాచారం & ఖాతా ఫ్రీజ్",
                    "action_type": "FINANCIAL_RECOVERY",
                    "step_by_step": [
                        "మీ బ్యాంక్ కస్టమర్ కేర్‌కు కాల్ చేసి జరిగిన మోసాన్ని వివరించండి.",
                        "మోసగాడి ఖాతాలోకి వెళ్లిన డబ్బును రీకాల్ చేయమని రాతపూర్వకంగా దరఖాస్తు చేయండి.",
                        "బ్యాంకు ఇచ్చే ఎక్నాలెడ్జ్‌మెంట్ నంబర్‌ను భద్రపరుచుకోండి."
                    ],
                    "contact_or_link": "మీ బ్యాంక్ 24/7 అత్యవసర నంబర్ లేదా టోల్‌ఫ్రీ నంబర్"
                },
                {
                    "title": "కాల్ వెంటనే కట్ చేసి నంబర్ బ్లాక్ చేయండి",
                    "action_type": "IMMEDIATE_ACTION",
                    "step_by_step": [
                        "ఎటువంటి భయం లేకుండా వెంటనే వీడియో కాల్ కట్ చేయండి.",
                        "ఆ నంబర్‌ను వాట్సాప్ మరియు ఫోన్‌లో బ్లాక్ చేయండి.",
                        "ఎట్టి పరిస్థితుల్లోనూ అదనపు డబ్బు చెల్లించవద్దు.",
                        "ధైర్యంగా ఉండండి; మీ సమీప పోలీస్ స్టేషన్‌కు వెళ్లి చెప్పండి, పోలీసులు మీకు అండగా ఉంటారు."
                    ],
                    "contact_or_link": "పోలీస్ అత్యవసర నంబర్: 112"
                },
                {
                    "title": "cybercrime.gov.in లో అధికారిక ఆన్‌లైన్ ఫిర్యాదు",
                    "action_type": "LEGAL_POLICE",
                    "step_by_step": [
                        "https://cybercrime.gov.in వెబ్‌సైట్‌ను సందర్శించండి.",
                        "కింద జన్ రక్షక్ AI రూపొందించిన అధికారిక కంప్లైంట్ కాపీని అక్కడ పేస్ట్ చేయండి.",
                        "స్క్రీన్‌షాట్లు మరియు ట్రాన్సాక్షన్ మెసేజ్ కాపీని అప్‌లోడ్ చేయండి."
                    ],
                    "contact_or_link": "https://cybercrime.gov.in"
                }
            ],
            "verified_scheme_redirect": None,
            "cybercrime_1930_draft": {
                "incident_category": "Digital Arrest / Impersonation & Extortion via UPI",
                "suspect_identifiers": "Fake Police Video Call / UPI Reference",
                "incident_summary": "Extortion committed via video impersonation of law enforcement officers threatening fake criminal arrest. Victim coerced into transferring Rs 15,000 via UPI. Immediate account freeze requested under 1930 helpline.",
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
            "verdict_title": "🚨 आपातकालीन चेतावनी: फर्जी 'डिजिटल अरेस्ट' और कानून प्रवर्तन ब्लैकमेल!",
            "explanation": "आप एक संगठित और खतरनाक साइबर अपराध गिरोह द्वारा किए जा रहे 'डिजिटल अरेस्ट' धोखाधड़ी के शिकार हुए हैं। इस अपराध में ठग सीबीआई, पुलिस, नारकोटिक्स या सीमा शुल्क (Customs) अधिकारी बनकर वर्दी में स्काइप या व्हाट्सएप वीडियो कॉल करते हैं।\n\nवे दावा करते हैं कि आपके आधार कार्ड पर एक अवैध पार्सल पकड़ा गया है जिसमें ड्रग्स या फर्जी पासपोर्ट हैं। कानूनी गिरफ्तारी का झूठा डर दिखाकर, 24 घंटे कैमरे के सामने रहने को मजबूर करते हैं और 'आरबीआई सत्यापन' के नाम पर बैंक या यूपीआई से लाखों रुपये ट्रांसफर करा लेते हैं।\n\nकानूनी सच्चाई: भारतीय कानून (CrPC या BNSS) में 'डिजिटल अरेस्ट' नाम का कोई प्रावधान नहीं है। कोई भी पुलिस अधिकारी या अदालत वीडियो कॉल पर पूछताछ या डिजिटल हिरासत नहीं ले सकती, न ही सत्यापन के नाम पर पैसे की मांग कर सकती है।",
            "red_flags": [
                "व्हाट्सएप/स्काइप वीडियो कॉल पर पुलिस या सीबीआई की वर्दी पहनकर धमकाना",
                "भारतीय कानून में गैर-मौजूद 'डिजिटल अरेस्ट' का भय दिखाना",
                "'सत्यापन' के नाम पर यूपीआई या बैंक खाते में तत्काल पैसा ट्रांसफर कराना",
                "परिवार या स्थानीय पुलिस से बात करने पर तुरंत जेल भेजने की धमकी देना"
            ],
            "solution_pathways": [
                {
                    "title": "तत्काल 1930 साइबर हेल्पलाइन पर कॉल (गोल्डन आवर)",
                    "action_type": "IMMEDIATE_ACTION",
                    "step_by_step": [
                        "तत्काल 1930 डायल करें: अपराध के शुरुआती 2 घंटे 'गोल्डन आवर' होते हैं।",
                        "बताएं कि फर्जी पुलिस वीडियो कॉल द्वारा आपसे जबरन पैसे ट्रांसफर कराए गए हैं।",
                        "अपना बैंक खाता, यूपीआई ट्रांजेक्शन आईडी और ठग का खाता विवरण दें ताकि बैंक संदिग्ध खाते को फ्रीज कर सके।"
                    ],
                    "contact_or_link": "डायल 1930 (राष्ट्रीय साइबर हेल्पलाइन)"
                },
                {
                    "title": "बैंक साइबर सेल से संपर्क एवं फंड फ्रीज",
                    "action_type": "FINANCIAL_RECOVERY",
                    "step_by_step": [
                        "अपने बैंक के 24/7 हेल्पलाइन पर तुरंत धोखाधड़ी की रिपोर्ट करें।",
                        "लेनदेन को रिवर्स करने का आधिकारिक अनुरोध दर्ज कराएं।",
                        "आरबीआई के नियमों के तहत अनधिकृत कटौती की लिखित शिकायत दर्ज करें।"
                    ],
                    "contact_or_link": "बैंक कस्टमर केयर नंबर"
                },
                {
                    "title": "कॉल तुरंत काटें एवं नंबर ब्लॉक करें",
                    "action_type": "IMMEDIATE_ACTION",
                    "step_by_step": [
                        "बिना डरे तुरंत वीडियो कॉल काट दें।",
                        "उस नंबर को व्हाट्सएप और फोन से ब्लॉक करें।",
                        "एक भी रुपया अतिरिक्त ट्रांसफर न करें।",
                        "अपने नजदीकी थाने जाएं, पुलिस आपकी सहायता करेगी।"
                    ],
                    "contact_or_link": "पुलिस आपातकालीन नंबर: 112"
                },
                {
                    "title": "cybercrime.gov.in पर आधिकारिक रिपोर्ट दर्ज करें",
                    "action_type": "LEGAL_POLICE",
                    "step_by_step": [
                        "वेबसाइट https://cybercrime.gov.in पर जाएं।",
                        "नीचे जनरक्षक AI द्वारा तैयार की गई रिपोर्ट को कॉपी करके फॉर्म में पेस्ट करें।"
                    ],
                    "contact_or_link": "https://cybercrime.gov.in"
                }
            ],
            "verified_scheme_redirect": None,
            "cybercrime_1930_draft": {
                "incident_category": "Digital Arrest / Impersonation & Extortion via UPI",
                "suspect_identifiers": "Fake Police Video Call / UPI Transaction",
                "incident_summary": "Victim extorted of Rs 15,000 under duress of fraudulent 'Digital Arrest' by suspects impersonating CBI/police officers on video call. Request urgent inter-bank lien under 1930 Golden-Hour mechanism.",
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
    final_key = api_key.strip() or os.getenv("GEMINI_API_KEY", "")

    # Instant preset for demo scenarios
    if demo_id and demo_id in DEMO_PRESETS and not final_key:
        return DEMO_PRESETS[demo_id][selected_lang]
        
    if not final_key:
        # Check if text matches demo presets for offline resilience
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
            f"User Input / Context: {text_input or 'Analyze the uploaded image for scams, digital hazards, or government scheme information.'}\n"
            f"REQUIREMENT: Provide a deep, multi-paragraph educational explanation and 3 to 4 concrete, actionable solution pathways to resolve this issue completely."
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

        raise HTTPException(status_code=500, detail=f"Gemini API Error: {str(last_error)}")

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent Error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
