# Changelog

All notable changes to AgentLedger are documented in this file.

## [0.3.2] - 2026-08-17

### Added

- Added an official six-event end-to-end underwriting demo with deterministic mock tools.
- Added repeatable JSON, CSV, Markdown, raw-log, and trace-level demo exports.
- Added one end-to-end contract test covering event order, exports, repeat runs, workflow completion, and integrity verification.
- Added a 60-second README path and a “How AgentLedger Works” explanation.
- Added packaged examples and a `dev` installation extra for pytest.
- Added regression coverage for decision-event and completed-trace hash-chain integrity.

### Changed

- Rebuilt hash links when records are rewritten and ensured final decision-review fields are hashed before storage.
- Updated the founder demo walkthrough to match the official v0.3.2 command and output.
- Aligned active package, SDK, legacy audit-export, app, documentation, and test version references to v0.3.2.
- Removed generated v0.3.1 validation logs and reports from the tracked source tree.

### Validation

- 61 automated tests passing from the repository checkout.
- Source distribution and wheel build successfully.
- 61 automated tests passing from the extracted source distribution.
- Clean wheel installation reports version `0.3.2`.
- The packaged end-to-end demo produces six events and valid event and trace hash chains.

## v0.3.1 - Evidence & Integrity Polish - 2026-07-25

- Added `log_action()` for audit logging real-world agent actions.
- Added `action_status` support for executed, denied, failed, and held-for-review actions.
- Added attribution fields for agent, model, prompt, workflow, and policy versions.
- Added tamper-evident event hashing with `prev_hash` and `sha256`.
- Added `verify_hash_chain()` to validate log integrity offline.
- Added tamper detection coverage for modified JSONL records.
- Updated CSV exports to include new audit fields.
- Updated Markdown audit reports to include new audit fields.
- Confirmed full test suite passes with 58 tests.

## [0.3.0] - 2026-07-06

### Added

- Persistent trace records stored separately from event logs.
- `create_trace()` for creating structured workflow traces.
- `get_trace()` for retrieving trace metadata and related events.
- `complete_trace()` for recording final workflow outcome, approval status, and completion timestamp.
- Risk and review controls on decision events:
  - `risk_level`
  - `review_required`
  - `review_reason`
  - `policy_status`
  - `approval_status`
- `export_trace()` for generating a complete trace-level audit record.
- Trace-level export summaries for event count, tool-call count, decision count, review requirement, and highest risk level.
- Underwriting audit demo showing an end-to-end AI-agent review workflow.
- Minimal quickstart example for new developers.
- Validation coverage for trace lifecycle, review fields, exports, and edge cases.

### Changed

- Updated package version to `0.3.0`.
- Updated README around the v0.3.0 SDK workflow and runnable examples.
- Updated legacy audit-export version metadata to `v0.3.0`.

### Validation

- 41 automated tests passing.
- Source distribution and wheel build successfully.
- Wheel installation and smoke test completed in a clean virtual environment.
