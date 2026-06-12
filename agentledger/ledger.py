from datetime import datetime, timezone
from uuid import uuid4


class AgentLedger:
    """In-memory audit ledger for local AgentLedger demos."""

    def __init__(self):
        self.events = []

    def log_event(self, step, action, input_data, output_data, risk_level="low"):
        event = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event_id": str(uuid4()),
            "step": step,
            "action": action,
            "input": input_data,
            "output": output_data,
            "risk_level": risk_level,
        }
        self.events.append(event)
        return event

    def get_trace(self):
        return list(self.events)

    def get_audit_record(self):
        return {
            "ledger_version": "v0.1.4",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "event_count": len(self.events),
            "trace": self.get_trace(),
        }
        #v0.2.1 Added the SDK Core Class 
    from datetime import datetime, timezone
from uuid import uuid4

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
        event = {
            "event_id": str(uuid4()),
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event_type": event_type,
            "agent_name": agent_name,
            "input_data": input_data or {},
            "output_data": output_data or {},
            "reason_codes": reason_codes or [],
            "metadata": metadata or {},
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
