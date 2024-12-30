from langchain_neo4j import GraphCypherQAChain, Neo4jGraph
from langchain_openai import ChatOpenAI

graph = Neo4jGraph(url="bolt://172.104.129.10:7687", username="neo4j", password="")

import getpass
import os

if "OPENAI_API_KEY" not in os.environ:
    os.environ["OPENAI_API_KEY"] = ""

chain = GraphCypherQAChain.from_llm(
    llm=ChatOpenAI(temperature=0, model="gpt-4"),#"gpt-3.5-turbo"),
    graph=graph,
    verbose=True,
    validate_cypher=True,
    return_direct=True,
    use_function_response=True,
    function_response_system="""You are an expert of neo4j cypher queries as well as 
        the foam factories performance and maintenance data. 
        Assume that all questions are related 
        to the foam factories performance and maintenance and/or neo4j cypher queries. Keep 
        your answers technical and based on 
        facts – do not hallucinate features.""",
    allow_dangerous_requests=True
)

def get_kg_answer(question):
    return chain.invoke({"query": question})

#"which factory is highest profit margin?"