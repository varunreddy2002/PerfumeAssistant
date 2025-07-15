from google import genai
import json
import re
from dotenv import load_dotenv
from neo4j import GraphDatabase
import os

URI  = os.getenv("NEO4J_URI")
USER = os.getenv("NEO4J_USER")
PWD  = os.getenv("NEO4J_PASSWORD")

client = genai.Client(
    api_key=os.getenv("API_KEY")
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
output=llm("Tell me what you're in the mood for: ")
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
ORDER BY score DESC
LIMIT 5
"""
driver = GraphDatabase.driver(URI, auth=(USER, PWD))
driver.verify_connectivity()
with driver.session() as session:
    result = session.run(query)
    for record in result:
        print(record)