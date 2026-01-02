# services/llm_answer_engine.py
# Central LLM reasoning layer (stable)

from llm.client import GroqLLMClient


class LLMAnswerEngine:
    """
    Generates answers using LLM with injected factual context.
    """

    SYSTEM_PROMPT = """
You are a finance assistant for Loara Finance.

Rules:
- Answer ONLY using provided data
- Do NOT hallucinate
- Be professional and concise
- If data is missing, say you do not have it
"""

    def __init__(self):
        self.llm = GroqLLMClient()

    # ---------- NORMAL FINANCE Q&A ----------
    def answer(self, question: str, knowledge_context: str) -> str:
        prompt = f"""
KNOWLEDGE:
{knowledge_context}

QUESTION:
{question}

ANSWER:
"""
        return self.llm.generate(
            prompt=prompt,
            system_prompt=self.SYSTEM_PROMPT
        )

    # ---------- EMI EXPLANATION ----------
    def explain_emi(self, emi_data: dict) -> str:
        prompt = f"""
Loan Type: {emi_data['loan_type']}
Principal: {emi_data['principal']}
Interest Rate: {emi_data['interest_rate']}%
Tenure: {emi_data['tenure_years']} years
Monthly EMI: {emi_data['emi']}

Explain the EMI calculation in simple terms.
"""
        return self.llm.generate(
            prompt=prompt,
            system_prompt=self.SYSTEM_PROMPT
        )
