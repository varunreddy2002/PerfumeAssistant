import os
import json
import re
from dotenv import load_dotenv
from neo4j import GraphDatabase
from genAI import llm
from notes_embed import load_embeddings, find_closest_note

load_dotenv()
URI = os.getenv("NEO4J_URI")
USER = os.getenv("NEO4J_USER")
PWD = os.getenv("NEO4J_PASSWORD")

# Load note embeddings
note_embeddings = load_embeddings()

# Collect user input
current_query = input("Describe your ideal scent: ")
res = llm(current_query)
match = re.search(r'\{[\s\S]*?\}', res)
if match:
    json_str = match.group(0)
    parsed = json.loads(json_str)
    mood= parsed["mood"]
    occasion=parsed["occasion"]
    notes=parsed["notes"]
else:
    print("❌ No JSON object found.")

print(notes)


# Map LLM notes to known dataset notes
mapped_notes = [find_closest_note(note, note_embeddings) for note in notes]
print("Mapped Notes:", mapped_notes)

# Query Neo4j based on mapped notes
query = f"""
MATCH (p:Perfume)-[:HAS_TOP_NOTE|HAS_MIDDLE_NOTE|HAS_BASE_NOTE]->(n:Note)
WHERE toLower(n.name) IN {mapped_notes}
RETURN p.name AS perfume, COUNT(*) AS score, p.rating AS rating
ORDER BY score DESC, p.rating DESC
LIMIT 3
"""

# Connect to Neo4j
driver = GraphDatabase.driver(URI, auth=(USER, PWD))
driver.verify_connectivity()
with driver.session() as session:
    result = session.run(query)
    for record in result:
        print(f"Perfume: {record['perfume']} | Match Score: {record['score']} | Rating: {record['rating']}")
