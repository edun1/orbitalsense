
import json
import random
import uuid
from datetime import datetime, timezone, timedelta


SATELLITES = [f"SAT-{i:03d}" for i in range(1, 13)]
GROUND_STATIONS = [f"GS-{i:03d}" for i in range(1, 5)]


def generate_telemetry(satellite_id, ground_station_id):

    """Generate one simulated satellite telemetry event."""

    # Record when the satellite generates telemetry
    event_time = datetime.now(timezone.utc)

    # Simulate delivery delays between 0 and 15 minutes
    delay_seconds = random.randint(0, 900)

    # Calculate when the ground station receives the message
    arrival_time = event_time + timedelta(seconds=delay_seconds)

    return {

        "event_id": str(uuid.uuid4()),
        "satellite_id": satellite_id,
        "ground_station_id": ground_station_id,
       "timestamp": event_time.isoformat(),
"arrival_timestamp": arrival_time.isoformat(),
        "power": {
            "battery_voltage": round(random.uniform(24.0, 32.0), 2),
            "battery_level": round(random.uniform(40.0, 100.0), 2)
        },
        "thermal": {
            "temperature_c": round(random.uniform(-20.0, 60.0), 2)
        },
        "communications": {
            "signal_strength_dbm": round(
                random.uniform(-110.0, -50.0), 2
            )
        },
        "position": {
            "latitude": round(random.uniform(-90.0, 90.0), 4),
            "longitude": round(random.uniform(-180.0, 180.0), 4),
            "altitude_km": round(random.uniform(400.0, 600.0), 2)
        }
    }





def simulate_reporting_cycles():
    """Simulate three reporting cycles with controlled failures."""
    all_events = []

    for cycle in range(1, 4):
        events = []

        for index, satellite_id in enumerate(SATELLITES):
            # SAT-007 stops transmitting during cycle 2.
            if cycle == 2 and satellite_id == "SAT-007":
                continue

            ground_station_id = GROUND_STATIONS[
                index % len(GROUND_STATIONS)
            ]

            event = generate_telemetry(
                satellite_id,
                ground_station_id
            )

            event["reporting_cycle"] = cycle
            events.append(event)

        if cycle == 2:
            # Inject a malformed reading from SAT-003.
            malformed_event = generate_telemetry(
                "SAT-003", "GS-003"
            )
            malformed_event["power"]["battery_level"] = 150.0
            malformed_event["reporting_cycle"] = cycle
            events.append(malformed_event)

            # Retransmit an existing event without changing its identity.
            duplicate_event = events[0].copy()
            events.append(duplicate_event)

        all_events.extend(events)

    return all_events


if __name__ == "__main__":
    for event in simulate_reporting_cycles():
        print(json.dumps(event))
