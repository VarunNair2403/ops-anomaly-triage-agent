from dotenv import load_dotenv
import os
from typing import List, Dict, Any
from openai import OpenAI

load_dotenv()
_api_key = os.getenv("OPENAI_API_KEY")
assert _api_key, "OPENAI_API_KEY is not set in .env"

_client = OpenAI(api_key=_api_key)


def summarize_incidents(incidents: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    incidents: list of dicts with keys:
      - desk
      - type
      - amount
      - status
      - created_at
    Returns dict with keys: summary (str), severity (str), actions (List[str]).
    """
    if not incidents:
        return {
            "summary": "No incidents in the selected window.",
            "severity": "low",
            "actions": [],
        }

    # Format incidents into a compact table-like text
    lines = []
    for inc in incidents:
        line = (
            f"{inc['created_at']} | {inc['desk']} | {inc['type']} | "
            f"{inc['status']} | {inc['amount']}"
        )
        lines.append(line)
    incidents_text = "\n".join(lines)

    prompt = f"""
You are an experienced operations risk analyst.

You are given a list of recent incidents, one per line, in the format:
timestamp | desk | type | status | amount

Incidents:
{incidents_text}

Your task:

1. Summarize key patterns in 3–5 bullet points.
2. Classify the overall severity as one of: low, medium, high.
   - Use "high" if there are large amounts, many open incidents on the same desk,
     or repeated critical types like SystemOutage or LimitBreach.
3. Propose 2–3 concrete next actions for the ops/engineering teams.

Return your answer as strict JSON with this schema:

{{
  "summary": "short paragraph or bullet list as plain text",
  "severity": "low" | "medium" | "high",
  "actions": ["action 1", "action 2", "action 3"]
}}

Do not include any extra keys or text outside the JSON.
"""

    response = _client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": "You are a precise assistant that outputs valid JSON only."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
    )

    content = response.choices[0].message.content.strip()

    # Basic JSON parse with a fallback error structure
    import json

    try:
        parsed = json.loads(content)
    except json.JSONDecodeError:
        parsed = {
            "summary": f"Model returned non-JSON content: {content[:200]}",
            "severity": "medium",
            "actions": [],
        }

    # Normalize fields
    summary = parsed.get("summary", "").strip()
    severity = parsed.get("severity", "low").lower()
    actions = parsed.get("actions", [])
    if not isinstance(actions, list):
        actions = [str(actions)]

    return {
        "summary": summary,
        "severity": severity,
        "actions": actions,
    }


if __name__ == "__main__":
    # Simple manual test
    sample_incidents = [
        {
            "desk": "Equities",
            "type": "TradeBreak",
            "amount": 50000.0,
            "status": "open",
            "created_at": "2026-03-15T10:00:00",
        },
        {
            "desk": "Macro",
            "type": "SystemOutage",
            "amount": 150000.0,
            "status": "open",
            "created_at": "2026-03-15T09:30:00",
        },
    ]
    result = summarize_incidents(sample_incidents)
    print(result)
