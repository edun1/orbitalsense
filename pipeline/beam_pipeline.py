
import json
import apache_beam as beam

from pipeline.validation import validate_telemetry
from pipeline.parsing import parse_telemetry
from pipeline.freshness import classify_freshness, calculate_freshness_metrics
from pipeline.completeness import calculate_completeness_metrics

def add_freshness_status(event):
    """
    Add a freshness classification to a telemetry event.
    """

    event = event.copy()

    arrival_timestamp = event.get("arrival_timestamp")

    if not arrival_timestamp:
        event["freshness_status"] = "arrival_time_missing"
        return event

    try:
        event["freshness_status"] = classify_freshness(
            event["timestamp"],
            arrival_timestamp
        )
    except (ValueError, TypeError, KeyError, AttributeError):
        event["freshness_status"] = "invalid_timestamp"

    return event

def main():
    with beam.Pipeline(runner="DirectRunner") as pipeline:

        # Read and parse satellite telemetry


        # Read incoming telemetry messages
        raw_messages = (
            pipeline
            | "Read Telemetry" >> beam.io.ReadFromText(
                "telemetry_freshness_test.jsonl"
            )
        )

        # Safely parse each incoming message
        parsed_messages = (
            raw_messages
            | "Safe Parse JSON" >> beam.Map(parse_telemetry)
        )

        # Keep successfully parsed telemetry
        events = (
            parsed_messages
            | "Keep Parsed Events" >> beam.Filter(
                lambda event: event is not None
            )
        )

        # Identify malformed messages
        malformed_messages = (
            raw_messages
            | "Filter Malformed JSON" >> beam.Filter(
                lambda message: parse_telemetry(message) is None
            )
        )

        # Save malformed messages for investigation
        (
            malformed_messages
            | "Format Malformed Records" >> beam.Map(
                lambda message: json.dumps({
                    "reason": "malformed_json",
                    "raw_message": message
                })
            )
            | "Write Malformed Quarantine" >> beam.io.WriteToText(
                "beam_malformed_telemetry",
                file_name_suffix=".jsonl",
                shard_name_template=""
            )
        )

        # Count malformed messages
        (
            malformed_messages
            | "Count Malformed" >> beam.combiners.Count.Globally()
            | "Print Malformed Count" >> beam.Map(
                lambda count: print("Malformed JSON messages:", count)
            )
        )



        # Identify valid battery readings
        valid_events = (
            events
            | "Filter Valid" >> beam.Filter(validate_telemetry)
        )

        # Identify invalid battery readings
        invalid_events = (
            events
            | "Filter Invalid" >> beam.Filter(
                lambda event: not validate_telemetry(event)
            )
        )


        # Group telemetry by event ID
        grouped_events = (
            valid_events
            | "Key By Event ID" >> beam.Map(
                lambda event: (event["event_id"], event)
            )
            | "Group By Event ID" >> beam.GroupByKey()
        )

        # Keep one complete telemetry record per event ID
        unique_events = (
            grouped_events
            | "Keep One Event" >> beam.Map(
                lambda item: next(iter(item[1]))
            )
        )

        # Classify freshness of unique valid telemetry
        enriched_events = (
            unique_events
            | "Add Freshness Status" >> beam.Map(
                add_freshness_status
            )
        )



        # Calculate freshness KPIs
        freshness_metrics = (
            enriched_events
            | "Collect Freshness Events" >> beam.combiners.ToList()
            | "Calculate Freshness KPIs" >> beam.Map(
                calculate_freshness_metrics
            )
        )

        # Calculate completeness KPIs from valid, unique events
        completeness_metrics = (
            enriched_events
            | "Collect Completeness Events" >> beam.combiners.ToList()
            | "Calculate Completeness KPIs" >> beam.Map(
                calculate_completeness_metrics
            )
        )

        # Display completeness KPIs
        (
            completeness_metrics
            | "Print Completeness KPIs" >> beam.Map(
                lambda metrics: print(
                    "Completeness KPIs:",
                    json.dumps(metrics, indent=2)
                )
            )
        )

        # Save completeness KPIs as a JSON report
        (
            completeness_metrics
            | "Convert Completeness KPIs to JSON" >> beam.Map(
                json.dumps
            )
            | "Save Completeness KPI Report" >> beam.io.WriteToText(
                "beam_completeness_kpis",
                file_name_suffix=".json",
                shard_name_template=""
            )
        )


        # Display freshness KPIs
        (
            freshness_metrics
            | "Print Freshness KPIs" >> beam.Map(
                lambda metrics: print(
                    "Freshness KPIs:",
                    json.dumps(metrics, indent=2)
                )
            )
        )

        # Save freshness KPIs as a JSON report
        (
            freshness_metrics
            | "Convert Freshness KPIs to JSON" >> beam.Map(
                json.dumps
            )
            | "Write Freshness KPI Report" >> beam.io.WriteToText(
                "beam_freshness_kpis",
                file_name_suffix=".json",
                shard_name_template=""
            )
        )


        # Extract additional records sharing an event ID
        duplicate_events = (
            grouped_events
            | "Extract Duplicate Records" >> beam.FlatMap(
                lambda item: list(item[1])[1:]
            )
        )

        # Save duplicate telemetry records
        (
            duplicate_events
            | "Convert Duplicates to JSON" >> beam.Map(json.dumps)
            | "Write Duplicate Telemetry" >> beam.io.WriteToText(
                "beam_duplicate_telemetry",
                file_name_suffix=".jsonl",
                shard_name_template=""
            )
        )

        # Count additional records sharing an event ID
        duplicate_counts = (
            grouped_events
            | "Count Duplicates Per ID" >> beam.Map(
                lambda item: max(0, len(list(item[1])) - 1)
            )
            | "Total Duplicate Events" >> beam.CombineGlobally(sum)
        )

        (
            duplicate_counts
            | "Print Duplicate Count" >> beam.Map(
                lambda count: print("Duplicate events:", count)
            )
        )


        # Save complete, validated, deduplicated telemetry
        (
            enriched_events
            | "Convert Curated Events to JSON" >> beam.Map(
                json.dumps
            )
            | "Write Curated Telemetry" >> beam.io.WriteToText(
                "beam_curated_telemetry",
                file_name_suffix=".jsonl",
                shard_name_template=""
            )
        )

        # Count unique valid telemetry records
        (
            unique_events
            | "Count Unique Valid" >> beam.combiners.Count.Globally()
            | "Print Unique Valid" >> beam.Map(
                lambda count: print("Valid unique events:", count)
            )
        )

        # Save invalid telemetry for investigation
        (
            invalid_events
            | "Convert Quarantined Events to JSON" >> beam.Map(
                json.dumps
            )
            | "Write Quarantined Telemetry" >> beam.io.WriteToText(
                "beam_quarantine_telemetry",
                file_name_suffix=".jsonl",
                shard_name_template=""
            )
        )

        # Count quarantined telemetry records
        (
            invalid_events
            | "Count Invalid" >> beam.combiners.Count.Globally()
            | "Print Invalid" >> beam.Map(
                lambda count: print("Quarantined events:", count)
            )
        )


if __name__ == "__main__":
    main()
