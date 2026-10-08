
import unittest
from pathlib import Path
import sys

# Allow Python to import our producer module.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from producer.main import (
    SATELLITES,
    GROUND_STATIONS,
    generate_telemetry,
    simulate_reporting_cycles,
)


class TestTelemetryProducer(unittest.TestCase):


    def test_total_simulated_events(self):
        """The simulation generates exactly 37 events."""
        events = simulate_reporting_cycles()
        self.assertEqual(len(events), 37)

    def test_duplicate_event(self):
        """One event is retransmitted with the same ID."""
        events = simulate_reporting_cycles()
        event_ids = [event["event_id"] for event in events]
        self.assertEqual(len(event_ids), 37)
        self.assertEqual(len(set(event_ids)), 36)

    def test_malformed_battery_reading(self):
        """One simulated battery reading exceeds 100%."""
        events = simulate_reporting_cycles()
        malformed = [
            event for event in events
            if event["power"]["battery_level"] > 100
        ]
        self.assertEqual(len(malformed), 1)
        self.assertEqual(
            malformed[0]["power"]["battery_level"],
            150.0
        )


    def test_satellite_count(self):
        """The simulator defines 12 satellites."""
        self.assertEqual(len(SATELLITES), 12)
        self.assertEqual(len(set(SATELLITES)), 12)

    def test_ground_station_count(self):
        """The simulator defines four ground stations."""
        self.assertEqual(len(GROUND_STATIONS), 4)

    def test_telemetry_structure(self):
        """A generated event contains required fields."""
        event = generate_telemetry("SAT-001", "GS-001")

        required_fields = [
            "event_id",
            "satellite_id",
            "ground_station_id",
            "timestamp",
            "power",
            "thermal",
            "communications",
            "position",
        ]

        for field in required_fields:
            self.assertIn(field, event)

    def test_valid_battery_percentage(self):
        """Normal battery readings remain within 0–100%."""
        for _ in range(100):
            event = generate_telemetry("SAT-001", "GS-001")
            battery = event["power"]["battery_level"]

            self.assertGreaterEqual(battery, 0)
            self.assertLessEqual(battery, 100)

    def test_unique_event_ids(self):
        """Separately generated events have different IDs."""
        first = generate_telemetry("SAT-001", "GS-001")
        second = generate_telemetry("SAT-001", "GS-001")

        self.assertNotEqual(
            first["event_id"],
            second["event_id"],
        )

    def test_satellite_silence_and_recovery(self):
        """SAT-007 is silent in cycle 2 and recovers in cycle 3."""
        events = simulate_reporting_cycles()

        def satellite_reported(cycle):
            return any(
                event["satellite_id"] == "SAT-007"
                and event["reporting_cycle"] == cycle
                for event in events
            )

        self.assertTrue(satellite_reported(1))
        self.assertFalse(satellite_reported(2))
        self.assertTrue(satellite_reported(3))



if __name__ == "__main__":
    unittest.main()
