"""
AI-Powered Public Infrastructure Issue Detection and Reporting System
Source modules for preprocessing, prediction, department routing, GPS utilities, and LLM recommendation.
"""

from .preprocessing import preprocess_image, validate_image
from .prediction import load_classification_model, predict_infrastructure_issue, load_class_names
from .department_routing import get_department_recommendation
from .llm_recommendation import (
    generate_llm_recommendation,
    verify_gemini_api_key,
    call_gemini_rest_api,
    AVAILABLE_GEMINI_MODELS
)
from .gps_utils import (
    extract_gps_from_exif,
    format_coordinates,
    get_google_maps_link,
    get_map_dataframe,
    CITY_PRESETS
)
from .database import (
    init_db,
    insert_ticket,
    get_ticket_by_id,
    get_tickets,
    update_ticket_status,
    get_admin_metrics,
    export_tickets_df
)

__all__ = [
    "preprocess_image",
    "validate_image",
    "load_classification_model",
    "predict_infrastructure_issue",
    "load_class_names",
    "get_department_recommendation",
    "generate_llm_recommendation",
    "verify_gemini_api_key",
    "call_gemini_rest_api",
    "AVAILABLE_GEMINI_MODELS",
    "extract_gps_from_exif",
    "format_coordinates",
    "get_google_maps_link",
    "get_map_dataframe",
    "CITY_PRESETS",
    "init_db",
    "insert_ticket",
    "get_ticket_by_id",
    "get_tickets",
    "update_ticket_status",
    "get_admin_metrics",
    "export_tickets_df",
]
