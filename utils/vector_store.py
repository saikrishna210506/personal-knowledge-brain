import chromadb
from sentence_transformers import SentenceTransformer

client = chromadb.PersistentClient(path="./vector_db")

collection = client.get_or_create_collection(
    name="knowledge_base"
)

model = SentenceTransformer("all-MiniLM-L6-v2")


import uuid

def store_chunks(chunks):

    for chunk in chunks:

        embedding = model.encode(chunk).tolist()

        unique_id = str(uuid.uuid4())

        collection.add(
    documents=[chunk],
    embeddings=[embedding],
    ids=[unique_id]
)

    print("Chunks stored successfully!")


def search_chunks(query):

    query_embedding = model.encode(query).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=10,
        include=["documents"]
    )

    print("\nSEARCH RESULTS:")
    for doc in results["documents"][0]:
        print("\n----------------")
        print(doc[:300])

    print("\nRETRIEVED CHUNKS:")
    for i, doc in enumerate(results["documents"][0]):
        print(f"\n--- Retrieved {i+1} ---")
        print(doc[:500])

    return results
def clear_collection():

    print("Before clear:", collection.count())

    ids = collection.get()["ids"]

    if ids:
        collection.delete(ids=ids)

    print("After clear:", collection.count())
    print("Collection cleared!")