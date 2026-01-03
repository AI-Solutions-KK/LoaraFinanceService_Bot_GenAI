# memory/session.py

# TEMPORARY in-memory store
# Clears automatically on server restart

_SESSION_STORE = {}


def get_session_context(session_id: str) -> str:
    return _SESSION_STORE.get(session_id, "")


def append_session_context(session_id: str, text: str):
    existing = _SESSION_STORE.get(session_id, "")
    updated = (existing + "\n" + text).strip()
    _SESSION_STORE[session_id] = updated


def clear_session(session_id: str):
    _SESSION_STORE.pop(session_id, None)
