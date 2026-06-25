from datetime import datetime, timezone
from uuid import uuid4

from .events import (
    ALLOWED_EVENT_TYPES,
    validate_event,
    validate_non_empty_string,
)
from .storage import JsonlStorage


class AgentLedger:
    def __init__(self, storage_path="agentledger_logs.jsonl"):
        self.storage = JsonlStorage(storage_path)

    def log_event(
        self,
        event_type,
        agent_name,
        input_data=None,
        output_data=None,
        reason_codes=None,
        metadata=None,
    ):
        input_data = input_data or {}
        output_data = output_data or {}
        reason_codes = reason_codes or []
        metadata = metadata or {}

        validate_event(
            event_type=event_type,
            agent_name=agent_name,
            input_data=input_data,
            output_data=output_data,
            reason_codes=reason_codes,
            metadata=metadata,
        )

        event = {
            "event_id": str(uuid4()),
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event_type": event_type,
            "agent_name": agent_name,
            "input_data": input_data,
            "output_data": output_data,
            "reason_codes": reason_codes,
            "metadata": metadata,
        }

        self.storage.write(event)
        return event

    def log_decision(
        self,
        agent_name,
        input_data=None,
        output_data=None,
        reason_codes=None,
        metadata=None,
    ):
        return self.log_event(
            event_type="decision",
            agent_name=agent_name,
            input_data=input_data,
            output_data=output_data,
            reason_codes=reason_codes,
            metadata=metadata,
        )

    def log_tool_call(
        self,
        agent_name,
        tool_name,
        input_data=None,
        output_data=None,
        metadata=None,
    ):
        if not isinstance(tool_name, str) or not tool_name.strip():
            raise ValueError("tool_name is required and must be a non-empty string.")

        return self.log_event(
            event_type="tool_call",
            agent_name=agent_name,
            input_data=input_data,
            output_data=output_data,
            reason_codes=[],
            metadata={
                **(metadata or {}),
                "tool_name": tool_name,
            },
        )

    def list_events(self):
        return self.storage.read_all()

    def get_events_by_type(self, event_type):
        validate_non_empty_string(event_type, "event_type")

        if event_type not in ALLOWED_EVENT_TYPES:
            allowed_types = ", ".join(sorted(ALLOWED_EVENT_TYPES))
            raise ValueError(f"event_type must be one of: {allowed_types}.")

        return [
            event
            for event in self.list_events()
            if event["event_type"] == event_type
        ]

    def get_events_by_agent(self, agent_name):
        validate_non_empty_string(agent_name, "agent_name")
    

        return [
            event
            for event in self.list_events()
            if event["agent_name"] == agent_name
        ]
    
    def export_json(self, path, events=None):
        events_to_export = events if events is not None else self.list_events()
        return self.storage.export_json(events_to_export, path)

    def export_csv(self, path, events=None):
        events_to_export = events if events is not None else self.list_events()
        return self.storage.export_csv(events_to_export, path)

    def export_markdown_report(self, path, events=None):
        events_to_export = events if events is not None else self.list_events()
        return self.storage.export_markdown_report(events_to_export, path)