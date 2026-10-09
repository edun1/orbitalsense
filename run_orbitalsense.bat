
@echo off
cd /d "%~dp0"

echo =====================================
echo      OrbitalSense Data Pipeline
echo =====================================

echo.
echo Step 1: Processing satellite telemetry...
py -3.14 -m pipeline.beam_pipeline

if errorlevel 1 (
    echo ERROR: Apache Beam pipeline failed.
    exit /b 1
)

echo.
echo Step 2: Generating data-quality report...
py -3.14 -m pipeline.quality_report

if errorlevel 1 (
    echo ERROR: Quality report generation failed.
    exit /b 1
)

echo.
echo =====================================
echo OrbitalSense pipeline completed!
echo Report: orbital_quality_report.json
echo =====================================
