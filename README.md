## Overview

## Problem

Ops and risk teams get noisy incident queues (late reports, limit breaches, outages) and spend time manually scanning for what is truly urgent

## Users

Primary users are the **ops / risk team** plus on-call engineers who respond to high-severity incidents

## Workflow

Cron or button → SQL (`ops.db`) → LLM summarize / classify → Slack notification (and future Jira auto-tickets)

## How I’d productionize this in a hedge fund setting

In a real hedge fund environment this prototype would evolve into a hardened service:

- **Authentication & RBAC.** Deploy the triage API behind SSO (e.g., Okta) and enforce role-based access so only approved ops/risk users can trigger runs or change thresholds.

- **Data security & PII handling.** Run against production incident stores over a private network, minimize fields sent to the LLM (no raw client identifiers), and log all access for audit. Where possible, keep processing in a VPC or on-prem model endpoint to avoid sending sensitive data to third parties.

- **Model versioning & change management.** Pin a specific model + prompt version for triage, track changes in a structured changelog, and roll out new versions behind feature flags with the ability to instantly roll back if quality regresses. 

- **Guardrails and evaluations.** Add lightweight guardrails (regex/LLM-based classifiers) to prevent obviously incorrect or unsafe summaries, and maintain a small eval set of historical incident batches to regression-test severity labeling and action quality before any model update. 

- **Monitoring, logging, and SLAs.** Emit metrics for runs (latency, incident counts, severity mix, Slack/Jira success) and centralize logs so ops can trace any triage decision. Alert if runs fail, response times spike, or severity distribution looks anomalous over time. 

- **Cost and risk governance.** Cap daily LLM spend, periodically review prompts and outputs with risk/compliance, and document an incident-response playbook for any LLM failure modes (e.g., hallucinated actions, missed high-severity incidents). 

## Project structure

High-level overview of the main files and what they do.

- `src/triage.py` – CLI orchestrator. Pulls recent incidents from the DB, calls the LLM to summarize/classify, prints the report, and (optionally) sends a Slack notification.

- `src/db.py` – Database access layer. Connects to `ops.db` (SQLite) and exposes `get_recent_open_incidents(hours)` to fetch incidents for the last N hours.

- `src/llm_client.py` – LLM client. Wraps the model API call and returns structured JSON: `summary`, `severity`, `actions` for a batch of incidents.

- `src/notifier.py` – Slack notifier. Formats the triage output into a readable Slack message and posts it to a channel via `SLACK_WEBHOOK_URL`.

- `src/debug_print_incidents.py` – Debug helper to print incidents from `ops.db` so you can inspect the raw data.

- `src/llm_smoketest.py` – LLM smoke test that runs a tiny hard-coded example through the LLM to validate the prompt and JSON schema.

- `schema.sql` – SQL schema for the `incidents` table.

- `seed_db.py` – Script to create and seed `ops.db` with example incidents.

- `ops.db` – Local SQLite database file containing incident rows used for triage.

- `.env` – Local environment variables (not committed), e.g., LLM API key.

- `README.md` – Overview, setup instructions, and how to run the triage agent.

- `PRD.md` – Product requirements document: background, goals, non-goals, user stories, and success metrics.

Run manually:

```bash
python -m src.triage --hours 48 --notify

