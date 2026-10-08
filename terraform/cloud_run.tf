
# Cloud Run Job for the satellite telemetry producer

resource "google_cloud_run_v2_job" "telemetry_producer" {
  count = var.producer_image == null ? 0 : 1

  name     = "${var.resource_prefix}-${var.environment}-producer"
  project  = var.project_id
  location = var.region

  deletion_protection = true

  template {
    template {
      service_account = google_service_account.telemetry_producer.email

      max_retries = 0
      timeout     = "300s"

      containers {
        image = var.producer_image

        env {
          name  = "PUBLISH_MODE"
          value = "cloud"
        }

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
  }

  depends_on = [
    google_project_service.required_apis,
    google_pubsub_topic_iam_member.producer_publisher
  ]
}
