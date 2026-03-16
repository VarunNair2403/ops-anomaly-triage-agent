import os
import json
import requests
from typing import List, Dict, Any

SLACK_WEBHOOK_URL = os.environ.get("SLACK_WEBHOOK_URL")


def format_triage_message(
    severity: str,
    summary: str,
    actions: List[str],
    incidents: List[Dict[str, Any]],
) -> dict:
    title = f":rotating_light: Ops triage – severity *{severity.upper()}*"

    incident_lines = []
    for inc in incidents[:5]:
        incident_lines.append(
            f"- `{inc['id']}` | {inc['desk']} | {inc['type']} | {inc['status']} | {inc['amount']}"
        )
    if len(incidents) > 5:
        incident_lines.append(f"...and {len(incidents) - 5} more open incidents")

    actions_text = "\n".join(f"- {a}" for a in actions)

    text = f"{title}\n\n*Summary*\n{summary}\n\n*Top incidents*\n" + "\n".join(
        incident_lines
    ) + f"\n\n*Recommended actions*\n{actions_text}"

    return {"text": text}


def send_slack_notification(payload: dict) -> None:
    if not SLACK_WEBHOOK_URL:
        print("SLACK_WEBHOOK_URL not set, skipping Slack notification.")
        return

    headers = {"Content-Type": "application/json"}
    resp = requests.post(SLACK_WEBHOOK_URL, data=json.dumps(payload), headers=headers)
    if resp.status_code != 200:
        raise RuntimeError(
            f"Slack webhook error {resp.status_code}: {resp.text}"
        )
