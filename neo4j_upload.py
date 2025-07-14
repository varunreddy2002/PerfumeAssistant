from neo4j import GraphDatabase
import pandas as pd
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

URI = os.getenv("NEO4J_URI")
AUTH = (os.getenv("NEO4J_USER"), os.getenv("NEO4J_PASSWORD"))

def split_notes(notes):
    if pd.isna(notes):
        return []
    return [note.strip() for note in str(notes).split(',')]

# Load and clean data
df = pd.read_csv("perfume_list.csv")
df['Top'] = df['Top'].apply(split_notes)
df['Middle'] = df['Middle'].apply(split_notes)
df['Base'] = df['Base'].apply(split_notes)

print(df.head())

# Neo4j operations
with GraphDatabase.driver(URI, auth=AUTH) as driver:
    driver.verify_connectivity()

    def create_perfume_and_notes(tx, row):
        # Create perfume node
        tx.run("""
            MERGE (p:Perfume {name: $name})
            SET p.brand = $brand,
                p.country = $country,
                p.gender = $gender,
                p.rating = toFloat($rating),
                p.year = $year
        """, 
        name=row['Perfume'],
        brand=row['Brand'],
        country=row['Country'],
        gender=row['Gender'],
        rating=row['Rating Value'],
        year=row['Year'])

        # Create and link top notes
        for note in row['Top']:
            tx.run("""
                MERGE (n:Note {name: $note})
                WITH n
                MATCH (p:Perfume {name: $perfume})
                MERGE (p)-[:HAS_TOP_NOTE]->(n)
            """, note=note, perfume=row['Perfume'])

        # Create and link middle notes
        for note in row['Middle']:
            tx.run("""
                MERGE (n:Note {name: $note})
                WITH n
                MATCH (p:Perfume {name: $perfume})
                MERGE (p)-[:HAS_MIDDLE_NOTE]->(n)
            """, note=note, perfume=row['Perfume'])

        # Create and link base notes
        for note in row['Base']:
            tx.run("""
                MERGE (n:Note {name: $note})
                WITH n
                MATCH (p:Perfume {name: $perfume})
                MERGE (p)-[:HAS_BASE_NOTE]->(n)
            """, note=note, perfume=row['Perfume'])

    # Run transactions
    with driver.session() as session:
        for _, row in df.iterrows():
            session.write_transaction(create_perfume_and_notes, row)
