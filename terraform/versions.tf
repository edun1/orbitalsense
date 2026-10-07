terraform {
  required_version = ">= 1.6.0"

  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 6.0"
    }
  }

  # Remote state will be configured with a GCS backend
  # after the state bucket has been bootstrapped.
  backend "gcs" {}
}