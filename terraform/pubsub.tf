
resource "google_pubsub_topic" "satellite_telemetry" {
  name    = "${var.resource_prefix}-${var.environment}-telemetry"
  project = var.project_id

  labels = {
    environment = var.environment
    application = "orbitalsense"
    managed_by  = "terraform"
  }
}
