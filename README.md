# Ops Anomaly Triage Agent

## Problem

Ops and risk teams get noisy incident queues (late reports, limit breaches, outages) and spend time manually scanning for what is truly urgent.

## Users

Primary users are the **ops / risk team** plus on-call engineers who respond to high-severity incidents.

## Workflow

Cron or button → SQL (`ops.db`) → LLM summarize / classify → Slack notification (and future Jira auto-tickets).

Run manually:

```bash
python triage.py --hours 48 --notify
