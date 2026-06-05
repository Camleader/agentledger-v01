# AgentLedger v0.1 Founder Demo Script

## One-sentence pitch

AgentLedger is an audit and approval layer for AI agents operating in regulated workflows.

## 30-second explanation

AI agents are starting to make recommendations and take actions in sensitive workflows like lending, insurance, healthcare, legal, and finance.

The problem is simple: companies need to prove what the agent did.

AgentLedger captures the agent's inputs, calculations, decision, risk flags, reason codes, human review status, and trace events, then exports everything as a structured audit record.

## Demo setup

This v0.1 demo uses a simulated HELOC underwriting agent.

The workflow is:

Log → Trace → Flag risk → Explain → Approve → Export

## What I will show

First, I can load a clean borrower scenario and run the agent.

AgentLedger captures the application data, calculates CLTV and DTI, produces an approval recommendation, explains the decision, and generates an exportable audit record.

Next, I can load a manual review case.

Here, the agent identifies higher risk conditions, flags them, explains why manual review is required, and allows a human reviewer to approve or reject the decision.

Finally, I can show the audit export.

The export creates a structured JSON record containing the full agent run: product metadata, borrower data, decision summary, calculations, reason codes, risk flags, human review status, and trace events.

## Why this matters

For AI startups selling into fintech or regulated enterprise customers, trust and compliance are blockers.

AgentLedger gives those companies a way to show that their agent decisions are traceable, reviewable, and exportable.

## Current status

AgentLedger v0.1 is a local prototype.

It does not include authentication, database storage, external APIs, or production compliance guarantees yet.

The current goal is to validate the core workflow and show why agent auditability matters.

## Next version

v0.2 will focus on turning AgentLedger into a developer SDK so builders can add audit logging to their own agents with simple Python commands.
