# api/api.py

from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy.orm import Session

from db.config import engine
from services.finance_service import is_emi_question, handle_emi_query
from services.llm_answer_engine import LLMAnswerEngine
from llm.client import GroqLLMClient
from memory.session import add_message, build_context

app = FastAPI(title="Production-grade Finance Assistant API")

llm = GroqLLMClient()
llm_engine = LLMAnswerEngine()


class ChatRequest(BaseModel):
    message: str
    session_id: str = "default"


@app.get("/")
def root():
    return {"status": "API is running. Use /docs to test."}


@app.post("/chat")
def chat(req: ChatRequest):
    session = Session(bind=engine)

    # ✅ Store user message
    add_message(req.session_id, "user", req.message)

    # ---- EMI FLOW ----
    if is_emi_question(req.message):
        emi_data = handle_emi_query(req.message, session)

        if "error" in emi_data:
            return {"response": emi_data["error"], "session_id": req.session_id}

        explanation = llm_engine.explain_emi(emi_data)

        # ✅ Store assistant response
        add_message(req.session_id, "assistant", explanation)

        return {
            "response": explanation,
            "data": emi_data,
            "session_id": req.session_id
        }

    # ---- NORMAL FINANCE Q&A ----
    context = build_context(req.session_id)

    answer = llm.generate(
        prompt=f"{context}\n\nUser: {req.message}",
        system_prompt=llm_engine.SYSTEM_PROMPT
    )

    add_message(req.session_id, "assistant", answer)

    return {"response": answer, "session_id": req.session_id}
