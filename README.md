## Overview

Ops Anomaly Triage Agent is a small internal AI agent that scans recent operational incidents from a SQL database, summarizes patterns, classifies overall severity, and triggers alerts to downstream tools (Slack now, Jira next). It is meant to mimic the kind of self‑service AI agents that infra and SRE teams use to reduce noise and speed up incident response.

Today, the project includes:
- A SQLite schema and seed script for synthetic incident data
- A Python service that can read incidents and call an LLM
- A basic agent loop that can be extended with notifications, configs, and evaluations
