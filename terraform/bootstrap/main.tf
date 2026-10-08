
terraform {
  required_version = ">= 1.6.0"

  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 6.0"
    }
  }
}

provider "google" {
  project = "orbitalsense-edun-2026"
  region  = "us-central1"
}

resource "google_storage_bucket" "terraform_state" {
  name     = "orbitalsense-edun-2026-tfstate"
  project  = "orbitalsense-edun-2026"
  location = "US"

  storage_class               = "STANDARD"
  uniform_bucket_level_access = true
  public_access_prevention    = "enforced"

  versioning {
    enabled = true
  }

  lifecycle {
    prevent_destroy = true
  }

  labels = {
    application = "orbitalsense"
    purpose     = "terraform-state"
    managed_by  = "terraform"
  }
}
