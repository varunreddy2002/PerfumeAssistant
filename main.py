import os
import json
import re
from dotenv import load_dotenv
from neo4j import GraphDatabase
from genAI import llm
from notes_embed import load_embeddings, find_closest_note
from input_collector import collect_user_input, json_append
import warnings
from requests.exceptions import RequestsDependencyWarning
warnings.filterwarnings("ignore", category=RequestsDependencyWarning)

# load_dotenv()
# URI = os.getenv("NEO4J_URI")
# USER = os.getenv("NEO4J_USER")
# PWD = os.getenv("NEO4J_PASSWORD")

# # Load note embeddings
# note_embeddings = load_embeddings()

# # Collect user input
# user_input = collect_user_input()
# current_query = user_input["prompt"]

# try:
#     with open('user_input.json', 'r') as file:
#         data = json.load(file)
#     if not data:
#         data = ''
# except:
#     data = ''

# target_user = user_input['username']
# matching_entries = [entry["Recommended_Perfumes"] for entry in data if entry.get("username") == target_user]

# res = llm(current_query, matching_entries)
# match = re.search(r'\{[\s\S]*?\}', res)
# if match:
#     json_str = match.group(0)
#     parsed = json.loads(json_str)
#     mood= parsed["mood"]
#     occasion=parsed["occasion"]
#     notes=parsed["notes"]
# else:
#     print("❌ No JSON object found.")

# print(notes)


# # Map LLM notes to known dataset notes
# mapped_notes = [find_closest_note(note, note_embeddings) for note in notes]
# print("Mapped Notes:", mapped_notes)

# # Query Neo4j based on mapped notes
# query = f"""
# MATCH (p:Perfume)-[:HAS_TOP_NOTE|HAS_MIDDLE_NOTE|HAS_BASE_NOTE]->(n:Note)
# WHERE toLower(n.name) IN {mapped_notes}
# RETURN p.name AS perfume, COUNT(*) AS score, p.rating AS rating
# ORDER BY score DESC, p.rating DESC
# LIMIT 3
# """

# # Connect to Neo4j
# driver = GraphDatabase.driver(URI, auth=(USER, PWD))
# driver.verify_connectivity()
# with driver.session() as session:
#     result = session.run(query)
#     perfumes = []
#     for record in result:
#         print(f"Perfume: {record['perfume']} | Match Score: {record['score']} | Rating: {record['rating']}")
#         perfumes.append(record['perfume'])
# user_input["Recommended_Perfumes"] = perfumes
# json_append(user_input)

def find_rec(user_input):      
    load_dotenv()
    URI = os.getenv("NEO4J_URI")
    USER = os.getenv("NEO4J_USER")
    PWD = os.getenv("NEO4J_PASSWORD")

    # Load note embeddings
    note_embeddings = load_embeddings()

    # Collect user input
    current_query = user_input["prompt"]

    try:
        with open('user_input.json', 'r') as file:
            data = json.load(file)
        if not data:
            data = ''
    except:
        data = ''

    target_user = user_input['username']
    matching_entries = [entry["Recommended_Perfumes"] for entry in data if entry.get("username") == target_user]

    res = llm(current_query, matching_entries)
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
    LIMIT 4
    """

    # Connect to Neo4j
    driver = GraphDatabase.driver(URI, auth=(USER, PWD))
    driver.verify_connectivity()
    with driver.session() as session:
        result = session.run(query)
        suggestions = [f"Analyzing: {current_query}"]
        perfumes = []
        s = ""
        for record in result:
            perfume_line = f"Suggestion: {record['perfume']} (Score: {record['score']}, Rating: {record['rating']})"
            suggestions.append(perfume_line)
            perfumes.append(record['perfume'])
    user_input["Recommended_Perfumes"] = perfumes
    json_append(user_input)
    return suggestions
