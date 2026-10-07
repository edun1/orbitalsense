variable "project_id" {
  description = "Google Cloud project ID for OrbitalSense"
  type        = string
}

variable "region" {
  description = "Primary Google Cloud region for OrbitalSense resources"
  type        = string
  default     = "us-central1"
}

variable "environment" {
  description = "Deployment environment"
  type        = string
  default     = "dev"
}

variable "resource_prefix" {
  description = "Prefix used when naming OrbitalSense resources"
  type        = string
  default     = "orbitalsense"
}