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
try:
    with open('user_input.json', 'r') as file:
        data = json.load(file)
    if not data:
        data = ''
except:
    data = ''
target_user = "tester" #change to user_var when making into method
matching_entries = [entry for entry in data if entry.get("username") == target_user]

current_query = collect_user_input()

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
RETURN p.name AS perfume, COUNT(*) AS score, p.rating AS rating
ORDER BY score DESC, p.rating DESC
LIMIT 3
"""
driver = GraphDatabase.driver(URI, auth=(USER, PWD))
driver.verify_connectivity()
with driver.session() as session:
    result = session.run(query)
    perfume_recs = []
    for record in result:
        print(record)
        perfume_recs.append(record)
current_query["Perfume-Recommendations"] = perfume_recs
json_append(current_query)