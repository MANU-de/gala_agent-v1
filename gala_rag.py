import json
from langchain_community.document_loaders import TextLoader, JSONLoader
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
import os

load_dotenv() # Load environment variables from .env file

class GalaRAG:
    def __init__(self, gemini_api_key):
        self.gemini_api_key = gemini_api_key
        self.vectorstore = None
        self.embeddings = GoogleGenerativeAIEmbeddings(
            google_api_key=self.gemini_api_key,
            model="models/embedding-001"
        )
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
            is_separator_regex=False,
        )

    def _load_documents(self):
        # Load menu and schedule from markdown
        menu_loader = TextLoader("data/menu.md")
        schedule_loader = TextLoader("data/schedule.md")
        
        # Load guests from JSON. We need a custom way to handle JSON loading for specific fields.
        def metadata_func(record: dict, metadata: dict) -> dict:
            metadata["name"] = record.get("name")
            metadata["interests"] = record.get("interests")
            metadata["background"] = record.get("background")
            metadata["gossip"] = record.get("gossip")
            metadata["fun_fact"] = record.get("fun_fact")
            return metadata

        guest_loader = JSONLoader(
            file_path="data/guests.json",
            jq_schema='.', # Load the entire JSON as one document initially
            content_key='', # No specific content key, we'll process it
            text_content=False, # We'll create custom text content
            metadata_func=metadata_func
        )
        
        docs = []
        # Process guests specifically to create meaningful documents for RAG
        with open("data/guests.json", "r") as f:
            guests_data = json.load(f)
            for guest in guests_data:
                content = (
                    f"Guest Name: {guest['name']}\n"
                    f"Interests: {', '.join(guest['interests'])}\n"
                    f"Background: {guest['background']}\n"
                    f"Gossip: {guest['gossip']}\n"
                    f"Fun Fact: {guest['fun_fact']}"
                )
                docs.append({"page_content": content, "metadata": {"source": "guests.json", "name": guest['name']}})
        
        # Add menu and schedule documents
        docs.extend(menu_loader.load())
        docs.extend(schedule_loader.load())
        
        return docs

    def initialize_vectorstore(self):
        print("Loading documents and initializing vector store...")
        raw_docs = self._load_documents()
        
        # Since _load_documents now returns a list of dicts or actual Document objects,
        # we need to ensure it's in a format compatible with `from_documents`.
        # If raw_docs contains dictionaries, convert them to Document objects
        from langchain_core.documents import Document
        processed_docs = []
        for doc in raw_docs:
            if isinstance(doc, dict):
                processed_docs.append(Document(page_content=doc['page_content'], metadata=doc.get('metadata', {})))
            else:
                processed_docs.append(doc)

        split_docs = self.text_splitter.split_documents(processed_docs)
        self.vectorstore = FAISS.from_documents(split_docs, self.embeddings)
        print("Vector store initialized successfully.")

    def retrieve_info(self, query, k=3):
        if not self.vectorstore:
            raise ValueError("Vector store not initialized. Call initialize_vectorstore() first.")
        
        results = self.vectorstore.similarity_search(query, k=k)
        return "\n---\n".join([doc.page_content for doc in results])

if __name__ == "__main__":
    # Ensure you have your Gemini API key set as an environment variable (e.g., in a .env file)
    # GEMINI_API_KEY="your_gemini_api_key"
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    if not gemini_api_key:
        raise ValueError("GEMINI_API_KEY environment variable not set.")

    gala_rag = GalaRAG(gemini_api_key=gemini_api_key)
    gala_rag.initialize_vectorstore()

    # Test retrieval
    print("\n--- Testing Retrieval for 'Dr. Eleanor Vance interests' ---")
    print(gala_rag.retrieve_info("What are Dr. Eleanor Vance's interests?"))

    print("\n--- Testing Retrieval for 'What's for dessert?' ---")
    print(gala_rag.retrieve_info("What's for dessert at the gala?"))

    print("\n--- Testing Retrieval for 'schedule of fireworks' ---")
    print(gala_rag.retrieve_info("What time are the fireworks scheduled?"))