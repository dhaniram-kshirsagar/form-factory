from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import TextLoader

class RevenueRAG:
    def __init__(self, knowledge_base_path):
        self.knowledge_base_path = knowledge_base_path
        self.embeddings = OpenAIEmbeddings()
        self.vectorstore = self._initialize_vectorstore()
        
    def _initialize_vectorstore(self):
        """Initialize or load the vector store"""
        try:
            return FAISS.load_local(self.knowledge_base_path, self.embeddings)
        except:
            return FAISS.from_texts([""], self.embeddings)
    
    def add_knowledge(self, text):
        """Add new knowledge to the RAG system"""
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        docs = text_splitter.split_documents(text)
        self.vectorstore.add_documents(docs)
        self.vectorstore.save_local(self.knowledge_base_path)
    
    def query(self, question):
        """Query the RAG system with a question"""
        qa_chain = RetrievalQA.from_chain_type(
            llm=ChatOpenAI(model="gpt-4", temperature=0),
            chain_type="stuff",
            retriever=self.vectorstore.as_retriever(),
            return_source_documents=True
        )
        return qa_chain({"query": question})

def create_revenue_rag_layer(knowledge_base_path="revenue_knowledge"):
    """Create and return a RevenueRAG instance"""
    return RevenueRAG(knowledge_base_path)
