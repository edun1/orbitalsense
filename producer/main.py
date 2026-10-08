
import json
import random
import uuid
from datetime import datetime, timezone


SATELLITES = [f"SAT-{i:03d}" for i in range(1, 13)]
GROUND_STATIONS = [f"GS-{i:03d}" for i in range(1, 5)]


def generate_telemetry(satellite_id, ground_station_id):
    """Generate one simulated satellite telemetry event."""

    return {
        "event_id": str(uuid.uuid4()),
        "satellite_id": satellite_id,
        "ground_station_id": ground_station_id,
        "timestamp": datetime.now(timezone.utc).isoformat(),
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




if __name__ == "__main__":

    for cycle in range(1, 4):
        events = []

        for index, satellite_id in enumerate(SATELLITES):

            # SAT-007 goes silent during cycle 2.
            if cycle == 2 and satellite_id == "SAT-007":
                continue

            ground_station_id = GROUND_STATIONS[
                index % len(GROUND_STATIONS)
            ]

            event = generate_telemetry(
                satellite_id,
                ground_station_id
            )

            events.append(event)

        # Inject failures into reporting cycle 2.
        if cycle == 2:

            # Malformed reading from SAT-003.
            malformed_event = generate_telemetry(
                "SAT-003", "GS-003"
            )
            malformed_event["power"]["battery_level"] = 150.0
            events.append(malformed_event)

            # Retransmit the original SAT-001 event.
            duplicate_event = events[0].copy()
            events.append(duplicate_event)

        # Print JSON records only.
        for event in events:
            event["reporting_cycle"] = cycle
            print(json.dumps(event))


