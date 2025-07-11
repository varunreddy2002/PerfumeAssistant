from neo4j import GraphDatabase
import pandas as pd
# URI examples: "neo4j://localhost", "neo4j+s://xxx.databases.neo4j.io"
URI = "neo4j+s://6765e61f.databases.neo4j.io"
AUTH = ("neo4j", "vyZbWGJXjnfbwkAXI6C-UvnSgHZQ9QYqhwesnMajhhM")

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
