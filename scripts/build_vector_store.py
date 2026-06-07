from pathlib import Path
import json

import chromadb
from sentence_transformers import SentenceTransformer


CHUNKS_FILE = Path("data/processed/chunks.json")
CHROMA_DIR = Path("data/chroma_db")

COLLECTION_NAME = "uhm_cs_professor_reviews"
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"
TOP_K = 5


def load_chunks():
    """
    Load chunks created by Milestone 3.
    """
    if not CHUNKS_FILE.exists():
        raise FileNotFoundError(
            f"Could not find {CHUNKS_FILE}. Run scripts/build_chunks.py first."
        )

    with CHUNKS_FILE.open("r", encoding="utf-8") as f:
        chunks = json.load(f)

    if not chunks:
        raise ValueError("chunks.json is empty. Check your ingestion/chunking step.")

    return chunks


def clean_metadata(metadata):
    """
    ChromaDB metadata values should be simple types:
    string, int, float, or bool.

    This converts None values into empty strings.
    """
    cleaned = {}

    for key, value in metadata.items():
        if value is None:
            cleaned[key] = ""
        elif isinstance(value, (str, int, float, bool)):
            cleaned[key] = value
        else:
            cleaned[key] = str(value)

    return cleaned


def build_vector_store():
    """
    Embed all chunks and store them in ChromaDB.
    """
    chunks = load_chunks()

    print(f"Loaded {len(chunks)} chunks from {CHUNKS_FILE}")

    print(f"Loading embedding model: {EMBEDDING_MODEL_NAME}")
    model = SentenceTransformer(EMBEDDING_MODEL_NAME)

    texts = [chunk["text"] for chunk in chunks]
    ids = [chunk["id"] for chunk in chunks]

    metadatas = []

    for chunk in chunks:
        metadata = {
            "source": chunk.get("source", ""),
            "source_type": chunk.get("source_type", ""),
            "professor": chunk.get("professor", ""),
            "record_index": chunk.get("record_index", -1),
            "chunk_index": chunk.get("chunk_index", -1),
            "word_count": chunk.get("word_count", -1),
        }

        metadatas.append(clean_metadata(metadata))

    print("Creating embeddings...")
    embeddings = model.encode(texts, show_progress_bar=True).tolist()

    CHROMA_DIR.mkdir(parents=True, exist_ok=True)

    client = chromadb.PersistentClient(path=str(CHROMA_DIR))

    # Delete old collection if it exists.
    # This prevents duplicate ID errors when you rerun the script.
    try:
        client.delete_collection(COLLECTION_NAME)
        print(f"Deleted old collection: {COLLECTION_NAME}")
    except Exception:
        pass

    collection = client.create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"}
    )

    print("Adding chunks to ChromaDB...")

    collection.add(
        ids=ids,
        documents=texts,
        embeddings=embeddings,
        metadatas=metadatas,
    )

    print(f"Saved {collection.count()} chunks to ChromaDB collection: {COLLECTION_NAME}")

    return collection, model


def get_collection():
    """
    Load the existing ChromaDB collection.
    """
    client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    return client.get_collection(name=COLLECTION_NAME)


def retrieve(query, top_k=TOP_K):
    """
    Retrieve top-k chunks for a query.
    Returns documents, metadata, IDs, and distance scores.
    """
    model = SentenceTransformer(EMBEDDING_MODEL_NAME)
    collection = get_collection()

    query_embedding = model.encode([query]).tolist()

    results = collection.query(
        query_embeddings=query_embedding,
        n_results=top_k,
        include=["documents", "metadatas", "distances"],
    )

    retrieved = []

    for i in range(len(results["ids"][0])):
        retrieved.append({
            "id": results["ids"][0][i],
            "text": results["documents"][0][i],
            "metadata": results["metadatas"][0][i],
            "distance": results["distances"][0][i],
        })

    return retrieved


def print_retrieval_results(query, results):
    """
    Print retrieval results in a readable format.
    """
    print("\n" + "=" * 80)
    print(f"QUERY: {query}")
    print("=" * 80)

    for i, item in enumerate(results, start=1):
        metadata = item["metadata"]

        print(f"\n--- Result {i} ---")
        print(f"Distance: {item['distance']:.4f}")
        print(f"ID: {item['id']}")
        print(f"Professor: {metadata.get('professor')}")
        print(f"Source type: {metadata.get('source_type')}")
        print(f"Source: {metadata.get('source')}")
        print()
        print(item["text"])
        print("-" * 80)


def run_test_queries():
    """
    Test at least 3 retrieval queries before moving to Milestone 5.
    """
    test_queries = [
        "What do students say about Peter Sadowski's teaching style?",
        "According to student reviews, what is the workload like in Carleton Moore's class?",
        "Do students say Henri Casanova's course is more focused on exams, projects, homework, or quizzes?",
        "What are Jason Leigh's research interests, and what do students say about their classroom experience?",
        "What do students say about Haopeng Zhang's teaching style and workload?",
    ]

    for query in test_queries:
        results = retrieve(query, top_k=TOP_K)
        print_retrieval_results(query, results)


def main():
    build_vector_store()
    run_test_queries()


if __name__ == "__main__":
    main()
