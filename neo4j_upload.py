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

df = pd.read_csv("perfume_list.csv")
df['Top'] = df['Top'].apply(split_notes)
df['Middle'] = df['Middle'].apply(split_notes)
df['Base'] = df['Base'].apply(split_notes)

print(df.head())

with GraphDatabase.driver(URI, auth=AUTH) as driver:
    driver.verify_connectivity()
