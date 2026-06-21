import chromadb
import ollama
import os

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

DB_PATH = os.path.join(
    BASE_DIR,
    "chroma_db_v2"
)

client = chromadb.PersistentClient(path=DB_PATH)

#client = chromadb.PersistentClient(path="./chroma_db_v2")

collection = client.get_collection("products")


def semantic_search(query):

    query_embedding = ollama.embeddings(
        model="nomic-embed-text",
        prompt=query
    )["embedding"]

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=3
    )

    return results["metadatas"][0]

