
"""
Safe JSON parsing for OrbitalSense telemetry.
"""

import json


def parse_telemetry(message):
    """
    Parse a JSON telemetry message.

    Return a dictionary if parsing succeeds.
    Return None if the message is malformed
    or does not contain a JSON object.
    """
    try:
        event = json.loads(message)

        if not isinstance(event, dict):
            return None

        return event

    except (json.JSONDecodeError, TypeError):
        return None
