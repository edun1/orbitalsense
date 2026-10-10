# 🛰️ OrbitalSense
### Event-Driven Satellite Telemetry Processing & Data Reliability Platform

**Python | Apache Beam | Data Engineering | Terraform | Docker | Google Cloud**

OrbitalSense is an end-to-end data engineering capstone project focused on building reliable satellite telemetry processing pipelines.

The project simulates telemetry from multiple satellites and ground stations, processes events using Apache Beam, validates incoming records, detects duplicates, measures ingestion freshness, identifies missing reports, and generates automated data-quality metrics.

**Engineering challenge:** How can a data pipeline produce trustworthy analytical datasets when incoming events are delayed, duplicated, invalid, or missing?

OrbitalSense addresses this challenge through modular Python development, event-based processing, automated data-quality checks, and Infrastructure as Code.

**Current status:** The Apache Beam processing pipeline has been implemented and tested locally. Google Cloud infrastructure has been defined using Terraform but has not yet been deployed.

---

## Engineering Highlights

- **Event-driven architecture:** Designed a satellite telemetry processing workflow with separate event and arrival timestamps.
- **Apache Beam processing:** Implemented modular transformations for parsing, validation, deduplication, and telemetry enrichment.
- **Data quality engineering:** Developed quarantine handling, freshness monitoring, and reporting completeness checks.
- **Controlled fault injection:** Simulated invalid, duplicate, delayed, and missing telemetry observations to test pipeline behavior.
- **Pipeline observability:** Generated JSON-based quality metrics for evaluating data reliability.
- **Infrastructure as Code:** Authored Terraform configuration for a planned Google Cloud architecture.
- **Reproducible execution:** Created a Windows batch script for running the local processing pipeline and generating reports.
- **Automated testing:** Added Python tests for telemetry producer and publishing components.

---

## System Architecture

### Implemented Local Architecture

```text
                  SATELLITE TELEMETRY SOURCES
                  12 Satellites | 4 Stations
                              |
                              v
                   Python Telemetry Producer
                              |
                              v
                      JSONL Event Dataset
                              |
                              v
                    Apache Beam Pipeline
                              |
             +----------------+----------------+
             |                                 |
             v                                 v
       Parsing & Validation              Invalid Records
             |                             Quarantine
             v
        Deduplication
             |
             v
       Curated Telemetry
             |
       +-----+------+
       |            |
       v            v
   Freshness    Completeness
   Monitoring   Monitoring
       |            |
       +------+-----+
              |
              v
       Data Quality KPIs
              |
              v
       JSON Quality Reports
```

### Planned Google Cloud Architecture

```text
Satellite Telemetry Producer
             |
             v
       Cloud Run
             |
             v
       Pub/Sub Topic
             |
             v
   Apache Beam / Dataflow
             |
      +------+-------+
      |              |
      v              v
 Cloud Storage     BigQuery
 Raw / Curated     Analytics
      |              |
      +------+-------+
             |
             v
    Monitoring & Reporting

    Infrastructure: Terraform
    Containerization: Docker
```

The cloud architecture represents the target deployment design. It is not a currently running cloud environment.

---

## Dataset Engineering and Fault Injection

OrbitalSense simulates satellite telemetry across multiple reporting cycles.

| Dataset characteristic | Value |
|---|---|
| Simulated satellites | 12 |
| Ground stations | 4 |
| Reporting cycles | 3 |
| Expected reports | 36 |
| Raw events processed | 37 |
| Invalid records | 1 |
| Duplicate records | 1 |
| Missing expected reports | 1 |

The dataset intentionally includes the following scenarios:

1. An invalid battery reading associated with SAT-003.
2. A duplicate telemetry event.
3. A missing report from SAT-007 during reporting cycle 2.
4. Simulated arrival delays ranging from 0 to 900 seconds.

These controlled scenarios make it possible to evaluate pipeline behavior against known data-quality conditions.

---

## Data Pipeline Engineering

### 1. Telemetry Parsing and Validation

The Apache Beam pipeline reads JSONL telemetry events and applies validation rules to identify invalid observations.

Records that fail validation are quarantined instead of being included in the curated dataset.

This prevents invalid source records from silently affecting downstream analytical results.

### 2. Duplicate Detection

Duplicate telemetry observations are identified and excluded from the curated output.

Deduplication helps prevent inflated event counts and repeated observations from distorting analytical metrics.

### 3. Event-Time Freshness Monitoring

The telemetry simulator represents two distinct timestamps:

- **Event timestamp:** When the simulated satellite observation occurred.
- **Arrival timestamp:** When the event is represented as arriving for processing.

Telemetry arrival latency is calculated as:

`latency_seconds = arrival_timestamp - event_timestamp`

The pipeline uses a five-minute threshold to classify events as on time or delayed.

This demonstrates an important challenge in distributed data engineering: an event can be valid but still arrive too late to meet a system's freshness requirements.

### 4. Reporting Completeness Monitoring

Completeness monitoring compares expected satellite reporting observations with successfully processed valid, unique observations.

`completeness_percentage = (valid_unique_reports / expected_reports) × 100`

The pipeline identifies SAT-007, reporting cycle 2, as a missing observation.

### 5. Automated Data-Quality Reporting

OrbitalSense generates machine-readable quality reports, including:

- `beam_freshness_kpis.json`
- `beam_completeness_kpis.json`
- `orbital_quality_report.json`

These reports provide a foundation for future dashboards, automated monitoring, and operational alerts.

---

## Verified Local Pipeline Results

The locally tested Apache Beam workflow produced the following results:

| Data-quality metric | Result |
|---|---:|
| Raw telemetry events | 37 |
| Valid unique records | 35 |
| Invalid records quarantined | 1 |
| Duplicate records excluded | 1 |
| Malformed records | 0 |
| On-time telemetry events | 14 / 35 |
| Freshness compliance | **40.00%** |
| Reporting completeness | **97.22%** |
| Missing observation | SAT-007, Cycle 2 |

### Engineering Interpretation

**Freshness:** Only 40% of valid unique telemetry observations met the five-minute arrival threshold, demonstrating why ingestion latency requires independent monitoring.

**Completeness:** The pipeline achieved 97.22% reporting completeness and identified the missing satellite-cycle report.

**Data integrity:** Invalid and duplicate observations were detected and excluded from the curated dataset.

**Key takeaway:** A successful pipeline execution does not automatically guarantee reliable analytical data. Data quality must be assessed across validity, uniqueness, timeliness, and completeness.

*All results are based on controlled simulated telemetry, not live satellite measurements.*

---

## Technology Stack

| Technology | Engineering responsibility |
|---|---|
| Python 3.14 | Telemetry simulation and processing logic |
| Apache Beam 2.77.0 | Event processing and data-quality transformations |
| Apache Beam DirectRunner | Local pipeline execution |
| JSON / JSONL | Telemetry exchange and KPI reporting |
| Terraform | Infrastructure as Code |
| Docker | Container build configuration |
| Google Cloud Pub/Sub | Planned cloud event ingestion |
| Google Cloud Run | Planned telemetry producer hosting |
| Google Cloud Dataflow | Planned managed pipeline execution |
| Google Cloud Storage | Planned raw and curated cloud storage |
| BigQuery | Planned analytics and SQL processing |
| Git / GitHub | Version control and project documentation |

---

## Repository Structure

```text
orbitalsense/
├── producer/
│   ├── main.py
│   ├── publisher.py
│   ├── run.py
│   └── requirements.txt
│
├── pipeline/
│   ├── beam_pipeline.py
│   ├── parsing.py
│   ├── validation.py
│   ├── deduplication.py
│   ├── freshness.py
│   ├── completeness.py
│   ├── quality_report.py
│   └── main.py
│
├── terraform/
│   ├── bootstrap/
│   ├── pubsub.tf
│   ├── cloud_run.tf
│   ├── storage.tf
│   ├── iam.tf
│   └── artifact_registry.tf
│
├── tests/
├── docs/
├── sql/
├── Dockerfile
├── requirements.txt
├── run_orbitalsense.bat
└── README.md
```

---

## Getting Started — Local Execution

### Prerequisites

- Windows with Command Prompt
- Python 3.14
- Git
- Python package installation through pip

### 1. Clone the Repository

```cmd
git clone https://github.com/edun1/orbitalsense.git
cd orbitalsense
```

### 2. Install Dependencies

The project-level `requirements.txt` declares Apache Beam and Google Cloud Pub/Sub dependencies.

```cmd
py -3.14 -m pip install -r requirements.txt
```

### 3. Run the Local Pipeline

```cmd
run_orbitalsense.bat
```

The batch script executes two stages:

**Stage 1 — Apache Beam processing**

```cmd
py -3.14 -m pipeline.beam_pipeline
```

**Stage 2 — Quality report generation**

```cmd
py -3.14 -m pipeline.quality_report
```

The script checks for errors after each stage and stops if a stage fails.

### 4. Review Generated Reports

After successful execution, inspect:

- `beam_freshness_kpis.json`
- `beam_completeness_kpis.json`
- `orbital_quality_report.json`

The combined report summarizes telemetry data-quality performance.

**Note:** The workflow has been successfully tested in the author's Windows development environment. Some input datasets are generated locally and excluded from Git; a complete fresh-clone setup workflow is still being finalized.

---

## Testing and Reliability

The repository includes Python tests for telemetry producer and publishing components.

The local pipeline has also been tested against controlled data-quality scenarios involving:

- Invalid telemetry values
- Duplicate observations
- Missing satellite reports
- Delayed event arrivals

These tests demonstrate the importance of verifying both pipeline execution and the quality of resulting datasets.

Future improvements include expanded Apache Beam unit tests, automated regression checks, and CI-based validation.

---

## Infrastructure as Code

Terraform configuration is provided for the planned Google Cloud deployment.

The infrastructure definitions cover:

- Cloud Run
- Pub/Sub
- Cloud Storage
- Artifact Registry
- IAM permissions
- Required Google Cloud APIs
- Infrastructure bootstrap configuration

Terraform configuration has been validated locally.

**Deployment status:** The cloud infrastructure has not yet been provisioned. No live Cloud Run, Pub/Sub, Dataflow, or BigQuery deployment is claimed.

---

## Engineering Roadmap

| Phase | Engineering deliverable | Status |
|---|---|---|
| 1 | Repository foundation and telemetry producer | Implemented |
| 2 | Local Apache Beam processing | Implemented |
| 3 | Validation, deduplication, and quarantine | Implemented |
| 4 | Freshness, completeness, and KPI reporting | Implemented |
| 5 | Terraform infrastructure configuration | Authored and validated |
| 6 | Cloud Run and Pub/Sub integration | Planned |
| 7 | Managed Dataflow execution | Planned |
| 8 | BigQuery analytics and dashboards | Planned |
| 9 | CI/CD, monitoring, and alerting | Planned |

---

## Security and Development Practices

The project uses `.gitignore` rules to exclude local configuration, generated telemetry outputs, credential files, and Terraform state artifacts from routine commits.

Cloud deployment will require appropriate authentication, IAM permissions, and billing configuration.

The repository is intended for learning, engineering experimentation, and portfolio demonstration rather than production satellite operations.

---

## Skills Demonstrated

**Data Engineering**
- Apache Beam pipeline development
- Event processing and transformation
- JSONL data ingestion
- Data validation and quarantine
- Deduplication
- Data-quality KPI computation

**Data Reliability Engineering**
- Data freshness monitoring
- Completeness analysis
- Controlled fault injection
- Expected-versus-observed event reconciliation
- Machine-readable quality reporting

**Cloud Engineering**
- Google Cloud architecture design
- Infrastructure as Code with Terraform
- Docker container configuration
- Event-driven cloud integration planning

**Software Engineering**
- Modular Python development
- Automated testing
- Git branching and version control
- Scripted pipeline execution
- Technical documentation

---

## Project Purpose

OrbitalSense demonstrates how a data engineering system can be designed to handle imperfect event data while producing measurable reliability indicators.

The project combines practical Python development, Apache Beam processing, automated data-quality monitoring, and cloud infrastructure design to showcase engineering capabilities relevant to Data Engineering and Cloud Engineering roles.

**Repository:** https://github.com/edun1/orbitalsense