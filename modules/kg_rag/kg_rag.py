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
            llm=ChatOpenAI(model="gpt-4", temperature=0.2),
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
                print("Initializing Neo4j Graph Chat Asistent...")  
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