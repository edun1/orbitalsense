
import json
import unittest
from io import StringIO
from unittest.mock import patch

from producer.run import run_producer


class TestProducerRun(unittest.TestCase):

    @patch.dict("os.environ", {"PUBLISH_MODE": "local"})
    @patch("sys.stdout", new_callable=StringIO)
    @patch("producer.run.publish_telemetry")
    def test_local_mode(self, mock_publish, mock_stdout):
        """Local mode generates 37 events without publishing."""

        run_producer()

        output = mock_stdout.getvalue().splitlines()

        self.assertEqual(len(output), 37)

        for line in output:
            event = json.loads(line)
            self.assertIn("satellite_id", event)

        mock_publish.assert_not_called()

    @patch.dict(
        "os.environ",
        {
            "PUBLISH_MODE": "cloud",
            "GCP_PROJECT_ID": "",
            "PUBSUB_TOPIC_ID": ""
        }
    )
    def test_cloud_mode_requires_configuration(self):
        """Cloud mode rejects missing project and topic IDs."""

        with self.assertRaises(ValueError):
            run_producer()

    @patch.dict("os.environ", {"PUBLISH_MODE": "invalid"})
    def test_invalid_mode(self):
        """An unsupported publishing mode is rejected."""

        with self.assertRaises(ValueError):
            run_producer()

    @patch.dict(
        "os.environ",
        {
            "PUBLISH_MODE": "cloud",
            "GCP_PROJECT_ID": "test-project",
            "PUBSUB_TOPIC_ID": "test-telemetry"
        }
    )
    @patch("producer.run.publish_telemetry")
    def test_cloud_mode_publishes_events(self, mock_publish):
        """Cloud mode publishes all 37 telemetry events."""

        run_producer()

        self.assertEqual(mock_publish.call_count, 37)

        for call in mock_publish.call_args_list:
            args, kwargs = call

            self.assertEqual(args[0], "test-project")
            self.assertEqual(args[1], "test-telemetry")
            self.assertIn("satellite_id", args[2])
            self.assertIn("event_id", args[2])



if __name__ == "__main__":
    unittest.main()
