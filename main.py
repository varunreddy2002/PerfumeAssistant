import os
import json
import re
from dotenv import load_dotenv
from neo4j import GraphDatabase
from genAI import llm, perfume_description
from notes_embed import load_embeddings, find_closest_note
from input_collector import collect_user_input, json_append
from gen_images import generate_image, clear_folder
import warnings
from requests.exceptions import RequestsDependencyWarning
warnings.filterwarnings("ignore", category=RequestsDependencyWarning)

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
    return suggestions, perfumes

def find_notes(perfume_names):
    load_dotenv()
    URI = os.getenv("NEO4J_URI")
    USER = os.getenv("NEO4J_USER")
    PWD = os.getenv("NEO4J_PASSWORD")
    driver = GraphDatabase.driver(URI, auth=(USER, PWD))

    query = """
    MATCH (p:Perfume {name: $perfume_name})
    OPTIONAL MATCH (p)-[:HAS_TOP_NOTE]->(top:Note)
    OPTIONAL MATCH (p)-[:HAS_MIDDLE_NOTE]->(middle:Note)
    OPTIONAL MATCH (p)-[:HAS_BASE_NOTE]->(base:Note)
    RETURN 
      p.name AS perfume,
      collect(DISTINCT top.name) AS top_notes,
      collect(DISTINCT middle.name) AS middle_notes,
      collect(DISTINCT base.name) AS base_notes
    """

    results = {}
    with driver.session() as session:
        for name in perfume_names:
            result = session.run(query, perfume_name=name).single()
            results[result["perfume"]] = [result["top_notes"],result["middle_notes"],result["base_notes"]]
                # "name": result["perfume"],
                # "top_notes": result["top_notes"],
                # "middle_notes": result["middle_notes"],
                # "base_notes": result["base_notes"],
            
    driver.close()
    return results

def find_descriptions(perfumes):
    clear_folder()
    descriptions = {}
    for p in perfumes.keys():
        desc = perfume_description(p, perfumes[p])
        s = generate_image(f"Generate an image for the perfume {p} with a visual emphasis on the notes {perfumes[p]}.", p)
        # s = ""
        descriptions[p] = [desc if isinstance(desc, str) else "No description available.", s]
    return descriptions