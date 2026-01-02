from llm.client import GroqLLMClient

llm = GroqLLMClient()

def handle_support_query(message: str) -> str:
    prompt = f"""
You are customer support for Loara Finance.
Handle complaints, guidance, escalation info.

User query:
{message}
"""
    return llm.generate(prompt)
