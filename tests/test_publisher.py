
import json
import unittest
from unittest.mock import MagicMock

from producer.main import generate_telemetry
from producer.publisher import publish_telemetry


class TestTelemetryPublisher(unittest.TestCase):

    def test_publish_telemetry(self):
        """Verify telemetry is correctly prepared for Pub/Sub."""

        event = generate_telemetry("SAT-001", "GS-001")

        fake_publisher = MagicMock()
        fake_publisher.topic_path.return_value = (
            "projects/test-project/topics/test-telemetry"
        )
        fake_publisher.publish.return_value.result.return_value = (
            "message-123"
        )

        message_id = publish_telemetry(
            "test-project",
            "test-telemetry",
            event,
            publisher=fake_publisher
        )

        fake_publisher.topic_path.assert_called_once_with(
            "test-project",
            "test-telemetry"
        )

        fake_publisher.publish.assert_called_once()

        args, kwargs = fake_publisher.publish.call_args

        self.assertEqual(
            args[0],
            "projects/test-project/topics/test-telemetry"
        )

        self.assertEqual(
            json.loads(args[1].decode("utf-8")),
            event
        )

        self.assertEqual(message_id, "message-123")


if __name__ == "__main__":
    unittest.main()
