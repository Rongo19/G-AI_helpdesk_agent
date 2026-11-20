
from pathlib import Path
import hashlib

from langchain_core.documents import Document
from langchain_chroma import Chroma

from app.rag.embeddings import get_embeddings


# Project paths
BASE_DIR = Path(__file__).resolve().parents[2]

CHROMA_DIR = BASE_DIR / "chroma_db"

COLLECTION_NAME = "hr_it_policies"


def generate_document_ids(
    documents: list[Document]
) -> list[str]:
    """
    Generate deterministic IDs for document chunks.
    """

    ids = []

    for document in documents:

        unique_content = (
            f"{document.metadata.get('source', '')}"
            f"{document.metadata.get('page', '')}"
            f"{document.metadata.get('chunk_index', '')}"
            f"{document.page_content}"
        )

        document_id = hashlib.sha256(
            unique_content.encode("utf-8")
        ).hexdigest()

        ids.append(document_id)

    return ids


def create_vector_store(
    chunks: list[Document]
) -> Chroma:
    """
    Generate embeddings and store document chunks
    in a persistent ChromaDB collection.
    """

    if not chunks:
        raise ValueError("No document chunks provided.")

    # Initialize embedding model
    embeddings = get_embeddings()

    # Create persistent ChromaDB directory
    CHROMA_DIR.mkdir(parents=True, exist_ok=True)

    # Initialize ChromaDB
    vector_store = Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=embeddings,
        persist_directory=str(CHROMA_DIR),
        collection_metadata={
            "hnsw:space": "cosine"
        }
    )

    # Generate stable IDs
    document_ids = generate_document_ids(chunks)

    # Store documents and their embeddings
    vector_store.add_documents(
        documents=chunks,
        ids=document_ids
    )

    print("\nVector storage completed successfully!")

    print(f"Collection: {COLLECTION_NAME}")
    print(f"Stored chunks: {len(chunks)}")
    print(f"Storage location: {CHROMA_DIR}")

    return vector_store
