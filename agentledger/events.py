# Validation Logic Step 3 v0.2.2 

ALLOWED_EVENT_TYPES = {
    "event",
    "decision",
    "tool_call",
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


def validate_event(
    event_type,
    agent_name,
    input_data,
    output_data,
    reason_codes,
    metadata,
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