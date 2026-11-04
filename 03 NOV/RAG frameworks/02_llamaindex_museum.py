
from pathlib import Path

import chromadb
from llama_index.core import (
    Document,
    SimpleDirectoryReader,
    StorageContext,
    VectorStoreIndex,
)
from pathlib import Path

from llama_index.core.node_parser import SentenceSplitter
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.vector_stores.chroma import ChromaVectorStore


PROJECT_ROOT = Path(__file__).resolve().parent
DOCUMENTS_PATH = PROJECT_ROOT / "Documents"
DATABASE_PATH = PROJECT_ROOT / "chroma_db"
COLLECTION_NAME = "llamaindex_museum"

if not DOCUMENTS_PATH.exists():
    raise SystemExit(f"Document not found: {DOCUMENTS_PATH}")


# STEP 1: READ DOCUMENT

documents = []

txt_files = list(DOCUMENTS_PATH.glob("*.txt"))

#print("TXT files found:", len(txt_files))

for file_path in txt_files:

    text = file_path.read_text(encoding="utf-8").strip()

    #print("Reading:", file_path.name)
    #print("Characters:", len(text))

    if not text:
        print("WARNING: Empty file:", file_path.name)
        continue

    document = Document(
        text=text,
        metadata={"source": file_path.name}
    )

    documents.append(document)

if not documents:
    raise SystemExit("No document content found.")

#print("Documents loaded:", len(documents))


# STEP 2: CREATE NODES

splitter = SentenceSplitter(
    chunk_size=150,
    chunk_overlap=20
)

nodes = splitter.get_nodes_from_documents(documents)

print("Total nodes:", len(nodes))

for i, node in enumerate(nodes, start=1):
    print("\nNode:", i)
    print("Text:", node.get_content()[:300])


# STEP 3: LOCAL EMBEDDING MODEL
embedding_model = HuggingFaceEmbedding(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

print("Embedding dimensions:",
      len(embedding_model.get_text_embedding("annual leave")))


# STEP 4: CONNECT TO CHROMADB
DATABASE_PATH.mkdir(exist_ok=True)

client = chromadb.PersistentClient(path=str(DATABASE_PATH))

# Rebuild only the LlamaIndex collection on each execution.
existing_names = [c.name for c in client.list_collections()]

if COLLECTION_NAME in existing_names:
    client.delete_collection(COLLECTION_NAME)

collection = client.get_or_create_collection(COLLECTION_NAME)

vector_store = ChromaVectorStore(
    chroma_collection=collection
)

storage = StorageContext.from_defaults(
    vector_store=vector_store
)

# STEP 5: CREATE VECTOR INDEX
index = VectorStoreIndex(
    nodes,
    storage_context=storage,
    embed_model=embedding_model
)

print("Stored nodes:", collection.count())


# STEP 6: SEMANTIC SEARCH
retriever = index.as_retriever(similarity_top_k=3)

while True:
    question = input("\nQuestion (exit to stop): ").strip()

    if question.lower() == "exit":
        break

    if not question:
        continue

    results = retriever.retrieve(question)

    for i, result in enumerate(results, start=1):
        print("\n" + "=" * 60)
        print("Result:", i)
        print("Node ID:", result.node.node_id)
        print("Relevance score:", result.score)
        print("Text:", result.node.get_content())
