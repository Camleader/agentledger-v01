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
