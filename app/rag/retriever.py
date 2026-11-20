
from langchain_core.documents import Document

from app.rag.embeddings import get_embeddings
from app.rag.vector_store import (
    CHROMA_DIR,
    COLLECTION_NAME
)
from langchain_chroma import Chroma


def get_vector_store() -> Chroma:
    """
    Connect to the existing persistent ChromaDB collection.
    """

    if not CHROMA_DIR.exists():
        raise FileNotFoundError(
            "ChromaDB not found. Run the ingestion pipeline first."
        )

    embeddings = get_embeddings()

    vector_store = Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=embeddings,
        persist_directory=str(CHROMA_DIR),
        collection_metadata={
            "hnsw:space": "cosine"
        }
    )

    if vector_store._collection.count() == 0:
        raise ValueError(
            "ChromaDB collection is empty. Build the vector store first."
        )

    return vector_store


def retrieve_documents(
    query: str,
    k: int = 4,
    category: str | None = None
) -> list[tuple[Document, float]]:
    """
    Retrieve relevant policy chunks from ChromaDB.

    Args:
        query: User's question.
        k: Number of chunks to retrieve.
        category: Optional HR or IT metadata filter.

    Returns:
        List of documents with their vector distances.
    """

    if not query.strip():
        raise ValueError("Search query cannot be empty.")

    if k < 1:
        raise ValueError("k must be at least 1.")

    if category is not None:
        category = category.upper()

        if category not in {"HR", "IT"}:
            raise ValueError("Category must be HR or IT.")

    vector_store = get_vector_store()

    search_filter = (
        {"category": category}
        if category
        else None
    )

    results = vector_store.similarity_search_with_score(
        query=query,
        k=k,
        filter=search_filter
    )

    return results


def display_results(
    results: list[tuple[Document, float]]
) -> None:
    """
    Display retrieved chunks with source information.
    """

    if not results:
        print("No relevant documents found.")
        return

    print("\n" + "=" * 60)
    print("RETRIEVAL RESULTS")
    print("=" * 60)

    for index, (document, distance) in enumerate(results, start=1):

        metadata = document.metadata

        print(f"\nRESULT {index}")
        print("-" * 40)

        print("Content:")
        print(document.page_content)

        print("\nSource:", metadata.get("source", "Unknown"))
        print("Category:", metadata.get("category", "Unknown"))

        if "page" in metadata:
            print("Page:", metadata["page"])

        print(f"Cosine distance: {distance:.4f}")


def format_retrieved_context(
    results: list[tuple[Document, float]]
) -> str:

    if not results:
        return ""

    context_parts = []

    for index, (document, distance) in enumerate(
        results, start=1
    ):

        metadata = document.metadata

        source = metadata.get("source", "Unknown")
        category = metadata.get("category", "Unknown")
        page = metadata.get("page")

        source_reference = source

        if page is not None:
            source_reference += f", page {page + 1}"

        context_parts.append(
            f"""
Source [{index}]: {source_reference}
Category: {category}

Content:
{document.page_content}
"""
        )

    return "\n".join(context_parts)