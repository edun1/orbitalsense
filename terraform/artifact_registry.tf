
# Docker image repository for the OrbitalSense producer
resource "google_artifact_registry_repository" "producer" {
  project       = var.project_id
  location      = var.region
  repository_id = "${var.resource_prefix}-${var.environment}-docker"

  description = "Docker images for OrbitalSense services"
  format      = "DOCKER"

  labels = {
    environment = var.environment
    application = "orbitalsense"
    managed_by  = "terraform"
  }
}








