
"""
OrbitalSense telemetry freshness checks.
"""

from datetime import datetime, timezone


def calculate_delay_seconds(event_timestamp, arrival_timestamp):
    """
    Calculate the delay between telemetry generation
    and arrival at the processing system.
    """

    event_time = datetime.fromisoformat(
        event_timestamp.replace("Z", "+00:00")
    )

    arrival_time = datetime.fromisoformat(
        arrival_timestamp.replace("Z", "+00:00")
    )

    if event_time.tzinfo is None or arrival_time.tzinfo is None:
        raise ValueError("Both timestamps must include a timezone")

    delay = arrival_time - event_time

    return delay.total_seconds()

def classify_freshness(event_timestamp, arrival_timestamp, threshold_seconds=300):
    """
    Classify telemetry based on its arrival delay.

    300 seconds = 5 minutes.
    """

    delay = calculate_delay_seconds(
        event_timestamp,
        arrival_timestamp
    )

    if delay < 0:
        return "future_timestamp"

    if delay <= threshold_seconds:
        return "on_time"

    return "late"

def calculate_freshness_metrics(events):
    """
    Calculate telemetry freshness performance metrics.
    """

    total = len(events)

    on_time = sum(
        event.get("freshness_status") == "on_time"
        for event in events
    )

    late = sum(
        event.get("freshness_status") == "late"
        for event in events
    )

    freshness_rate = (
        round((on_time / total) * 100, 2)
        if total > 0 else 0.0
    )

    return {
        "total_events": total,
        "on_time": on_time,
        "late": late,
        "freshness_rate_percent": freshness_rate
    }
