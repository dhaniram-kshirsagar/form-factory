from langchain_neo4j import GraphCypherQAChain, Neo4jGraph
from langchain_openai import ChatOpenAI

from modules.kg_rag.cypher_prompt_template import CYPHER_RECOMMENDATION_PROMPT
from modules.kg_rag.qa_prompt_template import QA_PROMPT

import os
from dotenv import load_dotenv
import asyncio

load_dotenv()

# Get the OpenAI API key
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")
URI = os.getenv("NEO4J_URI")
USERNAME = os.getenv("NEO4J_USERNAME")

graph = None
chain = None

async def init_graph( ):
    global graph, chain

    if graph is None:
        graph = Neo4jGraph(url=URI, username=USERNAME, password=NEO4J_PASSWORD, enhanced_schema=True)

        chain = GraphCypherQAChain.from_llm(
            ChatOpenAI(temperature=0), graph=graph, verbose=True, return_intermediate_steps=True,
            cypher_prompt=CYPHER_RECOMMENDATION_PROMPT,
            qa_prompt=QA_PROMPT,
            allow_dangerous_requests=True 
        )

import json
from neo4j.exceptions import CypherSyntaxError
def get_kg_answer(question):
    
    result = {}
    if chain is None:
        init_graph()
        if chain is None:
            result['result'] = 'I am still initializing. Please try again later'
            return result

    try:
        result = chain.invoke({"query": question})
    except CypherSyntaxError as e:
        result['result'] = 'I do not understand this type of queries'
    finally:
        return result

def yeild_kg_answer(question):
    yield chain.invoke({"query": question})