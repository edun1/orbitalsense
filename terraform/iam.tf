
# Identity used by the satellite telemetry producer
resource "google_service_account" "telemetry_producer" {
  project      = var.project_id
  account_id   = "orbitalsense-producer"
  display_name = "OrbitalSense Telemetry Producer"
  description  = "Publishes simulated satellite telemetry to Pub/Sub"
}

# Grant publishing permission on the telemetry topic only
resource "google_pubsub_topic_iam_member" "producer_publisher" {
  project = var.project_id
  topic   = google_pubsub_topic.satellite_telemetry.name
  role    = "roles/pubsub.publisher"
  member  = "serviceAccount:${google_service_account.telemetry_producer.email}"
}
