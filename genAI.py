from google import genai
import json
import re
from dotenv import load_dotenv
import os
load_dotenv()
URI  = os.getenv("NEO4J_URI")
USER = os.getenv("NEO4J_USER")
PWD  = os.getenv("NEO4J_PASSWORD")
api_k = os.getenv("API_KEY")
client = genai.Client(
    api_key=api_k
)


def llm(prompt):
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents= f"""
        You are a fragrance expert. A user says: '{prompt}'.
        Identify:
        - Mood
        - Occasion (if mentioned)
        - Suggested scent notes (top 3)
        Return the result as *only* valid JSON. Do NOT add explanation, notes, or introductions, I want just the JSON.
        Only return:
        {{
          "mood": "...",
          "occasion": "...",
          "notes": ["...", "...", "..."]
        }}
        """
        ,
    )
    return response.text