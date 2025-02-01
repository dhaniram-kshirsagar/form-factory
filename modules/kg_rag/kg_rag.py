'''from langchain_neo4j import GraphCypherQAChain, Neo4jGraph
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.memory import ConversationBufferWindowMemory

from modules.kg_rag.cypher_prompt_template import CYPHER_RECOMMENDATION_PROMPT
from modules.kg_rag.qa_prompt_template import QA_PROMPT
import streamlit as st

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
st.session_state['memory'] =  None

async def init_graph( ):
    global graph, chain
    # st.session_state['memory'] =  ConversationBufferWindowMemory(
    #         input_key="question",
    #         output_key="result",
    #         memory_key="chat_history",
    #     )
    if graph is None:
        graph = Neo4jGraph(url=URI, username=USERNAME, password=NEO4J_PASSWORD, enhanced_schema=True)
        chain = GraphCypherQAChain.from_llm(
            ChatOpenAI(temperature=0), graph=graph, verbose=True, return_intermediate_steps=True,
            cypher_prompt=CYPHER_RECOMMENDATION_PROMPT,
            qa_prompt=QA_PROMPT,
            allow_dangerous_requests=True,
            #memory=st.session_state['memory']
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
        inputs = {"query": question, "chat_history": st.session_state['memory']}
        print(inputs)
        #result = chain.invoke({"query": question})
        result = chain.invoke(inputs)
        st.session_state['memory'] = [{"last_query": question}, {"last_response": result["result"]}]
    except Exception as e:
        print(e)
        result['result'] = 'I do not understand this type of queries'
    finally:
        return result

def yeild_kg_answer(question):
    yield chain.invoke({"query": question})'''

import os
import threading
from uuid import uuid4
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_neo4j import (
    Neo4jGraph,
    Neo4jChatMessageHistory,
    GraphCypherQAChain
)

# from cypher_prompt_template import CYPHER_RECOMMENDATION_PROMPT
# from qa_prompt_template import QA_PROMPT

from modules.kg_rag.cypher_prompt_template import CYPHER_RECOMMENDATION_PROMPT
from modules.kg_rag.qa_prompt_template import QA_PROMPT

# Load environment variables
load_dotenv()

assistant = None

class Neo4jGraphChatAssistant:
    def __init__(self, session_id: str):
        # Initialize Neo4j Graph connection
        self.graph = Neo4jGraph(
            url=os.getenv("NEO4J_URI"),
            username=os.getenv("NEO4J_USERNAME"),
            password=os.getenv("NEO4J_PASSWORD"),
            database="neo4j",
            enhanced_schema=True
        )
        
        # Initialize Neo4j-backed chat history
        self.history = Neo4jChatMessageHistory(
            session_id=session_id,
            url=os.getenv("NEO4J_URI"),  
            username=os.getenv("NEO4J_USERNAME"),
            password=os.getenv("NEO4J_PASSWORD")
        )
        
        # Configure domain-specific prompts
        self.cypher_prompt = CYPHER_RECOMMENDATION_PROMPT
        
        self.qa_prompt = QA_PROMPT

        # Initialize QA chain with Neo4j optimizations
        self.chain = GraphCypherQAChain.from_llm(
            llm=ChatOpenAI(temperature=0.2),
            graph=self.graph,
            cypher_prompt=self.cypher_prompt,
            qa_prompt=self.qa_prompt,
            verbose=True,
            allow_dangerous_requests=True,
            return_intermediate_steps=True,
        )

    def _format_history(self) -> str:
        """Format last 3 exchanges for context"""
        return "\n".join(
            f"{msg.content}" 
            for msg in self.history.messages[-5:] if msg.type == "ai" # 3 pairs of Q/A
        )

    def query(self, question: str) -> str:
        try:
            # Execute chain with context
            hist = self._format_history()
            print("HISTORY TO BE USED:" +str(hist))
            result = self.chain.invoke({
                "query": question,
                "history": hist,
            })
            
            # Persist conversation
            print("Persisting conversation... : "+ str(result))
            self.history.add_user_message(question)
            self.history.add_ai_message(result["result"])
            
            return result
        
        except Exception as e:
            print(f"Research error: {str(e)}")
            return {"result": "I do not understand this type of queries"}

import inspect
lock = threading.Lock()

async def init_graph( ):
    global assistant
    global count
    caller = inspect.getouterframes(inspect.currentframe())[1][3]
    print("Inside : " + str(caller))
    print("Acquiring lock")
    if assistant is None:
        with lock:
            if assistant is None:     
                print("Initializing Neo4j Graph Chat ASSISTANT...")  
                session_id = f"factory_session_{uuid4()}"
                assistant = Neo4jGraphChatAssistant(session_id)
            print("Releasing lock")

from neo4j.exceptions import CypherSyntaxError
import streamlit as st

def get_kg_answer(question):
    global assistant

    result = {}
    if assistant is None:
        init_graph()
        if assistant is None:
            result['result'] = 'I am still initializing. Please try again later'
            return result

    try:
        result = assistant.query(question)
        print("RESULT: "+str(result))
    except Exception as e:
        print(e)
        result['result'] = 'I do not understand this type of queries'
    finally:
        return result
    
# Example Usage
if __name__ == "__main__":
    # Initialize with session ID
    session_id = f"pharma_session_{uuid4()}"
    assistant = Neo4jGraphChatAssistant(session_id)
    
    # Research conversation
    queries = [
        "What is the factory 1 location?",
        "What is the production volume for factory",
        "What is the profit margin for factory?",
        "What are the machines in factory?",
    ]
    
    for query in queries:
        print(f"\nResearcher: {query}")
        response = assistant.query(query)
        print(f"Assistant: {response}")
    
    # Verify Neo4j storage
    print("\nNeo4j Conversation Records:")
    for msg in assistant.history.messages:
        print(f"[{msg.type.upper()}]: {msg.content[:75]}...")

# requirements.txt
# langchain_neo4j>=0.1.2
# langchain_openai>=0.1.7
# python-dotenv>=1.0.0
# neo4j>=5.20.0

# .env
# NEO4J_URI=bolt://localhost:7687
# NEO4J_USERNAME=neo4j
# NEO4J_PASSWORD=your_password
# OPENAI_API_KEY=your_openai_key