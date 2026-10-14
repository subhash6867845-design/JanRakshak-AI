# JanRakshak AI — Test Inputs & Live Demo Prompts

Copy and paste any of these inputs into the app to test different agents and languages.

---

### Scenario A: Fake Welfare APK Phishing (Forensic Scam Shield + Scheme Navigator)
```text
Urgent Govt Alert! PM-Kisan & Vidya Deevena beneficiary installment approved. Download official AP-Kisan App directly: http://pmkisan-direct-claim.apk to claim ₹5,000 immediately within 24 hours.
```
- **Language to Test:** English or Telugu
- **Expected Outcome:** 
  - Risk Level: `RED_SCAM`
  - Red Flags: Fake .apk file, psychological urgency, untrusted domain.
  - Safe Redirect: Genuine PM-Kisan (`pmkisan.gov.in`) eligibility and application steps.

---

### Scenario B: Electricity Disconnection Cyber Extortion
```text
Dear Consumer, your electricity power will be disconnected tonight at 9:30 PM from the sub-station because your previous month bill was not updated. Please immediately call our electricity officer at +91-91234-56789 or pay via UPI to prevent cutoff.
```
- **Language to Test:** English or Hindi
- **Expected Outcome:**
  - Risk Level: `RED_SCAM`
  - Red Flags: Direct personal mobile number for billing, nighttime cutoff panic tactic, unofficial payment channel.
  - 1930 Draft: Auto-extracted suspect phone number, incident summary for 1930 portal.

---

### Scenario C: Citizen Welfare & Scholarship Inquiry (Scheme Navigator)
```text
My daughter just completed 12th grade in Andhra Pradesh with good marks. We are from a middle-class farming family. What official government scholarships and fee reimbursements can we apply for safely?
```
- **Language to Test:** Telugu or English
- **Expected Outcome:**
  - Risk Level: `GREEN_SAFE`
  - Official Scheme: Jagananna Vidya Deevena / Central Post-Matric Scholarships.
  - 3 Simple Bullet Points on eligibility + official portal `jnanabhumi.ap.gov.in`.

---

### Scenario D: "Digital Arrest" & Police Extortion Emergency (Golden-Hour 1930 Drafter)
```text
Emergency: I received a WhatsApp video call from someone in police uniform claiming to be CBI officers from Mumbai. They said a parcel with narcotics was registered in my Aadhaar name and put me under 'Digital Arrest'. They forced me to transfer ₹15,000 via UPI to a verification account and are demanding more.
```
- **Language to Test:** Any
- **Expected Outcome:**
  - Risk Level: `RED_SCAM` (Emergency)
  - Formal 1930 incident report draft in English.
  - Golden-Hour steps: Call 1930 within 2 hours, notify bank fraud desk, freeze suspect UPI ID.
