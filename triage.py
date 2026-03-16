# triage.py

import argparse
# existing imports...

def run_triage(hours: int = 24, notify: bool = False, auto_jira: bool = False):
    incidents = get_recent_open_incidents(hours=hours)
    if not incidents:
        print(f"No open incidents in the last {hours} hours.")
        return

    # ...existing LLM + print + Slack logic...

    if auto_jira:
        # Placeholder for future Jira integration
        print("\n[auto-jira] Jira integration not implemented yet (V2 idea).")


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
