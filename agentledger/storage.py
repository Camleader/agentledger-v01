# Adding in the ability to read JSONL Logs 

import csv
import json
from pathlib import Path


class JsonlStorage:
    def __init__(self, path):
        self.path = Path(path)

    def write(self, event):
        with self.path.open("a", encoding="utf-8") as file:
            file.write(json.dumps(event) + "\n")

    def read_all(self):
        if not self.path.exists():
            return []

        events = []

        with self.path.open("r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()

                if not line:
                    continue

                events.append(json.loads(line))

        return events

    def export_json(self, events, path):
        export_path = Path(path)

        with export_path.open("w", encoding="utf-8") as file:
            json.dump(events, file, indent=2)

        return export_path

    def export_csv(self, events, path):
        export_path = Path(path)

        fieldnames = [
            "event_id",
            "timestamp",
            "event_type",
            "agent_name",
            "input_data",
            "output_data",
            "reason_codes",
            "metadata",
        ]

        with export_path.open("w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()

            for event in events:
                writer.writerow(
                    {
                        "event_id": event.get("event_id", ""),
                        "timestamp": event.get("timestamp", ""),
                        "event_type": event.get("event_type", ""),
                        "agent_name": event.get("agent_name", ""),
                        "input_data": json.dumps(event.get("input_data", {})),
                        "output_data": json.dumps(event.get("output_data", {})),
                        "reason_codes": json.dumps(event.get("reason_codes", [])),
                        "metadata": json.dumps(event.get("metadata", {})),
                    }
                )

        return export_path

    def export_markdown_report(self, events, path):
        export_path = Path(path)

        lines = [
            "# AgentLedger Audit Report",
            "",
            f"Total events: {len(events)}",
            "",
        ]

        for index, event in enumerate(events, start=1):
            lines.extend(
                [
                    f"## Event {index}",
                    "",
                    f"- **Event ID:** {event.get('event_id', '')}",
                    f"- **Timestamp:** {event.get('timestamp', '')}",
                    f"- **Event Type:** {event.get('event_type', '')}",
                    f"- **Agent Name:** {event.get('agent_name', '')}",
                    f"- **Input Data:** `{json.dumps(event.get('input_data', {}))}`",
                    f"- **Output Data:** `{json.dumps(event.get('output_data', {}))}`",
                    f"- **Reason Codes:** `{json.dumps(event.get('reason_codes', []))}`",
                    f"- **Metadata:** `{json.dumps(event.get('metadata', {}))}`",
                    "",
                ]
            )

        export_path.write_text("\n".join(lines), encoding="utf-8")

        return export_path
    


