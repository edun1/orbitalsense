
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


# Dedicated identity for the future Dataflow pipeline
resource "google_service_account" "dataflow_worker" {
  project      = var.project_id
  account_id   = "orbitalsense-dataflow"
  display_name = "OrbitalSense Dataflow Worker"
  description  = "Processes satellite telemetry from Pub/Sub"
}

# Allow Dataflow to consume telemetry messages
resource "google_pubsub_subscription_iam_member" "dataflow_subscriber" {
  project      = var.project_id
  subscription = google_pubsub_subscription.telemetry_stream.name
  role         = "roles/pubsub.subscriber"
  member       = "serviceAccount:${google_service_account.dataflow_worker.email}"
}
