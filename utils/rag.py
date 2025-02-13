from langchain.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI


def create_rag_layer(model):
    """
    Create RAG layer for model explanations
    """
    docs = [
        "Churn prediction is based on customer behavior and contract details",
        "Important features include tenure, monthly charges, and contract type",
        "Higher monthly charges increase churn risk",
        "Longer tenure reduces churn probability",
        "Month-to-month contracts have higher churn risk"
    ]
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_texts(docs, embeddings)
    return RetrievalQA.from_chain_type(
        llm=ChatOpenAI(temperature=0),
        chain_type="stuff",
        retriever=vectorstore.as_retriever()
    )
