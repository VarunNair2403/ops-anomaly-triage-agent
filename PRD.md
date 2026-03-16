# Ops Anomaly Triage Agent – PRD

## Background

Ops and risk teams receive a continuous stream of incidents (late reports, limit breaches, outages). Today, analysts manually scan these queues, try to spot patterns, and decide what deserves urgent attention. This is slow, inconsistent across people, and easy to miss when volumes spike.

The goal of this project is to use an LLM to summarize recent incidents, assign an overall severity, and push a concise triage view into Slack so on‑call humans can respond faster and more consistently.

## Goals

- Automatically summarize recent incidents (last N hours) into a short narrative that a human can read in under 30 seconds.
- Assign an overall severity level (e.g., low / medium / high) for the batch of incidents.
- Recommend 2–4 concrete next actions for the ops / risk team.
- Deliver the triage output into a Slack channel that on‑call engineers and analysts already monitor.

## Non‑Goals (V1)

- Replacing existing systems of record such as ServiceNow/Jira.
- Making autonomous trading or risk limit decisions.
- Building dashboards or a full web UI; Slack is the primary UX for V1.
- Implementing complex approval workflows or RBAC beyond basic access to run the script.

## Users

- **Ops / risk analysts** who monitor incident queues and need a quick picture of current risk.
- **On‑call engineers** who need to know when an operational issue (e.g., outage, pricing error) is severe enough to jump on.
- **Risk leads / managers** who want more consistent severity classification across shifts.

## User Stories

- As an ops analyst, I want a single Slack message summarizing the last N hours of incidents so I can quickly understand whether risk is elevated.
- As an on‑call engineer, I want high‑severity batches to show up in my Slack channel with clear recommended actions so I know what to do next.
- As a risk lead, I want severity classification to be consistent over time so I can compare incident load between days and across desks.
- As a platform owner, I want a simple CLI and cron‑friendly entry point so I can schedule triage runs without manual work.

## Workflow (V1)

1. Cron job or human runs `python triage.py --hours N --notify`.
2. Script queries `ops.db` (SQLite) for open incidents in the last N hours.
3. Incidents are serialized and sent to an LLM for summarization, severity, and action generation.
4. Results are printed to the console and posted into a Slack channel via Incoming Webhook.

Future variants may add automatic Jira ticket creation for high‑severity batches.

## Scope (V1)

In scope:

- SQLite backing store (`ops.db`) with seeded example incidents.
- Python CLI (`triage.py`) with `--hours` and `--notify` flags.
- LLM client that returns a structured JSON payload: `summary`, `severity`, `actions`.
- Slack notification with a formatted message (summary, top incidents, recommended actions).

Out of scope for V1 (future work):

- Model evaluations, guardrails, and calibration against historical incidents.
- Authentication / SSO and per‑user permissions.
- Dashboards, web UI, and long‑term triage history storage.
- Full Jira / ServiceNow integration.

## Success Metrics

Directional metrics for a real deployment:

- Reduction in manual triage time per batch (e.g., from ~10 minutes to <2 minutes).
- Percentage of on‑call shifts where the triage agent is used at least once.
- Consistency of severity ratings for similar incident patterns over time.
- User feedback from ops / risk team (e.g., “triage summary helpful?” thumbs‑up rate in Slack).

For this project as a portfolio piece:

- Clear, reproducible README and setup instructions.
- At least one example Slack screenshot showing a high‑severity triage summary.
- Code structured so it is easy to extend with guardrails, evals, and Jira integration in a V2.
