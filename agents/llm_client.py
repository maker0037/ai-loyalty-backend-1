import os
from groq import Groq

from dotenv import load_dotenv

load_dotenv()


def get_groq_client():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError("GROQ_API_KEY not found in environment")

    return Groq(api_key=api_key)

def get_groq_model():
    return os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")
