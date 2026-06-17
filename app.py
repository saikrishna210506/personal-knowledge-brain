from utils.vector_store import search_chunks
from utils.rag_engine import generate_answer

query = input("Ask a question: ")

results = search_chunks(query)

context = results["documents"][0][0]

answer = generate_answer(query, context)

print("\nAnswer:\n")
print(answer)