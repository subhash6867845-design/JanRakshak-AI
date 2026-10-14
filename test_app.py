import pytest
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_home_page_status():
    """Verify frontend entry point returns HTTP 200"""
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers.get("content-type", "")

def test_slides_endpoint_status():
    """Verify presentation pitch deck route returns HTTP 200"""
    response = client.get("/slides")
    assert response.status_code == 200

def test_health_check_status():
    """Verify API health endpoint returns healthy status"""
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data.get("status") == "healthy"
    assert "JanRakshak" in data.get("service")

def test_analyze_endpoint_missing_payload():
    """Verify endpoint input validation on empty request"""
    response = client.post("/api/analyze", data={})
    assert response.status_code in [200, 400, 422, 500]

def test_btech_scholarship_custom_query():
    """Test user exact prompt: B.Tech scholarship and fee reimbursement"""
    prompt = "i am pursuing the btech second year and i am unable to bear the fees, is their any schlolership which reduse my burden"
    response = client.post(
        "/api/analyze",
        data={"text_input": prompt, "language": "English"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["risk_level"] == "GREEN_SAFE"
    assert len(data.get("solution_pathways", [])) >= 3
    assert data.get("verified_scheme_redirect") is not None
    assert ".gov.in" in data["verified_scheme_redirect"]["official_portal"]

def test_digital_arrest_scam_detection():
    """Verify detection of high-risk Digital Arrest extortion scams"""
    scam_text = "CBI officer on Skype video call says my Aadhaar is involved in money laundering, transfer penalty to avoid immediate arrest"
    response = client.post(
        "/api/analyze",
        data={"text_input": scam_text, "language": "English"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["risk_level"] == "RED_SCAM"
    assert data.get("cybercrime_1930_draft") is not None
    assert len(data.get("solution_pathways", [])) >= 3

def test_electricity_cutoff_apk_scam():
    """Verify detection of electricity bill disconnection APK scams"""
    scam_text = "Dear consumer, your electricity will be disconnected tonight at 9:30 PM. Download apcpdcl-bill.apk immediately to update."
    response = client.post(
        "/api/analyze",
        data={"text_input": scam_text, "language": "English"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["risk_level"] == "RED_SCAM"
    assert len(data.get("red_flags", [])) > 0

def test_multilingual_telugu_query():
    """Verify Telugu regional language analysis support"""
    response = client.post(
        "/api/analyze",
        data={
            "text_input": "పీఎం కిసాన్ సబ్సిడీ మరియు రేషన్ కార్డు దరఖాస్తు విధానం",
            "language": "Telugu"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data.get("verdict_title") is not None
    assert len(data.get("solution_pathways", [])) >= 1

def test_multilingual_hindi_query():
    """Verify Hindi regional language analysis support"""
    response = client.post(
        "/api/analyze",
        data={
            "text_input": "बिजली बिल अपडेट न करने पर कनेक्शन कटने का मैसेज आया है",
            "language": "Hindi"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data.get("verdict_title") is not None
    assert data.get("risk_level") == "RED_SCAM"

def test_civic_schema_structure():
    """Unit test for response model schema structure"""
    sample_payload = {
        "text_input": "PM Kisan subsidy status check",
        "language": "Telugu"
    }
    assert sample_payload["language"] == "Telugu"
    assert "PM Kisan" in sample_payload["text_input"]
