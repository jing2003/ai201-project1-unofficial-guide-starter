from pathlib import Path
import os

import chromadb
from dotenv import load_dotenv
from groq import Groq
from sentence_transformers import SentenceTransformer


load_dotenv()

CHROMA_DIR = Path("data/chroma_db")
COLLECTION_NAME = "uhm_cs_professor_reviews"
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"
LLM_MODEL = "llama-3.3-70b-versatile"

TOP_K = 5
MAX_BEST_DISTANCE = 0.85


embedding_model = SentenceTransformer(EMBEDDING_MODEL_NAME)

groq_api_key = os.getenv("GROQ_API_KEY")

if not groq_api_key:
    raise ValueError("Missing GROQ_API_KEY. Add it to your .env file.")

groq_client = Groq(api_key=groq_api_key)


def get_collection():
    """
    Load the existing ChromaDB collection created in Milestone 4.
    """
    client = chromadb.PersistentClient(path=str(CHROMA_DIR))

    try:
        collection = client.get_collection(name=COLLECTION_NAME)
    except Exception as error:
        raise RuntimeError(
            "Could not load ChromaDB collection. "
            "Run scripts/build_vector_store.py before using query.py."
        ) from error

    return collection


def retrieve(query, top_k=TOP_K):
    """
    Retrieve top-k relevant chunks from ChromaDB.
    """
    collection = get_collection()

    query_embedding = embedding_model.encode([query]).tolist()

    results = collection.query(
        query_embeddings=query_embedding,
        n_results=top_k,
        include=["documents", "metadatas", "distances"],
    )

    retrieved_chunks = []

    for i in range(len(results["ids"][0])):
        retrieved_chunks.append({
            "id": results["ids"][0][i],
            "text": results["documents"][0][i],
            "metadata": results["metadatas"][0][i],
            "distance": results["distances"][0][i],
        })

    return retrieved_chunks


def format_context(retrieved_chunks):
    """
    Format retrieved chunks into a clear context block for the LLM.
    Each chunk gets a source number.
    """
    context_parts = []

    for i, chunk in enumerate(retrieved_chunks, start=1):
        metadata = chunk["metadata"]

        professor = metadata.get("professor", "Unknown professor")
        source_type = metadata.get("source_type", "Unknown source type")
        source = metadata.get("source", "Unknown source")
        distance = chunk["distance"]

        context_parts.append(
            f"[Source {i}]\n"
            f"Professor: {professor}\n"
            f"Source type: {source_type}\n"
            f"Source file: {source}\n"
            f"Distance: {distance:.4f}\n"
            f"Content:\n{chunk['text']}"
        )

    return "\n\n---\n\n".join(context_parts)


def build_sources(retrieved_chunks):
    """
    Build source attribution programmatically.
    This guarantees sources are shown even if the LLM forgets to cite them.
    """
    sources = []

    for i, chunk in enumerate(retrieved_chunks, start=1):
        metadata = chunk["metadata"]

        source = metadata.get("source", "Unknown source")
        professor = metadata.get("professor", "Unknown professor")
        source_type = metadata.get("source_type", "Unknown source type")
        distance = chunk["distance"]

        sources.append(
            f"[Source {i}] {source} | Professor: {professor} | "
            f"Type: {source_type} | Distance: {distance:.4f}"
        )

    return sources


def generate_response(question, retrieved_chunks):
    """
    Generate a grounded answer using Groq.
    The LLM must answer only from retrieved chunks.
    """
    if not retrieved_chunks:
        return "I don't have enough information in the provided documents to answer that."

    best_distance = retrieved_chunks[0]["distance"]

    if best_distance > MAX_BEST_DISTANCE:
        return (
            "I don't have enough information in the provided documents to answer that. "
            "The retrieved chunks were not similar enough to the question."
        )

    context = format_context(retrieved_chunks)

    system_prompt = """
You are a grounded question-answering assistant for a RAG system.

Rules:
1. Answer using ONLY the provided context sources.
2. Do NOT use outside knowledge.
3. Do NOT guess or infer beyond what the sources say.
4. If the context does not contain enough information, say:
   "I don't have enough information in the provided documents to answer that."
5. When you use information from a source, cite it using the source label, such as [Source 1].
6. If the question asks about official information such as research interests, title, office, email, or education, use sources with Source type: official_faculty.
7. If the question asks about student reviews, only use sources with Source type: student_review.
8. If a professor appears in the official faculty source but has no student review source, say that student review information is not available in the provided documents.
"""

    user_prompt = f"""
Question:
{question}

Retrieved context:
{context}

Write a clear answer grounded only in the retrieved context.
"""

    response = groq_client.chat.completions.create(
        model=LLM_MODEL,
        messages=[
            {"role": "system", "content": system_prompt.strip()},
            {"role": "user", "content": user_prompt.strip()},
        ],
        temperature=0.1,
        max_tokens=600,
    )

    return response.choices[0].message.content.strip()


def ask(question):
    """
    End-to-end RAG function:
    question -> retrieval -> generation -> answer + sources.
    """
    retrieved_chunks = retrieve(question, top_k=TOP_K)
    answer = generate_response(question, retrieved_chunks)
    sources = build_sources(retrieved_chunks)

    return {
        "answer": answer,
        "sources": sources,
        "retrieved_chunks": retrieved_chunks,
    }


if __name__ == "__main__":
    test_questions = [
        "What do students say about Peter Sadowski's teaching style?",
        "According to student reviews, what is the workload like in Carleton Moore's class?",
        "Do students say Henri Casanova's course is more focused on exams, projects, homework, or quizzes?",
        "What are Jason Leigh's research interests, and what do students say about their classroom experience?",
        "What do students say about Haopeng Zhang's teaching style and workload?",
    ]

    for question in test_questions:
        result = ask(question)

        print("\n" + "=" * 80)
        print(f"QUESTION: {question}")
        print("=" * 80)
        print("\nANSWER:")
        print(result["answer"])

        print("\nSOURCES:")
        for source in result["sources"]:
            print(f"- {source}")
