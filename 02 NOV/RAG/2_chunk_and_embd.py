
from rag_core import make_chunks, read_documents, TOKENIZER

documents = read_documents()

total_chunks = 0

for document in documents:

    filename = document["source"]
    text = document["text"]

    chunks = make_chunks(text, chunk_size=120, overlap=20)

    total_chunks += len(chunks)
    print("DOCUMENT:", filename)
    print("CHUNK COUNT:", len(chunks))

    # Print one sample chunk
    if chunks:
        sample = chunks[0]

        print("\nSAMPLE CHUNK:")
        print(sample)

        print("\nSAMPLE TOKEN COUNT:", len(TOKENIZER.encode(sample)))

print("TOTAL CHUNKS FROM BOTH DOCUMENTS:", total_chunks)
