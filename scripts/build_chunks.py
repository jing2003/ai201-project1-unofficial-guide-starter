from pathlib import Path
import json
import random
import re


DATA_DIR = Path("data/raw")
OUTPUT_DIR = Path("data/processed")
OUTPUT_FILE = OUTPUT_DIR / "chunks.json"

CHUNK_SIZE = 450
OVERLAP = 50


def clean_text(text):
    """
    Light cleanup because the files are already manually cleaned.
    """
    text = text.replace("\r\n", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def get_source_type(text, file_path):
    """
    Get source type from the file content first.
    If missing, infer it from the filename.
    """
    match = re.search(r"Source type:\s*(.+)", text, re.IGNORECASE)

    if match:
        return match.group(1).strip()

    filename = file_path.name.lower()

    if "official" in filename or "faculty" in filename:
        return "official_faculty"

    if "review" in filename:
        return "student_review"

    return "unknown"


def get_professor_name(text, file_path):
    """
    Extract professor name from a chunk or document.
    If missing, fall back to the filename.
    """
    match = re.search(r"Professor:\s*(.+)", text)

    if match:
        return match.group(1).strip()

    name = file_path.stem
    name = name.replace("review_", "")
    name = name.replace("official_", "")
    name = name.replace("_", " ").replace("-", " ")

    return name.title()


def count_words(text):
    return len(text.split())


def split_long_text(text, chunk_size=CHUNK_SIZE, overlap=OVERLAP):
    """
    Split only if a record is too long.
    Most student reviews and faculty entries should stay together.
    """
    words = text.split()

    if len(words) <= chunk_size:
        return [text]

    chunks = []
    start = 0

    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end]).strip()

        if chunk:
            chunks.append(chunk)

        start += chunk_size - overlap

    return chunks


def split_official_faculty_entries(text):
    """
    Split one official faculty file into one chunk per professor.

    Expected format:
    Source type: official_faculty

    Professor: Kyungim Baek
    Title: ...
    Research interests: ...

    Professor: Mahdi Belcaid
    Title: ...
    Research interests: ...
    """
    source_match = re.search(r"Source type:\s*(.+)", text, re.IGNORECASE)
    source_type_line = source_match.group(0).strip() if source_match else "Source type: official_faculty"

    # Split whenever a new professor entry begins.
    entries = re.split(r"\n(?=Professor:\s*)", text)

    cleaned_entries = []

    for entry in entries:
        entry = entry.strip()

        if not entry:
            continue

        # Skip the first piece if it only contains Source type and no professor.
        if "Professor:" not in entry:
            continue

        # Make sure every entry contains the source type.
        if "Source type:" not in entry:
            entry = f"{source_type_line}\n\n{entry}"

        cleaned_entries.append(entry)

    return cleaned_entries


def split_student_reviews(text):
    """
    Split one professor review file into one chunk per review.
    Each review chunk also keeps the professor/header summary.

    Expected format:
    Source type: student_review

    Professor: Kyungim Baek
    Department: Computer Science
    Overall rating summary: ...

    Review 1:
    Course: ...
    Review text: ...

    Review 2:
    Course: ...
    Review text: ...
    """
    review_start = re.search(r"\nReview\s+\d+:", text)

    # If no Review 1/2/3 labels exist, keep the whole file as one document.
    if not review_start:
        return [text]

    header = text[:review_start.start()].strip()
    reviews_text = text[review_start.start():].strip()

    review_blocks = re.split(r"\n(?=Review\s+\d+:)", reviews_text)

    chunks = []

    for review in review_blocks:
        review = review.strip()

        if not review:
            continue

        chunk = f"{header}\n\n{review}".strip()
        chunks.append(chunk)

    return chunks


def load_documents():
    """
    Load every .txt file from the data folder.
    """
    documents = []

    txt_files = sorted(DATA_DIR.glob("*.txt"))

    for file_path in txt_files:
        text = file_path.read_text(encoding="utf-8")
        text = clean_text(text)

        if not text:
            print(f"Skipping empty file: {file_path}")
            continue

        source_type = get_source_type(text, file_path)

        documents.append({
            "source": str(file_path),
            "source_type": source_type,
            "text": text,
        })

    return documents


def build_chunks(documents):
    """
    Build final chunks with metadata.
    """
    final_chunks = []

    for doc in documents:
        source = doc["source"]
        source_type = doc["source_type"]
        text = doc["text"]
        file_path = Path(source)

        if source_type == "official_faculty":
            records = split_official_faculty_entries(text)
        elif source_type == "student_review":
            records = split_student_reviews(text)
        else:
            records = [text]

        for record_index, record in enumerate(records):
            smaller_chunks = split_long_text(record)

            for sub_index, chunk_text in enumerate(smaller_chunks):
                professor = get_professor_name(chunk_text, file_path)

                chunk_id = f"{file_path.stem}_record_{record_index}_chunk_{sub_index}"

                final_chunks.append({
                    "id": chunk_id,
                    "text": chunk_text,
                    "source": source,
                    "source_type": source_type,
                    "professor": professor,
                    "record_index": record_index,
                    "chunk_index": sub_index,
                    "word_count": count_words(chunk_text),
                })

    return final_chunks


def save_chunks(chunks):
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    with OUTPUT_FILE.open("w", encoding="utf-8") as f:
        json.dump(chunks, f, indent=2, ensure_ascii=False)


def print_summary(chunks):
    print("\n==============================")
    print("Chunking Summary")
    print("==============================")
    print(f"Total chunks: {len(chunks)}")

    by_source_type = {}

    for chunk in chunks:
        source_type = chunk["source_type"]
        by_source_type[source_type] = by_source_type.get(source_type, 0) + 1

    for source_type, count in by_source_type.items():
        print(f"{source_type}: {count}")

    print("==============================\n")


def inspect_random_chunks(chunks, count=5):
    """
    Print 5 random chunks for manual inspection.
    """
    if not chunks:
        print("No chunks to inspect.")
        return

    sample = random.sample(chunks, min(count, len(chunks)))

    print("\n==============================")
    print(f"Random {len(sample)} Chunk Inspection")
    print("==============================\n")

    for chunk in sample:
        print("----- CHUNK -----")
        print(f"ID: {chunk['id']}")
        print(f"Professor: {chunk['professor']}")
        print(f"Source type: {chunk['source_type']}")
        print(f"Source: {chunk['source']}")
        print(f"Word count: {chunk['word_count']}")
        print()
        print(chunk["text"])
        print("-----------------\n")


def main():
    documents = load_documents()

    print(f"Loaded {len(documents)} document files.")

    if not documents:
        print("No .txt files found. Put your cleaned .txt files inside the data/ folder.")
        return

    chunks = build_chunks(documents)

    # Remove accidental empty chunks
    chunks = [chunk for chunk in chunks if chunk["text"].strip()]

    save_chunks(chunks)
    print_summary(chunks)
    inspect_random_chunks(chunks, count=5)

    print(f"Saved chunks to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
