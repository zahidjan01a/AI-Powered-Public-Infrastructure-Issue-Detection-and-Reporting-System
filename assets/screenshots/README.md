# Application Screenshots & Visual Assets

This directory stores visual documentation and UI screenshots for the **CivicAlert AI** platform and PowerPoint presentation.

---

## The 5 Screenshots Embedded in Slides 12 & 13

These screenshots are captured from the live application and embedded directly into **Slide 12** and **Slide 13** of [`presentation/AI_Public_Infrastructure_Detector.pptx`](../../presentation/AI_Public_Infrastructure_Detector.pptx):

| Screenshot File | Step in App | What is Captured | Embedded Slide |
| :--- | :--- | :--- | :--- |
| **`01_portal_landing.png`** | Step 1 | Citizen Service Portal banner, photo uploader box, and *"Where is this issue located?"* landmark selection. | Slide 12 (Left Card) |
| **`02_ai_diagnosis.png`** | Step 2 | Street photograph alongside MobileNetV2 verification card (*Garbage - 99.99% Confidence*) and class breakdown bar. | Slide 12 (Right Card) |
| **`03_department_routing.png`** | Step 3 | Designated Municipal Authority card (*Municipal Solid Waste Management*), urgency badge, 24-48h SLA, and #311 helpline. | Slide 13 (Top-Left) |
| **`04_automated_report.png`** | Step 4 | Official Citizen Grievance & Infrastructure Report drafted by Google Gemini LLM with safety impacts and municipal action items. | Slide 13 (Right Card) |
| **`05_official_ticket_receipt.png`** | Step 5 | Green success banner with official tracking ticket (*#REF-2026-WMD-SAN-22415*), location (*Charsadda muslimabad*), and download receipt. | Slide 13 (Bottom-Left) |

---

## How to Capture These Screenshots

1. Launch the Streamlit application:
   ```powershell
   streamlit run app/app.py
   ```
2. Upload a sample image (e.g. from the pothole, crack, or garbage sets).
3. Type a street address (e.g., *"Main Market Road, near Commercial Center"*).
4. Review the AI diagnosis, click **"🚀 Submit Official Report to Department"**, and capture the 4 screen sections using Windows Snipping Tool (`Win + Shift + S`).
5. Save the PNG files into this directory (`assets/screenshots/`).
