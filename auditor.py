import json
import os
from datetime import UTC, datetime
from config import LOG_FILE


def log_interaction(question: str, tier: str, response: str, session_id: str = "unknown") -> None:
    """
    Append a structured record of this interaction to the audit log.

    TODO — Milestone 3:

    Before writing any code, complete specs/auditor-spec.md. The key decisions
    are what fields to log, how much of the question and response to include,
    and how to handle the logs/ directory not existing yet.

    Each record should be a JSON object written as a single line to LOG_FILE
    (defined in config.py as "logs/audit.jsonl").

    Required fields:
      - "timestamp"        : ISO 8601 datetime string
      - "tier"             : the safety tier assigned to this question
      - "question"         : the user's question (truncate to 300 chars if longer)
      - "response_preview" : first 200 characters of the response

    If the logs/ directory doesn't exist, create it before writing.

    Also print a one-line summary to the terminal so you can see logged
    interactions in real time without opening the file:
      e.g. [LOGGED] tier=caution | "How do I replace a faucet?" → 47 chars

    Design your log entry in specs/auditor-spec.md before implementing here.
    """
    #1. Create the logs directory if it doesn't exist
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

    #2. Prepare the log entry
    log_entry = {
        "timestamp": datetime.now(UTC).isoformat() + "Z",
        "tier": tier,
        "question": question[:300],  # Truncate to 300 chars
        "response_preview": response[:200],  # First 200 chars of the response
        "question_length": len(question),
        "session_id": session_id
    }

    #3. Write the log entry to the log file
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(log_entry) + "\n")
    preview = question[:50] + ("…" if len(question) > 50 else "")
    print(f'At timestamp: {log_entry["timestamp"]} for Session {log_entry["session_id"]}: [LOGGED] tier={tier} | "{preview}" → {len(response)} chars')
