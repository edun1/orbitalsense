

\# OrbitalSense



\## Cloud-Native Satellite Telemetry Platform



OrbitalSense is a Data Engineering capstone project designed to simulate, ingest, process, validate, store, and analyze satellite telemetry using Google Cloud.



\## Project Objectives



\- Simulate telemetry from multiple satellites and ground stations.

\- Ingest telemetry through Google Cloud Pub/Sub.

\- Process streaming events using Apache Beam and Dataflow.

\- Validate telemetry and quarantine malformed records.

\- Store raw and curated telemetry separately.

\- Analyze satellite performance using BigQuery SQL.

\- Provision cloud infrastructure using Terraform.



\## Technology Stack



\- Python

\- Google Cloud Platform

\- Terraform

\- Docker

\- Cloud Run

\- Pub/Sub

\- Apache Beam / Dataflow

\- BigQuery

\- Git and GitHub



\## Project Structure



\- `terraform/` - Infrastructure as Code

\- `producer/` - Satellite telemetry simulator

\- `pipeline/` - Streaming data processing

\- `sql/` - Analytics queries

\- `docs/` - Architecture and technical documentation

\- `tests/` - Automated tests



\## Development Status



Phase 1: Infrastructure and telemetry producer — In progress.



\## Security



Credentials, Terraform state files, and local environment configuration are excluded from version control.



