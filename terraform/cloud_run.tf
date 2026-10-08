
# Cloud Run service for the satellite telemetry producer

resource "google_cloud_run_v2_service" "telemetry_producer" {
  count = var.producer_image == null ? 0 : 1

  name     = "${var.resource_prefix}-${var.environment}-producer"
  project  = var.project_id
  location = var.region

  deletion_protection = true

  template {
    service_account = google_service_account.telemetry_producer.email

    scaling {
      min_instance_count = 1
      max_instance_count = 1
    }

    containers {
      image = var.producer_image

      env {
        name  = "GCP_PROJECT_ID"
        value = var.project_id
      }

      env {
        name  = "PUBSUB_TOPIC_ID"
        value = google_pubsub_topic.satellite_telemetry.name
      }

      resources {
        limits = {
          cpu    = "1"
          memory = "512Mi"
        }
      }
    }
  }

  depends_on = [
    google_project_service.required_apis,
    google_pubsub_topic_iam_member.producer_publisher
  ]
}
