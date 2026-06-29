# Validation Logic Step 3 v0.2.6

ALLOWED_EVENT_TYPES = {
    "event",
    "decision",
    "tool_call",
}
ALLOWED_RISK_LEVELS = {
    "low",
    "medium",
    "high",
    "critical",
}

ALLOWED_POLICY_STATUSES = {
    "pass",
    "warning",
    "fail",
    "not_evaluated",
}

ALLOWED_APPROVAL_STATUSES = {
    "not_required",
    "pending",
    "approved",
    "rejected",
}

def validate_non_empty_string(value, field_name):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} is required and must be a non-empty string.")


def validate_dict(value, field_name):
    if not isinstance(value, dict):
        raise ValueError(f"{field_name} must be a dictionary.")


def validate_list(value, field_name):
    if not isinstance(value, list):
        raise ValueError(f"{field_name} must be a list.")
    
def validate_boolean(value, field_name):
    if not isinstance(value, bool):
        raise ValueError(f"{field_name} must be a boolean.")


def validate_optional_string(value, field_name):
    if value is not None:
        validate_non_empty_string(value, field_name)


def validate_allowed_value(value, field_name, allowed_values):
    validate_non_empty_string(value, field_name)

    if value not in allowed_values:
        allowed = ", ".join(sorted(allowed_values))
        raise ValueError(f"{field_name} must be one of: {allowed}.")


def validate_trace_id(trace_id):
    validate_non_empty_string(trace_id, "trace_id")


def validate_event(
    event_type,
    agent_name,
    input_data,
    output_data,
    reason_codes,
    metadata,
    trace_id,
):
    validate_non_empty_string(event_type, "event_type")

    if event_type not in ALLOWED_EVENT_TYPES:
        allowed_types = ", ".join(sorted(ALLOWED_EVENT_TYPES))
        raise ValueError(f"event_type must be one of: {allowed_types}.")

    validate_non_empty_string(agent_name, "agent_name")
    validate_dict(input_data, "input_data")
    validate_dict(output_data, "output_data")
    validate_list(reason_codes, "reason_codes")
    validate_dict(metadata, "metadata")
    validate_trace_id(trace_id)




# This keeps the SDK controlled 

# Step 4 Add Validations Functions 
# THe file will check things like: 
    #Is event_type allowed?
    #Is agent_name a real non-empty string?
    #Is input_data a dictionary?
    #Is output_data a dictionary?
    #Is reason_codes a list?
    #Is metadata a dictionary?
    # This gives AgentLedger guardrails 