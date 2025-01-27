import os
from neo4j import GraphDatabase


URI = os.getenv("NEO4J_URI")
DB = os.getenv("NEO4J_DB")
AUTH = (os.getenv("NEO4J_USERNAME"), os.getenv("NEO4J_PASSWORD"))

driver = GraphDatabase.driver(URI, auth=AUTH)
driver.verify_connectivity()
print("Connection established.")

def execute_query(query):
    result = driver.execute_query(query, database_ = DB)
    print(result)
    return result

def close():
    driver.close()

