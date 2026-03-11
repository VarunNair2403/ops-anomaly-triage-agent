# Ops Anomaly Triage Agent

An internal AI agent that scans recent operational incidents from a SQL database, summarizes patterns, classifies overall severity (low/medium/high), and triggers Slack/Jira alerts so ops and engineering teams can triage faster.

## What it does

- Pulls recent incidents from a SQLite/Postgres database
- Uses an LLM to summarize patterns and classify severity
- Sends a formatted alert to Slack (and optionally creates Jira tickets)
- Exposes a simple CLI (and later API) to run triage on-demand or on a schedule
