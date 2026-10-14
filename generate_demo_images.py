import os
from PIL import Image, ImageDraw, ImageFont

os.makedirs("demo_assets", exist_ok=True)

def create_whatsapp_scam_img():
    # WhatsApp style chat screenshot
    img = Image.new("RGB", (600, 450), color="#0b141a")
    draw = ImageDraw.Draw(img)

    # Header bar
    draw.rectangle([(0, 0), (600, 60)], fill="#202c33")
    draw.text((20, 20), "Govt Welfare Alerts (+91 98765 43210)", fill="#e9edef")

    # Chat bubble
    draw.rectangle([(40, 90), (560, 320)], fill="#005c4b", outline="#005c4b")
    
    text_lines = [
        "🚨 URGENT: PM-Kisan & Vidya Deevena Scheme 2026",
        "",
        "Dear Beneficiary, your pending installment of Rs 5,000",
        "has been sanctioned by Govt of India.",
        "",
        "Click below to download official PM-Kisan app and claim:",
        "👉 http://pmkisan-direct-claim.apk",
        "",
        "⚠️ Must claim within 24 hours or subsidy will expire!",
        "11:42 AM • Forwarded many times"
    ]
    y = 105
    for line in text_lines:
        color = "#ffdddd" if "http" in line or "URGENT" in line else "#ffffff"
        draw.text((60, y), line, fill=color)
        y += 20

    # Warning watermark
    draw.rectangle([(40, 350), (560, 410)], fill="#2a1215", outline="#e53e3e")
    draw.text((60, 370), "⚠️ SUSPICIOUS SAMPLE FOR JANRAKSHAK AI DEMO", fill="#fc8181")

    img.save("demo_assets/fake_pmkisan_whatsapp.png")
    print("Saved demo_assets/fake_pmkisan_whatsapp.png")

def create_electricity_sms_img():
    img = Image.new("RGB", (600, 400), color="#1a202c")
    draw = ImageDraw.Draw(img)

    # SMS header
    draw.rectangle([(0, 0), (600, 50)], fill="#2d3748")
    draw.text((20, 15), "Messages • VM-APCPDCL-ALERT", fill="#edf2f7")

    # SMS bubble
    draw.rectangle([(30, 80), (570, 290)], fill="#2d3748", outline="#4a5568")

    text_lines = [
        "Dear Consumer, your electricity power will be disconnected",
        "tonight at 9:30 PM from the sub-station because your",
        "previous month bill was not updated.",
        "",
        "Please immediately call our electricity officer at:",
        "📞 +91-91234-56789 or pay via UPI to prevent cutoff.",
        "",
        "Electricity Board Officer: Mr. Sharma"
    ]
    y = 95
    for line in text_lines:
        color = "#feb2b2" if "disconnected" in line or "📞" in line else "#e2e8f0"
        draw.text((50, y), line, fill=color)
        y += 22

    # Warning box
    draw.rectangle([(30, 320), (570, 370)], fill="#2a1215", outline="#e53e3e")
    draw.text((50, 335), "⚠️ FAKE DISCONNECTION SMS SAMPLE", fill="#fc8181")

    img.save("demo_assets/fake_electricity_sms.png")
    print("Saved demo_assets/fake_electricity_sms.png")

if __name__ == "__main__":
    create_whatsapp_scam_img()
    create_electricity_sms_img()
