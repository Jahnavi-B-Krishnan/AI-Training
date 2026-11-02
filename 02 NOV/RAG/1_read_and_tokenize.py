"""STEP 1 — Read the source document (no AI required)."""
from rag_core import DOCUMENT_PATHS, read_documents, TOKENIZER

text = read_documents()
print("DOCUMENT:", DOCUMENT_PATHS)
print("Characters:", len(text))
print(text)

for file_path in DOCUMENT_PATHS:
    filename = file_path.name
    txt = file_path.read_text(encoding="utf-8")
    ids = TOKENIZER.encode(txt)
    print("Tokens:", len(ids))



