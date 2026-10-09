
"""
OrbitalSense telemetry completeness monitoring.
"""

SATELLITES = [
    f"SAT-{i:03d}"
    for i in range(1, 13)
]

REPORTING_CYCLES = [1, 2, 3]


def find_missing_reports(events):
    """
    Identify missing satellite reporting cycles.
    """

    expected_reports = {
        (satellite, cycle)
        for satellite in SATELLITES
        for cycle in REPORTING_CYCLES
    }

    received_reports = {
        (
            event["satellite_id"],
            event["reporting_cycle"]
        )
        for event in events
    }

    missing_reports = expected_reports - received_reports

    return sorted(missing_reports)

def calculate_completeness_metrics(events):
    """
    Calculate telemetry reporting completeness KPIs.
    """

    missing_reports = find_missing_reports(events)

    expected_count = len(SATELLITES) * len(REPORTING_CYCLES)

    received_count = expected_count - len(missing_reports)

    completeness_rate = (
        round((received_count / expected_count) * 100, 2)
        if expected_count > 0 else 0.0
    )

    return {
        "expected_reports": expected_count,
        "received_reports": received_count,
        "missing_reports": len(missing_reports),
        "completeness_rate_percent": completeness_rate,
        "missing_details": [
            {
                "satellite_id": satellite,
                "reporting_cycle": cycle
            }
            for satellite, cycle in missing_reports
        ]
    }
