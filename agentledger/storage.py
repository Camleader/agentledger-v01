# Adding in the ability to read JSONL Logs 

import csv
import json
from pathlib import Path


class JsonlStorage:
    def __init__(self, path):
        self.path = Path(path)

    def compute_hash(self, record):
        record_to_hash = dict(record)
        record_to_hash.pop("sha256", None)

        encoded_record = json.dumps(
            record_to_hash,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")

        return hashlib.sha256(encoded_record).hexdigest()

    def get_last_hash(self):
        events = self.read_all()

        if not events:
            return None

        return events[-1].get("sha256")
    
    def verify_hash_chain(self):
        records = self.read_all()
        previous_hash = None

        for index, record in enumerate(records):
            if record.get("prev_hash") != previous_hash:
                return {
                    "valid": False,
                    "error": f"Invalid prev_hash at record {index}",
                    "index": index,
                }

            expected_hash = self.compute_hash(record)

            if record.get("sha256") != expected_hash:
                return {
                    "valid": False,
                    "error": f"Invalid sha256 at record {index}",
                    "index": index,
                }

            previous_hash = record.get("sha256")

        return {
            "valid": True,
            "total_records": len(records),
        }

    def write(self, event):
        event["sha256"] = self.compute_hash(event)
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
    
    def replace_all(self, records):
       with self.path.open("w", encoding="utf-8") as file:
            for record in records:
             file.write(json.dumps(record) + "\n")

    def export_json(self, events, path):
        export_path = Path(path)

        with export_path.open("w", encoding="utf-8") as file:
            json.dump(events, file, indent=2)

        return export_path

    def export_csv(self, events, path):
        export_path = Path(path)

        fieldnames = [
            "event_id",
            "trace_id",
            "timestamp",
            "event_type",
            "agent_name",
            "input_data",
            "output_data",
            "reason_codes",
            "metadata",
            "action_status",
            "risk_level",
            "review_required",
            "review_reason",
            "policy_status",
            "approval_status",
            "agent_id",
            "agent_version",
            "model_version",
            "prompt_version",
            "workflow_version",
            "policy_version",
            "prev_hash",
            "sha256",
        ]

        with export_path.open("w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()

            for event in events:
                writer.writerow(
                    {
                        "event_id": event.get("event_id", ""),
                        "trace_id": event.get("trace_id", ""),
                        "timestamp": event.get("timestamp", ""),
                        "event_type": event.get("event_type", ""),
                        "agent_name": event.get("agent_name", ""),
                        "input_data": json.dumps(event.get("input_data", {})),
                        "output_data": json.dumps(event.get("output_data", {})),
                        "reason_codes": json.dumps(event.get("reason_codes", [])),
                        "metadata": json.dumps(event.get("metadata", {})),
                        "action_status": event.get("action_status", ""),
                        "risk_level": event.get("risk_level", ""),
                        "review_required": event.get("review_required", ""),
                        "review_reason": event.get("review_reason", ""),
                        "policy_status": event.get("policy_status", ""),
                        "approval_status": event.get("approval_status", ""),
                        "agent_id": event.get("agent_id", ""),
                        "agent_version": event.get("agent_version", ""),
                        "model_version": event.get("model_version", ""),
                        "prompt_version": event.get("prompt_version", ""),
                        "workflow_version": event.get("workflow_version", ""),
                        "policy_version": event.get("policy_version", ""),
                        "prev_hash": event.get("prev_hash", ""),
                        "sha256": event.get("sha256", ""),
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
                    f"- **Trace ID:** {event.get('trace_id', '')}",
                    f"- **Input Data:** `{json.dumps(event.get('input_data', {}))}`",
                    f"- **Output Data:** `{json.dumps(event.get('output_data', {}))}`",
                    f"- **Reason Codes:** `{json.dumps(event.get('reason_codes', []))}`",
                    f"- **Metadata:** `{json.dumps(event.get('metadata', {}))}`",
                    f"- **Action Status:** {event.get('action_status', '')}",
                    f"- **Risk Level:** {event.get('risk_level', '')}",
                    f"- **Review Required:** {event.get('review_required', '')}",
                    f"- **Review Reason:** {event.get('review_reason', '')}",
                    f"- **Policy Status:** {event.get('policy_status', '')}",
                    f"- **Approval Status:** {event.get('approval_status', '')}",
                    f"- **Agent ID:** {event.get('agent_id', '')}",
                    f"- **Agent Version:** {event.get('agent_version', '')}",
                    f"- **Model Version:** {event.get('model_version', '')}",
                    f"- **Prompt Version:** {event.get('prompt_version', '')}",
                    f"- **Workflow Version:** {event.get('workflow_version', '')}",
                    f"- **Policy Version:** {event.get('policy_version', '')}",
                    f"- **Previous Hash:** {event.get('prev_hash', '')}",
                    f"- **SHA256:** {event.get('sha256', '')}",
                    "",
                ]
            )

        export_path.write_text("\n".join(lines), encoding="utf-8")

        return export_path
    
import hashlib
    


