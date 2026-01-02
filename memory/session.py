# memory/session.py
import uuid

def new_session_id():
    return str(uuid.uuid4())
