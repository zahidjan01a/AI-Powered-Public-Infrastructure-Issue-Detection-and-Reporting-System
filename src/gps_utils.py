"""
GPS metadata extraction and geolocation utilities for public infrastructure imagery.

This module provides:
1. EXIF metadata extraction to retrieve embedded GPS coordinates from camera photographs.
2. Conversion of DMS (Degrees, Minutes, Seconds) coordinates to decimal format.
3. Coordinate formatting and Google Maps URL generation.
4. City center presets for testing images lacking EXIF metadata.
"""

from typing import Dict, Optional, Tuple, Any
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
import pandas as pd


CITY_PRESETS: Dict[str, Tuple[float, float]] = {
    "New York, USA": (40.7128, -74.0060),
    "London, UK": (51.5074, -0.1278),
    "Karachi, Pakistan": (24.8607, 67.0011),
    "Tokyo, Japan": (35.6762, 139.6503),
    "Dubai, UAE": (25.2048, 55.2708),
    "Sydney, Australia": (-33.8688, 151.2093),
    "Toronto, Canada": (43.6532, -79.3832),
    "Berlin, Germany": (52.5200, 13.4050),
    "Mumbai, India": (19.0760, 72.8777)
}


def _dms_to_decimal(dms_tuple: Any) -> float:
    """
    Converts a (degrees, minutes, seconds) tuple or rational numbers into decimal degrees.
    """
    try:
        degrees = float(dms_tuple[0])
        minutes = float(dms_tuple[1])
        seconds = float(dms_tuple[2])
        return degrees + (minutes / 60.0) + (seconds / 3600.0)
    except Exception:
        return 0.0


def extract_gps_from_exif(image: Image.Image) -> Optional[Dict[str, float]]:
    """
    Attempts to extract latitude and longitude coordinates from an image's EXIF metadata.

    Args:
        image: PIL Image object.

    Returns:
        Optional[Dict[str, float]]: Dictionary containing 'latitude' and 'longitude' in decimal degrees,
                                   or None if no GPS tags are found.
    """
    if not hasattr(image, "getexif"):
        return None

    try:
        exif = image.getexif()
        if not exif:
            return None

        # GPS IFD is tag 34853 (0x8825)
        gps_ifd = exif.get_ifd(0x8825) if hasattr(exif, "get_ifd") else None

        # Fallback to legacy _getexif if get_ifd is empty
        if not gps_ifd and hasattr(image, "_getexif"):
            raw_exif = image._getexif()
            if raw_exif:
                for tag_id, val in raw_exif.items():
                    if TAGS.get(tag_id) == "GPSInfo":
                        gps_ifd = val
                        break

        if not gps_ifd:
            return None

        # Tag IDs in GPS IFD:
        # 1: GPSLatitudeRef ('N' or 'S')
        # 2: GPSLatitude (tuple of degrees, minutes, seconds)
        # 3: GPSLongitudeRef ('E' or 'W')
        # 4: GPSLongitude (tuple of degrees, minutes, seconds)
        lat_ref = gps_ifd.get(1) or gps_ifd.get("GPSLatitudeRef")
        lat_val = gps_ifd.get(2) or gps_ifd.get("GPSLatitude")
        lon_ref = gps_ifd.get(3) or gps_ifd.get("GPSLongitudeRef")
        lon_val = gps_ifd.get(4) or gps_ifd.get("GPSLongitude")

        if lat_ref and lat_val and lon_ref and lon_val:
            lat = _dms_to_decimal(lat_val)
            lon = _dms_to_decimal(lon_val)

            if str(lat_ref).strip().upper() == "S":
                lat = -lat
            if str(lon_ref).strip().upper() == "W":
                lon = -lon

            if -90.0 <= lat <= 90.0 and -180.0 <= lon <= 180.0 and (lat != 0.0 or lon != 0.0):
                return {
                    "latitude": round(lat, 6),
                    "longitude": round(lon, 6)
                }

    except Exception:
        return None

    return None


def format_coordinates(lat: float, lon: float) -> str:
    """
    Formats decimal coordinates into human-readable notation (e.g. '40.712800° N, 74.006000° W').
    """
    lat_cardinal = "N" if lat >= 0 else "S"
    lon_cardinal = "E" if lon >= 0 else "W"
    return f"{abs(lat):.6f}° {lat_cardinal}, {abs(lon):.6f}° {lon_cardinal}"


def get_google_maps_link(lat: float, lon: float) -> str:
    """
    Returns a clickable Google Maps navigation URL with a coordinate pin.
    """
    return f"https://www.google.com/maps?q={lat:.6f},{lon:.6f}"


def get_map_dataframe(lat: float, lon: float) -> pd.DataFrame:
    """
    Returns a pandas DataFrame formatted for Streamlit's `st.map` component.
    """
    return pd.DataFrame([{"lat": lat, "lon": lon}])
