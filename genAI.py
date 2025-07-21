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
# try:
#     os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "intern-api-use.json"
# except:
#     print("Key Not Found")
client = genai.Client(
    api_key=api_k
)


def llm(prompt, past_perfume):
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents= f"""
        You are a fragrance expert. A user says: '{prompt}'.  Their prior perfume recommendations were '{past_perfume}'.
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

def perfume_description(prompt, t_notes,m_notes,b_notes):
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents= f"""
        Write a verbose description of the perfume {prompt}, considering that it has the top notes {t_notes},
        the middle notes {m_notes}, and the base notes {b_notes}.  Write at least 3 sentences and at most 5.
        """
        ,
    )
    return response.text