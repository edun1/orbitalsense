
import json
import os

from producer.main import simulate_reporting_cycles
from producer.publisher import publish_telemetry


def run_producer():
    """Run the telemetry producer in local or cloud mode."""

    mode = os.getenv("PUBLISH_MODE", "local").lower()

    if mode not in ("local", "cloud"):
        raise ValueError("PUBLISH_MODE must be local or cloud")

    project_id = None
    topic_id = None

    if mode == "cloud":
        project_id = os.getenv("GCP_PROJECT_ID")
        topic_id = os.getenv("PUBSUB_TOPIC_ID")

        if not project_id or not topic_id:
            raise ValueError(
                "Cloud mode requires GCP_PROJECT_ID "
                "and PUBSUB_TOPIC_ID"
            )

    events = simulate_reporting_cycles()

    for event in events:
        if mode == "local":
            print(json.dumps(event))
        else:
            publish_telemetry(project_id, topic_id, event)


if __name__ == "__main__":
    run_producer()
