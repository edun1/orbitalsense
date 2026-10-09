
"""
OrbitalSense telemetry validation rules.
"""

import math
from datetime import datetime


# Registered OrbitalSense satellites
VALID_SATELLITES = {
    f"SAT-{number:03d}"
    for number in range(1, 13)
}

# Registered OrbitalSense ground stations
VALID_GROUND_STATIONS = {
    f"GS-{number:03d}"
    for number in range(1, 5)
}


def validate_telemetry(event):
    """
    Validate essential satellite telemetry fields.
    Return True for valid events and False otherwise.
    """

    if not isinstance(event, dict):
        return False

    # Check required identifiers
    required_fields = [
        "event_id",
        "satellite_id",
        "ground_station_id",
        "timestamp",
    ]

    for field in required_fields:
        if not isinstance(event.get(field), str):
            return False

        if not event[field].strip():
            return False

    # Validate timestamp format and timezone
    try:
        timestamp = event["timestamp"]

        parsed_timestamp = datetime.fromisoformat(
            timestamp.replace("Z", "+00:00")
        )

        if parsed_timestamp.tzinfo is None:
            return False

    except (ValueError, TypeError):
        return False

    # Validate satellite identifier
    if event["satellite_id"] not in VALID_SATELLITES:
        return False

    # Validate ground station identifier
    if event["ground_station_id"] not in VALID_GROUND_STATIONS:
        return False

    # Check power measurements
    power = event.get("power")

    if not isinstance(power, dict):
        return False

    battery_level = power.get("battery_level")

    if isinstance(battery_level, bool):
        return False

    if not isinstance(battery_level, (int, float)):
        return False

    if not math.isfinite(battery_level):
        return False

    if not 0 <= battery_level <= 100:
        return False

    return True
