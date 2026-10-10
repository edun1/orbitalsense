# OrbitalSense
### Satellite Telemetry Data Engineering Platform

**Python | Apache Beam | Data Quality Engineering | Google Cloud | Terraform | Git**

[![Project Status](https://img.shields.io/badge/Status-Local%20Pipeline%20Operational-brightgreen)](https://github.com/edun1/orbitalsense)
[![Apache Beam](https://img.shields.io/badge/Apache%20Beam-2.77.0-blue)](https://beam.apache.org/)
[![Python](https://img.shields.io/badge/Python-3.14-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-Not%20Specified-lightgrey)](https://github.com/edun1/orbitalsense)

**Repository:** https://github.com/edun1/orbitalsense

---

## 1. Project Overview

OrbitalSense is a satellite telemetry data engineering capstone designed to demonstrate how telemetry from a constellation of satellites can be generated, validated, processed, and monitored for data quality.

The project simulates telemetry from **12 satellites communicating through 4 ground stations**, with measurements representing satellite subsystems such as power, thermal conditions, communications, and orbital position.

The engineering objective is to build a trustworthy data platform that addresses three operational priorities:

1. **Trust:** Prevent invalid or duplicate telemetry from contaminating curated datasets.
2. **Timeliness:** Measure whether telemetry reaches the processing system within an acceptable delay.
3. **Completeness:** Identify missing satellite reports rather than silently ignoring gaps.

The project combines practical Python development, Apache Beam processing, data-quality engineering, infrastructure-as-code preparation, and cloud architecture design.

### Current implementation status

The **local data processing workflow is operational and tested**.

A single Windows batch command automatically:

- Generates simulated satellite telemetry.
- Processes the dataset using Apache Beam.
- Validates and quarantines suspicious records.
- Identifies duplicate telemetry.
- Calculates freshness and completeness KPIs.
- Produces a consolidated data-quality report.

**Important:** The Google Cloud architecture is a planned deployment target. Terraform configuration has been validated locally, but the cloud infrastructure has not yet been deployed because billing is not enabled. Cloud streaming, BigQuery integration, and production deployment should not be considered completed.

---

## 2. Business Problem

Satellite operations depend on telemetry to understand spacecraft health and operational conditions.

However, satellite telemetry is not always delivered cleanly or consistently.

Real-world challenges include:

- Satellites temporarily moving outside ground-station coverage.
- Delayed or out-of-order telemetry.
- Duplicate messages caused by retries.
- Physically implausible sensor readings.
- Missing reporting cycles.
- Malformed messages.
- Differences between raw incoming data and trusted analytical data.

Without proper data engineering controls, these conditions can lead to misleading dashboards, inaccurate operational decisions, and undetected system failures.

OrbitalSense addresses these challenges by building an explicit data-quality workflow.

---

## 3. Architecture

### 3.1 Implemented local architecture

```text
              SATELLITE TELEMETRY SIMULATOR
                       producer/main.py
                              |
                              v
                  37 Raw Telemetry Events
                              |
                              v
                telemetry_freshness_test.jsonl
                              |
                              v
                     APACHE BEAM PIPELINE
                  pipeline/beam_pipeline.py
                              |
               +--------------+--------------+
               |                             |
               v                             v
       Validation and Parsing       Invalid / Malformed Data
               |                             |
               v                             v
         Deduplication                 Quarantine Output
               |
               v
        Valid Unique Events
               |
        +------+------+
        |             |
        v             v
    Freshness     Completeness
      Metrics        Metrics
        |             |
        +------+------+
               |
               v
        DATA-QUALITY REPORT
     pipeline/quality_report.py
               |
               v
    orbital_quality_report.json
```

This local implementation uses Apache Beam's execution environment to process generated JSONL data.

It does not require an active Google Cloud project.

### 3.2 Target cloud architecture

The planned cloud-native implementation is:

```text
               SATELLITE TELEMETRY
                    PRODUCER
                       |
                       v
                 CLOUD RUN
                       |
                       v
                 CLOUD PUB/SUB
                       |
                       v
              APACHE BEAM / DATAFLOW
                       |
          +------------+------------+
          |                         |
          v                         v
      VALID DATA                INVALID DATA
          |                         |
          v                         v
   CURATED STORAGE            QUARANTINE /
          |                   DEAD-LETTER
          v                      STORAGE
       BIGQUERY
          |
          v
   OPERATIONAL ANALYTICS
```

Supporting services planned for this architecture include:

- **Terraform:** Infrastructure provisioning and configuration.
- **Cloud Storage:** Raw telemetry storage and related artifacts.
- **Pub/Sub:** Messaging and ingestion.
- **Dataflow:** Managed execution of Apache Beam pipelines.
- **BigQuery:** Analytical storage and SQL querying.
- **Cloud Run:** Containerized telemetry producer.
- **Artifact Registry:** Container image storage.
- **IAM:** Service identities and least-privilege access.

This diagram represents the intended cloud architecture, not a deployed environment.

---

## 4. Technology Stack

| Technology | Purpose | Status |
|---|---|---|
| Python 3.14 | Telemetry generation and processing | Tested locally |
| Apache Beam 2.77.0 | Data transformation and quality checks | Tested locally |
| JSON / JSONL | Local event exchange and output | Implemented |
| Windows Batch | Automated local pipeline execution | Implemented |
| Git and GitHub | Version control and source publication | Implemented |
| Terraform | Infrastructure-as-code configuration | Validated locally |
| Google Cloud Pub/Sub | Planned cloud messaging | Not deployed |
| Google Cloud Dataflow | Planned managed pipeline execution | Not deployed |
| Google Cloud Storage | Planned cloud storage | Not deployed |
| Google BigQuery | Planned analytical warehouse | Not deployed |
| Google Cloud Run | Planned container hosting | Not deployed |

---

## 5. Telemetry Simulation

The simulator models a constellation of **12 satellites**, identified as:

`SAT-001` through `SAT-012`.

Telemetry is associated with one of four ground stations.

The simulated data includes measurements relating to:

- Satellite power systems.
- Thermal conditions.
- Communications.
- Orbital location.
- Event timestamps.
- Arrival timestamps.
- Satellite identification.
- Reporting cycles.
- Unique event identifiers.

### Controlled data-quality scenarios

The current local test generates three reporting cycles and deliberately introduces data-quality problems.

| Scenario | Implementation |
|---|---|
| Normal reporting | Satellites produce telemetry during reporting cycles |
| Missing report | SAT-007 is omitted from reporting cycle 2 |
| Invalid reading | SAT-003 receives an invalid battery reading in cycle 2 |
| Duplicate event | A telemetry event is repeated |
| Delayed delivery | Random arrival delays of up to 900 seconds |

This design allows the pipeline to demonstrate quality checks against both normal and problematic data.

### Expected dataset size

For 12 satellites and 3 reporting cycles:

```text
Expected reporting combinations = 12 × 3 = 36
```

One reporting combination is intentionally missing, while one event is duplicated.

Therefore, the simulator emits:

```text
37 raw telemetry events
```

Of those:

```text
35 valid unique events
1 invalid event
1 duplicate event
```

---

## 6. Data Processing Pipeline

The main Apache Beam pipeline is implemented in:

`pipeline/beam_pipeline.py`

Its processing stages include:

### 6.1 Parsing

Incoming JSONL records are read and interpreted as telemetry events.

Malformed records are counted separately from valid events.

### 6.2 Validation

Telemetry records are checked for validity, including implausible values.

Invalid records are routed to quarantine instead of being included in the trusted output.

### 6.3 Deduplication

Duplicate telemetry is identified to prevent repeated events from inflating downstream metrics.

### 6.4 Freshness measurement

Freshness measures whether a telemetry event arrived within the configured time threshold.

The current local evaluation uses a five-minute threshold.

```text
Freshness Rate =
(On-Time Valid Events / Total Valid Unique Events) × 100
```

### 6.5 Completeness measurement

Completeness measures how many expected satellite reporting combinations are represented by valid, unique events.

```text
Completeness Rate =
(Received Valid Reports / Expected Reports) × 100
```

### 6.6 Reporting

The pipeline produces KPI outputs, and the reporting module generates a consolidated JSON report.

---

## 7. Verified Local Pipeline Results

The following results were obtained from a successful local execution of `run_orbitalsense.bat`.

### 7.1 Data-quality summary

| Metric | Verified result |
|---|---:|
| Raw telemetry events | 37 |
| Valid unique events | 35 |
| Quarantined events | 1 |
| Duplicate events | 1 |
| Malformed JSON messages | 0 |
| Expected reports | 36 |
| Received valid reports | 35 |
| Missing reports | 1 |
| Completeness rate | **97.22%** |
| On-time events | 16 |
| Late events | 19 |
| Freshness rate | **45.71%** |

### 7.2 Completeness results

```json
{
  "expected_reports": 36,
  "received_reports": 35,
  "missing_reports": 1,
  "completeness_rate_percent": 97.22,
  "missing_details": [
    {
      "satellite_id": "SAT-007",
      "reporting_cycle": 2
    }
  ]
}
```

The completeness check successfully identified the missing report from **SAT-007 during reporting cycle 2**.

### 7.3 Freshness results

```json
{
  "total_events": 35,
  "on_time": 16,
  "late": 19,
  "freshness_rate_percent": 45.71
}
```

The latest tested run found 16 events arriving within the freshness threshold and 19 arriving late.

**Reproducibility note:** Arrival delays are randomized. The exact freshness percentage may change when the simulator runs again. The figures above represent one verified execution, not a guaranteed result for every run.

---

## 8. Repository Structure

The following structure highlights the principal source files and workflow components.

```text
orbitalsense/
|
|-- producer/
|   |-- main.py
|   |-- publisher.py
|   |-- requirements.txt
|   |-- run.py
|
|-- pipeline/
|   |-- beam_pipeline.py
|   |-- completeness.py
|   |-- deduplication.py
|   |-- freshness.py
|   |-- main.py
|   |-- parsing.py
|   |-- quality_report.py
|   |-- validation.py
|
|-- requirements.txt
|-- run_orbitalsense.bat
|-- README.md
|
|-- [Additional infrastructure and project files]
```

### Main components

**`producer/main.py`**

Generates the simulated satellite telemetry dataset.

**`producer/publisher.py`**

Contains producer-side publishing functionality intended for messaging integration.

**`pipeline/beam_pipeline.py`**

Executes the local Apache Beam processing workflow.

**`pipeline/validation.py`**

Contains telemetry validation logic.

**`pipeline/deduplication.py`**

Contains duplicate-handling logic.

**`pipeline/freshness.py`**

Contains freshness-related processing logic.

**`pipeline/completeness.py`**

Contains completeness-related processing logic.

**`pipeline/quality_report.py`**

Generates the consolidated data-quality report.

**`run_orbitalsense.bat`**

Automates the local workflow.

**`requirements.txt`**

Declares the project's main Python dependencies.

The directory listing above is intentionally focused on verified pipeline components rather than claiming to be a complete inventory of every repository file.

---

## 9. Installation and Local Execution

### 9.1 Prerequisites

The tested environment uses:

- Windows 11.
- Python 3.14.
- Git.
- Internet access for initial Python dependency installation.

Google Cloud billing is not required to execute the local workflow.

### 9.2 Clone the repository

Open Windows Command Prompt and run:

```cmd
git clone https://github.com/edun1/orbitalsense.git
cd orbitalsense
```

### 9.3 Install Python dependencies

The root `requirements.txt` contains:

```text
apache-beam==2.77.0
google-cloud-pubsub>=2.20,<3.0
```

Install the dependencies with:

```cmd
py -3.14 -m pip install -r requirements.txt
```

### 9.4 Run the complete local pipeline

Execute:

```cmd
run_orbitalsense.bat
```

The batch script automatically runs three stages.

**Stage 1 — Generate satellite telemetry**

```cmd
py -3.14 -m producer.main > telemetry_freshness_test.jsonl
```

This creates the JSONL input dataset required by the local Apache Beam pipeline.

**Stage 2 — Process satellite telemetry**

```cmd
py -3.14 -m pipeline.beam_pipeline
```

Apache Beam processes the telemetry, applies data-quality controls, and calculates KPIs.

**Stage 3 — Generate the data-quality report**

```cmd
py -3.14 -m pipeline.quality_report
```

The reporting module generates:

`orbital_quality_report.json`

### 9.5 Expected completion message

A successful run ends with:

```text
=====================================
OrbitalSense pipeline completed!
Report: orbital_quality_report.json
=====================================
```

### 9.6 Important execution notes

- The batch script runs from the project root.
- The script regenerates `telemetry_freshness_test.jsonl` each time it executes.
- Existing generated output files may be replaced.
- Freshness results may change because simulated arrival delays are randomized.
- Generated JSONL and KPI reports are excluded from version control.
- The workflow has been tested in the development environment; a separate clean-clone test remains to be completed.

---

## 10. Data Quality Engineering Approach

OrbitalSense uses explicit quality checks rather than assuming every received event is trustworthy.

### Validity

Records must satisfy the implemented telemetry validation rules before entering curated output.

### Uniqueness

Duplicate events are detected and excluded from valid unique counts.

### Freshness

Events are evaluated against a five-minute delivery threshold.

Late telemetry is distinguished from invalid telemetry.

### Completeness

The pipeline compares received valid reporting combinations with expected satellite reporting combinations.

Missing data is surfaced through structured KPI output.

### Quarantine

Invalid records are kept separate from curated telemetry so data-quality failures can be investigated.

Together, these controls demonstrate how telemetry processing can prioritize correctness, timeliness, and traceability.

---

## 11. Infrastructure as Code

OrbitalSense includes Terraform-based infrastructure preparation for the planned Google Cloud deployment.

### Current status

Terraform configuration has been validated locally.

However:

- Google Cloud billing is not currently enabled.
- Cloud resources have not been deployed.
- Cloud execution has not been tested.
- A complete cloud teardown and redeployment test has not been performed.

### Planned infrastructure responsibilities

Terraform is intended to manage the cloud services required for ingestion, processing, storage, analytics, and access control.

Infrastructure goals include:

- Reproducible provisioning.
- Least-privilege service accounts.
- Separation of raw and curated telemetry.
- Managed streaming execution.
- Cloud-based analytical storage.
- Remote Terraform state management.
- Documented deployment and teardown procedures.

These are target capabilities and must be validated against a deployed environment before being reported as complete.

---

## 12. Planned Cloud Deployment

The next cloud implementation phases will extend the verified local workflow.

### Phase 1 — Cloud infrastructure

- Configure an appropriate Google Cloud project.
- Enable billing and required APIs.
- Finalize Terraform configuration.
- Configure remote Terraform state.
- Provision infrastructure using Terraform.
- Validate IAM permissions.

### Phase 2 — Cloud telemetry ingestion

- Package the telemetry producer for container execution.
- Publish the container image.
- Deploy the producer to Cloud Run.
- Publish telemetry events to Pub/Sub.
- Verify ingestion behavior.

### Phase 3 — Managed stream processing

- Adapt the Apache Beam pipeline for Pub/Sub input.
- Execute the pipeline using Google Cloud Dataflow.
- Preserve validation and deduplication behavior.
- Route invalid telemetry to an inspectable quarantine destination.
- Handle late and out-of-order events.

### Phase 4 — Storage and analytics

- Store raw and curated telemetry separately.
- Create appropriate BigQuery tables.
- Configure partitioning and clustering.
- Develop operational SQL queries.
- Analyze satellite health and communication performance.

### Phase 5 — Operational reliability

- Add automated tests.
- Introduce controlled failure scenarios.
- Add monitoring and alerting.
- Validate recovery behavior.
- Document deployment and rollback procedures.

These phases describe planned work rather than completed deliverables.

---

## 13. Engineering Challenges Addressed

The current local implementation demonstrates several important data engineering concepts.

**Challenge 1: Duplicate delivery**

A duplicated telemetry event should not be counted twice in curated output.

**Approach:** Identify and exclude duplicates before computing trusted KPIs.

**Challenge 2: Invalid sensor readings**

An event may be syntactically valid JSON while containing an impossible or implausible value.

**Approach:** Apply validation checks and quarantine rejected records.

**Challenge 3: Satellite reporting gaps**

A satellite may fail to report during an expected cycle.

**Approach:** Compare expected and received reporting combinations and identify missing satellite-cycle pairs.

**Challenge 4: Delayed telemetry**

A valid event may arrive later than the required operational threshold.

**Approach:** Measure freshness independently of validity.

**Challenge 5: Repeatable local execution**

A pipeline should not require developers to manually prepare input files before every run.

**Approach:** Use a batch script that generates input data, processes it, and creates a report automatically.

---

## 14. Limitations and Next Improvements

The current project has several known limitations.

1. The verified workflow runs locally rather than on deployed Google Cloud infrastructure.
2. The simulator uses randomized delays, so exact freshness results are not deterministic.
3. The local pipeline reads a generated JSONL file rather than a live Pub/Sub subscription.
4. Cloud-based quarantine storage and BigQuery analytics are not yet operational.
5. A fresh-clone execution test remains outstanding.
6. More automated tests and failure-injection scenarios are needed.
7. The simulated reporting gap is currently controlled rather than demonstrating a complete satellite dropout-and-recovery lifecycle.

These limitations provide a clear engineering roadmap for the next stages.

---

## 15. Skills Demonstrated

This project provides practical evidence of work in:

- Python data engineering.
- Apache Beam pipeline development.
- Structured event processing.
- Data validation.
- Duplicate detection.
- Data freshness measurement.
- Completeness monitoring.
- Quarantine and error handling.
- JSONL processing.
- Local workflow automation.
- Git and GitHub version control.
- Infrastructure-as-code preparation.
- Cloud data platform architecture.

It is designed as a technical portfolio project for roles including:

**Data Engineer | Cloud Data Engineer | Data Platform Engineer | Data Quality Engineer**

---

## 16. Project Roadmap

| Milestone | Status |
|---|---|
| Create GitHub repository | Completed |
| Develop satellite telemetry simulator | Completed locally |
| Implement Apache Beam processing | Completed locally |
| Add validation and quarantine | Completed locally |
| Implement duplicate detection | Completed locally |
| Implement freshness KPIs | Completed locally |
| Implement completeness KPIs | Completed locally |
| Generate consolidated quality report | Completed locally |
| Automate local pipeline execution | Completed |
| Document installation and execution | Completed |
| Validate Terraform configuration locally | Completed |
| Test execution from a fresh clone | Pending |
| Deploy Terraform infrastructure to GCP | Pending |
| Deploy producer to Cloud Run | Pending |
| Integrate Pub/Sub ingestion | Pending |
| Run Apache Beam on Dataflow | Pending |
| Implement BigQuery analytics | Pending |
| Add cloud monitoring and recovery tests | Pending |

---

## 17. Author

**Blessing Atigbolaye Edun**

Financial Engineering Graduate Student | Data Analyst | Data Engineering Practitioner

**GitHub:** https://github.com/edun1

**Project Repository:** https://github.com/edun1/orbitalsense

---

## 18. Conclusion

OrbitalSense demonstrates an end-to-end local satellite telemetry data engineering workflow that generates realistic test events, processes them using Apache Beam, identifies data-quality problems, and produces measurable quality indicators.

The latest verified execution processed **37 raw events**, identified **35 valid unique events**, detected **1 invalid event** and **1 duplicate**, achieved **97.22% completeness**, and measured **45.71% freshness compliance**.

The next major milestone is extending this validated local foundation into a reproducible, cloud-native telemetry platform on Google Cloud.

**Project status: Local pipeline operational; cloud deployment in progress.**