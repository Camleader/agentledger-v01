from datetime import datetime, timezone
from uuid import uuid4

from .events import (
    ALLOWED_APPROVAL_STATUSES,
    ALLOWED_POLICY_STATUSES,
    ALLOWED_RISK_LEVELS,
    ALLOWED_EVENT_TYPES,
    validate_allowed_value,
    validate_boolean,
    validate_dict,
    validate_event,
    validate_non_empty_string,
    validate_optional_string,
    validate_trace_id,
)
from .storage import JsonlStorage


class AgentLedger:
    def __init__(
        self,
        storage_path="agentledger_logs.jsonl",
        trace_storage_path="agentledger_traces.jsonl",
    ):
        self.storage = JsonlStorage(storage_path)
        self.trace_storage = JsonlStorage(trace_storage_path)

    def start_trace(self):
        return str(uuid4())

    def create_trace(
        self,
        workflow,
        agent_name,
        entity_id=None,
        metadata=None,
    ):
        validate_non_empty_string(workflow, "workflow")
        validate_non_empty_string(agent_name, "agent_name")

        if entity_id is not None:
            validate_non_empty_string(entity_id, "entity_id")

        metadata = metadata or {}
        validate_dict(metadata, "metadata")

        trace = {
            "trace_id": str(uuid4()),
            "workflow": workflow,
            "agent_name": agent_name,
            "entity_id": entity_id,
            "metadata": metadata,
            "status": "active",
            "outcome": None,
            "approval_status": "not_required",
            "started_at": datetime.now(timezone.utc).isoformat(),
            "completed_at": None,
        }

        self.trace_storage.write(trace)
        return trace

    def get_trace(self, trace_id):
        validate_trace_id(trace_id)

        for trace in self.trace_storage.read_all():
            if trace.get("trace_id") == trace_id:
                return {
                    "trace": trace,
                    "events": self.get_events_by_trace(trace_id),
                }

        raise ValueError(f"Trace not found: {trace_id}")


    def export_trace(self, trace_id):
        trace_record = self.get_trace(trace_id)
        trace = trace_record["trace"]
        events = trace_record["events"]

        decision_events = [
            event for event in events
            if event.get("event_type") == "decision"
        ]

        tool_call_events = [
            event for event in events
            if event.get("event_type") == "tool_call"
        ]

        risk_priority = {
            "low": 0,
            "medium": 1,
            "high": 2,
            "critical": 3,
        }

        highest_risk_level = "low"
        review_required = False

        for event in decision_events:
            risk_level = event.get("risk_level", "low")

            if risk_priority.get(risk_level, 0) > risk_priority[highest_risk_level]:
                highest_risk_level = risk_level

            if event.get("review_required", False):
                review_required = True

        return {
            "export_type": "AgentLedger Trace Audit Record",
            "trace": trace,
            "events": events,
            "summary": {
                "event_count": len(events),
                "tool_call_count": len(tool_call_events),
                "decision_count": len(decision_events),
                "review_required": review_required,
                "highest_risk_level": highest_risk_level,
            },
        }

    def complete_trace(
        self,
        trace_id,
        outcome,
        approval_status="not_required",
    ):
        validate_trace_id(trace_id)
        validate_non_empty_string(outcome, "outcome")
        validate_allowed_value(
            approval_status,
            "approval_status",
            ALLOWED_APPROVAL_STATUSES,
        )

        traces = self.trace_storage.read_all()
        completed_trace = None

        for trace in traces:
            if trace.get("trace_id") == trace_id:
                trace["status"] = "completed"
                trace["outcome"] = outcome
                trace["approval_status"] = approval_status
                trace["completed_at"] = datetime.now(timezone.utc).isoformat()
                completed_trace = trace
                break

        if completed_trace is None:
            raise ValueError(f"Trace not found: {trace_id}")

        self.trace_storage.replace_all(traces)
        return completed_trace

# Preserves the existing generic event logger while giving decisions events the new audit-review fields

    def log_event(
        self,
        event_type,
        agent_name,
        input_data=None,
        output_data=None,
        reason_codes=None,
        metadata=None,
        trace_id=None,
        action_status="executed",
        agent_id=None,
        agent_version=None,
        model_version=None,
        prompt_version=None,
        workflow_version=None,
        policy_version=None,
        extra_fields=None,
):
        
    
        input_data = input_data or {}
        output_data = output_data or {}
        reason_codes = reason_codes or []
        metadata = metadata or {}
        trace_id = trace_id or self.start_trace()
        validate_trace_id(trace_id)

        validate_optional_string(agent_id, "agent_id")
        validate_optional_string(agent_version, "agent_version")
        validate_optional_string(model_version, "model_version")
        validate_optional_string(prompt_version, "prompt_version")
        validate_optional_string(workflow_version, "workflow_version")
        validate_optional_string(policy_version, "policy_version")

        validate_event(
            event_type=event_type,
            agent_name=agent_name,
            input_data=input_data,
            output_data=output_data,
            reason_codes=reason_codes,
            metadata=metadata,
            trace_id=trace_id,
            action_status=action_status,
        )

        event = {
            "event_id": str(uuid4()),
            "trace_id": trace_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event_type": event_type,
            "agent_name": agent_name,
            "input_data": input_data,
            "output_data": output_data,
            "reason_codes": reason_codes,
            "metadata": metadata,
            "action_status": action_status,
            "agent_id": agent_id,
            "agent_version": agent_version,
            "model_version": model_version,
            "prompt_version": prompt_version,
            "workflow_version": workflow_version,
            "policy_version": policy_version,
        }

        if extra_fields:
            event.update(extra_fields)

        self.storage.write(event)
        return event

        event["prev_hash"] = self.storage.get_last_hash()
        event["sha256"] = self.storage.compute_hash(event)
        self.storage.write(event)
        return event

    def log_decision(  
        self,
        agent_name,
        input_data=None,
        output_data=None,
        reason_codes=None,
        metadata=None,
        trace_id=None,
        risk_level="low",
        review_required=False,
        review_reason=None,
        policy_status="not_evaluated",
        approval_status="not_required",
        action_status="executed",
        agent_id=None,
        agent_version=None,
        model_version=None,
        prompt_version=None,
        workflow_version=None,
        policy_version=None,
    ):
        validate_allowed_value(
            risk_level,
            "risk_level",
            ALLOWED_RISK_LEVELS,
        )
        validate_boolean(review_required, "review_required")
        validate_optional_string(review_reason, "review_reason")
        validate_allowed_value(
            policy_status,
            "policy_status",
            ALLOWED_POLICY_STATUSES,
        )
        validate_allowed_value(
            approval_status,
            "approval_status",
            ALLOWED_APPROVAL_STATUSES,
        )

        event = self.log_event(
            event_type="decision",
            agent_name=agent_name,
            input_data=input_data,
            output_data=output_data,
            reason_codes=reason_codes,
            metadata=metadata,
            trace_id=trace_id,
            action_status=action_status,
            agent_id=agent_id,
            agent_version=agent_version,
            model_version=model_version,
            prompt_version=prompt_version,
            workflow_version=workflow_version,
            policy_version=policy_version,
        )

        event["risk_level"] = risk_level
        event["review_required"] = review_required
        event["review_reason"] = review_reason
        event["policy_status"] = policy_status
        event["approval_status"] = approval_status

        events = self.storage.read_all()
        events[-1] = event
        self.storage.replace_all(events)

        return event

    def log_tool_call(
        self,
        agent_name,
        tool_name,
        input_data=None,
        output_data=None,
        metadata=None,
        trace_id=None,
        action_status="executed",
        agent_id=None,
        agent_version=None,
        model_version=None,
        prompt_version=None,
        workflow_version=None,
        policy_version=None,
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
            trace_id=trace_id,
            action_status=action_status,
            agent_id=agent_id,
            agent_version=agent_version,
            model_version=model_version,
            prompt_version=prompt_version,
            workflow_version=workflow_version,
            policy_version=policy_version,
        )

    def log_action(
        self,
        agent_name,
        action_name,
        input_data=None,
        output_data=None,
        reason_codes=None,
        metadata=None,
        trace_id=None,
        action_status="executed",
        agent_id=None,
        agent_version=None,
        model_version=None,
        prompt_version=None,
        workflow_version=None,
        policy_version=None,
    ):
        validate_non_empty_string(action_name, "action_name")

        return self.log_event(
            event_type="action",
            agent_name=agent_name,
            input_data=input_data,
            output_data=output_data,
            reason_codes=reason_codes,
            metadata={
                **(metadata or {}),
                "action_name": action_name,
            },
            trace_id=trace_id,
            action_status=action_status,
            agent_id=agent_id,
            agent_version=agent_version,
            model_version=model_version,
            prompt_version=prompt_version,
            workflow_version=workflow_version,
            policy_version=policy_version,
        )


    def list_events(self):
        return self.storage.read_all()
    
    def verify_hash_chain(self):
        return self.storage.verify_hash_chain()

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

    def get_events_by_trace(self, trace_id):
        validate_trace_id(trace_id)

        return [
            event
            for event in self.list_events()
            if event.get("trace_id") == trace_id
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
