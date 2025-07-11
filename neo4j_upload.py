from neo4j import GraphDatabase

# URI examples: "neo4j://localhost", "neo4j+s://xxx.databases.neo4j.io"
URI = "neo4j+s://6765e61f.databases.neo4j.io"
AUTH = ("neo4j", "vyZbWGJXjnfbwkAXI6C-UvnSgHZQ9QYqhwesnMajhhM")

with GraphDatabase.driver(URI, auth=AUTH) as driver:
    driver.verify_connectivity()
