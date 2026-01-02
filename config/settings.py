# config/settings.py
import os
from dotenv import load_dotenv

load_dotenv()

APP_NAME = "Loara Finance GenAI Service"

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL is missing. Check your .env file")
