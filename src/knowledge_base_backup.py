from pathlib import Path
import csv
import re

from pypdf import PdfReader


BASE_DIR = Path(__file__).resolve().parent.parent
DOCS_DIR = BASE_DIR / "data" / "product_docs"


def extract_pdf(path):
    reader = PdfReader(str(path))
    return "\n".join(
        (page.extract_text() or "")
        for page in reader.pages
    )


def load_documents():
    documents = []

    for path in sorted(DOCS_DIR.iterdir()):

        if path.suffix.lower() == ".pdf":
            text = extract_pdf(path)

        elif path.suffix.lower() in {".json", ".txt"}:
            text = path.read_text(errors="ignore")

        elif path.suffix.lower() == ".csv":
            with open(path, newline="", encoding="utf-8") as f:
                rows = list(csv.reader(f))

            text = "\n".join(
                ", ".join(row)
                for row in rows
            )

        else:
            continue

        documents.append({
            "source": path.name,
            "text": text.strip()
        })

    return documents


def chunk_text(text, chunk_size=1200, overlap=200):

    text = re.sub(r"\s+", " ", text).strip()

    chunks = []

    start = 0

    while start < len(text):

        end = min(start + chunk_size, len(text))

        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        if end >= len(text):
            break

        start = end - overlap

    return chunks


def build_knowledge_base():

    documents = load_documents()

    chunks = []

    for document in documents:

        for chunk in chunk_text(document["text"]):

            chunks.append({
                "source": document["source"],
                "text": chunk
            })

    return chunks


def search_documents(question, top_k=3):

    chunks = build_knowledge_base()

    q = question.lower()

    keyword_groups = {

        "shipping": [
            "shipping",
            "delivery",
            "express",
            "standard delivery",
            "tracking",
            "package",
            "delayed",
        ],

        "returns": [
            "return",
            "refund",
            "return window",
            "eligible",
            "final sale",
        ],

        "warranty": [
            "warranty",
            "warranty period",
            "covered",
            "coverage",
        ],

        "loyalty": [
            "loyalty",
            "points",
            "redeem",
            "rewards",
            "voucher",
        ],

        "sizing": [
            "size",
            "sizing",
            "denim jacket",
            "chest",
            "waist",
        ],

        "promotions": [
            "promotion",
            "promotional",
            "discount",
            "offer",
            "seasonal",
            "clearance",
        ],

        "support": [
            "support",
            "contact",
            "complaint",
            "escalation",
        ],

        "stationery": [
            "stationery",
            "bulk order",
        ],
    }

    source_mapping = {

        "shipping": "shipping.json",
        "returns": "returns.pdf",
        "warranty": "warranty.pdf",
        "loyalty": "loyalty.json",
        "sizing": "sizing.txt",
        "promotions": "promotions.pdf",
        "support": "support.pdf",
        "stationery": "stationery-faq.csv",
    }

    detected_topics = []

    for topic, keywords in keyword_groups.items():

        if any(keyword in q for keyword in keywords):
            detected_topics.append(topic)

    question_words = set(
        re.findall(r"[a-zA-Z0-9]+", q)
    )

    results = []

    for chunk in chunks:

        text = chunk["text"].lower()
        source = chunk["source"].lower()

        score = 0

        # Strong source match
        for topic in detected_topics:

            if source_mapping.get(topic) == source:
                score += 20

        # Topic keyword match
        for topic in detected_topics:

            for keyword in keyword_groups[topic]:

                if keyword in text:
                    score += 3

        # General word match
        for word in question_words:

            if len(word) > 3 and word in text:
                score += 1

        if score > 0:

            results.append({
                "source": chunk["source"],
                "score": score,
                "text": chunk["text"],
            })

    results.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return results[:top_k]


if __name__ == "__main__":

    documents = load_documents()

    print("=" * 70)
    print("NORTHSTAR KNOWLEDGE BASE")
    print("=" * 70)

    print("\nDocuments loaded:", len(documents))

    chunks = build_knowledge_base()

    print("Chunks created:", len(chunks))

    question = "How long does express delivery take?"

    print("\n========== SEARCH TEST ==========")
    print("Question:", question)

    results = search_documents(question)

    for i, result in enumerate(results, 1):

        print(f"\n--- RESULT {i} ---")
        print("Source:", result["source"])
        print("Score:", result["score"])
        print("Text:")
        print(result["text"])
