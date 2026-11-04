
from pathlib import Path

from haystack import Document, Pipeline
from haystack.components.preprocessors import DocumentSplitter
from haystack.components.retrievers.in_memory import InMemoryEmbeddingRetriever
from haystack.components.writers import DocumentWriter
from haystack.document_stores.in_memory import InMemoryDocumentStore

from haystack_integrations.components.embedders.sentence_transformers import (
    SentenceTransformersDocumentEmbedder,
    SentenceTransformersTextEmbedder,
)


# STEP 1: PROJECT CONFIGURATION

PROJECT_ROOT = Path(__file__).resolve().parent
DOCUMENTS_PATH = PROJECT_ROOT / "Documents"

COLLECTION = "museum_haystack"

MODEL = "sentence-transformers/all-MiniLM-L6-v2"


# STEP 2: READ BOTH TXT FILES

documents = []

txt_files = list(DOCUMENTS_PATH.glob("*.txt"))

if len(txt_files) != 2:
    raise SystemExit(
        f"Expected 2 TXT files, found {len(txt_files)}"
    )

for file_path in txt_files:

    text = file_path.read_text(encoding="utf-8").strip()

    if not text:
        print("Skipping empty file:", file_path.name)
        continue

    document = Document(
        content=text,
        meta={"source": file_path.name}
    )

    documents.append(document)

if not documents:
    raise SystemExit("No document content found.")

print("Documents loaded:", len(documents))


# STEP 3: CREATE IN-MEMORY DOCUMENT STORE

store = InMemoryDocumentStore(
    embedding_similarity_function="cosine"
)


# STEP 4: CREATE INDEXING PIPELINE

indexing = Pipeline()

indexing.add_component(
    "splitter",
    DocumentSplitter(
        split_by="word",
        split_length=120,
        split_overlap=20
    )
)

indexing.add_component(
    "embedder",
    SentenceTransformersDocumentEmbedder(
        model=MODEL
    )
)

indexing.add_component(
    "writer",
    DocumentWriter(
        document_store=store
    )
)

indexing.connect(
    "splitter.documents",
    "embedder.documents"
)

indexing.connect(
    "embedder.documents",
    "writer.documents"
)


# STEP 5: RUN INDEXING PIPELINE

indexing.run({
    "splitter": {
        "documents": documents
    }
})

print("Stored chunks:", store.count_documents())


# STEP 6: CREATE QUERY PIPELINE

search = Pipeline()

search.add_component(
    "query_embedder",
    SentenceTransformersTextEmbedder(
        model=MODEL
    )
)

search.add_component(
    "retriever",
    InMemoryEmbeddingRetriever(
        document_store=store,
        top_k=3
    )
)

search.connect(
    "query_embedder.embedding",
    "retriever.query_embedding"
)


# STEP 7: ASK QUESTIONS

while True:

    question = input(
        "\nQuestion (exit to stop): "
    ).strip()

    if question.lower() == "exit":
        print("Exiting Haystack application...")
        break

    if not question:
        continue

    result = search.run({
        "query_embedder": {
            "text": question
        }
    })

    chunks = result["retriever"]["documents"]

    if not chunks:
        print("No matching documents found.")
        continue

    for i, chunk in enumerate(chunks, start=1):

        print("\n" + "=" * 50)
        print("Result:", i)
        print("Source:", chunk.meta.get("source"))
        print("Similarity:", chunk.score)
        print("Text:", chunk.content)
