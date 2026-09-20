"""
Municipal department identification and routing module for public infrastructure issues.

This module maps detected visual conditions to relevant municipal authorities,
providing urgency classifications, departmental codes, SLAs, and response protocols.
"""

from typing import Dict, Any


DEPARTMENT_ROUTING_REGISTRY: Dict[str, Dict[str, Any]] = {
    "garbage": {
        "department_code": "WMD-SAN",
        "primary_department": "Municipal Solid Waste Management & Sanitation Department",
        "secondary_department": "City Environmental Health and Cleaning Bureau",
        "portal_channel": "Municipal Rapid Sanitation & Waste Disposal Unit",
        "contact_helpline": "City Line 311 / Sanitation Desk #4",
        "urgency_level": "Medium to High",
        "priority_tag": "Public Health & Environmental Sanitation Hazard",
        "estimated_sla": "24 to 48 Hours",
        "recommended_action": (
            "Dispatch municipal waste collection vehicle, clear accumulated solid waste, "
            "and sanitize the surrounding public area or disposal bins."
        ),
        "safety_notes": (
            "Accumulated garbage attracts disease-carrying vectors, creates odor nuisance, and poses hygiene risks. "
            "Pedestrians should avoid contact with uncovered waste materials."
        ),
        "citizen_advisory": (
            "Please refrain from dumping additional refuse in this area. "
            "Keep pets and children away from decomposing waste or glass."
        )
    },
    "pothole": {
        "department_code": "DPW-ROADS",
        "primary_department": "Department of Public Works & Road Maintenance Division",
        "secondary_department": "Municipal Highway & Traffic Safety Authority",
        "portal_channel": "Emergency Pavement Repair & Rapid Response Team",
        "contact_helpline": "City Line 311 / Road Hazard Desk #1",
        "urgency_level": "High",
        "priority_tag": "Traffic Safety & Vehicular Hazard",
        "estimated_sla": "24 to 72 Hours",
        "recommended_action": (
            "Deploy emergency road repair crew to place high-visibility hazard cones, "
            "excavate loose aggregate, and apply hot/cold mix asphalt patch compaction."
        ),
        "safety_notes": (
            "Open potholes cause severe vehicle tire blowouts, rim damage, suspension breakage, "
            "and severe tipping hazards for motorcyclists and cyclists."
        ),
        "citizen_advisory": (
            "Slow down when approaching this road section. Avoid swerving into opposing traffic lanes "
            "to bypass the hazard."
        )
    },
    "road_crack": {
        "department_code": "HEM-CRACK",
        "primary_department": "Highways Engineering & Road Asset Maintenance Bureau",
        "secondary_department": "Municipal Civil Infrastructure Department",
        "portal_channel": "Pavement Preservation & Preventative Maintenance Division",
        "contact_helpline": "City Line 311 / Infrastructure Desk #2",
        "urgency_level": "Medium",
        "priority_tag": "Preventative Infrastructure Maintenance",
        "estimated_sla": "5 to 7 Business Days",
        "recommended_action": (
            "Perform surface inspection to classify crack depth. Apply hot-pour rubberized "
            "bituminous sealant to block moisture intrusion and prevent pothole formation."
        ),
        "safety_notes": (
            "Cracks are early indicators of sub-base degradation. If left unsealed, water penetration "
            "and freeze-thaw cycles will accelerate deterioration into major potholes."
        ),
        "citizen_advisory": (
            "Roadway remains navigable at standard speed limits. Exercise caution during rainy weather "
            "as standing water may conceal deeper longitudinal cracks."
        )
    },
    "normal": {
        "department_code": "CID-ROUTINE",
        "primary_department": "Municipal Civil Infrastructure Directorate",
        "secondary_department": "Routine Public Assets Monitoring Bureau",
        "portal_channel": "General Infrastructure Asset Registry",
        "contact_helpline": "City Line 311 / Asset Information Desk",
        "urgency_level": "None / Routine",
        "priority_tag": "Routine Maintenance Schedule",
        "estimated_sla": "Standard Maintenance Cycle",
        "recommended_action": (
            "No immediate emergency repair is required. Record visual condition into the municipal "
            "infrastructure asset registry for periodic quarterly re-inspection."
        ),
        "safety_notes": (
            "Infrastructure asset appears structurally intact without visible distress, obstruction, or hazards."
        ),
        "citizen_advisory": (
            "No hazard detected. The public roadway or facility is operating under normal, safe conditions."
        )
    }
}


from typing import Dict, Any, Optional


def get_department_recommendation(
    predicted_class: str,
    confidence: float = 0.0,
    location: Optional[str] = None,
    **kwargs
) -> Dict[str, Any]:
    """
    Retrieves the municipal department routing details and recommendations for a given class.

    Args:
        predicted_class: Predicted class label ('garbage', 'normal', 'pothole', 'road_crack').
        confidence: Confidence score percentage (0.0 to 100.0) or ratio.
        location: Optional location name or landmark.

    Returns:
        Dict[str, Any]: Comprehensive routing and advisory profile with all aliases.
    """
    key = predicted_class.lower().strip()
    data = DEPARTMENT_ROUTING_REGISTRY.get(key, DEPARTMENT_ROUTING_REGISTRY["normal"]).copy()

    data["predicted_class"] = key
    data["confidence"] = confidence
    data["location"] = location or "Unspecified Municipal Sector"

    # Synchronize UI aliases
    data["sub_department"] = data.get("secondary_department", "City Public Works Bureau")
    data["urgency_tier"] = data.get("urgency_level", "Medium to High")
    data["emergency_helpline"] = data.get("contact_helpline", "City Line 311")

    return data

