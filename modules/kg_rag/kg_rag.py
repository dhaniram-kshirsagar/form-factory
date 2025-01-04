from langchain_neo4j import GraphCypherQAChain, Neo4jGraph
from langchain_openai import ChatOpenAI

from modules.kg_rag.cypher_prompt_template import CYPHER_RECOMMENDATION_PROMPT
from modules.kg_rag.qa_prompt_template import QA_PROMPT

graph = Neo4jGraph(url="bolt://172.104.129.10:7687", username="neo4j", password="", enhanced_schema=True)

import getpass
import os

if "OPENAI_API_KEY" not in os.environ:
    os.environ["OPENAI_API_KEY"] = ""

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