import os
import sys
import time
from datetime import datetime
from pathlib import Path
import pandas as pd
import streamlit as st

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import importlib
import src
import src.database

importlib.reload(src.database)
importlib.reload(src)

# Ensure database is initialized
src.init_db()

# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Municipal Operations Console | CivicAlert AI",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# PROFESSIONAL MUNICIPAL EXECUTIVE THEME (DARK NAVY / SLATE)
# =========================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    color: #0f172a;
}

.admin-header {
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0369a1 100%);
    color: white;
    padding: 2.2rem 2.5rem;
    border-radius: 18px;
    margin-bottom: 2rem;
    box-shadow: 0 10px 25px -5px rgba(15, 23, 42, 0.25);
    border: 1px solid rgba(255, 255, 255, 0.1);
}

.admin-header h1 {
    font-size: 2.2rem;
    font-weight: 800;
    margin: 0.3rem 0;
    color: #ffffff;
    letter-spacing: -0.02em;
}

.admin-header p {
    font-size: 1.05rem;
    color: #cbd5e1;
    margin: 0;
    max-width: 850px;
    line-height: 1.5;
}

.admin-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(3, 105, 161, 0.35);
    color: #38bdf8;
    padding: 4px 12px;
    border-radius: 9999px;
    font-size: 0.8rem;
    font-weight: 700;
    letter-spacing: 0.04em;
    text-transform: uppercase;
    border: 1px solid rgba(56, 189, 248, 0.4);
    margin-bottom: 0.6rem;
}

.kpi-container {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 16px;
    margin-bottom: 2rem;
}

.kpi-card {
    background: #ffffff;
    border-radius: 14px;
    padding: 1.4rem 1.2rem;
    box-shadow: 0 4px 12px rgba(15, 23, 42, 0.05);
    border: 1px solid #e2e8f0;
    text-align: center;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.kpi-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 20px rgba(15, 23, 42, 0.08);
}

.kpi-value {
    font-size: 2.4rem;
    font-weight: 800;
    line-height: 1.1;
    margin-bottom: 0.3rem;
}

.kpi-label {
    font-size: 0.82rem;
    font-weight: 600;
    color: #64748b;
    text-transform: uppercase;
    letter-spacing: 0.04em;
}

.step-card {
    background: #ffffff;
    border-radius: 16px;
    padding: 1.6rem 2rem;
    margin-bottom: 1.8rem;
    border: 1px solid #e2e8f0;
    box-shadow: 0 4px 14px rgba(15, 23, 42, 0.04);
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
    display: flex;
    align-items: center;
    justify-content: center;
    width: 34px;
    height: 34px;
    background: #0284c7;
    color: white;
    border-radius: 10px;
    font-weight: 800;
    font-size: 0.95rem;
}

.badge-status {
    display: inline-block;
    padding: 4px 10px;
    border-radius: 9999px;
    font-size: 0.75rem;
    font-weight: 700;
    text-transform: uppercase;
}
.badge-submitted { background: #fee2e2; color: #991b1b; }
.badge-underreview { background: #fef3c7; color: #92400e; }
.badge-crewdispatched { background: #e0e7ff; color: #3730a3; }
.badge-inprogress { background: #dbeafe; color: #1e40af; }
.badge-resolved { background: #d1fae5; color: #065f46; }

.auth-box {
    background: #ffffff;
    border-radius: 18px;
    padding: 2.5rem;
    max-width: 520px;
    margin: 3rem auto;
    border: 1px solid #e2e8f0;
    box-shadow: 0 15px 35px -5px rgba(15, 23, 42, 0.12);
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# AUTHENTICATION STATE
# =========================================================

DEFAULT_ADMIN_PIN = "admin2026"

if "admin_authenticated" not in st.session_state:
    st.session_state.admin_authenticated = False

if "admin_user" not in st.session_state:
    st.session_state.admin_user = ""

# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/smart-city.png", width=56)
    st.markdown("### CivicAlert AI 🏛️")
    st.markdown("**Municipal Operations Console**")
    st.caption("Restricted City Official Access")
    st.markdown("---")

    if st.session_state.admin_authenticated:
        st.success(f"👤 Logged In: **{st.session_state.admin_user}**")
        st.caption("Role: Municipal Operations Supervisor")
        
        if st.button("🚪 Sign Out", use_container_width=True):
            st.session_state.admin_authenticated = False
            st.session_state.admin_user = ""
            st.rerun()

        st.markdown("---")
        st.markdown("#### ⚡ Quick Actions")
        if st.button("🔄 Refresh Defect Database", use_container_width=True):
            st.rerun()

    else:
        st.info("🔒 Authentication required to access city operations database.")

    st.markdown("---")
    st.caption("CivicAlert AI Municipal Edition v2.6.0")
    st.caption("SQLite DB: `data/tickets.db`")


# =========================================================
# MAIN VIEW: LOGIN GATE vs CONSOLE
# =========================================================

if not st.session_state.admin_authenticated:
    st.markdown("""
    <div class="auth-box">
        <div style="font-size: 3rem; margin-bottom: 0.5rem;">🏛️</div>
        <h2 style="font-weight: 800; color: #0f172a; margin-bottom: 0.5rem;">Municipal Official Login</h2>
        <p style="color: #64748b; font-size: 0.95rem; margin-bottom: 1.8rem;">
            Please enter your municipal staff credentials or operational security passkey to access the city defect registry and dispatch controls.
        </p>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns([1, 1.2, 1])
    with c2:
        username_input = st.text_input("Officer Name / Badge ID:", value="Eng. Zahid Jan (Operations Lead)")
        pin_input = st.text_input("Municipal Access Passkey:", type="password", placeholder="Enter official passkey (Default: admin2026)")
        
        if st.button("🔓 Authenticate & Open Command Console", type="primary", use_container_width=True):
            if pin_input.strip() == DEFAULT_ADMIN_PIN or pin_input.strip().lower() == "admin":
                st.session_state.admin_authenticated = True
                st.session_state.admin_user = username_input.strip() or "City Official"
                st.toast("✅ Authentication successful. Welcome to Municipal Console.", icon="🏛️")
                time.sleep(0.4)
                st.rerun()
            else:
                st.error("❌ Invalid passkey. Authorized municipal personnel only.")
                st.caption("Demo Passkey: `admin2026`")

    st.stop()


# =========================================================
# AUTHENTICATED MUNICIPAL CONSOLE
# =========================================================

st.markdown(f"""
<div class="admin-header">
    <div class="admin-badge">🏛️ Internal Municipal Command & Operations Console</div>
    <h1>City Infrastructure Incident Registry 📊</h1>
    <p>
        Authorized Supervisor: <strong>{st.session_state.admin_user}</strong> | Real-time centralized grievance monitoring, automated AI diagnosis triage, rapid field repair dispatch, and municipal resolution tracking.
    </p>
</div>
""", unsafe_allow_html=True)

# Fetch latest database metrics
metrics = src.get_admin_metrics()

# Top KPI Metric Cards
st.markdown(f"""
<div class="kpi-container">
    <div class="kpi-card" style="border-top:4px solid #2563eb;">
        <div class="kpi-value" style="color:#2563eb;">{metrics['total_tickets']}</div>
        <div class="kpi-label">📋 Total Reports Logged</div>
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
        <div class="kpi-label">⏱️ SLA Compliance</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Filter Controls
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
        "Responsible Department Agency:",
        options=list(dept_options.keys()),
        format_func=lambda x: dept_options[x]
    )

with f_col2:
    status_options = ["ALL", "Submitted", "Under Review", "Crew Dispatched", "In Progress", "Resolved"]
    status_filter = st.selectbox("Operational Lifecycle Status:", status_options)

with f_col3:
    search_query = st.text_input("Live Search Location or Ticket ID:", placeholder="e.g. Charsadda, Pothole, REF-2026")

st.markdown("</div>", unsafe_allow_html=True)

# Query SQLite database
tickets_list = src.get_tickets(dept_code=dept_filter, status=status_filter, search=search_query)

st.markdown(f"### 📋 Active Incidents & Work-Orders ({len(tickets_list)} records)")

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
    <div class="step-card" style="border-top:4px solid #0284c7;">
        <div class="step-title">
            <span class="step-number">🛠️</span>
            <span>Operational Triage & Field Crew Dispatch</span>
        </div>
    """, unsafe_allow_html=True)

    ticket_choices = {
        t["ticket_id"]: f"{t['ticket_id']} — {t['category']} @ {t['location']} [{t['status']}]"
        for t in tickets_list
    }
    selected_tid = st.selectbox("Select Ticket to Triage or Update:", options=list(ticket_choices.keys()), format_func=lambda x: ticket_choices[x])

    selected_t = next((t for t in tickets_list if t["ticket_id"] == selected_tid), None)

    if selected_t:
        act_col1, act_col2 = st.columns([1, 1.2])

        with act_col1:
            st.markdown(f"""
            <div style="background:#f8fafc; padding:1.2rem; border-radius:12px; border:1px solid #e2e8f0;">
                <span style="font-size:0.8rem; color:#64748b; font-weight:700;">INCIDENT SPECIFICATIONS</span><br>
                <strong>Reference ID:</strong> <code>{selected_t['ticket_id']}</code><br>
                <strong>Category:</strong> {selected_t['category']} ({selected_t['confidence']:.1f}% AI Conf)<br>
                <strong>Location:</strong> {selected_t['location']}<br>
                <strong>Agency:</strong> {selected_t['department']}<br>
                <strong>Urgency Tier:</strong> {selected_t['urgency']} | <strong>Target SLA:</strong> {selected_t['sla']}<br>
                <strong>Current Status:</strong> <span class="badge-status badge-{selected_t['status'].lower().replace(' ', '')}">{selected_t['status']}</span>
            </div>
            """, unsafe_allow_html=True)

        with act_col2:
            status_choices = ["Submitted", "Under Review", "Crew Dispatched", "In Progress", "Resolved"]
            current_idx = status_choices.index(selected_t["status"]) if selected_t["status"] in status_choices else 0

            new_st = st.selectbox("Assign New Operational Status:", status_choices, index=current_idx)
            new_notes = st.text_area(
                "Supervisor & Field Crew Notes (Visible to Citizen):",
                value=selected_t.get("admin_notes") or "",
                placeholder="Log dispatch orders, crew assigned, vehicle license, or completion verification details."
            )

            if st.button("💾 Apply Operational Status Update", type="primary", use_container_width=True):
                success = src.update_ticket_status(selected_tid, new_st, new_notes)
                if success:
                    st.success(f"✅ Ticket {selected_tid} updated to '{new_st}' successfully!")
                    time.sleep(0.5)
                    st.rerun()
                else:
                    st.error("Failed to update status in database.")

        with st.expander("📄 View Full Citizen Grievance & Technical Petition"):
            st.markdown(selected_t.get("report_text") or "No report text available.")

    st.markdown("</div>", unsafe_allow_html=True)

    # CSV Export
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

# Footer
st.markdown("""
<br><hr>
<div style="text-align: center; color: #64748b; font-size: 0.85rem; padding: 1rem 0;">
    <strong>CivicAlert AI | Municipal Administration & Operations Console</strong><br>
    Restricted Municipal Staff Dashboard & Dispatch Center
</div>
""", unsafe_allow_html=True)
