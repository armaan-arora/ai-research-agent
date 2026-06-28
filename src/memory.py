from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv


load_dotenv()

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

vectorstore  = Chroma(
    collection_name= "research_memory",
    embedding_function=embeddings,
    persist_directory="./chroma_db"
)

def store_results(query, results):
    docs = []
    docs = [
        Document(
            page_content=result,
            metadata={"query": query}
        )
        for result in results
    ]
    vectorstore.add_documents(docs)
    print(f"\nRAG: Stored {len(docs)} results for: {query}")


def retrieve_results(query, k=5):
    results = vectorstore.similarity_search(query, k=k)
    if results:
        print(f"\nRAG: Found {len(results)} cached results for: {query}")
        return [r.page_content for r in results]
    return []

def has_results(query, threshold=0.85):
    results = vectorstore.similarity_search_with_score(query, k=1) #returns tuple (document,score)
    if results:
        doc, score = results[0]
        # chromadb returns distance — lower is better
        # threshold 0.85 means very similar
        if score < threshold:
            print(f"\nRAG cache hit for: {query} (score: {score:.2f})")
            return True
    return False
