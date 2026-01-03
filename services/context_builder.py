# services/context_builder.py

from services.db_context_resolver import resolve_context_from_db
from memory.session import get_session_context, append_session_context


def build_context(question: str, session_id: str, db_session) -> str:
    """
    Builds final trusted context for LLM.
    Order matters:
    1. Session memory (short)
    2. Database facts
    """

    session_context = get_session_context(session_id)
    db_context = resolve_context_from_db(question, db_session)

    final_context = ""

    if session_context:
        final_context += f"PAST CONTEXT:\n{session_context}\n\n"

    if db_context:
        final_context += f"FACTS FROM DATABASE:\n{db_context}\n\n"

    # Update memory (temporary)
    append_session_context(session_id, f"User: {question}")

    return final_context.strip()
