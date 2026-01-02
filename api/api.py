# api/api.py
from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy.orm import Session

from db.config import engine
from services.finance_service import is_emi_question, handle_emi_query
from services.llm_answer_engine import LLMAnswerEngine
from services.finance_knowledge import FinanceKnowledgeBuilder

app = FastAPI(title="Production-grade Finance Assistant API")

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

    # ---------- EMI FLOW ----------
    if is_emi_question(req.message):
        emi_data = handle_emi_query(req.message, session)

        if "error" in emi_data:
            return {"response": emi_data["error"], "session_id": req.session_id}

        explanation = llm_engine.explain_emi(emi_data)

        return {
            "response": explanation,
            "data": emi_data,
            "session_id": req.session_id
        }

    # ---------- NORMAL FINANCE Q&A ----------
    kb = FinanceKnowledgeBuilder(session)
    context = kb.build_full_context()

    answer = llm_engine.answer(req.message, context)

    return {
        "response": answer,
        "session_id": req.session_id
    }
