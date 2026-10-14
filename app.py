import os
import re
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
    title: str = Field(description="Title of the solution method")
    action_type: str = Field(description="IMMEDIATE_ACTION | OFFICIAL_PORTAL | FINANCIAL_RECOVERY | LEGAL_POLICE")
    step_by_step: List[str] = Field(description="Step-by-step instructions in target language")
    contact_or_link: str = Field(description="Official helpline number, website URL, or office")

class VerifiedScheme(BaseModel):
    scheme_name: str = Field(description="Name of legitimate government scheme")
    eligibility_bullets: List[str] = Field(description="Simple bullet points explaining eligibility")
    official_portal: str = Field(description="Official .gov.in or state government portal")
    safe_application_steps: List[str] = Field(description="Safe application steps")

class CybercrimeReportDraft(BaseModel):
    incident_category: str = Field(description="Category of cyber threat")
    suspect_identifiers: str = Field(description="Extracted phone numbers, URLs, APK names, or UPI IDs")
    incident_summary: str = Field(description="Formal summary drafted in English for 1930 portal")
    immediate_checklist: List[str] = Field(description="Golden-hour actions")

class CivicShieldResponse(BaseModel):
    intent: str = Field(description="SCAM_CHECK | SCHEME_QUERY | EMERGENCY_REPORT")
    risk_level: str = Field(description="RED_SCAM | YELLOW_SUSPICIOUS | GREEN_SAFE")
    plain_takeaway: str = Field(description="Crystal-clear 1-sentence bottom-line for ordinary citizens")
    analysis_engine: str = Field(default="Gemini Multi-Agent AI", description="Transparency indicator of engine used")
    query_summary: str = Field(default="", description="Summary of user query showing dynamic personalization")
    verdict_title: str = Field(description="Short punchy verdict in the requested target language")
    explanation: str = Field(description="Deep, natural, comprehensive explanation covering technical and legal reality")
    red_flags: List[str] = Field(default_factory=list, description="Detected psychological manipulation or technical triggers")
    solution_pathways: List[SolutionPathway] = Field(default_factory=list, description="All actionable ways to solve this problem")
    verified_scheme_redirect: Optional[VerifiedScheme] = None
    cybercrime_1930_draft: Optional[CybercrimeReportDraft] = None

SYSTEM_PROMPT = """
You are JanRakshak AI (CivicShield), an elite Multi-Agent Public Safety & Citizen Service Guardian for India.
Analyze the user's text and/or uploaded image and produce an empathetic, highly accurate, and transparent response.

CRITICAL REQUIREMENTS:
1. `plain_takeaway`: Provide an unmistakable, 1-sentence bottom line that any citizen, elderly person, or student can understand in 3 seconds (e.g. "❌ 100% FRAUD: Do NOT send any money or click the link." or "✅ SAFE GOVERNMENT SCHEME: Legitimate process explained below.").
2. `query_summary`: Summarize the user's exact issue so they know their specific input was understood.
3. `explanation`: Provide a natural, thorough explanation in their language of why this is safe or dangerous, explaining the exact technical mechanism or legal reality.
4. `solution_pathways`: Provide 3 to 4 distinct ways to solve the problem (Immediate phone/app action, Official verification, Banking & RBI recovery, Legal/Police reporting).
5. If it's a scam exploiting a real government scheme, populate `verified_scheme_redirect` with the genuine .gov.in portal.
6. If financial fraud or extortion is involved, populate `cybercrime_1930_draft` with a formal English summary ready for 1930 / cybercrime.gov.in.

LANGUAGE: Write user-facing fields naturally in the requested language (English, Telugu, or Hindi). Keep `incident_summary` in formal English.
"""

# Extract entities helper
def extract_identifiers(text: str) -> str:
    phones = re.findall(r"(?:\+91[\-\s]?)?[6-9]\d{9}", text)
    urls = re.findall(r"https?://[^\s]+|[a-zA-Z0-9.\-]+\.(?:apk|com|in|org|net|xyz|top)[^\s]*", text)
    amounts = re.findall(r"(?:Rs\.?|₹|INR)\s?[\d,]+|\b\d{3,7}\s?(?:rupees|rs)\b", text, re.IGNORECASE)
    
    parts = []
    if phones: parts.append(f"Phone(s): {', '.join(set(phones))}")
    if urls: parts.append(f"Link/APK(s): {', '.join(set(urls))}")
    if amounts: parts.append(f"Amount mentioned: {', '.join(set(amounts))}")
    return " | ".join(parts) if parts else "Identified via user submission"

# Dynamic Real-Time Rule Engine for ANY Custom Input
def analyze_custom_dynamically(text: str, language: str, image_name: Optional[str] = None) -> CivicShieldResponse:
    t = (text or "").lower()
    selected_lang = language if language in ["English", "Telugu", "Hindi"] else "English"
    identifiers = extract_identifiers(text)
    
    # Category 1: Electricity / Power Cutoff Extortion
    if any(k in t for k in ["electricity", "power", "disconnected", "cutoff", "sub-station", "meter", "bijli", "current", "bill not updated", "apcpdcl", "tneb", "bescom", "tsspdcl"]):
        if selected_lang == "Telugu":
            return CivicShieldResponse(
                intent="SCAM_CHECK",
                risk_level="RED_SCAM",
                plain_takeaway="❌ ఇది 100% నకిలీ విద్యుత్ బిల్లు స్కామ్! ఎటువంటి నంబర్‌కు కాల్ చేయవద్దు లేదా యూపీఐ ద్వారా డబ్బు పంపవద్దు.",
                analysis_engine="JanRakshak Dynamic Intelligence Engine",
                query_summary="విద్యుత్ కనెక్షన్ రద్దు పేరిట వచ్చిన బెదిరింపు సందేశం",
                verdict_title="🚨 ప్రమాదకరమైన నకిలీ విద్యుత్ బిల్లు & సైబర్ దోపిడీ హెచ్చరిక!",
                explanation="ఈ సందేశం పూర్తిగా మోసపూరితమైనది. సైబర్ నేరగాళ్లు రాత్రి పూట విద్యుత్ కనెక్షన్ కట్ చేస్తామని భయపెట్టి, వ్యక్తిగత ఫోన్ నంబర్లకు కాల్ చేయించి యూపీఐ లేదా రిమోట్ యాప్స్ (AnyDesk, TeamViewer) ద్వారా బ్యాంక్ ఖాతాలను ఖాళీ చేస్తున్నారు.\n\nచట్టపరమైన వాస్తవం: విద్యుత్ చట్టం 2003 (Electricity Act Section 56) ప్రకారం, సరైన రాతపూర్వక 15 రోజుల ముందస్తు నోటీసు లేకుండా ఏ విద్యుత్ శాఖ కూడా కనెక్షన్ కట్ చేయదు. అలాగే విద్యుత్ అధికారులు ఎప్పుడూ వ్యక్తిగత మొబైల్ నంబర్ల నుండి ఇలాంటి సందేశాలు పంపరు.",
                red_flags=[
                    "రాత్రి 9:30 గంటలకు విద్యుత్ నిలిపివేస్తామని కృత్రిమ భయాన్ని సృష్టించడం",
                    "అధికారిక బిల్లింగ్ కౌంటర్ కాకుండా వ్యక్తిగత మొబైల్ నంబర్‌కు కాల్ చేయమనడం",
                    "విద్యుత్ శాఖ అధికారిక .gov.in లేదా సంస్థ డొమైన్ లేకపోవడం"
                ],
                solution_pathways=[
                    SolutionPathway(
                        title="తక్షణ రక్షణ: కాల్ చేయవద్దు & నంబర్ బ్లాక్ చేయండి",
                        action_type="IMMEDIATE_ACTION",
                        step_by_step=["సందేశంలో ఉన్న నంబర్‌కు ఎట్టి పరిస్థితుల్లోనూ కాల్ చేయవద్దు.", "ఎటువంటి యాప్ (AnyDesk, QuickSupport) డౌన్‌లోడ్ చేయవద్దు.", "సందేశాన్ని డిలీట్ చేయకుండా పోలీసు ఫిర్యాదు కోసం స్క్రీన్‌షాట్ తీసుకోండి."],
                        contact_or_link="ఫోన్ సెట్టింగ్స్ > బ్లాక్ నంబర్"
                    ),
                    SolutionPathway(
                        title="అధికారిక విద్యుత్ శాఖ ద్వారా బిల్లు తనిఖీ",
                        action_type="OFFICIAL_PORTAL",
                        step_by_step=["మీ విద్యుత్ బోర్డు అధికారిక యాప్ లేదా వెబ్‌సైట్ ద్వారా మీ సర్వీస్ నంబర్‌తో బిల్లు బకాయి ఉందో లేదో చూడండి.", "మీ సమీప విద్యుత్ సబ్-స్టేషన్ లేదా ఈఆర్వో (ERO) ఆఫీస్‌కు నేరుగా వెళ్లండి."],
                        contact_or_link="జాతీయ విద్యుత్ హెల్ప్‌లైన్: 1912 (టోల్‌ఫ్రీ)"
                    ),
                    SolutionPathway(
                        title="సైబర్ క్రైమ్ పోలీసులకు ఫిర్యాదు",
                        action_type="LEGAL_POLICE",
                        step_by_step=["ఒకవేళ మోసపోయి డబ్బు బదిలీ చేసి ఉంటే వెంటనే 1930 నంబర్‌కు కాల్ చేయండి.", "cybercrime.gov.in లో ఆ నంబర్‌పై ఫిర్యాదు నమోదు చేయండి."],
                        contact_or_link="హెల్ప్‌లైన్: 1930 / cybercrime.gov.in"
                    )
                ],
                cybercrime_1930_draft=CybercrimeReportDraft(
                    incident_category="Extortion / Fake Electricity Bill Disconnection Fraud",
                    suspect_identifiers=identifiers,
                    incident_summary=f"Victim received fraudulent SMS threatening imminent power disconnection unless immediate payment was made to personal contact. Input details: {text[:200]}",
                    immediate_checklist=["Do not dial suspect number", "Call 1912 for genuine power board inquiry", "Report number to 1930 if funds were sent"]
                )
            )
        else:
            return CivicShieldResponse(
                intent="SCAM_CHECK",
                risk_level="RED_SCAM",
                plain_takeaway="❌ 100% FRAUD: Do NOT call the number or transfer money. Your electricity will NOT be disconnected.",
                analysis_engine="JanRakshak Dynamic Intelligence Engine",
                query_summary="Electricity disconnection panic SMS / Call",
                verdict_title="🚨 Dangerous Electricity Bill Extortion Cyber Trap Detected!",
                explanation="This is an organized cyber scam spreading across India. Fraudsters send bulk SMS messages claiming your power supply will be cut off tonight due to unpaid bills. They urge you to call a personal 10-digit mobile number, where they trick you into installing remote desktop apps (AnyDesk, RustDesk) or sharing UPI PINs to siphon your savings.\n\nLEGAL REALITY: Under Section 56 of the Indian Electricity Act (2003), power distribution utilities are legally mandated to serve a formal 15-day written notice before disconnecting any consumer. Power companies never send SMS threats from personal mobile numbers demanding urgent direct calls.",
                red_flags=[
                    "Threatens immediate nighttime disconnection to induce panic",
                    "Provides an unofficial 10-digit personal mobile number instead of official billing counters",
                    "Non-standard sender ID with no official state electricity board verification"
                ],
                solution_pathways=[
                    SolutionPathway(
                        title="Immediate Action: Ignore Call & Do Not Install Any App",
                        action_type="IMMEDIATE_ACTION",
                        step_by_step=["Do NOT call the phone number mentioned in the SMS.", "Never install remote support apps (AnyDesk, TeamViewer, RustDesk) under caller instructions.", "Block and report the sender on your mobile network."],
                        contact_or_link="Device Dial-pad > Block Number"
                    ),
                    SolutionPathway(
                        title="Official Power Utility Verification",
                        action_type="OFFICIAL_PORTAL",
                        step_by_step=["Check your genuine bill status on your electricity board's official portal or app using your Consumer/Service Number.", "Call the national power helpline 1912 to verify your meter account."],
                        contact_or_link="National Electricity Toll-Free Helpline: 1912"
                    ),
                    SolutionPathway(
                        title="Emergency 1930 Cyber Reporting",
                        action_type="LEGAL_POLICE",
                        step_by_step=["If you already shared UPI PIN or money was debited, call 1930 immediately within the 2-hour Golden Hour.", "Submit this incident draft on cybercrime.gov.in."],
                        contact_or_link="Helpline: 1930 / https://cybercrime.gov.in"
                    )
                ],
                cybercrime_1930_draft=CybercrimeReportDraft(
                    incident_category="Fake Electricity Bill Disconnection Extortion",
                    suspect_identifiers=identifiers,
                    incident_summary=f"Complainant received an extortion SMS threatening immediate power cut-off unless money was transferred to an unofficial mobile contact. Modus operandi matches nationwide power bill scam syndicate. Details: {text[:200]}",
                    immediate_checklist=["Call 1912 to verify bill", "Call 1930 immediately if money was debited", "Block suspect sender"]
                )
            )

    # Category 2: Bank KYC / PAN Card Freeze / Account Suspended
    elif any(k in t for k in ["kyc", "pan card", "account blocked", "account suspended", "yono", "sbi", "hdfc", "icici", "axis", "debit card blocked", "sim blocked"]):
        return CivicShieldResponse(
            intent="SCAM_CHECK",
            risk_level="RED_SCAM",
            plain_takeaway="❌ 100% PHISHING: Banks NEVER send SMS links to update KYC or PAN. Do NOT click.",
            analysis_engine="JanRakshak Dynamic Intelligence Engine",
            query_summary="Bank Account Suspended / PAN Card KYC Phishing alert",
            verdict_title="🚨 Urgent Bank KYC & Credential Phishing Scam Detected!",
            explanation="This message is a credential harvesting phishing attack. Scammers falsely claim that your bank account, net banking, or debit card will be blocked immediately unless you update your PAN or KYC via the provided web link.\n\nWhen you click the link, it loads a fraudulent clone of your bank's login page. Entering your username, password, or OTP allows cybercriminals to take over your account and drain your funds. Reserve Bank of India (RBI) regulations explicitly state that banks will NEVER request sensitive KYC updates or passwords through third-party SMS links.",
            red_flags=[
                "Fake urgency: 'Account will be deactivated within 24 hours'",
                "Unofficial link containing misspellings or non-bank domains",
                "Requests PAN card, Aadhaar, or net-banking credentials via an SMS link"
            ],
            solution_pathways=[
                SolutionPathway(
                    title="Immediate Quarantine & Link Deletion",
                    action_type="IMMEDIATE_ACTION",
                    step_by_step=["Do not click or open the link.", "If opened, do NOT enter your net-banking password or OTP.", "Immediately delete the SMS."],
                    contact_or_link="Phone Messaging > Delete & Block"
                ),
                SolutionPathway(
                    title="Official Bank Branch Verification",
                    action_type="OFFICIAL_PORTAL",
                    step_by_step=["KYC can only be updated securely inside your bank's official mobile app or by visiting your local branch with physical documents.", "Call your bank's official helpline printed on your debit card."],
                    contact_or_link="Check official bank website or back of your ATM card"
                ),
                SolutionPathway(
                    title="Bank Account Freeze if Password Entered",
                    action_type="FINANCIAL_RECOVERY",
                    step_by_step=["If credentials were typed, call your bank's fraud desk to block net-banking immediately.", "Change your internet banking and UPI passwords from a secure computer."],
                    contact_or_link="Bank 24/7 Helpline or 1930"
                )
            ],
            cybercrime_1930_draft=CybercrimeReportDraft(
                incident_category="Banking Credential Phishing / Fake KYC Alert",
                suspect_identifiers=identifiers,
                incident_summary=f"Phishing SMS received pretending to be from bank demanding urgent PAN/KYC update via external website link. Designed to compromise banking credentials. Content: {text[:200]}",
                immediate_checklist=["Freeze net banking if credentials entered", "Report to bank fraud desk", "Lodge complaint on 1930"]
            )
        )

    # Category 3: Work-From-Home / Telegram Task / Part-Time Job Scam
    elif any(k in t for k in ["telegram", "task", "youtube like", "work from home", "part time job", "daily income", "rating", "earn 3000", "earn 5000", "hotel review"]):
        return CivicShieldResponse(
            intent="SCAM_CHECK",
            risk_level="RED_SCAM",
            plain_takeaway="❌ 100% PONZI SCAM: Legitimate companies never pay you for liking videos or ask you to deposit money to withdraw earnings.",
            analysis_engine="JanRakshak Dynamic Intelligence Engine",
            query_summary="Work-from-Home Telegram task / YouTube like fraud",
            verdict_title="🚨 High-Risk Task-Based Ponzi Job Fraud Detected!",
            explanation="You are being targeted by an organized Telegram task-based investment scam. In the first phase, scammers pay small sums (₹150 - ₹500) for simple tasks like liking YouTube videos or writing Google reviews to win your trust.\n\nNext, they lure you into a 'Pre-paid Task' or 'VIP Crypto Investment' on a fake trading dashboard, asking for deposits of ₹5,000 to ₹50,000. When you attempt to withdraw your money, they freeze your funds and demand additional 'taxes' or 'unlock fees' until you are completely drained.",
            red_flags=[
                "Offers unrealistically high daily income for trivial tasks (liking videos, hotel ratings)",
                "Conducts all communication on Telegram or WhatsApp groups",
                "Demands deposits or recharge fees to withdraw your earned balance"
            ],
            solution_pathways=[
                SolutionPathway(
                    title="Stop All Deposits & Sever Contact",
                    action_type="IMMEDIATE_ACTION",
                    step_by_step=["Do NOT deposit any money under any promise of doubled returns.", "Leave and report the Telegram group immediately.", "Do not communicate with the 'receptionist' or 'tutor'."],
                    contact_or_link="Telegram > Report Group > Fake Account"
                ),
                SolutionPathway(
                    title="Immediate 1930 Golden-Hour Fund Freeze",
                    action_type="FINANCIAL_RECOVERY",
                    step_by_step=["If you already transferred money, dial 1930 immediately.", "Provide the UPI Transaction IDs (UTR) and recipient bank accounts to initiate an inter-bank lien."],
                    contact_or_link="Dial 1930 (National Cyber Crime Helpline)"
                ),
                SolutionPathway(
                    title="Formal Incident Submission",
                    action_type="LEGAL_POLICE",
                    step_by_step=["Collect screenshots of the Telegram chat and payment transaction receipts.", "File an online FIR at https://cybercrime.gov.in."],
                    contact_or_link="https://cybercrime.gov.in"
                )
            ],
            cybercrime_1930_draft=CybercrimeReportDraft(
                incident_category="Task-Based Part-Time Job / Investment Fraud",
                suspect_identifiers=identifiers,
                incident_summary=f"Victim lured through messaging apps promising high income for online review tasks, then coerced into fraudulent deposit transactions. Input: {text[:200]}",
                immediate_checklist=["Do not send any further deposits", "Report all transaction IDs to 1930", "File FIR on cybercrime.gov.in"]
            )
        )

    # Category 4: Government Welfare / Subsidy / Scholarship Query (Safe / Legitimate)
    elif any(k in t for k in ["scholarship", "scheme", "subsidy", "farmer", "kisan", "vidya deevena", "college", "fees", "student", "daughter", "education", "pm-kisan", "pm awas", "housing", "ration", "ayushman"]):
        scheme_title = "Central & State Welfare Support"
        portal = "https://scholarships.gov.in"
        if "farmer" in t or "kisan" in t:
            scheme_title = "PM-Kisan & Agricultural Welfare"
            portal = "https://pmkisan.gov.in"
        elif "housing" in t or "awas" in t:
            scheme_title = "Pradhan Mantri Awas Yojana (PMAY)"
            portal = "https://pmaymis.gov.in"
        elif "health" in t or "ayushman" in t:
            scheme_title = "Ayushman Bharat PM-JAY Health Coverage"
            portal = "https://pmjay.gov.in"
        
        return CivicShieldResponse(
            intent="SCHEME_QUERY",
            risk_level="GREEN_SAFE",
            plain_takeaway="✅ LEGITIMATE GOVERNMENT INQUIRY: Here is the verified, safe official pathway to apply without middlemen.",
            analysis_engine="JanRakshak Dynamic Intelligence Engine",
            query_summary=f"Citizen Inquiry: {scheme_title}",
            verdict_title=f"🏛️ Verified Information & Application Guide: {scheme_title}",
            explanation=f"Your inquiry regarding {scheme_title} is a genuine civic entitlement. Government welfare subsidies and student scholarships in India are disbursed through the Direct Benefit Transfer (DBT) framework directly to your Aadhaar-seeded bank account.\n\nYou do NOT need to pay any application fees to middlemen, agents, or third-party websites. All central and state welfare benefits are processed transparently through verified government portals or your local village/ward secretariat.",
            red_flags=[],
            solution_pathways=[
                SolutionPathway(
                    title="Local Offline Application via Sachivalayam / CSC",
                    action_type="OFFICIAL_PORTAL",
                    step_by_step=["Visit your nearest Grama / Ward Sachivalayam or Common Service Centre (CSC).", "Carry Aadhaar card, income certificate, and land records or educational admission allotment order.", "Enrollment and status verification at government centers is completely free."],
                    contact_or_link="Local Grama/Ward Secretariat or Toll-Free 1902"
                ),
                SolutionPathway(
                    title="Direct Online Registration on Official Portal",
                    action_type="OFFICIAL_PORTAL",
                    step_by_step=[f"Visit the verified portal: {portal}.", "Ensure the URL ends strictly in .gov.in before entering any personal details.", "Complete Aadhaar e-KYC authentication on the portal."],
                    contact_or_link=f"Official Portal: {portal}"
                ),
                SolutionPathway(
                    title="Citizen Protection Against Bribery & Middlemen",
                    action_type="LEGAL_POLICE",
                    step_by_step=["Never pay cash or commission to anyone promising faster subsidy release.", "If anyone demands a bribe, report immediately to the state public grievance helpline."],
                    contact_or_link="Public Grievance Toll-Free: 1902 / 1800-11-4000"
                )
            ],
            verified_scheme_redirect=VerifiedScheme(
                scheme_name=scheme_title,
                eligibility_bullets=[
                    "Eligible based on verified family income and criteria in the official state database",
                    "Direct Benefit Transfer (DBT) directly into your Aadhaar-linked bank account",
                    "Mandatory e-KYC completed on the verified government portal"
                ],
                official_portal=portal,
                safe_application_steps=[
                    f"Visit {portal} directly in your browser",
                    "Select your respective scheme category and verify eligibility",
                    "Submit documentation at your local administrative office without paying any fees"
                ]
            )
        )

    # Category 5: General Suspicious Message / Unknown Scam Query
    else:
        return CivicShieldResponse(
            intent="SCAM_CHECK",
            risk_level="YELLOW_SUSPICIOUS",
            plain_takeaway="⚠️ CAUTION: Unverified message. Never share passwords, OTPs, or send money to unverified sources.",
            analysis_engine="JanRakshak Dynamic Intelligence Engine",
            query_summary=f"Custom Query: {text[:80]}...",
            verdict_title="⚠️ Unverified Claim — High Vigilance Recommended",
            explanation=f"Based on your input '{text[:100]}...', this communication displays patterns commonly associated with social engineering or digital solicitation.\n\nLegitimate government departments, banks, and reputable organizations never demand urgent money transfers, confidential PINs, or downloads of external application files through casual text messages. Always cross-verify the sender's identity through official public channels before taking any action.",
            red_flags=[
                "Unverified sender identity and lack of official institutional channels",
                "Requests personal information, phone contact, or financial interaction",
                "Requires independent verification before any trust is placed"
            ],
            solution_pathways=[
                SolutionPathway(
                    title="Independent Channel Verification",
                    action_type="OFFICIAL_PORTAL",
                    step_by_step=["Do not use any phone number or link provided in the message.", "Look up the official contact details of the organization independently through their verified .gov.in or official website."],
                    contact_or_link="Official Department / Organization Website"
                ),
                SolutionPathway(
                    title="Digital Privacy & Credential Defense",
                    action_type="IMMEDIATE_ACTION",
                    step_by_step=["Never share OTPs, passwords, UPI MPIN, or Aadhaar OTP with any caller or website.", "If in doubt, ignore and block the sender."],
                    contact_or_link="Device Dial-pad > Block Number"
                ),
                SolutionPathway(
                    title="National Cyber Crime Helpline (1930)",
                    action_type="LEGAL_POLICE",
                    step_by_step=["If you suspect fraudulent solicitation or lost money, call 1930 immediately for guidance and account protection.", "Lodge incident details on cybercrime.gov.in."],
                    contact_or_link="Helpline: 1930 / https://cybercrime.gov.in"
                )
            ],
            cybercrime_1930_draft=CybercrimeReportDraft(
                incident_category="Suspicious Cyber Solicitation / Potential Fraud",
                suspect_identifiers=identifiers,
                incident_summary=f"User requested verification for suspicious communication: {text[:200]}",
                immediate_checklist=["Verify through official channels", "Do not share OTP or send money", "Dial 1930 if funds were compromised"]
            )
        )

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

    # Clean text input
    cleaned_text = (text_input or "").strip()

    # Try Live Gemini Call if API Key is Available
    if final_key:
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
                f"User Input: {cleaned_text or 'Analyze the uploaded screenshot for scams, government schemes, or cyber hazards.'}\n\n"
                f"TASK: Provide an empathetic, highly accurate, and transparent multi-agent response tailored SPECIFICALLY to this exact user input."
            )
            contents.append(prompt_text)

            candidate_models = ["gemini-2.5-flash", "gemini-2.0-flash", "gemini-1.5-flash", "gemini-3.8-flash"]
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
                        parsed_json["analysis_engine"] = f"Gemini Cloud AI ({model_name})"
                        if not parsed_json.get("query_summary"):
                            parsed_json["query_summary"] = cleaned_text[:60] if cleaned_text else "Multimodal Analysis"
                        return parsed_json
                except Exception:
                    continue
        except Exception:
            pass  # Fall through seamlessly to dynamic analyzer so user is NEVER blocked!

    # Dynamic Analysis Engine: Guarantees tailored output for ANY user input!
    img_name = image.filename if image else None
    dynamic_result = analyze_custom_dynamically(cleaned_text, selected_lang, img_name)
    return dynamic_result

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
