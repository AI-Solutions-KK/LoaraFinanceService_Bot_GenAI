# memory/session.py

from typing import Dict, List

# In-memory store (safe for Phase-1 / replaceable later)
_SESSION_STORE: Dict[str, List[dict]] = {}

MAX_TURNS = 10  # keep memory bounded


def get_session(session_id: str) -> List[dict]:
    return _SESSION_STORE.get(session_id, [])


def add_message(session_id: str, role: str, content: str):
    history = _SESSION_STORE.get(session_id, [])
    history.append({"role": role, "content": content})

    # Trim old messages
    if len(history) > MAX_TURNS:
        history = history[-MAX_TURNS:]

    _SESSION_STORE[session_id] = history


def build_context(session_id: str) -> str:
    """
    Convert session messages into compact context for LLM.
    """
    history = get_session(session_id)

    if not history:
        return ""

    lines = []
    for msg in history:
        prefix = "User" if msg["role"] == "user" else "Assistant"
        lines.append(f"{prefix}: {msg['content']}")

    return "\n".join(lines)
