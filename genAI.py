from google import genai
import json
import re
from dotenv import load_dotenv
from neo4j import GraphDatabase
import os
from input_collector import collect_user_input, json_append

load_dotenv()
URI  = os.getenv("NEO4J_URI")
USER = os.getenv("NEO4J_USER")
PWD  = os.getenv("NEO4J_PASSWORD")
api_k = os.getenv("API_KEY")
# api_k = "AIzaSyC7wKywRl94y89kMWkBvnWM6_Mth9AYgjU"
client = genai.Client(
    api_key=api_k
)


def llm(prompt, past_prompt):
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents= f"""
        You are a fragrance expert. A user says: '{prompt}'.  The user's past prompts are '{past_prompt}'.
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

with open('user_input.json', 'r') as file:
    data = json.load(file)

target_user = "tester" #change to user_var when making into method
matching_entries = [entry for entry in data if entry.get("user") == target_user]

current_query = collect_user_input()

json_append(current_query)

query = ""
output=llm(current_query, matching_entries)
print(output)
match = re.search(r'\{[\s\S]*?\}', output)
if match:
    json_str = match.group(0)
    parsed = json.loads(json_str)
    mood= parsed["mood"]
    occasion=parsed["occasion"]
    notes=parsed["notes"]
else:
    print("❌ No JSON object found.")

print(notes)

query = f"""
MATCH (p:Perfume)-[:HAS_TOP_NOTE|HAS_MIDDLE_NOTE|HAS_BASE_NOTE]->(n:Note)
WHERE toLower(n.name) IN {notes}
RETURN p.name, COUNT(*) AS score
ORDER BY score DESC, p.rating DESC
LIMIT 3
"""
driver = GraphDatabase.driver(URI, auth=(USER, PWD))
driver.verify_connectivity()
with driver.session() as session:
    result = session.run(query)
    for record in result:
        print(record)