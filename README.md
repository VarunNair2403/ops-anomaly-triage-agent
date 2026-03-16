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

- **Data security & PII handling.** Run against production incident stores over a private network, minimize fields sent to the LLM (no raw client identifiers), and log all access for audit. Where possible, keep processing in a VPC or on-prem model endpoint to avoid sending sensitive data to third parties. [web:271][web:275]

- **Model versioning & change management.** Pin a specific model + prompt version for triage, track changes in a structured changelog, and roll out new versions behind feature flags with the ability to instantly roll back if quality regresses. [web:277][web:280][web:283]

- **Guardrails and evaluations.** Add lightweight guardrails (regex/LLM-based classifiers) to prevent obviously incorrect or unsafe summaries, and maintain a small eval set of historical incident batches to regression-test severity labeling and action quality before any model update. [web:272][web:274][web:279][web:282][web:285]

- **Monitoring, logging, and SLAs.** Emit metrics for runs (latency, incident counts, severity mix, Slack/Jira success) and centralize logs so ops can trace any triage decision. Alert if runs fail, response times spike, or severity distribution looks anomalous over time. [web:273][web:274][web:279]

- **Cost and risk governance.** Cap daily LLM spend, periodically review prompts and outputs with risk/compliance, and document an incident-response playbook for any LLM failure modes (e.g., hallucinated actions, missed high-severity incidents). [web:271][web:275][web:276]


Run manually:

```bash
python triage.py --hours 48 --notify
