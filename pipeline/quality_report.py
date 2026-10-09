
"""
OrbitalSense data-quality summary report.
"""

import json


def generate_quality_report(freshness_file, completeness_file):
    """
    Combine freshness and completeness KPIs into one report.
    """

    with open(freshness_file, "r", encoding="utf-8") as file:
        freshness = json.load(file)

    with open(completeness_file, "r", encoding="utf-8") as file:
        completeness = json.load(file)

    return {
        "project": "OrbitalSense",
        "freshness": freshness,
        "completeness": completeness,
    }

def main():
    report = generate_quality_report(
        "beam_freshness_kpis.json",
        "beam_completeness_kpis.json"
    )

    with open(
        "orbital_quality_report.json",
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(report, file, indent=2)

    print("OrbitalSense quality report generated successfully.")


if __name__ == "__main__":
    main()
