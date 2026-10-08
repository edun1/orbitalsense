
import json

from google.cloud import pubsub_v1


def publish_telemetry(project_id, topic_id, event, publisher=None):
    """Publish one satellite telemetry event to Pub/Sub."""

    if publisher is None:
        publisher = pubsub_v1.PublisherClient()

    topic_path = publisher.topic_path(project_id, topic_id)

    message_data = json.dumps(event).encode("utf-8")

    publish_future = publisher.publish(
        topic_path,
        message_data
    )

    message_id = publish_future.result(timeout=30)

    return message_id
