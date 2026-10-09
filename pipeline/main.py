
import json

from pipeline.validation import validate_telemetry
from pipeline.deduplication import remove_duplicates


def main():
    # Read the satellite telemetry
    with open("docker_telemetry.jsonl", "r") as file:
        events = [json.loads(line) for line in file]

    # Step 1: Remove duplicate events
    unique_events, duplicate_events = remove_duplicates(events)

    # Step 2: Validate battery readings
    valid_events = []
    invalid_events = []

    for event in unique_events:
        if validate_telemetry(event):
            valid_events.append(event)
        else:
            invalid_events.append(event)

    # Step 3: Save the results
    outputs = {
        "valid_telemetry.jsonl": valid_events,
        "quarantine_telemetry.jsonl": invalid_events,
        "duplicate_telemetry.jsonl": duplicate_events,
    }

    for filename, records in outputs.items():
        with open(filename, "w") as file:
            for record in records:
                file.write(json.dumps(record) + "\n")

    print("Total events:", len(events))
    print("Valid unique events:", len(valid_events))
    print("Quarantined events:", len(invalid_events))
    print("Duplicate events:", len(duplicate_events))


if __name__ == "__main__":
    main()
