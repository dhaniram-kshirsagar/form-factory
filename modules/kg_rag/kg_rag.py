from langchain_neo4j import GraphCypherQAChain, Neo4jGraph
from langchain_openai import ChatOpenAI

from modules.kg_rag.cypher_prompt_template import CYPHER_RECOMMENDATION_PROMPT
from modules.kg_rag.qa_prompt_template import QA_PROMPT

import os
from dotenv import load_dotenv
import asyncio
import logging

logging.basicConfig(level=logging.INFO)

load_dotenv()

# Get the OpenAI API key
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

graph = None
chain = None

async def init_graph( ):
    global graph, chain

    if graph is None:
        graph = Neo4jGraph(url="bolt://172.104.129.10:7687", username="neo4j", password='neo4j', enhanced_schema=True)

        chain = GraphCypherQAChain.from_llm(
            ChatOpenAI(temperature=0), graph=graph, verbose=True,
            cypher_prompt=CYPHER_RECOMMENDATION_PROMPT,
            qa_prompt=QA_PROMPT,
            allow_dangerous_requests=True 
        )

def get_kg_answer(question):
    logging.info(f"User question: {question}")
    generated_query = chain.invoke({"query": question})
    logging.info(f"Generated Cypher query: {generated_query}")
    return generated_query

def yeild_kg_answer(question):
    yield chain.invoke({"query": question})