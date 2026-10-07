
# Storage bucket for OrbitalSense application artifacts
resource "google_storage_bucket" "application" {
  project                     = var.project_id
  name                        = "${var.project_id}-${var.environment}-artifacts"
  location                    = "US"
  storage_class               = "STANDARD"
  uniform_bucket_level_access = true

  public_access_prevention = "enforced"

  versioning {
    enabled = true
  }

  labels = {
    environment = var.environment
    application = "orbitalsense"
    managed_by  = "terraform"
  }
}
