
"""
OrbitalSense telemetry deduplication.
"""

def remove_duplicates(events):
    seen_ids = set()
    unique_events = []
    duplicate_events = []

    for event in events:
        event_id = event["event_id"]

        if event_id in seen_ids:
            duplicate_events.append(event)
        else:
            seen_ids.add(event_id)
            unique_events.append(event)

    return unique_events, duplicate_events
