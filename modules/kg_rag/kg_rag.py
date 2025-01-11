from langchain_neo4j import GraphCypherQAChain, Neo4jGraph
from langchain_openai import ChatOpenAI

from modules.kg_rag.cypher_prompt_template import CYPHER_RECOMMENDATION_PROMPT
from modules.kg_rag.qa_prompt_template import QA_PROMPT

import os

# Get the OpenAI API key
NEO4J_PASSWORD = os.getenv("NEO_4J_PASS")

graph = None
chain = None

def init_graph( ):
    global graph, chain

    if graph is None:
        graph = Neo4jGraph(url="bolt://172.104.129.10:7687", username="neo4j", password=NEO4J_PASSWORD, enhanced_schema=True)

        chain = GraphCypherQAChain.from_llm(
            ChatOpenAI(temperature=0), graph=graph, verbose=True,
            cypher_prompt=CYPHER_RECOMMENDATION_PROMPT,
            qa_prompt=QA_PROMPT,
            allow_dangerous_requests=True 
        )

def get_kg_answer(question):
    return chain.invoke({"query": question})

def yeild_kg_answer(question):
    yield chain.invoke({"query": question})