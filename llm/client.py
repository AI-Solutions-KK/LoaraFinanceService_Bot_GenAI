# llm/client.py
from groq import Groq
import os


class GroqLLMClient:
    def __init__(self):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        # Updated to a currently supported model
        self.model = "llama-3.1-8b-instant"  # ✅ Fast and efficient
        # Alternative options:
        # self.model = "llama-3.3-70b-versatile"  # More powerful
        # self.model = "mixtral-8x7b-32768"  # Larger context window

    def generate(self, prompt: str, system_prompt: str) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2
        )
        return response.choices[0].message.content.strip()