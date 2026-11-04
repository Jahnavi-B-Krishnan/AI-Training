
from pathlib import Path

import chromadb

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings


# STEP 1: PROJECT CONFIGURATION

PROJECT_ROOT = Path(__file__).resolve().parent
DOCUMENTS_PATH = PROJECT_ROOT / "Documents"
DB_PATH = PROJECT_ROOT / "chroma_db"

COLLECTION = "museum_langchain"


# STEP 2: READ BOTH TXT FILES

documents = []

txt_files = list(DOCUMENTS_PATH.glob("*.txt"))


for file_path in txt_files:

    text = file_path.read_text(encoding="utf-8")

    document = Document(
        page_content=text,
        metadata={"source": file_path.name}
    )

    documents.append(document)


# STEP 3: SPLIT INTO CHUNKS

splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
    encoding_name="cl100k_base",
    chunk_size=150,
    chunk_overlap=20
)

chunks = splitter.split_documents(documents)

for i, chunk in enumerate(chunks, start=1):
    chunk.metadata["chunk_id"] = f"museum_{i:03d}"

print("Total chunks:", len(chunks))

if not chunks:
    raise SystemExit("No chunks generated.")

print("Sample chunk:", chunks[0].page_content[:200])


# STEP 4: GENERATE LOCAL EMBEDDINGS

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

print("Local embedding model loaded.")


# STEP 5: STORE CHUNKS IN CHROMADB

client = chromadb.PersistentClient(
    path=str(DB_PATH)
)

if COLLECTION in [c.name for c in client.list_collections()]:
    client.delete_collection(COLLECTION)

store = Chroma.from_documents(
    documents=chunks,
    embedding=embedding_model,
    collection_name=COLLECTION,
    persist_directory=str(DB_PATH),
    collection_metadata={"hnsw:space": "cosine"}
)

print("Stored chunks:", client.get_collection(COLLECTION).count())


# STEP 6: QUESTION AND RETRIEVAL

while True:

    question = input(
        "\nEnter your question (exit to stop): "
    ).strip()

    if question.lower() == "exit":
        break

    if not question:
        continue

    results = store.similarity_search_with_score(
        question,
        k=2
    )

    print("\n" + "=" * 60)
    print("TOP 2 MATCHING CHUNKS")
    print("=" * 60)

    for i, (document, distance) in enumerate(results, start=1):

        print("\nResult:", i)
        print("Chunk ID:", document.metadata["chunk_id"])
        print("Source file:", document.metadata["source"])
        print("Distance:", round(distance, 4))
        print("Content:", document.page_content)

