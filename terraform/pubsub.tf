
resource "google_pubsub_topic" "satellite_telemetry" {
  name    = "${var.resource_prefix}-${var.environment}-telemetry"
  project = var.project_id

  labels = {
    environment = var.environment
    application = "orbitalsense"
    managed_by  = "terraform"
  }
}


# Subscription for the future Apache Beam streaming pipeline

resource "google_pubsub_subscription" "telemetry_stream" {
  name    = "${var.resource_prefix}-${var.environment}-telemetry-sub"
  project = var.project_id
  topic   = google_pubsub_topic.satellite_telemetry.id

  ack_deadline_seconds = 60

  message_retention_duration = "604800s"

  labels = {
    environment = var.environment
    application = "orbitalsense"
    managed_by  = "terraform"
  }
}
