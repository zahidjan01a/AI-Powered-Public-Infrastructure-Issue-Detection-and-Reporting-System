import os
import sys
import time
import random
from datetime import datetime
from pathlib import Path
from PIL import Image
import numpy as np
import pandas as pd
import streamlit as st
import tensorflow as tf

# Add project root to sys.path to enable clean imports from src
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import importlib
import src
import src.department_routing
import src.prediction
import src.preprocessing
import src.llm_recommendation
import src.gps_utils
import src.database

importlib.reload(src.department_routing)
importlib.reload(src.prediction)
importlib.reload(src.preprocessing)
importlib.reload(src.llm_recommendation)
importlib.reload(src.gps_utils)
importlib.reload(src.database)
importlib.reload(src)

# Initialize local SQLite persistence layer
src.init_db()

# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="CivicAlert AI | Municipal Operations & Citizen Portal",
    page_icon="🏙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# ADVANCED CUSTOM CSS & SLEEK CIVIC PORTAL THEME
# =========================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    color: #0f172a;
}

.main {
    padding-top: 0.5rem;
    max-width: 1200px;
    margin: 0 auto;
}

/* Header & Banner */
.portal-header {
    padding: 2.2rem 2.5rem;
    border-radius: 22px;
    background: linear-gradient(135deg, #0b132b 0%, #1c2541 50%, #253258 100%);
    color: #ffffff;
    margin-bottom: 2rem;
    box-shadow: 0 15px 35px -10px rgba(11, 19, 43, 0.4);
    border: 1px solid rgba(255, 255, 255, 0.12);
    position: relative;
    overflow: hidden;
}

.portal-header h1 {
    font-size: 2.25rem;
    font-weight: 800;
    margin-bottom: 0.4rem;
    color: #ffffff !important;
    letter-spacing: -0.025em;
}

.portal-header p {
    font-size: 1.05rem;
    color: #94a3b8;
    line-height: 1.6;
    margin-bottom: 0;
    max-width: 780px;
}

.portal-tag {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 0.35rem 0.85rem;
    border-radius: 9999px;
    background: rgba(37, 99, 235, 0.25);
    border: 1px solid rgba(147, 197, 253, 0.4);
    color: #bfdbfe;
    font-size: 0.8rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-bottom: 0.9rem;
}

/* Step Badges & Containers */
.step-card {
    background: #ffffff;
    border-radius: 18px;
    padding: 1.8rem;
    border: 1px solid #e2e8f0;
    box-shadow: 0 4px 20px -2px rgba(0, 0, 0, 0.04);
    margin-bottom: 1.8rem;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.step-card:hover {
    box-shadow: 0 8px 30px -4px rgba(0, 0, 0, 0.08);
}

.step-title {
    display: flex;
    align-items: center;
    gap: 12px;
    font-size: 1.25rem;
    font-weight: 700;
    color: #0f172a;
    margin-bottom: 1.2rem;
}

.step-number {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 34px;
    height: 34px;
    border-radius: 10px;
    background: #2563eb;
    color: #ffffff;
    font-weight: 800;
    font-size: 0.95rem;
}

/* Issue Result Cards */
.issue-badge-garbage {
    background: #fef2f2;
    color: #991b1b;
    border: 1px solid #fecaca;
}

.issue-badge-pothole {
    background: #fff7ed;
    color: #9a3412;
    border: 1px solid #fed7aa;
}

.issue-badge-crack {
    background: #fefce8;
    color: #854d0e;
    border: 1px solid #fef08a;
}

.issue-badge-normal {
    background: #f0fdf4;
    color: #166534;
    border: 1px solid #bbf7d0;
}

.result-card-inner {
    padding: 1.5rem;
    border-radius: 16px;
    background: #f8fafc;
    border: 1px solid #e2e8f0;
}

.result-label {
    font-size: 0.8rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: #64748b;
    margin-bottom: 0.3rem;
}

.result-heading {
    font-size: 1.9rem;
    font-weight: 800;
    color: #0f172a;
    margin-bottom: 0.4rem;
}

.dept-highlight {
    background: #f1f5f9;
    border-left: 5px solid #2563eb;
    padding: 1.2rem 1.4rem;
    border-radius: 0 14px 14px 0;
    margin: 1rem 0;
}

.dept-name {
    font-size: 1.3rem;
    font-weight: 800;
    color: #0f172a;
    margin-bottom: 0.3rem;
}

.sla-pill {
    display: inline-block;
    padding: 0.3rem 0.75rem;
    border-radius: 8px;
    background: #e0f2fe;
    color: #0369a1;
    font-weight: 700;
    font-size: 0.85rem;
    border: 1px solid #bae6fd;
}

/* Success Ticket Container */
.ticket-success {
    background: linear-gradient(135deg, #ecfdf5 0%, #f0fdf4 100%);
    border: 2px solid #34d399;
    border-radius: 20px;
    padding: 2.2rem;
    margin-top: 1.5rem;
    box-shadow: 0 10px 25px -5px rgba(16, 185, 129, 0.15);
}

.ticket-header {
    display: flex;
    align-items: center;
    gap: 12px;
    font-size: 1.6rem;
    font-weight: 800;
    color: #065f46;
    margin-bottom: 1rem;
}

.ticket-code {
    font-family: monospace;
    font-size: 1.35rem;
    font-weight: 800;
    background: #ffffff;
    padding: 0.4rem 1rem;
    border-radius: 8px;
    border: 1px dashed #059669;
    color: #047857;
    display: inline-block;
    letter-spacing: 0.05em;
}

/* KPI Cards for Municipal Admin */
.kpi-container {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 16px;
    margin-bottom: 2rem;
}

.kpi-card {
    background: #ffffff;
    border-radius: 16px;
    padding: 1.4rem 1rem;
    border: 1px solid #e2e8f0;
    box-shadow: 0 4px 15px -3px rgba(0, 0, 0, 0.04);
    text-align: center;
}

.kpi-value {
    font-size: 2.2rem;
    font-weight: 800;
    line-height: 1.1;
    margin-bottom: 0.3rem;
}

.kpi-label {
    font-size: 0.82rem;
    font-weight: 700;
    color: #64748b;
    text-transform: uppercase;
    letter-spacing: 0.04em;
}

/* Status Badges */
.badge-status {
    display: inline-block;
    padding: 0.28rem 0.75rem;
    border-radius: 9999px;
    font-size: 0.8rem;
    font-weight: 700;
    text-align: center;
}
.badge-submitted { background: #fef2f2; color: #b91c1c; border: 1px solid #fecaca; }
.badge-review { background: #fffbeb; color: #b45309; border: 1px solid #fde68a; }
.badge-dispatched { background: #eff6ff; color: #1d4ed8; border: 1px solid #bfdbfe; }
.badge-progress { background: #faf5ff; color: #7e22ce; border: 1px solid #e9d5ff; }
.badge-resolved { background: #ecfdf5; color: #047857; border: 1px solid #a7f3d0; }

/* Footer */
.portal-footer {
    text-align: center;
    color: #64748b;
    padding: 3rem 0 1.5rem 0;
    font-size: 0.9rem;
}

.portal-footer a {
    color: #2563eb;
    text-decoration: none;
    font-weight: 600;
}

/* Button override */
.stButton button {
    border-radius: 12px !important;
    font-weight: 700 !important;
    padding: 0.65rem 1.5rem !important;
    transition: all 0.2s ease !important;
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# MODEL PATH & RESOURCE LOADING
# =========================================================

MODEL_PATH = PROJECT_ROOT / "models" / "best_model.keras"
CLASS_NAMES_PATH = PROJECT_ROOT / "models" / "class_names.txt"


@st.cache_resource
def get_model():
    """Loads and caches the trained MobileNetV2 Keras model."""
    return src.load_classification_model(MODEL_PATH)


try:
    model = get_model()
    class_names = src.load_class_names(CLASS_NAMES_PATH)
    model_loaded = True
except Exception as e:
    model_loaded = False
    st.error("❌ Could not load the AI model.")
    st.code(str(MODEL_PATH))
    st.exception(e)
    st.stop()

# =========================================================
# SESSION STATE INITIALIZATION
# =========================================================

if "submitted_ticket" not in st.session_state:
    st.session_state.submitted_ticket = None

if "report_text" not in st.session_state:
    st.session_state.report_text = None

if "location_input" not in st.session_state:
    st.session_state.location_input = ""

if "admin_authenticated" not in st.session_state:
    st.session_state.admin_authenticated = False

# =========================================================
# SIDEBAR NAVIGATION & PORTAL SETTINGS
# =========================================================

with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/smart-city.png", width=54)
    st.markdown("### CivicAlert AI 🏙️")
    st.caption("Public Infrastructure Citizen Portal")

    st.markdown("---")
    st.markdown("#### 🧭 Portal Navigation")
    
    portal_options = [
        "👤 Citizen Reporting Portal",
        "🔍 Track My Ticket"
    ]
    if st.session_state.admin_authenticated:
        portal_options.append("🏛️ Municipal Admin Dashboard")

    nav_mode = st.radio(
        "Select Portal Mode:",
        options=portal_options,
        index=0
    )

    st.markdown("---")
    st.markdown("#### 🔑 Google Gemini API")
    api_key_env = os.environ.get("GEMINI_API_KEY", "")

    api_key_input = st.text_input(
        "API Key:",
        type="password",
        value=api_key_env,
        placeholder="Enter your GEMINI_API_KEY",
        help="Optional. Real-time Gemini LLM petition generation."
    )

    selected_model = st.selectbox(
        "AI Engine Model:",
        options=src.AVAILABLE_GEMINI_MODELS,
        index=0
    )

    if st.button("⚡ Test Gemini Connection", use_container_width=True):
        if api_key_input.strip():
            with st.spinner("Connecting to Google Gemini..."):
                valid, msg = src.verify_gemini_api_key(api_key_input)
                if valid:
                    st.success("✅ Connected to Google Gemini live!")
                else:
                    st.error(f"❌ {msg}")
        else:
            st.warning("⚠️ Enter an API key to test.")

    has_live_key = bool(api_key_input and api_key_input.strip())
    if has_live_key:
        st.success("⚡ Live Gemini AI Active")
    else:
        st.info("💡 Built-in Expert Engine Active")

    st.markdown("---")
    st.markdown("#### 🏛️ Municipal Staff Access")
    if not st.session_state.admin_authenticated:
        with st.expander("🔐 Official Portal Login"):
            st.caption("Restricted to municipal authorities & department supervisors.")
            passkey_input = st.text_input("Staff Passkey:", type="password", placeholder="Enter official passkey", key="staff_pin_sidebar")
            if st.button("Unlock Admin Console", use_container_width=True):
                if passkey_input.strip() == "admin2026" or passkey_input.strip().lower() == "admin":
                    st.session_state.admin_authenticated = True
                    st.toast("✅ Municipal Admin Dashboard Unlocked!", icon="🏛️")
                    time.sleep(0.3)
                    st.rerun()
                else:
                    st.error("❌ Invalid Passkey. Staff access only.")
                    st.caption("Demo Passkey: `admin2026`")
    else:
        st.success("🏛️ Municipal Admin Mode Active")
        if st.button("🔒 Sign Out to Citizen Mode", use_container_width=True):
            st.session_state.admin_authenticated = False
            st.rerun()

    st.markdown("---")
    st.caption("AI Model: MobileNetV2 (98.33% Test Acc)")
    st.caption("v2.6.0 | Citizen Service Edition")


# =========================================================
# VIEW 1: CITIZEN REPORTING PORTAL
# =========================================================

if nav_mode == "👤 Citizen Reporting Portal":

    st.markdown("""
    <div class="portal-header">
        <div class="portal-tag">🏛️ Municipal Citizen Service Portal</div>
        <h1>Public Infrastructure Issue Reporting 🏙️</h1>
        <p>
            Help keep our city clean, safe, and well-maintained. Simply snap a photo of any public issue
            (like garbage piles, potholes, or cracked roads), enter the location, and our AI will immediately
            identify the responsible municipal department, draft your official report, and file it for repair.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # STEP 1: PHOTO UPLOAD & LOCATION
    st.markdown("""
    <div class="step-card">
        <div class="step-title">
            <span class="step-number">1</span>
            <span>Take or Upload a Photo & Specify Location</span>
        </div>
    """, unsafe_allow_html=True)

    col_up, col_loc = st.columns([1.1, 1.2])

    with col_up:
        uploaded_file = st.file_uploader(
            "Upload a photograph of the issue (Garbage, Pothole, Road Crack):",
            type=["jpg", "jpeg", "png"],
            help="Accepted formats: JPG, JPEG, PNG. Crisp, clear photos yield the most accurate AI verification."
        )

    with col_loc:
        st.markdown("##### 📍 Where is this issue located?")
        st.caption("Provide a street name, neighborhood, or nearby landmark so city crews can locate it.")

        sample_col1, sample_col2 = st.columns(2)
        with sample_col1:
            if st.button("📍 Main Market Road", use_container_width=True):
                st.session_state.location_input = "Main Market Road, near Commercial Center"
        with sample_col2:
            if st.button("📍 Sector 4 Park Ave", use_container_width=True):
                st.session_state.location_input = "Sector 4 Park Ave, opposite Gate #2"

        loc_text = st.text_input(
            "Street Address or Area Name:",
            value=st.session_state.location_input,
            placeholder="e.g., Main Market Road, near Central Park West Gate",
            help="Type your location or pick one of the quick buttons above."
        )
        st.session_state.location_input = loc_text

    st.markdown("</div>", unsafe_allow_html=True)

    if uploaded_file is not None:
        try:
            image = Image.open(uploaded_file)
            if not src.validate_image(image):
                st.error("⚠️ Image validation failed: Please upload a valid JPG or PNG photograph.")
                st.stop()
        except Exception as e:
            st.error(f"⚠️ Error reading uploaded image: {e}")
            st.stop()

        with st.spinner("🤖 AI Vision Model analyzing photograph..."):
            time.sleep(0.15)
            processed_tensor, _ = src.preprocess_image(image)
            prediction_res = src.predict_infrastructure_issue(
                model,
                processed_tensor,
                class_names
            )
            if isinstance(prediction_res, dict):
                predicted_class = prediction_res["predicted_class"]
                conf_val = prediction_res.get("confidence_score", prediction_res.get("confidence", 0.0))
                confidence_score = float(conf_val / 100.0 if conf_val > 1.0 else conf_val)
                raw_probs = prediction_res.get("all_probabilities", prediction_res.get("class_probabilities", {}))
                all_probabilities = {
                    k: float(v / 100.0 if v > 1.0 else v) for k, v in raw_probs.items()
                }
            else:
                predicted_class, confidence_score, all_probabilities = prediction_res

        badge_class = f"issue-badge-{predicted_class.replace('road_', '')}"
        class_formatted = predicted_class.replace('_', ' ').title()

        # STEP 2: AI VERIFICATION
        st.markdown("""
        <div class="step-card">
            <div class="step-title">
                <span class="step-number">2</span>
                <span>AI Verification & Visual Diagnosis</span>
            </div>
        """, unsafe_allow_html=True)

        col_img, col_res = st.columns([1, 1.2])

        with col_img:
            st.image(image, caption=f"Captured Image ({image.size[0]} × {image.size[1]} px)", use_container_width=True)

        with col_res:
            st.markdown(f"""
            <div class="result-card-inner">
                <div class="result-label">AI Visual Classification</div>
                <div class="result-heading">{class_formatted}</div>
                <div style="font-size:0.95rem; color:#64748b; margin-bottom:1rem;">
                    Confidence Rating: <strong style="color:#2563eb;">{confidence_score * 100:.2f}%</strong>
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("##### Verification Breakdown")
            for c_name, prob in sorted(all_probabilities.items(), key=lambda x: x[1], reverse=True):
                c_title = c_name.replace('_', ' ').title()
                col_bar_lbl, col_bar_val = st.columns([1, 3])
                with col_bar_lbl:
                    st.caption(f"**{c_title}**")
                with col_bar_val:
                    st.progress(float(prob), text=f"{prob * 100:.1f}%")

        st.markdown("</div>", unsafe_allow_html=True)

        # STEP 3: MUNICIPAL DEPARTMENT ROUTING
        loc_context = st.session_state.location_input.strip() or "Unspecified Municipal Sector"
        dept_info = src.get_department_recommendation(
            predicted_class,
            confidence_score
        )
        dept_info["location"] = loc_context

        primary_dept = dept_info.get("primary_department", "Municipal Public Works Department")
        sub_dept = dept_info.get("sub_department", dept_info.get("secondary_department", "City Operations Division"))
        action_plan = dept_info.get("recommended_action", "Inspect and dispatch response crew.")
        urgency = dept_info.get("urgency_tier", dept_info.get("urgency_level", "Medium to High"))
        sla_window = dept_info.get("estimated_sla", "24 to 48 Hours")
        helpline = dept_info.get("emergency_helpline", dept_info.get("contact_helpline", "City Line 311"))

        st.markdown("""
        <div class="step-card">
            <div class="step-title">
                <span class="step-number">3</span>
                <span>Designated Municipal Department Routing</span>
            </div>
        """, unsafe_allow_html=True)

        dept_col1, dept_col2 = st.columns([1.5, 1])

        with dept_col1:
            st.markdown(f"""
            <div style="background:#f8fafc; border-left:5px solid #2563eb; padding:1.2rem 1.4rem; border-radius:0 14px 14px 0;">
                <div style="font-size:0.8rem; font-weight:700; color:#2563eb; text-transform:uppercase; letter-spacing:0.06em;">Designated Municipal Authority</div>
                <div style="font-size:1.35rem; font-weight:800; color:#0f172a; margin:0.2rem 0;">{primary_dept}</div>
                <div style="font-size:0.9rem; color:#64748b; margin-bottom:0.6rem;">Operating Division: {sub_dept}</div>
                <div style="font-size:0.88rem; color:#334155;"><strong>Action Plan:</strong> {action_plan}</div>
            </div>
            """, unsafe_allow_html=True)

        with dept_col2:
            st.markdown(f"""
            <div style="background:#ffffff; border:1px solid #e2e8f0; border-radius:14px; padding:1.2rem;">
                <div style="font-size:0.8rem; color:#64748b; font-weight:600;">Urgency Tier:</div>
                <div style="font-size:1.05rem; font-weight:700; color:#0f172a; margin-bottom:0.8rem;">{urgency}</div>
                <div style="font-size:0.8rem; color:#64748b; font-weight:600;">Expected Turnaround:</div>
                <div class="sla-pill" style="margin-bottom:0.8rem;">⏱️ {sla_window}</div>
                <div style="font-size:0.8rem; color:#64748b; font-weight:600;">Municipal Helpline:</div>
                <div style="font-size:0.9rem; font-weight:700; color:#2563eb;">📞 {helpline}</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

        # STEP 4: AUTOMATED INCIDENT REPORT
        st.markdown("""
        <div class="step-card">
            <div class="step-title">
                <span class="step-number">4</span>
                <span>Automated Incident Report for Department</span>
            </div>
        """, unsafe_allow_html=True)

        if st.session_state.report_text is None:
            with st.spinner("✍️ Drafting formal municipal grievance petition..."):
                st.session_state.report_text = src.generate_llm_recommendation(
                    predicted_class=predicted_class,
                    confidence=confidence_score,
                    dept_info=dept_info,
                    citizen_location=loc_context,
                    api_key=api_key_input if has_live_key else None,
                    model_name=selected_model
                )

        if has_live_key:
            st.caption(f"⚡ Mode: Live Google Gemini AI (`{selected_model}`)")
        else:
            st.caption("💡 Mode: Built-in Expert Civil Advisory Engine | Enter Gemini API key in sidebar for dynamic drafting.")

        st.markdown(st.session_state.report_text)
        st.markdown("</div>", unsafe_allow_html=True)

        # STEP 5: SUBMISSION & TICKET
        st.markdown("""
        <div class="step-card">
            <div class="step-title">
                <span class="step-number">5</span>
                <span>Submit Report to Responsible Department</span>
            </div>
        """, unsafe_allow_html=True)

        submit_col1, submit_col2 = st.columns([1.6, 1])

        with submit_col1:
            submit_btn = st.button(
                label=f"🚀 Submit Official Report to {dept_info['primary_department']}",
                type="primary",
                use_container_width=True
            )

        with submit_col2:
            st.download_button(
                label="💾 Save Draft as File (.md)",
                data=st.session_state.report_text,
                file_name=f"report_{predicted_class}_{datetime.now().strftime('%Y%m%d')}.md",
                mime="text/markdown",
                use_container_width=True
            )

        if submit_btn:
            random_id = random.randint(10000, 99999)
            dept_code = dept_info.get("department_code", "GEN-MUN")
            timestamp_now = datetime.now().strftime("%B %d, %Y at %I:%M %p")
            ticket_id = f"REF-{datetime.now().year}-{dept_code}-{random_id}"

            ticket_data = {
                "ticket_id": ticket_id,
                "department": dept_info["primary_department"],
                "dept_code": dept_code,
                "timestamp": timestamp_now,
                "category": class_formatted,
                "confidence": float(confidence_score * 100),
                "location": loc_context,
                "urgency": dept_info.get("urgency_tier", "Medium to High"),
                "sla": dept_info["estimated_sla"],
                "status": "Submitted",
                "report_text": st.session_state.report_text,
                "admin_notes": "Citizen report filed via CivicAlert portal. Queued for department triage."
            }

            # Persist to SQLite Database
            src.insert_ticket(ticket_data)
            st.session_state.submitted_ticket = ticket_data
            st.toast("✅ Official Ticket Logged & Saved in Database!", icon="🎫")

        if st.session_state.submitted_ticket:
            ticket = st.session_state.submitted_ticket
            st.markdown(f"""
            <div class="ticket-success">
                <div class="ticket-header">
                    <span>✅</span>
                    <span>Report Successfully Filed & Registered!</span>
                </div>
                <p style="font-size:1.05rem; color:#064e3b; margin-bottom:1.2rem;">
                    Your report has been successfully logged and routed to the <strong>{ticket['department']}</strong>.
                    Municipal crews have been notified to inspect the site.
                </p>
                <div style="background:#ffffff; border-radius:14px; padding:1.4rem; border:1px solid #a7f3d0;">
                    <div style="margin-bottom:0.8rem;">
                        <span style="font-size:0.85rem; color:#64748b; font-weight:600;">Official Municipal Reference Ticket:</span><br>
                        <span class="ticket-code">{ticket['ticket_id']}</span>
                    </div>
                    <div style="display:grid; grid-template-columns: 1fr 1fr; gap:12px; margin-top:1rem;">
                        <div>
                            <span style="font-size:0.85rem; color:#64748b; font-weight:600;">Issue Category:</span><br>
                            <strong>{ticket['category']}</strong>
                        </div>
                        <div>
                            <span style="font-size:0.85rem; color:#64748b; font-weight:600;">Incident Location:</span><br>
                            <strong>{ticket['location']}</strong>
                        </div>
                        <div>
                            <span style="font-size:0.85rem; color:#64748b; font-weight:600;">Logged Timestamp:</span><br>
                            <strong>{ticket['timestamp']}</strong>
                        </div>
                        <div>
                            <span style="font-size:0.85rem; color:#64748b; font-weight:600;">Target Resolution Window:</span><br>
                            <strong style="color:#059669;">{ticket['sla']}</strong>
                        </div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            receipt_text = f"""==================================================
MUNICIPAL CITIZEN GRIEVANCE RECEIPT
Ticket Reference ID: {ticket['ticket_id']}
==================================================
Date & Time: {ticket['timestamp']}
Department: {ticket['department']}
Issue Type: {ticket['category']}
Location: {ticket['location']}
Expected SLA: {ticket['sla']}
Status: Submitted to Municipal Registry

Please retain this receipt for tracking with your municipal helpline.
=================================================="""

            col_rcpt1, col_rcpt2 = st.columns([1, 1])
            with col_rcpt1:
                st.download_button(
                    label="📥 Download Official Submission Receipt (.txt)",
                    data=receipt_text,
                    file_name=f"receipt_{ticket['ticket_id']}.txt",
                    mime="text/plain",
                    use_container_width=True
                )
            with col_rcpt2:
                if st.button("🔄 File Another Report", use_container_width=True):
                    st.session_state.submitted_ticket = None
                    st.session_state.report_text = None
                    st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

    else:
        st.markdown("""
        <div style="background:#f8fafc; border:2px dashed #cbd5e1; border-radius:18px; padding:3rem 2rem; text-align:center; color:#64748b;">
            <img src="https://img.icons8.com/fluency/96/camera.png" width="70" style="margin-bottom:1rem; opacity:0.85;">
            <h3 style="color:#334155; font-weight:700; margin-bottom:0.4rem;">No photograph uploaded yet</h3>
            <p style="font-size:1rem; max-width:500px; margin:0 auto 1.5rem auto;">
                Take or upload a photo of road damage, uncollected garbage, or normal infrastructure to generate your official municipal report.
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        col_c1, col_c2, col_c3, col_c4 = st.columns(4)
        with col_c1:
            st.markdown("""
            <div style="background:#ffffff; border:1px solid #e2e8f0; border-radius:14px; padding:1.2rem; text-align:center;">
                <h4 style="color:#0f172a; margin-bottom:0.3rem;">🗑️ Garbage</h4>
                <p style="font-size:0.85rem; color:#64748b;">Routes to Solid Waste & Sanitation Dept.</p>
            </div>
            """, unsafe_allow_html=True)
        with col_c2:
            st.markdown("""
            <div style="background:#ffffff; border:1px solid #e2e8f0; border-radius:14px; padding:1.2rem; text-align:center;">
                <h4 style="color:#0f172a; margin-bottom:0.3rem;">🕳️ Pothole</h4>
                <p style="font-size:0.85rem; color:#64748b;">Routes to Public Works & Road Repair Dept.</p>
            </div>
            """, unsafe_allow_html=True)
        with col_c3:
            st.markdown("""
            <div style="background:#ffffff; border:1px solid #e2e8f0; border-radius:14px; padding:1.2rem; text-align:center;">
                <h4 style="color:#0f172a; margin-bottom:0.3rem;">🚧 Road Crack</h4>
                <p style="font-size:0.85rem; color:#64748b;">Routes to Highway Engineering Bureau.</p>
            </div>
            """, unsafe_allow_html=True)
        with col_c4:
            st.markdown("""
            <div style="background:#ffffff; border:1px solid #e2e8f0; border-radius:14px; padding:1.2rem; text-align:center;">
                <h4 style="color:#0f172a; margin-bottom:0.3rem;">✅ Normal</h4>
                <p style="font-size:0.85rem; color:#64748b;">Recorded in Civil Asset Monitoring Registry.</p>
            </div>
            """, unsafe_allow_html=True)


# =========================================================
# VIEW 2: CITIZEN TICKET TRACKER
# =========================================================

elif nav_mode == "🔍 Track My Ticket":

    st.markdown("""
    <div class="portal-header">
        <div class="portal-tag">🔍 Citizen Service Transparency</div>
        <h1>Track Your Municipal Repair Ticket 🎫</h1>
        <p>
            Check the real-time resolution progress of any infrastructure complaint filed with the city.
            View the assigned municipal department, target repair SLA, and field inspection updates.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="step-card">
        <div class="step-title">
            <span class="step-number">🔍</span>
            <span>Enter Official Reference Ticket ID</span>
        </div>
    """, unsafe_allow_html=True)

    c_srch1, c_srch2 = st.columns([2, 1])
    with c_srch1:
        search_id = st.text_input(
            "Ticket ID:",
            placeholder="e.g., REF-2026-WMD-SAN-22415",
            help="Enter the exact reference number provided on your submission receipt."
        )

    with c_srch2:
        st.markdown("<div style='margin-top:28px;'></div>", unsafe_allow_html=True)
        sample_pick = st.selectbox(
            "Or pick a recent demo ticket:",
            ["(Choose sample ticket)", "REF-2026-WMD-SAN-22415", "REF-2026-DPW-ROADS-18920", "REF-2026-HDA-EXPR-10452", "REF-2026-WMD-SAN-09142"]
        )
        if sample_pick != "(Choose sample ticket)":
            search_id = sample_pick

    st.markdown("</div>", unsafe_allow_html=True)

    if search_id and search_id.strip():
        found = src.get_ticket_by_id(search_id)
        if found:
            # Determine lifecycle index
            status_order = ["Submitted", "Under Review", "Crew Dispatched", "In Progress", "Resolved"]
            cur_status = found["status"]
            step_idx = status_order.index(cur_status) if cur_status in status_order else 0

            st.markdown(f"""
            <div class="step-card" style="border-top: 5px solid #2563eb;">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:1.2rem;">
                    <div>
                        <span style="font-size:0.85rem; color:#64748b; font-weight:700; text-transform:uppercase;">Municipal Reference</span><br>
                        <span class="ticket-code" style="font-size:1.4rem;">{found['ticket_id']}</span>
                    </div>
                    <div>
                        <span class="badge-status badge-{cur_status.lower().replace(' ', '')}" style="font-size:0.95rem; padding:0.4rem 1.2rem;">
                            ● {cur_status.upper()}
                        </span>
                    </div>
                </div>
            """, unsafe_allow_html=True)

            # Visual Progress Stepper
            st.markdown("##### 📍 Resolution Lifecycle")
            prog_val = (step_idx + 1) / len(status_order)
            st.progress(prog_val, text=f"Stage {step_idx + 1} of 5: {cur_status}")

            col_t1, col_t2 = st.columns(2)
            with col_t1:
                st.markdown(f"""
                <div style="background:#f8fafc; border-radius:14px; padding:1.2rem; border:1px solid #e2e8f0; margin-top:1rem;">
                    <div style="font-size:0.8rem; color:#64748b; font-weight:700;">ISSUE CLASSIFICATION</div>
                    <div style="font-size:1.2rem; font-weight:800; color:#0f172a;">{found['category']}</div>
                    <div style="font-size:0.85rem; color:#64748b; margin-bottom:0.8rem;">AI Confidence: {found['confidence']:.1f}%</div>

                    <div style="font-size:0.8rem; color:#64748b; font-weight:700;">LOCATION</div>
                    <div style="font-size:0.95rem; font-weight:700; color:#0f172a; margin-bottom:0.8rem;">📍 {found['location']}</div>

                    <div style="font-size:0.8rem; color:#64748b; font-weight:700;">REPORTED TIMESTAMP</div>
                    <div style="font-size:0.9rem; color:#334155;">🕒 {found['created_at']}</div>
                </div>
                """, unsafe_allow_html=True)

            with col_t2:
                st.markdown(f"""
                <div style="background:#f8fafc; border-radius:14px; padding:1.2rem; border:1px solid #e2e8f0; margin-top:1rem;">
                    <div style="font-size:0.8rem; color:#64748b; font-weight:700;">ASSIGNED MUNICIPAL AGENCY</div>
                    <div style="font-size:1.1rem; font-weight:800; color:#2563eb;">{found['department']}</div>
                    <div style="font-size:0.85rem; color:#64748b; margin-bottom:0.8rem;">Agency Code: <strong>{found['dept_code']}</strong></div>

                    <div style="font-size:0.8rem; color:#64748b; font-weight:700;">TURNAROUND SLA</div>
                    <div class="sla-pill" style="margin-bottom:0.8rem;">⏱️ {found['sla']}</div>

                    <div style="font-size:0.8rem; color:#64748b; font-weight:700;">OFFICIAL FIELD ENGINEER NOTES</div>
                    <div style="font-size:0.92rem; color:#0f172a; background:#ffffff; padding:0.6rem 0.8rem; border-radius:8px; border:1px solid #cbd5e1;">
                        {found.get('admin_notes') or 'Awaiting initial department assessment.'}
                    </div>
                </div>
                """, unsafe_allow_html=True)

            with st.expander("📄 View Full Citizen Grievance & Technical Report"):
                st.markdown(found.get("report_text") or "No detailed report text logged.")

            st.markdown("</div>", unsafe_allow_html=True)

        else:
            st.error(f"❌ No ticket found matching '{search_id}'. Please verify your Reference ID.")


# =========================================================
# VIEW 3: MUNICIPAL ADMIN DASHBOARD
# =========================================================

elif nav_mode == "🏛️ Municipal Admin Dashboard":

    st.markdown("""
    <div class="portal-header">
        <div class="portal-tag">🏛️ Municipal Administration Center</div>
        <h1>City Infrastructure Operations Dashboard 📊</h1>
        <p>
            Centralized command dashboard for municipal engineers and department supervisors.
            Review incoming citizen reports, dispatch field maintenance crews, update repair statuses, and monitor operational SLA compliance.
        </p>
    </div>
    """, unsafe_allow_html=True)

    metrics = src.get_admin_metrics()

    # KPI Summary Cards
    st.markdown(f"""
    <div class="kpi-container">
        <div class="kpi-card" style="border-top:4px solid #2563eb;">
            <div class="kpi-value" style="color:#2563eb;">{metrics['total_tickets']}</div>
            <div class="kpi-label">📋 Total Reports Filed</div>
        </div>
        <div class="kpi-card" style="border-top:4px solid #e11d48;">
            <div class="kpi-value" style="color:#e11d48;">{metrics['pending_triage']}</div>
            <div class="kpi-label">⏳ Pending Triage</div>
        </div>
        <div class="kpi-card" style="border-top:4px solid #d97706;">
            <div class="kpi-value" style="color:#d97706;">{metrics['active_field']}</div>
            <div class="kpi-label">🚛 Active Field Crews</div>
        </div>
        <div class="kpi-card" style="border-top:4px solid #059669;">
            <div class="kpi-value" style="color:#059669;">{metrics['resolved_count']}</div>
            <div class="kpi-label">✅ Issues Resolved</div>
        </div>
        <div class="kpi-card" style="border-top:4px solid #7c3aed;">
            <div class="kpi-value" style="color:#7c3aed;">{metrics['sla_compliance']}%</div>
            <div class="kpi-label">⏱️ SLA Compliance Rate</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Department & Status Filter Controls
    st.markdown("""
    <div class="step-card">
        <div class="step-title">
            <span class="step-number">⚙️</span>
            <span>Filter Municipal Defect Registry</span>
        </div>
    """, unsafe_allow_html=True)

    f_col1, f_col2, f_col3 = st.columns([1.5, 1.2, 1.5])

    with f_col1:
        dept_options = {
            "ALL": "🏛️ All Municipal Departments",
            "WMD-SAN": "🗑️ Solid Waste Management (WMD-SAN)",
            "DPW-ROADS": "🕳️ Public Works & Roads (DPW-ROADS)",
            "HDA-EXPR": "🚧 Highway Engineering (HDA-EXPR)",
            "DCI-INFR": "✅ Civil Asset Monitoring (DCI-INFR)"
        }
        dept_filter = st.selectbox(
            "Filter by Department Agency:",
            options=list(dept_options.keys()),
            format_func=lambda x: dept_options[x]
        )

    with f_col2:
        status_options = ["ALL", "Submitted", "Under Review", "Crew Dispatched", "In Progress", "Resolved"]
        status_filter = st.selectbox("Filter by Status:", status_options)

    with f_col3:
        search_query = st.text_input("Search Location or Ticket ID:", placeholder="e.g. Charsadda, Main Market, Pothole")

    st.markdown("</div>", unsafe_allow_html=True)

    # Filtered Tickets Data
    tickets_list = src.get_tickets(dept_code=dept_filter, status=status_filter, search=search_query)

    st.markdown(f"#### 📋 Municipal Incidents Queue ({len(tickets_list)} records)")

    if tickets_list:
        df_export = src.export_tickets_df(dept_code=dept_filter, status=status_filter, search=search_query)
        st.dataframe(
            df_export[[
                "Ticket ID", "Category", "Confidence (%)", "Location",
                "Dept Code", "Urgency", "SLA", "Status", "Created At"
            ]],
            use_container_width=True,
            hide_index=True
        )

        st.markdown("<br>", unsafe_allow_html=True)

        # Operational Triage Action Box
        st.markdown("""
        <div class="step-card" style="border-top:4px solid #2563eb;">
            <div class="step-title">
                <span class="step-number">🛠️</span>
                <span>Operational Triage & Field Crew Dispatch</span>
            </div>
        """, unsafe_allow_html=True)

        ticket_choices = {t["ticket_id"]: f"{t['ticket_id']} — {t['category']} @ {t['location']} ({t['status']})" for t in tickets_list}
        selected_tid = st.selectbox("Select Ticket to Triage or Update:", options=list(ticket_choices.keys()), format_func=lambda x: ticket_choices[x])

        selected_t = next((t for t in tickets_list if t["ticket_id"] == selected_tid), None)

        if selected_t:
            act_col1, act_col2 = st.columns([1, 1.2])

            with act_col1:
                st.markdown(f"""
                <div style="background:#f8fafc; padding:1.2rem; border-radius:12px; border:1px solid #e2e8f0;">
                    <span style="font-size:0.8rem; color:#64748b; font-weight:700;">TICKET DETAILS</span><br>
                    <strong>ID:</strong> <code>{selected_t['ticket_id']}</code><br>
                    <strong>Category:</strong> {selected_t['category']} ({selected_t['confidence']:.1f}%)<br>
                    <strong>Location:</strong> {selected_t['location']}<br>
                    <strong>Agency:</strong> {selected_t['department']}<br>
                    <strong>Urgency:</strong> {selected_t['urgency']} | <strong>SLA:</strong> {selected_t['sla']}<br>
                    <strong>Current Status:</strong> <span class="badge-status badge-{selected_t['status'].lower().replace(' ', '')}">{selected_t['status']}</span>
                </div>
                """, unsafe_allow_html=True)

            with act_col2:
                status_choices = ["Submitted", "Under Review", "Crew Dispatched", "In Progress", "Resolved"]
                current_idx = status_choices.index(selected_t["status"]) if selected_t["status"] in status_choices else 0

                new_st = st.selectbox("Update Operational Status:", status_choices, index=current_idx)
                new_notes = st.text_area(
                    "Field Engineer / Supervisor Action Notes:",
                    value=selected_t.get("admin_notes") or "",
                    placeholder="Enter dispatch notes, crew assigned, vehicle license, or resolution verification details."
                )

                if st.button("💾 Apply Operational Status Update", type="primary", use_container_width=True):
                    success = src.update_ticket_status(selected_tid, new_st, new_notes)
                    if success:
                        st.success(f"✅ Ticket {selected_tid} updated to '{new_st}' successfully!")
                        time.sleep(0.6)
                        st.rerun()
                    else:
                        st.error("Failed to update status in database.")

            with st.expander("📄 View Full Citizen Grievance Petition"):
                st.markdown(selected_t.get("report_text") or "No report text available.")

        st.markdown("</div>", unsafe_allow_html=True)

        # CSV Export for Municipal Reports
        st.markdown("<br>", unsafe_allow_html=True)
        csv_data = df_export.to_csv(index=False)
        st.download_button(
            label="📥 Export Filtered Municipal Incident Log (.csv)",
            data=csv_data,
            file_name=f"municipal_incident_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            use_container_width=True
        )

    else:
        st.info("No tickets found matching the selected filters.")


# =========================================================
# FOOTER
# =========================================================

st.markdown("""
<div class="portal-footer">
    <strong>CivicAlert AI | Public Infrastructure Citizen & Municipal Portal</strong><br>
    Deep Learning Vision (MobileNetV2), Real-Time Gemini LLM, & Municipal Dispatch Engine<br>
    Repository: <a href="https://github.com/zahidjan01a/AI-Powered-Public-Infrastructure-Issue-Detection-and-Reporting-System.git" target="_blank">zahidjan01a/AI-Powered-Public-Infrastructure-Issue-Detection-and-Reporting-System</a>
</div>
""", unsafe_allow_html=True)