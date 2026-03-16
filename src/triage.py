# triage.py

import argparse
from src.db import get_recent_open_incidents
from src.llm_client import summarize_incidents
from src.notifier import format_triage_message, send_slack_notification

def run_triage(hours: int = 24, notify: bool = False, auto_jira: bool = False):
    incidents = get_recent_open_incidents(hours=hours)

    if not incidents:
        print(f"No open incidents in the last {hours} hours.")
        return

    print(f"Found {len(incidents)} open incidents in the last {hours} hours.\n")

    result = summarize_incidents(incidents)
    summary = result["summary"]
    severity = result["severity"]
    actions = result["actions"]

    print(f"Overall severity: {severity.upper()}\n")
    print("Summary:")
    print(summary)
    print("\nRecommended actions:")
    for a in actions:
        print(f"- {a}")

    if notify:
        payload = format_triage_message(severity, summary, actions, incidents)
        send_slack_notification(payload)
        print("\nSent Slack notification.")



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run ops anomaly triage.")
    parser.add_argument("--hours", type=int, default=24)
    parser.add_argument("--notify", action="store_true")
    parser.add_argument(
        "--auto-jira",
        action="store_true",
        help="Future: automatically open Jira tickets for high severity.",
    )
    args = parser.parse_args()

    run_triage(hours=args.hours, notify=args.notify, auto_jira=args.auto_jira)

