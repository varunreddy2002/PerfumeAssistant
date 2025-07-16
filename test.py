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

notes = ['vanilla', 'musk', 'citrus']
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
    for record in result:
        print(record)