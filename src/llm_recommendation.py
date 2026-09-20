"""
Real-time LLM-powered recommendation and issue-reporting generation module.

This module generates comprehensive, real-time citizen-to-department infrastructure reports,
recommends responsible municipal authorities, and formats official submission tickets.

Capabilities:
1. Live real-time LLM generation via Google Gemini REST API using the user's API key
   (supporting gemini-1.5-flash, gemini-2.0-flash, gemini-1.5-pro).
2. Citizen-first reporting format addressed directly to the responsible municipal department.
3. Natural location context (street address, neighborhood, landmark) without raw coordinate clutter.
4. Resilient deterministic Expert Advisory Engine providing full structured reports offline
   if an API key is not supplied or network connectivity is unavailable.
"""

import os
import random
from typing import Dict, Any, Optional, Tuple
import requests


DEFAULT_GEMINI_MODEL = "gemini-1.5-flash"
AVAILABLE_GEMINI_MODELS = [
    "gemini-1.5-flash",
    "gemini-2.0-flash",
    "gemini-1.5-pro"
]


def verify_gemini_api_key(api_key: str) -> Tuple[bool, str]:
    """
    Verifies the validity of a Gemini API key by making a lightweight ping to the Google API.

    Args:
        api_key: Google Gemini API key string.

    Returns:
        Tuple[bool, str]: (Success bool, Message description)
    """
    if not api_key or not api_key.strip():
        return False, "API key cannot be empty."

    clean_key = api_key.strip()
    url = f"https://generativelanguage.googleapis.com/v1beta/models?key={clean_key}"

    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return True, "API Key is valid and connected to Google Gemini!"
        elif response.status_code == 400:
            error_data = response.json().get("error", {})
            return False, f"API Error: {error_data.get('message', 'Invalid API key or request parameters.')}"
        elif response.status_code == 403:
            return False, "Permission denied. Check that the Gemini API is enabled for this key."
        else:
            return False, f"Connection returned HTTP status {response.status_code}."
    except requests.exceptions.Timeout:
        return False, "Connection timed out while verifying API key with Google servers."
    except Exception as e:
        return False, f"Connection error: {str(e)}"


def call_gemini_rest_api(
    prompt: str,
    api_key: str,
    model_name: str = DEFAULT_GEMINI_MODEL
) -> str:
    """
    Calls the Google Generative Language REST API directly using requests.

    Args:
        prompt: System and contextual prompt text.
        api_key: Gemini API key.
        model_name: Name of the Gemini model to invoke.

    Returns:
        str: Generated markdown text.

    Raises:
        Exception: If the API call fails or returns an error.
    """
    clean_key = api_key.strip()
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={clean_key}"
    headers = {"Content-Type": "application/json"}

    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }],
        "generationConfig": {
            "temperature": 0.35,
            "maxOutputTokens": 1500
        }
    }

    response = requests.post(url, headers=headers, json=payload, timeout=35)

    if response.status_code == 200:
        data = response.json()
        candidates = data.get("candidates", [])
        if candidates:
            parts = candidates[0].get("content", {}).get("parts", [])
            if parts:
                return parts[0].get("text", "").strip()
        raise ValueError("API returned response without candidates.")
    else:
        error_info = response.json().get("error", {})
        err_msg = error_info.get("message", f"HTTP {response.status_code}")
        raise RuntimeError(f"Google Gemini API error ({response.status_code}): {err_msg}")


def _generate_expert_rule_based_report(
    predicted_class: str,
    confidence: float,
    dept_info: Dict[str, Any],
    citizen_location: Optional[str] = None
) -> str:
    """
    Generates a structured citizen-to-department incident report offline.
    """
    class_title = predicted_class.replace("_", " ").title()
    loc_display = citizen_location.strip() if (citizen_location and citizen_location.strip()) else "Location to be confirmed on-site"
    dept_code = dept_info.get("department_code", "GEN-CIVIC")
    primary_dept = dept_info.get("primary_department", "Municipal Infrastructure Department")
    secondary_dept = dept_info.get("secondary_department", dept_info.get("sub_department", "Operations Bureau"))
    urgency_lvl = dept_info.get("urgency_level", dept_info.get("urgency_tier", "Medium"))
    priority_tag = dept_info.get("priority_tag", "Civil Maintenance")
    sla_time = dept_info.get("estimated_sla", "24 to 48 Hours")
    action_plan = dept_info.get("recommended_action", "Inspect site and deploy remediation crew.")
    safety_info = dept_info.get("safety_notes", "Avoid contact with damaged infrastructure area.")
    advisory_info = dept_info.get("citizen_advisory", "Exercise caution around affected road section.")

    if predicted_class == "normal":
        return f"""### 🏛️ Official Municipal Infrastructure Inspection Record
**Addressed To**: {primary_dept}  
**Coordinating Agency**: {secondary_dept}  
**Departmental Unit**: {dept_info.get('portal_channel', 'Civil Asset Registry')}  
**Reported Location**: **{loc_display}**  
**Assessment Result**: **{class_title} Infrastructure** (AI Confidence: `{confidence:.2f}%`)

---

#### 1. Citizen Observation & AI Verification
A photograph of the public roadway/facility was submitted for automated civil inspection. The deep-learning vision diagnostic confirms that the infrastructure at **{loc_display}** is in sound operational condition with no critical pavement cavities, structural cracks, or uncollected refuse piles.

#### 2. Departmental Handling
- **Priority Tier**: Routine / Informational
- **Action Required**: Record photographic verification into the municipal GIS asset registry for periodic scheduled maintenance.
- **Citizen Notice**: The roadway or public area is safe for normal vehicular and pedestrian transit.

---
*Generated via Built-in Expert Civil Advisory Engine | CivicConnect Platform*
"""

    return f"""### 🏛️ Official Citizen Grievance & Infrastructure Report
**Addressed To**: {primary_dept}  
**Coordinating Agency**: {secondary_dept}  
**Department Unit**: {dept_info.get('portal_channel', 'Municipal Operations Desk')}  
**Incident Location**: **{loc_display}**  
**Verified Issue**: **{class_title}** (AI Verification Confidence: `{confidence:.2f}%`)  
**Urgency Tier**: **{urgency_lvl}** ({priority_tag})

---

#### 1. Incident Overview & Problem Statement
A citizen report supported by photographic evidence was captured at **{loc_display}**. Automated visual analysis verified an infrastructure defect classified as **{class_title}**.
- **Community Safety Impact**: {safety_info}
- **Citizen Guidance**: {advisory_info}

#### 2. Requested Municipal Action & Intervention
The responsible municipal department is respectfully urged to take the following operational measures:
1. **Immediate Precaution**: Dispatch field personnel to place protective safety markers or temporary signage around the affected zone.
2. **Remediation Plan**: {action_plan}
3. **Turnaround SLA**: Address and resolve this defect within the standard **{sla_time}** resolution window.

#### 3. Formal Departmental Submission Summary
```text
[MUNICIPAL SERVICE REQUEST - {dept_code}]
Department: {primary_dept}
Incident Category: {class_title}
Urgency Level: {urgency_lvl}
Verified Location: {loc_display}
Target Response SLA: {sla_time}
Action Requested: Inspect site and deploy municipal response crew per standard protocols.
```

---
*Generated via Built-in Expert Civil Advisory Engine | CivicConnect Platform*
"""


def generate_llm_recommendation(
    predicted_class: Optional[str] = None,
    confidence: float = 0.0,
    dept_info: Optional[Dict[str, Any]] = None,
    api_key: Optional[str] = None,
    citizen_location: Optional[str] = None,
    model_name: str = DEFAULT_GEMINI_MODEL,
    provider: str = "auto",
    *args,
    issue_type: Optional[str] = None,
    location: Optional[str] = None,
    department_info: Optional[Dict[str, Any]] = None,
    **kwargs
) -> str:
    """
    Generates a live citizen-to-department grievance report using Google Gemini or the offline expert engine.
    Universally accepts all parameter aliases and calling conventions.
    """
    # Handle any positional args if passed dynamically
    if args:
        for i, val in enumerate(args):
            if i == 0 and predicted_class is None:
                predicted_class = val
            elif i == 1 and confidence == 0.0:
                confidence = val
            elif i == 2 and dept_info is None and isinstance(val, dict):
                dept_info = val
            elif i == 2 and citizen_location is None and isinstance(val, str):
                citizen_location = val
            elif i == 3 and citizen_location is None and isinstance(val, str):
                citizen_location = val

    # Resolve aliases gracefully
    pred_class = (
        predicted_class
        or issue_type
        or kwargs.get("issue_type")
        or kwargs.get("category")
        or "normal"
    )
    conf_val = confidence if confidence > 0.0 else kwargs.get("confidence_score", 0.0)
    conf_percent = float(conf_val * 100.0 if conf_val <= 1.0 else conf_val)

    resolved_dept_info = (
        dept_info
        or department_info
        or kwargs.get("department_info")
        or kwargs.get("dept_info")
        or {}
    )
    department_info = resolved_dept_info
    if not department_info:
        from .department_routing import get_department_recommendation
        department_info = get_department_recommendation(pred_class, conf_percent)

    raw_loc = (
        citizen_location
        or location
        or kwargs.get("location")
        or kwargs.get("citizen_location")
        or kwargs.get("incident_location")
        or ""
    )
    loc_text = raw_loc.strip() if raw_loc.strip() else "Civic roadway / public location"

    gemini_key = api_key or os.environ.get("GEMINI_API_KEY")

    if provider != "offline" and gemini_key and gemini_key.strip():
        primary_dept = department_info.get('primary_department', 'Municipal Services')
        sec_dept = department_info.get('secondary_department', 'Operations Division')
        urg_lvl = department_info.get('urgency_level', 'Medium')
        pri_tag = department_info.get('priority_tag', 'Public Infrastructure Hazard')
        sla_val = department_info.get('estimated_sla', '24 to 48 Hours')
        action_val = department_info.get('recommended_action', 'Inspect and repair.')

        prompt = f"""
You are a municipal citizen advocate writing a formal, polished public infrastructure grievance and work-order request on behalf of a citizen.
The issue was photographed and automatically verified by an AI computer vision system:

- Detected Condition: {pred_class.replace('_', ' ').title()}
- Vision Verification Confidence: {conf_percent:.2f}%
- Addressed To Department: {primary_dept}
- Coordinating Unit: {sec_dept}
- Urgency Level: {urg_lvl} ({pri_tag})
- Standard Resolution SLA: {sla_val}
- Citizen's Stated Location: {loc_text}
- Recommended Field Action: {action_val}

Write a formal, highly professional Citizen Incident Report in Markdown formatting addressed directly to the responsible municipal department:
1. **Department Header & Formal Subject Line**: Addressed to {primary_dept}.
2. **Citizen Statement & Visual Verification**: Clearly state what was photographed at {loc_text} and verified by AI.
3. **Public Health & Neighborhood Safety Assessment**: Highlight the immediate risks (e.g. hygiene hazard, road safety, vehicle damage, pedestrian hazard).
4. **Action Requested from Municipal Department**: List concrete operational remediation steps and urge completion within {sla_val}.
5. **Citizen Safety Notice**: Advice for local residents and motorists in the area.
6. **Formal Service Request Draft**: A clean, formatted municipal complaint template inside a code block ready for official logging.

Keep the tone formal, respectful, urgent, and constructive.
"""
        try:
            live_report = call_gemini_rest_api(
                prompt=prompt,
                api_key=gemini_key,
                model_name=model_name
            )
            return f"""> ⚡ **Live Real-Time Generation via Google Gemini (`{model_name}`)**  
> *Customized in real time for `{primary_dept}`.*

{live_report}
"""
        except Exception as e:
            fallback_report = _generate_expert_rule_based_report(
                pred_class, conf_percent, department_info, loc_text
            )
            return f"""> ⚠️ **Live LLM Notice**: Unable to query Google Gemini live ({str(e)}).  
> *Displaying report compiled by the Built-in Expert Civil Advisory Engine:*

{fallback_report}
"""

    # Offline / Default Expert Engine
    offline_notice = (
        "> 💡 **Mode: Built-in Expert Civil Advisory Engine**  \n"
        "> *Tip: Enter your Google Gemini API key in the left sidebar for live, dynamic AI report drafting.*"
    )
    return f"""{offline_notice}

{_generate_expert_rule_based_report(pred_class, conf_percent, department_info, loc_text)}
"""

