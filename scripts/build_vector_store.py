
from app.rag.ingestion import ingest_documents
from app.rag.vector_store import create_vector_store


def main():

    print("=" * 60)
    print("GOAIFIED HR/IT - RAG INGESTION PIPELINE")
    print("=" * 60)

    # Step 1: Load and split documents
    print("\n[1] Loading and chunking documents...")

    chunks = ingest_documents()

    # Step 2: Generate embeddings and store vectors
    print("\n[2] Generating embeddings and storing vectors...")

    vector_store = create_vector_store(chunks)

    # Step 3: Verify stored records
    print("\n[3] Verifying ChromaDB storage...")

    stored_records = vector_store.get()

    print(
        f"Total records in collection: "
        f"{len(stored_records['ids'])}"
    )

    print("\nRAG ingestion pipeline completed!")


if __name__ == "__main__":
    main()
