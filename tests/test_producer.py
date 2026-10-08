
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
)


class TestTelemetryProducer(unittest.TestCase):

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


if __name__ == "__main__":
    unittest.main()
