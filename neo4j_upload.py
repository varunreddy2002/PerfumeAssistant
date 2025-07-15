#!/usr/bin/env python3
"""
neo4j_upload.py

Iteratively load your semicolon‑delimited CSV into Neo4j,
creating separate Brand and Country nodes (1-to-many relation)
and linking Top/Middle/Base notes.

1) pip install neo4j pandas python-dotenv
2) Place this script and 'perfume_list.csv' in the same folder.
3) Create a .env file with NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD.
4) Run:
     python neo4j_upload.py
"""

import os
import csv
from dotenv import load_dotenv
from neo4j import GraphDatabase

# ─── Load env vars ─────────────────────────────────────────────────────────────
load_dotenv()
URI  = os.getenv("NEO4J_URI")
USER = os.getenv("NEO4J_USER")
PWD  = os.getenv("NEO4J_PASSWORD")
CSV_FILE = "perfume_list.csv"
# ────────────────────────────────────────────────────────────────────────────────

def split_notes(notes):
    if not notes:
        return []
    return [n.strip() for n in notes.split(',') if n.strip()]

def create_perfume_and_notes(tx, row):
    # 1) Merge Perfume node (now without brand/country props)
    tx.run("""
        MERGE (p:Perfume {name: $perfume})
        ON CREATE SET
            p.gender = $gender,
            p.rating = toFloat($rating),
            p.year   = toInteger($year)
        """,
        perfume=row['Perfume'],
        gender=row['Gender'],
        rating=row['Rating Value'],
        year=row['Year']
    )

    # 2) Merge Brand node and link
    tx.run("""
        MERGE (b:Brand {name: $brand})
        WITH b
        MATCH (p:Perfume {name: $perfume})
        MERGE (p)-[:MADE_BY]->(b)
        """,
        brand=row['Brand'],
        perfume=row['Perfume']
    )

    # 3) Merge Country node and link
    tx.run("""
        MERGE (c:Country {name: $country})
        WITH c
        MATCH (p:Perfume {name: $perfume})
        MERGE (p)-[:ORIGIN]->(c)
        """,
        country=row['Country'],
        perfume=row['Perfume']
    )

    # 4) Top/Middle/Base notes
    for rel, col in [("HAS_TOP_NOTE", "Top"),
                     ("HAS_MIDDLE_NOTE", "Middle"),
                     ("HAS_BASE_NOTE", "Base")]:
        for note in row[col]:
            tx.run(f"""
                MERGE (n:Note {{name: $note}})
                  ON CREATE SET n.type = $type
                WITH n
                MATCH (p:Perfume {{name: $perfume}})
                MERGE (p)-[:{rel}]->(n)
                """,
                note=note,
                type=col.lower(),
                perfume=row['Perfume']
            )

def main():
    # Connect & verify
    driver = GraphDatabase.driver(URI, auth=(USER, PWD))
    driver.verify_connectivity()

    # Read CSV and split lists
    with open(CSV_FILE, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        data = []
        for row in reader:
            row['Top']    = split_notes(row.get('Top', ''))
            row['Middle'] = split_notes(row.get('Middle', ''))
            row['Base']   = split_notes(row.get('Base', ''))
            data.append(row)

    # Run import transactions
    with driver.session() as session:
        for row in data:
            session.write_transaction(create_perfume_and_notes, row)

    driver.close()
    print("✅ Import complete with separate Brand & Country nodes.")

if __name__ == "__main__":
    main()

